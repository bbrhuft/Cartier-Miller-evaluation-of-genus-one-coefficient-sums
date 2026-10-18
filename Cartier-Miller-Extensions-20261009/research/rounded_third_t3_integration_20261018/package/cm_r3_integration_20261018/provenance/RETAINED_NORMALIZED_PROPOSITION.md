# Rounded-third boundary: an explicitly normalized de Rham proposition

David Jordan research project, 14 October 2026. Unrefereed, AI-assisted mathematics for independent human review. This version develops Opus's corrected argument and makes the function-field exactness qualification explicit. Computational evidence is recorded separately in `REVIEW.md` and `results/`; it does not establish the cohomological statements.

## Statement and conventions

Let $p\ge5$ be prime with $p\equiv2\pmod3$. Work over $k=\mathbb F_p$, and put

$$
h=\frac{p-1}{2},\qquad m=\frac{p-2}{3},\qquad L=m+1=\frac{p+1}{3},\qquad
a_j=\binom{2j}{j}8^{-j},\qquad G=m!\pmod p.
$$

Here $m$ is odd and $L$ is even. Let $E$ be the smooth projective curve with affine equation $y^2=f(x)=x^3+1/4$, identity $O$, and differential $\omega=dx/y$. Write uniquely

$$f(x)^h=T(x)+x^pS(x),\qquad \deg T<p.$$

Let $U=E\setminus\{O\}$ and $W=E\setminus\{(0,1/2),(0,-1/2)\}$. A Čech–de Rham cocycle is a triple $(\alpha_U,\alpha_W,g)$ with $\alpha_U-\alpha_W=dg$; a coboundary is $(du_U,du_W,u_U-u_W)$. Define

$$
e_1=[(\omega,\omega,0)],\qquad
e_2=\left[\left(x\omega,\frac{\omega}{2x^2},\frac{2y}{x}\right)\right].
$$

The Cartier convention is $\mathcal C(\sum_{i=0}^{p-1}u_i^px^i\,dx)=u_{p-1}dx$ in the function field. In particular $\mathcal C(v^p\alpha)=v\mathcal C(\alpha)$ and $\mathcal C(dv)=0$. Define the two maps on cocycles by

$$
V_{\mathcal C}[(\alpha_U,\alpha_W,g)]
=[(\mathcal C\alpha_U,\mathcal C\alpha_W,0)],\qquad
F_{\rm abs}[(\alpha_U,\alpha_W,g)]=[(0,0,g^p)].
$$

These are linear over $\mathbb F_p$. After base extension to a perfect field, the same conventions give $\sigma^{-1}$-semilinear $V_{\mathcal C}$ and $\sigma$-semilinear $F_{\rm abs}$, with the associated Frobenius twists understood. No inverse Frobenius is applied to a general coefficient without stating it.

**Proposition.** The classes $(e_1,e_2)$ form a basis of $H^1_{\rm dR}(E/k)$. For every prime in the branch,

$$
d(yS)=a_L\omega,\qquad \mathcal C(\omega)=0,\qquad
\mathcal C(x\omega)=\mathcal C\left(\frac{\omega}{2x^2}\right)=2a_L\omega.
$$

With columns giving images of basis vectors, the matrices are

$$
[V_{\mathcal C}]_{(e_1,e_2)}=
\begin{pmatrix}0&2a_L\\0&0\end{pmatrix},\qquad
[F_{\rm abs}]_{(e_1,e_2)}=
\begin{pmatrix}0&-2a_L\\0&0\end{pmatrix}.
$$

The nonzero entry satisfies

$$
2a_L=3G^{-3}\quad\text{in }\mathbb F_p,\qquad
2a_L\equiv3\Gamma_p(1/3)^{-3}\pmod p.
$$

The latter statement uses Morita's gamma function and is only a congruence of $p$-adic units. The usual genus-one Cartier–Manin matrix on $H^0(E,\Omega^1)$ is the single entry $0$. The displayed $2\times2$ matrix concerns full de Rham cohomology in the specified basis.

## Polynomial and Cartier proof

For any polynomial $P$, put $\Theta(P)=fP'+f'P/2$. Differentiating $y^2=f$ gives $d(yP)=\Theta(P)\omega$. Since $h+1/2=p/2=0$ in $k$, $\Theta(f^h)=0$. Also $\Theta(x^pP)=x^p\Theta(P)$, so

$$\Theta(T)=-x^p\Theta(S).$$

The expansion is $f^h=\sum_{j=0}^h\binom hj4^{j-h}x^{3j}$. The coefficient $c_{p-1}$ vanishes, and $\deg T=p-2$. Thus $\deg\Theta(T)\le p$, while $x^p$ divides it. Consequently $\Theta(S)$ is constant. Evaluating at zero gives

$$\Theta(S)=\frac14c_{p+1}=\binom hL4^{L-h-1}.$$

For $j<p$, the binomial identity at $h\equiv-1/2$ yields $a_j=(-2)^{-j}\binom hj$. Therefore

$$
\binom hL4^{L-h-1}
=(-1)^L2^{3L-2h-2}a_L=a_L,
$$

because $L$ is even and $3L-2h-2=0$. This proves the full differential identity, including every polynomial coefficient.

For a Laurent polynomial $R$, use $y^{-1}=(y^{-1})^pf^h$ to obtain

$$
\mathcal C(R\omega)=
\left(\sum_{n\equiv-1\ (p)}[x^n](Rf^h)x^{(n+1)/p-1}\right)\omega.
$$

All coefficients are in $\mathbb F_p$, so their $p$th roots are themselves. For $R=1$ the only selected coefficient is $c_{p-1}=0$. For $R=x$ the selected coefficient is $c_{p-2}$. The integer identity $\binom h{L-1}=2\binom hL$ follows from $h-L+1=L/2$, and hence $c_{p-2}=2a_L$. For $R=1/(2x^2)$, the possible terms are $c_1/(2x)$ and $c_{p+1}/2$. They give $0+2a_L$. This proves all stated Cartier identities.

## Basis and maps

The two opens are affine. For example, $W$ has coordinates $u=1/x$, $v=y/x^2$ and equation $v^2=u+u^4/4$, including $O=(0,0)$. The differential $\omega$ is regular and nonvanishing; $x$ and $y$ have poles of orders $2$ and $3$ at $O$.

Both differential components of $e_2$ are regular on their respective opens. Its transition function is regular on their intersection. Direct differentiation gives

$$d(2y/x)=\left(x-\frac1{2x^2}\right)\omega,$$

so it is a cocycle. The injection $H^0(E,\Omega^1)\to H^1_{\rm dR}(E)$ is injective: a cocycle $(\alpha,\alpha,0)$ which is a coboundary would have a global regular primitive, and every global regular function is constant. The kernel of projection to $H^1(E,\mathcal O_E)$ consists exactly of these global differential classes, by subtracting a coboundary when the transition function is a Čech coboundary.

The class of $2y/x$ in $H^1(E,\mathcal O_E)$ is nonzero. Otherwise $2y/x=u_U-u_W$ would force $u_U$ to have a single simple pole at $O$. Riemann–Roch on a genus-one curve gives $L(O)=k$, which forbids that pole. Since both $H^0(E,\Omega^1)$ and $H^1(E,\mathcal O_E)$ have dimension one, $e_1,e_2$ are independent and span. This argument also establishes dimension two without assuming a splitting beforehand.

The standard local properties of Cartier ensure regularity on both opens. It kills $dg$, so the two Cartier images agree and define a global differential. It kills coboundaries as well. Thus $V_{\mathcal C}$ is well-defined by the formula above. The formula for $F_{\rm abs}$ is well-defined because $d(g^p)=0$ and the Frobenius of a coboundary is the coboundary of the $p$th powers. These are the customary de Rham Frobenius and Cartier-induced Verschiebung conventions; the explicit calculations below do not require a comparison with an integral Dieudonné module.

Cartier gives $V_{\mathcal C}e_1=0$ and $V_{\mathcal C}e_2=2a_Le_1$. Frobenius kills $e_1$. For the second column, write

$$
(2y/x)^p=2yS+2yT/x^p=u_U-u_W,
\qquad u_U=2yS,\quad u_W=-2yT/x^p.
$$

The first function is regular on $U$. The second is regular on $W$: at $O$ its order is at least $-3-2(p-2)+2p=1$. Both differentials equal $2a_L\omega$, using $\Theta(T)=-x^p\Theta(S)$. Subtracting the coboundary $(du_U,du_W,u_U-u_W)$ from $(0,0,(2y/x)^p)$ gives $-2a_Le_1$. This proves the stated signs and matrices.

## Exactness, gamma normalization, and interpretation

The identity $a_L\omega=d(yS)$ holds in the function field, while $a_Le_1$ is nonzero in projective de Rham cohomology. The injectivity already proved and $a_L\ne0$ suffice to establish this distinction. More concretely, $\deg S=h-1$ with leading coefficient one, so $yS$ has a pole of order exactly $p$ at $O$. Every other function-field primitive is $yS+v^p$. If it were globally regular, $v$ would be regular on $U$ and have exactly one simple pole at $O$, contradicting $L(O)=k$.

**The regularity qualification is essential.** Pole cancellation at $O$ alone is possible: indeed

$$yS-(y/x)^p=-yT/x^p$$

is regular at $O$. But this cancellation introduces poles at the points with $x=0$. It does not produce a global primitive. Thus the assertion that no $p$th power can cancel the pole without any qualification is false. The Čech computation measures precisely this failure of a global primitive.

For the factorial normalization, Wilson's theorem and the parity of $m$ give $(2m)!=-3G^{-1}$ and $8^m=1/2$. Hence $a_m=-6G^{-3}$, and the ratio $a_L/a_m=(2m+1)/(4L)=-1/4$ gives $a_L=(3/2)G^{-3}$. Cubing is bijective on $\mathbb F_p^\times$, with inverse exponent $(2p-1)/3$. Therefore, if $c=2a_L$, then

$$G=(3/c)^{(2p-1)/3}.$$

The normalized scalar and $m!\bmod p$ are equivalent with $O(\log p)$ additional field operations. This is a reduction, not a lower bound.

Morita's definition on positive integers is $\Gamma_p(N)=(-1)^N\prod_{0<j<N,\ p\nmid j}j$. Wilson shows $\Gamma_p(N+p)\equiv\Gamma_p(N)\pmod p$. Continuity then gives $\Gamma_p(z)\equiv(-1)^n(n-1)!$ when $z\equiv n\pmod p$ and $1\le n\le p$. Since $1/3\equiv L$ and $L$ is even, $\Gamma_p(1/3)\equiv G$. No identification with a Chowla–Selberg period is claimed.

Over a perfect extension, rescaling the basis to $(\mu e_1,\lambda e_2)$ replaces the Verschiebung entry by $2a_L\lambda^{1/p}/\mu$. Thus the scalar requires the model, representative, and basis normalization. The vanishing trace or abstract supersingular isomorphism type does not specify it in this basis; this observation does not exclude an independent arithmetic algorithm.

For orientation, in the ordinary branch $p\equiv1\pmod3$, the same representative gives $V_{\mathcal C}=\operatorname{diag}(a_{(p-1)/3},0)$. This follows from selecting $c_{p-1}$ and $c_{p-2}$ in the same Laurent formula. The ordinary stopping index is $(p-1)/3$, distinct from the rounded index used throughout this proposition.

## References and dependency boundary

The elementary coefficient, factorial, cocycle, and matrix arguments are written out here. The general facts used are the local Cartier theorem, genus-one Riemann–Roch, and affine Čech computation for the two-term de Rham complex. They are literature dependencies, not outputs of numerical tests. The note does not rely on Tal, a canonical lift, an integral comparison theorem, or an Ogus period formula.

Cartier, P. (1957). Une nouvelle opération sur les formes différentielles. *Comptes Rendus de l'Académie des Sciences de Paris, 244*, 426–428.

Oda, T. (1969). The first de Rham cohomology group and Dieudonné modules. *Annales scientifiques de l'École Normale Supérieure, 2*(1), 63–135. https://doi.org/10.24033/asens.1175. Definitions 5.5–5.6 give the local Cartier operator and its action on de Rham cocycles; the matrices in this note are computed directly.

Morita, Y. (1975). A $p$-adic analogue of the $\Gamma$-function. *Journal of the Faculty of Science, University of Tokyo, Section IA, 22*, 255–266. Only the integer definition and continuous unit-valued extension are used above.

Silverman, J. H. (2009). *The arithmetic of elliptic curves* (2nd ed.). Springer. Genus-one geometry and regular invariant differentials.
