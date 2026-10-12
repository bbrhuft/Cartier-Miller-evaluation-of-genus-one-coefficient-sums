"""Bounded failure injection for the repaired independent checks.

Part A reproduces the reported defect on the PRESERVED ORIGINAL c1_cech.py: with a
deliberately wrong comparator it reports 0 matches and a nonempty failure list yet
exits 0.  Part B applies a wrong comparator (or a broken invariant) to each repaired
driver in a temporary copy and requires exit 1 with a FAIL record.  Part C checks a
missing target CSV (exit 2) and a vacuous run (exit 4).  Part D checks that the
runner propagates an injected failure.  Exit 0 only if every expectation holds.

    python -I inject_failures.py --targets <ordinary_targets.csv> --original <preserved original dir>
"""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PY = sys.executable

TRIALS = [  # (driver, anchor, wrong replacement, bounded args, needs targets)
    ('c1_cech.py', 'good = M == [[0, (-beta) % p], [0, H]]', 'good = M == [[1, (-beta) % p], [0, H]]',
     ['--primes', '7'], False),
    ('c1_cech.py', 'require(r_f != 0,', 'require(r_f == 0,', ['--primes', '7'], False),
    ('c1_kedlaya.py', 'Mp == [[0, (-beta) % p], [0, H]]', 'Mp == [[0, beta % p], [0, H]]', ['--p', '7'], False),
    ('c1_extra.py', 'run.check(hasse_beta(p, A, B) != (0, 0)', 'run.check(hasse_beta(p, A, B) == (0, 0)',
     ['--lift-primes', '7', '--rank-primes', '7', '--skip-p5-informational'], False),
    ('c2_formal.py', '(sc // a.p) % a.p == kap', '(sc // a.p + 1) % a.p == kap', ['--p', '7', '--models', '4', '--lifts', '1'], True),
    ('c3_etale.py', 'pred = (-sV * pow(t * t, -1, p)) % p', 'pred = (sV * pow(t * t, -1, p)) % p', ['--primes', '7'], True),
    ('c4_c5.py', 'if (-s) % p == beta:', 'if s % p == beta:', ['--c4-max', '7', '--c5-max', '7'], False),
    ('c4_c5.py', 'val = (6 * B * dHdA - 4 * inv3 * A * A * dHdB) % p', 'val = (6 * B * dHdA + 4 * inv3 * A * A * dHdB) % p',
     ['--c4-max', '7', '--c5-max', '7'], False),
    ('l3_katz_signs.py', 'av == (-S0) % p', 'av == S0 % p', ['--primes', '7'], False),
]


def copy_tree(dst):
    shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns('results*', '__pycache__'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--targets', default=os.environ.get('ORDK_TARGETS'))
    ap.add_argument('--original', required=True, help='directory holding the preserved original independent check')
    ap.add_argument('--out', default=str(HERE / 'results_injection'))
    a = ap.parse_args()
    if not a.targets or not Path(a.targets).is_file():
        print('DEPENDENCY_MISSING: targets')
        sys.exit(2)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    clean_env = {k: v for k, v in os.environ.items() if k != 'ORDK_TARGETS'}
    results, ok = [], True

    # Part A: the reported defect on the preserved original
    with tempfile.TemporaryDirectory() as td:
        orig = Path(td) / 'orig'
        shutil.copytree(a.original, orig, ignore=shutil.ignore_patterns('*.txt', '*.log', '__pycache__'))
        src = (orig / 'c1_cech.py').read_text()
        anchor = 'if M == [[0, (-beta) % p], [0, H]]:'
        defect = {'part': 'A_original_defect', 'anchor_found': anchor in src}
        if anchor in src:
            # comparator wrong for every model (top-left entry 1), as in the review's demonstration
            (orig / 'c1_cech.py').write_text(src.replace(anchor, 'if M == [[1, (-beta) % p], [0, H]]:'))
            proc = subprocess.run([PY, 'c1_cech.py', '7'], cwd=orig, capture_output=True, text=True)
            line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ''
            defect.update({'returncode': proc.returncode, 'output': line[:300],
                           'reproduced': proc.returncode == 0 and ': 0/42' in line and 'fails=[]' not in line})
        results.append(defect)
        print('A original defect:', defect.get('returncode'), defect.get('reproduced'), flush=True)
        ok &= bool(defect.get('reproduced'))

    # Part B: wrong comparators / invariants in the repaired drivers
    for driver, anchor, wrong, args, needs in TRIALS:
        with tempfile.TemporaryDirectory() as td:
            dst = Path(td) / 'ic'
            copy_tree(dst)
            src = (dst / driver).read_text()
            rec = {'part': 'B_injected_error', 'driver': driver, 'wrong': wrong, 'anchor_unique': src.count(anchor) == 1}
            if src.count(anchor) == 1:
                (dst / driver).write_text(src.replace(anchor, wrong))
                cmd = [PY, '-I', str(dst / driver), '--out', str(dst / 'res')] + args
                if needs:
                    cmd += ['--targets', a.targets]
                proc = subprocess.run(cmd, capture_output=True, text=True)
                rjson = sorted((dst / 'res').glob('*.json'))
                status = json.loads(rjson[0].read_text())['status'] if rjson else None
                rec.update({'returncode': proc.returncode, 'status': status,
                            'detected': proc.returncode == 1 and status == 'FAIL'})
            results.append(rec)
            ok &= bool(rec.get('detected'))
            print(f"B {driver}: rc={rec.get('returncode')} status={rec.get('status')} detected={rec.get('detected')}", flush=True)

    # Part C: missing dependency and vacuous run
    for driver, args in (('c2_formal.py', ['--p', '7']), ('c3_etale.py', ['--primes', '7'])):
        proc = subprocess.run([PY, '-I', str(HERE / driver), '--out', str(out / 'scratch')] + args,
                              capture_output=True, text=True, env=clean_env)
        rec = {'part': 'C_missing_targets', 'driver': driver, 'returncode': proc.returncode,
               'detected': proc.returncode == 2 and 'DEPENDENCY_MISSING' in proc.stdout}
        results.append(rec)
        ok &= rec['detected']
        print(f"C {driver} without targets: rc={proc.returncode}", flush=True)
    proc = subprocess.run([PY, '-I', str(HERE / 'c1_cech.py'), '--out', str(out / 'scratch'), '--primes'],
                          capture_output=True, text=True)
    rec = {'part': 'C_vacuous', 'driver': 'c1_cech.py --primes (empty)', 'returncode': proc.returncode,
           'detected': proc.returncode == 4}
    results.append(rec)
    ok &= rec['detected']
    print(f'C vacuous c1_cech: rc={proc.returncode}', flush=True)

    # Part D: runner propagation
    with tempfile.TemporaryDirectory() as td:
        dst = Path(td) / 'ic'
        copy_tree(dst)
        f = dst / 'c3_etale.py'
        f.write_text(f.read_text().replace('pred = (-sV * pow(t * t, -1, p)) % p', 'pred = (sV * pow(t * t, -1, p)) % p'))
        proc = subprocess.run([PY, '-I', str(dst / 'run_independent.py'), '--profile', 'bounded', '--targets', a.targets,
                               '--out', str(dst / 'rb')], capture_output=True, text=True)
        rec = {'part': 'D_runner_propagation', 'returncode': proc.returncode,
               'detected': proc.returncode == 1 and 'INDEPENDENT_RUN_FAIL' in proc.stdout}
        results.append(rec)
        ok &= rec['detected']
        print(f'D runner with injected c3 error: rc={proc.returncode}', flush=True)
        proc = subprocess.run([PY, '-I', str(dst / 'run_independent.py'), '--profile', 'bounded', '--out', str(dst / 'rb2')],
                              capture_output=True, text=True, env=clean_env)
        rec = {'part': 'D_runner_missing_targets', 'returncode': proc.returncode, 'detected': proc.returncode == 2}
        results.append(rec)
        ok &= rec['detected']
        print(f'D runner without targets: rc={proc.returncode}', flush=True)

    (out / 'INJECTION_REPORT.json').write_text(json.dumps({'all_detected': ok, 'trials': results}, indent=2))
    if not ok:
        print('INJECTION_NOT_ALL_DETECTED')
        sys.exit(1)
    print('INJECTION_ALL_DETECTED')


if __name__ == '__main__':
    main()
