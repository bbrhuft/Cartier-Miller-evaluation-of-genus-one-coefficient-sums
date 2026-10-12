from mpmath import mp, mpf, mpc, sqrt, pi, exp, nsum, inf, identify
mp.dps = 60
def eis(tau, N=400):
    q = exp(2j*pi*tau)
    s1=s3=s5=mpc(0)
    qn=mpc(1)
    for n in range(1,N):
        qn*=q
        t=qn/(1-qn)
        s1+=n*t; s3+=n**3*t; s5+=n**5*t
    E2=1-24*s1; E4=1+240*s3; E6=1-504*s5
    return E2,E4,E6
def s2(tau):
    E2,E4,E6=eis(tau)
    E2s=E2-3/(pi*tau.imag)
    j=1728*E4**3/(E4**3-E6**2)
    return E2s*E4/E6, j, E2s
for name,tau in [('-7',mpc(0.5,sqrt(7)/2)),('-8',mpc(0,sqrt(2))),('-12',mpc(0,sqrt(3))),('-16',mpc(0,2)),('-3',mpc(-0.5,sqrt(3)/2)),('-4',mpc(0,1))]:
    v,j,e2s=s2(tau)
    print(name, mp.nstr(v,30), mp.nstr(j,25), 'E2*=',mp.nstr(e2s,20))
print(5/mpf(21),5/mpf(14),5/mpf(11),11/mpf(21))
