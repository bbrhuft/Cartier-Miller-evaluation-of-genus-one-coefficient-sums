# Bounded survey audit informing version 0.1

The supplied Deep Research report is useful for identifying components, but it is not treated as executable pseudocode or a complete independent theorem audit. This note records corrections relevant to this package. It does not audit every bibliographic or complexity claim in the survey.

Wilson reflection requires the exponent n+1, not n. Version 0.1 implements and exhaustively checks the corrected sign on small primes.

The BGS shift theorem requires the shift-dependent quantities alpha−d*beta through alpha+d*beta to be units, as well as the other stated units. The inequality 2d+1 < p is insufficient for arbitrary alpha and beta: alpha = beta = 1, d = 2, p = 11 already includes a zero shifted difference. The original backend uses monic remainder trees, so it does not require this interpolation hypothesis. Version 0.5 adds an audited scalar BGS path with explicit reuse of known samples at overlapping nodes; all remaining kernel denominators are tested before inversion. The survey's displayed convolution indexing was corrected using the author manuscript's Theorem 5 proof; BGS_BACKEND.md gives the implemented indexing.

The rounded third is not the only affine family collapsing to a single factorial by Wilson reflection. For p ≡ 1 (mod 3), L = (p−1)/3 yields a_L = −(L!)^(−3), as proved in MATHEMATICS.md. Neither formula is presented here as a new discovery.

The proposed harmonic-sum open problem is already covered by a classical congruence. For p ≥ 5, H_floor(p/3) = −(3/2)q_p(3) modulo p. In the rounded-third case floor(p/3) = (p−2)/3. Liu (2017, Lemma 2.2), citing Lehmer, states the needed congruence. This removes the suggested harmonic-elimination novelty claim; it does not make a boundary-only lift into a complete fast prime-square Cartier–Miller algorithm.

Liu, J.-C. (2017). Congruences for truncated hypergeometric series 2F1. Bulletin of the Australian Mathematical Society, 96, 14–23. https://doi.org/10.1017/S0004972717000181 . This is a primary research paper recording the classical lemma.

The full Tal classical report is accessible from the ECCC download link. Proposition 4.3 and Appendix H describe the uniform deterministic logarithmic improvement modulo p and p². Theorem 1.1 separately states a deterministic classical q | (p−1) bound of soft-O(q^c + sqrt(p/q)); the p+1 construction includes an odd-(p+1)/q condition. These statements warrant individual source-based audits rather than the survey table's uniform treatment. This package implements none of those algorithms and claims no empirical speedup from them.

All zero shortcuts and Wilson reductions in version 0.1 are tagged by their mod-p scope. Prime-power requests are explicitly rejected. A generic coefficient recurrence with an index crossing p can encounter nonunit denominators; the survey's discussion is not a license to divide through them in F_p. Generic higher-order recurrence and selected-coefficient support are therefore not included here.

Performance crossovers and constant-factor improvements must be measured. The direct cutoff is configurable. Timings in the package concern boundary evaluation and the documented complete third/fifth outputs in the provided Python implementation. They do not compare the published fast prefix algorithm with FLINT, Harvey's implementations, Tal's methods or the earlier CUDA implementation. A later batch backend should reuse and audit existing project code instead of relabeling existing remainder-forest work as new.


## Version 0.5 implementation update

The previous product-tree backend remains available. The new `bgs` backend now implements the scalar arithmetic-progression value-shift/doubling construction from Bostan–Gaudry–Schost, Sections 3–4, with explicit field-only known-node collision handling. `BGS_BACKEND.md` audits the full kernel denominators and convolution indexing. Earlier statements that BGS was not implemented describe the earlier release. Tal refinements remain unimplemented.
