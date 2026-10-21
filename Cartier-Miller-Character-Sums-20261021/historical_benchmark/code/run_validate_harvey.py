"""Validation of the Harvey-kernel BGS adapter (runs under the passagemath interpreter).

python run_validate_harvey.py --mode development|confirmation --seed S --out FILE [--refs FILE]
Small/medium p: compared with the supplied direct enumeration (handover reference, pure Python,
imported by path).  Large p: compared with reference residues produced by the system-Python
methods (file --refs, JSON list of [p, f, a, value, source]).
"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cmbench import core, cases
from cmbench.harvey import BGSHarvey

ap = argparse.ArgumentParser()
ap.add_argument('--mode', required=True)
ap.add_argument('--seed', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--refs')
ap.add_argument('--comparators', default=os.environ.get('CM_HANDOVER_COMPARATORS'))
a = ap.parse_args()
sys.path.insert(0, a.comparators)
import reference_comparators as R

rng = cases.rng_for(a.seed, a.mode + '-harvey')
counts, failures = {}, []


def ok(k, c, d=None):
    counts[k] = counts.get(k, 0) + 1
    if not c:
        failures.append({'check': k, 'detail': d})


t0 = time.time()
if a.mode == 'development':
    primes = [q for q in range(7, 140) if core.is_prime_small(q)] + [211, 257, 331, 499, 1009, 2003, 4001, 8009, 16411, 65537]
else:
    dev = set([q for q in range(7, 140) if core.is_prime_small(q)] + [211, 257, 331, 499, 1009, 2003, 4001, 8009, 16411, 65537])
    primes = sorted(set(cases.random_prime(rng, 140, 70000, dev | cases.INHERITED_PRIMES) for _ in range(24)))
for p in primes:
    for d in (3, 4):
        for kind in ('generic', 'zero_const'):
            f = cases.random_curve(rng, p, d, kind)
            eps, fib, inv = R.character_tables(f, p)
            A = list(range(p)) if p < 120 else sorted(set([0] + rng.sample(range(p), 16)))
            for x in A:
                try:
                    v = BGSHarvey.query((p, f), x)
                except Exception as e:
                    v = 'EXC ' + repr(e)
                ok('H.harvey_vs_direct.%s' % ('branch' if eps[x] == 0 else 'nonbranch'), v == R.direct_single(eps, inv, x, p), (p, f, x, v))
            cval, Hval = BGSHarvey.query_with_H((p, f), A[-1])
            ok('H.harvey_query_with_H.value', cval == R.direct_single(eps, inv, A[-1], p))
            ok('H.harvey_query_with_H.sum_eps', cases.sum_eps_from_H(p, f, Hval) == sum(eps) % p)
if a.refs:
    for p, f, x, val, src in json.load(open(a.refs)):
        v = BGSHarvey.query((p, f), x)
        ok('H.harvey_vs_refs.%s' % src, v == val, (p, f, x, v, val))
res = {'mode': a.mode, 'seed': a.seed, 'primes': primes, 'counts': counts, 'total_checks': sum(counts.values()),
       'n_failures': len(failures), 'failures': failures[:100], 'status': 'PASS' if not failures else 'FAIL',
       'elapsed_s': round(time.time() - t0, 1), 'python': sys.version}
json.dump(res, open(a.out, 'w'), indent=1, default=str)
print({k: res[k] for k in ('mode', 'status', 'total_checks', 'n_failures', 'elapsed_s')})
