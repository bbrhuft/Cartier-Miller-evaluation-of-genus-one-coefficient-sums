"""Bounded rational 2-isogeny recovery, research prototype (standard library).
Trusted trace input is not certified. Root splitting is randomized; failures
are explicit. No point-count backend or performance benchmark is included.
"""
from collections import deque
from dataclasses import dataclass
from pathlib import Path
import random
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'branch_point_20261006'))
from branch_evaluator import BranchEvaluator, check_cubic, is_prime64

class RootSplitIncomplete(RuntimeError):
    pass

def trim(a,p):
    a=[x%p for x in a]
    while a and a[-1]==0:a.pop()
    return a

def add(a,b,p):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))],p)

def sub(a,b,p):return add(a,[-x for x in b],p)

def mul(a,b,p):
    if not a or not b:return []
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return trim(c,p)

def divrem(a,b,p):
    a=trim(a,p);b=trim(b,p)
    if not b:raise ZeroDivisionError('zero polynomial')
    out=[0]*max(0,len(a)-len(b)+1); inv=pow(b[-1],-1,p)
    while len(a)>=len(b):
        i=len(a)-len(b); q=a[-1]*inv%p;out[i]=q
        for j,v in enumerate(b):a[i+j]=(a[i+j]-q*v)%p
        a=trim(a,p)
    return trim(out,p),a

def monic(a,p):
    a=trim(a,p)
    return [(x*pow(a[-1],-1,p))%p for x in a] if a else []

def gcd(a,b,p):
    a=trim(a,p);b=trim(b,p)
    while b:a,b=b,divrem(a,b,p)[1]
    return monic(a,p)

def powmod(a,n,m,p,stats):
    out=[1];a=divrem(a,m,p)[1]
    while n:
        if n&1:
            out=divrem(mul(out,a,p),m,p)[1];stats['polynomial_mod_products']+=1
        n>>=1
        if n:
            a=divrem(mul(a,a,p),m,p)[1];stats['polynomial_mod_products']+=1
    return out

def rational_roots(A,B,p,rng=None,max_attempts=64,stats=None):
    """All F_p roots of nonsingular x^3+A*x+B, verified against gcd.
    Uniform independent random polynomial trials yield expected O(log p)
    field work for this fixed degree. A capped split reports incompleteness.
    Caller must ensure p is prime; max_attempts=0 exercises failure handling.
    """
    if rng is None:rng=random.SystemRandom()
    if stats is None:stats={'root_calls':0,'split_trials':0,'polynomial_mod_products':0}
    stats['root_calls']+=1
    f=[B%p,A%p,0,1]
    g=gcd(f,sub(powmod([0,1],p,f,p,stats),[0,1],p),p)
    def split(v):
        n=len(v)-1
        if n==0:return []
        if n==1:return [(-v[0]*pow(v[1],-1,p))%p]
        for _ in range(max_attempts):
            stats['split_trials']+=1
            u=[rng.randrange(p) for _ in range(n)]
            d=gcd(v,u,p)
            if len(d) in (1,len(v)):
                d=gcd(v,sub(powmod(u,(p-1)//2,v,p,stats),[1],p),p)
            if 1<len(d)<len(v):
                w,rem=divrem(v,d,p)
                if rem:raise AssertionError('factor division')
                return split(d)+split(monic(w,p))
        raise RootSplitIncomplete('randomized rational-root splitting exhausted its retry budget')
    roots=sorted(split(g))
    product=[1]
    for q in roots:
        if (q*q*q+A*q+B)%p:raise AssertionError('root check')
        product=mul(product,[-q,1],p)
    if product!=g or len(set(roots))!=len(roots):raise AssertionError('complete factor check')
    return roots

def check_short(A,B,p):
    A%=p;B%=p
    if (4*A**3+27*B**2)%p==0:raise ValueError('singular short cubic')
    return A,B

def quotient(A,B,q,p):
    if (q**3+A*q+B)%p:raise ValueError('specified kernel coordinate is not a root')
    return check_short(-4*A-15*q*q,-8*A*q-22*q**3,p)

def easy(A,B,p):
    if A%p==0 and p%3==1:return 'A=0,p=1mod3'
    if B%p==0 and p%4==1:return 'B=0,p=1mod4'
    return None

def verify_path(A,B,p,roots):
    """Target -> easy seed path. Returns beta_target/H without dividing by H."""
    A,B=check_short(A,B,p);start=(A,B);c=0;weight=1
    steps=[]
    for q in roots:
        q%=p;weight=weight*pow(2,-1,p)%p;c=(c+weight*q)%p
        nxt=quotient(A,B,q,p)
        steps.append({'source':[A,B],'root':q,'target':list(nxt),'differential_scale':1})
        A,B=nxt
    family=easy(A,B,p)
    if family is None:raise ValueError('path does not end at a permitted easy seed')
    return {'status':'verified_path','start':list(start),'endpoint':[A,B],'seed_family':family,'roots':[s['root'] for s in steps],'steps':steps,'length':len(steps),'beta_multiplier':c}

def find_path(A,B,p,max_depth=2,rng=None,max_attempts=64):
    """BFS on exact displayed models, no j-only merging or hidden scan fallback.
    Capped randomized failures are reported as incomplete, never not_found.
    Completeness means all rational normalized paths to the stated depth.
    """
    A,B=check_short(A,B,p)
    if not isinstance(max_depth,int) or isinstance(max_depth,bool) or max_depth<0:
        raise ValueError('max_depth must be a nonnegative integer')
    if max_attempts<0:raise ValueError('max_attempts must be nonnegative')
    if rng is None:rng=random.SystemRandom()
    stats={'root_calls':0,'split_trials':0,'polynomial_mod_products':0,'visited_models':1,'expanded_models':0}
    queue=deque([(A,B,0)])
    predecessors={(A,B):None}; incomplete=[]
    while queue:
        aa,bb,depth=queue.popleft()
        if easy(aa,bb,p):
            path=[];cursor=(aa,bb)
            while predecessors[cursor] is not None:
                cursor,q=predecessors[cursor];path.append(q)
            path.reverse()
            cert=verify_path(A,B,p,path);cert.update({'status':'found','max_depth':max_depth,'statistics':stats,'root_method':'fixed_degree_randomized_factorization'})
            return cert
        if depth>=max_depth:continue
        stats['expanded_models']+=1
        try:roots=rational_roots(aa,bb,p,rng,max_attempts,stats)
        except RootSplitIncomplete:
            incomplete.append({'model':[aa,bb],'depth':depth})
            continue
        for q in roots:
            nxt=quotient(aa,bb,q,p)
            if nxt not in predecessors:
                predecessors[nxt]=((aa,bb),q);queue.append((*nxt,depth+1));stats['visited_models']+=1
    return {'status':'incomplete_root_splitting' if incomplete else 'not_found_within_depth','max_depth':max_depth,'statistics':stats,'incomplete_models':incomplete,'root_method':'fixed_degree_randomized_factorization'}

def short_model(f,p):
    _,c,b,a=f
    return ((a*c-b*b*pow(3,-1,p))%p,(a*a-a*b*c*pow(3,-1,p)+2*b**3*pow(27,-1,p))%p)

@dataclass(frozen=True)
class ClosurePreparation:
    evaluator: BranchEvaluator
    certificate: dict
    trusted_exact_trace: int

def prepare_from_trace(p,f,trusted_exact_trace,*,roots=None,max_depth=2,rng=None,max_attempts=64):
    """Return preparation or explicit search status. Trace remains caller trusted.
    roots is a supplied target-to-seed path, including [] for an easy input.
    Path verification O(length); automatic discovery expected O(3^d log p).
    """
    if p<7 or not is_prime64(p):raise ValueError('require prime 7<=p<2^64')
    f=check_cubic(f,p)
    if not isinstance(trusted_exact_trace,int) or isinstance(trusted_exact_trace,bool) or trusted_exact_trace**2>4*p:
        raise ValueError('trusted trace fails necessary Hasse bound; this is not certification')
    A,B=short_model(f,p)
    cert=verify_path(A,B,p,roots) if roots is not None else find_path(A,B,p,max_depth,rng,max_attempts)
    if cert['status'] not in ('found','verified_path'):return cert
    H=trusted_exact_trace%p; beta=cert['beta_multiplier']*H%p
    _,_,b,a=f;K=(beta-b*pow(3,-1,p)*H)*pow(a,-1,p)%p
    return ClosurePreparation(BranchEvaluator(p,f,H,K,'degree_two_closure_caller_supplied_exact_trace'),cert,trusted_exact_trace)
