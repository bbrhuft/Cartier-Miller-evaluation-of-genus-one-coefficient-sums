"""Algebraic identification of the CM order (no analytic matching needed).
Each loop endomorphism alpha has (lambda-mu)^2 = D, so Z[alpha] is the order
of discriminant D and End(E) is an order O' containing it, disc(O') = D/k^2
with k | f (f = conductor of D).  CM degree theorem: [Q(j):Q] = h(O').
Checks: the exact minimal polynomial of j (from cm_tables.json) is
irreducible of degree h(D); every proper overorder has class number < deg
(or, at depth one, the overorder's j is 0 or 1728, which differs from j).
Hence End(E) has discriminant exactly D and the j polynomial is H_D."""
import json, sys
import cypari2
pari = cypari2.Pari()
here = __file__.rsplit('/theory/', 1)[0]
tabs = json.load(open(here + '/results/cm_tables.json'))
loops = json.load(open(here + '/results/family_loops.json'))
out = []; ok_all = True
for name, v in tabs.items():
    D = v['D']; H = v['H_D_low_to_high']; deg = len(H) - 1
    P = pari(f'Pol({list(reversed(H))})')
    irreducible = bool(pari.polisirreducible(P))
    lm = loops[name]
    disc_ok = lm['lambda_minus_mu_squared'] == str(D)
    fund = int(pari(f'coredisc({D})')); f = int(round((D / fund) ** 0.5))
    over = []
    for k in range(2, f + 1):
        if f % k == 0:
            Dk = D // (k * k)
            hk = int(pari(f'qfbclassno({Dk})'))
            over.append({'k': k, 'disc': Dk, 'class_number': hk})
    hD = int(pari(f'qfbclassno({D})'))
    jval = None if deg > 1 else -H[0]
    if deg == 1:
        excluded = all((o['disc'] == -3 and jval != 0) or (o['disc'] == -4 and jval != 1728) or o['class_number'] < deg for o in over)
    else:
        excluded = all(o['class_number'] < deg for o in over)
    ok = disc_ok and irreducible and deg == hD and excluded
    ok_all &= ok
    out.append({'family': name, 'D': D, 'conductor': f, 'loop_lambda_minus_mu_squared': lm['lambda_minus_mu_squared'], 'loop_disc_equals_D': disc_ok,
                'deg_j_minpoly': deg, 'h(D)': hD, 'irreducible': irreducible, 'proper_overorders': over,
                'overorders_excluded': excluded, 'End_has_disc_D': ok})
    print(out[-1])
json.dump(out, open(here + '/results/order_argument.json', 'w'), indent=1)
print('ORDER_ARGUMENT_OK' if ok_all else 'ORDER_ARGUMENT_FAILED')
sys.exit(0 if ok_all else 1)
