"""Independent finite certificates and regression checks for consolidation.

Standard library only. The elliptic group law and scalar multiplication here
do not import the prototype's implementation. Finite point witnesses prove
the small-prime proper-subgroup lemma; enumeration is separate supporting
evidence. Timing is not benchmark evidence.
"""
from pathlib import Path
from math import gcd, isqrt
import csv, hashlib, json, platform, random, subprocess, sys
from copy import deepcopy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import depth_three_recognize as impl


def add(P, Q, A, p):
    if P is None: return Q
    if Q is None: return P
    x, y = P; u, v = Q
    if x == u and (y+v) % p == 0: return None
    numerator, denominator = (3*x*x+A, 2*y) if P == Q else (v-y, u-x)
    slope = numerator*pow(denominator, -1, p) % p
    X = (slope*slope-x-u) % p
    return X, (slope*(x-X)-y) % p


def multiply(n, P, A, p):
    # Left-to-right multiplication; production code uses right-to-left.
    R = None
    for bit in bin(n)[2:]:
        R = add(R, R, A, p)
        if bit == '1': R = add(R, P, A, p)
    return R


def family(p, e, g, r):
    A, B = 0, -r**3 % p
    for q in [r, (1+2*e)*r % p, (1+2*e+6*g+2*e*g)*r % p]:
        assert (q**3+A*q+B) % p == 0
        A, B = (-4*A-15*q*q) % p, (-8*A*q-22*q**3) % p
    return A, B


def square_roots(p, n): return [x for x in range(p) if x*x % p == n]


def write_csv(name, rows):
    with (HERE/name).open('w', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def main():
    primes = [p for p in range(7,337) if p % 24 == 1 and all(p%d for d in range(2,isqrt(p)+1))]
    assert primes == [73,97,193,241,313]
    witnesses=[]; scans=[]; arithmetic=[]
    for p in primes:
        representations=[(2*x,y) for y in range(1,isqrt(p//48)+1)
                         for x in [isqrt(p-48*y*y)] if x*x+48*y*y==p]
        assert len(representations)==1
        t0,f=representations[0]
        common=gcd(p+1-t0,p+1+t0)
        arithmetic.append({'p':p,'t0':t0,'f':f,'common_gcd':common,'minimum_order':p+1-t0,
                           'general_kernel_upper_bound':4*common,'needs_point_witness':4*common>=p+1-t0})
        nonresidue=next(x for x in range(2,p) if pow(x,(p-1)//2,p)==p-1)
        root_of={y*y % p:y for y in range(p)}
        for e in square_roots(p,3):
          for g in square_roots(p,2):
            for r in [1,nonresidue]:
                A,B=family(p,e,g,r)
                good=[]; group_order=1
                for x in range(p):
                    z=(x**3+A*x+B) % p
                    if z not in root_of: continue
                    y=root_of[z]
                    group_order += 1 if y==0 else 2
                    if multiply(common,(x,y),A,p) is not None: good.append((x,y))
                assert good
                # This checks the raw-x sampler, without assuming uniform points.
                assert 5*len(good)>=p
                assert group_order in [p+1-t0,p+1+t0]
                tau=p+1-group_order
                scans.append({'p':p,'e':e,'g':g,'r':r,'A':A,'B':B,'order':group_order,
                              'successful_x':len(good),'probability_denominator':p,
                              'at_least_one_fifth':True})
                P=good[0];R=multiply(common,P,A,p)
                assert R is not None and (P[1]*P[1]-P[0]**3-A*P[0]-B) % p==0
                if p==97:
                    witnesses.append({'p':p,'e':e,'g':g,'r':r,'A':A,'B':B,'common_gcd':common,
                                      'P_x':P[0],'P_y':P[1],'gP_x':R[0],'gP_y':R[1]})
                decided,info=impl.decide_trace_sign(A,B,p,t0,random.Random(p+e+g+r),max_trials=None)
                assert decided==tau
                assert impl.verify_trace_sign_witness(A,B,p,t0,info['witness'])==tau
                w=info['witness'];point=tuple(w['point'])
                assert [multiply(n,point,A,p) is None for n in w['candidate_orders']]==w['annihilated']
                assert info['expected_raw_trials_upper_bound']==5
    assert len(witnesses)==8 and len(scans)==40
    write_csv('sign_bound_small_prime_arithmetic.csv',arithmetic)
    write_csv('sign_bound_p97_witnesses.csv',witnesses)
    write_csv('validation_sign_sampler.csv',scans)

    # A genuine obstruction to extending the success bound to every easy seed.
    p,A,B,common=97,0,19,28
    pts=[None]+[(x,y) for x in range(p) for y in range(p) if (y*y-x**3-B) % p==0]
    assert len(pts)==112 and all(multiply(common,P,A,p) is None for P in pts)
    obstruction={'p':p,'A':A,'B':B,'order':len(pts),'trace':-14,'candidate_orders':[84,112],
                 'all_points_killed_by':common,'why_retained':'generic sign trial can be inconclusive forever; recognized depth-three premise is essential'}
    (HERE/'sign_test_obstruction.json').write_text(json.dumps(obstruction,indent=2)+'\n')
    try: impl.decide_trace_sign(A,B,p,14)
    except ValueError: pass
    else: raise AssertionError('uncovered easy seed accepted by bounded sign API')

    # Force y=0 for every raw draw: cap must return an honest non-answer.
    class ForcedRoot:
        def __init__(self,p,A,B):
            self.p=p;self.q=next(x for x in range(p) if (x**3+A*x+B) % p==0)
        def randrange(self,*args):
            if args==(self.p,): return self.q
            if args==(2,self.p):
                return next(c for c in range(2,self.p) if pow(c,(self.p-1)//3,self.p)!=1)
            raise AssertionError(args)
    decided,info=impl.decide_trace_sign(4,16,73,10,ForcedRoot(73,4,16),3)
    assert decided is None and info['status']=='inconclusive_after_max_trials' and info['trials']==3
    assert info['inconclusive_probability_upper_bound']=='(4/5)^3'
    # The probability assertion concerns uniform draws; forced draws test status only.
    capped=impl.prepare_cm(73,[1,4,0,37],rng=ForcedRoot(73,2,55),max_trials=3)
    assert capped['status']=='trace_sign_inconclusive'
    prepared=impl.prepare_cm(73,[1,4,0,37],rng=random.Random(73),max_trials=None)
    assert prepared.exact_trace==10 and prepared.evaluator.K==55 and prepared.evaluator.query(9)['T']==3
    assert prepared.evaluator.query(9)['status']=='exact_mod_p'
    verified=impl.prepare_from_trace(73,[1,4,0,37],10,verify_sign=True,rng=random.Random(73),max_trials=None)
    assert verified.evaluator.query(9)['status']=='exact_mod_p'
    assert impl.verify_trace_sign_witness(2,55,73,10,verified.trace_sign_verification['witness'])==10
    assert impl.prepare_from_trace(73,[1,4,0,37],10).evaluator.query(9)['status']=='computed_from_trusted_data'

    # Stored point witness must not be accepted on its declared flags alone.
    _,info=impl.decide_trace_sign(4,16,73,10,random.Random(73),max_trials=None)
    w=deepcopy(info['witness']);w['annihilated'].reverse()
    try:impl.verify_trace_sign_witness(4,16,73,10,w)
    except ValueError:pass
    else:raise AssertionError('altered annihilation flags accepted')
    w=deepcopy(info['witness']);w['point']=[0,0]
    try:impl.verify_trace_sign_witness(4,16,73,10,w)
    except ValueError:pass
    else:raise AssertionError('off-curve witness accepted')
    stored=impl.recognize_depth_three(4,16,73)['matches'][0]
    stored=deepcopy(stored);stored['parameters']['unverified_extra']=1
    try:impl.verify_supplied_certificate(73,4,16,stored)
    except ValueError:pass
    else:raise AssertionError('unknown stored parameter accepted')

    fx=json.loads((HERE.parents[2]/'fixtures/depth_three_recognition_fixtures.json').read_text())
    negative=[]
    for A,B in fx['p73_B0_chain_depth3_rejected']:
        out=impl.recognize_short_through_depth_three(A,B,73)
        assert out['status']=='not_in_implemented_families'
        negative.append({'p':73,'A':A,'B':B,'status':out['status'],'known_uncovered_family':'depth-three B=0 seed'})
    write_csv('validation_partial_recognition_status.csv',negative)
    cli=HERE/'cli.py'
    for args,status in [(['--short','16','27','--through-depth-two'],'not_in_implemented_families'),
                        (['--f','1','4','0','37','--cm','--unbounded-sign-test','--mu','9'],'prepared_by_cm_trace'),
                        (['--f','1','4','0','37','--trusted-trace','10','--verify-sign','--mu','9'],'prepared_from_sign_verified_trace')]:
        data=json.loads(subprocess.run([sys.executable,str(cli),'--p','73',*args],check=True,capture_output=True,text=True).stdout)
        assert data['status']==status

    result={'status':'passed','scope':'new sign-bound certificates and code changes; not a benchmark',
            'finite_lemma_witnesses':len(witnesses),'sampler_base_models':len(scans),'uncovered_status_regressions':len(negative),
            'counterexample':obstruction,'forced_cap_status':'trace_sign_inconclusive',
            'environment':{'python':sys.version,'platform':platform.platform()},
            'source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ['depth_three_recognize.py','cli.py','validate_consolidation.py']}}
    (HERE/'consolidation_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
