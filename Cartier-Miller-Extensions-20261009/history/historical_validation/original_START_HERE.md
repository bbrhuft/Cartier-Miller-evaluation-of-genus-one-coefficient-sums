# Depth-three recognition handover

7 October 2026. This package delivers the bounded target set by the previous handover: one explicit depth-three family reachable from the ordinary $j=0$ easy seed by explicitly normalized degree-two isogenies, with a direct parameter-checked recognition certificate, a trace proposition that removes point counting from complete preparation, a runnable prototype and CLI, validation artifacts, an independent adversarial report, an updated research ledger and the complete previous handover for context. The published manuscript is historical context and is unchanged. No repository URL or commit was supplied and no GitHub inspection is claimed. Proofs are unrefereed.

| Read order | File | Purpose |
|---|---|---|
| First | PROJECT_STATE.md | Status table and the retained normalizations |
| Next | research/depth_three_recognition_20261007/Depth_Three_Recognition_Proof_Note_20261007.md | The family, the recognition theorem, exceptional primes, the trace proposition, costs, and what is proved versus tested versus deferred |
| Next | research/Cartier_Miller_Extension_Ledger_20261007.md | The retained ledger with the new 7 October entry at the end (question, assumptions, derivation, checks, corrections, deferred items) |
| Evidence | research/depth_three_recognition_20261007/core/validation.json and the CSV files beside it | Exhaustive classification, coefficient, twist, tamper, cubic, large-prime and CM-trace checks with source hashes and environment |
| Evidence | research/depth_three_recognition_20261007/theory/integer_invariants_depth3.json | Every integer factorization used in the exceptional-prime and collision arguments, standard library only |
| Independent | research/depth_three_recognition_20261007/independent/INDEPENDENT_VALIDATION_REPORT.md | Second worker's own derivations, attacks, literature checks and criticisms; the reconciliation is in the proof note |
| Code | research/depth_three_recognition_20261007/core/depth_three_recognize.py, cli.py; retained branch_evaluator.py, isogeny_closure.py, recognize.py in their original relative layout | Preserve the layout; the new code imports the retained modules |
| Fixtures | fixtures/depth_three_recognition_fixtures.json, fixtures/depth_three_p73.json, fixtures/depth_three_four_certificates_20261006.csv | Regression fixtures, not proofs |
| Prior work | previous_handover/ | The complete 6 October handover, including the original manuscript, code and historical branches |

Run `python verify_handover.py` from this directory. It checks SHA256SUMS.json and performs small independent checks of the fixtures and of the recognizer, including the complete CM preparation on the modulo-73 cubic and a 63-bit member. The full validation is `python research/depth_three_recognition_20261007/core/validate_depth_three.py` (about twenty seconds; standard library, with PARI used as an optional extra trace source if cypari2 is installed). Neither is a benchmark.

What remains open is stated in the proof note's penultimate sections: the $B=0$-seed depth-three chain (dihedral class field), depth four and all-family classification, a deterministic trace-sign rule from a verified primary source, and generic or supersingular $K$ recovery. The next AI or human reviewer should read the proof note critically before extending anything; the independent report lists the sentences that were challenged and how they were resolved.
