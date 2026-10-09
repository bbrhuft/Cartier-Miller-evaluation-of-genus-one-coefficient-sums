# Changelog

## 2026.10.09 — first public release

This first public release of the Cartier–Miller extension research covers the branch formula, normalized rational 2-isogeny transport, direct recognition through depth two from the stated ordinary easy seeds, and one consolidated depth-three family with CM trace preparation. It also includes the rounded-third obstruction: for p ≡ 2 mod 3, the boundary a_(p+1)/3 equals 3/(2(⌊p/3⌋!)³) mod p, so the complete weighted sum there is equivalent to a Gauss factorial.

Preparing the release added a replacement validator for the closure branch, whose original validator was not retained. It fixed two absolute fixture paths in independent checks. It added an unchanged copy of `elliptic_prefix.py` under retained/, and README, RESULTS, STATUS, REPRODUCTION, PROVENANCE, the MIT LICENSE and CITATION.cff. Every validator was rerun in the release layout, including 2,640 new PARI trace cross-checks. GPL-licensed and paper material was excluded. No theorem, recognizer or evaluator changed.
