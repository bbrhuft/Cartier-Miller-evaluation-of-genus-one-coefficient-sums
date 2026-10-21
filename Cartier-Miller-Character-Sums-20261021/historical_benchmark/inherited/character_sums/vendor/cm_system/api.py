"""Bounded exact integration. Public services validate before arithmetic.

This is a research API, not a new boundary or Witt extraction algorithm.
"""
from dataclasses import dataclass, field
from math import isqrt
from .backends import elliptic, ordinary_third, hyperelliptic_prefix as hg
from .backends import product_tree as pt
from .backends.cm import d7_seed, fixed_D_evaluator as cm


class Unsupported(ValueError):
    pass


class ResourceLimit(ValueError):
    pass


def prime(p):
    if isinstance(p, bool) or not isinstance(p, int) or p < 5 or not d7_seed.is_prime64(p):
        raise ValueError('require a prime 5 <= p < 2^64')


def integer(n, name):
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError(name + ' must be an integer')


def sum_input(p, L, precision):
    prime(p); integer(L, 'L'); integer(precision, 'precision')
    if not 0 <= L <= (p-1)//2:
        raise ValueError('require 0 <= L <= (p-1)/2')
    if precision not in (1, 2):
        raise Unsupported('integrated precision is 1 or 2')


def original_direct(p, L, q):
    """Cleared-denominator ORIGINAL rational recurrence; one final inverse."""
    h=(p-1)//2; t=1; u=0; den=1
    for i in range(L):
        d=2*(i+1)
        u=d*(u+(h+1+i)*t)%q
        t=(h+2+i)*t%q
        den=den*d%q
    return u*pow(den, -1, q)%q


def binomial_direct(p, indices, q):
    wanted=set(indices); A=1; B=0; D=1; out={}
    for n in range(max(wanted)+1):
        if n in wanted:
            inv=pow(D,-1,q); out[n]=(A*inv%q,B*inv%q)
        if n < max(wanted):
            d=4*(n+1)
            A,B,D=A*(2*n+1)%q,(B+A)*d%q,D*d%q
    return out


def binomial_tree(p, L, q):
    if L == 0: return 1, 0
    P=pt.product_bsgs(pt.coef_S(1,q),L,2,q)
    inv=pow(P[(1,1)],-1,q)
    return P[(0,0)]*inv%q,P[(1,0)]*inv%q


def interval_product(start, length, q):
    if length == 0:return 1
    return pt.product_bsgs({(0,0):(start,1)},length,1,q)[(0,0)]


def boundary_product(p,L):
    """Central binomial by two interval products; no prefix computed."""
    if L == 0:return 1
    num=interval_product(L+1,L,p)
    den=interval_product(1,L,p)
    return num*pow(den,-1,p)*pow(8,-L,p)%p


def fifth_boundaries(p):
    """Tenth-point formulas: three half-length products, still sqrt scale."""
    if p%5 != 4:raise Unsupported('fifth reduction requires p = 4 mod 5')
    L=(p+1)//5; ell=L//2
    den=interval_product(1,ell,p); inv=pow(den,-1,p)
    x=interval_product(2*L-ell,ell,p)*inv%p
    y=interval_product(L-ell+1,ell,p)*inv%p
    sign=-1 if ell%2 else 1
    return {L:sign*pow(2,-2*L,p)*x%p,
            2*L:sign*pow(2,2*L,p)*pow(16,-1,p)*y%p}


def rounded_boundary(p):
    """Retained factorial reduction a_(m+1) = 3/(2*(m!)^3)."""
    m=(p-2)//3
    G=interval_product(1,m,p)
    return 3*pow(2,-1,p)*pow(pow(G,3,p),-1,p)%p


def reconstruct(p,L,a,B):
    return (4*B-2*L*(2*L+5)*a)%p


@dataclass
class Budget:
    direct_terms:int=500_000
    block_width:int=4096
    genus:int=8
    point_count_prime:int=5000

    def __post_init__(self):
        for name in ('direct_terms','block_width','genus','point_count_prime'):
            value=getattr(self,name);integer(value,name)
            if value<1:raise ValueError('budget limits must be positive')


@dataclass
class Session:
    """Explicit reusable per-prime setup. Create a fresh one for complete timing."""
    p:int
    budget:Budget=field(default_factory=Budget)
    cache:dict=field(default_factory=dict,init=False)
    def __post_init__(self):prime(self.p)

    def _block(self,L):
        if isqrt(L)>self.budget.block_width:
            raise ResourceLimit('product block exceeds configured width budget')

    def plan(self,L,precision=1):
        sum_input(self.p,L,precision);p=self.p;h=(p-1)//2
        choices=['direct','product_tree']
        if precision==1:
            if L in (0,h):choices.insert(0,'endpoint')
            if p>=13 and p%4==1 and L==(p-1)//4:choices.insert(0,'quarter')
            if p%3==1 and L==(p-1)//3:choices.insert(0,'ordinary_third')
            for g in range(1,self.budget.genus+1):
                d=2*g+1
                if p>d and p%d==d-1 and L and L%((p+1)//d)==0 and L//((p+1)//d)<=g:
                    choices.append('higher:'+str(g))
        # Conservative policy: no automatic higher-genus claim while its
        # boundary remains product work. Explicit hybrids are available.
        selected=next((x for x in choices if x in ('endpoint','quarter','ordinary_third')),None)
        if selected is None:selected='direct' if L<=128 else 'product_tree'
        return {'p':p,'L':L,'precision':precision,'candidates':choices,'selected':selected,
                'policy':'structural complete methods first; direct <=128; otherwise product tree; no fitted crossover'}

    def evaluate(self,L,precision=1,method='auto'):
        plan=self.plan(L,precision);p=self.p;q=p**precision
        if method=='auto':method=plan['selected']
        if method not in plan['candidates']:
            raise Unsupported('method does not apply to this input')
        out={'p':p,'L':L,'precision':precision,'modulus':q,'status':'exact',
             'target':'original_U','method':method,'cache_reused':False,
             'input_certification':'deterministic 64-bit primality test',
             'scope':'research prototype; no generic polylogarithmic claim'}
        if method=='endpoint':
            out.update(U=0 if L==0 else 4*elliptic.legendre2(p)%p,
                       complete_cost='O(1) field work after prime validation')
        elif method=='direct':
            if L>self.budget.direct_terms:raise ResourceLimit('direct term budget exceeded')
            out.update(U=original_direct(p,L,q),complete_cost='O(L) ring operations; O(1) state')
        elif method=='product_tree':
            self._block(L)
            P=pt.product_bsgs(pt.coef_U(p,q),L,4,q)
            V=[(P.get((i,0),0)+P.get((i,3),0))%q for i in range(4)]
            out.update(U=V[2]*pow(V[3],-1,q)%q,
                       complete_cost='polynomial product/remainder tree in sqrt(L); Python integer multiplication',
                       backend=pt.PZ.BACKEND)
        elif method in ('quarter','ordinary_third'):
            key=(method,)
            reuse=key in self.cache
            if not reuse:
                self.cache[key]=elliptic.quarter(p) if method=='quarter' else ordinary_third.third(p)
            z=self.cache[key]
            out.update(U=z['U'],B=z['B'],a=z['a'],trace=z['trace'],M=z['M'],
                       cache_reused=reuse,exceptional=z.get('exceptional',False),
                       setup_method='Cornacchia/classical CM normalization; deterministic nonresidue scan',
                       complete_cost='O(log p) Miller work after setup; no unconditional polylog bound for scan')
        else:
            g=int(method.split(':')[1]);d=2*g+1;step=(p+1)//d;j=L//step
            key=('higher',g);reuse=key in self.cache
            if not reuse:self.cache[key]=hg.prefixes(p,d)
            z=self.cache[key];B=z['B'][j-1]
            factor=2*L*(2*L+5)%p
            if factor==0:
                out.update(U=4*B%p,B=B,a=None,genus=g,cache_reused=reuse,
                           prefix_cost='O(g^3 log p), includes family setup',
                           boundary_method='not required: boundary multiplier is zero',
                           complete_cost='prefix only; boundary work skipped')
                return out
            if g==2:
                ell=step//2;self._block(ell)
                denkey=('fifth_interval',0)
                if denkey not in self.cache:self.cache[denkey]=interval_product(1,ell,p)
                interval=3 if j==1 else 1;bk=('fifth_interval',interval)
                if bk not in self.cache:
                    start=3*ell if j==1 else ell+1
                    self.cache[bk]=interval_product(start,ell,p)
                v=self.cache[bk]*pow(self.cache[denkey],-1,p)%p;sign=-1 if ell%2 else 1
                a=(sign*pow(2,-2*step,p)*v if j==1 else sign*pow(2,2*step,p)*pow(16,-1,p)*v)%p
                boundary='lazy tenth-point intervals: two for one boundary, three shared across the pair'
            elif g==1:
                self._block((p-2)//3);a=rounded_boundary(p);boundary='rounded-third factorial reduction by product tree'
            else:
                self._block(L);a=boundary_product(p,L);boundary='central-binomial interval products'
            out.update(U=reconstruct(p,L,a,B),B=B,a=a,genus=g,cache_reused=reuse,
                       prefix_cost='O(g^3 log p), includes family setup',boundary_method=boundary,
                       complete_cost='prefix plus square-root-scale product boundary; no exponent saving claimed')
        return out

    def evaluate_many(self,indices,precision=1,method='auto'):
        if method=='direct':
            indices=list(indices)
            if not indices:return []
            for L in indices:sum_input(self.p,L,precision)
            if max(indices)>self.budget.direct_terms:raise ResourceLimit('direct term budget exceeded')
            p=self.p;q=p**precision;h=(p-1)//2;t=1;u=0;den=1;values={};wanted=set(indices)
            for i in range(max(indices)+1):
                if i in wanted:values[i]=u*pow(den,-1,q)%q
                if i<max(indices):
                    d=2*(i+1);u=d*(u+(h+1+i)*t)%q;t=(h+2+i)*t%q;den=den*d%q
            return [{'p':p,'L':L,'precision':precision,'modulus':q,'U':values[L],
                     'status':'exact','target':'original_U','method':'shared_direct',
                     'cache_reused':False,'complete_cost':'O(max(indices)) ring operations, O(number of outputs) storage'}
                    for L in indices]
        return [self.evaluate(L,precision,method) for L in indices]


def evaluate(p,L,precision=1,method='auto',budget=None):
    return Session(p,budget or Budget()).evaluate(L,precision,method)


def point_trace(p,A,B):
    return -sum(0 if (v:=(x*x*x+A*x+B)%p)==0 else 1 if pow(v,(p-1)//2,p)==1 else -1 for x in range(p))


def streaming_cubic(p,f):
    """H,K of normalized cubic, using the retained scaled recurrence."""
    _,c,b,a=f;h1=(p+1)//2;v0,v1,v2=1,0,0
    for n in range(1,p):
        v0,v1,v2=((h1-n)*c*v0+(2*h1-n)*b*v1+(3*h1-n)*a*v2)%p,n*v0%p,n*v1%p
    return -v0%p,-v1%p


def cartier_data(p,A,B,trace=None,budget=None):
    """Separate coefficient service; does not purport to evaluate U."""
    prime(p)
    if p<7:raise Unsupported('Cartier service requires p>=7')
    integer(A,'A');integer(B,'B');A%=p;B%=p
    if (4*A**3+27*B*B)%p==0:raise ValueError('singular short model')
    budget=budget or Budget();hits=cm.slope_from_cm_table(A,B,p)
    if len({x[1] for x in hits})>1:raise ArithmeticError('conflicting CM slopes')
    trusted=False
    if hits:
        if trace is not None:
            integer(trace,'trace')
            if trace*trace>4*p or trace%p==0:raise ValueError('trace fails necessary ordinary conditions')
            rec=d7_seed.recognize_d7(A,B,p)
            if rec['status']=='recognized':
                ok,why=d7_seed.verify_supplied_trace(p,rec['matches'][0]['parameters']['r'],trace)
                if not ok:raise ValueError(why)
                source='supplied trace certified by D=-7 shape/sign'
            else:source='caller-trusted exact trace; Hasse bound is not certification';trusted=True
        else:
            rec=d7_seed.recognize_d7(A,B,p)
            if rec['status']=='recognized':
                trace,_=d7_seed.signed_trace_d7(p,rec['matches'][0]['parameters']['r']);source='D=-7 signed CM trace'
            elif p<=budget.point_count_prime:
                trace=point_trace(p,A,B);source='direct point count, O(p log p) field work'
            else:raise ResourceLimit('recognized slope needs trace; direct point-count budget exceeded')
        H=trace%p;beta=hits[0][1]*H%p;method='fixed_D_CM_table'
        if H==0:raise ArithmeticError('CM ordinary eligibility contradicted')
    else:
        if p>budget.direct_terms:raise ResourceLimit('generic Cartier coefficient recurrence budget exceeded')
        shift=next(s for s in range(4) if (s**3+A*s+B)%p)
        C=(shift**3+A*shift+B)%p;ic=pow(C,-1,p)
        H,beta=streaming_cubic(p,(1,(3*shift*shift+A)*ic%p,3*shift*ic%p,ic))
        scale=pow(C,(p-1)//2,p);H=H*scale%p;beta=(beta*scale+shift*H)%p
        method='streaming_cubic_coefficients_O(p)';source='coefficient recurrence; trace not needed'
        if trace is not None:
            integer(trace,'trace')
            if trace*trace>4*p or trace%p!=H:raise ValueError('supplied trace contradicts computed H')
    return {'p':p,'A':A,'B':B,'H':H,'beta':beta,'kappa':beta*pow(H,-1,p)%p if H else None,
            'ordinary':H!=0,'method':method,'CM_hits':hits,'trace_source':source,
            'status':'conditional_on_trusted_trace' if trusted else 'exact',
            'target':'short_model_Cartier_coefficients','basis':'omega=dx/y, eta=x dx/y'}


def branch_query(p,f,mu,trace=None,budget=None):
    prime(p);integer(mu,'mu');f=d7_seed.check_cubic(f,p);mu%=p
    if mu==0 or d7_seed.eval_poly(f,mu,p):raise ValueError('require supplied nonzero root')
    A,B=d7_seed.short_model(f,p);z=cartier_data(p,A,B,trace,budget)
    K=(z['beta']-f[2]*pow(3,-1,p)*z['H'])*pow(f[3],-1,p)%p
    der=(f[1]+2*f[2]*mu+3*f[3]*mu*mu)%p
    T=f[3]*mu*(mu*z['H']-K)*pow(der,-1,p)%p
    return {**z,'target':'cubic_branch_sum','f':list(f),'mu':mu,'K':K,'T':T,
            'root_finding_included':False,'query_cost':'O(1) after coefficient preparation'}


def quarter_precision_diagnostics(p,method='product_tree',budget=None):
    """Complete B,U and Witt recovery; explicitly computes sums first."""
    from .backends import padic_lift as pa
    prime(p)
    if p<13 or p%4!=1:raise Unsupported('quarter precision diagnostics require p>=13, p=1 mod4')
    if method not in ('direct','product_tree'):raise Unsupported('diagnostic backend must be direct or product_tree')
    session=Session(p,budget or Budget());z=pa.lifted_quarter(p);L=z['L'];q=p*p
    if method=='direct':
        if L>session.budget.direct_terms:raise ResourceLimit('direct term budget exceeded')
        a,B=binomial_direct(p,[L],q)[L]
    else:session._block(L);a,B=binomial_tree(p,L,q)
    if a!=z['boundary']:raise ArithmeticError('boundary lift disagrees with independent product')
    K=pt.K_reverse(p,z,B)
    G=pt.kpow(pa.Ring(p),pa.Ring(p).scale(z['M'],z['v']),p-1)[0]*pow(z['e'],p,q)-z['e']*a
    Gamma=G%q;d=(z['w'][0]-1)//p;b=B%p
    prediction=(Gamma-p*(K+2*d*(b+a)))%q
    if prediction!=B:raise ArithmeticError('W2 recovery mismatch')
    U=session.evaluate(L,2,method)['U']
    base=(4*B-2*L*(2*L+5)*a)%q
    if (U-base)%p:raise ArithmeticError('original correction does not reduce modulo p')
    Hcorr=((U-base)%q)//p
    J=(Hcorr-2*(a%p)-4*K-8*d*(b+a))%p
    if (4*Gamma+9*pow(4,-1,q)*a+p*J)%q!=U:raise ArithmeticError('combined correction mismatch')
    return {'p':p,'L':L,'precision':2,'B':B,'a':a,'U':U,'epsilon':z['e'],
            'K_p':K,'Gamma':Gamma,'pole_shift_d':d,'harmonic_correction_mod_p':Hcorr,
            'combined_J_p':J,'status':'exact','target':'complete_quarter_precision_diagnostics',
            'method':method,'Witt_acquisition':'recovered from computed B; NOT sum-avoiding extraction',
            'harmonic_acquisition':'recovered from independently computed original U',
            'naive_boundary':z['e']*(z['chi']-a)%q,
            'naive_unit_root':z['e']*(z['chi']-z['unit_root'])%q}


def weighted_sum(p,L,coefficients,budget=None):
    """Falling-factorial weighted a_i prefix, modulo p; B and a shared."""
    for c in coefficients:integer(c,'weight')
    if len(coefficients)>32:raise ResourceLimit('weight degree cap is 31')
    session=Session(p,budget or Budget());plan=session.plan(L)
    if plan['selected'] in ('quarter','ordinary_third'):
        z=session.evaluate(L);a,B=z['a'],z['B'];preparation=z['method']
    elif L<=128:
        if L>session.budget.direct_terms:raise ResourceLimit('direct term budget exceeded')
        a,B=binomial_direct(p,[L],p)[L];preparation='direct_binomial_state'
    else:
        session._block(L);a,B=binomial_tree(p,L,p);preparation='binomial_product_tree'
    T=B;fall=1;half=pow(2,-1,p);ans=0
    for r,c in enumerate(coefficients):
        if r:fall=fall*(L-r+1)%p;T=((r-half)*T-2*fall*a)%p
        ans=(ans+c*T)%p
    return {'p':p,'L':L,'value':ans,'weight_basis':'falling factorial','target':'weighted_binomial_prefix',
            'status':'exact','coefficients':list(coefficients),'preparation_method':preparation}


def general_weight_prefixes(p,g,lam,budget=None):
    from .backends.general_argument import prefixes_general
    prime(p);integer(g,'genus');integer(lam,'lambda');budget=budget or Budget()
    if not 1<=g<=budget.genus:raise ResourceLimit('genus budget exceeded')
    d=2*g+1;lam%=p
    if p<=d or p%d!=d-1 or lam in (0,1):raise Unsupported('general-weight family hypotheses fail')
    vals=prefixes_general(p,d,lam)
    return {'p':p,'genus':g,'lambda':lam,'indices':[j*(p+1)//d for j in range(1,g+1)],
            'values':vals,'status':'exact','target':'general_weight_prefixes',
            'complete_cost':'O(g^3 log p) field work including family setup',
            'derivative_available':False}
