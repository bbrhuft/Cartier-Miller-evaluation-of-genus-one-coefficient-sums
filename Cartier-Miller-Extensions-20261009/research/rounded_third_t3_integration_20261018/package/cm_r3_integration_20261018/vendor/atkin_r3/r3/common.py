"""Round-3 shared helpers: certified primality, references, class-number backends.

Standard library unless stated. FLINT (python-flint wheel) and PARI (cypari2) are optional
and every backend reports which one produced a value.
"""
from math import gcd, isqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Deterministic Miller-Rabin: the first 13 prime bases are a proof of primality for
# n < 3.317e24 (Sorenson & Webster, 2017, Math. Comp. 86, 985-1003).
_MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def is_prime(n):
    if n < 2:
        return False
    for b in _MR_BASES:
        if n % b == 0:
            return n == b
    if n >= 3317044064679887385961981:
        raise ValueError('deterministic base set not proved beyond 3.317e24')
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _MR_BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def params(p):
    """m, L, h, N, q0 for p = 5 mod 6 (q0 only meaningful for p = 1 mod 4)."""
    if type(p) is not int or p < 11 or p % 6 != 5:
        raise ValueError('supply a certified prime p >= 11 with p = 5 mod 6')
    return dict(m=(p - 2) // 3, L=(p + 1) // 3, h=(p - 1) // 2, N=(p - 5) // 12, q0=(p - 1) // 4)


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


# ------------------------------------------------------------------ class numbers
def pari():
    import cypari2
    return cypari2.Pari()


QFBCLASSNO_UNCONDITIONAL_BOUND = 2 * 10 ** 10   # PARI 2.17.2 doc: correct for |D| < 2.10^10


def classno_qfb_unconditional(D, _p=[]):
    """h(D) via PARI qfbclassno(D,0), ONLY inside the documented unconditional range."""
    if D >= 0 or not abs(D) < QFBCLASSNO_UNCONDITIONAL_BOUND:
        raise ValueError('qfbclassno is documented unconditional only for -2*10^10 < D < 0')
    if not _p:
        _p.append(pari())
    return int(_p[0].qfbclassno(D, 0))


def classno_grh(D, _p=[]):
    """h(D) via PARI quadclassunit (Buchmann-McCurley), correct under GRH only."""
    if not _p:
        _p.append(pari())
    return int(_p[0].quadclassunit(D)[0])


def classno_forms(D, cache=None):
    """h(D) by counting reduced primitive forms; unconditional, O(|D|^{1/2} polylog).

    cache: None means a fresh sieve on every call (cold).  Pass a dict to reuse the
    smallest-prime-factor sieve across calls at the same size (warm; disclosed).
    """
    sys.dont_write_bytecode = True
    import charp
    if cache is None:
        charp.classno.__defaults__[0].clear()      # inherited module-level sieve cache
    return charp.classno(D)


class ClassNumberPolicy:
    """Frozen backend policy.

    mode 'unconditional': qfbclassno inside |D| < 2e10, else reduced-form count.
    mode 'grh'          : quadclassunit everywhere (labelled GRH-conditional).
    mode 'forms'        : reduced-form count everywhere.
    Each call returns (h, backend_label, status).
    """
    def __init__(self, mode='unconditional'):
        if mode not in ('unconditional', 'grh', 'forms'):
            raise ValueError(mode)
        self.mode = mode

    def __call__(self, D):
        if self.mode == 'grh':
            return classno_grh(D), 'pari.quadclassunit', 'GRH-conditional'
        if self.mode == 'unconditional' and abs(D) < QFBCLASSNO_UNCONDITIONAL_BOUND:
            return classno_qfb_unconditional(D), 'pari.qfbclassno(D,0)', \
                'unconditional (PARI documented range |D|<2e10)'
        return classno_forms(D), 'reduced-form count', 'unconditional'


# ------------------------------------------------------------------ FLINT references
def flint_factorial(n, p):
    import flint_backend
    return flint_backend.flint_factorial(n, p)


def flint_rising(p, length, starts, block_size=None):
    import flint_backend
    return flint_backend.flint_rising(p, length, starts, block_size)


def interval(p, a, b):
    """prod_{j=a}^{b} j mod p (empty product = 1), FLINT block engine, a >= 1."""
    if b < a:
        return 1
    (v,), _ = flint_rising(p, b - a + 1, [a])
    return v


def a_from_c(p, c):
    """a_L = (3/4) c_p."""
    return 3 * c * pow(4, p - 2, p) % p


def c_from_mfact(p, mf):
    return 2 * pow(mf, 3 * (p - 2), p) % p
