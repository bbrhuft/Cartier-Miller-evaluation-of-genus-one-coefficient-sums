# Primary-source guide and verification status

This guide records source locations actually consulted in the originating conversation. It is not a replacement for reading the theorem and checking its hypotheses. The full Katz and Bruinier–Ono–Sutherland PDFs are not bundled; the original AI had public-source access. If the new AI lacks it, say so and keep direct verification pending.

| Source | Location and relevance | Access status |
|---|---|---|
| Katz, N. M. (1976). p-adic interpolation of real analytic Eisenstein series. Annals of Mathematics, 104(3), 459–571. | Sections 1.3 and 5.7; Comparison Theorem 8.0.9 and Lemma 8.0.13. https://web.math.princeton.edu/~nmk/old/padicinterp.pdf ; official bibliographic page https://annals.math.princeton.edu/1976/104-3/p06 . | Author-hosted paper opened and these passages read. The scanned formulas require careful visual normalization checks. |
| Bruinier, J. H., Ono, K., & Sutherland, A. V. Class polynomials for nonholomorphic modular functions. arXiv:1301.5672v3, 28 January 2015. | Definition (1.2), Lemma 2.3, Theorem 1.1 and Section 3.1. https://arxiv.org/abs/1301.5672 and https://arxiv.org/pdf/1301.5672 . | Paper opened and relevant passages read. Use the manuscript version explicitly unless final journal metadata are verified. |
| Masser, D. W. (1975). Elliptic functions and transcendence. Lecture Notes in Mathematics, 437. Springer. | Appendix 1, Lemma A2 and p.118 are the pointers given by the preceding paper, including the special-discriminant issue. https://link.springer.com/book/10.1007/BFb0069432 . | Book metadata verified; relevant full appendix not directly obtained. Do not claim otherwise. |
| Ireland, K., & Rosen, M. (1990). A classical introduction to modern number theory (2nd ed.). Springer. | Chapter 18, Section 3, Theorem 4, p.305, and Section 4, Theorem 5, p.307. | User-supplied chapter bundled. Both trace conventions checked; Theorem 5 visually inspected. These concern the existing j=0/1728 seeds, not the proposed new -7/-8 trace route. |
| Lemmermeyer, F. Rational quartic reciprocity II. arXiv:1310.6597. | Section 4, p.2, Gauss's criterion for the quartic character of 2. https://arxiv.org/abs/1310.6597 . | Paper directly read; used to prove the B=0 depth-three eligibility equivalence. |
| Sutherland, A. V. (2023). 18.783 Elliptic Curves, Lecture 22: Isogeny volcanoes. MIT. | Theorem 22.11 and Remark 22.12, p.7. https://math.mit.edu/classes/18.783/2023/LectureNotes22.pdf . | Directly read. The remark is needed when the component contains the exceptional seed j=0 or 1728. |
| Cox, D. A. Primes of the form x^2+ny^2. | A classical pointer in inherited materials. | Not newly inspected in this pass. Do not cite a guessed theorem statement. |

Katz's comparison assumes a characteristic-zero CM curve with the relevant arithmetic data defined over its number field, good reduction at the selected place, and ordinary reduction. It compares a normalized algebraic direction, not an unscaled numerical E_2^* value. The finite-field coefficient conventions in PROMPT.md still need their own explicit reduction bridge.

Bruinier–Ono–Sutherland use

$$\gamma(\tau)=\frac{s_2(\tau)}{6j(\tau)}-
\frac{7j(\tau)-6912}{6j(\tau)(j(\tau)-1728)}.$$

Their non-special Masser formula obtains gamma from local coefficients of a classical modular polynomial. It assumes D<-4 and D is not -3d^2. The -12 normalization control is therefore exceptional for that formula. The paper points to Masser for the modification; do not extrapolate the simple denominator statement to that case. Cases j=0 or 1728 also need separate treatment. Distinguish the polynomial coefficients used in that paper from this project's coefficient beta.

Exact CM-value computation and its algorithmic cost are separate questions. The paper's complexity guarantees include GRH assumptions. A fixed-D exact precomputation may be reusable across primes, but the computation, storage, denominator exclusions and pairing with j must be made concrete and charged under the declared contract.
