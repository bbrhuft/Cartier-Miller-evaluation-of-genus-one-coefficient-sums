# CM Eisenstein proposal: bounded assessment and research ledger

12 October 2026. David Jordan's Cartier–Miller extension programme. A literature and normalization assessment of the supplied external-AI suggestion. No new evaluator, proof of a general CM reduction theorem, benchmark or manuscript revision is delivered here.

The central connection is credible and worth a bounded follow-up. It is grounded in existing theory, rather than inferred only from the six explicit families. Katz's Sections 1.3 and 5.7 describe the complex antiholomorphic and p-adic unit-root directions using weight-two Eisenstein data, and Comparison Theorem 8.0.9 and Lemma 8.0.13 compare the CM eigenlines at good ordinary reduction. Bruinier, Ono and Sutherland give exact class-polynomial methods for related normalized nonholomorphic CM values. The application to this project's coefficient conventions still requires an explicit reduction proof and an algorithmic cost contract.

## Normalization to check

For E:y^2=x^3+Ax+B put omega=dx/y, eta=x dx/y and h=(p-1)/2. The retained Cartier formulas immediately give

$$\ker C=\langle\eta-(\beta/H)\omega\rangle$$

on ordinary inputs. This is a slope in a chosen basis, not a scalar invariant of j: twisting A,B by d^2,d^3 multiplies beta/H by d. The dimensionless combination A beta/(BH) is invariant under that scaling, when AB is nonzero.

For a complex lattice Lambda=lambda(Z+tau Z), uniformize with x=wp(z), y=wp'(z)/2. Then omega=2 dz and eta=2 wp(z)dz. Write the full-period zeta increments as eta_1,eta_2; their relation eta_1 lambda tau-eta_2 lambda=2 pi i fixes the sign. Subtracting a multiple of the holomorphic period vector so that the remainder is antiholomorphic gives the line

$$\langle\eta+G_2^*(\Lambda)\omega\rangle,\qquad
G_2^*(\Lambda)=\frac{\pi^2}{3\lambda^2}E_2^*(\tau).$$

This calculation uses eta_1/lambda=pi^2 E_2/(3lambda^2) and the correction pi/(lambda^2 Im(tau)). As x,y are normalized above, g_2=-4A and g_3=-4B. Their standard lattice formulas give

$$G_2^*(\Lambda)\frac{A}{B}=
\frac32\frac{E_2^*(\tau)E_4(\tau)}{E_6(\tau)}.$$

Accordingly, the model-normalized comparison to prove after ordinary reduction is

$$\frac\beta H\equiv-\frac{3B}{2A}s_2(\tau),\qquad
s_2(\tau)=\frac{E_2^*(\tau)E_4(\tau)}{E_6(\tau)}.$$

The CM value must be represented exactly, with a specified reduction prime/conjugate and all model and denominator exceptions addressed. Raw E_2^*(tau) alone is a weight-two quantity and must not be called an algebraic j-invariant without period normalization. The displayed comparison is a derived target, not a newly certified all-CM theorem in this assessment.

## The proposed small test

For discriminant -12 use tau=i sqrt(3) and the retained depth-one model A=-15r^2, B=-22r^3. The known transport formula gives beta/(rH)=-1. The proposed comparison therefore predicts s_2(tau)=5/11, and the coefficient multiplier is -11 s_2/5.

An 80-digit Decimal calculation with 39 nonconstant summands gave E_2^* approximately 0.44822039438838143211638545001748524956939220170812073049, s_2 approximately 0.45454545454545454545454545454545454545454545454545454545, and the signed predicted multiplier approximately -1. The difference s_2-5/11 was -3e-80 in the working arithmetic. This is a numerical normalization check, with no interval certification or exact algebraic identification. It is not a proof or performance benchmark.

The calculation is reproducible with Python's standard library:

```python
from decimal import Decimal, localcontext
with localcontext() as ctx:
    ctx.prec = 80
    D = Decimal
    pi = D('3.14159265358979323846264338327950288419716939937510582097494459230781640628620899')
    y = D(3).sqrt()
    q = (-2*pi*y).exp()
    sums = [D(0), D(0), D(0)]
    for n in range(1, 40):
        term = q**n/(1-q**n)
        for k, exponent in enumerate((1, 3, 5)):
            sums[k] += D(n)**exponent*term
    E2 = 1-24*sums[0]
    E4 = 1+240*sums[1]
    E6 = 1-504*sums[2]
    E2star = E2-3/(pi*y)
    s2 = E2star*E4/E6
    print(E2star, s2, s2-D(5)/11)
    print('predicted beta/(rH):', -D(11)/5*s2)
```

## Critical qualifications and next bounded question

The original six non-seed families do not all contain 4(p-1) models: at depths one, two and three the generic distinct-j counts give p-1, 2(p-1) and 4(p-1), at primes where the corresponding family is eligible and nondegenerate. Small overall coverage remains the correct interpretation. The delivered O(p) and square-root-scale recurrence routes are available reference methods, not proved lower bounds for generic K.

Class-number growth, embeddings, denominators and representation size still matter when depth increases. The A=0 depth-three coefficient field is biquadratic, so the blanket statement that the Galois groups remain dihedral is inaccurate unless carefully phrased in terms of generalized dihedral ring class extensions. A new CM-value method could remove the need for an explicit isogeny path at a fixed discriminant; it would not make a growing-discriminant problem constant cost.

Bruinier–Ono–Sutherland's simplest Masser formula excludes discriminants -3d^2. In particular -12 and all the A=0 depth discriminants need the stated special treatment. Thus -12 is a useful normalization control, while -7 or -8 would be a cleaner first additional seed for the non-special algebraic formula. Their algorithmic complexity statements have GRH hypotheses; they do not replace this project's unconditional Schoof setup without a separate argument.

A CM lift preserving the appropriate endomorphisms can provide the canonical lift under suitable ordinary good-reduction hypotheses. That fact alone does not identify a coefficient in a literal polynomial power modulo p^2 or compute the weighted Witt correction. The retained p=13 failures of direct lifting and of a simple unit-root substitution remain genuine obstructions to those particular formulas. The new proposal must not erase those tests.

| Ledger field | Current record |
|---|---|
| Question | Can normalized algebraic CM splitting data recover beta/H directly, without an explicit easy-seed isogeny path? |
| Assumptions to specify | Fixed CM order; good ordinary reduction; p away from order/model/denominator exceptions; specified embedding and exact model; H nonzero. |
| Derivation | Cartier kernel slope; complex full-period/quasiperiod calculation; weight-zero s_2 normalization; Katz CM comparison as the literature route. |
| Independent checks | Corrected discriminant -12 numerical comparison agrees with the retained exact depth-one transport. No new finite-field evaluator implemented. |
| Counterexamples/obstructions | Raw E_2^* is not the desired multiplier; slope is not twist-invariant; generic ordinary finite-field CM orders can have growing discriminant; prior precision-two failures retained. |
| Status | Promising literature-grounded route. Normalized comparison and complete algorithmic theorem not yet delivered. No novelty claim. |
| Recommended target | Prove the normalization/reduction bridge and recover the retained families; then certify one new class-number-one case (-7 or -8), with exact CM values and charged preparation. |

The published manuscript remains unchanged. If successful, this work should first become a separate extension note. The rounded-third p=2 modulo 3 boundary and generic/supersingular K are not resolved by the ordinary CM proposal.

## Primary sources checked

Katz, N. M. (1976). p-adic interpolation of real analytic Eisenstein series. Annals of Mathematics, 104(3), 459–571. Sections 1.3 and 5.7; Comparison Theorem 8.0.9 and Lemma 8.0.13. Author-hosted scan: https://web.math.princeton.edu/~nmk/old/padicinterp.pdf .

Bruinier, J. H., Ono, K., & Sutherland, A. V. (2015 manuscript version). Class polynomials for nonholomorphic modular functions. arXiv:1301.5672v3. Definition (1.2), Theorem 1.1, Lemma 2.3 and the special-discriminant qualifications. https://arxiv.org/abs/1301.5672 .

Masser's 1975 book metadata was verified at Springer, but its full relevant appendix was not directly read in this assessment. Specific claims about its formula were checked through the directly read Bruinier–Ono–Sutherland paper. The cited Cox book was not newly inspected. These access distinctions matter for later proof and novelty review.
