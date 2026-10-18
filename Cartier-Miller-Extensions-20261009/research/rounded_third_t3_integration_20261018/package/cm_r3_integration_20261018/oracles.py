"""Independent definition-level oracles; no elliptic/Jacobi/factorial reduction."""
from math import comb


def direct(p):
    L, m, h = (p + 1) // 3, (p - 2) // 3, (p - 1) // 2
    # T_i / D_i = t_i; S_i / D_i = sum_{j<i} (h+1+j)t_j.
    T, D, S, U_m = 1, 1, 0, None
    # A_i/E_i = binom(2i,i)/8**i; C_i/E_i = strict prefix.
    A, E, C = 1, 1, 0
    for i in range(L):
        if i == m:
            U_m = S * pow(D, -1, p) % p
        d = 2 * i + 2
        S = (S + (h + 1 + i) * T) * d % p
        T = T * (h + 2 + i) % p
        D = D * d % p
        factor = 4 * (i + 1)
        C = (C + A) * factor % p
        A = A * (2 * i + 1) % p
        E = E * factor % p
    return dict(p=p, B_L=C * pow(E, -1, p) % p,
                a_L=A * pow(E, -1, p) % p, U_p_L=S * pow(D, -1, p) % p,
                U_p_m=U_m)


def integer_binomial(p):
    L = (p + 1) // 3
    if p < 20000:
        value = comb(2 * L, L) % p
    else:
        numerator = denominator = 1
        for j in range(1, L + 1):
            numerator = numerator * (L + j) % p
            denominator = denominator * j % p
        value = numerator * pow(denominator, -1, p) % p
    return value * pow(8, -L, p) % p
