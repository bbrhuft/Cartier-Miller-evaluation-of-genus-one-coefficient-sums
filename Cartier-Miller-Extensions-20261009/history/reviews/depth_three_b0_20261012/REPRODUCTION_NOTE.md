# Reproducing this review

This directory keeps the B=0 depth-three adversarial review of 12 October 2026: its reports, independent audit script, CSV and JSON results, logs, the schema patch and the patched module. The review's input archive (`inputs/Depth_Three_Recognition_Handover_20261012.zip`) is **not** redistributed here. It contains the full transfer handover, including the manuscript and GPL-licensed benchmark code that this MIT release excludes (see PROVENANCE.md). Only its two Markdown inputs, the proof note and ledger as reviewed, are kept in `inputs/`.

`run_review.py` and `independent_audit.py` therefore need the original review archive. They expect the unmodified handover under `inherited/`, and the audit deliberately uses that unpatched source to retain the original schema counterexample. The B=0 code as integrated into this release, with the schema patch applied, is validated by `research/depth_three_recognition_20261007/core/validate_depth_three_b0.py`.
