"""cmbench.harvey -- adapter from the matched output C_f(a) to D. Harvey's published BGS-type
interval-products kernel (hypellfrob 2.1.1, recurrences_ntl.cpp: "an algorithm similar to
Theorem 15 of [BGS]", dyadic evaluation implementing BGS Theorem 8), shipped compiled in
passagemath-ntl 10.8.13 as sage.schemes.hyperelliptic_curves.hypellfrob.interval_products.

Must run under the passagemath interpreter (venv_sage); imports only cmbench.core otherwise.

interval_products(M0, M1, [a, b]) returns M(a+1) M(a+2) ... M(b), M(t) = M0 + t M1 (increasing
order).  The recurrence needs A(N) ... A(1) (decreasing order), so the adapter passes transposes:
(A(N)...A(1))^T = A(1)^T ... A(N)^T.  Denominators: the companion recurrence carries
D_k = k! g0^k (core.companion_matrices); D_N is a second 1 x 1 interval product of M(t) = g0 t.
e_N = (A(N)...A(1))[0][0] g0^h / D_N.  Every unit used is nonzero mod p because N < p and
g0 = lead(f) != 0; the kernel's own preconditions (2..2^t+1 and shifted points invertible) are
validated against the direct recurrence on the development set (cmbench.validate).
"""
import sage.all__sagemath_schemes  # noqa: F401  (initialises the Sage category framework)
from sage.matrix.constructor import Matrix
from sage.rings.finite_rings.integer_mod_ring import Integers
from sage.schemes.hyperelliptic_curves.hypellfrob import interval_products

from . import core


def high(p, f, a, with_H=False):
    d = len(f) - 1
    h = (p - 1) // 2
    g = core.reversed_shift([c % p for c in f], a % p, p)
    N = core.N_index(p, d)
    A0, A1 = core.companion_matrices(g, h, p)
    R = Integers(p)
    M0 = Matrix(R, A0).transpose()
    M1 = Matrix(R, A1).transpose()
    P = interval_products(M0, M1, [0, N])[0]
    D = interval_products(Matrix(R, [[0]]), Matrix(R, [[g[0]]]), [0, N])[0][0, 0]
    g0h = pow(g[0], h, p)
    eN = int(P[0, 0]) * g0h % p * pow(int(D), -1, p) % p
    if not with_H:
        return eN
    # P is the transpose of A(N)...A(1): first column of the latter = first row of P
    WN = [int(P[0, i]) * g0h % p for i in range(d)]
    row0 = [(A0[0][j] + A1[0][j] * (N + 1)) % p for j in range(d)]
    W1 = sum(r * w for r, w in zip(row0, WN)) % p
    return eN, W1 * pow(int(D) * (N + 1) % p * g[0] % p, -1, p) % p


class BGSHarvey:
    name = 'bgs_harvey'
    contract = {'supplied': 'p, f, a', 'acquired': 'nothing reusable across poles',
                'query': 'two interval products (d x d and 1 x 1) by Harvey\'s NTL kernel',
                'implementation': 'passagemath-ntl 10.8.13 hypellfrob (C++/NTL), adapter here'}

    @staticmethod
    def prepare(p, f, trace=None):
        return (p, [c % p for c in f])

    @staticmethod
    def query(st, a):
        p, f = st
        return core.from_high_value(f, a % p, p, high(p, f, a))

    @classmethod
    def query_many(cls, st, A):
        return [cls.query(st, a) for a in A]

    @staticmethod
    def query_with_H(st, a):
        p, f = st
        eN, H = high(p, f, a, with_H=True)
        return core.from_high_value(f, a % p, p, eN), H

    @classmethod
    def cold(cls, p, f, a):
        return cls.query(cls.prepare(p, f), a)
