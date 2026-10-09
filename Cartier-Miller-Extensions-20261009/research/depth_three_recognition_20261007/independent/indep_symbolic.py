#!/usr/bin/env python3
"""
Independent symbolic recomputation of claims C1, C2, C3, C6 (and the
P/Q recognition polynomials of C5) in the biquadratic ring
    R = Z[e, g] / (e^2 - 3, g^2 - 2),   basis (1, e, g, eg).

Written from scratch by the second worker WITHOUT reading the first
worker's code.  Uses only the Python standard library, sympy (for an
independent cross-check of the ring arithmetic and for resultants) and
cypari2 (for polclass, factor, polresultant, poldisc).
"""
from fractions import Fraction
import json, sys, itertools

# ---------------------------------------------------------------------------
# Biquadratic ring arithmetic on 4-tuples (a0, a1, a2, a3) = a0 + a1 e + a2 g + a3 eg
# ---------------------------------------------------------------------------
class BQ:
    __slots__ = ("c",)
    def __init__(self, c0=0, c1=0, c2=0, c3=0):
        if isinstance(c0, (tuple, list)):
            self.c = tuple(Fraction(x) for x in c0)
        else:
            self.c = (Fraction(c0), Fraction(c1), Fraction(c2), Fraction(c3))
    def __add__(self, o):
        o = _lift(o); return BQ(tuple(a + b for a, b in zip(self.c, o.c)))
    __radd__ = __add__
    def __neg__(self): return BQ(tuple(-a for a in self.c))
    def __sub__(self, o): return self + (-_lift(o))
    def __rsub__(self, o): return _lift(o) - self
    def __mul__(self, o):
        o = _lift(o)
        a0, a1, a2, a3 = self.c
        b0, b1, b2, b3 = o.c
        # e^2=3, g^2=2, (eg)^2=6, e*eg=3g, g*eg=2e
        r0 = a0*b0 + 3*a1*b1 + 2*a2*b2 + 6*a3*b3
        r1 = a0*b1 + a1*b0 + 2*a2*b3 + 2*a3*b2
        r2 = a0*b2 + a2*b0 + 3*a1*b3 + 3*a3*b1
        r3 = a0*b3 + a3*b0 + a1*b2 + a2*b1
        return BQ((r0, r1, r2, r3))
    __rmul__ = __mul__
    def __pow__(self, n):
        r = BQ(1); b = self
        while n:
            if n & 1: r = r * b
            b = b * b; n >>= 1
        return r
    def conj_e(self):  # e -> -e
        a0, a1, a2, a3 = self.c; return BQ((a0, -a1, a2, -a3))
    def conj_g(self):  # g -> -g
        a0, a1, a2, a3 = self.c; return BQ((a0, a1, -a2, -a3))
    def conj_eg(self): return self.conj_e().conj_g()
    def norm(self):
        n = self * self.conj_e() * self.conj_g() * self.conj_eg()
        assert n.c[1] == 0 and n.c[2] == 0 and n.c[3] == 0, n.c
        return n.c[0]
    def inv(self):
        # N(x) = x * (product of the three other conjugates)
        cof = self.conj_e() * self.conj_g() * self.conj_eg()
        n = (self * cof).c
        assert n[1] == n[2] == n[3] == 0
        return cof * BQ(Fraction(1, 1) / n[0])
    def __truediv__(self, o): return self * _lift(o).inv()
    def __eq__(self, o): return self.c == _lift(o).c
    def is_zero(self): return all(x == 0 for x in self.c)
    def ints(self):
        assert all(x.denominator == 1 for x in self.c), self.c
        return tuple(int(x) for x in self.c)
    def __repr__(self): return "BQ%s" % (tuple(str(x) for x in self.c),)

def _lift(o):
    return o if isinstance(o, BQ) else BQ(o)

E  = BQ(0, 1, 0, 0)
G  = BQ(0, 0, 1, 0)
ONE = BQ(1)

# cross-check the ring arithmetic against sympy on random elements
def _sympy_check():
    import sympy as sp, random
    e, g = sp.sqrt(3), sp.sqrt(2)
    def tosym(x):
        a0, a1, a2, a3 = x.c
        return sp.Rational(a0) + sp.Rational(a1)*e + sp.Rational(a2)*g + sp.Rational(a3)*e*g
    random.seed(1)
    for _ in range(50):
        x = BQ(tuple(random.randint(-9, 9) for _ in range(4)))
        y = BQ(tuple(random.randint(-9, 9) for _ in range(4)))
        lhs = sp.nsimplify(sp.expand(tosym(x) * tosym(y)))
        rhs = sp.nsimplify(sp.expand(tosym(x * y)))
        assert sp.simplify(lhs - rhs) == 0, (x, y)
        if not x.is_zero():
            assert sp.simplify(sp.expand(tosym(x) * tosym(x.inv())) - 1) == 0
    return True

# ---------------------------------------------------------------------------
# The normalized 2-isogeny step (Velu, kernel (q,0)) on y^2 = x^3 + A x + B
# ---------------------------------------------------------------------------
def step(A, B, q):
    """(A', B') of the normalized quotient by the 2-torsion point (q, 0).
    Derived by the second worker: shift x -> x+q gives y^2 = x(x^2 + 3q x + (3q^2 + A));
    Velu's quotient of y^2 = x(x^2+ax+b) is y^2 = x(x^2 - 2a x + a^2 - 4b);
    shifting back by X = x' - 2q gives a depressed cubic."""
    assert (q**3 + A*q + B).is_zero(), "q must be a root"
    a = 3 * q
    b = 3 * q * q + A
    # x'^3 - 2a x'^2 + (a^2-4b) x'  ;  x' = X + 2q
    s = 2 * q
    # (X+s)^3 - 2a (X+s)^2 + (a^2-4b)(X+s)
    A1 = 3*s*s - 4*a*s + (a*a - 4*b)
    B1 = s**3 - 2*a*s*s + (a*a - 4*b)*s
    quad = 3*s - 2*a          # coefficient of X^2 must vanish
    assert quad.is_zero()
    return A1, B1

def cofactor_roots(A, B, q):
    """Claim C1: on the target, cubic = (x+2q)(x^2 - 2q x + (A'+4q^2)),
    quadratic roots q +- 2 sqrt(A + 3 q^2).  Returns (A', B', c) and checks."""
    A1, B1 = step(A, B, q)
    c = A1 + 4*q*q
    # (x + 2q)(x^2 - 2q x + c) = x^3 + (c - 4q^2) x + 2 q c
    assert (c - 4*q*q) == A1 and (2*q*c) == B1
    # roots q +- 2 sqrt(A+3q^2):  product = q^2 - 4(A+3q^2) must equal c, sum = 2q
    assert (q*q - 4*(A + 3*q*q)) == c
    return A1, B1, c

# ---------------------------------------------------------------------------
# The family: seed (0, -r^3) with r = 1 (homogeneity restores r)
# ---------------------------------------------------------------------------
def build_family():
    A0, B0 = BQ(0), BQ(-1)
    q0 = ONE
    A1, B1, c1 = cofactor_roots(A0, B0, q0)
    # nondual roots on E1: q0 +- 2 sqrt(A0 + 3 q0^2) = 1 +- 2 sqrt(3) = 1 +- 2e
    q1 = ONE + 2*E
    assert (q1**3 + A1*q1 + B1).is_zero()
    A2, B2, c2 = cofactor_roots(A1, B1, q1)
    # nondual roots on E2: q1 +- 2 sqrt(A1 + 3 q1^2)
    rad = A1 + 3*q1*q1          # should be 24 + 12 e = 12(2+e) = 6 (1+e)^2
    cand = 3*G + E*G            # claimed sqrt(rad) = 3g + eg
    assert (cand*cand) == rad, (cand*cand, rad)
    q2 = q1 + 2*cand
    assert (q2**3 + A2*q2 + B2).is_zero()
    A3, B3, c3 = cofactor_roots(A2, B2, q2)
    return dict(A1=A1, B1=B1, q1=q1, A2=A2, B2=B2, q2=q2, A3=A3, B3=B3, q0=q0, c3=c3)

def reverse_check(fam):
    """Reverse path from E3 using dual roots -2 q2, then -8 q1, then -32 q0."""
    A3, B3 = fam["A3"], fam["B3"]
    d1 = -2 * fam["q2"]
    A, B = step(A3, B3, d1)
    assert A == 16*fam["A2"] and B == 64*fam["B2"]
    d2 = -8 * fam["q1"]
    A, B = step(A, B, d2)
    assert A == 256*fam["A1"] and B == 4096*fam["B1"]
    d3 = -32 * fam["q0"]
    A, B = step(A, B, d3)
    assert A == BQ(0) and B == BQ(-(64**3))
    return [d1.ints(), d2.ints(), d3.ints()], (A.ints(), B.ints())

def beta_multiplier(fam):
    """beta transport beta' = 2 beta - q H starting from beta0 = 0 (seed A=0, p=1 mod 3)."""
    m = BQ(0)
    for q in (fam["q0"], fam["q1"], fam["q2"]):
        m = 2*m - q
    return m

# ---------------------------------------------------------------------------
# j-invariant and its minimal polynomial over Q (by elimination of the 4 conjugates)
# ---------------------------------------------------------------------------
def j_invariant(A, B):
    num = 1728 * 4 * A**3
    den = 4 * A**3 + 27 * B**2
    return num / den, den

def minpoly_from_conjugates(x):
    """Product over the four Galois conjugates of (J - sigma(x)) using BQ arithmetic
    on polynomials with BQ coefficients; the result must be rational."""
    conjs = [x, x.conj_e(), x.conj_g(), x.conj_eg()]
    poly = [ONE]  # coefficients low->high of prod (J - c)
    for c in conjs:
        new = [BQ(0)] * (len(poly) + 1)
        for i, a in enumerate(poly):
            new[i + 1] = new[i + 1] + a
            new[i] = new[i] - a * c
        poly = new
    out = []
    for a in poly:
        assert a.c[1] == 0 and a.c[2] == 0 and a.c[3] == 0, a
        out.append(a.c[0])
    return out  # low -> high, Fractions

# ---------------------------------------------------------------------------
# Recognition polynomials (claim C5)
# ---------------------------------------------------------------------------
def PQ_polys(U):
    U0, U1, U2, U3 = U
    P0 = U0*U0 + 3*U1*U1 - 2*U2*U2 - 6*U3*U3
    P1 = 2*(U0*U1 - 2*U2*U3)
    Q0 = U0*U0 - 3*U1*U1 + 2*U2*U2 - 6*U3*U3
    Q1 = 2*(U0*U2 - 3*U1*U3)
    return P0, P1, Q0, Q1

def main():
    import cypari2
    pari = cypari2.Pari(); pari.allocatemem(512 * 1024 * 1024)
    res = {}
    assert _sympy_check()
    res["ring_arith_sympy_crosscheck"] = "passed (50 random products + inverses)"

    # ---- C1 generic check with symbolic q: use sympy over Q(A, q) with B = -q^3 - A q
    import sympy as sp
    Asym, qsym, xsym = sp.symbols("A q x")
    Bsym = -qsym**3 - Asym*qsym
    # my own Velu derivation, symbolic
    a = 3*qsym; b = 3*qsym**2 + Asym; s = 2*qsym
    A1s = sp.expand(3*s*s - 4*a*s + (a*a - 4*b))
    B1s = sp.expand(s**3 - 2*a*s*s + (a*a - 4*b)*s)
    res["C1_symbolic"] = {
        "A_prime": str(A1s), "B_prime": str(B1s),
        "A_prime_matches_-4A-15q^2": sp.expand(A1s - (-4*Asym - 15*qsym**2)) == 0,
        "B_prime_matches_-8Aq-22q^3": sp.expand(B1s - (-8*Asym*qsym - 22*qsym**3)) == 0,
        "factorization": str(sp.factor(xsym**3 + A1s*xsym + B1s)),
        "cofactor_identity": sp.expand(xsym**3 + A1s*xsym + B1s - (xsym + 2*qsym)*(xsym**2 - 2*qsym*xsym + (A1s + 4*qsym**2))) == 0,
        "quadratic_roots": [str(sp.simplify(r)) for r in sp.solve(xsym**2 - 2*qsym*xsym + (A1s + 4*qsym**2), xsym)],
        "dual_root_-2q_is_root": sp.expand((-2*qsym)**3 + A1s*(-2*qsym) + B1s) == 0,
        "double_step_at_dual_root_gives_16A_64B": None,
    }
    # double step: apply the step at the dual root -2q on (A1s, B1s)
    q2 = -2*qsym
    a = 3*q2; b = 3*q2**2 + A1s; s = 2*q2
    A2s = sp.expand(3*s*s - 4*a*s + (a*a - 4*b))
    B2s = sp.expand(s**3 - 2*a*s*s + (a*a - 4*b)*s)
    res["C1_symbolic"]["double_step_at_dual_root_gives_16A_64B"] = (sp.expand(A2s - 16*Asym) == 0 and sp.expand(B2s - 64*Bsym) == 0)

    # ---- C2 family
    fam = build_family()
    alpha, gamma = fam["A3"], fam["B3"]
    res["C2_family"] = {
        "A1,B1": [fam["A1"].ints(), fam["B1"].ints()],
        "q1": fam["q1"].ints(),
        "A2,B2": [fam["A2"].ints(), fam["B2"].ints()],
        "q2": fam["q2"].ints(),
        "alpha": alpha.ints(), "gamma": gamma.ints(),
        "alpha_claimed": (-1095, -540, -540, -420), "gamma_claimed": (-22198, -13860, -16380, -8820),
        "alpha_matches": alpha.ints() == (-1095, -540, -540, -420),
        "gamma_matches": gamma.ints() == (-22198, -13860, -16380, -8820),
    }
    mult = beta_multiplier(fam)
    res["C2_family"]["beta_multiplier"] = mult.ints()
    res["C2_family"]["beta_multiplier_matches_-(7,6,6,2)"] = mult.ints() == (-7, -6, -6, -2)
    rev_roots, endpoint = reverse_check(fam)
    res["C2_family"]["reverse_roots"] = rev_roots
    res["C2_family"]["reverse_endpoint"] = endpoint
    res["C2_family"]["reverse_endpoint_is_(0,-(64)^3)"] = endpoint == ((0,0,0,0), (-(64**3),0,0,0))
    # alternative sign choices at each step produce conjugates; check that the four
    # Galois conjugates of (alpha,gamma) are exactly the other sign choices
    # (step 2 sign flips e; step 3 sign flips g)
    q1m = ONE - 2*E
    A2m, B2m, _ = cofactor_roots(fam["A1"], fam["B1"], q1m)
    assert A2m == fam["A2"].conj_e() and B2m == fam["B2"].conj_e()
    q2m = fam["q1"] - 2*(3*G + E*G)
    A3m, B3m, _ = cofactor_roots(fam["A2"], fam["B2"], q2m)
    assert A3m == alpha.conj_g() and B3m == gamma.conj_g()
    res["C2_family"]["other_sign_choices_are_galois_conjugates"] = True

    # ---- alpha^3, gamma^2 (C5 constants)
    a3 = alpha**3; g2 = gamma**2
    res["C5_constants"] = {
        "alpha^3": a3.ints(), "gamma^2": g2.ints(),
        "alpha^3_claimed": (-13988298375,-8054356500,-9859360500,-5708191500),
        "gamma^2_claimed": (2072413204,1193214960,1460677680,845626320),
        "alpha^3_matches": a3.ints() == (-13988298375,-8054356500,-9859360500,-5708191500),
        "gamma^2_matches": g2.ints() == (2072413204,1193214960,1460677680,845626320),
    }
    # symbolic verification that U*conj_g(U) = P0 + P1 e and U*conj_e(U) = Q0 + Q1 g
    U = sp.symbols("U0:4")
    Usym = BQ(0)  # not used; do it via sympy directly
    e_, g_ = sp.sqrt(3), sp.sqrt(2)
    Uexpr = U[0] + U[1]*e_ + U[2]*g_ + U[3]*e_*g_
    Ucg   = U[0] + U[1]*e_ - U[2]*g_ - U[3]*e_*g_
    Uce   = U[0] - U[1]*e_ + U[2]*g_ - U[3]*e_*g_
    P0 = U[0]**2 + 3*U[1]**2 - 2*U[2]**2 - 6*U[3]**2
    P1 = 2*(U[0]*U[1] - 2*U[2]*U[3])
    Q0 = U[0]**2 - 3*U[1]**2 + 2*U[2]**2 - 6*U[3]**2
    Q1 = 2*(U[0]*U[2] - 3*U[1]*U[3])
    res["C5_constants"]["P_identity_U*conj_g(U)=P0+P1e"] = sp.simplify(sp.expand(Uexpr*Ucg) - (P0 + P1*e_)) == 0
    res["C5_constants"]["Q_identity_U*conj_e(U)=Q0+Q1g"] = sp.simplify(sp.expand(Uexpr*Uce) - (Q0 + Q1*g_)) == 0

    # ---- C3 j-invariant and minimal polynomial
    j, disc_den = j_invariant(alpha, gamma)
    mp = minpoly_from_conjugates(j)
    assert all(x.denominator == 1 for x in mp)
    mp_int = [int(x) for x in mp]
    H_claimed = [-1080060886113159937649308593750000, 826335556188178615474500000000,
                 15705521635909735050750000, -8041801037378436000, 1]
    pc = pari("polclass(-192)")
    pc_coeffs = [int(pc.polcoef(i)) for i in range(5)]
    res["C3_minpoly"] = {
        "j_in_basis": [str(x) for x in j.c],
        "minpoly_low_to_high": mp_int,
        "matches_claim": mp_int == H_claimed,
        "pari_polclass(-192)_low_to_high": pc_coeffs,
        "matches_pari_polclass": mp_int == pc_coeffs,
        "pari_classno(-192)": int(pari("qfbclassno(-192)")),
        "j_is_root_of_polclass_in_BQ": sum((BQ(c) * j**i for i, c in enumerate(pc_coeffs)), BQ(0)).is_zero(),
        "4alpha^3+27gamma^2": disc_den.ints(),
    }
    # field generated by j: check that the four conjugates are distinct and that
    # j is NOT fixed by any nontrivial automorphism => Q(j) = Q(e,g)
    conjs = [j, j.conj_e(), j.conj_g(), j.conj_eg()]
    res["C3_minpoly"]["four_conjugates_distinct"] = all(not (conjs[i] - conjs[k]).is_zero() for i in range(4) for k in range(i+1, 4))

    # ---- C6 integer invariants
    def fac(n):
        n = int(n)
        f = pari.factor(abs(n))
        return [[int(f[0][i]), int(f[1][i])] for i in range(len(f[0]))]
    def primes_mod24(fl):
        return sorted(set((p, p % 24) for p, _ in fl))
    inv = {}
    items = {
        "N(alpha)": alpha.norm(),
        "N(gamma)": gamma.norm(),
        "N(4alpha^3+27gamma^2)": disc_den.norm(),
    }
    # collision norms: N(gamma^2 sigma(alpha)^3 - alpha^3 sigma(gamma)^2) for the three nontrivial sigma
    for name, sig in (("sigma_e", BQ.conj_e), ("sigma_g", BQ.conj_g), ("sigma_eg", BQ.conj_eg)):
        coll = g2 * sig(alpha)**3 - a3 * sig(gamma)**2
        items["N(collision_%s)" % name] = coll.norm()
    Hpol = pari("polclass(-192)")
    items["H(0)"] = int(Hpol.subst("x", 0))
    items["H(1728)"] = int(Hpol.subst("x", 1728))
    items["H(54000)"] = int(Hpol.subst("x", 54000))
    items["H(287496)"] = int(Hpol.subst("x", 287496))
    items["Res(H,H_-64)"] = int(pari.polresultant(Hpol, pari("x^2-82226316240*x-7367066619912")))
    items["Res(H,H_-48)"] = int(pari.polresultant(Hpol, pari("x^2-2835810000*x+6549518250000")))
    items["disc(H)"] = int(pari.poldisc(Hpol))
    bad = {}
    for k, v in items.items():
        v = int(v)
        fl = fac(v)
        pm = primes_mod24(fl)
        inv[k] = {"value": v, "factorization": fl, "primes_mod24": pm,
                  "has_prime_1_mod_24": any(m == 1 for _, m in pm)}
        if inv[k]["has_prime_1_mod_24"]:
            bad[k] = [p for p, m in pm if m == 1]
    res["C6_invariants"] = inv
    res["C6_any_prime_1_mod_24"] = bad
    # sanity: H_-64 and H_-48 from pari
    res["C6_aux"] = {"polclass(-64)": str(pari("polclass(-64)")), "polclass(-48)": str(pari("polclass(-48)"))}

    with open("indep_symbolic_results.json", "w") as f:
        json.dump(res, f, indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))

if __name__ == "__main__":
    main()
