# Direct recognition of the ordinary depth-two families

6 October 2026. Unrefereed extension note. The retained degree-two transport and closure notes were read before this derivation. This note gives a parameter certificate and an elementary classification of the ordinary easy-seed closure through depth two. It does not revise the manuscript or claim novelty. Independent finite checks support the executable identities and membership decisions; the algebraic arguments below require human review.

## Assumptions and normalized data

Let $p\ge7$ be prime and $E:y^2=x^3+Ax+B$ nonsingular over $\mathbb F_p$. Set $h=(p-1)/2$, $H=\lbrack x^{p-1}\rbrack\,(x^3+Ax+B)^h$, and $\beta=\lbrack x^{p-2}\rbrack\,(x^3+Ax+B)^h$. The differentials are $\omega=dx/y$ and $\eta=x\omega$. The retained explicitly normalized quotient at a rational root $q$ is

\[
A'=-4A-15q^2,\qquad B'=-8Aq-22q^3,
\]
\[
\phi^*\omega'=\omega,\qquad
\phi^*\eta'=(2x-q)\omega-2d\left(\frac{y}{x-q}\right),
\qquad H'=H,\quad \beta'=2\beta-qH.
\]

The differential scale is $+1$, and the second-kind correction is a global exact differential. At infinity, using $t=-x/y$, one has $x=t^{-2}+O(t^2)$, $y=-t^{-3}+O(t)$, hence $\eta=+2t^{-2}dt+O(1)dt$; there is no $t^{-1}dt$ term. The sign would be negative if $t=x/y$ were chosen instead. At the kernel point, using $z=y$, the primitive has leading term $F'(q)/z$, where $F(x)=x^3+Ax+B$, and its derivative has leading term $-F'(q)z^{-2}dz$. Thus the exact correction contributes $+2F'(q)z^{-2}dz$ there, with zero residue. These facts explain why substituting only the principal part at infinity would omit essential data. With $dx/(2y)$ the primitive correction has coefficient $-1$, while the transport law for the coefficient pair is unchanged. This note uses the retained global identity rather than a new local-residue shortcut.

The easy seeds are the ordinary $B=0$ models for $p\equiv1\pmod4$, and the ordinary $A=0$ models for $p\equiv1\pmod3$. Exponent support gives $\beta=0$ in each class; the surviving coefficient of $H$ is a nonzero binomial coefficient with arguments below $p$. Thus the seed ordinarity and slope zero are elementary here, rather than assumed from experimental traces.

## The two families and their twist closure

For $n\in\{2,3\}$, put

| $n$ | Required ordinary prime class | $\alpha_n(e)$ | $\gamma_n(e)$ |
| --- | --- | --- | --- |
| $2$ | $p\equiv1\pmod8$ | $-91-60e$ | $-462-308e$ |
| $3$ | $p\equiv1\pmod{12}$ | $-135-60e$ | $-694-420e$ |

For $e^2=n$ and $r\ne0$, the target and its coefficient are

\[
A=\alpha_n(e)r^2,\quad B=\gamma_n(e)r^3,
\qquad \boxed{\beta=-(3+2e)rH.}
\]

For $n=2$, start at $(A_0,B_0)=(-r^2,0)$, quotient at $r$, then at $(1+2e)r$. The first model is $(-11r^2,-14r^3)$, whose cubic factors as $(x+2r)(x^2-2rx-7r^2)$. The second root is nondual because $e^2=2$ prevents $(1+2e)r=-2r$ in characteristic at least seven. Substitution gives the displayed target and slope.

For $n=3$, start at $(A_0,B_0)=(0,-r^3)$. The first target is $(-15r^2,-22r^3)$, with factorization $(x+2r)(x^2-2rx-11r^2)$. The nondual roots are $(1+2e)r$, $e^2=3$. Now $s^2=(13+4e)r^2$ and $s^3=(37+30e)r^3$; substituting in the same quotient formulas gives $-135-60e$ and $-694-420e$. Both two-step slopes are $2(-r)-(1+2e)r=-(3+2e)r$. Rational nondual roots and ordinary seeds coexist precisely in the listed prime classes, using the usual quadratic-character formulas for two and three.

For a displayed quadratic twist $d\ne0$, direct polynomial scaling gives

\[
H_d=\chi(d)H,\qquad \beta_d=d\chi(d)\beta,
\qquad (A_d,B_d)=(d^2A,d^3B).
\]

For these families the twist is absorbed exactly by $r\mapsto dr$. Thus the parameterized family already includes every quadratic twist, with no nonresidue choice or square root of $d$. The recovered slope uses the final model's certified $H$, so no Legendre-symbol calculation is required in reconstruction. This claim concerns quadratic twists; it does not equate different quartic twists of $j=1728$ or sextic twists of $j=0$. The full seed classes are separately included when classifying the closure.

## Direct extraction without a square-root algorithm

Reduce $\alpha_n(e)^3=a_0+a_1e$, $\gamma_n(e)^2=g_0+g_1e$ modulo $e^2=n$. The exact integer constants are

| $n$ | $a_0$ | $a_1$ | $g_0$ | $g_1$ |
| --- | --- | --- | --- | --- |
| $2$ | $-2719171$ | $-1922580$ | $403172$ | $284592$ |
| $3$ | $-6834375$ | $-3928500$ | $1010836$ | $582960$ |

Given the actual short coefficients $A,B$, compute

\[
U=a_0B^2-g_0A^3,\qquad V=a_1B^2-g_1A^3,
\qquad \boxed{e=-U/V},
\]
\[
\boxed{r=\frac{\alpha_n(e)B}{\gamma_n(e)A}}.
\]

These are proposals until all conditions are verified: the appropriate prime congruence, nonsingularity, $A B V\ne0$, $e^2=n$, $r\ne0$, $A=\alpha_n(e)r^2$, and $B=\gamma_n(e)r^3$. Once they pass, the preceding explicit path proves the stated coefficient identity. Conversely every permitted parameter model passes, because

\[
V=\bigl(a_1g_0-g_1a_0\bigr)r^6.
\]

Both $e$ and $r$ are unique on a permitted family. Thus recognition uses a constant number of field operations including inversions, with no random factoring or square-root step. This is stronger than a supplied-$e$ certificate: the input model itself supplies the necessary conjugate choice. A $j$-only membership test does not supply the coordinate-dependent factor $r$, and cannot by itself normalize $\beta$.

## Vanishing and conjugate collisions

For a linear quadratic-algebra element $a+be$, its norm is $a^2-nb^2$. The following exact factorizations identify every possible vanishing prime, before considering the ordinary congruence.

| Family | Quantity | Integer value or factorization |
| --- | --- | --- |
| $n=2$ | $N(\alpha)$ | $23\cdot47$ |
| $n=2$ | $N(\gamma)$ | $2^2 7^2 11^2$ |
| $n=2$ | $a_1g_0-g_1a_0$ | $-2^6\cdot3\cdot7^2\cdot11^2\cdot19\cdot59$ |
| $n=2$ | $4\alpha^3+27\gamma^2$ | $8960-6336e$, norm $-2^{13}$ |
| $n=3$ | $N(\alpha)$ | $3^3 5^2 11$ |
| $n=3$ | $N(\gamma)$ | $-2^2\cdot11\cdot23\cdot47$ |
| $n=3$ | $a_1g_0-g_1a_0$ | $2^6 3^4 5^3 17\cdot29\cdot41$ |
| $n=3$ | $4\alpha^3+27\gamma^2$ | $-44928+25920e$, norm $2^{12}3^6$ |

No prime $p\equiv1\pmod8$ divides the relevant $n=2$ factors, and no prime $p\equiv1\pmod{12}$ divides the $n=3$ factors. Therefore the accepted ordinary families never have zero $\alpha$, zero $\gamma$, zero extraction denominator, singular models, or a collision of the two conjugate $j$ values, for any $p\ge7$. This eliminates a case split in the ordinary recognizer; it does not authorize ignoring the congruence check.

Small-characteristic degeneracies are real outside the ordinary range. At $p=7$, both $n=2$ conjugates have $\gamma=0$, and collapse to $j=1728$. At $p=23$, the $n=2$ choice $e=5$ gives $\alpha=0$, hence $j=0$. At $p=11$, the $n=3$ choices $e=6$ and $e=5$ give respectively $\alpha=0$ and $\gamma=0$. These models are nonsingular, but their seed congruences fail and the beta-zero ordinary reconstruction is unavailable. Rejecting them preserves the supersingular obstruction. Other listed exceptional primes may have no rational $e$, in which case they do not define a base-field parameter model at all. The CSV explicitly records root existence and congruence status.

## Collisions with lower-depth and other depth-two classes

The two conjugate $j$ values satisfy the following monic integer polynomials, derived by eliminating $e$ from $j=6912\alpha^3/(4\alpha^3+27\gamma^2)$:

\[
P_2(J)=J^2-82226316240J-7367066619912,
\]
\[
P_3(J)=J^2-2835810000J+6549518250000.
\]

These are classical CM polynomials: Lario’s author-maintained table lists them for order discriminants $-64$ and $-48$, respectively. This is prior-work context, not evidence that the recognition formula or its computational application is new. The table lists all possible prime factors at least seven for a collision with a seed or one-step $j$, from exact evaluations of $P_n$. Every entry fails the ordinary prime class for that row.

| Family | $J=0$ | $J=1728$ | $J=287496$ | $J=54000$ |
| --- | --- | --- | --- | --- |
| $n=2$ | $23,47$ | $7,11$ | $7,19,23,31$ | $11,23,71,167,191$ |
| $n=3$ | $11$ | $11,23,47$ | $11,23,71,167,191$ | $11,17,23$ |

The mixed resultant is

\[
\operatorname{Res}(P_2,P_3)
=2^6 3^{12}11^4\cdot23\cdot47\cdot59^2\cdot239\cdot479\cdot599\cdot647\cdot719\cdot743.
\]

When both families are eligible, $p\equiv1\pmod{24}$. No prime factor in the mixed resultant satisfies this congruence. Hence the two ordinary depth-two families do not collide with each other. These factorization arguments are global algebraic exclusions, not extrapolations from the finite graph census. They establish actual new $j$ classes for every eligible ordinary prime, after all lower-depth classes and dual square scalings are removed.

## Completeness through depth two

From a $j=1728$ seed, the root zero remains in the seed class. A nonzero root exists precisely when the seed can be written $(-r^2,0)$, and the first quotient is $(-11r^2,-14r^3)$. Its next root is either the distinguished dual root $-2r$, returning to square scaling of the seed, or one of the two nondual roots requiring $e^2=2$. From a $j=0$ seed, a rational root $r$ gives the first quotient $(-15r^2,-22r^3)$; its second roots have exactly the corresponding dual/nondual split with $e^2=3$. Each possible first root is already included by allowing all $r\ne0$. A dual pair gives $(16A,64B)$, the square scaling $d=4$, and supplies no new class or coefficient information.

Consequently the ordinary closure through depth two consists exactly of the two seed classes, the two one-step parameter families, and the two nondual depth-two families above when their congruences hold. This statement concerns paths originating in the retained easy seeds, rational normalized degree-two quotients, and arbitrary displayed quadratic twists. It is not a classification of all degree-four isogenies, all elliptic curves, or all CM reductions.

## Costs, original cubic reconstruction, and an example

For the retained original cubic $f(w)=1+cw+bw^2+aw^3$, $a\ne0$, normalize with $x=aw+b/3$, $y=av$, so 

\[
A=ac-b^2/3,\quad B=a^2-abc/3+2b^3/27,
\qquad K=\frac{\beta-(b/3)H}{a}.
\]

The normalization has differential scale $dw/v=dx/y$; no additional factor of two is inserted. Once a recognition certificate has passed and an exact final trace has been supplied, $H$ is its reduction modulo $p$, and $\beta=-(3+2e)rH$. Therefore $K$ is recovered directly. The existing branch-root formula is then applied with its previously explicit scale and sign.

| Task | Cost and status |
| --- | --- |
| Direct family recognition and complete parameter certificate verification | $O(1)$ field operations including a constant number of inversions |
| Complete unconditional preparation for an accepted curve | $T_{\mathrm{Schoof}}(E,p)+O(1)$ field operations; trace preparation is charged |
| Prototype accepting an external trace | Trusted-data result; a Hasse interval check does not certify that trace |
| Original cubic normalization and $K$ reconstruction | $O(1)$ field operations |
| Existing supplied rational branch-root query after preparation | $O(1)$ field operations |
| Bit cost | Field inversions and operations have their usual polynomial cost in $\log p$; no arithmetic benchmark is claimed |

At $p=13$, choose $n=3,e=4,r=1$. The short model is $(A,B)=(2,5)$, its exact coefficient pair is $(H,\beta)=(2,4)$, and the slope is $2$. Its twist by $d=2$ has $(A_d,B_d)=(8,1)$, $r_d=2$, slope $4$, and $(H_d,\beta_d)=(11,5)$. Recognition obtains these parameters from the coefficients alone. Both conjugates are outside all lower-depth classes at this prime.

## Independent checks and research status

The standalone standard-library script `check_recognition.py` does not import the retained evaluator. Its coefficient checks use integer multinomial expansions. It enumerates every eligible $e$ and nonzero $r$ through prime $250$, verifies parameter extraction and a displayed twist, and compares the recognizer against independently generated membership sets for every nonsingular short model through prime $73$. Finite expansion checks extend through prime $97$. Outputs retain raw CSVs, Python/platform information and source hashes.

| Check | Count and scope |
| --- | --- |
| Family parameter certificates and displayed twist checks | $5,208$ parameter cases, $7\le p\le250$ |
| Independent exact $H,\beta$ pairs | $1,176$ model pairs through $p=97$ |
| Exhaustive nonsingular short-model membership decisions | $69,192$ family-specific decisions through $p=73$ |
| Exceptional reduction records | $56$ rational-parameter rows across exceptional prime factors |

All delivered checks pass. These counts overlap parameter/model inputs and are not counts of distinct mathematical theorems. The constant-operation recognizer and global collision exclusion are derived results with supporting prototype checks; they remain unrefereed. Generic $K$, supersingular amplitude recovery, and higher-depth class coverage remain separate open targets. Matching $j$ and discarding the coordinate parameter is a retained unsuccessful approach because it loses the normalization factor required for $\beta$.

## Verified primary context

Sutherland, A. V. (2013). *18.782 Introduction to arithmetic geometry, Lecture 25*, Section 25.3. Massachusetts Institute of Technology. https://ocw.mit.edu/courses/18-782-introduction-to-arithmetic-geometry-fall-2013/e011c006f6aeb95083197457da90598d_MIT18_782F13_lec25.pdf . Directly reopened 6 October 2026. The classical rational-kernel quotient is background; the coordinate normalization and second-kind correction used here are explicitly derived in the retained extension notes.

Katz, N. M. *On a Question of Zannier*. Published author text: https://web.math.princeton.edu/~nmk/zannier_publ.pdf . Directly reopened 6 October 2026; Section 1 provides the coefficient/Cartier context. The current note does not attribute its family recognition or novelty to that paper, and does not rely on unverified issue-year metadata.


Lario, J.-C. (n.d.). *Elliptic curves with CM defined over extensions of type (2,...,2).* Author-maintained academic data table. https://web.mat.upc.edu/joan.carles.lario/ellipticm.htm . Directly opened 6 October 2026; rows for discriminants $-48$ and $-64$ agree with the two exact polynomial eliminations above. This is a primary author-curated computational table, not a refereed novelty assessment.
