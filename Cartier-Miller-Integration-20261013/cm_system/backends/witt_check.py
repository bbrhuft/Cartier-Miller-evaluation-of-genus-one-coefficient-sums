"""Independent local-series check of the first missing Witt coordinate.

Intentionally a small-prime reference: quadratic-time series multiplication.
It does NOT constitute a fast algorithm for the incomplete sum.
"""
from .padic_lift import Ring,Curve,lifted_quarter,reference


class Series:
    def __init__(self,k,N):self.k=k;self.N=N;self.zero=k.e(0)
    def one(self):return [self.k.e(1)]+[self.zero]*self.N
    def add(self,a,b):return [self.k.add(x,y) for x,y in zip(a,b)]
    def neg(self,a):return [self.k.neg(x) for x in a]
    def scale(self,a,c):return [self.k.mul(x,c) for x in a]
    def shift(self,a,n):return [self.zero]*n+a[:self.N+1-n]
    def mul(self,a,b):
        k=self.k;c=[self.zero]*(self.N+1)
        for i,x in enumerate(a):
            if x==self.zero:continue
            for j,y in enumerate(b[:self.N+1-i]):
                if y!=self.zero:c[i+j]=k.add(c[i+j],k.mul(x,y))
        return c
    def inv(self,a):
        k=self.k;c=[k.div(k.e(1),a[0])]+[self.zero]*self.N
        for n in range(1,self.N+1):
            s=self.zero
            for j in range(1,n+1):s=k.add(s,k.mul(a[j],c[n-j]))
            c[n]=k.neg(k.div(s,a[0]))
        return c
    def div(self,a,b):return self.mul(a,self.inv(b))


def normalized_miller_series(E,P,M,S,base):
    """At quartic P_-: x=4*base/w^2, y=8*base/w^3.

    base=(1+sqrt(1-w^4/2))/2. Drop Laurent monomials and scalar
    factors at each step; after taking a ratio the result has constant 1.
    """
    k=E.k;one=S.one();Q=E.O;f=one
    def vertical(x):
        z=base[:];z[2]=k.sub(z[2],k.div(x,k.e(4)));return z
    def step(P,Q):
        R,mu=E.add(P,Q)
        if P==E.O or Q==E.O:return R,one
        if R==E.O:return R,vertical(P[1])
        # (w^3/8)*(y-mu*x+mu*x(P)-y(P)).
        line=S.add(base,S.scale(S.shift(base,1),k.neg(k.div(mu,k.e(2)))))
        line[3]=k.add(line[3],k.div(k.sub(k.mul(mu,P[1]),P[2]),k.e(8)))
        return R,S.div(line,vertical(R[1]))
    for bit in bin(M)[2:]:
        Q,g=step(Q,Q);f=S.mul(S.mul(f,f),g)
        if bit=='1':Q,g=step(Q,P);f=S.mul(f,g)
    assert Q==E.O
    return f


def witt_coordinate(p):
    z=lifted_quarter(p);k=Ring(p);k.q=p
    if k.root is not None:k.root%=p
    E=Curve(k);S=Series(k,p)
    sigma=k.e(0,1)
    Rplus=('A',k.sub(k.e(2),sigma),k.sub(k.e(4),k.scale(2,sigma)))
    Rminus=('A',k.add(k.e(2),sigma),k.add(k.e(4),k.scale(2,sigma)))
    base=S.one();c=1
    for j in range(1,p//4+1):
        c=c*(2*j-3)*pow(4*j,-1,p)%p
        base[4*j]=k.e(c*pow(2,-1,p))
    fp=normalized_miller_series(E,Rplus,z['M'],S,base)
    fm=normalized_miller_series(E,Rminus,z['M'],S,base)
    F=S.div(fp,fm)
    g0=k.neg(F[1])  # c_1=-F'(0), since F(0)=1.
    expected=k.neg(k.scale(z['M']*z['e'],(z['v'][0]%p,z['v'][1]%p)))
    assert g0==expected,(p,g0,expected)
    residual=F[:]
    for j in range(1,p):
        cj=k.neg(residual[j])
        for i in range(j,p+1):residual[i]=k.add(residual[i],k.mul(cj,residual[i-j]))
        assert residual[j]==k.e(0)
    cp=k.neg(residual[p])
    c_scaled=k.div(cp,k.scale(z['M'],(z['v'][0]%p,z['v'][1]%p)))
    assert c_scaled[1]==0
    q=p*p;d=(z['w'][0]-1)//p
    assert z['w'][1]==0
    vM=z['M'] # evaluate (v*M)^(p-1) in the p^2 ring
    kk=Ring(p);base2=kk.scale(vM,z['v']);power=kk.e(1)
    for bit in bin(p-1)[2:]:
        power=kk.mul(power,power)
        if bit=='1':power=kk.mul(power,base2)
    assert power[1]==0
    ref=reference(p,z['L'])
    b=z['e']*(z['chi']-z['boundary'])%p
    predicted=(power[0]*pow(z['e'],p,q)-z['e']*z['boundary']
               -p*(2*d*(b+z['boundary'])+c_scaled[0]))%q
    assert predicted==ref['B'],(p,predicted,ref)
    return dict(p=p,M=z['M'],c_p=cp,c_scaled=c_scaled[0],pole_shift=d,
                B=ref['B'],predicted_B=predicted)


if __name__=='__main__':
    import json,sys
    print(json.dumps(witt_coordinate(int(sys.argv[1])),indent=2))
