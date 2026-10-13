"""
Weierstrass model of the genus-one curve C: v^2 = f(w), f(0) = 1, deg f in {3, 4}, sending P+ = (0, 1) to O.
Functions with poles only at P+ (Riemann–Roch basis of L(2P+), L(3P+)), Connell's normalisation:
    x = (2(v+1) + f1 w) / w^2,
    y = (4(v+1) + 2(f1 w + f2 w^2) - f1^2 w^2 / 2) / w^3,
    y^2 + a1 x y + a3 y = x^3 + a2 x^2 + a4 x + a6,
    a1 = f1, a2 = f2 - f1^2/4, a3 = 2 f3, a4 = -4 f4, a6 = a2 a4.
Then the short model  Y^2 = X^3 + A X + B  via  Y = y + (a1 x + a3)/2,  X = x + b2/12  (p >= 5).
The invariant differential dX/(2Y) equals dx/(2y + a1 x + a3); kappa := (dw/v) / (dX/(2Y)) is a constant.
All formulas are re-verified numerically in validate.py (random points, and Laurent series at P+).
"""
from .fields import FpCtx, legendre

class Model:
    def __init__(s, f, p):
        assert p >= 5
        f = [c % p for c in f] + [0]*(5 - len(f))
        assert f[0] == 1 and (f[3] or f[4]), "need f(0)=1 and degree 3 or 4"
        s.f, s.p = f[:5], p
        s.deg = 4 if f[4] else 3
        i = lambda n: pow(n, -1, p)
        f1, f2, f3, f4 = f[1], f[2], f[3], f[4]
        s.a1, s.a2, s.a3, s.a4 = f1, (f2 - f1*f1*i(4)) % p, 2*f3 % p, (-4*f4) % p
        s.a6 = s.a2 * s.a4 % p
        b2 = (s.a1*s.a1 + 4*s.a2) % p
        b4 = (2*s.a4 + s.a1*s.a3) % p
        b6 = (s.a3*s.a3 + 4*s.a6) % p
        s.b2 = b2
        s.A = (b4*i(2) - b2*b2*i(48)) % p
        s.B = (b6*i(4) - b2*b4*i(24) + b2*b2*b2*i(864)) % p
        s.kappa = (-2) % p      # derived: dX/(2Y) = -(1/2) dw/v ; re-verified by series in validate.py
        s.disc = (-16*(4*pow(s.A, 3, p) + 27*s.B*s.B)) % p
    def fval(s, ctx, w):
        acc = ctx.zero
        for c in reversed(s.f): acc = ctx.add(ctx.mul(acc, w), ctx.fromint(c))
        return acc
    def to_short(s, ctx, w, v):
        """Image of an affine point (w, v) of C with w != 0 on Y^2 = X^3 + A X + B."""
        p = s.p; i = lambda n: pow(n, -1, p)
        f1, f2 = s.f[1], s.f[2]
        winv = ctx.inv(w); winv2 = ctx.mul(winv, winv); winv3 = ctx.mul(winv2, winv)
        vp1 = ctx.add(v, ctx.one)
        x = ctx.mul(ctx.add(ctx.mul(ctx.fromint(2), vp1), ctx.mul(ctx.fromint(f1), w)), winv2)
        inner = ctx.add(ctx.add(ctx.mul(ctx.fromint(4), vp1),
                                ctx.mul(ctx.fromint(2), ctx.add(ctx.mul(ctx.fromint(f1), w),
                                                                ctx.mul(ctx.fromint(f2), ctx.mul(w, w))))),
                        ctx.mul(ctx.fromint((-f1*f1*i(2)) % p), ctx.mul(w, w)))
        y = ctx.mul(inner, winv3)
        Y = ctx.add(y, ctx.mul(ctx.fromint(i(2)), ctx.add(ctx.mul(ctx.fromint(s.a1), x), ctx.fromint(s.a3))))
        X = ctx.add(x, ctx.fromint(s.b2 * i(12)))
        return (X, Y)
    def image_of_Pminus(s):
        """Image of P- = (0, -1) (limit w -> 0 on the branch v = -sqrt f); exact Laurent evaluation."""
        p = s.p; i = lambda n: pow(n, -1, p)
        f1, f2, f3 = s.f[1], s.f[2], s.f[3]
        # sqrt(f) = 1 + s1 w + s2 w^2 + s3 w^3 + ...
        s1 = f1*i(2) % p
        s2 = (f2 - s1*s1) * i(2) % p
        s3 = (f3 - 2*s1*s2) * i(2) % p
        # on P- branch v = -(1 + s1 w + s2 w^2 + s3 w^3 + ...):  v+1 = -(s1 w + s2 w^2 + s3 w^3)
        x = (2*(-s2) + 0) % p                        # (2(v+1) + f1 w)/w^2 -> -2 s2   (since 2 s1 = f1)
        y = (4*(-s3)) % p                            # (4(v+1) + 2 f1 w + (2 f2 - f1^2/2) w^2)/w^3 -> -4 s3
        Y = (y + (s.a1*x + s.a3)*i(2)) % p
        X = (x + s.b2*i(12)) % p
        return (X, Y)

def trace_naive(A, B, p):
    return -sum(legendre(x*x*x + A*x + B, p) for x in range(p))

_PARI = None
def get_pari():
    global _PARI
    if _PARI is None:
        import cypari2; _PARI = cypari2.Pari(); _PARI.allocatemem(2*10**8, silent=True)
    return _PARI

def trace_pari(A, B, p):
    pari = get_pari()
    E = pari.ellinit([A, B], p)
    return int(pari.ellap(E))
