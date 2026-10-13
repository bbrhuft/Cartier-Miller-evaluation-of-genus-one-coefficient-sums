"""Focused complete-output comparison. No coefficient-only speedup ratios."""
from pathlib import Path
import csv,json,platform,statistics,sys,time,subprocess,tracemalloc,os,importlib.util
from cm_system.api import evaluate,Session,Budget,quarter_precision_diagnostics

ROOT=Path(__file__).resolve().parent
CASES=[
    {'case':'quarter_small','p':65537,'indices':[16384],'precision':1,'methods':['quarter','direct','product_tree']},
    {'case':'quarter_large','p':1048589,'indices':[262147],'precision':1,'methods':['quarter','direct','product_tree']},
    {'case':'ordinary_third','p':100003,'indices':[33334],'precision':1,'methods':['ordinary_third','direct','product_tree']},
    {'case':'fifth_both','p':1000039,'indices':[200008,400016],'precision':1,'methods':['higher:2','direct','product_tree']},
    {'case':'seventh_all','p':10009,'indices':[1430,2860,4290],'precision':1,'methods':['higher:3','direct','product_tree']},
    {'case':'generic','p':100003,'indices':[12345],'precision':1,'methods':['direct','product_tree']},
    {'case':'original_U_precision_two','p':1048589,'indices':[262147],'precision':2,'methods':['direct','product_tree']},
]


def calculation(case,method):
    s=Session(case['p'])
    return s.evaluate_many(case['indices'],case['precision'],method)


def original_reference(case):
    p=case['p'];q=p**case['precision'];h=(p-1)//2;t=1;u=0;out={}
    for i in range(max(case['indices'])+1):
        if i in case['indices']:out[i]=u
        if i<max(case['indices']):
            u=(u+(h+1+i)*t)%q
            t=t*(h+2+i)*pow(2*i+2,-1,q)%q
    return [out[i] for i in case['indices']]


def memory_worker(case,method):
    tracemalloc.start();result=calculation(case,method)
    _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    try:
        import resource
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss_bytes=int(rss if sys.platform=='darwin' else rss*1024)
    except ImportError:rss_bytes=None
    return {'case':case['case'],'method':method,'python_traced_peak_bytes':peak,
            'process_peak_RSS_bytes':rss_bytes,'outputs':[r['U'] for r in result],
            'scope':'fresh process; imports included in RSS, not tracemalloc; memory run outside timing'}


def main():
    ROOT.joinpath('results').mkdir(exist_ok=True)
    samples=[];rows=[];mem=[]
    for case in CASES:
        expected=original_reference(case);per={m:[] for m in case['methods']}
        for rep in range(5):
            order=case['methods'][rep%len(case['methods']):]+case['methods'][:rep%len(case['methods'])]
            for method in order:
                t=time.perf_counter_ns();out=calculation(case,method);seconds=(time.perf_counter_ns()-t)/1e9
                if [r['U'] for r in out]!=expected:raise AssertionError((case,method,out,expected))
                per[method].append(seconds)
                samples.append({**case,'method':method,'repetition':rep,'seconds':seconds,'outputs':expected})
        for method,values in per.items():
            rows.append({'case':case['case'],'p':case['p'],'indices':';'.join(map(str,case['indices'])),
                         'precision':case['precision'],'method':method,'median_ms':1000*statistics.median(values),
                         'minimum_ms':1000*min(values),'maximum_ms':1000*max(values),
                         'outputs':';'.join(map(str,expected)),'complete_setup':True})
        print(case['case'],'verified',flush=True)
    for case in [CASES[1],CASES[3],CASES[-1]]:
        for method in case['methods']:
            r=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--memory',json.dumps(case),method],cwd=ROOT,capture_output=True,text=True,check=True)
            mem.append(json.loads(r.stdout))
    # Repeated exact quarter query: intentionally cached result lookup, separate.
    s=Session(1048589);s.evaluate(262147,method='quarter');cached=[]
    for _ in range(5):
        t=time.perf_counter_ns();z=s.evaluate(262147,method='quarter');cached.append((time.perf_counter_ns()-t)/1e9)
        if not z['cache_reused']:raise AssertionError('cache flag lost')
    cold=[]
    for _ in range(3):
        t=time.perf_counter_ns()
        r=subprocess.run([sys.executable,'-m','cm_system','sum','1048589','262147','--method','quarter'],cwd=ROOT,capture_output=True,text=True,check=True)
        cold.append((time.perf_counter_ns()-t)/1e9)
        if json.loads(r.stdout)['U']!=evaluate(1048589,262147,method='quarter')['U']:raise AssertionError('process result')
    env={'python':sys.version,'platform':platform.platform(),'cpu_count':os.cpu_count(),
         'backend':__import__('cm_system.backends.product_tree',fromlist=['PZ']).PZ.BACKEND,
         'flint_available':importlib.util.find_spec('flint') is not None,'timer':'perf_counter_ns','repeats':5,
         'timing_contract':'fresh Session each complete query; imports and serialization excluded; prime validation included',
         'multi_output_contract':'one shared direct pass; one shared higher-genus pass; independent original-U product tree per index',
         'affinity':'not pinned; no portable crossover inferred'}
    out={'environment':env,'cases':CASES,'samples':samples,'summaries':rows,'memory':mem,
         'cached_quarter_lookup_seconds':cached,'fresh_process_quarter_seconds':cold,
         'cached_scope':'exact repeated-answer cache; not a distinct-input arithmetic speedup'}
    (ROOT/'results/benchmarks.json').write_text(json.dumps(out,indent=2)+'\n')
    with (ROOT/'results/benchmarks.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps(rows,indent=2))


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--memory':print(json.dumps(memory_worker(json.loads(sys.argv[2]),sys.argv[3])))
    else:main()
