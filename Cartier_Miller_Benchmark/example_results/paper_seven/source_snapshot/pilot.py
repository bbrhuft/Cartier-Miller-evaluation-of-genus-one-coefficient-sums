# SPDX-License-Identifier: GPL-2.0-or-later
"""Validate the unchanged Harvey kernel and run a deliberately small pilot.

Python standard library only. Timings compare compiled Harvey to archived Python
Miller; they are pilot measurements, not a controlled implementation contest.
"""
import argparse
import csv
import sys
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import random
import statistics
import subprocess
import time
from elliptic_prefix import quarter

ROOT = Path(__file__).resolve().parent

def is_prime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n == p: return True
        if n % p == 0: return False
    d=n-1;s=0
    while d%2==0: d//=2;s+=1
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        if a%n==0: continue
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

def original_values(p):
    """The original t_i, U recurrence, independently of the telescoping formula."""
    h=(p-1)//2;t=1;U=0;values=[0]
    for i in range(h):
        U=(U+(h+1+i)*t)%p;values.append(U)
        t=t*(h+2+i)*pow(2*i+2,-1,p)%p
    return values

def prefix_values(p):
    h=(p-1)//2;a=1;B=0;D=1;values=[]
    for L in range(h+1):
        values.append({'a':a,'B':B,'A':a*D%p,'C':B*D%p,'D':D})
        if L<h:
            B=(B+a)%p
            a=a*(2*L+1)*pow(4*(L+1),-1,p)%p
            D=D*4*(L+1)%p
    return values

def env_for_kernel():
    e=os.environ.copy()
    local=ROOT/'deps/root/usr/lib/x86_64-linux-gnu'
    if local.exists():e['LD_LIBRARY_PATH']=str(local)+os.pathsep+e.get('LD_LIBRARY_PATH','')
    e['OMP_NUM_THREADS']='1';e['OPENBLAS_NUM_THREADS']='1'
    return e

def call_kernel(exe,cases,force_big=False):
    cmd=[str(exe)]+(['--force-big'] if force_big else [])
    text=''.join(f'{p} {L} {reps}\n' for p,L,reps in cases)
    r=subprocess.run(cmd,input=text,text=True,capture_output=True,
                     env=env_for_kernel(),timeout=180,check=True)
    rows=[json.loads(line) for line in r.stdout.splitlines()]
    if len(rows)!=len(cases):raise RuntimeError('wrong output length')
    return rows

class HarveyWorker:
    """A persistent child: no process startup inside or between timed samples."""
    def __init__(self,exe):
        self.process=subprocess.Popen([str(exe)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,text=True,bufsize=1,env=env_for_kernel())
    def query(self,p,L,reps):
        self.process.stdin.write(f'{p} {L} {reps}\n');self.process.stdin.flush()
        line=self.process.stdout.readline()
        if not line:
            raise RuntimeError('Harvey child failed: '+self.process.stderr.read())
        return json.loads(line)
    def close(self):
        self.process.stdin.close()
        code=self.process.wait(timeout=30)
        if code:raise RuntimeError(self.process.stderr.read())

def validate(exe):
    refs={};cases=[];checks={'all_stopping_indices':0,'exact_binomial_checks':0,
                           'miller_cross_checks':0,'forced_big_cross_checks':0,
                           'large_modulus_checks':0}
    for p in range(7,500):
        if not is_prime(p):continue
        direct=original_values(p);prefix=prefix_values(p)
        for L,ref in enumerate(prefix):
            ref={**ref,'U':direct[L]};refs[p,L]=ref;cases.append((p,L,1))
            if p<=199:
                a=math.comb(2*L,L)*pow(pow(8,L,p),-1,p)%p
                assert ref['a']==a
                checks['exact_binomial_checks']+=1
    rows=call_kernel(exe,cases)
    for z in rows:
        ref=refs[z['p'],z['L']]
        for k in ('a','B','U','A','C','D'):assert z[k]==ref[k],(z,k,ref)
        checks['all_stopping_indices']+=1
    # Noncommutative order check: M(1)M(2), not M(2)M(1).
    z=call_kernel(exe,[(97,2,1)])[0]
    assert (z['A'],z['C'],z['D'])==(3,40,32)
    # Quarter results must also match the archived elliptic evaluator.
    qcases=[(p,(p-1)//4,1) for p in range(13,5000) if p%4==1 and is_prime(p)]
    qr=call_kernel(exe,qcases)
    for z in qr:
        m=quarter(z['p'])
        assert all(m[k]==z[k] for k in ('a','B','U')),(z,m)
        checks['miller_cross_checks']+=1
    selected=qcases[::max(1,len(qcases)//25)]
    for z in call_kernel(exe,selected,force_big=True):
        m=quarter(z['p'])
        assert all(m[k]==z[k] for k in ('a','B','U'))
        checks['forced_big_cross_checks']+=1
    # Exercise the automatic arbitrary-precision path at cheap small indices.
    large=(1<<61)-1
    assert is_prime(large)
    prefix=prefix_values_small(large,64);direct=original_values_small(large,64)
    for z in call_kernel(exe,[(large,L,1) for L in (0,1,2,7,16,31,64)]):
        assert z['backend']=='ZZ_p_auto',z['backend']
        ref=prefix[z['L']]
        assert all(z[k]==ref[k] for k in ('a','B','A','C','D'))
        assert z['U']==direct[z['L']]
        checks['large_modulus_checks']+=1
    for bad in ('15 3 1\n','97 49 1\n','97 -1 1\n'):
        r=subprocess.run([str(exe)],input=bad,text=True,capture_output=True,env=env_for_kernel())
        assert r.returncode!=0
    checks['invalid_input_checks']=3
    checks['multiplication_order_check']='passed'
    checks['primes_all_indices']=sum(is_prime(p) for p in range(7,500))
    checks['status']='passed'
    return checks

def prefix_values_small(p,last):
    a=1;B=0;D=1;out=[]
    for L in range(last+1):
        out.append({'a':a,'B':B,'A':a*D%p,'C':B*D%p,'D':D})
        B=(B+a)%p;a=a*(2*L+1)*pow(4*(L+1),-1,p)%p;D=D*4*(L+1)%p
    return out

def original_values_small(p,last):
    h=(p-1)//2;t=1;U=0;out=[0]
    for i in range(last):
        U=(U+(h+1+i)*t)%p;out.append(U)
        t=t*(h+2+i)*pow(2*i+2,-1,p)%p
    return out

def benchmark(exe,reps,on_row=None):
    primes=[97,1009,10009,100049,1000033,10000121,100000037]
    # Warm code once; subsequent calls still recreate all per-input state.
    worker=HarveyWorker(exe)
    worker.query(97,24,1);quarter(97)
    rows=[]
    for p in primes:
        assert is_prime(p) and p%4==1
        L=(p-1)//4;m_samples=[];b_samples=[];values=[]
        initial=worker.query(p,L,1)
        t=time.perf_counter_ns();quarter(p);estimate=(time.perf_counter_ns()-t)/1e6
        m_batch=max(1,min(2000,math.ceil(25/max(estimate,.001))))
        b_batch=max(1,min(2000,math.ceil(25/max(initial['samples'][0]['total_ms'],.001))))
        for rep in range(reps):
            def miller():
                t=time.perf_counter_ns()
                for _ in range(m_batch):z=quarter(p)
                m_samples.append((time.perf_counter_ns()-t)/1e6/m_batch);return z
            def harvey():
                z=worker.query(p,L,b_batch)
                b_samples.append({k:statistics.mean(s[k] for s in z['samples'])
                     for k in ('setup_ms','kernel_ms','finish_ms','total_ms')})
                b_samples[-1]['individual_call_samples']=z['samples']
                return z
            if rep%2==0:m=miller();b=harvey()
            else:b=harvey();m=miller()
            assert all(m[k]==b[k] for k in ('a','B','U')),(p,m,b)
            values.append({k:m[k] for k in ('B','a','U')})
        row={'p':p,'L':L,**values[-1],'harvey_backend':b['backend'],
             'miller_calls_per_sample':m_batch,'harvey_calls_per_sample':b_batch,
             'miller_python_samples_ms':m_samples,'harvey_cpp_samples':b_samples,
             'miller_python_median_ms':statistics.median(m_samples),
             'harvey_cpp_median_ms':statistics.median(x['total_ms'] for x in b_samples)}
        rows.append(row)
        if on_row is not None: on_row(row)
        print(f"p={p}: Python Miller {row['miller_python_median_ms']:.4f} ms; Harvey C++ {row['harvey_cpp_median_ms']:.4f} ms",flush=True)
    worker.close()
    return {'repetitions':reps,'target_sample_duration_ms':25,'rows':rows,
       'scope':'Complete B,a,U; prime validation, process startup and IPC excluded. Harvey includes NTL context/model setup; Miller includes Cornacchia/trace/boundary preparation.',
       'limitation':'Pilot: compiled Harvey versus archived Python Miller, warmed persistent processes, duration-calibrated batches. Seven primes only; no population-level speedup claim. Both recreate per-call matrices or elliptic data; library-global tables may remain warm.',
       'memory':'Not measured in this timing pilot.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--executable',type=Path,default=ROOT/'bin'/('harvey_adapter.exe' if os.name=='nt' else 'harvey_adapter'))
    ap.add_argument('--repetitions',type=int,default=11);ap.add_argument('--validate-only',action='store_true')
    ap.add_argument('--output',type=Path,default=ROOT/'results/benchmark.json');args=ap.parse_args()
    if not 1<=args.repetitions<=100:ap.error('repetitions must be 1..100')
    version=json.loads(subprocess.check_output([str(args.executable),'--version'],text=True,env=env_for_kernel()))
    start=time.time();checks=validate(args.executable)
    print(json.dumps(checks),flush=True)
    result={'utc_started':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(start)),
       'platform':platform.platform(),'python':platform.python_version(),'python_executable':sys.executable,'cpu':cpu_name(),
       'machine':platform.machine(),'processor_count':os.cpu_count(),
       'environment':{k:os.environ.get(k) for k in ('MSYSTEM','WSL_DISTRO_NAME','NTL_NUM_THREADS','OMP_NUM_THREADS')},
       'kernel_version':version,'upstream':json.loads((ROOT/'upstream/SOURCE_PROVENANCE.json').read_text()),
       'validation':checks,'adapter_sha256':hashlib.sha256((ROOT/'harvey_adapter.cpp').read_bytes()).hexdigest(),
       'miller_source_sha256':hashlib.sha256((ROOT/'elliptic_prefix.py').read_bytes()).hexdigest()}
    if not args.validate_only:
        exporter=CSVExporter(args.output.parent)
        result['benchmark']=benchmark(args.executable,args.repetitions,exporter.write_row)
        result['csv_files']=[str(exporter.summary),str(exporter.samples)]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('Saved '+str(args.output),flush=True)

class CSVExporter:
    """Flush after each completed prime, so interrupted runs retain completed rows."""
    def __init__(self, directory):
        directory.mkdir(parents=True,exist_ok=True)
        self.summary=directory/'summary.csv'
        self.samples=directory/'samples.csv'
        self.fields=['p','L','B_mod_p','a_L_mod_p','U_mod_p','validation',
            'repetitions','miller_python_median_ms','miller_python_min_ms','miller_python_max_ms',
            'harvey_cpp_median_ms','harvey_cpp_min_ms','harvey_cpp_max_ms',
            'harvey_setup_median_ms','harvey_kernel_median_ms','harvey_finish_median_ms',
            'harvey_over_miller_time_ratio','miller_calls_per_sample','harvey_calls_per_sample','harvey_backend']
        self.sample_fields=['p','L','method','sample_number','batch_size','mean_ms_per_call',
            'setup_ms_per_call','kernel_ms_per_call','finish_ms_per_call']
        for path,fields in ((self.summary,self.fields),(self.samples,self.sample_fields)):
            with path.open('w',newline='',encoding='utf-8-sig') as f:
                csv.DictWriter(f,fieldnames=fields).writeheader()
    def write_row(self,r):
        m=r['miller_python_samples_ms']; b=r['harvey_cpp_samples']; totals=[x['total_ms'] for x in b]
        row={'p':r['p'],'L':r['L'],'B_mod_p':r['B'],'a_L_mod_p':r['a'],'U_mod_p':r['U'],
            'validation':'PASS','repetitions':len(m),
            'miller_python_median_ms':statistics.median(m),'miller_python_min_ms':min(m),'miller_python_max_ms':max(m),
            'harvey_cpp_median_ms':statistics.median(totals),'harvey_cpp_min_ms':min(totals),'harvey_cpp_max_ms':max(totals),
            'harvey_over_miller_time_ratio':statistics.median(totals)/statistics.median(m),
            **{f'harvey_{k}_median_ms':statistics.median(x[f'{k}_ms'] for x in b) for k in ('setup','kernel','finish')},
            **{k:r[k] for k in ('miller_calls_per_sample','harvey_calls_per_sample','harvey_backend')}}
        with self.summary.open('a',newline='',encoding='utf-8') as f:
            csv.DictWriter(f,fieldnames=self.fields).writerow(row)
        with self.samples.open('a',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=self.sample_fields)
            for i,(mv,bv) in enumerate(zip(m,b),1):
                common={'p':r['p'],'L':r['L'],'sample_number':i}
                w.writerow({**common,'method':'Cartier-Miller Python','batch_size':r['miller_calls_per_sample'],'mean_ms_per_call':mv})
                w.writerow({**common,'method':'Harvey BGS C++','batch_size':r['harvey_calls_per_sample'],'mean_ms_per_call':bv['total_ms'],
                    **{f'{k}_ms_per_call':bv[f'{k}_ms'] for k in ('setup','kernel','finish')}})
        print('CSV updated: '+str(self.summary),flush=True)

def cpu_name():
    p=Path('/proc/cpuinfo')
    if p.exists():
        for line in p.read_text().splitlines():
            if line.startswith('model name'):return line.split(':',1)[1].strip()
    return platform.processor()

if __name__=='__main__':main()
