# Reproduction

Run every command from the repository root. Python 3.10 or later with the standard library is sufficient unless the table says otherwise. SymPy is needed for the symbolic derivation and transport checks. cypari2 (with PARI) is needed for one independent script and enables optional trace cross-checks in the depth-three validator; without it, that validator skips the cross-checks and still passes. The recorded rerun used Python 3.13, SymPy 1.14.0, cypari2 2.2.4 and PARI 2.17.2.

Most validators rewrite their result files in place, in the same directory. To regenerate evidence without altering the committed records, run them in a separate clone or copy. Alternatively, restore the committed files afterwards with `git checkout -- research`. A regenerated file normally differs only in environment, timing and source-hash fields. The exceptions are explained in evidence/rerun_20261009/README.md.

## Smoke check and examples

| Command | Expected result |
|---|---|
| `python verify_release.py` | Status passed, with every hash in SHA256SUMS.json matching; well under a second |
| `python research/depth_two_recognition_20261006/core/cli.py --p 17 --short 8 2` | Recognized depth-two certificate with a verified reverse path to the B=0 seed |
| `python research/depth_two_recognition_20261006/core/cli.py --p 13 --f 1 12 0 9 --trusted-trace -2 --mu 7` | H=11, K=8, T=2 from a caller-trusted trace |
| `python research/depth_three_recognition_20261007/core/cli.py --p 73 --f 1 4 0 37 --cm --mu 9` | H=10, K=55, T=3 by the restricted CM route with the deterministic sign; only the √−3 search is randomized |
| `python research/depth_three_recognition_20261007/core/cli.py --p 73 --f 1 4 0 37 --cm --sign-method las_vegas --unbounded-sign-test --mu 9` | The same values with the zero-error Las Vegas sign test |

If you edit any tracked file, the hash check in verify_release.py will fail until SHA256SUMS.json is regenerated. That is intended.

## Full validation

Times are wall-clock seconds from the 9 October rerun, which ran 17 jobs in parallel on two cores. They are indicative only and are not benchmarks.

| Branch | Command | Needs | Time (s) |
|---|---|---|---|
| Branch point | `python research/branch_point_20261006/validate.py` | stdlib | 20 |
| Closure (replacement) | `python research/isogeny_closure_20261006/replacement_validation_20261009/check_closure_replacement.py` | stdlib | 20, run alone |
| Depth-two recognition | `python research/depth_two_recognition_20261006/core/validate_direct.py` | stdlib | 7 |
| Depth-two parameters | `python research/depth_two_recognition_20261006/theory/check_recognition.py` | stdlib | 1 |
| Depth-two integer invariants | `python research/depth_two_recognition_20261006/theory/check_integer_invariants.py` | stdlib | 0.3 |
| Finite higher-depth graph | `python research/depth_two_recognition_20261006/audit/audit_depth_three.py` | stdlib | 11 |
| Depth-three family | `python research/depth_three_recognition_20261007/core/validate_depth_three.py` | stdlib; cypari2 optional | 29 |
| Depth-three certificates and API | `python research/depth_three_recognition_20261007/core/validate_consolidation.py` | stdlib | 2 |
| Depth-three integer invariants | `python research/depth_three_recognition_20261007/theory/check_integer_invariants_depth3.py` | stdlib | 0.6 |
| Depth-three symbolic derivation | `python research/depth_three_recognition_20261007/theory/derive_family.py` | SymPy | 6 |
| Depth-three symbolic transport | `python research/depth_three_recognition_20261007/theory/verify_transport.py` | SymPy | 4 |
| Independent Cartier checks | `python research/depth_three_recognition_20261007/independent/indep_cartier.py` | stdlib | 10 |
| Independent adversarial checks | `python research/depth_three_recognition_20261007/independent/indep_attack.py` | stdlib | 7 |
| Independent PARI checks | `python research/depth_three_recognition_20261007/independent/indep_extra.py` | cypari2 | 15 |
| Independent symbolic checks | `python research/depth_three_recognition_20261007/independent/indep_symbolic.py` | SymPy | 10 |
| Independent Theorem 4 check (10 October) | `python research/depth_three_recognition_20261007/independent/indep_sextic_theorem4_20261010.py` | cypari2 | about 10 |
| Rounded third point | `python research/rounded_third_boundary_20261009/validate_rounded_third.py` | stdlib | 6 alone, 19 in parallel |
| Fresh transport cross-check | `python research/rounded_third_boundary_20261009/independent_transport_check.py` | stdlib | 19 in parallel |

## Benchmarks

No benchmark is included. Any future performance claim must charge trace preparation, certification and reconstruction. It must compare identical outputs modulo the same modulus, and distinguish cached queries from complete runs. It must retain raw CSVs, source hashes, the environment and validation records. At the rounded third point, a complete weighted sum must include the cost of the boundary. The O(log p) prefix alone is not a complete cost.
