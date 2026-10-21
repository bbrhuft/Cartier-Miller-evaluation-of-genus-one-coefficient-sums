"""Entry point: python3 -I run_validate.py --mode development|confirmation --seed S --out FILE"""
import argparse, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cmbench import validate
ap = argparse.ArgumentParser()
ap.add_argument('--mode', choices=['development', 'confirmation'], required=True)
ap.add_argument('--seed', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()
r = validate.run(a.mode, a.out, a.seed)
print({k: r[k] for k in ('mode', 'status', 'total_checks', 'n_failures', 'elapsed_s')})
for fl in r['failures'][:10]:
    print('FAIL', fl)
