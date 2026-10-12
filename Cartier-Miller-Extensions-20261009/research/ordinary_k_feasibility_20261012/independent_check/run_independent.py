"""Runner for the repaired independent checks.

    python -I run_independent.py --profile full|bounded --targets <ordinary_targets.csv> [--out DIR]

Every step is listed in RUN_REPORT.json with its arguments (scope), return code, the
status/check/failure counts read back from the driver's own JSON, and its duration.
The runner exits 1 if any step returns nonzero, fails to write its JSON, reports a
status other than PASS, or executes zero checks.  A missing target CSV is an error (2),
never a skip.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent

PROFILES = {
    'full': [  # the scope of the original independent pass (12 October 2026)
        ('c1_cech.py', ['--primes', '7', '11', '13', '17', '19', '23', '--sample-primes', '29', '31', '37', '41',
                        '--sample-size', '30', '--seed', '1'], 'c1_cech'),
        *[('c1_kedlaya.py', ['--p', str(p), '--N', '2'], f'c1_kedlaya_p{p}_N2') for p in (7, 11, 13, 17, 19, 23)],
        *[('c1_kedlaya.py', ['--p', str(p), '--N', '2', '--sample', '25'], f'c1_kedlaya_p{p}_N2_s25') for p in (29, 31, 37)],
        ('c1_kedlaya.py', ['--p', '7', '--N', '3'], 'c1_kedlaya_p7_N3'),
        ('c1_extra.py', [], 'c1_extra'),
        ('c2_formal.py', ['--p', '7', '--lifts', '3'], 'c2_formal_p7'),
        ('c2_formal.py', ['--p', '11', '--lifts', '2'], 'c2_formal_p11'),
        ('c2_formal.py', ['--p', '13', '--lifts', '2'], 'c2_formal_p13'),
        ('c2_formal.py', ['--p', '17', '--models', '30', '--lifts', '2'], 'c2_formal_p17'),
        ('c2_formal.py', ['--p', '19', '--models', '15', '--lifts', '2'], 'c2_formal_p19'),
        ('c2_formal.py', ['--p', '23', '--models', '15', '--lifts', '2'], 'c2_formal_p23'),
        ('c3_etale.py', [], 'c3_etale'),
        ('c4_c5.py', [], 'c4_c5'),
        ('l3_katz_signs.py', [], 'l3_katz_signs'),
    ],
    'bounded': [
        ('c1_cech.py', ['--primes', '7', '11'], 'c1_cech'),
        ('c1_kedlaya.py', ['--p', '7', '--N', '2'], 'c1_kedlaya_p7_N2'),
        ('c1_extra.py', ['--lift-primes', '7', '--rank-primes', '7', '11', '--skip-p5-informational'], 'c1_extra'),
        ('c2_formal.py', ['--p', '7', '--models', '6', '--lifts', '1'], 'c2_formal_p7'),
        ('c3_etale.py', ['--primes', '7', '11'], 'c3_etale'),
        ('c4_c5.py', ['--c4-max', '13', '--c5-max', '13'], 'c4_c5'),
        ('l3_katz_signs.py', ['--primes', '7', '11'], 'l3_katz_signs'),
    ],
}
NEEDS_TARGETS = {'c2_formal.py', 'c3_etale.py'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--profile', choices=sorted(PROFILES), default='bounded')
    ap.add_argument('--targets', default=os.environ.get('ORDK_TARGETS'))
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    if not a.targets or not Path(a.targets).is_file():
        print(f'DEPENDENCY_MISSING: ordinary_targets.csv not found ({a.targets!r})')
        sys.exit(2)
    targets = str(Path(a.targets).resolve())
    out = Path(a.out) if a.out else HERE / f'results_{a.profile}'
    out.mkdir(parents=True, exist_ok=True)
    steps, ok = [], True
    for script, args, result_name in PROFILES[a.profile]:
        cmd = [sys.executable, '-I', str(HERE / script), '--out', str(out)] + args
        if script in NEEDS_TARGETS:
            cmd += ['--targets', targets]
        res_file = out / f'{result_name}.json'
        if res_file.exists():
            res_file.unlink()
        t0 = time.time()
        proc = subprocess.run(cmd, capture_output=True, text=True)
        rec = {'script': script, 'args': args, 'returncode': proc.returncode, 'seconds': round(time.time() - t0, 2),
               'result_file': res_file.name, 'stdout_tail': proc.stdout[-1500:], 'stderr_tail': proc.stderr[-1500:]}
        if res_file.is_file():
            r = json.loads(res_file.read_text())
            rec.update({'executed': True, 'status': r['status'], 'checks': r['checks'], 'failures': r['failures'],
                        'groups': r['groups'], 'scope': r['scope'], 'driver_exit_code': r['exit_code']})
        else:
            rec.update({'executed': False, 'status': 'NO_RESULT_FILE', 'checks': 0, 'failures': None})
        passed = (proc.returncode == 0 and rec['executed'] and rec['status'] == 'PASS'
                  and rec['checks'] > 0 and rec.get('driver_exit_code') == 0)
        rec['passed'] = passed
        ok &= passed
        steps.append(rec)
        print(f"{result_name}: {'PASS' if passed else 'FAIL'} rc={proc.returncode} checks={rec['checks']} "
              f"failures={rec['failures']} ({rec['seconds']} s)", flush=True)
    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*.py'))}
    report = {'profile': a.profile, 'overall': 'PASS' if ok else 'FAIL', 'targets': targets,
              'targets_sha256': hashlib.sha256(Path(targets).read_bytes()).hexdigest(),
              'steps': steps, 'total_checks': sum(s['checks'] or 0 for s in steps),
              'source_sha256': sources, 'python': sys.version, 'platform': platform.platform()}
    (out / 'RUN_REPORT.json').write_text(json.dumps(report, indent=2, default=str))
    if not ok:
        print('INDEPENDENT_RUN_FAIL')
        sys.exit(1)
    print('INDEPENDENT_RUN_PASS')


if __name__ == '__main__':
    main()
