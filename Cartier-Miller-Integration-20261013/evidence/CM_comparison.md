# The CM-to-Cartier comparison in the project's coefficient chart, recovery of the six depth-three families, and a certified seed at discriminant −7

**Extension note, 12 October 2026.** For David Jordan's Cartier–Miller evaluation project.

This is an AI-assisted research note. It has not been refereed. It does not revise the published manuscript, and no repository was inspected or changed. Every numerical statement below is observed output from the scripts in this package, run in the environment recorded in §10. Section 11 separates classical facts, new unrefereed statements, finite tests and open items.

## 0. Outcome

The proposed normalization is **correct as stated**. For $AB\neq0$, a characteristic-zero CM model, and a prime $\mathfrak p$ meeting the hypotheses of Theorem 5,

$$\frac{\beta}{H}\equiv-\frac{3B}{2A}\,s_2(\tau)\pmod{\mathfrak p},\qquad s_2=\frac{E_2^*E_4}{E_6}.$$

The proof has two elementary steps.

- **Characteristic $p$ (Theorem 1).** Let $\alpha$ be a separable endomorphism defined over $\mathbb F_p$, with $\alpha^*\omega=\lambda\omega$ and $\alpha^*\eta=\mu\eta+\nu\omega+(\text{exact})$. Then Cartier commutation gives $\beta(\lambda-\mu)=\nu H$.
- **Characteristic zero (Theorem 4).** The quasi-period law of a normalized isogeny gives $G_2^*(\Lambda)=\sigma_G/\bigl(a(a-\bar a)\bigr)$, which is the same algebraic number as the de Rham eigenline coefficient $c=\nu/(\mu-\lambda)$.

Reduction modulo $\mathfrak p$ identifies the two. This proof needs neither the unit-root line nor any $p$-adic machinery. The unit-root interpretation is recorded separately in §3, together with a warning that is specific to characteristic $p$.

Further results:

1. **The six families are recovered.** Exact endomorphism loops were computed in each coefficient field. They use neither the seed property $\beta=0$ nor the transport recurrence. In every case they give $-c$ equal to the retained multiplier (Theorem 6). This proves all six slope formulas afresh at every eligible prime.
   - For $D=-12$ and $D=-16$ there are additional seed-free checks, through odd-degree endomorphisms of degree 3 and 5.
   - The weight-zero CM values $S=s_2(\tau)\in\mathbb Q(j)$ are paired with $j$ by explicit $R_D\in\mathbb Q[J]/(H_D)$.
   - Every complex embedding was matched to its CM form numerically, with errors below $10^{-78}$.
2. **New seed at $D=-7$ (Theorems 7–8).** Let $p\equiv1,2,4\pmod 7$.
   - Every short model with $j=-3375$ is $(-35r^2,-98r^3)$ for some $r\in\mathbb F_p^*$, and $\beta=-rH=-\dfrac{5B}{14A}H$, with $H\ne0$.
   - The signed trace is the unique $t$ with $4p=t^2+7v^2$ and $(t/7)=(r/p)$. Two independent derivations are given.
   - No admissible prime divides any $j$-collision resultant against the two seeds or the six families.
   - The original-cubic evaluator is implemented and validated.
3. **Control at $D=-8$:** $\beta/H=r=-15B/(28A)$ on $(-30r^2,56r^3)$, for $p\equiv1,3\pmod8$, with $s_2(\sqrt{-2})=5/14$.
4. **Decision on direct CM data.** For a fixed discriminant, exact CM data give the coefficient directly as $\beta/H=-(3B/2A)R_D(j)$, with no isogeny path at query time. This uniform evaluator matches the retained recognizers on all 13,130 family members tested. It is not a generic method: the table grows with $D$, and identifying the CM order of a generic curve is a separate and expensive problem (§9).
5. **Source warning.** Read literally ($\Phi_D=\Phi_{|D|}$), Bruinier–Ono–Sutherland's Lemma 2.3 reproduces $5/21$ at $D=-7$ but is inapplicable at $D=-8$, where $\Phi_8(j,j)\neq0$. Its output there disagrees with the true value $5/14$ (§6).

## 1. Conventions

Let $p\ge7$ be prime and $E/\mathbb F_p:\ y^2=F(x)=x^3+Ax+B$ be nonsingular. Put $h=(p-1)/2$ and

$$H=[x^{p-1}]F^h,\qquad\beta=[x^{p-2}]F^h,\qquad \omega=dx/y,\qquad \eta=x\,dx/y.$$

$\mathcal C$ is the Cartier operator on meromorphic differentials of $\mathbb F_p(E)$. It is $p^{-1}$-linear, so over a perfect field $k$ it satisfies $\mathcal C(f^p\theta)=f\,\mathcal C\theta$. It also satisfies $\mathcal C(dg)=0$, and $\theta$ is exact if and only if $\mathcal C\theta=0$ (Cartier's theorem). Write $\theta=y^{-p}\cdot y^{p-1}(\cdot)\,dx$ and use $\deg F^h=3h<2p-1$. This gives

$$\mathcal C\omega=H^{1/p}\omega,\qquad \mathcal C\eta=\beta^{1/p}\omega,$$

which over $\mathbb F_p$ are the retained formulas $\mathcal C\omega=H\omega$ and $\mathcal C\eta=\beta\omega$.

Under the twist $(A,B)\mapsto(d^2A,d^3B)$, the identity $F_d(x)=d^3F(x/d)$ gives $H\mapsto\chi(d)H$ and $\beta\mapsto\chi(d)d\beta$. Hence $\beta/H\mapsto d\,\beta/H$, and $A\beta/(BH)$ is invariant.

The original-cubic conventions are those of the retained code. The cubic is $f=1+cw+bw^2+aw^3$ with $a\ne0$, given low-to-high as `[1,c,b,a]`. The change of variables is $x=aw+b/3$, $y=av$, with

$$A=ac-\tfrac{b^2}{3},\qquad B=a^2-\tfrac{abc}{3}+\tfrac{2b^3}{27}.$$

Then $dw/v=dx/y$ exactly, and $\beta=aK+(b/3)H$, where $K=[w^{p-2}]f^h$ and $H=[w^{p-1}]f^h$.

Write $f^h=\sum d_iw^i$ and $T_f(\mu)=\sum_{i=0}^{p-1}d_i\mu^i$, with $S_f(1/\mu)=T_f(\mu)$ (manuscript eq. 2). For a nonzero simple root $\mu$ of $f$,

$$T_f(\mu)=\frac{a\mu(\mu H-K)}{f'(\mu)}.$$

No convention is changed in this note. The formula was re-tested against direct dense coefficient sums (§10, T6).

## 2. Characteristic p: the eigen-equation

**Theorem 1.** Let $k$ be a perfect field of characteristic $p\ge5$, let $E/k$ be as above, and let $\alpha$ be a separable endomorphism of $E$ defined over $k$. Suppose

$$\alpha^*\omega=\lambda\omega,\qquad\alpha^*\eta=\mu\eta+\nu\omega+dg$$

for some $\lambda,\mu,\nu\in k$ and $g\in k(E)$. Then $\lambda^p\beta=\mu\beta+\nu H$. Over $k=\mathbb F_p$ this reads

$$\boxed{\beta(\lambda-\mu)=\nu H.}$$

In particular, if $\lambda\neq\mu$ then $\beta/H=\nu/(\lambda-\mu)$ whenever $H\ne0$.

*Proof.* Cartier commutes with pullback along a separable $k$-morphism. In a separating variable $x$, write $\theta=\sum_{i<p}u_i^px^i\,dx$; then $\mathcal C$ selects $u_{p-1}dx$, and a separable pullback keeps $\alpha^*x$ separating (manuscript Sublemma 3a; Serre, 1958). Applying $\mathcal C$ to the hypothesis gives

$$\mathcal C(\alpha^*\eta)=\bigl(\mu^{1/p}\beta^{1/p}+\nu^{1/p}H^{1/p}\bigr)\omega.$$

Commutation gives

$$\mathcal C(\alpha^*\eta)=\alpha^*(\beta^{1/p}\omega)=\beta^{1/p}\lambda\,\omega.$$

Comparing the two and raising to the $p$-th power proves the claim. ∎

The decomposition $(\mu,\nu)$ is **not** unique in characteristic $p$, because $\eta-(\beta/H)\omega$ is itself exact there (§3.1). The relation holds for every valid decomposition. A useful decomposition is one that comes from a characteristic-free formula, for which $\lambda\ne\mu$ (Lemma 2).

**Lemma 2 (pullback matrices).** Write $f^*(\omega_2,\eta_2)=(\omega_1,\eta_1)M_f$ modulo exact forms, so that $M_{f\circ g}=M_gM_f$. Then:

| Map | $M$ | Identity used |
|---|---|---|
| Normalized 2-isogeny, kernel root $q$: $x'=x+F'(q)/(x-q)$, quotient $A'=-4A-15q^2$, $B'=-8Aq-22q^3$ | $\begin{pmatrix}1&-q\\0&2\end{pmatrix}$ | $\phi^*\omega'=\omega$, $\phi^*\eta'=(2x-q)\omega-2\,d\!\left(\frac{y}{x-q}\right)$ |
| Normalized Vélu isogeny with kernel $G$, $\lvert G\rvert=\ell$ prime to $p$ | $\begin{pmatrix}1&-\sigma_G\\0&\ell\end{pmatrix}$, $\sigma_G=\sum_{Q\in G\setminus O}x(Q)$ | $(x(P{+}Q)-x(P))\omega=-d\!\left(\frac{2(y-y_Q)}{x-x_Q}\right)$ |
| Isomorphism $(x',y')\mapsto(x'/u^2,y'/u^3)$ from $(u^4A,u^6B)$ to $(A,B)$ | $\mathrm{diag}(u,u^{-1})$ | direct |
| $j=0$: $(x,y)\mapsto(\zeta x,y)$, $\zeta^2+\zeta+1=0$ | $\mathrm{diag}(\zeta,\zeta^2)$ | direct |
| $j=1728$: $(x,y)\mapsto(-x,iy)$ | $\mathrm{diag}(i,-i)$ | direct |

These are polynomial identities in the curve coefficients and kernel data, so they hold in every characteristic $\ne2$ where the models are nonsingular. Identities V1–V4 were verified symbolically in this pass, independently of the retained code (`theory/symbolic_velu_check.py`). For odd $\ell$ the quotient equation is Vélu's (Vélu, 1971; not re-derived here). The pullback matrix follows from Vélu's $x$-map $x'=x+\sum_{Q\ne O}(x(P{+}Q)-x(Q))$ and the translation identity V2.

Nonsingularity is preserved along a normalized 2-isogeny for odd $p$. With $u=F'(q)$ and $w=4A+3q^2$, the two discriminants are

$$4A^3+27B^2=u^2w,\qquad 4A'^3+27B'^2=-16\,u\,w^2.$$

**Corollary 2.1 (kernel-sum form).** Let $\alpha=\psi_u\circ\phi_G$ be separable and non-scalar over $\mathbb F_p$. Write $\iota(\alpha)=u$ for its action on $\omega$, and $\iota(\bar\alpha)=\ell/u$. Then

$$\frac{\beta}{H}=\frac{\sigma_G}{\iota(\alpha)\,\iota(\bar\alpha-\alpha)}=\frac{\sigma_G}{\ell-u^2}.$$

The **seeds** are the case $\nu=0$. For $j=0$ with $p\equiv1\pmod3$: $\lambda=\zeta$, $\mu=\zeta^2$, so $\beta(\zeta-\zeta^2)=0$ and $\beta=0$. For $j=1728$ with $p\equiv1\pmod4$: $\beta(2i)=0$, so $\beta=0$.

## 3. De Rham cohomology in characteristic p and the unit-root line (interpretation)

None of the proofs in §§2, 4–8 uses this section. It answers how the meromorphic representatives relate to $H^1_{\mathrm{dR}}$ and to the unit-root line, and fixes the Frobenius conventions involved.

**3.1 Warning: second-kind differentials modulo exact forms are not $H^1_{\rm dR}$ in characteristic $p$.**

At a point with parameter $t$, a differential $\theta=\sum a_nt^n\,dt$ is locally exact modulo regular forms if and only if $a_{mp-1}=0$ for all $m\le0$. This holds if and only if $\mathcal C\theta$ is regular there. So the second-kind differentials are $D_2=\mathcal C^{-1}(H^0(\Omega^1))$. Since $\ker\mathcal C=dK$, $\mathcal C$ induces a semilinear isomorphism $D_2/dK\cong H^0(\Omega^1)$, which is **one**-dimensional.

Concretely, for ordinary $E$ the form $\eta-(\beta/H)\omega$ is exact. Put $c=\beta/H$ and $(x-c)F^h=\sum a_mx^m$, so that $a_{p-1}=\beta-cH=0$. Set

$$G(x)=\sum_{m\not\equiv-1}\frac{a_m\,x^{m+1}}{(m\bmod p)+1},\qquad g=G(x)/y^p.$$

Then $dg=G'(x)\,dx/y^p=(x-c)F^h\,dx/y^p=\eta-c\omega$. The primitive $g$ has at most a simple pole at $O$. Its other poles lie at 2-torsion points, where its polar part is a $p$-th power and so is invisible to $d$. This was checked exactly at five curves (`theory/char_p_exactness_demo.py`).

**3.2 Classes in $H^1_{\rm dR}$.** Use Čech–de Rham cocycles $(\{g_i-g_j\},\{\theta-dg_i\})$. The class attached to $\theta$ depends on the local primitives $g_i$ only up to adding $p$-th powers of non-regular local functions. That ambiguity is a class in the conjugate line $F^*H^1(E^{(p)},\mathcal O)$. If the poles of $\theta$ have order $\le p$, requiring primitives of pole order $<p$ removes the ambiguity. This is the convention under which $[\omega]$ and $[\eta]$ (primitive $-2/z$ at $O$, with $z=-x/y$) are the reduction of the standard basis of $H^1_{\rm dR}$ of an integral model. Katz uses this basis (Katz, 1976, §4.0, p. 500, for $y^2=4x^3-g_2x-g_3$).

**3.3 The intrinsic Cartier map.** Applying $\mathcal C$ to the $\Omega^1$-components of a cocycle gives a well-defined map

$$\mathcal C_{\rm dR}:H^1_{\rm dR}(E/\mathbb F_p)\to H^0(\Omega^1),$$

because $\mathcal C(df_{ij})=0$. It is independent of the primitive choice: $\mathcal C_{\rm dR}[\theta]=\mathcal C(\theta)$. So $\mathcal C_{\rm dR}[\omega]=H\omega$ and $\mathcal C_{\rm dR}[\eta]=\beta\omega$. The map is natural for all morphisms, separable or not, and its kernel is the conjugate line $\operatorname{Im}F^*$. This is the exact conjugate-filtration sequence (Cartier isomorphism; Katz, 1970; Oda, 1969 — not re-read in this pass).

**3.4 The unit-root line.** Let $E/\mathbb Z_p$ be the integral model ($p\ge5$, good reduction), with crystalline Frobenius $\varphi$ on $H^1_{\rm dR}(E/\mathbb Z_p)$. This $\varphi$ is $\sigma$-linear with $\sigma=\mathrm{id}$ on $\mathbb Z_p$, satisfies $\varphi\equiv F^*_{\rm abs}\pmod p$, and has $\varphi({\rm Fil}^1)\subset pH$. For ordinary reduction, the unit-root line $U$ is the unique $\varphi$-stable complement of ${\rm Fil}^1=\langle\omega\rangle$ on which $\varphi$ is invertible. It follows that

$$U\otimes\mathbb F_p=\operatorname{Im}(\varphi\bmod p)=\operatorname{Im}F^*=\ker\mathcal C_{\rm dR}=\bigl\langle[\eta]-\tfrac{\beta}{H}[\omega]\bigr\rangle.$$

Hence $U=\mathbb Z_p([\eta]+u[\omega])$ with $u\equiv-\beta/H\pmod p$.

Conventions: $\varphi$ is Frobenius pullback; $V=p\varphi^{-1}$ on the Dieudonné module; $\mathcal C$ is $\sigma^{-1}$-linear on differentials. The identification $V=\mathcal C_{\rm dR}$ is **not** used anywhere. The only facts used here are that $\ker\mathcal C_{\rm dR}=\operatorname{Im}F^*$ and that $U$ reduces to $\operatorname{Im}(\varphi\bmod p)$. Both are classical (Katz), but their primary sources were not re-read in this pass.

Under these facts, Theorem 5 shows that the reduction of the CM eigenline $\langle\eta+c\omega\rangle$ equals $U\otimes\mathbb F_p$. This is consistent with, but strictly weaker than, Katz's identification of $U$ with the CM eigenline over $\mathbb Z_p$ (Katz, 1976, §5.7 and §VIII, which could not be reached in the text available here).

## 4. Characteristic zero: the CM eigenline and $G_2^*$

Uniformize by $x=\wp(z)$ and $y=\wp'(z)/2$ on $\mathbb C/\Lambda$, with $\Lambda=\lambda(\mathbb Z+\tau\mathbb Z)$ and $\operatorname{Im}\tau>0$. Then $\omega=2\,dz$, $\eta=2\wp\,dz$, $g_2=-4A$ and $g_3=-4B$. Put

$$G_2^*(\Lambda)=\frac{\pi^2}{3\lambda^2}E_2^*(\tau).$$

**Theorem 4.** Let $E/L$ have CM over a number field $L$, and let $\alpha\in\operatorname{End}_L(E)\setminus\mathbb Z$ have kernel $G$, degree $\ell$ and $\iota(\alpha)=a$. Put

$$c:=\frac{\sigma_G}{a(a-\bar a)}=\frac{\nu}{\mu-\lambda}\in L,$$

where $(\lambda,\mu,\nu)$ come from the matrix of Lemma 2. Then:

- (i) For every embedding $\sigma:L\hookrightarrow\mathbb C$, $\sigma(c)=G_2^*(\Lambda_\sigma)$.
- (ii) If $AB\ne0$, then $c=\dfrac{3B}{2A}S$, where $S:=s_2(\tau)\in\mathbb Q(j)$, and $\sigma(S)=s_2(\tau_\sigma)$ for every $\sigma$.
- (iii) The class $\eta+c\,\omega$ spans $H^{0,1}\cap H^1_{\rm dR}(E/L)$, which is the $\bar a$-eigenline of $\alpha^*$, and $c$ does not depend on $\alpha$.

*Proof of (i): quasi-periods.* For a normalized isogeny $\mathbb C/\Lambda\to\mathbb C/\Lambda'$ ($z\mapsto z$, $[\Lambda':\Lambda]=\ell$), Vélu's identity is

$$\wp(z;\Lambda')=\sum_{w\in\Lambda'/\Lambda}\wp(z+w;\Lambda)-\sum_{w\ne0}\wp(w;\Lambda).$$

Integrating gives $\zeta(z;\Lambda')=\sum_w\zeta(z+w;\Lambda)+\sigma_Gz+C$, and therefore

$$\eta(\omega_0;\Lambda')=\ell\,\eta(\omega_0;\Lambda)+\sigma_G\,\omega_0\qquad(\omega_0\in\Lambda).$$

Write the full-period quasi-periods as $\eta(\omega_0;\Lambda)=G_2^*(\Lambda)\omega_0+\pi\bar\omega_0/\operatorname{area}(\Lambda)$. This form follows from $\eta_1=\pi^2E_2(\tau)/(3\lambda)$ and Legendre's relation $\eta_1\omega_2-\eta_2\omega_1=2\pi i$. Since $\operatorname{area}(\Lambda')=\operatorname{area}(\Lambda)/\ell$, comparing $\omega_0$-coefficients gives

$$G_2^*(\Lambda')=\ell\,G_2^*(\Lambda)+\sigma_G.$$

For $\alpha(z)=az$ one has $\Lambda'=a^{-1}\Lambda$, and $G_2^*$ is homogeneous of weight 2, so $G_2^*(\Lambda')=a^2G_2^*(\Lambda)$. Hence $(a^2-\ell)G_2^*(\Lambda)=\sigma_G$, and $a^2-\ell=a(a-\bar a)$. Under $\sigma$, the multiplier of $\alpha^\sigma$ is $\sigma(\iota(\alpha))$. The second expression for $c$ is Corollary 2.1 read in characteristic 0.

*Proof of (ii).* From $g_2=60G_4=\frac{4\pi^4}{3\lambda^4}E_4$ and $g_3=140G_6=\frac{8\pi^6}{27\lambda^6}E_6$ we get

$$\frac{A}{B}=\frac{g_2}{g_3}=\frac92\,\frac{\lambda^2E_4}{\pi^2E_6},\qquad\text{so}\qquad G_2^*\frac{A}{B}=\frac32\,s_2.$$

$S=2Ac/(3B)$ is unchanged by twisting. For $\sigma$ fixing $\mathbb Q(j)$, $\tau_\sigma$ is $SL_2(\mathbb Z)$-equivalent to $\tau$, and $s_2$ has weight 0, so $\sigma(S)=S$ and $S\in\mathbb Q(j)$.

*Proof of (iii).* The periods of $\eta+G\omega$ are $2(G\omega_i-\eta_i)$. These are proportional to $\bar\omega_i$ exactly when $G=G_2^*(\Lambda)$. Also $\alpha^*d\bar z=\bar a\,d\bar z$. This is Katz (1976), Lemma 4.0.7 (p. 501), read in the scan.

The constants were also checked directly. PARI's periods and quasi-periods give the antiholomorphic coefficient equal to the exact $c$ at every real embedding of every model, with Legendre's relation holding (`results/period_check.json`). The identity $G_2^*=\sigma_G/(a(a-\bar a))$ was checked for $D=-7$, $-8$ and $-12$ (`results/quasiperiod_isogeny_check.json`).

The **seeds** satisfy $c=0$, which matches $E_2^*(i)=E_2^*(\rho)=0$.

## 5. The comparison theorem

**Theorem 5.** Keep the notation of Theorem 4, and suppose $\alpha$ is given by an explicit chain of the maps in Lemma 2. Let $\mathfrak P\mid p$ be a prime of $L$ with residue field $\mathbb F_p$, and assume:

- (a) $p\ge7$;
- (b) the model and all chain data $(A,B,\text{kernel data},u,\zeta\text{ or }i)$ are $\mathfrak P$-integral;
- (c) the reduction of $E$ is nonsingular, which persists along the chain by the discriminant identity above;
- (d) $p\nmid\ell$, so the reduced isogenies are separable;
- (e) $\iota(\alpha)-\iota(\bar\alpha)$ is a $\mathfrak P$-unit; for the loops used here $(\lambda-\mu)^2=D$, so this means $p\nmid D$.

Then the reduced model satisfies $H\ne0$ and

$$\frac{\beta}{H}\equiv-c\equiv-\frac{3B}{2A}S\pmod{\mathfrak P}\qquad(AB\not\equiv0).$$

If $A\equiv0$ or $B\equiv0$, then $c=0$ and $\beta=0$; the quotient form does not apply.

*Proof.* The chain identities of Lemma 2 are characteristic-free. Reducing them modulo $\mathfrak P$ gives an $\mathbb F_p$-endomorphism $\alpha_0$ with the reduced matrix. Theorem 1 then gives $\beta(\bar\lambda-\bar\mu)=\bar\nu H$.

Hypothesis (e) forces $H\ne0$, since $H\equiv t\pmod p$ and $p\nmid t$ for ordinary reduction. Ordinarity holds: if $E_0$ were supersingular then, since $p\ge5$, its trace is 0 and $\pi^2=-p$. Every $\mathbb F_p$-endomorphism commutes with $\pi$, so it lies in the centralizer $\mathbb Q(\pi)\cong\mathbb Q(\sqrt{-p})$ inside the quaternion algebra $\operatorname{End}^0_{\bar{\mathbb F}_p}(E_0)$. So $\mathbb Q(\alpha)=\mathbb Q(\sqrt{-p})$, contradicting $p\nmid D$. ∎

**Exclusions, in full.**

- Bad reduction of the model at $\mathfrak P$.
- $p$ non-split in $K$. Then $E$ has supersingular reduction, $H=0$, and $\beta\ne0$ was observed in 78 checks (T4).
- $p\mid D$ (eigenvalue separation fails; this includes the conductor primes for the orders here) and $p\mid\ell$.
- Non-integral chain data or CM value. $c$ has denominators dividing $\iota(\alpha)(\iota(\alpha)-\iota(\bar\alpha))$; since $c=\sigma_G/(a(a-\bar a))$, these divide $\ell D$ up to units.
- $AB\equiv0$ for the quotient form. $S$ has denominators from $B$, and these never occur at eligible primes (§7).
- Residue degree of $\mathfrak P$ greater than 1. Then $\mathcal C$ is semilinear and the statement must be read with $\lambda^p$. At eligible primes of the families here, $p$ splits completely in $L$.
- $j$-collisions. These are handled by exact resultants (§§7–8).

## 6. Literature audit

| Source | What was checked | Status |
|---|---|---|
| Katz (1976), *Annals* 104 | Author scan, text-extracted. §4.0 (p. 500): $\omega=dx/y$, $\eta=x\,dx/y$. Thm 4.0.4 (p. 500): CM values of $S$ lie in $K$. **Lemma 4.0.7 (p. 501)**: $H^{0,1}\cap H^1_{\rm dR}(E/K)$ is the $\bar\alpha$-eigenspace of $[\alpha]^*$ when $[\alpha]^*\omega=\alpha\omega$, with projector $(\bar\alpha-\alpha)^{-1}([\alpha]^*-\alpha)$. Lemma 1.3.6 (p. 467): direction of $H^{0,1}$ is $-\tfrac1{12}S$. | Verified from the OCR extract; formulas partly garbled. **§5.7 (p. 511), Thm 8.0.9 and Lemma 8.0.13 were not reachable** (extraction ended near p. 506). The handover's reading of them is not re-verified. |
| Bruinier, Ono & Sutherland (2015 arXiv v3) | (1.2) $\gamma=\frac{E_4E_2^*}{6E_6j}-\frac{7j-6912}{6j(j-1728)}$; (1.3) $E_2^*$; Thm 1.1 (Algorithm 1, **under GRH** expected $\tilde O(\lvert D\rvert^{7/2})$ time, $\tilde O(\lvert D\rvert^2)$ space); Thm 1.2 (GRH, $\tilde O(\lvert D\rvert^{5/2})$); §2.4 (2.6)–(2.9), Lemma 2.3 $\gamma=(2\beta_{0,2}-\beta_{1,1})/\beta_{0,1}$, hypotheses $D<-4$, $D\ne-3d^2$, Masser p. 118 for the special case. The paper does not state that $\gamma\in\mathbb Q(j)$ directly; it shows that $H_D(\gamma;x)$ has rational coefficients. | Read (arXiv text; no page numbers). **Our checks:** literal $\Phi_7$ gives $s_2=5/21$ at $D=-7$, equal to the loop value. Literal $\Phi_8$ at $D=-8$ has $\Phi_8(j,j)\ne0$, because no primitive element of norm 8 exists in $\mathbb Z[\sqrt{-2}]$, and outputs $0.871\ne5/14$. Either the extraction misreports $\Phi_D$, or the lemma tacitly needs $\Phi_{\lvert D\rvert}(j,j)=0$. Masser-type variants with $\Phi_2$ ($D=-8$) and $\Phi_3$ ($D=-12$) reproduce $5/14$ and $5/11$; these are our own experiments, not literature claims. |
| Masser (1975), LNM 437 | Appendix, Lemma A2, p. 118. | Not obtained; only the pointers in BOS. |
| Sutherland (2023), 18.783 Lecture 21 | Thm 21.5 (p. 4): for $p$ split, "$H_D$ splits completely ⇔ $4p=t^2-v^2D$, $t\not\equiv0$". Cor 21.11 (p. 8). **Thm 21.14 (Deuring, p. 10)**: $H_D$ splits into *distinct* linear factors modulo primes of degree one coprime to $D$; the endomorphism ring is preserved. | Read via fetch. Supports the collision and pairing logic; the exact resultants in §§7–8 are the operative certificates. |
| Ireland & Rosen (1990) | Ch. 18. | Concerns the $j=0$ and $1728$ seeds only; not used for $D=-7$. |
| Silverman (1994) *Advanced Topics* II §§9–10 (Deuring's Hecke character; conductor $N_E=\lvert d_K\rvert N\mathfrak f$); Cohen (1993) Alg. 1.5.3 (Cornacchia); Schoof (1985); Elkies (1998); Vélu (1971); Oda (1969); Katz (1970, 1973); Knapp (1992) Thm 4.2 (halving) | Standard facts cited in proofs. | **Not re-read in this pass**; page and theorem numbers are from memory and should be checked. |

**Is this standard?** In substance, yes.

- The identification of the unit-root (Cartier) splitting with the Hodge splitting at ordinary CM primes is Katz's theory, from 1973 and 1976.
- The quasi-period law $G_2^*(\Lambda')=\ell G_2^*(\Lambda)+\sigma_G$ is classical. It is the non-holomorphic form of the relation behind the kernel sum $p_1$ in Elkies' SEA formulas; this attribution is unverified.
- The characteristic-$p$ eigen-equation (Theorem 1) is a direct consequence of Cartier commuting with endomorphisms and is likely folklore; no source was located.

What appears new, pending specialist review:

- The explicit form in this project's $(H,\beta)$ chart.
- The elementary proof of the reduction, which avoids $p$-adic theory.
- The closed formulas for $D=-7$ and $D=-8$, with their certified recognition and trace sign.
- The uniform fixed-$D$ evaluator and its agreement with the six retained families.

No priority claim is made.

## 7. Exact CM values and recovery of the six families

**Method.** For each family a non-scalar endomorphism was built: the retained reverse path to the seed, then a seed automorphism, then the forward path, closed by an isomorphism with $u=2^k$. Every kernel root, every intermediate quotient and the closing scale were checked exactly in the tower of quadratic fields. $c=\nu/(\mu-\lambda)$ was computed there with $r=1$; $c$ scales linearly in $r$. No characteristic-$p$ datum, no $\beta=0$ input and no transport recurrence was used (`theory/family_loops.py`).

| Family | $D$ | Endomorphism | $\lambda,\mu$ | $c$ (r=1) | Retained $\beta/(rH)$ | $-c=$ retained? |
|---|---|---|---|---|---|---|
| depth 1, A=0 | −12 | loop, deg 4 | $-1\pm\sqrt{-3}$ | 1 | −1 | yes |
| same (seed-free) | −12 | $\sqrt{-3}$, odd Vélu, deg 3, kernel $x=-3$ | $\pm\sqrt{-3}$ | 1 | −1 | yes |
| depth 1, B=0 | −16 | loop, deg 4 | $\pm2i$ | 1 | −1 | yes |
| same (seed-free) | −16 | $1+2i$-type, deg 5 (kernel factor of $\psi_5$ over $\mathbb Q(i)$) | $-1\mp2i$ | 1 | −1 | yes |
| depth 2, A=0 | −48 | loop, deg 16 | $-2\pm2\sqrt{-3}$ | $3+2e$ | $-(3+2e)$ | yes |
| depth 2, B=0 | −64 | loop, deg 16 | $\pm4i$ | $3+2e$ | $-(3+2e)$ | yes |
| depth 3, A=0 | −192 | loop, deg 64 | $-4\pm4\sqrt{-3}$ | $7+6e+6g+2eg$ | $-(7+6e+6g+2eg)$ | yes |
| depth 3, B=0 | −256 | loop, deg 64 | $\pm8i$ | $7+4s+6s^2+4s^3$ | $-(7+4s+6s^2+4s^3)$ | yes |
| **new seed** | **−7** | $(1+\sqrt{-7})/2$, deg 2 | $\frac{1\pm\sqrt{-7}}2$ | **1** | (new) **−1** | — |
| control | −8 | $\sqrt{-2}$, deg 2 | $\pm\sqrt{-2}$ | −1 | (new) +1 | — |

In every row $(\lambda-\mu)^2=D$.

**Theorem 6 (recovery).** At every eligible prime of each family, the retained slope formula follows from Theorem 1 applied to the reduced loop. The hypotheses are met as follows:

- the loop data lie in $\mathbb F_p$, because eligibility makes $\zeta$ or $i$ and all parameters rational;
- the models stay nonsingular;
- $p\nmid D$, because eligible primes are $\equiv1\pmod8$ or $\pmod{24}$, or $\equiv1\pmod{3,4}$.

This is a complete proof of all six formulas at all eligible primes, independent of the seed slope. It shares with the retained proof only the Vélu pullback identity, which is re-verified symbolically. Status: **proved (unrefereed)** for all six.

**Weight-zero values, pairing and tables** (`results/cm_tables.json`):

| $D$ | $h$ | $S=s_2$ in the family parameter | $R_D(J)$ (low→high) | $H_D$ = PARI polclass | primes dividing den($R_D$) |
|---|---|---|---|---|---|
| −7 | 1 | 5/21 | 5/21 | $J+3375$ ✓ | 3, 7 |
| −8 | 1 | 5/14 | 5/14 | $J-8000$ ✓ | 2, 7 |
| −12 | 1 | 5/11 | 5/11 | $J-54000$ ✓ | 11 |
| −16 | 1 | 11/21 | 11/21 | $J-287496$ ✓ | 3, 7 |
| −48 | 2 | $\frac{6015}{11891}+\frac{1500}{11891}e$ | $\frac{6278745}{21850253},\ \frac{1}{6489525141}$ | ✓ | 3, 11, 17, 23, 29, 41, 47 |
| −64 | 2 | $\frac{13}{33}+\frac{20}{77}e$ | $\frac{1103131313}{41453652933},\ \frac{10}{1119248629191}$ | ✓ | 3, 7, 11, 19, 59 |
| −192 | 4 | Appendix A | 4 coefficients, numerators ≤ 35 digits, common denominator 53 digits | ✓ (coefficients ≤ 34 digits) | 3, 5, 11, 17, 23, 29, 41, 47, 53, 59, 71, 83, 89, 101, 113, 131, 149, 167, 173, 179, 191 |
| −256 | 4 | Appendix A | numerators ≤ 44 digits, common denominator 57 digits | ✓ (≤ 37 digits) | 3, 7, 11, 19, 23, 31, 43, 47, 59, 71, 83, 103, 107, 131, 139, 191, 211, 227, 239, 251 |

Every prime dividing a denominator, and every prime dividing $\operatorname{disc}H_D$, is inert or ramified in $K$, so none is eligible. This was checked by complete factorization multiplied back.

The pairing $S=R_D(j)$ is an identity in $\mathbb Q(j)$. Numerically, every embedding of every tower was matched to a reduced form $\tau_Q$, every form was hit, and $|\sigma(S)-s_2(\tau_Q)|<3.2\times10^{-79}$, with explicit $q$-series tail bounds below $10^{-78}$.

**Proposition 10 (uniform fixed-$D$ evaluator).** Let $p$ be split in $K$, with $p\nmid D\cdot\mathrm{den}(R_D)$ (automatic, by the factorization), $H_D(j(E))\equiv0$ and $AB\ne0$. Then

$$\frac{\beta}{H}=-\frac{3B}{2A}\,R_D(j(E)).$$

This follows from Theorem 5, because reduction is a ring map on $\mathfrak P$-integral elements of $\mathbb Q(j)$. Validation: 18,214 members over all conjugates and twists, 13,130 agreements with the retained recognizers, 15,179 dense checks, and 62,652 exhaustively scanned models ($p\le100$) with no disagreement. The 45 pairwise class-polynomial resultants have no prime split in both fields (`results/validation/fixed_D_validation.json`).

Cost for fixed $D$: $O(h)$ field operations for $H_D(j)$ and $R_D(j)$, plus one inversion. The stored table has $2h+1$ rationals, whose sizes are recorded above. That cost is constant only because $D$ is fixed; tables grow with $D$.

**On the special discriminants $D=-3d^2$.** The obstruction in Masser's modular-polynomial formula is specific to that formula. At such $D$, several non-associate primitive elements of norm $|D|$ make $(j,j)$ a singular point of $\Phi_{|D|}=0$. For example, at $D=-12$ the elements $3\pm\sqrt{-3}$ have norm 12. The endomorphism route never meets this obstruction, so it is the "other exact CM argument" that the brief allows for $-12$, $-48$ and $-192$.

## 8. The new seed: discriminant −7 (principal) and the −8 control

**Theorem 7 (slope).** Let $p$ be prime with $p\equiv1,2,4\pmod7$; equivalently $(-7/p)=(p/7)=1$ and $p\ne7$, hence $p\ge11$. For a short model over $\mathbb F_p$ the following are equivalent: $AB\ne0$ and $28A^3+125B^2=0$; $j=-3375$; and $(A,B)=(-35r^2,-98r^3)$ with $r=5B/(14A)\in\mathbb F_p^*$. For every such model, $E$ is ordinary and

$$\beta=-rH=-\frac{5B}{14A}H,\qquad H\ne0,\qquad \frac{A\beta}{BH}=-\frac5{14}=-\frac32\cdot\frac5{21}.$$

*Proof.*

1. *Recognition.* $j=-3375$ is equivalent to $3^6(28A^3+125B^2)=0$. If $j(A,B)=j(A_0,B_0)\notin\{0,1728\}$, then $(A,B)=(t^2A_0,t^3B_0)$ with $t=BA_0/(AB_0)$; with $(A_0,B_0)=(-35,-98)$ this gives $t=r=5B/(14A)$. At admissible $p$, $j\equiv-3375$ is never $0$ or $1728$: the differences are $3^35^3$ and $3^67$.
2. *Endomorphism.* $F=(x-7r)(x^2+7rx+14r^2)$, and $e^2=-7$ has a root in $\mathbb F_p$. Take $q=r(-7+e)/2$ and $u=(1+e)/2$. Then $u^2-u+2=0$. The normalized quotient is $\bigl(r^2\tfrac{35(-1+3e)}2,\;r^3(-441-245e)\bigr)=(u^4A,u^6B)$, so $\alpha=\psi_u\circ\phi_q$ is an $\mathbb F_p$-endomorphism.
3. *Slope.* Its matrix is $\begin{pmatrix}u&-q/u\\0&2/u\end{pmatrix}$, with $\lambda-\mu=u-\bar u=e\neq0$ since $p\ne7$. Theorem 1 gives $\beta(u^2-2)=-qH$, so $\beta/H=q/(2-u^2)=\dfrac{r(-7+e)/2}{(7-e)/2}=-r$.
4. *Ordinarity* follows from the quaternion argument in Theorem 5, since $\mathbb Q(\alpha)=\mathbb Q(\sqrt{-7})\neq\mathbb Q(\sqrt{-p})$. ∎

The two endomorphisms $(1\pm\sqrt{-7})/2$ give the same slope (T10: 852 checks).

**CM-value cross-checks for $D=-7$.** All give $s_2\bigl(\frac{1+\sqrt{-7}}2\bigr)=5/21$:

- loop: $c=1$, $S=5/21$;
- BOS/Masser with $\Phi_7$, exact: $\gamma=181/637875$, $s_2=5/21$;
- $q$-series to 90 digits: error below $10^{-91}$;
- PARI quasi-periods: $G=1$.

E is curve 49a1 (minimal model $[1,-1,0,-2,-1]$, conductor 49, PARI).

**Exclusions and exceptional primes for $D=-7$.**

- $p\in\{2,3,5\}$: outside the project range.
- $p=7$: ramified, and the model reduces to $(0,0)$, which is singular.
- $p\equiv3,5,6\pmod7$: inert. These are supersingular, with $H=0$ and $\beta\ne0$ (observed); the recognizer returns `not_eligible_prime`.
- Collisions: $N_D=\pm H_D(-3375)$ was factored for $D\in\{-3,-4,-8,-12,-16,-48,-64,-192,-256\}$. The prime factors are 3, 5, 7, 13, 17, 19, 31, 41, 47, 59, 83, 103, 167, 223, 311, 367, 439. **None is admissible**: each is non-split in $\mathbb Q(\sqrt{-7})$ or below 11 (`results/collision_resultants.json`).
- Denominators: 14 and 21 only.

So at every admissible prime, the $p-1$ models with $j=-3375$ (two $\mathbb F_p$-isomorphism classes, $r$ modulo squares) are disjoint from the two seeds and the six families. This was also observed exhaustively for all $p\le151$: 236,590 models scanned, zero overlaps (T3).

**Theorem 8 (signed trace).** For admissible $p$ and $E_r=(-35r^2,-98r^3)$, the trace $t=p+1-\#E_r(\mathbb F_p)$ is the unique integer with

$$4p=t^2+7v^2\ (v\in\mathbb Z),\qquad\Bigl(\frac t7\Bigr)=\Bigl(\frac rp\Bigr).$$

Equivalently, $t=(r/p)\,(t_0/7)\,t_0$ for either Cornacchia solution $t_0$. Uniqueness: class number 1 and $p=\pi\bar\pi$ leave only $(\pm t_0,\pm v_0)$ as solutions. Since $7\nmid t_0$ (otherwise $7\mid p$) and $(-1/7)=-1$, the symbol $(t/7)$ separates $\pm t_0$.

*Proof (a), via the Hecke character.* This route rests on classical facts that were not re-read in this pass. E has CM by $\mathcal O_K$, $K=\mathbb Q(\sqrt{-7})$, and conductor 49. Deuring's character $\psi$ has conductor $\mathfrak f$ with $|d_K|\,N\mathfrak f=49$, so $\mathfrak f=(\sqrt{-7})$. Then $\psi((\gamma))=\varepsilon(\gamma)\gamma$, where $\varepsilon:(\mathcal O_K/\mathfrak f)^*\cong\mathbb F_7^*\to\mathcal O_K^*=\{\pm1\}$ and $\varepsilon(-1)=-1$, so $\varepsilon$ is the Legendre symbol modulo 7. For $\pi=(t+v\sqrt{-7})/2\equiv t/2\pmod{\sqrt{-7}}$ and $(2/7)=1$, this gives $a_p=\varepsilon(\pi)(\pi+\bar\pi)=(t/7)\,t$. Twisting by $r$ multiplies the trace by $(r/p)$.

*Proof (b), 2-adic, independent of (a).*

1. $\operatorname{End}(E_r)=\mathcal O_K=\mathbb Z[\alpha]$, with $\iota(\alpha)=u$, so $\pi\in\mathcal O_K$. Since $\iota(\pi)=0$, $(t+ve)/2\equiv0$; this fixes the sign of $v$ relative to $t$.
2. $2=\alpha\bar\alpha$ splits. $T_2(E)$ is free of rank one over $\mathcal O_K\otimes\mathbb Z_2=\mathbb Z_2\times\mathbb Z_2$, so $E(\mathbb F_p)[\alpha^\infty]\cong\mathbb Z/2^a$ with $a=v_{(\alpha)}(\pi-1)$.
3. $T=(q,0)$ generates $\ker\alpha$, so $T\in2E(\mathbb F_p)$ if and only if $a\ge2$. By the halving criterion this holds if and only if $q-7r$ and $q-\bar q$ are squares; the two symbols always agree, which is observed and also forced by the next step.
4. Exactly one of $\pi\equiv\pm1\pmod{(\alpha)^2}$ holds, since $v_{(\alpha)}(2)=1$ and the residue field is $\mathbb F_2$.
5. Writing $\pi_+=x_0+y_0\alpha$, the test $\pi_+\equiv1\pmod{\alpha^2}$ is "$x_0$ odd and $(x_0-1)/2+y_0$ even". ∎

Both rules agree with naive point counts on every member with $p\le20{,}000$ tested (T1, T2: 23,868 cases, all $r$ for $p\le700$). They agree with PARI `ellap` on 36 members at primes up to $2^{62}$ (T9) and on 8,971 primes up to $2\times10^5$ for $r=1$, and with the 2-adic rule on 6,040 cases with random $r$ (exploratory runs, `theory/exploratory/sign_rule*.py`).

**Original-cubic evaluator** (`core/d7_seed.py`):

1. Validate $p$ (deterministic Miller–Rabin for $p<2^{64}$).
2. Check that $f$ is squarefree with $a\ne0$, and form $(A,B)$.
3. Recognize: $p\bmod7\in\{1,2,4\}$, $AB\ne0$, $28A^3+125B^2=0$, $r=5B/(14A)$.
4. Obtain $t$: either certify a supplied value (Hasse bound, $4p-t^2=7v^2$, $(t/7)=(r/p)$), or compute it by Cornacchia plus the sign rule.
5. Set $H=t\bmod p$, $\beta=-rH$ and $K=(\beta-\frac b3H)/a$.
6. For a query, check that $\mu$ is a nonzero, simple root of $f$, and return $T_f(\mu)=a\mu(\mu H-K)/f'(\mu)$.

An optional `endomorphism_certificate` rechecks $q$, $u$, the quotient and the Theorem-1 slope from a supplied $\sqrt{-7}$.

**Proposition 9 (control, $D=-8$).** Let $p\equiv1,3\pmod8$. The models with $j=8000$ are exactly those with $392A^3+3375B^2=0$ and $AB\ne0$, namely $(-30r^2,56r^3)$ with $r=-15B/(28A)$. Then $\beta/H=r$.

*Proof:* the kernel root $q=4r$ is rational; $u^2=-2$; Theorem 1 gives $\beta/H=q/(2-u^2)=q/4$. Validated on all $r$ for $p\le400$ (6,078 members). No trace route is certified for this control.

## 9. Cost contract

All costs below are for fixed $D$. Field operations are in $\mathbb F_p$, and bit costs are for schoolbook arithmetic.

| Phase | $D=-7$ seed | Notes |
|---|---|---|
| Exact CM value | $S=5/21$; $c$ from one Vélu step over $\mathbb Q(\sqrt{-7})$ | Precomputed once. A general fixed $D$ needs $R_D$ ($2h+1$ rationals; the table in §7 records growth). |
| Prime certification | Deterministic Miller–Rabin, $p<2^{64}$ ($O(\log p)$ exponentiations) | General $p$: AKS (deterministic polynomial), or ECPP/APR-CL in practice. Charged separately. |
| Model recognition | $p\bmod7$; $28A^3+125B^2=0$; one inversion for $r$ | $O(1)$ field operations, with no square root and no exponentiation. |
| Conjugate selection and reduction | None ($h=1$) | For the six families: retained parameter extraction, $O(1)$ for fixed $D$; or $R_D(j)$ in $O(h)$. |
| Trace preparation | $\sqrt{-7}\bmod p$; Cornacchia ($O(\log p)$ Euclidean steps on integers $\le2p$); sign via $(t_0\bmod7)$ and one Legendre symbol | The square root is deterministic for $p\equiv3\pmod4$ (exponent $(p+1)/4$) and $p\equiv5\pmod8$ (Atkin). For $p\equiv1\pmod8$ it uses Tonelli–Shanks with a **randomized** nonresidue search (expected $O(1)$ trials). Deterministic polylogarithmic only under GRH. The unconditional deterministic fallback is Schoof's algorithm, which is polynomial in $\log p$. |
| Supplied-trace certification | Hasse bound, $4p-t^2=7v^2$, $(t/7)=(r/p)$ | Deterministic; one Legendre symbol. |
| Reconstruction | $H=t\bmod p$; $\beta=-rH$; $K=(\beta-\frac b3H)/a$ | $O(1)$. |
| Supplied-root query | Root, nonzero and simplicity checks, then the formula | $O(1)$; at most three branch roots per cubic. |

No benchmark was run and no timing claim is made. A supplied trace, or PARI `ellap`, does not remove the trace cost from a complete theoretical claim.

## 10. Validation (observed output)

Environment: Python 3.13.16, PARI/GP 2.17.2 (cypari2), python-flint 0.9.0, mpmath 1.3.0, sympy 1.14.0, Linux x86_64. Dense references use flint `nmod_poly` powers, spot-checked against a pure-Python convolution. A second reference is the retained $O(p)$ recurrence and `BranchEvaluator`, imported read-only. Suite time in the final run: 72.8 s, plus 11.5 s for the fixed-$D$ checks.

| Test | Reference | Count | Failures |
|---|---|---|---|
| T1: all $r$, all admissible $p\le700$: recognition, dense $\beta\equiv-rH$, $H\ne0$, both trace rules vs naive count, retained recognizer must reject | dense, naive | 19,602 | 0 |
| T2: admissible $701\le p\le20{,}000$, $r\in\{1,$ nonsquare, 2 random$\}$ | dense, naive | 4,266 (2,143 nonsquare $r$) | 0 |
| T3: exhaustive scan of all nonsingular models, $p\le151$ | $j$ computed independently; retained recognizers | 236,590 models; 1,290 accepted ($=\sum(p-1)$); 8,124 retained | 0 overlaps |
| T4: inadmissible $p\le400$ (twist types 1 and nonsquare), $p=7$ | dense | 78; $H=0$, $\beta\ne0$ in all | 0 |
| T5: **Theorem 1 universal**, all models with $p\le67$, all closed normalized-2-isogeny walks of length ≤ 3 | dense | 22,248 with $\lambda\ne\mu$; 47,896 with $\lambda=\mu$; no supersingular non-scalar loop | 0 |
| T6: original cubics (fresh), all three branch roots | dense $f^h$ sums; retained recurrence | 444 queries | 0 |
| T7: wrong supplied traces ($-t$, $t\pm2$, $t+1$, $t+14$, $0$, $\lfloor2\sqrt p\rfloor+1$) | — | 26 accepted correct, 180 rejected wrong | 0 |
| T8: altered certificates ($r$, multiplier, family, extra key, nested key, CM label) | — | 21 valid, 147 rejected | 0 |
| T9: large primes $2^{20}$–$2^{62}$, random $r$ | PARI `ellap` (SEA; practical, uncertified) | 36 | 0 |
| T10: endomorphism certificates, both $(1\pm\sqrt{-7})/2$ | exact $\mathbb F_p$ | 852 | 0 |
| T11: $D=-8$ control, all $r$, $p\le400$ | dense | 6,078 | 0 |
| T14: `is_prime64` vs PARI `isprime` | PARI | 3,005 | 0 |
| Fixed-$D$ evaluator (§7) | dense; retained recognizers | 18,214 / 13,130 / 15,179; exhaustive 62,652 | 0 |

The theory scripts are exact unless marked otherwise:

- symbolic Vélu identities;
- loops in quadratic towers;
- class polynomials, which equal PARI `polclass` (a practical comparator);
- collision factorizations, proved prime by PARI `isprime` and multiplied back;
- period and $q$-series checks, which are numerical with explicit tail bounds and are corroboration, not proof.

Reproduction: `python run_all.py` (see `README.md`). Not done in this pass:

- the retained review suite (`retained/review/run_review.py`) was not rerun;
- no SEA implementation is included;
- large-prime controls test only the trace, since no dense coefficients are available there.

## 11. Status separation

**Classical, used as background:**

- Cartier operator facts and Cartier's theorem.
- Vélu's formulas.
- Legendre's relation.
- Weight-two behaviour of $E_2^*$.
- Katz's eigenline lemma (verified, Lemma 4.0.7).
- The conjugate filtration and unit-root theory (§3; not re-read).
- Deuring reduction and the distinctness of roots of $H_D$ (Sutherland Thm 21.14; read).
- Hecke characters and Cornacchia (not re-read).

**New, unrefereed, proved here:**

- Theorem 1 in the project chart and Corollary 2.1, the kernel-sum slope.
- Theorem 4's identification $c=\sigma_G/(a(a-\bar a))=G_2^*$ with the project's constants; classical in substance.
- Theorem 5, the comparison, with explicit exclusions.
- Theorem 6, recovery of all six formulas without the seed slope.
- Theorem 7 for $D=-7$ (elementary and complete given Theorem 1).
- Theorem 8 for $D=-7$. It is proved from standard facts that were cited but not re-read: route (a) uses Deuring's Hecke character and the conductor formula; route (b) uses freeness of $T_2$ and the halving criterion. It is also checked on 23,868 naive point counts.
- Proposition 9 ($D=-8$ control).
- Proposition 10, the uniform fixed-$D$ evaluator.
- The exact tables.

**Finite tests:** everything in §10.

**Conjectural or unverified:**

- Novelty.
- The exact contents of Katz §5.7, 8.0.9 and 8.0.13.
- The intended scope of BOS Lemma 2.3 at even $D$.
- Page and theorem references marked "not re-read".

**Failures and obstructions:**

- Literal BOS at $D=-8$ fails ($\Phi_8(j,j)\neq0$).
- In characteristic $p$, second-kind modulo exact is one-dimensional, so the matrix entries $(\mu,\nu)$ are meaningful only through characteristic-free formulas or the canonical-primitive convention.
- The retained $p=13$ counterexamples (the unchanged full-block formula modulo $p^2$, and simple unit-root replacement at precision two) are **unchanged and not reopened**. The present result is a mod-$p$ statement and supplies no Witt or precision-two correction.
- The rounded-third $p\equiv2\pmod3$ boundary was not reopened.
- Generic and supersingular $K$, growing discriminants, depth four and BSD are outside this note. Every ordinary curve has CM by some order, but that order's discriminant is typically of size about $p$, so precomputation does not give a fast generic method.

## References

Bruinier, J. H., Ono, K., & Sutherland, A. V. (2015). *Class polynomials for nonholomorphic modular functions* (arXiv:1301.5672v3). https://arxiv.org/abs/1301.5672

Cohen, H. (1993). *A course in computational algebraic number theory*. Springer. [Algorithm 1.5.3; not re-read]

Elkies, N. D. (1998). Elliptic and modular curves over finite fields and related computational issues. In D. A. Buell & J. T. Teitelbaum (Eds.), *Computational perspectives on number theory* (pp. 21–76). AMS/IP. [not re-read]

Ireland, K., & Rosen, M. (1990). *A classical introduction to modern number theory* (2nd ed.). Springer.

Katz, N. M. (1970). Nilpotent connections and the monodromy theorem. *Publications Mathématiques de l'IHÉS, 39*, 175–232. [not re-read]

Katz, N. M. (1973). p-adic properties of modular schemes and modular forms. In *Modular functions of one variable III* (LNM 350, pp. 69–190). Springer. [not re-read]

Katz, N. M. (1976). p-adic interpolation of real analytic Eisenstein series. *Annals of Mathematics, 104*(3), 459–571. https://web.math.princeton.edu/~nmk/old/padicinterp.pdf

Knapp, A. W. (1992). *Elliptic curves*. Princeton University Press. [not re-read]

Masser, D. W. (1975). *Elliptic functions and transcendence* (LNM 437). Springer. [not obtained]

Oda, T. (1969). The first de Rham cohomology group and Dieudonné modules. *Annales scientifiques de l'ÉNS, 2*, 63–135. [not re-read]

Schoof, R. (1985). Elliptic curves over finite fields and the computation of square roots mod p. *Mathematics of Computation, 44*(170), 483–494. [not re-read]

Serre, J.-P. (1958). Sur la topologie des variétés algébriques en caractéristique p. In *Symposium internacional de topología algebraica* (pp. 24–53). [not re-read]

Silverman, J. H. (1994). *Advanced topics in the arithmetic of elliptic curves*. Springer. [not re-read]

Sutherland, A. V. (2023). *18.783 Elliptic curves, Lecture 21*. MIT. https://math.mit.edu/classes/18.783/2023/LectureNotes21.pdf

Vélu, J. (1971). Isogénies entre courbes elliptiques. *Comptes Rendus de l'Académie des Sciences de Paris, Série A, 273*, 238–241. [not re-read]

## Appendix A. Exact data for class number 4

In each block, $j$ is given in the tower basis, followed by $S$ and $H_D$ (low→high). $R_D$ is in `results/cm_tables.json`.

**$D=-192$** ($e^2=3$, $g^2=2$):

- $j=2010450259344609000+1160733998424384000e+1421603011620136125g+820762881440077125eg$
- $S=\frac{569844035}{1170843179}+\frac{2578473000}{26929393117}e-\frac{23275500}{1170843179}g+\frac{2613718260}{26929393117}eg$
- $H_D=[-1080060886113159937649308593750000,\ 826335556188178615474500000000,\ 15705521635909735050750000,\ -8041801037378436000,\ 1]$

**$D=-256$** ($w=s^2=\sqrt2$, $s^4=2$):

- $j=1690291743695465540328+1195216754150697417216w+1421360268006467529594s+1005053484016501794441ws$
- $S=\frac{247571}{447051}+\frac{46520}{447051}w+\frac{251480}{3129357}s+\frac{22360}{447051}ws$
- $H_D=[-1064410681181869521037208505239142408,\ 26925623396663008311375890966784,\ -1826592673506207200904172752,\ -6761166974781862161312,\ 1]$
