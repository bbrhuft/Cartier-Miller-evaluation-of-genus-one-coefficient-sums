# Received-handover verification record

The handover ZIP was extracted unchanged into its own directory. `python verify_handover.py` returned "Verified 67 packaged files and selected historical provenance" with exit status 0.

`validation/reference_controls.py` was run on a separate copy so that the received results stayed untouched. It printed REFERENCE_CONTROLS_PASS with 1,428 nonsingular models, 1,256 ordinary targets, 172 supersingular controls, 2,512 twist checks, 996 outside-table rows, 8 same-trace pairs, 5 known CM controls, 120 original cubics and 51 branch queries. `ordinary_targets.csv`, `same_trace_different_slopes.json`, `known_CM_controls.json` and `original_cubic_controls.json` were byte-identical to the received copies. `reference_summary.json` differed only in its environment fields (Python 3.13.16 here, 3.12.14 in the handover).

`unpack_support.py`, run on the same copy, verified 88 review artifacts and the nested review hashes, and confirmed that `depth_three_recognition_20261007/core/depth_three_b0_recognize.py` is present. It printed the RETAINED_RESEARCH directory used by the pilot. The pilot imported only `source/CM_Cartier_Extension_20261012/core/fixed_D_evaluator.py` (SHA-256 69ec093b5d7f874c2f12021bb4796c8f0883c05f9f9f9e8e1bc9e38345850742; table cm_tables.json 66bbf3b00fd35bbe09f1f2cd49b4cb49ef24b4dc83e0119772aafbd4b9d3f63f). It recorded, without executing them, the completed `depth_three_recognize.py` (b3bffe46aa792aa82c63035b1928d8acf67dd12882d34bcc03967b00d064a1c2) and `depth_three_b0_recognize.py` (a7142c42e1a748612a961ec9f4e185589569f4de2b398ff7fe0c8f293b95614a).

The retained native BGS sources (`historical_precision_two/native.c` and `preserved/native_mod_p/bgs_native.c`) were inspected and not built. They implement the historical quarter-family and fifth-point recurrences. They are not a generic β backend for arbitrary short models, so no native comparator for the present target exists in the retained material.

## Revision 1 additions

For revision 1 the pilot no longer reads environment variables implicitly. Each script takes `--retained`, `--extension` and `--handover`, checks that the expected files are present, and stops with exit status 2 if they are not. The paths actually used, together with the hashes of every imported retained module, are in `ordinary_k_pilot/results/retained_dependency_check.json` and `ordinary_k_pilot/results/RUN_REPORT.json`.

The retained imports were confirmed against the retained manifests and executed. `fixed_D_evaluator.py` and `cm_tables.json` match the extension's SHA256SUMS.json. The completed `depth_three_b0_recognize.py`, `depth_three_recognize.py`, `recognize.py`, `isogeny_closure.py` and `branch_evaluator.py` match the inherited research SHA256SUMS.json and are the modules actually loaded. The extension tables equal the handover's `knowledge/retained_CM_tables.json`.

The independent checks take the target CSV through `--targets` or `ORDK_TARGETS`. The SHA-256 of the CSV used is recorded in `independent_check/results_full/RUN_REPORT.json`.
