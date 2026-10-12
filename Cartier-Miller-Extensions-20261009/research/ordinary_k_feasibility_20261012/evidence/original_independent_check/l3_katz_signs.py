"""Numerical check of the signs in Katz's Section-6 character-sum formulas, in Katz's own model
y^2 = f(x) = 4x^3 - g2 x - g3, with a_p = [x^(p-1)] f^h, b_p = [x^(p-2)] f^h (mod p), nu = quadratic character, nu(0)=0."""
from common import *
out = open('l3_katz_signs_results.txt', 'w')
for p in (5, 7, 11, 13, 17, 19, 23, 29, 31):
    h = (p - 1) // 2
    cnt = {'a=+S0': 0, 'a=-S0': 0, 'b=+S1': 0, 'b=-S1': 0}
    n = 0
    for g2 in range(p):
        for g3 in range(p):
            if (g2 ** 3 - 27 * g3 ** 2) % p == 0:
                continue
            f = ptrim([(-g3) % p, (-g2) % p, 0, 4])
            fh = ppow(f, h, p)
            a, b = coeff(fh, p - 1), coeff(fh, p - 2)
            S0 = sum(legendre(4 * t ** 3 - g2 * t - g3, p) for t in range(p)) % p
            S1 = sum(t * legendre(4 * t ** 3 - g2 * t - g3, p) for t in range(p)) % p
            n += 1
            cnt['a=+S0'] += (a == S0); cnt['a=-S0'] += (a == (-S0) % p)
            cnt['b=+S1'] += (b == S1); cnt['b=-S1'] += (b == (-S1) % p)
    line = f"p={p}: {n} models; " + ", ".join(f"{k}: {v}" for k, v in cnt.items())
    print(line); out.write(line + '\n')
out.close()
