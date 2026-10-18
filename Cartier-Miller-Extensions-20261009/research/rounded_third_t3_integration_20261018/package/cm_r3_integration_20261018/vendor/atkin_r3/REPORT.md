# Atkin endpoint: audit, attribution and a characteristic-p half-interval acquisition

David Jordan research project, round 2, 18 October 2026. AI-assisted and unrefereed. This report supersedes the round-1 report, which is kept unchanged at `provenance/REPORT_round1_20261018.md`. It claims no publication or priority, no universal lower bound, no polylogarithmic or sub-square-root algorithm, and no new best factorial algorithm.

Status labels used throughout: **[background]** for established literature, **[proved here]** for complete proofs written in this investigation (novelty unsettled unless stated), **[finite evidence]** for exact checks on stated finite sets, and **[conjecture]**.

## Result

1. **The round-1 package is correct.** It audits clean and reproduces exactly. Every step of the Wronskian proof was checked symbolically. For all 40 admissible primes below 420, an independent brute-force enumeration of supersingular j-invariants over F_{p²} confirms A_n ≡ ss_p, the endpoint derivative, the signed normalization and Opus's product formula (N5). One clarification: identity (1) holds for j ≥ 1. It is also the confluent Christoffel–Darboux identity at J = 0, combined with a Gosper antidifference.

2. **Attribution correction.** The endpoint derivative is a one-line consequence of Kaneko–Zagier Proposition 5:
$$D=A_n'(0)\equiv 1728^{N}R_N\ (p\equiv5\bmod 12),\qquad D\equiv-1728^{N+1}R_N\ (p\equiv11\bmod12),\qquad R_N=\frac{(4/3)_N}{N!}.$$
Both the round-1 formula (2) and the "simplified nodal anchor" (3) are therefore implicit in KZ. The Wronskian derivation and Opus's nodal argument are independent alternative proofs. In the machine-extracted texts read here, neither KZ nor El-Guindy–Ismail states A_n'(0) or a Christoffel–Darboux identity.

3. **A formal obstruction [proved here].** For p ≡ 2 (mod 3), an explicit odd linear functional Φ vanishes on every reflection relation, every Gauss multiplication relation and every Gross–Koblitz relation, of every conductor prime to p. It does not vanish on Γ_p(1/3). Two consequences follow:
   - In the formal relation calculus of §4, no identity built from Jacobi or Gauss sums, at any conductor, determines c_p without interval products.
   - If all the points used have conductor at most Q, some interval product has length at least p/Q² − 1. Bounded-conductor characteristic-p identities can only change constants. Beating √p requires a conductor that grows like p^δ, which is the regime of Tal (2026).

4. **The frozen round-2 candidate holds exactly on 27 disjoint primes up to 2·10¹¹.** The candidate is c_p = 2HP³, where P = ∏_{j=(p+1)/3}^{(p−1)/2} j is a single product of (p+1)/6 factors and H = ((p−1)/2)!. The value H, sign included, comes from class numbers:
   - Mordell (1961) [background] for p ≡ 3 (mod 4);
   - Gauss's binomial congruence combined with Dirichlet's class number formula [proved here from background] for p ≡ 5 (mod 8);
   - an identity (\*) using h(−3p) [conjecture, novelty unknown; 4504 development primes plus 18 fresh primes] for p ≡ 17 (mod 24).

5. **Measured gain: a constant factor, conditional on fast class numbers.** In an optimized FLINT backend at p ≈ 2·10⁹–2·10¹¹, the method is faster than FLINT's native n_factorial_fast_mod2_preinv applied to m! by 1.18–1.56×. It is faster than the same backend running the round-1 nodal anchor by 1.03–1.26×. These speeds use PARI's subexponential class number, whose output PARI guarantees only under GRH. Every class number used was checked against an unconditional reduced-form count. With that unconditional Python count instead, or in the pure-Python engine, the method does not beat the nodal anchor.

6. **The quarter identity [proved here] and its exact first failure.** For p ≡ 5 (mod 12):
   - (m!·((p−1)/4)!/N!)² ≡ (2/p)·3^{(p−1)/4}/2, and therefore (m!/N!)⁴ ≡ a², where p = a² + b² and a ≡ 1 (mod 4). A product of about p/12 factors thus fixes c_p up to a 4th root of unity.
   - With class numbers this narrows to one sign. The narrowing uses an identity equivalent to (\*): (m!/N!)² ≡ a·(m!/p).
   - No relation found in the conductor-12 lattice fixes that last sign. It is the recorded first exact failure.

No faster exponent emerged. The asymptotic cost of every method here remains O(M_F(√p) log p).

## 1. Target and notation

Supply a certified prime p ≥ 11 with p ≡ 5 (mod 6). Put

$$m=\tfrac{p-2}{3},\quad h=\tfrac{p-1}{2},\quad N=\left\lfloor\tfrac{p-5}{12}\right\rfloor,\quad \epsilon=[p\equiv11\bmod12],\quad n=N+1+\epsilon,\quad c_p=2(m!)^{-3}.$$

A_j denotes the monic Atkin polynomials, with A_0 = 1, A_1 = J − 720, A_2 = J² − 1640J + 269280. For j ≥ 2 they satisfy A_{j+1} = (J−α_j)A_j − β_jA_{j−1}, with

$$\alpha_j=\frac{24(144j^2-29)}{(2j+1)(2j-1)},\qquad \beta_j=\frac{36(12j-13)(12j-7)(12j-5)(12j+1)}{j(j-1)(2j-1)^2}.$$

Set β_1 = 393120. Kaneko–Zagier Theorem 3 gives A_n ≡ ss_p (mod p) **[background]**. The signed target is D = A_n'(0). It is linked to c_p by the audited round-1 normalization

$$c_p=-\frac{4\chi(6)(-1)^N}{3\cdot1728^N(-1728)^{\epsilon}}\,D .$$

Write Γ_p for Morita's p-adic gamma function. For x in Z_(p), let R(x) ∈ {1,…,p} be its residue. Then Γ_p(x) ≡ (−1)^{R(x)}(R(x)−1)! (mod p).

## 2. Audit of round 1 (newly executed)

| Check | Result |
|---|---|
| `audit.py` on the delivered bytes | PASS: manifest and round-1 freeze hashes |
| `develop.py` rerun (152 primes, rational indices 1–40) | PASS; DEVELOPMENT.json identical |
| `confirm.py` rerun (11 frozen primes) | PASS; selection, c_p, D and the direct Atkin derivative identical |
| Symbolic proof steps (sympy, `research/audit/sym_audit.py`) | r_j = −α_j − β_j/r_{j−1}, γ_j, R(j) − γ_jR(j−1) = 1, β_{j+1}/r_j, β_1 = 393120 and −β_1/(4a_1) = 273/2: all exact |
| Independent supersingular enumeration (`ss_brute.py`) | All 40 admissible p < 420: the Legendre-form Hasse roots over F_{p²} give ss_p = A_n mod p. D, the signed normalization and N5 all agree |
| KZ Proposition 5 form of D (`kz_prop5_check.py`) | All 1135 admissible p < 20000 |

**Denominator hypotheses.** Put r = n − 1. The denominators of α_j and β_j for j ≤ r, and that of R(r) = (12r−1)(12r+5)/(96r), are p-units, because 2j + 1 < p. The numerator factors of B_r = ∏_{i≤r}β_i are p-units. The factors 12i−7 and 12i−13 reach p only at i = r + 1, in the two classes respectively. The value a_r is a p-unit, since (12j−1)(12j+5) ≡ 0 only at j = r. Finally a_n ≡ 0 and R(r) ≡ 0. The round-1 proof is complete with these ranges. Identity (1) is stated and proved for j ≥ 1, since R(0) is undefined.

**Interpretation [proved here, elementary].** The norms are h_k = (A_k, A_k) = B_k, with h_0 = 1. So W_j = a_jd_{j+1} − a_{j+1}d_j equals B_j Σ_{k=0}^{j} a_k²/B_k. This is the confluent Christoffel–Darboux formula at J = 0 (Szegő, 1975, §3.2). Identity (1) is therefore equivalent to the closed Gosper antidifference

$$\sum_{k=0}^{j}\frac{a_k^2}{B_k}=R(j)\frac{a_j^2}{B_j}-\frac14\qquad(j\ge1).$$

**Freeze caveat.** `evidence/FREEZE.json` is an internal hash commitment, consistent with the files and timestamps. It has no external timestamp, so it records the order of operations only as far as the package's own records do.

**Qualification of the round-1 speed-ups.** Round 1 reported 1.48–1.59× for the shared nodal anchor over the matched pure-Python factorial. Against FLINT's optimized native factorial (§6), the same nodal structure in a FLINT block engine gains 1.03–1.29× at p ≥ 2·10⁹.

## 3. Attribution: the endpoint formula is implicit in Kaneko–Zagier

KZ Proposition 5 states ss_p ≡ U_n^ε (mod p) **[background]**. Here U_n^0 is the polynomial part of j^n·₂F₁(1/12, 5/12; 1; 1728/j), and U_n^1 is the polynomial part of j^{n−1}(j−1728)·₂F₁(7/12, 11/12; 1; 1728/j).

- For p ≡ 5 (mod 12), the j¹ coefficient of U_n^0 is the k = N term: D ≡ 1728^N (1/12)_N(5/12)_N/(N!)².
- For p ≡ 11 (mod 12), write c_k for the ₂F₁(7/12, 11/12) coefficients. The j¹ coefficient is 1728^{N+1}(c_{N+1} − c_N), and c_{N+1} ≡ 0 because 11/12 + N ≡ 0. So D ≡ −1728^{N+1}(7/12)_N(11/12)_N/(N!)².

The reflection (x)_N = (−1)^N(1−x−N)_N holds identically. With N ≡ −5/12 or −11/12 (mod p) it gives (5/12)_N ≡ (−1)^N N! and (1/12)_N ≡ (−1)^N(4/3)_N in the first class, and (11/12)_N ≡ (−1)^N N! and (7/12)_N ≡ (−1)^N(4/3)_N in the second. Hence

$$\boxed{D\equiv1728^N R_N\ (p\equiv5),\qquad D\equiv-1728^{N+1}R_N\ (p\equiv11)\pmod p.}$$

Substituting into the normalization reproduces round-1 formula (3) in both classes. This gives a third, independent proof of (3) **[proved here from background; finite evidence: 1135 primes]**.

Other prior-work points:

- KZ Proposition 6 gives A_n(0), A_n(1728) and the norms. It gives no derivative.
- KZ §6 contains a Casoratian identity for A_n and the companion polynomials B_n. That identity is different from (1).
- KZ §10 discusses de Shalit's formula for ss_p'(j) at supersingular j via Kronecker's polynomial. It gives no value of ss_p'(0).
- El-Guindy–Ismail (2014) give A_n(0) and A_n(1728) in (6.12) and (6.15), and the associated-Jacobi representations of Theorems 3.1, 4.1 and 5.1. They give no derivative and no Christoffel–Darboux identity.

**Status.** The endpoint formula is not new; it is implicit in KZ. The Wronskian/Christoffel–Darboux closed form (1) was not found in KZ or El-Guindy–Ismail. Both papers were read through machine-extracted text, which is partly garbled, so a statement missed by the extraction cannot be excluded. Identity (1) is probably routine, and its novelty is unsettled.

## 4. Characteristic-p reformulation and a formal obstruction

**4.1 Reformulation [proved here].** For a rational number a and p ∤ (a + i) with i < N, (a)_N ≡ (−1)^N Γ_p(a+N)/Γ_p(a). The index N is p-related: 4/3 + N ≡ 11/12 (p ≡ 5) or 5/12 (p ≡ 11) modulo p. For p ≡ 5 (mod 12) this gives

$$R_N\doteq\frac{\Gamma_p(11/12)}{\Gamma_p(1/3)\,\Gamma_p(7/12)},\qquad c_p\doteq\Gamma_p(1/3)^{-3},$$

where ≐ means "up to explicit signs and powers of 2 and 3". Here Γ_p(1/3) ≡ m! (mod p), because R(1/3) = (p+1)/3. The arithmetic content of every method in this package is a single Γ_p value at a conductor-12 point.

**4.2 Theorem C6 [proved here].** Let p ≡ 2 (mod 3) be prime. Let V be the Q-vector space with basis [x], for x ∈ Q/Z with denominator prime to p. Let W ⊂ V be spanned by:

- (i) the reflection relations [x] + [−x];
- (ii) the multiplication relations Σ_{i<M}[x + i/M] − [Mx], for M ≥ 1;
- (iii) the Gross–Koblitz orbit relations Σ_{i<f}[p^i x], where f is the order of p modulo the denominator of x;
- [0].

Then [1/3] ∉ W.

*Proof.* Let B̄₁(t) = {t} − ½, with B̄₁(t) = 0 for t ∈ Z. For x of denominator d, put M = lcm(d, 3) and

$$\Phi([x])=\frac1{\varphi(M)}\sum_{u\in(\mathbb Z/M)^\times}\chi_{-3}(u)\,\bar B_1(ux).$$

This is independent of M, because u ↦ u mod d has uniform fibres. Φ vanishes on each family:

- (i): B̄₁ is odd, and ux ∉ Z for x ≠ 0.
- (ii): Raabe's identity Σ_{i<M}B̄₁(t + i/M) = B̄₁(Mt) holds, and u coprime to M permutes the i/M.
- (iii): Σ_{i<f}Φ([p^ix]) = (Σ_{i<f}χ_{−3}(p)^{−i})·Φ([x]). If 3 | d, then f is even, because p has order 2 modulo 3, and the sum is 0. If 3 ∤ d, then Φ([x]) = 0 by the Chinese remainder theorem, because the average of χ_{−3} over (Z/3)^× is 0.
- [0]: Φ([0]) = 0.

Finally Φ([1/3]) = ½(χ(1)B̄₁(1/3) + χ(2)B̄₁(2/3)) = −1/6 ≠ 0. ∎

A Γ_p monomial whose exponent vector lies in W is computable from Gauss and Jacobi sums, multiplication formulas and reflection, up to explicit algebraic factors. Γ_p(1/3)^e with e ≠ 0, and hence c_p, which has Φ-weight +½, is never among them. The functional was also checked exactly on 3032 random relations: 400 reflection, 400 multiplication and 2232 Gross–Koblitz instances at six primes (`develop_charp.py`).

**4.3 Corollary (interval length) [proved here].** Mod p, an interval product ∏_{j<k}(R(x)+j) from the residue of x = a/M to the residue of y = b/M' relates Γ_p(x) and Γ_p(y). Suppose x ≠ y in Q/Z. Then kMM' − bM + aM' is a nonzero multiple of p, so |k| ≥ p/(MM') − 1.

Consider any formal derivation of Γ_p(1/3)^e (e ≠ 0) from (i)–(iii) on points of conductor at most Q, plus interval products between residues of such points. Since Φ is additive and kills (i)–(iii), the derivation must include an interval product between distinct Q/Z classes. Such an interval has length at least p/Q² − 1.

This is a statement about derivations in a stated calculus. It is not a lower bound for all algorithms. It shows that fixed-conductor CM data can only change constants. With BGS-type interval cost about √(length), a cost of p^{1/2−δ} forces a conductor of at least about p^δ, together with Jacobi sums computable at that conductor. Tal's (2026) construction has exactly this shape, with q | 1 + p + p².

## 5. The frozen round-2 candidate

The candidate was frozen in `CANDIDATE_CHARP.md` and `evidence/charp/FREEZE_CHARP.json` at 2026-10-18T03:42:12Z, before any round-2 confirmation prime was selected. The round-1 freeze is unchanged.

**Process note.** The handover asked for one candidate to be stated before any broad search. That order was not kept. A first candidate was set out with its operations and cost: the conductor-12 Gross–Koblitz identity for R_N. Its first exact failure is Theorem C6. After that, the candidate below came out of a development search over primes below 2·10⁵: the exact-lattice scans and the interval enumeration of C7. Because it was chosen with that data in view, its statements were frozen together with every development input, and only the disjoint post-freeze primes count as confirmation.

**C1 [proved here, elementary].** Put P = ∏_{j=m+1}^{h} j, which has (p+1)/6 factors, and H = h!. Then m! = H/P and H² = ±1. Hence H⁴ = 1 and

$$\boxed{c_p\equiv2\,H\,P^3\pmod p.}$$

**C2 [background].** For p ≡ 3 (mod 4), H ≡ (−1)^{(h(−p)+1)/2} (Mordell, 1961).

**C3 [proved here from background].** Let p ≡ 5 (mod 8), put q = (p−1)/4, and let p = a² + b² with a ≡ 1 (mod 4).

- Gauss's congruence (Gauss, 1828; Berndt, Evans & Williams, 1998) gives H/(q!)² ≡ 2a.
- The Legendre symbol of q! is therefore (q!/p) = (q!²)^q = (H/2a)^q.
- Dirichlet's formula Σ_{j≤q}(j/p) = h(−4p)/2 (Berndt, 1976) gives (q!/p) = (−1)^{(q−h(−4p)/2)/2}.
- Since q is odd, the two square roots ±ι of −1 have distinct q-th powers.

So H is the unique square root of −1 with H^q = (q!/p)(2a)^q. Cornacchia's algorithm with √−1 = 2^{q} supplies a deterministically. The Dirichlet sum was rechecked at 818 development primes.

**C4 [conjecture].** For p ≡ 1 (mod 4) and p ≡ 2 (mod 3),

$$H\equiv\left(\tfrac2p\right)\left(\tfrac{m!}p\right)3^{(p-1)/4}\pmod p,\qquad\left(\tfrac{m!}{p}\right)=(-1)^{(m-h(-3p)/2)/2}.\tag{\*}$$

The second equation is the Dirichlet-type sum Σ_{j≤m}(j/p) = h(−3p)/2, rechecked at 818 development primes. Evidence for (\*):

- all 4504 admissible primes p ≡ 5 (mod 12) below 2·10⁵ (development);
- 18 fresh confirmation primes up to 2·10¹¹.

In class B (p ≡ 5 mod 24) the Gauss route agrees with (\*) at all 9 confirmation primes.

An elementary approach cannot settle (\*). Since −1 is a square, Legendre symbols of algebraic Γ_p identities never see the sign of H. The identity is plausibly equivalent to a known class-number/biquadratic-reciprocity congruence. Williams & Currie (1982) normalize b by b ≡ a·((p−1)/2)! and study class numbers against biquadratic residuacity. Their scanned paper could not be read here, so this attribution is unverified. Under (\*), the method is unconditional only in classes A and B.

**Cost.** One channel of length (p+1)/6 in the block engine, or two channels of length about (p+1)/12 sharing one tree ("layout 2"), plus one class number and O(log p) powerings. Class numbers:

- the stdlib method counts reduced forms in O(|D|^{1/2} polylog) operations, which has the same exponent as the product;
- PARI's `quadclassunit` is subexponential (Hafner & McCurley, 1989, give a rigorous subexponential algorithm), but PARI guarantees its output only under GRH.

The asymptotic class stays O(M_F(√p) log p). The total product length (p+1)/6 equals the nodal anchor's 2N + O(1), now in one channel.

**C5: the quarter identity [proved here].** Let p ≡ 5 (mod 12), q = (p−1)/4, ι₃ = 3^{q} (a square root of −1, since (3/p) = −1), and T = m!·q!/N!. Then

$$T^2\equiv\left(\tfrac2p\right)\frac{\iota_3}{2},\qquad T^4\equiv-\tfrac14,\qquad \left(\frac{m!}{N!}\right)^4\equiv a^2,\qquad \left(\frac{m!}{N!}\right)^2\equiv-\left(\tfrac2p\right)a\,\iota_3 H\pmod p.$$

*Proof.* Two exact mod-p forms are used:

- reflection Γ_p(x)Γ_p(1−x) = (−1)^{R(x)};
- Gauss multiplication ∏_{i<M}Γ_p((x+i)/M) = ε_M M^{1−R(x)}Γ_p(x), with ε_M = ∏_{0<i<M}Γ_p(i/M) (Robert, 2000, §7.1).

Both were checked in exactly these forms on 21 811 random instances (`research/verify_gamma_formulas.py`).

With p = 12N + 5, the residues are R(1/2) = 6N+3, R(1/3) = 4N+2, R(1/4) = 9N+4, R(3/4) = 3N+2, R(1/6) = 2N+1, R(5/12) = 11N+5 and R(7/12) = N+1. Hence

$$T=-\frac{\Gamma_p(1/3)\Gamma_p(3/4)}{\Gamma_p(7/12)},\qquad T^2=\frac{\Gamma_p(1/3)^2\,\Gamma_p(5/12)^2}{\Gamma_p(1/4)^2}.$$

The relations needed, after reflection, are:

- triplication at x = 1/4: Γ_p(1/12)Γ_p(5/12) = ε₃3^{1−R(1/4)}(−1)^NΓ_p(1/4)²;
- duplication at x = 1/6 and at x = 1/3: Γ_p(1/12)/Γ_p(5/12) = (−1)^{N+1}ε₂²2^{2−R(1/6)−R(1/3)}Γ_p(1/3)²;
- the constants ε₂² = Γ_p(1/2)² = (−1)^{6N+3} = −1 and ε₃ = (−1)^{R(1/3)} = 1.

Dividing the triplication relation by the duplication relation gives Γ_p(5/12)². Substituting:

$$T^2=3^{1-R(1/4)}\,2^{R(1/6)+R(1/3)-2}=3^{-3q}\,2^{(p-3)/2}=\iota_3\cdot\tfrac12\left(\tfrac2p\right).$$

Squaring gives T⁴ = −1/4. Gauss's H/(q!)² ≡ 2a then gives the last two identities. ∎

The sign of T² was confirmed at all 1516 development primes below 6·10⁴ and at all 18 round-2 confirmation primes p ≡ 5 (mod 12) (post-freeze check, labelled as such).

**Consequences and exact first failure.**

- A product of about p/12 factors, N!, determines c_p up to μ₄, which is half the length of P.
- Under (\*), the last identity becomes (m!/N!)² ≡ a·(m!/p), finite evidence at 2408 primes below 10⁵. Class numbers then reduce the ambiguity to one sign.
- The conductor-12 lattice (C7 below) contains no relation fixing that sign. This is the first exact failure of the quarter route.
- For p ≡ 11 (mod 12), Γ_p(1/4) is a second free direction, and no finite power of m!/N! lies in the lattice.

**C7: conductor-12 exact lattice [finite evidence].** `research/conductor12_lattice.py` intersects, over about 100 primes per class modulo 24, the exact multiplicative relations among the 11 grid factorials (R(k/12) − 1)!. The polylog constants allowed are −1, 2, 3, the cube roots of 2 and 3, a, b, 3^{(p−1)/4} and parity signs, optionally with the class-number Legendre symbols of the grid factorials. An exhaustive search then runs over all single intervals and pairs of intervals between grid residues.

| p mod 24 | Constants | Torsion of quotient | Min exact total length | Min Σ√length | Exact length-N interval? | Exact power of m!/N! |
|---|---|---|---|---|---|---|
| 5, 17 | polylog only | Z/2 ⊕ Z/4 | 2N | 2√N | no | 4 |
| 5, 17 | + Legendre (class numbers) | Z/2 ⊕ Z/2 | 2N | √(2N) | no | 2 |
| 11, 23 | polylog only | Z/2 ⊕ Z/4 (rank 2) | 2N | 2√N | no | none |
| 11, 23 | + Legendre (class numbers) | Z/4 (rank 2) | 2N | √(2N) | no | none |

The nodal anchor R_N, with two intervals of length N, is optimal in the polylog-constant calculus, tied with m!. Class numbers buy a single interval of length 2N, and nothing shorter. These are empirical lattices on finite ranges, not proofs.

## 6. Exact evidence

**Development (round 2).**

- C1–C5, both layouts, Mordell, Gauss and (\*), and both Dirichlet sums: exact at all 1632 admissible p < 3·10⁴.
- With FLINT: Mordell, Gauss and (\*) at all 8993 admissible p < 2·10⁵.
- Φ exactly invariant on 3032 random relations.
- Pilots: 1000003, 10000019, 100000037, 1000000021, 100000007, 1000000007 and 10000000019. These were excluded from confirmation.

**Confirmation (frozen rule; evidence/charp/CONFIRMATION_CHARP.json; all PASS).** Every case was checked as follows:

- c_p against 2(m!)^{−3}, with m! from FLINT's native factorial; the small set also against an independent stdlib linear loop;
- H against FLINT's h!;
- every applicable route;
- the stdlib forms class number against PARI;
- both layouts in the FLINT engine for all p, and in the stdlib engine (together with the round-1 nodal anchor) for p ≤ 2·10⁹. The large-set bin above 2·10⁹ therefore received FLINT checks only.

| Class | Small set | Large set (first prime ≥ 2·10^k, k = 6…11) |
|---|---|---|
| A, p ≡ 11 mod 12 (Mordell) | 300023, 300119, 300191 | 2000003, 20000003, 200000039, 2000000063, 20000000219, 200000000171 |
| B, p ≡ 5 mod 24 (Gauss; also \*) | 300149, 300221, 300317 | 2000093, 20000069, 200000069, 2000000141, 20000000117, 200000000093 |
| C, p ≡ 17 mod 24 (\* only) | 300017, 300089, 300137 | 2000081, 20000033, 200000033, 2000000033, 20000000201, 200000000129 |

These primes are disjoint from this round's development inputs, including the earlier rounds' inputs. They are not claimed to be globally historically unused.

The thin API `acquire_charp.py` was checked afterwards against these references (36 runs, `API_CHECK_CHARP.json`). Rows in class C are flagged as conditional.

## 7. Complexity and matched benchmarks

Notation: b = ⌈log₂p⌉, and M_F(L) is the cost of multiplying length-L field polynomials.

| Method | Products | Extra constants | Field work |
|---|---|---|---|
| m! block (round 1) / FLINT native | 1 × p/3 | — | O(M_F(√p) log p) |
| Nodal anchor, shared tree (round 1) | 2 × p/12 | χ(6) | same class |
| Half-interval (this round), layout 1 / 2 | 1 × p/6 / 2 × p/12 | h(D) with \|D\| ≤ 4p; a by Cornacchia | same class, plus class number |
| Quarter identity | 1 × p/12 | — | c_p known only up to sign (failure) |

**Benchmarks.** Five cold samples per method, rotated order, everything inside the timed region, all methods returning c_p (`evidence/charp/BENCHMARK_CHARP.json`, single machine, Python 3.13, python-flint 0.9.0 with FLINT 3.6.0, PARI 2.17.2). Medians are in milliseconds.

| p | Class | Stdlib m! block | Stdlib nodal | Stdlib HI1 (forms) | FLINT native m! | FLINT nodal | FLINT HI1 (PARI) | FLINT HI1 (forms) | Native / HI1 | Nodal / HI1 |
|---:|:-:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2000003 | A | 61.2 | 37.5 | 45.0 | 0.63 | 0.64 | 1.01 | 3.38 | 0.63 | 0.64 |
| 20000069 | B | 251.9 | 177.4 | 195.2 | 3.57 | 3.21 | 3.38 | 31.4 | 1.05 | 0.95 |
| 200000033 | C | 972.2 | 623.6 | 711.8 | 20.3 | 18.0 | 14.6 | 79.2 | 1.39 | 1.23 |
| 2000000033 | C | — | — | — | 121.1 | 98.4 | 80.0 | 244.6 | 1.51 | 1.23 |
| 2000000063 | A | — | — | — | 116.7 | 96.5 | 88.8 | 293.8 | 1.31 | 1.09 |
| 2000000141 | B | — | — | — | 111.7 | 97.4 | 94.8 | 440.2 | 1.18 | 1.03 |
| 20000000117 | B | — | — | — | 646.3 | 505.6 | 413.3 | 1300.0 | 1.56 | 1.22 |
| 20000000201 | C | — | — | — | 614.8 | 477.1 | 398.8 | 895.7 | 1.54 | 1.20 |
| 20000000219 | A | — | — | — | 536.8 | 521.7 | 413.4 | 823.8 | 1.30 | 1.26 |
| 200000000093 | B | — | — | — | 2747.0 | 2311.2 | 1926.8 | 4754.6 | 1.43 | 1.20 |
| 200000000129 | C | — | — | — | 2472.4 | 2199.6 | 1790.8 | 3462.2 | 1.38 | 1.23 |
| 200000000171 | A | — | — | — | 2606.8 | 2148.1 | 1802.1 | 3042.5 | 1.45 | 1.19 |

The evidence file has all 18 primes plus the FLINT block-factorial, layout-2 and class-number-only timings.

Interpretation:

- **FLINT backend, p ≥ 2·10⁹:** half-interval layout 1 with PARI class numbers is the fastest method, 1.18–1.56× faster than FLINT's native factorial on m! and 1.03–1.26× faster than the FLINT nodal anchor. The idealized single-channel prediction is √2 against m!. PARI's class number costs ≤ 1.5 ms.
- **Unconditional class number:** with the stdlib forms count (0.46–2.9 s at 2·10¹⁰–2·10¹¹), the FLINT half-interval method loses to FLINT nodal.
- **Pure-Python engine:** the round-1 shared nodal anchor remains fastest. The half-interval method runs at 0.77–0.94 of its speed, because two short channels sharing one tree are cheaper there than one long channel.
- **Small p:** fixed costs dominate.
- **FLINT nodal vs native:** 1.03–1.29× at p ≥ 2·10⁹, which qualifies the round-1 1.48–1.59× figure.
- **Engine fairness:** on the same m!, our FLINT block engine takes 0.98–1.49 times as long as FLINT's own factorial, so these gains are not an artifact of a weak engine.

No BGS shifting implementation, no batch remainder trees and no Tal-type method was benchmarked. Nothing is extrapolated beyond 2·10¹¹.

## 8. Prior work and status

| Claim | Status |
|---|---|
| Atkin recurrence, A_{n_p} ≡ ss_p, Prop. 5 hypergeometric form, special values | [background] Kaneko & Zagier (1998); El-Guindy & Ismail (2014) |
| D = ±1728^{N+ε}R_N; round-1 formulas (2), (3) | Implicit in KZ Prop. 5 (one line plus reflection); three independent proofs now on record |
| Wronskian identity (1) as confluent Christoffel–Darboux plus Gosper | [proved here]; probably routine; novelty unsettled |
| Signed normalization, nodal anchor | Opus round input, re-audited; independently re-derived via KZ |
| C6 formal obstruction and interval-length corollary | [proved here]; in the spirit of Koblitz–Ogus / Das-type Γ-monomial criteria; novelty unsettled |
| C1 half-interval identity; C3 Gauss route | [proved here] from Wilson, Gauss (1828), Dirichlet (Berndt, 1976) |
| C2 Mordell route | [background] Mordell (1961) |
| (\*) and its equivalent (m!/N!)² ≡ a(m!/p) | [conjecture]; 4504 development primes plus 18 fresh primes; possibly in Williams & Currie (1982), unverified |
| C5 quarter identity (T² and its sign) | [proved here]; first exact failure: one residual sign |
| C7 conductor-12 lattice optimality | [finite evidence] |
| FLINT-backend speed-ups 1.18–1.56× vs native m!, 1.03–1.26× vs nodal | Measured, these implementations, PARI class numbers (GRH-conditional speed; values cross-checked) |
| Sub-√p or polylog acquisition | Not obtained here. Tal (2026, unrefereed) claims p^{1/2−δ} for n! mod p for most primes; not audited |

## 9. Next question

C6 shows that sub-square-root acquisition of c_p needs Gauss/Jacobi data at conductor of at least about p^δ. The question is whether this can be done at the inert point 1/3 for **every** sufficiently large p ≡ 5 (mod 6):

> Is there an exact derivation of Γ_p(1/3)³, signs included, that uses Gross–Koblitz relations of conductor q ≤ p^{1/2−δ}, with Jacobi sums computable in p^{1/2−δ} time, and interval products of total length at most p^{1−2δ}?

Tal (2026) claims such constructions for general n! through divisors q of 1 + p + p², and also of p ± 1, for a density-one-minus-ε set of primes. Answering the question means specializing that construction to m!. One must then check whether the class p ≡ 5 (mod 6) and the point 1/3 are covered, with explicit δ and sign acquisition (van Wamelen's criterion).

## 10. Reproduction

Python 3.10 or later is required. The production core (`atkin.py`, `charp.py`) uses the standard library only. The FLINT comparator needs `pip install python-flint`, and the PARI class numbers need `pip install cypari2`. The research and audit scripts also need sympy.

```
python3 audit.py                    # both freezes + manifest
python3 develop.py; python3 confirm.py                 # round 1 (unchanged)
python3 develop_charp.py            # round-2 development  -> evidence/charp/DEVELOPMENT_CHARP.json
python3 confirm_charp.py            # frozen round-2 confirmation (~1.5 min)
python3 benchmark_charp.py          # matched benchmarks (~7 min; timings will differ)
python3 acquire_charp.py 200000000171 --backend flint --classno pari
python3 research/conductor12_lattice.py 6000 out.json  # C7 evidence
python3 research/verify_gamma_formulas.py               # post-freeze proof support
```

Regenerating evidence changes timings and output hashes, but both freezes still verify. Never overwrite a freeze to conceal a source change.

## References

Berndt, B. C. (1976). Classical theorems on quadratic residues. *L'Enseignement Mathématique, 22*, 261–304.

Berndt, B. C., Evans, R. J., & Williams, K. S. (1998). *Gauss and Jacobi sums*. Wiley.

Bostan, A., Gaudry, P., & Schost, É. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier–Manin operator. *SIAM Journal on Computing, 36*(6), 1777–1806. https://doi.org/10.1137/S0097539704443793

Costa, E., Gerbicz, R., & Harvey, D. (2014). A search for Wilson primes. *Mathematics of Computation, 83*(290), 3071–3091. https://doi.org/10.1090/S0025-5718-2014-02800-7

El-Guindy, A., & Ismail, M. E. H. (2014). On the Atkin polynomials. *Pacific Journal of Mathematics, 272*(1), 111–129. https://doi.org/10.2140/pjm.2014.272.111 (arXiv:1309.2123)

FLINT team. (2026). *FLINT: Fast Library for Number Theory* (Version 3.6.0, via python-flint 0.9.0) [Computer software]. https://flintlib.org

Gauss, C. F. (1828). Theoria residuorum biquadraticorum, commentatio prima. *Commentationes Societatis Regiae Scientiarum Gottingensis Recentiores, 6*.

Gosper, R. W. (1978). Decision procedure for indefinite hypergeometric summation. *Proceedings of the National Academy of Sciences, 75*(1), 40–42. https://doi.org/10.1073/pnas.75.1.40

Gross, B. H., & Koblitz, N. (1979). Gauss sums and the p-adic Γ-function. *Annals of Mathematics, 109*(3), 569–581. https://doi.org/10.2307/1971226

Hafner, J. L., & McCurley, K. S. (1989). A rigorous subexponential algorithm for computation of class groups. *Journal of the American Mathematical Society, 2*(4), 837–850. https://doi.org/10.1090/S0894-0347-1989-1002631-0

Kaneko, M., & Zagier, D. (1998). Supersingular j-invariants, hypergeometric series, and Atkin's orthogonal polynomials. In *Computational perspectives on number theory* (AMS/IP Studies in Advanced Mathematics, Vol. 7, pp. 97–126). American Mathematical Society. https://www2.math.kyushu-u.ac.jp/~mkaneko/papers/atkin.pdf

Mordell, L. J. (1961). The congruence ((p−1)/2)! ≡ ±1 (mod p). *The American Mathematical Monthly, 68*(2), 145–146. https://doi.org/10.2307/2312481

PARI Group. (2025). *PARI/GP* (Version 2.17.2, via cypari2 2.2.4) [Computer software]. https://pari.math.u-bordeaux.fr

Robert, A. M. (2000). *A course in p-adic analysis* (Graduate Texts in Mathematics, Vol. 198). Springer. https://doi.org/10.1007/978-1-4757-3254-2

Szegő, G. (1975). *Orthogonal polynomials* (4th ed., AMS Colloquium Publications, Vol. 23). American Mathematical Society.

Tal, Y. (2026). *Computing modular factorials below the square-root barrier* (ECCC Report TR26-211). Unrefereed; abstract read, not theorem-audited. https://eccc.weizmann.ac.il/report/2026/211/

Williams, K. S., & Currie, J. D. (1982). Class numbers and biquadratic reciprocity. *Canadian Journal of Mathematics, 34*(4), 969–988. https://doi.org/10.4153/CJM-1982-070-x (scan only; content not verified here)

Prior project inputs (unrefereed): the round-1 report (`provenance/REPORT_round1_20261018.md`); the Sol and Opus local reports (`provenance/`).
