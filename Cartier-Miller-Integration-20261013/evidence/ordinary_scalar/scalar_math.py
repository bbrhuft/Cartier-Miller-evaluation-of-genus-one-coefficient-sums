"""Arithmetic references and local compatibility jets; no fast scalar solver.

This module never opens validation fixtures or retained target residues.
Its functions assume a certified prime unless explicitly stated otherwise.
Ordinary Taylor equations are verified modulo z**r, not as derivations of
an arbitrary truncated quotient ring. Python standard library only.
"""


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def mul(a, b, p):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = (out[i+j] + x*y) % p
    return out


def power(f, n, p):
    out = [1]
    while n:
        if n & 1:
            out = mul(out, f, p)
        n >>= 1
        if n:
            f = mul(f, f, p)
    return out


def coefficient(poly, n):
    return poly[n] if n < len(poly) else 0


def dense_target(A, B, p):
    P = power([B % p, A % p, 0, 1], (p-1)//2, p)
    return coefficient(P, p-1), coefficient(P, p-2)


def trace_count(A, B, p):
    total = 0
    for x in range(p):
        s = pow((x**3 + A*x + B) % p, (p-1)//2, p)
        total += -1 if s == p-1 else s
    return -total


def dmul(a, b, p):
    return a[0]*b[0] % p, (a[0]*b[1]+a[1]*b[0]) % p


def dpower(a, n, p):
    out = (1, 0)
    while n:
        if n & 1:
            out = dmul(out, a, p)
        n >>= 1
        if n:
            a = dmul(a, a, p)
    return out


def dinv(a, p):
    require(a[0] % p != 0, 'dual inverse needs nonzero constant term')
    inv = pow(a[0], -1, p)
    return inv, -a[1]*inv*inv % p


def scaled_recurrence_jets(A, B, p):
    """Exact O(p) arithmetic derivative circuit, O(1) field state; B!=0.

    F_eps=B_eps*(1+c_eps*x+a_eps*x**3). Set V_n=n! times
    (u_n,u_(n-1),u_(n-2)) for coefficients u of the normalized power.
    Its three-by-three recurrence is degree one in n. Wilson normalization
    and the dual prefactor B_eps**h give both H and beta jets. This is an
    explicit valid AD circuit, not differentiated Schoof or a new exponent.
    """
    i3 = pow(3, -1, p)
    Ae = (A % p, 6*B % p)
    Be = (B % p, -4*i3*A*A % p)
    invB = dinv(Be,p)
    c,a = dmul(Ae,invB,p), invB
    prefactor=dpower(Be,(p-1)//2,p)
    v0,v1,v2=(1,0),(0,0),(0,0)
    h1=(p+1)//2
    for n in range(1,p):
        term1=dmul(c,v0,p)
        term3=dmul(a,v2,p)
        top=tuple(((h1-n)*term1[i]+(3*h1-n)*term3[i]) % p for i in range(2))
        v0,v1,v2=top,tuple(n*x%p for x in v0),tuple(n*x%p for x in v1)
    H,b=dmul(prefactor,v0,p),dmul(prefactor,v1,p)
    return tuple(-x%p for x in H),tuple(-x%p for x in b)


def dual_jet(A, B, p, *, wrong_direction=False):
    dA = 6*B % p
    dB = (-4*A*A*pow(3, -1, p)) % p
    if wrong_direction:
        dB = -dB % p
    f = [(B % p, dB), (A % p, dA), (0, 0), (1, 0)]
    out = [(1, 0)]
    for _ in range((p-1)//2):
        q = [(0, 0)] * (len(out)+3)
        for i, a in enumerate(out):
            for j, b in enumerate(f):
                c = dmul(a, b, p)
                q[i+j] = ((q[i+j][0]+c[0]) % p, (q[i+j][1]+c[1]) % p)
        out = q
    return out[p-1]


def character_power_jet(A, B, p):
    """Arithmetic Euler-power sum, O(p log p); not a symbol-valued counter."""
    total = (0, 0)
    i3 = pow(3, -1, p)
    for x in range(p):
        c = dpower(((x**3+A*x+B) % p, (6*B*x-4*i3*A*A) % p), (p-1)//2, p)
        total = ((total[0]+c[0]) % p, (total[1]+c[1]) % p)
    return -total[0] % p, -total[1] % p


def hasse_terms(p, exponent):
    """Independent exact multinomial polynomial, used for validation only."""
    from math import factorial
    h = (p-1)//2
    out = {}
    for i in range(h+1):
        j = exponent - 3*i
        k = h-i-j
        if j >= 0 and k >= 0:
            c = factorial(h)//(factorial(i)*factorial(j)*factorial(k))
            if c % p:
                out[j, k] = c % p
    return out


def theta(poly, p):
    out = {}
    i3 = pow(3, -1, p)
    for (j, k), c in poly.items():
        for key, value in (((j-1, k+1), 6*j*c), ((j+2, k-1), -4*i3*k*c)):
            if value % p:
                out[key] = (out.get(key, 0)+value) % p
    return {key: c for key, c in out.items() if c}


def conv(a, b, n, p):
    return sum(a[i]*b[n-i] for i in range(n+1)) % p


def smul(a, b, p, r):
    return [sum(a[i]*b[n-i] for i in range(n+1)
                if i < len(a) and n-i < len(b)) % p for n in range(r+1)]


def sinv(a, p, r):
    require(a[0] % p != 0, 'series inversion needs a unit constant term')
    out = [pow(a[0], -1, p)]
    for n in range(1, r+1):
        out.append(-out[0]*sum(a[i]*out[n-i] for i in range(1, min(n, len(a)-1)+1)) % p)
    return out


def deriv(a, p):
    return [n*a[n] % p for n in range(1, len(a))]


def local_jets(A0, B0, H0, proposed_slope, p, r):
    """Construct necessary-equation jets for ANY proposed initial slope."""
    require(1 <= r < p, 'ordinary Taylor order must satisfy 1 <= r < p')
    require(H0 % p != 0, 'ordinary input needs H nonzero')
    i3 = pow(3, -1, p)
    A, B, H, b = [[value % p]+[0]*r for value in
                   (A0, B0, H0, proposed_slope*H0)]
    for n in range(r):
        inv = pow(n+1, -1, p)
        A[n+1] = 6*B[n]*inv % p
        B[n+1] = -4*i3*conv(A, A, n, p)*inv % p
        H[n+1] = b[n]*inv % p
        b[n+1] = i3*conv(A, H, n, p)*inv % p
    k = smul(b, sinv(H, p, r), p, r)
    norm = [x*pow(H0, -1, p) % p for x in H]
    a = sinv(norm, p, r)
    u = [[-x*pow(H0, -1, p) % p for x in b], norm]
    g = smul(a, a, p, r)
    q = [1]+[0]*r
    for n in range(r):
        q[n+1] = conv(g, q, n, p)*pow(n+1, -1, p) % p
    return {'A': A, 'B': B, 'H': H, 'b': b, 'k': k, 'a': a, 'u': u, 'g': g, 'q': q}


def check_jets(J, p, r):
    A, B, H, b, k, a, g, q = (J[n] for n in ('A','B','H','b','k','a','g','q'))
    i3 = pow(3, -1, p)
    require(deriv(A, p) == [6*x % p for x in B[:r]], 'flow A failed')
    require(deriv(B, p) == [-4*i3*conv(A, A, n, p) % p for n in range(r)], 'flow B failed')
    require(deriv(H, p) == b[:r], 'H derivative failed')
    require(deriv(b, p) == [i3*conv(A, H, n, p) % p for n in range(r)], 'b derivative failed')
    require(deriv(k, p) == [(i3*A[n]-conv(k, k, n, p)) % p for n in range(r)], 'Riccati failed')
    u1, u2 = J['u']
    require(all((deriv(u1, p)[n]+i3*conv(A, u2, n, p)) % p == 0 for n in range(r)), 'u not horizontal, component 1')
    require(all((deriv(u2, p)[n]+u1[n]) % p == 0 for n in range(r)), 'u not horizontal, component 2')
    require(deriv(a, p) == smul(g, u1, p, r)[:r], 'Hodge normal form, component 1')
    require(a[:r] == smul(g, u2, p, r)[:r], 'Hodge normal form, component 2')
    require(deriv(q, p) == smul(g, q, p, r)[:r], 'q differential failed')
    require(q[0] == q[1] == 1, 'first-order q values changed')
    if r >= 2:
        require(q[2] == (pow(2, -1, p)-k[0]) % p, 'second-order q coefficient wrong')
    disc = [(4*x+27*y) % p for x,y in zip(smul(smul(A,A,p,r),A,p,r),smul(B,B,p,r))]
    require(all(x == 0 for x in disc[1:]), 'discriminant not constant along flow')


def substitute_terms(poly, A, B, p, r):
    one = [1]+[0]*r
    Ap, Bp = [one], [one]
    for _ in range(max((j for j,k in poly), default=0)):
        Ap.append(smul(Ap[-1], A, p, r))
    for _ in range(max((k for j,k in poly), default=0)):
        Bp.append(smul(Bp[-1], B, p, r))
    out = [0]*(r+1)
    for (j, k), c in poly.items():
        term = smul(Ap[j], Bp[k], p, r)
        out = [(x+c*y) % p for x,y in zip(out,term)]
    return out


def matrix_controls(t, proposed_slope, p):
    """Abstract matrices satisfying the supplied trace/determinant at p**2."""
    modulus = p*p
    tau = (t-p*pow(t, -1, modulus)) % modulus
    rho = p*pow(tau, -1, modulus) % modulus
    b = -proposed_slope*tau % modulus
    require((tau+rho-t) % modulus == 0, 'abstract matrix trace failed')
    require(tau*rho % modulus == p, 'abstract matrix determinant failed')
    require((tau*tau-t*tau+p) % modulus == 0, 'Hensel unit root failed')
    return [[rho, b], [0, tau]]


def eval_poly(f, x, p):
    out = 0
    for c in reversed(f):
        out = (out*x+c) % p
    return out


def reconstruct(f, t, kappa, mu, p):
    """O(1) reconstruction from trusted t,kappa and a supplied simple root."""
    require(len(f) == 4 and f[0] % p == 1 and f[3] % p != 0, 'bad normalized cubic')
    _, c, b, a = f
    H = t % p
    require(H != 0, 'ordinary reconstruction needs H nonzero')
    require(mu % p != 0 and eval_poly(f, mu, p) == 0, 'supplied mu must be a nonzero root')
    fp = (c+2*b*mu+3*a*mu*mu) % p
    require(fp != 0, 'supplied root must be simple')
    beta = H*kappa % p
    K = (beta-b*pow(3, -1, p)*H)*pow(a, -1, p) % p
    T = a*mu*(mu*H-K)*pow(fp, -1, p) % p
    return H, K, T
