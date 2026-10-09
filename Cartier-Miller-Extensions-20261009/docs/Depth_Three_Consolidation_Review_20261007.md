# Depth-three consolidation review

7 October 2026. The bounded result now has a reviewable trace-sign success argument, corrected implementation scope reporting and fresh validation. It remains an unrefereed computational mathematics extension. No manuscript revision, performance benchmark, priority claim or GitHub inspection has been made.

The inherited result is one explicit depth-three family from the ordinary j=0 seed at primes p≡1 modulo 24, with direct parameter recovery, verified rooted paths, quadratic-twist handling and β=−(7+6e+6g+2eg)rH. Its curves are classical CM curves of discriminant −192. The current work consolidates their use for normalized coefficient recovery rather than asserting that the curves are new.

| Change | Result | Evidence and limitation |
|---|---|---|
| Close the trace-sign complexity gap | Each raw uniform-x trial succeeds with probability ≥1/5; unbounded execution has at most five trials in expectation | Proper-subgroup proof, with eight exact p=97 point certificates; depends on the recognized-family two-candidate trace theorem |
| Charge complete preparation | Expected O(log²p) field operations plus polynomial integer work; includes candidate preparation, square roots, scalar multiplications and K reconstruction | Conservative O(log⁴p) bit bound with elementary multiplication/inversion; no measured speed claim |
| Report capped execution honestly | Default cap is 64, with inconclusive bound ≤(4/5)^64; `--unbounded-sign-test` exposes almost-sure completion | Returning no answer is distinct from returning an incorrect answer; no automatic Schoof backend |
| Retain decisive sign evidence | CM preparation and verified supplied-trace preparation retain point witnesses; a re-verifier checks both scalar multiplications | Certificate uses the two-candidate theorem; not general order certification |
| Correct partial recognition | Negative status is `not_in_implemented_families` | Deferred B=0-seed depth-three models are no longer labelled unreachable |
| Preserve a real obstruction | E:y²=x³+19 over F_97 has order 112, and every point is killed by 28 | Both candidates 84 and 112 kill all points; the sign success bound cannot be generalized to every easy seed |
| Preserve mathematical normalization | Differential scale +1, exact-correction signs, dual square scaling and original-cubic β-to-K relation retained | Explicit local checks in the companion trace note accompany the inherited global identity |

Fresh full validation passed on 1,215,024 nonsingular short models at ten eligible primes, accepting 12,480 family models and rejecting 1,202,544 non-members with no mismatch. It recomputed 2,640 coefficient pairs, checked 702 twists, rejected 15 tampered parameter certificates, verified 48 normalized cubics and 96 direct branch sums, and tested 27 CM preparations. The new validator independently checks eight proof witnesses, scans the actual raw-x success sets on 40 small-prime representatives, forces capped failure and tests all eight retained examples of the deferred B=0-seed chain. These checks support the formulas and implementation; they are not the source of the uniform success theorem.

PARI and Sympy were unavailable in this environment. Original PARI results, symbolic derivations, source hashes and the independent AI worker's report are retained as historical records. No new PARI confirmation of large-prime traces is claimed. The current exact-integer invariant script was rerun, and fresh environments and current source hashes accompany the validation CSVs. The previous manuscript PDF was preserved byte for byte.

The most useful human review is of the direct relative-norm recognition proof, its denominator/collision exclusions, the CM trace proposition's special j=0 volcano argument, and the new subgroup/sampler bound. The last bound is elementary once the two trace candidates are justified. A literature-priority assessment remains separate. Schoof retains the unconditional deterministic setup; the restricted CM preparation is a zero-error randomized alternative. The prototype accepts primes below 2^64 and expects a supplied root for queries.

This work covers one family and branch/root evaluations. It does not give every stopping index, the other depth-three chain, generic or supersingular K recovery, a new production SEA backend or a sum-avoiding Witt correction. An original weighted-sum claim still needs both B_L and a_L. The next step is focused mathematical review of this package before broader extensions or performance claims.
