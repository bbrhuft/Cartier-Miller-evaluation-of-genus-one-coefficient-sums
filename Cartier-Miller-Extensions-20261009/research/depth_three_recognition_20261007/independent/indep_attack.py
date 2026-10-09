#!/usr/bin/env python3
"""
Adversarial tests of the first worker's recognizer
    core/depth_three_recognize.py : recognize_depth_three, verify_supplied_certificate,
                                     prepare_from_trace, family_member
using the second worker's OWN enumeration (indep_cartier.py) as the oracle.
"""
import sys, json, random, copy, csv, ast
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "core"))
import indep_cartier as me                      # my own code
import depth_three_recognize as fw               # first worker's code (imported AFTER my code was written)

def is_prime(n):
    if n < 2: return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0: return False
    return True

def my_members(p, rs=None):
    e0 = me.sqrt_mod(3, p); g0 = me.sqrt_mod(2, p)
    out = {}
    rs = rs or range(1, p)
    for se in (1, -1):
        for sg in (1, -1):
            e = se * e0 % p; g = sg * g0 % p
            for r in rs:
                out[me.my_family_member(p, e, g, r)] = (e, g, r)
    return out

def status_of(A, B, p):
    try:
        return fw.recognize_depth_three(A, B, p)
    except Exception as ex:
        return {"status": "EXC:" + type(ex).__name__, "msg": str(ex)}

def main():
    random.seed(7)
    R = {}

    # ------------------------------------------------------------------ A. positive tests at eligible primes
    A_res = {}
    for p in (73, 97, 193, 241, 1009, 1033):
        full = p <= 241
        rs = None if full else sorted(random.sample(range(1, p), 60))
        mem = my_members(p, rs)
        rec = {"p": p, "members_tested": len(mem), "recognized": 0, "param_match": 0,
               "cert_verify_ok": 0, "fw_family_member_match": 0, "multiplier_match": 0,
               "H_beta_checked": 0, "H_beta_ok": 0, "failures": []}
        for (A, B), (e, g, r) in mem.items():
            res = status_of(A, B, p)
            if res["status"] != "recognized":
                rec["failures"].append(("not recognized", A, B, res)); continue
            rec["recognized"] += 1
            c = res["matches"][0]
            prm = c["parameters"]
            if (prm["e"], prm["g"], prm["r"]) == (e, g, r): rec["param_match"] += 1
            else: rec["failures"].append(("param mismatch", A, B, prm, (e, g, r)))
            if fw.family_member(p, e, g, r) == (A, B): rec["fw_family_member_match"] += 1
            mymult = me.ev(me.MULT, e, g, p) * r % p
            if c["beta_multiplier"] == mymult: rec["multiplier_match"] += 1
            else: rec["failures"].append(("multiplier mismatch", A, B, c["beta_multiplier"], mymult))
            try:
                fw.verify_supplied_certificate(p, A, B, c); rec["cert_verify_ok"] += 1
            except Exception as ex:
                rec["failures"].append(("verify raised", A, B, str(ex)))
            if p <= 193 or (p == 241 and r % 20 == 1) or (p > 241 and r % 6 == 1):
                H, beta = me.hasse_beta_exact(A, B, p)
                rec["H_beta_checked"] += 1
                if beta == c["beta_multiplier"] * H % p: rec["H_beta_ok"] += 1
                else: rec["failures"].append(("beta != mult*H", A, B, H, beta, c["beta_multiplier"]))
        A_res[p] = rec; print("A done", p, file=sys.stderr)
    R["A_positive"] = A_res

    # ------------------------------------------------------------------ B. exhaustive negative tests at p = 73, 97
    B_res = {}
    for p in (73, 97):
        mem = my_members(p)
        roots = me.hpol_roots(p)
        # trace table of family members for the same-trace attack
        fam_traces = {}
        for (A, B) in mem:
            H, _ = me.hasse_beta_exact(A, B, p); fam_traces.setdefault(H, 0); fam_traces[H] += 1
        rec = {"p": p, "inputs": 0, "family": 0, "nonfamily": 0, "nonfamily_rejected": 0,
               "nonfamily_accepted": [], "singular_valueerror": 0, "A0_or_B0_rejected": 0,
               "same_trace_as_some_member": 0, "same_trace_rejected": 0, "same_j_nonfamily": 0,
               "P1_zero_nonfamily": 0, "Q1_zero_nonfamily": 0, "P1orQ1_zero_in_family": 0,
               "unexpected_exceptions": [], "status_counts": {}}
        for A in range(p):
            for B in range(p):
                rec["inputs"] += 1
                res = status_of(A, B, p)
                st = res["status"]; rec["status_counts"][st] = rec["status_counts"].get(st, 0) + 1
                sing = (4 * A ** 3 + 27 * B * B) % p == 0
                if sing:
                    if st == "EXC:ValueError": rec["singular_valueerror"] += 1
                    else: rec["unexpected_exceptions"].append((A, B, res))
                    continue
                if st.startswith("EXC"):
                    rec["unexpected_exceptions"].append((A, B, res)); continue
                inf = (A, B) in mem
                if inf:
                    rec["family"] += 1
                    _, info = me.my_recognize(p, A, B)
                    if info["P1"] == 0 or info["Q1"] == 0: rec["P1orQ1_zero_in_family"] += 1
                    continue
                rec["nonfamily"] += 1
                if st == "recognized": rec["nonfamily_accepted"].append((A, B, res))
                else: rec["nonfamily_rejected"] += 1
                if A == 0 or B == 0:
                    if st != "recognized": rec["A0_or_B0_rejected"] += 1
                else:
                    _, info = me.my_recognize(p, A, B)
                    if info["P1"] == 0: rec["P1_zero_nonfamily"] += 1
                    if info["Q1"] == 0: rec["Q1_zero_nonfamily"] += 1
                if me.j_inv(A, B, p) in roots: rec["same_j_nonfamily"] += 1
                H, _ = me.hasse_beta_exact(A, B, p)
                if H in fam_traces:
                    rec["same_trace_as_some_member"] += 1
                    if st != "recognized": rec["same_trace_rejected"] += 1
        rec["family_trace_values"] = sorted(fam_traces)
        B_res[p] = rec; print("B done", p, file=sys.stderr)
    R["B_exhaustive_negative"] = B_res

    # ------------------------------------------------------------------ C. ineligible primes p = 13, 17 mod 24 and others
    C_res = {}
    for p in (13, 37, 61, 109, 157, 181, 17, 41, 89, 113, 137, 7, 11, 19, 23, 31, 43, 47, 71, 79, 103, 127, 151, 167, 191, 199, 223, 239, 263):
        roots = me.hpol_roots(p)
        rec = {"p": p, "p_mod_24": p % 24, "Hpol_roots_mod_p": roots, "tested": 0, "statuses": {}}
        for _ in range(60):
            A = random.randrange(p); B = random.randrange(p)
            res = status_of(A, B, p); rec["tested"] += 1
            rec["statuses"][res["status"]] = rec["statuses"].get(res["status"], 0) + 1
        # also check: no rational nondual third step from A=0 seeds at p = 13 mod 24 (claim C4)
        if p % 24 == 13:
            found = 0
            for Bs in range(1, p):
                # roots of x^3 + Bs
                for q0 in range(p):
                    if (q0 ** 3 + Bs) % p: continue
                    A1, B1 = me.velu(0, Bs, q0, p)
                    for q1 in range(p):
                        if (q1 ** 3 + A1 * q1 + B1) % p or q1 == -2 * q0 % p: continue
                        A2, B2 = me.velu(A1, B1, q1, p)
                        for q2 in range(p):
                            if (q2 ** 3 + A2 * q2 + B2) % p or q2 == -2 * q1 % p: continue
                            found += 1
            rec["rational_nondual_depth3_paths_from_A0_seeds"] = found
        C_res[p] = rec; print("C done", p, file=sys.stderr)
    R["C_ineligible_primes"] = C_res

    # ------------------------------------------------------------------ D. bad p values
    D_res = {}
    for p in (0, 1, 2, 3, 5, 25, 49, 121, 145, 169, 217, 289, 361, 529, 1105, 2465, 46657, -73, 73.0, True, "73", 2 ** 64 + 1, 2 ** 64 + 9):
        try:
            res = fw.recognize_depth_three(4, 16, p)
            D_res[repr(p)] = res["status"]
        except Exception as ex:
            D_res[repr(p)] = "EXC:%s: %s" % (type(ex).__name__, ex)
    # Carmichael-like / strong pseudoprime check: is_prime64 uses deterministic bases, test a few
    R["D_bad_p"] = D_res
    R["primes_1_mod_24_below_73"] = [n for n in range(2, 73) if is_prime(n) and n % 24 == 1]

    # ------------------------------------------------------------------ E. tampered certificates (p=73, (4,16))
    p = 73; A, B = 4, 16
    good = fw.recognize_depth_three(A, B, p)["matches"][0]
    tampers = {}
    def attempt(name, cert, A_=A, B_=B, p_=p):
        try:
            fw.verify_supplied_certificate(p_, A_, B_, cert); tampers[name] = "ACCEPTED"
        except Exception as ex:
            tampers[name] = "rejected (%s: %s)" % (type(ex).__name__, ex)
    attempt("untampered", good)
    c = copy.deepcopy(good); c["parameters"]["e"] = (-c["parameters"]["e"]) % p; attempt("flip_e", c)
    c = copy.deepcopy(good); c["parameters"]["g"] = (-c["parameters"]["g"]) % p; attempt("flip_g", c)
    c = copy.deepcopy(good); c["parameters"]["e"], c["parameters"]["g"] = c["parameters"]["g"], c["parameters"]["e"]; attempt("swap_e_g", c)
    c = copy.deepcopy(good); c["parameters"]["r"] = 2 * c["parameters"]["r"] % p; attempt("scale_r_by_2", c)
    c = copy.deepcopy(good); c["parameters"]["r"] = (-c["parameters"]["r"]) % p; attempt("negate_r", c)
    c = copy.deepcopy(good); c["parameters"]["r"] = 0; attempt("r_zero", c)
    c = copy.deepcopy(good); c["parameters"]["e"] = 5; attempt("e_not_sqrt3", c)
    c = copy.deepcopy(good); c["forward_roots"][1] = (c["forward_roots"][1] + 1) % p; attempt("alter_forward_root", c)
    c = copy.deepcopy(good); c["beta_multiplier"] = (c["beta_multiplier"] + 1) % p; attempt("alter_beta_multiplier", c)
    c = copy.deepcopy(good); c["family"] = "depth2"; attempt("alter_family", c)
    c = copy.deepcopy(good); del c["parameters"]; attempt("missing_parameters", c)
    c = copy.deepcopy(good); c["reverse_path"]["endpoint"] = [0, 1]; attempt("alter_reverse_endpoint_only(stored_output_untrusted)", c)
    c = copy.deepcopy(good); attempt("cert_against_other_curve_(8,64)", c, 16, 128)   # twist by 2: (4*4, 8*16)
    c = copy.deepcopy(good); attempt("cert_against_conjugate_member", c, *fw.family_member(p, (-good["parameters"]["e"]) % p, good["parameters"]["g"], good["parameters"]["r"]))
    # parameters of a different member
    other = fw.recognize_depth_three(*fw.family_member(p, 21, 41, 5), p)["matches"][0]
    attempt("other_members_certificate", other)
    c = copy.deepcopy(good); c["parameters"]["e"] = c["parameters"]["e"] + p; attempt("e_plus_p (should be accepted, reduced mod p)", c)
    R["E_tampered"] = tampers

    # ------------------------------------------------------------------ F. fixture CSV: depth-3/4 classes
    F_res = []
    with open(HERE.parents[2] / 'fixtures' / 'depth_three_four_certificates_20261006.csv') as fh:
        for row in csv.DictReader(fh):
            p = int(row["p"]); depth = int(row["depth"]); seed = ast.literal_eval(row["seed"])
            A, B = ast.literal_eval(row["target"])
            res = status_of(A, B, p)
            roots192 = me.hpol_roots(p) if p % 24 == 1 else []
            # roots of H_-64 and H_-48 mod p
            r64 = [j for j in range(p) if (j * j - 82226316240 * j - 7367066619912) % p == 0]
            r48 = [j for j in range(p) if (j * j - 2835810000 * j + 6549518250000) % p == 0]
            j = me.j_inv(A, B, p)
            entry = {"p": p, "depth": depth, "seed": seed, "target": [A, B], "j": j, "csv_j": int(row["j"]),
                     "status": res["status"], "j_root_H192": j in roots192, "j_root_H64": j in r64, "j_root_H48": j in r48,
                     "seed_type": "A=0" if seed[0] == 0 else "B=0"}
            if res["status"] == "recognized":
                c = res["matches"][0]
                entry["fw_multiplier"] = c["beta_multiplier"]; entry["csv_multiplier"] = int(row["inverse_beta_multiplier"])
                entry["multiplier_agrees_with_csv"] = c["beta_multiplier"] == int(row["inverse_beta_multiplier"]) % p
                entry["csv_H_beta_consistent"] = int(row["beta"]) % p == c["beta_multiplier"] * int(row["H"]) % p
                entry["my_H_beta"] = me.hasse_beta_exact(A, B, p)
            F_res.append(entry)
    R["F_fixture_csv"] = F_res
    summ = {}
    for ent in F_res:
        k = (ent["p"] % 24 == 1, ent["seed_type"], ent["depth"], ent["status"])
        summ[str(k)] = summ.get(str(k), 0) + 1
    R["F_fixture_summary"] = summ

    # ------------------------------------------------------------------ G. prepare_from_trace on the C8 fixture and variants
    G = {}
    p = 73; f = [1, 4, 0, 37]
    prep = fw.prepare_from_trace(p, f, 10)
    G["fixture"] = {"K": prep.evaluator.K, "H": prep.evaluator.H, "T_at_9": prep.evaluator.query(9)["T"],
                    "short_model": list(fw.short_model(f, p)), "cert_params": prep.certificate["parameters"]}
    # my independent K: [w^(p-2)] f(w)^h by exact expansion
    h = (p - 1) // 2
    poly = [1]
    for _ in range(h):
        new = [0] * (len(poly) + 3)
        for i, c0 in enumerate(poly):
            new[i] += c0; new[i + 1] += 4 * c0; new[i + 3] += 37 * c0
        poly = new
    G["my_K_from_exact_expansion"] = poly[p - 2] % p
    G["my_H_from_exact_expansion"] = poly[p - 1] % p
    G["my_K_formula"] = ((4 - 0) * pow(37, -1, p)) % p   # (beta - (b/3)H)/a with beta=4, b=0, a=37
    # T_f(mu) by my own formula from the branch evaluator definition: a*mu/f'(mu)*(mu*H - K)
    mu = 9; fp = (4 + 3 * 37 * mu * mu) % p
    G["my_T_at_9"] = 37 * mu * pow(fp, -1, p) * (mu * 10 - G["my_K_from_exact_expansion"]) % p
    G["f(9)_mod_p"] = (1 + 4 * 9 + 37 * 729) % p
    for tr, label in ((11, "wrong_trace_11"), (-10, "wrong_sign_trace"), (18, "trace_outside_hasse"), (0, "trace_zero")):
        try:
            prep2 = fw.prepare_from_trace(p, f, tr)
            G[label] = {"accepted": True, "K": getattr(prep2, "evaluator", None) and prep2.evaluator.K, "status": getattr(prep2, "get", lambda k, d=None: d)("status")}
        except Exception as ex:
            G[label] = "EXC:%s: %s" % (type(ex).__name__, ex)
    # a non-family cubic
    try:
        G["nonfamily_cubic_[1,1,0,1]"] = fw.prepare_from_trace(p, [1, 1, 0, 1], 2)
        if not isinstance(G["nonfamily_cubic_[1,1,0,1]"], dict): G["nonfamily_cubic_[1,1,0,1]"] = "RecognizedPreparation"
    except Exception as ex:
        G["nonfamily_cubic_[1,1,0,1]"] = "EXC:%s: %s" % (type(ex).__name__, ex)
    R["G_prepare_from_trace"] = G

    # ------------------------------------------------------------------ H. large primes round trip (O(1) path only)
    Hs = {}
    big = []
    n = 10 ** 6; n += (1 - n) % 24
    while len(big) < 2:
        if n % 24 == 1 and fw.is_prime64(n): big.append(n)
        n += 24
    n = 10 ** 12; n += (1 - n) % 24
    while len(big) < 3:
        if n % 24 == 1 and fw.is_prime64(n): big.append(n)
        n += 24
    n = 2 ** 63; n += (1 - n) % 24
    while len(big) < 4:
        if n % 24 == 1 and fw.is_prime64(n): big.append(n)
        n += 24
    for p in big:
        # sqrt via Tonelli (p = 1 mod 8): use pow for p = 1 mod 8? use generic search of a quadratic nonresidue
        def tonelli(a, p):
            q, s = p - 1, 0
            while q % 2 == 0: q //= 2; s += 1
            z = 2
            while pow(z, (p - 1) // 2, p) != p - 1: z += 1
            m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
            while t != 1:
                i, t2 = 0, t
                while t2 != 1: t2 = t2 * t2 % p; i += 1
                b = pow(c, 1 << (m - i - 1), p); m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
            return r
        e = tonelli(3, p); g = tonelli(2, p)
        ok = 0; bad = 0; rej = 0
        for _ in range(30):
            r = random.randrange(1, p); se = random.choice((1, -1)); sg = random.choice((1, -1))
            A, B = fw.family_member(p, se * e % p, sg * g % p, r)
            res = status_of(A, B, p)
            if res["status"] == "recognized" and res["matches"][0]["parameters"] == {"e": se * e % p, "g": sg * g % p, "r": r, "e_squared": 3, "g_squared": 2}: ok += 1
            else: bad += 1
        for _ in range(30):
            A = random.randrange(1, p); B = random.randrange(1, p)
            res = status_of(A, B, p)
            if res["status"] != "recognized": rej += 1
        Hs[p] = {"family_roundtrip_ok": ok, "bad": bad, "random_rejected_of_30": rej}
    R["H_large_primes"] = Hs

    # ------------------------------------------------------------------ I. type confusion on A, B
    I = {}
    for A, B in ((4.0, 16), (4, 16.0), (True, 16), ("4", 16), (4 + 73, 16 + 73 * 5), (-69, -57)):
        try:
            I[repr((A, B))] = fw.recognize_depth_three(A, B, 73)["status"]
        except Exception as ex:
            I[repr((A, B))] = "EXC:%s: %s" % (type(ex).__name__, ex)
    R["I_type_confusion"] = I

    with open(HERE / "indep_attack_results.json", "w") as fh:
        json.dump(R, fh, indent=1, default=str)
    # concise print
    for k in ("A_positive", "B_exhaustive_negative", "C_ineligible_primes", "D_bad_p", "E_tampered", "F_fixture_summary", "G_prepare_from_trace", "H_large_primes", "I_type_confusion"):
        print("=====", k); print(json.dumps(R[k], indent=1, default=str)[:6000])

if __name__ == "__main__":
    main()
