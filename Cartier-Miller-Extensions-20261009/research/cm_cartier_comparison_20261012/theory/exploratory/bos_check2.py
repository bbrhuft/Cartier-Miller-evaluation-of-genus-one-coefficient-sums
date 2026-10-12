import cypari2, time
pari=cypari2.Pari()
pari.allocatemem(4*10**9)
t=time.time()
pari('P2 = polmodular(2);')                    # in x,y
pari('P2xz = subst(P2, y, z); P2zy = subst(P2, x, z);')
pari('R4 = polresultant(P2xz, P2zy, z);')
pari('Q4 = R4 / (x-y)^3;')
pari('P4 = Q4 / pollead(pollead(Q4,x),y) * 1;')
print('Phi4 deg', pari('poldegree(P4,x)'), 'time', time.time()-t)
pari('P4zy = subst(P4, x, z);')
pari('R8 = polresultant(P2xz, P4zy, z);')
pari('Q8 = R8 / P2^2;')
print('Phi8 deg', pari('poldegree(Q8,x)'), pari('poldegree(Q8,y)'), 'time', time.time()-t)
def bos(Pname, j0):
    pari(f'PP = subst(subst({Pname}, x, X+({j0})), y, Y+({j0}));')
    c=lambda i,k: pari(f'polcoef(polcoef(PP,{i},X),{k},Y)')
    b00,b01,b02,b11=c(0,0),c(0,1),c(0,2),c(1,1)
    gam=(2*b02-b11)/b01; j=pari(j0)
    return b00, gam, 6*j*gam+(7*j-6912)/(j-1728)
print('D=-8 via Phi_8 :', bos('Q8', 8000))
# sanity: is Q8 symmetric and monic-ish
print('symmetric:', pari('Q8 - subst(subst(subst(Q8,x,w),y,x),w,y) == 0'))
print('lead', pari('pollead(pollead(Q8,x),y)'))
