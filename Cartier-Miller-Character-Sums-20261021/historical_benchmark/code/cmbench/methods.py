"""cmbench.methods -- named implementations returning the matched residue C_f(a).

Each method exposes the same contract:
    prepare(p, f, trace=None) -> state      (data legitimately reusable for fixed (p, f))
    query(state, a) -> int in [0, p)        (one C_f(a))
    query_many(state, A) -> list            (several poles; may batch, e.g. multipoint)
    cold(p, f, a) -> int                    (complete first query: everything charged)
and a contract dict naming supplied data, newly acquired data and preparation.

Methods (all written for this package unless marked inherited/published):
  cmcs_frozen     inherited frozen candidate cmcs.Curve (UNCHANGED source, imported from the
                  verified archive); trace from TraceProvider (PARI ellap), charged in cold mode
  enum_c          native C enumeration: squares bitmap + blockwise batch inversion, O(p) per query
  enum_conv       all-poles enumeration: one FLINT convolution of chi(f(x)) with 1/t, O(M(p))
  linrec_py       supplied O(p) reversed-coefficient recurrence (handover reference, unchanged)
  linrec_c        native C port of the same recurrence (separately named)
  flint_power     FLINT truncated power (rev f)^h mod z^(N+1) -> H_high; Horner per query or
                  FLINT fmpz_mod_poly multipoint evaluation for batches
  bgs_harvey      genuine BGS-type interval products: D. Harvey's published hypellfrob kernel
                  (NTL; Harvey 2007 Thm 10, based on BGS 2007), via passagemath-ntl 10.8.13; runs
                  in a separate interpreter (cmbench.harvey_worker)
  bgs07           this package's transparent BGS (2007) implementation (python-flint + numpy)
  voloch_semaev   prior-work route for the exceptional case tau = chi(f(a)) only: twist +
                  Connell model + Miller chain with M = p (Semaev 1998 transfer) + adapter
"""
import ctypes
import os
import sys

from . import core

_HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------- native library
_LIB = None


def native():
    global _LIB
    if _LIB is None:
        path = os.environ.get('CMBENCH_NATIVE', os.path.join(_HERE, 'native', 'libcmnative.so'))
        lib = ctypes.CDLL(path)
        u64 = ctypes.c_uint64
        lib.cm_squares_bitmap.argtypes = [u64, ctypes.c_void_p]
        lib.cm_enum_single.argtypes = [u64, ctypes.c_int, ctypes.POINTER(u64), u64, ctypes.c_void_p]
        lib.cm_enum_single.restype = u64
        lib.cm_enum_epsilon.argtypes = [u64, ctypes.c_int, ctypes.POINTER(u64), ctypes.c_void_p,
                                        ctypes.c_void_p]
        lib.cm_linrec_coeff.argtypes = [u64, ctypes.c_int, ctypes.POINTER(u64), u64, u64]
        lib.cm_linrec_coeff.restype = u64
        lib.cm_inverse_table.argtypes = [u64, ctypes.c_void_p]
        lib.cm_linrec_all.argtypes = [u64, ctypes.c_int, ctypes.POINTER(u64), u64, u64, ctypes.c_void_p]
        lib.cm_linrec_all.restype = ctypes.c_int
        lib.cm_enum_sum_eps.argtypes = [u64, ctypes.c_int, ctypes.POINTER(u64), ctypes.c_void_p]
        lib.cm_enum_sum_eps.restype = u64
        lib.cm_linrec_coeff2.argtypes = [u64, ctypes.c_int, ctypes.POINTER(u64), u64, u64, ctypes.c_void_p]
        lib.cm_linrec_coeff2.restype = ctypes.c_int
        _LIB = lib
    return _LIB


def _u64arr(vals):
    return (ctypes.c_uint64 * len(vals))(*vals)


# ---------------------------------------------------------------------------- trace provider
class TraceProvider:
    """Exact trace tau = p + 1 - #C(F_p) of the smooth projective model of y^2 = f(x).

    Cubic: E: Y^2 = X^3 + f2 X^2 + l f1 X + l^2 f0 (X = l x, Y = l y; same character values).
    Quartic: Jacobian E_{I,J}: Y^2 = X^3 - 27 I X - 27 J with the classical invariants
      I = 12 a e - 3 b d + c^2, J = 72 a c e + 9 b c d - 27 a d^2 - 27 e b^2 - 2 c^3
      for f = a x^4 + b x^3 + c x^2 + d x + e (Cremona 2001; Stoll & Cremona 2002).
    #C(F_p) = #Jac(C)(F_p) because a genus-one curve over F_p has a rational point.  Both models
    are checked against direct point counts in validation (cmbench.validate).
    PARI's ellap returns p + 1 - #E(F_p) (SEA for large p).  Work charged: model + ellinit + ellap.
    """
    _pari = None

    @classmethod
    def pari(cls):
        if cls._pari is None:
            import cypari2
            cls._pari = cypari2.Pari()
            cls._pari.allocatemem(256 * 10 ** 6, silent=True)
        return cls._pari

    @classmethod
    def weierstrass(cls, p, f):
        if len(f) == 4:
            f0, f1, f2, l = f
            return [0, f2 % p, 0, l * f1 % p, l * l % p * f0 % p]
        e, d, c, b, a = f
        I = (12 * a * e - 3 * b * d + c * c) % p
        J = (72 * a * c * e + 9 * b * c * d - 27 * a * d * d - 27 * e * b * b - 2 * c ** 3) % p
        return [0, 0, 0, (-27 * I) % p, (-27 * J) % p]

    @classmethod
    def trace(cls, p, f):
        P = cls.pari()
        E = P.ellinit(cls.weierstrass(p, f), p)
        return int(P.ellap(E))


def trace_by_count(p, f):
    """Direct O(p) count for validation only."""
    s = sum(core.legendre(core.peval(f, x, p), p) for x in range(p))
    return 1 - core.n_infinity(f, p) - s


# ---------------------------------------------------------------------------- inherited candidate
_CMCS = None


def cmcs_module():
    """Import the UNCHANGED inherited candidate from the verified extraction (env CM_INHERITED_SRC)."""
    global _CMCS
    if _CMCS is None:
        src = os.environ.get('CM_INHERITED_SRC')
        if not src:
            raise RuntimeError('set CM_INHERITED_SRC to the extracted inherited src/ directory')
        if src not in sys.path:
            sys.path.insert(0, src)
        import cmcs
        _CMCS = cmcs
    return _CMCS


class CmcsFrozen:
    name = 'cmcs_frozen'
    contract = {'supplied': 'p, f, a; exact trace for prepared mode',
                'acquired_cold': 'exact trace by PARI ellap (TraceProvider), Curve validation, '
                                 'translation/normalization sessions, Miller query',
                'reuse': 'Curve object (trace, N_inf, sessions) across poles',
                'implementation': 'inherited cmcs.py + vendored cm_system, pure Python, unchanged'}

    @staticmethod
    def prepare(p, f, trace=None):
        cm = cmcs_module()
        if trace is None:
            trace = TraceProvider.trace(p, f)
        return cm.Curve(p, list(f), trace=trace, trace_label='PARI ellap (TraceProvider)')

    @staticmethod
    def query(E, a):
        return E.single_pole(a)

    @classmethod
    def query_many(cls, E, A):
        return [E.single_pole(a) for a in A]

    @classmethod
    def cold(cls, p, f, a):
        return cls.query(cls.prepare(p, f), a)

    @staticmethod
    def sum_eps(E, a_hint=None):
        """sum_x chi(f(x)) = 1 - N_inf - tau (integer identity), reduced mod p: from the trace."""
        return (1 - E.n_inf - E.trace) % E.p


class EnumC:
    name = 'enum_c'
    contract = {'supplied': 'p, f, a', 'acquired': 'squares bitmap ((p+7)/8 bytes, O(p))',
                'query': 'O(p) native loop: Horner f(x), bitmap chi, blockwise batch inversion',
                'implementation': 'C (gcc -O2), single thread, uint64/__int128'}

    @staticmethod
    def prepare(p, f, trace=None):
        lib = native()
        bm = ctypes.create_string_buffer((p + 7) // 8)
        lib.cm_squares_bitmap(p, bm)
        return (p, [c % p for c in f], bm)

    @staticmethod
    def query(st, a):
        p, f, bm = st
        return int(native().cm_enum_single(p, len(f) - 1, _u64arr(f), a % p, bm))

    @classmethod
    def query_many(cls, st, A):
        return [cls.query(st, a) for a in A]

    @classmethod
    def cold(cls, p, f, a):
        return cls.query(cls.prepare(p, f), a)

    @staticmethod
    def sum_eps(st, a_hint=None):
        p, f, bm = st
        return int(native().cm_enum_sum_eps(p, len(f) - 1, _u64arr(f), bm))


class EnumConv:
    """All poles at once: C(a) = sum_{t != 0} eps(a + t)/t, a cyclic correlation over Z/p.
    With E(x) = sum eps(x) x^x and I(x) = sum_{t=1}^{p-1} t^{-1} x^{p-t}, C(a) is the coefficient of
    x^(a+p) in E*I folded cyclically (indices a + p and a).  One FLINT multiplication, O(M(p))."""
    name = 'enum_conv'
    contract = {'supplied': 'p, f', 'acquired': 'eps table (C), inverse table (C), one FLINT product',
                'query': 'table lookup after the single convolution', 'memory': 'O(p) words'}

    @staticmethod
    def prepare(p, f, trace=None):
        import flint
        import numpy as np
        lib = native()
        bm = ctypes.create_string_buffer((p + 7) // 8)
        lib.cm_squares_bitmap(p, bm)
        eps = np.zeros(p, dtype=np.int8)
        ff = [c % p for c in f]
        lib.cm_enum_epsilon(p, len(ff) - 1, _u64arr(ff), bm, eps.ctypes.data)
        inv = np.zeros(p, dtype=np.uint64)
        lib.cm_inverse_table(p, inv.ctypes.data)
        e_coeffs = (eps.astype(np.int64) % p).tolist()
        I_arr = np.zeros(p + 1, dtype=np.uint64)
        I_arr[1:p] = inv[1:p][::-1]              # index j (1..p-1) holds inv[p - j]
        prod = flint.nmod_poly(e_coeffs, p) * flint.nmod_poly(I_arr.tolist(), p)
        c = prod.coeffs()
        c = c + [0] * (2 * p + 1 - len(c))
        # coefficient index x + (p - t) with x = a + t (mod p): equals a + p if x = a + t < p, else a
        table = [(int(c[a + p]) + int(c[a])) % p for a in range(p)]
        table.append(int(eps.astype(np.int64).sum()) % p)          # table[p] = sum_x chi(f(x)) mod p
        return table

    @staticmethod
    def query(table, a):
        return table[a]

    @classmethod
    def query_many(cls, table, A):
        return [table[a] for a in A]

    @classmethod
    def cold(cls, p, f, a):
        return cls.prepare(p, f)[a]

    @staticmethod
    def sum_eps(table, a_hint=None):
        return table[-1]


class LinrecPy:
    name = 'linrec_py'
    contract = {'supplied': 'p, f, a', 'acquired': 'nothing reusable', 'query': 'O(p) Python',
                'implementation': 'handover comparators/reference_comparators.py, unchanged'}
    _R = None

    @classmethod
    def ref(cls):
        if cls._R is None:
            path = os.environ.get('CM_HANDOVER_COMPARATORS')
            if path and path not in sys.path:
                sys.path.insert(0, path)
            import reference_comparators
            cls._R = reference_comparators
        return cls._R

    @staticmethod
    def prepare(p, f, trace=None):
        return (p, list(f))

    @classmethod
    def query(cls, st, a):
        p, f = st
        return cls.ref().reverse_coefficient_sum(f, a, p)

    @classmethod
    def query_many(cls, st, A):
        return [cls.query(st, a) for a in A]

    @classmethod
    def cold(cls, p, f, a):
        return cls.query((p, f), a)


class LinrecC:
    name = 'linrec_c'
    contract = {'supplied': 'p, f, a', 'acquired': 'nothing reusable',
                'query': 'O(p) native recurrence, one final inversion', 'implementation': 'C -O2'}

    @staticmethod
    def prepare(p, f, trace=None):
        return (p, [c % p for c in f])

    @staticmethod
    def query(st, a):
        p, f = st
        d = len(f) - 1
        g = core.reversed_shift(f, a % p, p)
        N = core.N_index(p, d)
        high = int(native().cm_linrec_coeff(p, d, _u64arr(g), (p - 1) // 2, N))
        return core.from_high_value(f, a % p, p, high)

    @staticmethod
    def query_with_H(st, a):
        """(C_f(a), H): one extra recurrence step gives e_{N+1} = [x^{p-1}] f(a+x)^h = H."""
        import numpy as np
        p, f = st
        d = len(f) - 1
        g = core.reversed_shift(f, a % p, p)
        out = np.zeros(2, dtype=np.uint64)
        native().cm_linrec_coeff2(p, d, _u64arr(g), (p - 1) // 2, core.N_index(p, d), out.ctypes.data)
        return core.from_high_value(f, a % p, p, int(out[0])), int(out[1])

    @classmethod
    def query_many(cls, st, A):
        return [cls.query(st, a) for a in A]

    @classmethod
    def cold(cls, p, f, a):
        return cls.query(cls.prepare(p, f), a)


class FlintPower:
    """H_high(x) = sum_{m >= p} c_m x^(m-p): its coefficients are the first N+1 coefficients of
    (rev f)^h reversed, because [z^(dh-m)] (rev f)^h = c_m.  One FLINT nmod_poly.pow_trunc."""
    name = 'flint_power'
    contract = {'supplied': 'p, f', 'acquired': 'F = f^h by FLINT nmod_poly_pow; H_high = F >> p',
                'query': 'FLINT nmod_poly evaluation (Horner, O(N)) + O(log p) for F\'(a)',
                'batch': 'FLINT fmpz_mod_poly.multipoint_evaluate (product tree) for many poles',
                'memory': 'N+1 words cached'}

    @staticmethod
    def prepare(p, f, trace=None):
        # FLINT nmod_poly_pow (binary powering with FFT products) of the full F = f^h, then the
        # high block F >> p.  (python-flint's pow_trunc took a per-coefficient path that was ~10x
        # slower in pilots, so the full power is the legitimate fast FLINT preparation here.)
        import flint
        F = flint.nmod_poly([c % p for c in f], p) ** ((p - 1) // 2)
        H = F.right_shift(p)                          # H[i] = c_{p+i}
        return (p, [c % p for c in f], H, int(F[p - 1]))

    @staticmethod
    def query(st, a):
        p, f, H = st[:3]
        return core.from_high_value(f, a % p, p, int(H(a % p)))

    @staticmethod
    def sum_eps(st, a_hint=None):
        from .cases import sum_eps_from_H
        return sum_eps_from_H(st[0], st[1], st[3])

    @staticmethod
    def query_many(st, A):
        import flint
        p, f, H = st[:3]
        ctx = flint.fmpz_mod_poly_ctx(p)
        Hm = ctx([int(x) for x in H.coeffs()])
        vals = Hm.multipoint_evaluate([a % p for a in A])
        return [core.from_high_value(f, a % p, p, int(v)) for a, v in zip(A, vals)]

    @classmethod
    def cold(cls, p, f, a):
        return cls.query(cls.prepare(p, f), a)


class PolyrecC(FlintPower):
    """Same reusable polynomial H_high, prepared by the native O(N) recurrence for (rev f)^h:
    [z^k] (rev f)^h = c_{dh-k}, so H_high[i] = c_{p+i} = e_{N-i}.  Evaluation as FlintPower."""
    name = 'polyrec_c'
    contract = {'supplied': 'p, f', 'acquired': 'H_high by native C recurrence (O(N), inverse table)',
                'query': 'FLINT Horner; batch: FLINT multipoint', 'memory': '2(N+1) words transient'}

    @staticmethod
    def prepare(p, f, trace=None):
        import flint
        import numpy as np
        f = [c % p for c in f]
        d = len(f) - 1
        N = core.N_index(p, d)
        g = list(reversed(f))
        out = np.zeros(N + 2, dtype=np.uint64)
        rc = native().cm_linrec_all(p, d, _u64arr(g), (p - 1) // 2, N + 1, out.ctypes.data)
        if rc:
            raise MemoryError('cm_linrec_all failed: %d' % rc)
        H = flint.nmod_poly(out[N::-1].tolist(), p)
        return (p, f, H, int(out[N + 1]))           # e_{N+1} of (rev f)^h = c_{p-1}


class BGS07:
    name = 'bgs07'
    contract = {'supplied': 'p, f, a', 'acquired': 'nothing reusable across poles',
                'query': 'two BGS products: d x d companion recurrence to N, and 1 x 1 for N! g0^N',
                'implementation': 'cmbench.bgs07 (python-flint nmod_poly + numpy), p < 2^50'}

    @staticmethod
    def prepare(p, f, trace=None):
        return (p, [c % p for c in f])

    @staticmethod
    def high(p, f, a, stats=None, with_H=False):
        from . import bgs07
        d = len(f) - 1
        h = (p - 1) // 2
        g = core.reversed_shift(f, a % p, p)
        N = core.N_index(p, d)
        A0, A1 = core.companion_matrices(g, h, p)
        P = bgs07.interval_product(A0, A1, N, p, stats)
        D = bgs07.interval_product([[0]], [[g[0]]], N, p)[0][0]      # N! g0^N
        g0h = pow(g[0], h, p)
        eN = P[0][0] * g0h % p * pow(D, -1, p) % p
        if not with_H:
            return eN
        # one more step: W_{N+1} = A(N+1) W_N, D_{N+1} = (N+1) g0 D_N; W_N = P[:,0] g0^h
        WN = [P[i][0] * g0h % p for i in range(d)]
        row0 = [(A0[0][j] + A1[0][j] * (N + 1)) % p for j in range(d)]
        W1 = sum(r * w for r, w in zip(row0, WN)) % p
        return eN, W1 * pow(D * (N + 1) % p * g[0] % p, -1, p) % p

    @classmethod
    def query(cls, st, a):
        p, f = st
        return core.from_high_value(f, a % p, p, cls.high(p, f, a))

    @classmethod
    def query_with_H(cls, st, a):
        p, f = st
        eN, H = cls.high(p, f, a, with_H=True)
        return core.from_high_value(f, a % p, p, eN), H

    @classmethod
    def query_many(cls, st, A):
        return [cls.query(st, a) for a in A]

    @classmethod
    def cold(cls, p, f, a):
        return cls.query(cls.prepare(p, f), a)


# ---------------------------------------------------------------------------- Voloch / Semaev route
def _ec_add(P, Q, A, p):
    if P is None:
        return Q, 0
    if Q is None:
        return P, 0
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None, 0
    if x1 == x2:
        lam = (3 * x1 * x1 + A) * pow(2 * y1, -1, p) % p
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (lam * lam - x1 - x2) % p
    return (x3, (lam * (x1 - x3) - y1) % p), lam


def miller_transfer(R, M, A, p):
    """alpha_M(R) = [z^0] dlog f_{M,R}/dz at O, z = -X/Y (differentiated Miller chain), and [M]R."""
    T, alpha = R, 0
    for bit in bin(M)[3:]:
        T, lam = _ec_add(T, T, A, p)
        alpha = (2 * alpha + lam) % p
        if bit == '1':
            T, lam = _ec_add(T, R, A, p)
            alpha = (alpha + lam) % p
    return alpha, T


def connell_short(g, p):
    """Short Weierstrass model Y^2 = X^3 + A X + B of v^2 = g(w), g(0) = 1, origin P+ = (0, 1),
    and the image R of P- = (0, -1).  Formulas as in manuscript (26)-(29) (Connell 1999, 1.2),
    re-implemented here; R from the w -> 0 limit on the branch v = -sqrt(g)."""
    g = list(g) + [0] * (5 - len(g))
    f1, f2, f3, f4 = g[1], g[2], g[3], g[4]
    i = lambda n: pow(n, -1, p)
    a1, a2, a3, a4 = f1, (f2 - f1 * f1 * i(4)) % p, 2 * f3 % p, (-4 * f4) % p
    a6 = a2 * a4 % p
    b2 = (a1 * a1 + 4 * a2) % p
    b4 = (2 * a4 + a1 * a3) % p
    b6 = (a3 * a3 + 4 * a6) % p
    A = (b4 * i(2) - b2 * b2 * i(48)) % p
    B = (b6 * i(4) - b2 * b4 * i(24) + b2 * b2 * b2 * i(864)) % p
    s1 = f1 * i(2) % p
    s2 = (f2 - s1 * s1) * i(2) % p
    s3 = (f3 - 2 * s1 * s2) * i(2) % p
    x = (-2 * s2) % p
    y = (-4 * s3) % p
    R = ((x + b2 * i(12)) % p, (y + (a1 * x + a3) * i(2)) % p)
    return A, B, R


class VolochSemaev:
    """Exceptional case tau = chi(f(a)) only (anomalous curve or anomalous twist).

    Derivation (REPORT section 4): twist by d = 1 or f(a) so that the curve is anomalous and
    f~(a) is a square; g(z) = f~(a+z)/f~(a); on the Connell model with origin P+, the function
    1/z equals h_R/2 - g_1/4 with h_R = (Y + Y_R)/(X - X_R), R = image of P-.  Summing over
    E(F_p) \\ {O, R} with #E(F_p) = p and sum h_R = -alpha_p(R) (Voloch high part + Theorem A)
        C_f(a) = chi(f(a)) * ( f'(a) / (2 f(a)) - alpha_p(R) / 2 ),
    where alpha_p(R) is Semaev's logarithmic transfer of (R) - (O) relative to dX/(2Y), computed by
    the differentiated Miller chain with M = p.  No square root is required.  The chain endpoint
    [p]R = O is a necessary check of the trace hypothesis."""
    name = 'voloch_semaev'
    contract = {'supplied': 'p, f, a and the hypothesis tau = chi(f(a)) (trace +-1)',
                'acquired': 'twist, translation, Connell model, Miller chain with M = p',
                'query': 'O(log p) field operations', 'scope': 'exceptional case only'}

    @staticmethod
    def value(p, f, a, check=True):
        f = [c % p for c in f]
        fa = core.peval(f, a, p)
        e = core.legendre(fa, p)
        if e == 0:
            raise ValueError('branch pole: outside this route')
        dtw = 1 if e == 1 else fa
        ft = [c * dtw % p for c in f]
        fta = fa * dtw % p
        g = [c * pow(fta, -1, p) % p for c in core.taylor_shift(ft, a, p)]
        A, B, R = connell_short(g, p)
        alpha, end = miller_transfer(R, p, A, p)
        if check and end is not None:
            raise ArithmeticError('[p]R != O: the curve (or twist) is not anomalous')
        fd = core.peval(core.deriv(f, p), a, p)
        half = pow(2, -1, p)
        return e * (fd * pow(2 * fa, -1, p) - alpha * half) % p

    @classmethod
    def cold(cls, p, f, a):
        return cls.value(p, f, a)


REGISTRY = {c.name: c for c in (CmcsFrozen, EnumC, EnumConv, LinrecPy, LinrecC, FlintPower,
                                PolyrecC, BGS07, VolochSemaev)}
