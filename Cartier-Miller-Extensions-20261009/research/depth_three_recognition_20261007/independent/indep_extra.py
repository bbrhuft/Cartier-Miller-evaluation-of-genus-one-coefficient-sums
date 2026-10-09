#!/usr/bin/env python3
"""
Extra independent checks:
  X1. The trace of every family member is determined by p up to sign:
      4p = t^2 + 192 f^2 (Frobenius lies in the order of discriminant -192).
      Compare with H from exact expansion at p = 73, 97, 193, 241 (all members) and
      samples at 1009, 1033.
  X2. The depth-3 B=0-seed classes at p=73 have j a root of H_{-256}; compute
      Res(H_{-192}, H_{-256}) and its prime factors mod 24 (not in the first worker's list).
  X3. Characterize the non-family inputs with P1 = 0 at p = 73, 97.
  X4. Check that H_{-192} mod p has 4 distinct roots for all p = 1 mod 24 below 20000
      (separability, Cox Thm 9.2 / Deuring) and that alpha, gamma, 4alpha^3+27gamma^2
      are nonzero at every embedding for those p.
"""
import json, sys, math, random
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import indep_cartier as me
import cypari2
pari = cypari2.Pari(); pari.allocatemem(512 * 1024 * 1024)

def cornacchia_t(p):
    """Solve 4p = t^2 + 192 f^2, t >= 0, f >= 1; return list of (t, f)."""
    sols = []
    f = 1
    while 192 * f * f < 4 * p:
        t2 = 4 * p - 192 * f * f
        t = math.isqrt(t2)
        if t * t == t2: sols.append((t, f))
        f += 1
    return sols

def main():
    R = {}
    # X1
    X1 = {}
    for p in (73, 97, 193, 241, 1009, 1033):
        sols = cornacchia_t(p)
        e0 = me.sqrt_mod(3, p); g0 = me.sqrt_mod(2, p)
        rs = range(1, p) if p <= 241 else sorted(random.Random(3).sample(range(1, p), 25))
        traces = set()
        for se in (1, -1):
            for sg in (1, -1):
                for r in rs:
                    A, B = me.my_family_member(p, se * e0 % p, sg * g0 % p, r)
                    H, _ = me.hasse_beta_exact(A, B, p)
                    t = H if H <= p // 2 else H - p
                    traces.add(t)
        X1[p] = {"cornacchia_solutions_(t,f)": sols, "observed_traces": sorted(traces),
                 "trace_is_pm_t0": sorted(traces) == sorted({sols[0][0], -sols[0][0]}) if len(sols) == 1 else None}
    R["X1_trace_determined_by_p"] = X1

    # X2
    H192 = pari("polclass(-192)"); H256 = pari("polclass(-256)")
    res = int(pari.polresultant(H192, H256))
    f = pari.factor(abs(res))
    fl = [[int(f[0][i]), int(f[1][i])] for i in range(len(f[0]))]
    X2 = {"polclass(-256)": str(H256), "Res(H_-192,H_-256)": res, "factorization": fl,
          "primes_mod_24": sorted(set((q, q % 24) for q, _ in fl)),
          "has_prime_1_mod_24": any(q % 24 == 1 for q, _ in fl)}
    p = 73
    r256 = [j for j in range(p) if int(H256.subst("x", j)) % p == 0]
    X2["roots_H256_mod_73"] = r256
    X2["B0_depth3_targets_p73_j"] = {}
    import csv, ast
    with open(HERE.parents[2] / 'fixtures' / 'depth_three_four_certificates_20261006.csv') as fh:
        for row in csv.DictReader(fh):
            if int(row["p"]) == 73 and ast.literal_eval(row["seed"])[1] == 0:
                A, B = ast.literal_eval(row["target"])
                X2["B0_depth3_targets_p73_j"][str((A, B))] = {"j": me.j_inv(A, B, p), "root_of_H256": me.j_inv(A, B, p) in r256}
    R["X2_B0_depth3_classes"] = X2

    # X3
    X3 = {}
    for p in (73, 97):
        roots = me.hpol_roots(p)
        zs = []
        for A in range(1, p):
            for B in range(1, p):
                if (4 * A ** 3 + 27 * B * B) % p == 0: continue
                _, info = me.my_recognize(p, A, B)
                if info["P1"] == 0 or info["Q1"] == 0:
                    zs.append((A, B, me.j_inv(A, B, p), info["P1"], info["Q1"], info["P0"], info["Q0"]))
        js = sorted(set(z[2] for z in zs))
        X3[p] = {"count": len(zs), "distinct_j": js, "any_in_family": any(z[2] in roots for z in zs),
                 "sample": zs[:6]}
        # interpretation: P1 = 0 means U*sigma_g(U) has no e-part; check whether these j satisfy
        # a quadratic relation: j in F_p such that the F_p[e]-norm is rational
    R["X3_P1_or_Q1_zero_nonfamily"] = X3

    # X4
    bad = []
    cnt = 0
    for p in range(73, 20000, 24):
        if not all(p % d for d in range(2, int(p ** 0.5) + 1)): continue
        cnt += 1
        roots = me.hpol_roots(p)
        if len(roots) != 4: bad.append(("roots", p, roots))
        e0 = me.sqrt_mod(3, p); g0 = me.sqrt_mod(2, p)
        for se in (1, -1):
            for sg in (1, -1):
                e = se * e0 % p; g = sg * g0 % p
                al = me.ev(me.ALPHA, e, g, p); ga = me.ev(me.GAMMA, e, g, p)
                if al == 0 or ga == 0 or (4 * al ** 3 + 27 * ga * ga) % p == 0: bad.append(("alpha/gamma/disc", p, e, g))
                if me.j_inv(al, ga, p) not in roots: bad.append(("j", p, e, g))
    R["X4_separability_and_nondegeneracy_p_lt_20000"] = {"primes_checked": cnt, "bad": bad}

    with open(HERE / "indep_extra_results.json", "w") as fh:
        json.dump(R, fh, indent=1, default=str)
    print(json.dumps(R, indent=1, default=str))

if __name__ == "__main__":
    main()
