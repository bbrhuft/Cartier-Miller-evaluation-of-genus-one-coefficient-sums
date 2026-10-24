# Small rational lifts of reciprocal character sums (24 October 2026)

This folder holds a standalone note:

| File | Contents |
|---|---|
| [`Cartier_Miller_Small_Lift_Note_20261024.pdf`](Cartier_Miller_Small_Lift_Note_20261024.pdf) | *Small rational lifts of reciprocal character sums at 256-bit primes: an empirical torsion dichotomy* (draft, 11 pages) |
| `Cartier_Miller_Small_Lift_Note.tex` | LaTeX source (pdfLaTeX; same packages as the main paper) |

## What the note does

It builds on Theorem A, Theorem B and Proposition 6.2 of the [main paper](../Cartier_Miller_Paper_Rewrite_Corrected_20261024.pdf).

- **Known direction (Proposition 2.2).** If the twist point R_a is torsion over ℚ, the reciprocal character sum satisfies C_f(a) ≡ Aε + Bτ (mod p) for fixed rationals A, B. The residue is then the reduction of a rational number u/d with |u|d = O(√p).
- **Basis-free size test (Section 3).** The minimal lift size of a residue is read off its continued fraction (Lemma 3.2). For uniform residues, Lemma 3.3 gives a rigorous counting bound. At 256-bit primes, one evaluation gives strong discrimination against a uniform-residue model.
- **Pre-registered survey (Sections 4–5).** The survey covered 2,668 pairs (f, a) over 184 small cubics and quartics, most without complex multiplication, each evaluated at three random 256-bit primes. Small lifts occurred at exactly the 80 pairs with R_a torsion (orders 2, 3, 5, 6), whose recovered relations equalled the predicted (A, B), and at none of the other 2,588. The survey was run on the author's laptop.
- **Balanced uniform converse (Theorem 2.5).** If a relation with A + B = g₁/2 holds at all but finitely many admissible primes, then R_a is torsion. The proof uses a Cartier-operator form of Theorem A (Lemma 2.4) and Bost's theorem on the Grothendieck–Katz conjecture for solvable groups (Bost, 2001, Theorem 2.9).
- **Relation to Katz (2014).** The Miller coefficient is, up to a factor −½, the invariant ω_p(P#) of Katz's *Equidistribution questions for universal extensions*. Lemma 2.4 coincides with Katz's Cartier identity. The density-zero converse (Conjecture 2.8) would follow from Katz's equidistribution conjecture.

## Status

This note is unrefereed and was prepared with extensive generative-AI assistance. Theorem 2.5 is assembled from published theorems. It awaits review by a specialist and may already be known in substance, as the rank-one case of the Grothendieck–Katz conjecture applied to the universal vectorial extension. The general unbalanced converse and the density-zero converse are not established. The survey's code and complete run records are available from the author.

## Licence

MIT, as for the rest of the author's material in this repository (see [`../LICENSE`](../LICENSE)).
