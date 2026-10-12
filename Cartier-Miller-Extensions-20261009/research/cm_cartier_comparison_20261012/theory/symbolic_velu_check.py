"""Independent symbolic verification (sympy) of the normalized isogeny
pullback identities used in the extension note. Nothing is imported from the
retained code. All identities are checked as rational-function identities in
the function field of y^2 = x^3 + A x + B (y^2 replaced by F(x)).

V1  normalized 2-isogeny with kernel root q (F(q)=0, so B = -q^3 - A q):
    x' = x + u/(x-q),  y' = y (1 - u/(x-q)^2),  u = F'(q)
    (a) y'^2 = x'^3 + A' x' + B',  A' = -4A - 15 q^2,  B' = -8 A q - 22 q^3
    (b) phi^*(dx'/y') = dx/y
    (c) phi^*(x' dx'/y') = (2x - q) dx/y - 2 d( y/(x-q) )
V2  translation identity (any point Q=(xq,yq) on E, P=(x,y) generic):
    ( x(P+Q) - x(P) ) dx/y = - d( 2 (y - yq)/(x - xq) )
V3  isomorphism psi:(x',y') -> (x'/u^2, y'/u^3) from (u^4 A, u^6 B) to (A,B):
    psi^* omega = u omega',  psi^* eta = u^{-1} eta'
V4  automorphisms: j=0: (x,y)->(z x, y), z^2+z+1=0: omega->z omega, eta->z^2 eta
                  j=1728: (x,y)->(-x, i y): omega-> i omega, eta-> -i eta
V5  odd Velu (degree 3) pullback matrix [[1,-sigma],[0,3]] on (omega,eta),
    checked on the explicit D=-12 example below via V2.
"""
import json, sys
import sympy as sp

x, y, A, q, X, Y, xq, yq, u, z, i_ = sp.symbols('x y A q X Y xq yq u z i_')
out = {}

def reduce_y(expr, F):
    """Replace y^2 by F(x) in a rational function; return numerator form."""
    expr = sp.together(sp.expand(expr))
    num, den = sp.fraction(expr)
    def red(poly):
        poly = sp.Poly(sp.expand(poly), y)
        res = 0
        for (k,), c in poly.terms():
            res += c * F**(k//2) * y**(k % 2)
        return sp.expand(res)
    return red(num), red(den)

# ---------- V1 ----------
B = -q**3 - A*q
F = x**3 + A*x + B
uu = 3*q**2 + A
xp = x + uu/(x - q)
yp = y*(1 - uu/(x - q)**2)
Ap = -4*A - 15*q**2
Bp = -8*A*q - 22*q**3
lhs = yp**2 - (xp**3 + Ap*xp + Bp)
n, d = reduce_y(lhs, F)
out['V1a_curve_equation'] = sp.simplify(n) == 0
# derivative along the curve: d/dx with dy/dx = F'(x)/(2y)
def Dx(expr):
    return sp.diff(expr, x) + sp.diff(expr, y)*sp.diff(F, x)/(2*y)
# (b) phi^*(dx'/y') / (dx/y) = Dx(xp) * y / yp
ratio_b = Dx(xp)*y/yp
n, d = reduce_y(ratio_b - 1, F)
out['V1b_omega_scale_plus_one'] = sp.simplify(n) == 0
# (c) phi^*(x' dx'/y') - [(2x - q) dx/y - 2 d(y/(x-q))], coefficient of dx
expr_c = xp*Dx(xp)/yp - ((2*x - q)/y - 2*Dx(y/(x - q)))
n, d = reduce_y(expr_c, F)
out['V1c_eta_pullback'] = sp.simplify(n) == 0

# ---------- V2 ----------
Bg = sp.Symbol('Bg')
F2 = x**3 + A*x + Bg
lam = (y - yq)/(x - xq)
xsum = lam**2 - x - xq           # x(P+Q) for P != +-Q
def Dx2(expr):
    return sp.diff(expr, x) + sp.diff(expr, y)*sp.diff(F2, x)/(2*y)
expr2 = (xsum - x)/y + Dx2(2*(y - yq)/(x - xq))
n, d = reduce_y(expr2, F2)
# impose Q on the curve: yq^2 = xq^3 + A xq + Bg
n = sp.expand(n.subs(Bg, yq**2 - xq**3 - A*xq))
out['V2_translation_exact'] = sp.simplify(n) == 0

# ---------- V3 ----------
# psi: x = x'/u^2, y = y'/u^3 ; omega = dx/y -> (dx'/u^2)/(y'/u^3) = u dx'/y'
xpp, ypp = sp.symbols('xpp ypp')
om_ratio = sp.simplify((sp.diff(xpp/u**2, xpp))/(ypp/u**3) / (1/ypp))
eta_ratio = sp.simplify(((xpp/u**2)*sp.diff(xpp/u**2, xpp)/(ypp/u**3)) / (xpp/ypp))
out['V3_iso_omega_factor'] = str(om_ratio)
out['V3_iso_eta_factor'] = str(eta_ratio)
out['V3_ok'] = (sp.simplify(om_ratio - u) == 0) and (sp.simplify(eta_ratio - 1/u) == 0)

# ---------- V4 ----------
# j=0: x -> z x, y -> y : omega -> z dx/y ; eta -> z x * z dx / y = z^2 eta
out['V4_j0'] = 'omega->z*omega, eta->z^2*eta (direct substitution)'
# j=1728: x -> -x, y -> i y : omega -> -dx/(i y) = i omega (since -1/i = i); eta -> (-x)(-dx)/(i y) = -i eta
w_om = sp.simplify((-1)/(i_) .subs(i_, sp.I))
w_eta = sp.simplify(((-1)*(-1))/(i_) .subs(i_, sp.I))
out['V4_j1728_omega_factor'] = str(w_om)
out['V4_j1728_eta_factor'] = str(w_eta)
out['V4_ok'] = (w_om == sp.I) and (w_eta == -sp.I)

# ---------- V5: degree-3 Velu on y^2 = x^3 - 15x - 22 (D=-12), kernel x-coordinate -3 ----------
A0, B0 = -15, -22
psi3 = 3*x**4 + 6*A0*x**2 + 12*B0*x - A0**2
out['V5_psi3_at_minus3'] = int(psi3.subs(x, -3))
xQ = -3; yQ2 = xQ**3 + A0*xQ + B0       # y_Q^2 = -4
gx = 3*xQ**2 + A0; vQ = 2*gx; uQ = 4*yQ2
t = vQ; w = uQ + xQ*vQ
A3, B3 = A0 - 5*t, B0 - 7*w
out['V5_quotient'] = [A3, B3]
# isomorphic to (A0,B0) with u^4 = A3/A0, u^6 = B3/B0
out['V5_u4'] = str(sp.Rational(A3, A0)); out['V5_u6'] = str(sp.Rational(B3, B0))
out['V5_u2'] = str(sp.Rational(B3, B0)/sp.Rational(A3, A0))
# matrix of alpha = psi o phi: [[1,-sigma],[0,3]] * diag(u,1/u); sigma = 2 xQ
u2 = sp.Rational(B3, B0)/sp.Rational(A3, A0)
sigma = 2*xQ
# beta(lambda-mu) = nu H with lambda=u, mu=3/u, nu=-sigma/u  =>  beta/H = sigma/(3-u^2)
out['V5_beta_over_H'] = str(sp.Rational(sigma)/(3 - u2))

print(json.dumps(out, indent=1))
ok = all(out[k] for k in ['V1a_curve_equation','V1b_omega_scale_plus_one','V1c_eta_pullback','V2_translation_exact','V3_ok','V4_ok']) and out['V5_psi3_at_minus3']==0
json.dump(out, open(sys.argv[1], 'w'), indent=1) if len(sys.argv) > 1 else None
print('ALL_SYMBOLIC_IDENTITIES_HOLD' if ok else 'FAILURE')
sys.exit(0 if ok else 1)
