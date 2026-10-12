# Existing coefficient targets: six non-seed families

These are retained, unrefereed algebraic results supported by proof notes and independent finite checks. They are controls for the new comparison. Read the corresponding code and proof notes for exceptional-prime and recognition arguments rather than treating this table as a stand-alone certificate.

Let p>=7, r nonzero, y^2=x^3+Ax+B, H=[x^(p-1)](x^3+Ax+B)^((p-1)/2), and beta=[x^(p-2)] of the same power. Arithmetic in the following table is modulo p. The underlying ordinary seeds A=0,p=1 modulo 3 and B=0,p=1 modulo 4 both have beta=0 and are handled separately from the AB-nonzero comparison.

| Family | Assumptions | A/r^2 | B/r^3 | beta/(rH) | CM discriminant |
|---|---|---|---|---|---|
| Depth one from A=0 | p=1 modulo 3 | -15 | -22 | -1 | -12 |
| Depth one from B=0 | p=1 modulo 4 | -11 | -14 | -1 | -16 |
| Depth two from A=0 | p=1 modulo 12, e^2=3 | -135-60e | -694-420e | -(3+2e) | -48 |
| Depth two from B=0 | p=1 modulo 8, e^2=2 | -91-60e | -462-308e | -(3+2e) | -64 |
| Depth three from A=0 | p=1 modulo 24, e^2=3, g^2=2 | -1095-540e-540g-420eg | -22198-13860e-16380g-8820eg | -(7+6e+6g+2eg) | -192 |
| Depth three from B=0 | p=1 modulo 8, s^4=2 | -731-600s-540s^2-360s^3 | -14798-11816s-10164s^2-8456s^3 | -(7+4s+6s^2+4s^3) | -256 |

The last eligibility condition is equivalent to p=x^2+64y^2; the latest proof-review addendum supplies a verified reciprocity argument. Distinct short-model counts at eligible nondegenerate primes are (p-1), 2(p-1), and 4(p-1) at depths one, two, and three. Do not carry over the external suggestion's count of 4(p-1) for every family.

The normalized rooted quotient is

$$A'=-4A-15q^2,\quad B'=-8Aq-22q^3,\quad
\phi^*\omega'=\omega,\quad
\phi^*\eta'=(2x-q)\omega-2d\left(\frac{y}{x-q}\right).$$

Thus H'=H and beta'=2beta-qH. A seed-to-target chain of length d gives beta/H=-sum(2^(d-1-i) q_i), since the seed slope is zero. Its normalized inverse has the appropriate powers of four in its kernel coordinates. These are existing comparison routes, not the new path-free proof.

| Fixture | Certified data |
|---|---|
| A=0 depth three, p=73 | Short model (4,16), e=21,g=41,r=42; slope 15; trace 10; H=10,beta=4. |
| Original cubic for the retained A=0 fixture | f=1+4w+37w^3 has short model (2,55); H=10,K=55,T_f(9)=3. |
| B=0 depth three, p=73 | Short model (16,27), s=18,r=27; slope 44; trace -6; H=67,beta=28. |
| Original cubic for the retained B=0 fixture | f=1+60w+10w^3; H=67,K=32,T_f(17)=5. |

After unpacking, the lower-depth recognizer is retained/inherited/research/depth_two_recognition_20261006/core/recognize.py. The depth-three implementations are retained/inherited/research/depth_three_recognition_20261007/core/depth_three_recognize.py and depth_three_b0_recognize.py. The combined recognizer is recognize_short_through_depth_three in the first of those modules.

The code's positive coefficient extraction uses fixed field work. Prime validation, a status-label exponentiation on some negative inputs, complete trace preparation and reconstruction must be counted separately. The default accepted-family trace formulas are deterministic given the appropriate primary representation; obtaining its square root still uses a randomized nonresidue search.
