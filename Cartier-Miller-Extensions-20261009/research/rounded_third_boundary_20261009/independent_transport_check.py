"""Fresh standard-library cross-check run on 9 October before the rounded-third work.

Brute-force (dense power) check of rooted 2-isogeny transport A'=-4A-15q^2, B'=-8Aq-22q^3,
H'=H, beta'=2beta-qH on random curves with rational 2-torsion x=q, 11<=p<400, and of the
depth-one A=0 seed relation beta=-rH for A=-15r^2, B=-22r^3, p=1 mod 3. Seeded; not proof.
"""
import random
def HB(A,B,p):
    # coefficients of x^(p-1), x^(p-2) in (x^3+Ax+B)^h
    h=(p-1)//2; v=[1]; c=[B%p,A%p,0,1]
    for _ in range(h):
        n=[0]*(len(v)+3)
        for i,a in enumerate(v):
            if a:
                for j,b in enumerate(c):
                    if b: n[i+j]=(n[i+j]+a*b)%p
        v=n
    return v[p-1], v[p-2]
def primes(lo,hi):
    return [n for n in range(lo,hi) if all(n%d for d in range(2,int(n**.5)+1))]
rng=random.Random(1); ok=bad=0
for p in primes(11,400):
    for _ in range(6):
        q=rng.randrange(p); A=rng.randrange(p); B=(-q**3-A*q)%p   # q is a 2-torsion x
        if (4*A**3+27*B*B)%p==0: continue
        A2=(-4*A-15*q*q)%p; B2=(-8*A*q-22*q**3)%p
        if (4*A2**3+27*B2*B2)%p==0: continue
        H,b=HB(A,B,p); H2,b2=HB(A2,B2,p)
        if H2==H and b2==(2*b-q*H)%p: ok+=1
        else: bad+=1
fam=0
for p in primes(13,400):
    if p%3!=1: continue
    r=rng.randrange(1,p); H,b=HB(-15*r*r,-22*r**3,p)
    assert b==(-r*H)%p; fam+=1
print("transport ok",ok,"bad",bad,"| depth-one A=0 family checks",fam)
