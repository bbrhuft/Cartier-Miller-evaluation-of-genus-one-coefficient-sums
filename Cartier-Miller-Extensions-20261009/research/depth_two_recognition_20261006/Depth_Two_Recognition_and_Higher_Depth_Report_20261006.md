# Direct recognition of two-step Cartier-data families and higher-depth coverage

6 October 2026. Separate unrefereed extension research. The manuscript is unchanged; GitHub URL and commit remain unknown and GitHub has not been inspected. The results below distinguish algebraic derivations from implemented prototypes and finite graph evidence. No novelty or wall-time benchmark is claimed.

## Outcome

There is now a deterministic, constant-field-operation recognizer for the entire rational degree-two closure through depth two of the two retained ordinary easy seed families. It supplies explicit model parameters and a checked path certificate, including every quadratic twist. No square-root computation or graph search is needed for this recognition. Small-characteristic degenerations and class collisions are addressed by exact integer norms and resultants, rather than extrapolating from test agreement.

The complementary graph audit establishes genuine additional classes at depths three and four for specified small primes, after quotienting by true base-field isomorphism and removing dual backtracking. It also preserves a complete component obstruction: sharing an easy curve's exact trace does not imply reachability by rational degree-two isogenies.

| Claim | Evidence category | Status |
|---|---|---|
| Complete easy-seed closure classification through depth two | Explicit rational-root case split and dual-scaling derivation | Unrefereed algebraic proof |
| Square-root-free recognition including quadratic twists | Parameter extraction plus exact exceptional-prime factorizations | Implemented and independently checked |
| Depth-three and depth-four class additions | Exhaustive finite isomorphism graphs at 51 primes through251 | Verified finite findings, not a uniform depth theorem |
| Trace-only membership shortcut | Explicit closed two-class component counterexample | False; retained obstruction |
| Generic fast K or supersingular amplitude recovery | No new algorithm | Unresolved |

The agents worked complementary theory and graph-audit branches. The parent independently derived the extraction constants, implemented a separate recognizer, checked it against a separately enumerated seed closure, and verified original-coordinate branch outputs.

## Definitions, differential scale and transport

For p>=7 prime, nonsingular E:y²=x³+Ax+B and h=(p-1)/2, define H=[x^(p-1)]F^h and beta=[x^(p-2)]F^h. The exact trace is tau=p+1-#E(F_p), and H=tau modp. The easy seeds are A=0,p=1mod3 and B=0,p=1mod4. Exponent support gives beta=0 and a nonzero surviving binomial coefficient gives H nonzero in these seed classes.

At a rational root q, the normalized quotient has

$$A'=-4A-15q^2,\qquad B'=-8Aq-22q^3,$$

and global differential identities

$$\phi^*(dx'/y')=dx/y,\qquad
\phi^*(x' dx'/y')=(2x-q)dx/y-2d\left(\frac{y}{x-q}\right).$$

Thus the differential scale is +1, the exact correction has the stated negative sign, and Cartier yields H'=H,beta'=2beta-qH. Both poles of the primitive are tracked. With local infinity parameter t=-x/y, eta has principal part +2t^-2dt and zero residue. At the kernel, z=y gives y/(x-q)=F'(q)/z+O(z), so -2d of the primitive contributes +2F'(q)z^-2dz and zero residue. The complete identities and independent sign checks appear in the theory note. Changing the basis to dx/(2y) halves the exact correction and preserves the scalar transport formulas.

For the original f=1+cw+bw²+aw³, a nonzero, the fixed normalization remains

$$x=aw+b/3,\quad y=av,\quad A=ac-b^2/3,\quad B=a^2-abc/3+2b^3/27,$$

$$dw/v=dx/y,\quad \beta=aK+(b/3)H,\quad
T_f(\mu)=\frac{a\mu}{f'(\mu)}(\mu H-K).$$

The supplied nonzero rational root mu is in the original w coordinate. No scale from the separate rational-origin manuscript construction is imported.

## Complete depth-at-most-two classification

Besides the full seed classes, the one-step families are (-11r²,-14r³),p=1mod4 and (-15r²,-22r³),p=1mod3, with beta=-rH and r nonzero. Their r parameters are recovered by r=11B/(14A) and r=15B/(22A), followed by checking both equations.

The genuinely nondual depth-two families are:

| Family | Prime condition | Parameter condition | A | B | beta/H multiplier |
|---|---|---|---|---|---|
| From j=1728 | p=1mod8 | e²=2, r nonzero | (-91-60e)r² | (-462-308e)r³ | -(3+2e)r |
| From j=0 | p=1mod12 | e²=3, r nonzero | (-135-60e)r² | (-694-420e)r³ | -(3+2e)r |

For j=1728 a zero kernel stays in the easy family; any nonzero root writes the seed as (-r²,0). For j=0 a rational root writes the seed as (0,-r³). The first targets factor as (x+2r)(x²-2rx-7r²) or (x+2r)(x²-2rx-11r²). Every second root is the dual -2r, returning to a square-scaled seed, or (1+2e)r with e²=2 or3. The usual quadratic-character congruences combine with seed ordinarity to give precisely the displayed prime conditions. This exhausts the rational two-step cases; it does not classify all degree-four isogenies or all curves.

A displayed quadratic twist d transforms (A,B) to (d²A,d³B) and beta/H to d times its previous value. In these parameter families it is absorbed exactly by r -> dr. No Legendre symbol or square root of d is required when reconstructing beta from the final model's trace. Special quartic/sextic seed twists are covered by the full A=0/B=0 seed classes; they are not confused with generic quadratic twisting.

## Direct parameter extraction and certificate

Write alpha(e)^3=a0+a1e and gamma(e)^2=g0+g1e after reducing e²=n. The integer constants are:

| n | (a0,a1) | (g0,g1) |
|---|---|---|
| 2 | (-2719171,-1922580) | (403172,284592) |
| 3 | (-6834375,-3928500) | (1010836,582960) |

From the actual coefficients compute

$$U=a_0B^2-g_0A^3,\qquad V=a_1B^2-g_1A^3,$$

$$\boxed{e=-U/V,\qquad r=\frac{\alpha(e)B}{\gamma(e)A}.}$$

The recognizer verifies the prime congruence, nonsingularity, nonzero denominators, e²=n, r nonzero and both A=alpha(e)r²,B=gamma(e)r³. Once these checks pass, beta=-(3+2e)rH is an algebraic corollary of the explicit path. Computing e is not numerical differentiation or choosing a square root by inspection: the two model coefficients determine the conjugate choice rationally.

Each accepted two-step certificate also verifies the reverse rooted path with roots -2(1+2e)r and -8r. It ends at a square-scaled easy seed and reproduces the same beta multiplier. This second coordinate check catches orientation or scaling errors. Supplied stored parameters can be independently reverified; tampered e values are rejected.

## Exceptional reductions and collisions

The norms N(alpha),N(gamma) and the extraction determinant a1g0-g1a0 are:

| n | N(alpha) | N(gamma) | Extraction determinant |
|---|---|---|---|
| 2 | 23*47 | 2²7²11² | -2⁶*3*7²*11²*19*59 |
| 3 | 3³5²11 | -2²11*23*47 | 2⁶3⁴5³*17*29*41 |

For an actual family model V=(a1g0-g1a0)r⁶. None of these possible vanishing primes satisfy the relevant ordinary prime congruence. Norms of 4alpha³+27gamma² are -2¹³ and2¹²3⁶, so nonsingularity holds throughout the permitted p>=7 domain. Accordingly accepted ordinary models have A,B,V nonzero and unique e,r. This is a global factorization argument, not a finite-test conjecture.

Degenerations outside that domain are preserved. At p7 the n2 conjugates have B=0; at p23,e5 the n2 model has A=0; at p11 the n3 choices e6 ande5 give A=0 andB=0 respectively. Their seed ordinarity conditions fail. The recognizer rejects those family claims instead of applying beta-zero trace recovery to supersingular inputs. The exceptional CSV records root existence and admissibility separately.

The two conjugate j-polynomials are

$$P_2(J)=J^2-82226316240J-7367066619912,$$
$$P_3(J)=J^2-2835810000J+6549518250000.$$

The theory note factors their evaluations at the seed/one-step j values 0,1728,287496,54000 and their mixed resultant. Every candidate collision prime fails its corresponding ordinary congruence; when both families are eligible, p=1mod24, and no mixed-resultant prime satisfies that condition. Thus permitted depth-two classes remain distinct from each other and every smaller-depth class. Full integer values, factorizations and scripts are retained. A j-only hit would still lack the coordinate-dependent r needed to reconstruct beta; it is never substituted for a parameter certificate.

These polynomials match classical CM tables for discriminants -64 and -48. That literature overlap is explicitly acknowledged; neither the curves nor their j-polynomials are presented as new discoveries.

## Higher-depth paths after dual scaling

The graph audit uses actual F_p isomorphism orbits (A,B)->(d²A,d³B) with d a nonzero square. Nonsquare twists remain separate. Every certificate keeps its unscaled models and +1 quotient scales; canonical orbit keys are only for graph identity. Square scaling changes beta by d and is checked explicitly.

A dual step at -2q returns (16A,64B,4beta), not the original displayed coefficients. Deleting an adjacent dual pair and rescaling remaining roots by1/4 preserves endpoint class and seed reachability. Pruned and unpruned finite searches agree on every minimum class depth in the tested interval. Nondual root choices can also coincide as isomorphism classes, so root or edge counts are not used as class counts.

Across all51 primes7..251, exhaustive graphs give:

| Minimum seed distance | Additional F_p isomorphism classes, summed across primes | Additional j-values, summed across primes |
|---|---:|---:|
| 3 | 64 | 32 |
| 4 | 32 | 16 |

A genuine depth-three example at p73 is (0,7) ->(39,8) ->(50,22) ->(4,16), with forward roots42,54,1. Its endpoint H10,beta4,j20 is absent every smaller-depth seeded closure. The reverse roots71,6,43 give multiplier15. The original normalized cubic f=1+4w+37w³ has H10,K55, and the supplied root mu9 gives T3 by both the retained formula and independent dense summation.

At p193 the depth-four endpoint (131,85), reached from(0,11) with kernels47,12,118,56, has H191,beta81,j61 absent every seeded depth throughthree. Reverse kernels81,21,2,160 give multiplier56 and an easy endpoint(0,74). These are concrete higher-depth certificates, not claims that arbitrary curves have short paths.

Full finite graph exhaustion finds no additional classes beyond depthfour at these primes. This is restricted to the tested interval; no uniform depthfour bound is claimed.

## A retained component obstruction

Modulo13, y²=x³+x+1 has trace -4,H9,beta8 and rational root7. The easy curve y²=x³+7x has the same trace. Nevertheless its complete rational degree-two component is

$$ (1,1)\xrightarrow{7}(2,3)\xrightarrow{12}(3,12)\simeq_{\mathbb F_{13}}(1,1), $$

with no easy seed. The cubics have only those rational roots: their remaining quadratic discriminants are nonresidues. The final model is the d4 square scaling, so every further step repeats this two-class component. This provides a direct finite-field proof of nonreachability for this input, stronger than a bounded miss. It excludes the proposed trace-match shortcut, not odd-degree isogenies or every other K algorithm.

In the complete small-prime census780 ordinary classes share some easy seed trace but remain outside all seeded rational degree-two components;496 also have rational two-torsion. These counts are finite findings across different fields, not generic proportions.

## Preparation, query and search costs

| Route | Charged preparation | Supplied branch query |
|---|---|---|
| Direct depth<=2 recognizer | Exact trace preparation plus O(1) field work for recognition, normalization and K | O(1) |
| Deterministic theoretical setup | T_Schoof(E,p)+O(1) field work; bit arithmetic costs separately understood | O(1) |
| Supplied higher-depth path length m | Exact trace preparation plus O(m) verification/reconstruction | O(1) |
| Existing automatic higher-depth finder | Expected O(3^d logp) field work for unpruned discovery, plus trace and reconstruction | O(1) after success |
| Dual-pruned search tree, theoretical here | At most1+3(2^d-1)vertices; expected O(2^d logp) fixed-degree factoring work | Not a new implemented timing result |
| Exhaustive class audit | O(p) root scans and explicit isomorphism orbits; correctness only | Not a performance comparator |

The recognizer is standard-library Python with a fixed64-bit prime guard; the algebraic theorem applies to all permitted primes. Supplied traces remain explicitly trusted, with a Hasse interval check only necessary, not certification. No point-count backend or production SEA is added. Schoof is the unconditional theoretical setup; practical SEA or PARI alternatives would require separate integration and identical-output/modulus benchmarking. No benchmark, cached-query speed ratio or complete-run timing is claimed.

## Independent checks and reproducibility

| Check | Evidence retained |
|---|---|
| Parent direct recognition | All137,086 nonsingular short cubics at primes7..127 versus independent complete depth-two enumeration:4,960 positives,132,126 negatives |
| Parent coefficient/twist certificates | 4,960 integer multinomial coefficient pairs and9,920 twist certificates |
| Parent original-coordinate outputs | 66 normalized cubics,154 rational branch queries, direct traces and dense sums |
| Independent theory branch | 5,208 parameter cases,1,176 coefficient pairs,69,192 family-specific membership decisions,56 exceptional rows |
| Exact integer audit | Norms, determinants, discriminants, lower-depth collision factors and mixed resultant reproduced by standalone script |
| Higher-depth audit | All12,288 F_p classes through251;12,974 coefficient models,514 retained directed edges; pruned/unpruned and saturated finite coverage checked |

All checks pass. Counts overlap and must not be added as disjoint coverage. Finite agreement supports implementations; the stated algebraic derivations are the arguments requiring human review. Raw CSVs, validation JSON, seeds, environment information, CLI examples and source hashes are preserved. No elapsed validation time is a benchmark.

The retained handover and earlier extension code were checked before implementation. Historical quadratic-algebra sqrt2 handling belongs to the existing admissible evaluator and was not mistaken for a completed depth-two recognizer. Ordinary third-point evaluation, higher-genus prefix prototypes and sum-first precision-two recurrence products remain separate existing work. This investigation supplies no arbitrary stopping-index theorem, complete original weighted sum without its boundary, or fast sum-avoiding Witt correction.

The next bounded question is to derive similarly normalized parameter certificates for one depth-three family, using its classical CM polynomial only as a membership aid and preserving the coordinate factor needed for beta. The small-prime census provides exact target examples and retained unreachable components for testing. General supersingular recovery remains a separate harder branch.

## Primary sources and classical overlap

| Reference | Verified primary text and role |
|---|---|
| Sutherland,A.V.(2013). Introduction to arithmetic geometry,Lecture25,section25.3.MIT. | https://ocw.mit.edu/courses/18-782-introduction-to-arithmetic-geometry-fall-2013/e011c006f6aeb95083197457da90598d_MIT18_782F13_lec25.pdf ; explicit rational-kernel quotient |
| Katz,N.M.On a question of Zannier.Published author text. | https://web.math.princeton.edu/~nmk/zannier_publ.pdf ; Cartier coefficient identification |
| Sutherland,A.V.(2013).Isogeny volcanoes.ANTS X proceedings,507–530.https://doi.org/10.2140/obs.2013.1.507 | https://arxiv.org/pdf/1208.5370 ; classical isogeny-component background, not a replacement for our normalized coefficient proof |
| vonzurGathen,J.,&Panario,D.(2001).Factoring polynomials over finite fields:A survey.Journal of Symbolic Computation,31,3–17. | https://people.csail.mit.edu/dmoshkov/courses/codes/poly-factorization.pdf ; randomized fixed-degree root method |
| Lario,J.-C.(n.d.).Elliptic curves with CM defined over extensions of type(2,...,2).Author-curated computational table. | https://web.mat.upc.edu/joan.carles.lario/ellipticm.htm ; lists the same -48/-64 polynomials; a research data page, not itself a peer-reviewed proof |

These sources were opened and inspected. Our normalized recognition and collision derivations are supplied explicitly; broad priority review remains necessary before any novelty claim.
