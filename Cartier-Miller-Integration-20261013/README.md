# Cartier–Miller integration audit and exact prototype

David Jordan research programme, 13 October 2026. Separate, unrefereed, AI-assisted integration delivery. The published manuscript and repository were not changed. No external repository was inspected and no person was contacted.

Read `CONSOLIDATED_REPORT.md` for the conclusions and `TECHNICAL_SPECIFICATION.md` for the mathematical and software contracts. The prototype unifies existing exact arithmetic; it does not establish a new generic fast boundary, ordinary-scalar or Witt-extraction algorithm.

Extract the whole archive into a normal folder. Standard Python 3.10 or newer suffices for the live prototype and bounded validation. This delivery was executed on Linux with Python 3.12. Windows execution has not been tested. No Qt, QGIS, compiler, FLINT, browser or network connection is required for these commands. Optional GMP is used only if already installed; otherwise polynomial arithmetic uses Python integers.

```bash
python verify_package.py
python validate.py
python -m cm_system sum 13 3
python -m cm_system sum 17 4 --precision 2
python -m cm_system sum 19 4 --method higher:2
python -m cm_system quarter2 13
python -m cm_system row 13 1 2 3 1 --lambda 1
python -m cm_system cartier 11 -35 -98
python -m cm_system plan 1000039 200008
python -m cm_system weighted 13 3 1 2 3
```

The `quarter2` output recovers the Witt residue from an already computed sum. It expressly is not sum-avoiding Witt extraction. The `row`, `branch` and `cartier` commands have distinct targets from the original `sum` command. Primes must be below 2^64; the original-sum service permits p>=5, while row and coefficient services require p>=7. Stopping points satisfy 0<=L<=(p-1)/2. Precision is one or two. User-supplied traces retain an explicit trust status except for the implemented D=-7 shape-and-sign certificate.

In Python, setup can be reused explicitly:

```python
from cm_system.api import Session, Budget, evaluate, branch_query
from cm_system.rows import RowSession

s = Session(1000039)
answers = s.evaluate_many([200008, 400016], method="higher:2")
print([a["U"] for a in answers])

row = RowSession(13, [1, 2, 3, 1])
print(row.query(1))
print(row.query(2))
```

`Budget` controls direct terms, polynomial block width, genus and naive point-count setup. Budget exhaustion is reported; it never produces an approximate result. The automatic policy prefers applicable complete structural methods, then a direct recurrence through 128 terms, then the product tree. This is a conservative policy, not a measured universal crossover. Explicit higher-genus hybrids include boundary work. A zero boundary multiplier skips unnecessary boundary evaluation.

Run `python benchmark.py` to reproduce the focused comparisons. It overwrites only `results/benchmarks.json`, `results/benchmarks.csv` and its own outputs in the extracted working copy. `python validate.py` similarly refreshes its validation result. The packaged immutable result snapshots are also retained in `recorded_results`, so reproducibility runs do not destroy the delivered evidence. Integrity verification should precede reruns: it checks the packaged state and will report intentional result changes afterward.

`PROVENANCE.json` records copied source hashes and package-relative import adjustments. New integration code is in `cm_system/api.py`, `rows.py` and `__main__.py`. The corrected depth recognizers are retained under their original relative tree and checked against the fixed-D table. They are not generic curve recognizers. `evidence` contains governing reports and review qualifications. The delivery's `retained_archives` (original higher-genus, p-adic and native precision-two packages) and the manuscript convenience text are not redistributed in the repository release; `RELEASE_NOTE.md` identifies them by hash and records the refresh of vendored code to the repository's corrected versions. Native archives are evidence, not live backends of this dependency-free prototype.

The earlier Studio GUI is an existing integration demonstration. This delivery provides an arithmetic and contract layer that could later support that interface. It does not replace, modify or claim to retest the GUI.
