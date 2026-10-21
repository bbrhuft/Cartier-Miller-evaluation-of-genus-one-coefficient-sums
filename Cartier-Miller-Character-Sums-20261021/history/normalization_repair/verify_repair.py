"""Independent references for corrected trace-supplied route; standard library.

Run: python verify_repair.py development
Then: python freeze.py
Then: python verify_repair.py confirmation
No inherited evaluator, trace software, or timing measurements are used.
"""
import hashlib,itertools,json,pathlib,random,sys
from collections import Counter
import cm_character_route as C

ROOT=pathlib.Path(__file__).resolve().parent


def polyadd(a,b,p):
    return [( (a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p
            for i in range(max(len(a),len(b)))]


def polymul(a,b,p):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):r[i+j]=(r[i+j]+x*y)%p
    return r


def polypow(f,m,p):
    z=[1]
    while m:
        if m&1:z=polymul(z,f,p)
        f=polymul(f,f,p);m>>=1
    return z


def tables(p,f):
    sq={y*y%p for y in range(p)}
    eps=[0 if (v:=C.peval(f,x,p))==0 else 1 if v in sq else -1 for x in range(p)]
    ni=1 if len(f)==4 else 1+(1 if f[-1] in sq else -1)
    return eps,1-ni-sum(eps)


def reference(p,eps,a):
    # Fermat inverses independently of the evaluator's modular-inverse calls.
    return sum(eps[x]*pow((x-a)%p,p-2,p) for x in range(p) if x!=a)%p


def function_mul(U,V,f,p):
    a,b=U;c,d=V
    return (polyadd(polymul(a,c,p),polymul(f,polymul(b,d,p),p),p),
            polyadd(polymul(a,d,p),polymul(b,c,p),p))


def line_ratio(P,Q,A,p):
    S,lam=C.ec_add(P,Q,A,p)
    one=([1],[0])
    if P is None or Q is None:return S,one,one
    if S is None:return S,([-P[0]%p,1],[0]),one
    return S,([(lam*P[0]-P[1])%p,-lam%p],[1]),([-S[0]%p,1],[0])


def local_data(U,p):
    # x=t^-2+O(t^2), y=-t^-3+O(t); leading weights have distinct parity.
    terms={}
    for i,c in enumerate(U[0]):
        if c%p:terms[2*i]=c%p
    for j,c in enumerate(U[1]):
        if c%p:terms[2*j+3]=-c%p
    d=max(terms)
    return d,terms.get(d-1,0)*pow(terms[d],-1,p)%p


def explicit_miller(P,m,A,B,p):
    f=[B,A,0,1];one=([1],[0]);num,den=one,one;T=P
    for bit in bin(m)[3:]:
        T,u,v=line_ratio(T,T,A,p)
        num=function_mul(function_mul(num,num,f,p),u,f,p)
        den=function_mul(function_mul(den,den,f,p),v,f,p)
        if bit=='1':
            T,u,v=line_ratio(T,P,A,p)
            num=function_mul(num,u,f,p);den=function_mul(den,v,f,p)
    dn,an=local_data(num,p);dd,ad=local_data(den,p)
    return (an-ad)%p,T,dd-dn


def check_model(p,f,counts,rng=None):
    eps,tau=tables(p,f)
    poles=[a for a in range(p) if eps[a]]
    if rng is not None:poles=rng.sample(poles,min(len(poles),12))
    counts['models']+=1
    for a in poles:
        st={};got=C.value(p,f,a,tau,st)
        want=reference(p,eps,a)
        assert got==want,(p,f,a,tau,got,want)
        counts['values']+=1;counts['route_'+st['route']]+=1
        counts['chain_through_identity']+=st.get('chain_through_identity',False)
        counts['supersingular_values']+=tau==0


def development():
    counts=Counter()
    for d in (3,4):
        for lead in range(1,5):
            for low in itertools.product(range(5),repeat=d):
                f=list(low)+[lead]
                if C.squarefree(f,5):check_model(5,f,counts)
    assert C.value(5,[0,3,0,1],1,-4)==1
    counts['explicit_p5_regression']=1
    for p in (7,11,13,17,19,23,29):
        for A,B in itertools.product(range(p),repeat=2):
            if (4*A**3+27*B**2)%p==0:continue
            f=[B,A,0,1];eps,tau=tables(p,f)
            if p<=11:check_model(p,f,counts)
            pts=[(x,y) for x in range(p) for y in range(p)
                 if y*y%p==C.peval(f,x,p)]
            hpow=polypow(f,(p-1)//2,p)
            block=hpow[p:] or [0]
            H=hpow[p-1] if len(hpow)>=p else 0
            if tau==1:
                for P in pts:
                    alpha,end=C.miller_constant(P,p,A,p)
                    assert end is None
                    assert alpha==P[1]*C.peval(block,P[0],p)%p
                    counts['exceptional_symbolic_formula_checks']+=1
            if (p+1-tau)%p:
                for P in pts:
                    if not P[1]:continue
                    Q=C.ec_mul(P,pow(p,-1,p+1-tau),A,p)
                    alpha,end=C.miller_constant(Q,p,A,p)
                    assert end==P
                    assert P[1]*C.peval(block,P[0],p)%p==(H-1)*alpha%p
                    counts['general_cubic_formula_checks']+=1
            if p<=13:
                for P in [None]+pts:
                    for m in sorted({1,2,3,p,p+1}):
                        alpha,end=C.miller_constant(P,m,A,p)
                        explicit,endpoint,order=explicit_miller(P,m,A,B,p)
                        assert (alpha,end)==(explicit,endpoint),(p,A,B,P,m)
                        expected=0 if P is None else -m if end is None else -(m-1)
                        assert order==expected,(p,A,B,P,m,order,expected)
                        counts['explicit_function_local_expansions']+=1
                # Exact product-divisor addition law; source/end line constants both counted.
                for P,Q in itertools.product(([None]+pts)[:9],repeat=2):
                    S,k0=C.ec_add(P,Q,A,p)
                    for m in (2,p):
                        al,EP=C.miller_constant(P,m,A,p)
                        ar,EQ=C.miller_constant(Q,m,A,p)
                        ass,_=C.miller_constant(S,m,A,p)
                        _,k1=C.ec_add(EP,EQ,A,p)
                        assert ass==(al+ar+k1-m*k0)%p
                        counts['miller_addition_law_checks']+=1
    rng=random.Random(202610211501)
    for p in (7,11,17,31,101):
        for d in (3,4):
            for _ in range(15):
                while True:
                    f=[rng.randrange(p) for _ in range(d)]+[rng.randrange(1,p)]
                    if C.squarefree(f,p):break
                check_model(p,f,counts,rng)
        for c in (1,2):
            f=[1,0,0,0,c]
            if C.squarefree(f,p):check_model(p,f,counts)
    return dict(counts)


def confirmation():
    frozen=json.loads((ROOT/'FREEZE.json').read_text())
    for name,digest in frozen['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    rng=random.Random(int(frozen['digest'],16));counts=Counter()
    primes=[p for p in range(37,300) if all(p%d for d in range(2,int(p**.5)+1))]
    primes=rng.sample(primes,7)+[1009]
    for p in primes:
        for d in (3,4):
            for _ in range(20):
                while True:
                    f=[rng.randrange(p) for _ in range(d)]+[rng.randrange(1,p)]
                    if C.squarefree(f,p):break
                check_model(p,f,counts,rng)
    return {'freeze_digest':frozen['digest'],'confirmation_primes':primes,**dict(counts)}


if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'development'
    out={'mode':mode,'status':'PASS',**(development() if mode=='development' else confirmation())}
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/f'{mode}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
