"""Bounded failure injection for the pilot: wrong mathematics and missing dependencies
must both produce a nonzero exit, and run_all.py must propagate them.

Each trial copies the pilot into a temporary directory, applies one deliberate change,
runs the affected script, and requires the expected nonzero return code.  Dependency
paths are passed explicitly (same options as run_all.py).
"""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import okp_config  # noqa: E402

TRIALS = [
    # (script, anchor, replacement, expected rc, needs deps)
    ('padic_canonical_subgroup.py', "'kappa_C': (sigma / p).residue(1)",
     "'kappa_C': ((sigma / p).residue(1) + 1) % p", 1, True),
    ('padic_canonical_subgroup.py', "require(kappa_identity_only(A, B, p, 3) == kappa",
     "require(kappa_identity_only(A, B, p, 3) == (kappa + 1) % p", 1, True),
    ('charp_identities.py', 'kV = (-sV * pow(t * t, -1, p)) % p', 'kV = (sV * pow(t * t, -1, p)) % p', 1, False),
    ('serre_derivative_check.py', '(6 * B * HA - 4 * i3 * A * A * HB) % p == beta',
     '(6 * B * HA + 4 * i3 * A * A * HB) % p == beta', 1, False),
    ('retained_dependency_check.py', "['beta_multiplier'] == 44 == kap", "['beta_multiplier'] == 45 == kap", 1, True),
    ('kummer_degree_check.py', 'kprime = k // 2 if k % 2 == 0 else k', 'kprime = k', 1, False),
]


CLEAN_ENV = {k: v for k, v in os.environ.items() if k not in okp_config.ENV.values()}


def run(cmd, env=None):
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def main():
    args, deps = okp_config.parse('pilot failure injection')
    dep_args = sum(([f'--{k}', v] for k, v in deps['paths'].items()), [])
    results = []
    for script, old, new, want, needs in TRIALS:
        with tempfile.TemporaryDirectory() as td:
            dst = Path(td) / 'pilot'
            shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns('results', '__pycache__'))
            src = (dst / script).read_text()
            if src.count(old) != 1:
                print('INJECTION_ANCHOR_NOT_UNIQUE', script, old)
                sys.exit(1)
            (dst / script).write_text(src.replace(old, new))
            proc = run([sys.executable, '-I', str(dst / script)] + (dep_args if needs else []))
            runner = run([sys.executable, '-I', str(dst / 'run_all.py')] + dep_args)
            caught = proc.returncode == want and 'FAIL' in proc.stdout
            results.append({'trial': f'{script}: {new[:60]}', 'rc': proc.returncode, 'caught': caught,
                            'runner_rc': runner.returncode})
            print(f'{script}: injected -> rc={proc.returncode} caught={caught}; runner rc={runner.returncode}', flush=True)
    # missing dependency must not be skipped silently
    for script in ('padic_canonical_subgroup.py', 'retained_dependency_check.py', 'coverage.py', 'run_all.py'):
        proc = run([sys.executable, '-I', str(HERE / script)], env=CLEAN_ENV)  # no paths, dependency env vars removed
        results.append({'trial': f'{script}: no dependency configuration', 'rc': proc.returncode,
                        'caught': proc.returncode != 0, 'runner_rc': None})
        print(f'{script}: no dependencies -> rc={proc.returncode}', flush=True)
    # explicitly allowed missing dependencies -> REDUCED, still nonzero for the pilot and the runner
    with tempfile.TemporaryDirectory() as td:  # run in a copy so the real results are not overwritten
        dst = Path(td) / 'pilot'
        shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns('results', '__pycache__'))
        proc = run([sys.executable, '-I', str(dst / 'padic_canonical_subgroup.py'), '--allow-missing-dependencies'],
                   env=CLEAN_ENV)
    results.append({'trial': 'padic with --allow-missing-dependencies', 'rc': proc.returncode,
                    'caught': proc.returncode == 3 and 'REDUCED_SCOPE' in proc.stdout, 'runner_rc': None})
    print(f'padic --allow-missing-dependencies -> rc={proc.returncode}', flush=True)
    ok = all(r['caught'] and (r['runner_rc'] is None or r['runner_rc'] != 0) for r in results)
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results' / 'failure_injection.json').write_text(json.dumps(results, indent=2))
    if not ok:
        print('FAILURE_INJECTION_NOT_DETECTED')
        sys.exit(1)
    print('FAILURE_INJECTION_DETECTED_ALL')


if __name__ == '__main__':
    main()
