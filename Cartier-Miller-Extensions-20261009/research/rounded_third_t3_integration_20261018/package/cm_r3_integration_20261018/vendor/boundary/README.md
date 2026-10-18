# Cartier–Miller boundary framework 1.0.0rc1

This is the consolidated modulo-p boundary research release candidate. It combines the verified arithmetic implementation, retained native third/fifth prefixes, scalar BGS and product-tree backends, shared single-prime boundaries, many-prime forests and exact local measured dispatch. The supplied project prefix theorems remain unrefereed. Finite independent checks are execution evidence, not formal proof or independent specialist certification.

Read RELEASE_AUDIT.md for the audit verdict and current evidence. PUBLIC_INTERFACE.md is the authoritative public API and command guide. The original modules remain available; the consolidated entry point is cartier_miller.py.

## Run

Extract the entire ZIP and open a terminal in this folder. Python 3.10 or newer and the standard library are sufficient for the active paths. Run normal Python without -O.

```console
python cartier_miller.py third --p 17
python cartier_miller.py fifth --p 29
python cartier_miller.py boundaries --p 59 --indices 6 12 24 20 6 --backend bgs
```

The third returns U=7. The fifth returns U values [8,10]. The boundary batch returns [14,5,30,6,14]. These are distinct requested outputs; a boundary query alone does not supply an arbitrary-index fast prefix.

```python
from cartier_miller import ThirdPointSession, FifthPointSession

assert ThirdPointSession(23).evaluate()["U_p_L"] == 17
assert [r["U_p_L"] for r in FifthPointSession(29).evaluate()["outputs"]] == [8, 10]
```

## Capture laptop evidence

On Windows run release_check.bat. It checks the frozen runtime manifest, runs all regression tests and executes the public command smoke suite. It creates a timestamped evidence ZIP under results, recording the actual interpreter/platform, sources and outcomes. A reported successful laptop run is kept distinct from an inspected current-version evidence bundle.

For the complete release benchmark capture, run run_checks.bat, or:

```console
python cartier_miller.py check --benchmarks all
```

The all setting runs all eight benchmark scripts sequentially and takes longer than the default smoke run. Each command writes its output to a separate stage directory, preserving a coherent run rather than overwriting historical evidence. Failed stages retain their logs and produce a bundle marked failed. Explicit --output requires a new or empty directory.

## Many primes and measured dispatch

```console
python cartier_miller.py many --bound 20000 --family rounded_third --chunks 32 --out rounded_thirds.csv
python cartier_miller.py many --queries 1000037:333346 --engine independent --backend bgs
```

Dense ranges can benefit greatly from the retained forest. Sparse high-cutoff requests can favor independent native evaluation. There is no universal crossover rule.

```console
python cartier_miller.py calibrate --bound 20000 --family rounded_third --collection streaming --profile laptop_dispatch.json
python cartier_miller.py many --bound 20000 --family rounded_third --engine auto --profile laptop_dispatch.json --out rounded_thirds.csv
```

calibrate_and_run.bat runs this local workflow on Windows. Profiles are tied to the exact workload, output/collection mode, source version, configuration and machine signature. Normal evaluation never trains implicitly. Missing or unmatched profiles use a labeled independent default. Profile lookup can cost more than it saves for small calls; explicit engines remain available. Historical or current Linux profiles are evidence, not universal laptop tuning data.

## Documentation map

| File | Purpose |
|---|---|
| RELEASE_AUDIT.md | Findings, proof/software scope, evidence status and release decision |
| PUBLIC_INTERFACE.md | Consolidated Python and command contracts |
| RESULTS.md | Current release validation and benchmark summary |
| MATHEMATICS.md | Definitions, Wilson reflection, third reductions and complete-sum identity |
| INTEGRATION.md / FIFTHS.md | Retained native prefix integration and fifth formulas |
| BGS_BACKEND.md | Scalar shift/doubling construction and denominator audit |
| SHARED_BOUNDARIES.md | Ratio planning, exact/gap reuse and shared normalization |
| MANY_PRIMES.md / RETAINED_FOREST_PROOF.md | Forest scheduler, ordered products, repeated moduli, resource/timing semantics |
| OUTPUT_MODES.md | Full/U-only contracts and actual acquisition skipping |
| MEASURED_DISPATCH.md | Profile calibration, matching, fallbacks and limitations |
| SOURCE_PROVENANCE.json / RUNTIME_MANIFEST.json | Retained source provenance and frozen runtime hashes |

Earlier release evidence is kept under evidence/history and the attached Windows 0.1 logs under evidence/windows_v0_1. Current results/release_linux records this candidate's actual Linux checks. Mathematical functions, tests, benchmark scripts and native source are all delivered together.

## Scope

This candidate supports modulo p only, with odd primes below 2**64 and explicit resource guards. It does not integrate precision-two corrections, Tal refinements, a general matrix BGS backend, new stopping families or the separate historical CUDA/p-adic projects. The original manuscript and external repository are outside this consolidation's change scope. This is a bounded release audit of the boundary implementation, not an external review of the entire research programme.
