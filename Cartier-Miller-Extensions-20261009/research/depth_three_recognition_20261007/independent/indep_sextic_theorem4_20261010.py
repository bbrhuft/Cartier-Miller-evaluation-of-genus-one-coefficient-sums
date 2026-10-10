"""Independent check of Ireland & Rosen (1990), Ch. 18, Sec. 3, Theorem 4, written 10 October 2026.

Uses no project code: complex arithmetic in Z[omega], primary primes from PARI qfbsolve,
and compares the theorem trace with PARI ellap. Needs cypari2. Seeded; finite evidence only.
"""
import random, cypari2
pari=cypari2.Pari()
W=complex(-0.5, 3**0.5/2)
UNITS=[(1,0),(0,1),(-1,-1),(-1,0),(0,-1),(1,1)]
def primary(p):
    q=pari.qfbsolve(pari.Qfb(1,-1,1),p); u=(int(q[0]),int(q[1]))
    for _ in range(3):
        for v in (u,(-u[0],-u[1])):
            if v[0]%3==2 and v[1]%3==0: return v
        u=(-u[1],u[0]-u[1])                       # times omega
    raise RuntimeError(p)
def trace_thm4(p,D,pi):
    a,b=pi; assert a*a-a*b+b*b==p
    s=int(pari(f'lift(sqrt(Mod(-3,{p})))')); h=pow(2,-1,p)
    w=next(r for r in ((-1+s)*h%p,(-1-s)*h%p) if (a+b*r)%p==0)
    val=pow(4*D%p,(p-1)//6,p)
    z=next(u for u in UNITS if (u[0]+u[1]*w)%p==val)
    return -round(2*((z[0]+z[1]*W).conjugate()*(a+b*W)).real)
rng=random.Random(20261010); n=0
for p in [q for q in range(7,3000) if q%3==1 and pari.isprime(q)]:
    pi=primary(p)
    for D in rng.sample(range(1,p),min(10,p-1)):
        assert trace_thm4(p,D,pi)==int(pari.ellap(pari.ellinit([0,0,0,0,D]),p)),(p,D); n+=1
for bits in (40,48,52):
    for _ in range(3):
        p=int(pari.nextprime(rng.getrandbits(bits)))
        while p%3!=1: p=int(pari.nextprime(p+1))
        D=rng.randrange(1,p)
        assert trace_thm4(p,D,primary(p))==int(pari.ellap(pari.ellinit([0,0,0,0,D]),p)),(p,D); n+=1
assert trace_thm4(13,1,(-1,3))==2
print("Theorem 4 independent check passed on",n,"curves, primes up to ~52 bits, plus the p=13 book example")
