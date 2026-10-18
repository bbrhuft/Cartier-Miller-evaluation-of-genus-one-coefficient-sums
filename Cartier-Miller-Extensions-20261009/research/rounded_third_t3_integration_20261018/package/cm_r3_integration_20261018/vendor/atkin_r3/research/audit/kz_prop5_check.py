"""D = A_n'(0) from KZ Prop. 5 top coefficients vs Wronskian product (independent code)."""
def isprime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
def poch(a_num,a_den,L,p):  # (a)_L mod p, a = a_num/a_den
    a=a_num*pow(a_den,p-2,p)%p; r=1
    for i in range(L): r=r*(a+i)%p
    return r
def fact(L,p):
    r=1
    for i in range(1,L+1): r=r*i%p
    return r
def wronskian(p):
    N=(p-5)//12; eps=int(p%12==11); n=N+1+eps
    W=273*pow(2,p-2,p)%p
    for j in range(1,n-1): W=W*(-6)*(12*j+7)*(12*j+13)*pow((j+1)*(2*j+1),p-2,p)%p
    return W
bad=[]
ps=[p for p in range(11,20000) if p%6==5 and isprime(p)]
for p in ps:
    N=(p-5)//12; F2=pow(fact(N,p),2*(p-2),p)
    if p%12==5: D=pow(1728,N,p)*poch(1,12,N,p)*poch(5,12,N,p)*F2%p
    else: D=-pow(1728,N+1,p)*poch(7,12,N,p)*poch(11,12,N,p)*F2%p
    # reflection forms
    R=poch(4,3,N,p)*pow(fact(N,p),p-2,p)%p
    Dref=(pow(1728,N,p)*R if p%12==5 else -pow(1728,N+1,p)*R)%p
    if not (D==wronskian(p)==Dref): bad.append(p)
print(len(ps),'primes; mismatches:',bad[:10])
