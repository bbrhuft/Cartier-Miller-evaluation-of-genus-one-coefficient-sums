# Mathematical specification and proof notes

This note specifies the built-in mod-p algorithms. These are elementary reductions and standard algorithm integration, not a novelty claim. The supplied Cartier–Miller project identity is independently checked here against its original recurrence.

## Domain and definition

Let p be an odd prime and 0 ≤ L < p. Define

$$a_L=\binom{2L}{L}8^{-L}\pmod p,\qquad B_L=\sum_{0\le i<L}a_i.$$

The implementation validates primality in the bounded range p < 2^64. Its deterministic Miller–Rabin bases match the bounded set documented in SymPy's official primality-testing source. Larger inputs are rejected rather than labeled certified primes.

For L = 0, a_L = 1. If (p+1)/2 ≤ L < p, the integer binomial has exactly one factor of p: its numerator factorial contains p once and its denominator factorials contain none. Hence a_L = 0 modulo p. This assertion does not give a zero modulo p². If 0 ≤ L ≤ (p−1)/2, both factorials in

$$a_L=(2L)!\,(L!)^{-2}8^{-L}\pmod p$$

are units, so the generic ratio is valid.

## Wilson reflection

For 0 ≤ n < p, let r = p−1−n. Factoring (p−1)! into n! and the final r factors gives

$$-1\equiv n!\,(-1)^r r!\pmod p.$$

Because p−1 is even, r and n have the same parity. Thus

$$n!\equiv(-1)^{n+1}(r!)^{-1}\pmod p.$$

Each backend uses this only when r < n. The code explicitly applies the inverse and sign after evaluating the shorter factorial. A direct counterexample to the survey's sign is p = 11, n = 6: the correct result is 5, not 6.

## Ordinary third

Suppose p ≥ 7 and p ≡ 1 (mod 3), and put L = (p−1)/3. Then L is even and p−1−2L = L. Wilson reflection yields

$$-1\equiv(2L)!\,L!\pmod p.$$

Also 8^L = 2^(p−1) = 1 modulo p. With G = L!, substitution in the generic ratio gives

$$\boxed{a_L=-G^{-3}\pmod p.}$$

The plan requests precisely one factorial at index L.

## Rounded third

Suppose p ≥ 11 and p ≡ 2 (mod 3), and put m = (p−2)/3, L = m+1 = (p+1)/3. Then m is odd, 2L = p−m, and p−1−2L = m−1 is even. Wilson gives

$$-1\equiv(2L)!\,(m-1)!\pmod p.$$

Writing G = m! gives (2L)! = −m/G = (2/3)G^(−1), because m = −2/3 modulo p. Moreover L = 1/3 modulo p, so L! = G/3 and 8^L = 2^(p+1) = 4 modulo p. Consequently

$$\boxed{a_L=\frac32G^{-3}\pmod p.}$$

The plan requests precisely one factorial at index L−1. The prototype preserves the supplied project domain p ≥ 11; p = 5 is still evaluated correctly by the generic path and is not silently added to the named family.

## Block-product factorial backend

After reflection let the effective factorial index be n, and set s = floor(sqrt(n)). Define

$$f(X)=\prod_{j=1}^{s}(X+j).$$

Then

$$n!=\left(\prod_{i=0}^{s-1}f(is)\right)\prod_{j=s^2+1}^{n}j.$$

The tail has at most 2s factors. A product tree builds f and a second tree builds the monic polynomial products of X−is. A remainder tree evaluates f at the s points. Monic remainders use reverse-polynomial division and Newton power-series inversion, with schoolbook arithmetic for small fixed sizes. This avoids the survey's shift-dependent interpolation hazards. This describes the `product_tree` backend. Version 0.5 additionally implements the scalar BGS arithmetic-progression construction, with its own proof and denominator audit in BGS_BACKEND.md.

For larger polynomial products, each coefficient is represented by a base-B integer digit, with B a byte-aligned power of two strictly greater than min(len(a),len(b))*(p−1)^2. The largest unreduced convolution coefficient is at most that bound, so integer multiplication cannot produce interdigit carries. Unpacking and reducing each digit modulo p therefore returns the exact polynomial product. No floating-point arithmetic is used in the mathematical kernel.

At the polynomial-algorithm level, standard product/remainder trees require O(M(s) log s) polynomial-arithmetic work and O(s log s) stored field coefficients. The actual Python implementation uses Python's integer multiplication for M; no optimal integer-multiplication bound or FLINT-level performance is claimed. This prototype stores full evaluation trees rather than a specialized low-memory forest.

## Independent complete-sum identity

Put h = (p−1)/2 and define t_0 = 1 and

$$t_{i+1}=t_i\frac{h+2+i}{2i+2},\qquad U_p(L)=\sum_{0\le i<L}(h+1+i)t_i.$$

The definition of a_i gives 4(i+1)a_(i+1) = (2i+1)a_i. An induction using h+2 = 3/2 modulo p yields t_i = (2i+1)a_i for 0 ≤ i < p. No division by 2i+1 is needed, so the vanishing case at i = h is included.

Let F(L) = 4B_L−2L(2L+5)a_L. For L < p−1, substitution of the a recurrence shows

$$F(L+1)-F(L)=\frac{(2L+1)^2}{2}a_L=(h+1+L)t_L.$$

Both F(0) and U_p(0) are zero. Therefore

$$U_p(L)=4B_L-2L(2L+5)a_L\pmod p$$

throughout the implemented domain. This proves the final combination, but it does not provide a fast B_L algorithm for arbitrary L. At p = 17 and L = 6 the boundary multiplier is zero, and U_p(6) = 4B_6 automatically.

## Primary references

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. SIAM Journal on Computing, 36(6), 1777–1806. https://doi.org/10.1137/S0097539704443793 . Author manuscript: https://cs.uwaterloo.ca/~eschost/publications/pollard.pdf . The generic product-tree construction is a simpler baseline than their refined algorithms; Theorems 5 and 8 underpin the new scalar BGS backend. Section 7 describes selected-term improvements beyond this implementation.

SymPy development team. Primality testing source, bounded Miller–Rabin branch for n < 2^64. https://github.com/sympy/sympy/blob/master/sympy/ntheory/primetest.py . Inspected 15 October 2026. No SymPy dependency or source-code copy is required by this prototype.

Tal, Y. (2026). Computing modular factorials below the square-root barrier. ECCC, TR26-211, unrefereed technical report. https://eccc.weizmann.ac.il/report/2026/211/ . Full text: https://eccc.weizmann.ac.il/report/2026/211/download . Section 4.4, Proposition 4.3 and Appendix H are future implementation targets, not implemented backends in version 0.1.
