# Verification for the paper (current draft 24 October 2026)

This folder accompanies [`Cartier_Miller_Paper_Rewrite_Corrected_20261024.pdf`](../Cartier_Miller_Paper_Rewrite_Corrected_20261024.pdf), the draft dated 24 October 2026. The folder keeps its original 22 October name, after the first version of the rewrite. The search that led to Section 6.3 is in [`../Cartier-Miller-Congruence-Search-20261024/`](../Cartier-Miller-Congruence-Search-20261024/).

| File | Contents |
|---|---|
| `Cartier_Miller_Paper_Rewrite_Corrected.tex` | LaTeX source of the paper (pdfLaTeX; standard AMS, `hyperref`, `xurl`, `enumitem`, `booktabs`, `microtype` packages) |
| `cm_verify.py` | Pure Python 3 script (3.8+, no dependencies) that checks the paper's identities against direct computation and reproduces every number quoted in the text |
| `cm_verify_output.txt` | Saved output of the full run reported in the paper's Table 2 |

## Running

```
python3 cm_verify.py            # full run (the paper's Table 2)
python3 cm_verify.py --quick    # smaller samples, smoke test
```

The saved run used CPython 3.13.16 on Linux x86_64. Seeds are fixed: 20261022 for the checks inherited from the first rewrite, and 2026102202 for the checks added in the corrected version (marked † in Table 2 and `[new]` in the output). All arithmetic is exact modulo p, so the counts are reproducible; only the timing lines vary between machines.

## What is checked

- Theorem A (curve-order identity) at every affine rational point of random short curves, including chains in which an addition step meets T = P (Algorithm 2.2 then uses the tangent slope), plus an independent check of its normalization: the Miller function f_{N,P} is constructed from a basis of L(N(O)) without the Miller recurrence and expanded in t = −x/y, including on trace-one curves.
- Lemma 2.1, Theorem B (Theorem 4.1, including the pole a = 0), Corollary 4.2 and Theorem D (including 69 exceptional cases).
- Theorem 4.4 under the fast-algorithm hypothesis, and separately as an unrestricted identity with active branch poles.
- The trace-free identity (4.9), the coefficient ranges (6.1)–(6.3), Corollary E and (6.4) at all 221 eligible primes below 3000 plus p = 1,000,211, and the quarter-point formula (6.5) at all 210 eligible primes 13 ≤ p < 3000 plus p = 1,000,033.
- Table 1, Example 6.1 (p = 23), the p = 13 and p = 97 quarter-point examples and the p = 5 example.
- Section 6.3 (rows marked ‡, deterministic): the order of R over ℚ for 22 pairs (k, z), α₃(R) for z = 1 and −2, and Theorem 6.3 and Example 6.4 by direct summation at all primes 5 ≤ p < 3000.

These are finite checks, not proofs. Earlier and larger campaigns, with disjoint confirmation samples, are documented in the computational companion and the older dated folders, and are not counted here.

## Licence

MIT, as for the rest of the author's material in this repository (see [`../LICENSE`](../LICENSE)).
