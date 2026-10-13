"""Exact arithmetic modulo p^2; no floating point or optional dependencies.

The caller supplies an odd prime. Only the quarter family p=1 mod4,p>=13
is claimed. Points are ('A',x,y) or ('F',t), with t in pR and t^2=0.
Every division checks that its denominator is a unit modulo p.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'inputs'))
from .elliptic import cornacchia_quarter, legendre2


def sqrt_mod(a,p):
    """Tonelli--Shanks, deterministic nonresidue scan (cost not hidden)."""
    assert pow(a,(p-1)//2,p)==1
    q,s=p-1,0
    while q%2==0:q//=2;s+=1
    if s==1:return pow(a,(p+1)//4,p)
    z=2
    while pow(z,(p-1)//2,p)!=p-1:z+=1
    c,x,t,m=pow(z,q,p),pow(a,(q+1)//2,p),pow(a,q,p),s
    while t!=1:
        i,b=0,t
        while b!=1:b=b*b%p;i+=1
        assert i<m
        b=pow(c,1<<(m-i-1),p)
        x=x*b%p;t=t*b*b%p;c=b*b%p;m=i
    return x


class Ring:
    def __init__(self,p,root_sign=1):
        self.p,self.q=p,p*p
        self.chi=legendre2(p)
        self.root=None
        if self.chi==1:
            r=sqrt_mod(2,p)
            self.root=root_sign*(r-(r*r-2)*pow(2*r,-1,self.q))%self.q
    def e(self,a,b=0):
        if self.root is not None:return ((a+b*self.root)%self.q,0)
        return (a%self.q,b%self.q)
    def add(self,u,v):return ((u[0]+v[0])%self.q,(u[1]+v[1])%self.q)
    def neg(self,u):return (-u[0]%self.q,-u[1]%self.q)
    def sub(self,u,v):return self.add(u,self.neg(v))
    def mul(self,u,v):
        return ((u[0]*v[0]+2*u[1]*v[1])%self.q,(u[0]*v[1]+u[1]*v[0])%self.q)
    def unit(self,u):return (u[0]*u[0]-2*u[1]*u[1])%self.p!=0
    def div(self,u,v):
        assert self.unit(v),('nonunit denominator',self.p,v)
        ni=pow(v[0]*v[0]-2*v[1]*v[1],-1,self.q)
        return self.mul(u,(v[0]*ni%self.q,-v[1]*ni%self.q))
    def scale(self,n,u):return self.mul(self.e(n),u)


class Curve:
    def __init__(self,k):self.k=k;self.calls=0;self.O=('F',k.e(0))
    def neg(self,P):
        return ('F',self.k.neg(P[1])) if P[0]=='F' else ('A',P[1],self.k.neg(P[2]))
    def on_curve(self,P):
        k=self.k
        if P[0]=='F':return P[1][0]%k.p==0 and P[1][1]%k.p==0
        _,x,y=P
        return k.mul(y,y)==k.add(k.mul(k.mul(x,x),x),k.scale(2,x))
    def add(self,P,Q):
        """Complete two-chart addition at precision p^2; returns slope when affine."""
        self.calls+=1;k=self.k;zero=k.e(0)
        if P[0]=='F' and Q[0]=='F':return ('F',k.add(P[1],Q[1])),zero
        if P[0]=='F':P,Q=Q,P
        if Q[0]=='F':
            _,x,y=P;t=Q[1]
            return ('A',k.add(x,k.mul(k.scale(2,y),t)),
                    k.add(y,k.mul(k.add(k.scale(3,k.mul(x,x)),k.e(2)),t))),zero
        _,x,y=P;_,u,v=Q
        dx,dy,sy=k.sub(u,x),k.sub(v,y),k.add(v,y)
        N=k.add(k.add(k.add(k.mul(x,x),k.mul(x,u)),k.mul(u,u)),k.e(2))
        if k.unit(dx):mu=k.div(dy,dx)
        elif k.unit(sy):mu=k.div(N,sy)
        else:
            w=k.div(dx,dy) if k.unit(dy) else k.div(sy,N)
            assert w[0]%k.p==w[1]%k.p==0
            return ('F',w),zero
        X=k.sub(k.sub(k.mul(mu,mu),x),u)
        Y=k.sub(k.mul(mu,k.sub(x,X)),y)
        return ('A',X,Y),mu
    def mul(self,n,P):
        if n<0:return self.mul(-n,self.neg(P))
        Q=self.O
        for bit in bin(n)[2:]:
            Q,_=self.add(Q,Q)
            if bit=='1':Q,_=self.add(Q,P)
        return Q
    def miller(self,P,M):
        k=self.k;Q=self.O;c=k.e(0)
        assert M%k.p and self.mul(M,P)==self.O
        for bit in bin(M)[2:]:
            Q,slope=self.add(Q,Q);c=k.add(k.scale(2,c),slope)
            if Q[0]=='F':assert Q==self.O
            if bit=='1':
                Q,slope=self.add(Q,P);c=k.add(c,slope)
                if Q[0]=='F':assert Q==self.O
        assert Q==self.O
        return k.div(c,k.e(M))


def lifted_quarter(p,root_sign=1,check=False):
    assert p>=13 and p%4==1
    k=Ring(p,root_sign);E=Curve(k);q=p*p;n=(p-1)//4
    r,s,trials=cornacchia_quarter(p)
    ap=2*r*pow(pow(8,n,p),-1,p)%p
    trace=ap if ap%2==0 else ap-p
    M=p+1-trace if k.chi==1 else (p+1)**2-trace**2
    assert M%p
    sigma=k.e(0,1)
    R=('A',k.sub(k.e(2),sigma),k.sub(k.e(4),k.scale(2,sigma)))
    assert E.on_curve(R)
    S=E.mul(M,R);assert S[0]=='F'
    delta=k.neg(k.div(S[1],k.e(M)))
    Rlift,_=E.add(R,('F',delta))
    assert E.on_curve(Rlift) and E.mul(M,Rlift)==E.O
    A=E.miller(Rlift,M)
    _,x,y=Rlift
    w=k.div(k.scale(2,x),y)
    v=k.sub(k.e(1),k.div(k.scale(2,k.mul(k.mul(x,x),x)),k.mul(y,y)))
    e=k.div(k.sub(k.div(k.e(1),w),A),v)
    naive=k.mul(sigma,k.sub(k.e(1),A))
    assert e[1]==0,('descent',p,e)
    if check:
        projection=E.mul(p*pow(p,-1,M),R)
        assert projection==Rlift
        assert E.miller(Rlift,2*M)==A
        assert E.miller(Rlift,3*M)==A
        T=('A',k.e(0),k.e(0))
        other,_=E.add(T,E.neg(Rlift));assert E.on_curve(other)
        Aother=E.miller(other,M if M%2==0 else 2*M)
        assert k.add(A,Aother)==k.div(k.e(2),w)
    # Chowla--Dwork--Evans (1986), lifted central binomial boundary.
    boundary=(pow(2,p-1,q)+1)*pow(2,-1,q)*(2*r-p*pow(2*r,-1,q))*pow(pow(8,n,q),-1,q)%q
    alpha=(trace-p*pow(trace,-1,q))%q
    return dict(p=p,L=n,chi=k.chi,r=r,s=s,trace=trace,M=M,
                root=k.root,R=R,Rlift=Rlift,delta=delta,w=w,v=v,A=A,e=e[0],
                naive_e=naive,boundary=boundary,unit_root=alpha,calls=E.calls,
                nonresidue_trials=trials)


def reference(p,L):
    q=p*p;h=(p-1)//2;t=1;U=0;a=1;B=0;H=0;C=0
    for i in range(L):
        U=(U+(h+1+i)*t)%q
        C=(C+a*((2*i+1)+(2*i+1)**2*H)*pow(2,-1,p))%p
        B=(B+a)%q
        t=t*(h+2+i)*pow(2*i+2,-1,q)%q
        a=a*(2*i+1)*pow(4*i+4,-1,q)%q
        if i+1<L:H=(H+pow(2*i+3,-1,p))%p
    normal=(4*B-2*L*(2*L+5)*a)%q
    assert U==(normal+p*C)%q
    return dict(p=p,L=L,U=U,B=B,a=a,correction=C,normal=normal)


if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser();parser.add_argument('prime',type=int)
    z=lifted_quarter(parser.parse_args().prime,check=True)
    z.update(reference(z['p'],z['L']))
    q=z['p']**2
    z['candidate_boundary']=z['e']*(z['chi']-z['boundary'])%q
    z['candidate_unit_root']=z['e']*(z['chi']-z['unit_root'])%q
    print(json.dumps(z,indent=2))
