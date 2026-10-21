# Corrections and gates

The detailed prior review is in inherited/Independent_Review_20261020.md. Resolve the following before finalizing an application section or freezing benchmark claims.

## Complete common domain

The indexed points must enumerate U, or the correction sum must range over every omitted u in U. Zero coefficients may represent additional exclusions. With p=7, f=1+x+x^3, R=1/(x-1), the single-pole value is 0; excluding both 1 and 2 gives 6. The theorem as written with merely mu_j belonging to U misses that distinction. The implementation’s explicit extra-exclusion support is not itself wrong.

## Projective scope

For quartics with nonsquare leading coefficient there are no rational points at infinity. A nonconstant polynomial weight can then be defined on every point of E(F_p), even though it has geometric poles at nonrational infinity points. Either keep the stricter API requiring regularity at every geometric infinity point and say so, or extend the supported rational-point sum. Do not assert it is mathematically undefined in the nonsquare case. The squarefree example p=7, f=1+3x^4 has N_infinity=0.

## Reduction resonances

For Delta(S)=f S'+f'S/2, leading coefficients include -(k-1)f(mu), (1/2-k)f'(mu), and ell(j+D/2). State precisely when they are nonzero modulo p. General higher-order-pole claims require more than the implemented double-pole tests. In particular, branch reduction resonates at k=(p+1)/2 and cubic polynomial reduction at j=(p-3)/2.

## Claims of necessity and novelty

The branch reductions establish sufficient coefficient data, not a lower bound or an impossibility theorem for every alternative Miller-based method. The rounded-third factorial reduction is a specific equivalence. “No polylogarithmic acquisition was established in this investigation” is justified; a universal literature assertion requires the new audit.

## Other scope and cost points

State regularity on every included fibre when using cancellation of yB(x). The single-point-exclusion formula with (y+y0)/(x-mu) is affine unless infinity is handled separately. Its cubic model has a pole at infinity.

Large s does not alone prove that U union roots(f)=F_p. It can justify an O(s) full-field search. Distinguish cached storage from temporary query storage.

The optional endpoint-check method currently reruns the chain. Checking an endpoint exposed by the original chain could be inexpensive, but that optimization is not implemented. Passing the necessary endpoint condition does not certify the trace.

The program supports p<2^64 with a deterministic primality guard. An asymptotic bit-complexity statement for unbounded p needs its own input-primality convention and arithmetic model. Do not infer unbounded scaling from the finite implementation domain.

## Prior rerun evidence

The independent review matched all 48 archive-manifest entries and all 32 frozen files. The supplied verifier passed. The extended suite returned 3,288 inherited queries and 8,141 candidate checks without mismatches. The exploratory suites reproduced 97 branch, 6,281 double-pole, 126 polynomial-part and 1,550 single-point-exclusion checks, together with 1,416 supplied-second-kind-path checks. The derivative experiment had 242 matching values but only 3 matching formal derivatives, with 260 degeneracies.

Those implementation reruns substituted direct small-prime point counting for unavailable PARI in memory. The complete archived 208,272-check development and 261,423-check confirmation suites were not independently rerun. Neither their large-prime PARI adapter nor the manuscript’s entire proof was independently certified by the review.

Keep this provenance distinction in the new report. The derivative experiment is evidence against that particular pointwise differentiation procedure, not a universal lower bound.
