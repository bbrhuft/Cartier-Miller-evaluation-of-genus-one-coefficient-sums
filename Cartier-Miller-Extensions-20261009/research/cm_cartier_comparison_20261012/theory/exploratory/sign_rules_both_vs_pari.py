import cypari2, math, random
pari=cypari2.Pari()
def leg(a,p):
    a%=p
    return 0 if a==0 else (1 if pow(a,(p-1)//2,p)==1 else -1)
def sqrtm(n,p):
    return int(pari(f'lift(sqrt(Mod({n},{p})))'))
def corn7(p):
    for v in range(1, math.isqrt(4*p//7)+1):
        r=4*p-7*v*v; t=math.isqrt(r)
        if t*t==r: return t,v
rng=random.Random(1)
bad=0;n=0;incons=0
for p in pari('primes([11,60000])'):
    p=int(p)
    if p%7 not in (1,2,4): continue
    t0,v0=corn7(p)
    e=sqrtm(-7,p)
    for r in [1, rng.randrange(2,p)]:
        A=-35*r*r%p; B=-98*r**3%p
        q=r*(-7+e)*pow(2,-1,p)%p; e2=7*r%p; e3=r*(-7-e)*pow(2,-1,p)%p
        u=(1+e)*pow(2,-1,p)%p
        s1=leg(q-e2,p); s2=leg(q-e3,p)
        if s1!=s2: incons+=1
        v = v0 if (t0 + v0*e)%p==0 else -v0
        assert (t0+v*e)%p==0
        x0=(t0-v)//2; y0=v
        Pplus = (x0%2==1) and (((x0-1)//2 + y0)%2==0)
        t = t0 if (Pplus == (s1==1)) else -t0
        ap=int(pari(f'ellap(ellinit([{A},{B}]),{p})'))
        hecke = (t0 if leg(t0,7)==1 else -t0)*leg(r,p)
        n+=1
        if ap!=t or ap!=hecke: bad+=1; print('mismatch',p,r,ap,t,hecke)
print('2-adic and Hecke rules checked',n,'cases; mismatches',bad,'; s1!=s2 cases',incons)
