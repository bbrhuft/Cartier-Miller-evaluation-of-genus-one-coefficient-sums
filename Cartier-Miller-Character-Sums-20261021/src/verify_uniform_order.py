"""Standard-library correctness checks; no performance claims or trace backend.

Run development, freeze, confirmation in that order to reproduce this audit.
The confirmation source digest is checked before any samples are drawn.
"""
import hashlib,itertools,json,pathlib,random,sys
from collections import Counter
import cm_character_route as C
import uniform_order as U
ROOT=pathlib.Path(__file__).resolve().parent


def tables(p,f):
    sq={y*y%p for y in range(p)}
    es=[0 if (v:=C.peval(f,x,p))==0 else 1 if v in sq else -1 for x in range(p)]
    ninf=1 if len(f)==4 else 2 if f[-1]%p in sq else 0
    return es,1-ninf-sum(es)


def mul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return c


def power(f,h,p):
    a=[1]
    while h:
        if h&1:a=mul(a,f,p)
        f=mul(f,f,p);h>>=1
    return a


def early_identity(p,f,a,trace):
    e=C.character(C.peval(f,a,p),p)
    A,B,R=C.short_model(C.normalize_at(f,a,p),p)
    n=p+1-e*trace;T=R;prefix=1
    for bit in bin(n)[3:]:
        T=C.ec_add(T,T,A,p)[0];prefix*=2
        if T is None and prefix<n:return True
        if bit=='1':
            T=C.ec_add(T,R,A,p)[0];prefix+=1
            if T is None and prefix<n:return True
    return False


def check(p,f,ct,rng=None):
    es,tau=tables(p,f);ct['models']+=1
    aa=[a for a in range(p) if es[a]]
    if rng:aa=rng.sample(aa,min(len(aa),15))
    for a in aa:
        st={};out=U.value(p,f,a,tau,st)
        want=sum(es[x]*pow((x-a)%p,p-2,p) for x in range(p) if x!=a)%p
        assert out==want,(p,f,a,tau,out,want)
        assert out==C.value(p,f,a,tau)
        ct['direct_values']+=1
        ct['two_torsion']+=st['two_torsion']
        ct['twisted_trace_one']+=st['twisted_trace']==1
        ct['p_divides_order']+=st['scalar']%p==0
        ct['zero_final_endpoints']+=1
        ct['intermediate_identity']+=early_identity(p,f,a,tau)
        ct['supersingular_values']+=tau==0


def development():
    ct=Counter()
    for d in (3,4):
        for lead in range(1,5):
            for low in itertools.product(range(5),repeat=d):
                f=list(low)+[lead]
                if C.squarefree(f,5):check(5,f,ct)
    rng=random.Random(202610211744)
    for p in (7,11,13,17,19,23,29):
        for A,B in itertools.product(range(p),repeat=2):
            if (4*A**3+27*B*B)%p==0:continue
            f=[B,A,0,1];es,tau=tables(p,f);n=p+1-tau
            if p<=11:check(p,f,ct)
            vv=power(f,(p-1)//2,p)[p:] or [0]
            for x in range(p):
                for y in range(1,p):
                    if y*y%p!=C.peval(f,x,p):continue
                    alpha,end=C.miller_constant((x,y),n,A,p)
                    assert end is None
                    assert alpha==y*C.peval(vv,x,p)%p
                    ct['cubic_uniform_identity']+=1
        for d in (3,4):
            for _ in range(15):
                while True:
                    f=[rng.randrange(p) for _ in range(d)]+[rng.randrange(1,p)]
                    if C.squarefree(f,p):break
                check(p,f,ct,rng)
    assert U.value(5,[0,3,0,1],1,-4)==1
    return dict(ct)


def freeze():
    fs={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
        for n in ['uniform_order.py','cm_character_route.py','verify_uniform_order.py']}
    h=hashlib.sha256(json.dumps(fs,sort_keys=True).encode()).hexdigest()
    (ROOT/'FREEZE.json').write_text(json.dumps({'files':fs,'digest':h},indent=2)+'\n')
    return {'digest':h}


def confirmation():
    fr=json.loads((ROOT/'FREEZE.json').read_text())
    for n,h in fr['files'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h
    rng=random.Random(int(fr['digest'],16));ct=Counter()
    ps=[p for p in range(31,400) if all(p%d for d in range(2,int(p**.5)+1))]
    ps=rng.sample(ps,8)+[1009]
    for p in ps:
        for d in (3,4):
            for _ in range(20):
                while True:
                    f=[rng.randrange(p) for _ in range(d)]+[rng.randrange(1,p)]
                    if C.squarefree(f,p):break
                check(p,f,ct,rng)
    return {'digest':fr['digest'],'primes':ps,**dict(ct)}


if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'development'
    out={'mode':mode,'status':'PASS',**{'development':development,'freeze':freeze,'confirmation':confirmation}[mode]()}
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/(mode+'.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
