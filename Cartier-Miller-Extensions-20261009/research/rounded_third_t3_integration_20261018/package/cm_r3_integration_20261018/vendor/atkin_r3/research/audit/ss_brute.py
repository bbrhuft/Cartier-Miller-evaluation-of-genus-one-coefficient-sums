"""Independent check (no atkin.py): supersingular j's from the Legendre Hasse
polynomial over F_{p^2}, compared with A_n mod p, D=A_n'(0), c_p=2(m!)^-3."""
import sys
from math import comb
def isprime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
def run(p):
    nu=next(x for x in range(2,p) if pow(x,(p-1)//2,p)==p-1)
    def mul(a,b): return ((a[0]*b[0]+nu*a[1]*b[1])%p,(a[0]*b[1]+a[1]*b[0])%p)
    def inv(a):
        n=(a[0]*a[0]-nu*a[1]*a[1])%p; ni=pow(n,p-2,p); return (a[0]*ni%p,(-a[1])*ni%p)
    h=(p-1)//2; coeffs=[comb(h,i)**2%p for i in range(h+1)]
    roots=[]
    for x in range(p):
        for y in range(p):
            lam=(x,y); acc=(0,0)
            for c in reversed(coeffs): acc=mul(acc,lam); acc=((acc[0]+c)%p,acc[1])
            if acc==(0,0): roots.append(lam)
    js=set()
    for lam in roots:
        l2=mul(lam,lam); num=((l2[0]-lam[0]+1)%p,(l2[1]-lam[1])%p); num=mul(mul(num,num),num); num=(256*num[0]%p,256*num[1]%p)
        lm1=((lam[0]-1)%p,lam[1]); den=mul(l2,mul(lm1,lm1)); js.add(mul(num,inv(den)))
    js=sorted(js)
    # ss(J) = prod (J - j) over F_{p^2}; coefficients must lie in F_p
    poly=[(1,0)]
    for jj in js:
        new=[(0,0)]*(len(poly)+1)
        for i,c in enumerate(poly):
            new[i+1]=((new[i+1][0]+c[0])%p,(new[i+1][1]+c[1])%p)
            t=mul(c,((-jj[0])%p,(-jj[1])%p)); new[i]=((new[i][0]+t[0])%p,(new[i][1]+t[1])%p)
        poly=new
    assert all(c[1]==0 for c in poly)
    ss=[c[0] for c in poly]
    # Atkin A_n mod p by the recurrence (own implementation)
    N=(p-5)//12; eps=int(p%12==11); n=N+1+eps
    A=[[1],[(-720)%p,1],[269280%p,(-1640)%p,1]]
    for k in range(2,n):
        inv_=lambda v: pow(v%p,p-2,p)
        al=24*(144*k*k-29)*inv_((2*k+1)*(2*k-1))%p
        be=36*(12*k-13)*(12*k-7)*(12*k-5)*(12*k+1)*inv_(k*(k-1)*(2*k-1)**2)%p
        a,b=A[-1],A[-2]; new=[0]*(len(a)+1)
        for i,c in enumerate(a): new[i+1]+=c; new[i]-=al*c
        for i,c in enumerate(b): new[i]-=be*c
        A.append([c%p for c in new])
    An=A[n]
    D=ss[1]
    m=(p-2)//3; mf=1
    for t in range(1,m+1): mf=mf*t%p
    c=2*pow(mf,3*(p-2),p)%p
    chi=1 if pow(6,(p-1)//2,p)==1 else p-1
    # signed normalization c = -4 chi (-1)^N D / (3 1728^N (-1728)^eps)
    rhs=-4*chi*pow(-1,N)*D*pow(3*pow(1728,N,p)*pow(-1728,eps,p)%p,p-2,p)%p
    # product of ss j other than 0,1728
    P=(1,0)
    for jj in js:
        if jj not in ((0,0),(1728%p,0)): P=mul(P,jj)
    assert P[1]==0
    nodal=-3*pow(4,p-2,p)*chi*pow(1728,N,p)*c%p
    # Wronskian endpoint product (own implementation)
    W=273*pow(2,p-2,p)%p
    for jj in range(1,n-1): W=W*(-6)*(12*jj+7)*(12*jj+13)*pow((jj+1)*(2*jj+1),p-2,p)%p
    return dict(p=p,deg=len(js),n=n,atkin_eq_ss=(An==ss),D=D,W=W,c=c,rhs=rhs,P=P[0],nodal=nodal,
                ok=(An==ss and len(js)==n and rhs==c and P[0]==nodal and W==D))
ps=[p for p in range(11,int(sys.argv[1])) if p%6==5 and isprime(p)]
res=[run(p) for p in ps]
print(all(r['ok'] for r in res), len(res), [ (r['p'],r['D'],r['c']) for r in res[:6]])
