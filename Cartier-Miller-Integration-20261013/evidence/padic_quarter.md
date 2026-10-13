---
title: A p adic lift of the Miller coefficient
subtitle: Exact correction formulas and the remaining computational problem
date: 28 September 2026
---

## What this investigation established

The elliptic coefficient in our quarter-point evaluation has a well-defined lift to higher powers of $p$, once the integral curve and its local coordinate are fixed. We proved how to compute its first lift, modulo $p^2$, using a logarithmic number of elliptic group operations after the original setup. We also proved an exact identity that explains the additional information needed to lift the incomplete binomial sum.

The extra information is one coefficient of a normalized Miller function, expressed as an Euler-product or Witt coordinate. Its contribution vanishes modulo $p$ and becomes visible modulo $p^2$. This gives a concrete research target. We have not found a fast way to obtain that coefficient, so this branch does not yet give a fast modulo-$p^2$ algorithm for the incomplete sum or for $U_p(L)$.

In everyday terms, the original method reads one base-$p$ digit of the answer from the elliptic curve. The curve calculation can be made more precise, but that alone does not reveal the next digit of the sum. The proof now identifies a particular missing piece and states exactly how it contributes.

| Result | Scope | Status |
|:--|:--|:--|
| First correction from the original rational $U_p(L)$ | Every odd prime and $0\le L\le h$ | Proved modulo $p^2$ |
| Torsion lift and geometric elliptic coefficient | $p=4n+1\ge13$ | Proved and implemented modulo $p^2$ |
| Boundary coefficient modulo $p^2$ | Same quarter family | Known Chowla–Dwork–Evans theorem |
| Exact relation with a Witt coordinate | Same quarter family | Proved here; novelty uncertain |
| Unchanged formula and simple unit-root replacement | Same quarter family | Disproved by exact counterexamples |
| Fast incomplete summation modulo $p^2$ | Quarter family or arbitrary $L$ | Unresolved |

This is an additional research branch. The preceding combined report and implementation are preserved unchanged in `inputs/`. No conclusion about a decimal BBP formula, factoring, or Wilson-prime searches follows from the new results.

## Definitions and preserved baseline

For an odd prime $p$, put $h=(p-1)/2$. The original quantities are rational numbers

$$
t_0=1,\qquad t_{i+1}=t_i\frac{h+2+i}{2i+2},\qquad
U_p(L)=\sum_{i=0}^{L-1}(h+1+i)t_i.
$$

Throughout, $0\le L\le h$. Reduction modulo $p^2$ means reduction of these rational numbers using inverses of their denominators. Define

$$
a_i=\binom{2i}{i}8^{-i},\qquad B_L=\sum_{i=0}^{L-1}a_i.
$$

The exact identity $t_i=2^{-i}\binom{h+1+i}{i}$ follows from the recurrence. Upper negation and $-h-2\equiv h-1\pmod p$ give

$$
t_i\equiv\binom{h-1}{i}\left(-\frac12\right)^i
\equiv(2i+1)a_i\pmod p\qquad(0\le i<h).
$$

Let $S_m(L;x)=\sum_{i<L}\binom mi x^i$. For $1\le L\le h$ the original boundary identity is

$$
U_p(L)\equiv2S_{h-1}(L;-1/2)+(h-L)t_{L-1}\pmod p.
$$

For completeness, it holds at $L=1$. Subtract its versions at $L+1$ and $L$ and use $2Lt_L=(h+L+1)t_{L-1}$. The discrepancy is $-(2h+1)t_{L-1}=-pt_{L-1}$, which vanishes modulo $p$. At $L=h$, the binomial theorem and Euler's criterion therefore give $U_p(h)\equiv4(2/p)$. These are baseline results, not discoveries in this branch. The rational value $U_7(3)=39$ still supplies a counterexample to the unchanged full-block congruence modulo $49$.

An exact identity over $\mathbb Q$, useful at both precisions, is

$$
\frac12\sum_{i<L}(2i+1)^2a_i
=4B_L-2L(2L+5)a_L.
\qquad\text{(B)}
$$

Indeed, with $G_i=-4i(2i+5)a_i$ and $a_{i+1}/a_i=(2i+1)/(4i+4)$, direct simplification gives $G_{i+1}-G_i=((2i+1)^2-8)a_i$. Summing proves (B). This exact certificate is preserved rather than treating its modular specialization as new.

## The first correction for every stopping point

Define the odd harmonic sums

$$
O_i=\sum_{j=1}^{i}\frac1{2j+1},\qquad O_0=0,
$$

and the correction residue

$$
\mathcal H_L=\frac12\sum_{i<L}a_i
\left((2i+1)+(2i+1)^2O_i\right)\pmod p.
$$

**Theorem A.** For every odd prime and every permitted $L$,

$$
U_p(L)\equiv4B_L-2L(2L+5)a_L+p\mathcal H_L\pmod{p^2}.
\qquad\text{(A)}
$$

Here $B_L$ and $a_L$ must be evaluated modulo $p^2$; only $\mathcal H_L$ is needed modulo $p$.

**Proof.** The original recurrence gives, exactly for $i<h$,

$$
t_i=(2i+1)a_i\prod_{j=1}^{i}\left(1+\frac p{2j+1}\right).
$$

Its denominators satisfy $2j+1\le p-2$, so they are units. Expanding the product modulo $p^2$ gives $t_i\equiv(2i+1)a_i(1+pO_i)$. Since $h+1+i=(2i+1+p)/2$, multiplication and summation give (A) using (B). Empty sums cover $L=0$. The boundary $a_h$ is also integral at $p$ because $2h=p-1$. This checks both truncation endpoints. $\square$

At the quarter point $p=4n+1$, the formula becomes

$$
U_p(n)\equiv4B_n+\frac94a_n+p(\mathcal H_n-2a_n)\pmod{p^2}.
\qquad\text{(Aq)}
$$

The extra term matters. For $p=17$, direct rational summation gives $U_{17}(4)=179\pmod{289}$, whereas $4B_4+9a_4/4=43\pmod{289}$. The difference is $136=17\cdot8$. Consequently, a lift of $B_n$ alone does not automatically lift the old expression for $U_p(n)$.

The sum defining $\mathcal H_L$ is currently a linear-work reference. Its introduction does not improve the algorithm. Cancellation between this correction and other corrections remains possible and has not been excluded.

## Lifting the elliptic construction

For the rest of the geometric analysis, assume $p=4n+1\ge13$, put $\chi=(2/p)$, and use

$$
E:y^2=x^3+2x,\qquad \sigma^2=2,\qquad
R_+=(2-\sigma,4-2\sigma),\qquad T=(0,0).
$$

The coefficient from the previous report is

$$
e=\sigma(1-\mathcal A(R_+)),\qquad
B_n\equiv e(\chi-a_n)\pmod p.
\qquad\text{(E0)}
$$

For an annihilator $M$ prime to $p$, let $f_{M,R}$ have divisor $M(R)-M(O)$. With $t=-x/y$ at the identity, the definition is

$$
\mathcal A(R)=\frac1M[t^0]\frac{d}{dt}\log f_{M,R}.
$$

The expression denotes a logarithmic derivative; evaluating an analytic logarithm is unnecessary. Multiplication of $f_{M,R}$ by a nonzero constant does not affect it. Replacing $M$ by another permitted annihilator does not affect $\mathcal A$ either, since the functions become powers of a function for the exact order of $R$.

The inherited setup supplies the exact trace $\tau$ and an even annihilator

$$
M=\begin{cases}
p+1-\tau,&\chi=1,\\
(p+1)^2-\tau^2,&\chi=-1.
\end{cases}
$$

The trace is even and satisfies $|\tau|\le2\sqrt p<p-1$. Thus $\tau\not\equiv\pm1\pmod p$, proving $p\nmid M$ in this family. The exceptional prime $5$ is outside the theorem.

Work on the fixed integral model $y^2=x^3+2x$ over $\mathcal O$, where $\mathcal O=\mathbb Z_p$ when $\chi=1$, and is its unramified quadratic extension when $\chi=-1$. Its discriminant is $-512$, a unit. The reduction map on torsion of order prime to $p$ is an isomorphism after the appropriate unramified extension [S1]. Thus $R_+$ has a unique such torsion lift $\widetilde R_+$ on this model. “Unique” here refers to this fixed model and the given residue point.

**Theorem B.** The quantity $\mathcal A(\widetilde R_+)$ is integral and computable modulo $p^2$ with $O(\log M)$ group operations and a constant number of ring elements after the setup. A geometric lift of $e$ is obtained as follows:

$$
z=\frac{2\widetilde x}{\widetilde y},\qquad
\beta=1-\frac{2\widetilde x^3}{\widetilde y^2},\qquad
\varepsilon=\frac{z^{-1}-\mathcal A(\widetilde R_+)}{\beta}.
\qquad\text{(E1)}
$$

Then $z\equiv1$, $\beta\equiv\sigma/2$, and $\varepsilon\equiv e\pmod p$. Both $z$ and $\varepsilon$ belong to $\mathbb Z_p$, including the nonsplit case.

**Constructive proof of the lift.** Begin with the algebraic point $R_0=(2-\sigma,4-2\sigma)$ over $\mathcal O/p^2$. Usually $[M]R_0$ is close to the identity without being the identity. Write its formal parameter as $s\in p\mathcal O/p^2$. Since the formal group is additive to this precision,

$$
\widetilde R_+=R_0+Q(-s/M),
$$

where $Q(u)$ denotes the formal point with parameter $u$. This kills $[M]\widetilde R_+$ exactly modulo $p^2$. Equivalently, choose $k$ divisible by $p$ with $k\equiv1\pmod M$ and compute $[k]R_0$. The program checks these two constructions against each other.

The normalized local coefficient follows from the chord identity

$$
\mathcal A(P+Q)=\mathcal A(P)+\mathcal A(Q)-\mu(P,Q).
$$

A binary Miller pass accumulates the slopes, doubling the accumulator at doubling steps, and divides the final result by $M$. Identity and vertical chords contribute zero. Within torsion of order prime to $p$, coincident reductions lift to equal points. Therefore a nonvertical chord has a unit denominator; the tangent denominator fails to be a unit only at a point of order two, which is handled as a vertical chord. This proves integrality and the operation count.

To identify the prefactor, use the quartic curve

$$
C:v^2=1-w^4/2,\qquad
x=\frac{2(1-v)}{w^2},\quad y=\frac{4(1-v)}{w^3}.
$$

The lifted points on $C$ are $(z,\beta)$ and $(z,-\beta)$. Their images satisfy $\widetilde R_++\widetilde R_-=T$, and their chord has slope $2/z$. Hence $\mathcal A(\widetilde R_+)+\mathcal A(\widetilde R_-)=2/z$. Formula (E1) is unchanged on swapping the two points. Unramified conjugation swaps them when $\chi=-1$, proving the asserted descent. $\square$

This is a torsion-normalized algebraic coefficient with a $p$-adic lift. An identification with an analytically continued $p$-adic zeta function has not been proved here. The usual elliptic group logarithm vanishes on torsion and is a different object.

## The boundary already has a second digit

Write $p=r^2+s^2$ with $r\equiv1\pmod4$. The published Chowla–Dwork–Evans congruence [S2] gives

$$
a_n\equiv8^{-n}\frac{2^{p-1}+1}{2}
\left(2r-\frac p{2r}\right)\pmod{p^2}.
\qquad\text{(CDE)}
$$

Every denominator is a unit. Given the sum-of-two-squares representation, this takes modular exponentiation and a constant number of arithmetic operations, rather than a factorial product of length $n$. The report uses this known result as a component and makes no novelty claim for it. The theorem was read directly in the published paper of Cosgrave and Dilcher, Theorem 2, where the hypotheses and attribution are explicit. Attempts to retrieve the original 1986 PDF timed out.

## Why the unchanged formulas fail

The torsion point moves under lifting. In particular, its quartic coordinate is $z$, usually different from $1$ modulo $p^2$. Retaining the old prefactor $\sigma(1-\mathcal A)$ therefore need not even produce an element of the base ring.

At $p=13$, in $(\mathbb Z/169\mathbb Z)[\sigma]/(\sigma^2-2)$, exact computation gives

$$
M=180,\quad z=92,\quad \beta=163\sigma,
\quad\mathcal A(\widetilde R_+)=79+150\sigma.
$$

Consequently,

$$
\sigma(1-\mathcal A)=38+91\sigma,
\qquad\varepsilon=25.
$$

Correcting the geometric prefactor restores descent, but not the old evaluation formula. The exact rational sum is $B_3=43/32\equiv70\pmod{169}$ and $a_3\equiv4$. The natural substitution gives

$$
\varepsilon(\chi-a_3)=25(-1-4)\equiv44\ne70\pmod{169}.
$$

Another candidate replaces $a_n$ by the unit root $\alpha$ of $X^2-\tau X+p$, chosen with $\alpha\equiv\tau\pmod p$. Here $\tau=4$ and $\alpha\equiv\tau-p/\tau=43\pmod{169}$. It gives $\varepsilon(\chi-\alpha)\equiv83$, also incorrect.

These are counterexamples to two specified formulas. They place no lower bound on the complexity of other approaches. Both candidates failed at all 342 validation primes; that observation adds evidence about these candidates, not a general impossibility theorem.

## An exact relation with the missing coefficient

Normalize the local expansion at $P_-=(0,-1)$ of the Miller quotient

$$
F=\frac{f_{M,\widetilde R_+}}{f_{M,\widetilde R_-}}
$$

so that $F(P_-)=1$. Its divisor on the quartic is $M(z,\beta)-M(z,-\beta)$. The normalized series is an integral unit,

$$
F(w)\in1+w\mathcal O[[w]].
$$

It has a unique Euler-product factorization

$$
F(w)=\prod_{j\ge1}(1-c_jw^j),\qquad c_j\in\mathcal O.
\qquad\text{(W)}
$$

The coefficients $c_j$ are recursively determined without division. With the standard convention using inverse factors, they are the big Witt coordinates of $F^{-1}$; see [S3]. This convention matters for the sign of the correction.

**Theorem C.** With the definitions above, the following equality holds in the $p$-adic field:

$$
z^{-p}\sum_{k=0}^{n}a_kz^{4k}-(z^{-1}-\varepsilon)a_n
=(M\beta)^{p-1}\varepsilon^p-\frac{pc_p}{M\beta}.
\qquad\text{(W1)}
$$

In particular, put

$$
d=\frac{z-1}{p}\pmod p,\quad
K_p=\frac{c_p}{M\beta}\pmod p,\quad
b=B_n\pmod p,\quad a=a_n\pmod p,
$$

and calculate

$$
\Gamma=(M\beta)^{p-1}\varepsilon^p-\varepsilon a_n\pmod{p^2}.
$$

Then $K_p$ lies in $\mathbb F_p$ and

$$
B_n\equiv\Gamma-p\bigl(K_p+2d(b+a)\bigr)\pmod{p^2}.
\qquad\text{(W2)}
$$

**Proof of the geometric coefficient identity.** Set $\omega=dw/v$ and

$$
\eta=-\frac1{M\beta}\frac{dF}{F},\qquad
\theta_z=\frac{dw}{(z-w)v}.
$$

These last two differentials have the same simple poles and residues. Their difference is holomorphic, and the space of holomorphic differentials on the quartic has dimension one. At $P_-$ one has $t=-w/2$ and $\omega/dw=-1$. The constant coefficient of $F'/F$ there is $M\beta\varepsilon$, by the definition of $\mathcal A$ and the chord relation. It follows that

$$
\theta_z-\eta=(z^{-1}-\varepsilon)\omega.
\qquad\text{(D)}
$$

At $P_-$, write $v=-\sqrt{1-w^4/2}$. The exact expansion

$$
(1-w^4/2)^{-1/2}=\sum_{k\ge0}a_kw^{4k}
$$

and (D) show that the coefficient of $w^{p-1}=w^{4n}$ in $F'/F$ equals

$$
M\beta\left(z^{-p}\sum_{k=0}^{n}a_kz^{4k}
-(z^{-1}-\varepsilon)a_n\right).
$$

**Proof using the Euler product.** Logarithmically differentiating (W) gives

$$
[w^{m-1}]\frac{F'}F=-\sum_{j\mid m}j\,c_j^{m/j}.
$$

For prime $m=p$, only $j=1,p$ occur. Since $c_1=-M\beta\varepsilon$ and $p$ is odd,

$$
[w^{p-1}]\frac{F'}F=(M\beta\varepsilon)^p-pc_p.
$$

Equating the two expressions proves (W1). No characteristic-$p$ identity has been transferred without a correction term.

For (W2), use $z=1+pd$ and $z^{-p}\equiv1\pmod{p^2}$. The elementary identity

$$
\sum_{k=0}^{n}k a_k=\frac12B_n-na_n
$$

follows by summing $4(k+1)a_{k+1}=(2k+1)a_k$. Thus the left side of (W1) is

$$
B_n+\varepsilon a_n+2pd(B_n+a_n)\pmod{p^2},
$$

where $4n=p-1$ has been used only in terms already multiplied by $p$. This proves (W2).

The other terms in (W2) descend to the base ring: $\beta^2=1-z^4/2$ and $p-1$ is even. Since the left side also descends, $K_p$ is a base-field residue. This can alternatively be checked using $F\mapsto F^{-1}$ under the nonsplit conjugation. $\square$

Reducing (W1) modulo $p$ recovers the earlier evaluation: $z\equiv1$, $(M\beta)^{p-1}\equiv\chi$, and $\varepsilon^p\equiv\varepsilon$. This provides an independent derivation of the modulo-$p$ bridge within the lifted construction.

At $p=13$, the local-series computation gives $c_{13}=6\sigma\pmod{13}$, hence $K_{13}=7$, while $d=7$, $b=5$, $a=4$, and $\Gamma=109\pmod{169}$. Therefore

$$
B_3\equiv109-13\bigl(7+2\cdot7\cdot(5+4)\bigr)
\equiv70\pmod{169},
$$

in agreement with the rational sum. The coordinate $c_{13}$ was extracted from the full Miller-function series, without using $B_3$ to define it.

## What the formula does and does not compute quickly

After the elliptic setup, every quantity in (W2) except $K_p$ is computable using a number of arithmetic operations polynomial in $\log p$. Conversely, knowledge of $B_n\pmod{p^2}$ gives

$$
K_p\equiv\frac{\Gamma-B_n}{p}-2d(b+a)\pmod p.
\qquad\text{(R)}
$$

The numerator is divisible by $p$, so division means extracting the second residue digit, not inverting $p$. Equations (W2) and (R) are an explicit reduction in both directions between this particular Witt-coordinate problem and the second digit of the quarter-prefix sum. They do not reduce either problem to arbitrary factorial computation.

The missing residue is already determined by the finite-field Miller function: reducing the Euler factorization commutes with reducing its coefficients. Thus only $F\pmod p$ is needed for $K_p$. The challenge is extracting its degree-$p$ information from the short Miller representation.

The implementation of $c_p$ expands the normalized Miller function through degree $p$. It is deliberately a correctness reference: its elementary series arithmetic costs $O(p^2\log M)$ field operations and $O(p)$ field elements of working memory. It is slower than direct summation. Replacing it with fast power-series arithmetic would still need a cost analysis for coordinate extraction and would not by itself give a logarithmic or sub-square-root algorithm.

There is a precise reason the original local constant cannot provide this coefficient for arbitrary series. For any integral unit series $F$ and any integral $u$, replace $F$ by $F(1+uw^p)$. The constant coefficient of its logarithmic derivative is unchanged, and the entire logarithmic derivative modulo $p$ is unchanged. However, its coefficient of $w^{p-1}$ changes by $pu$, and $c_p$ changes by $-u$. Thus those derivative data alone cannot recover the second digit. This observation concerns arbitrary unit series; the modified function need not have the prescribed Miller divisor. It is not a lower bound for our special family.

**The unresolved lemma is now concrete.** Can $K_p$ for this specified Miller quotient be computed from its short Miller arithmetic circuit, or from the complex multiplication structure, using $p^{o(1)}$ bit operations? The current experiment does not answer that question. A solution would lift the quarter-prefix evaluation to modulo $p^2$. To obtain $U_p(n)$ at that precision, one must also evaluate or cancel the correction $\mathcal H_n-2a_n$ in (Aq).

## Cost and exact validation

The modulo-$p^2$ lift uses a pair of coordinate charts. Near the identity, the parameter $t\in p\mathcal O/p^2$ satisfies $t^2=0$. Addition to an affine point is

$$
(x,y)+Q(t)=\bigl(x+2yt,\ y+(3x^2+2)t\bigr).
$$

When an affine chord reduces to a vertical chord, the program switches to the formal chart instead of attempting to invert a multiple of $p$. All other divisions explicitly check that the denominator is a unit. The source contains the complete formulas and checks the final point against the identity.

| Validation | Discovery cases | Separate validation cases | Outcome |
|:--|--:|--:|:--|
| Torsion lift, descent, boundary and reduction to old results | 10 primes | 342 primes | All passed |
| Full Miller-series extraction and formula (W2) | 10 primes | 22 primes | All passed |
| Unchanged geometric boundary formula | 10 primes | 342 primes | All validation cases failed |
| Simple unit-root replacement | 10 primes | 342 primes | All validation cases failed |

Discovery primes are $13\le p\le97$ with $p\equiv1\pmod4$. The 342 validation primes consist of all such primes from $101$ to $5000$, together with 24 reproducibly selected primes between $100000$ and $150000$. They include 173 nonsplit and 169 split cases. The independent Witt-series validation uses the 22 admissible primes from $101$ to $349$.

The all-$L$ correction and the matrix recurrence below were checked in 6,981 cases covering every odd prime below $400$ and every permitted stopping point. In 292 cases below $70$, a separate exact-rational computation checked the original definition. The lift checks also compare two torsion-projection constructions, the annihilators $M,2M,3M$, and both square-root choices in split cases. The boundary is checked against an exact integer binomial coefficient, and traces below $350$ against direct point counting.

The following timings are medians of seven runs in the same Python process. Both columns compute the local elliptic coefficient with its required setup; they are not timings for a complete modulo-$p^2$ evaluation of $B_n$ or $U_p(n)$.

| Prime size | Modulo $p$ coefficient | Modulo $p^2$ lift | Group operations in lift |
|--:|--:|--:|--:|
| 17 bits | 0.035 ms | 0.206 ms | 73 |
| 30 bits | 0.231 ms | 1.539 ms | 189 |
| 64 bits | 2.088 ms | 14.650 ms | 849 |

The primes are recorded in `results/timings.json`. The code uses deterministic searches for nonresidues during Cornacchia and square-root setup. Their observed cost is included, but no unconditional polynomial-in-$\log p$ bound for those scans is asserted. Random nonresidue sampling gives the usual expected polynomial setup. With the setup supplied, the lift uses $O(\log M)$ ring operations; at precision two, each ring element occupies $O(\log p)$ bits. Inversions must be charged in a bit-operation count.

For the complete sum, the existing benchmark remains a fixed-dimensional polynomial matrix product, not just a linear loop. Indeed, put $D_i=2^ii!$ and $V_i=D_i(t_i,it_i,U_p(i),1)^T$. Then $V_0=(1,0,0,1)^T$ and

$$
V_{i+1}=\begin{pmatrix}
i+h+2&0&0&0\\
h+2&i+h+3&0&0\\
2(h+1)(i+1)&2(i+1)&2(i+1)&0\\
0&0&0&2(i+1)
\end{pmatrix}V_i.
$$

This matrix has degree one in $i$. Bostan–Gaudry–Schost, Theorem 14, applies over $\mathbb Z/p^2\mathbb Z$ with the required small-integer inverses [S4]. For $L\le h$, the interpolation integers, bounded by $2\sqrt L$, are less than $p$, and $D_L$ is a unit. This supplies the usual soft-$O(\sqrt L)$ ring-operation benchmark with soft-$O(\sqrt L)$ stored ring elements. This branch has not improved that bound for the complete modulo-$p^2$ workload.

## Literature interpretation and scope of novelty

Torsion lifting, Miller functions, and the Euler-product description of Witt coordinates are established mathematics. The boundary lift is a published congruence. The contribution of this branch is their explicit assembly for this incomplete binomial block, including the moving-pole normalization, the proved formulas (W1) and (W2), the exact counterexamples, and the reduction (R). I did not locate this particular assembly in the bounded search. Its novelty remains uncertain; no priority claim is made.

Blakestad and Grant's published work defines a $p$-adic sigma function and its logarithmic derivative for good ordinary or multiplicative reduction [S5]. Its power-series domain is the kernel of reduction. Our nontrivial torsion point reduces away from the identity, so substituting it into that series is unjustified. A relation through continuation or normalized differentials may be possible, but it would require a separate theorem.

The unit-root congruences in Beukers and Vlasenko require an invertible Hasse–Witt matrix and concern specified period or coefficient matrices [S6]. They do not identify our incomplete sum with a unit root. The exact failure at $p=13$ illustrates why replacing a coefficient by a unit root without establishing the comparison map is insufficient. The higher-genus cases in our previous branch with zero Hasse–Witt matrix also fail that invertibility hypothesis.

The Euler-product identity for $F'/F$ itself works for a local unit function on any smooth curve. The quarter-point reduction used here additionally relies on a one-dimensional space of holomorphic differentials. A higher-genus application would require its own divisor lift, a vector of holomorphic corrections, and an explicit relation to the desired sum. No higher-genus modulo-$p^2$ speedup is claimed in this branch.

## Reproduction and research decision

Run `python scripts/validate.py` from this report's directory. Python 3.12 and its standard library suffice; no optional mathematics package is required. The recorded run took about 31 seconds. Exact outputs, candidate failures, timings, and the $p=13$ counterexample are in `results/`. The separate `witt_check.py` program constructs the Miller functions as local series, so it does not manufacture the correction by rearranging the desired answer. `SOURCES.md` records what was read, and `LEDGER.md` records the bounded exploration.

This stage stops with a proved lift, a proved higher-modulus correction formula, and a specific computational target. The next substantive advance would be an evaluation of $K_p$ that avoids expanding a degree-$p$ series, together with control of the correction needed for the original rational $U_p(n)$. Until then, the new structure is a research tool rather than a faster higher-modulus summation algorithm.

## References

**S1.** Andrew Snowden, *Elliptic curves over DVRs*, Math 679 lecture 8. See the section on reduction of torsion and its prime-to-$p$ corollary. [Lecture notes](https://public.websites.umich.edu/~asnowden/teaching/2013/679/L08.html).

**S2.** John B. Cosgrave and Karl Dilcher, *Mod $p^3$ analogues of theorems of Gauss and Jacobi on binomial coefficients*, Acta Arithmetica 142 (2010), 103–118. Theorem 2 states the Chowla–Dwork–Evans modulo-$p^2$ congruence used here. [Published paper](https://www.impan.pl/shop/publication/transaction/download/product/83968).

**S3.** Lars Hesselholt, *Lecture notes on Witt vectors*. See the definition of the ghost map and Proposition 14 with Addendum 15 for power series. [Author's notes](https://math.mit.edu/~larsh/papers/s03/wittsurvey.pdf).

**S4.** Alin Bostan, Pierrick Gaudry and Éric Schost, *Linear Recurrences with Polynomial Coefficients and Application to Integer Factorization and Cartier–Manin Operator*, SIAM Journal on Computing 36 (2007), 1777–1806. Theorem 14. [Author-hosted published paper](https://specfun.inria.fr/bostan/publications/BoGaSc07.pdf).

**S5.** Clifford Blakestad and David Grant, *On the universal $p$-adic sigma and Weierstrass zeta functions*, Journal of Number Theory 249 (2023), 348–376. Introduction and the local parameter conventions in Section 2. [Published version](https://euclid.colorado.edu/~grant/publications/P_adic_sigma_function-published); [author manuscript](https://arxiv.org/abs/1903.02480).

**S6.** Frits Beukers and Masha Vlasenko, *Dwork Crystals I*, International Mathematics Research Notices (2021). Definitions of coefficient matrices in the introduction and Theorems 4.3 and 5.3. [Author manuscript](https://arxiv.org/abs/1903.11155).
