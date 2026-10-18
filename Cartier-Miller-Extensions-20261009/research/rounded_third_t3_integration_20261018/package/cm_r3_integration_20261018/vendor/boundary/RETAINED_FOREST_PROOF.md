# Ordered products and the reduced-state forest

David Jordan research project, 14 October 2026. Unrefereed implementation proof. The finite-field output contract is all primes $11\le p<X$ with $p\equiv2\pmod3$. The upper bound is exclusive, and $B_L$ is a strict prefix.

## Integer recurrence and recovery

Over the rationals, define $a_j=\binom{2j}{j}8^{-j}$, $B_j=\sum_{i<j}a_i$, and $D_j=4^jj!$. The two cleared quantities $\widehat B_j=D_jB_j$, $\widehat a_j=D_ja_j$ are integers because

$$
\begin{pmatrix}\widehat B_{j+1}\\\widehat a_{j+1}\end{pmatrix}
=M_j\begin{pmatrix}\widehat B_j\\\widehat a_j\end{pmatrix},\quad
M_j=\begin{pmatrix}4(j+1)&4(j+1)\\0&2j+1\end{pmatrix},\quad
\begin{pmatrix}\widehat B_0\\\widehat a_0\end{pmatrix}=
\begin{pmatrix}0\\1\end{pmatrix}.
$$

Induction gives

$$\Pi_j=M_{j-1}\cdots M_0=\begin{pmatrix}D_j&\widehat B_j\\0&\widehat a_j\end{pmatrix}.$$

For each selected prime, $L=(p+1)/3<p$ and $D_L$ is invertible modulo $p$. If the stored triple for $\Pi_L\bmod p$ is $(A,B',A')$, the outputs are

$$
B_L=B'A^{-1},\qquad a_L=A'A^{-1},\qquad
G=A(4^LL)^{-1},\qquad U_p(L)=4B_L-2L(2L+5)a_L.
$$

The independent definition of the last quantity is $t_0=1$, $t_{i+1}=t_i(h+2+i)/(2i+2)$ and $U_p(L)=\sum_{i<L}(h+1+i)t_i$. Induction gives $t_i=(2i+1)a_i$. With $Q_i=2i(2i+5)a_i$, direct substitution gives $4a_i-Q_{i+1}+Q_i=(h+1+i)t_i$. Summation proves the recovery formula. Since $2L(2L+5)\equiv34/9$, its only zero in the branch is $p=17$. The checker compares all four outputs separately.

## Tree invariant

For increasing primes $p_1,\ldots,p_n$, write $L_i=(p_i+1)/3$. A chunk starts at an earlier recurrence index $s$. Its first leaf is the exact product from $s$ to $L_1-1$; each subsequent leaf is the exact product from $L_{i-1}$ to $L_i-1$. Later matrices always multiply on the left. The product of a right child and then a left child is therefore $P_{\rm right}P_{\rm left}$.

For a tree node covering leaves $l$ through $r$, its incoming residue is the product of all leaves before $l$, times the incoming chunk carry, reduced modulo $N_{l,r}=\prod_{i=l}^rp_i$. The left child receives that residue reduced to its modulus. The right child receives $P_{\rm left}$ times that residue, reduced to its modulus. Induction down the tree proves the invariant because each child modulus divides its parent modulus. Multiplying the incoming leaf residue by that leaf product gives $\Pi_{L_i}\bmod p_i$. An unpaired last node is carried up unchanged; it introduces no extra recurrence step.

Long leaf intervals are formed with balanced multiplication: split $[s,t)$ at $u$ and return $P_{[u,t)}P_{[s,u)}$. Intervals of at most 16 steps use the elementary recurrence. This preserves exactly the same ordered product.

## Remaining-modulus carry

Let chunks be consecutive groups of primes. Before a chunk starting at recurrence index $s$, keep

$$N_{\rm rem}=\prod_{\text{unprocessed primes}}p,\qquad
R\equiv\Pi_s\pmod{N_{\rm rem}}.$$

Initially $s=0$, $R=I$, and $N_{\rm rem}$ is the product of all selected primes. If the current chunk modulus is $N_c$, its tree receives $R\bmod N_c$. Let $C$ be its exact total matrix product, and let $t$ be its ending recurrence index. After the chunk, set

$$N_{\rm next}=N_{\rm rem}/N_c,\qquad R_{\rm next}=CR\bmod N_{\rm next}.$$

Exact divisibility is checked. Because $N_{\rm next}\mid N_{\rm rem}$, the updated residue is $C\Pi_s=\Pi_t$ modulo every remaining prime. This proves the invariant for the next chunk. The final carry need not be computed when $N_{\rm next}=1$.

There are $K_{\rm used}-1$ carry updates. Earlier chunk products are discarded. The repaired Opus prototype instead uses $K_{\rm used}(K_{\rm used}-1)/2$ earlier-product multiplications. This extension removes that quadratic multiplication count; it does not claim that the bit cost of each update is constant. The remaining-modulus strategy is classical remainder-forest machinery, not a new number-theoretic algorithm.

## Arithmetic size and cost

Let $n$ be the number of selected primes, $B=\sum\lceil\log_2p_i\rceil$, and $J=L_n$. For $n=0$ the output is a header-only file. For $n>0$, put $H=O(J\log(J+2))$. A product over $g$ steps ending at $t$ has at most $O(1+g\log(t+2))$ bits per entry: its upper-right entry is at most twice its upper-left entry, since the ratio accumulated at each step is bounded by the geometric series $1+1/2+1/4+\cdots$. Balanced products and trees preserve a total entry-size bound of this order per level.

Write $H_c$ for the product-size bound of chunk $c$, $B_c$ for its modulus bits, and $B_{{\rm rem},c}\le B$ for its remaining-modulus bits. With a monotone, superadditive multiplication cost $\mathsf M$ and division cost $O(\mathsf M)$, a conservative arithmetic bound is

$$
O\!\left(\mathsf M(B)\log(n+2)
+\mathsf M(H)\log(J+2)
+\sum_c\mathsf M(H_c+B_c)\log(n_c+2)
+\sum_c\mathsf M(H_c+B_{{\rm rem},c})\right),
$$

plus the sieve and per-prime modular finishing. This expression includes balanced leaf formation; it does not silently remove its logarithmic factor. A simpler bound is $O((\log(X+2)+K)\mathsf M(X\log(X+2)))$ for $K$ chunks, plus sieve and finishing. Taking $K=O(\log X)$ and quasi-linear integer multiplication gives quasi-linear total cost up to logarithmic factors, and polynomial-logarithmic amortized cost per prime. This is an arithmetic-model statement, not a claim that CPython's multiplication realizes the fastest known asymptotic integer algorithm.

The resident arithmetic data require $O(B+\max_c(H_c+B_c)\log(n_c+2))$ bits. The implementation additionally retains an $O(X)$-byte sieve during prime enumeration, a prime list, and one chunk's output residues. Tuples stream to CSV, so it does not retain the complete output table. Python object overhead and transient multiplication allocations are outside the arithmetic bit count and must be measured separately. Balanced prime-count chunks need not have equal recurrence lengths; run records include their maximum length and modulus size instead of assuming perfect balance.

The abstract remainder-tree/forest bounds and strategy are established in Harvey and Sutherland (2016, Theorems 3.2–3.3). Our variable interval leaves and compact upper-triangular state are analyzed above on their own terms. No optimal-memory or compiled-backend claim is made.

## Reference

Harvey, D., & Sutherland, A. V. (2016). Computing Hasse–Witt matrices of hyperelliptic curves in average polynomial time, II. In *Frobenius distributions: Lang–Trotter and Sato–Tate conjectures* (Contemporary Mathematics, Vol. 663). American Mathematical Society. https://doi.org/10.1090/conm/663/13352. Author's offprint: https://math.mit.edu/~drew/conm13352.pdf.
