import cypari2
pari=cypari2.Pari()
pari.allocatemem(2*10**9)
from fractions import Fraction as Fr
def bos_s2(ell, j0):
    Phi = pari(f'polmodular({ell})')   # Phi(x,y) classical
    # Phi in variables x,y. Expand around (j0,j0)
    P = pari(f'subst(subst({Phi}, x, X+({j0})), y, Y+({j0}))')
    def coeff(i,k):
        return pari(f'polcoef(polcoef({P}, {i}, X), {k}, Y)')
    b01=coeff(0,1); b02=coeff(0,2); b11=coeff(1,1); b00=coeff(0,0)
    gam = (2*b02 - b11)/b01
    j=pari(j0)
    s2 = 6*j*gam + (7*j-6912)/(j-1728)
    return b00, b01, gam, s2
print('D=-7 via Phi_7:', bos_s2(7, -3375))
