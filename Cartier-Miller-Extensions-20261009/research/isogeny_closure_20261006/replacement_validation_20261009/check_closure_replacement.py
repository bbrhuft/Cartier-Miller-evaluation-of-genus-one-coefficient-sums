"""Replacement validator for the normalized rational 2-isogeny closure (written 9 October 2026).

The original check_closure.py and its validation.csv/json, described in
theory/ISOGENY_CLOSURE_THEORY.md, were not retained in the transfer archive. This
script is a fresh reconstruction of that documented scope. It is NOT the lost
original, and it imports nothing from the research code: every H and beta is read
from a dense power (x^3 + A x + B)^h with h=(p-1)/2, where H=[x^(p-1)] and
beta=[x^(p-2)].

Checks, standard library only:
  T. rooted transport, exhaustive over 7 <= p < 60: for every A and every rational
     kernel root q (B = -q^3 - A q), with source and quotient nonsingular,
     A' = -4A - 15q^2, B' = -8Aq - 22q^3, H' = H and beta' = 2 beta - q H;
  D. dual normalization on the same cases: q' = -2q is a root on the quotient, the
     second quotient is (16A, 64B), and beta'' = 4 beta, H'' = H, as the square
     scaling x = 4X predicts;
  C. seeded random rooted chains of 1..4 edges for 7 <= p < 150:
     beta_0 = H * sum_i q_i / 2^(i+1) + beta_m / 2^m;
  F. every depth-one and depth-two family row of RESULTS.md, for all nonzero r and
     both square roots e, for p < 200 in the stated congruence class (singular
     members skipped and counted).

Run from the repository root:
    python research/isogeny_closure_20261006/replacement_validation_20261009/check_closure_replacement.py
Finite evidence only; no timings are benchmarks.
"""
import json
import platform
import random
import sys
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def primes(lo, hi):
    return [n for n in range(max(lo, 2), hi) if all(n % d for d in range(2, int(n**0.5) + 1))]


def h_beta(A, B, p):
    h = (p - 1)//2
    base = [B % p, A % p, 0, 1]
    v = [1]
    for _ in range(h):
        n = [0]*(len(v) + 3)
        for i, x in enumerate(v):
            if x:
                for j, y in enumerate(base):
                    if y:
                        n[i + j] = (n[i + j] + x*y) % p
        v = n
    return v[p - 1], v[p - 2]


def nonsingular(A, B, p):
    return (4*A**3 + 27*B*B) % p != 0


def quotient(A, B, q, p):
    assert (q**3 + A*q + B) % p == 0
    return (-4*A - 15*q*q) % p, (-8*A*q - 22*q**3) % p


def roots(A, B, p):
    return [x for x in range(p) if (x**3 + A*x + B) % p == 0]


def sqrt_mod(n, p):
    return [x for x in range(p) if x*x % p == n % p]


FAMILIES = [
    # name, modulus condition, extra square, A(r,e), B(r,e), beta multiplier m(r,e) with beta = m H
    ('depth1_B0', lambda p: p % 4 == 1, None, lambda r, e: -11*r*r, lambda r, e: -14*r**3, lambda r, e: -r),
    ('depth1_A0', lambda p: p % 3 == 1, None, lambda r, e: -15*r*r, lambda r, e: -22*r**3, lambda r, e: -r),
    ('depth2_B0', lambda p: p % 8 == 1, 2, lambda r, e: (-91 - 60*e)*r*r, lambda r, e: (-462 - 308*e)*r**3, lambda r, e: -(3 + 2*e)*r),
    ('depth2_A0', lambda p: p % 12 == 1, 3, lambda r, e: (-135 - 60*e)*r*r, lambda r, e: (-694 - 420*e)*r**3, lambda r, e: -(3 + 2*e)*r),
]


def main():
    counts = {'transport_cases': 0, 'transport_primes': [], 'singular_quotients_skipped': 0,
              'dual_cases': 0, 'chain_cases': 0, 'chain_edges': 0,
              'family_members': {}, 'family_singular_skipped': {}, 'failures': 0}
    cache = {}

    def hb(A, B, p):
        key = (A % p, B % p, p)
        if key not in cache:
            cache[key] = h_beta(A, B, p)
        return cache[key]

    # T and D
    for p in primes(7, 60):
        counts['transport_primes'].append(p)
        for A in range(p):
            for q in range(p):
                B = (-q**3 - A*q) % p
                if not nonsingular(A, B, p):
                    continue
                A1, B1 = quotient(A, B, q, p)
                if not nonsingular(A1, B1, p):
                    counts['singular_quotients_skipped'] += 1
                    continue
                H, b = hb(A, B, p)
                H1, b1 = hb(A1, B1, p)
                assert H1 == H and b1 == (2*b - q*H) % p, ('T', p, A, B, q)
                counts['transport_cases'] += 1
                q1 = (-2*q) % p
                A2, B2 = quotient(A1, B1, q1, p)
                assert (A2, B2) == ((16*A) % p, (64*B) % p), ('D', p, A, B, q)
                H2, b2 = hb(A2, B2, p)
                assert H2 == H and b2 == (4*b) % p == (2*b1 - q1*H1) % p, ('D2', p, A, B, q)
                counts['dual_cases'] += 1
    # C
    rng = random.Random(20261009)
    for p in primes(7, 150):
        inv2 = pow(2, -1, p)
        for _ in range(12):
            while True:
                A, q = rng.randrange(p), rng.randrange(p)
                B = (-q**3 - A*q) % p
                if nonsingular(A, B, p):
                    break
            H0, b0 = hb(A, B, p)
            qs, cur = [], (A, B)
            for _ in range(rng.randint(1, 4)):
                rs = roots(*cur, p)
                if not rs:
                    break
                r = rng.choice(rs)
                nxt = quotient(*cur, r, p)
                if not nonsingular(*nxt, p):
                    break
                qs.append(r)
                cur = nxt
            if not qs:
                continue
            Hm, bm = hb(*cur, p)
            m = len(qs)
            pred = (H0*sum(qi*pow(inv2, i + 1, p) for i, qi in enumerate(qs)) + bm*pow(inv2, m, p)) % p
            assert Hm == H0 and pred == b0, ('C', p, A, B, qs)
            counts['chain_cases'] += 1
            counts['chain_edges'] += m
    # F
    for name, cond, sq, Af, Bf, mf in FAMILIES:
        n = skipped = 0
        for p in primes(7, 200):
            if not cond(p):
                continue
            es = [0] if sq is None else sqrt_mod(sq, p)
            assert sq is None or len(es) == 2, (name, p)
            for e in es:
                for r in range(1, p):
                    A, B = Af(r, e) % p, Bf(r, e) % p
                    if not nonsingular(A, B, p):
                        skipped += 1
                        continue
                    H, b = hb(A, B, p)
                    assert b == (mf(r, e)*H) % p, (name, p, e, r)
                    n += 1
        counts['family_members'][name] = n
        counts['family_singular_skipped'][name] = skipped
    counts.update(status='passed', seed=20261009,
                  scope='replacement reconstruction of the documented closure checks; independent dense powers; finite evidence, not proof',
                  python=sys.version, platform=platform.platform(),
                  source_sha256={'check_closure_replacement.py': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    (HERE/'validation.json').write_text(json.dumps(counts, indent=2) + '\n')
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    main()
