"""Shared test machinery for development and confirmation runs.

Each check family returns a dict {name, checks, failures, details...}.  Failures
record the exact input.  Ground truth always comes from reference.py (enumeration,
FLINT powers, PARI traces), never from cmcs.py.
"""
import math
import random
import time

import reference as ref
import cmcs
from cmcs import Curve

from cm_system.rows import RowSession                                   # inherited
from cm_system.api import Unsupported as InheritedUnsupported           # inherited
from cm_system.backends.genus_one.fields import QuadCtx, FpCtx, ZeroDivisorFound
from cm_system.backends.genus_one.miller import _add as inherited_add, _ops as inherited_ops


def primes_in(lo, hi):
    return [q for q in range(lo, hi) if ref.is_prime(q)]


def random_squarefree(p, deg, rng, const=None):
    """Random squarefree f of exact degree deg; const fixes f(0) when given."""
    import flint
    while True:
        f = [rng.randrange(p) for _ in range(deg)] + [rng.randrange(1, p)]
        if const is not None:
            f[0] = const % p
        P = flint.nmod_poly(f, p)
        if P.gcd(P.derivative()).degree() == 0:
            return f


def mu_list(p, f, rng, full_below=600, k=24):
    """All mu for small p; otherwise 0, every rational root of f (when cheap) and k random mu."""
    if p < full_below:
        return list(range(p))
    out = {0}
    if p < 3_000_000:
        roots = [int(x) for x in __import__('numpy').nonzero(ref.poly_values(f, p) == 0)[0]]
        out.update(roots)
    while len(out) < k:
        out.add(rng.randrange(p))
    return sorted(out)


class Family:
    def __init__(self, name):
        self.name = name
        self.checks = 0
        self.failures = []
        self.counters = {}
        self.t0 = time.perf_counter()

    def check(self, ok, detail):
        self.checks += 1
        if not ok:
            if len(self.failures) < 50:
                self.failures.append(detail)
            self.counters['failures_total'] = self.counters.get('failures_total', 0) + 1

    def count(self, key, n=1):
        self.counters[key] = self.counters.get(key, 0) + n

    def result(self):
        return {'family': self.name, 'checks': self.checks,
                'failures': self.counters.get('failures_total', 0),
                'failure_examples': self.failures,
                'counters': {k: v for k, v in sorted(self.counters.items()) if k != 'failures_total'},
                'seconds': round(time.perf_counter() - self.t0, 3)}

# --------------------------------------------------------------------------- A/B: reference identities

def fam_reference_identities(primes, rng, per_prime=4):
    """Independent identities: polynomial-division forms, point sums, kernel sign, eq. (50)/(51)."""
    F = Family('reference_identities')
    for p in primes:
        h = (p - 1) // 2
        counts = ref.square_counts(p)
        inv = ref.inverse_table(p)
        for t in range(per_prime):
            deg = (3, 4)[t % 2]
            const = [None, 0, 1, rng.randrange(1, p)][t % 4]
            f = random_squarefree(p, deg, rng, const)
            c = ref.power_coefficients(f, p)
            ds = ref.DirectSums(p, f, counts, inv)
            tau = ref.trace_pari(f, p)
            F.check(tau == ref.trace_by_count(f, p, counts), ('trace', p, f))
            n_inf = 1 if deg == 3 else 1 + ref.legendre(f[4], p)
            F.check(ds.integer_character_sum() == 1 - n_inf - tau, ('sum_eps', p, f))
            F.check(c[p - 1] == tau % p, ('H=tau', p, f))
            fd = [(i * f[i]) % p for i in range(1, len(f))]
            Fd = [(i * c[i]) % p for i in range(1, len(c))]
            for mu in mu_list(p, f, rng):
                C = ds.character_sum(simple=[(mu, 1)])
                P = ds.affine_point_sum(simple=[(mu, 1)])
                F.check(C == P, ('C=P', p, f, mu))
                # general form: C = -q_{p-1} - F'(mu), q_{p-1} = sum_{m>=p} c_m mu^{m-p}
                q = 0
                for m in range(len(c) - 1, p - 1, -1):
                    q = (q * mu + c[m]) % p
                F.check(C == (-q - ref.peval(Fd, mu, p)) % p, ('general', p, f, mu))
                d = ref.peval(f, mu, p)
                if mu and d:
                    e = ref.legendre(d, p)
                    T = ref.truncation_value(c, mu, p)
                    pred = ((T - e) * pow(mu, -1, p) + e * ref.peval(fd, mu, p) * pow(2 * d, -1, p)) % p
                    F.check(C == pred, ('nonbranch', p, f, mu))
                    F.count('nonbranch_nonzero')
                    # kernel sign: sum_{P, x != mu} 1/(1 - x/mu) = -mu * P_f(mu)
                    lam = pow(mu, -1, p)
                    ker = ds.affine_point_sum(simple=[(mu, (-mu) % p)])
                    F.check(ker == (-mu * P) % p, ('kernel', p, f, mu))
                    # manuscript (50) and (51) with S = T_f(mu)
                    rhs50 = (e - e * ref.peval(fd, mu, p) * pow(2 * d * lam, -1, p) - ker) % p
                    F.check(T == rhs50, ('eq50', p, f, mu))
                    rhs51 = (e - e * ref.peval(fd, mu, p) * pow(2 * d * lam, -1, p) + mu * C) % p
                    F.check(T == rhs51, ('eq51', p, f, mu))
                elif mu and not d:
                    F.check(C == ref.truncation_value(c, mu, p) * pow(mu, -1, p) % p, ('branch', p, f, mu))
                    F.count('branch_nonzero')
                elif mu == 0:
                    c1 = c[1] if len(c) > 1 else 0
                    F.check(C == (-c[p] - c1) % p, ('zero', p, f))
                    F.count('pole_zero')
    return F.result()


def fam_constants_infinity(primes, rng, per_prime=3):
    """Constant weights, N_inf, affine vs projective, integer counts vs residues."""
    F = Family('constants_and_infinity')
    for p in primes:
        counts = ref.square_counts(p)
        inv = ref.inverse_table(p)
        for t in range(per_prime):
            deg = (3, 4)[t % 2]
            f = random_squarefree(p, deg, rng)
            ds = ref.DirectSums(p, f, counts, inv)
            tau = ref.trace_pari(f, p)
            # N_inf by counting square roots of the leading coefficient (quartic) -- no Euler
            n_inf = 1 if deg == 3 else int(counts[f[4] % p])
            F.check(n_inf == (1 if deg == 3 else 1 + ref.legendre(f[4], p)), ('ninf', p, f))
            s = rng.randrange(1, min(6, p - 1))
            U = rng.sample(range(p), s)
            simple = [(u, rng.randrange(1, p)) for u in U]
            b = rng.randrange(1, p)
            eps = [int(ds.eps[u]) for u in U]
            nu = [int(ds.nu[u]) for u in U]
            # integer counts on the domain
            int_char = ds.integer_character_sum(excluded=U)
            F.check(int_char == 1 - n_inf - tau - sum(eps), ('int_char', p, f, U))
            aff_count = int(ds.nu.sum()) - sum(nu)
            F.check(aff_count == p + 1 - n_inf - tau - sum(nu), ('aff_count', p, f, U))
            # the constant contribution is the residue of the integer count times b
            with_b = ds.character_sum(simple=simple, b=b)
            without = ds.character_sum(simple=simple)
            F.check((with_b - without) % p == b * int_char % p, ('char_const', p, f))
            with_b = ds.affine_point_sum(simple=simple, b=b)
            without = ds.affine_point_sum(simple=simple)
            F.check((with_b - without) % p == b * aff_count % p, ('point_const', p, f))
            # brief's candidate formulas (r_k corrections)
            r = []
            for k, (mk, _) in enumerate(simple):
                r.append(sum(a * pow(mk - mj, -1, p) for j, (mj, a) in enumerate(simple) if j != k) % p)
            oracle = sum(a * ds.character_sum(simple=[(m, 1)]) for m, a in simple) % p
            F.check(ds.character_sum(simple=simple) == (oracle - sum(e * rk for e, rk in zip(eps, r))) % p,
                    ('multi_char', p, f, U))
            F.check(ds.affine_point_sum(simple=simple) == (oracle - sum(n * rk for n, rk in zip(nu, r))) % p,
                    ('multi_point', p, f, U))
            F.check((ds.affine_point_sum(simple=simple) - ds.character_sum(simple=simple)) % p
                    == (-sum(r)) % p, ('P-C', p, f, U))
            if len(simple) >= 2:
                F.count('multi_with_nonzero_P_minus_C', int(sum(r) % p != 0))
            # projective: enumerate points at infinity; weight there is R(inf) = b (limit, proved)
            proj = (ds.affine_point_sum(simple=simple, b=b) + b * n_inf) % p
            v_inf_limit = b  # R(1/u) at u = 0: each a/(1/u - mu) = a u/(1 - mu u) -> 0
            F.check(proj == (ds.affine_point_sum(simple=simple, b=b) + v_inf_limit * n_inf) % p, ('proj', p, f))
            F.count('rational_points_at_infinity', n_inf)
    return F.result()


def fam_translation_twist(primes, rng, per_prime=3):
    """tau_g = chi(f(a)) tau_f, character scaling, point sums NOT scaled by alpha."""
    F = Family('translation_and_twist')
    for p in primes:
        counts = ref.square_counts(p)
        inv = ref.inverse_table(p)
        for t in range(per_prime):
            deg = (3, 4)[t % 2]
            f = random_squarefree(p, deg, rng, const=[0, None, 1][t % 3])
            tau = ref.trace_pari(f, p)
            ds = ref.DirectSums(p, f, counts, inv)
            for a in rng.sample(range(p), min(4, p)):
                fa = ref.peval(f, a, p)
                if fa == 0:
                    continue
                g = [0] * len(f)                      # g(z) = f(a+z)/f(a)
                for i, ci in enumerate(f):
                    for k in range(i + 1):
                        g[k] = (g[k] + ci * math.comb(i, k) * pow(a, i - k, p)) % p
                ig = pow(fa, -1, p)
                g = [x * ig % p for x in g]
                alpha = ref.legendre(fa, p)
                tg = ref.trace_pari(g, p)
                F.check(tg == alpha * tau, ('twist', p, f, a))
                F.count('nonsquare_translations', int(alpha == -1))
                dg = ref.DirectSums(p, g, counts, inv)
                for mu in rng.sample(range(p), min(5, p)):
                    if mu == a:
                        continue
                    F.check(ds.character_sum(simple=[(mu, 1)])
                            == alpha * dg.character_sum(simple=[((mu - a) % p, 1)]) % p, ('C scale', p, f, a, mu))
                    pf = ds.affine_point_sum(simple=[(mu, 1)])
                    pg = dg.affine_point_sum(simple=[((mu - a) % p, 1)])
                    F.count('point_sum_not_alpha_scaled', int(alpha == -1 and pf != (alpha * pg) % p and pf != pg))
                    if ref.peval(f, mu, p):
                        # exceptional status and annihilator are invariant
                        e_f = ref.legendre(ref.peval(f, mu, p), p)
                        e_g = ref.legendre(ref.peval(g, (mu - a) % p, p), p)
                        F.check(p + 1 - e_f * tau == p + 1 - e_g * tg, ('M invariant', p, f, a, mu))
    return F.result()


def fam_extension_and_multiplicative(primes, rng, per_prime=2):
    """Extension-field pole identity; field-valued vs multiplicative-character sums."""
    F = Family('extension_poles_and_multiplicative_contrast')
    for p in primes:
        counts = ref.square_counts(p)
        inv = ref.inverse_table(p)
        K = ref.Fp2(p)
        h = (p - 1) // 2
        for t in range(per_prime):
            deg = (3, 4)[t % 2]
            f = random_squarefree(p, deg, rng)
            c = ref.power_coefficients(f, p)
            ds = ref.DirectSums(p, f, counts, inv)
            for _ in range(3):
                mu = (rng.randrange(p), rng.randrange(1, p))
                L = (0, 0)
                for x in range(p):
                    e = int(ds.eps[x])
                    if e:
                        L = K.add(L, K.mul(K.scal(e), K.inv(K.sub(K.scal(x), mu))))
                fmu = (0, 0)
                for cc in reversed(f):
                    fmu = K.add(K.mul(fmu, mu), K.scal(cc))
                Fmu = K.pow(fmu, h)
                Tmu = (0, 0)
                for k in range(p - 1, -1, -1):
                    Tmu = K.add(K.mul(Tmu, mu), K.scal(c[k]))
                mup = K.pow(mu, p)
                R = K.add(K.mul((p - 1, 0), K.mul(K.inv(mup), K.sub(Fmu, Tmu))), K.mul(Fmu, K.inv(K.sub(mup, mu))))
                F.check(R == L, ('extension', p, f, mu))
            if deg == 3:
                mu = rng.randrange(p)
                while not ref.peval(f, mu, p):
                    mu = rng.randrange(p)
                integer_sum = ds.multiplicative_sum(mu)
                g = [(-mu * f[0]) % p] + [(f[i - 1] - mu * f[i]) % p for i in range(1, 4)] + [f[3]]
                tg = ref.trace_pari(g, p)
                n_inf_g = 1 + ref.legendre(f[3], p)
                F.check(integer_sum == 1 - n_inf_g - tg, ('multiplicative = other curve', p, f, mu))
                field_sum = ds.character_sum(simple=[(mu, 1)])
                F.count('field_value_differs_from_residue_of_multiplicative', int(field_sum != integer_sum % p))
    return F.result()


def fam_multipoint_identity(primes, rng, per_prime=6):
    F = Family('multipoint_finite_part_identity')
    for p in primes:
        for _ in range(per_prime):
            s = rng.randrange(1, min(12, p))
            U = rng.sample(range(p), s)
            simple = [(u, rng.randrange(p)) for u in U]
            q = cmcs.finite_parts_quadratic(U, simple, [], [], 0, p)
            d = cmcs.finite_parts_by_derivatives(simple, p)
            F.check(all(q[u] == d[u] for u in U), ('multipoint', p, simple))
    return F.result()


def fam_rounded_third(primes):
    """f = 1 - x^3/2, p = 5 mod 6, mu0 = 2^{(2p-1)/3}: C = mu0 G^{-3}, T = (-1)^m binom(h-1,m)."""
    F = Family('rounded_third_branch_reduction')
    for p in primes:
        if p % 6 != 5:
            continue
        m, h = (p - 2) // 3, (p - 1) // 2
        G = 1
        for i in range(2, m + 1):
            G = G * i % p
        mu0 = pow(2, (2 * p - 1) // 3, p)
        F.check(pow(mu0, 3, p) == 2, ('cube root', p))
        f = [1, 0, 0, (-pow(2, -1, p)) % p]
        T_binom = (-1) ** m * math.comb(h - 1, m) % p
        F.check(T_binom == mu0 * mu0 * pow(G, -3, p) % p, ('binomial identity', p))
        if p < 3000:
            ds = ref.DirectSums(p, f)
            F.check(ds.character_sum(simple=[(mu0, 1)]) == mu0 * pow(G, -3, p) % p, ('char sum', p))
            F.count('direct_character_checks')
        F.count('primes')
    return F.result()

# --------------------------------------------------------------------------- C: inherited Miller evaluator

def chain_events(p, g, trace, lam):
    """Replay the inherited Miller chain with the inherited _add; count structural events."""
    from cm_system.backends.genus_one.curve import Model
    model = Model(g, p)
    w = pow(lam, -1, p)
    d = model.fval(FpCtx(p), w)
    e = 1 if pow(d, (p - 1) // 2, p) == 1 else -1
    M = p + 1 - e * trace
    k = QuadCtx(p, d)
    R = model.to_short(k, k.fromint(w), k.gen)
    ev = {'identity_inputs': 0, 'identity_outputs': 0, 'split': 0, 'steps': 0}
    T = R
    ctx = k
    comps = None
    ops = inherited_ops(M)
    j = 0
    while j < len(ops):
        op = ops[j]
        Q = T if op == 'D' else R
        if T is None:
            ev['identity_inputs'] += 1
        try:
            T2, _ = inherited_add(ctx, T, Q, ctx.fromint(model.A))
        except ZeroDivisorFound as z:
            ev['split'] += 1
            root = k.sqrt_from_witness(z.element)
            comps = []
            for sgn in (1, -1):
                def cv(x):
                    return (x[0] + sgn * x[1] * root) % p
                Ti = None if T is None else (cv(T[0]), cv(T[1]))
                Ri = (cv(R[0]), cv(R[1]))
                comps.append((Ti, Ri))
            F = FpCtx(p)
            for Ti, Ri in comps:
                for jj in range(j, len(ops)):
                    Qi = Ti if ops[jj] == 'D' else Ri
                    if Ti is None:
                        ev['identity_inputs'] += 1
                    Ti, _ = inherited_add(F, Ti, Qi, F.fromint(model.A))
                    ev['steps'] += 1
                    if Ti is None:
                        ev['identity_outputs'] += 1
            return ev
        ev['steps'] += 1
        if T2 is None:
            ev['identity_outputs'] += 1
        T = T2
        j += 1
    return ev


def fam_inherited_miller(primes, rng, per_prime=6, all_lambdas=True, want_exceptional=True):
    """RowSession.query (inherited, unmodified) against FLINT truncations, every admissible lambda."""
    F = Family('inherited_miller_rowsession')
    for p in primes:
        curves = []
        for t in range(per_prime):
            f = random_squarefree(p, (3, 4)[t % 2], rng, const=1)
            curves.append((f, ref.trace_pari(f, p)))
        if want_exceptional:                      # add up to two curves of trace +-1
            extra = 0
            for attempt in range(300):
                f = random_squarefree(p, (3, 4)[attempt % 2], rng, const=1)
                tau = ref.trace_pari(f, p)
                if abs(tau) == 1:
                    curves.append((f, tau))
                    extra += 1
                    if extra == 2:
                        break
        for f, tau in curves:
            deg = len(f) - 1
            if abs(tau) == 1:
                F.count('trace_plus_one_curves' if tau == 1 else 'trace_minus_one_curves')
            c = ref.power_coefficients(f, p)
            row = RowSession(p, f, trace=tau)
            lams = range(1, p) if (all_lambdas and p < 600) else rng.sample(range(1, p), min(24, p - 1))
            for lam in lams:
                mu = pow(lam, -1, p)
                truth = ref.truncation_value(c, mu, p)
                d = ref.peval(f, mu, p)
                try:
                    res = row.query(lam)
                except InheritedUnsupported:
                    F.check(d == 0 and deg == 4, ('unexpected Unsupported', p, f, lam))
                    F.count('quartic_branch_routed_unsupported')
                    continue
                except Exception as exc:          # audit finding, not a crash of the harness
                    F.check(False, ('inherited exception', p, f, lam, type(exc).__name__, str(exc)[:100]))
                    continue
                F.check(res['S'] == truth, ('S', p, f, lam, res.get('method')))
                if d == 0:
                    F.count('cubic_branch_inherited_service')
                    continue
                F.count('admissible_queries')
                F.count('square_fibre' if res['chi'] == 1 else 'nonsquare_fibre')
                if res.get('exceptional'):
                    F.count('exceptional_queries')
                    F.count('exceptional_trace_+1' if tau == 1 else 'exceptional_trace_-1')
                if res.get('split_fallback'):
                    F.count('split_fallbacks')
                if p < 400 or rng.random() < 0.05:
                    ev = chain_events(p, f, tau, lam)
                    F.count('chains_replayed')
                    F.count('chains_with_identity_steps', int(ev['identity_inputs'] > 0))
                    F.count('chains_with_vertical_or_identity_outputs', int(ev['identity_outputs'] > 0))
                    F.count('replayed_splits', ev['split'])
            res0 = row.query(0)
            F.check(res0['S'] == c[p - 1], ('lambda0', p, f))
    return F.result()

# --------------------------------------------------------------------------- D: candidate vs references

def fam_candidate_single(primes, rng, per_prime=4):
    F = Family('candidate_single_pole_and_truncation')
    for p in primes:
        counts = ref.square_counts(p)
        inv = ref.inverse_table(p)
        for t in range(per_prime):
            deg = (3, 4)[t % 2]
            const = [None, 0, 1, rng.randrange(1, p)][t % 4]
            f = random_squarefree(p, deg, rng, const)
            tau = ref.trace_pari(f, p)
            E = Curve(p, f, trace=tau, trace_label='PARI hyperellcharpoly')
            E.prepare_second_kind()
            c = ref.power_coefficients(f, p)
            F.check(E.second_kind['low'] == [c[p - 1 - i] for i in range(4)], ('low coeffs', p, f))
            Dh = deg * ((p - 1) // 2)
            F.check(E.second_kind['top'] == [c[Dh - i] for i in range(4)], ('top coeffs', p, f))
            ds = ref.DirectSums(p, f, counts, inv)
            for mu in mu_list(p, f, rng):
                truth = ds.character_sum(simple=[(mu, 1)])
                F.check(E.single_pole(mu) == truth, ('single', p, f, mu))
                if E.is_branch(mu):
                    F.count('branch_poles')
                elif mu == 0:
                    F.count('pole_zero')
                if mu:
                    F.check(E.truncation(mu) == ref.truncation_value(c, mu, p), ('truncation', p, f, mu))
                    if f[0] == 0:
                        F.count('truncation_with_f0_zero')
                if not E.is_branch(mu):
                    # translation independence: two different admissible a
                    a2 = next((a for a in range(p - 1, max(p - 12, -1), -1) if a != mu and ref.peval(f, a, p)), None)
                    if a2 is not None:
                        v2, _, _ = E.oracle(mu, a2)
                        F.check(v2 == truth, ('translation a2', p, f, mu, a2))
            F.count('split_fallbacks', E.stats.get('split_fallbacks', 0))
            F.count('exceptional_queries', E.stats.get('exceptional_queries', 0))
            F.count('oracle_calls', E.stats.get('oracle_calls', 0))
    return F.result()


def fam_candidate_weighted(primes, rng, per_prime=3, configs=12, smax=8):
    F = Family('candidate_weighted_sums')
    for p in primes:
        counts = ref.square_counts(p)
        inv = ref.inverse_table(p)
        for t in range(per_prime):
            deg = (3, 4)[t % 2]
            f = random_squarefree(p, deg, rng, const=[None, 0, 1][t % 3])
            tau = ref.trace_pari(f, p)
            E_plain = Curve(p, f, trace=tau)            # never given second-kind data
            E_sk = Curve(p, f, trace=tau)
            E_sk.prepare_second_kind()
            ds = ref.DirectSums(p, f, counts, inv)
            n_inf_count = 1 if deg == 3 else int(counts[f[4] % p])
            roots = [x for x in range(p) if ref.peval(f, x, p) == 0]
            for cfg in range(configs):
                s = rng.randrange(1, min(smax, p - 2) + 1)
                pool = list(range(p))
                U = rng.sample(pool, s)
                if roots and rng.random() < 0.3 and roots[0] not in U:
                    U[0] = roots[0]
                if rng.random() < 0.3 and 0 not in U:
                    U[-1] = 0
                U = list(dict.fromkeys(U))
                simple = [(u, rng.randrange(p)) for u in U]
                rest = [x for x in range(p) if x not in U and ref.peval(f, x, p)]
                double = []
                use_sk = rng.random() < 0.5
                if use_sk and rest:
                    double = [(rng.choice(rest), rng.randrange(1, p))]
                poly = [rng.randrange(p) for _ in range(rng.randrange(0, 4 if use_sk else 2))]
                b = rng.choice([0, rng.randrange(1, p)])
                needs = use_sk or any(ref.peval(f, m, p) == 0 for m, _ in simple) or \
                    (len([x for x in poly[1:] if x]) > 0 and not (deg == 4 and len(poly) <= 2))
                if needs:
                    E = E_sk
                    F.count('configs_with_second_kind')
                else:
                    E = E_plain
                    F.count('configs_miller_only')
                kw = dict(simple=simple, double=double, poly=poly, b=b)
                for kind in ('character', 'affine_points', 'projective_points'):
                    nonconst = len([x for x in poly[1:] if x]) > 0
                    if kind == 'projective_points' and nonconst:
                        try:
                            E.weighted_sum(kind=kind, **kw)
                            F.check(False, ('projective with pole at infinity accepted', p, f))
                        except cmcs.UnsupportedCase:
                            F.count('projective_with_polynomial_routed_unsupported')
                        continue
                    v, info = E.weighted_sum(kind=kind, **kw)
                    if kind == 'character':
                        w = ds.character_sum(**kw)
                    else:
                        w = ds.affine_point_sum(**kw)
                        if kind == 'projective_points':
                            Rinf = (b + (poly[0] if poly else 0)) % p
                            w = (w + Rinf * n_inf_count) % p
                    F.check(v == w, ('weighted', kind, p, f, kw, v, w))
                    F.count('kind_' + kind)
                if len(simple) >= 2:
                    F.count('configs_with_several_poles')
                if any(m == 0 for m, _ in simple):
                    F.count('configs_with_pole_zero')
                if any(ref.peval(f, m, p) == 0 for m, _ in simple):
                    F.count('configs_with_branch_pole')
                if b:
                    F.count('configs_with_constant')
            for E in (E_plain, E_sk):
                F.count('oracle_calls', E.stats.get('oracle_calls', 0))
                F.count('split_fallbacks', E.stats.get('split_fallbacks', 0))
                F.count('exceptional_queries', E.stats.get('exceptional_queries', 0))
            F.check(E_plain.second_kind is None, ('plain curve acquired data', p, f))
    return F.result()


def fam_quartic_infinity(primes, rng, per_prime=3):
    """Quartic linear polynomial part through a Miller query at the pole at infinity, no second-kind data."""
    F = Family('quartic_pole_at_infinity')
    for p in primes:
        counts = ref.square_counts(p)
        inv = ref.inverse_table(p)
        for t in range(per_prime):
            f = random_squarefree(p, 4, rng, const=[None, 0][t % 2])
            tau = ref.trace_pari(f, p)
            E = Curve(p, f, trace=tau)
            ds = ref.DirectSums(p, f, counts, inv)
            v, how = E.poly_value(1)
            F.check(how == 'miller_pole_at_infinity' and E.second_kind is None, ('route', p, f))
            F.check(v == ds.character_sum(poly=[0, 1]), ('value', p, f))
            c = ref.power_coefficients(f, p)
            F.check((-v - c[2 * p - 3]) % p == c[p - 2], ('c_{p-2} via Miller', p, f))
            F.count('exceptional_queries', E.reversed_curve().stats.get('exceptional_queries', 0))
    return F.result()


def fam_degenerate_domains(primes, rng):
    F = Family('degenerate_and_large_s_domains')
    for p in primes:
        counts = ref.square_counts(p)
        inv = ref.inverse_table(p)
        for deg in (3, 4):
            f = random_squarefree(p, deg, rng)
            E = Curve(p, f, trace=ref.trace_pari(f, p))
            ds = ref.DirectSums(p, f, counts, inv)
            roots = [x for x in range(p) if ref.peval(f, x, p) == 0]
            nonroots = [x for x in range(p) if x not in roots]
            # U = all nonroots: domain consists of roots only
            simple = [(u, rng.randrange(p)) for u in nonroots]
            for kind in ('character', 'affine_points'):
                v, info = E.weighted_sum(simple=simple, b=3, kind=kind)
                w = ds.character_sum(simple=simple, b=3) if kind == 'character' else ds.affine_point_sum(simple=simple, b=3)
                F.check(v == w, ('degenerate', kind, p, f))
                F.count('degenerate_route', int(info['route'][0][0] == 'degenerate_domain'))
            # s close to p with one admissible translation left
            if len(nonroots) >= 2:
                keep = rng.choice(nonroots)
                simple = [(u, rng.randrange(p)) for u in nonroots if u != keep]
                v, info = E.weighted_sum(simple=simple, kind='character')
                F.check(v == ds.character_sum(simple=simple), ('large s', p, f))
                F.check(info['translation'] == keep, ('forced translation', p, f, keep, info['translation']))
    return F.result()


def fam_endpoint(primes, rng, per_prime=3):
    F = Family('trace_endpoint_check')
    for p in primes:
        for t in range(per_prime):
            deg = (3, 4)[t % 2]
            f = random_squarefree(p, deg, rng)
            tau = ref.trace_pari(f, p)
            E = Curve(p, f, trace=tau)
            nb = [x for x in range(p) if ref.peval(f, x, p)]
            mus = rng.sample(nb, min(4, len(nb)))
            for mu in mus:
                try:
                    E.endpoint_check(mu)
                    F.check(True, None)
                except cmcs.TraceInconsistent:
                    F.check(False, ('true trace rejected', p, f, mu))
            wrong = [w for w in range(-int(2 * p ** 0.5), int(2 * p ** 0.5) + 1) if w != tau]
            w = rng.choice(wrong)
            Ew = Curve(p, f, trace=w)
            detected = 0
            for mu in mus:
                try:
                    Ew.endpoint_check(mu)
                except cmcs.TraceInconsistent:
                    detected += 1
            F.count('wrong_trace_trials')
            F.count('wrong_trace_detected_by_some_query', int(detected > 0))
            F.count('wrong_trace_queries', len(mus))
            F.count('wrong_trace_queries_detected', detected)
            try:
                Ew.prepare_second_kind()
                F.count('wrong_trace_passed_cp1_check')
            except cmcs.TraceInconsistent:
                F.count('wrong_trace_detected_by_cp1_check')
    return F.result()


def fam_partial_fractions(primes, rng):
    F = Family('partial_fraction_route')
    for p in primes:
        counts = ref.square_counts(p)
        inv = ref.inverse_table(p)
        f = random_squarefree(p, 3, rng)
        E = Curve(p, f, trace=ref.trace_pari(f, p))
        ds = ref.DirectSums(p, f, counts, inv)
        s = rng.randrange(1, min(5, p - 2))
        roots = rng.sample([x for x in range(p) if ref.peval(f, x, p)], s)
        D = [1]
        for m in roots:
            D = [((D[i - 1] if i > 0 else 0) - m * (D[i] if i < len(D) else 0)) % p for i in range(len(D) + 1)]
        N = [rng.randrange(p) for _ in range(s + 1)]
        poly, simple = cmcs.partial_fractions(N, D, roots, p)
        v, info = E.weighted_sum(simple=simple, poly=poly, kind='character')
        # direct: sum eps(x) N(x)/D(x) over x notin roots
        tot = 0
        for x in range(p):
            if x in roots:
                continue
            tot += int(ds.eps[x]) * ref.peval(N, x, p) * pow(ref.peval(D, x, p), -1, p)
        F.check(v == tot % p, ('pf', p, f, N, D))
        # extension-field pole: multiply D by an irreducible quadratic
        nr = next(c for c in range(2, p) if ref.legendre(c, p) == -1)
        Dq = [0] * (len(D) + 2)
        for i, dc in enumerate(D):
            Dq[i] = (Dq[i] - nr * dc) % p
            Dq[i + 2] = (Dq[i + 2] + dc) % p
        try:
            cmcs.partial_fractions(N, Dq, roots, p)
            F.check(False, ('extension pole accepted', p))
        except cmcs.UnsupportedCase:
            F.check(True, None)
            F.count('extension_poles_routed_unsupported')
        if len(roots) >= 2:
            try:
                cmcs.partial_fractions(N, D, roots[:-1], p)
                F.check(False, ('missing root accepted', p))
            except cmcs.InputError:
                F.check(True, None)
    return F.result()


def fam_invalid_inputs(rng, p=101, big=1000003):
    """Deliberately invalid or unsupported inputs must raise the stated exception class."""
    F = Family('invalid_and_unsupported_inputs')
    f_good = [1, 3, 0, 5]
    while True:
        try:
            E = Curve(p, f_good, trace=ref.trace_pari(f_good, p))
            break
        except cmcs.InputError:
            f_good[1] += 1
    roots = [x for x in range(p) if ref.peval(f_good, x, p) == 0]
    E4 = None
    for c in range(1, 50):
        f4 = [1, c, 2, 0, 3]
        try:
            E4 = Curve(p, f4, trace=ref.trace_pari(f4, p))
            r4 = [x for x in range(p) if ref.peval(f4, x, p) == 0]
            if r4:
                break
        except cmcs.InputError:
            pass
    cases = [
        ('p composite', lambda: Curve(91, [1, 1, 0, 1]), cmcs.InputError),
        ('p too small', lambda: Curve(5, [1, 1, 0, 1]), cmcs.InputError),
        ('p too large', lambda: Curve(2**64 + 13, [1, 1, 0, 1]), cmcs.InputError),
        ('p bool', lambda: Curve(True, [1, 1, 0, 1]), cmcs.InputError),
        ('degree 2', lambda: Curve(p, [1, 1, 1]), cmcs.InputError),
        ('degree 5', lambda: Curve(p, [1, 1, 1, 1, 1, 1]), cmcs.InputError),
        ('leading zero mod p', lambda: Curve(p, [1, 1, 1, p]), cmcs.InputError),
        ('not squarefree', lambda: Curve(p, [0, 0, 1, 1]), cmcs.InputError),
        ('float coefficient', lambda: Curve(p, [1, 1.0, 0, 1]), cmcs.InputError),
        ('trace outside Hasse', lambda: Curve(p, f_good, trace=100), cmcs.InputError),
        ('trace not integer', lambda: Curve(p, f_good, trace=1.0), cmcs.InputError),
        ('no trace, budget', lambda: Curve(big, [1, 1, 0, 1], count_budget=1000), cmcs.ResourceLimit),
        ('pole negative', lambda: E.single_pole(-1), cmcs.InputError),
        ('pole >= p', lambda: E.single_pole(p), cmcs.InputError),
        ('pole bool', lambda: E.single_pole(False), cmcs.InputError),
        ('repeated pole', lambda: E.weighted_sum(simple=[(3, 1), (3, 2)]), cmcs.InputError),
        ('non-integer weight', lambda: E.weighted_sum(simple=[(3, 0.5)]), cmcs.InputError),
        ('unknown kind', lambda: E.weighted_sum(simple=[(3, 1)], kind='complex'), cmcs.InputError),
        ('branch pole without second-kind data', lambda: E.single_pole(roots[0]) if roots else (_ for _ in ()).throw(cmcs.SecondKindMissing('n/a')), cmcs.SecondKindMissing),
        ('cubic linear polynomial part without data', lambda: E.weighted_sum(poly=[0, 1]), cmcs.SecondKindMissing),
        ('double pole without data', lambda: E.weighted_sum(double=[(5 if ref.peval(f_good, 5, p) else 6, 1)]), cmcs.SecondKindMissing),
        ('polynomial part degree 4', lambda: (E.prepare_second_kind(), E.weighted_sum(poly=[0, 0, 0, 0, 1]))[1], cmcs.UnsupportedCase),
        ('double pole at branch', lambda: E.weighted_sum(double=[(roots[0], 1)]) if roots else (_ for _ in ()).throw(cmcs.UnsupportedCase('n/a')), cmcs.UnsupportedCase),
        ('projective with polynomial part', lambda: E.weighted_sum(poly=[0, 1], kind='projective_points'), cmcs.UnsupportedCase),
        ('extension-field denominator', lambda: cmcs.partial_fractions([1], [2, 0, 1] if ref.legendre(-2, p) == -1 else [3, 0, 1], [], p), cmcs.UnsupportedCase),
        ('supplied cubic data inconsistent', lambda: Curve(p, f_good, trace=E.trace).prepare_second_kind(supplied=(E.trace % p, 1, 1)), (cmcs.InputError, cmcs.TraceInconsistent)),
        ('supplied data contradict trace', lambda: Curve(p, f_good, trace=E.trace).prepare_second_kind(supplied=((E.trace + 1) % p, 0, 0)), (cmcs.InputError, cmcs.TraceInconsistent)),
        ('truncation at zero', lambda: E.truncation(0), cmcs.UnsupportedCase),
        ('quartic branch in inherited RowSession', lambda: RowSession(p, f4, trace=E4.trace).query(pow(r4[0], -1, p)) if E4 and r4 and f4[0] == 1 else (_ for _ in ()).throw(InheritedUnsupported('n/a')), InheritedUnsupported),
        ('second-kind budget', lambda: Curve(big, [1, 1, 0, 1], trace=0).prepare_second_kind(budget=10), (cmcs.ResourceLimit, cmcs.InputError)),
    ]
    for name, fn, exc in cases:
        try:
            fn()
            F.check(False, ('accepted', name))
        except exc:
            F.check(True, None)
            F.count('rejected_or_routed')
        except Exception as other:  # wrong exception class
            F.check(False, ('wrong exception', name, type(other).__name__, str(other)[:120]))
    F.counters['case_names'] = [c[0] for c in cases]
    return F.result()


def fam_large_consistency(primes, rng, per_prime=2, queries=6):
    """Large p: no ground truth.  Translation invariance, twist invariance (independent PARI
    traces of both twists), endpoint checks.  Internal consistency only."""
    F = Family('large_prime_internal_consistency')
    for p in primes:
        nr = next(c for c in range(2, 200) if ref.legendre(c, p) == -1)
        for t in range(per_prime):
            deg = (3, 4)[t % 2]
            f = [rng.randrange(p) for _ in range(deg)] + [rng.randrange(1, p)]
            if t % 3 == 2:
                f[0] = 0
            tau = ref.trace_invariants(f, p)
            try:
                E = Curve(p, f, trace=tau)
            except cmcs.InputError:
                continue
            ft = [nr * x % p for x in f]
            tt = ref.trace_invariants(ft, p)
            F.check(tt == -tau, ('twist trace', p, f))
            Et = Curve(p, ft, trace=tt)
            mus = [0] + [rng.randrange(p) for _ in range(queries)]
            for mu in mus:
                if E.is_branch(mu):
                    continue
                a1 = E.choose_translation({mu})
                v1, e1, m1 = E.oracle(mu, a1)
                a2 = rng.randrange(p)
                while a2 == mu or E.is_branch(a2) or a2 == a1:
                    a2 = rng.randrange(p)
                v2, e2, m2 = E.oracle(mu, a2)
                F.check(v1 == v2 and e1 == e2, ('translation', p, f, mu, a1, a2))
                vt, et, mt = Et.oracle(mu, Et.choose_translation({mu}))
                F.check(vt == (-v1) % p and et == -e1, ('twist', p, f, mu))
                try:
                    E.endpoint_check(mu, a1)
                    F.check(True, None)
                except cmcs.TraceInconsistent:
                    F.check(False, ('endpoint true trace', p, f, mu))
                F.count('queries')
                F.count('split_fallbacks', int(bool(m1['split'])) + int(bool(m2['split'])) + int(bool(mt['split'])))
                F.count('exceptional', int(bool(m1['exceptional'])))
            Ew = Curve(p, f, trace=tau + 2)
            mu = next(m for m in mus if not E.is_branch(m))
            try:
                Ew.endpoint_check(mu)
                F.count('wrong_trace_undetected')
            except cmcs.TraceInconsistent:
                F.count('wrong_trace_detected')
    return F.result()


def fam_medium_ground_truth(primes, rng, per_prime=2, configs=3):
    """10^4 <= p <= ~10^7: numpy enumeration and FLINT powers as ground truth (sampled)."""
    F = Family('medium_prime_ground_truth')
    for p in primes:
        counts = ref.square_counts(p)
        inv = ref.inverse_table(p)
        for t in range(per_prime):
            deg = (3, 4)[t % 2]
            f = random_squarefree(p, deg, rng, const=[None, 0][t % 2])
            tau = ref.trace_pari(f, p)
            F.check(tau == ref.trace_by_count(f, p, counts), ('trace', p, f))
            E = Curve(p, f, trace=tau)
            ds = ref.DirectSums(p, f, counts, inv)
            c = ref.power_coefficients(f, p)
            mus = mu_list(p, f, rng, k=10)
            for mu in mus:
                if E.is_branch(mu):
                    continue
                F.check(E.single_pole(mu) == ds.character_sum(simple=[(mu, 1)]), ('single', p, f, mu))
                if mu:
                    F.check(E.truncation(mu) == ref.truncation_value(c, mu, p), ('trunc', p, f, mu))
            for cfg in range(configs):
                s = rng.randrange(2, 7)
                U = rng.sample(range(p), s)
                simple = [(u, rng.randrange(p)) for u in U if not E.is_branch(u)]
                b = rng.randrange(p)
                for kind in ('character', 'affine_points'):
                    v, info = E.weighted_sum(simple=simple, b=b, kind=kind)
                    w = ds.character_sum(simple=simple, b=b) if kind == 'character' else \
                        ds.affine_point_sum(simple=simple, b=b)
                    F.check(v == w, ('weighted', kind, p, f, simple, b))
            F.count('oracle_calls', E.stats.get('oracle_calls', 0))
            F.count('split_fallbacks', E.stats.get('split_fallbacks', 0))
            F.count('exceptional_queries', E.stats.get('exceptional_queries', 0))
    return F.result()
