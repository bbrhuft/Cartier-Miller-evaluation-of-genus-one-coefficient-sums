"""Run every pilot check with explicit dependencies and failure propagation.

Usage:
    python -I run_all.py --retained <research tree> --extension <CM extension source> --handover <handover root>
(or set RETAINED_RESEARCH, CM_EXTENSION_SOURCE, HANDOVER_ROOT).  A step passes only if it
exits 0 AND prints its PASS sentinel.  A missing dependency (exit 2), a reduced scope
(exit 3) or a mathematical failure (exit 1) makes this runner exit 1.  The report
results/RUN_REPORT.json lists every step, its scope arguments, return code and duration.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import okp_config  # noqa: E402
from okp_common import environment  # noqa: E402

STEPS = [('charp_identities.py', 'CHARP_IDENTITIES_PASS', False),
         ('serre_derivative_check.py', 'SERRE_DERIVATIVE_PASS', False),
         ('kummer_degree_check.py', 'KUMMER_DEGREE_PASS', False),
         ('padic_canonical_subgroup.py', 'PADIC_PILOT_PASS', True),
         ('retained_dependency_check.py', 'RETAINED_DEPENDENCY_PASS', True),
         ('coverage.py', 'COVERAGE_DONE', True)]


def main():
    args, deps = okp_config.parse('pilot runner')
    dep_args = []
    for key in ('retained', 'extension', 'handover'):
        if key in deps['paths']:
            dep_args += [f'--{key}', deps['paths'][key]]
    if args.allow_missing_dependencies:
        dep_args.append('--allow-missing-dependencies')
    (HERE / 'results').mkdir(exist_ok=True)
    log, ok = [], True
    for script, sentinel, needs in STEPS:
        cmd = [sys.executable, '-I', str(HERE / script)] + (dep_args if needs else [])
        t0 = time.time()
        proc = subprocess.run(cmd, capture_output=True, text=True)
        passed = proc.returncode == 0 and sentinel in proc.stdout
        ok &= passed
        log.append({'script': script, 'command': [Path(c).name if i == 2 else c for i, c in enumerate(cmd)],
                    'returncode': proc.returncode, 'sentinel': sentinel, 'sentinel_seen': sentinel in proc.stdout,
                    'passed': passed, 'seconds': round(time.time() - t0, 2),
                    'stdout_tail': proc.stdout[-2000:], 'stderr_tail': proc.stderr[-2000:]})
        print(f'{script}: {"PASS" if passed else "FAIL"} (rc={proc.returncode})', flush=True)
    files = sorted(p for p in HERE.rglob('*') if p.is_file() and p.suffix in ('.py', '.csv', '.json')
                   and p.name not in ('RUN_REPORT.json',) and '__pycache__' not in p.parts)
    report = {'overall': 'PASS' if ok else 'FAIL', 'dependencies': deps, 'steps': log,
              'environment': environment(),
              'sha256': {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (HERE / 'results' / 'RUN_REPORT.json').write_text(json.dumps(report, indent=2))
    if not ok:
        print('RUN_ALL_FAIL')
        sys.exit(1)
    print('ALL_PASS')


if __name__ == '__main__':
    main()
