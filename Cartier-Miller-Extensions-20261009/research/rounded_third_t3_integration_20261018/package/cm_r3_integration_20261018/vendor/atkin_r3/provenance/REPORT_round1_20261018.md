# Atkin endpoint reduction and shared signed-scale acquisition

David Jordan research project, 18 October 2026. AI-assisted and unrefereed. The investigation combines the supplied Sol and Opus local reports with classical Atkin-polynomial theory. No publication, priority, universal lower bound, polylogarithmic algorithm or new best factorial algorithm is claimed.

## Result

There is useful partial progress. A rational Wronskian identity collapses the four-component Atkin value/derivative recurrence at its supersingular endpoint to a single explicit scalar product. A shared product/remainder implementation of the resulting signed-scale problem outperforms both included factorial comparators at the two largest matched benchmark primes. At p=100,000,007 its median cold acquisition is 386 ms, compared with 614 ms for the matched block-factorial comparator, a 1.59-fold speedup. It also acquires the requested derivative with only logarithmic additional normalization work.

The mathematical simplification does not remove the factorial-type product. The asymptotic work remains O(M_F(sqrt(p)) log p), rather than poly(log p), and no sub-square-root exponent was obtained. The practical improvement is specific to these standard-library implementations. Optimized BGS shifting, FLINT, PARI, GMP and the recent unrefereed Tal algorithms were not implemented or benchmarked.

## Exact target and inherited bridge

Supply a certified prime p>=11, p=5 mod6. Define

$$N=\left\lfloor\frac{p-5}{12}\right\rfloor,\quad
\epsilon=\begin{cases}0&p\equiv5\pmod{12},\\1&p\equiv11\pmod{12},\end{cases}
\quad n=N+1+\epsilon.$$

Let A_j(J) be the monic Atkin polynomials with

$$A_0=1,\quad A_1=J-720,\quad A_2=J^2-1640J+269280,$$

and for j>=2

$$A_{j+1}=(J-\alpha_j)A_j-\beta_j A_{j-1},$$
$$\alpha_j=\frac{24(144j^2-29)}{(2j+1)(2j-1)},\qquad
\beta_j=\frac{36(12j-13)(12j-7)(12j-5)(12j+1)}{j(j-1)(2j-1)^2}.$$

The classical Atkin theorem identifies A_n modulo p with the supersingular polynomial, including its roots at 0 and, when epsilon=1, 1728. The signed derivative target is D=A_n'(0). It is a distinguished polynomial derivative in the modular invariant J, not differentiation of the original Frobenius-composed value circuit.

The supplied Opus global identity, checked algebraically here and independently through factorial references, gives

$$\boxed{c_p=-\frac{4\chi(6)(-1)^N}{3\,1728^N(-1728)^\epsilon}\,D,}
\qquad c_p=2\left(((p-2)/3)!\right)^{-3}.$$

For completeness, if P is the product of the supersingular j-invariants other than 0 and 1728, then A_n(J)=J(J-1728)^epsilon Q(J), with Q monic of degree N. Therefore P=(-1)^N D/(-1728)^epsilon. The Opus identity is P=-(3/4)chi(6)1728^N c_p. The roots are simple, so D is nonzero. This uses the exact signed scale, with no square-root or sign-selection step.

The supplied local reports and their proof qualifications are retained under provenance/. Their shared branch-chart conclusion is consistent: leading residues reach one terminal cancellation but do not acquire its amplitude. This global experiment uses a different recurrence and does not invoke their model-specific limitations as lower bounds.

## A homogeneous constant-space baseline

Writing a_j=A_j(0), d_j=A_j'(0), the literal recurrence is

$$a_{j+1}=-\alpha_j a_j-\beta_j a_{j-1},\qquad
d_{j+1}=a_j-\alpha_jd_j-\beta_jd_{j-1}.$$

It has four field-element components, but a scalar inverse at every step is not free. The implemented baseline clears a common denominator

$$q_j=j(j-1)(2j-1)^2(2j+1).$$

Multiplying the four-component update by q_j and retaining a fifth residue S=product q_j gives a homogeneous state with one final inverse. In particular the derivative component receives q_j a_j as its forcing term. All q_j are p-units for 2<=j<n, since 2j+1<p. Induction proves that the four stored numerators have the same denominator S. This yields O(p) field operations and O(1) stored residues, with scalar setup, indices and the final inversion charged. It avoids dense polynomials but is not faster than factorial acquisition.

## Exact Wronskian collapse

Set beta_1=393120; this is the exceptional first recurrence coefficient obtained from the initial polynomials, with alpha_1=920. Put

$$W_j=a_jd_{j+1}-a_{j+1}d_j,\qquad B_j=\prod_{i=1}^j\beta_i,$$
$$R(j)=\frac{(12j-1)(12j+5)}{96j}.$$

**Proposition.** Over Q, for every j>=1,

$$\boxed{W_j=a_j^2 R(j)-\tfrac14 B_j.}\tag{1}$$

Here is a complete elementary proof. The classical special value, also obtained by checking its initial value and substituting its ratio into the recurrence, is

$$a_j=\frac{(-12)^{3j+1}(-1/12)_j(5/12)_j}{(2j-1)!},\qquad
r_j:=\frac{a_{j+1}}{a_j}=-\frac{6(12j-1)(12j+5)}{j(2j+1)}.$$

To prove the special-value expression without importing an evaluation oracle, check a_1=-720 and r_1=-374, and verify the rational identity r_j=-alpha_j-beta_j/r_(j-1) for j>=2. The product formula then follows by induction; it is used for proof, not as a cheap acquisition input.

The value/derivative recurrences give exactly W_j=a_j^2+beta_j W_(j-1). Also

$$\gamma_j:=\frac{\beta_j}{r_{j-1}^2}
=\frac{(j-1)(12j-5)(12j+1)}{j(12j-13)(12j-7)},$$

and the rational difference telescopes:

$$R(j)-\gamma_jR(j-1)
=\frac{(12j-1)(12j+5)-(12j-5)(12j+1)}{96j}=1.$$

It follows that a_j^2 R(j) obeys the same inhomogeneous recurrence as W_j. At j=1, W_1=911520 and a_1^2R(1)=1009800, whose difference is -98280=-beta_1/4. Their difference subsequently multiplies by beta_j. This proves (1).

This is a discrete Wronskian/Christoffel-Darboux-type calculation using classical Atkin special values. It was derived in this investigation; novelty has not been established.

## Endpoint corollary: no derivative propagation remains

Let r=n-1. All denominators in (1) through index r are p-units. The special-value product shows a_n=0 mod p and a_r!=0. If p=12N+5, then r=N and the factor 12r+5 equals p; if p=12N+11, then r=N+1 and 12r-1 equals p. Therefore R(r)=0 mod p.

Reducing (1) gives a_r D=-B_r/4. For 1<=j<r, the intermediate ratios are nonzero and

$$\frac{\beta_{j+1}}{r_j}
=-\frac{6(12j+7)(12j+13)}{(j+1)(2j+1)}.$$

Since -beta_1/(4a_1)=273/2, cancellation of the known special-value ratios proves

$$\boxed{D=\frac{273}{2}\prod_{j=1}^{n-2}
\frac{-6(12j+7)(12j+13)}{(j+1)(2j+1)}\pmod p.}\tag{2}$$

The product is empty when n=2. Its factors and denominators are all p-units for the two allowed prime classes. Equation (2) computes a numeric signed derivative using scalar products; it does not use a selected-coefficient oracle or an unavailable normalization. It eliminates the four-component matrix product, but retains a number of scalar factors proportional to p.

## Simplifying the nodal anchor

The faster implementation uses a closely related product for c_p. The Opus nodal argument is as follows. For h=(p-1)/2, m=(p-2)/3 and k=(p-5)/6, the Hasse polynomial factors as

$$H(t)=c_p t S(t^3/B^2),\quad B=1/4,$$
$$S(x)=\sum_{i=0}^{\lfloor k/2\rfloor}
\frac{m!k!}{(m-i)!(3i+1)!(k-2i)!}x^i.$$

At t_s=-3/4 the cubic is (z-1/2)^2(z+1). Summing quadratic characters gives H(t_s)=chi(6). Modulo p the terminating series S reduces to a Gauss hypergeometric polynomial. Chu-Vandermonde gives S(-27/4)=(C-b)_N/(C)_N, with C=4/3 and b=(1-k)/2 for k even, b=-k/2 for k odd. These are identities whose denominators are p-units in the displayed ranges.

In both cases C-b is congruent to -N modulo p: their sum with N equals p/6. Hence (C-b)_N=(-1)^N N!, and

$$\boxed{c_p=-\frac43\chi(6)(-1)^N\frac{(4/3)_N}{N!}.}\tag{3}$$

This simplifies the earlier anchor; it is not a new exponent reduction. The linear implementation uses integer progressions product(3j+4)/product(3j+3), with 2N modular factor multiplications and a final inverse, versus approximately 4N factors for m!. The original Opus anchor already had two length-N products; the new practical improvement is sharing their multipoint evaluation infrastructure.

## Shared product acquisition and its proof

Choose w=floor(sqrt(N)) and q=floor(N/w). For a in {4/3,1}, build the monic block polynomial P_a(X)=product_(i=0)^(w-1)(X+a+i). Evaluate both at the same points 0,w,...,(q-1)w, multiply the resulting values and append fewer than w tail factors. This returns (a)_N exactly. Reduction of the argument into blocks proves the identity directly; no interpolation or recognition oracle is needed.

Both channels use the same product tree of evaluation points. At each remainder-tree node, the implementation acquires one inverse of the reversed divisor to the maximum required precision, then uses it for both dividends. The polynomial remainder formula is exact and each child residue is the corresponding polynomial modulo its monic divisor. Induction on the tree proves every evaluation. One final field inverse forms the ratio in (3).

The comparator computes m! using exactly the same engine and polynomial multiplication backend with a single channel starting at 1. Both skip unnecessary Fermat powering of the constant 1 during monic inversions. A separate-channel control uses the same point tree but recomputes the reversed-divisor inverses for each channel. This isolates the gain from shared inverses. All cold calls build their own trees, constants and normalization; there is no fixed-prime cached context. At the largest benchmark prime, sharing reduced inverse-series calls from 11544 to 5772 and polynomial multiplication calls from 58832 to 45288 relative to the separate-channel control, as recorded in the raw metadata.

The immutable polynomial backend and generic product/remainder ancestor are supplied under vendor/, with provenance inherited from Sol. The new SharedArithmetic code is readable in atkin.py. Per-call metadata records polynomial products, coefficient operations, integer packing, scalar operations inside the tree, and inverse-series call counts. Setup pow calls and some integer coefficient construction are explicit in source and included in timings and asymptotic bounds; the backend counters alone are not presented as complete counts of every scalar setup operation or Python instruction.

## Complexity and restricted telescoping limitation

Let b=ceil(log_2 p), M_F(L) be field polynomial multiplication cost, and mu(b) modular multiplication/reduction bit cost.

| Method | Field work including scalar setup | Stored residues |
|---|---|---|
| Homogeneous direct Atkin derivative | O(p+log p) | O(1) |
| Endpoint Wronskian product, linear | O(p+log p) | O(1) |
| Simplified nodal product, linear | O(p+log p), with shorter main product | O(1) |
| Shared nodal products, generic block method | O(M_F(sqrt(p)) log p+log p) | O(sqrt(p) log p) |
| Matched factorial block acquisition | Same asymptotic class | Same asymptotic class |

All methods assume prime certification is supplied. Conversion between D and c_p costs O(log p) field work, including Legendre powering and normalization. Recovering m! from c_p uses the unique cube root of 2/c_p, with charged exponent (2p-1)/3.

The scalar block method uses polynomial lengths O(sqrt(p)). Carry-free integer packing has slot width O(b+log p), so a safe bit bound is O(log p times [M_Z(sqrt(p)(b+log p))+sqrt(p) rho(b+log p,b)+sqrt(p)(b+log p)]), plus polynomial-in-b scalar setup. Here rho charges reduction of an unpacked integer modulo a b-bit p. With CPython the integer multiplication backend is Karatsuba at these sizes; no FFT asymptotics are inferred from timings. Trees and reversed-divisor series occupy O(sqrt(p) log p) field residues plus temporary packed operands and Python overhead. A process peak-RAM measurement was not performed.

There is a small exact negative fact about a tempting shortcut. The ratio R_N=(4/3)_N/N! obeys R_(N+1)/R_N=(N+4/3)/(N+1). There is no nonzero rational function Q(X) over characteristic zero with Q(X+1)/Q(X)=(X+4/3)/(X+1). Indeed, on each orbit of roots modulo integer translation, a rational coboundary Q(X+1)/Q(X) has total zero divisor multiplicity. The right side has a zero at -4/3 and pole at -1 in distinct such orbits. This rules out one characteristic-zero rational telescoper, even after a constant exponential factor (whose value must be 1 by behavior at infinity). It is not a finite-field or circuit lower bound. Characteristic-dependent identities, supplied arithmetic anchors and more general representations remain open.

## Exact evidence and benchmark discipline

The rational Wronskian identity was checked with exact Fraction arithmetic at indices 1 through 40. Development checked every acquisition method at all 152 admissible primes below 2000. Four timing pilots used 10007,100019,1000037,10000019; their inputs were included in the frozen exclusion list, and pilot timings are not the final table.

CANDIDATE.md, the production and validation sources, benchmark runner and vendor dependencies were hashed before confirmation selection. The frozen rule selected six small confirmation primes and five bin-selected larger primes, disjoint from all current development inputs. All 11 passed. At the first nine, direct Atkin recurrence, endpoint product, nodal products and factorial acquisition agreed. At the two largest, the slow direct Atkin recurrence was omitted as specified before selection; endpoint product, shared/separate block products and linear factorial agreed. A non-square block width 7 was also checked at inputs up to 2,000,000.

The exact confirmation primes are 2003,2027,2039,2063,2069,2081,10037,100043,1000121,10000079,100000007. They are not claimed globally historically unused. The largest case gave c_p=68178598 and D=69532504. Full raw residues, sources, interpreter, precision and counters are in evidence/. The report's numerical statements must be read with those records; proofs, rather than finite agreement, establish the formulas.

After exact confirmation completed, every timing method received five cold samples, with method order rotated across repetitions. All methods return c_p, so their outputs are matched. The methods also return metadata; its construction occurs inside the timed region. Each call starts without reusable prime setup. The table below contains medians in milliseconds.

| p | Factorial linear | Factorial block | Nodal linear | Nodal separate | Nodal shared | Shared / best factorial speedup |
|---:|---:|---:|---:|---:|---:|---:|
| 10037 | 0.141 | 2.604 | 0.120 | 2.193 | 1.769 | 0.08x |
| 100043 | 1.569 | 10.550 | 1.336 | 9.528 | 7.235 | 0.22x |
| 1000121 | 16.021 | 39.902 | 12.916 | 35.310 | 25.752 | 0.62x |
| 10000079 | 165.320 | 140.797 | 126.028 | 120.681 | 95.118 | 1.48x |
| 100000007 | 1595.478 | 614.198 | 1236.454 | 517.194 | 386.221 | 1.59x |

At the two largest inputs, shared evaluation beats the best included factorial method by 1.48 and 1.59 respectively. It beats the same nodal acquisition with separate channels by approximately 1.27 and 1.34. At smaller inputs the linear factorial loop remains faster than shared block acquisition; an automatic choice must retain that regime. The linear nodal ratio also gives a smaller loop-based improvement. Neither phenomenon establishes a new asymptotic algorithm or a win over optimized external libraries.

## Closest prior work and status

Kaneko and Zagier (1998), Theorems 3-4 and Proposition 6, supply the supersingular reduction, recurrence and special values underlying the derivation. El-Guindy and Ismail (2014), especially Theorems 3.1, 4.1 and 5.1, place the polynomials in associated-Jacobi theory and give coefficient/hypergeometric representations. A short primary-source reading did not establish whether the particular modular endpoint form (2) has already been stated. The Wronskian identity is plausibly a classical consequence of this theory; no priority claim is made.

Bostan, Gaudry and Schost (2007) are the appropriate selected-term asymptotic comparator. This implementation is a generic product/remainder-tree method, not optimized BGS shifting. The ECCC abstract of Tal (2026, TR26-211, unrefereed) also reports divisor-dependent sub-square-root bounds and a divisor-free logarithmic refinement. Its theorem and implementation were not audited in this task, so this report makes no claim against those bounds and does not use an outdated Wilson-quotient quotation as a normalization lower bound.

| Claim | Status |
|---|---|
| Atkin recurrence and supersingular reduction | Established primary literature |
| Signed global normalization and nodal anchor | Supplied Opus result, algebraically checked and restated |
| Wronskian identity and endpoint scalar product | Complete proof in this investigation; novelty unsettled |
| Homogeneous direct recurrence and shared product engine | Proved correct and exactly confirmed |
| 1.48-1.59 speedups at the largest two benchmark inputs | Measured for the included matched Python methods |
| Polylogarithmic or sub-square-root exponent improvement | Not obtained |
| Rational-coboundary limitation | Proved only over characteristic zero, in the stated rational model |

The strongest standalone contribution is the exact endpoint collapse together with a reproducible shared-product implementation and a modest matched performance gain. The next research question is whether a characteristic-p interval identity can evaluate (4/3)_N/N!, for the p-related N above, below square-root cost while acquiring every boundary normalization. The characteristic-zero telescoper is unavailable, but the investigation proves no obstruction to a genuinely finite-field mechanism.

## Reproduction and references

Use python3 acquire_derivative.py p --method shared for the fast derivative API. This thin wrapper was added after core confirmation and checked against all 11 frozen-confirmation derivatives; its separate source hash and role are in evidence/API_WRAPPER_CHECK.json. The benchmark table times signed c_p acquisition; the API additionally times the O(log p) conversion to the derivative. Run python3 audit.py on the delivered package before regenerating timed evidence. Run python3 develop.py for exact rational and development checks, python3 confirm.py for the frozen confirmation, and python3 benchmark.py for matched timings. All production code uses the Python standard library. Regenerating output evidence changes its timings and output manifest; the source freeze still verifies. Never overwrite the actual freeze to conceal a source change.

Kaneko, M., & Zagier, D. (1998). Supersingular j-invariants, hypergeometric series, and Atkin's orthogonal polynomials. In Computational perspectives on number theory (pp. 97-126). AMS/IP. Primary full text: https://www2.math.kyushu-u.ac.jp/~mkaneko/papers/atkin.pdf

El-Guindy, A., & Ismail, M. E. H. (2014). On the Atkin polynomials. Pacific Journal of Mathematics, 272(1), 111-129. https://doi.org/10.2140/pjm.2014.272.111 ; author version https://arxiv.org/abs/1309.2123

Bostan, A., Gaudry, P., & Schost, E. (2007). Linear recurrences with polynomial coefficients and application to integer factorization and Cartier-Manin operator. SIAM Journal on Computing, 36(6), 1777-1806. https://doi.org/10.1137/S0097539704443793

Tal, Y. (2026). Computing modular factorials below the square-root barrier. ECCC TR26-211. Unrefereed; abstract inspected, not theorem-audited in this investigation. https://eccc.weizmann.ac.il/report/2026/211/
