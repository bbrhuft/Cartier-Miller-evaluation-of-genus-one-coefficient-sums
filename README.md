# Cartier–Miller evaluation of genus-one coefficient sums

A research manuscript and computational project is shared for independent mathematical review and possible collaboration.

**Current version (draft of 24 October 2026):** [`Cartier_Miller_Paper_Rewrite_Corrected_20261024.pdf`](Cartier_Miller_Paper_Rewrite_Corrected_20261024.pdf), a shortened 17-page rewrite. It adds Section 6.3, closed forms for sums whose twist point is torsion (see [below](#torsion-closed-forms-section-63)). Its LaTeX source, verification script and saved output are in [`Cartier-Miller-Verification-20261022/`](Cartier-Miller-Verification-20261022/). The pre-registered search that led to Section 6.3, with its code and complete run records, is in [`Cartier-Miller-Congruence-Search-20261024/`](Cartier-Miller-Congruence-Search-20261024/). The draft supersedes the 22 October rewrite (same filename stem, previously dated `_20261022`), `Cartier_Miller_Paper_Revised_20261022.pdf` and the earlier dated PDFs, which are kept for the record. Boundary methods and benchmark protocols are in [`Cartier_Miller_Computational_Companion_20261022.pdf`](Cartier_Miller_Computational_Companion_20261022.pdf).

Let $p\ge5$ be prime and $f\in\mathbb F_p[x]$ a squarefree cubic or quartic. Building on the differentiated Miller chains of Semaev and Rück, the paper shows that, once the trace of Frobenius of $v^2=f(x)$ is known, one chain of $O(\log p)$ field operations on a quadratic twist evaluates the truncation $T_f=f^{(p-1)/2}\bmod x^p$ at any $\mu\in\mathbb F_p^\times$ with $f(\mu)\ne0$, and the reciprocal character sum $\sum_{x\ne a}\chi(f(x))/(x-a)\in\mathbb F_p$ at any $a$ with $f(a)\ne0$. Combined with Schoof's algorithm this gives deterministic polynomial time in $\log p$.

The construction combines established ingredients: the Cartier operator and characteristic-$p$ descent, differentiated Miller recurrences (Semaev; Rück), and elliptic-curve point counting. The proposed contribution is specific: the curve-order identity (Theorem A), the twist evaluator (Theorem B), the normalization of the residue-divisor identity at the exceptional traces (Theorem D), and their binomial consequences. Whether these are new or already implicit in the literature remains for specialist assessment.

**Status:** This is an unrefereed research draft created with substantial generative-AI assistance. Numerical checks support the formulas, but do not replace independent review of the proofs.

## What the evaluation does

Put $h=(p-1)/2$ and write

$$
F=f^{h}=T_f+x^pJ_f,\qquad \deg T_f<p .
$$

$T_f$ is the *truncation* and $J_f$ the *high block*. For $a\in\mathbb F_p$, with $\chi$ the quadratic character,

$$
T_f(a)=\chi(f(a))-aJ_f(a),\qquad
C_f(a):=\sum_{x\ne a}\frac{\chi(f(x))}{x-a}=-F'(a)-J_f(a)\quad\text{in }\mathbb F_p .
$$

For $a\ne0$ the three values $T_f(a)$, $J_f(a)$ and $C_f(a)$ determine one another with $O(\log p)$ field operations. At $a=0$ the identities still hold, but $T_f(0)=\chi(f(0))$ carries no information about $J_f(0)$; there only $J_f(0)$ and $C_f(0)$ are equivalent. The character-sum evaluator covers $a=0$ whenever $f(0)\ne0$.

For $f(0)=1$ and $\lambda=1/\mu$, the value $T_f(\mu)$ is also the coefficient

$$
S_f(\lambda)=[w^{p-1}]\frac{f(w)^h}{1-\lambda w}=T_f(1/\lambda).
$$

The cutoff is fixed at degree below $p$; the evaluation point varies. This is not a general algorithm for arbitrary stopping indices in central-binomial sums.

## The curve-order identity and the evaluator

On a short model $E:y^2=W(x)=x^3+Ax+B$ over $\mathbb F_p$, let $f_{m,P}$ be a Miller function with divisor $m(P)-([m]P)-(m-1)(O)$, and let $\alpha_m(P)=[t^0]\,d\log f_{m,P}/dt$ be the constant Laurent coefficient of its logarithmic derivative at $O$, with $t=-x/y$. The differentiated Miller chain computes $\alpha_m(P)$ in $O(\log m)$ field operations.

**Theorem A (curve-order identity).** Let $N=\\#E(\mathbb F_p)$ and write $W^h=U+H_Ex^{p-1}+x^pJ_W$ with $\deg U\le p-2$. For every affine point $P=(a,b)\in E(\mathbb F_p)$,

$$
\alpha_N(P)=b\,J_W(a).
$$

No hypothesis on $N$ is needed: $N$ may be divisible by $p$, and $E$ may be supersingular.

**Theorem B (evaluation at a nonbranch point).** Let $f(a)\ne0$, $\varepsilon=\chi(f(a))$, $\tau_f$ the trace of the projective curve $v^2=f(x)$, and $N=p+1-\varepsilon\tau_f$. Normalizing at $a$ gives an explicit short model $E_a$ of $v^2=f(a+z)/f(a)$, with $\\#E_a(\mathbb F_p)=N$, and an explicit rational point $R$. With $g_1=f'(a)/f(a)$,

$$
C_f(a)=\varepsilon\Big(-\frac{g_1}{4}(N-2)-\frac{\alpha_N(R)}{2}\Big),
\qquad
T_f(a)=\varepsilon\Big(1-\frac{aNg_1}{4}-\frac{a}{2}\alpha_N(R)\Big)\quad(a\ne0).
$$

This is one base-field chain. It needs no square root, no quadratic algebra and no exceptional-trace case distinction, and it holds for $p\ge5$ and any constant term.

## The residue-divisor identity and the exceptional case

Theorem D explains where the evaluator comes from. Assume $p\ge7$ and $f(0)=1$, take $E:v^2=f(w)$ with origin $(0,1)$ and $\omega=dw/v$, and write $\tau:=\tau_f$ and $H=[w^{p-1}]f^h\equiv\tau\pmod p$. For $\lambda\ne0$ with $f(1/\lambda)\ne0$, choose $v_0^2=f(1/\lambda)$, let $\varepsilon=\chi(f(1/\lambda))$, and set $\mathfrak D=(1/\lambda,v_0)-(1/\lambda,-v_0)$. Then

$$
S_f(\lambda)=H-\varepsilon\,r\,\Psi_{M_\varepsilon}(\mathfrak D),
\qquad
r=\frac{1}{\lambda v_0},
\qquad
M_\varepsilon=p+1-\varepsilon\tau .
$$

Here $\Psi_M$ is the logarithmic derivative, relative to $dw/v$ at the origin, of a function with divisor $M\mathfrak D$. When $\tau=\varepsilon$ the annihilator is $M_\varepsilon=p$, and the identity needs a separate normalization. The paper proves it directly in characteristic $p$ (Lemma 5.2, proof in Appendix B), with exact examples in Table 1. The characteristic-$p$ additive transfer itself is established mathematics, associated with Serre, Semaev, Rück and Voloch.

Remark B.1 compares the sign with the quasi-period formula printed in Voloch (1997, Section 3). The paper's sign is fixed by its own divisor calculation and confirmed on the exact examples. Whether the printed sign reflects a convention not matched here or a misprint is left open.

## Complexity

With the exact trace supplied, each nonbranch query uses $O(\log p)$ field operations, including $O(\log p)$ inversions, and a constant number of registers: $O((\log p)^3)$ bit operations with schoolbook arithmetic. The trace is computed once per curve and prime, and every pole reuses it through the sign $\varepsilon$. Schoof's deterministic point count makes the whole computation deterministic polynomial time in $\log p$. In practice the trace can come from SEA or PARI/GP's `ellap`. A trace-free $\tilde O(\sqrt p)$ route, which also covers branch poles, follows from Bostan–Gaudry–Schost and Harvey interval products (Remark 4.5).

For constant-plus-simple-pole weights over a complete excluded set (Theorem 4.4), the identities hold for any excluded set. The $O(s\log p+s^2)$ bound requires $r_i\ne0\Rightarrow f(a_i)\ne0$; excluded branch points with zero residue remain allowed.

## Worked application: the original quarter-point sum

For $p=4n+1\geq13$, define

$$
a_i=\binom{2i}{i}8^{-i},
\qquad
B_n=\sum_{i=0}^{n-1}a_i.
$$

Choosing $f(w)=1-w^4/2$ gives $T_f(1)=B_n+a_n$. The corresponding elliptic curve has $j=1728$, and its trace supplies the boundary coefficient $a_n$. The original weighted sum is recovered through

$$
U_p(n)\equiv4B_n+\frac94a_n\pmod p.
$$

The trace is the representative of $a_n\equiv2u\,8^{-n}$ in $(-p/2,p/2)$, where $p=u^2+s^2$ with $u\equiv1\pmod4$ (Gauss's congruence), so both the prefix and the boundary are available in polynomial time. At $p=97$, the example gives $n=24$, $\tau_f=-18$, $B_n=33$, $a_n=79$ and $U_p(n)=43$ (Section 6.2 of the paper).

## Worked application: the original third-point sum

The same machinery handles a second stopping family, which is not written up in the current paper; the numbers below were rechecked against direct summation on 22 October 2026. For $p=3L+1\geq7$, with the same $a_i$, define

$$
B_L=\sum_{i=0}^{L-1}a_i,\qquad L=\frac{p-1}{3}.
$$

Choosing $f(w)=1-w^3/2$ gives $T_f(1)=B_L+a_L$, since $f^{(p-1)/2}$ contains only powers $w^{3i}$ with coefficient $a_i$. The corresponding elliptic curve now has $j=0$ rather than $j=1728$, and again its trace supplies the boundary coefficient: $a_L\equiv H\equiv\tau\pmod p$. The boundary is classical complex-multiplication data. Writing $4p=r^2+27s^2$ with $r\equiv1\pmod 3$, Jacobi's congruence and $8^L=2^{p-1}\equiv1$ give

$$
a_L\equiv\binom{2L}{L}\equiv-r\pmod p,
$$

so the trace is $-r$, obtained from Cornacchia's algorithm without point counting. Since $L\equiv-1/3\pmod p$, the original weighted sum is recovered through

$$
U_p(L)\equiv4B_L+\frac{26}{9}a_L\pmod p.
$$

At $p=97$, the example gives $L=32$ and $4\cdot97=19^2+27\cdot1^2$, so $r=19$, the trace is $-19$ and $a_L=78$. Cartier–Miller evaluates $T_f(1)=4$, giving $B_L=23$ and $U_p(L)=91$. All four values agree with direct summation and with a point count on $v^2=1-w^3/2$.

The two examples use different curves ($j=1728$ and $j=0$), different CM fields ($\mathbb Q(i)$ and $\mathbb{Q}(\sqrt{-3})$ and different stopping indices. The same evaluation theorem serves both. The third-point family also exercises the exceptional case: at $p=61$, $4\cdot61=1^2+27\cdot3^2$ gives trace $-1$, which equals the character of $f(1)=1/2$, so the annihilator is $M_\varepsilon=p$ and the exceptional normalization (Lemma 5.2) is required. The twist evaluator of Theorem B needs no special treatment there.

## The rounded third point (Corollary E)

For $p\equiv2\pmod3$ the index $(p-1)/3$ is not an integer. Put $L=(p+1)/3$ and $m=L-1=(p-2)/3$. The curve $v^2=1-w^3/2$ is then supersingular, with trace $0$, so no point counting is needed, and Corollary E of the paper shows:

- $B_L=\sum_{k=0}^{m}\binom{2k}{k}8^{-k}\bmod p$ is computable deterministically in $O(\log p)$ field operations;
- the next term is $a_L=3/(2\,m!^3)$, with $m!=(3/(2a_L))^{(2p-1)/3}$, so computing the next partial sum $B_{L+1}=B_L+a_L$ is equivalent, up to $O(\log p)$ operations, to computing $((p-2)/3)!\bmod p$.

The reduction runs in both directions; it proves no lower bound and no complexity separation. No polynomial-time algorithm for $((p-2)/3)!\bmod p$ is known to us. Classical methods take $\tilde O(\sqrt p)$ operations. Tal (2026, ECCC TR26-211) goes below the square-root exponent by Jacobi-sum reconstruction when $p-1$, or another cyclotomic value, has a divisor in a suitable range. The companion and the extensions folder describe exact boundary methods. These include a certified Jacobi-sum backend that, at the nine primes where it was selected, made complete evaluation 1.67–6.52× faster than a native factorial, with cost still of square-root type for a fixed conductor.

## Torsion closed forms (Section 6.3)

When the point $R$ on the twist used by Theorem B has finite order $m$ over $\mathbb Q$, the evaluator collapses. Writing $N$ for the curve order and $q=N/m$, Proposition 6.2 gives $\alpha_N(R)=q\,\alpha_m(R)$, so the sum is a fixed rational combination of $\varepsilon$ and the trace, with no Miller chain at all. The paper's main example (Theorem 6.3) is the central-binomial sum to the third point:

$$
\sum_{k=0}^{\lfloor p/3\rfloor}\binom{2k}{k}\equiv
\begin{cases}
-\tfrac13 \pmod p, & p\equiv2\pmod3,\\[2pt]
\tfrac{1-2r}{3} \pmod p, & p\equiv1\pmod3,
\end{cases}
$$

where $4p=r^2+27s^2$ and $r\equiv1\pmod3$. The proof uses the point $R=(4/3,-4/3)$ on $Y^2=X^3-16/27$, which has order 3 with $\alpha_3(R)=-2$, together with Jacobi's congruence $\binom{2L}{L}\equiv-r$. Example 6.4 treats the weight $z=-2$, which the same proposition gives as $\tfrac13$ for $p\equiv2\pmod3$ and $\bigl(1-2\cdot2^{(p-1)/3}r\bigr)/3$ for $p\equiv1\pmod3$.

Remark 6.5 records how Theorem 6.3 was found. A pre-registered search ([`Cartier-Miller-Congruence-Search-20261024/`](Cartier-Miller-Congruence-Search-20261024/)) tested 224 residue-class runs by lattice reduction. Its candidates were frozen by SHA-256 and confirmed at 1,110 fresh primes of 64–256 bits; the folder includes the code, the pre-registration and every run record, including the freeze hash. The search shows only how the congruence was **discovered**: the result rests on the proof in Section 6.3. Example 6.4 was derived afterwards, not found by the search. We found the congruence in none of the papers on partial central-binomial sums that we checked (Sun, Tauraso, Mattarei and others), but that search was not exhaustive, and novelty is not claimed.

## Validation and benchmarks

The current paper's Table 2 reports one full run of [`Cartier-Miller-Verification-20261022/cm_verify.py`](Cartier-Miller-Verification-20261022/cm_verify.py), a pure-Python script with fixed seeds whose saved output is in the same folder. All comparisons agreed, including:

- Theorem A at 4,601 rational points;
- an independent normalization check at 354 points, 108 of them on trace-one curves, built without the Miller recurrence;
- Theorem B at 20,837 nonbranch poles, 303 of them at $a=0$;
- Theorem D at 2,739 arguments, 69 of them exceptional;
- Corollary E at all 221 eligible primes below 3000 plus $p=1{,}000{,}211$;
- the quarter-point formula at all 210 eligible primes $13\le p<3000$ plus $p=1{,}000{,}033$;
- for Section 6.3, the order of $R$ over $\mathbb Q$ for 22 pairs $(k,z)$, $\alpha_3(R)$ for $z=1$ and $-2$, and Theorem 6.3 and Example 6.4 by direct summation at all 428 primes $5\le p<3000$ (856 comparisons).

These are finite checks, not proofs. Earlier and larger campaigns, with disjoint confirmation samples, are documented in the companion and the dated folders.

The benchmarks below are historical. They are reported in full in the computational companion.

The retained pilot benchmark compares complete quarter-point evaluations with a C++ adapter to SageMath's Harvey interval-product kernel, using BGS-based recurrence techniques. Both methods compute the prefix, boundary and weighted sum, including their per-prime preparation. This compares a recurrence task, not Harvey's full Kedlaya algorithm.

The pilot uses specialized Cornacchia/Gauss trace preparation. It does not benchmark a complete Schoof- or SEA-based implementation. The manuscript documents the timing protocol and limitations; the selected timings do not establish universal speedups or real world workload.

Table 1 is a quarter-point pilot run for seven primes $p\equiv1\pmod4$, with $n=(p-1)/4$, for Cartier-Miller v SageMath 10.8 Harvey `hypellfrob` interval-product kernel, which uses the Bostan–Gaudry–Schost algorithm (BGS). Both implementations compute $B_n$, $a_n$ and $U_p(n)$, including per-input preparation.

**Table 1. Complete quarter-point evaluation in milliseconds**

| Prime $p$ | Stopping index $n$ | Cartier–Miller Python | Harvey BGS C++ |
|--:|--:|--:|--:|
| 97 | 24 | 0.05 | 0.01 |
| 1,009 | 252 | 0.06 | 0.05 |
| 10,009 | 2,502 | 0.07 | 0.10 |
| 100,049 | 25,012 | 0.09 | 0.54 |
| 1,000,033 | 250,008 | 0.10 | 1.78 |
| 10,000,121 | 2,500,030 | 0.11 | 4.44 |
| 100,000,037 | 25,000,009 | 0.29 | 16.19 |

*See the computational companion for the timing protocol and limitations of this historical pilot.* 

## Extension research: branch points, isogeny closure, CM seeds and the rounded third point

The folder [`Cartier-Miller-Extensions-20261009/`](Cartier-Miller-Extensions-20261009/) contains follow-up research carried out between 6 and 18 October 2026, with its own README, proofs, validators and evidence. It addresses the branch arguments $f(\mu)=0$ excluded from the main theorem. It gives an explicit branch formula and normalized rational 2-isogeny transport, direct recognition of curves reachable from two ordinary easy seeds through depth two, and both depth-three families, of discriminants $-192$ and $-256$, with CM trace preparation. A 12 October addition explains all these slopes through a CM-to-Cartier comparison, $\beta/H\equiv-\tfrac{3B}{2A}s_2(\tau)$, which is classical in substance (Katz). It also adds a certified seed at discriminant $-7$. It also proves that, for $p\equiv2\pmod 3$, the missing boundary at the rounded third point is $a_{(p+1)/3}\equiv3/(2(\lfloor p/3\rfloor!)^3)\pmod p$. The complete weighted sum there is therefore equivalent to a Gauss factorial, an obstruction rather than a new fast family. An 18 October experiment integrates a certified Jacobi-sum route for that factorial with the Miller prefix. At the nine tested primes where it was selected, complete evaluation was 1.67–6.52× faster than with a native factorial. A remainder forest remains the better choice for dense tables of primes. No polylogarithmic method or new exponent is claimed. A further 12 October feasibility study shows that, for a generic ordinary curve, the missing slope $\kappa=\beta/H$ is exactly one entry of Frobenius modulo $p$, and a canonical-subgroup kernel sum of any $p$-adic lift. The canonical-lift and Serre–Tate constructions it examined gave no cheaper algorithm than existing $\tilde O(\sqrt p)$ methods, though no lower bound is claimed. Like the manuscript, this work is unrefereed, AI-assisted and makes no novelty claim; its [HUMAN_REVIEW.md](Cartier-Miller-Extensions-20261009/HUMAN_REVIEW.md) lists concrete questions for reviewers.

## Integration layer: one exact interface for the whole project

The folder [`Cartier-Miller-Integration-20261013/`](Cartier-Miller-Integration-20261013/) contains a consolidation audit and a dependency-free Python prototype, `cm_system`, dated 13 October 2026. It puts one input/output and modulus contract over the project's existing exact methods:

- the original sums modulo $p$ and $p^2$;
- the main genus-one row theorem, including the exceptional case;
- cubic branch queries;
- the fixed-discriminant Cartier tables;
- higher-genus hybrids and weighted prefixes.

It keeps quantities that earlier code called $K$ or $\kappa$ distinct, labels supplied traces as trusted unless certified, and falls back to exact computation, or refuses, rather than estimating. Its validator and recorded measurements are included; the measurements compare its own Python implementations only. It claims no new generic fast algorithm, no sum-avoiding Witt extraction and no novelty. Its [RELEASE_NOTE.md](Cartier-Miller-Integration-20261013/RELEASE_NOTE.md) records what was excluded from the delivery and the refresh of its vendored code to the corrected versions in this repository.

## Character and elliptic-point sums

The folder [`Cartier-Miller-Character-Sums-20261021/`](Cartier-Miller-Character-Sums-20261021/) holds the rationally weighted quadratic-character-sum application, dated 21 October 2026. For a squarefree cubic or quartic $f$ with any constant term and a nonbranch pole $a$, it evaluates

$$
C_f(a)=\sum_{x\ne a}\frac{\chi(f(x))}{x-a}\in\mathbb F_p,\qquad p\ge5,
$$

with one differentiated Miller chain at the curve order $N=p+1-\chi(f(a))\tau_f$ of the normalized twist. This works for every trace, with no exceptional branch. It is now Theorem B and Theorem 4.4 of the current paper. Constant-plus-simple-pole weights over a complete excluded set give the equivalent affine and projective elliptic-point sums. The rational points at infinity are counted exactly, and no character value is assigned there.

After a separately charged exact trace, a query costs $O(\log p)$ field operations, or $O((\log p)^3)$ bit operations with classical arithmetic. Preparing $s$ exclusions costs $O(s\log p+s^2)$, and each later coefficient vector costs $O(s)$. The faster polynomial-tree correction is proved but not implemented.

The live interface is the integration layer's `charsum` service. It certifies primality below $2^{64}$. The trace can be supplied, in which case it is labelled trusted, or counted directly up to a budget at a stated $O(p\log p)$ cost.

The constructions are attributed to Miller (1986; 2004), Semaev (1998), Rück (1999) and the earlier Cartier and high-block sources. Priority for the combined general-trace identity and the weighted-sum adapter is unresolved, and no new attack is claimed. The folder's historical benchmark measured the older frozen implementation, not the new code, and its qualifications are listed with it. Raw per-job data are kept in a separate archive identified by hash.

## Review and collaboration

Independent scrutiny is especially welcome on: Theorem A and its proof; the exceptional proof in Appendix B; the differential scale and residue signs; and the sign comparison with Voloch (1997) in Remark B.1. A specialist comparison with existing Cartier, descent, anomalous-curve and Frobenius literature would help establish whether the normalization is already implicit in known results.

Possible further work includes practical exact point-counting integration, faster curve arithmetic, branch arguments, higher genus and other stopping families; the paper's open questions list these. The current results do not give a uniform algorithm for all stopping indices, or congruences modulo $p^2$.

Please open an issue to discuss a proof gap, counterexample, literature connection or reproducibility problem. For computational findings, include the prime, input polynomial, evaluation argument, expected and obtained values, software versions and a minimal reproducing example. Pull requests for corrections and independently checked improvements are welcome.

## Licensing

The repository's [MIT License](LICENSE) covers the author's own material, including the extension, integration, character-sum and verification folders, which carry their own MIT licence files. It does not cover third-party or separately licensed code. [`Cartier_Miller_Benchmark/`](Cartier_Miller_Benchmark/) bundles David Harvey's interval-product sources from SageMath under the GNU General Public License, with their original notices in `upstream/COPYING.txt`. That folder's adapter, GUI, point counters, harness, tests and launchers carry `GPL-2.0-or-later` notices, and its `LICENSE` file reproduces the SageMath copyright statement. Those files remain under the GPL. The manuscript PDFs and LaTeX source are shared for review and remain the author's work under their own terms.

## AI assistance and attribution

Generative AI was used extensively in mathematical exploration, programming, computational checking and manuscript preparation under the author's direction. This project is shared transparently to invite human assessment and contribution; AI-generated feedback is not human peer review.

The manuscript contains the full proofs, mathematical references and benchmark details. This project does not claim to introduce the Cartier operator, Miller recurrence, characteristic $p$ additive transfer or point-counting algorithms.
