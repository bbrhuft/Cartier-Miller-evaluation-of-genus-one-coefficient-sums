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


if __name__ == "__main__":
    # auxiliary identity check (symbolic in A, B via random integer evaluation is not needed: it is linear algebra)
    # verify 6xF + (-(4/3)A - 2x^2)F' == 6Bx - (4/3)A^2 at many random integer (A,B,x)
    import random
    random.seed(1)
    for _ in range(200):
        A, B, x = (Fraction(random.randint(-50, 50)) for _ in range(3))
        F = x ** 3 + A * x + B
        dF = 3 * x ** 2 + A
        assert 6 * x * F + (-Fraction(4, 3) * A - 2 * x ** 2) * dF == 6 * B * x - Fraction(4, 3) * A ** 2
    out = open("c4_c5_results.txt", "w")
    out.write("auxiliary identity 6xF + (-(4/3)A - 2x^2)F' = 6Bx - (4/3)A^2: OK (200 random rational points; it is a degree-4 polynomial identity)\n")
    primes = [q for q in range(5, int(sys.argv[1]) if len(sys.argv) > 1 else 110) if is_prime(q)]
    for p in primes:
        exact, modok, evok = check_C4(p) if p <= 60 else (*check_C4_fast(p),) if False else check_C4(p)
        line = f"C4 p={p}: exact identity D H = (p+1)beta - (4p/3)A[x^p]F^h over Q: {exact}; D H == beta mod p as polynomials: {modok}; pointwise on all p^2 (A,B): {evok}"
        print(line, flush=True)
        out.write(line + "\n")
    for p in [q for q in primes if q >= 7 and q <= 61]:
        ok, n, fails = check_C5(p)
        line = f"C5 p={p}: beta == -sum_{{affine P}} x(P): {ok}/{n} nonsingular models (incl. supersingular); fails={fails[:5]}"
        print(line, flush=True)
        out.write(line + "\n")
    out.close()
