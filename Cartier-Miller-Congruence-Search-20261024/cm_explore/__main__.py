"""
Command line:  python -m cm_explore <step> [--out DIR]

steps:  stage0 | round1 | round2 | freeze | confirm | summary | all | smoke
  all    runs stage0, round1, round2, freeze, confirm, summary in order
         (stops if Stage 0 fails)
  smoke  a short end-to-end test with separate seeds (results are NOT the experiment)
"""
import argparse
import json
import sys
import time
from pathlib import Path

from . import experiment as ex
from .lattice import HAVE_FLINT


def main():
    ap = argparse.ArgumentParser(prog="python -m cm_explore")
    ap.add_argument("step", choices=["stage0", "round1", "round2", "freeze", "confirm",
                                     "summary", "all", "smoke"])
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    out = Path(a.out if a.step != "smoke" else a.out + "_smoke")
    out.mkdir(parents=True, exist_ok=True)
    if not HAVE_FLINT:
        print("WARNING: python-flint not found; using the slow pure-Python LLL fallback.")
    with open(out / "log.txt", "a", encoding="utf-8") as fh:
        ex.log(f"=== {a.step} === {json.dumps(ex.environment())}", fh)
        t0 = time.time()

        def need_stage0():
            f = out / "stage0.json"
            if not f.exists() or not json.loads(f.read_text(encoding="utf-8"))["passed"]:
                sys.exit("Stage 0 has not passed in this output folder; run stage0 first.")

        if a.step == "stage0":
            ex.stage0(out, fh)
        elif a.step in ("round1", "round2"):
            need_stage0()
            ex.discovery_round(int(a.step[-1]), out, fh)
        elif a.step == "freeze":
            ex.freeze(out, fh)
        elif a.step == "confirm":
            ex.confirm(out, fh)
            ex.summary(out, fh)
        elif a.step == "summary":
            ex.summary(out, fh)
        elif a.step == "all":
            if not ex.stage0(out, fh):
                sys.exit("Stage 0 failed; stopping as pre-registered.")
            ex.discovery_round(1, out, fh)
            ex.discovery_round(2, out, fh)
            ex.freeze(out, fh)
            ex.confirm(out, fh)
            ex.summary(out, fh)
        elif a.step == "smoke":
            s = ex.PREREG["smoke_test_seeds_not_used_for_results"]
            ex.discovery_round(1, out, fh, seed=s["discovery"], limit=4, prime_count=40)
            ex.discovery_round(2, out, fh, seed=s["discovery"], limit=4, prime_count=40)
            ex.freeze(out, fh)
            ex.confirm(out, fh, seed=s["confirmation"], schedule=[[64, 20], [128, 3], [256, 1]])
            ex.summary(out, fh)
        ex.log(f"=== {a.step} finished in {time.time() - t0:.0f} s ===", fh)


if __name__ == "__main__":
    main()
