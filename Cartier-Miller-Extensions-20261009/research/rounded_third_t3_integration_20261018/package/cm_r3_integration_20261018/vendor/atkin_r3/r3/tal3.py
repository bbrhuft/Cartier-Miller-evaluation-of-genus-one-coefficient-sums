"""Rounded-third specialization of Tal's split construction (q prime, q | p-1).

Target: m! with m = (p-2)/3, hence c_p = 2 (m!)^{-3} and a_L = (3/4) c_p, signs included.

Notation: K = (p-1)/q, y_c = (cK)! (0 <= c <= q), eta of order q in F_p, J_w = J(chi, chi^w) in
Z[zeta_q] with rho(chi(x)) = x^{-K} (r3/jacobi.py).  Exact relations used (all mod p):

  Wilson   W_c  : y_c y_{q-c} = (-1)^{cK+1}                                   (1 <= c <= (q-1)/2)
  Jacobi   T_t^w: y_u y_v y_x = (-1)^{(u+v)K} / J_w(eta^t),  u=<t>, v=<tw>, x=<-t(1+w)>,
                  whenever u + v + x = q                                   (Tal 2026, eqs. (2)-(3))
  Target        : Z = m! = y_b I_m^{s_m}          (b = nearest grid index to m; |I_m| = (K-+1)/3)
  Anchor 'dup6' : (Z6/Z^2)^2 = (-1)^{(p+1)/2} 4^{1-(p+1)/3},  Z6 = ((p-5)/6)!       (all p)
                  [Gauss multiplication, M = 2 at x = 1/3; only H^2 enters]     |I_6| = (K-+4)/6
  Anchor 'dup12' (p = 5 mod 12 only), a = odd part of p = a^2 + b^2:
                  (Z/N!)^4 = a^2                     if q = +-1 mod 12   (round-2 C5, proved)
                  (Z (5N+2)!)^4 = (16 a^2)^{-1}      if q = +-5 mod 12               |I_12| = (K-+4)/12
In grid variables the anchor is one integer row (2e_b6 - 4e_b, 4e_b - 4e_b12 or 4e_b + 4e_b12).
For each (q, anchor) an integer vector lambda with lambda^T R = k e_b, k in {1,3}, is precomputed
(depends on q only).  Then y_b^k = prod val_i^{lambda_i} and Z^3 = y_b^3 I_m^{3 s_m}; cubing is a
bijection on F_p^* (p = 2 mod 3), so no root extraction is needed.  No class number is used.
"""
from functools import lru_cache
from time import perf_counter

from .jacobi import JacobiContext, evaluate
from .common import params, flint_rising, legendre


def _nearest(xq):
    """nearest integer to a rational given as (num, den)."""
    num, den = xq
    return (2 * num + den) // (2 * den)


@lru_cache(maxsize=None)
def grid(q, anchor):
    """p-independent grid indices: b (target), b_a (anchor), anchor kind and row."""
    if q < 5 or q % 2 == 0 or q % 3 == 0:
        raise ValueError('q must be a prime >= 5')
    b = _nearest((q, 3))
    if anchor == 'dup6':
        ba, kind, cb, ca = _nearest((q, 6)), 'dup6', -4, 2
    elif anchor == 'dup12':
        if q % 12 in (1, 11):
            ba, kind, cb, ca = _nearest((q, 12)), 'N', 4, -4
        else:
            ba, kind, cb, ca = _nearest((5 * q, 12)), '5N+2', 4, 4
    else:
        raise ValueError(anchor)
    row = {}
    for idx, coef in ((b, cb), (ba, ca)):          # indices may coincide (e.g. q = 5)
        row[idx] = row.get(idx, 0) + coef
    return b, ba, kind, tuple(sorted(row.items()))


def _rows(q, classes, anchor):
    b, ba, kind, arow = grid(q, anchor)
    rows = []
    for c in range(1, (q - 1) // 2 + 1):
        r = [0] * (q - 1)
        r[c - 1] += 1
        r[q - c - 1] += 1
        rows.append((('W', c), r))
    for w in classes:
        for t in range(1, q):
            u, v, x = t % q, (t * w) % q, (-t * (1 + w)) % q
            if 0 in (u, v, x) or u + v + x != q:
                continue
            r = [0] * (q - 1)
            for i in (u, v, x):
                r[i - 1] += 1
            rows.append((('T', w, t, u, v), r))
    r = [0] * (q - 1)
    for idx, coef in arow:
        r[idx - 1] += coef
    rows.append((('A',), r))
    return rows


_TABLE = []


def _table():
    if not _TABLE:
        import json
        from pathlib import Path
        f = Path(__file__).resolve().parent / 'PLANS_R3.json'
        _TABLE.append(json.loads(f.read_text())['plans'] if f.exists() else {})
    return _TABLE[0]


@lru_cache(maxsize=None)
def plan(q, anchor='dup6'):
    """(classes, k, ((row_tag, lambda_i), ...)) with lambda^T R = k e_b.  p-independent.

    Taken from the frozen table PLANS_R3.json when present (re-checked exactly in integers
    against the relation matrix, O(q^2) work), otherwise computed by an integer HNF.
    """
    ent = _table().get('%d/%s' % (q, anchor))
    if ent is None:
        return compute_plan(q, anchor)
    classes, k = tuple(ent['classes']), ent['k']
    lam = tuple((tuple(tag), l) for tag, l in ent['lam'])
    rows = dict(_rows(q, classes, anchor))
    b = grid(q, anchor)[0]
    acc = [0] * (q - 1)
    for tag, l in lam:
        for i, x in enumerate(rows[tag]):
            acc[i] += l * x
    if acc != [k if i == b - 1 else 0 for i in range(q - 1)]:
        raise ArithmeticError('frozen plan failed its integer check for q=%d' % q)
    return classes, k, lam


def compute_plan(q, anchor='dup6'):
    """Integer HNF computation of a plan (PARI mathnf)."""
    import cypari2
    P = cypari2.Pari()
    b = grid(q, anchor)[0]
    for classes in ((1,), (1, 2)):
        rows = _rows(q, classes, anchor)
        n, d = len(rows), q - 1
        M = P.matrix(d, n, [rows[j][1][i] for i in range(d) for j in range(n)])
        H, U = P.mathnf(M, 1)                       # M * U = [0 | H]
        r = int(P.matsize(H)[1])
        for k in (1, 3):
            target = P.matrix(d, 1, [k if i == b - 1 else 0 for i in range(d)])
            try:
                y = P.matsolve(H, target)
            except Exception:
                continue
            if all(P.denominator(y[i, 0]) == 1 for i in range(r)):
                full = [0] * (n - r) + [int(y[i, 0]) for i in range(r)]
                lam = [sum(int(U[j, i]) * full[i] for i in range(n)) for j in range(n)]
                for i in range(d):                  # exact integer re-check
                    if sum(lam[j] * rows[j][1][i] for j in range(n)) != (k if i == b - 1 else 0):
                        raise ArithmeticError('plan check failed')
                return classes, k, tuple((rows[j][0], lam[j]) for j in range(n) if lam[j])
    raise ArithmeticError('no plan for q=%d anchor=%s' % (q, anchor))


# ------------------------------------------------------------------ intervals
def _interval(p, a, b, engine):
    """prod_{j=a}^{b} j mod p (empty = 1)."""
    if b < a:
        return 1
    if engine == 'flint':
        (v,), _ = flint_rising(p, b - a + 1, [a])
        return v
    r = 1
    for j in range(a, b + 1):
        r = r * j % p
    return r


def _to_grid(n, c, K):
    """n! = y_c * I^s with I the product strictly between cK and n."""
    if n >= c * K:
        return (c * K + 1, n), 1
    return (n + 1, c * K), -1


def residuals(p, q, anchor):
    P = params(p)
    K = (p - 1) // q
    b, ba, kind, _ = grid(q, anchor)
    if kind == 'dup6':
        na = (p - 5) // 6
    elif kind == 'N':
        na = P['N']
    else:
        na = 5 * P['N'] + 2
    im, sm = _to_grid(P['m'], b, K)
    ia, sa = _to_grid(na, ba, K)
    lm, la = im[1] - im[0] + 1, ia[1] - ia[0] + 1
    # the nearest-grid-point lengths predicted in the docstring
    exp_m = (K - 1) // 3 if q % 3 == 1 else (K + 1) // 3
    if lm != exp_m or not (0 <= la <= K // (6 if kind == 'dup6' else 12) + 1):
        raise ArithmeticError('unexpected residual lengths (p too small for q?)')
    return dict(K=K, b=b, ba=ba, kind=kind, na=na, I_m=im, s_m=sm, I_a=ia, s_a=sa, len_m=lm, len_a=la)


def two_squares_a2(p):
    """a^2 where p = a^2 + b^2 with a odd (p = 1 mod 4); deterministic least non-residue."""
    from math import isqrt
    z = 2
    while legendre(z, p) != -1:
        z += 1
    r = pow(z, (p - 1) // 4, p)
    a0, b0 = p, min(r, p - r)
    lim = isqrt(p)
    while b0 > lim:
        a0, b0 = b0, a0 % b0
    x = b0
    y = isqrt(p - x * x)
    if x * x + y * y != p:
        raise ArithmeticError('Cornacchia failed')
    a = x if x % 2 else y
    return a * a, z


# ------------------------------------------------------------------ acquisition
def default_anchor(p):
    return 'dup12' if p % 12 == 5 else 'dup6'


def acquire(p, q, anchor=None, engine='flint', ctx=None, method='flint'):
    """Signed c_p for a certified prime p = 5 mod 6 and a prime q >= 5 dividing p-1.

    Returns (c_p, metadata) with timings split into plan, svp (incl. eta), intervals, assembly.
    """
    t0 = perf_counter()
    params(p)
    if (p - 1) % q:
        raise ValueError('q must divide p-1')
    anchor = anchor or default_anchor(p)
    if anchor == 'dup12' and p % 12 != 5:
        raise ValueError('dup12 anchor needs p = 5 mod 12')
    classes, k, lam = plan(q, anchor)
    t_plan = perf_counter()
    ctx = ctx or JacobiContext(p, q, method=method)
    Jw = {w: ctx.J(1, w) for w in classes}
    t_svp = perf_counter()
    R = residuals(p, q, anchor)
    Im = _interval(p, R['I_m'][0], R['I_m'][1], engine)
    Ia = _interval(p, R['I_a'][0], R['I_a'][1], engine)
    t_int = perf_counter()
    K, e, eta = R['K'], p - 1, ctx.eta
    sm, sa = R['s_m'], R['s_a']
    extra = {}
    if R['kind'] == 'dup6':
        cdup = (p - 1 if ((p + 1) // 2) % 2 else 1) * pow(4, (1 - (p + 1) // 3) % e, p) % p
        aval = cdup * pow(Im, (4 * sm) % e, p) * pow(Ia, (-2 * sa) % e, p) % p
    else:
        a2, z = two_squares_a2(p)
        extra = dict(qnr_used=z)
        if R['kind'] == 'N':
            aval = a2 * pow(Im, (-4 * sm) % e, p) * pow(Ia, (4 * sa) % e, p) % p
        else:
            aval = pow(16 * a2 % p, p - 2, p) * pow(Im, (-4 * sm) % e, p) * pow(Ia, (-4 * sa) % e, p) % p
    acc = 1
    for tag, li in lam:
        if tag[0] == 'W':
            val = 1 if (tag[1] * K + 1) % 2 == 0 else p - 1
        elif tag[0] == 'T':
            _, w, t, u, v = tag
            rj = evaluate(Jw[w], pow(eta, t, p), p)
            if rj == 0:
                raise ArithmeticError('zero Jacobi residue')
            val = pow(rj, p - 2, p)
            if ((u + v) * K) % 2:
                val = p - val
        else:
            val = aval
        acc = acc * pow(val, li % e, p) % p
    yb3 = pow(acc, 3 // k, p)
    Z3 = yb3 * pow(Im, (3 * sm) % e, p) % p
    c = 2 * pow(Z3, p - 2, p) % p
    t_end = perf_counter()
    meta = dict(route='tal_split_rounded_third', q=q, K=K, anchor=anchor, anchor_kind=R['kind'],
                eta=eta, eta_seed=ctx.eta_seed, classes=list(classes), k=k, lambda_terms=len(lam),
                svp=ctx.stats['svp'], enumeration_fallbacks=ctx.stats['enumeration_fallbacks'],
                residual_lengths=dict(target=R['len_m'], anchor=R['len_a']), engine=engine,
                lll=method, status='unconditional; exact', **extra,
                timings=dict(plan=t_plan - t0, svp=t_svp - t_plan, intervals=t_int - t_svp,
                             assembly=t_end - t_int, total=t_end - t0))
    return c, meta


def mfact_from_c(p, c):
    """The unique cube root of 2/c_p in F_p (p = 2 mod 3): m!."""
    x = 2 * pow(c, p - 2, p) % p
    return pow(x, (2 * p - 1) // 3, p)
