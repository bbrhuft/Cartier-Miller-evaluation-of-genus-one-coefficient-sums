# Changelog

## 2026.10.10 — deterministic trace sign and cost correction

The depth-three CM preparation now fixes the trace sign deterministically by Ireland and Rosen (1990, Ch. 18, Theorem 4) applied to the j = 0 seed. Only the cubic-nonresidue search for √−3 remains randomized. The consolidated zero-error Las Vegas test, with its 1/5 bound, is kept as `sign_method='las_vegas'`. The supplied update was merged onto the consolidated code rather than replacing it, so no consolidation repair was lost. A new note, DETERMINISTIC_TRACE_SIGN_20261010.md, records the rule, and a new independent PARI check passed on 2,075 curves. The depth-three validation outputs were regenerated for the new code.

The rounded-third cost statement was corrected. A classical ECCC report (Tal, TR26-211, unrefereed) claims randomized p^{1/2−δ} factorial algorithms for most primes, and a deterministic logarithmic-factor improvement for every prime. The equivalence with ⌊p/3⌋! mod p is unchanged, and no polylogarithmic method is known. The received update files are kept in history/handover_records/depth_three_update_20261010/.

## 2026.10.09 — first public release

This first public release of the Cartier–Miller extension research covers the branch formula, normalized rational 2-isogeny transport, direct recognition through depth two from the stated ordinary easy seeds, and one consolidated depth-three family with CM trace preparation. It also includes the rounded-third obstruction: for p ≡ 2 mod 3, the boundary a_(p+1)/3 equals 3/(2(⌊p/3⌋!)³) mod p, so the complete weighted sum there is equivalent to a Gauss factorial.

Preparing the release added a replacement validator for the closure branch, whose original validator was not retained. It fixed two absolute fixture paths in independent checks. It added an unchanged copy of `elliptic_prefix.py` under retained/, and README, RESULTS, STATUS, REPRODUCTION, PROVENANCE, the MIT LICENSE and CITATION.cff. Every validator was rerun in the release layout, including 2,640 new PARI trace cross-checks. GPL-licensed and paper material was excluded. No theorem, recognizer or evaluator changed.
