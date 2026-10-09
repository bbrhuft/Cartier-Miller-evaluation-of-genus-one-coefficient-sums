"""Validation for the rounded supersingular third point, 9 October 2026.

Run from the export root:  python research/rounded_third_boundary_20261009/validate_rounded_third.py
Optional: --limit N (default 20000), --dense-limit N (default 600).

Standard library only. For every prime 5 <= p <= limit with p = 2 mod 3 it checks,
with m = (p-2)/3 and L = (p+1)/3:

  1. direct coefficient recurrences give a_m, a_L, B_L, and the ORIGINAL t_i weighted
     recurrence (manuscript eq. 32) gives U_p(L) and U_p(m) without using eq. (35);
  2. Theorem R:  a_m = -6/(m!)^3,  a_L = 3/(2 (m!)^3),  8^m = 1/2  (mod p);
  3. Corollary U: U_p(L) = 4 B_L - (17/3)/(m!)^3 and U_p(m) = 4 B_L + (8/9) a_m;
  4. Theorem E inversion: m! = (3/(2 a_L))^((2p-1)/3), and U -> a_L for p != 17;
  5. the branch bridge (B6): mu = 2^(-m) is the unique cube root of 2,
     T_f(mu) = -a_m/(3 mu) and a_L = (3 mu/4) T_f(mu); for p <= dense-limit T_f(mu)
     and H, K are recomputed from a dense power of 1 - w^3/2 (no sparsity assumed);
  6. the retained O(log p) prefix routine elliptic_prefix.third(p) returns B_L.

For contrast, primes p = 1 mod 3 up to min(limit, 5000) check the elementary
companion C(2L,L) = -1/(L!)^3 at L = (p-1)/3 and Jacobi's -r by brute-force r.
This is evidence, not proof, and contains no timing benchmark.
"""
import argparse
import csv
import hashlib
import json
import platform
import sys
from math import comb, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RETAINED = ROOT/'retained'   # unchanged copy of the original project's elliptic_prefix.py


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d*d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def direct(p):
    """O(p) recurrences straight from the definitions; no closed forms."""
    h, m = (p-1)//2, (p-2)//3
    L = m + 1
    a, B, t, U = 1, 0, 1, 0
    out = {}
    for i in range(L + 1):
        if i == m:
            out['a_m'], out['B_m'], out['U_m'] = a, B, U
        if i == L:
            out['a_L'], out['B_L'], out['U_L'] = a, B, U
            break
        B = (B + a) % p
        U = (U + (h + 1 + i)*t) % p                      # eq. (32), original weights
        t = t*(h + 2 + i)*pow(2*i + 2, -1, p) % p
        a = a*(2*i + 1)*pow(4*(i + 1), -1, p) % p
    return out


def factorial_mod(n, p):
    f = 1
    for i in range(2, n + 1):
        f = f*i % p
    return f


def dense_power_coeffs(p):
    """Coefficients of (1 - w^3/2)^h by repeated dense multiplication."""
    h, half = (p-1)//2, pow(2, -1, p)
    base = [1, 0, 0, (-half) % p]
    v = [1]
    for _ in range(h):
        n = [0]*(len(v) + 3)
        for i, x in enumerate(v):
            if x:
                for j, y in enumerate(base):
                    if y:
                        n[i+j] = (n[i+j] + x*y) % p
        v = n
    return v


def jacobi_r(p):
    for s in range(0, isqrt(4*p//27) + 1):
        r2 = 4*p - 27*s*s
        r = isqrt(r2)
        if r*r == r2:
            return r if r % 3 == 1 else -r
    raise AssertionError(p)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(limit, dense_limit, csv_path):
    sys.dont_write_bytecode = True   # keep the export free of __pycache__
    sys.path.insert(0, str(RETAINED))
    import elliptic_prefix  # retained O(log p) prefix routine (Theorem T')
    counts = dict(primes_2_mod_3=0, theorem_R_checks=0, corollary_U_checks=0,
                  inversion_checks=0, branch_bridge_checks=0, dense_power_checks=0,
                  retained_prefix_checks=0, U_to_a_recoveries=0,
                  p17_degenerate=None, contrast_primes_1_mod_3=0, failures=0)
    rows = []
    for p in range(5, limit + 1):
        if p % 3 != 2 or not is_prime(p):
            continue
        m, L = (p-2)//3, (p+1)//3
        d = direct(p)
        f = factorial_mod(m, p)
        inv = lambda x: pow(x, -1, p)
        # Theorem R
        assert pow(8, m, p) == inv(2), p
        assert d['a_m'] == (-6*inv(pow(f, 3, p))) % p, p
        assert d['a_L'] == 3*inv(2*pow(f, 3, p)) % p, p
        assert d['a_L'] == (-d['a_m']*inv(4)) % p, p
        counts['theorem_R_checks'] += 1
        # Corollary U, against the original weighted recurrence
        assert d['U_L'] == (4*d['B_L'] - 17*inv(3)*inv(pow(f, 3, p))) % p, p
        assert d['U_m'] == (4*d['B_L'] + 8*inv(9)*d['a_m']) % p, p
        assert d['U_L'] == (4*d['B_L'] - 34*inv(9)*d['a_L']) % p, p   # eq. (35) at L
        counts['corollary_U_checks'] += 1
        # Theorem E: inversions
        assert pow(3*inv(2*d['a_L']) % p, (2*p - 1)//3, p) == f, p
        if p != 17:
            assert (9*inv(34)*(4*d['B_L'] - d['U_L'])) % p == d['a_L'], p
            counts['U_to_a_recoveries'] += 1
        else:
            assert d['U_L'] == 4*d['B_L'] % p
            counts['p17_degenerate'] = {'p': 17, 'U_L': d['U_L'], 'B_L': d['B_L'],
                                        'note': '34/9 = 0 mod 17, so U_p(L) = 4 B_L'}
        counts['inversion_checks'] += 1
        # Branch bridge (B6)
        mu = pow(2, (-m) % (p-1), p)
        assert pow(mu, 3, p) == 2, p
        if p < 2000:   # uniqueness of the rational branch, by exhaustion
            assert [x for x in range(1, p) if pow(x, 3, p) == 2] == [mu], p
        T = 0
        a, w = 1, 1
        for i in range(m + 1):       # T_f(mu) = sum_{3i <= p-1} a_i mu^(3i), sparse form
            T = (T + a*w) % p
            w = w*2 % p
            a = a*(2*i + 1)*inv(4*(i + 1)) % p
        assert T == (-d['a_m']*inv(3*mu)) % p, p
        assert d['a_L'] == 3*mu*inv(4)*T % p, p
        counts['branch_bridge_checks'] += 1
        if p <= dense_limit:
            c = dense_power_coeffs(p)
            H, K = c[p-1], c[p-2]
            Td = sum(c[k]*pow(mu, k, p) for k in range(p)) % p
            assert H == 0 and K == d['a_m'] and Td == T, p
            counts['dense_power_checks'] += 1
        # Retained fast prefix
        z = elliptic_prefix.third(p)
        assert z['L'] == L and z['trace'] == 0 and z['B'] == d['B_L'] and z['U'] is None, p
        counts['retained_prefix_checks'] += 1
        counts['primes_2_mod_3'] += 1
        rows.append({'p': p, 'm': m, 'L': L, 'm_factorial': f, 'm_factorial_cubed': pow(f, 3, p),
                     'B_L': d['B_L'], 'a_m': d['a_m'], 'a_L': d['a_L'], 'U_L': d['U_L'],
                     'U_m': d['U_m'], 'mu': mu, 'T_f_mu': T})
    for p in range(7, min(limit, 5000) + 1):
        if p % 3 != 1 or not is_prime(p):
            continue
        L = (p-1)//3
        f = factorial_mod(L, p)
        cb = comb(2*L, L) % p
        assert cb == (-pow(pow(f, 3, p), -1, p)) % p and cb == (-jacobi_r(p)) % p, p
        counts['contrast_primes_1_mod_3'] += 1
    with open(csv_path, 'w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts.update(limit=limit, dense_limit=dense_limit, status='passed',
                  scope='finite evidence for Theorems R and E and bridge (B6); not proof; no timings',
                  python=sys.version, platform=platform.platform(),
                  source_sha256={'validate_rounded_third.py': sha(__file__),
                                 'retained elliptic_prefix.py': sha(RETAINED/'elliptic_prefix.py')})
    return counts


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--limit', type=int, default=20000)
    ap.add_argument('--dense-limit', type=int, default=600)
    ap.add_argument('--output', type=Path, default=HERE/'results/validation.json')
    ap.add_argument('--csv', type=Path, default=HERE/'results/rounded_third_values.csv')
    args = ap.parse_args()
    result = run(args.limit, args.dense_limit, args.csv)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
