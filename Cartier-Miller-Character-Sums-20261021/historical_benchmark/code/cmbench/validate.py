"""cmbench.validate -- exact validation suite (development or confirmation mode).

python3 -I -m-free usage:  python3 -I code/run_validate.py --mode development|confirmation ...
Every check compares exact residues; nothing here is timed.  Counts are checks, not curves.

Families
  T  trace provider (PARI ellap on cubic model / quartic Jacobian E_{I,J}) vs direct point count
  S  single-pole matched output: every system-Python method vs the supplied direct enumeration
     (all a for small p, including a = 0 and branch poles for trace-free methods)
  B  branch poles through the frozen candidate with prepared second-kind data
  M  medium/large p consensus (no enumeration): methods must agree with each other
  X  exceptional traces (+-1): small-p search and large-p CM constructions; voloch_semaev route
  W  multi-pole common-domain sums: adapter vs direct, frozen weighted_sum vs adapter, zero
     coefficients as extra exclusions, constant terms with sum_eps from H for trace-free methods
  K  corrections: review counterexamples, cmcs_v2 behaviours, resonance algebra
"""
import json
import os
import sys
import time

from . import core, cases, methods as M

SYS_METHODS = ['cmcs_frozen', 'enum_c', 'enum_conv', 'linrec_py', 'linrec_c', 'flint_power',
               'polyrec_c', 'bgs07']


def _ref():
    return M.LinrecPy.ref()


class Ledger:
    def __init__(self):
        self.counts, self.failures = {}, []

    def ok(self, key, cond, detail=None):
        self.counts[key] = self.counts.get(key, 0) + 1
        if not cond:
            self.failures.append({'check': key, 'detail': detail})

    def bump(self, key, n=1):
        self.counts[key] = self.counts.get(key, 0) + n


def family_T(L, rng, primes):
    for p in primes:
        for d in (3, 4):
            kinds = ['generic', 'zero_const'] + (['lead_square', 'lead_nonsquare'] if d == 4 else [])
            for kind in kinds:
                f = cases.random_curve(rng, p, d, kind)
                t1, t2 = M.trace_by_count(p, f), M.TraceProvider.trace(p, f)
                L.ok('T.trace_vs_count.d%d' % d, t1 == t2, (p, f, t1, t2))


def family_S(L, rng, primes, all_a_below=120, sample=24):
    R = _ref()
    for p in primes:
        for d in (3, 4):
            kinds = ['generic', 'zero_const', 'unit_const'] + (['lead_nonsquare'] if d == 4 else [])
            for kind in kinds:
                f = cases.random_curve(rng, p, d, kind)
                eps, fib, inv = R.character_tables(f, p)
                tr = M.trace_by_count(p, f)
                st = {}
                for name in SYS_METHODS:
                    cls = M.REGISTRY[name]
                    st[name] = cls.prepare(p, f, trace=tr) if name == 'cmcs_frozen' else cls.prepare(p, f)
                A = list(range(p)) if p < all_a_below else sorted(set([0] + rng.sample(range(p), sample)))
                ref = {a: R.direct_single(eps, inv, a, p) for a in A}
                for name in SYS_METHODS:
                    cls = M.REGISTRY[name]
                    for a in A:
                        if name == 'cmcs_frozen' and eps[a] == 0:
                            continue
                        try:
                            v = cls.query(st[name], a)
                        except Exception as e:      # recorded, never silently skipped
                            v = 'EXC ' + repr(e)
                        L.ok('S.%s.%s' % (name, 'branch' if eps[a] == 0 else ('zero_pole' if a == 0 else 'nonbranch')),
                             v == ref[a], (p, f, a, v, ref[a]))
                    if name in ('flint_power', 'polyrec_c'):
                        vb = cls.query_many(st[name], A)
                        for a, v in zip(A, vb):
                            L.ok('S.%s.multipoint' % name, v == ref[a], (p, f, a, v, ref[a]))
                    if name == 'enum_conv':
                        L.bump('S.enum_conv.tables_built')
                # every method's own route to sum_x chi(f(x)) mod p (constant terms of weighted sums)
                se_ref = sum(eps) % p
                for name in ('cmcs_frozen', 'enum_c', 'enum_conv', 'flint_power', 'polyrec_c'):
                    L.ok('S.%s.sum_eps' % name, M.REGISTRY[name].sum_eps(st[name]) == se_ref, (p, f))
                for name in ('linrec_c', 'bgs07'):
                    x0 = A[-1]
                    cval, Hval = M.REGISTRY[name].query_with_H(st[name], x0)
                    L.ok('S.%s.query_with_H.value' % name, cval == ref[x0], (p, f, x0))
                    L.ok('S.%s.query_with_H.sum_eps' % name, cases.sum_eps_from_H(p, f, Hval) == se_ref, (p, f, x0))
                # constant-term input H from the same reversed recurrence (index N+1) == trace mod p
                g0 = core.reversed_shift(f, A[0], p)
                H = R.coefficient_scaled(g0, (p - 1) // 2, core.N_index(p, d) + 1, p)
                L.ok('S.H_from_reversed_index_N+1', H == tr % p, (p, f, H, tr))
                L.ok('S.sum_eps_from_H', cases.sum_eps_from_H(p, f, H) == sum(eps) % p, (p, f))


def family_B(L, rng, primes):
    R = _ref()
    for p in primes:
        for d in (3, 4):
            f = cases.random_curve(rng, p, d, 'generic')
            roots = [x for x in range(p) if core.peval(f, x, p) == 0]
            if not roots:
                continue
            tr = M.trace_by_count(p, f)
            E = M.CmcsFrozen.prepare(p, f, trace=tr)
            E.prepare_second_kind()
            eps, fib, inv = R.character_tables(f, p)
            for a in roots:
                L.ok('B.cmcs_frozen.branch_with_second_kind', E.single_pole(a) == R.direct_single(eps, inv, a, p), (p, f, a))


def family_M(L, rng, specs):
    """specs: list of (p, d).  Consensus of independent methods where enumeration is infeasible."""
    for p, d in specs:
        f = cases.random_curve(rng, p, d, 'generic')
        tr = M.TraceProvider.trace(p, f)
        E = M.CmcsFrozen.prepare(p, f, trace=tr)
        for a in [cases.random_pole(rng, p, f) for _ in range(3)] + ([0] if core.peval(f, 0, p) else []):
            vals = {'cmcs_frozen': E.single_pole(a)}
            if p < 2 * 10 ** 8:
                vals['linrec_c'] = M.LinrecC.cold(p, f, a)
            if p < 2 * 10 ** 7:
                vals['polyrec_c'] = M.PolyrecC.cold(p, f, a)
            if p < 10 ** 10:
                vals['bgs07'] = M.BGS07.cold(p, f, a)
            if len(vals) >= 2:
                L.ok('M.consensus.%dmethods' % len(vals), len(set(vals.values())) == 1, (p, f, a, vals))
            else:
                L.bump('M.no_independent_reference (cmcs only; translation consistency below)')
            # translation invariance of the frozen candidate (two different translation parameters)
            a1 = E.choose_translation({a})
            a2 = next(x for x in range(a1 + 1, a1 + 20) if x != a and core.peval(f, x, p))
            L.ok('M.cmcs_translation_consistency', E.oracle(a, a1)[0] == E.oracle(a, a2)[0], (p, f, a))


def family_X(L, rng, small_primes, cm_specs):
    R = _ref()
    # small p: exhaustive search for trace +-1 curves among random draws
    for p in small_primes:
        found = 0
        for _ in range(4000):
            d = rng.choice((3, 4))
            f = cases.random_curve(rng, p, d, 'generic')
            tr = M.trace_by_count(p, f)
            if tr not in (1, -1):
                continue
            found += 1
            eps, fib, inv = R.character_tables(f, p)
            E = M.CmcsFrozen.prepare(p, f, trace=tr)
            for a in range(p):
                if eps[a] == 0:
                    continue
                ref = R.direct_single(eps, inv, a, p)
                L.ok('X.small.cmcs', E.single_pole(a) == ref, (p, f, a))
                if eps[a] == tr:
                    L.ok('X.small.voloch_semaev.d%d.tau%+d' % (d, tr), M.VolochSemaev.value(p, f, a) == ref, (p, f, a))
                else:
                    L.bump('X.small.regular_point_on_exceptional_curve')
            if found >= 6:
                break
    # large p: CM-constructed curves with trace +-1, cubic and quartic models
    pari = M.TraceProvider.pari()
    for bits, D, j, want in cm_specs:
        p, f0 = cases.cm_trace_pm1_curve(rng, bits, D, j, want, pari)
        f3 = cases.scramble_cubic(rng, p, f0)
        f4 = cases.cubic_to_quartic(rng, p, f3)
        for f in (f3, f4):
            tr = M.TraceProvider.trace(p, f)
            L.ok('X.cm.trace_preserved', tr == want, (p, f, tr, want))
            E = M.CmcsFrozen.prepare(p, f, trace=tr)
            n_exc = 0
            for _ in range(40):
                a = cases.random_pole(rng, p, f)
                if core.legendre(core.peval(f, a, p), p) != tr:
                    continue
                v1 = E.single_pole(a)
                v2 = M.VolochSemaev.value(p, f, a)
                vals = {'cmcs_frozen': v1, 'voloch_semaev': v2}
                if p < 10 ** 10:
                    vals['bgs07'] = M.BGS07.cold(p, f, a)
                L.ok('X.cm.agree.d%d.D%d.tau%+d.%dmethods' % (len(f) - 1, D, tr, len(vals)),
                     len(set(vals.values())) == 1, (p, f, a, vals))
                n_exc += 1
                if n_exc >= 3:
                    break


def family_W(L, rng, primes):
    R = _ref()
    for p in primes:
        for d in (3, 4):
            f = cases.random_curve(rng, p, d, 'generic')
            eps, fib, inv = R.character_tables(f, p)
            tr = M.trace_by_count(p, f)
            E = M.CmcsFrozen.prepare(p, f, trace=tr)
            single = {a: R.direct_single(eps, inv, a, p) for a in range(p)}
            H = tr % p
            se = cases.sum_eps_from_H(p, f, H)
            for s in (1, 2, 3, 5, 8):
                if s > p - 6:
                    continue
                poles = rng.sample(range(p), s)
                weights = [rng.randrange(p) for _ in poles]
                if s > 1:
                    weights[rng.randrange(s)] = 0           # zero coefficient = extra exclusion
                b = rng.randrange(p)
                char, aff = cases.weighted_from_scalars(single, {a: eps[a] for a in poles}, poles, weights, b, se, p)
                L.ok('W.adapter_vs_direct.character', char == R.direct_weighted(eps, inv, poles, weights, b, p))
                L.ok('W.adapter_vs_direct.affine', aff == R.direct_weighted(fib, inv, poles, weights, b, p))
                simple = [(a, v) for a, v in zip(poles, weights) if v]
                excl = [a for a, v in zip(poles, weights) if not v]
                if any(eps[a] == 0 for a, _ in simple):
                    E.prepare_second_kind()
                vc, _ = E.weighted_sum(simple=simple, b=b, excluded=excl)
                va, _ = E.weighted_sum(simple=simple, b=b, excluded=excl, kind='affine_points')
                L.ok('W.cmcs_frozen_vs_adapter.character', vc == char, (p, f, poles, weights, b))
                L.ok('W.cmcs_frozen_vs_adapter.affine', va == aff, (p, f, poles, weights, b))


def family_K(L, rng):
    """Corrections: review counterexamples, corrected variant, resonance algebra."""
    R = _ref()
    from .cmcs_v2 import make_curve2_class
    Curve2 = make_curve2_class()
    cm = M.cmcs_module()
    # K1 complete common domain: p = 7, f = 1 + x + x^3, R = 1/(x - 1), U = {1, 2}
    p, f = 7, [1, 1, 0, 1]
    eps, fib, inv = R.character_tables(f, p)
    E = cm.Curve(p, f, trace=M.trace_by_count(p, f))
    L.ok('K1.single_pole_value_is_0', E.single_pole(1) == 0, E.single_pole(1))
    full = R.direct_weighted(eps, inv, [1, 2], [1, 0], 0, p)
    L.ok('K1.common_domain_U12_is_6', full == 6, full)
    L.ok('K1.frozen_weighted_sum_with_excluded_2', E.weighted_sum(simple=[(1, 1)], excluded=[2])[0] == 6)
    E2 = Curve2(p, f, trace=M.trace_by_count(p, f))
    L.ok('K1.v2_weighted_sum_U', E2.weighted_sum_U([1, 2], {1: 1, 2: 0})[0] == 6)
    # K2 projective scope: p = 7, f = 1 + 3x^4, N_inf = 0
    p, f = 7, [1, 0, 0, 0, 3]
    L.ok('K2.squarefree', core.squarefree(f, p))
    L.ok('K2.N_inf_is_0', core.n_infinity(f, p) == 0)
    eps, fib, inv = R.character_tables(f, p)
    aff = sum(fib[x] * x for x in range(p)) % p
    L.ok('K2.sum_x_over_E_is_0', aff == 0, aff)
    tr = M.trace_by_count(p, f)
    E = cm.Curve(p, f, trace=tr)
    try:
        E.weighted_sum(poly=[0, 1], kind='projective_points')
        frozen = 'accepted'
    except cm.UnsupportedCase:
        frozen = 'rejected'
    L.ok('K2.frozen_rejects (documented strict API)', frozen == 'rejected')
    E2 = Curve2(p, f, trace=tr)
    E2.prepare_second_kind()
    v2, _ = E2.weighted_sum(poly=[0, 1], kind='projective_points')
    L.ok('K2.v2_projective_equals_affine_0', v2 == aff, v2)
    # random N_inf = 0 quartics: v2 projective polynomial sums vs direct affine sums
    for p in (11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        f = cases.random_curve(rng, p, 4, 'lead_nonsquare')
        eps, fib, inv = R.character_tables(f, p)
        E2 = Curve2(p, f, trace=M.trace_by_count(p, f))
        E2.prepare_second_kind()
        for k in (1, 2, 3):
            poly = [0] * k + [1]
            v2, _ = E2.weighted_sum(poly=poly, b=3, kind='projective_points')
            direct = sum(fib[x] * (3 + pow(x, k, p)) for x in range(p)) % p
            L.ok('K2.v2_projective_poly_deg%d' % k, v2 == direct, (p, f, k))
    # K3 endpoint from the chain (V2-2): equals the frozen oracle; detects wrong traces
    for p in (101, 211, 307, 401, 1009):
        for d in (3, 4):
            f = cases.random_curve(rng, p, d)
            tr = M.trace_by_count(p, f)
            E2 = Curve2(p, f, trace=tr)
            for _ in range(10):
                a = cases.random_pole(rng, p, f)
                a0 = E2.choose_translation({a})
                L.ok('K3.oracle_checked_equals_oracle', E2.oracle_checked(a, a0)[0] == E2.oracle(a, a0)[0])
            bad = tr + 2 if (tr + 2) ** 2 <= 4 * p else tr - 2
            Eb = Curve2(p, f, trace=bad)
            det_chain = det_old = 0
            for _ in range(10):
                a = cases.random_pole(rng, p, f)
                a0 = Eb.choose_translation({a})
                try:
                    Eb.oracle_checked(a, a0)
                except cm.TraceInconsistent:
                    det_chain += 1
                try:
                    Eb.endpoint_check(a, a0)
                except cm.TraceInconsistent:
                    det_old += 1
            L.ok('K3.chain_endpoint_detection_equals_rerun_detection', det_chain == det_old, (det_chain, det_old))
            L.bump('K3.wrong_trace_queries', 10)
            L.bump('K3.wrong_trace_detected', det_chain)
    # K4 resonance algebra: leading coefficients of Delta(S) = f S' + f' S / 2 (exact, symbolic in k)
    for p in (7, 11, 13, 101, 1009):
        h = (p - 1) // 2
        # branch pole: coefficient (1/2 - k) f'(mu) vanishes iff k = (p+1)/2 mod p
        bad = [k for k in range(1, 2 * p) if (pow(2, -1, p) - k) % p == 0]
        L.ok('K4.branch_resonance_at_(p+1)/2', bad[0] == (p + 1) // 2, (p, bad[:2]))
        # nonbranch: -(k-1) f(mu) vanishes iff k = 1 mod p (first k >= 2: p + 1)
        bad = [k for k in range(2, 2 * p + 2) if (k - 1) % p == 0]
        L.ok('K4.nonbranch_first_resonance_p+1', bad[0] == p + 1)
        # polynomial part: l (j + D/2) vanishes iff j = -D/2 mod p: cubic (p-3)/2, quartic p-2
        L.ok('K4.cubic_poly_resonance', [j for j in range(p) if (2 * j + 3) % p == 0][0] == (p - 3) // 2)
        L.ok('K4.quartic_poly_resonance', [j for j in range(p) if (j + 2) % p == 0][0] == p - 2)
        # identity at the branch resonance: (x-mu)^(-(p+1)/2) = chi(x-mu)/(x-mu) for x != mu
        mu = 3 % p
        ok = all(pow((x - mu) % p, -((p + 1) // 2), p) == core.legendre(x - mu, p) * pow(x - mu, -1, p) % p
                 for x in range(p) if x != mu)
        L.ok('K4.branch_resonance_weight_is_character_weight', ok)


def run(mode, out_path, seed, quick=False):
    L = Ledger()
    t0 = time.time()
    rng = cases.rng_for(seed, mode)
    if mode == 'development':
        small = [q for q in range(7, 140) if core.is_prime_small(q)]
        medium = [211, 331, 499, 1009, 2003, 4001, 8009]
        tracep = small + [1009, 2003]
        mspecs = [(10 ** 5 + 3, 3), (10 ** 5 + 3, 4), (10 ** 6 + 3, 3), (10 ** 6 + 3, 4), (10 ** 7 + 19, 3),
                  (10 ** 7 + 19, 4), (10 ** 9 + 7, 3), (10 ** 9 + 7, 4), (2 ** 61 - 1, 3), (10 ** 18 + 9, 4)]
        cm_specs = [(24, -3, 0, 1), (24, -11, -32768, -1), (30, -19, -884736, 1), (30, -43, -884736000, -1),
                    (40, -67, -147197952000, 1), (61, -163, -262537412640768000, -1), (62, -11, -32768, 1)]
        xsmall = [101, 131, 151, 181]
        wprimes = [11, 13, 23, 31, 53, 101]
    else:
        # confirmation: hash-seeded primes disjoint from development lists and inherited primes
        dev = set([q for q in range(7, 140) if core.is_prime_small(q)] + [211, 331, 499, 1009, 2003, 4001, 8009,
                  10 ** 5 + 3, 10 ** 6 + 3, 10 ** 7 + 19, 10 ** 9 + 7, 2 ** 61 - 1, 10 ** 18 + 9, 101, 131, 151, 181])
        ex = dev | cases.INHERITED_PRIMES
        small = sorted(set(cases.random_prime(rng, 140, 600, ex) for _ in range(14)))
        medium = sorted(set(cases.random_prime(rng, 600, 12000, ex) for _ in range(7)))
        tracep = small + medium[:3]
        mspecs = [(cases.random_prime(rng, lo, 2 * lo, ex), d) for lo in (10 ** 5, 10 ** 6, 10 ** 7, 10 ** 9, 10 ** 12, 10 ** 17)
                  for d in (3, 4)]
        cm_specs = [(26, -3, 0, -1), (27, -19, -884736, 1), (28, -11, -32768, 1), (32, -19, -884736, -1),
                    (34, -43, -884736000, 1), (44, -67, -147197952000, -1), (63, -163, -262537412640768000, 1)]
        xsmall = sorted(set(cases.random_prime(rng, 140, 400, ex) for _ in range(4)))
        wprimes = sorted(set(cases.random_prime(rng, 140, 300, ex) for _ in range(4)))
    sel = {'small': small, 'medium': medium, 'trace': tracep, 'mspecs': mspecs, 'cm_specs': cm_specs,
           'xsmall': xsmall, 'wprimes': wprimes}
    timings = {}

    def _run(name, fn, *args):
        t = time.time()
        fn(L, rng, *args)
        timings[name] = round(time.time() - t, 1)
        print('[validate] %s done in %.1f s; checks so far %d; failures %d'
              % (name, timings[name], sum(L.counts.values()), len(L.failures)), file=sys.stderr, flush=True)

    _run('T', family_T, tracep)
    _run('S', family_S, small + medium)
    _run('B', family_B, [q for q in small if q > 20][:10])
    _run('M', family_M, mspecs)
    _run('X', family_X, xsmall, cm_specs)
    _run('W', family_W, wprimes)
    if mode == 'development':
        _run('K', family_K)
    res = {'mode': mode, 'seed': str(seed), 'selection': sel, 'counts': L.counts,
           'total_checks': sum(L.counts.values()), 'failures': L.failures[:200],
           'n_failures': len(L.failures), 'status': 'PASS' if not L.failures else 'FAIL',
           'elapsed_s': round(time.time() - t0, 1), 'family_seconds': timings, 'python': sys.version}
    if out_path:
        with open(out_path, 'w') as fh:
            json.dump(res, fh, indent=1, default=str)
    return res
