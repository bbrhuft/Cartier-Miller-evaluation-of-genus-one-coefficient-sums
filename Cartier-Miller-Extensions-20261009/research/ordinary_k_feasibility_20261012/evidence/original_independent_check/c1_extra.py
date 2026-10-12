"""Extra C1 checks: (i) Kedlaya matrix mod p is independent of the integral lift (random lifts A+p*r, B+p*s);
(ii) behaviour at p = 5 (outside the claim's range, informational); (iii) rank of M mod p is always 1 ((H,beta) != (0,0))."""
import random
from common import *
from c1_kedlaya import frob_matrix, fr_mod
from c1_cech import frobenius_cech
random.seed(99)
out = open('c1_extra_results.txt', 'w')
for p in (7, 11, 13):
    ok = n = 0; fails = []
    for A, B in all_models(p):
        H, beta = hasse_beta(p, A, B)
        At, Bt = A + p * random.randrange(1, p**3), B + p * random.randrange(1, p**3)
        M, prec = frob_matrix(p, At, Bt, 4, 6)
        Mi = [[fr_mod(M[r][c], p**2, p) for c in range(2)] for r in range(2)]
        t = trace(p, A, B)
        n += 1
        good = ((Mi[0][0] + Mi[1][1]) % p**2 == t % p**2 and (Mi[0][0]*Mi[1][1]-Mi[0][1]*Mi[1][0]) % p**2 == p
                and [[x % p for x in r] for r in Mi] == [[0, (-beta) % p], [0, H]])
        ok += good
        if not good: fails.append((A, B, At, Bt, Mi))
    line = f"Kedlaya with random integral lifts, p={p}: {ok}/{n} models give trace=t, det=p mod p^2 and M mod p = [[0,-beta],[0,H]]; fails={fails[:3]}"
    print(line); out.write(line + '\n')
# rank-1 check
for p in (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
    bad = [(A, B) for A, B in all_models(p) if hasse_beta(p, A, B) == (0, 0)]
    line = f"p={p}: models with H = beta = 0 (would make F^* zero mod p): {bad}"
    print(line); out.write(line + '\n')
# p = 5
p = 5
okc = okk = n = 0; det = []
for A, B in all_models(p):
    H, beta = hasse_beta(p, A, B)
    c, Mc = frobenius_cech(p, A, B)
    n += 1
    okc += (Mc == [[0, (-beta) % p], [0, H]])
    M, prec = frob_matrix(p, A, B, 5, 8)
    try:
        Mi = [[fr_mod(M[r][c], p**2, p) for c in range(2)] for r in range(2)]
        okk += ([[x % p for x in r] for r in Mi] == [[0, (-beta) % p], [0, H]])
    except ValueError as e:
        det.append((A, B, 'nonintegral'))
line = f"p=5 (outside claim): Cech route matches [[0,-beta],[0,H]] for {okc}/{n}; Kedlaya route for {okk}/{n}; nonintegral={det[:5]}"
print(line); out.write(line + '\n')
out.close()
