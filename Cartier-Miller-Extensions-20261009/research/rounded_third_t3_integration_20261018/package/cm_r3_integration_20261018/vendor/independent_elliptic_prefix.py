"""Independent synthesis implementation of the quarter/third identities.

No imports from either research branch. Exact Python integer arithmetic.
Inputs p are assumed prime. Quadratic algebra avoids extracting sqrt(2).
Miller's logarithmic derivative uses a single pass, including intermediate O.
The default Cornacchia search is deterministic; its unconditional worst-case
scan length is NOT asserted polylogarithmic. Supply rng for Las Vegas sampling.
"""
from math import isqrt


class SplitRoot(Exception):
    def __init__(self, root):
        self.root = root


class Quadratic:
    def __init__(self, p, root=None):
        self.p, self.root = p, root

    def elt(self, a, b=0):
        return ((a+b*self.root) % self.p, 0) if self.root is not None else (a % self.p, b % self.p)

    def add(self, u, v):
        return ((u[0]+v[0]) % self.p, (u[1]+v[1]) % self.p)

    def neg(self, u):
        return (-u[0] % self.p, -u[1] % self.p)

    def sub(self, u, v):
        return self.add(u, self.neg(v))

    def mul(self, u, v):
        return ((u[0]*v[0]+2*u[1]*v[1]) % self.p,
                (u[0]*v[1]+u[1]*v[0]) % self.p)

    def div(self, u, v):
        norm = (v[0]*v[0]-2*v[1]*v[1]) % self.p
        if norm == 0:
            if v == (0,0):
                raise ZeroDivisionError('zero algebra element')
            raise SplitRoot(v[0]*pow(v[1],-1,self.p) % self.p)
        ni = pow(norm,-1,self.p)
        return self.mul(u,(v[0]*ni % self.p,-v[1]*ni % self.p))


class Elliptic:
    def __init__(self, field, a, b):
        self.k, self.a, self.b = field, field.elt(a), field.elt(b)
        self.calls = self.verticals = self.identities = 0

    def add(self, P, Q):
        """Return sum and constant coefficient of dlog(g_P,Q) at O."""
        self.calls += 1
        k = self.k
        if P is None or Q is None:
            self.identities += 1
            return (Q if P is None else P), k.elt(0)
        x,y = P; u,v = Q
        if x == u:
            if k.add(y,v) == k.elt(0):
                self.verticals += 1
                return None, k.elt(0)
            if y != v:
                # Over the split algebra, one component may be a tangent and
                # the other a vertical chord. Extract a root before branching.
                k.div(k.elt(1),k.sub(y,v))
                raise AssertionError('incompatible points at the same x')
            slope = k.div(k.add(k.mul(k.elt(3),k.mul(x,x)),self.a), k.mul(k.elt(2),y))
        else:
            slope = k.div(k.sub(v,y),k.sub(u,x))
        X = k.sub(k.sub(k.mul(slope,slope),x),u)
        Y = k.sub(k.mul(slope,k.sub(x,X)),y)
        return (X,Y), slope

    def on_curve(self,P):
        if P is None:return True
        x,y=P;k=self.k
        return k.mul(y,y)==k.add(k.add(k.mul(k.mul(x,x),x),k.mul(self.a,x)),self.b)


def miller_constant(E,P,M,normalize=True):
    """One binary pass; works for every annihilating M, not only exact order.

    Invariant div f_k = k(P)-(kP)-(k-1)(O). Identity chords have g=1.
    Vertical chords have g=x-x(P) and contribute zero to the constant.
    """
    assert M>0 and E.on_curve(P)
    k=E.k
    if normalize and M % k.p == 0:raise ValueError('M must be prime to p')
    Q,alpha=None,k.elt(0)
    for j in range(M.bit_length()-1,-1,-1):
        Q,slope=E.add(Q,Q)
        alpha=k.add(k.add(alpha,alpha),slope)
        if (M>>j)&1:
            Q,slope=E.add(Q,P)
            alpha=k.add(alpha,slope)
    assert Q is None,'M does not annihilate P'
    assert E.calls <= 2*M.bit_length()
    return k.div(alpha,k.elt(M)) if normalize else alpha


def legendre2(p):return 1 if p%8 in (1,7) else -1


def cornacchia_quarter(p,rng=None):
    assert p%4==1
    c,trials=2,0
    while True:
        if rng is not None:c=rng.randrange(1,p)
        trials+=1
        if pow(c,(p-1)//2,p)==p-1:break
        c+=1
    root=pow(c,(p-1)//4,p)
    u,v=p,root
    while v*v>p:u,v=v,u%v
    w=isqrt(p-v*v)
    assert v*v+w*w==p
    r,s=(v,w) if v%2 else (w,v)
    if r%4!=1:r=-r
    return r,s,trials


def cornacchia_third(p,rng=None):
    assert p%3==1
    c,trials=2,0
    while True:
        if rng is not None:c=rng.randrange(1,p)
        trials+=1
        z=pow(c,(p-1)//3,p)
        if z!=1:break
        c+=1
    root=(2*z+1)%p
    assert root*root%p==p-3
    u,v=p,root
    while v*v>p:u,v=v,u%v
    w=isqrt((p-v*v)//3)
    assert v*v+3*w*w==p
    for r,t in ((2*v,2*w),(v+3*w,v-w),(v-3*w,v+w)):
        if t%3==0:
            if r%3!=1:r=-r
            s=abs(t)//3
            assert r*r+27*s*s==4*p
            return r,s,trials
    raise AssertionError('Cornacchia transformation')


def _elliptic_e(p,kind,M):
    root=None
    restarts=0
    while True:
        k=Quadratic(p,root)
        s=k.elt(0,1)
        if kind=='quarter':
            E=Elliptic(k,2,0)
            P=(k.sub(k.elt(2),s),k.sub(k.elt(4),k.mul(k.elt(2),s)))
        else:
            E=Elliptic(k,0,pow(4,-1,p))
            P=(k.elt(-pow(2,-1,p)),k.mul(s,k.elt(pow(4,-1,p))))
        try:
            A=miller_constant(E,P,M)
            value=k.mul(s,k.sub(k.elt(1),A)) if kind=='quarter' else k.add(k.elt(1),k.mul(s,A))
            assert value[1]==0,'coefficient did not descend to F_p'
            return value[0],{'M':M,'bits_M':M.bit_length(),'curve_calls':E.calls,
                             'identity_calls':E.identities,'vertical_calls':E.verticals,
                             'split_restarts':restarts}
        except SplitRoot as err:
            assert root is None and err.root*err.root%p==2
            root=err.root;restarts+=1


def quarter(p,rng=None,trace=None):
    """Return B_n,a_n,U_p(n), n=(p-1)/4. p=1 mod4, p>=13.

    Optional exact trace replaces Cornacchia/Gauss and permits a Schoof front end.
    No Schoof implementation is included. With rng=None deterministic scan is used.
    """
    assert p>=13 and p%4==1
    n=(p-1)//4
    if trace is None:
        r,s,trials=cornacchia_quarter(p,rng)
        boundary=2*r*pow(pow(8,n,p),-1,p)%p
        trace=boundary if boundary%2==0 else boundary-p
    else:
        boundary=trace%p;r=s=None;trials=0
    assert trace%2==0 and trace*trace<=4*p
    chi=legendre2(p)
    M=p+1-trace if chi==1 else (p+1)**2-trace*trace
    e,info=_elliptic_e(p,'quarter',M)
    B=e*(chi-boundary)%p
    U=(4*B+9*pow(4,-1,p)*boundary)%p
    return {'p':p,'L':n,'B':B,'a':boundary,'U':U,'e':e,'trace':trace,
            'r':r,'s':s,'root_trials':trials,**info}


def third(p,rng=None):
    """p=1 mod3 gives B_L,a_L,U_L; p=2 mod3 gives only B_(p+1)/3.

    At exceptional ordinary primes the prime-to-p formula is rejected.
    """
    assert p>=5 and p%3!=0
    chi=legendre2(p)
    if p%3==1:
        r,s,trials=cornacchia_third(p,rng)
        trace=-r
        if trace==chi:raise ValueError('exceptional ordinary third-point prime')
        L=(p-1)//3;boundary=-r%p
    else:
        trace=0;L=(p+1)//3;boundary=None;r=s=None;trials=0
    M=p+1-chi*trace  # Frobenius(P)=chi P, so its characteristic polynomial kills P.
    e,info=_elliptic_e(p,'third',M)
    B=e*(chi-(boundary or 0))%p
    U=None if boundary is None else (4*B+26*pow(9,-1,p)*boundary)%p
    return {'p':p,'L':L,'B':B,'a':boundary,'U':U,'e':e,'trace':trace,
            'r':r,'s':s,'root_trials':trials,**info}


def weighted_quarter(p,coefficients,rng=None):
    """Coefficients in the falling-factorial basis; O(d) beyond quarter()."""
    z=quarter(p,rng);T=z['B'];falling=1;answer=0;half=pow(2,-1,p)
    for r,c in enumerate(coefficients):
        if r:
            falling=falling*(z['L']-r+1)%p
            T=((r-half)*T-2*falling*z['a'])%p
        answer=(answer+c*T)%p
    return answer


def accessible_digit_prefix(p,N,rng=None):
    """Return a_N,B_N for digits in {0..3,n-1,n,n+1,h..p-1}.

    A constant-size dictionary plus a range test; NO O(p) digit table.
    O(log_p(N+1)) field work after quarter(). Base conversion charged separately.
    """
    assert N>=0
    z=quarter(p,rng);n=z['L'];h=(p-1)//2;chi=legendre2(p)%p
    table={};a,B=1,0
    for r in range(4):
        table[r]=(a,B)
        B=(B+a)%p;a=a*(2*r+1)*pow(4*(r+1),-1,p)%p
    prev=z['a']*4*n*pow(2*n-1,-1,p)%p
    nxt=z['a']*(2*n+1)*pow(4*(n+1),-1,p)%p
    table[n-1]=(prev,(z['B']-prev)%p)
    table[n]=(z['a'],z['B'])
    table[n+1]=(nxt,(z['B']+z['a'])%p)
    ah=pow(-pow(2,-1,p),h,p)
    table[h]=(ah,(chi-ah)%p)
    digits=[]
    while N:N,d=divmod(N,p);digits.append(d)
    a,B=1,0
    for d in reversed(digits):
        if d>h:ad,Bd=0,chi
        elif d in table:ad,Bd=table[d]
        else:raise ValueError('digit outside the proved accessible set')
        B=(chi*B+a*Bd)%p;a=a*ad%p
    return a,B


if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser()
    parser.add_argument('family',choices=['quarter','third'])
    parser.add_argument('prime',type=int)
    args=parser.parse_args()
    print(json.dumps((quarter if args.family=='quarter' else third)(args.prime),indent=2))
