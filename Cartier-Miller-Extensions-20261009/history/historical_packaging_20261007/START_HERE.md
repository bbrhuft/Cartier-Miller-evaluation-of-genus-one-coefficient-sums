# Consolidated depth-three recognition handover

7 October 2026. The first depth-three family from the ordinary j=0 seed has been consolidated for human mathematical review. The family and recognition derivation are inherited research claims; this pass adds an explicit trace-sign success bound, exact finite certificates, a retained obstruction to overgeneralization, corrected status reporting and fresh validation. The published manuscript is unchanged. No repository URL or commit was provided, and no GitHub inspection or publication is claimed.

| Read order | File | Purpose |
|---|---|---|
| First | Depth_Three_Consolidation_Review_20261007.md | Outcome, changes, evidence and remaining limits |
| Next | PROJECT_STATE.md | Current mathematical and implementation status |
| Mathematics | research/depth_three_recognition_20261007/Depth_Three_Recognition_Proof_Note_20261007.md | Family, parameter recovery, normalized paths, collision exclusions and CM trace proposition |
| New mathematics | research/depth_three_recognition_20261007/TRACE_SIGN_BOUND_20261007.md | Proper-subgroup proof, eight small-prime witnesses, actual sampler probability, costs and obstruction |
| Current evidence | research/depth_three_recognition_20261007/core/validation.json and consolidation_validation.json | Fresh runs with source hashes and environment; supporting evidence, not general proofs |
| Exact proof certificates | research/depth_three_recognition_20261007/core/sign_bound_p97_witnesses.csv | Eight points establishing the finite proper-subgroup lemma |
| Obstruction | research/depth_three_recognition_20261007/core/sign_test_obstruction.json | Easy seed at p=97 where the generic sign test can never decide |
| Code | research/depth_three_recognition_20261007/core/depth_three_recognize.py and cli.py | Repaired prototype; preserve research-relative import layout |
| Ledger | research/Cartier_Miller_Extension_Ledger_20261007.md | Chronological ledger; final consolidation entry controls current status |
| Prior evidence | historical_validation/ and research/depth_three_recognition_20261007/independent/ | Original results and AI-worker report, preserved as historical evidence |
| Earlier scope and branches | previous_handover/ | Original manuscript, code, research handover and retained unsuccessful approaches |
| Reproduction | REPRODUCTION.md | Executable commands and limits of fresh validation |

Run `python verify_handover.py` from this directory for hash checks and small exact fixture checks, including the eight new point certificates. SHA256SUMS.json is the current outer manifest; nested and historical manifests describe their original snapshots. Full validation and its regenerating commands are separate. This package has no new performance benchmark and no referee or priority certification.

The prototype accepts primes below 2^64. The mathematical success-bound argument is stated for every prime in the eligible class, subject to review of the inherited family and CM trace proposition. The partial combined recognizer covers depth≤2 plus this one depth-three family; `not_in_implemented_families` is deliberately not a certificate of non-reachability in the full depth-three graph. The other depth-three chain from the B=0 seed remains deferred.
