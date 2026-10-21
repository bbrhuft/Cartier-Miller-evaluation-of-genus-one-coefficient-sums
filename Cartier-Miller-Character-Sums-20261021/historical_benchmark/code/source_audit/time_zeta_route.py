"""Post-freeze exploratory timing (separately labelled; not part of the frozen benchmark):
prepared-query cost of the general-trace route (A7'') versus the frozen candidate on the same curves,
trace supplied to both (W2-style, Q = 64 distinct poles per curve, 5 fresh curves per class).
Outputs are compared exactly; timings are perf_counter_ns medians per query."""
import json, os, statistics, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
from cmbench import cases, core, methods as M
import voloch_zeta_route as VZ

rng = cases.rng_for('post-freeze-zeta-timing', 'v1')
out = {'note': 'post-freeze exploratory timing; trace supplied to both methods', 'rows': []}
for bits in (20, 30, 40, 50, 62):
    for d in (3, 4):
        per = {'cmcs_frozen': [], 'voloch_zeta_route': []}
        mismatch = 0
        for blk in range(5):
            p = cases.random_prime(rng, 1 << (bits - 1), 1 << bits)
            f = cases.random_curve(rng, p, d)
            tau = M.TraceProvider.trace(p, f)
            A = [cases.random_pole(rng, p, f) for _ in range(64)]
            E = M.CmcsFrozen.prepare(p, f, trace=tau)
            E.single_pole(A[0]); VZ.value(p, f, A[0], tau)          # warm-up
            t0 = time.perf_counter_ns(); r1 = [E.single_pole(a) for a in A]; t1 = time.perf_counter_ns()
            r2 = [VZ.value(p, f, a, tau) for a in A]; t2 = time.perf_counter_ns()
            per['cmcs_frozen'].append((t1 - t0) / 64e9)
            per['voloch_zeta_route'].append((t2 - t1) / 64e9)
            mismatch += sum(x != y for x, y in zip(r1, r2))
        out['rows'].append({'bits': bits, 'd': d, 'mismatches': mismatch,
                            **{k + '_median_s_per_query': statistics.median(v) for k, v in per.items()},
                            **{k + '_blocks_s_per_query': v for k, v in per.items()}})
        print(bits, d, mismatch, {k: '%.3g' % statistics.median(v) for k, v in per.items()}, flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
