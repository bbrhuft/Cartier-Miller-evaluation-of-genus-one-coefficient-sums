# Reproduce the B=0 depth-three adversarial review

Read REVIEW_REPORT.md and PROOF_REVIEW_ADDENDUM.md first. This archive preserves the supplied handover under inputs, together with its companion proof note and ledger. It includes the independent audit, CSVs, JSON results, rerun logs and the optional certificate-schema patch. The published manuscript is untouched and GitHub was not inspected.

With Python 3.10 or later, run:

```bash
python run_review.py
```

This extracts the unchanged input, verifies its hashes and smoke checks, reruns its B=0 exact derivation and validation, and executes the independent audit. No network access or third-party package is required. If cypari2 happens to be installed, the inherited suite performs optional PARI checks. In the present review environment it was unavailable, and that limitation is recorded explicitly. Run without Python's -O option; these research scripts use assertions for validation.

The independent script treats the original recognizer as a black box. It uses its own exact quotient derivation, Fraction-based determinants and resultants, brute-force graph with the previous dual root in the state, literal point counts, coefficient expansions, dense original-cubic references and affine group arithmetic for large trace-sign witnesses. The scripts' elapsed time is diagnostic only, not an arithmetic benchmark.

SCHEMA_FIX.patch applies to the extracted inherited tree. The patched module is also included under patched for inspection. Only unknown nested certificate keys are newly rejected; the curve arithmetic is unchanged. PATCH_VALIDATION.json records a valid certificate and an injected unknown-key control. The full inherited validation was run before the schema change. Rerunning the independent audit uses the unmodified source under inherited by design, so it retains and documents the original counterexample.

SHA256SUMS.json hashes every file delivered in this review archive except itself. The original handover has its own manifest. Saving and source hashes are independent of filesystem metadata. ENVIRONMENT.json records the interpreter and platform. The report counts do not combine overlapping validation routes as independent observations.
