"""Extension to S(h,L;-lam), with the measured half-argument core unchanged."""
from .hyperelliptic_prefix import Field,Jacobian,SplitRoot

class ParameterField(Field):
    def __init__(self,p,radicand,root=None):
        super().__init__(p,root);self.radicand=radicand
    def mul(self,a,b):
        return ((a[0]*b[0]+self.radicand*a[1]*b[1])%self.p,
                (a[0]*b[1]+a[1]*b[0])%self.p)
    def inv(self,a):
        self.inversions+=1
        norm=(a[0]*a[0]-self.radicand*a[1]*a[1])%self.p
        if not norm:
            if a==self.zero:raise ZeroDivisionError('zero field element')
            raise SplitRoot(a[0]*pow(a[1],-1,self.p)%self.p)
        t=pow(norm,-1,self.p)
        return (a[0]*t%self.p,-a[1]*t%self.p)

class ParameterJacobian(Jacobian):
    def __init__(self,k,d,lam,jets):
        super().__init__(k,d,jets)
        self.f[-1]=k.e(-lam)
        self.y=[k.one]+[k.zero]*(self.prec-1)
        for n in range(1,self.prec):
            t=self.f[n] if n<len(self.f) else k.zero
            for i in range(1,n):t=k.sub(t,k.mul(self.y[i],self.y[n-i]))
            self.y[n]=k.scale(t,pow(2,-1,k.p))

def prefixes_general(p,d,lam):
    """Prime p assumed; output sum_{k<L} binom(h,k)*(-lam)^k mod p."""
    lam%=p
    assert p>2 and d>=3 and d%2 and p%d==d-1 and lam not in (0,1)
    root=None;radicand=(1-lam)%p;g=(d-1)//2
    while True:
        k=ParameterField(p,radicand,root);J=ParameterJacobian(k,d,lam,g)
        v=k.e(0,1);Q=([k.e(-1),k.one],[v])
        try:
            A=J.miller(Q,p+1)
            chi=pow(radicand,(p-1)//2,p)
            scale=k.scale(k.inv(v),-chi)
            values=[k.mul(scale,k.add(k.scale(a,2),k.one)) for a in A]
            assert all(a[1]==0 for a in values)
            return [a[0] for a in values]
        except SplitRoot as e:
            assert root is None and e.root*e.root%p==radicand
            root=e.root

if __name__=='__main__':
    import json,math,time
    from pathlib import Path
    start=time.perf_counter();pairs=prefix_count=0
    for p in range(3,150):
        if any(p%i==0 for i in range(2,math.isqrt(p)+1)):continue
        for d in range(3,12,2):
            if p%d!=d-1:continue
            h=(p-1)//2;L=(p+1)//d
            for lam in range(2,p):
                vals=prefixes_general(p,d,lam)
                ref=[sum(math.comb(h,k)*pow(-lam,k,p) for k in range(j*L))%p
                     for j in range(1,(d+1)//2)]
                assert vals==ref,(p,d,lam,vals,ref)
                pairs+=1;prefix_count+=len(vals)
    result={'status':'all checks passed','p_bound_exclusive':150,'d_values':[3,5,7,9,11],
            'lambda_scope':'every element of F_p except 0 and 1',
            'parameter_triples':pairs,'prefixes':prefix_count,'seconds':time.perf_counter()-start}
    out=Path(__file__).resolve().parents[1]/'results/general_argument_validation.json'
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
