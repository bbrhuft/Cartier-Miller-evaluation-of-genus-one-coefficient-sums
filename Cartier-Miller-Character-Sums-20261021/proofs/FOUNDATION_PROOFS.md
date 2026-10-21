# Normalization and the trace-supplied evaluator

These arguments are independent derivations for this repair. They use standard Cartier properties, the elliptic Frobenius characteristic equation, and the Miller divisor recurrence. They do not use an inherited exceptional-normalization lemma, a characteristic-zero lift, or experimental selection of a sign. They are written for specialist review; computation is supporting evidence rather than a substitute for the arguments.

## Conventions and the local Miller coefficient

Let \(p\ge5\) be prime, let \(E/\mathbb F_p\) have short equation \(y^2=W(x)=x^3+ux+v\) with nonzero discriminant, and set \(\omega=dx/(2y)\), \(t=-x/y\). All coefficient identities below are in characteristic \(p\). For a point \(Q\) and positive integer \(m\), choose a Miller function with divisor

\[
\operatorname{div}(f_{m,Q})=m(Q)-([m]Q)-(m-1)(O).
\]

Set \(f_{m,O}=1\). A nonzero multiplicative constant has no effect on its logarithmic differential. Define \(\alpha_m(Q)\) to be the constant coefficient of \((d f_{m,Q}/f_{m,Q})/dt\) at \(O\). The expansions \(x=t^{-2}+O(t^2)\), \(y=-t^{-3}+O(t)\), \(\omega=(1+O(t^4))dt\) show that the same constant is obtained relative to \(\omega\), even when the differential has a simple pole at \(O\). The absence of a term linear in \(t\) in \(\omega/dt\) matters here.

For points \(S,T\), choose \(g_{S,T}\) with divisor \((S)+(T)-(S+T)-(O)\). When neither operand nor their sum is \(O\) and the line slope is \(\lambda\), use

\[
g_{S,T}=\frac{y-\lambda x-\nu}{x-x(S+T)}.
\]

Its numerator has expansion \(-t^{-3}(1+\lambda t+O(t^2))\) and its denominator has expansion \(t^{-2}(1+O(t^2))\). Hence its logarithmic differential has constant \(\lambda\). For a vertical step \(T=-S\) use \(x-x(S)\), whose logarithmic differential has constant zero. If either operand is \(O\) use 1, again with constant zero. These definitions also cover tangent doubling at a 2-torsion point.

The divisor recurrence \(f_{m+n,Q}\doteq f_{m,Q}f_{n,Q}g_{[m]Q,[n]Q}\) therefore proves the slope accumulation rule for every step, including an intermediate multiple equal to \(O\). No condition excluding such chains is needed. Binary accumulation takes \(O(\log m)\) field operations and inversions. This proves the meaning of the implemented accumulator, not only its agreement on generic chains.

A second divisor calculation, valid for any points S,T, gives

\[
f_{m,S+T}\ \doteq\
f_{m,S} f_{m,T}\frac{g_{[m]S,[m]T}}{g_{S,T}^{m}},
\]

Here dotted equality means equality up to a nonzero constant. Thus, if \(\kappa(S,T)\) is the local constant of \(d\log g_{S,T}\),

\[
\alpha_m(S+T)=\alpha_m(S)+\alpha_m(T)
+\kappa([m]S,[m]T)-m\kappa(S,T).
\tag{1}
\]

In particular \(\alpha_p\) is additive when one summand is \(p\)-torsion, since its multiplied endpoint is \(O\). Negation sends \(t\) to \(-t\) and gives \(\alpha_m(-S)=-\alpha_m(S)\).

## A Cartier identity over the algebraic closure

Write

\[
W(x)^{(p-1)/2}=U(x)+A x^{p-1}+x^p V(x),\qquad \deg U\le p-2.
\]

Let \(P=(a,b)\) be rational over \(\mathbb F_p\) with \(b\ne0\), and let \(Q\) be any geometric point satisfying \([p]Q=P\). Such a \(Q\) exists because multiplication by \(p\) is a nonconstant surjective morphism. Put \(\alpha=\alpha_p(Q)\). The following identity is the common source of both cases:

\[
\boxed{\ bV(a)=A\alpha-\alpha^p.\ }
\tag{2}
\]

To prove it, let

\[
\vartheta_P=\frac{y+b}{x-a}\omega.
\]

It has residues +1 at \(P\) and -1 at \(O\), with no other poles. Since \(W(a)^{(p-1)/2}=1\), put \(q=(W^{(p-1)/2}-1)/(x-a)\). Polynomial division gives \([x^{p-1}]q=V(a)\), and \(\deg q<2p-1\). Using \(C(g^p\eta)=gC(\eta)\), \(C(d\log h)=d\log h\), and \(1/y=W^{(p-1)/2}/y^p\), the coefficient rule for Cartier on \(q\,dx\) gives

\[
C\left(\frac{dx}{(x-a)y}\right)
=\frac1y\left(V(a)dx+\frac{dx}{x-a}\right),
\qquad (C-1)\vartheta_P=bV(a)\omega.
\tag{3}
\]

Let \(\theta=-d\log f_{p,Q}\). Its divisor multiplicity \(p\) at \(Q\) contributes no pole to its logarithmic differential. Its other residues are +1 at \(P\) and -1 at \(O\); these statements still hold if \(Q=P\), since multiplicities are combined before reduction modulo \(p\). Therefore \(\vartheta_P-\theta\) is holomorphic. At \(O\),

\[
\vartheta_P/\omega=-t^{-1}+O(t),\qquad
\theta/\omega=-t^{-1}-\alpha+O(t),
\]

because \(\operatorname{ord}_O(f_{p,Q})=-(p-1)\). Hence \(\vartheta_P-\theta=\alpha\omega\). Now \(C(\theta)=\theta\) and \(C(\omega)=A^{1/p}\omega\). Applying \(C-1\) gives \(bV(a)=(A\alpha)^{1/p}-\alpha\). Raising to \(p\), and using \(a,b,A,V(a)\in\mathbb F_p\), proves (2). This derivation does not assume ordinarity.

## The general trace and its complete chain proof

Let \(n=\#E(\mathbb F_p)\) with \(\gcd(p,n)=1\), and set \(Q=[p^{-1}\bmod n]P\). This is rational, \([p]Q=P\), and its Miller coefficient lies in \(\mathbb F_p\). Equation (2) becomes

\[
\boxed{\ bV(a)=(A-1)\alpha_p(Q).\ }
\tag{4}
\]

The preceding local lemma proves (4) for all binary chains, including chains passing through \(O\) and curves with \(A=0\). A group order coprime to \(p\) is the exact hypothesis needed for the inversion of \(p\) modulo \(n\).

## The exceptional sign, established symbolically

Assume the signed integer trace is exactly 1, so \(n=p\) and \(A=1\). Let \(\Phi\) be Frobenius and let \(\mathcal V\) be its dual Verschiebung. The elliptic Frobenius relation gives

\[
\Phi+\mathcal V=[1],\qquad \Phi\mathcal V=[p].
\]

For nonzero \(P\in E(\mathbb F_p)\), choose \(Q\) with \([p]Q=P\). Since \(\Phi(\mathcal VQ)=P=\Phi(P)\) and Frobenius is injective on geometric points, \(\mathcal VQ=P\), and consequently \(\Phi Q=Q-P\). Galois compatibility of the Miller coefficient and (1) give

\[
\alpha_p(Q)^p=\alpha_p(\Phi Q)
=\alpha_p(Q-P)=\alpha_p(Q)-\alpha_p(P).
\]

Here \([p](-P)=O\), so the endpoint \(\kappa\) term in (1) is zero and its source term is multiplied by \(p\). Applying (2) with \(A=1\) therefore proves

\[
\boxed{\ bV(a)=\alpha_p(P).\ }
\tag{5}
\]

The sign is +1 relative to \(\omega=dx/(2y)\) and \(t=-x/y\). No test among candidate constants and no interpretation of a quasi-period sign is used. Since \(\operatorname{div}f_{p,P}=p(P)-p(O)\), its logarithmic differential is holomorphic and equals \(\alpha_p(P)\omega\). At an auxiliary affine point \(T=(r,s)\) with \(s\ne0\) and outside the support, the coefficient measured using \(d/dx\) is \(\alpha_p(P)/(2s)\). This states the precise conversion to Semaev-style evaluation. On \(p\)-torsion, the divisor representative \((P)-(-P)\) corresponds to twice the class \((P)-(O)\), so its transfer coefficient is twice this one.

## Character sums and a complete cubic/quartic adapter

For a squarefree cubic or quartic \(f\) and any \(a\), let \(F=f^{(p-1)/2}=L+x^pH\) with \(\deg L<p\). Polynomial division and finite-field power sums prove

\[
C_f(a):=\sum_{x\ne a}\frac{\chi(f(x))}{x-a}=-F'(a)-H(a).
\tag{6}
\]

Indeed \(Q=(F-F(a))/(x-a)\) has degree at most \(2p-3\), \(\sum_x Q(x)=-[x^{p-1}]Q=-H(a)\), and the excluded value is \(Q(a)=F'(a)\). At a nonbranch point \(F'(a)=-\chi(f(a))f'(a)/(2f(a))\). This statement includes branch values in its polynomial form, although the fast evaluator below is restricted to nonbranch poles.

For \(f(a)\ne0\), set \(e=\chi(f(a))\) and \(g(z)=f(a+z)/f(a)\). Then \(g(0)=1\), \(C_f(a)=eC_g(0)\), and the signed projective trace of \(v^2=g(z)\) is \(\tau_t=e\tau_f\). No square root is needed. Write \(g=1+a_1z+a_2z^2+a_3z^3+a_4z^4\), setting \(a_4=0\) in the cubic case. A short model \(Y^2=X^3+uX+v_0\), with \((0,1)\) as \(O\), has

\[
u=-4a_4+a_1a_3-a_2^2/3,\quad
v_0=a_3^2-8a_2a_4/3+a_1^2a_4-a_1a_2a_3/3+2a_2^3/27.
\]

For \(z\ne0\), use the explicit map

\[
\begin{aligned}
x_0&=\frac{2(v+1)+a_1z}{z^2},&
y_0&=\frac{4(v+1)+2(a_1z+a_2z^2)-a_1^2z^2/2}{z^3},\\
X&=x_0+a_2/3,&Y&=y_0+(a_1x_0+2a_3)/2.
\end{aligned}
\]

It extends to an isomorphism of smooth projective curves. Its inverse on a dense open set follows from (7) below and then \(v=(x_0z^2-a_1z)/2-1\). The point \((0,-1)\) maps to the nonzero point \(R=(r,s)\), where

\[
r=a_1^2/4-2a_2/3,\qquad s=-a_3+a_1a_2/2-a_1^3/8.
\]

Substitution proves the curve equation and the rational-function identity

\[
\boxed{\ \frac1z=\frac12 h_R-\frac{a_1}{4},\qquad
h_R=\frac{Y+s}{X-r}.\ }
\tag{7}
\]

The latter identity is exact already before imposing \(v^2=g(z)\). Smoothness and the birational inverse ensure the projective extension. Zeros and poles are treated as values of rational functions on the smooth curve, with regular limits at removable points.

If \(s\ne0\), the value of \(h_R\) at \(-R\) is \(-W'(r)/(2s)\). Summing fibres with \(X\ne r\) and using \(\sum_{x\ne r}1/(x-r)=0\) yields

\[
\sum_{T\in E(F_p)\setminus\{O,R\}}h_R(T)
=s C_W(r)-\frac{W'(r)}{2s}=-sV_W(r).
\tag{8}
\]

The last equality follows from (6). If \(s=0\), \(R\) is nonzero 2-torsion and \(h_R=Y/(X-r)\). Negation pairs all nonfixed terms with opposite signs; the remaining fixed points contribute zero. Thus the sum in (8) is zero, without division by \(s\).

The rational function \(1/z\) vanishes at the points at infinity of \(v^2=g(z)\), so their inclusion contributes zero. Its affine point sum away from \(z=0\) equals \(C_g(0)\), because the extra baseline \(\sum_{z\ne0}1/z\) is zero. There are \(n=p+1-\tau_t\) points on the short curve and exactly two excluded points \(O,R\). Equations (4), (5), (7), and (8) now prove the complete formulas

\[
C_f(a)=e\left[-\frac{a_1}{4}(n-2)
-\frac{\tau_t-1}{2}\alpha_p([p^{-1}\bmod n]R)\right]
\quad (\gcd(p,n)=1, s\ne0),
\tag{9}
\]

\[
C_f(a)=e\left[\frac{a_1}{2}-\frac{\alpha_p(R)}2\right]
\quad (\tau_t=1),
\tag{10}
\]

\[
C_f(a)=-e\frac{a_1}{4}(n-2)\quad(s=0).
\tag{11}
\]

The Hasse invariant of the short curve is congruent to \(\tau_t\) modulo \(p\). In the case \(\gcd(p,n)=1\), \(s=0\) also gives \(\alpha_p(R)=0\): the inverse of \(p\) modulo even \(n\) is odd and fixes \(R\), and \(f_{p,R}\) is proportional to \((X-r)^{(p-1)/2}\), with zero local logarithmic constant. Thus (11) agrees with (9) extended to this case. In (10), \(n=p\) is odd, so nonzero rational 2-torsion cannot occur.

For \(p\ge7\), the Hasse bound implies \(p\mid n\) if and only if \(\tau_t=1\). For \(p=5\), \(\tau_t=-4\) gives \(n=10\) as an additional possibility. The implementation uses bounded enumeration for every \(p=5\) input. Opus's report already assumed \(p\ge7\) globally; the earlier review overstated the \(p=5\) example if read as a counterexample to that theorem. It is an API boundary repair and an extension.

## Field and bit costs, with preparation explicit

Let \(\ell=\lceil\log_2p\rceil\), let \(M(\ell)\) and \(I(\ell)\) be modular multiplication and inversion bit costs, and let \(E(\ell)\) bound the integer extended-gcd cost for finding \(p^{-1}\) modulo \(n\). For fixed degree, normalization, model formation, and the 2-torsion test cost \(O(1)\) field operations apart from \(e=\chi(f(a))\), which takes \(O(\ell)\) operations by exponentiation. Scalar multiplication and one Miller pass each use \(O(\ell)\) field operations and at most \(O(\ell)\) inversions, with a constant number of field registers. The trace is an independently charged input. Constant-degree squarefreeness validation adds \(O(1)\) field operations; primality certification is an input obligation, not hidden in this query cost.

Thus the per-query field cost after trace preparation is \(O(\ell)\), counting inversions as field operations, and a safe bit bound is

\[
O\bigl(E(\ell)+\ell(M(\ell)+I(\ell)+\ell)\bigr).
\tag{12}
\]

Classical multiplication and Euclidean inversion give \(O(\ell^3)\) bit operations. With fast multiplication, inversion, and gcd, the bound is \(\widetilde O(\ell^2)\). It is not \(O(\log p)\) bit time. Cold time adds the chosen exact-trace procedure, with that procedure's own hypotheses and cost. Constant-size \(p=5\) enumeration does not change the asymptotics.

For \(s\) distinct simple poles and a supplied partial-fraction weight, the existing common-domain correction gives \(O(s\ell+s^2)\) field operations after trace acquisition, or \(O(s\ell+\mathsf M_{\rm poly}(s)\log(s+1))\) with product/remainder-tree corrections. A constant term uses the trace-derived unweighted character sum, and each excluded point must be removed from every single-pole oracle that still includes it. These bounds do not grant the same cost to branch poles, higher-order poles, implicit factorization, or arbitrary rational weights. Existing admissibility and exclusion statements remain essential.
