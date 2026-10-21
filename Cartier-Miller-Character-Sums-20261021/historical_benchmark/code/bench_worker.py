"""Benchmark worker: one method, one job, one fresh interpreter.

python3 -I bench_worker.py JOB.json OUT.json        (system interpreter)
venv_sage/bin/python bench_worker.py JOB.json OUT.json   (method bgs_harvey)

Timing: time.perf_counter_ns around the measured region only.  Imports, interpreter start-up and
PARI library initialisation happen before the first block and are reported separately
('import_ns', 'pari_init_ns'); they are excluded consistently from every algorithm timing.
Outputs of every timed call are returned for exact validation by the driver (outside timers).
Peak RSS: resource.getrusage(RUSAGE_SELF).ru_maxrss (KiB on Linux) after imports and at the end.
"""
import gc
import json
import os
import resource
import sys
import time

T_START = time.perf_counter_ns()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

job = json.load(open(sys.argv[1]))
method = job['method']
if method == 'bgs_harvey':
    from cmbench.harvey import BGSHarvey as CLS
else:
    from cmbench import methods as M
    base = method.split('+')[0].split('[')[0]
    CLS = M.REGISTRY[base]
from cmbench import core, cases
if method != 'bgs_harvey':
    import flint  # noqa: F401  (loaded for every system method, so import costs are comparable)
T_IMPORT = time.perf_counter_ns() - T_START
PARI_INIT = 0
if method != 'bgs_harvey' and job.get('needs_pari'):
    t = time.perf_counter_ns()
    M.TraceProvider.pari()
    PARI_INIT = time.perf_counter_ns() - t
RSS_AFTER_IMPORT = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

batch = '+multipoint' in method
trace_supplied = '[trace supplied]' in method
second_kind = '[second-kind prepared]' in method


def prep(p, f, trace):
    if trace_supplied:
        return CLS.prepare(p, f, trace=trace)
    return CLS.prepare(p, f)


def eps_of(f, a, p):
    return core.legendre(core.peval(f, a, p), p)


def sum_eps_of(st, p, f, first_pole):
    """Each method's own route to sum_x chi(f(x)) mod p; returns (sum_eps, extra_single_or_None)."""
    if hasattr(CLS, 'sum_eps'):
        return CLS.sum_eps(st), None
    c, H = CLS.query_with_H(st, first_pole)
    return cases.sum_eps_from_H(p, f, H), c


samples, outputs, status = [], [], 'ok'
WARM_NS = None
if job.get('warmup'):
    tw = time.perf_counter_ns()
    try:
        wp, wf, wa = job['warmup'][:3]
        if method.startswith('voloch_semaev'):
            CLS.value(wp, wf, wa)
        elif job['workload'] == 'TRACE':
            M.TraceProvider.trace(wp, wf)
        else:
            _st = CLS.prepare(wp, wf, trace=job['warmup'][3]) if (trace_supplied or len(job['warmup']) > 3) and hasattr(CLS, 'prepare') and method.startswith('cmcs') else CLS.prepare(wp, wf)
            if second_kind:
                _st.prepare_second_kind()
            if hasattr(CLS, 'query_many') and batch:
                CLS.query_many(_st, [wa])
            else:
                CLS.query(_st, wa)
            del _st
    except Exception:
        pass
    WARM_NS = time.perf_counter_ns() - tw
deadline = time.perf_counter() + job.get('job_budget_s', 1e9)
exc = None
try:
    W = job['workload']
    for b, block in enumerate(job['blocks']):
        if time.perf_counter() > deadline:
            status = 'budget_stop'
            break
        gc.collect()
        if W in ('W1', 'W7', 'TRACE'):
            res = []
            t0 = time.perf_counter_ns()
            if W == 'TRACE':
                for p, f, a in block['instances']:
                    res.append(M.TraceProvider.trace(p, f))
            elif trace_supplied:
                for (p, f, a), tr in zip(block['instances'], block['traces']):
                    res.append(CLS.query(CLS.prepare(p, f, trace=tr), a))
            elif method.startswith('voloch_semaev'):
                for p, f, a in block['instances']:
                    res.append(CLS.value(p, f, a))
            else:
                for p, f, a in block['instances']:
                    res.append(CLS.cold(p, f, a))
            t1 = time.perf_counter_ns()
            samples.append({'block': b, 'reps': len(block['instances']), 'stage': 'total', 'ns': t1 - t0})
            outputs.append(res)
        elif W in ('W2', 'W5', 'W6'):
            p, f, A = block['p'], block['f'], block['poles']
            t0 = time.perf_counter_ns()
            st = prep(p, f, block.get('trace'))
            if second_kind:
                st.prepare_second_kind()
            t1 = time.perf_counter_ns()
            res = CLS.query_many(st, A) if batch else [CLS.query(st, a) for a in A]
            t2 = time.perf_counter_ns()
            samples += [{'block': b, 'reps': 1, 'stage': 'prep', 'ns': t1 - t0},
                        {'block': b, 'reps': len(A), 'stage': 'query', 'ns': t2 - t1},
                        {'block': b, 'reps': 1, 'stage': 'total', 'ns': t2 - t0}]
            outputs.append(res)
            del st
        elif W == 'W3':
            p, f, U, vecs = block['p'], block['f'], block['poles'], block['vectors']
            t0 = time.perf_counter_ns()
            st = prep(p, f, block.get('trace'))
            single = {a: CLS.query(st, a) for a in U}
            se, _ = sum_eps_of(st, p, f, U[0])
            e = {a: eps_of(f, a, p) for a in U}
            K = []
            for j, aj in enumerate(U):
                diffs = [(ak - aj) % p for ak in U if ak != aj]
                inv = cases._batch_inv(diffs, p) if diffs else []
                corr = sum(e[ak] * iv for ak, iv in zip([x for x in U if x != aj], inv))
                K.append((single[aj] - corr) % p)
            const = (se - sum(e.values())) % p
            t1 = time.perf_counter_ns()
            res = [(sum(v * k for v, k in zip(vv, K)) + bb * const) % p for vv, bb in vecs]
            t2 = time.perf_counter_ns()
            samples += [{'block': b, 'reps': 1, 'stage': 'prep', 'ns': t1 - t0},
                        {'block': b, 'reps': len(vecs), 'stage': 'query', 'ns': t2 - t1},
                        {'block': b, 'reps': 1, 'stage': 'total', 'ns': t2 - t0}]
            outputs.append(res)
        elif W == 'W4':
            p, f = block['p'], block['f']
            t0 = time.perf_counter_ns()
            st = prep(p, f, block.get('trace'))
            t1 = time.perf_counter_ns()
            samples.append({'block': b, 'reps': 1, 'stage': 'prep', 'ns': t1 - t0})
            res = []
            for inst in block['sums']:
                U, v, bb = inst['poles'], inst['weights'], inst['b']
                ta = time.perf_counter_ns()
                if method.startswith('cmcs_frozen+weighted_sum'):
                    simple = [(a, w) for a, w in zip(U, v) if w]
                    excl = [a for a, w in zip(U, v) if not w]
                    val, _ = st.weighted_sum(simple=simple, b=bb, excluded=excl)
                    tb = tc = time.perf_counter_ns()
                else:
                    single = {}
                    se, c0 = sum_eps_of(st, p, f, U[0])
                    if c0 is not None:
                        single[U[0]] = c0
                    for a in U:
                        if a not in single:
                            single[a] = CLS.query(st, a)
                    e = {a: eps_of(f, a, p) for a in U}
                    tb = time.perf_counter_ns()
                    val, _ = cases.weighted_from_scalars(single, e, U, v, bb, se, p)
                    tc = time.perf_counter_ns()
                samples += [{'block': b, 'reps': 1, 'stage': 'scalars_s%d' % len(U), 'ns': tb - ta},
                            {'block': b, 'reps': 1, 'stage': 'correction_s%d' % len(U), 'ns': tc - tb},
                            {'block': b, 'reps': 1, 'stage': 'sum_s%d' % len(U), 'ns': tc - ta}]
                res.append(val)
            outputs.append(res)
        else:
            raise ValueError('unknown workload ' + W)
except MemoryError as e:
    status, exc = 'memory', repr(e)
except Exception as e:  # recorded, never silently dropped
    import traceback
    status, exc = 'exception', traceback.format_exc()[-2000:]

out = {'method': method, 'workload': job['workload'], 'group': job['group'], 'status': status,
       'exception': exc, 'samples': samples, 'outputs': outputs, 'import_ns': T_IMPORT,
       'pari_init_ns': PARI_INIT, 'warmup_ns': WARM_NS, 'rss_after_import_kib': RSS_AFTER_IMPORT,
       'rss_peak_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
       'python': sys.version.split()[0], 'executable': sys.executable}
json.dump(out, open(sys.argv[2], 'w'))
