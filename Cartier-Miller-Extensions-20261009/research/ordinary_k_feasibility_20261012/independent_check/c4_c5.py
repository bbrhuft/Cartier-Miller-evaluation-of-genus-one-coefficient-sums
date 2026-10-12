"""C4: beta == 6B dH/dA - (4/3) A^2 dH/dB (mod p) as polynomials in A,B.
C5: beta == - sum_{P affine in E(F_p)} x(P) (mod p).

C4 is checked (a) as an exact identity over Q:  D H = (p+1) beta, D = 6B d/dA - (4/3)A^2 d/dB
(this is what the algebraic proof below gives), and (b) mod p as polynomials, and (c) by evaluation on all (A,B).
Proof sketch (verified symbolically below for the auxiliary identity):
  6x F + (-(4/3)A - 2x^2) F' = 6Bx - (4/3)A^2,   F = x^3 + A x + B.
  Hence D(F^h) = h F^{h-1} (6Bx - (4/3)A^2) = 6h x F^h + (-(4/3)A - 2x^2) (F^h)'.
  Take [x^{p-1}]:  [x^{p-1}] x F^h = beta;  [x^{p-1}] (F^h)' = p [x^p]F^h;  [x^{p-1}] x^2 (F^h)' = (p-2) beta.
  So D H = 6h beta - 2(p-2) beta + p*(stuff) ... exactly: D H = (3(p-1) - 2(p-2)) beta - (4/3)A p [x^p]F^h
       = (p+1) beta - (4p/3) A [x^p]F^h.   Mod p: D H == beta.
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))  # explicit: python -I omits the script directory

import sys
from fractions import Fraction
from math import factorial
from common import *


def coeff_poly(p, deg):
    """[x^deg] (x^3 + A x + B)^h as dict {(i,j): int} (A^i B^j), exact over Z"""
    h = (p - 1) // 2
    d = {}
    for a in range(h + 1):
        b = deg - 3 * a
        c = h - a - b
        if b < 0 or c < 0:
            continue
        d[(b, c)] = d.get((b, c), 0) + factorial(h) // (factorial(a) * factorial(b) * factorial(c))
    return d


def Dop(P):
    """D = 6B d/dA - (4/3) A^2 d/dB, exact Fractions"""
    out = {}
    for (i, j), c in P.items():
        if i:
            key = (i - 1, j + 1)
            out[key] = out.get(key, 0) + Fraction(6 * i * c)
        if j:
            key = (i + 2, j - 1)
            out[key] = out.get(key, 0) - Fraction(4, 3) * j * c
    return {k: v for k, v in out.items() if v != 0}


def check_C4(p):
    H = coeff_poly(p, p - 1)
    beta = coeff_poly(p, p - 2)
    xp = coeff_poly(p, p)
    DH = Dop(H)
    # exact identity: D H = (p+1) beta - (4p/3) A [x^p]F^h
    rhs = {k: Fraction((p + 1) * v) for k, v in beta.items()}
    for (i, j), v in xp.items():
        key = (i + 1, j)
        rhs[key] = rhs.get(key, 0) - Fraction(4 * p, 3) * v
    rhs = {k: v for k, v in rhs.items() if v != 0}
    exact = (DH == rhs)
    # mod p polynomial identity
    def modp(P):
        r = {}
        for k, v in P.items():
            v = Fraction(v)
            x = (v.numerator * pow(v.denominator, -1, p)) % p
            if x:
                r[k] = x
        return r
    modok = (modp(DH) == modp(beta))
    # evaluation on all (A,B) in F_p^2, against independent direct computation of beta
    inv3 = pow(3, -1, p)
    evok = True
    for A in range(p):
        for B in range(p):
            dHdA = sum(i * c * pow(A, i - 1, p) * pow(B, j, p) for (i, j), c in H.items() if i) % p
            dHdB = sum(j * c * pow(A, i, p) * pow(B, j - 1, p) for (i, j), c in H.items() if j) % p
            val = (6 * B * dHdA - 4 * inv3 * A * A * dHdB) % p
            if val != hasse_beta(p, A, B)[1]:
                evok = False
    return exact, modok, evok


def check_C5(p):
    ok = n = 0
    fails = []
    for A in range(p):
        for B in range(p):
            if not nonsingular(p, A, B):
                continue
            s = 0
            for x in range(p):
                s += x * (1 + legendre(x ** 3 + A * x + B, p))
            beta = hasse_beta(p, A, B)[1]
            n += 1
            if (-s) % p == beta:
                ok += 1
            else:
                fails.append((A, B, s % p, beta))
    return ok, n, fails


def _main():
    import random
    from harness import base_parser, Run, run_main
    ap = base_parser('C4 exact Serre-derivative identity and C5 point-sum identity')
    ap.add_argument('--c4-max', type=int, default=71, help='check C4 for primes 5 <= p <= this')
    ap.add_argument('--c5-max', type=int, default=61, help='check C5 for primes 7 <= p <= this')
    a = ap.parse_args()
    scope = {'C4_primes': f'5..{a.c4_max}', 'C5_primes': f'7..{a.c5_max}', 'C5_models': 'all nonsingular'}

    def body(run):
        rng = random.Random(1)
        for _ in range(200):
            A, B, x = (Fraction(rng.randint(-50, 50)) for _ in range(3))
            F = x ** 3 + A * x + B
            dF = 3 * x ** 2 + A
            run.check(6 * x * F + (-Fraction(4, 3) * A - 2 * x ** 2) * dF == 6 * B * x - Fraction(4, 3) * A ** 2,
                      {'A': A, 'B': B, 'x': x}, group='auxiliary_identity')
        for p in [q for q in range(5, a.c4_max + 1) if is_prime(q)]:
            exact, modok, evok = check_C4(p)
            run.check(exact, {'p': p}, group='C4_exact_identity_over_Q')
            run.check(modok, {'p': p}, group='C4_mod_p_polynomial_identity')
            run.check(evok, {'p': p}, group='C4_pointwise')
        for p in [q for q in range(7, a.c5_max + 1) if is_prime(q)]:
            ok, n, fails = check_C5(p)
            for _ in range(ok):
                run.check(True, None, group='C5')
            for f in fails:
                run.check(False, {'p': p, 'fail': f}, group='C5')

    run_main(lambda: Run('c4_c5', scope, a.out), body)


if __name__ == "__main__":
    _main()
