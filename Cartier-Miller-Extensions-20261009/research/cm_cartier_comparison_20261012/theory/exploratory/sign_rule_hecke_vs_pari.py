import cypari2, math
pari=cypari2.Pari()
def legendre(a,p): 
    a%=p
    if a==0: return 0
    return 1 if pow(a,(p-1)//2,p)==1 else -1
def corn7(p):
    # 4p = t^2 + 7 v^2, brute small
    for v in range(1, int(math.isqrt(4*p//7))+1):
        r=4*p-7*v*v
        t=math.isqrt(r)
        if t*t==r: return t,v
    return None
bad=0; n=0
for p in pari('primes([11,200000])'):
    p=int(p)
    if p%7 not in (1,2,4): continue
    t0,v0=corn7(p)
    ap=int(pari(f'ellap(ellinit([-35,-98]),{p})'))
    pred = t0 if legendre(t0,7)==1 else -t0     # (t0/7)*t0
    n+=1
    if ap!=pred: bad+=1; 
    if bad and bad<5 and ap!=pred: print('mismatch',p,t0,ap)
print('Hecke rule checked',n,'primes, mismatches',bad)
