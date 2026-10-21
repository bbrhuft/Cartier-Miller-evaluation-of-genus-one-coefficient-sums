# Mathematical contract and proof map

Work over a supplied prime field F_p, p at least 5. The character chi has chi(0)=0. The relevant curve is the smooth projective model of y squared equals f(x), with f a squarefree cubic or quartic. All weighted sums below are elements of F_p.

Write F=f^((p-1)/2)=L+x^p J_f with degree L less than p. Polynomial division and finite-field power sums prove, including branch values and zero,

\[
C_f(a)=\sum_{x\ne a}\frac{\chi(f(x))}{x-a}=-F'(a)-J_f(a).
\]

This identity alone does not supply a fast branch oracle. For a nonbranch pole, put e=chi(f(a)), g(z)=f(a+z)/f(a), g_1=f'(a)/f(a), and N=p+1-e tau_f. On the short model of v squared equals g(z), with (0,1) as origin, let R be the image of (0,-1). The current evaluator is

\[
C_f(a)=e\left(-\frac{g_1}{4}(N-2)-\frac{\alpha_N(R)}2\right).
\]

Here alpha_m(P) is the Laurent constant of dlog f_{m,P} at infinity in t=-X/Y, with divisor m(P)-([m]P)-(m-1)(O). The invariant differential is dX/(2Y). On a short curve W, writing W^((p-1)/2)=U+A_E X^(p-1)+X^p V_W, the central uniform identity is

\[
\alpha_{\#E(\mathbb F_p)}(P)=Y(P)V_W(X(P)).
\]

UNIFORM_ORDER_PROOF.md proves this from the Cartier defect, the Frobenius/Verschiebung trace relation and the Miller addition and composition identities. It includes all traces and rational two-torsion and proves the positive sign. On the representative (P)-(-P), the local logarithmic constant is twice this scalar. The proof constructs a geometric division point; the algorithm does not. FOUNDATION_PROOFS.md supplies more detail on local lines, identity steps, the Connell model and the rational-function decomposition of 1/z. Its earlier case-split evaluator is superseded by the uniform-order strategy.

For a complete excluded set U={a_1,...,a_s}, supplied residues r_i, a constant c, w_i=chi(f(a_i)), K_f=sum_x chi(f(x)), and D_i(v)=sum_(j not equal i) v_j/(a_i-a_j), the common-domain formulas are

\[
\begin{aligned}
\sum_{x\notin U}R(x)\chi(f(x))
&=c\left(K_f-\sum_iw_i\right)+\sum_i r_i\bigl(C_f(a_i)+D_i(w)\bigr),\\
\sum_{\substack{P\ \mathrm{affine}\\x(P)\notin U}}R(x(P))
&=c\left(K_f-s-\sum_iw_i\right)+\sum_i r_i\bigl(C_f(a_i)+D_i(1+w)\bigr).
\end{aligned}
\]

Their difference is -sc+sum_i r_i D_i(1). The unweighted integer K_f is 1-N_infinity-tau_f. A cubic has N_infinity=1; a quartic has N_infinity=1+chi(leading coefficient). The projective point sum adds c N_infinity to the affine sum. No character value is assigned at infinity. Every excluded coordinate participates in corrections, even if its own residue is zero.

For B(X)=product_j(X-a_j) and W_v(X)=sum_j v_j B(X)/(X-a_j), the fast correction identity is

\[
D_i(v)=\frac{W_v'(a_i)}{B'(a_i)}-
       \frac{v_iB''(a_i)}{2B'(a_i)}.
\]

Product and remainder trees give O(M_pol(s) log(s+1)) field operations under the usual polynomial-arithmetic assumptions. This is proved but not implemented by weighted_sums.py, which uses pairwise differences and one batched inversion.

With n=ceil(log_2 p), the scalar query costs O(n) field operations and a safe O(n(M(n)+I(n)+n)) bits after trace preparation. Classical arithmetic gives O(n^3) bits; fast arithmetic gives soft-O(n^2). Pairwise weighted preparation costs O(sn+s^2) field operations and O(sn^3+s^2 n^2) bits classically. Prime certification, exact-trace acquisition, denominator factorization and unsupplied partial fractions are not hidden in those query bounds.

The reverse coefficient identity J_f(a)=[z^(d(p-1)/2-p)](z^d f(a+1/z))^((p-1)/2) supplies a trace-free selected-coefficient comparator, including branch poles. The BGS/Harvey machinery gives soft-O(sqrt(p)) field operations for fixed degree with its interpolation setup charged. This is a different preparation model. The historical benchmark contains its adapters and matched outputs.

Miller's construction dates to the circulated 1986 manuscript and is explained in the 2004 paper; its addition and composition identities are classical. Semaev's differentiated order-p transfer and Rück's coefficient cocycle are direct computational antecedents. The source comparison and replacement prior-work section make these attributions explicit. The complete general-trace scalar and weighted-sum adapter were not located in the passages examined; this is a bounded finding and does not establish publication priority.
