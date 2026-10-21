"""Summaries, tables and plots from the raw benchmark samples (no timing is invented: every number
is a median/min/max over recorded blocks; missing cells carry the recorded outcome).

python3 -I analyze.py RESULTS_BENCH_DIR OUT_DIR
Writes: summary.json, tables.md, plots/*.png (each plot lists its source CSV and sha256).
"""
import csv, hashlib, json, math, os, statistics, sys
from collections import defaultdict

rdir, odir = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(odir, 'plots'), exist_ok=True)
src = os.path.join(rdir, 'timing_samples_validated.csv')
if not os.path.exists(src):
    src = os.path.join(rdir, 'timing_samples.csv')
SRC_SHA = hashlib.sha256(open(src, 'rb').read()).hexdigest()
rows = list(csv.DictReader(open(src)))

# ----------------------------------------------------------------------------- collect
main = defaultdict(lambda: defaultdict(list))     # (W, g, m) -> stage -> [per-rep seconds]
blocks_total = defaultdict(list)                  # (W, g, m) -> [block total seconds]
outcome, extra_of, validation = {}, {}, {}
for r in rows:
    key = (r['workload'], r['group'], r['method'])
    ex = json.loads(r['extra']) if r['extra'] else {}
    if r['run'] == 'main':
        extra_of.setdefault(key, ex)
        validation[key] = r['validation']
        if r['ns']:
            reps = max(1, int(r['reps'] or 1))
            main[key][r['stage']].append(int(r['ns']) / 1e9 / reps)
            if r['stage'] in ('total',) or r['stage'].startswith('sum_'):
                blocks_total[key].append(int(r['ns']) / 1e9)
            outcome[key] = r['status']
        else:
            outcome.setdefault(key, r['status'])
    elif r['run'] == 'pilot':
        if key not in outcome or outcome[key] not in ('ok',):
            if not main.get(key):
                ps = ex.get('pilot_single_s') or ex.get('pilot_block_s')
                st = ex.get('status_note') or r['status']
                if st == 'ok':
                    st = 'budget'
                outcome[key] = '%s (pilot %.3g s)' % (st, ps) if isinstance(ps, (int, float)) else st
        extra_of.setdefault(key, ex)


def med(x):
    return statistics.median(x) if x else None


def fmt(t):
    if t is None:
        return '—'
    if t < 1e-3:
        return '%.1f µs' % (t * 1e6)
    if t < 1:
        return '%.2f ms' % (t * 1e3)
    return '%.2f s' % t


def cell(key, stage='total'):
    v = main.get(key, {}).get(stage)
    if v:
        s = fmt(med(v))
        if len(v) > 1:
            s += ' [%s–%s]' % (fmt(min(v)), fmt(max(v)))
        return s
    o = outcome.get(key)
    return o.replace('_', ' ') if o else 'n/a'


summary = {'source_csv': os.path.basename(src), 'source_sha256': SRC_SHA, 'groups': {}}
for key, st in main.items():
    summary['groups']['|'.join(key)] = {s: {'median_s': med(v), 'min_s': min(v), 'max_s': max(v), 'n_blocks': len(v)}
                                        for s, v in st.items()}
summary['outcomes'] = {'|'.join(k): v for k, v in outcome.items()}
summary['validation'] = {'|'.join(k): v for k, v in validation.items()}
summary['extra'] = {'|'.join(k): v for k, v in extra_of.items()}
json.dump(summary, open(os.path.join(odir, 'summary.json'), 'w'), indent=1, default=str)

T = []


def table(title, header, body, note=None):
    T.append('### ' + title + '\n')
    T.append('| ' + ' | '.join(header) + ' |')
    T.append('|' + '---|' * len(header))
    for b in body:
        T.append('| ' + ' | '.join(b) + ' |')
    if note:
        T.append('\n' + note)
    T.append('')


# ----------------------------------------------------------------------------- W1
W1M = ['cmcs_frozen', 'bgs_harvey', 'bgs07', 'linrec_c', 'linrec_py', 'enum_c', 'enum_conv', 'flint_power', 'polyrec_c']
groups = sorted({k[1] for k in list(main) + list(outcome) if k[0] == 'W1'}, key=lambda g: (int(g.split('_')[1][1]), int(g[1:3])))
for d in (3, 4):
    body = []
    for g in [x for x in groups if x.endswith('d%d' % d)]:
        bits = int(g[1:3])
        tr = main.get(('TRACE', g, 'cmcs_frozen'), {}).get('total')
        body.append(['%d' % bits] + [cell(('W1', g, m)) for m in W1M] + [fmt(med(tr)) if tr else '—'])
    table('W1 cold single query, %s (median per complete query [min–max over blocks])' % ('cubics' if d == 3 else 'quartics'),
          ['bits'] + W1M + ['of which PARI trace (TRACE)'], body,
          'Each instance is a new prime p in [2^(bits-1), 2^bits), a new curve and a new pole. cmcs_frozen includes the exact trace (PARI ellap: baby-step/giant-step below ~30 digits), validation and translation sessions; the TRACE column is the trace alone, measured on separate fresh instances of the same class. Square-root comparators (bgs_*) and cmcs at >= 30 bits use the declared 60 s extended budget; others 2 s.')

# ----------------------------------------------------------------------------- W7
groups7 = sorted({k[1] for k in list(main) + list(outcome) if k[0] == 'W7'}, key=lambda g: (int(g.split('_')[1][1]), int(g[1:3])))
W7M = ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'voloch_semaev', 'bgs_harvey']
table('W7 exceptional traces tau = chi(f(a)) = +-1 (CM-constructed curves; median per query)',
      ['group'] + W7M, [[g] + [cell(('W7', g, m)) for m in W7M] for g in groups7],
      'PARI ellap recognises CM by a principal order and uses its O(log q)^2 formula here, so the cmcs_frozen trace cost is not representative of general curves. voloch_semaev receives the hypothesis tau = +-1 for free (known-trace family assumption), as does cmcs_frozen[trace supplied].')

# ----------------------------------------------------------------------------- W2 / W5 / W6 / W3
def prepared_table(W, methods, title, note, per_query=True):
    def qkey(g):
        q = g.split('_', 2)[2] if g.count('_') > 1 else ''
        if q.startswith('Qp/'):
            return 1.0 / int(q[3:])
        return int(q[1:]) if q[1:].isdigit() else 0
    gs = sorted({k[1] for k in list(main) + list(outcome) if k[0] == W}, key=lambda g: (int(g[1:3]), g.split('_')[1], qkey(g)))
    body = []
    for g in gs:
        for m in methods:
            key = (W, g, m)
            if key not in main and key not in outcome:
                continue
            st = main.get(key, {})
            ex = extra_of.get(key, {})
            mem = ex.get('rss_peak_kib')
            base = ex.get('rss_after_import_kib')
            memtxt = ('%.0f MiB' % ((mem - base) / 1024) if (mem and base) else '—')
            if st:
                q = st.get('query', [])
                nq = None
                body.append([g, m, fmt(med(st.get('prep'))), fmt(med(q)) + ('/query' if per_query else ''),
                             fmt(med([a for a in blocks_total[key]])), memtxt, validation.get(key, '')])
            else:
                body.append([g, m, '—', '—', outcome.get(key, 'n/a'), '—', ''])
    table(title, ['group', 'method', 'preparation', 'query', 'total per block', 'peak RSS above imports', 'output validation'], body, note)


prepared_table('W2', ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'flint_power', 'flint_power+multipoint', 'polyrec_c',
                      'polyrec_c+multipoint', 'enum_conv', 'enum_c', 'linrec_c', 'bgs_harvey', 'bgs07'],
               'W2 prepared curve: fixed (p, f), Q distinct admissible poles (medians over 5 fresh curves)',
               'query = per-pole time; total = preparation + all Q queries. cmcs_frozen acquires the trace in preparation; [trace supplied] is the workload assumption of a free trace.')
prepared_table('W5', ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'flint_power+multipoint', 'polyrec_c+multipoint', 'enum_conv', 'enum_c', 'bgs_harvey'],
               'W5 dense queries: Q ~ p/16, p/4 or all admissible poles',
               'multipoint = FLINT fmpz_mod_poly_evaluate_fmpz_vec (subproduct tree); enum_conv = one cyclic correlation for all poles.')
prepared_table('W6', ['cmcs_frozen[second-kind prepared]', 'linrec_c', 'polyrec_c', 'enum_c', 'bgs_harvey'],
               'W6 branch poles (all rational roots of f), secondary workload',
               'cmcs_frozen charges the trace and its O(p) streaming second-kind recurrence (Python) in preparation; the coefficient methods need no extra data.')
prepared_table('W3', ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'enum_c', 'linrec_c', 'polyrec_c', 'bgs_harvey'],
               'W3 fixed excluded set (s = 8) and 1000 coefficient vectors', 'query = per coefficient vector (identical O(s) dot product for every method).')

# ----------------------------------------------------------------------------- condensed W2 / W5
def condensed(W, methods, title, note):
    def qkey(g):
        q = g.split('_', 2)[2] if g.count('_') > 1 else ''
        if q.startswith('Qp/'):
            return 1.0 / int(q[3:])
        return int(q[1:]) if q[1:].isdigit() else 0
    gs = sorted({k[1] for k in list(main) + list(outcome) if k[0] == W},
                key=lambda g: (int(g[1:3]), g.split('_')[1], qkey(g)))
    body = []
    for g in gs:
        tots = {}
        row = [g]
        for m in methods:
            key = (W, g, m)
            if main.get(key) and blocks_total.get(key):
                t = med(blocks_total[key])
                tots[m] = t
                row.append(fmt(t))
            else:
                o = outcome.get(key, 'n/a')
                row.append(o.replace('_', ' ') if len(o) < 40 else o[:38])
        best = min(tots, key=tots.get) if tots else '—'
        row.append(best)
        body.append(row)
    table(title, ['group'] + methods + ['fastest measured'], body, note)


condensed('W2', ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'polyrec_c', 'polyrec_c+multipoint', 'flint_power',
                 'enum_conv', 'bgs_harvey', 'enum_c', 'linrec_c', 'bgs07'],
          'W2 condensed: median total per workload block (preparation + all Q queries)',
          'Totals include each method\'s legitimate preparation once per curve. Budget outcomes are recorded pilots (no timing blocks run).')
condensed('W5', ['cmcs_frozen', 'cmcs_frozen[trace supplied]', 'polyrec_c+multipoint', 'flint_power+multipoint', 'enum_conv',
                 'enum_c', 'bgs_harvey'],
          'W5 condensed: dense queries, median total per block', 'Q = floor((p-4)/16), floor((p-4)/4) or all admissible poles of a fresh curve.')

# ----------------------------------------------------------------------------- W4
gs4 = sorted({k[1] for k in list(main) + list(outcome) if k[0] == 'W4'})
for g in gs4:
    ms = sorted({k[2] for k in main if k[0] == 'W4' and k[1] == g} | {k[2] for k in outcome if k[0] == 'W4' and k[1] == g})
    svals = sorted({int(s.split('_s')[1]) for k in main if k[0] == 'W4' and k[1] == g for s in main[k] if s.startswith('sum_s')})
    body = []
    for s in svals:
        row = [str(s)]
        for m in ms:
            st = main.get(('W4', g, m), {})
            if st:
                row.append('%s (scalars %s, corr %s)' % (fmt(med(st.get('sum_s%d' % s))), fmt(med(st.get('scalars_s%d' % s))),
                                                         fmt(med(st.get('correction_s%d' % s)))))
            else:
                row.append(outcome.get(('W4', g, m), 'n/a'))
        body.append(row)
    prep_row = ['prep'] + [fmt(med(main.get(('W4', g, m), {}).get('prep'))) for m in ms]
    table('W4 one weighted sum with s poles, %s (median over 3 fresh curves)' % g, ['s'] + ms, [prep_row] + body,
          'Weighted sum with a constant term and one zero coefficient (an extra exclusion). Each method also acquires sum_x chi(f(x)) mod p by its own route (trace; coefficient index N+1; table sum).')

open(os.path.join(odir, 'tables.md'), 'w').write('\n'.join(T) + '\n\nSource: %s (sha256 %s)\n' % (os.path.basename(src), SRC_SHA))

# ----------------------------------------------------------------------------- plots
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SLOTS = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6']
MARK = ['o', 's', '^', 'D', 'v', 'P', 'X']
PLOT_M = ['cmcs_frozen', 'bgs_harvey', 'bgs07', 'linrec_c', 'enum_c', 'polyrec_c', 'flint_power']
LABEL = {'cmcs_frozen': 'Cartier–Miller (frozen, incl. PARI trace)', 'bgs_harvey': 'BGS – Harvey kernel (NTL)',
         'bgs07': 'BGS – this package (FLINT+numpy)', 'linrec_c': 'linear recurrence (C)', 'enum_c': 'enumeration (C)',
         'polyrec_c': 'power via recurrence (C) + Horner', 'flint_power': 'FLINT power + Horner'}
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': '#52514e', 'axes.labelcolor': '#0b0b0b', 'xtick.color': '#52514e',
                     'ytick.color': '#52514e', 'axes.grid': True, 'grid.color': '#e6e5e1', 'grid.linewidth': 0.6,
                     'axes.spines.top': False, 'axes.spines.right': False, 'figure.facecolor': '#fcfcfb', 'axes.facecolor': '#fcfcfb'})
fig, axes = plt.subplots(1, 2, figsize=(11, 5.0), sharey=True)
for ax, d in zip(axes, (3, 4)):
    for i, m in enumerate(PLOT_M):
        xs, ys, lo, hi = [], [], [], []
        for g in [x for x in groups if x.endswith('d%d' % d)]:
            v = main.get(('W1', g, m), {}).get('total')
            if v:
                xs.append(int(g[1:3])); ys.append(med(v)); lo.append(min(v)); hi.append(max(v))
        if xs:
            ax.plot(xs, ys, color=SLOTS[i], marker=MARK[i], markersize=5, linewidth=2, label=LABEL[m])
            ax.fill_between(xs, lo, hi, color=SLOTS[i], alpha=0.12, linewidth=0)
    tr = [(int(g[1:3]), med(main[('TRACE', g, 'cmcs_frozen')]['total'])) for g in groups if g.endswith('d%d' % d) and ('TRACE', g, 'cmcs_frozen') in main]
    if tr:
        ax.plot([a for a, _ in tr], [b for _, b in tr], color='#52514e', linestyle='--', linewidth=1.2, label='PARI trace alone')
    ax.set_yscale('log'); ax.set_xlabel('prime size (bits)'); ax.set_title('W1 cold single query — %s' % ('cubics' if d == 3 else 'quartics'), fontsize=10, loc='left')
axes[0].set_ylabel('median seconds per complete query (log)')
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc='lower center', ncol=4, fontsize=7.5, frameon=False, bbox_to_anchor=(0.5, 0.035))
fig.text(0.01, 0.005, 'Source: %s sha256 %s… · bands = min–max over timing blocks · one uncontrolled 2-core host' % (os.path.basename(src), SRC_SHA[:16]), fontsize=6.5, color='#52514e')
fig.tight_layout(rect=(0, 0.14, 1, 1))
fig.savefig(os.path.join(odir, 'plots', 'W1_cold_ladder.png'), dpi=160)
plt.close(fig)

# W2: total time vs Q per method, one panel per (degree, bits); colours follow the W1 figure per method
gs2 = sorted({k[1] for k in main if k[0] == 'W2'})
cls = sorted({g.rsplit('_Q', 1)[0] for g in gs2})
W2S = [  # method, label, colour (same method = same colour as in W1), line style, marker, filled
    ('cmcs_frozen', 'Cartier–Miller (frozen, incl. PARI trace)', SLOTS[0], '-', 'o', True),
    ('cmcs_frozen[trace supplied]', 'Cartier–Miller, trace supplied', SLOTS[0], '--', 'o', False),
    ('polyrec_c', 'power via recurrence (C) + Horner', SLOTS[5], '-', 'P', True),
    ('polyrec_c+multipoint', 'power via recurrence (C) + multipoint', SLOTS[5], ':', 'P', False),
    ('flint_power', 'FLINT power + Horner', SLOTS[6], '-', 'X', True),
    ('enum_conv', 'all-poles correlation (C tables + FLINT product)', '#52514e', '-', 'h', True),
    ('bgs_harvey', 'BGS – Harvey kernel (NTL), per pole', SLOTS[1], '-', 's', True),
    ('enum_c', 'enumeration (C), per pole', SLOTS[4], '-', 'v', True)]
bits2 = sorted({int(c.split('_')[0][1:]) for c in cls})
if cls:
    fig, axes = plt.subplots(2, len(bits2), figsize=(3.6 * len(bits2), 6.6), sharey=True, squeeze=False)
    for r_, d in enumerate((3, 4)):
        for c_, b in enumerate(bits2):
            ax = axes[r_][c_]
            c = 'b%02d_d%d' % (b, d)
            for m, lab, col, ls, mk, filled in W2S:
                pts = []
                for g in gs2:
                    if g.rsplit('_Q', 1)[0] == c and ('W2', g, m) in main and blocks_total.get(('W2', g, m)):
                        pts.append((int(g.rsplit('_Q', 1)[1]), med(blocks_total[('W2', g, m)])))
                pts.sort()
                if pts:
                    ax.plot([a for a, _ in pts], [y for _, y in pts], color=col, linestyle=ls, marker=mk, markersize=5,
                            linewidth=1.8, label=lab, markerfacecolor=col if filled else '#fcfcfb', markeredgecolor=col)
            ax.set_xscale('log', base=2); ax.set_yscale('log')
            ax.set_title('%s, %d-bit p' % ('cubic' if d == 3 else 'quartic', b), fontsize=9.5, loc='left')
            if r_ == 1:
                ax.set_xlabel('distinct poles Q on one prepared curve')
        axes[r_][0].set_ylabel('preparation + all Q queries (s, log)')
    hl = {}
    for row in axes:
        for ax in row:
            for h_, l_ in zip(*ax.get_legend_handles_labels()):
                hl.setdefault(l_, h_)
    order = [lab for _, lab, *_ in W2S if lab in hl]
    fig.legend([hl[k] for k in order], order, loc='lower center', ncol=4, fontsize=7.5, frameon=False, bbox_to_anchor=(0.5, 0.03))
    fig.text(0.01, 0.005, 'Source: %s sha256 %s… · medians over 5 fresh curves · missing points = budget, timeout or size ceiling (see tables) · one uncontrolled 2-core host' % (os.path.basename(src), SRC_SHA[:16]), fontsize=6.5, color='#52514e')
    fig.tight_layout(rect=(0, 0.11, 1, 1))
    fig.savefig(os.path.join(odir, 'plots', 'W2_prepared_totals.png'), dpi=160)
    plt.close(fig)
print('wrote', odir, 'groups', len(summary['groups']))
