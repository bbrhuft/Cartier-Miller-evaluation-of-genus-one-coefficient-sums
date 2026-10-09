# Depth-three direct recognition (j=0-seed chain, discriminant −192)

Python 3.10+ standard-library research prototype. The retained `branch_evaluator.py`, `isogeny_closure.py` and `recognize.py` are included unchanged under `../branch_point_20261006`, `../isogeny_closure_20261006/core` and `../depth_two_recognition_20261006/core`; keep this relative layout. No GitHub URL or commit is claimed and no manuscript is changed.

| Path | Purpose |
|---|---|
| `TRACE_SIGN_BOUND_20261007.md` | Consolidated success bound, finite witnesses, sampler costs and seed obstruction |
| `Depth_Three_Recognition_Proof_Note_20261007.md` | Reviewable proof note: family, recognition theorem, exceptional primes, trace proposition, costs, status |
| `core/depth_three_recognize.py` | Recognizer, certificate verifier, trusted-trace and complete CM preparation |
| `core/cli.py` | JSON command line |
| `core/validate_consolidation.py` | New finite proof certificates, independent group law, witness and failure/status tests |
| `core/validate_depth_three.py` | Validation suite; regenerates `validation.json` and the CSV files |
| `theory/check_integer_invariants_depth3.py` | Standard-library reproduction of every integer in the proof note's table (`integer_invariants_depth3.json`) |
| `theory/derive_family.py`, `theory/verify_transport.py` | Sympy derivation of the family and symbolic re-check of the retained transport (need sympy; PARI optional) |
| `independent/` | Second worker's independent scripts, results and adversarial/literature report |

Direct recognition from the short coefficients, no trace needed:

```bash
python core/cli.py --p 73 --short 4 16
```

returns $(e,g,r)=(21,41,42)$, multiplier $15$, the forward and reverse paths. Preparation of an original normalized cubic with a caller-supplied exact trace (necessary CM condition enforced; `--verify-sign` adds a Las Vegas sign check), or by the complete CM route with no supplied trace:

```bash
python core/cli.py --p 73 --f 1 4 0 37 --trusted-trace 10 --verify-sign --mu 9
python core/cli.py --p 73 --f 1 4 0 37 --cm --unbounded-sign-test --mu 9
```

Both give $H=10$, $K=55$, $T_f(9)=3$. The default capped CM route can return `trace_sign_inconclusive`; its cap is 64 raw draws. The unbounded route has at most five raw draws in expectation under independent uniform randomness. `--through-depth-two` combines the retained depth-two recognizer with this one and reports `not_in_implemented_families` for uncovered cases; `--verify-certificate cert.json` reverifies a stored certificate field by field.

Reproduction from this directory:

```bash
python core/validate_depth_three.py
python core/validate_consolidation.py
python theory/check_integer_invariants_depth3.py
python theory/verify_transport.py      # needs sympy
python theory/derive_family.py         # needs sympy; cypari2 optional
```

These are correctness audits, not benchmarks. Eligible primes are $p\equiv1\pmod{24}$; the family's smallest prime is $73$. The recognizer covers only the depth-three chain descending from the $A=0$ seed; the chain descending from the $B=0$ seed is deferred.
