# Release note for this folder (added 13 October 2026)

This folder is the Cartier–Miller integration audit and exact prototype of 13 October 2026. It was received as `Cartier_Miller_Integration_Audit_20261013.zip` (SHA-256 4074f1d32595dde20909a84701ef46ba612faf7e7d3ce1d98b96bc47cf594ee4). Start with `README.md`, then `CONSOLIDATED_REPORT.md` and `TECHNICAL_SPECIFICATION.md`. Three kinds of change were made for the repository release. They are recorded in `PROVENANCE.json` and summarized here.

## Not redistributed

Four items in the delivery are identified by hash only. They are still recorded in `PROVENANCE.json` with `"redistributed": false`; `verify_package.py` skips them.

| Delivered path | SHA-256 | Reason |
|---|---|---|
| `evidence/manuscript_convenience.md` | d0e1a2600e6d9f349d601760b49ebad69e981f4ed89e264796d2ab9f771c3eb5 | Manuscript text; the extensions release likewise excludes manuscript material (the PDF is at the repository root) |
| `retained_archives/HIGHER_GENUS_RESEARCH_20260928.zip` | c2294b9fe038aacdf15a8d96c86cba8d6dd55137d60865c8a56054eb7fc6f38f | September historical archive, excluded as not re-reviewed by the extensions PROVENANCE |
| `retained_archives/Witt_BGS_Precision_Two_20261001.zip` | 4469f014a3d10b16368cb93775548b1618d724dd475b33fb02ae013f73c38ce4 | Contains LGPL FLINT headers, a compiled Linux binary and nested collaborator-handoff archives |
| `retained_archives/p-Adic_quarter.zip` | 9cd3e84a31b74d21358e26f928b4fb14119107a7585f15e54578370805feeb3d | September historical archive, as above |

The prototype does not import any of these at run time. The relevant reports summarized from them remain in `evidence/`. The delivery's duplicate working-output folder `results/` was also left out; `validate.py` and `benchmark.py` recreate it, and `.gitignore` keeps it out of the repository. The immutable snapshots are in `recorded_results/`.

## Vendored code refreshed to the repository's corrected versions

The delivery had copied older versions of five files that the repository has since corrected. Each was replaced with the version on `main` at commit e7c3242. The source hashes are in `PROVENANCE.json` under `refreshed_from`, and the audit's original hashes under `audit_delivered_sha256`.

| Path | Change |
|---|---|
| `retained_research/depth_three_recognition_20261007/core/depth_three_recognize.py` | Current consolidated recognizer (deterministic trace-sign merge) |
| `retained_research/depth_three_recognition_20261007/core/depth_three_b0_recognize.py` | Current B=0 recognizer (review schema patch, B=0 Las Vegas sign helper) |
| `retained_research/depth_three_recognition_20261007/core/validate_depth_three.py`, `cli.py` | Current versions, for consistency with the two recognizers |
| `cm_system/backends/cm/fixed_D_evaluator.py` | Review-corrected revision 1: `D % p` test and prime validation. Its import of `d7_seed` is package-relative inside `cm_system`, with a standalone fallback |

`d7_seed.py` and `cm_tables.json` were already identical to the repository's copies. After the refresh, `python validate.py` passed with exit status 0. Every counter equals the audit's recorded run, and `results/validation_checks.jsonl` is byte-identical to `recorded_results/validation_checks.jsonl`. The refreshed run's summary is `recorded_results/validation_repository_refresh_20261013.json`. The benchmarks were not rerun; `recorded_results/benchmarks.*` are the audit's measurements.

## Added

- **`LICENSE`:** MIT, as for the extensions. The vendored code is the author's own project code and carries no other licence notice.
- **`.gitignore`:** keeps the working-output folder `results/` out of the repository.
- **This note.**
- **`verify_package.py`:** one line skips hash-only provenance entries.

`SHA256SUMS.json` was regenerated over the released files. `recorded_results/*.log` are committed although the repository ignores `*.log`, because the manifest covers them.

The scope statements of the delivery are unchanged. This is an exact integration layer and prototype. It claims no new generic fast algorithm, no sum-avoiding Witt extraction and no novelty, and it has not been tested on Windows.
