"""Complete paired-fifth benchmarks with shared direct and generic baselines."""
import argparse
import csv
import json
from pathlib import Path
import platform
from statistics import median
import sys
from time import perf_counter

from boundary_framework import BoundaryEvaluator, __version__
from integrated_fifths import FifthPointSession
from retained_cm.hyperelliptic_prefix import prefixes
from test_boundary_framework import original_sum_oracle


def original_pair_shared(p,indices):
    """One pass of the original rational t recurrence for both requested U."""
    h=(p-1)//2;T,S,D=1,0,1;out={};wanted=set(indices)
    for i in range(max(indices)):
        factor=2*(i+1)%p
        T,S,D=T*(h+2+i)%p,(S+(h+1+i)*T)*factor%p,D*factor%p
        if i+1 in wanted:out[i+1]=S*pow(D,-1,p)%p
    return [out[n] for n in indices]


def generic_boundaries_shared(p):
    """One prefix pass, three unique factorials across the two generic ratios.

    This comparator shares (2L)! instead of running two unshared evaluators.
    Its factorials use the normal dispatcher and Wilson reflection.
    """
    session=FifthPointSession(p)  # Same validated domain and setup charge.
    L=session.L;engine=BoundaryEvaluator();facts={}
    for n in (L,2*L,4*L):
        effective=min(n,p-1-n)
        backend='direct' if effective<=engine.direct_cutoff else 'bgs'
        facts[n]=engine.backends[backend].factorial(n,p).value
    boundaries=[facts[2*L]*pow(facts[L],-2,p)*pow(8,-L,p)%p,
                facts[4*L]*pow(facts[2*L],-2,p)*pow(8,-2*L,p)%p]
    B=prefixes(p,5,True)['B']
    return [(4*b-2*n*(2*n+5)*a)%p for n,b,a in zip((L,2*L),B,boundaries)]


def run(repeats=3,output=Path('results')):
    output.mkdir(exist_ok=True,parents=True);rows=[]
    for p in (10009,100019,1000039,4000039,10000019):
        L=(p+1)//5;indices=(L,2*L);expected=original_pair_shared(p,indices)
        if p<=100019:
            if expected!=[original_sum_oracle(p,n) for n in indices]:
                raise RuntimeError('shared original recurrence baseline failed')
        for mode in ('paired_auto','paired_product_tree','separate_auto','shared_generic_auto','direct_original_shared'):
            group=[]
            for repeat in range(repeats):
                begin=perf_counter();interval_count=None;prefix_passes=None
                if mode in ('paired_auto','paired_product_tree'):
                    r=FifthPointSession(p).evaluate(backend='product_tree' if mode=='paired_product_tree' else 'auto')
                    values=[row['U_p_L'] for row in r['outputs']]
                    interval_count=len(r['boundary_details']['interval_calls']);prefix_passes=r['prefix_passes']
                elif mode=='separate_auto':
                    values=[];interval_count=0;prefix_passes=0
                    for n in indices:
                        r=FifthPointSession(p).evaluate([n])
                        values.append(r['outputs'][0]['U_p_L'])
                        interval_count+=len(r['boundary_details']['interval_calls']);prefix_passes+=r['prefix_passes']
                elif mode=='shared_generic_auto':
                    values=generic_boundaries_shared(p);prefix_passes=1
                else:values=original_pair_shared(p,indices)
                wall=perf_counter()-begin
                if values!=expected:raise RuntimeError(f'fifth benchmark mismatch {(p,mode,values,expected)}')
                group.append({'p':p,'L':L,'second_index':2*L,'mode':mode,'repeat':repeat,
                              'U_first':values[0],'U_second':values[1],'correct':True,
                              'wall_ms':wall*1000,'interval_products':interval_count,
                              'prefix_passes':prefix_passes,'answer_cache_used':False})
            rows.extend(group)
            print(f'p={p} {mode}: {median(r["wall_ms"] for r in group):.3f} ms',flush=True)
    with (output/'fifth_benchmark.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    groups=[]
    for i in range(0,len(rows),repeats):
        group=rows[i:i+repeats]
        groups.append({**{key:group[0][key] for key in ('p','L','second_index','mode')},
                       'median_wall_ms':median(r['wall_ms'] for r in group)})
    record={'version':__version__,'python':sys.version,'platform':platform.platform(),
            'repeats':repeats,'timed_evaluations':len(rows),'all_correct':True,
            'scope':'Complete U pair. Cold preparation, boundary acquisition and prefix work included; imports, serialization and prime selection excluded. No persistent answer cache.',
            'references':'Shared original-t recurrence baseline for both outputs; checked against unscaled t recurrence at smaller benchmark primes.',
            'sharing':'Paired: one d=5 all-prefix pass, three intervals and one denominator inverse. Separate: two all-prefix passes, four intervals. Generic comparator: one prefix pass and three unique factorials, sharing (2L)!. Direct baseline: one original-sum pass. Native prefix routine computes both prefixes even for a single selected output.',
            'medians':groups}
    (output/'fifth_benchmark_summary.json').write_text(json.dumps(record,indent=2)+'\n')
    return record


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats',type=int,default=3)
    parser.add_argument('--output',type=Path,default=Path('results'))
    args=parser.parse_args()
    if args.repeats<1:parser.error('--repeats must be positive')
    run(args.repeats,args.output)
