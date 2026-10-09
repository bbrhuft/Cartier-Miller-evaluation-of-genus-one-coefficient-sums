# Explicit rational 2-isogeny closure of known Cartier-data families

6 October 2026. Complementary theory branch; unrefereed mathematical note. Current scope is a supplied rational rooted chain, fixed-degree model changes, and one additional nondual depth-two family. No manuscript revision, generic chain-search algorithm, performance benchmark, or novelty claim is made. The retained structural note and parent K-recovery report were read before extending them.

## Normalized short rooted transport

Let p>=7 be prime and E:y²=x³+Ax+B be nonsingular over F_p. Let r be a supplied rational root, so r³+Ar+B=0. Put z=x-r, t=3r, u=A+3r². Then

$$y^2=z(z^2+t z+u),\qquad u(t^2-4u)\ne0.$$

The inequality follows from squarefreeness; alternatively 4A³+27B²=(A+3r²)²(4A+3r²). The classical rational kernel quotient is

$$X=z+t+u/z,\qquad Y=y(1-u/z^2).$$

Its short coordinate x'=X-2r can be written directly as

$$x'=x+\frac{A+3r^2}{x-r},\qquad y'=y\left(1-\frac{A+3r^2}{(x-r)^2}\right).$$

Direct substitution gives the target

$$\boxed{A'=-4A-15r^2,\qquad B'=-8Ar-22r^3.}$$

Use omega=dx/y, eta=x omega and their target counterparts. The holomorphic differential pullback scale is +1. The exact global second-kind identity is

$$\boxed{\phi^*\omega'=\omega,\qquad
\phi^*\eta'=(2x-r)\omega-2d\left(\frac{y}{x-r}\right).}$$

Indeed d(y/z)=1/2(z-u/z)omega. The primitive has poles at infinity and (r,0); the formula accounts for both preimages of the target infinity pole. No local-principal-part substitution or unrecorded holomorphic adjustment is used. With omega=dx/(2y), the exact term is -d(y/(x-r)); the first-kind scale stays +1.

Let H=[x^(p-1)](x³+Ax+B)^h and beta=[x^(p-2)](x³+Ax+B)^h, h=(p-1)/2. Cartier kills the exact term. Naturality in this separable extension follows from the unique p-basis decomposition in a separating target coordinate: sum q_i^p (x')^i dx' pulls back to the same decomposition and Cartier selects i=p-1. Hence

$$\boxed{H'=H,\qquad\beta'=2\beta-rH.}$$

This identity holds in ordinary and supersingular cases. The root, curve equation, nonsingularity and target model can all be verified with fixed-degree arithmetic. The quotient map is separable because p is odd; its x derivative is not identically zero. The map's denominator zeros are kernel points, not invalid mathematics; implementations of the coefficient transport need not evaluate the point map there.

## Scaling and quadratic twists

For d in F_p× define the displayed twist model

$$E^{(d)}:y_d^2=x_d^3+d^2A x_d+d^3B.$$

The coefficient identity F_d(x)=d³F(x/d) gives, without choosing a square root,

$$\boxed{H_d=\chi(d)H,\qquad\beta_d=d\chi(d)\beta,\qquad\chi(d)=d^h\in\{1,-1\}.}$$

The relevant exponents are 3h-(p-1)=h and 3h-(p-2)=h+1. This polynomial proof avoids treating inverse Frobenius on an extension-field square root as if it were base-field linearity. Exact traces satisfy tau_d=chi(d)tau, as follows directly from the Legendre-symbol point-count sum.

When d=s², x_d=s²x,y_d=s³y is a base-field isomorphism. Its omega pullback scale is 1/s, not +1; beta_d=s²beta and H_d=H. A minus choice y_d=-s³y changes the differential scale sign but does not change the coefficient pair. When d is nonsquare, the analogous point map requires sqrt(d) and lies over the quadratic extension; the coefficient formula above still computes the correct base-field twist pair.

Twists commute with rooted quotients: the transported root is dr, and the target coefficients are d²A',d³B'. Both routes give beta'=d chi(d)(2beta-rH). Thus quadratic twisting expands the recognized family without a nonresidue or square-root search, provided d is supplied and its Legendre symbol is charged. If an exact trace of the final model is already supplied, an ordinary closure calculation can recover beta using the slope q below without computing a twist trace separately.

## Supplied-chain recurrence and costs

For a chain of m explicitly normalized rooted quotients with roots r_0,...,r_(m-1),

$$H_m=H_0,\qquad
\boxed{\beta_m=2^m\beta_0-H_0R_m,\quad
R_0=0,\quad R_{i+1}=2R_i+r_i.}$$

Equivalently R_m=sum_{i=0}^{m-1}2^(m-1-i)r_i. Every root is in its own displayed short coordinate; roots from a previous or rescaled coordinate cannot be reused without conversion. A known ordinary beta-zero seed therefore gives beta_m=-H_0 R_m. The final trace supplies H_0 because each quotient is over F_p.

For arbitrary interspersed twists, one can retain H_i=epsilon_i H_0 and beta_i=M_i beta_0-N_i H_0. Start epsilon=1,M=1,N=0. A rooted quotient updates epsilon unchanged, M to 2M and N to 2N+r epsilon. A twist d updates epsilon to chi(d)epsilon and both M,N to d chi(d) times their former values. These formulas contain no division by H and are valid with supplied supersingular Cartier data.

For ordinary inputs the ratio q=beta/H simplifies the bookkeeping:

$$\boxed{q'_{\mathrm{isogeny}}=2q-r,\qquad q'_{\mathrm{twist}}=dq.}$$

Use this only after a proven ordinary seed, or after checking a certified H is nonzero. It permits a final exact trace to reconstruct beta_final=q_final H_final even when twist factors were inserted.

| Task | Cost and necessary scope |
| --- | --- |
| Verify and propagate a supplied rooted chain of length m | O(m) field operations; root-finding/search outside this bound |
| Interspersed supplied twists | O(1) field work per update plus each required Legendre-symbol exponentiation, unless the ordinary q route avoids it |
| Complete ordinary seeded preparation | T_Schoof(final curve,p)+O(m) field operations and certificate verification |
| Normalize the retained f=1+cw+bw²+aw³ and reconstruct K | O(1) field operations; A=ac-b²/3, B=a²-abc/3+2b³/27, K=(beta-bH/3)/a |
| Supplied-root branch query after preparation | O(1), using the retained branch formula; query root checked |
| Discover a chain or square roots | Separate cost; no deterministic polylogarithmic discovery result claimed |

An arbitrary curve need not have a supplied short rational path to the ordinary seeds. Fixed-depth family construction is useful because every edge and the seed can be checked; it does not prove a uniform fast method. All preparation, coordinate reconstruction and trace certification must be charged. There are at most three branch roots per cubic, so cached query costs do not establish a large-workload speedup.

## Dual consistency and why backtracking provides no new data

The target root -2r is the distinguished rational 2-torsion root of the dual quotient. Applying the same normalization at -2r gives

$$\boxed{A''=16A,\quad B''=64B,\quad H''=H,\quad\beta''=4\beta.}$$

Indeed beta''=2(2beta-rH)-(-2r)H=4beta. The twice-quotiented model is the square scaling d=4, x''=4x,y''=8y. To identify it with the original model one must rescale x=x''/4,y=y''/8; the resulting composite map has first-kind differential scale 2, as expected for multiplication by two. Treating the second normalized quotient as already returning to the identical short model would omit this scale and create a false beta constraint.

For the chain recurrence this two-edge path has R_2=2r-2r=0. It merely transports beta to 4beta. Repeated immediate dual steps therefore give no trace-only recovery or new fast family.

## One explicit nondual depth-two family

Start with the retained ordinary seed y²=x³-r²x, r nonzero and p=1 mod4. Its beta is zero by exponent support. Quotient at r gives A_1=-11r²,B_1=-14r³,beta_1=-rH. Its roots factor as

$$x^3-11r^2x-14r^3=(x+2r)(x^2-2rx-7r^2).$$

If e in F_p satisfies e²=2, take the nondual root s=(1+2e)r, distinct from -2r for p>=7. A second quotient gives

$$\boxed{A_2=(-91-60e)r^2,\qquad B_2=(-462-308e)r^3,\qquad
\beta_2=-(3+2e)rH.}$$

The derivation uses s²=(9+4e)r² and s³=(25+22e)r³, followed by the rooted transport. Nonsingularity follows from the two separable quotients. The required ordinary congruence and rational e exist simultaneously for p=1 mod8. One can either take e as supplied and verify e²=2 in constant field work, or charge a square-root algorithm separately. The formula itself does not require choosing a particular sign of e: each sign describes its corresponding rooted path.

This adds a genuinely nondual depth-two construction. It is a fixed algebraic family over Q(sqrt2), not a theorem that an arbitrary ordinary curve lies in this family. Twists d yield coefficients d²A_2,d³B_2 and beta_d=d chi(d)beta_2. Given the displayed parameters and certified final trace, the ordinary slope is q_2=-(3+2e)r and after twisting q_d=dq_2.

A parallel symbolic depth-two j=0 seed would require sqrt3 and gives A_2=(-135-60e)r²,B_2=(-694-420e)r³, beta_2=-(3+2e)rH with e²=3. This formula follows by substitution, but is not included in this pass's numerical validation or a production classifier. Its required seed ordinary congruence remains p=1 mod3; the root-existence condition is additional.

## A bounded closed-chain certificate, not a chain-finding algorithm

Suppose a supplied m-edge normalized rooted chain from (A,B) ends at (d²A,d³B), d nonzero, and define R_m as above. The twist identity and chain transport give

$$\boxed{(2^m-d\chi(d))\beta=H R_m.}$$

If the denominator is nonzero, it recovers beta from a certified trace and the verified path. This is a useful certificate-style extension even without a known seed. In the ordinary case H_final=H and H_final=chi(d)H force chi(d)=1, so a valid ordinary closure must be a square twist. The denominator becomes 2^m-d. Its nonvanishing must be checked, not inferred from the path length. At p=7, (A,B)=(5,1), roots (1,3) return to the identical model, d=1. H=3,R_2=5 gives beta=3*5/(4-1)=5 modulo 7. This small example is an illustration, not a scalability claim.

A dual two-edge loop has d=4 and 2^m=4, so its denominator and R vanish. It yields no data. More general cycles can be degenerate too. Discovering a nondegenerate closed chain can be expensive; no practical or unconditional fast search result is asserted here.

## Supersingular obstruction remains

The rooted and twist transport formulas remain correct when H=0, but become beta'=2beta and beta_d=d chi(d)beta. They propagate a supplied unknown amplitude instead of producing it. Ordinary beta-zero seeds cannot reach supersingular curves by these prime-to-p isogenies, because H is preserved and twisting only changes its sign.

Katz's Cartier/de Rham discussion shows H and beta do not simultaneously vanish for a nonsingular elliptic model. Therefore, for a genuine supersingular closed-chain certificate beta is nonzero, and the closure relation forces 2^m-d chi(d)=0. The nondegenerate recovery denominator cannot occur. This is a specific obstruction to this certificate mechanism, not a lower bound or impossibility proof for all K algorithms.

## Checks, evidence and source status

`check_closure.py` is independent of the retained evaluator. It computes coefficient pairs by exact integer multinomial coefficients reduced modulo p. It checks all nonsingular rooted short curve cases for 7<=p<60, all three supplied twist values in {1,2,p-1}, and dual normalization. Seeded random rooted chains of up to four edges use seed 20261006 for primes below150. Every recognized closure is checked by coefficient scaling and the denominator formula. Depth-two families enumerate every nonzero r and both square roots of2 for p<200,p=1mod8.

| Check | Coverage |
| --- | --- |
| Rooted coefficient transport | 15,872 rooted curve cases, including ordinary and supersingular |
| Twist identities and twist/quotient compatibility | 47,616 cases, including trivial square twists |
| Dual scaling | 15,872 cases |
| Sampled chain prefixes | 3,600 prefixes; repeated samples possible |
| Nondual depth-two family | 1,504 parameter cases |
| Nondegenerate closed-chain certificates | 225 instances; overlapping curves and repeated samples possible |

All checks passed. These totals overlap internally and earlier passes and must not be added as disjoint coverage. They support arithmetic implementation; the displayed identities supply the proof. Raw per-prime summaries, representative closure certificates and environment are retained in validation.csv and validation.json. Source hashes are retained separately. No validation runtime is a benchmark.

Sutherland, A. V. (2013). *18.782 Introduction to Arithmetic Geometry, Lecture 25*, Section25.3, pp.3–4. MIT. https://ocw.mit.edu/courses/18-782-introduction-to-arithmetic-geometry-fall-2013/e011c006f6aeb95083197457da90598d_MIT18_782F13_lec25.pdf . Directly reopened and read6 October2026. Used for the classical explicit rational degree-two quotient, independently substituted above. The dual normalization is derived explicitly here rather than inferred from ambiguous model labels in the OCR.

Katz, N. M. *On a Question of Zannier*. Experimental Mathematics. https://doi.org/10.1080/10586458.2018.1551818 . Published author text https://web.math.princeton.edu/~nmk/zannier_publ.pdf . Directly reopened6 October2026; Section1 and the de Rham/Cartier surjectivity discussion support coefficient identification and the no-common-zero statement. Final issue-year metadata not re-resolved. The rooted transport, twists and closure formulas are supplied as elementary derivations rather than attributed quotations.

No broad priority/novelty review has been performed. This is an explicit computational use of classical Cartier and low-degree isogeny machinery, with supplied-certificate costs and a bounded family.
