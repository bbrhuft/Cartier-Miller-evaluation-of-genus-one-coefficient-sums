# CM-to-Cartier extension package (12 October 2026)

Part of the Cartier–Miller extensions release (MIT). This directory is the 12 October 2026 research package, revision 1 after an independent adversarial review, added to the release unchanged apart from the default retained-code path in the two validation suites and this README's run instructions.

| Path | Contents |
|---|---|
| `CM_Cartier_Extension_Note_20261012_rev1.md` | Extension note, revision 1 (after review), with theorems, proofs, exclusions, literature audit, cost contract and status separation. |
| `CM_Cartier_Extension_Ledger_20261012_rev1.md` | Research ledger, revision 1. |
| `REVIEW_RESPONSE.md` | Item-by-item response to the independent adversarial review. |
| `history/` | The note and ledger exactly as reviewed. |
| `core/d7_seed.py` | D = −7 recognizer, endomorphism certificate, signed trace (two rules), trace certification and original-cubic evaluator. Standard library only. |
| `core/d8_control.py` | D = −8 control: recognizer and endomorphism certificate. |
| `core/fixed_D_evaluator.py` | Uniform fixed-D evaluator β/H = −(3B/2A)·R_D(j). |
| `core/qtower.py`, `core/isogeny_matrices.py` | Exact quadratic-tower arithmetic and de Rham pullback matrices. |
| `theory/*.py` | Katz (2019) check, order/class-polynomial argument, symbolic Vélu identities, exact endomorphism loops, (j, S) tables with R_D and H_D, collision resultants, Masser/BOS check, period checks, the characteristic-p exactness demo, and the seed-free degree-5 check. |
| `theory/exploratory/` | First-pass scripts kept for provenance, including the sign-rule comparisons with PARI. |
| `validation/validate_d7.py`, `validation/validate_fixed_D.py` | Exact validation suites. |
| `results/` | JSON and CSV outputs of every script. `results/validation/validation_summary.json` records environment and source hashes. |

## Requirements

`core/d7_seed.py` and `core/d8_control.py` need only the Python standard library. The theory and validation scripts also need `python-flint`, `cypari2` (PARI/GP), `mpmath` and `sympy`:

```
pip install python-flint cypari2 mpmath sympy
```

The validation suites import the release's retained research code read-only: the branch evaluator, the closure code and the depth-two and depth-three recognizers, including the B=0 family. In this repository they find it automatically in the sibling directories of `research/`. Set `RETAINED_RESEARCH` only to test against another copy. From this directory:

```
python run_all.py
```

`run_all.py` reruns every theory and validation script, rewrites `results/` and writes this directory's own `SHA256SUMS.json`. The release-level manifest is `../../SHA256SUMS.json`; run the suite in a separate copy to avoid altering the committed records. Every script exits nonzero on failure, and `run_all.py` exits nonzero if any step fails.

Bounds can be changed with the environment variables `T1_MAX`, `T2_MAX`, `T3_MAX` and `T5_MAX`.

## Scope

- PARI `ellap`, `polclass` and `polmodular` are practical comparators, not certificates.
- The exact certificates are the symbolic identities, the tower computations, and the factored resultants (each factor proved prime and multiplied back).
- The q-series checks carry explicit tail bounds. The period checks are 320-bit floating-point corroboration. Neither is an interval certificate.
- No benchmark is included.
- Nothing was published, and the manuscript is unchanged.
