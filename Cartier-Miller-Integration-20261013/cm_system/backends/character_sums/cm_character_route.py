"""Trace-supplied, nonbranch character sums; corrected audit route, 21 Oct 2026.

All polynomial arrays have increasing degree. Requires a prime p>=5, a
squarefree cubic/quartic, and the exact signed projective trace. No trace
acquisition or primality certification is hidden here. Endpoint checks are
necessary consistency checks, not certificates of a supplied trace.

Standard library only. See PROOFS.md for normalization and every chain case.
This is a separate implementation; the frozen benchmark is not modified.
"""
from math import comb, gcd, isqrt


def peval(f, x, p):
    z = 0
    for c in reversed(f):
        z = (z*x+c) % p
    return z


def _trim(f):
    while len(f)>1 and f[-1]==0:
        f.pop()
    return f


def _rem(f, g, p):
    f = list(f)
    inv = pow(g[-1], -1, p)
    while len(f)>=len(g) and any(f):
        k, c = len(f)-len(g), f[-1]*inv % p
        for j, v in enumerate(g):
            f[k+j] = (f[k+j]-c*v) % p
        _trim(f)
    return f


def squarefree(f, p):
    a, b = list(f), _trim([i*f[i] % p for i in range(1,len(f))])
    while any(b):
        a, b = b, _rem(a,b,p)
    return len(a)==1


def character(v, p):
    v %= p
    if not v:
        return 0
    z = pow(v, (p-1)//2, p)
    if z not in (1,p-1):
        raise ValueError('prime-field character assumption failed')
    return 1 if z==1 else -1


def normalize_at(f, a, p):
    inv = pow(peval(f,a,p),-1,p)
    return [sum(f[j]*comb(j,k)*pow(a,j-k,p) for j in range(k,len(f)))*inv % p
            for k in range(len(f))]


def ec_add(P, Q, A, p):
    """Return sum, and local dlog constant of the Miller line ratio."""
    if P is None:
        return Q, 0
    if Q is None:
        return P, 0
    x,y = P; u,v = Q
    if x==u and (y+v)%p==0:
        return None, 0
    slope = ((3*x*x+A)*pow(2*y,-1,p) if x==u
             else (v-y)*pow(u-x,-1,p)) % p
    w = (slope*slope-x-u)%p
    return (w,(slope*(x-w)-y)%p),slope


def ec_mul(P, m, A, p):
    Q = None
    while m:
        if m&1:
            Q = ec_add(Q,P,A,p)[0]
        P = ec_add(P,P,A,p)[0]
        m >>= 1
    return Q


def miller_constant(P, m, A, p, stats=None):
    """Constant of dlog f_{m,P} at O in t=-X/Y, including identity steps."""
    if m<1:
        raise ValueError('positive Miller scalar required')
    Q, alpha, touched = P, 0, P is None
    for bit in bin(m)[3:]:
        Q, slope = ec_add(Q,Q,A,p)
        alpha = (2*alpha+slope)%p
        touched |= Q is None
        if bit=='1':
            Q, slope = ec_add(Q,P,A,p)
            alpha = (alpha+slope)%p
            touched |= Q is None
    if stats is not None:
        stats['chain_through_identity'] = touched
    return alpha, Q


def short_model(g, p):
    """Connell model, P+=(0,1) as O; return A,B,image of P-."""
    g = list(g)+[0]*(5-len(g))
    f1,f2,f3,f4 = g[1:5]
    i = lambda n: pow(n,-1,p)
    a1,a2,a3,a4 = f1,(f2-f1*f1*i(4))%p,2*f3%p,-4*f4%p
    a6 = a2*a4%p
    b2,b4,b6 = (a1*a1+4*a2)%p,(2*a4+a1*a3)%p,(a3*a3+4*a6)%p
    A = (b4*i(2)-b2*b2*i(48))%p
    B = (b6*i(4)-b2*b4*i(24)+b2**3*i(864))%p
    s1 = f1*i(2)%p
    s2 = (f2-s1*s1)*i(2)%p
    s3 = (f3-2*s1*s2)*i(2)%p
    x,y = -2*s2%p,-4*s3%p
    R = ((x+b2*i(12))%p,(y+(a1*x+a3)*i(2))%p)
    return A,B,R


def direct(p,f,a):
    return sum(character(peval(f,x,p),p)*pow((x-a)%p,-1,p)
               for x in range(p) if x!=a)%p


def value(p, f, a, trace, stats=None):
    """C_f(a) mod p; admissible nonbranch inputs, exact trace supplied.

    p=5 uses bounded enumeration. For p>=7, the general route applies iff
    trace of the normalized twist is not 1. The two-torsion case is explicit.
    """
    if not isinstance(p,int) or p<5 or p%2==0:
        raise ValueError('requires an odd prime p>=5')
    if not isinstance(trace,int) or abs(trace)>isqrt(4*p):
        raise ValueError('signed integer trace outside the Hasse interval')
    f = _trim([int(c)%p for c in f])
    if len(f) not in (4,5) or not squarefree(f,p):
        raise ValueError('requires a squarefree cubic or quartic')
    a %= p
    e = character(peval(f,a,p),p)
    if not e:
        raise ValueError('branch pole: outside this evaluator contract')
    if p==5:
        if stats is not None:
            stats['route'] = 'small_field'
        return direct(p,f,a)
    g = normalize_at(f,a,p)
    tau = e*trace
    n = p+1-tau
    A,B,R = short_model(g,p)
    if (R[1]**2-R[0]**3-A*R[0]-B)%p:
        raise ArithmeticError('invalid adapted point')
    i2,i4 = pow(2,-1,p),pow(4,-1,p)
    if R[1]==0:
        if n%2:
            raise ArithmeticError('two-torsion contradicts supplied curve order')
        if stats is not None:
            stats['route'] = 'two_torsion'
        return -e*g[1]*i4*(n-2)%p
    if tau==1:
        alpha,end = miller_constant(R,p,A,p,stats)
        if end is not None:
            raise ArithmeticError('anomalous endpoint contradicts supplied trace')
        if stats is not None:
            stats['route'] = 'exceptional'
        return e*(g[1]*i2-alpha*i2)%p
    if gcd(p,n)!=1:
        raise ArithmeticError('p must be invertible modulo the supplied order')
    Q = ec_mul(R,pow(p,-1,n),A,p)
    alpha,end = miller_constant(Q,p,A,p,stats)
    if end!=R:
        raise ArithmeticError('general endpoint contradicts supplied trace')
    if stats is not None:
        stats['route'] = 'general'
    return e*(-(tau-1)*alpha*i2-g[1]*i4*(n-2))%p
