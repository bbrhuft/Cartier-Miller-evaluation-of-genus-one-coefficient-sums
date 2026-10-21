# A uniform curve-order coefficient identity

21 October 2026. This is a derivation in this project from classical Cartier, Frobenius, and Miller identities. Publication priority for the combined scalar identity is not established. The computational local-coefficient construction must be attributed to its classical antecedents, including Rück (1999, p. 806).

## Statement

Let \(p\ge5\), let \(E/\mathbb F_p\) be the nonsingular short curve \(y^2=W(x)=x^3+ux+v\), and put \(\omega=dx/(2y)\), \(t=-x/y\), and \(N=\#E(\mathbb F_p)=p+1-\tau\). Write

\[
W(x)^{(p-1)/2}=U(x)+A x^{p-1}+x^pV(x),\qquad \deg U\le p-2,
\]

so \(A\equiv\tau\pmod p\). Let \(f_{m,S}\) have divisor \(m(S)-([m]S)-(m-1)(O)\), and let \(\alpha_m(S)\) be the constant coefficient at \(O\) of \(d\log f_{m,S}\) relative to \(dt\). Use \(f_{m,O}=1\). The coefficient is unchanged if a Miller function is multiplied by a nonzero scalar.

For every rational nonbranch \(P=(a,b)\),

\[
\boxed{\alpha_N(P)=bV(a).}
\tag{U1}
\]

The same formula holds at a rational 2-torsion point, with both sides zero. At \(O\), set the coefficient to zero. There is no hypothesis that \(p\) and \(N\) be coprime and no restriction to ordinary curves.

When \(p\nmid N\), the differential \(d\log f_{N,P}\) has poles at \(P,O\). The coefficient in (U1) is its Laurent constant, not its value at \(O\), and not an asserted homomorphism from the entire curve group to \(\mathbb F_p^+\).

## Local and composition identities

On a short model, \(x=t^{-2}+O(t^2)\), \(y=-t^{-3}+O(t)\), and \(\omega=(1+O(t^4))dt\). A nonvertical Miller line ratio has expansion \(-t^{-1}(1+\lambda t+O(t^2))\), hence logarithmic constant \(\lambda\). A vertical step has constant zero, and an identity step uses the function 1. This proves slope accumulation even when an intermediate multiple is \(O\). The full proof and explicit cubic/quartic model calculations are retained in FOUNDATION_PROOFS.md.

Let \(g_{S,T}\) have divisor \((S)+(T)-(S+T)-(O)\), and let \(\kappa(S,T)\) be its logarithmic constant. Comparing divisors gives

\[
\alpha_m(S+T)=\alpha_m(S)+\alpha_m(T)
+\kappa([m]S,[m]T)-m\kappa(S,T).
\tag{U2}
\]

In particular, for \([p]T=O\), \(\alpha_p(Q-T)=\alpha_p(Q)-\alpha_p(T)\). Negation changes the sign of the local coefficient. A separate divisor comparison gives the composition identity

\[
f_{mn,Q}\doteq f_{m,Q}^{\,n} f_{n,[m]Q},\qquad
\alpha_{mn}(Q)=n\alpha_m(Q)+\alpha_n([m]Q).
\tag{U3}
\]

These statements hold for geometric points and include zero endpoints; dotted equality allows a nonzero constant factor.

## Proof of the uniform identity

Choose a geometric point \(Q\) with \([p]Q=P\), and put \(\alpha=\alpha_p(Q)\). The Cartier calculation in the preceding repair proves

\[
bV(a)=A\alpha-\alpha^p.
\tag{U4}
\]

For completeness, put \(\vartheta_P=((y+b)/(x-a))\omega\) and \(\theta=-d\log f_{p,Q}\). They have the same residues, and their difference is \(\alpha\omega\), as seen at \(O\). Dividing \(W^{(p-1)/2}-1\) by \(x-a\) gives a polynomial whose \(x^{p-1}\) coefficient is \(V(a)\). The Cartier coefficient rule therefore gives \((C-1)\vartheta_P=bV(a)\omega\). Using \(C(\theta)=\theta\) and \(C(\omega)=A^{1/p}\omega\), and raising to \(p\), yields (U4). All field elements on its left lie in \(\mathbb F_p\).

Let \(\Phi\) be Frobenius and \(\mathcal V\) its dual. Since \(\Phi\mathcal V=[p]\), the equality \(\Phi(\mathcal VQ)=P=\Phi(P)\) and injectivity of Frobenius on geometric points imply \(\mathcal VQ=P\). Thus the Frobenius trace relation gives

\[
\Phi Q=[\tau]Q-P=[\tau-p]Q=Q-[N]Q.
\]

Set \(T=[N]Q\). It is \(p\)-torsion because \([p]T=[N]P=O\). Galois compatibility and (U2) give

\[
\alpha^p=\alpha_p(\Phi Q)=\alpha_p(Q-T)=\alpha-\alpha_p(T).
\tag{U5}
\]

Applying (U3) in both orders gives, in characteristic \(p\),

\[
N\alpha+\alpha_N(P)=\alpha_{pN}(Q)
=p\alpha_N(Q)+\alpha_p(T)=\alpha_p(T).
\tag{U6}
\]

Substituting (U5) and (U6) into (U4) yields

\[
bV(a)=(A-1+N)\alpha+\alpha_N(P)=\alpha_N(P),
\]

since \(A-1+N\equiv\tau-1+p+1-\tau=0\pmod p\). This proves (U1) without a trace case split. If \(P=(a,0)\) is rational 2-torsion, then \(N\) is even and \(f_{N,P}\doteq(x-a)^{N/2}\), whose local logarithmic constant is zero. This supplies that remaining case. The geometric point \(Q\) is only a proof device; the algorithm never constructs it.

## A single formula for cubic and quartic character sums

For squarefree \(f\) of degree 3 or 4 and \(f(a)\ne0\), set

\[
e=\chi(f(a)),\qquad g(z)=\frac{f(a+z)}{f(a)},\qquad
g_1=\frac{f'(a)}{f(a)},\qquad \widetilde\tau=e\tau_f,\qquad
N=p+1-\widetilde\tau.
\]

On the short model of \(v^2=g(z)\) with \((0,1)\) as origin, let \(R\) be the image of \((0,-1)\). The already proved identities are

\[
\frac1z=\frac12\frac{Y+Y_R}{X-X_R}-\frac{g_1}{4},\qquad
\sum_{S\ne O,R}\frac{Y(S)+Y_R}{X(S)-X_R}=-\alpha_N(R).
\]

The second identity uses (U1) when \(Y_R\ne0\), and negation plus \(\alpha_N(R)=0\) when \(R\) is 2-torsion. Regular limits are used at removable points. Consequently,

\[
\boxed{\quad
C_f(a)=\chi(f(a))\left(-\frac{g_1}{4}(N-2)-\frac{\alpha_N(R)}2\right).
\quad}
\tag{U7}
\]

This requires just normalization, a constant-size model change, and one differentiated Miller chain with scalar \(N\). The exact signed trace is supplied and separately charged. No square root, inversion of \(p\) modulo \(N\), preliminary scalar multiplication, anomalous branch, explicit 2-torsion branch, or small-field enumeration is required. The identity-step conventions remain essential.

The formula includes \(p=5\), where a twisted curve order can be \(2p\). For the previous API example \(p=5,f=x^3+3x,a=1,\tau=-4\), it gives 1 by the uniform chain. Opus's original report assumed \(p\ge7\), so this is an extension rather than a counterexample to that report.

For \(p\nmid N\), comparison with the previous general-trace identity gives

\[
\alpha_N(P)=(A-1)\alpha_p([p^{-1}\bmod N]P).
\]

For trace one, \(N=p\) and (U1) is exactly the positive exceptional normalization. The same trace-dependent scalar \(p+1-\chi\tau_f\) already appears as the annihilator in the original Cartier–Miller formulation; this identity helps explain the relationship rather than establish an unrelated new algorithm.

For the representative \((P)-(-P)\) on this short model, the function \(f_{N,P}/f_{N,-P}\) has divisor \(N((P)-(-P))\) and local logarithmic constant \(2\alpha_N(P)=2bV(a)\). This identifies the factor of two for that representative with the stated differential and parameter. A change of differential or reversal of the divisor must be accounted for explicitly when comparing another normalization.

## Cost and attribution

For \(\ell=\lceil\log_2p\rceil\), the query costs \(O(\ell)\) field operations including inversions, with a constant number of field registers. A safe bit bound is \(O(\ell(M(\ell)+I(\ell)+\ell))\), giving \(O(\ell^3)\) with classical arithmetic and soft-\(O(\ell^2)\) with fast arithmetic, after trace acquisition. No new timing claim is made.

Miller's short function construction, Semaev's differentiated evaluation on \(p\)-torsion, and Rück's local-coefficient cocycle are classical. Gunji supplies earlier Cartier/logarithmic-differential structure on ordinary elliptic curves. The source check did not locate (U1) or (U7) explicitly in the four newly supplied sources. The derivation above is recorded as a deduction in this project, with historical priority left unresolved. It supplies no new discrete-logarithm attack on ordinary curves.
