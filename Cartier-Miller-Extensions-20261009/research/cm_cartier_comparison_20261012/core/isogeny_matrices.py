"""De Rham pullback matrices of the explicit maps used in the note.
Convention: for f: E1 -> E2, f^*(omega2, eta2) = (omega1, eta1) M_f with
M_f = [[a, b], [0, d]] meaning f^*omega2 = a omega1 and
f^*eta2 = b omega1 + d eta1 + (exact differential).
Composition: M_{f o g} = M_g M_f.
  normalized Velu 2-isogeny with kernel root q : [[1, -q], [0, 2]]
  normalized odd Velu isogeny, kernel G         : [[1, -sigma_G], [0, ell]]
  isomorphism (x',y') -> (x'/u^2, y'/u^3)        : [[u, 0], [0, 1/u]]
  j=0 automorphism (x,y)->(z x, y)               : [[z, 0], [0, z^2]]
  j=1728 automorphism (x,y)->(-x, i y)          : [[i, 0], [0, -i]]
Theorem 1 (characteristic p): if alpha^*omega = lam omega and
alpha^*eta = nu omega + mu eta + exact, then beta (lam - mu) = nu H.
"""

def matmul(T, M, N):
    (a1, b1), (_, d1) = M
    (a2, b2), (_, d2) = N
    return ((T.mul(a1, a2), T.add(T.mul(a1, b2), T.mul(b1, d2))), (None, T.mul(d1, d2)))

def velu2(T, q):
    return ((T.const(1), T.neg(q)), (None, T.const(2)))

def velu_odd(T, sigma, ell):
    return ((T.const(1), T.neg(sigma)), (None, T.const(ell)))

def iso(T, u):
    return ((u, T.const(0)), (None, T.inv(u)))

def aut(T, a, d):
    return ((a, T.const(0)), (None, d))

def quotient2(T, A, B, q):
    """Normalized 2-isogeny quotient; asserts q is a root."""
    F = T.add(T.add(T.pow(q, 3), T.mul(A, q)), B)
    assert T.is_zero(F), 'kernel coordinate is not a root'
    A2 = T.sub(T.neg(T.mul(T.const(4), A)), T.mul(T.const(15), T.mul(q, q)))
    B2 = T.sub(T.neg(T.mul(T.const(8), T.mul(A, q))), T.mul(T.const(22), T.pow(q, 3)))
    return A2, B2

def slope_from_matrix(T, M):
    """Return (lam, mu, nu, c, slope) with c = nu/(mu-lam) the eigenline
    coefficient (eta + c omega) and slope = beta/H = -c."""
    (lam, nu), (_, mu) = M
    c = T.div(nu, T.sub(mu, lam))
    return lam, mu, nu, c, T.neg(c)
