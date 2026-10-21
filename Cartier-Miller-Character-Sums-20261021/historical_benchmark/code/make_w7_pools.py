"""Exceptional-trace (tau = +-1) benchmark pools for W7 from CM constructions (class number one,
D = 5 mod 8, not only j = 0): cubic models scrambled by x -> alpha x + beta, quartic models by a
Moebius change.  Poles a satisfy chi(f(a)) = tau.  Each pool entry: [p, f, a, tau]."""
import hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cmbench import cases, core, methods as M
FREEZE = json.load(open(os.path.join(HERE, 'FREEZE.json')))
SEED = hashlib.sha256((FREEZE['digest'] + '|benchmark').encode()).hexdigest()
out = sys.argv[1]
pari = M.TraceProvider.pari()
pools = {}
CM = [(D, j) for D, j in cases.CM_DATA]
for bits in (24, 32, 40, 48, 56, 62):
    for d in (3, 4):
        gid = 'b%02d_d%d_exc' % (bits, d)
        r = cases.rng_for(SEED, 'W7|' + gid)
        pool = []
        k = 0
        while len(pool) < 3 + 9 * 20:
            D, j = CM[k % len(CM)]
            want = 1 if k % 2 == 0 else -1
            k += 1
            p, f0 = cases.cm_trace_pm1_curve(r, bits, D, j, want, pari)
            f = cases.scramble_cubic(r, p, f0)
            if d == 4:
                f = cases.cubic_to_quartic(r, p, f)
            tr = M.TraceProvider.trace(p, f)
            assert tr == want
            for _ in range(200):
                a = r.randrange(p)
                if core.legendre(core.peval(f, a, p), p) == tr:
                    pool.append([p, f, a, tr])
                    break
        pools[gid] = {'pilot': pool[:3], 'pool': pool[3:], 'bits': bits, 'd': d,
                      'construction': 'CM D in %s, alternating tau = +1/-1' % [x[0] for x in CM]}
json.dump(pools, open(out, 'w'))
print('pools', {g: len(v['pool']) for g, v in pools.items()})
