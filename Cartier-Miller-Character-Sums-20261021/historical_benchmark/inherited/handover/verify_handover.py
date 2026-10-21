"""Integrity and bounded correctness checks, not benchmark timings.

Run from anywhere: python verify_handover.py [--with-opus] [--output PATH]
The optional integration route uses direct small-prime traces and a temporary
extraction of the original package. It never edits the original ZIP or sources.
"""
import argparse
import hashlib
import json
import pathlib
import random
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'comparators'))
import reference_comparators as R


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_archive(path, destination):
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            p = pathlib.PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts:
                raise ValueError('unsafe archive member')
        z.extractall(destination)
    return destination / 'Cartier_Miller_Character_Sums_20261020'


def integrity():
    provenance = json.loads((ROOT / 'INPUT_PROVENANCE.json').read_text())
    for record in provenance['inputs']:
        assert sha(ROOT / record['path']) == record['sha256'], record['path']
    manifest = ROOT / 'SHA256SUMS.txt'
    checked = 0
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            digest, name = line.split(maxsplit=1)
            assert sha(ROOT / name) == digest, name
            checked += 1
    with zipfile.ZipFile(ROOT / 'inherited/Opus_Character_Sums_20261020.zip') as z:
        prefix = 'Cartier_Miller_Character_Sums_20261020/'
        archive_checks = 0
        for line in z.read(prefix + 'SHA256SUMS.txt').decode().splitlines():
            digest, name = line.split(maxsplit=1)
            name = pathlib.PurePosixPath(name).as_posix()
            assert hashlib.sha256(z.read(prefix + name)).hexdigest() == digest, name
            archive_checks += 1
        freeze = json.loads(z.read(prefix + 'FREEZE.json'))
        for name, digest in freeze['files'].items():
            assert hashlib.sha256(z.read(prefix + name)).hexdigest() == digest, name
        lines = ''.join('%s  %s\n' % (freeze['files'][k], k)
                        for k in sorted(freeze['files']))
        assert hashlib.sha256(lines.encode()).hexdigest() == freeze['digest']
    return {'handover_manifest_entries': checked, 'inherited_manifest_entries': archive_checks,
            'inherited_frozen_files': len(freeze['files']), 'freeze_digest': freeze['digest']}


def validate(cmcs=None):
    rng = random.Random(2026102023)
    result = {'models': 0, 'single_pole_cases': 0, 'branch_cases': 0,
              'zero_pole_cases': 0, 'weighted_character_checks': 0,
              'weighted_affine_checks': 0, 'miller_nonbranch_checks': 0,
              'prepared_branch_checks': 0, 'integration_weighted_checks': 0}
    for p in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 101):
        for d in (3, 4):
            for sample in range(4):
                while True:
                    f = [rng.randrange(p) for _ in range(d)] + [rng.randrange(1, p)]
                    if sample == 0:
                        f[0] = 0
                    if sample == 1:
                        f[0] = 1
                    if R.squarefree(f, p):
                        break
                epsilon, fibres, inverses = R.character_tables(f, p)
                coefficients = R.polynomial_power(f, (p - 1) // 2, p)
                n_inf = 1 if d == 3 else (0 if pow(f[-1], (p - 1) // 2, p) == p - 1 else 2)
                trace = 1 - n_inf - sum(epsilon)
                curve = cmcs.Curve(p, f, trace=trace) if cmcs else None
                if curve is not None:
                    curve.prepare_second_kind()
                single = {}
                result['models'] += 1
                for a in range(p):
                    expected = R.direct_single(epsilon, inverses, a, p)
                    assert R.reverse_coefficient_sum(f, a, p) == expected, (p, f, a, 'recurrence')
                    assert R.full_power_sum(coefficients, a, p) == expected, (p, f, a, 'full_power')
                    single[a] = expected
                    result['single_pole_cases'] += 1
                    result['branch_cases'] += epsilon[a] == 0
                    result['zero_pole_cases'] += a == 0
                    if curve is not None:
                        assert curve.single_pole(a) == expected, (p, f, a, 'candidate')
                        key = 'miller_nonbranch_checks' if epsilon[a] else 'prepared_branch_checks'
                        result[key] += 1
                for s in (1, min(3, p), min(5, p)):
                    poles = sorted(rng.sample(range(p), s))
                    weights = [rng.randrange(p) for _ in poles]
                    weights[-1] = 0   # an extra omitted point remains in the domain contract
                    constant = rng.randrange(p)
                    char, baseline = R.common_domain_from_scalars(
                        single, epsilon, poles, weights, constant, p)
                    assert char == R.direct_weighted(epsilon, inverses, poles, weights, constant, p)
                    affine = R.direct_weighted(fibres, inverses, poles, weights, constant, p)
                    assert (char + baseline) % p == affine
                    result['weighted_character_checks'] += 1
                    result['weighted_affine_checks'] += 1
                    if curve is not None:
                        terms = list(zip(poles, weights))
                        assert curve.weighted_sum(simple=terms, b=constant)[0] == char
                        assert curve.weighted_sum(simple=terms, b=constant, kind='affine_points')[0] == affine
                        result['integration_weighted_checks'] += 2
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--with-opus', action='store_true')
    parser.add_argument('--output', type=pathlib.Path)
    args = parser.parse_args()
    output = {'status': 'PASS', 'scope': 'Bounded correctness/integrity checks, not timing benchmarks',
              'seed': 2026102023, 'python': sys.version, 'integrity': integrity()}
    if args.with_opus:
        with tempfile.TemporaryDirectory(prefix='cm_handover_') as temp:
            package = extract_archive(ROOT / 'inherited/Opus_Character_Sums_20261020.zip', pathlib.Path(temp))
            sys.path.insert(0, str(package / 'src'))
            import cmcs
            output['checks'] = validate(cmcs)
            output['integration'] = 'actual inherited candidate; direct small-prime traces; branch data explicitly prepared'
    else:
        output['checks'] = validate()
        output['integration'] = 'not requested'
    text = json.dumps(output, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + '\n')
    print(text)


if __name__ == '__main__':
    main()
