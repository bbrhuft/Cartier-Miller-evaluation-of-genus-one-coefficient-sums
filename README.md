# Cartier–Miller evaluation of genus-one coefficient sums

A research manuscript and computational project shared for independent mathematical review and possible collaboration.

**Status:** This is an unrefereed research draft with substantial generative-AI assistance. Numerical checks support the formulas, but do not replace independent review of the proofs. The precise novelty of the exceptional normalization remains open to specialist assessment.

## What the project does

Cartier–Miller evaluates certain large truncated polynomial-power sums modulo a prime through elliptic-curve arithmetic, rather than accumulating their terms individually.

Let $p\geq7$ be prime, put $h=(p-1)/2$, and let $f\in\mathbb F_p[w]$ be squarefree of degree three or four, initially normalized by $f(0)=1$. Write

$$
f(w)^h=\sum_m c_mw^m,
\qquad
T_f(w)=\sum_{m=0}^{p-1}c_mw^m.
$$

The main result evaluates $T_f(\mu)$ for nonzero $\mu\in\mathbb F_p$ with $f(\mu)\ne0$. Equivalently, for $\lambda=1/\mu$,

$$
S_f(\lambda)
=[w^{p-1}]\frac{f(w)^h}{1-\lambda w}
=T_f(1/\lambda).
$$

The cutoff is fixed at degree below $p$; the evaluation point varies. This is not a general algorithm for arbitrary stopping indices in central-binomial sums. Inputs with $f(0)\ne0$ can be normalized, with the factor $f(0)^h$ restored afterward.

## The identity and exceptional case

On the smooth projective curve $E:v^2=f(w)$, with origin $(0,1)$, let

$$
\tau=p+1-\left|E(\mathbb F_p)\right|,
\qquad H=c_{p-1}\equiv\tau\pmod p.
$$

Put $d=f(1/\lambda)$, choose $v_0^2=d$, let $\chi$ be the quadratic character of $d$, and set $D=(1/\lambda,v_0)-(1/\lambda,-v_0)$ as a divisor difference. The formula is

$$
S_f(\lambda)=H-\chi r\Psi_{M_\chi}(D),
\qquad
r=\frac{1}{\lambda v_0},
\qquad
M_\chi=p+1-\chi\tau.
$$

Here $\Psi_M$ is a logarithmic derivative of a function with divisor $MD$, normalized by the differential $dw/v$ and evaluated at the origin. It is computed through a differentiated Miller recurrence. The notation $d\log F$ means $dF/F$, not an analytic logarithm.

The draft proves the exceptional normalization directly in characteristic $p$. When $\tau=\chi$, the annihilator is $M_\chi=p$; the displayed formula does not divide by it. The characteristic-$p$ additive transfer itself is established mathematics, associated with Serre, Semaev, Rück and Voloch. The proposed contribution is the explicit coefficient-sum identity, its normalization and its computational application.

## Complexity

After preparing a fixed curve and its exact trace, each admissible query uses $O(\log p)$ field operations. The trace is reusable across queries on the same curve and prime. Computation in a quadratic algebra, with a resumable split when necessary, avoids searching for a quadratic nonresidue during the query.

Combining the query with Schoof's deterministic point count gives the paper's deterministic polynomial-time consequence. Under classical modular arithmetic, the total bit-operation cost for $N_q$ queries is bounded by

$$
T_{\mathrm{total}}
=T_{\mathrm{Schoof}}(p)
+O\!\left(N_q(\log p)^3\right).
$$

Practical exact trace preparation may instead use SEA or an automatic routine such as PARI/GP's `ellap`, replacing Schoof in the stated deterministic worst-case proof. Complexity illustrations are not measured timings.

![Illustrative cost complexity of Cartier-Miller with Shoof and SEA prep compared to Harvey BGS](https://github.com/bbrhuft/Cartier-Miller-evaluation-of-genus-one-coefficient-sums/blob/main/Cartier-Miller-With-SEA.jpg) 

Illustrative cost complexity of Cartier-Miller with Shoof (dotted) or SEA (solid) point counting compared to Bostan-Gaudry-Schost (BGS). 

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

At $p=97$, the example gives $n=24$, $B_n=33$, $a_n=79$ and $U_p(n)=43$. Computing both the prefix and boundary is essential to evaluating the complete weighted sum.

## Validation and benchmarks

The manuscript reports checks against direct polynomial expansion, independent point counts, kernel identities and an elementary rational-point sum. Reported generic tests include 20,316 admissible queries, with 368 exceptional cases. An independent point-sum verifier agreed on 4,357 queries, including 155 exceptional cases. These checks arose within the AI-assisted research programme.

The retained pilot benchmark compares complete quarter-point evaluations with a C++ adapter to SageMath's Harvey interval-product kernel, using BGS-based recurrence techniques. Both methods compute the prefix, boundary and weighted sum, including their per-prime preparation. This compares a recurrence task, not Harvey's full Kedlaya algorithm.

The pilot uses specialized Cornacchia/Gauss trace preparation. It does not benchmark a complete Schoof- or SEA-based implementation. The manuscript documents the timing protocol and limitations; the selected timings do not establish universal speedups or workload crossovers.

## Review and collaboration

Independent scrutiny of the exceptional proof, differential scale, residue signs and split-algebra arithmetic is especially welcome. A specialist comparison with existing Cartier, descent, anomalous-curve and Frobenius literature would help establish whether the normalization is already implicit in known results.

Possible further work includes practical exact point-counting integration, faster curve arithmetic, branch arguments and other stopping families. The current theorem does not establish a uniform algorithm for all stopping indices or congruences modulo $p^2$.

Please open an issue to discuss a proof gap, counterexample, literature connection or reproducibility problem. For computational findings, include the prime, input polynomial, evaluation argument, expected and obtained values, software versions and a minimal reproducing example. Pull requests for corrections and independently checked improvements are welcome.

## AI assistance and attribution

Generative AI was used extensively in mathematical exploration, programming, computational checking and manuscript preparation under the author's direction. This project is shared transparently to invite human assessment and contribution; AI-generated feedback is not human peer review.

The manuscript contains the full proofs, mathematical references and benchmark details. This project does not claim to introduce the Cartier operator, Miller recurrence, characteristic-$p$ additive transfer or point-counting algorithms.
