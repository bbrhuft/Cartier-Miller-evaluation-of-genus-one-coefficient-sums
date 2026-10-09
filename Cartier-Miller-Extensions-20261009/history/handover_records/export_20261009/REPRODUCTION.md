# Reproduction for the consolidated depths

Python 3.10+ standard library suffices for the active prototypes and small smoke checks. Preserve the package layout and run commands from its root.

```bash
python verify_handover.py
python research/depth_two_recognition_20261006/core/cli.py --p 17 --short 8 2
python research/depth_two_recognition_20261006/core/cli.py --p 13 --f 1 12 0 9 --trusted-trace -2 --mu 7
python research/depth_three_recognition_20261007/core/cli.py --p 73 --f 1 4 0 37 --cm --unbounded-sign-test --mu 9
```

The depth-two examples return a checked n2 certificate and H=11,K=8,T=2 respectively; the supplied trace remains caller-trusted. The depth-three cubic returns H=10,K=55,T=3 through its restricted CM route. The uncapped randomized command has expected, not deterministic, completion cost.

| Branch | Full validation commands |
|---|---|
| Depth-two recognition | python research/depth_two_recognition_20261006/core/validate_direct.py |
| Depth-two parameters | python research/depth_two_recognition_20261006/theory/check_recognition.py |
| Depth-two integer invariants | python research/depth_two_recognition_20261006/theory/check_integer_invariants.py |
| Finite higher-depth graph | python research/depth_two_recognition_20261006/audit/audit_depth_three.py |
| Depth-three family | python research/depth_three_recognition_20261007/core/validate_depth_three.py |
| Depth-three finite certificates and API | python research/depth_three_recognition_20261007/core/validate_consolidation.py |
| Depth-three integer invariants | python research/depth_three_recognition_20261007/theory/check_integer_invariants_depth3.py |
| Rounded third boundary (9 October) | python research/rounded_third_boundary_20261009/validate_rounded_third.py (about 6 s to p=20,000; writes results/validation.json and results/rounded_third_values.csv) |

These commands regenerate evidence and may take substantial time. Regeneration changes recorded environment and outer file hashes; it does not retroactively change the preserved validation snapshot. Optional symbolic scripts need Sympy and optional PARI checks need their documented dependencies. Neither was newly available in the previous consolidation. The original depth-one closure command documentation is retained in its report and theory note; the code and its supporting records remain complete in the package.

EXPORT_VALIDATION_20261009.json records the checks run for the 9 October continuation. The earlier export reran the package hash/small fixture verifier and the three CLI examples in a fresh extraction. It does not rerun the full exhaustive suites or make benchmark claims. EXPORT_VALIDATION.json records exactly the packaging checks. Nested historical manifests retain their original scope; SHA256SUMS.json governs the whole current export.
