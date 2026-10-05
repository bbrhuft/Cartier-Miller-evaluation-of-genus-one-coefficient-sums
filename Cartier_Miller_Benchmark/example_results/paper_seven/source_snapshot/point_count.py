# SPDX-License-Identifier: GPL-2.0-or-later
"""Independent exact point counters for E: y^2=x^3+2x.

Schoof: division polynomials, Frobenius equation, CRT, and D5 splitting.
BSGS: intersect certified Hasse-interval annihilators on E and its twist.
Neither counter calls Cornacchia, Gauss, PARI, or the Miller evaluator.
Polynomial arithmetic is deliberately elementary, not an optimized Schoof.
"""
from math import isqrt
from functools import lru_cache


def add(P,Q,p,A=2):
    if P is None:return Q
    if Q is None:return P
    x,y=P;u,v=Q
    if x==u:
        if (y+v)%p==0:return None
        m=(3*x*x+A)*pow(2*y,-1,p)%p
    else:m=(v-y)*pow(u-x,-1,p)%p
    X=(m*m-x-u)%p
    return X,(m*(x-X)-y)%p


def mul(n,P,p,A=2):
    if n<0:return mul(-n,None if P is None else (P[0],-P[1]%p),p,A)
    R=None
    while n:
        if n&1:R=add(R,P,p,A)
        P=add(P,P,p,A);n>>=1
    return R


def sqrt_mod(a,p):
    a%=p
    if a==0:return 0
    if pow(a,(p-1)//2,p)!=1:return None
    if p%4==3:return pow(a,(p+1)//4,p)
    q=p-1;s=0
    while q%2==0:q//=2;s+=1
    z=2
    while pow(z,(p-1)//2,p)!=p-1:z+=1
    c=pow(z,q,p);x=pow(a,(q+1)//2,p);t=pow(a,q,p);m=s
    while t!=1:
        i=1;v=t*t%p
        while v!=1:v=v*v%p;i+=1
        b=pow(c,1<<(m-i-1),p);x=x*b%p;c=b*b%p;t=t*c%p;m=i
    return x


def interval_annihilators(P,p,A,lo,hi):
    """Return ALL n in [lo,hi] with nP=O, including low-order collisions."""
    width=hi-lo+1;m=isqrt(width)+1
    babies={};R=None
    for j in range(m):
        babies.setdefault(R,[]).append(j);R=add(R,P,p,A)
    step=mul(m,P,p,A);R=mul(-lo,P,p,A);answers=set()
    for i in range((width+m-1)//m):
        for j in babies.get(R,[]):
            n=lo+i*m+j
            if n<=hi:answers.add(n)
        R=add(R,None if step is None else (step[0],-step[1]%p),p,A)
    return answers


def bsgs_trace(p):
    """Exact on successful return; fail closed if candidate count is ambiguous.

    Every actual group order survives every intersection. A singleton therefore
    certifies the order, without assuming a sampled point generates the group.
    The search uses successive x-coordinates, not randomized probable orders.
    """
    H=isqrt(4*p);lo=p+1-H;hi=p+1+H
    z=2
    while pow(z,(p-1)//2,p)!=p-1:z+=1
    twist_A=2*z*z%p;candidates=None
    for x in range(min(p,10000)):
        for A,twist in ((2,False),(twist_A,True)):
            y=sqrt_mod((x*x*x+A*x)%p,p)
            if y is None or y==0:continue
            ns=interval_annihilators((x,y),p,A,lo,hi)
            if twist:ns={2*(p+1)-n for n in ns}
            candidates=ns if candidates is None else candidates&ns
            if not candidates:raise ArithmeticError('empty Hasse candidate set')
            if len(candidates)==1:return p+1-next(iter(candidates))
    raise ArithmeticError('BSGS could not certify a unique order; no CM fallback used')


class Split(Exception):
    def __init__(self,factor):self.factor=factor


class Polys:
    def __init__(self,p):self.p=p
    def trim(self,a):
        a=[x%self.p for x in a]
        while a and a[-1]==0:a.pop()
        return tuple(a)
    def add(self,a,b):return self.trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
    def neg(self,a):return self.trim([-x for x in a])
    def sub(self,a,b):return self.add(a,self.neg(b))
    def scale(self,a,k):return self.trim([x*k for x in a])
    def mul(self,a,b):
        if not a or not b:return ()
        out=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):out[i+j]+=x*y
        return self.trim(out)
    def divmod(self,a,b):
        if not b:raise ZeroDivisionError('zero polynomial')
        a=list(a);q=[0]*max(0,len(a)-len(b)+1);inv=pow(b[-1],-1,self.p)
        while len(a)>=len(b):
            d=len(a)-len(b);c=a[-1]*inv%self.p;q[d]=c
            for i,v in enumerate(b):a[d+i]=(a[d+i]-c*v)%self.p
            while a and a[-1]==0:a.pop()
        return self.trim(q),tuple(a)
    def rem(self,a,b):return self.divmod(a,b)[1]
    def pow(self,a,n,m=None):
        r=(1,)
        while n:
            if n&1:
                r=self.mul(r,a)
                if m:r=self.rem(r,m)
            n>>=1
            if n:
                a=self.mul(a,a)
                if m:a=self.rem(a,m)
        return r
    def inverse(self,a,m):
        r0,r1=m,a;s0,s1=(),(1,)
        while r1:
            q,r=self.divmod(r0,r1);r0,r1=r1,r;s0,s1=s1,self.sub(s0,self.mul(q,s1))
        if len(r0)>1:raise Split(self.scale(r0,pow(r0[-1],-1,self.p)))
        if not r0:raise ZeroDivisionError('zero in quotient')
        return self.rem(self.scale(s0,pow(r0[0],-1,self.p)),m)


def division_polynomial(p,l):
    R=Polys(p);F=(0,2,0,1);F2=R.mul(F,F)
    @lru_cache(None)
    def d(n):
        if n==0:return ()
        if n==1:return (1,)
        if n==2:return (2,)
        if n==3:return R.trim((-4,0,12,0,3))
        if n==4:return R.scale(R.trim((-8,0,-20,0,10,0,1)),4)
        m=n//2
        if n%2:
            a=R.mul(d(m+2),R.pow(d(m),3));b=R.mul(d(m-1),R.pow(d(m+1),3))
            if m%2==0:a=R.mul(a,F2)
            else:b=R.mul(b,F2)
            return R.sub(a,b)
        return R.scale(R.mul(d(m),R.sub(R.mul(d(m+2),R.pow(d(m-1),2)),R.mul(d(m-2),R.pow(d(m+1),2)))),pow(2,-1,p))
    f=d(l)
    return R.scale(f,pow(f[-1],-1,p))


def schoof_mod_l(p,l):
    R=Polys(p);F=(0,2,0,1)
    def solve(mod):
        def red(a):return R.rem(a,mod)
        def plus(a,b):return R.add(a,b)
        def minus(a,b):return R.sub(a,b)
        def times(a,b):return red(R.mul(a,b))
        def scale(a,k):return R.scale(a,k)
        def divide(a,b):return times(a,R.inverse(b,mod))
        ff=red(F);one=(1,);x=red((0,1));P=(x,one)
        def ap(U,V):
            if U is None:return V
            if V is None:return U
            x,b=U;u,c=V
            if x==u:
                if not plus(b,c):return None
                if b!=c:
                    # Opposite signs may occur in different components.
                    R.inverse(minus(b,c),mod)
                    raise ArithmeticError('inconsistent torsion coordinates')
                s=divide(plus(scale(times(x,x),3),(2,)),scale(times(ff,b),2))
            else:s=divide(minus(c,b),minus(u,x))
            X=minus(minus(times(ff,times(s,s)),x),u)
            return X,minus(times(s,minus(x,X)),b)
        def mp(n,U):
            Q=None
            while n:
                if n&1:Q=ap(Q,U)
                n>>=1
                if n:U=ap(U,U)
            return Q
        def frob(U):
            if U is None:return None
            x,b=U
            return R.pow(x,p,mod),times(R.pow(b,p,mod),R.pow(ff,(p-1)//2,mod))
        pi=frob(P);left=ap(frob(pi),mp(p%l,P));right=None
        for t in range(l):
            if left==right:return {t}
            right=ap(right,pi)
        raise ArithmeticError('no trace residue satisfies Frobenius')
    def recurse(mod):
        try:return solve(mod)
        except Split as e:
            q,rem=R.divmod(mod,e.factor)
            if rem or len(e.factor)<=1 or len(q)<=1:raise ArithmeticError('invalid D5 split')
            answer=recurse(e.factor)&recurse(q)
            if not answer:raise ArithmeticError('inconsistent component residues')
            return answer
    out=recurse(division_polynomial(p,l))
    if len(out)!=1:raise ArithmeticError('nonunique trace residue')
    return out.pop()


def schoof_trace(p):
    """Deterministic Schoof, specialized ONLY in knowing rational (0,0) 2-torsion.

    All odd-prime residues use the Frobenius characteristic equation on E[l].
    Product of CRT moduli exceeds the entire integer Hasse interval width.
    """
    H=isqrt(4*p);t=0;modulus=2;l=3
    while modulus<=2*H:
        if l!=p and all(l%d for d in range(2,isqrt(l)+1)):
            residue=schoof_mod_l(p,l)
            t+=modulus*((residue-t)*pow(modulus,-1,l)%l);modulus*=l
        l+=2
    if t>H:t-=modulus
    if abs(t)>H:raise ArithmeticError('CRT trace outside Hasse interval')
    return t


def direct_trace(p):
    return -sum(0 if (f:=(x*x*x+2*x)%p)==0 else (1 if pow(f,(p-1)//2,p)==1 else -1) for x in range(p))
