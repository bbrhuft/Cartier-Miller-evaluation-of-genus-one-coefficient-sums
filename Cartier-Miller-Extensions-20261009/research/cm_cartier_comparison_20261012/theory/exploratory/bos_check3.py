import cypari2
pari=cypari2.Pari()
def bos(ell, j0):
    pari(f'PP = subst(subst(polmodular({ell}), x, X+({j0})), y, Y+({j0}));')
    c=lambda i,k: pari(f'polcoef(polcoef(PP,{i},X),{k},Y)')
    b00,b01,b02,b11=c(0,0),c(0,1),c(0,2),c(1,1)
    gam=(2*b02-b11)/b01; j=pari(j0)
    return b00, 6*j*gam+(7*j-6912)/(j-1728)
for ell,j0,lab in [(2,8000,'D=-8, m=2 (sqrt-2)'),(2,-3375,'D=-7, m=2 ((1+sqrt-7)/2, trace 1)'),(7,-3375,'D=-7, m=7 (sqrt-7)'),(3,54000,'D=-12, m=3 (sqrt-3) special'),(11,-32768,'D=-11 m=11'),(19,-884736,'D=-19 m=19'),(5,632000+0,'D=-20? j not rational')]:
    try: print(lab, bos(ell,j0))
    except Exception as e: print(lab,'ERR',e)
