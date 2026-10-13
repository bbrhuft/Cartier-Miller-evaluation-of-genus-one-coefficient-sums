# Rounded third point: bounded Tal applicability audit

David Jordan research project, 10 October 2026. This is an unrefereed, AI-assisted research audit for independent human review. The original manuscript, ordinary third-point evaluator, completed depth research and GitHub repository are unchanged.

## Outcome

The elementary factorial reduction is correct. Any certified algorithm for
$G=((p-2)/3)!\bmod p$ transfers to the complete rounded-third output
$(B_L,a_L,U_p(L))$ with only logarithmic additional field work. Tal's classical report therefore applies to the missing boundary, rather than merely to the already fast prefix. Its divisor-dependent bounds give a **proved transfer conditional on the relevant unrefereed Tal theorem and the retained Cartier–Miller prefix theorem**. They do not supply an implemented fast backend here.

The most accessible theoretical result is the uniform logarithmic corollary from Tal's Proposition 4.3. For a full algebraic reconstruction pilot, the split $p-1$ route is the best first target because it works in the base field and uses a directly proved multifold Jacobi identity. No unconditional ranking of actual runtimes between the three divisor routes is justified: their reconstruction exponents and constants have not been quantified. An admissible $p+1$ divisor can be more attractive for an individual prime with poor split divisors.

New exact evidence comprises every one of the 336 target primes from 11 through 5,000, held-out primes 10,007, 20,021 and 50,021, 26 dense polynomial controls, 43 split identity controls, 20 trace-one controls, 142 cubic-extension identity controls and 199 halving controls. Arithmetic certificates record 11,969 route/divisor inputs, including failures. None of these are performance benchmarks. The runnable complete-output routine uses the retained Miller prefix and a labelled linear reference factorial.

## Applicability and decision table

All costs below are for a single prime and complete output. Put $b=\lceil\log_2p\rceil$, and let $P(p)=O(b^3)$ be a conservative classical-bit bound for the retained prefix, including its fixed-rank quadratic arithmetic and inversions. Soft-O suppresses logarithmic factors in the represented input parameters. It does not suppress powers of $q$.

| Route | Exact prerequisites at $n=m$ | Full bit cost and parameter contract | Proof dependence | Engineering burden and decision |
|---|---|---|---|---|
| Ordinary factorial BGS | Prime $p$, $m<p/2$; small required integers are units | $\widetilde O(\sqrt m)+P(p)$, with bit costs for represented field arithmetic | Classical Bostan–Gaudry–Schost; retained prefix | Appropriate correctness/performance baseline; no new method |
| Split $p-1$, Tal Theorems 1.1/1.5 | $q\mid p-1$; $q\le2$ invokes ordinary interval products; compatible order-$q$ root, character and selected prime | $\widetilde O(q^c+\sqrt{p/q})+P(p)$. Theorem 1.1 takes $q$ as input and includes its deterministic character setup; discovering a useful $q$ is a separate contract | Split identity proved below; classical polarized recovery and orientation; Tal's assembly and accounting unrefereed | Simplest full recovery pilot; selected engineering target, without a runtime winner claim |
| $p+1$, Tal Proposition 4.2/Appendix G | $q\ge4$, $q\mid p+1$, $K=(p+1)/q$ odd; representation of $\mathbb F_{p^2}$, compatible character of order $2q$ | $\widetilde O(q^C+\sqrt{p/q})+P(p)$ with the supplied field/character, or the same expected bound after its Las Vegas setup; divisor search charged separately | Trace-one identity and root selection audited below; the new trace-one orientation adaptation is Tal's argument | Adds a quadratic field and its own recovery family; consider when better admissible divisors exist |
| $r=3$, Tal Theorems 1.3/5.3 | $q>1$, $q\mid p^2+p+1$; after removal of the index factor; compatible $\mathbb F_{p^3}$, character and all restricted reduction maps | $\widetilde O(q^{c_3}+D^{1/4})+P(p)$, $D=(p^2+p+1)/q$; expected setup from $p,q$ is polynomial in $q,b$; search/factorization charged separately | Classical Gauss–Jacobi/Stickelberger identities; Tal's reconstruction and lattice recursion | Weaker interval exponent for a given $q$, more local precision and conductor handling; certificates and identity controls implemented |
| Uniform, Tal Proposition 4.3/Appendix H | Prime $p\ge5$; $0\le m<p$; no divisor | $O(\sqrt p\,b^{3/2}\sqrt{\log b})+P(p)$ deterministic bits | BGS selected-term theorem and fast integer multiplication are classical; Tal's routing/counting assembly unrefereed | Easiest bounded theoretical fallback; literal published parameters use the ordinary fallback for all 64-bit inputs |

There is no reason to identify $c,C,c_3$, and no justification for setting any of them to one. Tal §3.3 chooses an unspecified common exponent greater than one covering its operations and then enlarges the theorem exponents when necessary. The cited Lenstra–Silverberg theorem establishes polynomial time in the full representation length, not a linear-in-conductor recovery routine. In its dense order representation the input alone has at least $\phi(q)^3$ scalar entries, as its proof explicitly notes for rank $\phi(q)$. This is an engineering size cost for that interface, not a lower bound on every possible algorithm or compact interface.

## Endpoint verification and elementary proof

Assume throughout that $p\ge7$ is prime and $p\equiv2\pmod3$. The first such prime is 11. Write $p=3m+2$, $h=(p-1)/2$, $L=m+1$. Then $m$ is odd and $L\le h$. The prefix is strict: $B_L=\sum_{i=0}^{m}a_i$, whereas $B_m=B_L-a_m$.

The independent definition is

$$
t_0=1,\quad t_{i+1}=t_i\frac{h+2+i}{2i+2},\qquad
U_p(N)=\sum_{i=0}^{N-1}(h+1+i)t_i.
$$

Upper negation gives $t_i=(2i+1)a_i$, where $a_i=\binom{2i}{i}8^{-i}$. The manuscript's telescoping identity near equations (32)–(35) gives

$$
U_p(N)=4B_N-2N(2N+5)a_N\quad(0\le N\le h).
$$

All inversions are of nonzero residues. Wilson reflection is
$n!(p-1-n)!=(-1)^{n+1}$. At $n=2m$, it gives
$(2m)!(m+1)!=-1$. Since $m+1\equiv1/3$, setting $G=m!$ gives $(2m)!=-3/G$. Also $8^m=2^{p-2}=1/2$. Consequently

$$
\binom{2m}{m}=-3/G^3,\qquad a_m=-6/G^3.
$$

The ratio $a_{m+1}/a_m=(2m+1)/(4(m+1))=-1/4$, so

$$
\boxed{a_L=\frac3{2G^3}},\qquad
\boxed{U_p(L)=4B_L-\frac{17}{3G^3}}.
$$

For the floor endpoint, $m\equiv-2/3$. Substituting $B_m=B_L-a_m$ yields

$$
U_p(m)=4B_L+\frac89a_m=4B_L-\frac{16}{3G^3}.
$$

Because $3((2p-1)/3)=2(p-1)+1$, cubing is bijective and
$G=(3/(2a_L))^{(2p-1)/3}$. Recovering $a_L$ from the rounded $U$ additionally uses $(9/34)(4B_L-U)$, which fails at $p=17$. This is an inversion degeneracy, not a boundary zero. Newly recomputed values at $p=17$ are

| $m$ | $L$ | $G$ | $B_L$ | $a_m$ | $a_L$ | $U_p(L)$ | $U_p(m)$ |
|---|---|---|---|---|---|---|---|
| 5 | 6 | 1 | 6 | 11 | 10 | 7 | 13 |

Thus $U_p(6)=4B_6=7$, but the requested boundary remains 10.

For $f(w)=1-w^3/2$, $f^h=\sum_i a_iw^{3i}$, hence $H=c_{p-1}=0$, $K=c_{p-2}=a_m$ and the cutoff at degree $p-1$ contains exactly $i\le m$. At the unique root $\mu=2^{-m}$, $\mu^3=2$. The classical telescoping sum

$$
T_f(\mu)=\sum_{i=0}^{m}\binom{2i}{i}4^{-i}
=(2m+1)\binom{2m}{m}4^{-m}
=-\frac{a_m}{3\mu}
$$

proves $a_L=(3\mu/4)T_f(\mu)$ without assuming the general branch theorem. In the branch differential proof, $\omega=dw/v=dx/y$, $x=-w/2$, $y=-v/2$, so $\beta=-K/2$ and $H=0$. The branch formula uses leading coefficient $-1/2$ and derivative $-3\mu^2/2$, giving the same negative sign. This short model is separate from the original manuscript's rational-point normalization with $\kappa=-2$. No differential scale or residue convention is changed.

Trace zero follows directly because cubing permutes $\mathbb F_p$: the quadratic character sum of $1-w^3/2$ equals the sum of a quadratic character over the base field, which is zero. It explains the known prefix annihilator $p+1$; it supplies no factorial amplitude. The old 9 October claim about the absence of classical exponent-saving algorithms is historical after Tal's new classical report, which is distinct from his earlier quantum work.

## Conditional complete-output theorem

Let $\mathcal F$ be an algorithm returning the correct nonzero $G=m!\bmod p$, with bit cost $F(p,m)$ under a stated setup contract. Accept the retained prefix theorem and its implementation. Compute $B_L$ with trace zero, compute $v=(G^3)^{-1}$, and return

$$
(B_L,\ (3/2)v,\ 4B_L-(17/3)v).
$$

The independent identities above prove correctness. The boundary and output arithmetic use a constant number of field operations and one inversion beyond the prefix, and the total cost is $F(p,m)+P(p)+O(I(b))$, where $I(b)$ is modular inversion cost. The same construction works at $p=17$, retaining the boundary. The reverse conversion from $a_L$ to $G$ costs $O(\log p)$ field operations and has no exception in this progression.

Taking $\mathcal F$ to be the respective Tal factorial theorem proves each conditional corollary in the decision table. No new point counting or CM formula is needed. Taking $\mathcal F$ to be ordinary BGS proves the established square-root baseline; taking it to be this package's direct product yields a correct linear-reference complete evaluator. The reduction alone establishes neither Tal's theorem nor the manuscript theorem.

## The split identity and its reconstruction hypotheses

Put $K=(p-1)/q$. Choose an element $\eta\in\mathbb F_p$ of exact order $q$, fix $\rho(\zeta_q)=\eta$, and define the character by $\rho(\chi(x))=x^{-K}$. This is a compatible choice, not an arbitrary root paired with an unrelated character. All character powers, including the trivial one, are extended by zero at zero.

Let $J_a(\chi)$ be the sum over $x_1+\cdots+x_a=1$ of $\prod_i\chi(x_i)$, with $1\le a<q$. The exact identity needed is

$$
(aK)!=(-1)^{a-1}\rho(J_a(\chi))(K!)^a\pmod p.
$$

An independent proof reduces each character to $x^s$, $s=p-1-K$, and writes the sum constraint as $1-(x_1+\cdots+x_a-1)^{p-1}$. The unconstrained first term sums to zero. In the remaining multinomial expansion each surviving variable exponent must satisfy $s+k_i=p-1$, since $0<s+k_i<2(p-1)$. Thus $k_i=K$ and $k_0=p-1-aK$. Summing each $x_i^{p-1}$ contributes $-1$. Wilson reflection converts the remaining factorial ratio to exactly the displayed $(-1)^{a-1}$ sign. This proof does not require accepting an attribution to Young without reading that paper.

Binary factors satisfy $J_{u+v}=J_uJ_vJ_q(u,v)$. For $u,v,u+v\not\equiv0\pmod q$, the two-character sum has polarization $J\bar J=p$, and at $\mathfrak p_t=\sigma_t^{-1}(\mathfrak p)$ its exponent is

$$
c_t=\lfloor(u+v)t/q\rfloor-\lfloor ut/q\rfloor-\lfloor vt/q\rfloor.
$$

The selected prime has exponent zero when $u+v<q$, so every top-conductor addition-chain factor is a local unit. Degenerate proper-conductor factors are evaluated separately. The multifold ideal has exponents $\lfloor at/q\rfloor$, while its polarization is $p^{a-1}$; replacing it with a binary polarization $p$ would be wrong.

Lenstra and Silverberg's Theorem 1.3 applies to the full CM-order $A=\mathbb Z[\zeta_d]$ for $d>2$, an invertible fractional ideal $I$, and totally positive $w$ with $I\bar I=wA$. These are precisely satisfied by nondegenerate binary Jacobi ideals, because the ring is the maximal cyclotomic order and the actual sum is a generator with that polarization. The theorem returns a polarized generator, not an arbitrary generator of a known principal ideal. Rational conductors 1 and 2 and degenerate sums are explicit base cases.

The quotient of two polarized generators is an everywhere-unit with all complex absolute values one, hence a root of unity. It cannot be discarded: it can change the requested modular residue. Van Wamelen's Theorem 9 and §7 resolve it using all proper-conductor values, polynomial CRT modulo $X^q-1$, integral coefficients, and the derivative congruence

$$
A'(1)\equiv0\pmod q\quad(q\text{ odd}),\qquad
A'(1)\equiv\frac{p-1}{2}(\gcd(q,u)+\gcd(q,v))\pmod q\quad(q\text{ even}).
$$

The number of roots is $\operatorname{lcm}(q,2)$, so an odd conductor requires testing signs as well as powers of $\zeta_q$. Van Wamelen's original fast computation uses shortest-vector search exponential in dimension; Tal replaces that search with polynomial polarized recovery, while retaining the orientation criterion. A generic shortest-vector call therefore does not implement Tal's claimed complexity.

At $n=m$, there is no Wilson complement because $m<p/2$. The nearest grid point $aK$ leaves an interval of length at most $K/2$; one $K!$, an addition chain, orientation, reduction and the interval correction must all be charged. The 43 toy controls test multifold signs, compatible roots, exact conjugation norms and binary ideal support at every selected conjugate. They enumerate $\mathbb F_p$ and are explicitly not a recovery backend.

## What transfers from the p+1 route

Let $q\ge4$ divide $p+1$ and $K=(p+1)/q$ be odd. Necessarily $q$ contains the full $2$-part of $p+1$. Order $2q$ divides $p^2-1$, and the compatible character restricts to the quadratic character on $\mathbb F_p^\times$, because $(p^2-1)/(2q)=K(p-1)/2$ with $K$ odd.

For odd $a<q$, put $k_a=(aK-1)/2$ and
$E_a=\sum_{\operatorname{Tr}(x)=1}\chi(x)^a$. The exact identity is

$$
\rho(E_a)=\binom h{k_a},\qquad
\binom{2k_a}{k_a}=(-4)^{k_a}\rho(E_a).
$$

Grouping a Gauss sum by trace gives $G_{p^2}(\chi^a)=E_aG_p(\lambda)$. The exponent $a(p^2-1)/(2q)=k_ap+(h-k_a)$ has these two base-$p$ digits. The compatible first-order Gauss congruences cancel their common $-\pi^h$, giving $h!/(k_a!(h-k_a)!)$. The negative character convention is essential to this digit/sign identification. This is not the cubic supersingular trace supplying a coefficient; it is a larger character order and a different factorial recursion.

Tal's Appendix G recovers the trace-one family at all conductors dividing $M=2q$. If $d>1$ divides $p+1$, $E_d=(-1)^{(p+1)/d+1}$ is explicit. Otherwise $d$ is divisible by four, $p\equiv d/2-1\pmod d$, $E_d\bar E_d=p$, and its ideal is the product of selected prime orbits with representative above $d/2$. Polarized recovery applies. For a nonprimitive requested power, reduce to $d=M/\gcd(a,M)$ and then use a genuine Galois automorphism at that conductor.

The trace-one orientation criterion is Tal's adaptation, rather than a direct quotation of van Wamelen for ordinary Jacobi sums. It tests integral CRT polynomials and $A'(1)=0\pmod d$. The correct counting polynomial has $A(1)=p$, and its derivative condition comes from the product of roots of $X^p+X-1$, which is one for odd $p$. For a wrong root $\xi$, integrality forces the norm of $(X^d-1)/\Phi_d$ to divide the norm of $(1-\xi)E_d$. Since $p\nmid d$, the norm of $E_d$ is coprime to $d$. A conductor with two distinct prime factors rules out every wrong root by incompatible norm divisibilities. A prime-power conductor here is a power of two, leaving only $-1$; its derivative changes by $(d/2)p\ne0\pmod d$. Thus the supplied argument does resolve the residual root under the stated hypotheses. This audit found no failed case, but it remains an unrefereed adaptation.

The recursion stops directly when $n\le2K$. Otherwise its odd grid has spacing $2K$, $z=aK-1$ lies within $K$ of $n$, and
$z!=(-4)^{z/2}\rho(E_a)((z/2)!)^2$. The child is less than $3n/4$; each correction has length at most $K$. Fixed $q$ saves only a constant in the interval term.

Concrete controls distinguish valid divisibility from admissibility. At $p=23$, $q=3$ divides $p+1$ but violates $q\ge4$; $q=4$ also divides it but has even quotient six and fails. The admissible choices are eight and 24. At $p=17$, six and 18 are admissible; the first target lies in the direct stopping range for six. Twenty exact trace-one controls at five primes test both binomial identities, proper-conductor values, polarization, ideal support and unique orientation. Enumeration of $\mathbb F_{p^2}$ is charged as a toy control, not as the fast algorithm.

## Cubic conductors, reduction maps and lattice certificates

For this progression $p^2+p+1\equiv1\pmod3$. Consequently the index factor three never occurs; removal changes nothing. For every nontrivial $d\mid q\mid\Phi_3(p)$, $\gcd(d,p-1)=1$: any common divisor divides three, which is absent. Also $p^3\equiv1\pmod d$ and $p\not\equiv1\pmod d$, so $\operatorname{ord}_d(p)=3$. This checks composite conductors as well as primes. It also shows $p\nmid q$, so local cyclotomic reduction is unramified.

Choose $\eta_q$ of exact order $q$ in $\mathbb F_{p^3}$; fix $\rho_q(\zeta_q)=\eta_q$. For every $d\mid q$, use $\eta_d=\eta_q^{q/d}$, $\zeta_d=\zeta_q^{q/d}$ and $\chi_d=\chi_q^{q/d}$, with $\rho_d(\chi_d(x))=x^{-(p^3-1)/d}$. The reduction maps must restrict to one another; independently choosing roots at each conductor would not certify this condition.

Let $\Theta_d=J_{p^3}(\chi_d,\chi_d^{p-1})$. The three characters are nontrivial. Gauss–Jacobi and Frobenius invariance give
$\sigma_u(\Theta_d)=G_{p^3}(\chi_d^{(p-1)u})$, and $\Theta_d\bar\Theta_d=p^3$. For a requested $a$, reduce to $d=q/\gcd(a,q)$, $a'=a/\gcd(a,q)$, and use $u=a'(p-1)^{-1}\pmod d$. An automorphism with a nonunit index at the original conductor would be invalid.

If $aD=pA+B$, $1\le B\le A<p$, set $y_0=B-1$, $y_1=A-B$, $Y=A-1$. The exponent $a(p^3-1)/q$ has digits $(p-B,p-1-A+B,A-1)$, whose sum is $2(p-1)$. With the convention

$$
G_{p^3}(\chi_q^a)\equiv-p^2U_a\pmod{\mathfrak p^3},
\qquad \binom{A-1}{B-1}=(-1)^{A-1}U_a^{-1}\pmod p,
$$

the sign follows from $\pi^{p-1}=-p$ and Wilson reflection. Obtaining the unit requires precision $p^3$, not reduction of the vanishing Gauss sum directly modulo $p$. At arbitrary conductor-family primes the valuations range from zero to three; correct ideal construction and compatible local precision are part of recovery.

The lattice $pA+B\equiv0\pmod D$ has determinant $D$ and Eisenstein rotational symmetry. A short vector $v$ and its rotation $(B-A,-A)$ are independent, of lengths $O(\sqrt D)$. Rational coefficient rounding near $(n+1,n/2+1)$ gives numerator and two denominator factorial indices with deviations $O(\sqrt D)$. One recursive factorial and short ratios give the rest. The code implements exact two-dimensional Gauss reduction and records an explicit coordinate rounding bound $E$, determinant, digits, conductor and the stopping condition $E\ge p/24$ or $n\le24E$. It supplies geometry and prerequisites, not the unknown $U_a$.

This stopping test matters at modest inputs. For $p=10007$, $q=7,31,217$ all stop directly with this certified rounding routine. The larger divisors permit recursion but have enormous reconstruction dimensions relative to the small factorial. A small $D$ alone is not a speed certificate. At $p=20021,q=7927$, the recorded bound is $E=147$, and the top level can recurse; this remains an arithmetic possibility, without a recovered algebraic family or a practical advantage.

The 142 exact local-unit controls include $p=11,q=133$, a composite conductor with lower-conductor requests. They build a full field logarithm table, enumerate binary Jacobi sums, Hensel-lift the compatible root, evaluate modulo $p^3$, check all selected-conjugate ideal valuations and compare the normalized unit with direct binomial coefficients. Orientation enumeration is capped at $q\le19$; larger-conductor rows explicitly contain null orientation results. None of these operations represent the fast reconstruction algorithm or its asymptotic bound.

## Full costs and contracts

| Component | Work that must be charged |
|---|---|
| Divisor provision and discovery | Check divisibility, certify the factorization used for exact-order tests, enumerate/select appropriate divisors or charge a search. Input $q$ is different from input $p$ alone. The code's bounded trial division is a correctness control, not the asymptotically fast setup. |
| Finite-field and character preparation | Certify the irreducible defining polynomial, construct an exact-order root, test $\eta^{q/d}\ne1$ for each prime divisor $d\mid q$, fix the compatible character/prime pair, and restrict it at every conductor. Full logarithm tables are unnecessary for the theoretical recovery algorithm and are forbidden as an uncharged setup. |
| Algebraic recovery | Construct cyclotomic bases and conjugation, selected prime ideals and their orbit exponents, HNF ideal descriptions, polarization, a polarized generator and the residual-root orientation using proper conductors. Store output in the representation actually guaranteed by the algorithm. |
| Local evaluation | Account for coefficient denominators, Galois action, local-unit prerequisites, Hensel precision, negative exponents and valuation removal. Split binary factors are units at the selected prime; cubic Gauss sums first vanish modulo $p^2$. |
| Factorial assembly | Compute the base factorial, interval products, recursion and their inversions; count one recursive child, not two independent large factorial calls; include all logarithmic levels. |
| Cartier–Miller output | Charge the prefix, constant boundary arithmetic, final weighted sum and certificate checks. Reading a cached prefix does not constitute a complete run. |
| External validation | Direct factorial, original recurrence and direct binomial references are linear or slower and must be charged if run for every performance query. The theorem's normal computation validates its construction, not its output by recomputing a linear reference. |

For $q=p^{\theta+o(1)}$, the claimed split and plus exponents are
$\max(c\theta,(1-\theta)/2)$ and $\max(C\theta,(1-\theta)/2)$, respectively. Their balances are $\theta=1/(2c+1)$ and $1/(2C+1)$, with exponents $c/(2c+1)$, $C/(2C+1)$. The cubic exponent is $\max(c_3\theta,1/2-\theta/4)$, balanced at $\theta=2/(4c_3+1)$, with exponent $2c_3/(4c_3+1)$. Positive savings require growing divisors and $c\theta,C\theta,c_3\theta<1/2$. These symbolic statements cannot be turned into numerical windows without a justified reconstruction exponent.

From $p$ alone, rigorous expected complete factorization of any fixed-degree $p$-polynomial integer costs $p^{o(1)}$, using Lenstra–Pomerance's established expected subexponential theorem. Factor verification and primality certification have polynomial bit costs. With the factors supplied, Tal's trimmed-list method finds divisors close to the symbolic optimum in polynomial input time. Thus a from-$p$ split or plus contract has expected total cost $p^{o(1)}+\widetilde O(q^c+\sqrt{p/q})+P(p)$, using its own appropriately enlarged reconstruction exponent; the cubic contract similarly has $p^{o(1)}+\widetilde O(q^{c_3}+D^{1/4})+P(p)$. These statements are conditional on finding a divisor in a useful window and the relevant Tal theorem. They include field/character and compatible-reduction preparation in the polynomial conductor term. This justifies expected setup asymptotically; it does not describe a competitive practical factoring implementation or remove the requirement that a useful divisor actually exist. Alternatively, narrow-window density searches can use deterministic trial scanning, charged as described below. Tal's separate deterministic split setup is part of his Theorem 1.1; this audit does not independently re-prove its least-power-nonresidue bounds.

For interval and prefix work, $M_{\mathbb F_p}(s)$ means field operations for degree-$s$ polynomial multiplication. General product trees give $O(M_{\mathbb F_p}(\sqrt K)\log K)$ field operations and approximately square-root workspace up to logarithms. Fixed-rank extensions change scalar arithmetic by a constant depending on their rank. With quasi-linear polynomial arithmetic and represented $b$-bit field elements this gives the soft bit bounds in the table; a direct $b$-bit modular operation costs at most quadratic bits classically. The reconstruction terms instead count integer lattice and number-field bit work. Dividing their bit cost by $b$ does not produce a justified $\mathbb F_p$-operation count.

A more faithful mixed field-work statement is $R_{\rm bit}(q,p)$ reconstruction bits, plus $\widetilde O(\sqrt{p/q})+O(\log p)$ field operations for split/plus assembly, or $\widetilde O(D^{1/4})+O(\log p)$ for cubic assembly, plus the separately stated setup. Tal guarantees polynomial-in-$q,b$ recovery space. The interval stage uses roughly $\widetilde O(\sqrt K)$ field elements for split/plus or $\widetilde O(D^{1/4})$ for cubic stages; the recovery's $q^{O(1)}b^{O(1)}$ bits can dominate. No $\widetilde O(\sqrt p)$ bound is asserted for the entire reconstruction memory. Ideal descriptions have rank-$\phi(q)$ integer bases, potentially $\phi(q)^2$ entries, and a dense order action can require $\phi(q)^3$ entries. Operand size includes conductor and ideal height, not just $\log p$.

## Uniform refinement audit

Tal's Proposition 4.3 claims
$O(\sqrt p(\log p)^{3/2}\sqrt{\log\log p})$ deterministic bit operations. Relative to the cited $O(\sqrt p(\log p)^2)$ BGS bit bound, the factor is $\sqrt{\log p/\log\log p}$. It is a logarithmic improvement and retains exponent $1/2$.

Modulo $p$, splitting an interval into even and odd integers gives

$$
\prod_{a<j\le b}j
=2^{b-a}\left(\prod_{\lfloor a/2\rfloor<j\le\lfloor b/2\rfloor}j\right)
\left(\prod_{\lfloor(a+p)/2\rfloor<j\le\lfloor(b+p)/2\rfloor}j\right).
$$

The lifted version preserves shifts $z/2$ and $(z-1)/2$ modulo $p$, as $2(y+p(z-1)/2)\equiv2y-p+pz\pmod{p^2}$. The 199 halving controls independently verify these identities and their full routed products modulo $p^2$, using artificial small parameters and direct products.

Tal routes the permutation $T(x)=x/2$ for even $x$ and $(x+p)/2$ for odd $x$. A branch stops on entering a prefix of length $H=\lfloor p/2^h\rfloor$. A surviving rational $y/p$ avoids $h$ consecutive zero bits during repeated doubling. The expected waiting time for a run is $2^{h+1}-2$. Markov's inequality on independent blocks of length $4\cdot2^h$ gives Tal's remaining-length bound; discretization contributes the extra $2^t2^h$ term. This use of binary strings is a counting argument, not an assumption that the particular residues of a given prime are independent random samples.

The stopped endpoints are evaluated with BGS Theorem 15. Its relevant hypotheses are degree-one fixed-size recurrence, an inverse of the specified auxiliary product, units through at most $2\sqrt H+1<p$, and fewer than $H^{1/2-\epsilon}$ requested endpoints. Tal uses at most $H^{3/8}$, safely below $H^{2/5}$ for $\epsilon=1/10$, and charges the auxiliary inverse. Its remaining intervals are batch-evaluated with monic remainder trees, so ring divisions introduce no hidden nonunit assumption. The distinct endpoint count and length estimates provide the logarithmic saving. The audit found no violation of those hypotheses; the full asymptotic theorem remains unrefereed.

The literal parameter rule is $t=\lfloor b/4\rfloor$ and the largest power of two no greater than $t/(128\lceil\log_2(t+2)\rceil)$. The first $t$ allowing this power to be at least two is 3,072, corresponding to $b\ge12,288$. This is only a necessary condition, not a practical crossover: the endpoint-count and unit conditions still need checking. Every 64-bit input triggers its ordinary fallback. Tuned parameters could change actual performance but would require a new implementation and full-output benchmark. The published asymptotic theorem supplies no measured advantage at this project's prime sizes.

Assuming Tal Proposition 4.3 and the retained prefix theorem, the complete rounded-third output therefore has the same deterministic bit bound plus $P(p)$. This is the bounded universal theoretical fallback established by the transfer, without a universal positive exponent saving.

## Density within p congruent to 2 modulo 3

A general-prime density theorem cannot simply be divided by two. The following arithmetic-progression adaptation of Tal Proposition 1.7 supplies the missing justification for its narrow windows. It is an unrefereed derivation in this audit, based on classical distribution theorems; no wider-window independence heuristic is asserted.

Fix $t$ distinct odd prime-power indices $r_i$ and fixed valid reconstruction exponents $c_i$. For primes in $[X,2X]$, freeze candidate prime windows
$(2X)^{1/(24tc_i)}\le\lambda\le X^{1/(12tc_i)}$, excluding all primes dividing $3\prod r_i$. Let $\Omega_\lambda$ be the union of residue classes of exact orders $r_i$ for active windows. Distinct orders are disjoint. The prime number theorem in each fixed progression $\lambda\equiv1\pmod{r_i}$, which follows from the Siegel–Walfisz statement in Vaughan §1, gives by partial summation a reciprocal-prime mass $(\log2)/\phi(r_i)+o(1)$ in its window. Multiplying by its $\phi(r_i)$ order classes and summing gives
$\sum_\lambda |\Omega_\lambda|/(\lambda-1)=t\log2+o(1)$, and the largest summand tends to zero.

For a product $Q$ of $j\le4t$ distinct candidate primes, $Q\le X^{1/3}$ and $3\nmid Q$. Each selection of order classes has, by CRT, a unique reduced class modulo $3Q$ with $p\equiv2\pmod3$. Its expected prime count is the interval logarithmic integral divided by $\phi(3Q)=2\phi(Q)$. The denominator, the number of primes in the target progression, has main term one half of the same interval logarithmic integral. These halves cancel, leaving exactly $\prod_{\lambda\mid Q}|\Omega_\lambda|/(\lambda-1)$.

The Bombieri–Vinogradov maximum-over-reduced-classes bound applies to $3Q\le3X^{1/3}$, well inside its range. Distinct unordered candidate sets give distinct moduli $3Q$; the number of residue choices is bounded by a constant depending on the fixed indices and $j$. Summing the errors, followed by partial summation, gives $o(X/\log X)$. After conditioning on the target progression this remains $o(1)$. Hence, for the count $Z$ of successful candidate factors,

$$
\mathbb E_{p\equiv2\ (3)}\binom Zj=\frac{(t\log2)^j}{j!}+o(1),\qquad 0\le j\le4t.
$$

Even Bonferroni truncation gives
$\Pr(Z=0\mid p\equiv2\pmod3)\le2^{1-t}+o(1)$, exactly as in Tal's final finite-moment argument. Each success yields, conditional on its factorial theorem, a saving of at least $1/(48t\max_i(c_i\phi(r_i)))$. Scanning integers to $p^{1/(12t)}$ detects every candidate success, and this search cost is below that factorial exponent. Fixed-rank Las Vegas setup is also absorbed after conductor certification.

Choosing $t$ sufficiently large for a given $\epsilon$, and summing dyadic intervals with a smaller error margin, gives at least a $1-\epsilon$ fraction of primes in the target progression for sufficiently large bounds, conditional on the relevant factorial algorithms. This concerns a finite collection of fixed cyclotomic indices. For $r=3$ alone, the displayed $t=1$ bound is trivial and proves no almost-all statement. The more attractive wider divisor windows remain outside this argument. No computational density extrapolation is made from the small certificates.

## Evidence and reproducibility

The input zip was preserved byte-for-byte. `python verify_handover.py` passed all 24 recorded hashes and six smoke primes. The supplied small reference script was then run at limit 1,000 and newly passed 85 primes. That script rewrites its result/environment files in the extracted working copy; the original uploaded archive was not altered. These 85 controls overlap the expanded run and are not added to its prime count. The note's historical 1,136-prime evidence was not supplied and has not been adopted as reproduced evidence.

| New evidence file | Scope |
|---|---|
| `results/exact_small.csv` | All 336 target primes through 5,000; original $t_i$ recurrence, unreduced integer central binomial generation, direct factorial, both endpoints, inverse cube and Miller prefix |
| `results/exact_heldout.csv` | Same complete-output checks at 10,007, 20,021, 50,021 after small controls passed |
| `results/applicability_certificates.csv` | 3,334 valid split entries, 2,101 valid plus entries, 4,598 failed plus entries and 1,936 valid cubic entries; compatible algebraic recovery data explicitly absent |
| `results/split_identity_controls.csv` | 43 multifold identity controls, signs, orientation, norm and binary ideal support |
| `results/trace_one_controls.csv` | 20 trace-one identities, proper conductors, root orientation, norm and ideal support |
| `results/r3_identity_controls.csv` | 142 cubic normalized units, digits/signs, compatible local lifts, ideal valuations and nonprimitive requests |
| `results/halving_identity_controls.csv` | 199 full modulo-$p^2$ routed-product identity checks; artificial small parameters |
| `results/uniform_parameter_controls.csv` | Literal fallback parameters and necessary size threshold; not a benchmark |
| `results/validation.json`, `results/environment.json`, `results/run.log` | Counts, degeneracy values, platform, Python version, command, no random seed and no benchmark claim |
| `SOURCE_RECORD.json`, `SHA256SUMS.json` | Input/primary-source provenance and byte hashes; generated-file manifest |

The small run contains 168 split and 168 nonsplit quadratic cases for $\sqrt2$. No split-algebra restart occurred in this range. Dense expansion of the entire cubic power was performed at the 26 target primes through 251, independently verifying $H,K,T$. Algebraic tests compare exact identities; numerical agreement does not prove the recovery theorem or its costs.

Run these commands from the package root with Python 3.12 or newer. No third-party package is required.

```bash
python code/audit.py validate --limit 5000
python code/audit.py complete 17
python code/audit.py complete 50021
python code/audit.py certificate 23 plus 3
python code/audit.py certificate 23 plus 8
python code/audit.py certificate 20021 r3 7927
python seal.py --check
```

The CLI limits its reference and certificate prime inputs to 1,000,000, since trial division and the complete routine are deliberately bounded. `validate` regenerates environment bytes and evidence; after regeneration use `python seal.py` to seal a new manifest. `seal.py --check` checks the delivered bytes without rewriting them. The copied retained `elliptic_prefix.py` hash equals the input code hash. Every complete call computes setup afresh; no cached timing is reported.

## Concrete next scope

The missing engineering component is a polynomial-time polarized-generator recovery implementation in the representations required by Lenstra–Silverberg, followed by exact root orientation and local evaluation. The bounded audit established its mathematical applicability; it did not establish that building that backend fits an unspecified practical budget. No full recovery backend was initiated.

The next manageable target is a split binary-Jacobi recovery pilot with conductors capped at $\phi(q)\le32$, certified prime ideals, exact polarization and proper-conductor orientation. Its acceptance condition should be independent agreement with the existing enumeration controls and preservation of complete $(B_L,a_L,U)$ outputs. Implementing ordinary shortest-vector search may be useful for small fixed dimensions, but its output must remain a fixed-dimension prototype and its cost must not be attributed to Tal's polynomial-time method. Before claiming Tal complexity, implement or integrate the actual polynomial polarized-recovery algorithm and derive a concrete exponent from its representation and operations.

A separate, smaller project could implement the uniform routing planner together with BGS selected-term evaluation and batched interval products. That would avoid algebraic-number recovery, but at modest primes a tuned implementation must demonstrate complete-run benefit against ordinary BGS. It should not begin with the literal 12,288-bit threshold as a practical performance target.

Any future benchmark should log divisor discovery/factorization, field/character preparation, recovery, local precision, recursive products, prefix and final validation separately while comparing identical outputs. Record both uncached complete runs and cached-query runs, peak memory, operand sizes, source hashes, platform and randomness. Published manuscript timings provide no evidence about this backend.

The present outcome is a conditional theoretical transfer with validated prerequisites, identities and a correctness reference implementation. The rounded third point remains incomplete in the claimed fast implementation sense. There is no documented counterexample to the audited identities, no universal exponent saving, no polylogarithmic algorithm, no new CM-trace formula and no novelty claim.

## References and source review

Tal, Y. (2026). *Computing modular factorials below the square-root barrier* (ECCC TR26-211). https://eccc.weizmann.ac.il/report/2026/211/. Official record checked; official PDF byte-identical to the supplied PDF. Theorem 1.1, Theorems 1.3/1.5, §§2–5, Proposition 1.7 and Appendices A–D/G/H were audited for this modulo-$p$ task. Precision-power extensions were not fully audited. Unrefereed report, not accepted published machinery.

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793. Author-hosted published PDF read at https://mathexp.eu/bostan/publications/BoGaSc07.pdf; selected-term Theorem 15 and its unit, inverse, count and memory conditions checked.

Lenstra, H. W., Jr., & Silverberg, A. (2019). Testing isomorphism of lattices over CM-orders. *SIAM Journal on Computing, 48*(4), 1300–1334. https://doi.org/10.1137/17M115390X. Author preprint https://arxiv.org/abs/1706.07373 read; Theorem 1.3, representation requirements and the polynomial-time recovery argument inspected. Published metadata cross-checked, but no explicit polynomial degree was extracted or invented.

van Wamelen, P. (2002). Jacobi sums over finite fields. *Acta Arithmetica, 102*(1), 1–20. https://doi.org/10.4064/aa102-1-1. Publisher PDF read at https://www.impan.pl/shop/en/publication/transaction/download/product/83146. Theorems 3, 8–9 and §7 checked; character convention converted to Tal's inverse character and inverse prime indexing.

Gross, B. H., & Koblitz, N. (1979). Gauss sums and the p-adic Γ-function. *Annals of Mathematics, 109*(3), 569–581. https://doi.org/10.2307/1971226. Original scan read, including printed pp. 570–571 and Theorem 1.7, from https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/gross_koblitz.pdf. The original leading-minus convention was tracked when using Tal's positive Gauss sums. The full proof was not re-proved.

Lenstra, H. W., Jr., & Pomerance, C. (1992). A rigorous time bound for factoring integers. *Journal of the American Mathematical Society, 5*(3), 483–516. https://doi.org/10.1090/S0894-0347-1992-1137100-0. Original first-page theorem visually checked at https://www.cs.umd.edu/~gasarch/TOPICS/factoring/rigorous.pdf. Expected $L_N[1/2,1+o(1)]$ factorization is a classical theorem; no practical backend was benchmarked.

Vaughan, R. C. (n.d.). *The Bombieri–Vinogradov theorem* [Lecture notes]. https://personal.science.psu.edu/rcv4/Bombieri.pdf. Section 1 maximum-over-reduced-classes and Siegel–Walfisz statements checked for the fixed-modulus-three adaptation. The reciprocal-prime mass used above follows by partial summation in fixed progressions; no new claim about wider windows is derived.

Jordan, D. (2026). *Cartier–Miller manuscript* (supplied 5 October PDF), *Rounded third boundary note* (9 October), and *Rounded third research handover* (10 October) [Unrefereed AI-assisted project materials]. Local source hashes identify the supplied versions. Equation (32)–(35) definitions, prefix code, branch note and updated depth-three state read. Repository URL and commit were absent; GitHub was not inspected.
