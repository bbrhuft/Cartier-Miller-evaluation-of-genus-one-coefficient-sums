# Cancellation-aware local extraction at an elliptic branch

David Jordan research study, 18 October 2026. AI-assisted and unrefereed. No publication, priority, general impossibility, or cryptographic consequence is claimed.

## Outcome

This investigation did not find fast signed-scale acquisition. It produced a precise description of the cancellation in the supplied smooth branch chart, an explicit formal-group coordinate conversion, an executable adaptive local representation, and an exact account of where that representation needs a long jet. The adaptive representation acquires the correct scalar, but still requires precision proportional to p. It does not improve on factorial acquisition.

The most useful project-specific result is the following concentration theorem. For the neighboring-index recurrence used to compute f_(2p)(s;t,1/4), every positive-index nonterminal division state is a unit. The constant term of every nonterminal recurrence subtraction is nonzero. At the final even recurrence, two units L and R both have constant 1/4 and agree through degree (p−1)/2. Their normalized difference has first coefficient

$$[t^{(p+1)/2}](L/R-1)=-4s^{(p-1)/2}c_p.$$

Thus a leading-term state does not encounter a sequence of progressively harder division-state cancellations. It reaches one high-contact terminal pair. Knowing its common unit, valuation, and exact contact order still leaves its residual amplitude undetermined in the explicitly defined generic-pair interface. This is not a lower bound for representations that exploit the entire distinguished recurrence.

The formal-group calculation identifies the coordinate conversion completely at leading order: translation by the moving two-torsion point gives w=q/(3s²)+O(q³), for w=−x/y. Its leading Jacobian is cheap. In this coordinate the desired amplitude is the first parameter derivative of the degree-p formal multiplication coefficient. Consequently, for this explicit translation, the unresolved scalar is in the formal multiplication law rather than in an unspecified chart Jacobian. This is a reduction, not an acquisition algorithm.

## Evidence classes and inputs

The attached archive and prompt were read locally. Its delivered manifest audit passed before any evidence was regenerated. Both baseline modes passed, at development inputs 11,17,23,29 and handover confirmation inputs 41,47. These are checks of the inherited references, not confirmation of a compressed mechanism. The original uploaded archive remains unchanged and is included in the reproducibility bundle.

The retained branch argument was checked at its dependencies: smoothness, relative Frobenius coordinates, the fixed differential, the trace-zero special fiber, local regularity, and the differential normalization. The complete-deformation statement and restricted lower bound in Sol's report, and the index-polynomiality and restricted shift comparison in Opus's revision, were inspected as project inputs. Neither report was used as a general impossibility theorem. The proofs needed for the local conclusions are given below. No claim here relies on the unaudited sigma-recurrence suggestion or on a formal-moduli normal-form oracle.

Throughout, p=6k+5≥11 is supplied as a certified prime; h=(p−1)/2, m=(p−2)/3, B=1/4, and s³=−B in F_p. The cube map is bijective, so s=(−B)^((2p−1)/3). This is a charged scalar exponentiation. The target is numeric c_p in F_p, including its sign. A factorial expression is used only for mathematical identification, independent validation, and explicitly charged comparators.

The classification of results is as follows.

| Statement | Status and dependency |
|---|---|
| Division-polynomial recurrences and chain rule | Established background; conventions checked against primary sources |
| Hasse normalization, relative Frobenius and duality | Established background in the specified differential basis |
| G_t(s)=c_p t+O(t²) and branch error coefficient c_p²/(3s) | Retained project theorem; locally rederived here |
| Signed multiplier normalization | Independently rederived here from the chain rule |
| Two-torsion restriction of f_n | Elementary specialization of classical division polynomials; proved here, no novelty claimed |
| Concentration at the terminal unit pair and its smooth-chart ratio | Derived here from the restriction and retained branch theorem |
| Generic-pair interface ambiguity | Proved here in its explicitly limited model |
| Explicit torsion translation and leading Jacobian | Derived here from the addition law; constituent identities are classical |
| Adaptive prefix extractor | Proved correct; executed, but not fast |
| Polylogarithmic or uniform sub-square-root acquisition | Open; not obtained |

## Fixed geometric and sign conventions

The family is E_t:y²=z³+tz+B over F_p[[t]], with invariant differential dz/(2y). Its discriminant has nonzero constant because p≠2,3 and B≠0. Relative Frobenius is (z,y)↦(X,Y)=(z^p,y^p), into Y²=X³+t^pX+B. Verschiebung is V_t(X,Y)=(Φ_t(X),YG_t(X)). The parameter t is not replaced by t^p in the target equation E_t.

For H(t)=[z^(p−1)](z³+tz+B)^h the standard Cartier normalization gives

$$V_t^*\frac{dz}{2y}=H(t)\frac{dX}{2Y},\qquad
\partial_X\Phi_t=H(t)G_t,$$

$$\Phi_t^3+t\Phi_t+B=(X^3+t^pX+B)G_t^2.$$

To see the coefficient convention, write dz/(2y)=(z³+tz+B)^h dz/(2y^p). Relative Cartier selects the coefficient of z^(p−1); the cubic power has degree below 2p−1, so no other selected term occurs. Duality with Frobenius fixes the same scalar in the tangent of Verschiebung. This fixes H, rather than an unspecified root, power or reciprocal of H.

At t=0, cubing permutes F_p, so the quadratic-character sum of z³+B is zero. The Frobenius trace is zero, its characteristic equation is π²+[p]=0, and V_0=−π. Thus Φ_0(X)=X^p and G_0(X)=−(X³+B)^h. This uses no numerical point-count input.

Counting the monomials contributing to the coefficient linear in t gives

$$H(t)=ct+O(t^2),\qquad c=\frac{h!}{m!k!}B^k\ne0.$$

Indeed a monomial with one tz factor must have m cubic factors and k constant factors. All factorial arguments are below p. Wilson reflection also gives c=2(m!)^(−3). One explicit check of that reduction is (4k+3)!=1/m!, followed by separating even and odd factors and reflecting the latter: h!(m!)²=2·4^k k!. This identification does not supply c to the acquisition code.

Let r(t) be the root of r³+tr+B=0 with r(0)=s. The derivative 3s² is a unit, so r exists uniquely and r=s−t/(3s)+O(t²). Write Φ_t=X^p+tφ_1+O(t²) and G_t=−F_0^h+tg_1+O(t²), F_0=X³+B. Regularity near X=s follows from the multiplication denominator being a unit, as proved below. The parameter coefficients in the curve and differential identities are

$$3X^{2p}\varphi_1+X^p=-2F_0^{h+1}g_1,\qquad
\varphi_1'=-cF_0^h.$$

Put X=s+u and a_0=3s². Modulo u^p, X^p=s and X^(2p)=s². Since h+1<p, local integration through this degree is unambiguous:

$$\varphi_1(s+u)-\varphi_1(s)
=-\frac{c a_0^h}{h+1}u^{h+1}+O(u^{h+2}).$$

The constant equation gives φ_1(s)=−1/(3s). Comparing degree h+1 in the curve identity gives g_1(s)=c/(2(h+1))=c in F_p. Therefore G_t(s)=ct+O(t²). At fixed X=s the curve identity is

$$F_t(\Phi_t(s))=s t^pG_t(s)^2.$$

Subtract F_t(r)=0 and divide by the unit derivative 3s². This proves the retained exact order and coefficient

$$\Phi_t(s)-r(t)=\frac{c^2}{3s}t^{p+2}+O(t^{p+3}).$$

These deductions check the inherited local theorem; they are not counted as new acquisition.

Use ψ_1=1, ψ_2=2y, f_n=ψ_n for odd n and f_n=ψ_n/(2y) for even n. The plus sign is essential. The chain rule with the outer multiplier 2 is

$$\psi_{2p}(P)=\psi_2([p]P)\psi_p(P)^4
=2y([p]P)\psi_p(P)^4.$$

As a rational identity, dividing by 2y(P) gives

$$M_p(t)=\frac{f_{2p}(s;t,B)}{f_p(s;t,B)^4}
=\frac{y([p]P)}{y(P)}=(st)^hG_t(s).$$

No square root for y is constructed. The identity is obtained generically before restricting to the branch arc. The denominator has constant f_p(s;0,B)^4=1, as the next section proves. Hence

$$e=h+1,\qquad \nu_t M_p=\nu_t f_{2p}=e,\qquad
[t^e]f_{2p}=s^h c.$$

With t=q²/s and P=(s,q), substitution yields y([p]P)=(c/s)q^(p+2)+O(q^(p+4)). The signed quantity c is acquired directly; branch-error squaring, square-root acquisition and sign selection are unnecessary in this implementation.

## The local concentration theorem

For a simple two-torsion point (r,0) on y²=x³+Ax+B, put a=3r²+A. The following restriction identities hold in any characteristic different from 2 and 3:

$$f_n(r)=(-1)^{(n-1)/2}a^{(n^2-1)/4}\quad(n\text{ odd}),$$

$$f_n(r)=(-1)^{n/2-1}\frac n2 a^{(n^2-4)/4}\quad(n\text{ even}).\tag{1}$$

These are polynomial specialization identities, including when the integer coefficient n/2 becomes zero. They do not involve division by n.

Here is a direct proof. At the root, the initial values are f_1=f_2=1, f_3=−a², f_4=−2a³; these follow by replacing B by −r³−Ar in the standard initial polynomials. In the odd recurrence the factor 16(x³+Ax+B)² is zero, leaving one product. Substituting (1) into that product gives its asserted sign and exponent. In the even recurrence f_(2j)=f_j(f_(j+2)f_(j−1)²−f_(j−2)f_(j+1)²), the two possible parities reduce the numerical difference to ((j+2)−(j−2))/2=2 when j is even, or ((j−1)²−(j+1)²)/4=−j when j is odd; the powers of a and their signs give (1). Strong induction proves the identities. This proof works first over Z[1/6] with a simple root and then specializes; reduction modulo p introduces no forbidden denominator.

Apply (1) at t=0, r=s and a_0=3s². Every f_n(s;0,B) for 1≤n<2p is nonzero: the odd formula has no index factor, and the even formula has n/2 between 1 and p−1. Thus all positive-index states needed below 2p are units.

The odd value at n=p is −1. For p≡3 mod4, its exponent (p²−1)/4 is a multiple of p−1 and (−1)^h=−1. For p≡1 mod4, necessarily p≡5 mod12, so the quadratic character of 3 is −1; the same formula gives −1. This gives the required local denominator normalization independently of a factorial oracle. One may alternatively recover its sign using the six-term recurrence at (0,1/2) on the supersingular fiber, but that alternative is not needed here.

Consider the subtraction in a nonterminal division-state update. At odd index, one summand has zero constant from F(s,0)=0 and the other is a unit. At even index n=2j<2p, the difference in the preceding proof is nonzero: it is proportional to 2 or to j, with j<p. Therefore no such division-state subtraction cancels its constant term. This statement concerns the subtraction that defines each division state. It does not assert that every addition inside base-polynomial construction is free of elementary cancellations.

At the terminal even update define

$$L=f_{p+2}f_{p-1}^2,\qquad R=f_{p-2}f_{p+1}^2,\qquad
f_{2p}=f_p(L-R).$$

Formula (1) gives L(0)=R(0). More explicitly the constant of R is

$$R(0)=\frac14(-1)^{h-1}a_0^{3(p^2-1)/4}
=-\frac14 f_p(s;0,B)^3=\frac14.$$

The same holds for L. Both are genuine units, so the following ratio is regular. Since M_p=(L−R)/f_p³ and f_p(0)=−1, the signed normalization above gives

$$L-R=-s^h c\,t^e+O(t^{e+1}),$$

$$\boxed{\frac LR=1-4s^h c\,t^e+O(t^{e+1}),\qquad e=(p+1)/2.}\tag{2}$$

This is the smooth-branch analogue of the supplied cusp-chart terminal ratio. Its sign and constant are different and were derived in this chart. No transition between the cusp algebra and the branch algebra is assumed.

## Defined cancellation-aware state, closure, and first failure

The initial compressed interface stores a node's index and exact recurrence provenance, valuation zero for each unit state, its constant residue, and the final-pair relation L−R∈t^e F_p[[t]] with exact order e. The common unit R may even be retained symbolically. Multiplication of valuations and residues is closed as long as the residual subtraction is nonzero. The preceding theorem proves that this leading-only rule succeeds at every nonterminal division-state update.

It does not close numerically at n=2p. To make the limitation exact, define the generic-pair interface to admit any units L,R with the prescribed constant B and ν(L−R)=e, while forgetting the higher coefficients in their source expressions. Even if R is supplied exactly and all coefficients of L below e are supplied, the residue of L/R−1 is undetermined: for every ρ∈F_p^×, L_ρ=R(1+ρt^e) has the same retained data and exact contact order, but gives residue ρ. This remains true for every fixed prefix precision N≤e. The missing datum is one transverse residual, not merely an unknown valuation.

Equivalently, changing the terminal input f_(p+2) by δt^e changes [t^e](L−R) by δ f_(p−1)(0)², a nonzero multiple, without changing any input prefix below e. Such perturbations need not satisfy the preceding actual recurrence. They prove an interface insufficiency and do not prove that the distinguished circuit has many possible outputs. Retaining an exact DAG preserves its unique answer; the question is the cost of evaluating the needed residual from that DAG.

For example, at p=11 the interface stores L(0)=R(0)=3, e=6 and zero difference through degree 5. The actual missing difference residue is 5; the ratio residue is 9 and c=5. All ten nonzero residual choices are compatible with the generic-pair data. The raw evidence records the actual complete terminal prefixes, the leading-only state, the first failing index, the missing residue and every alternative generic-interface residual.

The implemented repair stores actual prefixes modulo t^N for all requested states. These quotient states have a simple closed update theorem: reduction F_p[[t]]→F_p[t]/(t^N) is a ring homomorphism, the recurrence uses only polynomial operations, and induction on the dependency DAG gives every state correctly modulo t^N. Multiplication is truncated convolution and subtraction is coefficientwise. No division by t^e is allowed to manufacture an unknown coefficient. Only after acquiring N=e+1 does the program read the verified first difference coefficient and multiply by −s^(−h).

The adaptive precision schedule is 1,2,4,…, capped at e+1. Every preceding stage certifies the zero prefix of the numerator but does not determine its unit residue. The final stage acquires it. The sum of acquired prefix precisions is less than 3(e+1), and there are at most ceil(log₂(e+1))+1 stages. A one-pass version starts at e+1. It avoids repeated work but makes no smaller-state claim. Exact expression provenance is represented by O(log p) recurrence states; it is not identified with a computed high coefficient.

This repair supplies additional information through the actual small-index initial polynomials and coefficient arithmetic. It does not obtain a new equation for T from the shift comparisons excluded by Opus's theorem. Sol's fixed-algebra lower bound applies to a different family of inputs and is not invoked. The measured failure of this interface says nothing against other exact identities, adaptive coordinate changes, or more powerful representations of the distinguished recurrence.

## Explicit moving-torsion formal chart

The chart calculation is useful because it locates the unresolved scalar without attributing it to an unspecified normal-form conversion. Put T=(r,0), δ=s−r and a(t)=3r²+t. With q²=st, the curve equation gives

$$q^2=\delta(\delta^2+3r\delta+a).$$

Translation by T is its own inverse. The ordinary addition law gives, exactly,

$$x(P-T)=r+\frac a\delta,\qquad
y(P-T)=-\frac{a q}{\delta^2}.$$

For the parameter w=−x/y at the identity,

$$w(P-T)=\frac\delta q\left(1+\frac{r\delta}{a}\right).\tag{3}$$

All denominators other than the displayed known uniformizer powers are units. Since δ=t/(3s)+O(t²)=q²/(3s²)+O(q⁴), (3) yields

$$w(P-T)=\frac{q}{a_0}+O(q^3),\qquad a_0=3s^2.$$

The inverse translation has y(T+Q)=a(t)w(Q)+O(w(Q)³). The leading coefficient also follows from invariance of dz/(2y): near T it is dy/a(t), while near the identity it is dw+O(w)dw. Thus no unidentified scalar has entered the chart. Only the constant and linear terms of the moving root were needed; they cost O(1) field operations after s is acquired. No extension-field construction or numeric square root is required: q is a formal ramified parameter.

Let [p]_t(w) denote formal multiplication in this same differential basis. Relative Frobenius gives

$$[p]_t(w)=H(t)w^p+\sum_{j\ge2}b_j(t)w^{pj}.$$

At t=0 it is −w^(p²), because [p]=−π². Hence b_j(0)=0 for j<p; the degree-p coefficient is exactly H(t), by the tangent scalar of Verschiebung. Substitute t=q²/s and w=q/a_0+O(q³). The first term contributes (c/s)a_0^(−p)q^(p+2). Terms j≥2 and the special-fiber degree p² term have larger q-order, so no uncharged coefficient of them is required for this leading conversion. Translation back multiplies by a_0; since a_0^p=a_0, it gives c/s as required. The same calculation gives the stated O(q^(p+4)) remainder; the Weierstrass inversion symmetry makes these local y-parameters odd.

This proves that, in this explicit chart, the leading conversion in either direction costs O(log p) scalar work including initial setup. It reduces signed branch acquisition to acquiring the first parameter derivative of [w^p][p]_t(w)=H(t). Naming that coefficient, supplying a height-two deformation parameter whose Jacobian contains it, or constructing a p-typical normal form without costing its scalar does not acquire c. We have not implemented such a new formal-group acquisition method. The independent affine reference verifies the actual arc output without using a division-polynomial recurrence.

## Fully charged complexity model

Let b=ceil(log₂p), μ(b) be the bit cost of a modular multiplication including reduction, M_F(N) the field-operation cost of multiplying length-N polynomials, and M_Z(L) the bit cost of multiplying L-bit integers. The neighboring-index dependency graph has O(log p)=O(b) states and operations. All indices and valuations need O(b) bits, including expressions such as n²; the retained index metadata is polynomial in b. The coefficient representation, rather than the exponent size, dominates the local extractor.

| Method | Cold acquisition work | Cached coefficient storage | Role |
|---|---|---|---|
| Leading-only state with terminal contact certificate | O(b) recurrence ring steps and polynomial-in-b scalar bookkeeping | O(b) residues and O(b²) index bits | Stops at terminal residual |
| One-pass or adaptive unit-pair prefix extractor | O(M_F(p)b), plus O(b²) scalar setup work in the adaptive schedule | O(pb) residues | Correct, linear precision |
| Included schoolbook implementation | O(p²b) field work; O(p²b μ(b)) bit upper bound | O(pb²) bits | Reproducible reference |
| Dense signed multiplier | O(M_F(p)b) with fast series inversion | O(pb) residues | Delivered reference; length h+2 |
| Dense endpoint and moving root | O(M_F(p)b) with fast series arithmetic | O(pb) residues | Delivered reference; length p+3 |
| Prior cusp extractor | O(M_F(p)b), at two length-(k+1) jets per state | O(pb) residues | Completed prior route; retained comparator |
| Linear factorial, then c=2/G³ | O(p+b) modular multiplications | O(1) residues, O(b) bits | Often fastest at these small inputs |
| Generic product/remainder-tree factorial | O(M_F(√p) log p), with usual regularity assumptions | O(√p log p) residues | Included comparator, not optimized BGS shifting |
| Optimized selected-term recurrence methods | Square-root scale under their unit and inverse hypotheses | Square-root scale | Literature benchmark; not newly implemented |

The adaptive schedule recomputes rather than caching all refinement stages. Geometric summation bounds total coefficient work at the same asymptotic order as one pass, with additional setup overhead. It still explicitly acquires Θ(p) precision. The implementation caches all indices rather than recycling a minimal window. The recorded `peak_cached_residue_slots` counts coefficients in cached division states; it is not a measured peak process RSS. Temporary products and the previous stage can add a constant multiple of the same O(pb) bound. Raw arrays, prefix lengths, coefficient copies, normalization scans and arithmetic categories are separately recorded. These counters are not presented as a count of Python interpreter instructions.

The packed implementation uses Kronecker substitution. Each convolution digit has enough bits to exceed N(p−1)². A coefficient slot therefore occupies O(b+log N)=O(b) bits, an operand has O(Nb) bits, and a packed product is charged at M_Z(Nb), together with O(N) packing, unpacking and modular reductions. Across the recurrence and geometric precision schedule the bit upper bound is O(b M_Z(pb)+pb μ(b)), apart from polynomial-in-b scalar setup and index bookkeeping. A packed integer product is never counted as one F_p multiplication. Packing accelerates ordinary dense arithmetic and supplies no algebraic extraction improvement.

Setup computes B and s by charged scalar powering. Final normalization uses charged powering for s^(−h); its exponent is reduced modulo p−1. Scalar negations, exponent construction, residue comparisons and valuation scans have their ordinary bit costs, absorbed in the displayed bounds. There is no series inverse in the paired numerator acquisition, no selected-coefficient oracle, and no free division by a parameter power. The dense signed comparator includes its unit inverse; the branch comparator includes the root computation and all its inversions. The factorial comparators include their normalization. Certification is an explicit input cost, outside the timed modular acquisition regions; the validation runner certifies its small primes separately by trial division.

The auxiliary affine reference keeps finite Laurent expansions with propagated absolute error precision. Addition uses the smaller input precision. Multiplication of quantities with valuations v_a,v_b and precisions N_a,N_b uses precision min(N_a+v_b,N_b+v_a). Inversion of a nonzero series of valuation v and precision N returns precision N−2v, and explicitly computes the inverse unit. Thus its divisions by known uniformizer powers do not hide precision acquisition. This reference is for independent checking, not a proposed fast mechanism or a claimed uniform optimal-precision affine algorithm.

No result here should be extrapolated to 1,201-bit p. A length proportional to p is exponential in b regardless of how compactly its order is written.

## Primary-literature applicability audit

The following primary texts were opened and the named statements or sections examined. This is a targeted applicability audit, not a complete novelty search. Bibliographic descriptions were not substituted for theorem hypotheses.

| Primary source and inspected location | What applies here and what does not |
|---|---|
| Debry (2014), Theorem 1, Proposition 3 and Proposition 4 | The Hasse/division-polynomial coefficient equality and Frobenius support justify coefficient identities. The support proposition is stated for ordinary curves over finite fields; generic-family use must be justified algebraically, rather than applying it to a supersingular special fiber. It is not an acquisition-cost theorem. |
| Doliskani (2018), Section 2.1, equations (3)–(4), neighboring-index algorithm | Uses the same ψ_2=2y and normalized f_n convention. A bounded index window gives logarithmically many operations in the chosen coefficient algebra. A growing modulus degree is charged; it cannot be treated as a scalar operation. |
| Stange (2026), introduction, chain rules, Section 5.1 and Section 7.4 | Divisor, chain and formal-leading-coefficient normalizations are relevant, including inseparable maps. The paper explicitly discusses the even-sign convention; this report independently fixes its plus convention in the multiplier identity. The results read do not supply the deformation scalar's acquisition cost. |
| Stange (2016 preprint), Section 4 and Lemma 10 in Section 5 | The local valuation framework is a close antecedent, but its K is a finite extension of Q_p and formulas use finite v(p). Our valuation is t-adic in characteristic p, where p=0. Those formulas cannot be transferred verbatim. Orders alone do not determine residual amplitudes. |
| Katz (1977), opening setup and invariant-derivation examples | Starts in characteristic zero with residue characteristic p and ord(p)=1. Useful for understanding normalization and derivative divisibility, but not an equal-characteristic signed-residue algorithm. |
| Caruso, Roe, and Vaccon (2014), Section 2.2, Lemma 3.4, Section 4 and Appendix A | Explicitly includes K=k((t)); correlated precision and manifold charts are directly relevant. Lemma 3.4 requires a surjective differential. It tracks images of supplied precision data; it does not compute an unknown coefficient for free. In characteristic p the derivative of a Frobenius power vanishes, and the paper explicitly flags this non-surjective case. This is the closest algorithmic antecedent to preserving relations between paired units. |
| Bostan, Gaudry, and Schost (2007), Theorem 14 and its setup | Provides the selected-term square-root benchmark, with specified integer-unit and supplied-inverse conditions. The included factorial comparator instead constructs generic monic product and remainder trees, with their setup paid. It is not an implementation of the optimized shifting theorem. |

Lubin's foundational formal-group existence results were not used to claim an algorithm; no specific Lubin theorem is asserted here without an audited statement. No independent local-algebra paper was found in this targeted reading that acquires this distinguished amplitude from this circuit at sub-square-root cost. That observation is a limitation of this audit, not a statement that no such work exists.

The main methodological distinction is between preserving precision and acquiring information. Correlation-aware precision can certify that a large common prefix cancels. It still needs a method to acquire the surviving center/residue. The generic-pair example proves exactly this distinction for our interface, without appealing to an unproved global complexity lower bound.

## Exact execution, freezes and reproducibility

Eight development inputs were 11,17,23,29,41,47,53,59. They include the preliminary ratio exploration and affine pilot. The first implementation was frozen and passed confirmation at 71,83,89,101,107,113. During benchmark review, diagnostic constant-formula exponentiations were moved out of production acquisition; their previous cost was included in old timings but absent from the core arithmetic counters. This was a diagnostic-path correction, not a change in the output algorithm or theorem.

A second source freeze records the complete observed-input set, including timing inputs 251,509,1013. After that freeze, its stated selection rule chose 131,137,149,167,173,179, excluding every input observed in this study before that freeze. All six passed. They are not claimed historically unused: in particular some appeared in the inherited reports. The first p=1013 benchmark was interrupted during its slow reference phase and is not a completed final benchmark. Historical v1 sources, evidence and an execution note are retained separately.

Each final confirmation compares both polynomial backends and both refinement schedules against the factorial oracle, dense signed multiplier, dense branch error and an affine group-law implementation that does not call the division recurrence. Every complete division state through 2p is also compared with the unchanged support recurrence; chart coefficients and terminal-interface perturbations are checked exactly. These shared-recurrence checks are distinguished from the independent affine check.

The final confirmed signed scales are as follows.

| p | 131 | 137 | 149 | 167 | 173 | 179 |
|---|---|---|---|---|---|---|
| c_p | 91 | 82 | 22 | 147 | 108 | 76 |

All exact assertions passed. This confirms the implementation and its finite instances; the uniform statements rest on the proofs above. Confirmation of a slow fallback does not confirm a fast compressed acquisition mechanism.

The bundle's README gives commands. `audit_results.py` checks every final frozen source and output manifest. `validate.py --confirmation` regenerates confirmation after checking the source freeze. `local_candidate.py` acquires a signed value from a certified prime without importing or calling a factorial oracle. `affine_reference.py` is the independent local group-law check. `benchmark.py` performs cold timed acquisition and retains all samples and arithmetic metadata. The supplied references and their historical evidence are included for reproduction; the original upload bytes are also preserved.

## Cold-acquisition measurements

All entries below are medians of three complete calls in milliseconds. No fixed-prime context or scale cache is reused. Setup and final normalization occur inside the timed functions. The same Python standard-library modular arithmetic is used throughout; schoolbook and packed multiplication are separated because changing multiplication backends is not an extraction improvement. Tiny factorial times are indicative microbenchmarks, not high-precision performance estimates. Raw individual samples are retained.

| Schoolbook method | p=113 | p=251 | p=509 |
|---|---:|---:|---:|
| Dense signed multiplier | 41.12814 | 222.41574 | 1146.65810 |
| Dense endpoint and branch root | 160.24560 | 840.12479 | 4936.05954 |
| Unit-pair, one pass | 36.27443 | 190.89274 | 1101.03973 |
| Unit-pair, adaptive prefixes | 56.45534 | 277.45559 | 1505.22729 |
| Prior cusp extractor | 10.55315 | 55.70999 | 302.57043 |
| Linear factorial plus normalization | 0.00787 | 0.01095 | 0.01952 |
| Generic block factorial plus normalization | 0.14536 | 0.25958 | 0.48823 |

| Packed polynomial method | p=113 | p=251 | p=509 |
|---|---:|---:|---:|
| Unit-pair, one pass | 3.27099 | 8.30115 | 23.90833 |
| Unit-pair, adaptive prefixes | 10.77591 | 20.56718 | 55.88560 |
| Prior cusp extractor | 3.11017 | 7.52271 | 19.09688 |
| Generic block factorial plus normalization | 0.23985 | 0.31610 | 0.54321 |

At p=509 the packed one-pass local acquisition takes about 23.91 ms, versus 0.543 ms for the packed block-factorial comparator and 0.0195 ms for linear factorial acquisition. The adaptive local version is slower still. The numerator-only simplification saves the dense denominator inverse, but produces no competitive scale-acquisition algorithm. Faster packing relative to the schoolbook reference is ordinary arithmetic acceleration. The linear factorial winning at these small inputs does not refute the asymptotic square-root benchmark.

## One precise next question

Does the distinguished terminal pair admit a recurrence for the acquired residual

$$\mathcal R_p=\operatorname{res}_{t=0}\left(t^{-(p+1)/2}(L/R-1)\right)=-4s^h c_p$$

in a representation of total size o(√p), using the actual initial division-polynomial states and explicitly acquired coefficients, with every transition proved and charged? A useful candidate must define how it obtains this residual when constant terms cancel, and must improve on the factorial comparator after setup. Equivalently, the explicit torsion translation permits studying the derivative of the degree-p formal multiplication coefficient in the fixed differential basis; it does not permit taking that derivative as an input.

The defensible contribution is a local concentration and interface analysis, an explicit leading coordinate conversion, and reproducible exact evidence. It narrows this mechanism's failure to one precise terminal residue. It neither proves nor suggests that all cancellation-aware local algebras fail, and it leaves fast signed-scale acquisition open.

## References

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793. Primary full text: https://mathexp.eu/bostan/publications/BoGaSc07.pdf

Caruso, X., Roe, D., & Vaccon, T. (2014). *Tracking p-adic precision* [Author preprint]. https://arxiv.org/abs/1402.7142

Debry, C. (2014). Beyond two criteria for supersingularity: coefficients of division polynomials. *Journal de Théorie des Nombres de Bordeaux, 26*(3), 595–605. https://doi.org/10.5802/jtnb.881

Doliskani, J. (2018). On division polynomial PIT and supersingularity. *Applicable Algebra in Engineering, Communication and Computing, 29*, 393–407. https://doi.org/10.1007/s00200-018-0349-z. Primary preprint: https://arxiv.org/abs/1801.02664

Katz, N. M. (1977). Formal groups and p-adic interpolation. *Astérisque, 41–42*, 55–65. https://www.numdam.org/article/AST_1977__41-42__55_0.pdf

Stange, K. E. (2016). Integral points on elliptic curves and explicit valuations of division polynomials. *Canadian Journal of Mathematics, 68*(5), 1120–1158. https://doi.org/10.4153/CJM-2015-005-0. Author preprint inspected: https://arxiv.org/abs/1108.3051

Stange, K. E. (2026). Division polynomials for arbitrary isogenies. *Research in Number Theory, 12*, Article 53. https://doi.org/10.1007/s40993-026-00741-2. Author version inspected: https://arxiv.org/html/2503.15428v3
