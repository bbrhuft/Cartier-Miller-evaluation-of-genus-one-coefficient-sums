"""Direct family recognition / trusted-trace preparation, JSON CLI."""
import argparse,json
from dataclasses import asdict
from recognize import recognize_short,prepare_from_trace,RecognizedPreparation

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--p',type=int,required=True)
 g=p.add_mutually_exclusive_group(required=True)
 g.add_argument('--short',type=int,nargs=2,metavar=('A','B'))
 g.add_argument('--f',type=int,nargs=4,metavar=('ONE','C','B','A'))
 p.add_argument('--trusted-trace',type=int)
 p.add_argument('--mu',type=int)
 args=p.parse_args()
 try:
  if args.short is not None:
   out=recognize_short(*args.short,args.p)
  else:
   if args.trusted_trace is None:raise ValueError('--f preparation requires --trusted-trace')
   ev=prepare_from_trace(args.p,args.f,args.trusted_trace)
   if isinstance(ev,RecognizedPreparation):
    out=asdict(ev);out['status']='prepared_from_caller_trusted_trace'
    if args.mu is not None:out['query']=ev.evaluator.query(args.mu)
   else:out=ev
 except ValueError as err:out={'status':'invalid_input','error':str(err)}
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
