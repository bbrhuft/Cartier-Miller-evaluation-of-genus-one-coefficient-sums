"""Regression check of the values quoted in the 18 October rounded-third handover.

1. The four control rows (p = 11, 17, 23, 29) are recomputed from the
   definitions: integer binomials for a_i and B_j, the original weighted
   recurrence t_i for U_p(j), and a direct factorial for G = m! mod p.
   Every displayed identity is checked, including the p = 17 case where the
   boundary multiplier 2L(2L+5) vanishes.
2. At p = 7,000,000,009,553 the recorded tuple (B_L, a_L, U_p(L), G) is
   checked for internal consistency (a_L = 3/(2G^3), U_p(L) = 4B_L - 17/(3G^3),
   and the inverse cube-root formula), and B_L is recomputed with this
   release's retained O(log p) prefix routine, retained/elliptic_prefix.py.
   G itself is not recomputed (about 2.3e12 multiplications).

These are small regression inputs and a cross-check against code already in
this repository, not new held-out evidence. Standard library only. Exits 1 on
any failure.
"""
import json
import random
import sys
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent.parent / 'retained'))
import elliptic_prefix  # noqa: E402

HANDOVER_ROWS = {  # p: (B_L, a_L, U_p(L), G, U_p(m)) as printed in the handover
    11: (8, 1, 5, 6, 4), 17: (6, 10, 7, 1, 13), 23: (7, 9, 17, 3, 19), 29: (13, 21, 21, 3, 16)}
LARGE_P = 7000000009553
LARGE_TUPLE = (4770090998586, 303509152059, 6267107181755, 2406416797142)


def is_prime(n):
    if n < 2:
        return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):  # deterministic below 3.3e24
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def control_row(p):
    inv = lambda x: pow(x % p, -1, p)
    h, m = (p - 1) // 2, (p - 2) // 3
    L = m + 1
    a = lambda i: comb(2 * i, i) * pow(inv(8), i, p) % p
    B = lambda j: sum(a(i) for i in range(j)) % p

    def U(j):  # original weighted recurrence, independent of the telescoping identity
        t, s = 1, 0
        for i in range(j):
            s = (s + (h + 1 + i) * t) % p
            t = t * (h + 2 + i) * inv(2 * i + 2) % p
        return s
    G = factorial(m) % p
    G3 = pow(G, 3, p)
    checks = {
        'telescoping_L': U(L) == (4 * B(L) - 2 * L * (2 * L + 5) * a(L)) % p,
        'a_L = 3/(2G^3)': a(L) == 3 * inv(2 * G3) % p,
        'G = (3/(2a_L))^((2p-1)/3)': G == pow(3 * inv(2 * a(L)), (2 * p - 1) // 3, p),
        'a_m = -4a_L': a(m) == -4 * a(L) % p,
        'B_m = B_L + 4a_L': B(m) == (B(L) + 4 * a(L)) % p,
        'U(L) = 4B_L - 17/(3G^3)': U(L) == (4 * B(L) - 17 * inv(3 * G3)) % p,
        'U(m) = 4B_L - 16/(3G^3)': U(m) == (4 * B(L) - 16 * inv(3 * G3)) % p,
        'U(L) - U(m) = -1/(3G^3) != 0': (U(L) - U(m)) % p == -inv(3 * G3) % p != 0,
    }
    return (B(L), a(L), U(L), G, U(m)), checks


def main():
    failures, rows = [], {}
    for p, printed in HANDOVER_ROWS.items():
        computed, checks = control_row(p)
        rows[p] = {'computed': computed, 'matches_handover': computed == printed, 'identities': checks}
        if computed != printed:
            failures.append(f'p={p}: computed {computed}, handover {printed}')
        failures += [f'p={p}: {k}' for k, ok in checks.items() if not ok]
    p = LARGE_P
    BL, aL, UL, G = LARGE_TUPLE
    inv = lambda x: pow(x % p, -1, p)
    G3 = pow(G, 3, p)
    prefix = elliptic_prefix.third(p, rng=random.Random(20261018))
    large = {'p_is_prime': is_prime(p), 'p_mod_6': p % 6,
             'a_L = 3/(2G^3)': aL == 3 * inv(2 * G3) % p,
             'U(L) = 4B_L - 17/(3G^3)': UL == (4 * BL - 17 * inv(3 * G3)) % p,
             'G = (3/(2a_L))^((2p-1)/3)': G == pow(3 * inv(2 * aL), (2 * p - 1) // 3, p),
             'retained_prefix_B': prefix['B'], 'retained_prefix_matches_B_L': prefix['B'] == BL,
             'G_recomputed': False}
    failures += [f'p={p}: {k}' for k, v in large.items() if v is False and k != 'G_recomputed']
    if large['p_mod_6'] != 5:
        failures.append(f'p={p}: not 5 mod 6')
    out = {'status': 'failed' if failures else 'passed', 'control_rows': rows,
           'largest_confirmation_prime': {'p': p, 'tuple': LARGE_TUPLE, **large},
           'failures': failures,
           'scope': 'regression check of handover values; not new held-out evidence'}
    print(json.dumps(out, indent=2))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
