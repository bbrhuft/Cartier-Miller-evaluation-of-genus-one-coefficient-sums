"""Cold, matched boundary timings; Python standard library only."""
import argparse
import csv
import json
from pathlib import Path
import platform
from statistics import median
import sys
from time import perf_counter

from boundary_framework import BoundaryEvaluator, BoundaryRequest, __version__


def run(repeats=3, output=Path("results")):
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in (10007, 20021, 100003, 100019, 1000003, 1000037, 4000037):
        third_L = (p-1)//3 if p % 3 == 1 else (p+1)//3
        for case, L, family in (("third_reduced", third_L, "auto"),
                                ("third_unreduced", third_L, "generic"),
                                ("generic_fifth_index", (p-1)//5, "generic")):
            # Direct route gives a matched cross-backend comparison. Full
            # independent binomial-oracle checks are in the validation suite.
            expected = BoundaryEvaluator().evaluate(BoundaryRequest(p, L, family, "direct")).value
            for backend in ("direct", "product_tree", "auto"):
                samples = []
                for repeat in range(repeats):
                    evaluator = BoundaryEvaluator()  # No cache/warm workspace.
                    start = perf_counter()
                    result = evaluator.evaluate(BoundaryRequest(p, L, family, backend))
                    wall = perf_counter() - start
                    if result.value != expected:
                        raise RuntimeError(f"benchmark disagreement {(p,L,backend)}")
                    samples.append({
                        "p": p, "L": L, "case": case, "requested_backend": backend,
                        "reduction": result.reduction,
                        "actual_backends": "+".join(c.backend for c in result.factorial_calls),
                        "repeat": repeat, "value": result.value, "correct": True,
                        "wall_ms": wall * 1000,
                        "setup_ms": sum(c.setup_seconds for c in result.factorial_calls)*1000,
                        "evaluation_ms": sum(c.evaluation_seconds for c in result.factorial_calls)*1000,
                        "validation_ms": result.validation_seconds*1000,
                        "normalization_ms": result.normalization_seconds*1000,
                        "factorial_calls": len(result.factorial_calls),
                        "largest_degree": max((c.block_degree for c in result.factorial_calls), default=0),
                    })
                rows.extend(samples)
                print(f"p={p} {case} {backend}: {median(s['wall_ms'] for s in samples):.3f} ms", flush=True)
    with (output / "benchmark.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    groups = []
    for offset in range(0, len(rows), repeats):
        group = rows[offset:offset+repeats]
        groups.append({**{k:group[0][k] for k in ("p", "L", "case", "requested_backend", "actual_backends", "reduction")},
                       "median_wall_ms": median(r["wall_ms"] for r in group),
                       "median_setup_ms": median(r["setup_ms"] for r in group),
                       "median_evaluation_ms": median(r["evaluation_ms"] for r in group)})
    metadata = {"version": __version__, "python": sys.version, "platform": platform.platform(),
                "processor": platform.processor(), "repeats": repeats,
                "scope": "boundary only; cold evaluator; no fast prefix or GPU; timing not portable",
                "correctness": "all timed values matched the direct boundary route; see validation_results.json for independent oracles",
                "timed_evaluations": len(rows), "medians": groups}
    (output / "benchmark_summary.json").write_text(json.dumps(metadata, indent=2)+"\n", encoding="utf-8")
    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    run(args.repeats, args.output)
