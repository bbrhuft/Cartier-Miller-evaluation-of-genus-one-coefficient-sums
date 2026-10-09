# Direct depth-two recognition and higher-depth research

Python3.10+ standard-library research prototype. The archive includes the retained branch_evaluator.py and isogeny_closure.py dependencies in their original relative layout. No GitHub URL/commit is claimed and no manuscript is changed.

Direct parameter recognition, without any trace or square-root computation:

```bash
python research/depth_two_recognition_20261006/core/cli.py --p 17 --short 8 2
```

This returns the n2 family with e6,r1 and a checked reverse path. Original-cubic preparation with a caller-trusted exact trace is:

```bash
python research/depth_two_recognition_20261006/core/cli.py --p 13 --f 1 12 0 9 --trusted-trace -2 --mu 7
```

The output is H11,K8,T2 and a certificate. The Hasse interval check is not trace certification. The separate retained path finder can use higher-depth certificates; direct recognition is complete only through depthtwo.

Reproduction commands from the archive root:

```bash
python research/depth_two_recognition_20261006/core/validate_direct.py
python research/depth_two_recognition_20261006/theory/check_recognition.py
python research/depth_two_recognition_20261006/theory/check_integer_invariants.py
python research/depth_two_recognition_20261006/audit/audit_depth_three.py
```

These are correctness audits, not benchmarks. They regenerate CSV/JSON outputs. The report, theory note and graph note distinguish algebraic derivations from finite coverage. SHA256SUMS_ALL.json covers source, evidence, dependencies and the updated ledger.
