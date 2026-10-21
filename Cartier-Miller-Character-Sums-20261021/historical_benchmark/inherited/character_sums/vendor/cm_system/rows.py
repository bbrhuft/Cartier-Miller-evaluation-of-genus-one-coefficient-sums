"""Main genus-one row theorem, including direct characteristic-p exception.

Arithmetic adapted from the retained evaluator; no SymPy dependency. Supplied
traces are explicitly trusted, not certified by a Hasse interval.
"""
from .api import prime, integer, Budget, ResourceLimit, Unsupported, branch_query
from .backends.genus_one.curve import Model,trace_naive
from .backends.genus_one.fields import FpCtx,QuadCtx
from .backends.genus_one.miller import miller_alpha_resumable,miller_continue,Resume


class RowSession:
    def __init__(self,p,f,trace=None,budget=None):
        prime(p)
        if p<7:raise Unsupported('genus-one row service requires p>=7')
        budget=budget or Budget()
        if len(f) not in (4,5) or any(isinstance(c,bool) or not isinstance(c,int) for c in f):
            raise ValueError('use 4 or 5 integer coefficients, low to high')
        f=[c%p for c in f]
        if f[0]!=1 or f[-1]==0:raise ValueError('require f(0)=1 and exact degree 3 or 4')
        model=Model(f,p)
        if model.disc==0:raise ValueError('singular genus-one model')
        self.p=p;self.f=f;self.model=model;self.budget=budget
        if trace is None:
            if p>budget.point_count_prime:raise ResourceLimit('point-count setup budget exceeded; supply trusted trace')
            trace=trace_naive(model.A,model.B,p);source='direct point count';self.trusted=False
        else:
            integer(trace,'trace');source='caller-trusted exact trace';self.trusted=True
        if trace*trace>4*p:raise ValueError('trace fails necessary Hasse interval')
        self.trace=trace;self.H=trace%p;self.source=source

    def query(self,lam):
        integer(lam,'lambda');p=self.p;lam%=p
        base={'p':p,'f':self.f,'lambda':lam,'trace':self.trace,'H':self.H,
              'status':'conditional_on_trusted_trace' if self.trusted else 'exact',
              'target':'genus_one_row_S','trace_source':self.source,
              'query_cost':'O(log p) field work after trace/model preparation'}
        if lam==0:return {**base,'S':self.H,'method':'lambda_zero_coefficient'}
        w=pow(lam,-1,p);d=self.model.fval(FpCtx(p),w)
        if d==0:
            if len(self.f)!=4:raise Unsupported('quartic branch query not integrated')
            z=branch_query(p,self.f,w,trace=self.trace,budget=self.budget)
            return {**base,'S':z['T'],'method':'cubic_branch_service',
                    'trace_reused':'row trace transferred through the two curve isomorphisms'}
        chi=1 if pow(d,(p-1)//2,p)==1 else -1;M=p+1-chi*self.trace
        k=QuadCtx(p,d);R=self.model.to_short(k,k.fromint(w),k.gen);split=False
        try:
            alpha,_=miller_alpha_resumable(k,R,M,self.model.A)
            rphi=2*alpha[1]*pow(lam,-1,p)%p
        except Resume as z:
            split=True;root=k.sqrt_from_witness(z.witness);F=FpCtx(p)
            def comp(e,i):return (e[0]+(1 if i==0 else -1)*e[1]*root)%p
            alphas=[]
            for i in (0,1):
                T=None if z.T is None else tuple(comp(e,i) for e in z.T)
                Ri=tuple(comp(e,i) for e in R)
                a,_=miller_continue(F,Ri,M,self.model.A,T,comp(z.alpha,i),z.j)
                alphas.append(a)
            rphi=(alphas[0]-alphas[1])*pow(lam*root,-1,p)%p
        rpsi=rphi*pow(self.model.kappa,-1,p)%p
        S=(self.H-chi*rpsi)%p
        return {**base,'S':S,'chi':chi,'M':M,'exceptional':M%p==0,
                'method':'undivided_Cartier_Miller','split_fallback':split,
                'exceptional_proof':'retained direct characteristic-p normalization' if M%p==0 else None}
