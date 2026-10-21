"""Verify this folder and rerun its portable correctness checks (repository entry point).

    python verify.py          integrity, frozen confirmations, table, freezes, example
    python verify.py --full   also repeats the development selections

Standard library only; no timing campaign runs. Calculations that write results
use temporary directories, so recorded evidence is never overwritten. Files kept
in the data asset (DATA_ASSET.json) are checked when they have been extracted
here, and reported otherwise. tools/verify_supplement.py is the handover's own
verifier and needs the complete supplement archive, including the manuscript
snapshot that the repository does not redistribute.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
INTEGRATION = ROOT.parent/'Cartier-Miller-Integration-20261013'
RENAMED = {'README.md': 'handover/SUPPLEMENT_README.md'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args, cwd, as_json=True):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    out = subprocess.run([sys.executable, '-B']+args, cwd=cwd, env=env,
                         capture_output=True, text=True)
    if out.returncode:
        raise AssertionError('command failed: %s\n%s' % (' '.join(args), out.stderr[-2000:]))
    return json.loads(out.stdout) if as_json else out.stdout.strip()


def integrity():
    sums = json.loads((ROOT/'SHA256SUMS.json').read_text())
    bad = [n for n, h in sums.items() if not (ROOT/n).is_file() or sha(ROOT/n) != h]
    assert not bad, ('changed or missing', bad)
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    asset = json.loads((ROOT/'DATA_ASSET.json').read_text())
    held, withheld = asset['files'], asset['not_redistributed']['files']
    tally = {'in_tree': 0, 'asset_present': 0, 'asset_not_extracted': 0, 'not_redistributed': 0}
    for name, digest in manifest.items():
        if name in withheld:
            assert withheld[name] == digest
            tally['not_redistributed'] += 1
            continue
        path = ROOT/RENAMED.get(name, name)
        if name in held:
            assert held[name] == digest
            if path.is_file():
                assert sha(path) == digest, name
                tally['asset_present'] += 1
            else:
                tally['asset_not_extracted'] += 1
            continue
        assert path.is_file() and sha(path) == digest, ('supplement file differs', name)
        assert RENAMED.get(name, name) in sums, name
        tally['in_tree'] += 1
    return {'sha256sums_files': len(sums), 'supplement_manifest_files': len(manifest), **tally}


def frozen_uniform(modes):
    out = {}
    with tempfile.TemporaryDirectory(prefix='cm-uniform-') as tmp:
        for name in ('cm_character_route.py', 'uniform_order.py', 'verify_uniform_order.py', 'FREEZE.json'):
            shutil.copy2(ROOT/'src'/name, Path(tmp)/name)
        for mode in modes:
            got = run(['verify_uniform_order.py', mode], tmp)
            want = json.loads((ROOT/'verification/uniform_order'/(mode+'.json')).read_text())
            assert got == want, ('uniform-order record differs', mode)
            out[mode] = {k: got[k] for k in ('models', 'direct_values') if k in got}
    return out


def frozen_adapter(modes):
    out = {}
    for mode in modes:
        got = run([str(ROOT/'tests/verify_weighted_adapter.py'), '--mode', mode], ROOT)
        want = json.loads((ROOT/'verification/adapter'/(mode+'.json')).read_text())
        assert got == want, ('adapter record differs', mode)
        out[mode] = {k: got[k] for k in ('weighted_queries', 'output_residue_comparisons',
                                          'invalid_inputs_rejected')}
    return out


def benchmark_freeze():
    code = ROOT/'historical_benchmark/code'
    if (code/'cmbench/native/libcmnative.so').is_file():
        line = run(['verify_freeze.py'], code, as_json=False)
        assert line.startswith('FREEZE OK'), line
        return line
    record = json.loads((code/'FREEZE.json').read_text())
    missing = [n for n in record['files'] if not (code/n).is_file()]
    assert missing == ['cmbench/native/libcmnative.so'], missing
    bad = [n for n, h in record['files'].items() if n not in missing and sha(code/n) != h]
    assert not bad, bad
    return ('%d of %d frozen files match; libcmnative.so is in the data asset, so the '
            'digest %s is checked only after extraction' % (len(record['files'])-1,
                                                            len(record['files']), record['digest']))


def main(full):
    modes = ('development', 'confirmation') if full else ('confirmation',)
    result = {'integrity': integrity(),
              'frozen_uniform_order': frozen_uniform(modes),
              'frozen_weighted_adapter': frozen_adapter(modes),
              'benchmark_table': run([str(ROOT/'tools/recompute_benchmark_table.py')], ROOT),
              'benchmark_code_freeze': benchmark_freeze(),
              'inherited_application_freeze':
                  run(['src/verify_freeze.py'], ROOT/'historical_benchmark/inherited/character_sums'),
              'example': run([str(ROOT/'examples/weighted_sum_example.py')], ROOT, as_json=False)}
    assert result['inherited_application_freeze']['status'] == 'MATCH'
    if (INTEGRATION/'validate_character_sums.py').is_file():
        z = run(['validate_character_sums.py'], INTEGRATION)
        assert z['status'] == 'PASS'
        result['adapted_cm_system_service'] = {k: z[k] for k in (
            'status', 'adapted_files_import_only', 'weighted_comparisons',
            'single_pole_comparisons', 'frozen_adapted_single_pole_matches')}
    return {'status': 'PASS', 'full': full, **result}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action='store_true')
    print(json.dumps(main(parser.parse_args().full), indent=2))
