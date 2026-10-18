"""Matched complete-U benchmarks, including real prefix preparation."""
import argparse
import csv
import json
from pathlib import Path
import platform
from statistics import median
import sys
from time import perf_counter

from integrated_thirds import ThirdPointSession
from boundary_framework import __version__
from test_boundary_framework import original_sum_oracle


def original_sum_scaled(p,L):
    """Original rational recurrence, with D_i=2**i*i! cleared each step."""
    h=(p-1)//2
    T,S,D=1,0,1
    for i in range(L):
        factor=2*(i+1)%p
        T,S,D=(T*(h+2+i)%p,
               (S+(h+1+i)*T)*factor%p,
               D*factor%p)
    return S*pow(D,-1,p)%p


def run(repeats=3, output=Path('results')):
    output.mkdir(exist_ok=True,parents=True)
    rows=[]
    for p in (10007,20021,100003,100019,1000003,1000037,4000037,4000039):
        L=(p-1)//3 if p%3==1 else (p+1)//3
        expected=original_sum_scaled(p,L)
        # A second, unscaled original-t oracle controls the baseline at all
        # smaller benchmark primes. Larger cases use the scaled original sum.
        if p <= 100019 and expected!=original_sum_oracle(p,L):
            raise RuntimeError('scaled original-sum benchmark oracle failed')
        for mode in ('cold_auto','warm_auto','cold_factorial','original_direct_scaled'):
            prepared=ThirdPointSession(p) if mode=='warm_auto' else None
            samples=[]
            for repeat in range(repeats):
                start=perf_counter()
                if mode=='original_direct_scaled':
                    value=original_sum_scaled(p,L)
                    result=None
                else:
                    session=prepared if prepared is not None else ThirdPointSession(p)
                    result=session.evaluate(boundary_policy='factorial' if mode=='cold_factorial' else 'auto')
                    value=result['U_p_L']
                wall=perf_counter()-start
                if value!=expected:
                    raise RuntimeError(f'integrated mismatch {(p,L,mode,value,expected)}')
                samples.append({'p':p,'L':L,'family':'ordinary_third' if p%3==1 else 'rounded_third',
                                'mode':mode,'repeat':repeat,'U_p_L':value,'correct':True,
                                'wall_ms':wall*1000,
                                'session_setup_ms':(result['session_setup_seconds']*1000 if result and mode!='warm_auto' else 0),
                                'prior_session_setup_ms':(result['session_setup_seconds']*1000 if result and mode=='warm_auto' else 0),
                                'prefix_ms':result['prefix_seconds']*1000 if result else None,
                                'boundary_ms':result['boundary']['total_seconds']*1000 if result else None,
                                'factorial_calls':len(result['boundary']['factorial_calls']) if result else None,
                                'answer_cache_used':False})
            rows.extend(samples)
            print(f'p={p} {mode}: {median(s["wall_ms"] for s in samples):.3f} ms',flush=True)
    with (output/'integrated_benchmark.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    medians=[]
    for i in range(0,len(rows),repeats):
        samples=rows[i:i+repeats]
        medians.append({**{k:samples[0][k] for k in ('p','L','family','mode')},
                        'median_wall_ms':median(s['wall_ms'] for s in samples),
                        'median_prefix_ms':(median(s['prefix_ms'] for s in samples) if samples[0]['prefix_ms'] is not None else None)})
    metadata={'version':__version__,'python':sys.version,'platform':platform.platform(),
              'repeats':repeats,'timed_evaluations':len(rows),'all_correct':True,
              'scope':'Complete U output. Cold modes include session preparation and boundary acquisition. Warm mode excludes previously recorded preparation but reruns Miller and boundary arithmetic; no answer cache. Imports, serialization and prime selection excluded.',
              'reference':'Original t recurrence with denominators cleared, additionally checked against the unscaled original recurrence at p <= 100019. Baseline returns U only; integrated modes also compute B and a diagnostics.',
              'medians':medians}
    (output/'integrated_benchmark_summary.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return metadata


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats',type=int,default=3)
    parser.add_argument('--output',type=Path,default=Path('results'))
    args=parser.parse_args()
    if args.repeats<1:parser.error('--repeats must be positive')
    run(args.repeats,args.output)
