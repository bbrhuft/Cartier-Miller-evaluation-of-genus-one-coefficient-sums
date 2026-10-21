"""Correctness checks for the character-sum service added on 21 October 2026.

Exercises the adapted package imports (cm_system.character_sums and
cm_system.backends.character_sums) against an independent enumeration, and
against the byte-identical frozen supplement sources in
../Cartier-Miller-Character-Sums-20261021/src. No timing is measured.

    python validate_character_sums.py [--output PATH]
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from cm_system import character_sums as S                    # noqa: E402
from cm_system.api import ResourceLimit, Unsupported, Budget  # noqa: E402
from cm_system.backends.cm.d7_seed import is_prime64          # noqa: E402
from cm_system.backends import character_sums as adapted      # noqa: E402
from cm_system.backends.character_sums import uniform_order as adapted_uniform  # noqa: E402

FROZEN = ROOT.parent/'Cartier-Miller-Character-Sums-20261021'/'src'
ADAPTED = ROOT/'cm_system'/'backends'/'character_sums'
IMPORT_EDITS = {
    'uniform_order.py': [('import cm_character_route as C\n', 'from . import cm_character_route as C\n')],
    'weighted_sums.py': [('import cm_character_route as arithmetic\nimport uniform_order\n',
                          'from . import cm_character_route as arithmetic\nfrom . import uniform_order\n')],
    'cm_character_route.py': [],
}


def load_frozen():
    """Import the three frozen modules under private names, without touching sys.path."""
    mods = {}
    for name in ('cm_character_route', 'uniform_order', 'weighted_sums'):
        spec = importlib.util.spec_from_file_location(name, FROZEN/(name+'.py'))
        mod = importlib.util.module_from_spec(spec)
        saved = {k: sys.modules.get(k) for k in mods}
        sys.modules.update(mods)          # resolve the frozen flat imports to frozen modules
        try:
            spec.loader.exec_module(mod)
        finally:
            for k, v in saved.items():
                if v is None:
                    sys.modules.pop(k, None)
                else:
                    sys.modules[k] = v
        mods[name] = mod
    return mods


def check_provenance(count):
    prov = {x['destination']: x for x in json.loads((ROOT/'PROVENANCE.json').read_text())}
    for name, edits in IMPORT_EDITS.items():
        frozen = (FROZEN/name).read_text()
        for old, new in edits:
            assert frozen.count(old) == 1, name
            frozen = frozen.replace(old, new)
        assert frozen == (ADAPTED/name).read_text(), 'adapted copy differs beyond imports: '+name
        entry = prov['cm_system/backends/character_sums/'+name]
        assert entry['source_sha256'] == hashlib.sha256((FROZEN/name).read_bytes()).hexdigest()
        assert entry['delivered_sha256'] == hashlib.sha256((ADAPTED/name).read_bytes()).hexdigest()
        count['adapted_files_import_only'] += 1


def peval(f, x, p):
    return sum(c*pow(x, k, p) for k, c in enumerate(f)) % p   # deliberately not Horner


def reference(p, f, excluded, residues, constant):
    sq = Counter(y*y % p for y in range(p))
    eps = [sq[peval(f, x, p)]-1 for x in range(p)]
    n_inf = 1 if len(f) == 4 else sq[f[-1] % p]
    trace = 1-n_inf-sum(eps)

    def weight(x):
        return (constant+sum(r*pow((x-a) % p, p-2, p) for a, r in zip(excluded, residues))) % p
    outside = [x for x in range(p) if x not in set(excluded)]
    ch = sum(eps[x]*weight(x) for x in outside) % p
    aff = sum((1+eps[x])*weight(x) for x in outside) % p
    return trace, eps, (ch, aff, (aff+constant*n_inf) % p)


def random_curve(rng, p, degree):
    while True:
        f = [rng.randrange(p) for _ in range(degree)]+[rng.randrange(1, p)]
        try:
            S._coefficients(p, f)
        except ValueError:
            continue
        return f


def check_service(count, rng):
    for p in (47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97):
        for degree in (3, 4):
            for _ in range(4):
                f = random_curve(rng, p, degree)
                trace, eps, _ = reference(p, f, [], [], 0)
                counted = S.CharacterSumSession(p, f)
                supplied = S.CharacterSumSession(p, f, trace=trace)
                assert counted.trace == trace and counted.trusted is False
                assert supplied.trusted is True
                count['models'] += 1
                for a in rng.sample(range(p), 6):
                    if eps[a] == 0:
                        try:
                            counted.single_pole(a)
                        except Unsupported:
                            count['branch_poles_refused'] += 1
                            continue
                        raise AssertionError('branch pole accepted')
                    _, _, (ch, _, _) = reference(p, f, [a], [1], 0)
                    for session, status in ((counted, 'exact'), (supplied, 'conditional_on_trusted_trace')):
                        z = session.single_pole(a)
                        assert z['value'] == ch and z['status'] == status, (p, f, a, z)
                        count['single_pole_comparisons'] += 1
                for scenario in range(6):
                    size = [0, 1, 3, p, rng.randrange(p+1), 5][scenario]
                    excluded = [0] if scenario == 1 else rng.sample(range(p), size)
                    residues = [rng.randrange(p) if eps[a] else 0 for a in excluded]
                    if residues and scenario in (2, 4):
                        residues[0] = 0
                    constant = rng.randrange(p)
                    state = counted.prepare(excluded)
                    for _ in range(2):          # second pass reuses the prepared vectors
                        got = state.evaluate(residues, constant)
                        _, _, want = reference(p, f, excluded, residues, constant)
                        assert (got['character'], got['affine_points'], got['projective_points']) == want
                        count['weighted_comparisons'] += 1
                        count['output_residue_comparisons'] += 3
                        count['empty_affine_domains'] += size == p
                        count['branch_exclusions'] += any(eps[a] == 0 for a in excluded)
                        count['zero_residue_exclusions'] += any(r == 0 for r in residues)
                        residues = [rng.randrange(p) if eps[a] else 0 for a in excluded]
                        constant = -constant
                    branch = [a for a in excluded if eps[a] == 0]
                    if branch:
                        bad = [1 if a == branch[0] else 0 for a in excluded]
                        try:
                            state.evaluate(bad)
                        except Unsupported:
                            count['active_branch_residues_refused'] += 1
                        else:
                            raise AssertionError('active branch residue accepted')


def check_frozen_equivalence(count, rng):
    frozen = load_frozen()
    fw, fu = frozen['weighted_sums'], frozen['uniform_order']
    assert fu.C is frozen['cm_character_route'] and fu is not adapted_uniform
    cases = []
    for p in (5, 7, 11, 13, 101, 103):
        for degree in (3, 4):
            for _ in range(6):
                f = random_curve(rng, p, degree)
                cases.append((p, f, reference(p, f, [], [], 0)[0]))
    # Large supersingular curves with exactly known trace 0 (no point count needed).
    for p in (1000000000000000003, 2305843009213693951, 18446744073709551557):
        assert is_prime64(p)
        if p % 4 == 3:
            cases.append((p, [0, 1, 0, 1], 0))         # y^2=x^3+x
        if p % 3 == 2:
            cases.append((p, [1, 0, 0, 1], 0))         # y^2=x^3+1
    for p, f, trace in cases:
        poles = [rng.randrange(p) for _ in range(8)]
        for a in poles:
            outs = []
            for module in (fw, adapted):
                try:
                    outs.append(('ok', module.single_pole(p, f, a, trace)))
                except ValueError as e:
                    outs.append(('ValueError', str(e)))
            assert outs[0] == outs[1], (p, f, a, outs)
            count['frozen_adapted_single_pole_matches'] += 1
        excluded = sorted(set(poles))
        try:
            g = fw.prepare_weights(p, f, trace, excluded)
        except ValueError:
            continue
        h = adapted.prepare_weights(p, f, trace, excluded)
        assert g.character_basis == h.character_basis and g.affine_basis == h.affine_basis
        assert (g.constant_character, g.constant_affine, g.infinity_count) == \
            (h.constant_character, h.constant_affine, h.infinity_count)
        count['frozen_adapted_prepared_state_matches'] += 1
        if p > 10**6:
            count['large_supersingular_models'] += 1


def check_contract(count):
    f = [1, 1, 0, 1]
    rejects = [
        (lambda: S.CharacterSumSession(9, f), ValueError),               # composite
        (lambda: S.CharacterSumSession(3, f), ValueError),               # below the domain
        (lambda: S.CharacterSumSession(2**64+13, f, trace=0), ValueError),  # beyond 64-bit domain
        (lambda: S.CharacterSumSession(True, f), ValueError),
        (lambda: S.CharacterSumSession(7, [1, True, 0, 1]), ValueError),
        (lambda: S.CharacterSumSession(7, [1, 0, 0, 0, 0, 1]), ValueError),  # degree 5
        (lambda: S.CharacterSumSession(7, [0, 0, 0, 1]), ValueError),        # not squarefree
        (lambda: S.CharacterSumSession(7, f, trace=99), ValueError),         # outside Hasse
        (lambda: S.CharacterSumSession(7, f, trace=1.0), ValueError),
        (lambda: S.CharacterSumSession(7, f, budget=Budget(point_count_prime=5)), ResourceLimit),
        (lambda: S.CharacterSumSession(7, f).prepare([1, 8]), ValueError),   # duplicate mod p
        (lambda: S.CharacterSumSession(7, f).prepare([1]).evaluate([]), ValueError),
        (lambda: S.CharacterSumSession(7, f).prepare([1]).evaluate([1], True), ValueError),
        (lambda: S.CharacterSumSession(7, [0, 1, 0, 1]).single_pole(0), Unsupported),
    ]
    for call, kind in rejects:
        try:
            call()
        except kind:
            count['invalid_or_unsupported_inputs_rejected'] += 1
        else:
            raise AssertionError('accepted: '+str(kind))
    # Documented examples, including the zero-residue extra exclusion and p=5 order 2p.
    s = S.CharacterSumSession(7, f, trace=3)
    assert s.single_pole(1)['value'] == 0
    z = s.prepare([1, 2]).evaluate([1, 0])
    assert (z['character'], z['affine_points'], z['projective_points']) == (6, 5, 5)
    assert S.CharacterSumSession(5, [0, 3, 0, 1], trace=-4).single_pole(1)['value'] == 1
    count['documented_examples'] += 3
    cli = [sys.executable, '-B', '-m', 'cm_system', 'charsum']
    run = lambda args: subprocess.run(cli+args, cwd=ROOT, capture_output=True, text=True)
    ok = run(['7', '1', '1', '0', '1', '--exclude', '1', '2', '--residues', '1', '0'])
    assert ok.returncode == 0 and json.loads(ok.stdout)['character'] == 6
    bad = run(['7', '0', '1', '0', '1', '--pole', '0'])
    assert bad.returncode == 2 and json.loads(bad.stdout)['type'] == 'Unsupported'
    count['cli_checks'] += 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    count = Counter()
    check_provenance(count)
    check_service(count, random.Random(202610210001))
    check_frozen_equivalence(count, random.Random(202610210002))
    check_contract(count)
    out = {'status': 'PASS', 'scope': 'adapted character-sum service; correctness only, no timing',
           'python': sys.version.split()[0], **dict(sorted(count.items()))}
    text = json.dumps(out, indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
