#!/usr/bin/env python3
"""Independent B=0 depth-three audit. Standard library; no inherited arithmetic.

The delivered recognizer is treated as a black box. Integer and finite-field
references below do not call its coefficient, quotient, trace or expansion
helpers. Run from any directory; writes results beside this script.
"""
from pathlib import Path
from fractions import Fraction
from math import isqrt, factorial
import csv, hashlib, json, platform, random, sys, time

HERE = Path(__file__).resolve().parent
SRC = HERE/'inherited/research/depth_three_recognition_20261007'
sys.path.insert(0,str(SRC/'core'))
import depth_three_b0_recognize as delivered
from depth_three_recognize import recognize_short_through_depth_three

def prime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))

def mul(a,b):
    z=[0]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            z[(i+j)%4]+=x*y*(2 if i+j>=4 else 1)
    return tuple(z)

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(n,a): return tuple(n*x for x in a)
def power(a,n):
    z=(1,0,0,0)
    for _ in range(n): z=mul(z,a)
    return z
def mat(a):
    return [[mul(a,tuple(int(j==k) for j in range(4)))[i] for k in range(4)] for i in range(4)]
def det(A):
    A=[list(map(Fraction,row)) for row in A]; sign=1; val=Fraction(1)
    for k in range(len(A)):
        j=next((j for j in range(k,len(A)) if A[j][k]),None)
        if j is None:return 0
        if j!=k:A[j],A[k]=A[k],A[j];sign=-sign
        v=A[k][k];val*=v
        for j in range(k+1,len(A)):
            q=A[j][k]/v
            A[j]=[x-q*y for x,y in zip(A[j],A[k])]
    val*=sign
    assert val.denominator==1
    return int(val)
def norm(a):return det(mat(a))
def resultant(a,b):
    m,n=len(a)-1,len(b)-1
    return det([[0]*i+list(reversed(a))+[0]*(n-i-1) for i in range(n)]
               +[[0]*i+list(reversed(b))+[0]*(m-i-1) for i in range(m)])
def poly_eval(f,x):
    z=0
    for c in f[::-1]:z=z*x+c
    return z
def ev(a,s,p):return sum(x*pow(s,i,p) for i,x in enumerate(a))%p

def quotient(A,B,q,p):
    # Direct two-torsion Vélu coefficients, distinct algebraic expression.
    assert (q*q*q+A*q+B)%p==0
    t=(3*q*q+A)%p
    return (A-5*t)%p,(B-7*q*t)%p
def roots(A,B,p):return [q for q in range(p) if (q*q*q+A*q+B)%p==0]
def j_invariant(A,B,p):return 6912*pow(A,3,p)*pow((4*A*A*A+27*B*B)%p,-1,p)%p
def coefficients(A,B,p):
    h=(p-1)//2; fac=[factorial(k) for k in range(h+1)]; res=[]
    for degree in (p-1,p-2):
        z=0
        for b_exp in range(h+1):
            remaining=h-b_exp
            # 3*x_exp + A_exp = degree, x_exp + A_exp = remaining.
            if (degree-remaining)%2:continue
            x_exp=(degree-remaining)//2; a_exp=remaining-x_exp
            if min(x_exp,a_exp)<0:continue
            z+=fac[h]//(fac[x_exp]*fac[a_exp]*fac[b_exp])*pow(A,a_exp,p)*pow(B,b_exp,p)
        res.append(z%p)
    return tuple(res)
def point_trace(A,B,p):
    squares=[False]*p
    for y in range(p):squares[y*y%p]=True
    affine=0
    for x in range(p):
        z=(x*x*x+A*x+B)%p
        affine+=1 if z==0 else 2 if squares[z] else 0
    return p-affine
def primary_pair(p):
    # Exhaustive integer reference; not Cornacchia.
    for a in range(1,isqrt(p)+1,2):
        b=isqrt(p-a*a)
        if a*a+b*b==p:
            a=a if (a+b)%4==1 else -a
            assert b%2==0
            return a,b
    raise AssertionError(p)
def dense(f,p):
    z=[1]
    for _ in range((p-1)//2):
        w=[0]*(len(z)+len(f)-1)
        for i,a in enumerate(z):
            for k,b in enumerate(f):w[i+k]=(w[i+k]+a*b)%p
        z=w
    return z
def write_csv(name,rows):
    if not rows:return
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (HERE/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def point_add(P,Q,A,p):
    if P is None:return Q
    if Q is None:return P
    x,y=P;u,v=Q
    if x==u and (y+v)%p==0:return None
    k=((3*x*x+A)*pow(2*y,-1,p) if P==Q else (v-y)*pow(u-x,-1,p))%p
    xx=(k*k-x-u)%p
    return xx,(k*(x-xx)-y)%p
def point_mul(n,P,A,p):
    R=None
    while n:
        if n&1:R=point_add(R,P,A,p)
        P=point_add(P,P,A,p);n>>=1
    return R
def sqrt_mod(a,p):
    if not a:return 0
    if pow(a,(p-1)//2,p)!=1:return None
    q=p-1;k=0
    while q%2==0:q//=2;k+=1
    z=2
    while pow(z,(p-1)//2,p)!=p-1:z+=1
    x=pow(a,(q+1)//2,p);t=pow(a,q,p);c=pow(z,q,p)
    while t!=1:
        i=1;tt=t*t%p
        while tt!=1:i+=1;tt=tt*tt%p
        b=pow(c,1<<(k-i-1),p)
        x=x*b%p;t=t*b*b%p;c=b*b%p;k=i
    assert x*x%p==a
    return x

def main():
    began=time.time(); rng=random.Random(9310712);summary={}
    # Exact chain over Z[s]/(s^4-2), without importing any constants.
    zero=(0,0,0,0);one=(1,0,0,0)
    model=(scale(-1,one),zero);qs=[one,(1,0,2,0),(1,4,2,4)];beta=zero
    chain=[]
    for q in qs:
        A,B=model
        assert add(add(power(q,3),mul(A,q)),B)==zero
        t=add(scale(3,power(q,2)),A)
        model=(add(A,scale(-5,t)),add(B,scale(-7,mul(q,t))))
        beta=add(scale(2,beta),scale(-1,q));chain.append(model)
    alpha,gamma=model
    assert alpha==delivered.ALPHA and gamma==delivered.GAMMA and beta==delivered.MULTIPLIER
    a3,g2=power(alpha,3),power(gamma,2)
    assert a3==delivered.ALPHA_CUBED and g2==delivered.GAMMA_SQUARED
    delta=add(scale(4,a3),scale(27,g2)); MD,MJ=mat(delta),mat(scale(6912,a3))
    const=json.loads((SRC/'theory/b0/b0_family_constants.json').read_text())
    H=const['class_polynomial_low_to_high']
    # Five distinct evaluations prove the claimed degree-four determinant identity.
    for z in (-3,-1,1,4,11):
        assert det([[z*MD[i][k]-MJ[i][k] for k in range(4)] for i in range(4)])==norm(delta)*poly_eval(H,z)
    quantities={'norm_alpha':norm(alpha),'norm_gamma':norm(gamma),'norm_discriminant':norm(delta),
                'disc_H256_via_resultant_with_derivative':resultant(H,[i*H[i] for i in range(1,5)])}
    for value in (0,1728,287496,54000):quantities['H256_at_'+str(value)]=poly_eval(H,value)
    polys={'P2':[-7367066619912,-82226316240,1],'P3':[6549518250000,-2835810000,1],
           'H192':[-1080060886113159937649308593750000,826335556188178615474500000000,
                   15705521635909735050750000,-8041801037378436000,1]}
    for name,pol in polys.items():quantities['resultant_H256_'+name]=resultant(H,pol)
    nonduals=[add(qs[1],scale(2,qs[0])),add(qs[2],scale(2,qs[1])),(0,4,0,4)]
    for name,z in zip(('q1_plus_2q0','q2_plus_2q1','third_root_difference_4(1+e)s'),nonduals):
        quantities['norm_'+name]=norm(z)
    factor_rows=[]
    for name,v in quantities.items():
        assert v==int(const['quantities'][name])
        fac=const['factorizations'][name];product=1
        for q,e in fac.items():
            q=int(q);assert prime(q);product*=q**e
            assert q in (2,3) or q%4==3
            factor_rows.append({'quantity':name,'factor':q,'exponent':e,'trial_division_prime':True})
        assert abs(v)==product
    write_csv('integer_factor_checks.csv',factor_rows)
    summary['exact_integer_identities']=len(quantities)
    summary['largest_factor_independently_trial_divided']=max(r['factor'] for r in factor_rows)
    # Positive membership, all twists and all four parameter conjugates.
    eligible=[p for p in range(7,5000) if prime(p) and p%8==1 and pow(2,(p-1)//4,p)==1]
    form_rows=[]
    for p in range(7,5000):
        if not prime(p):continue
        a,b=primary_pair(p) if p%4==1 else (None,None)
        form=any(p-x*x>=64 and (p-x*x)%64==0 and isqrt((p-x*x)//64)**2==(p-x*x)//64
                 for x in range(1,isqrt(p)+1))
        assert form==(p in eligible)
        if form:assert b%8==0
        form_rows.append({'p':p,'eligible':p in eligible,'form_x2_plus_64y2':form,'a':a,'b':b})
    write_csv('eligibility_checks.csv',form_rows)
    summary['eligible_primes_below_5000']=len(eligible)
    exhaustive=[];member_rows=[];den_rows=[];cubic_rows=[];family_by_p={}
    for p in [73,89,113,233,257,281,337,353,577,593,601,617]:
        ss=[s for s in range(p) if pow(s,4,p)==2];assert len(ss)==4
        expected={}
        for s in ss:
            for r in range(1,p):
                A,B=ev(alpha,s,p)*r*r%p,ev(gamma,s,p)*r**3%p
                assert (A,B) not in expected
                expected[A,B]=(s,r)
                found=delivered.recognize_depth_three_b0(A,B,p)
                assert found['status']=='recognized'
                cert=found['matches'][0]
                assert cert['parameters']['s']==s and cert['parameters']['r']==r
                qs_p=[ev(q,s,p)*r%p for q in qs]
                ab=(-r*r%p,0); h=(p-1)//2
                for q in qs_p:ab=quotient(*ab,q,p)
                assert ab==(A,B)
                U=[(B*B*a-A**3*b)%p for a,b in zip(a3,g2)]
                P1=(2*U[0]*U[2]-U[1]**2-2*U[3]**2)%p
                linear=(U[1]+U[3]*s*s)%p
                assert P1 and linear
                den_rows.append({'p':p,'s':s,'r':r,'P1':P1,'linear_denominator':linear})
        family_by_p[p]=expected
        # Independent brute-force graph: keep the previous dual root as state.
        states={(A,0,None) for A in range(1,p)}
        for depth in range(3):
            nxt=set()
            for A,B,previous in states:
                for q in roots(A,B,p):
                    if (depth==0 and q==0) or (previous is not None and q==previous):continue
                    AA,BB=quotient(A,B,q,p);nxt.add((AA,BB,-2*q%p))
            states=nxt
        assert {(A,B) for A,B,_ in states}==set(expected)
        js={j_invariant(A,B,p) for A,B in expected}
        assert len(js)==4 and all(poly_eval(H,j)%p==0 for j in js)
        accepted=0;tested=0
        for A in range(p):
            for B in range(p):
                if (4*A**3+27*B*B)%p==0:continue
                out=delivered.recognize_depth_three_b0(A,B,p);tested+=1
                yes=out['status']=='recognized'
                assert yes==((A,B) in expected)
                if not yes:assert out['status']=='not_in_depth_three_b0_family'
                accepted+=yes
        exhaustive.append({'p':p,'nonsingular_models':tested,'accepted':accepted,'graph_endpoints':len(expected)})
        # Point count and coefficient references on all members at the first 3 primes.
        a,b=primary_pair(p)
        items=list(expected.items()) if p<=113 else rng.sample(list(expected.items()),20)
        for (A,B),(s,r) in items:
            Href,bref=coefficients(A,B,p);tau=point_trace(A,B,p)
            chi=1 if pow(r,h,p)==1 else -1
            assert tau==2*chi*a and Href==tau%p and bref==ev(beta,s,p)*r*Href%p
            member_rows.append({'p':p,'A':A,'B':B,'s':s,'r':r,'H':Href,'beta':bref,'trace':tau})
        # Build normalized cubics independently from rational points on the target.
        for (A,B),(s,r) in rng.sample(list(expected.items()),3):
            for x in range(p):
                y=sqrt_mod((x**3+A*x+B)%p,p)
                if y:break
            f=[1,(3*x*x+A)*pow(y,-1,p)%p,3*x%p,y]
            poly=dense(f,p);prep=delivered.prepare_cm_b0(p,f,rng=rng)
            tau=point_trace(A,B,p)
            assert prep.exact_trace==tau
            assert (prep.evaluator.H,prep.evaluator.K)==(poly[p-1],poly[p-2])
            for q in roots(A,B,p):
                mu=(q-x)*pow(y,-1,p)%p
                if mu==0:continue # retained branch API explicitly requires nonzero root.
                T=sum(c*pow(mu,i,p) for i,c in enumerate(poly[:p]))%p
                assert prep.evaluator.query(mu)['T']==T
                cubic_rows.append({'p':p,'f':json.dumps(f),'H':poly[p-1],'K':poly[p-2],'mu':mu,'T':T})
        print('Independent exhaustive prime',p,'models',tested,flush=True)
    for name,rows in [('exhaustive_checks.csv',exhaustive),('coefficient_checks.csv',member_rows),
                      ('denominator_checks.csv',den_rows),('cubic_checks.csv',cubic_rows)]:write_csv(name,rows)
    summary.update({'exhaustive_primes':len(exhaustive),'exhaustive_models':sum(r['nonsingular_models'] for r in exhaustive),
                    'accepted_models':sum(r['accepted'] for r in exhaustive),'coefficient_and_trace_checks':len(member_rows),
                    'original_cubic_branch_checks':len(cubic_rows)})
    # New non-member sample, including valid quartic roots at supersingular primes.
    negative=[]
    for p in [7,11,13,17,23,31,41,47,71,97,137,167,191,193,239,251,313,401,409,479,599,647,719,743,12263]:
        assert p not in eligible
        for _ in range(100):
            A,B=rng.randrange(p),rng.randrange(p)
            if (4*A**3+27*B*B)%p==0:continue
            out=delivered.recognize_depth_three_b0(A,B,p)
            assert out['status']=='not_eligible_prime'
            negative.append({'p':p,'A':A,'B':B,'status':out['status']})
    write_csv('ineligible_checks.csv',negative);summary['ineligible_input_checks']=len(negative)
    # All conjugates and random twists at every recorded large prime, using independent
    # curve arithmetic for a sign witness. This is not a general point-count oracle.
    rows=list(csv.DictReader((SRC/'core/validation_b0_large_primes.csv').open()));large=[]
    for row in rows:
        p,A,B,tau=map(int,(row['p'],row['A'],row['B'],row['trace_theorem5']))
        for x in range(1,200):
            y=sqrt_mod((x**3+A*x+B)%p,p)
            if y is None or y==0:continue
            P=x,y
            assert point_mul(p+1-tau,P,A,p) is None
            if point_mul(p+1+tau,P,A,p) is not None:break
        else:raise AssertionError('No trace-sign witness')
        for s in [int(row['s']),-int(row['s']),sqrt_mod(p-1,p)*int(row['s']),-sqrt_mod(p-1,p)*int(row['s'])]:
            s%=p;r=rng.randrange(1,p);AA,BB=ev(alpha,s,p)*r*r%p,ev(gamma,s,p)*r**3%p
            cert=delivered.recognize_depth_three_b0(AA,BB,p)['matches'][0]
            assert (cert['parameters']['s'],cert['parameters']['r'])==(s,r)
        large.append({'p':p,'bits':p.bit_length(),'A':A,'B':B,'trace':tau,'witness_x':x,'witness_y':y,
                      'correct_order_annihilates':True,'opposite_order_does_not':True,'four_conjugates_checked':True})
    write_csv('large_sign_witnesses.csv',large);summary['large_trace_sign_witnesses']=len(large)
    # Demonstrate that caller-supplied trace checks alone do not certify the sign.
    prep=delivered.prepare_from_trace_b0(73,[1,60,0,10],6)
    assert prep.evaluator.H==6
    try:delivered.prepare_from_trace_b0(73,[1,60,0,10],6,verify_trace=True,rng=rng)
    except ValueError:pass
    else:raise AssertionError('Verified route accepted opposite sign')
    # Audit supplied certificate schema separately from its mathematical soundness.
    base=delivered.recognize_depth_three_b0(16,27,73)['matches'][0]
    extra=json.loads(json.dumps(base));extra['parameters']['unverified_note']='deliberately injected'
    rec=delivered.verify_supplied_certificate_b0(73,16,27,extra)
    summary['minor_schema_issue']='unknown nested parameter keys ignored; returned certificate is recomputed and sound'
    assert 'unverified_note' not in rec['parameters']
    summary.update({'status':'passed_mathematical_checks_with_documentation_and_schema_findings',
                    'python':sys.version,'platform':platform.platform(),'seed':9310712,
                    'elapsed_seconds_not_benchmark':round(time.time()-began,3),
                    'input_source_sha256':{str(f.relative_to(HERE)):hashlib.sha256(f.read_bytes()).hexdigest()
                                          for f in [SRC/'core/depth_three_b0_recognize.py',SRC/'theory/b0/derive_b0_family.py',
                                                    HERE/'inputs/Depth_Three_Recognition_Proof_Note_20261007-1.md']}})
    (HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
