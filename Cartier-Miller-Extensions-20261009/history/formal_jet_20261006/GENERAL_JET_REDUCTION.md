# General branch: the exact Hasse jet reduction

6 October 2026. Separate research pass; unrefereed, no novelty or speedup claim. The retained cubic report, evaluator, project state, roadmap and precision-two report were read before this pass. The historical Witt residue called K_p is a different object from the coefficient K here. Its sum-first BGS computation is not a derivative oracle. No manuscript changes were made.

## Question and result

Can the missing second-kind coefficient be obtained by a small formal jet of the Hasse coefficient? Yes, exactly. Can such a jet presently be obtained at scalar point-counting cost? This pass establishes no such algorithm.

Let p≥7, F=x³+Ax+B be nonsingular, h=(p−1)/2, and Δ=4A³+27B²≠0 in F_p. Regard

$$H(A,B)=[x^{p-1}]F^h,\qquad \beta(A,B)=[x^{p-2}]F^h$$

as their specified polynomials, not just values of a point-count routine. Formal derivatives satisfy

$$\boxed{\Delta H_A=-A^2H+\frac92B\beta,\qquad
\Delta H_B=-\frac92BH-3A\beta.}$$

These formulas require no inverse of H. If B≠0, then

$$\beta=\frac{2\Delta H_A+2A^2H}{9B};$$

if A≠0, then

$$\beta=-\frac{\Delta H_B+(9/2)BH}{3A}.$$

Nonsingularity guarantees that one reconstruction is available. At a supersingular input H=0 these become β=2Δ H_A/(9B) or β=−Δ H_B/(3A). No ordinary-only division has entered the derivation.

For the original f=1+cw+bw²+aw³, its verified normalization is x=aw+b/3, y=av, A=ac−b²/3, B=a²−abc/3+2b³/27. Hence K=(β−(b/3)H)/a. Once a correct Hasse jet is supplied, conversion and each supplied-root branch query are O(1) field operations.

## Global differential derivation and sign check

Take ω=dx/y and η=xω. Parameter derivatives in the fixed x coordinate are

$$\partial_A\omega=-\frac{x}{2F}\omega,\qquad
\partial_B\omega=-\frac1{2F}\omega.$$

For either parameter t, write u_t,v_t as below and put R_t=−4Av_t/3+2u_tx−2v_tx².

| Parameter | u_t | v_t |
|---|---|---|
| A | −A²/Δ | 9B/(2Δ) |
| B | −9B/(2Δ) | −3A/Δ |

The exact global identity is

$$\partial_t\omega=(u_t+v_tx)\omega+d_x(R_t/y).$$

It follows by clearing F and checking

$$-x/2=(u_A+v_Ax)F+FR_A'-F'R_A/2,$$
$$-1/2=(u_B+v_Bx)F+FR_B'-F'R_B/2.$$

These are polynomial equalities, with no local regularity assumptions omitted. Apply Cartier on the specialized curve over F_p. It kills the exact differential and sends ω to Hω and η to βω. Independently rewrite the left sides as −(x/2)F^{h−1}dx/y^p and −(1/2)F^{h−1}dx/y^p. Degree is below 2p−1, so coefficient selection gives H_Aω and H_Bω, respectively, because h=−1/2 in F_p. This proves the displayed identities without asserting an incorrect commutation of parameter differentiation and absolute Cartier over an imperfect parameter field.

Using ω∞=dx/(2y) instead multiplies every differential and its exact correction by 1/2, preserving the scalar formulas. No κ=−2 from the separate rational-point-origin construction is imported. The branch residue remains zero as in the retained report.

At p=7, H=3B and β=3A² by direct expansion; the identities give H_A=0 and H_B=3. This is a useful independent sign fixture. An initial scratch derivation assigned the wrong sign to both terms in H_B. The exhaustive test and independent parent review caught it before delivery. The corrected global identities are validated separately.

## Why this is not yet a fast preparation algorithm

An exact first-jet oracle for H immediately gives β. Conversely the boxed formulas compute both first derivatives from H and β in constant field work. Thus the two data-preparation problems are equivalent up to constant work once H is available; the reduction has exposed, rather than removed, the missing information.

Automatic differentiation of the coefficient recurrence over F_p[ε]/(ε²) works, but still uses O(p) recurrence steps. Evaluating the same fixed-dimension recurrence by polynomial block products retains the established soft-square-root field-operation cost, with a constant-size jet overhead. No improved bound follows merely from the use of dual numbers.

A numerical trace oracle evaluates H at isolated finite-field inputs. It does not evaluate its prescribed polynomial at A+ε or B+ε. For example at p=13,A=0,B=1, the formal values are H=2,H_B=4, while H(0,2)=8, so the finite difference is 6, not 4. More generally a polynomial can be changed by (B^p−B)G without changing its values on F_p, yet its derivative changes by −G at a rational input. Canonical coefficient-polynomial degree restrictions remove this ambiguity if the polynomial is reconstructed; they do not make two numerical samples into a derivative.

The usual Frobenius step is also sensitive to nilpotents: (B+ε)^p=B in F_p[ε]/(ε²). Simply replacing arithmetic in scalar Schoof with dual-number arithmetic therefore does not prove that its output differentiates H. Any valid family or infinitesimal Frobenius method must account for the different source and Frobenius-twisted target and identify the exact differential normalization. This observation blocks that naive argument, not every possible sophisticated deformation algorithm. We have neither a general lower bound nor a proof that a polylogarithmic jet oracle is impossible.

The CM families illustrate a further trap. At A=0, reconstruction requires H_A, a derivative transverse to the A=0 family; differentiating the closed expression H(0,B) only gives H_B and does not supply it. At B=0, the required H_B is likewise transverse. Thus cheap trace formulas within a special family do not automatically extend its β=0 rule to the supersingular class.

## Checks and current status

`python check_jets.py` checks dense polynomial expansion against both jet identities and both cleared differential identities. It exhausts A,B at every prime 7 through 31, then samples twelve inputs at each prime 37 through 251 with a fixed seed. Singular inputs are excluded; no rational branch restriction is needed for the derivative theorem. Of 3,682 nonsingular cases, 3,316 are ordinary and 366 supersingular. Every identity and reconstruction passed. Validation CSV, environment and source hash are retained. This code intentionally uses slow dense expansion and is not a performance comparator.

The parent independently derived the corrected exact reductions and tested the identities using a multinomial implementation on all 16,288 nonsingular short cubics at primes 7≤p<60, including 1,360 supersingular curves. Its source and results are in the sibling review directory. These test counts overlap; they must not be added as disjoint curve coverage.

| Claim | Status |
|---|---|
| Exact jet identities and reconstruction, including H=0 | Derived by global polynomial identities; unrefereed proof |
| Independent finite checks | Passed; supporting evidence only |
| Extra complete cost after a supplied certified jet | O(1) field work beyond its preparation |
| Direct jet recurrence | O(p), not an improvement |
| Polynomial block jet recurrence | Existing soft-square-root machinery; not implemented in this pass |
| Differentiating scalar traces by a finite difference | Failed; explicit counterexample retained |
| Polylogarithmic uniform jet preparation | Unresolved |
| Novelty | Not asserted; classical Gauss–Manin/Cartier mechanism |

The useful next general question is therefore whether a genuinely algebraic first-jet oracle can be built from normalized Frobenius or prime-to-p torsion data without computing the long coefficient recurrence. It should be evaluated against the identities here, not against a finite difference of traces.

## Verified primary sources

Katz, N. M. (2019 online). On a question of Zannier. Experimental Mathematics. https://doi.org/10.1080/10586458.2018.1551818. Author-hosted published text read at https://web.math.princeton.edu/~nmk/zannier_publ.pdf. Section 1 identifies H and β as first- and second-kind Cartier coefficients; Section 6 gives their separate character-sum computation. This report supplies its own differential derivation rather than claiming the displayed derivative formulas are quoted from Katz. Issue-date metadata were not independently resolved.

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. SIAM Journal on Computing, 36(6), 1777–1806. https://doi.org/10.1137/S0097539704443793. Published author PDF: https://specfun.inria.fr/bostan/publications/BoGaSc07.pdf. Supports the conventional recurrence-products route, not a new jet speedup.

Schoof, R. (1995). Counting points on elliptic curves over finite fields. Journal de Théorie des Nombres de Bordeaux, 7(1), 219–254. https://www.numdam.org/item/JTNB_1995__7_1_219_0/. Its scalar point-counting result does not by itself certify a formal derivative oracle.
