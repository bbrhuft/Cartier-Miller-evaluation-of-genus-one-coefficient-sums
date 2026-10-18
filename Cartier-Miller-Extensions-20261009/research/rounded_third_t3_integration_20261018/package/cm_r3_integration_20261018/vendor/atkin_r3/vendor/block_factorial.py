"""Independent generic block-product factorial comparator (not optimized BGS).

Balanced products + remainder-tree multipoint evaluation. All data acquired
from p and n; no precomputed inverse tables. Packed integer polynomial products
come from reciprocal.PolynomialRing, separately controlled against schoolbook.
"""
from math import isqrt
from reciprocal import PolynomialRing, Field

class Arithmetic:
    def __init__(self,p,backend='packed'):
        self.r=PolynomialRing(p,None,backend);self.f=Field(p);self.p=p
    def mul(self,a,b,limit=None):
        if limit is not None:
            a=a[:limit];b=b[:limit]
        c=self.r.mul(a,b)
        return self.r.norm(c if limit is None else c[:limit])
    def inverse_series(self,a,n):
        if not a or not a[0]:raise ZeroDivisionError
        x=(self.f.power(a[0],self.p-2),)
        precision=1
        while precision<n:
            precision=min(2*precision,n)
            ax=self.mul(a,x,precision)
            correction=self.r.sub((2%self.p,),ax)
            x=self.mul(x,correction,precision)
        return x
    def remainder(self,a,b):
        if not b:raise ZeroDivisionError
        if len(a)<len(b):return a
        size=len(a)-len(b)+1
        quotient_reversed=self.mul(tuple(reversed(a))[:size],self.inverse_series(tuple(reversed(b)),size),size)
        # The inverse/multiply representation may trim high zeros. The reversed
        # quotient must have exactly size slots before reversing back.
        qr=list(quotient_reversed)+[0]*(size-len(quotient_reversed))
        q=tuple(reversed(qr))
        rem=self.r.sub(a,self.mul(q,b))
        assert len(rem)<len(b)
        return rem
    def tree(self,points):
        if len(points)==1:return (((-points[0])%self.p,1),None,None)
        mid=len(points)//2
        left=self.tree(points[:mid]);right=self.tree(points[mid:])
        return self.mul(left[0],right[0]),left,right
    def evaluate_tree(self,a,tree):
        rem=self.remainder(a,tree[0])
        if tree[1] is None:return [rem[0] if rem else 0]
        return self.evaluate_tree(rem,tree[1])+self.evaluate_tree(rem,tree[2])

def factorial_block(p,n=None,backend='packed'):
    if n is None:n=(p-2)//3
    if not 0<=n<p:raise ValueError('0<=n<p required')
    ar=Arithmetic(p,backend);s=max(1,isqrt(n));blocks=n//s
    if n==0:return 1,{'block_size':s,'blocks':0,'ring_counts':ar.r.counts,'scalar_counts':ar.f.counts()}
    product=ar.tree([(-j)%p for j in range(1,s+1)])[0]
    evaluations=ar.evaluate_tree(product,ar.tree([j*s%p for j in range(blocks)]))
    result=1
    for value in evaluations:result=ar.f.mul(result,value)
    for j in range(s*blocks+1,n+1):result=ar.f.mul(result,j)
    return result,{'block_size':s,'blocks':blocks,'ring_counts':ar.r.counts,'scalar_counts':ar.f.counts()}

def q_from_factorial(p):
    G,meta=factorial_block(p)
    f=Field(p);B=f.power(4,p-2);s=f.power(-B%p,(2*p-1)//3)
    q=f.mul(f.mul(6,s),f.power(G,3*(p-2)))
    meta['normalization_counts']=f.counts()
    return q,meta
