#!/usr/bin/env python3
"""
Independent computation of the Cartier coefficients
    H    = [x^(p-1)] (x^3 + A x + B)^h ,   beta = [x^(p-2)] (x^3 + A x + B)^h ,  h = (p-1)/2,
by EXACT integer multinomial expansion (no polynomial arithmetic mod p, no
imports from the first worker), plus

  (T1) a randomized test of the transport claims  H' = H  and  beta' = 2 beta - q H
       under the normalized 2-isogeny (A,B) -> (-4A - 15 q^2, -8 A q - 22 q^3)
       at many primes (including p = 2 mod 3 and supersingular cases);
  (T2) a check that H equals the trace mod p (independent point count);
  (T3) full enumeration of the depth-three family at p = 73, 97, 193, 241 and a
       sample at 1009, 1033: beta = -(7+6e+6g+2eg) r H, j is a root of
       polclass(-192) mod p, distinctness, P1/Q1 nonvanishing, and the
       4(p-1)-count against the set of ALL F_p-curves with j a root of H_-192.
"""
import json, random, sys
from math import factorial, comb

def hasse_beta_exact(A, B, p):
    """Return (H, beta) in [0,p) from the exact integer multinomial expansion."""
    assert p >= 7 and p % 2 == 1
    h = (p - 1) // 2
    A = int(A) % p; B = int(B) % p
    out = []
    for n in (p - 1, p - 2):
        total = 0
        for i in range(0, h + 1):
            j = n - 3 * i
            if j < 0: break
            k = h - i - j
            if k < 0: continue
            mult = factorial(h) // (factorial(i) * factorial(j) * factorial(k))
            total += mult * (A ** j) * (B ** k)
        out.append(total % p)
    return out[0], out[1]

def hasse_beta_polymod(A, B, p):
    """Cross-check: square-and-multiply of the polynomial mod p (truncated at degree p-1)."""
    h = (p - 1) // 2
    base = [B % p, A % p, 0, 1]
    res = [1]
    def mul(u, v):
        w = [0] * min(len(u) + len(v) - 1, p)
        for i, a in enumerate(u):
            if a == 0: continue
            for jx, b in enumerate(v):
                if i + jx >= p: break
                w[i + jx] = (w[i + jx] + a * b) % p
        return w
    e = h
    while e:
        if e & 1: res = mul(res, base)
        base = mul(base, base); e >>= 1
    res += [0] * (p - len(res))
    return res[p - 1], res[p - 2]

def trace_by_count(A, B, p):
    """a_p = p + 1 - #E(F_p) by Legendre symbol sum."""
    leg = [0] * p
    for x in range(1, p):
        leg[x * x % p] = 1
    s = 0
    for x in range(p):
        v = (x * x * x + A * x + B) % p
        if v == 0: continue
        s += 1 if leg[v] else -1
    return -s  # a_p = -sum chi(f(x))

def sqrt_mod(a, p):
    a %= p
    for x in range(p):
        if x * x % p == a: return x
    return None

def velu(A, B, q, p):
    assert (q**3 + A*q + B) % p == 0
    return (-4*A - 15*q*q) % p, (-8*A*q - 22*q**3) % p

def small_primes(lo, hi):
    return [n for n in range(lo, hi) if n > 1 and all(n % d for d in range(2, int(n**0.5) + 1))]

def inv(a, p): return pow(a, p - 2, p)

# ---- family constants (my own, from indep_symbolic.py; identical to the claim) ----
ALPHA = (-1095, -540, -540, -420)
GAMMA = (-22198, -13860, -16380, -8820)
MULT  = (-7, -6, -6, -2)
A3C   = (-13988298375, -8054356500, -9859360500, -5708191500)
G2C   = (2072413204, 1193214960, 1460677680, 845626320)
HPOL  = [-1080060886113159937649308593750000, 826335556188178615474500000000,
         15705521635909735050750000, -8041801037378436000, 1]

def ev(vec, e, g, p):
    return (vec[0] + vec[1]*e + vec[2]*g + vec[3]*e*g) % p

def my_family_member(p, e, g, r):
    return ev(ALPHA, e, g, p) * r * r % p, ev(GAMMA, e, g, p) * pow(r, 3, p) % p

def my_recognize(p, A, B):
    """My own implementation of the C5 recognizer, to compare against the first worker's."""
    A %= p; B %= p
    U = [(B*B*A3C[i] - A*A*A*G2C[i]) % p for i in range(4)]
    U0, U1, U2, U3 = U
    P0 = (U0*U0 + 3*U1*U1 - 2*U2*U2 - 6*U3*U3) % p
    P1 = 2*(U0*U1 - 2*U2*U3) % p
    Q0 = (U0*U0 - 3*U1*U1 + 2*U2*U2 - 6*U3*U3) % p
    Q1 = 2*(U0*U2 - 3*U1*U3) % p
    info = dict(U=U, P0=P0, P1=P1, Q0=Q0, Q1=Q1)
    if P1 == 0 or Q1 == 0:
        return None, info
    e = (-P0 * inv(P1, p)) % p
    g = (-Q0 * inv(Q1, p)) % p
    if e*e % p != 3 or g*g % p != 2:
        return None, info
    al = ev(ALPHA, e, g, p); ga = ev(GAMMA, e, g, p)
    if al == 0 or ga == 0 or A == 0:
        return None, info
    r = al * B % p * inv(ga * A % p, p) % p
    if my_family_member(p, e, g, r) != (A, B):
        return None, info
    return (e, g, r), info

def j_inv(A, B, p):
    num = 1728 * 4 * pow(A, 3, p) % p
    den = (4 * pow(A, 3, p) + 27 * B * B) % p
    if den == 0: return None
    return num * inv(den, p) % p

def hpol_roots(p):
    return [j for j in range(p) if sum(c * pow(j, i, p) for i, c in enumerate(HPOL)) % p == 0]

def main():
    random.seed(20261007)
    out = {}

    # ---- T0: exact multinomial vs polynomial power mod p (sanity of my own code)
    chk = 0
    for p in (7, 11, 13, 73, 97, 101, 193):
        for _ in range(5):
            A = random.randrange(p); B = random.randrange(p)
            assert hasse_beta_exact(A, B, p) == hasse_beta_polymod(A, B, p); chk += 1
    out["T0_multinomial_vs_polypow_checks"] = chk

    # ---- T2: H == trace mod p, and beta == 0 when A == 0, p == 1 mod 3
    t2 = {"checked": 0, "mismatch": []}
    for p in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 97, 193):
        for _ in range(8):
            A = random.randrange(p); B = random.randrange(p)
            if (4*A**3 + 27*B*B) % p == 0: continue
            H, beta = hasse_beta_exact(A, B, p)
            tr = trace_by_count(A, B, p)
            t2["checked"] += 1
            if H != tr % p: t2["mismatch"].append((p, A, B, H, tr))
        if p % 3 == 1:
            for B in range(1, p):
                H, beta = hasse_beta_exact(0, B, p)
                assert beta == 0 and H != 0, (p, B, H, beta)
    out["T2_H_equals_trace"] = t2

    # ---- T1: transport of H and beta under the normalized 2-isogeny
    t1 = {"tests": 0, "H_mismatch": [], "beta_mismatch": [], "primes": []}
    for p in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 1009, 1033):
        t1["primes"].append(p)
        ntest = 40 if p < 300 else 12
        for _ in range(ntest):
            A = random.randrange(p); q = random.randrange(p)
            B = (-q**3 - A*q) % p
            if (4*A**3 + 27*B*B) % p == 0: continue
            A1, B1 = velu(A, B, q, p)
            if (4*A1**3 + 27*B1*B1) % p == 0: continue   # (should not happen for 2-isogeny of nonsingular)
            H, beta = hasse_beta_exact(A, B, p)
            H1, beta1 = hasse_beta_exact(A1, B1, p)
            t1["tests"] += 1
            if H1 != H: t1["H_mismatch"].append((p, A, B, q, H, H1))
            if beta1 != (2*beta - q*H) % p: t1["beta_mismatch"].append((p, A, B, q, beta, beta1))
    out["T1_transport"] = t1

    # ---- T3: family enumeration
    t3 = {}
    for p in (73, 97, 193, 241, 1009, 1033):
        assert p % 24 == 1
        e0 = sqrt_mod(3, p); g0 = sqrt_mod(2, p)
        assert e0 and g0
        roots = hpol_roots(p)
        rec = {"p": p, "sqrt3": e0, "sqrt2": g0, "Hpol_roots_mod_p": roots,
               "members": 0, "distinct_AB": 0, "singular": 0, "A0_or_B0": 0,
               "beta_mismatch": 0, "j_not_root": 0, "P1_zero": 0, "Q1_zero": 0,
               "my_recognizer_fail": 0, "j_by_sign": {}, "H_zero": 0, "full": p <= 241,
               "beta_checked": 0}
        seen = set()
        rs = range(1, p) if p <= 241 else sorted(random.sample(range(1, p), 40))
        for se in (1, -1):
            for sg in (1, -1):
                e = se * e0 % p; g = sg * g0 % p
                A_, B_ = my_family_member(p, e, g, 1)
                jj = j_inv(A_, B_, p)
                rec["j_by_sign"][f"e={'+' if se>0 else '-'},g={'+' if sg>0 else '-'}"] = jj
                for r in rs:
                    A, B = my_family_member(p, e, g, r)
                    rec["members"] += 1
                    seen.add((A, B))
                    if (4*A**3 + 27*B*B) % p == 0: rec["singular"] += 1
                    if A == 0 or B == 0: rec["A0_or_B0"] += 1
                    if j_inv(A, B, p) not in roots: rec["j_not_root"] += 1
                    cert, info = my_recognize(p, A, B)
                    if info["P1"] == 0: rec["P1_zero"] += 1
                    if info["Q1"] == 0: rec["Q1_zero"] += 1
                    if cert != (e, g, r): rec["my_recognizer_fail"] += 1
                    # beta check: all members for p<=193, sample otherwise
                    if p <= 193 or (p == 241 and r % 10 == 1) or p > 241:
                        H, beta = hasse_beta_exact(A, B, p)
                        rec["beta_checked"] += 1
                        if H == 0: rec["H_zero"] += 1
                        if beta != ev(MULT, e, g, p) * r % p * H % p: rec["beta_mismatch"] += 1
        rec["distinct_AB"] = len(seen)
        rec["expected_4(p-1)"] = 4 * (p - 1)
        # complement check (full primes): every curve with j in roots is a family member
        if p <= 241:
            cnt_all = 0; missing = 0
            for A in range(1, p):
                for B in range(1, p):
                    if (4*A**3 + 27*B*B) % p == 0: continue
                    if j_inv(A, B, p) in roots:
                        cnt_all += 1
                        if (A, B) not in seen: missing += 1
            rec["all_curves_with_j_in_roots"] = cnt_all
            rec["such_curves_not_in_family"] = missing
        t3[p] = rec
    out["T3_family"] = t3

    # ---- primes p = 1 mod 24 below 73
    out["primes_1_mod_24_below_73"] = [n for n in small_primes(2, 73) if n % 24 == 1]

    # ---- fixture C8 check at p = 73
    p = 73
    H, beta = hasse_beta_exact(4, 16, p)
    cert, info = my_recognize(p, 4, 16)
    e, g, r = cert
    out["C8_fixture"] = {"H": H, "beta": beta, "trace_by_count": trace_by_count(4, 16, p) % p,
                         "cert": cert, "multiplier": ev(MULT, e, g, p) * r % p,
                         "beta_equals_mult_H": beta == ev(MULT, e, g, p) * r % p * H % p,
                         "j": j_inv(4, 16, p)}
    with open("indep_cartier_results.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(json.dumps(out, indent=1, default=str))

if __name__ == "__main__":
    main()
