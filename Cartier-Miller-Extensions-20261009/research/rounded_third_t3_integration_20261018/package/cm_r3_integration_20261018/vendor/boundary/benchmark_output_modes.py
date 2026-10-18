"""Small, matched output-mode benchmark; no general speedup claim."""
import argparse
import csv
import json
from pathlib import Path
import platform
from statistics import median
import sys
from time import perf_counter

from boundary_framework import __version__
from integrated_thirds import ThirdPointSession
from integrated_fifths import FifthPointSession
from benchmark_integrated import original_sum_scaled
from benchmark_fifths import original_pair_shared


def run(repeats=3,output=Path('results')):
    output.mkdir(exist_ok=True,parents=True);rows=[]
    cases=(('ordinary13_forced_factorial',13,'third',None,'factorial'),
           ('rounded17',17,'third',None,'auto'),
           ('fifth29_second',29,'fifth','second','auto'),
           ('fifth29_pair',29,'fifth',None,'auto'),
           ('ordinary1000003_control',1000003,'third',None,'auto'),
           ('rounded1000037_control',1000037,'third',None,'auto'),
           ('fifth1000039_control',1000039,'fifth',None,'auto'))
    for label,p,kind,which,policy in cases:
        L=(p-1)//3 if p%3==1 else (p+1)//3
        if kind=='third':expected=[original_sum_scaled(p,L)]
        else:
            step=(p+1)//5
            wanted=[2*step] if which=='second' else [step,2*step]
            expected=original_pair_shared(p,wanted)
        for mode in ('full','u_only'):
            group=[]
            for repeat in range(repeats):
                begin=perf_counter()
                if kind=='third':
                    r=ThirdPointSession(p).evaluate(boundary_policy=policy,output_mode=mode)
                    values=[r['U_p_L']];calls=len(r['boundary']['factorial_calls'])
                    skipped=1 if r['boundary_status']=='skipped_zero_multiplier' else 0
                else:
                    r=FifthPointSession(p).evaluate(wanted,output_mode=mode)
                    values=[row['U_p_L'] for row in r['outputs']]
                    calls=len(r['boundary_details']['interval_calls']);skipped=len(r['skipped_boundary_indices'])
                wall=perf_counter()-begin
                if values!=expected:raise RuntimeError(f'output-mode mismatch {(label,mode)}')
                group.append({'case':label,'p':p,'output_mode':mode,'repeat':repeat,
                              'wall_ms':wall*1000,'acquisition_calls':calls,
                              'skipped_boundaries':skipped,'correct':True})
            rows.extend(group)
    with (output/'output_mode_benchmark.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    medians=[]
    for i in range(0,len(rows),repeats):
        group=rows[i:i+repeats]
        medians.append({**{k:group[0][k] for k in ('case','p','output_mode','acquisition_calls','skipped_boundaries')},
                        'median_wall_ms':median(r['wall_ms'] for r in group)})
    record={'version':__version__,'python':sys.version,'platform':platform.platform(),
            'repeats':repeats,'timed_evaluations':len(rows),'all_correct':True,
            'scope':'Cold complete-U outputs with preparation included; full mode also returns diagnostics. Imports/serialization excluded. Third counts are factorial calls; fifth counts are interval products. Ordinary13 explicitly forces the factorial route; its default trace route already uses no factorial. Tiny-case wall-time ratios are not meaningful performance claims.',
            'medians':medians}
    (output/'output_mode_benchmark_summary.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2));return record


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats',type=int,default=3)
    parser.add_argument('--output',type=Path,default=Path('results'))
    args=parser.parse_args()
    if args.repeats<1:parser.error('--repeats must be positive')
    run(args.repeats,args.output)
