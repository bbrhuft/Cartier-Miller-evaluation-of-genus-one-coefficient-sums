"""Finite check of Katz, 'On a question of Zannier' (Exp. Math. 2019), Thm 3.1,
translated into the project chart.  Katz: f = 4x^3 - g2 x - g3,
a_p = [x^(p-1)] f^h = E_{p-1} mod p, b_p = [x^(p-2)] f^h = E_{p+1}/12 mod p,
with the Tate-curve normalization g2 = E4/12, g3 = -E6/216.
Project chart: F = x^3 + A x + B = f/4 with g2 = -4A, g3 = -4B, so
f^h = 4^h F^h and 4^h = 2^(p-1) = 1: a_p = H, b_p = beta exactly.
We express E_k (constant term 1) as a polynomial in E4, E6 by exact linear
algebra on q-expansions, substitute, and compare with dense H, beta for every
nonsingular (A, B) at each listed prime.  Consequence checked here:
beta/H = E_{p+1}/(12 E_{p-1}) at all ordinary inputs (not only CM)."""
import json, sys
from fractions import Fraction as Fr
import sympy as sp
from flint import nmod_poly

def sigma(n, k):
    return sum(d**k for d in range(1, n+1) if n % d == 0)

def eis(k, N):
    Bk = Fr(str(sp.bernoulli(k)))
    c = -Fr(2*k) / Bk
    return [Fr(1)] + [c*sigma(n, k-1) for n in range(1, N)]

def mul(a, b, N):
    out = [Fr(0)]*N
    for i, x in enumerate(a):
        if x:
            for j in range(N - i):
                out[i+j] += x*b[j]
    return out

def express(k):
    mons = [(a, b) for a in range(k//4 + 1) for b in range(k//6 + 1) if 4*a + 6*b == k]
    N = len(mons) + 6
    E4, E6 = eis(4, N), eis(6, N)
    vecs = []
    for a, b in mons:
        v = [Fr(1)] + [Fr(0)]*(N-1)
        for _ in range(a): v = mul(v, E4, N)
        for _ in range(b): v = mul(v, E6, N)
        vecs.append(v)
    target = eis(k, N)
    M = sp.Matrix([[vecs[m][i] for m in range(len(mons))] for i in range(N)])
    sol = M.solve_least_squares(sp.Matrix(target)) if False else None
    # exact solve via sympy linsolve on the first len(mons) rows, check the rest
    sym = sp.symbols('c0:%d' % len(mons))
    eqs = [sum(sym[m]*sp.Rational(vecs[m][i].numerator, vecs[m][i].denominator) for m in range(len(mons))) - sp.Rational(target[i].numerator, target[i].denominator) for i in range(N)]
    s = sp.solve(eqs, sym, dict=True)
    assert len(s) == 1
    return {mons[m]: Fr(str(s[0][sym[m]])) for m in range(len(mons))}

def ev_mod(poly, E4v, E6v, p):
    tot = 0
    for (a, b), c in poly.items():
        if c.denominator % p == 0:
            raise ValueError('non-p-integral coefficient')
        tot += c.numerator * pow(c.denominator, -1, p) * pow(E4v, a, p) * pow(E6v, b, p)
    return tot % p

out = []
for p in [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
    Em, Ep = express(p - 1), express(p + 1)
    agree_a = agree_b = total = 0; bad = []
    for A in range(p):
        for B in range(p):
            if (4*A**3 + 27*B*B) % p == 0: continue
            g2, g3 = (-4*A) % p, (-4*B) % p
            E4v, E6v = 12*g2 % p, (-216*g3) % p
            P = nmod_poly([B, A, 0, 1], p) ** ((p-1)//2)
            H, beta = int(P[p-1]), int(P[p-2])
            ap = ev_mod(Em, E4v, E6v, p); bp = ev_mod(Ep, E4v, E6v, p) * pow(12, -1, p) % p
            total += 1; agree_a += (ap == H); agree_b += (bp == beta)
            if (ap, bp) != (H, beta) and len(bad) < 3: bad.append((A, B, H, beta, ap, bp))
            if H == 0 and beta == 0: bad.append(('common zero', A, B))
    out.append({'p': p, 'models': total, 'E_{p-1}=H': agree_a, 'E_{p+1}/12=beta': agree_b, 'bad': bad})
    print(out[-1])
json.dump(out, open(__file__.rsplit('/theory/', 1)[0] + '/results/katz_zannier_check.json', 'w'), indent=1)
ok = all(o['models'] == o['E_{p-1}=H'] == o['E_{p+1}/12=beta'] and not o['bad'] for o in out)
print('ALL_AGREE' if ok else 'DISAGREEMENT')
sys.exit(0 if ok else 1)
