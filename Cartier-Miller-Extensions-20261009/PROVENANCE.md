# Provenance

## Origin

This release was assembled on 9 October 2026 from a private research transfer archive, `Cartier_Miller_Depths_1_2_3_RoundedThird_20261009_Handover.zip` (SHA-256 7330b999695094edf1d2bdf74a63eb2b4f018c7704e39ac5cb5c1338f84c515c). That archive extended `Cartier_Miller_Depths_1_2_3_20261009_Handover.zip` (SHA-256 29271a82c6c25e634fefcb9b5cdae7e93d393b2493413e9d5f41f2009b03e141) with the rounded-third analysis. Neither archive is part of this release. The research is extension work on David Jordan's manuscript *Cartier–Miller evaluation of genus-one coefficient sums* (revised 5 October 2026), which is likewise not included.

The derivations, code, validators and reports were produced between 6 and 9 October 2026 with substantial generative-AI assistance, under the author's direction. Some checks were written by a separate AI worker as independent validation; they are labelled as such and are not human refereeing. The AI-handover records in history/handover_records/ show how the work was directed and transferred between sessions. No repository URL or commit existed before this release.

## Licence decision

The author chose the MIT License for this release. Everything in this directory is the author's project material and is covered by that licence. That includes the unchanged copy of `elliptic_prefix.py`, which carries no separate notice and comes from the author's own archived implementation. Material from the parent project that carries other terms, or that belongs to the paper, was excluded rather than relicensed.

| Excluded from this release | Reason |
|---|---|
| Benchmark GUI, Harvey adapter, point counters, harness, tests and launchers (`code/quarter_benchmark_gui/`, apart from `elliptic_prefix.py`) | They carry GPL-2.0-or-later notices, include David Harvey's Sage-distributed interval-product sources under the GPL, and include the Sage copyright file |
| Historical paper benchmark (`benchmarks/paper_run_20261002/`) | Includes the same GPL upstream Harvey sources |
| Manuscript PDF, DOCX and Markdown transcription, direct-proof DOCX, high-part verification and editorial records | They belong to the paper and remain under its own terms |
| Standalone p ≡ 1 mod 3 third-point package | Part of the parent project, with copied core files that retain their existing status; not extension work |
| September 2026 historical archives and extracted folders (research-essentials and precision-two zips, algebraic reductions, higher genus, p-adic quarter) | Parent-project history of mixed provenance, not re-reviewed for this release |
| Duplicate copies of the closure and depth-two branches, the superseded verifier, manifests and a duplicate fixture | Identical to the included copies, or superseded |

## Layout changes

| Origin in the transfer archive | Location here |
|---|---|
| research/ (closure, depth two, depth three, rounded third) | research/, unchanged layout |
| research/branch_point_20261006/branch_evaluator.py with the report, validator and results from previous_handover/research/branch_point_20261006/ | research/branch_point_20261006/, merged; the two evaluator copies were byte-identical |
| previous_handover/original_handover/code/quarter_benchmark_gui/elliptic_prefix.py | retained/elliptic_prefix.py, unchanged, SHA-256 3e79d82c931f41f3091e98f6f65783ce958f13851e2c6f05283efa2152c0634d |
| Depth_Three_Consolidated_Proof_Note_20261007.md and Depth_Three_Consolidation_Review_20261007.md | docs/ |
| Cartier_Miller_Consolidated_Ledger_20261009.md | docs/LEDGER_20261009.md |
| Earlier ledgers, historical_validation/, historical_packaging_20261007/, the formal-jet note and the parent extension roadmap | history/ |
| START_HERE, PROJECT_STATE, CONSOLIDATED_RESEARCH, NEXT_CONVERSATION_PROMPT, REPRODUCTION, the export validation records and verify_handover.py from both exports | history/handover_records/, unchanged |
| CONSOLIDATED_RESEARCH.md and PROJECT_STATE.md | Rewritten for a public audience as RESULTS.md and STATUS.md |
| verify_handover.py | verify_release.py |

## Modifications to carried-over files

A small number of carried-over files were edited. verify_release.py imports `elliptic_prefix` from retained/. The rounded-third validator does the same, and the rounded-third note has three wording edits that describe the new location. In research/depth_three_recognition_20261007/independent/, `indep_extra.py` and `indep_attack.py` opened a fixture through an absolute path on the original worker's machine; both now resolve it relative to the repository. No logic changed, and their recorded results did not pin source hashes. HUMAN_REVIEW.md gained one review question and a closing sentence. No recognizer, evaluator, theorem statement or retained evidence file was changed.

## Files that were never retained

The closure theory note describes `check_closure.py` together with `validation.csv` and `validation.json`. None of these is in the transfer archive or its nested archives. research/isogeny_closure_20261006/replacement_validation_20261009/ contains a fresh reconstruction of that documented scope, written on 9 October and labelled as a replacement. The branch-point report mentions `third_boundary_bridge.py`, which was likewise not retained. The bridge it checked, a_L=(3μ/4)T_f(μ), is now proved elementarily and validated in research/rounded_third_boundary_20261009/.

## Evidence authority

Nested SHA256SUMS files inside research directories describe their original scope and can include runtime artifacts. SHA256SUMS.json at the root is authoritative for this release. Retained validation outputs are historical records of the runs that produced them. The 9 October rerun outputs are kept separately in evidence/rerun_20261009/.
