# Release note for this folder (added 12 October 2026)

This folder is the ordinary Cartier-slope feasibility package, revision 2. It was received as `Ordinary_K_Feasibility_20261012_rev2.zip` (SHA-256 bfe5872d4a2aa8a573bcc5ab94d65c6137fddc79c618c784765f0043fcc5e1b4). It is reproduced here unchanged. Only this note was added; it is not covered by the package's own `SHA256SUMS.json`, which still verifies all 99 package files. The release-level `SHA256SUMS.json` covers this note too.

Start with `README.md`, then `Ordinary_K_Feasibility_Note_20261012_rev2.md` and `CHANGES.md`.

Three points for readers of the release:

1. **Scope of the result.** The study is a feasibility record, not a new algorithm. It derives Theorem A (Frobenius mod p is [[0, −β],[0, H]] in the low-pole basis) and Lemma B (κ ≡ σ_C/p for the canonical-subgroup kernel sum of any ordinary lift). Lemma B awaits specialist review. The study also shows that the constructions it examined give no cheaper complete algorithm for κ = β/H. It proves no lower bound and claims no speed-up or novelty. Much of it is probably classical; see Katz (2019) and Mazur–Stein–Tate (2006), as cited in the note.
2. **Reproduction from this repository alone.** The scripts need three data files from the received `Ordinary_K_Research_Handover_20261012.zip` (SHA-256 6ca8d4e09baff40851e9ed620ee810321b891d0eda1fb8f778266b04826cf104). Only those three are redistributed, in `handover_inputs/`, at the paths the scripts expect. Each matches the handover's own SHA-256 manifest, and the handover's `verify_handover.py` passed:

| File | SHA-256 |
|---|---|
| `handover_inputs/validation/results/ordinary_targets.csv` | dbae08872c11cc31f472089bfe58050f5eb36570dc63a57d189071dfca330573 |
| `handover_inputs/validation/results/same_trace_different_slopes.json` | 24dba472a8f4dd70da2a144b0ef5cb26b5d6db2b0aec263eb29ab87442ea122a |
| `handover_inputs/knowledge/retained_CM_tables.json` | 66bbf3b00fd35bbe09f1f2cd49b4cb49ef24b4dc83e0119772aafbd4b9d3f63f (identical to `research/cm_cartier_comparison_20261012/results/cm_tables.json`) |

The rest of the handover is not redistributed. It contains a nested review archive that in turn holds the CM research handover (with the manuscript and GPL-licensed benchmark code that this release excludes), and LGPL FLINT header files.

The other dependencies are code already in this release. From this folder, run in a copy (the pilot rewrites `ordinary_k_pilot/results/`):

```bash
python -I ordinary_k_pilot/run_all.py --retained .. --extension ../cm_cartier_comparison_20261012 --handover handover_inputs
python -I independent_check/run_independent.py --profile bounded --targets handover_inputs/validation/results/ordinary_targets.csv --out <dir>
```

Run this way on 12 October 2026 (Python 3.13.16), the pilot passed all six steps, and the bounded independent profile passed 7 steps with 1,531 checks and 0 failures. Those outputs are in `repository_rerun_20261012/`. Eight of the twelve pilot outputs are byte-identical to the originally recorded ones; the other four record paths, hashes or timings. Failure injection and the full independent profile (about 19 minutes) were not rerun here; their recorded outputs remain in `ordinary_k_pilot/results/`, `independent_check/results_full/` and `independent_check/results_injection/`.

The repository's CM evaluator is the review-corrected revision 1 (`fixed_D_evaluator.py`, which validates primes through `d7_seed`). The pilot was originally run against revision 0. Revision 1 at first failed to import its sibling module when loaded by path under `python -I`. Its import was fixed in this release; its arithmetic is unchanged, and its fixed-discriminant suite still passes. The pilot's dependency check records the revision-1 hash.
3. **Recorded paths.** Several result JSONs record absolute paths from the environment in which they were produced (`/home/claude/...`). They are left unchanged, because they are hashed evidence. The `.log` files are part of the package manifest and are committed even though the repository's `.gitignore` ignores `*.log`.

The nested ZIPs under `evidence/` are earlier revisions of this package and the external review's evidence bundle. They were checked before release and contain no manuscript, GPL-licensed code or copyrighted scans.
