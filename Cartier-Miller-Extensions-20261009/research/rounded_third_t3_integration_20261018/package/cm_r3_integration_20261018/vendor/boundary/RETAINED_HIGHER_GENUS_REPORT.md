# Higher genus Miller evaluation of incomplete binomial sums

Research extension for David · 28 September 2026

## What the investigation found

**A concrete higher-genus extension works.** For each genus $g\geq1$, a structured family of hyperelliptic curves gives a fast exact evaluation of $g$ incomplete binomial sums together. The method has been implemented and compared with direct summation and the preceding report’s block-product algorithm. The genus-two implementation evaluated a prefix with about 200 million terms in approximately 6.6 milliseconds, versus 378 milliseconds for that block-product implementation on the same input. These measurements concern a special family of stopping points and primes.

The donut picture describes the topology of a complex curve; a finite-field curve is not literally a surface with holes. The useful intuition is that each extra handle corresponds to another independent holomorphic differential to keep track of. Arithmetic then takes place in the curve’s Jacobian, which packages small collections of points into an addition law. On the curves and primes used here, a matrix that would normally mix the differentials is zero. A short Miller calculation can therefore recover several sums from a few local coefficients.

Higher-genus Miller arithmetic itself is established mathematics. The contribution of this investigation is the explicit connection to these binomial prefixes, its proof, a working implementation, and measured comparisons. The exact application’s novelty remains uncertain. Nothing here supplies a general method for solving arbitrary larger equations.

The result evaluates the incomplete central-binomial block $B_L$. For the original $U_p(L)$, an additional boundary coefficient is required. This report does not establish a fast way to obtain that coefficient at all the new stopping points.

## Definitions and relationship to the earlier report

Throughout, $p$ is an odd prime, $h=(p-1)/2$, and arithmetic is in $\mathbb F_p$ unless an extension is specified. Define

$$
a_k=\binom{2k}{k}8^{-k},\qquad B_L=\sum_{k=0}^{L-1}a_k.
$$

The original sequence is $t_0=1$ and $t_{i+1}=t_i(h+2+i)/(2i+2)$, with $U_p(L)=\sum_{i<L}(h+1+i)t_i$. The preceding report established

$$
t_i=(2i+1)a_i,\qquad U_p(L)=4B_L-2L(2L+5)a_L.
$$

Here the first equality is a congruence, not an equality of the original rational sequences. It follows by comparing ratios and initial terms after substituting $h=-1/2$ in $\mathbb F_p$. For the second, the rational identity

$$
\Delta\bigl[-4k(2k+5)a_k\bigr]
=\bigl((2k+1)^2-8\bigr)a_k
$$

telescopes, and $U_p(L)=\tfrac12\sum_{k<L}(2k+1)^2a_k$. These are baseline results. The full evaluation $U_p(h)=4(2/p)$ is also a baseline. The exact earlier report and its input algorithms are preserved in the accompanying archive.

The prior genus-one investigation had an ordinary elliptic family at quarter points, and a supersingular family for $B_{(p+1)/3}$ when $p\equiv-1\pmod3$. The theorem below extends the latter mechanism. It does not automatically extend the quarter-point boundary evaluation.

## The family in every genus

**Theorem HG.** Let $d=2g+1\geq3$ be odd, and let $p$ be an odd prime satisfying $p\equiv-1\pmod d$. Put $L=(p+1)/d$. On the smooth projective curve

$$
C_d:\quad y^2=1-\frac{x^d}{2},
$$

let $P_0=(0,1)$ and let $\infty$ be the unique point at infinity. Work in $K=\mathbb F_{p^2}$, choose $\sigma^2=2$, and set

$$
Q=(1,\sigma/2),\qquad M=p+1,\qquad \chi=\left(\frac2p\right).
$$

There is a rational function $f$ with $\operatorname{div}(f)=M(Q)-M(\infty)$. At $P_0$, use $x$ as local parameter and the branch $y(0)=1$. Define

$$
A_r=\frac1M[x^r]\frac{f'(x)}{f(x)},\qquad 0\leq r<g.
$$

Then

$$
\boxed{B_{jL}=-\chi\sigma\bigl(1+2A_{j-1}\bigr),\qquad 1\leq j\leq g.}
$$

The derivative is the derivative of the local expansion along the curve. The answer lies in $\mathbb F_p$ and is independent of the choice of square root. All $g$ coefficients can be obtained in one Cantor–Miller pass. An elementary implementation has a conservative bound of $O(g^3\log p)$ field operations and $O(g)$ working field elements, with field inversions included as operations. This includes the family-specific setup and requires no point-counting oracle.

The assumptions imply $p\geq2d-1$, so $p>d$, the curve is smooth, and every listed index $jL$ lies in $[1,h]$. For each fixed $g$, the residue class contains infinitely many primes. Composite odd $d$ is allowed.

| Genus | Curve degree $d$ | Required prime class | Prefixes obtained together |
|---|---:|---|---|
| 1 | 3 | $p\equiv2\pmod3$ | $B_{(p+1)/3}$ |
| 2 | 5 | $p\equiv4\pmod5$ | $B_{(p+1)/5}$ and $B_{2(p+1)/5}$ |
| 3 | 7 | $p\equiv6\pmod7$ | $B_{j(p+1)/7}$ for $1\leq j\leq3$ |
| 4 | 9 | $p\equiv8\pmod9$ | $B_{j(p+1)/9}$ for $1\leq j\leq4$ |
| $g$ | $2g+1$ | $p\equiv-1\pmod{2g+1}$ | $B_{j(p+1)/(2g+1)}$ for $1\leq j\leq g$ |

## Proof of the higher genus theorem

### A known annihilator replaces point counting

Since $d$ is odd and divides $p+1$, $\gcd(d,p-1)=1$. Hence there is $c\in\mathbb F_p$ with $c^d=2$. The Hermitian curve

$$
H:\quad U^{p+1}+V^{p+1}=1
$$

maps to $C_d$ over $\mathbb F_{p^2}$ by

$$
x=cU^{(p+1)/d},\qquad y=V^{(p+1)/2}.
$$

This is a nonconstant separable map, extending to the smooth projective models. The Hermitian curve has $p^3+1$ rational points and genus $p(p-1)/2$, so it is maximal over $\mathbb F_{p^2}$. The cohomology of a curve covered by it injects into the covering curve’s cohomology. Consequently, all Frobenius eigenvalues of $C_d$ over $\mathbb F_{p^2}$ are $-p$, and $C_d$ is maximal as well.

For a maximal curve, Frobenius acts on its Jacobian as multiplication by $-p$. Equivalently, its fundamental divisor equivalence gives

$$
p(P)+\operatorname{Fr}_{p^2}(P)\sim(p+1)(\infty).
$$

For $P$ rational over $\mathbb F_{p^2}$ this becomes $(p+1)(P-\infty)\sim0$. This standard implication is stated explicitly in Korchmáros–Torres, Introduction, equation (1.2) [R4]. In particular, $M=p+1$ kills the class of $Q-\infty$, proving the existence of $f$. Also $M\equiv1\pmod p$, so its inverse is legitimate. Computing $c$ or constructing the covering map is needed only for the proof, not for the evaluator.

### A differential encodes the incomplete sums

Write $f_0(x)=1-x^d/2$ and use the holomorphic basis

$$
\omega_i=x^{i-1}\frac{dx}{y},\qquad 1\leq i\leq g.
$$

Consider

$$
\theta=\frac{dx}{(1-x)y}.
$$

It has simple poles at $Q_+=(1,\sigma/2)$ and $Q_-=(1,-\sigma/2)$, with residues $-\sigma$ and $\sigma$, respectively. It has no other poles. Since $\operatorname{div}(x-1)=(Q_+)+(Q_-)-2(\infty)$, the function

$$
F=\frac{f^2}{(x-1)^M}
$$

has divisor $M(Q_+)-M(Q_-)$. Define the logarithmic differential

$$
\eta=-\frac{\sigma}{M}\frac{dF}{F}.
$$

Its residues equal those of $\theta$, so $\theta-\eta$ is holomorphic. The differential $\eta$ is defined over $\mathbb F_p$: Frobenius either fixes both $Q_\pm$ and $\sigma$, or swaps the two points and negates $\sigma$; the signs cancel in $\eta$. Constants multiplying $F$ do not affect $dF/F$.

For the Cartier operator $\mathcal C$, logarithmic differentials satisfy $\mathcal C(dF/F)=dF/F$, and constants are taken to their $p$th roots [R2]. Therefore

$$
\mathcal C(\eta)=\chi\eta.
$$

### The Cartier matrix vanishes

We use the column convention

$$
\mathcal C(\omega_j)=\sum_{i=1}^gH_{ij}\omega_i,
\qquad H_{ij}=[x^{pi-j}]f_0(x)^h.
$$

The coefficients are in $\mathbb F_p$, so taking their $p$th roots changes nothing. Specifying this convention avoids the transpose and semilinearity ambiguity discussed by Achter–Howe [R3]. The polynomial $f_0^h$ has nonzero coefficients only at multiples of $d$. But

$$
pi-j\equiv-i-j\pmod d,\qquad 2\leq i+j\leq2g=d-1.
$$

No relevant exponent is divisible by $d$. Thus $H=0$, and $\mathcal C(\theta)=\chi\eta$.

On the other hand,

$$
f_0(x)^h=\sum_{k=0}^h a_kx^{dk},
$$

because $\binom hk(-1/2)^k=a_k$ modulo $p$. Applying Cartier to the expansion

$$
\theta=\frac1{y^p}\frac{f_0(x)^h}{1-x}\,dx
$$

shows that the coefficient of $x^{i-1}$ in $\mathcal C(\theta)/(dx/y)$ is

$$
B_{\lfloor(ip-1)/d\rfloor+1}=B_{iL},\qquad 1\leq i\leq g.
$$

The displayed range is essential: $p=dL-1$ and $i+1<d$ make the floor simplify exactly.

### Local coefficients complete the extraction

At $P_0$, $f$ is a unit and $y=1+O(x^d)$. Hence

$$
\frac{\eta}{dx/y}
=-\sigma y\left(\frac2M\frac{f'}f-\frac1{x-1}\right).
$$

For degrees below $g$, the factor $y$ is $1$, and every coefficient of $-1/(x-1)=1/(1-x)$ is $1$. Thus the relevant coefficient is $-\sigma(2A_{i-1}+1)$. Comparing with $\mathcal C(\theta)=\chi\eta$ proves Theorem HG. Every division used here is by a nonzero field element; no division by $p$ or reduction of a singular classical hypergeometric parameter is involved.

## Other binomial weights

The same proof establishes a broader result. Let $\lambda\in\mathbb F_p$, with $\lambda\ne0,1$, and define

$$
B_L^{(\lambda)}=\sum_{k=0}^{L-1}\binom hk(-\lambda)^k
=\sum_{k=0}^{L-1}\binom{2k}{k}\left(\frac\lambda4\right)^k.
$$

Replace the curve by $y^2=1-\lambda x^d$, put $v^2=1-\lambda$, and use $Q=(1,v)$. Define $A_r$ from the Miller function as before, and let $\chi_\lambda=((1-\lambda)/p)$. Then

$$
\boxed{B_{jL}^{(\lambda)}=-\frac{\chi_\lambda}{v}\bigl(1+2A_{j-1}\bigr),\qquad1\leq j\leq g.}
$$

To check the extension, choose $c^d=\lambda^{-1}$ in the Hermitian covering argument. The support of $f_0^h$ is still in multiples of $d$, so the Cartier matrix still vanishes. The residue factor becomes $-1/v$, and Frobenius takes $v$ to $\chi_\lambda v$. These are the only changes in the proof. The restrictions exclude a degenerate curve and collision of the two poles. An additional implementation tested every permitted weight for admissible primes below 150 and $d\in\{3,5,7,9,11\}$: 2,853 parameter triples and 6,324 prefixes, all agreeing with direct integer binomials. This is exhaustive small-case evidence, not a separate large-prime validation. The timing tables below concern only $\lambda=1/2$.

This is a concrete application beyond the original appearance of the sum. It evaluates a family of incomplete binomial polynomials at many arguments, with the same stopping-point restrictions.

## What happens outside the special prime class

The general identity exposes exactly what the zero matrix removed. Assume $p>d$, retain $C_d$, and suppose the divisor class $(Q_+)-(Q_-)$ has order prime to $p$. Choose a prime-to-$p$ annihilator $N$ and a function with divisor $N(Q_+)-N(Q_-)$, and define $\eta=-\sigma\,dF/(NF)$ as above. Set

$$
e_i=[x^{i-1}]\frac{\eta}{dx/y},\qquad
b_i=B_{\lfloor(ip-1)/d\rfloor+1},\qquad1\leq i\leq g.
$$

With $\mathbf1$ the vector of ones and the same Cartier matrix convention,

$$
\boxed{\mathbf b=\chi\mathbf e+H(\mathbf1-\mathbf e).}
$$

Indeed, $\theta-\eta$ is holomorphic and its coordinates in the chosen basis are $\mathbf1-\mathbf e$. Apply Cartier and take the first $g$ local coefficients. All these coordinates are in $\mathbb F_p$, making the displayed ordinary matrix multiplication valid.

For $p\equiv1\pmod d$, $H$ is diagonal, with $H_{ii}=a_{i(p-1)/d}$. Writing $n_i=i(p-1)/d$ and subtracting $a_{n_i}$ from $B_{n_i+1}$ gives

$$
B_{n_i}=e_i\bigl(\chi-a_{n_i}\bigr).
$$

This is a proved structural formula under the stated torsion hypothesis. It is not a fast algorithm unless the annihilator, its prime-to-$p$ suitability, the coefficients of $H$, and the needed local data can all be supplied cheaply. Counting points on the Jacobian can dominate the work. Pila’s polynomial-time theorem applies with fixed defining data and has constants and exponents depending on those data [R5]; it is not a practical cost guarantee uniform in genus.

The shortcut $M=p+1$ genuinely fails outside its scope. For the same degree-five curve and $p=7,11,13$, the executable Jacobian calculation finds that $p+1$ does not annihilate $Q-\infty$. This falsifies reuse of that particular Miller length at those inputs. It does not exclude a different annihilator or another useful identity.

## How the implementation avoids a huge rational function

For genus greater than one, points on the curve do not themselves carry the elliptic addition law. The computation uses reduced degree-zero divisor classes in the Jacobian. A class has a Mumford representation $(u,v)$, where $u$ is monic, $\deg u\leq g$, $\deg v<\deg u$, and $u$ divides $f_0-v^2$. Cantor arithmetic adds such classes using polynomial greatest common divisors and reductions [R1].

The Miller invariant is

$$
\operatorname{div}(f_k)=k(Q-\infty)-D_k,
$$

where $D_k$ represents $k(Q-\infty)$. A binary chain for $M$ has $O(\log M)$ additions and doublings. If a Cantor step supplies a correction function $G$ with divisor $D_a+D_b-D_{a+b}$, then $f_{a+b}=f_af_bG$ up to a constant. Taking logarithmic derivatives turns products into additions.

The implementation therefore keeps only the first $g$ regular coefficients of $d\log f_k$ at $P_0$. A doubling replaces the stored vector by twice itself plus the correction vector. No polynomial of degree comparable to $p$ is constructed.

The correction factors are important. In Cantor composition, the common divisor polynomial contributes its logarithmic derivative. In each reduction from $(u,v)$ to $(u',v')$, the function factor is $(y-v)/u'$. Omitting either factor would corrupt the prefix value. The code implements these divisor identities from the standard algorithm, rather than treating a Jacobian addition routine as sufficient by itself.

An intermediate correction may vanish or have a pole at $P_0$. For $z=x^m(c_0+c_1x+\cdots)$, with $c_0\ne0$, we retain the integer valuation $m$ separately and expand the logarithmic derivative of its unit part. The missing term is exactly $m/x$, so it contributes no regular coefficient. The final valuation is checked to be zero. This handles actual zero and pole cases in the validation sample.

The degree bound also controls how much series information is needed. During composition, $\deg v\leq2g-1$, so $\deg(f_0-v^2)\leq\max(d,4g-2)$. Since $(y-v)(y+v)=f_0-v^2$, a local zero of $y-v$ has at most that order. A series precision of $\max(d,4g-2)+g+2$ is consequently sufficient for all required regular coefficients. The series for $y$ is obtained from $y^2=f_0$ using division by $2$, so there is no hidden factorial denominator when the precision reaches the characteristic.

Square-root selection does not conceal an expensive search. The code starts in $\mathbb F_p[s]/(s^2-2)$. If this is a field, ordinary arithmetic proceeds. If a nonzero zero divisor is encountered when $2$ is a square, that divisor yields a square root in $\mathbb F_p$; the calculation restarts once in that component. Conjugating the root leaves the result unchanged. The general-weight implementation uses $s^2=1-\lambda$ in exactly the same way.

## Cost as the genus grows

Using classical polynomial arithmetic, a conservative bound for one full Cantor step with the local coefficients is $O(g^3)$ field operations. There are $O(g)$ reductions, each involving polynomials and series of length $O(g)$; composition by extended gcd also fits within this bound. The binary chain has $O(\log p)$ steps because the proven annihilator is $p+1$. This gives $O(g^3\log p)$ operations for all $g$ prefixes, with $O(g)$ working field elements. The stored answer has $g$ elements as well. The bound is deliberately loose and is not a claim that optimized Cantor arithmetic requires cubic time.

For fixed genus, this is logarithmic in $p$ in a field-operation model. With elementary modular arithmetic and inversions, the conservative bit bound is $O(g^3(\log p)^3)$. A field operation and a bit operation are not interchangeable. These are single-query bounds, with no stored preprocessing over many primes.

The relevant existing comparison is a polynomial matrix-product method, with softly $O(\sqrt L)$ field complexity for this fixed-dimensional recurrence [R6]. The prior report includes a FLINT block-product implementation of that approach. It is not a fully optimized implementation of every Bostan–Gaudry–Schost refinement, so the measured ratios below describe the supplied implementations. The exponent comparison for fixed $g$ follows independently from the proof.

As genus increases, divisor arithmetic becomes more expensive while the first prefix length $L=(p+1)/(2g+1)$ becomes shorter. Both effects reduce the advantage. There is no justification for increasing genus indefinitely. Moreover, the comparison with an elliptic method at another stopping point is not a comparison of algorithms solving the same query.

## Exact validation and measured comparisons

The principal small-prime test checked every admissible pair with $p\leq2000$ and $d=3,5,\ldots,19$. It covered 452 pairs and 1,491 prefixes. A separate seeded validation sample used 24 pairs with primes between 20,000 and one million and genus up to 15, giving another 174 prefixes. Every result agreed with direct summation. All 24 fresh first prefixes were also checked against the independent block-product code.

Additional checks included 93 evaluations using exact integer binomial coefficients, 153 cross-checks against the preceding elliptic third-point code, 24 comparisons of binary and linear Miller chains with several annihilator multiples, and six direct point counts over $\mathbb F_{p^2}$ confirming maximality. The exhaustive small range encountered eight square-root component restarts and eight cases containing intermediate local zeros or poles. Discovery examples are recorded separately from the fresh validation sample. The counts are evidence supporting the implementation; the proof establishes the theorem.

| $p$ | Genus | First index $L$ | Prefix values $B_L,B_{2L},\ldots$ |
|---:|---:|---:|---|
| 19 | 2 | 4 | $14,16$ |
| 29 | 2 | 6 | $22,17$ |
| 41 | 3 | 6 | $9,28,18$ |
| 17 | 4 | 2 | $14,14,6,0$ |
| 43 | 5 | 4 | $38,26,18,13,40$ |

The following timings are medians of five runs on the same machine. Inputs, raw samples, environment, outputs, and operation counts are in `results/benchmarks.json`. Every first prefix in the benchmark was independently checked by both the C direct loop and the block-product code. The Miller times include constructing the curve arithmetic and local series; prime selection is outside all timed algorithms. No peak-memory measurement was made.

| $p$ for genus two | First prefix Miller ms | Both prefixes Miller ms | First prefix block product ms | Block product divided by first Miller |
|---:|---:|---:|---:|---:|
| 100,019 | 3.52 | 3.37 | 2.24 | 0.64 |
| 1,000,039 | 4.92 | 4.45 | 9.01 | 1.83 |
| 10,000,019 | 5.93 | 5.71 | 22.30 | 3.76 |
| 100,000,039 | 6.35 | 6.12 | 93.64 | 14.75 |
| 1,000,000,009 | 6.57 | 8.45 | 377.90 | 57.50 |

At the largest input in this table, $L=200{,}000{,}002$ and $B_L=264{,}371{,}186$. The small-prime result is useful too: the block-product implementation wins there. Small differences between the first-prefix and all-prefix medians reflect execution variability and are not evidence that requesting more coefficients is cheaper.

The optimized C direct loop is also competitive at small sizes. Its single reference-run times were 0.113 ms at $p=100{,}019$, 1.58 ms at $p=1{,}000{,}039$, 12.57 ms at $p=10{,}000{,}019$, and 1.50 seconds at $p=1{,}000{,}000{,}009$. Those single runs were correctness references, not five-run timing medians. They reinforce the need to choose methods by workload rather than asymptotics alone.

For a genus comparison, the same prime $p=1{,}000{,}206{,}899$ admits all the degrees below. The first-prefix indices differ with genus, as the theorem requires.

| Genus | Degree | First prefix Miller ms | All prefixes Miller ms | First prefix block product ms | Ratio for first prefix |
|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 4.14 | 5.09 | 526.77 | 127.35 |
| 2 | 5 | 7.35 | 7.22 | 361.86 | 49.22 |
| 3 | 7 | 11.23 | 16.17 | 306.14 | 27.26 |
| 4 | 9 | 18.66 | 19.90 | 275.14 | 14.74 |
| 5 | 11 | 24.94 | 33.14 | 259.34 | 10.40 |

The genus-one row uses the generic Cantor implementation, not the optimized elliptic code from the earlier report. The block-product routine also returns $a_L$ as part of its state, whereas this Miller evaluator returns prefixes only. The measurements establish a practical benefit on the tested inputs; they do not locate a universal crossover or establish a fitted genus exponent.

## What remains unresolved

The immediate unresolved quantity for the original problem is the boundary coefficient. At these new indices,

$$
U_p(jL)=4B_{jL}-2jL(2jL+5)a_{jL}.
$$

The theorem makes the first term cheap. Computing the second term by a general factorial or product algorithm may still dominate the total. A useful next target is an explicit, fully costed boundary evaluation at fifth or seventh points. Merely renaming the coefficient as a Jacobi sum would not settle its computational cost.

For less symmetric curves, the matrix identity gives a second precise research problem: find families where both the required divisor annihilator and the action of Cartier can be computed cheaply. A nonzero matrix by itself is not an obstruction, but its entries and the torsion data are real inputs to the computation. The failed $p+1$ tests show why the existing shortcut cannot simply be reused.

The result offers no uniform algorithm for arbitrary $L$ and no transfer to factoring, Wilson quotients, or a base-10 BBP formula. The earlier factorial reduction remains compatible with fast evaluation on these restricted families. A square-root benchmark is not a proved lower bound. The surrounding digit-extraction workload has not been audited here, so no overall improvement to that workload is claimed.

## Literature and novelty

Hyperelliptic divisor arithmetic, Miller functions, maximal-curve annihilators, and Cartier matrices are established tools. This report’s theorem and general-weight corollary are deductions combining those tools with the incomplete-binomial coefficient extraction. The implementations, exact checks, and timing measurements were made in this investigation. They have not undergone external peer review.

The literature search checked the sources below directly and used targeted searches for hyperelliptic Miller computations, Cartier–Manin matrices, maximal-curve fundamental equivalences, and incomplete central-binomial sums. No exact statement of Theorem HG was identified in that bounded search. This supports describing its novelty as uncertain; it does not establish priority. The earlier report’s bibliography is preserved with the inputs rather than silently replaced.

**R1.** Steven D. Galbraith, Florian Hess and Frederik Vercauteren, *Hyperelliptic pairings*, Pairing 2007, LNCS 4575, pp. 108–131. Published conference paper; consulted author PDF, divisor representations and Algorithm 1, together with the Miller discussion. [Author PDF](https://www.math.auckland.ac.nz/~sgal018/Pairing2007-survey.pdf).

**R2.** Alain Couvreur, *Codes and the Cartier operator*, Proceedings of the American Mathematical Society 142 (2014), pp. 1983–1996. Published paper; consulted author manuscript, Definition 3.1 and Propositions 3.2–3.3. [Author manuscript](https://arxiv.org/pdf/1206.4728).

**R3.** Jeffrey D. Achter and Everett W. Howe, *Hasse–Witt and Cartier–Manin matrices: a warning and a request*, Contemporary Mathematics 722 (2019), pp. 1–18. Published chapter; consulted matrix derivation and convention discussion. [Author PDF](https://www.math.colostate.edu/~achter/math/hwcm1017.pdf).

**R4.** Gábor Korchmáros and Fernando Torres, *Embedding of a maximal curve in a Hermitian variety*, Compositio Mathematica 128 (2001), pp. 95–113. Published paper; consulted author manuscript, Introduction and fundamental equivalence (1.2). [Author manuscript](https://arxiv.org/pdf/math/9911043), [publisher record](https://doi.org/10.1023/A:1017553432375).

**R5.** Jonathan Pila, *Frobenius maps of abelian varieties and finding roots of unity in finite fields*, Mathematics of Computation 55 (1990), pp. 745–763. Published paper; consulted Theorems A and B and their defining-data hypotheses. [Author PDF](https://people.maths.ox.ac.uk/pila/Frobenius.pdf).

**R6.** Alin Bostan, Pierrick Gaudry and Éric Schost, *Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator*, SIAM Journal on Computing 36 (2007), pp. 1777–1806. Published paper; recurrence-product benchmark inherited from the verified earlier report. [Author PDF](https://specfun.inria.fr/bostan/publications/BoGaSc07.pdf).

The archive contains the source notes, research ledger, exact algorithms, independent reference implementations, machine-readable results, reproduction instructions, and preserved prior report. The accompanying Word version uses native equations; this Markdown version uses Obsidian-compatible dollar-delimited mathematics.
