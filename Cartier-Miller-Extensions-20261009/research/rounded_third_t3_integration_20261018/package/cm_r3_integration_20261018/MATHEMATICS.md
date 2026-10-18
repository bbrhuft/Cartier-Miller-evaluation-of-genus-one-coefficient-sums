Exact identities and the integration boundary

Let p >= 11 be prime with p=6k+5, m=(p-2)/3 and L=m+1. All arithmetic below is in F_p. Define a_i=binom(2i,i)8^(-i), B_n=sum_{i<n} a_i, t_0=1, t_{i+1}=t_i(h+2+i)/(2i+2), h=(p-1)/2, and U_p(n)=sum_{i<n}(h+1+i)t_i. The denominators used for n<=L are units. A strict prefix stops before a_n.

The following derivation is elementary background retained in the project, included here so that the integration identities can be reviewed without any elliptic assumption. The recurrence a_{i+1}/a_i=(2i+1)/(4i+4) and h=-1/2 show by induction that t_i=(2i+1)a_i. Put Q_i=2i(2i+5)a_i. Direct substitution gives

$$4a_i-Q_{i+1}+Q_i=\frac{(2i+1)^2}{2}a_i=(h+1+i)t_i.$$

Summing proves U_p(n)=4B_n-2n(2n+5)a_n. This proof does not use a factorial reduction, a Miller evaluator or Jacobi sums. It justifies the complete_sum assembly once its two input values have been acquired correctly.

Let G=m!. Wilson complementation gives (2L)!(m-1)!=-1, because 2L+(m-1)=p-1 and 2L is even. Since (m+1)!=(m+1)G and (m-1)!=G/m,

$$a_L=-\frac{m}{(m+1)^2}\,8^{-L}G^{-3}.$$

The congruences m=-2/3, m+1=1/3 and 8^L=2^{3L}=2^{p+1}=4 reduce this to a_L=(3/2)G^(-3). The cube map is bijective since gcd(3,p-1)=1, so the adapter recovers G from a_L by the unique cube root of 3/(2a_L), with exponent (2p-1)/3. It never treats this conversion as a hardness statement.

The last binomial recurrence gives a_L/a_m=-1/4, hence a_m=-4a_L and B_m=B_L+4a_L. Substitution into the telescoping identity gives

$$U_p(L)=4B_L-\frac{17}{3}G^{-3},\qquad U_p(m)=4B_L-\frac{16}{3}G^{-3}.$$

Consequently U_p(L)-U_p(m)=-(1/3)G^(-3) is nonzero, so these two sums cannot vanish simultaneously. Also a_L never vanishes. The rounded-third multiplier 2L(2L+5)=34/9 vanishes only at p=17 in the stated domain. Checking U alone there cannot check the acquired boundary, so all complete components are checked separately.

The geometric input is the retained project theorem that ThirdPointPrefixProvider supplies the stated B_L by the d=3 Cantor–Miller kernel; its implementation and independent elliptic implementation are preserved. The source theorem remains unrefereed. Both are compared against the coefficient definition throughout development and on declared confirmation/survey inputs; these finite checks are not the proof of the theorem.

The boundary input is Opus's R3.1 small-conductor Jacobi reconstruction and its T3 anchor identities. For a prime q in [5,89] dividing p-1, the exact integer relation plans, ideal construction, norm certificate and van Wamelen root-of-unity selection justify every accepted value. The LLL search is not proved to discover the required vector for every eligible prime. Automatic mode tries a bounded chain and falls back to the exact nodal or factorial route; it never substitutes an uncertified value. No class number, point count or supplied unknown scale is used by the new T3 path.

For fixed conductor bounds, this remains a square-root product method, plus Miller's logarithmic arithmetic and setup. The deterministic searches for suitable character elements are charged in actual timings; this note does not assert that their unconditional worst-case costs are polylogarithmic. The dense forest has a different, amortized cost model: one exact ordered triangular recurrence product supplies many primes at once. Its integer work depends on the maximum cutoff even on a sparse prime schedule. The retained BATCH_PROOF and RETAINED_FOREST_PROOF give the source invariants and bounds.

Primary background includes Kaneko and Zagier (1998), https://www2.math.kyushu-u.ac.jp/~mkaneko/papers/atkin.pdf; van Wamelen (2002), https://doi.org/10.4064/aa102-1-1; Harvey and Sutherland (2016), https://doi.org/10.1090/conm/663/13352; and Tal (2026), https://eccc.weizmann.ac.il/report/2026/211/ (unrefereed). The complete source reports and their attribution limits are preserved under vendor/atkin_r3. No new priority or general optimality claim is made.
