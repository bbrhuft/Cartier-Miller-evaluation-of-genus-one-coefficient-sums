"""Independent bounded validation. Raises on every unexpected discrepancy."""
from pathlib import Path
from fractions import Fraction
from math import comb,isqrt
from collections import Counter
import json,random,time,sys,subprocess,hashlib
from cm_system.api import *
from cm_system.rows import RowSession
from cm_system.backends import product_tree as pt, witt_check, general_argument

ROOT=Path(__file__).resolve().parent
C=Counter();DETAIL=[]


def require(ok,label,**data):
    if not ok:raise AssertionError((label,data))
    C[label]+=1
    if data:DETAIL.append({'check':label,'status':'passed',**data})


def primes(n):
    return [p for p in range(5,n+1) if all(p%d for d in range(2,isqrt(p)+1))]


def dense_power(f,n,p):
    a=[1]
    for _ in range(n):
        b=[0]*(len(a)+len(f)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(f):b[i+j]=(b[i+j]+x*y)%p
        a=b
    return a


def refs(p,prec):
    q=p**prec;h=(p-1)//2;U=[0];B=[0];aa=[];i2=pow(2,-1,q);i8=pow(8,-1,q)
    for i in range(h+1):
        a=comb(2*i,i)*pow(i8,i,q)%q;aa.append(a)
        if i<h:
            t=comb(h+1+i,i)*pow(i2,i,q)%q
            U.append((U[-1]+(h+1+i)*t)%q);B.append((B[-1]+a)%q)
    return U,B,aa


def expected_error(fn,label):
    try:fn()
    except (ValueError,ArithmeticError):C[label]+=1
    else:raise AssertionError('expected rejection: '+label)


def main():
    began=time.perf_counter();rng=random.Random(20261013)
    for p in primes(199):
        for prec in (1,2):
            U,B,a=refs(p,prec)
            for L in range((p-1)//2+1):
                for method in ('auto','direct','product_tree'):
                    z=evaluate(p,L,prec,method)
                    require(z['U']==U[L],'sum_outputs',p=p,L=L,precision=prec,method=method,U=z['U'],expected=U[L])
            if p<71:
                h=(p-1)//2;value=Fraction(0)
                for L in range(h+1):
                    require(value.numerator*pow(value.denominator,-1,p**prec)%(p**prec)==U[L],'exact_fraction_outputs')
                    value+=(h+1+L)*Fraction(comb(h+1+L,L),2**L)
        if p>=13 and p%4==1:
            z=quarter_precision_diagnostics(p)
            U,B,a=refs(p,2)
            require((z['U'],z['B'],z['a'])==(U[z['L']],B[z['L']],a[z['L']]),'quarter2_complete')
            w=witt_check.witt_coordinate(p)
            require(z['K_p']==w['c_scaled'],'Witt_independent_series')
        if p%3==1:
            z=evaluate(p,(p-1)//3,method='ordinary_third')
            if z['exceptional']:C['ordinary_third_exceptions']+=1
        for g in range(1,9):
            d=2*g+1
            if p>d and p%d==d-1:
                s=Session(p);indices=[j*(p+1)//d for j in range(1,g+1)]
                U,B,a=refs(p,1)
                for j,L in enumerate(indices):
                    z=s.evaluate(L,method='higher:'+str(g))
                    require(z['U']==U[L] and z['B']==B[L] and (z['a'] is None or z['a']==a[L]),'higher_complete_outputs',p=p,g=g,L=L)
                    if z['a'] is None:C['zero_boundary_multiplier_skips']+=1
                    require(z['cache_reused']==(j>0),'cache_contracts')
                for lam in [2,3,p-1]:
                    if lam%p in (0,1):continue
                    z=general_argument.prefixes_general(p,d,lam)
                    for L,v in zip(indices,z):
                        val=sum(comb(2*i,i)*pow(lam*pow(4,-1,p)%p,i,p) for i in range(L))%p
                        require(v==val,'general_weight_prefixes')
        for L in sorted({0,1,(p-1)//4,(p-1)//2}):
            cs=[3,-2,5,1]
            val=0
            for i in range(L):
                w=0;fall=1
                for j,c in enumerate(cs):
                    if j:fall*=i-j+1
                    w+=c*fall
                val+=w*comb(2*i,i)*pow(8,-i,p)
            require(weighted_sum(p,L,cs)['value']==val%p,'weighted_outputs')
    # Actually force nontrivial tree widths; covers noncommutative order.
    for p in [277,397,1009]:
        for prec in (1,2):
            U,_,_=refs(p,prec);q=p**prec
            for L in [65,100,(p-1)//2]:
                for width in (3,7,13):
                    P=pt.product_bsgs(pt.coef_U(p,q),L,4,q,width)
                    require(P[(2,0)]*pow(P[(3,3)],-1,q)%q==U[L],'forced_tree_widths')
    # Main theorem, model conversions, split algebra and exceptional traces.
    row_exception=0;split=0
    for p in primes(47):
        if p<7:continue
        for degree in (3,4):
            for _ in range(12):
                f=[1]+[rng.randrange(p) for _ in range(degree-1)]+[rng.randrange(1,p)]
                try:session=RowSession(p,f)
                except ValueError:continue
                dense=dense_power(f,(p-1)//2,p)
                for lam in range(p):
                    if lam and sum(c*pow(pow(lam,-1,p),i,p) for i,c in enumerate(f))%p==0:
                        if degree==4:continue
                    z=session.query(lam)
                    expect=sum(c*pow(lam,p-1-i,p) for i,c in enumerate(dense[:p]))%p
                    require(z['S']==expect,'genus_one_row_queries',p=p,f=f,lam=lam,z=z,expected=expect)
                    row_exception+=bool(z.get('exceptional'));split+=bool(z.get('split_fallback'))
    C['row_exception_queries']=row_exception;C['row_split_queries']=split
    # Fixed-D and generic coefficient controls, including supersingular B=0.
    for p in primes(149):
        if p<7:continue
        models=[(0,1),(1,0),(1,1),(-35,-98),(-30,56)]
        models +=[(rng.randrange(p),rng.randrange(p)) for _ in range(12)]
        for A,B in models:
            if (4*A**3+27*B*B)%p==0:continue
            z=cartier_data(p,A,B);P=dense_power([B,A,0,1],(p-1)//2,p)
            require((z['H'],z['beta'])==(P[p-1],P[p-2]),'Cartier_coefficients',p=p,A=A,B=B,z=z)
            if z['CM_hits']:C['CM_model_hits']+=1
            d=rng.randrange(1,p);zz=cartier_data(p,A*d*d,B*d**3)
            chi=1 if pow(d,(p-1)//2,p)==1 else -1
            require(zz['H']==chi*z['H']%p and zz['beta']==chi*d*z['beta']%p,'model_scaling',p=p,A=A,B=B,d=d)
    # Depth recognizers are retained services; cross-check all six templates.
    sys.path.insert(0,str(ROOT/'retained_research/depth_three_recognition_20261007/core'))
    sys.path.insert(0,str(ROOT/'retained_research/depth_two_recognition_20261006/core'))
    from depth_three_recognize import recognize_depth_three,family_member
    from depth_three_b0_recognize import recognize_depth_three_b0,family_member_b0 as b0_member
    from recognize import recognize_short
    for p in primes(499):
        if p<7:continue
        es=[x for x in range(1,p) if x*x%p==3]
        gs=[x for x in range(1,p) if x*x%p==2]
        for e in es[:1]:
            for g in gs[:1]:
                if p%24!=1:continue
                A,B=family_member(p,e,g,2)
                rec=recognize_depth_three(A,B,p);require(rec['status']=='recognized','depth3_A0_recognition')
                z=cartier_data(p,A,B)
                require(z['kappa']==rec['matches'][0]['beta_multiplier'],'depth3_A0_table_agreement')
        if p%8==1:
            ss=[s for s in range(1,p) if pow(s,4,p)==2]
            if ss:
                A,B=b0_member(p,ss[0],2)
                rec=recognize_depth_three_b0(A,B,p);require(rec['status']=='recognized','depth3_B0_recognition')
                z=cartier_data(p,A,B)
                require(z['kappa']==rec['matches'][0]['beta_multiplier'],'depth3_B0_table_agreement')
        for alpha,gamma,mod in [(-11,-14,4),(-15,-22,3)]:
            if p%mod==1:
                A,B=alpha*4%p,gamma*8%p
                rec=recognize_short(A,B,p);require(rec['status']=='recognized','depth1_recognition')
                require(cartier_data(p,A,B)['kappa']==rec['matches'][0]['beta_multiplier'],'depth1_table_agreement')
        for D,mod,a0,a1,b0,b1 in [(2,8,-91,-60,-462,-308),(3,12,-135,-60,-694,-420)]:
            if p%mod!=1:continue
            roots=[x for x in range(1,p) if x*x%p==D]
            if not roots:continue
            e=roots[0];A=(a0+a1*e)*4%p;B=(b0+b1*e)*8%p
            rec=recognize_short(A,B,p);require(rec['status']=='recognized','depth2_recognition')
            require(cartier_data(p,A,B)['kappa']==rec['matches'][0]['beta_multiplier'],'depth2_table_agreement')
    for p in primes(59):
        if p<7:continue
        for _ in range(8):
            f=[1,rng.randrange(p),rng.randrange(p),rng.randrange(1,p)]
            try:d7_seed.check_cubic(f,p)
            except ValueError:continue
            P=dense_power(f,(p-1)//2,p)
            for mu in range(1,p):
                if d7_seed.eval_poly(f,mu,p):continue
                z=branch_query(p,f,mu)
                expected=sum(c*pow(mu,i,p) for i,c in enumerate(P[:p]))%p
                require(z['T']==expected,'branch_queries')
    # Retain exact negative controls and fail safely on invalid contracts.
    z=quarter_precision_diagnostics(13)
    require((z['B'],z['K_p'],z['naive_boundary'],z['naive_unit_root'])==(70,7,44,83),'p13_counterexamples')
    require(evaluate(17,4,2)['U']==179,'p17_original_correction')
    require(evaluate(7,3,2)['U']==39,'p7_full_block_counterexample')
    z=Session(29).evaluate(12,method='higher:2')
    require(z['a'] is None and z['U']==4*z['B']%29,'p29_boundary_skip')
    # The earlier fifth audit already proves why values alone do not fix a derivative.
    p=19;L=4;B=sum(comb(2*i,i)*pow(8,-i,p) for i in range(L))%p
    deriv=sum(i*comb(2*i,i)*pow(8,-i,p) for i in range(1,L))%p
    good=(B-2*deriv)*pow(4*L,-1,p)%p
    bad=(B-2*(deriv-1))*pow(4*L,-1,p)%p
    require((B,deriv,good,bad)==(14,1,15,8),'finite_field_derivative_counterexample')
    for p in [29,101,397]:
        indices=[0,1,(p-1)//4,(p-1)//2,1]
        for prec in (1,2):
            U,_,_=refs(p,prec)
            out=Session(p).evaluate_many(indices,prec,'direct')
            require([z['U'] for z in out]==[U[L] for L in indices],'shared_direct_batch')
    for fn in [lambda:evaluate(15,2),lambda:evaluate(True,1),lambda:evaluate(13,True),lambda:evaluate(13,7),
               lambda:evaluate(13,3,3),lambda:evaluate(13,3,2,'quarter'),lambda:Session(13).evaluate(3,method='higher:2'),
               lambda:cartier_data(13,0,0),lambda:branch_query(13,[1,0,0,1],0),
               lambda:cartier_data(11,-35,-98,trace=0),lambda:evaluate(1009,200,method='direct',budget=Budget(direct_terms=100)),
               lambda:evaluate(1009,200,method='product_tree',budget=Budget(block_width=2))]:
        expected_error(fn,'input_and_budget_rejections')
    t=cartier_data(13,-11,-14)
    trusted=cartier_data(13,-11,-14,trace=point_trace(13,-11,-14))
    require(trusted['status']=='conditional_on_trusted_trace','trust_status')
    # Child process must fail with nonzero exit, and no undefined output.
    r=subprocess.run([sys.executable,'-m','cm_system','sum','15','2'],cwd=ROOT,capture_output=True,text=True)
    require(r.returncode==2 and json.loads(r.stdout)['status']=='error','CLI_failure_exit')
    stats={'status':'passed','counts':dict(C),'seed':20261013,'elapsed_seconds':time.perf_counter()-began,
           'python':sys.version,'scope':'bounded implementation checks, not external proof review'}
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/validation.json').write_text(json.dumps(stats,indent=2)+'\n')
    with (ROOT/'results/validation_checks.jsonl').open('w') as f:
        for event in DETAIL:f.write(json.dumps(event)+'\n')
    print(json.dumps(stats,indent=2))


if __name__=='__main__':main()
