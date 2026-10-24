"""
Pipeline self-test (not part of the experiment):  python -m cm_explore.selftest

1. Positive control: the target S itself is appended to the basis as "cheat", so
   discovery must find S = cheat, freezing must hash it, and confirmation must
   confirm it at fresh primes of 64, 128 and 256 bits.
2. Negative control: a false candidate must be rejected, and an edited
   candidates.json must be refused after freezing.
Uses its own seeds and a temporary folder.
"""
import json
import random
import shutil
import tempfile
from fractions import Fraction
from pathlib import Path

from . import experiment as ex
from . import quantities
from .core import S_fast

_orig_basis = quantities.basis
_CTX = {}


def _cheat_basis(p, z, round_no):
    B = _orig_basis(p, z, round_no)
    k = _CTX["k"]
    return B + [("cheat", S_fast(k, z, p, random.Random(f"pts|{p}|{k}|{z}")))]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="cm_selftest_"))
    ok = True
    with open(tmp / "log.txt", "w", encoding="utf-8") as fh:
        # positive control
        ex.basis = _cheat_basis
        _CTX["k"] = 4
        z = Fraction(1, 8)
        cls = (13,)
        D = ex.PREREG["discovery"]
        rng = random.Random("selftest-disc")
        data = ex.sample_primes(cls, z, 1, D["prime_bits"], D["primes_per_run"], rng, True, 4)
        prs = [p for p, _ in data]
        bvals = [ex.basis(p, z, 1) for p in prs]
        names = [n for n, _ in bvals[0]]
        cols = [[bv[j][1] for bv in bvals] for j in range(len(names))]
        cand, info = ex.search([S for _, S in data], names, cols, prs, D["height_bound_H"], D["gap_factor"])
        found = cand is not None and cand["coefficients"] == {"cheat": "1"}
        ex.log(f"positive control discovery: {'found S = cheat' if found else 'FAILED ' + str(cand)}", fh)
        ok &= found
        if found:
            (tmp / "candidates.json").write_text(json.dumps([{"round": 1, "k": 4, "z": "1/8", "class": list(cls), **cand}]),
                                                 encoding="utf-8")
            ex.freeze(tmp, fh)
            rep = ex.confirm(tmp, fh, seed=99, schedule=[[64, 30], [128, 5], [256, 2]])
            conf = rep[0]["status"] == "CONFIRMED" and rep[0]["tested"] == 37
            ex.log(f"positive control confirmation: {rep[0]['status']} after {rep[0]['tested']} primes", fh)
            ok &= conf
        ex.basis = _orig_basis

        # negative control: false relation S = 1
        false = {"round": 1, "k": 4, "z": "1/8", "class": [13], "relation": [1, -1], "basis": ["1"],
                 "coefficients": {"1": "1"}}
        (tmp / "candidates.json").write_text(json.dumps([false]), encoding="utf-8")
        ex.freeze(tmp, fh)
        rep = ex.confirm(tmp, fh, seed=98, schedule=[[64, 30]])
        rej = rep[0]["status"] == "REJECTED" and rep[0]["tested"] == 1
        ex.log(f"negative control: {rep[0]['status']} after {rep[0]['tested']} prime(s)", fh)
        ok &= rej

        # tamper check
        (tmp / "candidates.json").write_text(json.dumps([false, false]), encoding="utf-8")
        try:
            ex.confirm(tmp, fh, seed=98, schedule=[[64, 1]])
            ex.log("tamper check FAILED: edited file accepted", fh)
            ok = False
        except SystemExit:
            ex.log("tamper check: edited candidates.json refused", fh)
    shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST", "PASSED" if ok else "FAILED")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
