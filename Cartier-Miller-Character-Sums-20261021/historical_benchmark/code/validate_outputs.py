"""Exact post-hoc validation of every timed output (outside all timers).

python3 -I validate_outputs.py RESULTS_DIR

Reference policy (recorded per output):
  'direct'      p < 2^14: the supplied pure-Python direct enumeration (handover reference)
  'consensus'   at least two method FAMILIES returned the same residue and no method disagreed:
                families = miller {cmcs_frozen*}, prior {voloch_semaev}, coefficient {linrec_*,
                polyrec_c*, flint_power*, bgs07, bgs_harvey}, enumeration {enum_c, enum_conv}
  'internal'    only one family ran (e.g. cmcs at > 41 bits): post-hoc checks only - the frozen
                oracle with a second translation parameter must agree, and the corrected variant's
                chain-endpoint test must pass.  Labelled 'internal consistency only'.
  'mismatch'    any disagreement (all are reported).
"""
import csv
import glob
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cmbench import core, cases, methods as M  # noqa: E402


def family(m):
    if m.startswith('cmcs'):
        return 'miller'
    if m.startswith('voloch'):
        return 'prior'
    if m.startswith('enum'):
        return 'enumeration'
    return 'coefficient'


def main(rdir):
    R = M.LinrecPy.ref()
    from cmbench.cmcs_v2 import make_curve2_class
    Curve2 = make_curve2_class()
    cm = M.cmcs_module()
    # pools: keys 'W:group'.  The main run was interrupted by a host restart before writing its pools;
    # cases_regenerated.json is the deterministic regeneration (resume_after_restart.py).  Any error in
    # the regeneration would surface below as mismatches against direct enumeration and consensus.
    pools = {}
    for fn in glob.glob(os.path.join(rdir, 'cases_*.json')):
        for g, v in json.load(open(fn)).items():
            pools.setdefault(g, v)
    w7 = os.path.join(rdir, 'w7_pools.json')
    if os.path.exists(w7):
        for g, v in json.load(open(w7)).items():
            pools.setdefault('W7:' + g, v)
    outs = defaultdict(dict)        # (workload, group) -> method -> record
    odir = os.path.join(rdir, 'outputs')
    for fn in glob.glob(os.path.join(odir, '**', '*.json'), recursive=True):
        rel = os.path.relpath(fn, odir)[:-5]          # group ids containing '/' became subdirectories
        W, rest = rel.split('__', 1)
        g = rest[:rest.rindex('__')]
        rec = json.load(open(fn))
        outs[(W, g)][rec['method']] = rec
    summary, mismatches = {}, []
    direct_cache = {}

    def direct(p, f, a):
        key = (p, tuple(f))
        if key not in direct_cache:
            direct_cache[key] = R.character_tables(f, p)
        eps, fib, inv = direct_cache[key]
        return R.direct_single(eps, inv, a, p)

    for (W, g), recs in sorted(outs.items()):
        # ---------------- map outputs to items
        items = defaultdict(dict)   # item key -> method -> value
        meta = {}
        if W in ('W1', 'W7', 'TRACE'):
            pool = (pools.get(W + ':' + g) or {}).get('pool', [])
            for m, rec in recs.items():
                Rr = rec.get('R') or 1
                for b, blk in enumerate(rec.get('outputs') or []):
                    for i, v in enumerate(blk):
                        idx = b * Rr + i
                        items[idx][m] = v
                        meta[idx] = pool[idx][:3]
        else:
            spec = pools.get(W + ':' + g, {})
            blocks = spec.get('blocks', [])
            for m, rec in recs.items():
                for b, blk in enumerate(rec.get('outputs') or []):
                    for i, v in enumerate(blk):
                        items[(b + 1, i)][m] = v          # main blocks start at 1 (block 0 = pilot)
                        bl = blocks[b + 1]
                        meta[(b + 1, i)] = (bl['p'], bl['f'], bl['poles'][i] if 'poles' in bl and W in ('W2', 'W5', 'W6') else None)
        # ---------------- validate
        for key, mv in items.items():
            p, f, a = meta[key]
            vals = set(mv.values())
            fams = set(family(m) for m in mv)
            if W == 'TRACE':
                tr = list(mv.values())[0]
                ok = tr * tr <= 4 * p
                if p < (1 << 16):
                    ok = ok and tr == M.trace_by_count(p, f)
                    how = 'direct count'
                else:
                    how = 'Hasse bound; downstream cmcs outputs validated'
                for m in mv:
                    summary.setdefault((W, g, m), defaultdict(int))[how if ok else 'mismatch'] += 1
                continue
            if a is not None and p < (1 << 14):
                ref = direct(p, f, a)
                for m, v in mv.items():
                    st = 'direct' if v == ref else 'mismatch'
                    summary.setdefault((W, g, m), defaultdict(int))[st] += 1
                    if st == 'mismatch':
                        mismatches.append({'W': W, 'g': g, 'm': m, 'p': p, 'f': f, 'a': a, 'v': v, 'ref': ref})
                continue
            if len(vals) > 1:
                for m, v in mv.items():
                    summary.setdefault((W, g, m), defaultdict(int))['mismatch'] += 1
                mismatches.append({'W': W, 'g': g, 'p': p, 'f': f, 'a': a, 'values': mv})
                continue
            if len(fams) >= 2:
                for m in mv:
                    summary.setdefault((W, g, m), defaultdict(int))['consensus'] += 1
                continue
            # single family: internal consistency (only meaningful for single-pole items)
            if a is not None and fams == {'miller'}:
                tr = M.TraceProvider.trace(p, f)
                E = Curve2(p, f, trace=tr)
                a1 = E.choose_translation({a})
                a2 = next(x for x in range(a1 + 1, a1 + 40) if x != a and core.peval(f, x, p))
                v1 = E.oracle(a, a1)[0]
                v2 = E.oracle_checked(a, a2)[0]
                st = 'internal' if (v1 == v2 == list(vals)[0]) else 'mismatch'
            else:
                st = 'single_family_unchecked'
            for m in mv:
                summary.setdefault((W, g, m), defaultdict(int))[st] += 1
    rows = [{'workload': W, 'group': g, 'method': m, **dict(c)} for (W, g, m), c in sorted(summary.items())]
    json.dump({'rows': rows, 'mismatches': mismatches[:500], 'n_mismatches': len(mismatches)},
              open(os.path.join(rdir, 'output_validation.json'), 'w'), indent=1)
    tot = defaultdict(int)
    for r in rows:
        for k, v in r.items():
            if k not in ('workload', 'group', 'method'):
                tot[k] += v
    print('validated outputs by status:', dict(tot), 'mismatch records:', len(mismatches))
    # annotate the CSV
    vmap = {(r['workload'], r['group'], r['method']): ('mismatch' if r.get('mismatch') else
            '+'.join(sorted(k for k in r if k not in ('workload', 'group', 'method')))) for r in rows}
    src = os.path.join(rdir, 'timing_samples.csv')
    rows_csv = list(csv.reader(open(src)))
    hdr = rows_csv[0]
    vi = hdr.index('validation')
    for row in rows_csv[1:]:
        if row[vi] == 'pending':
            row[vi] = vmap.get((row[1], row[2], row[3]), 'no_outputs')
    with open(os.path.join(rdir, 'timing_samples_validated.csv'), 'w', newline='') as fh:
        csv.writer(fh).writerows(rows_csv)


if __name__ == '__main__':
    main(sys.argv[1])
