# Frozen candidate: Atkin endpoint reduction and shared product acquisition

Certified p>=11, p=5 mod6 is supplied. Write N=floor((p-5)/12), eps=1 for p=11 mod12 and 0 otherwise, and n=N+1+eps. A_n denotes the classical monic Atkin polynomial with A_1=J-720 and A_2=J^2-1640J+269280.

The exact global target is D=A_n'(0). The signed normalization is

$$c_p=-\frac{4\chi(6)(-1)^N}{3\,1728^N(-1728)^\epsilon}D.$$

The following is an exact characteristic-zero Wronskian identity. Put a_j=A_j(0), d_j=A_j'(0), beta_1=393120 and use the standard Atkin beta_j for j>=2. Then

$$a_jd_{j+1}-a_{j+1}d_j
=\frac{(12j-1)(12j+5)}{96j}a_j^2-\frac14\prod_{i=1}^j\beta_i.$$

At the supersingular endpoint, a_n=0 modulo p and a_(n-1) is a unit, and the rational coefficient in the first term vanishes. Consequently

$$\boxed{D=\frac{273}{2}\prod_{j=1}^{n-2}
\frac{-6(12j+7)(12j+13)}{(j+1)(2j+1)}\pmod p.}$$

This is a scalar hypergeometric product; no matrix product or derivative jet is needed. Its acquisition is still factorial-type, not polylogarithmic. A second signed-scale formula, simplifying the preceding Opus nodal anchor, is

$$c_p=-\frac43\chi(6)(-1)^N\frac{(4/3)_N}{N!}.$$

The executable candidate acquires the numerator and denominator rising products using one common multipoint-evaluation tree, one reversed-divisor inverse per required node shared by both channels, and one final field inverse. Its abstract cost remains O(M_F(sqrt(p)) log p), with O(sqrt(p) log p) stored residues. The proposed gain is a possible implementation-level constant factor against a matched generic factorial backend. It is not a new asymptotic factorial algorithm or a claim against optimized libraries.

The direct five-residue homogeneous Atkin recurrence is also supplied, with one common denominator and a single inverse at the end. This corrects any implicit assumption that a modular scalar inverse at every step is free.

Development includes all 152 primes p=5 mod6 below 2000 and exploratory timing primes 10007,100019,1000037,10000019. Exact rational Wronskian checks used indices 1 through 40. The sources and statements are frozen before confirmation selection.

Confirmation rule: first six admissible primes strictly above 2000, excluding every development input; plus the first admissible prime at or above each of 10^4,10^5,10^6,10^7,10^8 excluding development inputs. This is disjoint from this candidate's development only, not globally historically unused. Full direct Atkin confirmation is used through 2*10^6; above that, the Wronskian endpoint, shared products and independent factorial reference are compared. Timings do not count as additional mathematical proof.

Benchmark rule: use the five bin-selected confirmation primes, after all exact confirmation checks finish, five cold samples per method, rotated method order, no cached setup. Compare linear factorial, matched generic block factorial, linear nodal ratio, separate-channel nodal block evaluation and shared-channel nodal block evaluation. All return c_p with setup and normalization included. The shared and separate block algorithms use the same polynomial multiplication backend, block-size rule and monic-inverse optimization. Record all samples and arithmetic metadata; do not extrapolate to 1201-bit primes.
