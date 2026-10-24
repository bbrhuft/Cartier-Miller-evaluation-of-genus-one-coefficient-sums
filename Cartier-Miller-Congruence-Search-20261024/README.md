# Pre-registered congruence search (24 October 2026)

This folder holds the code and run records behind Remark 6.5 of [`Cartier_Miller_Paper_Rewrite_Corrected_20261022.pdf`](../Cartier_Miller_Paper_Rewrite_Corrected_20261022.pdf) (draft dated 24 October 2026). It documents how Theorem 6.3 was **found**. The theorem is **established by the proof** in Section 6.3, not by this search.

## What the search asked

For k ∈ {3, 4}, ten values of z (1/8, −1/8, 1/16, −1/16, 1/32, 1/2, −1/2, 1, −1, 2) and every residue class of p modulo 24, it asked whether

S_k(z) = Σ_{i=0}^{⌊(p−1)/k⌋} C(2i, i) z^i  (mod p)

is a fixed combination, with small rational coefficients (height ≤ 10⁴), of cheap quantities:
- Fermat quotients;
- CM data (u from p = u² + s², r from 4p = r² + 27s²);
- power-residue symbols.

Round 2 classes were further split by the Legendre symbols of 5 or 7 where relevant, giving 224 runs in total. S_k(z) was computed with the paper's evaluator (Corollary 4.2). Relations were searched by lattice reduction at 40 primes of 48 bits. Candidates were frozen by SHA-256 and then tested at 1,110 fresh primes of 64, 128 and 256 bits. All parameters are fixed in [`cm_explore/prereg.json`](cm_explore/prereg.json).

## Outcome

| Round | Runs | Candidates | Confirmed |
|---|---|---|---|
| 1 (z = 1/8, the paper's sums) | 16 | 0 | — |
| 2 (the other nine values of z) | 208 | 8 | 8 |

All eight confirmed candidates are k = 3, z = 1, one per residue class:
- S₃(1) ≡ −1/3 when p ≡ 2 (mod 3);
- S₃(1) ≡ (1 − 2r)/3 when p ≡ 1 (mod 3).

Each held at all 1,110 confirmation primes. The genuine relations stood out by gap factors of 10²¹–10⁴³; every other run had a gap of about 10⁰. Stage 0 passed:
- 6,133 direct comparisons and 2,053 brute-force trace checks;
- 112 of 112 planted relations recovered;
- no false candidates from random targets;
- 96 primes checked at confirmation sizes.

The z = −2 case of Example 6.4 was **not** part of the search. It was derived from Proposition 6.2 afterwards and then checked separately.

## Files

| Path | Contents |
|---|---|
| `cm_explore/` | The package exactly as run: code fingerprint (SHA-256 of the code plus pre-registration) `985252540ac4cd2295418e7f9bfb03820e21c1aed972a57e5954705577ded5a8` |
| `cm_explore/prereg.json` | Pre-registration: targets, bases, seeds, thresholds and stopping rule |
| `results/log.txt` | Full log of the run (Windows 11, CPython 3.12.10, python-flint 0.9.0); its first line records the fingerprint above |
| `results/SUMMARY.md` | One-page summary written by the run |
| `results/confirmation.json` | The eight candidates, their relation vectors and bases, and their confirmation status |

The run also wrote `stage0.json`, `round1_runs.json`, `round2_runs.json`, `candidates.json` and `freeze.json`. These are not included here, and rerunning reproduces them.

## Reproducing

Use Python 3.10 or later, ideally with `python-flint` (`pip install python-flint`). From this folder, run:

```
python -m cm_explore.selftest
python -m cm_explore all
```

The whole run took 136 s on the original laptop. The fingerprint printed in the first log line should match the one above. All arithmetic is exact and the seeds are fixed, so the counts and candidates are reproducible.

## Disclosures

- **Testing before the real run.** The package was tested before the run with separate smoke-test seeds. That test showed "no relation" for 8 of the 224 runs (z = 1/8 and −1/8, k = 3, classes 1, 5, 7, 11). The hypotheses do not depend on the seed, so those outcomes were effectively seen in advance. Nothing was changed after seeing them.
- **Changes before the real run.** During testing, a floating-point square-root bug in computing r (affecting 128- and 256-bit primes) was found and fixed. A confirmation-size check was then added to Stage 0. Both changes were made before the real seeds were used, and are part of the fingerprinted code.
- **Status.** This is unrefereed, AI-assisted work. Finite agreement is evidence, not proof.

## Licence

MIT, as for the rest of the author's material in this repository (see [`../LICENSE`](../LICENSE)).
