# Frozen candidate (round 3): rounded-third specialization of Tal's split construction

This file is hash-frozen in `r3/FREEZE_R3.json` before any round-3 confirmation prime is selected. The round-1 and round-2 freezes (`evidence/FREEZE.json`, `evidence/charp/FREEZE_CHARP.json`) and every inherited file are unchanged; all round-3 code lives in `r3/`.

Throughout, p is a certified prime with p ≥ 11 and p ≡ 5 (mod 6), m = (p−2)/3, L = (p+1)/3, h = (p−1)/2, N = ⌊(p−5)/12⌋, q0 = (p−1)/4, c_p = 2(m!)^{−3} and a_L = binom(2L, L) 8^{−L} = (3/4) c_p. Classes are A (p ≡ 11 mod 12), B (p ≡ 5 mod 24) and C (p ≡ 17 mod 24).

## R1. Status correction of the round-2 p ≡ 17 (mod 24) route (background plus proved equivalence)

Williams and Currie (1982), Lemma 14(c): for p ≡ 1 (mod 4) and (p/3) = −1, (−3)^{(p−1)/4} ≡ (−1)^{(h(−3p)−2)/4} ((p−1)/2)! (mod p), where h(−3p) is the class number of discriminant −3p. Hence H := h! ≡ (−1)^{q0+(h(−3p)−2)/4} 3^{q0}. With (2/p) = (−1)^{q0} and the Pólya–Dirichlet evaluation Σ_{j≤m}(j/p) = h(−3p)/2, this is exactly round-2 identity (\*), which is therefore a theorem for every p ≡ 5 (mod 12). Its quarter consequence (m!/N!)² ≡ (−1)^{(h(−3p)−2)/4} a is promoted with it (algebraic equivalence written out in the report). This settles the sign of H; it does not certify any class-number computation.

## R2. Class-number backend policy

`ClassNumberPolicy('unconditional')` uses PARI `qfbclassno(D, 0)` only when −2·10^10 < D < 0 (the range in which the installed PARI 2.17.2 documentation states the result is unconditionally correct), and the reduced-form count otherwise. `ClassNumberPolicy('grh')` uses `quadclassunit` and labels every result GRH-conditional. No GRH output is ever used to certify another.

## T3. Main candidate (exact, unconditional, no class number)

Let q ≥ 5 be a prime with q | p − 1 and K = (p−1)/q ≥ 10^4. Let η ∈ F_p be the element x^K ≠ 1 for the least x ≥ 2, ρ: Z[ζ_q] → F_p the map ζ_q ↦ η, χ the order-q character with ρ(χ(x)) = x^{−K}, and J_w = J(χ, χ^w). Write y_c = (cK)!. The following hold exactly in F_p. Wilson: y_c y_{q−c} = (−1)^{cK+1}. Jacobi triples: for every t with u = ⟨t⟩, v = ⟨tw⟩, x = ⟨−t(1+w)⟩ nonzero and u + v + x = q, y_u y_v y_x = (−1)^{(u+v)K}/J_w(η^t), which follows from J(χ^u, χ^v) ≡ −binom((u+v)K, uK) (mod 𝔭) for u + v < q. Target: m! = y_b I_m^{±1}, where b is the nearest grid index to m and I_m is the product strictly between bK and m, of length (K∓1)/3. Anchor dup6 (all p): (Z6/(m!)²)² = (−1)^{(p+1)/2} 4^{1−(p+1)/3} with Z6 = ((p−5)/6)!, from Gauss's multiplication formula with M = 2 at x = 1/3; the anchor interval has length (K∓4)/6. Anchor dup12 (p ≡ 5 mod 12): (m!/N!)^4 = a² if q ≡ ±1 (mod 12), and (m!·(5N+2)!)^4 = (16a²)^{−1} if q ≡ ±5 (mod 12), with a the odd part of p = a² + b²; the anchor interval has length (K∓4)/12.

For each (q, anchor), an integer vector λ (depending on q only, frozen in `r3/PLANS_R3.json`) satisfies λ^T R = k e_b with k ∈ {1, 3} and R the relation matrix of the Wilson rows, the class-w = 1 triples and the anchor row. Then y_b^k = ∏ val_i^{λ_i}, (m!)³ = y_b³ I_m^{±3} and c_p = 2(m!)^{−3}. No root is extracted (cubing is a bijection since p ≡ 2 mod 3), no class number is used, and only H² = (−1)^{(p+1)/2} and a² enter.

The Jacobi sum J_1 ∈ Z[ζ_q] is reconstructed exactly. FLINT LLL is applied to the Stickelberger ideal ∏_{t∈S} (p, ζ − η^t) in the integral trace embedding, with exact Fincke–Pohst enumeration as the fallback. The output is certified by x·x̄ = p in Z[ζ_q], and its root of unity is selected by van Wamelen (2002), Theorems 6, 8 and 9: the unique twist whose degree-<q lift with I(1) = p − 2 is integral and satisfies Σ i a_i ≡ 0 (mod q).

## T4. Cost (supplied q)

The cost consists of one deterministic search for η (at most the least q-th power non-residue trials), one certified Jacobi sum (poly(q, log p) LLL plus O(q³) setup, enumeration only if LLL misses the minimum), two interval products of lengths (K∓1)/3 and (K∓4)/6 or (K∓4)/12 by the block (Pollard–Strassen/BGS-type) engine, and O(q log p) field operations for assembly. For bounded q this is O(M_F(√(p/q)) log p) field operations plus O_q(polylog p): a constant-factor change, no exponent claim. The total interval length is (p−1)/(2q) for dup6 and 5(p−1)/(12q) for dup12, against 4(p−1)/(3q) for Tal's lower-half routine at n = m (K! plus the residual) and (p+1)/6 for the half-interval method.

## T5. p-only algorithm and policy (frozen in `r3/POLICY_R3.json`)

Trial-divide p − 1 by the primes 5 ≤ q ≤ 89, admit q with (p−1)/q ≥ 10^4, and choose the q minimizing svp(q) + f(len_target) + f(len_anchor), with svp a measured table and f(L) = 1.93·10^{−7}·L^{0.673} s (development calibration). Use T3 if this is below the fallback prediction. Otherwise fall back to the half-interval route (with the unconditional class-number policy, when its discriminant −p or −3p has absolute value below 2·10^10), else to the FLINT nodal route. In 'grh' mode the fallback is the GRH half-interval route. The density of primes p ≡ 5 (mod 6) with an admissible prime q ∈ [5, 89] is 1 − ∏(1 − 1/(q−1)) = 0.6783 (Dirichlet's theorem with CRT). The policy affects speed only, never correctness.

## Development inputs (excluded from confirmation)

All inputs in `r3/evidence/LEDGER_R3.json` are excluded. These are all primes below 2·10^5; all primes p ≡ 5 (mod 12) below 10^6; all round-1 and round-2 development, pilot and confirmation primes; and every round-3 timing, lattice-cost and probe prime (listed explicitly). The candidate was developed with these data in view (brute-force Jacobi-sum tests below 3000, 12 481 T3 cases below 2·10^5, timings at 5·10^9 to 5·10^11). Only post-freeze primes count as confirmation.

## Confirmation rule

The rule is implemented verbatim in `r3/confirm_r3.py`. Every prime is the first one, not in the ledger, at or above the stated bound with the stated congruences, for each class A, B, C. Set S (bound 2·10^6, q ∈ primes 5..47) adds independent checks: a_L by a direct binom(2L, L) 8^{−L} loop, m! by a linear loop, and D by the Wronskian product and the Atkin recurrence. Set M uses bound 3·10^9 and q ∈ primes 5..89. Set L uses bound 3·10^11 and q ∈ {11, 23, 47, 89}. Set E1 (bound 4·10^10) has two primes per class with no prime 5 ≤ q ≤ 89 dividing p − 1. Set E2 (bound 3·10^9) has q² | p − 1 for q ∈ {5, 7, 11}. Set E3 (class A, bound 3·10^5) has two primes for which some prime 5 ≤ q ≤ 89 divides p − 1 but no such q has K ≥ 10^4, so the fallback is forced. Set E4 (bound 10^10) has ten generic primes per class. For each prime, m!, c_p, a_L and D are compared with FLINT references, for T3 with every applicable anchor and q, for every half-interval route and the nodal route, and for the API in both modes.

## Benchmark rule

The rule is implemented verbatim in `r3/benchmark_r3.py` and runs only after a PASS. Calls are cold: everything input-dependent is timed, and the form-count sieve is cleared. Process-level state (the PARI object, the FLINT library and the plan table) is disclosed. Warm calls are reported separately. Sets B1 to B4 are as specified there, with 5 rotated samples per method (3 for B2) and all samples retained.
