"""Reference residues for the Harvey-kernel check at medium/large p (system Python).
Each reference requires agreement of cmcs_frozen (PARI trace) and bgs07 (this package)."""
import argparse, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cmbench import cases, core, methods as M
ap = argparse.ArgumentParser()
ap.add_argument('--seed', required=True); ap.add_argument('--label', required=True); ap.add_argument('--out', required=True)
ap.add_argument('--sizes', default='100000,1000000,10000000,1000000000,10000000000')
a = ap.parse_args()
rng = cases.rng_for(a.seed, a.label + '-refs')
dev = set([10 ** 5 + 3, 10 ** 6 + 3, 10 ** 7 + 19, 10 ** 9 + 7])
refs = []
for lo in [int(x) for x in a.sizes.split(',')]:
    for d in (3, 4):
        p = (lo + 3 if a.label == 'development' and lo + 3 in dev else
             cases.random_prime(rng, lo, 2 * lo, cases.INHERITED_PRIMES | (dev if a.label != 'development' else set())))
        f = cases.random_curve(rng, p, d)
        E = M.CmcsFrozen.prepare(p, f)
        for _ in range(2):
            x = cases.random_pole(rng, p, f)
            v1, v2 = E.single_pole(x), M.BGS07.cold(p, f, x)
            if v1 != v2:
                raise SystemExit('reference disagreement %r' % ((p, f, x, v1, v2),))
            refs.append([p, f, x, v1, 'cmcs+bgs07'])
json.dump(refs, open(a.out, 'w'))
print(len(refs), 'references')
