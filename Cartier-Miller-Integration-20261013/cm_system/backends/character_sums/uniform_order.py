"""Uniform curve-order version of the nonbranch evaluator, 21 October 2026.

One differentiated Miller chain with scalar N=#E(F_p) on the normalized twist.
No inversion of p modulo N, exceptional branch, or p=5 enumeration is needed.
See UNIFORM_ORDER_PROOF.md. Prime and exact trace are supplied obligations.
The accompanying cm_character_route.py retains the preceding version unchanged.
"""
from math import isqrt
from . import cm_character_route as C


def value(p,f,a,trace,stats=None):
    if not isinstance(p,int) or p<5 or p%2==0:
        raise ValueError('requires an odd prime p>=5')
    if not isinstance(trace,int) or abs(trace)>isqrt(4*p):
        raise ValueError('requires a signed integer trace in the Hasse interval')
    f=C._trim([int(v)%p for v in f])
    if len(f) not in (4,5) or not C.squarefree(f,p):
        raise ValueError('requires a squarefree cubic or quartic')
    a%=p
    e=C.character(C.peval(f,a,p),p)
    if not e:
        raise ValueError('branch pole: outside this evaluator contract')
    g=C.normalize_at(f,a,p)
    A,B,R=C.short_model(g,p)
    n=p+1-e*trace
    alpha,end=C.miller_constant(R,n,A,p,stats)
    if end is not None:
        raise ArithmeticError('Miller endpoint contradicts supplied trace')
    if stats is not None:
        stats.update({'scalar':n,'twisted_trace':e*trace,'two_torsion':R[1]==0})
    return e*(-g[1]*pow(4,-1,p)*(n-2)-alpha*pow(2,-1,p))%p
