# The depth-three family below the B=0 seed (discriminant −256)

12 October 2026. This unrefereed note completes the depth-three nondual closure of the two ordinary easy seeds. It covers the chain below the B = 0 (j = 1728) seed, which the 7 October proof note had deferred. Its main text, from "This section treats the chain" onwards, is reproduced unchanged from the 12 October revision of the proof note (history/handover_records/depth_three_b0_20261012/). The code is core/depth_three_b0_recognize.py, the validator is core/validate_depth_three_b0.py, and the exact integer data come from theory/b0/derive_b0_family.py. No novelty or benchmark is claimed.

## Independent review and integration notes

An independent adversarial AI review on 12 October 2026 (history/reviews/depth_three_b0_20261012/) found no flaw in the family formulas, the normalized second-kind coefficient, recognition, twist coverage, collision exclusions or the classical trace preparation. It independently classified 1,885,840 nonsingular short models at twelve eligible primes up to 617, and exactly 16,448 were accepted. It required three corrections, applied here:

- **Eligibility.** The stated equivalence between p = x² + 64y² and 2 being a fourth power modulo p, for p ≡ 1 (mod 8), had only finite support and an unopened pointer. The review's addendum proves it from Gauss's criterion as given by Lemmermeyer: for p = a² + b² ≡ 1 (mod 8), (2/p)₄ = (−1)^{b/4}. So 2 is a fourth power if and only if 8 ∣ b, which gives p = a² + 64y².
- **Certificate schema.** The certificate verifier rejected unknown top-level fields but silently ignored unknown nested parameter fields. The review's two-line patch is applied in core/depth_three_b0_recognize.py. Valid certificates still pass.
- **Scope wording.** The earlier description of this chain as "deferred" is superseded throughout the release.

The review also flagged three points about the API contract:
- A trace supplied with verify_trace=False is trusted. For example, +6 instead of −6 at p = 73 yields the wrong H. With verify_trace=True it is rejected.
- Rejecting a non-member at p ≡ 1 (mod 8) costs one quartic-residue exponentiation, so the API is not constant-time throughout.
- Complete preparation is randomized in the search for √−1, even though the trace formula itself is deterministic.

When this family was merged into the consolidated release, the optional Las Vegas sign method was given its own helper, _las_vegas_sign_b0, which claims no success bound. The consolidated A = 0 routine decide_trace_sign deliberately refuses curves outside its own family, because its 1/5 bound is proved only there. The combined recognizer recognize_short_through_depth_three now covers both depth-three families. The CLI selects this family with --family b0.

The merged validator passed in this layout, with PARI 2.17.2 available. It ran 1,248 coefficient checks, the trace proposition at 81 primes, 400 twist checks, 17 tampered certificates rejected, 64 original-cubic branch queries and 15 large-prime recognitions.

## The family, recognition and trace

This section treats the chain that the 7 October version deferred: the nondual depth-three closure of the ordinary $B=0$ ($j=1728$) seed. The same transport, cofactor lemma and certificate shape apply. What changes is the coefficient algebra. The extraction works in the tower $\mathbb F_p[s]/(s^4-2)$, where $e=s^2$, instead of a biquadratic character algebra. The trace now follows exactly from Ireland and Rosen's Theorem 5.

**The chain.** The seed is $y^2=x^3+Ax$ with $p\equiv1\pmod4$. Every exponent of $(x^3+Ax)^h$ is even because $h$ is even, while $p-2$ is odd, so $\beta=0$; the leading binomial coefficient makes $H\ne0$. A nonzero rational root exists exactly when $-A=r^2$, so the seed is $(-r^2,0)$. The root $0$ only moves to another seed $(-4A,0)$, and on that seed the root $0$ is the dual, so a chain that starts at $0$ reaches its first non-seed model one step late and ends at a class of seed distance at most two. Quotienting at $q_0=r$ gives $(-11r^2,-14r^3)$ with $\beta_1=-rH$. The cofactor lemma gives the nondual second roots $q_1=(1+2e)r$ with $e^2=2$; this step reproduces the retained depth-two family $\bigl((-91-60e)r^2,(-462-308e)r^3\bigr)$. For the third step, $F_1'(q_1)=A_1+3q_1^2=(16+12e)r^2=4e(1+e)^2r^2$, because $e(1+e)^2=e(3+2e)=4+3e$. Its square root is $2(1+e)s\,r$ with $s^2=e$, so the nondual third roots are
$$q_2=(1+2e)r\pm4(1+e)s\,r=(1+4s+2s^2+4s^3)\,r,$$
where the sign is absorbed into $s$. The identity $4+3\sqrt2=\sqrt2\,(1+\sqrt2)^2$ shows that the earlier condition "$4+3e$ is a square" is the same as "$e$ is a square". Substituting into the quotient formula gives
$$\boxed{A=\alpha(s)r^2,\quad B=\gamma(s)r^3,\qquad \beta=-(7+4s+6s^2+4s^3)\,rH,}$$
with the coordinates in the table below, in the basis $(1,s,s^2,s^3)$ and with $s^4=2$. The reverse certificate has roots $(-2q_2,-8q_1,-32q_0)$ and ends at the seed scaled by $4^3$, namely $(-(64r)^2,0)$. Its multiplier $-q_2-2q_1-4q_0$ equals the forward one, so no division by $H$ occurs. Each step is nondual and the two third roots are distinct: $3+2e$ and $3+4s+6s^2+4s^3$ are units, of norm $1$, and $4(1+e)s$ has norm $2^9$.

| Quantity | Coordinates in $(1,s,s^2,s^3)$, $s^4=2$ |
|---|---|
| $\alpha$ | $(-731,\ -600,\ -540,\ -360)$ |
| $\gamma$ | $(-14798,\ -11816,\ -10164,\ -8456)$ |
| $\beta/(rH)$ | $(-7,\ -4,\ -6,\ -4)$ |
| $\alpha^3$ | $(-5570535491,\ -4681110600,\ -3938178420,\ -3310589880)$ |
| $\gamma^2$ | $(825258980,\ 693493472,\ 583439472,\ 490459424)$ |
| $4\alpha^3+27\gamma^2$ | $(-149504,\ -118656,\ 152064,\ 44928)$ |
| forward roots over $r$ | $(1,0,0,0)$, $(1,0,2,0)$, $(1,4,2,4)$ |
| reverse roots over $r$ | $(-2,-8,-4,-8)$, $(-8,0,-16,0)$, $(-32,0,0,0)$ |

**Eligibility.** The kernel roots are rational exactly when $s\in\mathbb F_p$. The seed is ordinary exactly when $p\equiv1\pmod4$. Together these hold exactly when $p\equiv1\pmod8$ and $2^{(p-1)/4}\equiv1\pmod p$. The validation confirms that this is equivalent to $p=x^2+64y^2$ for every prime below $5000$; Cox's Theorem 9.2 is the classical pointer but was not reopened here. The eligible primes below $700$ are $73,89,113,233,257,281,337,353,577,593,601,617$; the retained audit's four $B=0$ primes $73,89,113,233$ are exactly those below its bound of $251$. The Galois closure of $\mathbb Q(j)$ is dihedral of order eight, so no fixed modulus describes eligibility. A status label for a non-member therefore costs one exponentiation, while acceptance itself needs none. At an eligible prime $-1$ is a square, so $s^4-2$ has the four roots $i^ks_0$ in $\mathbb F_p$ and $\mathbb F_p[s]/(s^4-2)\cong\mathbb F_p^4$. Over $\mathbb Q$, however, the only nontrivial automorphism of $\mathbb Q(s)$ is $s\mapsto-s$. This is why the extraction descends by a relative norm to $\mathbb F_p[e]$ and then solves a linear equation for $s$, rather than using two commuting automorphisms.

**Completeness of the closure and the class polynomial.** By the cofactor lemma, every nondual length-three chain from a $B=0$ seed whose first root is nonzero has the displayed form. The endpoint set at an eligible prime is therefore
$$\mathcal G_3(p)=\{(\alpha(s)r^2,\gamma(s)r^3):s^4=2,\ r\in\mathbb F_p^\times\},$$
with $4(p-1)$ distinct models. The minimal polynomial of $j(s)$ over $\mathbb Q$ was computed as $\det(J\,M_\Delta-M_{6912\alpha^3})/N(\Delta)$ from multiplication matrices in $\mathbb Z[s]$; it equals PARI's `polclass(-256)` coefficient for coefficient. Since each $j$ with $j\ne0,1728$ has exactly $p-1$ short models, which form its quadratic twist orbit, $\mathcal G_3(p)$ is exactly the set of short models whose $j$ is a root of $H_{-256}$ modulo $p$.

**Recognition.** For $AB\ne0$ put $L=B^2\alpha^3-A^3\gamma^2=U_0+U_1s+U_2s^2+U_3s^3$. Its relative norm to $\mathbb F_p[e]$ is $L(s)L(-s)=P_0+P_1e$, where
$$P_0=U_0^2+2U_2^2-4U_1U_3,\qquad P_1=2U_0U_2-U_1^2-2U_3^2 .$$
The recognizer sets
$$\boxed{e=-P_0/P_1,\qquad s=-\frac{U_0+U_2e}{U_1+U_3e},\qquad r=\frac{\alpha(s)B}{\gamma(s)A},}$$
then verifies $e^2=2$, $s^2=e$, $r\ne0$, both coefficient equations, the forward chain from $(-r^2,0)$ and the reverse chain to $(-(64r)^2,0)$.

**Theorem (B=0 recognition).** Let $p=x^2+64y^2$ be prime and $(A,B)$ a nonsingular short model. If the recognizer accepts, then $(A,B)\in\mathcal G_3(p)$ with the exhibited parameters and $\beta=-(7+4s+6s^2+4s^3)rH$. Conversely every member of $\mathcal G_3(p)$ is accepted, and its parameters $(s,r)$ are uniquely determined by $(A,B)$.

*Proof.* Soundness is immediate, as before. For completeness take a member with parameters $(s_0,r_0)$, write $s_k=i^ks_0$, $\alpha_k=\alpha(s_k)$, $\gamma_k=\gamma(s_k)$, and put $c_k=\gamma_0^2\alpha_k^3-\alpha_0^3\gamma_k^2$, so that $L(s_k)=r_0^6c_k$ and $c_0=0$. Evaluating $L(s)L(-s)$ at $s_0$ and at $s_1$ gives $P_0+P_1e_0=0$ and $P_0-P_1e_0=r_0^{12}c_1c_3$. Hence
$$P_1=-r_0^{12}c_1c_3/(2e_0).$$
Writing $L=a(e)+b(e)s$ and evaluating at $\pm s_0$ gives
$$U_1+U_3e_0=b(e_0)=-r_0^6c_2/(2s_0).$$
Next, $27c_k=\alpha_k^3\Delta_0-\alpha_0^3\Delta_k$, so $c_k=0$ exactly when $j(s_k)=j(s_0)$. Over $\mathbb F_p$ the multiplication matrices diagonalize, so the identity $N(\Delta)H_{-256}(J)=\det(J\,M_\Delta-M_{6912\alpha^3})$ reduces to $N(\Delta)H_{-256}(J)\equiv\prod_k(\Delta_kJ-6912\alpha_k^3)$. Since $N(\Delta)=2^{29}$, the values $j(s_k)$ are the roots of $H_{-256}$ modulo $p$. They are pairwise distinct whenever $p\nmid\operatorname{disc}H_{-256}$. Then $c_1c_2c_3\ne0$, so the extraction returns $e_0$ and $s_0$. Finally, $p\nmid N(\alpha)N(\gamma)$ gives $\alpha_0\gamma_0\ne0$, so $r=r_0$. The table below shows that no eligible prime divides any of these integers. $\square$

| Quantity | Factorization |
|---|---|
| $N(\alpha)$ | $11^2\cdot23\cdot71\cdot167\cdot191$ |
| $N(\gamma)$ | $2^4\,3^2\,7^4\,11^2\,19^2\cdot23\cdot31$ |
| $N(4\alpha^3+27\gamma^2)$ | $2^{29}$ |
| $\operatorname{disc}H_{-256}$ | $2^{17}3^{80}7^{24}11^{10}19^6\,23^2\,31^6\,43^4\,47^2\,59^4\,71^2\,83^2\,103^2\,107^2\,131^4\,139^2\,191^2\,211^2\,227^2\,239^2\,251^2$ |
| $H_{-256}(0)$ | $2^3\,3^{12}11^6\,23^3\,71^3\,167^3\,191^3$ |
| $H_{-256}(1728)$ | $2^3\,3^{28}7^8\,11^4\,19^4\,23^2\,31^2$ |
| $H_{-256}(287496)$ | $2^3\,3^{26}7^8\,11^6\,19^2\,23^2\,47^2\,59^2$ |
| $H_{-256}(54000)$ | $2^3\,3^{12}11^4\,23^2\,47^2\,59^2\cdot239\cdot479\cdot599\cdot647\cdot719\cdot743$ |
| $\mathrm{Res}(H_{-256},P_2)$ | $2^6\,3^{52}7^{16}11^8\,19^4\,23^5\,31^3\,43^4\cdot47\cdot67^2\cdot79\cdot83^2\,103^3\cdot127$ |
| $\mathrm{Res}(H_{-256},P_3)$ | $2^6\,3^{24}11^{10}23^4\cdot47\cdot71\cdot83^2\,107^2\,131^2\cdot167\cdot191\cdot227^2\cdot263\cdot863\cdot1223\cdot1847\cdot2111\cdot2447\cdot2543\cdot2711\cdot2903\cdot3023$ |
| $\mathrm{Res}(H_{-256},H_{-192})$ | as in the previous table |

All factorizations are complete. They were found by trial division and Pollard–Brent, every prime factor is certified by deterministic Miller–Rabin because none exceeds $3.3\cdot10^{24}$, and every product was multiplied back to the original integer (`theory/b0/derive_b0_family.py`). Every odd prime factor other than $3$ is congruent to $3$ modulo $4$, as Deuring's reduction theory predicts, since such primes are inert in $\mathbb Q(i)$. No factor is eligible. At every eligible prime the family is therefore nonsingular and has four distinct conjugate $j$-values, and it is disjoint from the $B=0$ and $A=0$ closures through depth two and from the $A=0$ depth-three family. The family contains every quadratic twist via $r\mapsto dr$, and the multiplier scales by $d$. At $p\equiv7\pmod8$ (here $23,71,167,191$), $x^4=2$ has two roots and $\alpha$ or $\gamma$ vanishes at one of them, but the seed is supersingular and the recognizer reports `not_eligible_prime` for every input.

**Exact trace.** An accepted curve has the trace of its seed $y^2=x^3-r^2x$. Ireland and Rosen (1990, Ch. 18, §4, Theorem 5) state that for $p\equiv1\pmod4$ and $p\nmid D$, with $p=\pi\bar\pi$ in $\mathbb Z[i]$ and $\pi\equiv1\pmod{2+2i}$,
$$N_p(y^2=x^3-Dx)=p+1-\overline{(D/\pi)_4}\,\pi-(D/\pi)_4\,\bar\pi .$$
For $D=r^2$ the quartic symbol is the Legendre symbol $(r/p)$. Writing $\pi=a+bi$ with $a$ odd, $b$ even and $a+b\equiv1\pmod4$, the trace is therefore
$$\boxed{\tau=2\Bigl(\frac rp\Bigr)a .}$$
Cornacchia applied to $p=a^2+b^2$, with $\sqrt{-1}=c^{(p-1)/4}$ for a quadratic nonresidue $c$, supplies $(a,b)$. Unlike the $A=0$ case, the sign is part of the formula, so there is no separate sign step. The only randomized step is the nonresidue search. A consistency guard checks $8\mid b$, which follows from the trace proposition's volcano argument and makes $4p=\tau^2+256y^2$ the unique representation; a caller-supplied trace must satisfy that condition and can be recomputed exactly with `verify_trace=True`.

The retained audit row $(16,27)$ at $p=73$ comes from the seed $(1,0)=(-27^2,0)$. It is recognized with $s=18$, $e=32$, $r=27$, forward roots $(27,3,61)$, reverse roots $(24,49,12)$, endpoint $(8,0)$ and multiplier $44$, so $\beta=44\cdot67=28$. Cornacchia gives $73=(-3)^2+8^2$, and Theorem 5 gives $\tau=-6$, so $H=67$. For the normalized cubic $f=1+60w+10w^3$, which comes from the rational point $(0,10)$, the complete preparation `prepare_cm_b0` returns $H=67$, $K=32$ and $T_f(17)=5$ with no point counting. These agree with the retained $O(p)$ recurrence.

| Task | Cost |
|---|---|
| Recognition and extraction | $O(1)$ field operations including three inversions; no square root, no graph search |
| Eligibility label for a non-member | One exponentiation $2^{(p-1)/4}$, $O(\log p)$ field operations; not needed for acceptance |
| Exact trace | Randomized nonresidue search for $\sqrt{-1}$, Cornacchia $O(\log p)$ word steps, one Legendre symbol |
| $K$ reconstruction and supplied-root branch query | $O(1)$ each, unchanged |

**Validation, all passing; counts overlap.** At the eight eligible primes $73,89,113,233,257,281,337,353$, all $461{,}760$ nonsingular short models were classified. The $6{,}912$ accepted models coincide with the brute-force endpoints of nondual chains from every $(A,0)$ seed and with the set of models whose $j$ is a root of `polclass(-256)` modulo $p$; the forward roots agree with the brute-force chains, and $(s,r)$ is injective. At $p=73$ and $337$, where both depth-three families are eligible, the combined recognizer was run on every model and never accepted an input twice. For $1{,}248$ members, $(H,\beta)$ was recomputed by multinomial expansion and matched against Legendre, Theorem-5 and PARI traces. Theorem 5 itself matches Legendre traces for all $6{,}896$ curves $y^2=x^3-Dx$ at the $37$ primes $p\equiv1\pmod4$ below $400$, using a primary $\pi$ found by exhaustive search, and reproduces the book's example $y^2=x^3-x$ over $\mathbb F_{13}$ with $N=8$. The trace formula and the uniqueness of $4p=\tau^2+256y^2$ hold at all $81$ eligible primes below $5000$. A further $400$ twist checks and $17$ tampered certificates were all handled correctly; the tampering cases include $s\mapsto-s$, $s\mapsto is$, and altered reverse paths and labels. All $17$ ineligible primes tested reject every input. The $32$ retained audit rows from $B=0$ seeds are recognized with the audit's roots, models and multipliers, while the $32$ depth-three rows from $A=0$ seeds and the $32$ depth-four rows are rejected. On $48$ normalized cubics, $K$ agrees with the $O(p)$ recurrence and the $64$ branch queries agree with dense sums; the Las Vegas and Theorem-5 traces agree throughout. Recognition and complete preparation also round-trip at random eligible primes of $17$, $21$, $32$, $41$ and $63$ bits; $K$ was confirmed by the recurrence at the two smallest, and the trace by PARI at all of them.

**Status.** These are unrefereed algebraic derivations with executable checks. Unlike the 7 October work, this extension has not been reviewed by a second independent worker. The family and $H_{-256}$ are classical CM objects. The new parts are the explicit normalized transport, the relative-norm-then-linear extraction in the tower, the exclusions and the trace route, and their novelty is not claimed.
