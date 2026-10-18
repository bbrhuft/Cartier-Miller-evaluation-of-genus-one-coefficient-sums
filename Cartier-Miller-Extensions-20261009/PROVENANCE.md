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

## Update of 10 October 2026

A depth-three update was received as Depth_Three_Recognition_Handover_20261010.zip (SHA-256 acc944b70721255dbe51ed3a1e0ba459fb94bc09ccbc73ac5c0a1306d9e59104), with its revised proof note and ledger. It was built on the original 7 October depth-three code. Only its new deterministic-sign functions and validator checks were merged into this release, on top of the consolidated code; the details are in docs/LEDGER_20261009.md. The received note, ledger, sources note and state file are kept unchanged in history/handover_records/depth_three_update_20261010/. The Ireland–Rosen chapter scan and the Tal report PDF used by the author are not redistributed, for copyright reasons.

## Additions of 12 October 2026

Three archives were received:
- CM_Cartier_Extension_20261012_rev1.zip (SHA-256 4699bc1ad1b664a8cc2fd7e992a73754bab8d9bf8f545118ba7f5585d759d659), the CM-to-Cartier research package, revision 1;
- Depth_Three_B0_Adversarial_Review_20261012.zip (b367fbe0410cee3add2a242139e418ce5c9bdcb4773633746844c42fefcc8dc2), the B = 0 review, whose inputs include the B = 0 research handover;
- CM_Cartier_Research_Handover_20261012.zip (5007e508603aa60a13f21f75fee857b53ba0782f7a42df632184447ada141cb5), the handover that prompted the CM research.

The CM package is research/cm_cartier_comparison_20261012/, unchanged apart from the default retained-code path in its two validation suites and its README run instructions. From the B = 0 handover, only the B = 0 code, validator, derivation and data were merged into research/depth_three_recognition_20261007/, with the review's schema patch and the integration changes listed in docs/LEDGER_20261009.md.

The review records are in history/reviews/depth_three_b0_20261012/, and the handover records in history/handover_records/depth_three_b0_20261012/ and history/handover_records/cm_cartier_20261012/. Three items are not redistributed: the Ireland–Rosen Chapter 18 scan (copyright); the nested handover archive inside the review's inputs/, which contains the manuscript and GPL-licensed benchmark code that this release excludes; and the handover's unpack_retained.py and verify_handover.py, which refer to that archive layout.

## Addition of 12 October 2026 (ordinary slope)

The ordinary Cartier-slope feasibility package, revision 2, was received as Ordinary_K_Feasibility_20261012_rev2.zip (SHA-256 bfe5872d4a2aa8a573bcc5ab94d65c6137fddc79c618c784765f0043fcc5e1b4) and placed unchanged at research/ordinary_k_feasibility_20261012/; only RELEASE_NOTE.md was added. Its own SHA256SUMS.json verifies all 99 files. Its nested evidence ZIPs (revisions 0 and 1 and the external review's evidence bundle) were inspected and contain no manuscript, GPL-licensed code or copyrighted scans. From the Ordinary_K research handover (Ordinary_K_Research_Handover_20261012.zip, SHA-256 6ca8d4e09baff40851e9ed620ee810321b891d0eda1fb8f778266b04826cf104), only three data files are redistributed, in `handover_inputs/`. The rest is excluded, because it contains a nested review archive holding the CM research handover (manuscript and GPL code) and LGPL FLINT headers. The CM package's `fixed_D_evaluator.py` received a one-line import fix so that it loads by path; its manifest entry was updated. Some outputs record absolute paths from the producing environment and are left unchanged as hashed evidence.

## Addition of 18 October 2026 (rounded third, T3 backend)

Four files were received:
- the repository handover Cartier_Miller_Rounded_Third_GitHub_Handover_20261018.md (kept verbatim);
- the integration package Cartier_Miller_T3_Integration_20261018.zip (SHA-256 0af630b767ab93a9eebeaa6d09d5eaf2d74ba69475764676b6844d108bfa986a);
- its report, Cartier_Miller_T3_Integration_REPORT_20261018.md (00a73b60ed6a1f673330876d7b882760b9ef3390084dbd9cdb2f14dd52fce2d1), byte-identical to the package's REPORT.md;
- Atkin_Endpoint_Round3_20261018.zip (433b88da7c49d4ac7b65c4a1c31ca40bd42de22737634cd2e0b4f3ca999192d6), supplied to replace one file the package zip omitted.

The package was placed at research/rounded_third_t3_integration_20261018/package/cm_r3_integration_20261018/. Two changes were made:
- vendor/atkin_r3/MANIFEST.json, listed in the package's freeze but missing from its zip, was restored from the Atkin archive; its hash matches.
- vendor/atkin_r3/r3/sources/PARI_2.17.2_installed_doc.json, a verbatim GPL PARI/GP documentation excerpt, was not redistributed; it is identified by hash.

The folder's RELEASE_NOTE.md gives the details, and verify_import.py checks the package against its own hash lists. The package's vendored workbench and Atkin code were screened: they contain no other GPL or LGPL text and no binaries. Ten .log evidence files are committed despite the `*.log` ignore rule. Two vendored logs record absolute paths from the producing environment and are left unchanged as hashed evidence.
