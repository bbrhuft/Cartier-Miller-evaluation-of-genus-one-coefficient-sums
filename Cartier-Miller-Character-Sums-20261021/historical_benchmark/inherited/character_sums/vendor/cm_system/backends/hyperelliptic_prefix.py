"""Exact Cantor--Miller local jets for y^2=1-x^d/2, d odd dividing p+1.

Only the Python standard library is used. p is assumed prime.
The returned prefixes B_{j(p+1)/d}, 1<=j<=g, are conditional on the
mathematical theorem in HIGHER_GENUS_REPORT.md, independently tested below.
No factorial/boundary or original U value is hidden in the output.
"""
from __future__ import annotations
from dataclasses import dataclass


class SplitRoot(Exception):
    def __init__(self, root): self.root = root


class Field:
    """Quadratic algebra; a nonzero zero divisor triggers one field restart."""
    def __init__(self, p, root=None):
        self.p, self.root = p, root
        self.zero, self.one = (0, 0), (1, 0)
        self.inversions = 0

    def e(self, a, b=0):
        return ((a+b*self.root) % self.p, 0) if self.root is not None else (a % self.p, b % self.p)
    def add(self, a, b): return ((a[0]+b[0]) % self.p, (a[1]+b[1]) % self.p)
    def neg(self, a): return (-a[0] % self.p, -a[1] % self.p)
    def sub(self, a, b): return self.add(a, self.neg(b))
    def mul(self, a, b):
        return ((a[0]*b[0]+2*a[1]*b[1]) % self.p, (a[0]*b[1]+a[1]*b[0]) % self.p)
    def scale(self, a, n): return (a[0]*n % self.p, a[1]*n % self.p)
    def inv(self, a):
        self.inversions += 1
        norm = (a[0]*a[0]-2*a[1]*a[1]) % self.p
        if not norm:
            if a == self.zero: raise ZeroDivisionError('zero field element')
            raise SplitRoot(a[0]*pow(a[1], -1, self.p) % self.p)
        t = pow(norm, -1, self.p)
        return (a[0]*t % self.p, -a[1]*t % self.p)
    def div(self, a, b): return self.mul(a, self.inv(b))


class Polynomials:
    def __init__(self, k): self.k = k
    def trim(self, a):
        a=list(a)
        while a and a[-1]==self.k.zero: a.pop()
        return a
    def add(self, a, b):
        k=self.k; z=k.zero
        return self.trim([k.add(a[i] if i<len(a) else z,b[i] if i<len(b) else z) for i in range(max(len(a),len(b)))])
    def neg(self, a): return [self.k.neg(t) for t in a]
    def sub(self, a, b): return self.add(a,self.neg(b))
    def scale(self, a, t): return self.trim([self.k.mul(t,v) for v in a])
    def mul(self, a, b):
        if not a or not b:return []
        k=self.k;c=[k.zero]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            if x==k.zero:continue
            for j,y in enumerate(b):
                if y!=k.zero:c[i+j]=k.add(c[i+j],k.mul(x,y))
        return self.trim(c)
    def divmod(self, a, b):
        a=self.trim(a);b=self.trim(b);k=self.k
        if not b:raise ZeroDivisionError('zero polynomial')
        if len(a)<len(b):return [],a
        q=[k.zero]*(len(a)-len(b)+1);inv=k.inv(b[-1])
        while a and len(a)>=len(b):
            j=len(a)-len(b);t=k.mul(a[-1],inv);q[j]=t
            for i,v in enumerate(b):a[i+j]=k.sub(a[i+j],k.mul(t,v))
            a=self.trim(a)
        return self.trim(q),a
    def exact(self,a,b):
        q,r=self.divmod(a,b)
        assert not r, 'nonexact division in Cantor arithmetic'
        return q
    def mod(self,a,b):return self.divmod(a,b)[1]
    def monic(self,a):
        if not a: return []
        return self.scale(a,self.k.inv(a[-1]))
    def xgcd(self,a,b):
        k=self.k;r0,r1=list(a),list(b);s0,s1=[k.one],[];t0,t1=[],[k.one]
        while r1:
            q,r=self.divmod(r0,r1)
            r0,r1=r1,r;s0,s1=s1,self.sub(s0,self.mul(q,s1));t0,t1=t1,self.sub(t0,self.mul(q,t1))
        if not r0:return [],[],[]
        inv=k.inv(r0[-1]);return self.scale(r0,inv),self.scale(s0,inv),self.scale(t0,inv)


class Jacobian:
    def __init__(self,k,d,jets=1):
        assert d>=3 and d%2 and d%k.p
        self.k,self.d,self.g,self.jets=k,d,(d-1)//2,jets
        self.pol=Polynomials(k)
        self.f=[k.one]+[k.zero]*(d-1)+[k.e(-pow(2,-1,k.p))]
        self.identity=([k.one],[])
        self.calls=self.reductions=self.nonunit_local_factors=0
        # Norm(y-v)=f-v^2 has degree at most max(d,4g-2).
        # This precision includes the valuation and every required unit jet.
        self.prec=max(d,4*self.g-2)+jets+2
        self.y=[k.one]+[k.zero]*(self.prec-1)
        inv2=pow(2,-1,k.p)
        for n in range(1,self.prec):
            t=self.f[n] if n<len(self.f) else k.zero
            for i in range(1,n):t=k.sub(t,k.mul(self.y[i],self.y[n-i]))
            self.y[n]=k.scale(t,inv2)

    def valid(self,D):
        u,v=D;P=self.pol
        return bool(u) and u[-1]==self.k.one and len(v)<len(u) and len(u)-1<=self.g and not P.mod(P.sub(self.f,P.mul(v,v)),u)

    def log_jet(self,coeffs):
        """Regular coefficients of dlog at P0=(0,1), plus integer valuation.

        If z=x^v(c0+c1*x+...), dlog(z)=v/x+unit'/unit.
        Keeping v separately makes intermediate zeros and poles harmless.
        """
        k=self.k;q=self.jets
        val=next((i for i,c in enumerate(coeffs) if c!=k.zero),None)
        assert val is not None, 'insufficient local precision'
        if val:self.nonunit_local_factors+=1
        c=[coeffs[val+i] if val+i<len(coeffs) else k.zero for i in range(q+1)]
        inv0=k.inv(c[0]);z=[k.zero]*q
        for n in range(q):
            t=k.scale(c[n+1],n+1)
            for j in range(1,n+1):t=k.sub(t,k.mul(c[j],z[n-j]))
            z[n]=k.mul(t,inv0)
        return z,val

    def add(self,D1,D2):
        self.calls+=1;k=self.k;P=self.pol;q=self.jets
        if D1==self.identity:return D2,[k.zero]*q,0
        if D2==self.identity:return D1,[k.zero]*q,0
        u1,v1=D1;u2,v2=D2
        d1,e1,e2=P.xgcd(u1,u2)
        common,c1,c2=P.xgcd(d1,P.add(v1,v2))
        s1,s2,s3=P.mul(c1,e1),P.mul(c1,e2),c2
        u=P.exact(P.mul(u1,u2),P.mul(common,common))
        numerator=P.add(P.add(P.mul(P.mul(s1,u1),v2),P.mul(P.mul(s2,u2),v1)),P.mul(s3,P.add(P.mul(v1,v2),self.f)))
        v=P.mod(P.exact(numerator,common),u)
        ell,order=self.log_jet(common)
        while len(u)-1>self.g:
            self.reductions+=1
            new_u=P.monic(P.exact(P.sub(self.f,P.mul(v,v)),u))
            numer=list(self.y)
            for i,c in enumerate(v):numer[i]=k.sub(numer[i],c)
            a,va=self.log_jet(numer);b,vb=self.log_jet(new_u)
            ell=[k.add(z,k.sub(x,y)) for z,x,y in zip(ell,a,b)];order+=va-vb
            u,v=new_u,P.mod(P.neg(v),new_u)
        result=(u,v)
        assert self.valid(result)
        return result,ell,order

    def miller(self,D,M):
        assert self.valid(D) and M>0 and M%self.k.p
        k=self.k;R=self.identity;ell=[k.zero]*self.jets;order=0
        for bit in bin(M)[2:]:
            R,z,v=self.add(R,R)
            ell=[k.add(k.scale(a,2),b) for a,b in zip(ell,z)];order=2*order+v
            if bit=='1':
                R,z,v=self.add(R,D)
                ell=[k.add(a,b) for a,b in zip(ell,z)];order+=v
        assert R==self.identity, 'claimed integer does not annihilate the divisor'
        assert order==0, 'final Miller function unexpectedly meets P0'
        return [k.scale(t,pow(M,-1,k.p)) for t in ell]


def prefixes(p,d,all_prefixes=True):
    """Return B_{j(p+1)/d} for j=1..g (or just j=1), prime p assumed."""
    assert p>2 and d>=3 and d%2==1 and p%d==d-1
    g=(d-1)//2;q=g if all_prefixes else 1
    root=None;restarts=0;prior_calls=prior_inversions=prior_reductions=0
    while True:
        k=Field(p,root);J=Jacobian(k,d,q)
        s=k.e(0,1);Q=([k.e(-1),k.one],[k.scale(s,pow(2,-1,p))])
        try:
            A=J.miller(Q,p+1)
            # F=f_{M,Q}^2/(x-1)^M.  For degree <g, y(x)=1 mod x^g.
            # eta/omega=-sqrt(2)*(2*A+1/(1-x)).
            chi=1 if p%8 in (1,7) else -1
            vals=[]
            for a in A:
                e=k.neg(k.mul(s,k.add(k.scale(a,2),k.one)))
                b=k.scale(e,chi)
                assert b[1]==0,'prefix does not descend to F_p'
                vals.append(b[0])
            return {'p':p,'d':d,'g':g,'L':(p+1)//d,'indices':[(j+1)*(p+1)//d for j in range(q)],'B':vals,
                    'M':p+1,'M_bits':(p+1).bit_length(),'calls':prior_calls+J.calls,
                    'reductions':prior_reductions+J.reductions,'field_inversions':prior_inversions+k.inversions,
                    'nonunit_local_factors':J.nonunit_local_factors,'split_restarts':restarts}
        except SplitRoot as exc:
            assert root is None and exc.root*exc.root%p==2
            root=exc.root;restarts+=1
            prior_calls+=J.calls;prior_inversions+=k.inversions;prior_reductions+=J.reductions


def direct(p,indices):
    """Independent scaled original-binomial recurrence; single final inverse."""
    wanted=set(indices);A,E,D=1,0,1;out={}
    for n in range(max(wanted)+1):
        if n in wanted:out[n]=E*pow(D,-1,p)%p
        factor=4*(n+1)%p
        A,E,D=A*(2*n+1)%p,(E+A)*factor%p,D*factor%p
    return [out[n] for n in indices]


if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser();parser.add_argument('p',type=int);parser.add_argument('d',type=int);parser.add_argument('--first-only',action='store_true')
    args=parser.parse_args();print(json.dumps(prefixes(args.p,args.d,not args.first_only),indent=2))
