"""Independent symbolic re-check of the retained normalized degree-two transport.

Checks, as exact rational-function identities on y^2 = x^3 + A x + B with
q^3 + A q + B = 0 (q a rational 2-torsion abscissa):
  1. x' = x + (A+3q^2)/(x-q), y' = y (1 - (A+3q^2)/(x-q)^2) satisfies
     y'^2 = x'^3 + A' x' + B' with A' = -4A - 15 q^2, B' = -8 A q - 22 q^3.
  2. dx'/y' = dx/y (holomorphic scale +1).
  3. x' dx'/y' = (2x - q) dx/y - 2 d( y/(x-q) ) (exact global correction).
  4. The dual kernel -2q on the target returns (16A, 64B).
  5. The quadratic cofactor at the target has roots q +- 2 sqrt(A + 3 q^2).
Cartier naturality then gives H' = H, beta' = 2 beta - q H; the sympy check
covers the algebraic identities, not the Cartier step itself, which is argued
in the proof note.
"""
import sympy as sp

x, y, A, q, t = sp.symbols('x y A q t')
B = -(q**3 + A*q)                 # q is a root of x^3 + A x + B
F = x**3 + A*x + B
u = A + 3*q**2
xp = x + u/(x - q)
yp = y*(1 - u/(x - q)**2)
Ap = -4*A - 15*q**2
Bp = -8*A*q - 22*q**3


def on_curve(expr):
    """Reduce a rational expression modulo y^2 = F(x)."""
    expr = sp.together(sp.expand(expr))
    num, den = sp.fraction(expr)
    num = sp.Poly(sp.expand(num), y)
    # replace y^2 by F repeatedly
    out = 0
    for (k,), c in num.terms():
        out += c * F**(k // 2) * y**(k % 2)
    return sp.simplify(sp.expand(out) / den)


# 1. curve equation of the quotient
assert sp.simplify(on_curve(yp**2 - (xp**3 + Ap*xp + Bp))) == 0
# 2. holomorphic differential: dx'/y' = dx/y
dxp = sp.diff(xp, x)              # dx' = (dxp/dx) dx
assert sp.simplify(dxp/yp - 1/y) == 0
# 3. second-kind identity, written as coefficients of dx/y:
#    x' * (dx'/y') = x' dx/y; d(y/(x-q)) = [F'(x-q) - 2F]/(2 (x-q)^2) dx/y
dprim = (sp.diff(F, x)*(x - q) - 2*F)/(2*(x - q)**2)
assert sp.simplify(xp - ((2*x - q) - 2*dprim)) == 0
# 4. dual step
qq = -2*q
assert sp.simplify(qq**3 + Ap*qq + Bp) == 0
App = -4*Ap - 15*qq**2
Bpp = -8*Ap*qq - 22*qq**3
assert sp.simplify(App - 16*A) == 0 and sp.simplify(Bpp - 64*B) == 0
# 5. cofactor roots on the target
cof = sp.expand((x**3 + Ap*x + Bp)/(x + 2*q))
cof = sp.Poly(sp.cancel(cof), x)
assert cof.degree() == 2
disc = sp.discriminant(cof.as_expr(), x)
assert sp.simplify(disc - 16*u) == 0
root = q + 2*sp.sqrt(u)
assert sp.simplify(cof.as_expr().subs(x, root)) == 0
print('transport identities verified: curve equation, scale +1, exact correction, dual scaling, cofactor roots q +- 2 sqrt(A+3q^2)')
