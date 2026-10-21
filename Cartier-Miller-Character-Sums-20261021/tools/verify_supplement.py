"""Check package hashes and rerun portable correctness checks in temporary paths.

Run from any directory. --full additionally repeats development selections.
No trace backend, compiler or optional benchmark dependency is needed.
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

ROOT = Path(__file__).resolve().parents[1]


def execute(args, cwd, json_output=True):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    result = subprocess.run([sys.executable]+args, cwd=cwd, env=env,
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout) if json_output else result.stdout.strip()


def main(full):
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    for name, expected in manifest.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, name
    results = {'manifest_files': len(manifest)}
    with tempfile.TemporaryDirectory(prefix='cm-character-sums-') as folder:
        target = Path(folder)
        for name in ('cm_character_route.py', 'uniform_order.py', 'verify_uniform_order.py', 'FREEZE.json'):
            shutil.copy2(ROOT/'src'/name, target/name)
        for mode in (('development', 'confirmation') if full else ('confirmation',)):
            actual = execute(['verify_uniform_order.py', mode], target)
            expected = json.loads((ROOT/'verification/uniform_order'/(mode+'.json')).read_text())
            assert actual == expected, ('uniform result differs', mode)
            results['uniform_'+mode] = actual
        for mode in (('development', 'confirmation') if full else ('confirmation',)):
            actual = execute([str(ROOT/'tests/verify_weighted_adapter.py'), '--mode', mode], ROOT)
            expected = json.loads((ROOT/'verification/adapter'/(mode+'.json')).read_text())
            assert actual == expected, ('weighted adapter result differs', mode)
            results['adapter_'+mode] = actual
    results['benchmark_table'] = execute([str(ROOT/'tools/recompute_benchmark_table.py')], ROOT)
    results['benchmark_freeze'] = execute(['verify_freeze.py'], ROOT/'historical_benchmark/code', False)
    assert results['benchmark_freeze'].startswith('FREEZE OK')
    results['inherited_freeze'] = execute(['src/verify_freeze.py'], ROOT/'historical_benchmark/inherited/character_sums')
    assert results['inherited_freeze']['status'] == 'MATCH'
    results['example'] = execute([str(ROOT/'examples/weighted_sum_example.py')], ROOT, False)
    return {'status': 'PASS', 'full': full, **results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    print(json.dumps(main(args.full), indent=2))
