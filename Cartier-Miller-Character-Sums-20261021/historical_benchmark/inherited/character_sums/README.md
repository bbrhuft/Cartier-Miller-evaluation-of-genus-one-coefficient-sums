# Cartier–Miller weighted character sums: reproducibility package

Investigation of 20 October 2026 into rationally weighted quadratic-character sums and elliptic-point sums evaluated with the Cartier–Miller oracle. Unrefereed, AI-assisted research code. The manuscript was not modified and nothing was published.

* `REPORT.md` is the research report: theorems, proofs, classification, complexity, evidence and assessment.
* `PROPOSED_APPLICATION_SECTION.tex` is draft manuscript text. It compiles with amsmath, is about two pages, and has not been inserted into the manuscript.

## Layout

| Path | Content |
|---|---|
| `src/cmcs.py` | Candidate implementation (frozen): routing, validation, translation/normalization, multi-pole corrections, constants, affine/projective sums, branch values, bounded extensions, endpoint check |
| `src/reference.py` | Independent ground truth: enumeration (squares table, actual y counts), FLINT powers, PARI traces |
| `src/harness.py` | Check families shared by development and confirmation |
| `src/develop.py`, `src/confirm.py` | Development run; hash-seeded disjoint confirmation run |
| `src/freeze.py`, `src/verify_freeze.py`, `FREEZE.json` | Freeze and its verification |
| `src/verify_character_identities_extended.py` | The supplied verifier's 132 models + example, extended to the inherited Miller evaluator and the candidate |
| `src/exploratory_jets_and_closed_forms.py` | Post-freeze exploratory checks (closed branch form, double poles, polynomial parts, pointwise exclusion, jet counterexample, supplied second-kind data) |
| `supplied/verify_character_identities.py` | Supplied verifier, unchanged |
| `vendor/cm_system/` | Inherited evaluator, unmodified copy from commit `ef23079` (MIT, see `vendor/cm_system_LICENSE`) |
| `results/` | Raw machine-readable outputs |
| `PROVENANCE_INPUTS.json` | Hashes and versions of all inputs |
| `SHA256SUMS.txt` | Hashes of every file in the package |

## Requirements

Python ≥ 3.10. `cmcs.py` uses only the standard library and the vendored `cm_system`. The verification layers also use numpy, python-flint and cypari2 (PARI):

```
pip install numpy python-flint cypari2
```

## Commands (run from this directory)

```
python3 supplied/verify_character_identities.py      # supplied verifier (PASS expected)
python3 src/verify_character_identities_extended.py  # ~1 min
python3 src/develop.py                                # ~4 min; rewrites results/development_*.json
python3 src/verify_freeze.py                          # frozen files unchanged?
python3 src/confirm.py                                # ~9 min; same hash-seeded sample every time
python3 src/exploratory_jets_and_closed_forms.py     # ~10 s
```

Do not rerun `src/freeze.py`: it refuses to overwrite `FREEZE.json`, whose digest seeds the confirmation sample. Rerunning `develop.py` rewrites `results/development_ledger.json`, which is itself frozen. The rewritten file is identical as long as the prime lists in `develop.py` are unchanged.

## Using the candidate

```python
import sys; sys.path.insert(0, 'src')
import cmcs
E = cmcs.Curve(1009, [2, 3, 1, 5], trace=None)        # f(0) = 2; small p: trace counted directly
E.single_pole(0)                                      # pole at 0 (nonbranch): routed through a translation
v, info = E.weighted_sum(simple=[(0, 2), (5, 7)], b=3, kind='affine_points')
Z = cmcs.Curve(1009, [0, 3, 1, 5])                    # f(0) = 0 is allowed ...
Z.truncation(7)                                       # ... and T_f(7) comes back in the original coordinates
Z.classify_pole(0)                                    # 0 is a root of f here: a branch pole
Z.prepare_second_kind()                               # O(p); needed for branch poles and extensions
Z.single_pole(0)
```

A caller-supplied trace is trusted. `E.endpoint_check(mu)` gives a necessary, not sufficient, consistency check.

## Labels used in the report

[I] inherited from the manuscript · [P] inherited from prior project work · [N] proved here · [C] computational observation · [U] unresolved.
