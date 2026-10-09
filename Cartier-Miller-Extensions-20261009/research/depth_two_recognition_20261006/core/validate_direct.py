"""Independent seed enumeration, multinomial coefficients and dense original sums."""
from collections import deque
from math import comb,isqrt
from pathlib import Path
import csv,hashlib,json,platform,random,sys
from recognize import recognize_short,prepare_from_trace,verify_supplied_certificate,RecognizedPreparation
from isogeny_closure import find_path,prepare_from_trace as prepare_path,ClosurePreparation
ROOT=Path(__file__).resolve().parent

def prime(p):return p>=2 and all(p%d for d in range(2,isqrt(p)+1))
def roots(A,B,p):return [q for q in range(p) if (q**3+A*q+B)%p==0]
def target(A,q,p):return (-4*A-15*q*q)%p,(-8*A*q-22*q**3)%p
def pair(A,B,p):
 h=(p-1)//2
 def coeff(k):
  total=0
  for i in range(h+1):
   j=k-3*i;l=h-i-j
   if j>=0 and l>=0:total+=comb(h,i)*comb(h-i,j)*pow(A,j,p)*pow(B,l,p)
  return total%p
 return coeff(p-1),coeff(p-2)
def trace(A,B,p):return -sum(0 if (t:=(x**3+A*x+B)%p)==0 else 1 if pow(t,(p-1)//2,p)==1 else -1 for x in range(p))
def dense(f,p):
 v=[1]
 for _ in range((p-1)//2):
  n=[0]*(len(v)+3)
  for i,c in enumerate(v):
   for j,d in enumerate(f):n[i+j]=(n[i+j]+c*d)%p
  v=n
 return v

def normalize(A,B,p):
 for x in range(p):
  t=(x**3+A*x+B)%p
  if t and pow(t,(p-1)//2,p)==1:return [1,(3*x*x+A)%p,3*x*t%p,t*t%p]
 return None
rows=[];counts={'membership_inputs':0,'recognized':0,'negative_inputs':0,'coefficient_pairs':0,'normalized_originals':0,'branch_queries':0,'twist_certificates':0}
family_counts={};rng=random.Random(202610062323)
for p in [p for p in range(7,128) if prime(p)]:
 expected={}
 if p%3==1:
  for B in range(1,p):expected[0,B]=(0,0)
 if p%4==1:
  for A in range(1,p):expected[A,0]=(0,0)
 frontier=list(expected)
 for d in range(2):
  nxt=[]
  for A,B in frontier:
   _,slope=expected[A,B]
   for q in roots(A,B,p):
    tt=target(A,q,p);new=(2*slope-q)%p
    if tt in expected:assert expected[tt][1]==new
    else:expected[tt]=(d+1,new);nxt.append(tt)
  frontier=nxt
 checked_families=set()
 for A in range(p):
  for B in range(p):
   if (4*A**3+27*B**2)%p==0:continue
   rec=recognize_short(A,B,p);found=rec['status']=='recognized'
   assert found==((A,B) in expected),(p,A,B,rec,expected.get((A,B)))
   counts['membership_inputs']+=1
   if not found:counts['negative_inputs']+=1;continue
   counts['recognized']+=1;cert=min(rec['matches'],key=lambda m:m['depth'])
   assert cert['depth']==expected[A,B][0]
   assert cert['beta_multiplier']==expected[A,B][1]
   assert verify_supplied_certificate(p,A,B,cert)==cert
   H,beta=pair(A,B,p)
   assert beta==cert['beta_multiplier']*H%p;counts['coefficient_pairs']+=1
   family=cert['family'];family_counts[family]=family_counts.get(family,0)+1
   rows.append({'p':p,'A':A,'B':B,'family':family,'depth':cert['depth'],'H':H,'beta':beta,'multiplier':cert['beta_multiplier'],'r':cert['parameters'].get('r',''),'e':cert['parameters'].get('e',''),'status':'passed'})
   # Verify supplied quadratic twists without square roots.
   for d in [2,p-1]:
    twisted=recognize_short(d*d*A%p,d**3*B%p,p)
    assert twisted['status']=='recognized'
    tc=min(twisted['matches'],key=lambda m:m['depth'])
    assert tc['beta_multiplier']==d*cert['beta_multiplier']%p
    counts['twist_certificates']+=1
   if family in checked_families:continue
   checked_families.add(family)
   f=normalize(A,B,p)
   if f is None:continue
   ev=prepare_from_trace(p,f,trace(A,B,p));assert isinstance(ev,RecognizedPreparation)
   v=dense(f,p)
   assert (ev.evaluator.H,ev.evaluator.K)==(v[p-1],v[p-2]);counts['normalized_originals']+=1
   for mu in range(1,p):
    if sum(c*pow(mu,j,p) for j,c in enumerate(f))%p:continue
    result=ev.evaluator.query(mu)
    assert result['T']==sum(v[i]*pow(mu,i,p) for i in range(p))%p
    assert result['status']=='computed_from_trusted_data';counts['branch_queries']+=1
# Known genuine depth3 example remains a negative for the complete depth2 classifier.
assert recognize_short(4,16,73)['status']=='not_in_depth_at_most_two_closure'
path=find_path(4,16,73,3,rng)
assert path['status']=='found' and path['length']==3
assert path['beta_multiplier']==15
assert pair(4,16,73)==(10,4)
f=[1,4,0,37]
ev3=prepare_path(73,f,10,roots=[71*16%73,6*16%73,43*16%73])
assert isinstance(ev3,ClosurePreparation)
assert (ev3.evaluator.H,ev3.evaluator.K)==(10,55)
assert ev3.evaluator.query(9)['T']==3
v=dense(f,73);assert v[71]==55 and sum(v[i]*pow(9,i,73) for i in range(73))%73==3
example3={'p':73,'short_model':[4,16],'trace':10,'beta':4,'roots':[71,6,43],'normalized_f':f,'normalized_K':55,'mu':9,'T':3,'certificate':path}
# Tampering with a family parameter must fail algebraic verification.
c=recognize_short(8,2,17)['matches'][0]
bad=dict(c);bad['parameters']=dict(c['parameters']);bad['parameters']['e']=(bad['parameters']['e']+1)%17
try:verify_supplied_certificate(17,8,2,bad)
except ValueError:pass
else:raise AssertionError('tampered e accepted')
with (ROOT/'validation.csv').open('w',newline='') as out:
 w=csv.DictWriter(out,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={'status':'passed','counts':counts,'family_counts':family_counts,'range':'all nonsingular short cubics at everyprime7..127; independent seed graph <=2','seed':202610062323,'depth3_example':example3,'timing_status':'correctness only, not benchmark','environment':{'python':sys.version,'platform':platform.platform()},'tampered_certificate':'rejected'}
(ROOT/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'status':'passed','counts':counts,'family_counts':family_counts,'depth3example':example3}))
