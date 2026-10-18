"""Round-3 half-interval acquisition (supersedes the status labels of charp.py; charp.py is frozen
and unchanged).

c_p = 2 H P^3,  P = prod_{j=m+1}^{h} j  ((p+1)/6 factors),  H = ((p-1)/2)!   [C1, elementary]
H, sign included, from one imaginary quadratic class number:
  'mordell'          p = 3 mod 4 : H = (-1)^{(h(-p)+1)/2}                     Mordell (1961)
  'williams_currie'  p = 1 mod 4 : H = (-1)^{q0 + (h(-3p)-2)/4} 3^{q0}, q0=(p-1)/4
                     Williams & Currie (1982), Lemma 14(c) with q = 3: for p = 1 mod 4 and
                     (p/3) = -1, (-3)^{(p-1)/4} = (-1)^{(h(-3p)-2)/4} ((p-1)/2)! (mod p).
                     This proves round-2 identity (*); the p = 17 mod 24 route is a THEOREM.
  'gauss4p'          p = 5 mod 8 : Gauss (1828) + Dirichlet, as in round 2 (kept as a cross-check).
Class numbers come from a ClassNumberPolicy (r3.common): PARI qfbclassno only inside its documented
unconditional range |D| < 2e10, the reduced-form count otherwise, or a separately labelled GRH backend.
"""
from .common import params, ClassNumberPolicy, flint_rising


def half_factorial3(p, policy, route=None):
    P = params(p)
    q0 = P['q0']
    if route is None:
        route = 'mordell' if p % 4 == 3 else 'williams_currie'
    if route == 'mordell':
        if p % 4 != 3:
            raise ValueError('mordell route needs p = 3 mod 4')
        hD, backend, status = policy(-p)
        H = 1 if ((hD + 1) // 2) % 2 == 0 else p - 1
        return H, dict(route=route, D=-p, classno=hD, backend=backend, classno_status=status,
                       theorem='Mordell (1961)')
    if route == 'williams_currie':
        if p % 4 != 1:
            raise ValueError('Williams-Currie route needs p = 1 mod 4')
        hD, backend, status = policy(-3 * p)
        if hD % 4 != 2:
            raise ArithmeticError('h(-3p) must be 2 mod 4 (Redei); class-number backend failed')
        e = q0 + (hD - 2) // 4
        H = pow(3, q0, p)
        if e % 2:
            H = p - H
        return H, dict(route=route, D=-3 * p, classno=hD, backend=backend, classno_status=status,
                       theorem='Williams & Currie (1982) Lemma 14(c)')
    if route == 'gauss4p':
        import charp
        hD, backend, status = policy(-4 * p)
        H, meta = charp.half_factorial(p, 'gauss4p', classno_fn=lambda D: hD)
        meta.update(backend=backend, classno_status=status)
        return H, meta
    raise ValueError(route)


def halfinterval_c3(p, policy=None, route=None, engine='flint'):
    policy = policy or ClassNumberPolicy('unconditional')
    P = params(p)
    start, L = P['m'] + 1, (p + 1) // 6
    H, hmeta = half_factorial3(p, policy, route)
    if engine == 'flint':
        (Pv,), _ = flint_rising(p, L, [start])
    else:
        Pv = 1
        for j in range(start, start + L):
            Pv = Pv * j % p
    c = 2 * H * pow(Pv, 3, p) % p
    return c, dict(route='half_interval', half_factorial=hmeta, product_length=L, engine=engine,
                   status=('GRH-conditional' if hmeta['classno_status'] == 'GRH-conditional'
                           else 'unconditional'))
