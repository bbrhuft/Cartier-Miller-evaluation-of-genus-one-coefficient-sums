"""Paired fifth-point integration: p >= 19 prime, p = 4 modulo 5.

Returns complete original U sums at L=(p+1)/5 and 2L. One genus-two
Cantor--Miller pass supplies both strict prefixes; three half-length interval
products supply both boundaries, with one shared denominator inverse.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from math import isqrt
from time import perf_counter

from boundary_framework import (
    BoundaryError, ResourceLimitError, UnsupportedPrefixError,
    _multipoint, _product_tree, _bgs_interval_product, is_prime64, __version__,
)
from retained_cm.hyperelliptic_prefix import prefixes


@dataclass(frozen=True)
class IntervalResult:
    start: int
    length: int
    value: int
    backend: str
    block_degree: int
    setup_seconds: float
    evaluation_seconds: float


class IntervalProductEvaluator:
    """Unit interval products in an already validated prime field.

    The caller validates p. Intervals are [start,start+length), with factors
    in 1..p-1. Products use the same exact polynomial kernel as factorials.
    """
    def __init__(self, direct_cutoff=262144, max_degree=8192, max_direct_terms=2_000_000):
        for value,name,minimum in ((direct_cutoff,'direct_cutoff',0),
                                  (max_degree,'max_degree',1),
                                  (max_direct_terms,'max_direct_terms',0)):
            if type(value) is not int or value<minimum:
                raise BoundaryError(f'{name} must be an integer >= {minimum}')
        self.direct_cutoff,self.max_degree,self.max_direct_terms=direct_cutoff,max_degree,max_direct_terms

    def product(self,p,start,length,backend='auto'):
        if type(start) is not int or type(length) is not int or length<0 or start<1 or start+length>p:
            raise BoundaryError('unit interval requires integers start >= 1, length >= 0, start+length <= p')
        if not isinstance(backend,str) or backend not in ('auto','direct','product_tree','bgs'):
            raise BoundaryError('unknown interval backend')
        selected=backend
        if selected=='auto':
            selected='direct' if length<=self.direct_cutoff else 'bgs'
        if selected=='direct':
            if length>self.max_direct_terms:
                raise ResourceLimitError('direct interval term limit exceeded')
            begin=perf_counter();value=1
            for j in range(start,start+length): value=value*j%p
            return IntervalResult(start,length,value,selected,0,0.0,perf_counter()-begin)
        if selected=='bgs':
            value,degree,setup,elapsed=_bgs_interval_product(p,start,length,self.max_degree)
            return IntervalResult(start,length,value,selected,degree,setup,elapsed)
        degree=isqrt(length)
        if degree>self.max_degree:
            raise ResourceLimitError('product-tree interval degree limit exceeded')
        begin=perf_counter()
        if length==0:
            return IntervalResult(start,0,1,selected,0,0.0,perf_counter()-begin)
        f=_product_tree([[(start+j)%p,1] for j in range(degree)],p)[-1][0]
        tree=_product_tree([[(-i*degree)%p,1] for i in range(degree)],p)
        setup=perf_counter()-begin;begin=perf_counter();value=1
        for x in _multipoint(f,tree,p): value=value*x%p
        for j in range(degree*degree,length): value=value*(start+j)%p
        return IntervalResult(start,length,value,selected,degree,setup,perf_counter()-begin)


class FifthBoundaryEvaluator:
    """Retained tenth-point reductions, evaluated with shared interval work."""
    def __init__(self,p,*,direct_cutoff=262144,max_degree=8192,max_direct_terms=2_000_000):
        if type(p) is not int or p<19 or not is_prime64(p) or p%5!=4:
            raise BoundaryError('require prime 19 <= p < 2**64 with p = 4 modulo 5')
        self.p,self.L,self.ell=p,(p+1)//5,(p+1)//10
        self.intervals=IntervalProductEvaluator(direct_cutoff,max_degree,max_direct_terms)

    def indices(self,indices=None):
        if indices is None: return (self.L,2*self.L)
        try: result=tuple(indices)
        except TypeError as exc: raise BoundaryError('indices must be an iterable of integers') from exc
        for n in result:
            if type(n) is not int or n not in (self.L,2*self.L):
                raise UnsupportedPrefixError('fifth-point indices must equal L or 2L')
        return result

    def validate_request(self,indices=None,*,backend='auto',modulus_power=1):
        if type(modulus_power) is not int or modulus_power!=1:
            raise BoundaryError('fifth-point reductions support modulo p only')
        wanted=self.indices(indices)
        if not isinstance(backend,str) or backend not in ('auto','direct','product_tree','bgs'):
            raise BoundaryError('unknown interval backend')
        return wanted

    def evaluate(self,indices=None,*,backend='auto',modulus_power=1):
        begin=perf_counter()
        wanted=self.validate_request(indices,backend=backend,modulus_power=modulus_power)
        if not wanted:
            return {'indices':[],'values':[],'unique_boundaries':0,'interval_calls':[],
                    'denominator_inversions':0,'normalization_seconds':0.0,
                    'total_seconds':perf_counter()-begin}
        p,L,ell=self.p,self.L,self.ell
        calls=[];products={}
        def acquire(start):
            # One evaluation per unique interval in this call, including the
            # denominator; there is no persistent arithmetic/answer cache.
            if start not in products:
                result=self.intervals.product(p,start,ell,backend)
                products[start]=result.value;calls.append(result)
            return products[start]
        denominator=acquire(1)
        unique=tuple(dict.fromkeys(wanted))
        numerators={}
        for n in unique:
            numerators[n]=acquire(3*ell if n==L else ell+1)
        norm_start=perf_counter()
        inverse=pow(denominator,-1,p)
        sign=-1 if ell%2 else 1
        values={}
        for n in unique:
            factor=pow(2,-2*L,p) if n==L else pow(2,2*L,p)*pow(16,-1,p)%p
            values[n]=sign*factor*numerators[n]*inverse%p
        normalization=perf_counter()-norm_start
        return {'indices':list(wanted),'values':[values[n] for n in wanted],
                'unique_boundaries':len(unique),'interval_calls':[asdict(c) for c in calls],
                'denominator_inversions':1,'shared_denominator':denominator,
                'normalization_seconds':normalization,'total_seconds':perf_counter()-begin,
                'proof_reference':'FIFTHS.md: retained boundary identities',
                'formula_first':'a_L = (-1)^ell * 2^(-2L) * binom(2L-1,ell) mod p',
                'formula_second':'a_(2L) = (-1)^ell * 2^(2L)/16 * binom(L,ell) mod p'}


class FifthPointSession:
    """Both fifth points, with one prefix pass and per-call shared boundaries."""
    def __init__(self,p,**boundary_options):
        begin=perf_counter()
        if not __debug__:
            raise BoundaryError('retained prefix kernels require assertion checks; run without -O')
        self.boundaries=FifthBoundaryEvaluator(p,**boundary_options)
        self.p,self.L,self.ell=p,self.boundaries.L,self.boundaries.ell
        self.setup_seconds=perf_counter()-begin

    def evaluate(self,indices=None,*,backend='auto',modulus_power=1,output_mode='full'):
        begin=perf_counter()
        if output_mode not in ('full','u_only'):
            raise BoundaryError('output_mode must be full or u_only')
        wanted=self.boundaries.validate_request(indices,backend=backend,modulus_power=modulus_power)
        skipped=tuple(dict.fromkeys(n for n in wanted if output_mode=='u_only' and 2*n*(2*n+5)%self.p==0))
        required=tuple(n for n in wanted if n not in skipped)
        boundary=self.boundaries.evaluate(required,backend=backend,modulus_power=modulus_power)
        boundary_values=dict(zip(boundary['indices'],boundary['values']))
        prefix_seconds=0.0;metadata=None;outputs=[]
        if wanted:
            pstart=perf_counter()
            try: metadata=prefixes(self.p,5,all_prefixes=True)
            except (ArithmeticError,AssertionError,ValueError) as exc:
                raise BoundaryError(f'retained genus-two prefix failed: {exc}') from exc
            prefix_seconds=perf_counter()-pstart
            if metadata['indices']!=[self.L,2*self.L] or len(metadata['B'])!=2:
                raise BoundaryError('retained genus-two prefix returned unexpected indices')
            by_index=dict(zip(metadata['indices'],metadata['B']))
            for n in wanted:
                a=boundary_values.get(n)
                B=by_index[n]
                if type(B) is not int or not 0<=B<self.p:
                    raise BoundaryError('retained prefix returned a noncanonical residue')
                multiplier=2*n*(2*n+5)%self.p
                row={'L':n,'B_L':B if output_mode=='full' else None,
                     'a_L':a if output_mode=='full' else None,
                     'U_p_L':(4*B-(0 if n in skipped else multiplier*a))%self.p,
                     'boundary_multiplier':multiplier}
                if output_mode=='u_only':
                    row['boundary_status']='skipped_zero_multiplier' if n in skipped else 'computed'
                outputs.append(row)
        if output_mode=='u_only':
            boundary['values']=[None for _ in boundary['values']]
            if metadata is not None:metadata={k:v for k,v in metadata.items() if k!='B'}
        warm=perf_counter()-begin
        return {'version':__version__,'p':self.p,'family':'paired_fifths',
                'base_index':self.L,'ell':self.ell,'requested_indices':list(wanted),
                'output_mode':output_mode,'skipped_boundary_indices':list(skipped),
                'computed_boundary_indices':list(dict.fromkeys(required)),
                'outputs':outputs,'prefix_passes':1 if wanted else 0,
                'prefix_seconds':prefix_seconds,'boundary_details':boundary,
                'retained_diagnostics':metadata,'session_setup_seconds':self.setup_seconds,
                'warm_total_seconds':warm,'cold_total_seconds':self.setup_seconds+warm,
                'answer_cache_used':False,
                'assurance':'retained_project_theorem; unrefereed; independently_tested',
                'scope':'modulo p; prefix plus interval boundary work; no new exponent saving'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--p',type=int,required=True)
    parser.add_argument('--which',choices=('both','first','second'),default='both')
    parser.add_argument('--backend',choices=('auto','direct','product_tree','bgs'),default='auto')
    parser.add_argument('--modulus-power',type=int,default=1)
    parser.add_argument('--max-degree',type=int,default=8192)
    parser.add_argument('--direct-cutoff',type=int,default=262144)
    parser.add_argument('--output-mode',choices=('full','u_only'),default='full')
    args=parser.parse_args(argv)
    try:
        if args.modulus_power!=1: raise BoundaryError('integrated fifths support modulo p only')
        session=FifthPointSession(args.p,max_degree=args.max_degree,direct_cutoff=args.direct_cutoff)
        wanted=None if args.which=='both' else [session.L if args.which=='first' else 2*session.L]
        print(json.dumps(session.evaluate(wanted,backend=args.backend,output_mode=args.output_mode),indent=2))
        return 0
    except BoundaryError as exc:
        print(json.dumps({'error':str(exc)}));return 2


if __name__=='__main__':raise SystemExit(main())
