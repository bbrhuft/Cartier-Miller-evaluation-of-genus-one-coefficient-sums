# Depth-three research handover

This package hands off the next question; it does not contain a newly proved depth-three recognition theorem. The recommended bounded target is one explicit depth-three family, beginning with the modulo-73 fixture. Existing symbolic arguments remain subject to critical review. The manuscript is historical context and must not be revised unless requested.

| Read order | File | Purpose |
|---|---|---|
| First | DEPTH_THREE_RESEARCH_PROMPT.md and PROJECT_STATE.md | Task, bounds and current status |
| Next | fixtures/depth_three_p73.json | Concrete target and separately scaled cubic fixture |
| Next | research/Cartier_Miller_Extension_Ledger_20261006.md | Questions, derivations, checks and obstructions |
| Next | research/depth_two_recognition_20261006/Depth_Two_Recognition_and_Higher_Depth_Report_20261006.md | Current recognition results and higher-depth audit |
| Theory | research/depth_two_recognition_20261006/theory/RECOGNITION_THEORY.md | Parameter-checked depth-two families |
| Theory | research/isogeny_closure_20261006/theory/ISOGENY_CLOSURE_THEORY.md | Normalized isogenies, exact corrections and path transport |
| Theory | research/branch_point_20261006/Cubic_Branch_Point_Report_20261006.md | Branch-point second-kind data and cubic normalization |
| Evidence | research/depth_two_recognition_20261006/audit/DEPTH_THREE_FOUR_AUDIT.md | Finite-depth new classes and unreachable component obstruction |
| Code | research/depth_two_recognition_20261006/core/recognize.py; research/isogeny_closure_20261006/core/isogeny_closure.py; research/branch_point_20261006/branch_evaluator.py | Existing implementations; preserve relative directory layout |
| Prior work | original_handover/START_HERE.md, PROJECT_STATE.md, EXTENSION_ROADMAP.md and manuscript/Cartier_Miller_Paper_Revised_20261005.pdf | Published scope and historical source/branch inventory |
| Failed approach | research/k_parallel_20261006/general/GENERAL_JET_REDUCTION.md | Derivative identities do not themselves provide a fast coefficient oracle |

The complete original handover is retained under original_handover so the next researcher can check older code and branches. Its START_HERE, roadmap and manifests describe the original bundle; current root documents and the current research ledger govern this task. No repository URL or commit was supplied and no GitHub inspection is claimed. This package preserves research evidence, not a journal-refereed certification or novelty guarantee.

Run `python verify_handover.py` from this directory. It checks the current outer hash manifest and performs small independent checks of the two modulo-73 fixtures. Existing CSVs and environment records are retained as historical validation evidence. This package's smoke check is not the full research validation suite or a benchmark. Historical nested manifests describe their original bundles; SHA256SUMS.json is authoritative for this handover. The original manuscript and code are copied without requested mathematical revisions.

The outer archive and this prompt can be given together to another AI. If the AI cannot browse or execute code, it must state those limits rather than claim source verification or successful checks.
