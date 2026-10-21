"""Benchmark driver for the matched-output Cartier-Miller comparisons (BENCHMARK_PROTOCOL.md).

python3 -I bench.py --workloads W1,W2,... --out results/bench [--quick]

* Cases come from the benchmark seed sha256(freeze_digest + '|benchmark'); primes are drawn per
  instance from [2^(bits-1), 2^bits) excluding development lists and inherited primes.
* Every (workload, group, method) runs in its own fresh interpreter (bench_worker.py), in a
  seeded random method order per group, sequentially (no concurrent benchmark processes).
* Pilot runs (separate pilot instances) size repetitions: block target ~40 ms, <= 9 blocks,
  caps on repetitions and on job time; calls above the soft budget are recorded as 'budget'.
* Outputs are validated after the run, outside all timers (validate_outputs), and every sample
  row carries its validation status.
"""
import argparse
import csv
import hashlib
import json
import os
import random
import resource
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cmbench import core, cases  # noqa: E402

FREEZE = json.load(open(os.path.join(HERE, 'FREEZE.json')))
BENCH_SEED = hashlib.sha256((FREEZE['digest'] + '|benchmark').encode()).hexdigest()
SYS_PY = sys.executable
SAGE_PY = os.environ.get('CMBENCH_SAGE_PYTHON', os.path.join(HERE, '..', '..', 'venv_sage', 'bin', 'python'))
DEV_PRIMES = set([q for q in range(7, 140) if core.is_prime_small(q)] + [211, 257, 331, 499, 1009, 2003, 4001, 8009,
                 16411, 65537, 10 ** 5 + 3, 10 ** 6 + 3, 10 ** 7 + 19, 10 ** 9 + 7, 2 ** 61 - 1, 10 ** 18 + 9, 101, 131, 151, 181])
EXCLUDE = DEV_PRIMES | cases.INHERITED_PRIMES
SOFT_BUDGET_S = 2.0          # protocol default, per single call
EXTENDED_BUDGET_S = 60.0     # declared longer budget for first-query square-root comparators and traces
MEM_CEILING_KIB = 512 * 1024  # declared working-memory ceiling (peak RSS minus RSS after imports)
AS_LIMIT = 6 * 1024 ** 3     # hard address-space safety limit per worker
BLOCK_TARGET_S = 0.04
MAX_REPS = 200
JOB_CAP_S = 40.0

# per-method maximum feasible bit size (memory/time ceilings declared in advance; REPORT section 9)
MAX_BITS = {'cmcs_frozen': 64, 'cmcs_frozen[trace supplied]': 64, 'enum_c': 26, 'enum_conv': 20,
            'linrec_py': 20, 'linrec_c': 30, 'flint_power': 23, 'polyrec_c': 23, 'bgs07': 40,
            'bgs_harvey': 41, 'voloch_semaev': 64, 'flint_power+multipoint': 23, 'polyrec_c+multipoint': 23,
            'cmcs_frozen[second-kind prepared]': 23}
EXTENDED = {'bgs07', 'bgs_harvey', 'cmcs_frozen'}


def rng(label):
    return cases.rng_for(BENCH_SEED, label)


def env():
    e = dict(os.environ)
    e.setdefault('CM_INHERITED_SRC', '')
    return e


def _limit():
    resource.setrlimit(resource.RLIMIT_AS, (AS_LIMIT, AS_LIMIT))


def run_job(job, tmpdir, hard_timeout):
    os.makedirs(tmpdir, exist_ok=True)
    tag = hashlib.sha1(json.dumps([job['workload'], job['group'], job['method'], job.get('phase')]).encode()).hexdigest()[:12]
    jp, op = os.path.join(tmpdir, tag + '.job.json'), os.path.join(tmpdir, tag + '.out.json')
    json.dump(job, open(jp, 'w'))
    py = SAGE_PY if job['method'] == 'bgs_harvey' else SYS_PY
    t0 = time.time()
    try:
        cp = subprocess.run([py, '-I', os.path.join(HERE, 'bench_worker.py'), jp, op], env=env(),
                            preexec_fn=_limit, timeout=hard_timeout, capture_output=True, text=True)
        if cp.returncode != 0 or not os.path.exists(op):
            return {'status': 'crash', 'exception': (cp.stderr or '')[-2000:], 'samples': [], 'outputs': [],
                    'wall_s': time.time() - t0}
        out = json.load(open(op))
    except subprocess.TimeoutExpired:
        return {'status': 'timeout', 'exception': 'hard timeout %.0f s' % hard_timeout, 'samples': [], 'outputs': [],
                'wall_s': time.time() - t0}
    out['wall_s'] = time.time() - t0
    return out


# ------------------------------------------------------------------------------------ instances
KINDS3 = ['generic', 'zero_const', 'unit_const', 'generic']
KINDS4 = ['generic', 'zero_const', 'lead_square', 'lead_nonsquare']


def make_instance(r, bits, d, i):
    lo, hi = 1 << (bits - 1), 1 << bits
    p = cases.random_prime(r, max(lo, 11), hi, EXCLUDE)
    f = cases.random_curve(r, p, d, (KINDS3 if d == 3 else KINDS4)[i % 4])
    a = cases.random_pole(r, p, f, prefer_zero=(i % 8 == 0))
    return [p, f, a]


WARMUP = {}
SCALING = {'enum_c': 1.0, 'enum_conv': 1.1, 'linrec_py': 1.0, 'linrec_c': 1.0, 'flint_power': 1.1, 'polyrec_c': 1.0,
           'bgs07': 0.55, 'bgs_harvey': 0.55, 'cmcs_frozen': 0.0}


def pilot_and_size(workload, group, method, pilot_blocks, tmp, budget):
    """One-instance pilot; returns (t_single_s, status, pilot_record)."""
    job = {'workload': workload, 'group': group, 'method': method, 'phase': 'pilot', 'blocks': pilot_blocks,
           'needs_pari': method.startswith('cmcs') or workload == 'TRACE', 'job_budget_s': budget * 3,
           'warmup': WARMUP.get(group)}
    out = run_job(job, tmp, hard_timeout=budget * 6 + 120)
    if out.get('status') != 'ok' or not out.get('samples'):
        return None, out.get('status', 'crash'), out
    tot = [s for s in out['samples'] if s['stage'] == 'total']
    t = min(s['ns'] / s['reps'] for s in tot) / 1e9
    return t, ('budget' if t > budget else 'ok'), out


def write_rows(writer, run_id, workload, group, method, out, extra, validation):
    for s in out.get('samples', []):
        writer.writerow([run_id, workload, group, method, FREEZE['digest'][:16], s['block'], s['reps'], s['stage'],
                         s['ns'], out.get('status'), validation, json.dumps(extra)])
    if not out.get('samples'):
        writer.writerow([run_id, workload, group, method, FREEZE['digest'][:16], '', '', '', '', out.get('status'),
                         validation, json.dumps({**extra, 'exception': (out.get('exception') or '')[:300]})])


# ------------------------------------------------------------------------------------ workload specs
W1_BITS = [10, 13, 16, 20, 23, 26, 30, 33, 36, 40, 48, 56, 62]
W1_METHODS = ['cmcs_frozen', 'enum_c', 'enum_conv', 'linrec_py', 'linrec_c', 'flint_power', 'polyrec_c',
              'bgs07', 'bgs_harvey']


def budget_for(method, bits):
    base = method.split('[')[0].split('+')[0]
    return EXTENDED_BUDGET_S if (base in EXTENDED and bits >= 30) else SOFT_BUDGET_S


def w1_groups(quick):
    bits = W1_BITS if not quick else [10, 16, 30]
    return [('W1', 'b%02d_d%d' % (b, d), b, d) for b in bits for d in (3, 4)]


def blocks_from_pool(pool, R, n):
    return [{'instances': pool[i * R:(i + 1) * R]} for i in range(n)]


LAST_T = {}


def run_scalar_ladder(workload, groups, methods, writer, outdir, log, pools_out, quick):
    """W1 (cold), W7 (exceptional) and TRACE: blocks of fresh instances, same pool prefix for all methods."""
    tmp = os.path.join(outdir, 'tmp')
    skipped_after = {}
    for (_, gid, bits, d) in groups:
        r = rng('%s|%s' % (workload, gid))
        pilot_r = rng('%s|%s|pilot' % (workload, gid))
        if workload == 'W7':
            pool, ppool = pools_out[gid]['pool'], pools_out[gid]['pilot']
        else:
            pool = [make_instance(r, bits, d, i) for i in range(9 * MAX_REPS)]
            ppool = [make_instance(pilot_r, bits, d, i) for i in range(3)]
            pools_out[gid] = {'pool': pool, 'pilot': ppool, 'bits': bits, 'd': d}
        WARMUP[gid] = ppool[2] if len(ppool) > 2 else ppool[-1]
        order = list(methods)
        random.Random(BENCH_SEED + gid).shuffle(order)
        for m in order:
            base = m.split('[')[0]
            if bits > MAX_BITS.get(m, MAX_BITS.get(base, 64)):
                write_rows(writer, 'main', workload, gid, m, {'status': 'skipped_ceiling'}, {'bits': bits, 'd': d}, 'n/a')
                continue
            prev = LAST_T.get((workload, m, d))
            if prev is not None:
                pb_bits, pt = prev
                pred = pt * 2 ** (SCALING.get(base.split('+')[0], 1.0) * (bits - pb_bits))
                if pred > 3 * budget_for(m, bits):
                    write_rows(writer, 'main', workload, gid, m, {'status': 'skipped_predicted_budget'},
                               {'bits': bits, 'd': d, 'predicted_single_s_not_a_measurement': pred,
                                'from_class_bits': pb_bits}, 'n/a')
                    log('%s %s %-28s skipped: predicted %.3g s > 3x budget' % (workload, gid, m, pred))
                    continue
            if skipped_after.get(m) is not None and bits > skipped_after[m]:
                write_rows(writer, 'main', workload, gid, m, {'status': 'budget_skipped_after_smaller_class'},
                           {'bits': bits, 'd': d, 'first_budget_class_bits': skipped_after[m]}, 'n/a')
                continue
            bud = budget_for(m, bits)
            extra = {'bits': bits, 'd': d, 'budget_s': bud}
            if workload == 'W7' or '[trace supplied]' in m:
                pb = [{'instances': [x[:3] for x in ppool[:1]], 'traces': [x[3] for x in ppool[:1]]}]
            else:
                pb = [{'instances': ppool[:1]}]
            t, st, pout = pilot_and_size(workload, gid, m, pb, tmp, bud)
            if st != 'ok':
                write_rows(writer, 'pilot', workload, gid, m, pout, {**extra, 'pilot_single_s': t}, 'pilot')
                if st == 'budget':
                    skipped_after.setdefault(m, bits)
                log('%s %s %-28s pilot status %s (%.3g s)' % (workload, gid, m, st, t or -1))
                continue
            LAST_T[(workload, m, d)] = (bits, t)
            R = max(1, min(MAX_REPS, int(round(BLOCK_TARGET_S / max(t, 1e-7)))))
            nb = 9
            while nb > 3 and nb * R * t > JOB_CAP_S:
                nb -= 1
            if nb * R * t > JOB_CAP_S * 2:
                R = 1
                nb = max(1, min(3, int(JOB_CAP_S * 3 // max(t, 1e-9))))
            if R * nb > len(pool):                  # never reuse an instance within a job
                R = max(1, len(pool) // nb)
            if workload == 'W7' or '[trace supplied]' in m:
                blocks = [{'instances': [x[:3] for x in pool[i * R:(i + 1) * R]],
                           'traces': [x[3] for x in pool[i * R:(i + 1) * R]]} for i in range(nb)]
            else:
                blocks = blocks_from_pool(pool, R, nb)
            job = {'workload': workload, 'group': gid, 'method': m, 'phase': 'main', 'blocks': blocks,
                   'needs_pari': m.startswith('cmcs') or workload == 'TRACE', 'job_budget_s': JOB_CAP_S * 3,
                   'warmup': WARMUP.get(gid)}
            out = run_job(job, tmp, hard_timeout=max(300, JOB_CAP_S * 6 + t * nb * R * 2))
            out['R'], out['nb'] = R, nb
            res_path = os.path.join(outdir, 'outputs', '%s__%s__%s.json' % (workload, gid, m.replace('[', '(').replace(']', ')').replace(' ', '_')))
            os.makedirs(os.path.dirname(res_path), exist_ok=True)
            json.dump({'method': m, 'R': R, 'nb': nb, 'status': out.get('status'), 'outputs': out.get('outputs'),
                       'rss_peak_kib': out.get('rss_peak_kib'), 'rss_after_import_kib': out.get('rss_after_import_kib'),
                       'import_ns': out.get('import_ns'), 'pari_init_ns': out.get('pari_init_ns'),
                       'exception': out.get('exception')}, open(res_path, 'w'))
            extra.update({'R': R, 'nb': nb, 'rss_peak_kib': out.get('rss_peak_kib'),
                          'rss_after_import_kib': out.get('rss_after_import_kib'), 'import_ns': out.get('import_ns'),
                          'pari_init_ns': out.get('pari_init_ns')})
            write_rows(writer, 'main', workload, gid, m, out, extra, 'pending')
            log('%s %s %-28s R=%d nb=%d status=%s med=%.4g s/call' % (
                workload, gid, m, R, nb, out.get('status'),
                (sorted(s['ns'] / max(1, s['reps']) for s in out.get('samples', []) if s['stage'] == 'total') or [0])[
                    len([s for s in out.get('samples', []) if s['stage'] == 'total']) // 2] / 1e9))


def run_prepared(workload, specs, methods, writer, outdir, log, pools_out):
    """W2/W5/W6/W3/W4: each block is a fresh curve with its own pole list / sums."""
    tmp = os.path.join(outdir, 'tmp')
    for spec in specs:
        gid, blocks, bits = spec['gid'], spec['blocks'], spec['bits']
        pools_out[gid] = spec
        order = list(methods)
        random.Random(BENCH_SEED + gid).shuffle(order)
        for m in order:
            base = m.split('[')[0]
            if bits > MAX_BITS.get(m, MAX_BITS.get(base, 64)):
                write_rows(writer, 'main', workload, gid, m, {'status': 'skipped_ceiling'}, {'bits': bits}, 'n/a')
                continue
            if m in spec.get('exclude_methods', ()):
                write_rows(writer, 'main', workload, gid, m, {'status': 'skipped_predicted_budget'},
                           {'bits': bits, 'reason': spec['exclude_methods'][m]}, 'n/a')
                continue
            b0 = blocks[0]
            wa = b0['poles'][0] if 'poles' in b0 else b0['sums'][0]['poles'][0]
            warm = [b0['p'], b0['f'], wa]
            pilot = {'workload': workload, 'group': gid, 'method': m, 'phase': 'pilot', 'blocks': blocks[:1],
                     'needs_pari': m.startswith('cmcs'), 'job_budget_s': spec.get('block_budget_s', 20), 'warmup': warm}
            pout = run_job(pilot, tmp, hard_timeout=spec.get('block_budget_s', 20) * 3 + 120)
            tot = [s['ns'] for s in pout.get('samples', []) if s['stage'] in ('total',) or s['stage'].startswith('sum_')]
            tsum = sum(tot) / 1e9 if tot else None
            if pout.get('status') != 'ok' or tsum is None or tsum > spec.get('block_budget_s', 20):
                st = pout.get('status') if pout.get('status') != 'ok' else 'budget'
                write_rows(writer, 'pilot', workload, gid, m, pout, {'bits': bits, 'pilot_block_s': tsum,
                                                                     'status_note': st}, 'pilot')
                log('%s %s %-30s pilot %s (%.3g s)' % (workload, gid, m, st, tsum or -1))
                continue
            job = {'workload': workload, 'group': gid, 'method': m, 'phase': 'main', 'blocks': blocks[1:],
                   'needs_pari': m.startswith('cmcs'), 'job_budget_s': JOB_CAP_S * 3, 'warmup': warm}
            out = run_job(job, tmp, hard_timeout=max(300, JOB_CAP_S * 6))
            res_path = os.path.join(outdir, 'outputs', '%s__%s__%s.json' % (workload, gid, m.replace('[', '(').replace(']', ')').replace(' ', '_')))
            os.makedirs(os.path.dirname(res_path), exist_ok=True)
            json.dump({'method': m, 'status': out.get('status'), 'outputs': out.get('outputs'),
                       'pilot_outputs': pout.get('outputs'), 'rss_peak_kib': out.get('rss_peak_kib'),
                       'rss_after_import_kib': out.get('rss_after_import_kib'), 'exception': out.get('exception')},
                      open(res_path, 'w'))
            extra = {'bits': bits, 'rss_peak_kib': out.get('rss_peak_kib'), 'rss_after_import_kib': out.get('rss_after_import_kib'),
                     'pilot_rss_peak_kib': pout.get('rss_peak_kib'), **spec.get('extra', {})}
            write_rows(writer, 'pilot', workload, gid, m, pout, extra, 'pending')
            write_rows(writer, 'main', workload, gid, m, out, extra, 'pending')
            log('%s %s %-30s blocks=%d status=%s' % (workload, gid, m, len(blocks) - 1, out.get('status')))


def curve_with_poles(r, bits, d, Q, i, allow_branch=False):
    lo, hi = 1 << (bits - 1), 1 << bits
    p = cases.random_prime(r, max(lo, 11), hi, EXCLUDE)
    f = cases.random_curve(r, p, d, (KINDS3 if d == 3 else KINDS4)[i % 4])
    adm = None
    if Q >= p // 8:
        adm = [a for a in range(p) if core.peval(f, a, p)]
        r.shuffle(adm)
        A = adm[:Q]
    else:
        S = set()
        while len(S) < Q:
            a = r.randrange(p)
            if core.peval(f, a, p):
                S.add(a)
        A = sorted(S)
        r.shuffle(A)
    return p, f, A


def w2_specs(quick):
    specs = []
    for bits in ([16, 20, 23] if not quick else [16]):
        for d in (3, 4):
            for Q in ([1, 8, 64, 512] if not quick else [1, 8]):
                r = rng('W2|%d|%d|%d' % (bits, d, Q))
                blocks = []
                for i in range(6):           # block 0 = pilot
                    p, f, A = curve_with_poles(r, bits, d, Q, i)
                    blocks.append({'p': p, 'f': f, 'poles': A})
                specs.append({'gid': 'b%02d_d%d_Q%d' % (bits, d, Q), 'bits': bits, 'blocks': blocks,
                              'block_budget_s': 20, 'extra': {'d': d, 'Q': Q}})
    return specs


def w5_specs(quick):
    specs = []
    for bits in ([12, 14, 16, 18] if not quick else [12]):
        for d in (3, 4):
            for frac in (16, 4, 1):
                r = rng('W5|%d|%d|%d' % (bits, d, frac))
                blocks = []
                for i in range(4):
                    lo = 1 << (bits - 1)
                    p = cases.random_prime(r, lo, 2 * lo, EXCLUDE)
                    Q = (p - 4) // frac
                    p2, f, A = curve_with_poles_fixed_p(r, p, d, Q, i)
                    blocks.append({'p': p2, 'f': f, 'poles': A})
                specs.append({'gid': 'b%02d_d%d_Qp/%d' % (bits, d, frac), 'bits': bits, 'blocks': blocks,
                              'block_budget_s': 30, 'extra': {'d': d, 'Q_fraction': '1/%d' % frac}})
    return specs


def curve_with_poles_fixed_p(r, p, d, Q, i):
    f = cases.random_curve(r, p, d, (KINDS3 if d == 3 else KINDS4)[i % 4])
    adm = [a for a in range(p) if core.peval(f, a, p)]
    r.shuffle(adm)
    return p, f, adm[:Q]


def w6_specs(quick):
    specs = []
    for bits in ([13, 16, 20] if not quick else [13]):
        for d in (3, 4):
            r = rng('W6|%d|%d' % (bits, d))
            blocks = []
            while len(blocks) < 5:
                lo = 1 << (bits - 1)
                p = cases.random_prime(r, lo, 2 * lo, EXCLUDE)
                f = cases.random_curve(r, p, d)
                roots = [x for x in range(p) if core.peval(f, x, p) == 0] if p < 1 << 21 else []
                if roots:
                    blocks.append({'p': p, 'f': f, 'poles': roots})
            specs.append({'gid': 'b%02d_d%d_branch' % (bits, d), 'bits': bits, 'blocks': blocks,
                          'block_budget_s': 20, 'extra': {'d': d, 'poles': 'all rational roots of f'}})
    return specs


def w3_specs(quick):
    specs = []
    for bits in ([20, 30] if not quick else [20]):
        for d in (3, 4):
            r = rng('W3|%d|%d' % (bits, d))
            blocks = []
            for i in range(6):
                p, f, U = curve_with_poles(r, bits, d, 8, i)
                vecs = [[[r.randrange(p) for _ in U], r.randrange(p)] for _ in range(1000)]
                blocks.append({'p': p, 'f': f, 'poles': U, 'vectors': vecs})
            specs.append({'gid': 'b%02d_d%d_s8_V1000' % (bits, d), 'bits': bits, 'blocks': blocks,
                          'block_budget_s': 20, 'extra': {'d': d, 's': 8, 'vectors': 1000}})
    return specs


def w4_specs(quick):
    specs = []
    S = [1, 2, 4, 8, 16, 32, 64, 128, 256] if not quick else [1, 4, 16]
    for bits in ([20, 62] if not quick else [20]):
        for d in (3, 4):
            r = rng('W4|%d|%d' % (bits, d))
            blocks = []
            for i in range(4):
                lo = 1 << (bits - 1)
                p = cases.random_prime(r, lo, 2 * lo, EXCLUDE)
                f = cases.random_curve(r, p, d, (KINDS3 if d == 3 else KINDS4)[i % 4])
                sums = []
                for s in S:
                    U = set()
                    while len(U) < s:
                        a = r.randrange(p)
                        if core.peval(f, a, p):
                            U.add(a)
                    U = sorted(U)
                    r.shuffle(U)
                    v = [r.randrange(p) for _ in U]
                    if s > 1:
                        v[-1] = 0            # an extra exclusion represented by a zero coefficient
                    sums.append({'poles': U, 'weights': v, 'b': r.randrange(p)})
                blocks.append({'p': p, 'f': f, 'sums': sums})
            specs.append({'gid': 'b%02d_d%d_s1-%d' % (bits, d, S[-1]), 'bits': bits, 'blocks': blocks,
                          'block_budget_s': 30, 'extra': {'d': d, 's_values': S}})
    return specs


def w7_pools(quick, pari_py_helper):
    """Exceptional-trace pools from CM constructions (computed in a system-Python helper)."""
    return pari_py_helper


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workloads', default='TRACE,W1,W2,W3,W4,W5,W6,W7')
    ap.add_argument('--out', required=True)
    ap.add_argument('--quick', action='store_true')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    logf = open(os.path.join(a.out, 'bench.log'), 'a')

    def log(msg):
        line = time.strftime('%H:%M:%S ') + msg
        print(line, flush=True)
        logf.write(line + '\n')
        logf.flush()
    csv_path = os.path.join(a.out, 'timing_samples.csv')
    new = not os.path.exists(csv_path)
    fh = open(csv_path, 'a', newline='')
    w = csv.writer(fh)
    if new:
        w.writerow(['run', 'workload', 'group', 'method', 'impl_digest16', 'block', 'reps', 'stage', 'ns', 'status',
                    'validation', 'extra'])
    meta = {'bench_seed': BENCH_SEED, 'freeze_digest': FREEZE['digest'], 'soft_budget_s': SOFT_BUDGET_S,
            'extended_budget_s': EXTENDED_BUDGET_S, 'extended_methods': sorted(EXTENDED), 'mem_ceiling_kib': MEM_CEILING_KIB,
            'as_limit_bytes': AS_LIMIT, 'block_target_s': BLOCK_TARGET_S, 'max_reps': MAX_REPS, 'job_cap_s': JOB_CAP_S,
            'max_bits': MAX_BITS, 'bench_py_sha256': hashlib.sha256(open(__file__, 'rb').read()).hexdigest(),
            'worker_sha256': hashlib.sha256(open(os.path.join(HERE, 'bench_worker.py'), 'rb').read()).hexdigest(),
            'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    pools = {}
    for W in a.workloads.split(','):
        log('=== workload %s' % W)
        if W == 'W1':
            run_scalar_ladder('W1', w1_groups(a.quick), W1_METHODS, w, a.out, log, pools, a.quick)
        elif W == 'TRACE':
            run_scalar_ladder('TRACE', w1_groups(a.quick), ['cmcs_frozen'], w, a.out, log, pools, a.quick)
        elif W == 'W2':
            run_prepared('W2', w2_specs(a.quick), ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'enum_c', 'linrec_c',
                                                   'flint_power', 'flint_power+multipoint', 'polyrec_c',
                                                   'polyrec_c+multipoint', 'enum_conv', 'bgs_harvey', 'bgs07'], w, a.out, log, pools)
        elif W == 'W3':
            run_prepared('W3', w3_specs(a.quick), ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'enum_c', 'linrec_c',
                                                   'polyrec_c', 'bgs_harvey'], w, a.out, log, pools)
        elif W == 'W4':
            run_prepared('W4', w4_specs(a.quick), ['cmcs_frozen+weighted_sum', 'cmcs_frozen', 'enum_c', 'linrec_c',
                                                   'polyrec_c', 'polyrec_c+multipoint', 'bgs_harvey'], w, a.out, log, pools)
        elif W == 'W5':
            run_prepared('W5', w5_specs(a.quick), ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'flint_power+multipoint',
                                                   'polyrec_c+multipoint', 'enum_conv', 'enum_c', 'bgs_harvey'], w, a.out, log, pools)
        elif W == 'W6':
            run_prepared('W6', w6_specs(a.quick), ['cmcs_frozen[second-kind prepared]', 'enum_c', 'linrec_c', 'polyrec_c',
                                                   'bgs_harvey'], w, a.out, log, pools)
        elif W == 'W7':
            p7 = json.load(open(os.path.join(a.out, 'w7_pools.json')))
            groups = [('W7', g, v['bits'], v['d']) for g, v in p7.items()]
            for g, v in p7.items():
                pools[g] = v
            run_scalar_ladder('W7', groups, ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'voloch_semaev', 'bgs_harvey'],
                              w, a.out, log, pools, a.quick)
        fh.flush()
    meta['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    json.dump(pools, open(os.path.join(a.out, 'cases_%s.json' % a.workloads.replace(',', '_')), 'w'))
    json.dump(meta, open(os.path.join(a.out, 'bench_meta_%s.json' % a.workloads.replace(',', '_')), 'w'), indent=1)
    log('done')


if __name__ == '__main__':
    main()
