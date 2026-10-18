# Amendment R3.1 to the frozen round-3 candidate

This amendment is written and hash-frozen in `r3/FREEZE_R3_1.json` after the frozen R3 confirmation (run 1) failed. It is frozen before any R3.1 confirmation prime is selected. `CANDIDATE_R3.md`, `r3/FREEZE_R3.json` and every file they hash are unchanged and still verify. All changes are additive new files.

## What failed

Run 1 completed 88 cases, all exact. It covered set S for classes A and B, set M for class A and for class B with q ≤ 83, set L for class A, and sets E1, E2 and E4 for class A. It then stopped at set M, class B, q = 89, p = 3000013781. FLINT LLL with δ = 0.99 returned no vector of the known minimal trace norm (q−1)p; its best reduced vector had 18 times that norm. The frozen exact-enumeration fallback, PARI `qfminim` with flag 0, raised "precision too low". Its documented floating-point mode requires d·max|G|² < 2^53, while the Gram entries are of size (qp)², so this fallback could never have run at the sizes used. No value was returned and no identity was contradicted, but the frozen candidate did not pass confirmation. The record is in `r3/evidence/CONFIRMATION_R3_RUN1_SUMMARY.json` and `CONFIRMATION_R3_run1_FAILED.log`.

## What changes

The mathematical statements R1, R2, T3 and T4 of `CANDIDATE_R3.md` are unchanged. Only the lattice step and the policy constants change, as follows.

The lattice step is `r3/jacobi_r31.py` (`JacobiContextR31`). It runs FLINT LLL with δ = 0.999 on the integral embedding, then δ = 0.9999 on that output. After that it tries up to four seeded re-randomised bases at δ = 0.999, and otherwise raises. There is no enumeration. Every candidate is still certified by membership, x·x̄ = p and van Wamelen's selection, so correctness never depends on LLL, only termination does. Post-freeze development (`DEV_LLL_DELTA.json`, 12 random primes per prime q ≤ 89) recorded LLL misses for δ = 0.99 at q = 83 (1 of 12) and q = 89 (3 of 12), and for δ = 0.999 at q = 89 (1 of 12). The chain recovered every observed miss, including the run-1 case.

The interface is `r3/acquire_r31.py`. If the chain raises, it degrades to the next admissible q, then to the fallback route, and records this in `metadata['degraded']`.

The policy is `r3/POLICY_R3_1.json`. Its SVP table is the maximum of the R3 and R3.1 development measurements, with q = 89 set to 1.9 s to include the observed retry rate. The range 5 ≤ q ≤ 89, K ≥ 10^4, the interval model, the anchors (dup12 for p ≡ 5 mod 12, else dup6), the separate-channel layout and the fallbacks are unchanged.

## Development inputs added to the ledger

`r3/evidence/LEDGER_R3_1.json` contains the R3 ledger, every prime selected by the R3 confirmation rule in run 1 (145 primes, whether or not their case completed), and the 283 post-freeze development primes.

## Confirmation and benchmark rules

`r3/confirm_r3_1.py` has the same structure and checks as `r3/confirm_r3.py`. It uses the R3.1 modules and ledger, with fresh bounds: S at 2.5·10^6, M at 4·10^9, L at 4·10^11, E1 at 5·10^10, E2 at 4·10^9, E3 at 3.5·10^5 and E4 at 2·10^10. A labelled regression block reruns the run-1 failure and the development miss; it is not counted as confirmation. `r3/benchmark_r3_1.py` uses the same rule as `r3/benchmark_r3.py`, with the R3.1 modules and the R3.1 selection.
