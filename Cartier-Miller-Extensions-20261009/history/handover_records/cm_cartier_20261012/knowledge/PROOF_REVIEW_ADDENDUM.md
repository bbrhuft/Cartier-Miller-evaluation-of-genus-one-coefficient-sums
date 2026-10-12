# Review addendum: the ordinary B=0 seed at depth three

David Jordan's Cartier–Miller extension programme, 12 October 2026. Independent AI-assisted adversarial review of the supplied 12 October handover. This is an unrefereed proof review, not a novelty claim or a benchmark. The original manuscript and supplied files are preserved.

The new bounded extension survives this review. Its explicit family, recognition certificate, Cartier normalization, exclusion arithmetic and classical trace formula are consistent. This addendum closes the literature gap in the stated prime-eligibility equivalence and clarifies the scope and preparation contract. Finite checks corroborate the algebra; they do not prove it.

## The normalized family and its completeness

Let p be an odd prime, let p be congruent to 1 modulo 8, and suppose 2 is a fourth power modulo p. Equivalently, a parameter s in F_p satisfies s^4=2. Let r be nonzero. Start from the seed E_0: y^2=x^3-r^2x and set

$$q_0=r,\qquad q_1=(1+2s^2)r,\qquad q_2=(1+4s+2s^2+4s^3)r.$$

For a two-torsion root q of F=x^3+Ax+B use the normalized quotient

$$A'=-4A-15q^2,\qquad B'=-8Aq-22q^3.$$

The independently recomputed three-step endpoint is

$$A=(-731-600s-540s^2-360s^3)r^2,$$
$$B=(-14798-11816s-10164s^2-8456s^3)r^3.$$

Its inverse normalized roots are -2q_2,-8q_1,-32q_0; the inverse endpoint is (-(64r)^2,0). Nondual steps follow because the norms of q_1/r+2 and q_2/r+2q_1/r in Z[s]/(s^4-2) are 1. The norm of 4(1+s^2)s is 2^9, so the two third-step roots remain distinct at odd primes. These are exact integer identities.

For a B=0 seed, a zero first kernel root moves to another B=0 seed. That path spends one step among easy seeds and adds no class of minimal seed distance three. A nonzero first root requires A=-r^2. The quotient cofactor determines every later nondual root: q_next=q±2 sqrt(F'(q)). At the second step this requires e^2=2, and at the third step

$$F_1'(q_1)=4e(1+e)^2r^2.$$

Because 1+e is nonzero, a third rational nondual step requires e=s^2. Thus every genuinely new ordinary B=0 depth-three endpoint is in the displayed family. Conversely its parameters construct a valid chain. This is the claimed bounded completeness; it does not address generic curves or depth four.

## Differential scale, Cartier action and residue conventions

Use omega=dx/y, eta=x dx/y, h=(p-1)/2,

$$H=[x^{p-1}]F^h,\qquad \beta=[x^{p-2}]F^h.$$

There is no change to the retained differential convention. With u=F'(q), the quotient map is

$$x'=x+\frac{u}{x-q},\qquad y'=y\left(1-\frac{u}{(x-q)^2}\right).$$

Its derivative satisfies dx'/dx=1-u/(x-q)^2, hence phi*omega'=omega, with scale +1. Also

$$\phi^*\eta'=(2x-q)\omega-2d\left(\frac{y}{x-q}\right).$$

For separable isogenies Cartier commutes with pullback and kills the exact differential. Therefore H'=H and beta'=2 beta-qH. The seed has beta_0=0: its h-th power has only even exponents when p=1 modulo 4. Iteration gives

$$\beta_3=-(4q_0+2q_1+q_2)H=-(7+4s+6s^2+4s^3)rH.$$

The reverse coefficient reconstruction gives the same sign: beta/H=sum(q_reverse,i/2^(i+1))=-(q_2+2q_1+4q_0). This relation does not require division by H in its implementation. The ordinary family has H nonzero.

For the original normalized cubic f=1+cw+bw^2+aw^3, a nonzero, the retained change x=aw+b/3, y=av gives dx/y=dw/v exactly and

$$\beta=aK+(b/3)H,\qquad K=(\beta-(b/3)H)/a.$$

For a supplied nonzero simple rational root mu, the retained branch formula is

$$T_f(\mu)=\frac{a\mu(\mu H-K)}{f'(\mu)}.$$

No new residue convention is introduced. The independent dense-polynomial checks compute the entire coefficient polynomial first and evaluate the strict block of coefficients with indices 0 through p-1 directly; they do not use this branch formula as their reference.

## Recognition at all eligible primes

Write alpha and gamma for the two coefficient polynomials above and

$$L=B^2\alpha^3-A^3\gamma^2=U_0+U_1s+U_2s^2+U_3s^3.$$

The relative norm under s -> -s is P_0+P_1e, e=s^2, where

$$P_0=U_0^2+2U_2^2-4U_1U_3,\qquad P_1=2U_0U_2-U_1^2-2U_3^2.$$

The proposed extraction e=-P_0/P_1, s=-(U_0+U_2e)/(U_1+U_3e), r=alpha(s)B/(gamma(s)A) is correct. At an eligible prime the four roots i^k s_0 exist. For a true member, put c_k=gamma_0^2 alpha_k^3-alpha_0^3 gamma_k^2. Then

$$P_1=-r_0^{12}c_1c_3/(2e_0),\qquad U_1+U_3e_0=-r_0^6c_2/(2s_0).$$

The determinant identity for the independently derived quartic polynomial P(J) gives its roots j(s_k). Its discriminant and N(alpha)N(gamma) have only factors 2,3 and primes congruent to 3 modulo 4. All eligible primes are congruent to 1 modulo 8, so none divides those integers. Accordingly the j-values are distinct, each c_k for k!=0 is nonzero, both extraction denominators are nonzero, and alpha_0 gamma_0 is nonzero. Extraction is complete and unique. Acceptance separately verifies the parameter equations and both normalized paths, giving soundness.

All norms, discriminants, evaluations and cross-family resultants used here were recomputed by an independent rational Gaussian-elimination determinant implementation. Every asserted factor was certified by trial division, and every factorization was multiplied back. The largest factor is 12,263; no probable-prime assertion is needed. These exact checks also exclude collisions with all the retained depth-at-most-two classes and the A=0 depth-three family at eligible primes.

The determinant polynomial equals the handover's retained PARI polclass(-256) coefficients. A fresh PARI computation was unavailable in this review environment, so the fresh independent claim is the exact determinant identity, not a new PARI run. The family and recognition proof do not need the CM label to prove their explicit algebraic statements.

## A verified source for prime eligibility

The supplied note calls the equivalence with p=x^2+64y^2 a checked classical pointer. Its finite validation alone is insufficient to prove that equivalence. A directly read primary source supplies the needed step: Lemmermeyer's Rational Quartic Reciprocity II, Section 4, page 2 of the arXiv author manuscript, derives Gauss's criterion. For a prime p=a^2+16v^2 congruent to 1 modulo 8, it states

$$\left(\frac2p\right)_4=(-1)^v.$$

In any sum-of-two-squares representation of p=1 modulo 8, the odd coordinate is a and the even coordinate b is divisible by 4. Put v=b/4. The criterion therefore gives

$$2^{(p-1)/4}=1\quad\Longleftrightarrow\quad8\mid b
\quad\Longleftrightarrow\quad p=a^2+64y^2.$$

This establishes the eligibility equivalence for every relevant prime, without extrapolating the checks below 5,000. It also establishes the divisibility guard used in trace preparation. Cox Theorem 9.2 was not directly verified during this review and is not needed for this replacement argument.

## The trace and complete cost contract

Ireland and Rosen, second edition, Chapter 18, Section 4, Theorem 5, printed page 307, was checked visually in the supplied scan. For y^2=x^3-Dx and primary pi=a+bi, pi=1 modulo (2+2i), its point count is

$$N_p=p+1-\overline{(D/\pi)_4}\pi-(D/\pi)_4\overline\pi.$$

Thus the trace is the positive sum of the two displayed character terms. For D=r^2, the quartic character equals the ordinary Legendre symbol chi(r), because its reduction is (r^2)^((p-1)/4)=r^((p-1)/2). Hence

$$\tau=2\chi(r)a.$$

The primary condition is exactly a odd, b even, a+b=1 modulo 4. Replacing b by -b does not change the trace. The rational normalized isogenies preserve the exact trace, so this is also the target trace. Since 8 divides b, writing b=8y gives 4p=tau^2+256y^2; uniqueness follows from the uniqueness of the Gaussian factorization of a rational prime, up to units and conjugation. This is a classical trace formula, not a new trace theorem.

| Phase | Contract and cost |
|---|---|
| Prime input | The mathematical theorem assumes p prime. The prototype deterministically validates 7<=p<2^64. This validation is outside the constant arithmetic extraction claim and must be charged in complete runs. |
| Positive extraction and path certification | Fixed field work, three extraction inversions plus fixed certificate arithmetic; no square-root search and no quartic-residue exponentiation needed to accept a member. |
| Negative API status | At p=1 modulo 8 the current API performs an exponentiation to distinguish an ineligible prime from an eligible non-member. Its complete worst-case call is not constant field work. |
| Trace preparation | Random quadratic-nonresidue search; success probability exceeds one half for the implemented sample range. Each trial uses an exponentiation. One further exponentiation obtains sqrt(-1), Cornacchia uses O(log p) integer Euclidean steps, and one Legendre exponentiation fixes the trace. Expected field work is logarithmic; integer arithmetic and primality validation are separately charged. |
| Reconstruction | H=tau modulo p, beta from the certificate, and K from the original cubic require fixed field work. |
| Prepared supplied-root query | Fixed field work including checking the nonzero root and derivative. There are at most three branch roots per cubic. |

The trace formula is deterministic once the primary representation is supplied. The full delivered CM preparation is randomized in the nonresidue search and is not an unconditional deterministic polylogarithmic algorithm. No SEA implementation or point-count backend is part of this preparation. A trusted-trace route without verify_trace=True deliberately does not certify its input sign.

## Reconciliation and bounded conclusion

No mathematical counterexample was found. The original note's opening paragraph still says the B=0 family is deferred, its title still describes only the A=0 family, and parts of START_HERE and README likewise retain the earlier scope. Those sentences should be updated before a consolidated handover is published.

The certificate verifier ignores unknown keys nested inside parameters even though it rejects unknown top-level keys. It returns a recomputed, mathematically valid certificate, so this does not forge the curve or transport result. The accompanying one-line patch rejects such unknown nested keys; a valid certificate and the injected-key counterexample were both checked. This is a schema correction, not a mathematical repair.

The completed bounded result is direct recognition and complete classical CM preparation for the previously deferred ordinary B=0 depth-three family, with every quadratic twist. Together with the retained A=0 family and lower-depth recognizer, it covers the ordinary easy-seed closure through three rational degree-two steps, with paths spent inside the seed family assigned their smaller minimal seed distance. It does not address generic or supersingular K, arbitrary stopping indices, the rounded-third a_L boundary, depth four, or a sum-avoiding Witt correction. Human review and a separate novelty assessment remain appropriate.

## Sources read for this review

Ireland, K., & Rosen, M. (1990). A classical introduction to modern number theory (2nd ed.). Springer. Chapter 18, Section 4, Theorem 5, p. 307. User-supplied chapter scan; formula and conjugation visually inspected.

Lemmermeyer, F. (2013 posting). Rational quartic reciprocity II. Author manuscript, arXiv:1310.6597. Section 4, p. 2. https://arxiv.org/abs/1310.6597 . The source gives the classical quartic character criterion used here; no new reciprocity theorem is claimed.

Sutherland, A. V. (2023). 18.783 Elliptic Curves, Lecture 22: Isogeny volcanoes. MIT. Theorem 22.11 and Remark 22.12, p. 7. https://math.mit.edu/classes/18.783/2023/LectureNotes22.pdf . The remark explicitly covers the exceptional seed j=1728; a theorem excluding that seed should not be cited without the remark. The explicit trace and eligibility arguments above do not need an unverified volcano extension.
