"""Post-hoc internal-consistency check for the W4 groups in which only Cartier-Miller ran (62 bits).

validate_outputs.py labels these 54 outputs 'single_family_unchecked' (the two timed methods, the shared
adapter and the inherited weighted_sum API, agree but belong to one family).  This script applies the
'internal' policy of validate_outputs.py to every pole of every weighted sum, outside all timers:
the frozen oracle with translation parameter a1 and the corrected variant's endpoint-checked oracle
(cmcs_v2 V2-2) with a different parameter a2 must agree; the weighted sum is then rebuilt with the
exact O(s^2) correction and must equal both recorded outputs.  Same-family check only.

python3 -I validate_w4_internal.py RESULTS_BENCH_DIR
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cmbench import core, cases, methods as M  # noqa: E402
from cmbench.cmcs_v2 import make_curve2_class  # noqa: E402

rdir = sys.argv[1]
Curve2 = make_curve2_class()
pools = json.load(open(os.path.join(rdir, 'cases_regenerated.json')))
report = {'policy': 'internal consistency only (one family): two translation parameters, endpoint test, '
                    'exact correction; compared with both recorded W4 outputs', 'groups': []}
bad = 0
for gid in ('b62_d3_s1-256', 'b62_d4_s1-256'):
    spec = pools['W4:' + gid]
    recs = {}
    for m in ('cmcs_frozen', 'cmcs_frozen+weighted_sum'):
        fn = os.path.join(rdir, 'outputs', 'W4__%s__%s.json' % (gid, m))
        recs[m] = json.load(open(fn))['outputs']
    n_items = n_poles = 0
    agree = 0
    for b, blk in enumerate(spec['blocks'][1:]):
        p, f = blk['p'], blk['f']
        tr = M.TraceProvider.trace(p, f)
        E = Curve2(p, f, trace=tr)
        se = (1 - E.n_inf - tr) % p
        for j, inst in enumerate(blk['sums']):
            U, v, bb = inst['poles'], inst['weights'], inst['b']
            a1 = E.choose_translation(set(U))
            a2 = next(x for x in range(a1 + 1, a1 + 400) if x not in set(U) and core.peval(f, x, p))
            single, eps = {}, {}
            for a in U:
                c1, e1 = E.oracle(a, a1)[:2]
                c2, e2 = E.oracle_checked(a, a2)[:2]
                if c1 != c2 or e1 != e2:
                    bad += 1
                single[a], eps[a] = c1, e1
                n_poles += 1
            val, _ = cases.weighted_from_scalars(single, eps, U, v, bb, se, p)
            ok = all(recs[m][b][j] == val for m in recs)
            agree += ok
            bad += (not ok)
            n_items += 1
    report['groups'].append({'group': gid, 'items': n_items, 'poles_checked': n_poles, 'items_agreeing': agree})
    print(gid, n_items, n_poles, agree, flush=True)
report['mismatches'] = bad
json.dump(report, open(os.path.join(rdir, 'w4_internal_check.json'), 'w'), indent=1)
print('mismatches', bad)
