"""Reproduce quadratic-algebra norms, j polynomials, evaluations and resultant."""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent

def mul(x,y,n):
    return (x[0]*y[0]+n*x[1]*y[1],x[0]*y[1]+x[1]*y[0])

def qpow(x,k,n):
    r=(1,0)
    for _ in range(k):r=mul(r,x,n)
    return r

def factor(v):
    v=abs(v);out={};q=2
    while q*q<=v:
        if v%q==0:
            t=0
            while v%q==0:v//=q;t+=1
            out[str(q)]=t
        q+=1 if q==2 else 2
    if v>1:out[str(v)]=1
    return out

def det4(M):
    v=0
    for pp in itertools.permutations(range(4)):
        z=(-1)**sum(pp[i]>pp[j] for i in range(4) for j in range(i+1,4))
        for i,j in enumerate(pp):z*=M[i][j]
        v+=z
    return v

families={}
for n,a,g,m in [(2,(-91,-60),(-462,-308),8),(3,(-135,-60),(-694,-420),12)]:
    a3=qpow(a,3,n);g2=qpow(g,2,n)
    Delta=tuple(4*x+27*y for x,y in zip(a3,g2))
    vals={'norm_alpha':a[0]**2-n*a[1]**2,
          'norm_gamma':g[0]**2-n*g[1]**2,
          'extraction_determinant':a3[1]*g2[0]-g2[1]*a3[0],
          'norm_discriminant':Delta[0]**2-n*Delta[1]**2}
    # Polynomial in u=B²/A³ from n(a1 u-g1)²-(g0-a0 u)².
    a0,a1=a3;g0,g1=g2
    F=[n*g1*g1-g0*g0,-2*n*a1*g1+2*g0*a0,n*a1*a1-a0*a0]
    common=math.gcd(*F);F=[x//common for x in F]
    # Substitute u=(6912-4J)/(27J), clear denominator, primitive monic result.
    P=[F[2]*6912**2,F[1]*27*6912-8*6912*F[2],
       F[0]*729-108*F[1]+16*F[2]]
    common=math.gcd(*P);P=[x//common for x in P]
    if P[2]<0:P=[-x for x in P]
    assert P[2]==1
    # Verify the polynomial by substituting its rational quadratic-algebra j.
    D0,D1=Delta;den=D0**2-n*D1**2
    num=mul(tuple(6912*x for x in a3),(D0,-D1),n)
    # P(j) times den²; purely integer quadratic-algebra identity.
    jj=mul(num,num,n)
    residual=tuple(jj[i]+P[1]*num[i]*den+(P[0]*den*den if i==0 else 0) for i in range(2))
    assert residual==(0,0)
    evaluations={str(J):{'value':sum(P[i]*J**i for i in range(3)),
                         'factorization':factor(sum(P[i]*J**i for i in range(3)))}
                 for J in (0,1728,287496,54000)}
    for row in evaluations.values():
        assert all(int(q)%m!=1 for q in row['factorization'] if int(q)>=7)
    for name,val in vals.items():
        assert all(int(q)%m!=1 for q in factor(val) if int(q)>=7)
    families[str(n)]={'alpha':a,'gamma':g,'alpha_cubed':a3,'gamma_squared':g2,
                      'discriminant_pair':Delta,'integers':vals,
                      'factorizations':{k:factor(v) for k,v in vals.items()},
                      'invariant_polynomial_u':F,'polynomial_j':P,'lower_j_evaluations':evaluations}
f=families['2']['polynomial_j'];g=families['3']['polynomial_j']
M=[[f[2],f[1],f[0],0],[0,f[2],f[1],f[0]],
   [g[2],g[1],g[0],0],[0,g[2],g[1],g[0]]]
R=det4(M)
assert all(int(q)%24!=1 for q in factor(R) if int(q)>=7)
result={'families':families,'mixed_resultant':R,'mixed_resultant_factorization':factor(R),
        'all_ordinary_collision_exclusions_pass':True,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'integer_invariants.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'j_polynomials':{k:v['polynomial_j'] for k,v in families.items()},
                  'mixed_resultant':R,'all_passed':True},indent=2))
