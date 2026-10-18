"""Costed reciprocal division-polynomial extraction; certified prime input.

No factorial/binomial oracle is used here. The inherited normalized recurrence
is called unchanged. States are in F_p[T,epsilon]/(T^N,epsilon^2).
The precision N=(p+1)//6 is linear in p; no fast-extraction claim is made.
"""
from pathlib import Path
import sys, argparse, json
sys.path.insert(0,str(Path(__file__).resolve().parent/'inherited'))
from retained.stack_safe_beta import division_values, Field

class PolynomialRing:
    def __init__(self,p,precision=None,backend='naive'):
        self.p=p; self.precision=precision; self.backend=backend
        self.zero=();self.one=(1,)
        self.counts={'coefficient_additions':0,'coefficient_multiplications':0,
                     'polynomial_multiplications':0,'packed_integer_multiplications':0,
                     'packed_coefficient_reductions':0,'maximum_length':0,
                     'packed_max_operand_bits':0,'packed_max_digit_bits':0}
    def norm(self,a):
        if self.precision is not None:a=a[:self.precision]
        a=list(a)
        while a and a[-1]==0:a.pop()
        self.counts['maximum_length']=max(self.counts['maximum_length'],len(a))
        return tuple(a)
    def c(self,n):
        n%=self.p
        return (n,) if n else ()
    def add(self,a,b,sign=1):
        n=max(len(a),len(b)); out=list(a)+(n-len(a))*[0]
        for i,v in enumerate(b):out[i]=(out[i]+sign*v)%self.p
        self.counts['coefficient_additions']+=len(b)
        return self.norm(out)
    def sub(self,a,b):return self.add(a,b,-1)
    def mul(self,a,b):
        self.counts['polynomial_multiplications']+=1
        if not a or not b:return ()
        n=len(a)+len(b)-1
        if self.precision is not None:n=min(n,self.precision)
        if self.backend=='packed':
            bound=min(len(a),len(b))*(self.p-1)**2
            width=max(1,(bound.bit_length()+7)//8)
            aa=int.from_bytes(b''.join(v.to_bytes(width,'little') for v in a),'little')
            bb=int.from_bytes(b''.join(v.to_bytes(width,'little') for v in b),'little')
            product=aa*bb
            data=product.to_bytes(width*(len(a)+len(b)-1),'little')
            out=[int.from_bytes(data[i*width:(i+1)*width],'little')%self.p for i in range(n)]
            self.counts['packed_integer_multiplications']+=1
            self.counts['packed_coefficient_reductions']+=n
            self.counts['packed_max_operand_bits']=max(self.counts['packed_max_operand_bits'],aa.bit_length(),bb.bit_length())
            self.counts['packed_max_digit_bits']=max(self.counts['packed_max_digit_bits'],8*width)
        else:
            out=[0]*n
            for i,u in enumerate(a):
                if not u:continue
                for j,v in enumerate(b[:n-i]):
                    if not v:continue
                    out[i+j]=(out[i+j]+u*v)%self.p
                    self.counts['coefficient_multiplications']+=1
                    self.counts['coefficient_additions']+=1
        return self.norm(out)

class DualPolynomial:
    def __init__(self,r):
        self.r=r;self.zero=(r.zero,r.zero);self.one=(r.one,r.zero)
    def c(self,n):return self.r.c(n),self.r.zero
    def add(self,a,b):return self.r.add(a[0],b[0]),self.r.add(a[1],b[1])
    def sub(self,a,b):return self.r.sub(a[0],b[0]),self.r.sub(a[1],b[1])
    def mul(self,a,b):
        r=self.r
        return r.mul(a[0],b[0]),r.add(r.mul(a[0],b[1]),r.mul(a[1],b[0]))

def reciprocal_state(p,precision,backend='naive',indices=None):
    if type(p) is not int or p<11 or p%3!=2:raise ValueError('certified prime p>=11, p=2 mod3 required')
    r=PolynomialRing(p,precision,backend);d=DualPolynomial(r)
    variable=r.norm((0,1))
    values,F,states=division_values(d,(p,) if indices is None else indices,
                                  d.one,(r.zero,r.one),(variable,r.zero))
    return values,d,r,states

def extract(p,backend='naive'):
    k=(p-5)//6;N=k+1
    values,d,r,states=reciprocal_state(p,N,backend)
    coefficient=values[p][1][k] if len(values[p][1])>k else 0
    if not coefficient:raise ArithmeticError('nonzero leading coefficient theorem failed; check input primality')
    f=Field(p)
    B=f.power(4,p-2)
    s=f.power((-B)%p,(2*p-1)//3)
    Bk=f.power(B,k)
    c=f.mul(coefficient,Bk)
    q=f.mul(f.mul(3,s),c)
    return {'p':p,'k':k,'precision':N,'reciprocal_leading_coefficient':coefficient,
            'c_p':c,'x_star':s,'q_p':q,'backend':backend,
            'cached_indices':states,'ring_counts':r.counts,'scalar_setup_and_normalization_counts':f.counts(),
            'state_residue_slot_upper_bound':2*N*(states+5),
            'acquisition':'[T^k epsilon] psi_p(1,epsilon,T), then q=3*x_star*4^(-k)*coefficient'}

def final_cancellation(p,precision,backend='naive'):
    a=(p-1)//2
    children=(a-1,a,a+1,a+2)
    values,d,r,states=reciprocal_state(p,precision,backend,children)
    cube=lambda v:d.mul(d.mul(v,v),v)
    left=d.mul(values[a+2],cube(values[a]))
    right=d.mul(values[a-1],cube(values[a+1]))
    Q=d.mul(d.c(4),d.add(d.add(d.one,(r.zero,r.one)),(r.norm((0,1)),r.zero)))
    if a%2==0:left=d.mul(d.mul(Q,Q),left)
    else:right=d.mul(d.mul(Q,Q),right)
    out=d.sub(left,right)
    return {'left':left,'right':right,'difference':out,'counts':r.counts}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('p',type=int);ap.add_argument('--backend',choices=['naive','packed'],default='naive')
    a=ap.parse_args();print(json.dumps(extract(a.p,a.backend),indent=2))
