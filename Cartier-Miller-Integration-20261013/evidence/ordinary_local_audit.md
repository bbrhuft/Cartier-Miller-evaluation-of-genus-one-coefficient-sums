# Ordinary Cartier scalar: a bounded local compatibility audit

David Jordan's Cartier–Miller extension programme, 12 October 2026. Separate, unrefereed, AI-assisted proof and feasibility note for independent review. The supplied original feasibility submission and its qualified review were inspected as distinct versions. The requested later repair was not supplied and is not presumed complete. The manuscript, completed extensions and published repository were not changed. Nobody was contacted and nothing was published.

## Outcome and exact scope

No complete cheaper generic algorithm, new restricted fast family or exponent saving was obtained. The useful bounded result is a precise obstruction to a specific proposal: **the directional Gauss–Manin equations, their local jets of order below $p$, and the supplied trace do not select the initial Cartier slope merely by compatibility**. Every proposed initial slope has such compatible jets. Even the exact trace and determinant of an abstract ordinary Frobenius matrix leave its shear free. These are proofs about the enumerated necessary equations, not lower bounds for computing the actual geometric scalar from the curve.

The primary route therefore stops at a missing arithmetic initial condition. Automatic differentiation of a finite-field point-count algorithm does not automatically supply it. The sole secondary route, Katz's first-order Serre–Tate normalization, yields a precise derivative-oracle reduction; acquiring its normalization derivative cheaply remains unresolved. Actual geometric Frobenius, $p$-curvature, higher-order integral structure or global polynomial conditions could add information excluded from the partial local system studied here. This audit does not close those approaches.

The input is a certified prime $p\ge7$, a nonsingular ordinary short model $E:y^2=x^3+Ax+B$ over $\mathbb F_p$, and its certified exact signed integer trace $t$, with $p\nmid t$. Define

$$
h=\frac{p-1}{2},\qquad P=(x^3+Ax+B)^h,\qquad H=[x^{p-1}]P=t\bmod p,\qquad \beta=[x^{p-2}]P,\qquad \kappa=\frac\beta H.
$$

The required basis is $\omega=dx/y$, $\eta=x\,dx/y$. Its unit-root line is $\langle\eta-\kappa\omega\rangle$. With columns representing images, the retained reduction of Frobenius is

$$
\overline M=\begin{pmatrix}0&-\beta\\0&H\end{pmatrix}.
$$

The unit-root interpretation is classical; Katz's Theorem 3.1 and its proof give the relevant normalization. This note offers no literature novelty verdict for the differential identities.

## Candidate decision and dependencies

The following candidates were recorded in `CANDIDATE_DECISION.md` before substantive implementation. Only the primary was developed as a proposed direct extraction mechanism; the secondary was inspected after its dependency obstruction was identified.

| Candidate | Proposed scalar map | Inputs actually supplied | Missing data | Complete status and cost |
|---|---|---|---|---|
| Primary: local directional connection and relative Frobenius horizontality | Select $H'(0)$ from the local differential equations and return $H'(0)/H(0)$ | $p,A,B,t$ and the explicitly computed connection | Initial $H'(0)=\beta$ or a computable additional arithmetic selection condition | The connection is cheap; the audited equations admit all $p$ initial slopes. No complete acquisition algorithm survives. |
| Sole secondary: Katz-normalized Hodge section | If the section is $a\omega$, return $-\vartheta(a)/a$ | Curve, trace, connection; the canonical value $q=1$ if independently obtained | The derivative of $a$ in the specified basis, or the actual Frobenius-fixed section | Constant-size extraction from supplied normalization data; their acquisition cost remains unresolved. A first-order Kodaira–Spencer projection supplies no slope by itself. |

Neither candidate assumes that a full torsion orbit is universally mandatory. The issue is the missing conversion datum of these particular constructions.

## Coefficient certificate and the local connection

Put $\vartheta=6B\partial_A-(4/3)A^2\partial_B$ and $R=2x^2+4A/3$. Direct algebra gives $\vartheta F=6xF-RF'$ and therefore $\vartheta P=6hxP-RP'$. Extracting $x^{p-1}$ yields the retained exact characteristic-zero certificate

$$
\vartheta H=(p+1)\beta-\frac{4p}{3}A[x^p]P.
$$

All denominators are permitted at $p\ge7$, so reduction gives $\vartheta H=\beta$. This is equivalent to the dual-number jet $H(A+6B\varepsilon,B-(4/3)A^2\varepsilon)=H+\beta\varepsilon$.

A further coefficient calculation supplies the normalized second-order equation. Let $\gamma=[x^{p-3}]P$. Extracting $x^{p-1}$ from $FP'=hF'P$ gives, modulo $p$, $AH+3\gamma=0$. Extracting $x^{p-2}$ from $\vartheta P=6hxP-RP'$ gives $\vartheta\beta=3\gamma+(4A/3)H$. Thus

$$
\vartheta\beta=\frac A3H,\qquad \vartheta^2H=\frac A3H,\qquad \vartheta\kappa=\frac A3-\kappa^2.
$$

The first two are polynomial identities, before division by $H$. The third requires ordinariness. Their arithmetic branch is the Hasse polynomial itself; a differential equation does not make its first derivative available from its value.

The de Rham calculation explains the small size of this system. Differentiating with $x$ fixed and reducing exact differentials gives

$$
\nabla_\vartheta\omega=\eta-d(R/y),\qquad
\nabla_\vartheta\eta=\frac A3\omega+d(2y)-d(xR/y).
$$

Consequently its connection matrix in the specified basis is

$$
C_\vartheta=\begin{pmatrix}0&A/3\\1&0\end{pmatrix}.
$$

These meromorphic reductions are taken on the characteristic-zero family and its integral Gauss–Manin realization with $6$ and the discriminant inverted, then reduced modulo $p$. They are not an assertion that arbitrary characteristic-$p$ meromorphic forms modulo exact forms inject into projective de Rham cohomology. The scalar identities also have the independent coefficient proof above, so their validation avoids this representation issue.

For the actual unit-root section, $H\eta-\beta\omega$ is horizontal. Equivalently, preservation of its line gives the displayed Riccati equation. In a relative Frobenius matrix, source and target bases belong to the Frobenius-twisted and original families; when the derivative of the base Frobenius vanishes modulo $p$, horizontality has the form $M'=-CM$. Its second column again gives the same pair of equations. No relative family trace is identified with a varying signed integer point count.

## Finite local compatibility cannot choose the initial slope

**Proposition, restricted to the audited local system.** Fix $A_0,B_0,H_0\in\mathbb F_p$ with nonzero discriminant and $H_0\ne0$. For every $\lambda\in\mathbb F_p$ and every integer $1\le r<p$, there are ordinary Taylor jets through degree $r$ satisfying

$$
A'=6B,\qquad B'=-\frac43A^2,\qquad H_\lambda'=b_\lambda,\qquad b_\lambda'=\frac A3H_\lambda,
$$

through derivative degree $r-1$, with $A(0)=A_0$, $B(0)=B_0$, $H_\lambda(0)=H_0$ and $b_\lambda(0)=\lambda H_0$. Their logarithmic derivatives satisfy the Riccati equation to the corresponding order and have initial value $\lambda$.

**Proof.** Equating coefficients of $z^n$ recursively determines each next coefficient by division by $n+1$, for $0\le n<r$. These denominators are nonzero because $r<p$. The recurrence is triangular: the new coefficient uses already determined coefficients of $A,B,H_\lambda,b_\lambda$. Its constant Hasse value is a unit, so division by $H_\lambda$ is valid for these jets. Also $\vartheta(4A^3+27B^2)=0$, so the discriminant remains nonzero. This constructs and verifies a solution for every initial choice. The equations select no particular $\lambda$.

At the special point all matrices

$$
M_\lambda=\begin{pmatrix}0&-\lambda H_0\\0&H_0\end{pmatrix}
$$

kill $\omega$, have rank one and satisfy $M_\lambda^2=H_0M_\lambda$. Their characteristic polynomial is $X(X-H_0)$. Even the full signed characteristic polynomial does not remove the algebraic freedom: if $\tau$ is the $p$-adic unit root of $X^2-tX+p$ and $\rho=p/\tau$, then

$$
\begin{pmatrix}\rho&-\lambda\tau\\0&\tau\end{pmatrix}
$$

has exact trace $t$, determinant $p$ and the above reduction, for every integral lift of $\lambda$. These are abstract compatible matrices. Only the actual curve's crystalline Frobenius has the required geometric realization; the construction does not claim that all matrices are realized by that curve.

For a minimal witness, at $p=7$, $A=B=1$, one has $H=3$, $\beta=3$ and actual $\kappa=1$. Both proposed values $\lambda=0$ and $\lambda=2$ pass all the audited equations through degree six, as does the actual value. Their Hasse jets start respectively with $3+0z+4z^2$ and $3+6z+4z^2$; the actual jet starts $3+3z+4z^2$. The different initial derivatives remain precisely the unknown datum.

Ordinary Taylor differentiation is checked modulo $z^r$. Differentiation is not silently treated as a derivation of the quotient by $z^{r+1}$. At order $p$ the division recurrence fails and arithmetic compatibility may impose new conditions. More generally derivations in characteristic $p$ kill $p$-th powers. No characteristic-zero uniqueness principle is invoked beyond the bounded, explicitly invertible recurrence.

This proposition excludes selection from these necessary local equations alone. It excludes neither a direct formula using $A,B$ and additional global information nor an efficient $p$-curvature computation. The true Hasse polynomial determines the scalar uniquely. The alternative jets are not alternative Cartier scalars of the same curve.

## Automatic differentiation of point counts: a contract failure and a valid slow alternative

Over $R=\mathbb F_p[\varepsilon]/(\varepsilon^2)$, every $p$-th power erases its infinitesimal part. The coordinate $p$-power map is relative Frobenius $E_\varepsilon\longrightarrow E_\varepsilon^{(p)}=E_0$, rather than a same-family $R$-linear endomorphism. Treating it as an endomorphism leaves the residual

$$
y^{2p}-x^{3p}-A_\varepsilon x^p-B_\varepsilon
=-\left(6Bx^p-\frac43A^2\right)\varepsilon.
$$

This is nonzero as a coordinate-ring polynomial for the nonsingular inputs. The finite-field Schoof endomorphism equation therefore cannot simply be reused on a nonconstant dual-number family. Its torsion arithmetic, equality tests, denominator inversions, component splitting and final integer CRT reconstruction need new proofs and a new output contract. The retained Schoof source is a specialized exact prototype for $y^2=x^3+2x$, not a generic dual-number trace implementation or production SEA backend.

An explicit witness is $p=11$, $(A,B)=(1,4)$ and $P_\varepsilon=(0,2+7\varepsilon)$. It lies on $E_\varepsilon$, but its $p$-power coordinates $(0,2)$ have same-family curve residual $5\varepsilon$. They do lie on the Frobenius-twisted special-fiber target. This falsifies the wrong domain, not relative Frobenius itself.

Arithmetic differentiation is valid when the underlying circuit computes the appropriate polynomial. Indeed the monomial-sum identity gives the exact dual-number formula

$$
-\sum_{x\in\mathbb F_p}F_\varepsilon(x)^h=H+\beta\varepsilon,
$$

because $\deg F^h<2(p-1)$. Evaluating the sum with binary powering costs $O(p\log p)$ field operations. Here $F_\varepsilon(x)^h$ is an arithmetic value, not a Legendre symbol or integer multiplicity. A branchy point counter that converts only reduced values into $0,1,-1$ loses the derivative. This correct circuit thus supplies no shortcut.

Finite differences are also a different contract. At $p=11$, $(A,B)=(1,4)$, the literal neighbor in the specified direction is $(3,10)$. Both curves are ordinary, with $H=3$ and $H_1=6$, so their difference is $3$, whereas $\beta=5$. Substituting $\varepsilon=1$ is not a homomorphism from the dual-number ring. No additional trace query is used as an uncharged derivative oracle.

An explicit valid arithmetic derivative circuit is also delivered for $B\ne0$. Normalize $F_\varepsilon=B_\varepsilon G_\varepsilon$, with $G_\varepsilon=1+c_\varepsilon x+a_\varepsilon x^3$, and let $G_\varepsilon^h=\sum u_nx^n$. The state $V_n=n!(u_n,u_{n-1},u_{n-2})$ obeys

$$
V_n=M(n)V_{n-1},\qquad
M(n)=\begin{pmatrix}(h+1-n)c_\varepsilon&0&(3h+3-n)a_\varepsilon\\n&0&0\\0&n&0\end{pmatrix}.
$$

This follows directly from $G(G^h)'=hG'G^h$. At $n=p-1$, Wilson's theorem gives the jets of $H,\beta$ by multiplying the first two entries by $-B_\varepsilon^h$. The circuit constructs its own data from $A,B,p$ and uses $O(p)$ field work with constant state. Writing $M=M_0+\varepsilon M_1$ gives the fixed-size block circuit with rows $(M_0,0)$ and $(M_1,M_0)$. Its length remains $p-1$. This is a correct derivative circuit and an explicit baseline, not differentiated Schoof or a structural shortcut. Automorphism controls with $B=0$ have known ordinary $\kappa=0$; no nonunit inverse is attempted.

## The sole secondary route: first-order Serre–Tate normalization

Katz's compatibility theorems relate normalized Hodge sections, Frobenius-fixed sections and $d\log q$. Their canonical normalization contains more data than a coarse canonical $j$ or the value $q=1$. Specializing the differential normal form to one dimension, write its normalized Hodge section as $a\omega$ and its unit-root section as $u=c(\eta-\kappa\omega)$. Comparing coefficients in $\nabla(a\omega)=u\,d\log q$ along the specified direction yields

$$
\kappa=-\frac{\vartheta a}{a}.
$$

The Kodaira–Spencer projection modulo $\omega$ sees the $\eta$ coefficient, while the required derivative is the $\omega$ coefficient. A known first-order deformation class therefore does not immediately give this normalization derivative. Katz's actual Frobenius-fixed construction is arithmetic and unique; replacing it by an arbitrary horizontal local solution drops exactly that arithmetic condition.

There is a direct test of inference from the partial normal form. For every jet above, set $r_\lambda=H_\lambda/H_0$, $a_\lambda=r_\lambda^{-1}$ and $u_\lambda=r_\lambda(\eta-\kappa_\lambda\omega)$. Then $\nabla u_\lambda=0$ and $\nabla(a_\lambda\omega)=r_\lambda^{-2}u_\lambda\,dz$. Solving $q_\lambda'/q_\lambda=r_\lambda^{-2}$ with $q_\lambda(0)=1$ gives

$$
q_\lambda(z)=1+z+\left(\frac12-\lambda\right)z^2+\cdots.
$$

Thus all slopes share the same first-order $q$ jet in this formal normalization. Their second coefficient, or $a_\lambda'(0)=-\lambda$, would recover the answer if supplied. **These constructed $q_\lambda$ are not certified marked Serre–Tate coordinates.** They are compatible formal normal forms demonstrating that the displayed differential equations and first-order scalar values alone do not implement the genuine arithmetic normalization. No claim is made that every intrinsic construction must enumerate a full torsion point or orbit.

The result is a derivative-oracle reduction with unresolved acquisition cost. The checked Maiga–Robert theorems require $j\notin\mathbb F_{p^2}$ and therefore do not apply to these prime-field inputs. Their hypothesis restriction says nothing universal about other lift methods.

## Cost, positive controls and reconstruction

| Task or description | Field-operation cost beyond the supplied trace | Bit and representation qualification |
|---|---|---|
| Evaluate the directional connection at the input | $O(1)$ | A constant number of field elements; inversions and arithmetic on $\log p$-bit residues |
| Construct/check arbitrary local order-$r$ jets by the delivered recurrence | $O(r^2)$, $r<p$ | $O(r)$ field-element storage; conservative classical-arithmetic bound $O(r^2(\log p)^2)$; this constructs compatible jets from an input slope and does not extract it |
| Arithmetic Euler-power sum jet | $O(p\log p)$ | Constant-size arithmetic state; exact, slow acquisition |
| Delivered scaled recurrence derivative circuit, $B\ne0$ | $O(p)$ | Constant-size field state; valid AD of a coefficient circuit, not of an integer trace algorithm |
| Dense and sequential cubic-power reference | $O(p^2)$ | $O(p)$ field elements; validation only |
| Differentiate a length-$\Theta(p)$ fixed-dimensional recurrence | Same length with constant-size augmented state | A valid derivative circuit retains its exponent; a BGS acceleration still has square-root dependence under the original required unit conditions |
| Supplied genuine $a,\vartheta a$ or Frobenius off-diagonal entry | Constant-size extraction | Different oracle contract; acquisition unresolved |
| Retained fixed-small-$D$ CM evaluator | $O(h(D))$ evaluation for each fixed retained table | Constant-size tables only because $D$ is fixed; table production, excluded primes and recognition hypotheses are retained |
| Reconstruct one branch query from exact $t,\kappa$ and a supplied simple root | $O(1)$ | Root finding is excluded; all model and basis conversion is included |

The BGS statement is a conditional complexity transfer to the same recurrence over a constant-size jet ring, not a delivered native generic BGS backend. Harvey's related $p$-adic $E_2$ computation already has square-root dependence at fixed precision; his known-trace discussion gives a limited constant-factor saving, not a new exponent. His complexity statement fixes the curve, so a variable-lift implementation would additionally need coefficient-size control. There is no benchmark because neither new candidate passes its acquisition gate.

A cold complete solver would also need prime and ordinary input certification and acquisition of the signed trace. Schoof is an unconditional deterministic polynomial-in-$\log p$ setup option in principle; practical SEA/PARI alternatives have their own contracts. This audit obtains exact small-prime traces by direct enumeration for validation and does not implement a new generic complete scalar solver. The supplied trace is free only in the stated main theoretical contract.

For $f=1+cw+bw^2+aw^3$, the retained chart is $x=aw+b/3$, $y=av$. It preserves $dw/v=dx/y$ exactly and gives

$$
A=ac-b^2/3,\qquad B=a^2-abc/3+2b^3/27,\qquad
K=\frac{\kappa H-(b/3)H}{a},\qquad
T_f(\mu)=\frac{a\mu(\mu H-K)}{f'(\mu)}.
$$

The delivered reconstruction routine validates the supplied nonzero simple root. The checks compute the scalar by independent slow coefficient extraction, then verify $H,K$ against a separately powered original cubic and $T_f(\mu)$ against $\sum_{i=0}^{p-1}[w^i]f^h\mu^i$. This is a complete reconstruction control, not evidence that the rejected candidates computed $\kappa$ cheaply. No stopping-index claim or new computation of both $B_L$ and $a_L$ is made.

Under $(A,B)\mapsto(d^2A,d^3B)$, the checks recover $H\mapsto\chi(d)H$, $\beta\mapsto\chi(d)d\beta$, $\kappa\mapsto d\kappa$. The expression $A\kappa/B$ is invariant when $AB\ne0$. For a basis change $\omega'=v\omega$, $\eta'=s\eta+c\omega$, the scalar becomes $(s\kappa+c)/v$. Katz's chart uses $y_K=2y$ and $dx/(2y)$: its $E_2$ reduction is $12\kappa$. The weight-two value for $dx/y$ is $3\kappa$; common scaling of both basis vectors does not itself alter the line slope. Harvey likewise defines its modular-form input differential as the usual $dx/(2y)$ on a short model, despite writing its Frobenius matrix on $dx/y,x\,dx/y$.

## Reproducible evidence and limitations

| Check | Executed result |
|---|---|
| Supplied ordinary models, primes $7,11,13,17,19,23$ | 1,256 dense coefficient, dual-number jet, arithmetic power-sum jet and direct signed-trace agreements |
| Exact coefficient certificate over $\mathbb Q$, and global polynomial identities modulo $p$ | Passed for all six validation primes |
| Explicit scaled recurrence jets of both $H$ and $\beta$ | 1,228 models with $B\ne0$; agree with $(H,\beta)$ and $(\beta,(A/3)H)$ respectively |
| Every proposed initial slope at order five | 23,128 compatible jets across the 1,256 models |
| All proposed slopes through order $p-1$ | 90 jets across one actual model at each of six primes; true jets additionally match Hasse-polynomial substitution |
| Distinct model scales and twists | 2,512 checks with direct signed-trace verification |
| De Rham basis scales and shears | 1,256 checks |
| Same-trace/different-slope pairs | All eight supplied pairs independently recomputed |
| Actual retained fixed-$D$ evaluator | 260 agreements on the ordinary fixtures; all five named controls pass, including $D=-256$ at $p=73$ |
| Coverage | 996 outside-table models; 72 each with $t=1$ and $t=-1$; 108 with $\beta=0$, including 44 with $AB\ne0$; 36 with $A=0$ and 28 with $B=0$ |
| Original-cubic branch reconstruction | 51 supplied queries agree with independent coefficients and direct prefixes |
| Failure propagation | Six planted mathematical errors and two missing-dependency cases exit nonzero; two exit-zero false-success controls are rejected by the new runner |

These counts overlap; they are not independent statistical trials. Outside-table means outside the retained finite tables, not non-CM. Every ordinary finite-field curve has CM by an order. The completed $-256$ source and actual table entry were included; the historical comparator omitting that family was not reused. The historical precision-two weighted-sum implementation was inspected and kept separate. Its successful recurrence backend does not furnish a sum-avoiding correction here.

Raw CSVs, JSON jet examples, runner logs, source hashes and the environment are in the package. `scalar_math.py` does not read fixtures. Only `validate.py` reads the reference table, after computing its own arithmetic outputs. `run_checks.py` requires process success, an explicit PASS sentinel and zero failure counters. Missing fixtures or retained CM dependencies fail explicitly. The old independent feasibility drivers were not silently patched; their known exit-status issue and the pending integral-comparison clarification remain inherited qualifications.

## ELI5

We found a very small rule describing how the hidden answer changes when the curve changes. But a rule for change still needs a starting answer. In the local equations we tested, every proposed starting answer fits until more arithmetic information is supplied. The ideal $p$-adic twin gives a beautifully organized coordinate system, but converting that system into our required coordinates still needs a derivative we cannot yet obtain cheaply. We have identified the missing ingredient more precisely; we have neither found the general shortcut nor proved one impossible.

## Primary references

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793. Inspected published author PDF: https://specfun.inria.fr/bostan/publications/BoGaSc07.pdf, Theorem 14 and Section 8.

Harvey, D. (2008). Efficient computation of $p$-adic heights. *LMS Journal of Computation and Mathematics, 11*, 40–59. Inspected author preprint: arXiv:0708.3404v1, 24 August 2007, https://arxiv.org/pdf/0708.3404, Theorem 1, Section 3 and Section 3.1.

Katz, N. M. (1981). Serre–Tate local moduli. In *Algebraic surfaces (Orsay, 1976–78)* (Lecture Notes in Mathematics, Vol. 868, pp. 138–202). Springer. Inspected author scan: https://web.math.princeton.edu/~nmk/old/serretatelocmod.pdf, Main Theorems 3.7.1, 4.3.1 and 4.5.3, and Corollary 4.2.2.

Katz, N. M. (2019, inspected author-copy copyright year). On a question of Zannier. *Experimental Mathematics*. https://doi.org/10.1080/10586458.2018.1551818. Inspected copy: https://web.math.princeton.edu/~nmk/zannier_publ.pdf, Theorem 3.1 and Section 3. A readable additional author draft, https://web.math.princeton.edu/~nmk/zannier23.pdf, was consulted for notation; it was not silently substituted for the published copy. Final issue metadata was not used as mathematical evidence.

Maiga, A., & Robert, D. (n.d.). *Towards computing canonical lifts of ordinary elliptic curves in medium characteristic* [Author manuscript]. https://www.normalesup.org/~robert/pro/publications/articles/fast_canonical_lift_g1.pdf. Inspected Theorems 1.1 and 1.2 and Remark 1.3.

Schoof, R. (1985). Elliptic curves over finite fields and the computation of square roots mod $p$. *Mathematics of Computation, 44*(170), 483–494. Author-hosted scan: https://www.mat.uniroma2.it/~schoof/ctpts.pdf. Text extraction was unavailable; the present dual-number domain obstruction is proved directly and does not rely on interpreting its scanned formulas. Further source-access qualifications are recorded in `SOURCE_DEPENDENCY_AUDIT.md`.

Schoof, R. (1995). Counting points on elliptic curves over finite fields. *Journal de Théorie des Nombres de Bordeaux, 7*, 219–254. Readable author copy: https://www.mat.uniroma2.it/~schoof/ctg.pdf. Sections 3 and 5 supply the inspected coordinate-Frobenius relation and deterministic polynomial-time trace setup.
