"""Frozen confirmation, exact survey and matched end-to-end experiments."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import platform
import random
import statistics
import sys
from time import perf_counter

import bootstrap
from integrated import (evaluate, compact, full_tuple, forest_rows, acquire_boundary,
                        check_domain)
from oracles import direct, integer_binomial
from retained_cm import rounded_third_batch as forest
from boundary_framework import BoundaryError, is_prime64
from r3.common import flint_factorial
from r3.research.ledger_r31 import excluded as source_excluded
import independent_elliptic_prefix as independent

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'evidence'
CLASSES = {'A': (12,11), 'B': (24,5), 'C': (24,17)}
QS = [q for q in range(5,90) if is_prime64(q)]


def save(name, data):
    (EVIDENCE / name).write_text(json.dumps(data, indent=2, default=str)+'\n')


def verify_freeze():
    fr = json.loads((EVIDENCE / 'FREEZE.json').read_text())
    for name, digest in fr['sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != digest:
            raise AssertionError(('freeze mismatch', name))
    return fr


def excluded(p):
    if p < 20000 or source_excluded(p):
        return True
    if p in (20000000549,1000151,10000103,100000223):
        return True
    source = ROOT/'vendor/atkin_r3/r3/evidence'
    conf = json.loads((source/'CONFIRMATION_R3_1.json').read_text())
    old = {r['p'] for r in conf['cases']+conf.get('regression',[])}
    bench = json.loads((source/'BENCHMARK_R3_1.json').read_text())
    old.update(r['p'] for r in bench['rows'])
    return p in old


def first(bound, cls, condition):
    mo, residue = CLASSES[cls]
    p = bound + (residue-bound) % mo
    while not (condition(p) and is_prime64(p) and not excluded(p)):
        p += mo
    return p


def select_confirmation():
    jobs = []
    for cls in CLASSES:
        highq = {'A':23,'B':31,'C':47}[cls]
        for tier, bound, q in [('small',5000003,11),('medium',70000000,11),
                               ('large',7000000000,highq),('largest',700000000000,highq)]:
            p = first(bound, cls, lambda p,q=q:(p-1)%q==0)
            jobs.append(dict(tier=tier,p=p,cls=cls,q=q))
        p = first(7000000000,cls,lambda p:all((p-1)%q for q in QS))
        jobs.append(dict(tier='no_small_factor',p=p,cls=cls,q=None))
    p = first(7000000000,'C',lambda p:(p-1)%89==0)
    jobs.append(dict(tier='large_conductor',p=p,cls='C',q=89))
    p = first(7000000000000,'C',lambda p:(p-1)%47==0)
    jobs.append(dict(tier='extension',p=p,cls='C',q=47))
    return jobs


def identities(r):
    p,G,a,B,L=r['p'],r['G'],r['a_L'],r['B_L'],r['L']
    gi3=pow(G,-3,p)
    checks = dict(boundary=a==3*pow(2,-1,p)*gi3%p,
                  a_m=r['a_m']==-4*a%p,
                  B_m=r['B_m']==(B+4*a)%p,
                  U_L=r['U_p_L']==(4*B-17*pow(3,-1,p)*gi3)%p,
                  U_m=r['U_p_m']==(4*B-16*pow(3,-1,p)*gi3)%p,
                  difference=(r['U_p_L']-r['U_p_m'])%p==-pow(3,-1,p)*gi3%p,
                  original_multiplier=(2*L*(2*L+5))%p==34*pow(9,-1,p)%p,
                  unit_boundary=a!=0)
    if not all(checks.values()):
        raise AssertionError((p,checks))
    return checks


def confirm():
    verify_freeze()
    jobs=select_confirmation()
    cases=[]
    for job in jobs:
        p=job['p'];t=perf_counter()
        native=evaluate(p,'native')
        auto=evaluate(p)
        nodal=evaluate(p,'nodal')
        if not full_tuple(auto)==full_tuple(native)==full_tuple(nodal):
            raise AssertionError(('complete methods',p))
        if auto['B_L']!=independent.third(p)['B']:
            raise AssertionError(('independent elliptic Miller',p))
        if auto['G']!=native['boundary']['factorial_calls'][0]['value']:
            raise AssertionError(('native G',p))
        record=dict(**job,tuple=full_tuple(auto),identities=identities(auto),
                    route=auto['boundary_acquisition']['route'],selected_q=auto['boundary_acquisition']['q'],
                    independent_prefix=True)
        if job['q']:
            forced=evaluate(p,'t3',job['q'])
            if full_tuple(forced)!=full_tuple(auto):
                raise AssertionError(('forced T3',p,job['q']))
            record['forced_t3']=True
        if job['tier']=='small':
            d=direct(p)
            if compact(auto)!=tuple(d[k] for k in ('p','B_L','a_L','U_p_L')) or auto['U_p_m']!=d['U_p_m']:
                raise AssertionError(('original definitions',p))
            if auto['a_L']!=integer_binomial(p):
                raise AssertionError(('integer binomial',p))
            record['definition_level']=True
        record['seconds']=perf_counter()-t
        cases.append(record)
        print(json.dumps(record),flush=True)
    # A high-prime forest request is rejected before computing a long product.
    try:
        forest_rows([jobs[3]['p']])
    except BoundaryError:
        cap=True
    else:
        raise AssertionError('forest resource guard')
    out=dict(status='PASS',cases=cases,distinct_primes=len({r['p'] for r in cases}),
             forest_high_prime_resource_guard=cap,python=sys.version,platform=platform.platform())
    save('CONFIRMATION.json',out)
    verify_freeze()
    return out


def digest(rows):
    payload=''.join(','.join(map(str,row))+'\n' for row in rows)
    return hashlib.sha256(payload.encode()).hexdigest()


def dense_call(bound,method):
    if method.startswith('forest_'):
        rows=list(forest.iter_rows(bound,chunks=32,backend=method[7:]))
        return list(map(tuple,rows)),dict(route='forest_'+method[7:])
    rows=[evaluate(p,method) for p in forest.branch_primes(bound)]
    return [full_tuple(r) for r in rows],dict(routes=dict(Counter(r['boundary_acquisition']['route'] for r in rows)))


def benchmark():
    verify_freeze()
    conf=json.loads((EVIDENCE/'CONFIRMATION.json').read_text())
    if conf['status']!='PASS':raise AssertionError('confirmation required')
    import flint,gmpy2
    result=dict(python=sys.version,platform=platform.platform(),python_flint=flint.__version__,
                gmpy2=gmpy2.version(),samples=3,single=[],dense=[],sparse=[])
    for job in conf['cases']:
        if job['tier'] not in ('medium','large','largest','no_small_factor'):
            continue
        p=job['p'];methods=['native','nodal','auto'];samples={m:[] for m in methods};parts={m:[] for m in methods}
        expected=tuple(job['tuple'])
        for rep in range(3):
            for method in methods[rep:]+methods[:rep]:
                t=perf_counter();r=evaluate(p,method);seconds=perf_counter()-t
                samples[method].append(seconds)
                if full_tuple(r)!=expected:raise AssertionError(('single benchmark',p,method))
                parts[method].append(dict(prefix=r['prefix_seconds'],boundary=r['boundary_acquisition']['seconds'],
                                          route=r['boundary_acquisition']['route'],q=r['boundary_acquisition']['q']))
        row=dict(p=p,tier=job['tier'],cls=job['cls'],samples_s=samples,
                 medians_s={m:statistics.median(v) for m,v in samples.items()},parts=parts)
        result['single'].append(row);save('BENCHMARK_PARTIAL.json',result)
        print(json.dumps(dict(single=p,medians=row['medians_s'])),flush=True)
    for bound in (2000,20000,100000):
        methods=['native','auto','forest_python','forest_gmpy2'];samples={m:[] for m in methods};hashes=set();metadata={}
        for rep in range(3):
            for method in methods[rep:]+methods[:rep]:
                t=perf_counter();rows,md=dense_call(bound,method);h=digest(rows);seconds=perf_counter()-t
                samples[method].append(seconds);hashes.add(h);metadata[method]=md
        if len(hashes)!=1:raise AssertionError(('dense benchmark',bound))
        row=dict(bound_exclusive=bound,rows=len(rows),sha256=hashes.pop(),samples_s=samples,
                 medians_s={m:statistics.median(v) for m,v in samples.items()},metadata=metadata)
        result['dense'].append(row);save('BENCHMARK_PARTIAL.json',result)
        print(json.dumps(dict(dense=bound,medians=row['medians_s'])),flush=True)
    primes=[first(1000000+100000*j,list(CLASSES)[j%3],lambda p:(p-1)%5==0) for j in range(16)]
    methods=['native','auto','t3','forest_python','forest_gmpy2'];samples={m:[] for m in methods};hashes=set()
    for rep in range(3):
        for method in methods[rep:]+methods[:rep]:
            t=perf_counter()
            if method.startswith('forest_'):
                out,_=forest_rows(primes,chunks=32,integer_backend=method[7:]);rows=list(map(tuple,out))
            else:
                rows=[full_tuple(evaluate(p,method,5 if method=='t3' else None)) for p in primes]
            h=digest(rows);seconds=perf_counter()-t
            samples[method].append(seconds);hashes.add(h)
    if len(hashes)!=1:raise AssertionError('sparse schedule benchmark')
    result['sparse'].append(dict(primes=primes,rows=len(primes),sha256=hashes.pop(),samples_s=samples,
                                medians_s={m:statistics.median(v) for m,v in samples.items()}))
    result['status']='PASS';save('BENCHMARK.json',result)
    print(json.dumps(dict(sparse=result['sparse'][0]['medians_s'])),flush=True)
    return result


def survey():
    verify_freeze()
    t=perf_counter();rows=list(forest.iter_rows(1000000,chunks=32,backend='gmpy2'))
    residuals=Counter();zeros_L=[];zeros_m=[]
    for row in rows:
        p,B,a,U,G=row;g3=pow(G,-3,p)
        if a!=3*pow(2,-1,p)*g3%p or U!=(4*B-17*pow(3,-1,p)*g3)%p:
            raise AssertionError(('survey identity',p))
        Um=(4*B-16*pow(3,-1,p)*g3)%p
        if (U-Um)%p!=-pow(3,-1,p)*g3%p or a==0:
            raise AssertionError(('survey adjacent',p))
        if U==0:zeros_L.append(p)
        if Um==0:zeros_m.append(p)
    eligible=[r for r in rows if r.p>=20000]
    selected=random.Random(20261018).sample(eligible,64)
    verified=[]
    for row in [r for r in rows if r.p<20000]+selected:
        d=direct(row.p)
        if tuple(row[:4])!=tuple(d[k] for k in ('p','B_L','a_L','U_p_L')):
            raise AssertionError(('survey definition',row.p))
        if row.p>=20000:
            out=evaluate(row.p)
            if full_tuple(out)!=tuple(row):raise AssertionError(('survey adapter',row.p))
            if out['U_p_m']!=d['U_p_m']:raise AssertionError(('survey m definition',row.p))
            verified.append(row.p)
    with (EVIDENCE/'SURVEY.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(forest.HEADER);writer.writerows(rows)
    out=dict(status='PASS',bound_exclusive=1000000,rows=len(rows),tuple_sha256=digest(rows),
             identity_consistency_rows=len(rows),definition_rows_below_20000=sum(r.p<20000 for r in rows),
             definition_adapter_sample=verified,zeros_U_L=zeros_L,zeros_U_m=zeros_m,
             simultaneous_zeros=sorted(set(zeros_L)&set(zeros_m)),seconds=perf_counter()-t,
             role='New execution of a known-range exploratory survey, not fresh confirmation; identities alone are not independent checks')
    save('SURVEY.json',out);print(json.dumps(out),flush=True)
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('task',choices=('confirm','benchmark','survey'))
    task=parser.parse_args().task
    {'confirm':confirm,'benchmark':benchmark,'survey':survey}[task]()
