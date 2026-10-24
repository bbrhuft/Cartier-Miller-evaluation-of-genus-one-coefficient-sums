"""
Stage 0, discovery rounds, freeze and confirmation for the pre-registered experiment.
All parameters come from prereg.json.
"""
import hashlib
import itertools
import json
import platform
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

from . import core
from .core import AmbiguousTrace, S_direct, S_fast, brute_trace, frac_mod, is_prime, legendre
from .lattice import HAVE_FLINT, norm2, relations, supnorm
from .quantities import basis, class_key, strat_primes

PKG = Path(__file__).resolve().parent
PREREG = json.loads((PKG / "prereg.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- helpers

def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def code_fingerprint():
    h = hashlib.sha256()
    for f in sorted(PKG.glob("*.py")) + [PKG / "prereg.json"]:
        h.update(f.name.encode())
        h.update(f.read_bytes().replace(b"\r\n", b"\n"))
    return h.hexdigest()


def environment():
    try:
        import flint
        fv = flint.__version__
    except ImportError:
        fv = None
    return {"python": sys.version.split()[0], "implementation": platform.python_implementation(),
            "platform": platform.platform(), "python_flint": fv,
            "code_sha256": code_fingerprint()}


def log(msg, fh=None):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if fh:
        fh.write(line + "\n")
        fh.flush()


def all_classes(z, round_no):
    strat = strat_primes(z) if round_no == 2 else []
    for c in PREREG["residue_classes_mod_24"]:
        for signs in itertools.product((1, -1), repeat=len(strat)):
            yield (c,) + signs


def sample_primes(cls, z, round_no, bits, count, rng, need_target, k):
    """Random primes of the given bit length in class cls (and usable for target)."""
    out, tries = [], 0
    while len(out) < count:
        tries += 1
        if tries > 10_000_000:
            raise RuntimeError("could not find primes in class")
        n = rng.randrange(1 << (bits - 1), 1 << bits) | 1
        if n % 24 != cls[0]:
            n += (cls[0] - n) % 24
        if n.bit_length() != bits or not is_prime(n):
            continue
        if class_key(n, z, round_no) != cls or n in out:
            continue
        if need_target:
            zz = frac_mod(z, n)
            if zz == 0 or (1 - 4 * zz) % n == 0:
                continue
            try:
                S = S_fast(k, z, n, random.Random(f"pts|{n}|{k}|{z}"))
            except AmbiguousTrace:
                continue
            out.append((n, S))
        else:
            out.append((n, None))
    return out


def prune_basis(names, cols, primes, H, gap):
    """Remove linear dependencies among basis columns (logged)."""
    dropped = []
    while True:
        rels = relations(cols, primes)
        if not rels:
            break
        v = rels[0]
        nxt = norm2(rels[1]) if len(rels) > 1 else None
        if supnorm(v) <= H and (nxt is None or nxt >= int(gap) ** 2 * norm2(v)):
            j = max(i for i, x in enumerate(v) if x)
            dropped.append((names[j], v))
            names = names[:j] + names[j + 1:]
            cols = cols[:j] + cols[j + 1:]
        else:
            break
    return names, cols, dropped


def search(target_col, names, cols, primes, H, gap):
    """Relation search with the target as variable 0. Returns (candidate or None, info)."""
    names, cols, dropped = prune_basis(names, cols, primes, H, gap)
    rels = relations([target_col] + cols, primes)
    info = {"basis": names, "dropped_dependencies": [[n, v] for n, v in dropped],
            "dimension": len(cols) + 1}
    if not rels:
        return None, info
    v = rels[0]
    nxt = norm2(rels[1]) if len(rels) > 1 else None
    info["shortest_supnorm"] = supnorm(v)
    info["log10_gap"] = (None if nxt is None
                         else round(0.5 * (len(str(nxt)) - len(str(max(norm2(v), 1)))), 1))
    if v[0] != 0 and supnorm(v) <= H and (nxt is None or nxt >= int(gap) ** 2 * norm2(v)):
        if v[0] < 0:
            v = [-x for x in v]
        coeffs = {n: str(Fraction(-x, v[0])) for n, x in zip(names, v[1:]) if x}
        return {"relation": v, "basis": names, "coefficients": coeffs}, info
    return None, info


def check_relation(cand, p, S, z, round_no):
    vals = dict(basis(p, z, round_no))
    v, names = cand["relation"], cand["basis"]
    total = v[0] * S + sum(x * vals[n] for x, n in zip(v[1:], names))
    return total % p == 0


# ---------------------------------------------------------------- Stage 0

def stage0(out, fh):
    st = PREREG["stage0"]
    rng = random.Random(st["seed"])
    zs = [Fraction(z) for z in PREREG["round1_z"] + PREREG["round2_z"]]
    res = {"environment": environment()}

    # (a) correctness against direct summation
    n = bad = amb = 0
    primes = [p for p in range(11, st["direct_check_all_primes_below"]) if is_prime(p)]
    lo, hi = st["direct_check_random_primes"]["range"]
    extra = []
    while len(extra) < st["direct_check_random_primes"]["count"]:
        q = rng.randrange(lo, hi)
        if is_prime(q) and q not in extra:
            extra.append(q)
    for p in primes + extra:
        for k in PREREG["k_values"]:
            for z in zs:
                zz = frac_mod(z, p)
                if zz == 0 or (1 - 4 * zz) % p == 0:
                    continue
                try:
                    v = S_fast(k, z, p, random.Random(f"pts|{p}|{k}|{z}"))
                except AmbiguousTrace:
                    amb += 1
                    continue
                n += 1
                bad += v != S_direct(k, z, p)
    res["direct_check"] = {"comparisons": n, "mismatches": bad, "ambiguous_skipped": amb,
                           "random_large_primes": extra}
    log(f"Stage 0 (a) direct check: {n} comparisons, {bad} mismatches, {amb} ambiguous skipped", fh)

    # (b) trace selection against brute-force point counts
    n = bad = amb = 0
    for p in [p for p in range(11, st["trace_brute_force_primes_below"]) if is_prime(p)]:
        for k in PREREG["k_values"]:
            for z in zs:
                zz = frac_mod(z, p)
                if zz == 0 or (1 - 4 * zz) % p == 0:
                    continue
                f = [1] + [0] * (k - 1) + [(-4 * zz) % p]
                eps = legendre(core.ev(f, 1, p), p)
                _, Ag, Bg, _ = core.twist_data(f, p, 1)
                try:
                    N = core.select_order(Ag, Bg, k, p, random.Random(f"pts|{p}|{k}|{z}"))
                except AmbiguousTrace:
                    amb += 1
                    continue
                n += 1
                bad += N != p + 1 - eps * brute_trace(f, p)
    res["trace_check"] = {"comparisons": n, "mismatches": bad, "ambiguous_skipped": amb}
    log(f"Stage 0 (b) trace selection vs brute force: {n} comparisons, {bad} mismatches, {amb} ambiguous skipped", fh)

    # (c) planted and null tests for every (round, z, class) basis
    D = PREREG["discovery"]
    H, gap = D["height_bound_H"], D["gap_factor"]
    planted_ok = planted_n = null_hits = null_n = 0
    pruned = []
    for round_no, zlist in ((1, PREREG["round1_z"]), (2, PREREG["round2_z"])):
        for zs_ in zlist:
            z = Fraction(zs_)
            for cls in all_classes(z, round_no):
                prs = [p for p, _ in sample_primes(cls, z, round_no, D["prime_bits"],
                                                   D["primes_per_run"], rng, False, 3)]
                bvals = [basis(p, z, round_no) for p in prs]
                names = [nm for nm, _ in bvals[0]]
                cols = [[bv[j][1] for bv in bvals] for j in range(len(names))]
                names2, cols2, dropped = prune_basis(names, cols, prs, H, gap)
                if dropped:
                    pruned.append({"round": round_no, "z": zs_, "class": cls,
                                   "dropped": [d[0] for d in dropped]})
                # planted
                coef = {nm: Fraction(rng.randint(-50, 50), rng.choice([1, 2, 3, 4, 6]))
                        for nm in names2}
                tgt = [sum(frac_mod(c, p) * cols2[j][i] for j, c in enumerate(coef.values())) % p
                       for i, p in enumerate(prs)]
                cand, _ = search(tgt, names2, cols2, prs, H, gap)
                planted_n += 1
                if cand and all(Fraction(cand["coefficients"].get(nm, "0")) == c
                                for nm, c in coef.items()):
                    planted_ok += 1
                else:
                    log(f"  planted FAILED round {round_no} z={zs_} class {cls}", fh)
                # null
                tgt = [rng.randrange(p) for p in prs]
                cand, _ = search(tgt, names2, cols2, prs, H, gap)
                null_n += 1
                null_hits += cand is not None
    res["planted"] = {"runs": planted_n, "recovered": planted_ok}
    res["null"] = {"runs": null_n, "false_candidates": null_hits}
    res["basis_dependencies_pruned"] = pruned
    log(f"Stage 0 (c) planted: {planted_ok}/{planted_n} recovered; null: {null_hits}/{null_n} false candidates; "
        f"{len(pruned)} bases had dependencies pruned", fh)

    # (d) quantities and target at confirmation sizes (catches size-dependent bugs)
    from .quantities import cm_r, cm_u
    n = bad = 0
    for bits, _ in PREREG["confirmation"]["primes"]:
        for c in PREREG["residue_classes_mod_24"]:
            for k in PREREG["k_values"]:
                z = Fraction(1, 8)
                for p, S in sample_primes((c,), z, 1, bits, 2, rng, True, k):
                    n += 1
                    vals = dict(basis(p, z, 2))
                    good = True
                    if p % 4 == 1:
                        u = cm_u(p)
                        s2 = p - u * u
                        good &= u % 4 == 1 and s2 >= 0 and core.isqrt(s2) ** 2 == s2
                        good &= pow(vals["rho"], 4, p) == 1
                    if p % 3 == 1:
                        r = cm_r(p)
                        good &= r % 3 == 1 and (4 * p - r * r) % 27 == 0
                        good &= pow(vals["w"], 3, p) == 1
                    else:
                        good &= pow(vals["g"], 3, p) == 2
                    good &= vals["q2"] == (pow(2, p - 1, p * p) - 1) // p % p
                    bad += not good
    res["confirmation_size_check"] = {"primes": n, "failures": bad}
    log(f"Stage 0 (d) quantities at 64/128/256 bits: {n} primes, {bad} failures", fh)

    res["passed"] = (res["direct_check"]["mismatches"] == 0 and res["trace_check"]["mismatches"] == 0
                     and planted_ok == planted_n and null_hits == 0 and bad == 0)
    (out / "stage0.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    log(f"Stage 0 {'PASSED' if res['passed'] else 'FAILED'}", fh)
    return res["passed"]


# ---------------------------------------------------------------- discovery

def discovery_round(round_no, out, fh, seed=None, limit=None, prime_count=None):
    D = PREREG["discovery"]
    seed = D["seed"] if seed is None else seed
    H, gap = D["height_bound_H"], D["gap_factor"]
    zlist = PREREG["round1_z"] if round_no == 1 else PREREG["round2_z"]
    results, cands = [], []
    runs = [(k, Fraction(z), cls) for z in zlist for k in PREREG["k_values"]
            for cls in all_classes(Fraction(z), round_no)]
    if limit:
        runs = runs[:limit]
    t0 = time.time()
    for idx, (k, z, cls) in enumerate(runs, 1):
        rng = random.Random(f"{seed}|disc|{round_no}|{k}|{z}|{cls}")
        data = sample_primes(cls, z, round_no, D["prime_bits"], prime_count or D["primes_per_run"],
                             rng, True, k)
        prs = [p for p, _ in data]
        tgt = [S for _, S in data]
        bvals = [basis(p, z, round_no) for p in prs]
        names = [nm for nm, _ in bvals[0]]
        cols = [[bv[j][1] for bv in bvals] for j in range(len(names))]
        cand, info = search(tgt, names, cols, prs, H, gap)
        rec = {"round": round_no, "k": k, "z": str(z), "class": list(cls), "primes": prs, **info,
               "candidate": cand}
        results.append(rec)
        if cand:
            cands.append({"round": round_no, "k": k, "z": str(z), "class": list(cls), **cand})
        log(f"round {round_no} [{idx}/{len(runs)}] k={k} z={z} class={cls}: "
            f"{'CANDIDATE ' + json.dumps(cand['coefficients']) if cand else 'no relation'} "
            f"(dim {info['dimension']}, shortest sup {info.get('shortest_supnorm')}, "
            f"log10 gap {info.get('log10_gap')})", fh)
    (out / f"round{round_no}_runs.json").write_text(json.dumps(results, indent=1, default=str),
                                                    encoding="utf-8")
    prev = []
    cf = out / "candidates.json"
    if cf.exists():
        prev = [c for c in json.loads(cf.read_text(encoding="utf-8")) if c["round"] != round_no]
    cf.write_text(json.dumps(prev + cands, indent=1), encoding="utf-8")
    log(f"round {round_no}: {len(runs)} runs, {len(cands)} candidates, {time.time() - t0:.0f} s", fh)
    return cands


# ---------------------------------------------------------------- freeze and confirm

def freeze(out, fh):
    cf = out / "candidates.json"
    if not cf.exists():
        cf.write_text("[]", encoding="utf-8")
    rec = {"candidates_sha256": sha256_file(cf), "frozen_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "environment": environment()}
    (out / "freeze.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
    log(f"froze candidates.json, SHA-256 {rec['candidates_sha256']}", fh)


def confirm(out, fh, seed=None, schedule=None):
    C = PREREG["confirmation"]
    seed = C["seed"] if seed is None else seed
    schedule = schedule or C["primes"]
    fr = json.loads((out / "freeze.json").read_text(encoding="utf-8"))
    if sha256_file(out / "candidates.json") != fr["candidates_sha256"]:
        raise SystemExit("candidates.json changed after freezing; refusing to confirm")
    cands = json.loads((out / "candidates.json").read_text(encoding="utf-8"))
    report = []
    for i, c in enumerate(cands, 1):
        z, k, cls, rn = Fraction(c["z"]), c["k"], tuple(c["class"]), c["round"]
        rng = random.Random(f"{seed}|conf|{rn}|{k}|{z}|{cls}")
        tested = 0
        failure = None
        for bits, count in schedule:
            for p, S in sample_primes(cls, z, rn, bits, count, rng, True, k):
                tested += 1
                if not check_relation(c, p, S, z, rn):
                    failure = p
                    break
            if failure:
                break
        status = "CONFIRMED" if failure is None else "REJECTED"
        report.append({**c, "status": status, "tested": tested, "first_failure": failure})
        log(f"candidate {i}/{len(cands)} k={k} z={z} class={cls}: {status} after {tested} primes", fh)
    (out / "confirmation.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    return report


def summary(out, fh):
    lines = ["# Experiment summary", ""]
    s0 = json.loads((out / "stage0.json").read_text(encoding="utf-8")) if (out / "stage0.json").exists() else None
    if s0:
        lines += [f"- Stage 0: {'passed' if s0['passed'] else 'FAILED'} "
                  f"(direct {s0['direct_check']['comparisons']}, trace {s0['trace_check']['comparisons']}, "
                  f"planted {s0['planted']['recovered']}/{s0['planted']['runs']}, "
                  f"null false candidates {s0['null']['false_candidates']})"]
    for r in (1, 2):
        f = out / f"round{r}_runs.json"
        if f.exists():
            runs = json.loads(f.read_text(encoding="utf-8"))
            nc = sum(1 for x in runs if x["candidate"])
            lines.append(f"- Round {r}: {len(runs)} runs, {nc} candidates")
    cf = out / "confirmation.json"
    if cf.exists():
        conf = json.loads(cf.read_text(encoding="utf-8"))
        lines += ["", "| round | k | z | class | relation | status | primes tested |", "|---|---|---|---|---|---|---|"]
        for c in conf:
            rel = " + ".join(f"({v})*{n}" for n, v in c["coefficients"].items()) or "0"
            lines.append(f"| {c['round']} | {c['k']} | {c['z']} | {c['class']} | S = {rel} | {c['status']} | {c['tested']} |")
    lines += ["", f"Environment: {json.dumps(environment())}"]
    (out / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    log("wrote SUMMARY.md", fh)
