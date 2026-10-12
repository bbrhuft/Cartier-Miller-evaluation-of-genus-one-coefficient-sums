# Ordinary Cartier slope from canonical-lift data: consolidated package, revision 2 (12 October 2026)

Start with `Ordinary_K_Feasibility_Note_20261012_rev2.md`, then `CHANGES.md`. The updated ledger is `RESEARCH_LEDGER_Ordinary_K_20261012_rev2.md`. Revision 2 incorporates the independent review document and its evidence, both preserved under `evidence/review_20261012/`.

The conclusion is narrow. The constructions examined here did not yield a cheaper complete algorithm for κ = β/H, and whether canonical-lift or Serre–Tate data could give a shortcut remains unresolved.

Two exact statements are derived. Theorem A: in the low-pole basis, Frobenius modulo p is [[0, −β],[0, H]]. Lemma B: for any ordinary short Weierstrass lift, the canonical-subgroup kernel sum satisfies σ_C ∈ pZ_p and κ ≡ σ_C/p. Lemma B now comes with an explicit integral comparison and sign tracking, and its classical inputs are listed with their verification status. As the review recommends, its integral-model and comparison steps should have specialist review. Three further recovery formulas are derived. Each recovers κ from a scalar equivalent to it given t, which is a statement about information, not difficulty. No lower bound, speed-up or novelty is claimed.

| Path | Contents |
|---|---|
| `Ordinary_K_Feasibility_Note_20261012_rev2.md` | Revised note: outcome, Theorem A, Lemma B with its classical-input table, Propositions C–E, information audit, representation table, dependency and cost table with bound types, source audit, run families, status separation, plain-language conclusion |
| `CHANGES.md` | Each review finding (revision 1) and each statement of the review document (revision 2), with its resolution and any remaining limitation |
| `RESEARCH_LEDGER_Ordinary_K_20261012_rev2.md` | Updated ledger and dependency table |
| `ordinary_k_pilot/` | Repaired pilot. `okp_config.py` (explicit dependencies), `run_all.py` (runner), `charp_identities.py`, `serre_derivative_check.py`, `kummer_degree_check.py` (field of definition of Kummer coordinates), `padic_canonical_subgroup.py` (Lemma B, with precision floor), `retained_dependency_check.py`, `coverage.py`, `failure_injection.py`, and raw outputs in `results/` |
| `independent_check/` | Repaired independent drivers (`harness.py`, `c1_cech.py`, `c1_kedlaya.py`, `c1_extra.py`, `c2_formal.py`, `c3_etale.py`, `c4_c5.py`, `l3_katz_signs.py`), `run_independent.py` and `inject_failures.py`, with raw outputs in `results_full/` and `results_injection/` |
| `evidence/` | Unchanged originals: the revision-0 and revision-1 bundle ZIPs, the original independent-check sources and outputs, and `review_20261012/` (the review document and its evidence ZIP) |
| `handover_verification.md` | What was run from the received handover |
| `ENVIRONMENT.json`, `SHA256SUMS.json` | Environment and hashes of every file |

Reproduction needs the received handover, extracted and unpacked with its own `unpack_support.py`, and Python 3 with the standard library only. All paths are explicit. A missing dependency stops the run with exit status 2; it is never skipped.

```bash
H=<path>/Ordinary_K_Research_Handover_20261012      # after running its unpack_support.py
S=$H/support/CM_Cartier_Adversarial_Review_20261012  # created by unpack_support.py
DEPS="--retained $S/context/CM_Cartier_Research_Handover_20261012/retained/inherited/research \
      --extension $S/source/CM_Cartier_Extension_20261012 --handover $H"
python -I ordinary_k_pilot/run_all.py $DEPS              # ALL_PASS, exit 0
python -I ordinary_k_pilot/failure_injection.py $DEPS    # FAILURE_INJECTION_DETECTED_ALL
T=$H/validation/results/ordinary_targets.csv
python -I independent_check/run_independent.py --profile full --targets $T     # INDEPENDENT_RUN_PASS
python -I independent_check/inject_failures.py --targets $T --original evidence/original_independent_check
```

Exit statuses are 0 (pass), 1 (mathematical disagreement), 2 (missing dependency), 3 (explicitly reduced scope) and 4 (vacuous run). The runners fail on anything other than 0. The repaired runs recorded here took about 40 seconds (pilot), about 3 minutes (pilot failure injection) and about 19 minutes (independent full profile) under Python 3.13.16. These are reproducibility notes, not benchmarks.

Revision 1 was prepared from a description of the independent review; revision 2 checks the review document itself, statement by statement. The independent drivers are not part of `run_all.py`; they have their own runner and failure injection.
