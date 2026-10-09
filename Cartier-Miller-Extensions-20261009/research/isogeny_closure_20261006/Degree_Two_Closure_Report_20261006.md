# Bounded rational degree-two isogeny closure for Cartier–Miller branch evaluation

6 October 2026. Separate, unrefereed extension research. The published manuscript is unchanged. GitHub URL and commit are unknown; no GitHub inspection was performed. Proofs require human mathematical review, and no novelty or performance benchmark is claimed.

## Concrete outcome

The degree-two route now has a checked supplied-path evaluator and a bounded path-discovery prototype. Depth two reaches curves outside the previous depth-zero and depth-one classes. An explicit algebraic depth-two family is also derived. None of this supplies a uniform method for arbitrary curves or supersingular missing coefficients.

| Result | Evidence category | Status |
|---|---|---|
| Normalized rooted transport and reverse-chain formula | Global algebraic differential derivation | Unrefereed proof, independently derived and checked |
| Recovery along a supplied path to an easy seed | Proof plus implementation | O(path length) field work after exact trace preparation |
| Depth-limited discovery using rational cubic roots | Implemented randomized fixed-degree factorization | Verified positive paths; explicit bounded misses and splitting failures |
| New depth-two algebraic family | Explicit two-quotient derivation | Proof and 1,504 parameter checks; core graph search can reach it, no dedicated symbolic classifier |
| Nondegenerate closed-chain certificates | Algebraic corollary and separate checks | Theory branch only; not integrated into core preparation/search |
| Generic or supersingular fast K | Unresolved | No such claim |

The two research agents worked complementary theory and independent graph-audit branches. The parent implemented the search and separately checked coefficient recovery with integer multinomial coefficients and dense normalized branch sums. Test counts overlap; none are combined as disjoint coverage.

## Assumptions and inherited normalization

Take p>=7 prime, squarefree f(w)=1+cw+bw²+aw³ with a nonzero, and h=(p-1)/2. The earlier independently normalized branch note defines H=[w^(p-1)]f^h and K=[w^(p-2)]f^h and derives

$$T_f(\mu)=S_f(1/\mu)=\frac{a\mu}{f'(\mu)}(\mu H-K)$$

for a supplied nonzero rational root mu. This remains the fixed-cutoff branch output; no original weighted-sum endpoint is silently inferred.

Use the infinity-origin short coordinate x=aw+b/3,y=av:

$$A=ac-b^2/3,\quad B=a^2-abc/3+2b^3/27,\quad dw/v=dx/y=2dx/(2y).$$

On y²=x³+Ax+B, put beta=\[x^(p-2)\](x³+Ax+B)^h. Then beta=aK+(b/3)H and H equals the exact trace modulo p, using trace p+1-#E(F_p). The easy seed tests are A=0 with p congruent to 1 modulo 3, or B=0 with p congruent to 1 modulo 4. Exponent support supplies beta=0 in these classes. The characteristic-p branch residue and direct exceptional normalization in the existing manuscript are not revised.

## Rooted degree-two map, scales and signs

For a rational root q of x³+Ax+B, write u=A+3q². Squarefreeness ensures u nonzero. The normalized short quotient is

$$x'=x+\frac{u}{x-q},\qquad y'=y\left(1-\frac{u}{(x-q)^2}\right),$$

with

$$\boxed{A'=-4A-15q^2,\quad B'=-8Aq-22q^3.}$$

For omega=dx/y and eta=x omega, explicit differentiation gives

$$\phi^*\omega'=\omega,\qquad
\phi^*\eta'=(2x-q)\omega-2d\!\left(\frac{y}{x-q}\right).$$

Indeed d(y/(x-q))=1/2((x-q)-u/(x-q))omega. The exact primitive has poles at the kernel point and infinity, matching the two pullback poles. This is a global identity, not just principal-part cancellation. In the basis dx/(2y), the exact correction is -d(y/(x-q)); the holomorphic scale remains +1.

Cartier kills the exact term and is natural for the separable quotient; the separating-variable proof is included in the theory note. Hence

$$\boxed{H'=H,\qquad \beta'=2\beta-qH.}$$

This transport identity is valid also for supersingular curves. Trace-only recovery needs a seed with known beta, rather than merely a zero trace.

## Supplied paths and explicit recovery

For a path starting at the requested input and ending at an easy seed, let q_i be the rational root in the displayed short coordinate at step i. Reverse transport gives

$$\boxed{\beta_{\rm input}=H\sum_{i=0}^{m-1}\frac{q_i}{2^{i+1}},\qquad
K=\frac{\beta_{\rm input}-(b/3)H}{a}.}$$

The implementation computes this without dividing by H. It verifies every root, target nonsingularity and the endpoint seed conditions; a path ending at an unsupported curve is rejected. An empty path is valid only for an easy input. Each certificate records the exact models, roots, scale +1 and beta multiplier.

With a forward seed-to-input path, the equivalent relation is beta_m=2^m beta_0-H R_m, R_0=0, R_(i+1)=2R_i+q_i. These two orientations must not be mixed.

## Actual extension beyond depth one

Modulo 13 the short input y²=x³+12x+10 has the reverse path

$$ (12,10)\xrightarrow{q=5}(6,7)\xrightarrow{q=12}(0,5). $$

The endpoint satisfies A=0 and p=1 mod3. Its exact trace, shared by the input, is -2; thus H=11. The multiplier is 5/2+12/4=12 modulo13, giving beta_input=2. The input j=6 lies outside all seed and depth-one j sets at this prime, so this is not merely a dual backtrack or a renamed one-step class. Matching j alone is never used to reconstruct coefficients or identify base-field twists.

A corresponding normalized original cubic is f=1+12w+9w³. Its short model is (A,B)=(4,3); the supplied roots in this coordinate are 11 and 3, giving multiplier3, beta=7 and K=8. With mu=7, f'(mu)=9 and a=9, the branch result is T=2. Dense polynomial expansion agrees independently. This example has a supplied-trace status, not a certified backend claim.

The graph audit enumerated every nonzero easy seed coefficient through p=127 and all outgoing rational edges to depth two. New depth-two j classes occur at ten tested primes: 13,17,37,41,61,73,89,97,109,113. This finite finding is evidence about bounded coverage. It does not assert general coverage or a fraction of all isogeny classes. At p=13,(A,B)=(1,1),j=7 lies outside the depth-at-most-two seed closure and is a retained bounded-miss fixture. At p=11 mod12 neither seed class is available, so this construction supplies no seed path there.

## An explicit nondual depth-two family

Start with the ordinary seed y²=x³-r²x, r nonzero, p=1 mod4. Quotient at r to obtain A_1=-11r²,B_1=-14r³,beta_1=-rH. The target factors as (x+2r)(x²-2rx-7r²). If e²=2 in F_p, the nondual root q=(1+2e)r gives

$$\boxed{A_2=(-91-60e)r^2,\quad B_2=(-462-308e)r^3,\quad
\beta_2=-(3+2e)rH.}$$

The ordinary seed condition and rational e occur simultaneously when p=1 mod8. Both signs of e give their respective paths. The source and target are nonsingular because both quotients are separable. Supplied e,r can be checked with constant-degree arithmetic; finding e or recognizing the parameters must be charged. The core search handles general normalized models rather than implementing a dedicated inverse classifier for this parameterization.

The theory note also derives a depth-two j=0 analogue using e²=3: A_2=(-135-60e)r²,B_2=(-694-420e)r³,beta_2=-(3+2e)rH, with its additional root-existence condition. This analogue was not numerically validated as a parameter family in this pass and is not a separate implemented recognizer.

## Scaling, twists, backtracking and an auxiliary certificate

For the displayed twist (A_d,B_d)=(d²A,d³B), d nonzero, direct coefficient scaling gives

$$H_d=\chi(d)H,\quad \beta_d=d\chi(d)\beta,\quad \chi(d)=d^{(p-1)/2}.$$

For d=s² the coordinate map x_d=s²x,y_d=s³y has differential pullback scale 1/s; thus beta_d=s²beta and H_d=H. A nonsquare d needs an extension-field square root for a point map, but the base-field coefficient identity above is still valid. This prevents merging normalized data on j alone. The rooted map commutes with twisting after q is replaced by dq.

The dual kernel root is -2q. Applying that quotient gives (A'',B'')=(16A,64B),H''=H,beta''=4beta. Identifying it with the original model requires scaling back x''/4,y''/8; the composite then has differential scale2. Ignoring this model change would create a false constraint. The corresponding two-step R is zero and supplies no missing coefficient.

A separate theory corollary is worth retaining: a verified m-edge chain ending at (d²A,d³B) satisfies (2^m-d chi(d))beta=H R_m. If its denominator is nonzero, the chain and exact trace recover beta without an easy seed. For p=7,(A,B)=(5,1),roots1,3,d=1,H=3,R=5 give beta=5. This is not integrated into the core search and supplies no cheap chain-discovery claim. A supersingular genuine closure has H=0,beta nonzero, forcing the denominator to vanish; the certificate does not recover its amplitude. The no-common-zero fact is classical Cartier/de Rham context from Katz, not numerical inference.

## Discovery algorithm and costs

The supplied-path route is deterministic once the path and exact trace are supplied. The automatic route performs breadth-first search on exact displayed coefficient pairs, with no j-only merging. Every vertex has at most three rational roots. For each cubic F it computes G=gcd(F,x^p-x) by modular exponentiation, then splits G using uniformly random polynomial trials and quadratic-character gcds. The product of returned linear factors is checked against G, certifying that all rational roots were obtained. No hidden O(p) scan fallback is used.

For fixed degree, every modular power takes O(log p) field operations. Chinese-remainder independence gives a constant split success probability; complete uncapped root extraction has expected O(log p) field cost. The code caps each recursive split at64 attempts and explicitly reports exhaustion. This randomized cost follows classical finite-field factorization, not an assumption about integer factoring or point counts. The audit deliberately uses an independent O(p) root scan for correctness comparison.

| Task | Cost and scope |
|---|---|
| Supplied m-edge path verification and K reconstruction | O(m) field operations, including fixed-degree roots/model checks and inversions |
| Complete seeded preparation with supplied path | T_Schoof(p)+O(m) field operations; trace computation/certification included in T_Schoof |
| Automatic search to depth d | Expected O(3^d log p) field operations with uncapped independent root trials; capped implementation has explicit failure |
| Complete automatic preparation after successful discovery | Exact trace preparation plus discovery and O(d) reconstruction; randomized discovery is not a deterministic worst-case guarantee |
| Breadth-first storage | O(3^d) field elements/model and predecessor records; O(d) final reconstructed path |
| Supplied-root branch query | O(1) field operations after preparation |
| Root search for an original branch mu | Outside query cost; mu is supplied and checked |
| Deterministic validation scans | O(p) root work per vertex; not a speed comparator |

At depth two there are at most13 tree vertices before deduplication, and at most4 expanded vertices requiring root extraction. Search depth is a bounded parameter, not a hidden logarithmic guarantee. Larger depth can create exponentially more work. The implementation distinguishes found, not_found_within_depth, incomplete_root_splitting and invalid paths. A bounded negative result, when all required splits finish, covers all normalized rational paths within the stated depth; it is not a proof that no longer path exists. If any relevant split fails, no negative completeness claim is made. A found path remains valid even if another branch previously failed.

The prototype is standard-library Python with the retained fixed 64-bit prime guard. The exact trace is caller supplied and explicitly trusted; a Hasse interval check does not certify it. No point-count backend, production SEA, modular-polynomial database or generic isogeny-search system has been added. Schoof remains the unconditional theoretical setup, with practical point-count alternatives a separate engineering choice. No wall-time speedup is claimed. Cached query costs cannot hide preparation for at most three rational branches per cubic.

## Validation, failed shortcuts and reproducibility

| Independent check | Coverage | Evidence |
|---|---|---|
| Parent core root/discovery checks | All 7,948 nonsingular short cubics at primes7 through43 | Randomized roots versus exhaustive scans; multiplier versus integer multinomial coefficients |
| Parent bounded recovery | 760 curves found:276 depth0,276 depth1,208 depth2;7,188 bounded misses | Exact displayed models, not disjoint j classes |
| Parent normalized original outputs | 186 normalized cubics,330 rational branch queries | Dense polynomial powers and exact direct point counts |
| Parent transport/dual checks | 7,688 edges each;15,896 twist checks | Separate multinomial coefficient calculation |
| Independent graph audit | 7,420 directed edges across4,960 dense models through p127 | Dense expansions, root scans, conservative j coverage |
| Independent theory checks | 15,872 rooted/dual cases,47,616 twists,3,600 prefixes,1,504 depth-two parameters,225 nondegenerate cycle instances | Integer multinomial expansions; overlapping/repeated inputs |

All checks passed. Counts overlap both across branches and with earlier investigations; they are not added as unique curve coverage. No validation timing is used as benchmark evidence. Raw per-curve or per-prime CSVs, JSON results, seeds, environment details and source hashes are retained.

Root retries forced to zero produce an explicit incomplete status in a split case. Invalid kernel roots, unsupported endpoints and depth-zero misses are checked. During implementation a zero polynomial represented as [0,0] exposed a gcd canonicalization bug; trimming gcd inputs fixed it before the delivered run. A preparation-method label initially missed the retained evaluator's caller_supplied marker; it was corrected and all330 query statuses now explicitly report computed_from_trusted_data. Neither repair changed the mathematical transport law.

The mathematical failures remain informative: immediate dual backtracking gives only scaling, j matches do not supply coefficient normalization, supersingular transport preserves an unknown beta amplitude, finite-difference trace jets remain unavailable, and bounded misses do not imply global failure. These are recorded rather than presented as proof that every broader approach is impossible.

The relevant historical implementations and previous branch notes were checked before this extension; no completed isogeny-closure evaluator was found in the inspected handover. The complete third-point ordinary evaluator, higher-genus prefix prototypes and complete sum-first Witt/BGS branch remain separate. This result implies neither fast complete original weighted sums without their boundary coefficients nor a fast sum-avoiding Witt correction.

## Sources and review status

The explicit quotient map and classical factorization route were verified in primary mathematical sources. The coefficient transport and chain formulas are derived in the attached notes, rather than attributed as direct quotations. These are computational applications of classical machinery; a wider priority review remains necessary.

| APA-style reference | Verified primary text |
|---|---|
| Sutherland, A. V. (2013). Introduction to arithmetic geometry, Lecture25, section25.3. MIT. | https://ocw.mit.edu/courses/18-782-introduction-to-arithmetic-geometry-fall-2013/e011c006f6aeb95083197457da90598d_MIT18_782F13_lec25.pdf |
| Katz, N. M. (2019, online publication). On a question of Zannier. Experimental Mathematics. https://doi.org/10.1080/10586458.2018.1551818 . Final issue date not reverified. | https://web.math.princeton.edu/~nmk/zannier_publ.pdf |
| von zur Gathen, J., & Panario, D. (2001). Factoring polynomials over finite fields: A survey. Journal of Symbolic Computation,31,3–17. https://doi.org/10.1006/jsco.1999.1002 | https://people.csail.mit.edu/dmoshkov/courses/codes/poly-factorization.pdf |

## Suggested next bounded question

The next useful theoretical target is a direct, parameter-checked recognition certificate for the depth-two families, including twists and small-characteristic collisions, together with deciding which higher-depth paths add new classes after removing dual scaling. A depth-three coverage pass is a testable prototype question, not yet a theorem. Closed-chain certificates are a complementary exploratory branch only if their discovery cost is fully charged. A general fast supersingular coefficient remains a distinct harder problem.
