# SPDX-License-Identifier: GPL-2.0-or-later
"""Spawn-isolated benchmark jobs, cancellable deadlines, incremental exports."""
import csv
import datetime as dt
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
import platform
import statistics
import subprocess
import time
from elliptic_prefix import quarter, cornacchia_quarter
from point_count import schoof_trace, bsgs_trace
from pilot import is_prime, HarveyWorker, env_for_kernel, cpu_name

ROOT=Path(__file__).resolve().parent
PAPER_PRIMES=[97,1009,10009,100049,1000033,10000121,100000037]
LIMIT=2**63-1
METHODS={'cornacchia':'CM / Cornacchia–Gauss (Python)',
         'schoof':'CM / deterministic Schoof (Python)',
         'bsgs':'CM / certified point-count BSGS (Python)',
         'harvey':'Harvey BGS recurrence (C++)'}
FIELDS=['p','L','backend','method','status','B_mod_p','a_L_mod_p','U_mod_p','trace',
        'validation','repetitions','prep_median_ms','query_median_ms','total_median_ms',
        'total_min_ms','total_max_ms','setup_median_ms','kernel_median_ms','finish_median_ms','message']
SAMPLE_FIELDS=['p','backend','component','sample','batch_size','mean_ms_per_call']


def next_quarter_prime(n):
    n=max(13,int(n));n+=(1-n)%4
    while n<=LIMIT:
        if is_prime(n):return n
        n+=4
    raise ValueError('No supported prime at or above this target (<2^63 required).')


def make_primes(mode='paper',count=7,start='97',factor='10',custom=''):
    if not 1<=int(count)<=500:raise ValueError('Point count must be 1..500.')
    count=int(count)
    if mode=='custom':
        vals=[int(x) for x in custom.replace(',',' ').split()]
        if not vals:raise ValueError('Enter at least one prime.')
        if len(vals)>500 or len(vals)!=len(set(vals)):raise ValueError('Use at most 500 distinct primes.')
        vals=sorted(vals)
    elif mode=='paper':
        vals=PAPER_PRIMES[:count]
        # Extension targets 10^9, 10^10, ...; select first prime 1 mod 4 >= target.
        target=10**9
        while len(vals)<count:
            vals.append(next_quarter_prime(target));target*=10
    else:
        try:s=Decimal(start);f=Decimal(factor)
        except InvalidOperation:raise ValueError('Invalid grid start or factor.')
        if not s.is_finite() or not f.is_finite() or s<13 or f<=1:raise ValueError('Grid start >=13 and factor >1 required.')
        vals=[];target=s
        for _ in range(count):
            if target>LIMIT:raise ValueError('Generated target exceeds the supported 63-bit range.')
            p=next_quarter_prime(int(target.to_integral_value(rounding='ROUND_CEILING')))
            if not vals or p>vals[-1]:vals.append(p)
            else:raise ValueError('Grid gives duplicate primes; increase the spacing.')
            target*=f
    for p in vals:
        if p>LIMIT or p<13 or p%4!=1 or not is_prime(p):
            raise ValueError(f'{p} is not an admissible prime: require 13 <= p < 2^63 and p ≡ 1 mod 4.')
    return vals


def prepare(p,backend):
    if backend=='schoof':return schoof_trace(p)
    if backend=='bsgs':return bsgs_trace(p)
    r,_,_=cornacchia_quarter(p)
    h=2*r*pow(pow(8,(p-1)//4,p),-1,p)%p
    return h if h%2==0 else h-p


def measure(fn,repeats,target_ms):
    start=time.perf_counter_ns();last=fn();estimate=(time.perf_counter_ns()-start)/1e6
    batch=max(1,min(2000,math.ceil(target_ms/max(estimate,.001))))
    out=[]
    for _ in range(repeats):
        start=time.perf_counter_ns()
        for __ in range(batch):last=fn()
        out.append((time.perf_counter_ns()-start)/1e6/batch)
    return last,out,batch


def computation_job(connection,p,backend,settings):
    try:
        repeats=settings['repetitions'];target=settings['target_ms']
        # Correctness/reference work excluded from timings, explicitly CM classical path.
        ref=quarter(p)
        row={'p':p,'L':(p-1)//4,'backend':backend,'method':METHODS[backend],
             'status':'ok','B_mod_p':ref['B'],'a_L_mod_p':ref['a'],'U_mod_p':ref['U'],
             'trace':ref['trace'],'validation':'cross-checked','repetitions':repeats,'message':''}
        samples=[]
        if backend=='harvey':
            worker=HarveyWorker(Path(settings['executable']))
            marker=Path(settings['output'])/f'child_{os.getpid()}.pid'
            marker.write_text(str(worker.process.pid))
            try:
                first=worker.query(p,row['L'],1)
                batch=max(1,min(2000,math.ceil(target/max(first['samples'][0]['total_ms'],.001))))
                data=[]
                for _ in range(repeats):
                    z=worker.query(p,row['L'],batch)
                    if any(z[k]!=ref[k] for k in ('a','B','U')):raise ArithmeticError('Harvey/Miller answer mismatch')
                    data.append({k:statistics.mean(v[k] for v in z['samples']) for k in ('total_ms','setup_ms','kernel_ms','finish_ms')})
                totals=[v['total_ms'] for v in data]
                for component in ('setup','kernel','finish'):
                    row[component+'_median_ms']=statistics.median(v[component+'_ms'] for v in data)
                samples=[{'p':p,'backend':backend,'component':'total','sample':i+1,'batch_size':batch,'mean_ms_per_call':v} for i,v in enumerate(totals)]
            finally:
                worker.close();marker.unlink(missing_ok=True)
        else:
            trace,preps,pbatch=measure(lambda:prepare(p,backend),repeats,target)
            if trace!=ref['trace']:raise ArithmeticError('Point-count trace mismatch')
            q,queries,qbatch=measure(lambda:quarter(p,trace=trace),repeats,target)
            complete=(lambda:quarter(p)) if backend=='cornacchia' else (lambda:quarter(p,trace=prepare(p,backend)))
            z,totals,tbatch=measure(complete,repeats,target)
            for value in (q,z):
                if any(value[k]!=ref[k] for k in ('a','B','U')):raise ArithmeticError('Complete answer mismatch')
            row.update(prep_median_ms=statistics.median(preps),query_median_ms=statistics.median(queries))
            for component,values,batch in (('preparation',preps,pbatch),('prepared_query',queries,qbatch),('total',totals,tbatch)):
                samples.extend({'p':p,'backend':backend,'component':component,'sample':i+1,'batch_size':batch,'mean_ms_per_call':v} for i,v in enumerate(values))
        row.update(total_median_ms=statistics.median(totals),total_min_ms=min(totals),total_max_ms=max(totals))
        connection.send({'row':row,'samples':samples})
    except Exception as e:
        connection.send({'row':{'p':p,'L':(p-1)//4,'backend':backend,'method':METHODS[backend],
                              'status':'error','validation':'failed','message':f'{type(e).__name__}: {e}'},'samples':[]})
    finally:connection.close()


def isolated_job(p,backend,settings,cancel):
    ctx=mp.get_context('spawn');parent,child=ctx.Pipe(False)
    process=ctx.Process(target=computation_job,args=(child,p,backend,settings),daemon=False)
    process.start();child.close();start=time.monotonic()
    try:
        while True:
            if parent.poll(.1):return parent.recv()
            if cancel.is_set():status='cancelled';break
            if time.monotonic()-start>settings['timeout']:status='timeout';break
            if not process.is_alive():status='error';break
        return {'row':{'p':p,'L':(p-1)//4,'backend':backend,'method':METHODS[backend],
                       'status':status,'message':f'{status}; no timing/result reported'},'samples':[]}
    finally:
        # Kill the entire child tree (including a Harvey adapter) after a deadline.
        if process.is_alive():
            if os.name=='nt':subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            else:
                # Harvey is in a new session; job owns its PID via a small marker.
                marker=Path(settings['output'])/f'child_{process.pid}.pid'
                if marker.exists():
                    try:os.kill(int(marker.read_text()),9)
                    except (OSError,ValueError):pass
                process.terminate()
                marker.unlink(missing_ok=True)
        process.join(5);parent.close()
        (Path(settings['output'])/f'child_{process.pid}.pid').unlink(missing_ok=True)


def write_csv(path,fields,rows):
    temp=path.with_suffix(path.suffix+'.tmp')
    with temp.open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    temp.replace(path)


def save_outputs(directory,rows,samples,metadata):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    write_csv(directory/'summary.csv',FIELDS,rows)
    write_csv(directory/'samples.csv',SAMPLE_FIELDS,samples)
    wide=[]
    for p in sorted({r['p'] for r in rows}):
        wr={'p':str(p),'L':str((p-1)//4)}
        for r in rows:
            if r['p']==p:
                backend=r['backend'];wr[backend+'_status']=r['status']
                wr[backend+'_total_ms']=r.get('total_median_ms','')
                if backend!='harvey':
                    wr[backend+'_prep_ms']=r.get('prep_median_ms','');wr[backend+'_query_ms']=r.get('query_median_ms','')
                if r['status']=='ok':
                    for k in ('B_mod_p','a_L_mod_p','U_mod_p'):wr[k]=str(r[k])
        wide.append(wr)
    fields=['p','L','B_mod_p','a_L_mod_p','U_mod_p']
    for b in METHODS:
        fields+=[b+'_status',b+'_total_ms']
        if b!='harvey':fields+=[b+'_prep_ms',b+'_query_ms']
    write_csv(directory/'paper_table.csv',fields,wide)
    tmp=directory/'benchmark.json.tmp';tmp.write_text(json.dumps({**metadata,'rows':rows,'samples':samples},indent=2),encoding='utf-8');tmp.replace(directory/'benchmark.json')


def run_benchmark(primes,backends,settings,cancel,on_event=lambda event:None):
    out=Path(settings['output']);out.mkdir(parents=True,exist_ok=True)
    metadata={'utc_started':dt.datetime.now(dt.timezone.utc).isoformat(),'platform':platform.platform(),
              'python':platform.python_version(),'cpu':cpu_name(),'logical_cpus':os.cpu_count(),
              'settings':settings,'requested_primes':primes,'backends':backends,'state':'running',
              'source_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in list(ROOT.glob('*.py'))+[ROOT/'harvey_adapter.cpp']},
              'protocol':'Warm calibrated batch means, max 2000 calls, spawn startup/IPC/reference validation/export excluded. Preparation and query measured separately; complete totals measured independently. No trace cache for complete calls. Python backends and C++ Harvey explicitly distinguished. Backend order rotated by prime; no memory measurement.',
              'schoof_scope':'Elementary independent Python Schoof, not optimized production implementation.',
              'quarter_scope':'Complete B_L, a_L, U_p(L), L=(p-1)/4 on y^2=x^3+2x; not general-curve setup or multiple distinct queries.'}
    build_info=ROOT/'bin/build_metadata.json'
    if build_info.exists():metadata['build_metadata']=json.loads(build_info.read_text())
    metadata['upstream_provenance']=json.loads((ROOT/'upstream/SOURCE_PROVENANCE.json').read_text())
    if 'harvey' in backends and Path(settings['executable']).is_file():
        try:metadata['harvey_version']=json.loads(subprocess.check_output([settings['executable'],'--version'],env=env_for_kernel(),text=True,timeout=10))
        except Exception as e:metadata['harvey_version_error']=str(e)
    rows=[];samples=[]
    save_outputs(out,rows,samples,metadata)
    for index,p in enumerate(primes):
        order=backends[index%len(backends):]+backends[:index%len(backends)]
        for backend in order:
            if cancel.is_set():break
            on_event({'type':'progress','message':f'p={p:,}: {METHODS[backend]}'})
            reason=''
            if p>settings.get(backend+'_max_prime',LIMIT):reason='Above configured backend maximum prime'
            if backend=='harvey' and not Path(settings['executable']).is_file():reason='Harvey executable missing; build it first'
            if reason:
                result={'row':{'p':p,'L':(p-1)//4,'backend':backend,'method':METHODS[backend],'status':'skipped','message':reason},'samples':[]}
            else:result=isolated_job(p,backend,settings,cancel)
            rows.append(result['row']);samples.extend(result['samples']);save_outputs(out,rows,samples,metadata)
            on_event({'type':'row','row':result['row'],'rows':list(rows)})
        if cancel.is_set():break
    metadata['state']='cancelled' if cancel.is_set() else ('complete_with_missing_results' if any(r['status']!='ok' for r in rows) else 'complete')
    metadata['utc_finished']=dt.datetime.now(dt.timezone.utc).isoformat();save_outputs(out,rows,samples,metadata)
    on_event({'type':'done','rows':rows,'state':metadata['state'],'output':str(out)})
    return rows
