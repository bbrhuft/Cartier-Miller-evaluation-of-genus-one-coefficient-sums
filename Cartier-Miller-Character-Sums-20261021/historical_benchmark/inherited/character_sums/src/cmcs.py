"""cmcs -- Cartier-Miller application layer for rationally weighted quadratic-character
sums and elliptic-point sums modulo p.

Candidate implementation for the 20 October 2026 investigation.  Unrefereed research
code.  Every nonbranch single-pole value is obtained from the INHERITED, UNMODIFIED
Cartier-Miller row evaluator ``cm_system.rows.RowSession`` (repository
bbrhuft/cartier-miller-evaluation-of-genus-one-coefficient-sums, commit ef23079,
directory Cartier-Miller-Integration-20261013), applied to a translated and
normalized model.  This module adds:

  * validation and explicit routing (supported / unsupported / rejected);
  * the polynomial-division bridge  C_f(mu) <-> T_f(mu)  (Theorem A of the report);
  * bounded deterministic translation + normalization with trace transfer
    tau_g = chi(f(a)) tau_f   (Proposition D);
  * common-domain exclusion corrections for several poles  (Theorem C);
  * constant terms, cubic/quartic infinity, affine and projective point sums;
  * branch poles and the bounded exploratory extensions (double poles, polynomial
    parts), which require *second-kind data* (coefficients of f^h near index p-1)
    that the Miller evaluator does not supply  (Theorems E, F);
  * an optional endpoint check [M]R+ = [M]R- that detects many wrong traces.

Outputs are elements of F_p returned as integers in [0, p).  Integer counts
(N_inf, tau, fibre sizes) are kept as integers and reduced only when they
multiply a field-valued weight.

Field-operation counts in docstrings count additions, multiplications and
inversions separately; an inversion is NOT counted as a multiplication.
"""
from dataclasses import dataclass, field
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_VENDOR = os.path.join(os.path.dirname(_HERE), 'vendor')
if _VENDOR not in sys.path:
    sys.path.insert(0, _VENDOR)

from cm_system.rows import RowSession                                  # inherited
from cm_system.backends.genus_one.curve import Model                   # inherited
from cm_system.backends.genus_one.fields import QuadCtx, FpCtx        # inherited
from cm_system.backends.genus_one.miller import (                      # inherited
    miller_alpha_resumable, miller_continue, Resume)
from cm_system.backends.cm.d7_seed import is_prime64                   # inherited

__all__ = ['Curve', 'InputError', 'UnsupportedCase', 'TraceInconsistent',
           'SecondKindMissing', 'ResourceLimit', 'chi', 'finite_parts_quadratic',
           'finite_parts_by_derivatives']


class InputError(ValueError):
    """Rejected input: outside the mathematical hypotheses or malformed."""


class UnsupportedCase(ValueError):
    """Well-posed request that this investigation does not support (routed explicitly)."""


class SecondKindMissing(UnsupportedCase):
    """Branch / second-kind request made without prepared second-kind data."""


class TraceInconsistent(ArithmeticError):
    """Supplied trace contradicted by an exact internal check."""


class ResourceLimit(ValueError):
    """Requested preparation exceeds an explicit budget (never approximated)."""

# ------------------------------------------------------------------ small helpers

def chi(a, p):
    """Quadratic character with chi(0) = 0 (Euler's criterion; O(log p) multiplications)."""
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _peval(f, x, p):
    v = 0
    for c in reversed(f):
        v = (v * x + c) % p
    return v


def _deriv(f, p):
    return [(i * f[i]) % p for i in range(1, len(f))] or [0]


def _trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def _polyrem(a, b, p):
    a, b = _trim(a), _trim(b)
    inv = pow(b[-1], -1, p)
    while len(a) >= len(b):
        q = a[-1] * inv % p
        s = len(a) - len(b)
        for j, v in enumerate(b):
            a[s + j] = (a[s + j] - q * v) % p
        a = _trim(a)
    return a


def _squarefree(f, p):
    a, b = _trim(f), _trim(_deriv(f, p))
    while b:
        a, b = b, _polyrem(a, b, p)
    return len(a) == 1


def _div_linear(a, mu, p):
    """Synthetic division a = (x - mu) q + r; returns (q, r)."""
    n = len(a) - 1
    q = [0] * max(n, 1)
    acc = 0
    for i in range(n, 0, -1):
        acc = (acc * mu + a[i]) % p
        q[i - 1] = acc
    r = (acc * mu + a[0]) % p
    return q, r


def _add(a, b, p):
    n = max(len(a), len(b))
    return [((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p for i in range(n)]


def _scale(a, c, p):
    return [x * c % p for x in a]


def _taylor_shift(f, a, p):
    """Coefficients of f(a + z) in z (Horner with polynomials; O(deg^2) operations)."""
    out = [0]
    for c in reversed(f):
        nxt = [0] * (len(out) + 1)
        for i, v in enumerate(out):          # out * (z + a)
            nxt[i + 1] = (nxt[i + 1] + v) % p
            nxt[i] = (nxt[i] + v * a) % p
        nxt[0] = (nxt[0] + c) % p
        out = nxt
    return _trim(out) or [0]


def _batch_inverse(values, p):
    """Montgomery's simultaneous inversion: 1 inversion + 3(k-1) multiplications."""
    k = len(values)
    if k == 0:
        return []
    pref = [0] * k
    acc = 1
    for i, v in enumerate(values):
        pref[i] = acc
        acc = acc * v % p
    inv = pow(acc, -1, p)
    out = [0] * k
    for i in range(k - 1, -1, -1):
        out[i] = inv * pref[i] % p
        inv = inv * values[i] % p
    return out


def validate_prime(p):
    if not _is_int(p):
        raise InputError('p must be an integer')
    if p < 7:
        raise InputError('require p >= 7 (Hasse argument and exceptional analysis use p >= 7)')
    if p >= 2**64 or not is_prime64(p):
        raise InputError('require a prime 7 <= p < 2^64 (prototype primality guard)')


def validate_polynomial(f, p):
    """Return f reduced mod p; require integer coefficients, exact degree 3 or 4, squarefree."""
    if not isinstance(f, (list, tuple)) or len(f) not in (4, 5) or not all(_is_int(c) for c in f):
        raise InputError('f must be 4 or 5 integer coefficients, low to high')
    g = [c % p for c in f]
    if g[-1] == 0:
        raise InputError('leading coefficient vanishes mod p: exact degree 3 or 4 required')
    if not _squarefree(g, p):
        raise InputError('f is not squarefree mod p (singular double cover)')
    return g


def validate_residue(x, p, name):
    if not _is_int(x):
        raise InputError(name + ' must be an integer')
    if not 0 <= x < p:
        raise InputError(name + ' must be a residue in [0, p); poles outside F_p are not accepted')
    return x

# ------------------------------------------------------------------ correction kernels

def finite_parts_quadratic(U, simple, double, poly, b, p, stats=None):
    """Finite parts R_fin(u) for u in U: every term of R except the term singular at u.

    Straightforward algorithm: for each u, one batch inversion of the differences
    (u - mu) over the pole list.  Cost: |U| inversions, O(|U| * (s + d)) multiplications,
    O(s + d) working field elements.
    """
    poles = [m for m, _ in simple] + [m for m, _ in double]
    out = {}
    for u in U:
        diffs, owners = [], []
        for idx, m in enumerate(poles):
            if m != u:
                diffs.append((u - m) % p)
                owners.append(idx)
        invs = _batch_inverse(diffs, p)
        if stats is not None:
            stats['correction_inversions'] = stats.get('correction_inversions', 0) + (1 if diffs else 0)
            stats['correction_multiplications'] = (stats.get('correction_multiplications', 0)
                                                   + 3 * max(len(diffs) - 1, 0) + 2 * len(diffs))
        val = b % p
        ns = len(simple)
        for iv, idx in zip(invs, owners):
            if idx < ns:
                val = (val + simple[idx][1] * iv) % p
            else:
                val = (val + double[idx - ns][1] * iv % p * iv) % p
        xp = 1
        for k, a in enumerate(poly):
            if k:
                xp = xp * u % p
            val = (val + a * xp) % p
        out[u] = val
    return out


def finite_parts_by_derivatives(simple, p):
    """r_k = (N'(mu_k) - a_k D''(mu_k)/2) / D'(mu_k) for R = sum a_j/(x-mu_j) = N/D.

    Implements the rational-function identity of Proposition C3 with schoolbook
    polynomial arithmetic (quadratic cost).  It verifies the identity used by a
    subproduct-tree multipoint method; it is NOT itself the fast method.
    """
    mus = [m % p for m, _ in simple]
    D = [1]
    for m in mus:
        D = _add([0] + D, _scale(D, (-m) % p, p), p)
    N = [0]
    for m, a in simple:
        Q, r = _div_linear(D, m % p, p)
        assert r == 0
        N = _add(N, _scale(Q, a % p, p), p)
    D1, D2, N1 = _deriv(D, p), _deriv(_deriv(D, p), p), _deriv(N, p)
    half = pow(2, -1, p)
    out = {}
    for m, a in simple:
        out[m % p] = (_peval(N1, m, p) - a * _peval(D2, m, p) % p * half) * pow(_peval(D1, m, p), -1, p) % p
    return out

# ------------------------------------------------------------------ prepared curve

@dataclass
class _Session:
    a: int
    g: list
    alpha: int
    trace_g: int
    row: RowSession
    model: Model


class Curve:
    """Prepared data for the double cover y^2 = f(x) over F_p.

    Reusable per (p, f): the exact trace tau, N_inf, the translated/normalized
    sessions (one per translation parameter a), and optional second-kind data.
    """

    def __init__(self, p, f, trace=None, *, trace_label=None, count_budget=200_000):
        validate_prime(p)
        self.p = p
        self.f = validate_polynomial(f, p)
        self.deg = len(self.f) - 1
        self.lead = self.f[-1]
        self.h = (p - 1) // 2
        self.chi_lead = chi(self.lead, p)
        self.n_inf = 1 if self.deg == 3 else 1 + self.chi_lead
        if trace is None:
            if p > count_budget:
                raise ResourceLimit('no trace supplied and p exceeds the direct point-count budget')
            s = sum(chi(_peval(self.f, x, p), p) for x in range(p))
            trace = 1 - self.n_inf - s                      # sum_x eps(x) = 1 - N_inf - tau
            trace_label = 'direct character count O(p log p)'
        if not _is_int(trace):
            raise InputError('trace must be an integer')
        if trace * trace > 4 * p:
            raise InputError('trace violates the Hasse bound |tau| <= 2 sqrt(p)')
        self.trace = trace
        self.trace_label = trace_label or 'caller-supplied (trusted, not certified)'
        self.fd = _deriv(self.f, p)
        self._sessions = {}
        self._reversed = None
        self.second_kind = None
        self.stats = {}

    # .............................................................. basics
    def eps(self, x):
        return chi(_peval(self.f, x % self.p, self.p), self.p)

    def is_branch(self, mu):
        return _peval(self.f, mu % self.p, self.p) == 0

    def _bump(self, key, n=1):
        self.stats[key] = self.stats.get(key, 0) + n

    # .............................................................. translation
    def choose_translation(self, excluded):
        """Least a in {0, 1, ..., deg+|excluded|} (as residues) with a notin excluded, f(a) != 0.

        Marking + scan: O(|excluded|) residue comparisons and at most deg+1 evaluations
        of f.  Falls back to a full-field scan when deg+|excluded|+1 > p; returns None
        when U together with the roots of f exhausts F_p.
        """
        p = self.p
        bound = self.deg + len(excluded) + 1
        if bound > p:
            bound = p
        marks = bytearray(bound)
        for u in excluded:
            if u < bound:
                marks[u] = 1
        for a in range(bound):
            if not marks[a] and _peval(self.f, a, p):
                return a
        for a in range(bound, p):                      # only reachable when bound was capped
            if a not in excluded and _peval(self.f, a, p):
                return a
        return None

    def session(self, a):
        """g(z) = f(a+z)/f(a), alpha = chi(f(a)), tau_g = alpha tau_f (Proposition D)."""
        if a in self._sessions:
            return self._sessions[a]
        p = self.p
        fa = _peval(self.f, a, p)
        if fa == 0:
            raise InputError('translation parameter is a root of f')
        g = _scale(_taylor_shift(self.f, a, p), pow(fa, -1, p), p)
        g = g + [0] * (len(self.f) - len(g))
        alpha = chi(fa, p)
        tg = alpha * self.trace
        row = RowSession(p, list(g), trace=tg)
        s = _Session(a, g, alpha, tg, row, row.model)
        self._sessions[a] = s
        self._bump('sessions_built')
        return s

    # .............................................................. oracle (inherited Miller)
    def oracle(self, mu, a):
        """C_f(mu) for nonbranch mu, via the inherited evaluator on g = f(a+z)/f(a).

        C_f(mu) = alpha * C_g(mu - a),  C_g(nu) = (T_g(nu) - e)/nu + e g'(nu)/(2 g(nu)),
        T_g(nu) = S_g(1/nu) from RowSession.query.  Returns (C, eps_f(mu), metadata).
        """
        p = self.p
        s = self.session(a)
        nu = (mu - a) % p
        if nu == 0:
            raise InputError('translation parameter coincides with the pole')
        lam = pow(nu, -1, p)
        res = s.row.query(lam)
        self._bump('oracle_calls')
        if res.get('split_fallback'):
            self._bump('split_fallbacks')
        if res.get('exceptional'):
            self._bump('exceptional_queries')
        if res.get('method') != 'undivided_Cartier_Miller':
            raise ArithmeticError('inherited evaluator took an unexpected route: %r' % res.get('method'))
        T, e = res['S'], res['chi']
        gv = _peval(s.g, nu, p)
        gd = _peval(_deriv(s.g, p), nu, p)
        Cg = ((T - e) * lam + e * gd * pow(2 * gv, -1, p)) % p
        return s.alpha * Cg % p, s.alpha * e, {'a': a, 'M': res['M'], 'split': res['split_fallback'],
                                                'exceptional': res['exceptional'], 'T_g': T}

    def endpoint_check(self, mu, a=None):
        """Necessary condition on the trace: [M]R+ = [M]R- for the query at mu.

        Uses inherited Miller primitives; raises TraceInconsistent on failure.  Passing
        does NOT certify the trace.
        """
        p = self.p
        if self.is_branch(mu):
            raise UnsupportedCase('endpoint check applies to nonbranch poles')
        if a is None:
            a = self.choose_translation({mu % p})
        s = self.session(a)
        nu = (mu - a) % p
        d = _peval(s.g, nu, p)
        c = chi(d, p)
        M = p + 1 - c * s.trace_g
        k = QuadCtx(p, d)
        R = s.model.to_short(k, k.fromint(nu), k.gen)
        try:
            _, T = miller_alpha_resumable(k, R, M, s.model.A)
            ok = T is None or (T[0][1] % p == 0 and T[1][1] % p == 0)
        except Resume as z:
            root = k.sqrt_from_witness(z.witness)
            F = FpCtx(p)

            def comp(e, i):
                return (e[0] + (1 if i == 0 else -1) * e[1] * root) % p
            ends = []
            for i in (0, 1):
                Ti = None if z.T is None else tuple(comp(e, i) for e in z.T)
                Ri = tuple(comp(e, i) for e in R)
                _, Te = miller_continue(F, Ri, M, s.model.A, Ti, comp(z.alpha, i), z.j)
                ends.append(Te)
            ok = ends[0] == ends[1]
        if not ok:
            raise TraceInconsistent('[M]R+ != [M]R-: supplied trace is wrong')
        return True

    # .............................................................. second-kind data
    def prepare_second_kind(self, supplied=None, budget=5_000_000):
        """Coefficients of f^h needed by branch poles and the exploratory extensions.

        low  : c_{p-1}, c_{p-2}, c_{p-3}, c_{p-4}
        top  : c_{Dh}, c_{Dh-1}, c_{Dh-2}, c_{Dh-3}   (D = deg f; only used for quartics)

        Default: streaming scaled recurrence, O(p) field operations, O(1) working
        elements, three inversions at the end.  ``supplied`` = (c_{p-1}, c_{p-2},
        c_{p-3}) is trusted; c_{p-4} is then derived from the m = p and m = p-1
        recurrence identities.  Consistency c_{p-1} = tau mod p is checked either way.
        """
        p, f, h, D = self.p, self.f, self.h, self.deg
        if supplied is not None:
            if len(supplied) != 3 or not all(_is_int(x) for x in supplied):
                raise InputError('supply three integers (c_{p-1}, c_{p-2}, c_{p-3})')
            low = [x % p for x in supplied]
            if D == 3 and (f[1] * low[0] + 2 * f[2] * low[1] + 3 * f[3] * low[2]) % p:
                raise InputError('supplied cubic data violate sum_j j f_j c_{p-j} = 0')
            low.append(self._derive_c_p_minus_4(low))
            source = 'caller-supplied (trusted)'
        else:
            if p > budget:
                raise ResourceLimit('second-kind recurrence budget exceeded')
            low = self._stream_low()
            source = 'streaming recurrence O(p)'
            # internal identity  sum_j j f_j c_{p-j} = 0
            chk = sum(j * f[j] * low[j - 1] for j in range(1, D + 1) if j <= 4) % p
            if D == 4 and chk:
                raise ArithmeticError('recurrence identity failed')
            if D == 3 and (f[1] * low[0] + 2 * f[2] * low[1] + 3 * f[3] * low[2]) % p:
                raise ArithmeticError('recurrence identity failed')
        if low[0] != self.trace % p:
            raise TraceInconsistent('c_{p-1} != tau mod p: trace or second-kind data inconsistent')
        top = self._top_coefficients()
        self.second_kind = {'low': low, 'top': top, 'source': source}
        return self.second_kind

    def _stream_low(self):
        p, f, h, D = self.p, self.f, self.h, self.deg
        if f[0] != 0:
            base, N, shift = f, p - 1, 0
        else:                                   # f = x g, f^h = x^h g^h
            base, N, shift = f[1:] + [0], h, h
            base = _trim(base)
        b0 = base[0]
        Db = len(base) - 1
        hp1 = h + 1
        u = [chi(b0, p) % p, 0, 0, 0, 0]          # u_n, ..., u_{n-4};  u_0 = c_0 = b0^h
        s_hist = [1, 0, 0, 0]                    # s_n, s_{n-1}, s_{n-2}, s_{n-3}
        for n in range(1, N + 1):
            acc = 0
            P = 1
            for j in range(1, Db + 1):
                if j > 1:
                    P = P * (n - j + 1) % p
                if j > n:
                    break
                c = ((hp1 * j - n) * base[j]) % p
                if c:
                    acc += c * pow(b0, j - 1, p) % p * P % p * u[j - 1]
            un = acc % p
            u = [un] + u[:4]
            s_hist = [s_hist[0] * n % p * b0 % p] + s_hist[:3]
        # u[i] = u_{N-i}, s_hist[i] = s_{N-i}
        invs = _batch_inverse(s_hist, p)
        coeffs = [u[i] * invs[i] % p for i in range(4)]     # c_{N}, c_{N-1}, c_{N-2}, c_{N-3} of base^h
        return coeffs                                        # = c_{p-1-i} of f in both cases

    def _derive_c_p_minus_4(self, low):
        p, f, h = self.p, self.f, self.h
        c1, c2, c3 = low
        if self.deg == 4:
            # sum_{j=1}^4 j f_j c_{p-j} = 0
            return (-(f[1] * c1 + 2 * f[2] * c2 + 3 * f[3] * c3)) * pow(4 * f[4], -1, p) % p
        # cubic: recurrence at m = p-1:  f0 (p-1) c_{p-1} = sum_j ((h+1)j-(p-1)) f_j c_{p-1-j}
        lhs = f[0] * (p - 1) % p * c1
        rhs = sum((((h + 1) * j - (p - 1)) * f[j]) % p * cc for j, cc in ((1, c2), (2, c3))) % p
        coef = (((h + 1) * 3 - (p - 1)) * f[3]) % p
        return (lhs - rhs) * pow(coef, -1, p) % p

    def _top_coefficients(self):
        """c_{Dh-i}, i = 0..3, from the reversed polynomial: (f*)^h = l^h (1 + delta)^h."""
        p, f, h, D = self.p, self.f, self.h, self.deg
        l = self.lead
        rev = list(reversed(f))                  # rev[i] = f_{D-i}
        il = pow(l, -1, p)
        delta = [0] + [rev[i] * il % p for i in range(1, min(4, len(rev)))]
        delta += [0] * (4 - len(delta))
        res = [1, 0, 0, 0]
        power = [1, 0, 0, 0]
        binom = 1
        for k in range(1, 4):
            nxt = [0, 0, 0, 0]
            for i in range(4):
                for j in range(4 - i):
                    nxt[i + j] = (nxt[i + j] + power[i] * delta[j]) % p
            power = nxt
            binom = binom * ((h - k + 1) % p) % p * pow(k, -1, p) % p
            res = [(res[i] + binom * power[i]) % p for i in range(4)]
        lh = chi(l, p) % p
        return [lh * r % p for r in res]

    def coefficient(self, k):
        """c_k = [x^k] f^h when available from prepared data; raises otherwise."""
        p, D, h = self.p, self.deg, self.h
        if k < 0 or k > D * h:
            return 0
        if self.second_kind is None:
            raise SecondKindMissing('second-kind data (coefficients near index p-1) not prepared')
        if p - 4 <= k <= p - 1:
            return self.second_kind['low'][p - 1 - k]
        if D * h - 3 <= k <= D * h:
            return self.second_kind['top'][D * h - k]
        raise UnsupportedCase('coefficient index %d is outside the prepared windows' % k)

    def _sum_eps_times(self, W):
        """sum_{x in F_p} eps(x) W(x) = -sum_{j>=1} [x^{j(p-1)}](W F) for a polynomial W."""
        p = self.p
        total = 0
        for j in (1, 2, 3):
            idx = j * (p - 1)
            if idx - (len(W) - 1) > self.deg * self.h:
                break
            total += sum(W[i] * self.coefficient(idx - i) for i in range(len(W)) if W[i])
        return (-total) % p

    # .............................................................. single-term values
    def branch_value(self, mu):
        """C_f(mu) at a branch value f(mu) = 0 (Theorem E).  O(1) field operations
        after second-kind preparation (one inversion)."""
        p = self.p
        q, r = _div_linear(self.f, mu, p)
        if r:
            raise InputError('not a branch value')
        fmu = _peval(self.fd, mu, p)
        half = pow(2, -1, p)
        num = _add(_add(_scale(self.fd, half, p), _scale(q, p - 1, p), p), [fmu * half % p], p)
        W, rr = _div_linear(num, mu, p)
        assert rr == 0
        LW = self._sum_eps_times(W)
        J = sum(q[i] * self.coefficient(2 * p - 1 - i) for i in range(len(q))) % p
        self._bump('branch_poles')
        return 2 * pow(fmu, -1, p) * (LW - J) % p

    def double_pole_value(self, mu, C=None, a=None):
        """sum_{x != mu} eps(x)/(x-mu)^2 at a nonbranch mu (Theorem F); needs C_f(mu)."""
        p = self.p
        d = _peval(self.f, mu, p)
        if d == 0:
            raise UnsupportedCase('double pole at a branch value is not supported')
        if C is None:
            if a is None:
                a = self.choose_translation({mu})
            C, _, _ = self.oracle(mu, a)
        e = chi(d, p)
        fd1 = _peval(self.fd, mu, p)
        P1, r1 = _div_linear(_add(self.fd, [(-fd1) % p], p), mu, p)
        tmp = _add(_add(self.f, [(-d) % p], p), _scale([(-mu) % p, 1], (-fd1) % p, p), p)
        Pa, ra = _div_linear(tmp, mu, p)
        P2, rb = _div_linear(Pa, mu, p)
        assert r1 == 0 and ra == 0 and rb == 0
        P = _add(_scale(P1, pow(2, -1, p), p), _scale(P2, p - 1, p), p)
        f2 = _deriv(self.fd, p)
        K0p = e * pow(4, -1, p) * (_peval(f2, mu, p) - fd1 * fd1 % p * pow(2 * d, -1, p)) % p
        topK = 0
        if self.deg == 4:
            topK = self._top_of_power_h_plus_1(mu)
        sumP = self._sum_eps_times(P)              # sum over all x
        sumP_excl = (sumP - e * _peval(P, mu, p)) % p
        self._bump('double_poles')
        return pow(d, -1, p) * (-(topK - K0p) - fd1 * pow(2, -1, p) % p * C + sumP_excl) % p

    def _top_of_power_h_plus_1(self, mu):
        """[x^{2p-1}] (f^{h+1} - const)/(x - mu) = e_{2p} + e_{2p+1} mu + e_{2p+2} mu^2 (quartic)."""
        p, f = self.p, self.f
        # f^{h+1} = f * f^h ;  e_m = sum_i f_i c_{m-i}
        def e(m):
            return sum(f[i] * self.coefficient(m - i) for i in range(5)) % p
        return (e(2 * p) + e(2 * p + 1) * mu + e(2 * p + 2) * mu * mu) % p

    def reversed_curve(self):
        """y^2 = f*(u) = u^D f(1/u) (same curve, same trace) for quartic poles at infinity."""
        if self._reversed is None:
            rev = list(reversed(self.f))
            if rev[-1] == 0:                       # f(0) = 0: reversed polynomial is a cubic
                rev = rev[:-1]
            self._reversed = Curve(self.p, rev, trace=self.trace,
                                   trace_label='transferred: u = 1/x isomorphism')
        return self._reversed

    def poly_value(self, k):
        """sum_{x in F_p} eps(x) x^k  for 0 <= k <= 3, with explicit routing."""
        p = self.p
        if k == 0:
            return (1 - self.n_inf - self.trace) % p, 'trace'
        if k == 1 and self.deg == 4:
            rc = self.reversed_curve()
            a = rc.choose_translation({0})
            C, _, _ = rc.oracle(0, a)
            self._bump('oracle_calls_reversed')
            return C, 'miller_pole_at_infinity'
        if k > 3:
            raise UnsupportedCase('polynomial parts of degree > 3 are outside the bounded extension')
        return self._sum_eps_times([0] * k + [1]), 'second_kind_data'

    def classify_pole(self, mu):
        """Admissibility class of a simple pole mu in F_p (Section 3 of the report)."""
        mu = validate_residue(mu, self.p, 'mu')
        if self.is_branch(mu):
            return 'branch: second-kind data required (coordinate-invariant)'
        if mu == 0 or self.f[0] == 0:
            return 'nonbranch: Miller oracle after translation (coordinate restriction only)'
        if self.f[0] != 1:
            return 'nonbranch: Miller oracle after normalization by f(0)'
        return 'nonbranch: Miller oracle directly (manuscript coordinates)'

    def single_pole(self, mu):
        """C_f(mu) = sum_{x != mu} eps(x)/(x-mu) for any mu in F_p (routed)."""
        mu = validate_residue(mu, self.p, 'mu')
        if self.is_branch(mu):
            return self.branch_value(mu)
        a = self.choose_translation({mu})
        return self.oracle(mu, a)[0]

    def truncation(self, mu):
        """T_f(mu) for mu in F_p^x, any admissible f (Corollary A2: polynomial-division bridge)."""
        p = self.p
        mu = validate_residue(mu, p, 'mu')
        if mu == 0:
            raise UnsupportedCase('T_f(0) = f(0)^h is trivial; the bridge needs mu != 0')
        C = self.single_pole(mu)
        d = _peval(self.f, mu, p)
        if d == 0:
            return mu * C % p
        e = chi(d, p)
        return (mu * C - mu * e % p * _peval(self.fd, mu, p) % p * pow(2 * d, -1, p) + e) % p

    # .............................................................. weighted sums
    def weighted_sum(self, simple=(), double=(), poly=(), b=0, excluded=(),
                     kind='character', check_endpoints=False):
        """Common-domain weighted sum for R = b + sum a_j/(x-mu_j) + sum c_j/(x-nu_j)^2 + sum e_k x^k.

        kind = 'character'          : sum_{x notin U} chi(f(x)) R(x)
               'affine_points'      : sum_{P affine, x(P) notin U} R(x(P))
               'projective_points'  : affine + R(infinity) * N_inf  (R regular at infinity)
        U = poles of R together with ``excluded``.  Result in F_p.
        """
        p = self.p
        if kind not in ('character', 'affine_points', 'projective_points'):
            raise InputError('unknown kind')
        if not _is_int(b):
            raise InputError('b must be an integer')
        simple = [(validate_residue(m, p, 'pole'), a) for m, a in simple]
        double = [(validate_residue(m, p, 'double pole'), a) for m, a in double]
        excluded = [validate_residue(u, p, 'excluded point') for u in excluded]
        for _, a in list(simple) + list(double):
            if not _is_int(a):
                raise InputError('coefficients must be integers')
        if not all(_is_int(a) for a in poly):
            raise InputError('polynomial coefficients must be integers')
        simple = [(m, a % p) for m, a in simple]
        double = [(m, a % p) for m, a in double]
        poly = [a % p for a in poly]
        while poly and poly[-1] == 0:
            poly.pop()
        sp = [m for m, _ in simple]
        dp = [m for m, _ in double]
        if len(set(sp)) != len(sp) or len(set(dp)) != len(dp):
            raise InputError('poles must be distinct (combine coefficients of a repeated pole)')
        if kind == 'projective_points' and len(poly) > 1:
            raise UnsupportedCase('projective sum undefined: a nonconstant polynomial part has a pole '
                                  'at the points at infinity')
        U = list(dict.fromkeys(sp + dp + excluded))
        Uset = set(U)
        route = []
        info = {'translation': None, 'oracle_calls': 0, 'branch_poles': 0, 'double_poles': 0,
                'split_fallbacks': 0, 'exceptional_queries': 0, 'second_kind_used': False}
        # Degenerate domain: U together with the roots of f covers F_p.
        needs_oracle = any(not self.is_branch(m) for m in sp + dp)
        a0 = None
        if needs_oracle:
            a0 = self.choose_translation(Uset)
            if a0 is None:
                return self._degenerate_domain(simple, double, poly, b, U, kind, info)
            info['translation'] = a0
        eps_cache = {}
        total = 0
        for m, a in simple:
            if self.is_branch(m):
                val = self.branch_value(m)
                eps_cache[m] = 0
                info['branch_poles'] += 1
                info['second_kind_used'] = True
                route.append(('simple', m, 'branch_second_kind'))
            else:
                val, e, meta = self.oracle(m, a0)
                eps_cache[m] = e
                info['oracle_calls'] += 1
                info['split_fallbacks'] += int(bool(meta['split']))
                info['exceptional_queries'] += int(bool(meta['exceptional']))
                if check_endpoints:
                    self.endpoint_check(m, a0)
                route.append(('simple', m, 'miller_exceptional' if meta['exceptional'] else 'miller'))
            total = (total + a * val) % p
        for m, a in double:
            if self.is_branch(m):
                raise UnsupportedCase('double pole at a branch value is not supported')
            C, e, meta = self.oracle(m, a0)
            info['oracle_calls'] += 1
            info['split_fallbacks'] += int(bool(meta['split']))
            info['exceptional_queries'] += int(bool(meta['exceptional']))
            val = self.double_pole_value(m, C=C)
            eps_cache[m] = e
            info['double_poles'] += 1
            info['second_kind_used'] = True
            route.append(('double', m, 'miller_plus_second_kind'))
            total = (total + a * val) % p
        for k, a in enumerate(poly):
            if a == 0:
                continue
            val, how = self.poly_value(k)
            if how == 'second_kind_data':
                info['second_kind_used'] = True
            if how == 'miller_pole_at_infinity':
                info['oracle_calls'] += 1
            route.append(('poly', k, how))
            total = (total + a * val) % p
        if b % p:
            val, _ = self.poly_value(0)
            total = (total + b * val) % p
            route.append(('constant', 0, 'trace'))
        # exclusion corrections
        for u in U:
            if u not in eps_cache:
                eps_cache[u] = self.eps(u)
        fin = finite_parts_quadratic(U, simple, double, poly, b, p, self.stats)
        corr_char = sum(eps_cache[u] * fin[u] for u in U) % p
        value = (total - corr_char) % p
        if kind != 'character':
            value = (value - sum(fin.values())) % p
            if kind == 'projective_points':
                const = (b + (poly[0] if poly else 0)) % p        # R(infinity)
                value = (value + const * self.n_inf) % p
        info['route'] = route
        info['domain_size'] = p - len(U)
        return value, info

    def _degenerate_domain(self, simple, double, poly, b, U, kind, info):
        """Domain F_p \\ U consists of roots of f only: eps = 0 and nu = 1 there."""
        p = self.p
        info['route'] = [('degenerate_domain', len(U), 'direct')]
        if kind == 'character':
            return 0, info
        Uset = set(U)
        val = 0
        for x in range(p):
            if x in Uset:
                continue
            w = b % p
            for m, a in simple:
                w = (w + a * pow(x - m, -1, p)) % p
            for m, a in double:
                w = (w + a * pow(x - m, -2, p)) % p
            for k, a in enumerate(poly):
                w = (w + a * pow(x, k, p)) % p
            val = (val + w) % p
        if kind == 'projective_points':
            val = (val + (b + (poly[0] if poly else 0)) % p * self.n_inf) % p
        return val, info


# ------------------------------------------------------------------ optional partial fractions

def _polymulmod(a, b, m, p):
    prod = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                prod[i + j] = (prod[i + j] + x * y) % p
    return _polyrem(prod, m, p) if len(prod) >= len(_trim(m)) else _trim(prod)


def _gcd(a, b, p):
    a, b = _trim(a), _trim(b)
    while b:
        a, b = b, _polyrem(a, b, p)
    if not a:
        return a
    inv = pow(a[-1], -1, p)
    return [x * inv % p for x in a]


def split_part_degree(D, p):
    """deg gcd(D, x^p - x): number of distinct roots of D in F_p (O(s^2 log p) naive)."""
    D = _trim([c % p for c in D])
    if len(D) <= 1:
        return 0
    r, base, e = [1], [0, 1], p
    while e:                                   # x^p mod D by square-and-multiply
        if e & 1:
            r = _polymulmod(r, base, D, p) or [0]
        base = _polymulmod(base, base, D, p) or [0]
        e >>= 1
    xp_minus_x = _add(r, [0, p - 1], p)
    return len(_gcd(D, xp_minus_x, p)) - 1


def partial_fractions(N, D, roots, p):
    """Decompose N/D = poly + sum a_j/(x - mu_j) given the base-field roots of D.

    Requires D to split over F_p into distinct linear factors and the full root list to
    be supplied.  Extension-field or repeated poles are routed to UnsupportedCase.
    Cost with supplied roots: O(s^2) naive (O(M(s) log s) with a subproduct tree);
    root finding itself is NOT included.
    """
    validate_prime(p)
    D = _trim([c % p for c in D])
    N = _trim([c % p for c in N]) or [0]
    if len(D) < 2:
        raise InputError('denominator must have positive degree')
    s = len(D) - 1
    roots = [validate_residue(m, p, 'root') for m in roots]
    if len(set(roots)) != len(roots):
        raise InputError('roots must be distinct')
    for m in roots:
        if _peval(D, m, p):
            raise InputError('supplied root is not a root of D')
    if len(roots) != s:
        if split_part_degree(D, p) > len(roots):
            raise InputError('D has base-field roots that were not supplied')
        raise UnsupportedCase('D has repeated or extension-field poles; only distinct base-field '
                              'simple poles are supported')
    # polynomial part: N div D
    q = [0] * max(len(N) - len(D) + 1, 1)
    r = list(N)
    inv = pow(D[-1], -1, p)
    while len(_trim(r)) >= len(D):
        r = _trim(r)
        c = r[-1] * inv % p
        sh = len(r) - len(D)
        q[sh] = c
        for j, v in enumerate(D):
            r[sh + j] = (r[sh + j] - c * v) % p
    Dd = _deriv(D, p)
    simple = [(m, _peval(N, m, p) * pow(_peval(Dd, m, p), -1, p) % p) for m in roots]
    return _trim(q), simple
