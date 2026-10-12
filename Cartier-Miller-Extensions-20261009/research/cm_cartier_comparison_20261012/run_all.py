"""Rerun every theory and validation script and write SHA256SUMS.json."""
import hashlib, json, os, subprocess, sys, time
ROOT = os.path.dirname(os.path.abspath(__file__))
steps = [
    ['theory/symbolic_velu_check.py', 'results/symbolic_velu_check.json'],
    ['theory/family_loops.py', 'results/family_loops.json'],
    ['theory/cm_tables.py', 'results/cm_tables.json'],
    ['theory/seedfree_deg5_D16.py', 'results/seedfree_deg5_D16.json'],
    ['theory/collision_resultants.py'],
    ['theory/bos_masser_check.py'],
    ['theory/char_p_exactness_demo.py'],
    ['theory/period_check.py'],
    ['theory/quasiperiod_isogeny_check.py'],
    ['theory/katz_zannier_check.py'],
    ['theory/order_argument.py'],
    ['validation/validate_d7.py'],
    ['validation/validate_fixed_D.py'],
]
log = []
for st in steps:
    t = time.time()
    r = subprocess.run([sys.executable] + [os.path.join(ROOT, st[0])] + [os.path.join(ROOT, a) for a in st[1:]],
                       capture_output=True, text=True, cwd=ROOT)
    tail = r.stdout.strip().splitlines()[-1:] if r.stdout.strip() else []
    log.append({'script': st[0], 'returncode': r.returncode, 'seconds': round(time.time() - t, 1), 'last_line': tail})
    print(st[0], 'rc=', r.returncode, round(time.time() - t, 1), 's', tail)
    if r.returncode:
        print(r.stderr[-2000:])
json.dump(log, open(os.path.join(ROOT, 'results', 'run_all_log.json'), 'w'), indent=1)
sums = {}
for dp, dn, fn in os.walk(ROOT):
    if '__pycache__' in dp:
        continue
    for f in sorted(fn):
        if f == 'SHA256SUMS.json':
            continue
        path = os.path.join(dp, f)
        sums[os.path.relpath(path, ROOT)] = hashlib.sha256(open(path, 'rb').read()).hexdigest()
json.dump(dict(sorted(sums.items())), open(os.path.join(ROOT, 'SHA256SUMS.json'), 'w'), indent=1)
ok = all(x['returncode'] == 0 for x in log)
print('all steps ok' if ok else 'SOME STEP FAILED')
sys.exit(0 if ok else 1)
