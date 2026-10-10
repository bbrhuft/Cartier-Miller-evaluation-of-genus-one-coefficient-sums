# Current task and knowledge status

7 October 2026, updated 10 October 2026. This handover adds one depth-three family with a direct recognition certificate to the retained depth-at-most-two results. The manuscript is unchanged; the repository URL and commit remain unknown and GitHub has not been inspected.

| Item | Status and limits |
|---|---|
| Cubic branch/root identity, explicit second-kind normalization, degree-two transport | Retained; the transport's curve equation, holomorphic scale $+1$, exact correction, dual scaling and cofactor lemma were re-verified symbolically in this pass and independently by a second worker |
| Ordinary easy seeds | $A=0$ with $p\equiv1\pmod3$; $B=0$ with $p\equiv1\pmod4$; $\beta=0$ |
| Depth at most two | Retained explicit families, direct recognition and proof note; tested exhaustively at primes 7 through 127 |
| Depth three, $A=0$-seed chain (this handover) | Explicit family $A=\alpha(e,g)r^2$, $B=\gamma(e,g)r^3$, $\beta=-(7+6e+6g+2eg)rH$, $e^2=3$, $g^2=2$, eligible exactly for $p\equiv1\pmod{24}$; $j$ on the class polynomial of discriminant $-192$; direct $O(1)$ recognition by relative norms, complete and sound at every eligible prime by integer factorization; all quadratic twists absorbed; exhaustively tested at ten primes through 577 and at primes up to 63 bits |
| Trace of an accepted curve | Equals the seed's trace and is $\pm t_0$ with $4p=t_0^2+192f^2$ unique (Cartier transport, CM by $\mathbb Z[\omega]$, Kohel's volcano theorem as stated by Sutherland); complete preparation by Cornacchia plus the deterministic sextic sign rule (Ireland & Rosen Ch. 18 Thm 4, verified 10 October), no point counting; randomized only in the $\sqrt{-3}$ search; Las Vegas test retained as a cross-check; Schoof remains the fully deterministic fallback |
| Depth three, $B=0$-seed chain | Deferred: third roots exist iff $4+3e$ is a square with $e^2=2$; $j$ on `polclass(-256)`, dihedral Galois group; rejected by this recognizer at all eligible primes by the resultant with $H_{-192}$ |
| Depth four and all-family classification | Not attempted; retained finite audit only |
| Modulo-73 target | $(4,16)$ is $(e,g,r)=(21,41,42)$, multiplier 15; the cubic $1+4w+37w^3$ has short model $(2,55)$, $r=15$, multiplier 21, $\beta=64$, $K=55$, $T_f(9)=3$ |
| General $k$ recovery | Open beyond justified families; the formal-jet reduction remains a non-oracle |
| Unreachable ordinary component | Retained $p=13$ example $(1,1)$; unaffected |
| Third point, restricted higher genus, precision-two Witt/BGS, trace backends | Retained unchanged; no production SEA backend; PARI used only as an independent check |

For $f=1+cw+bw^2+aw^3$ define $H=[w^{p-1}]f^{(p-1)/2}$, $K=[w^{p-2}]f^{(p-1)/2}$, use $x=aw+b/3$, $y=av$, giving $A=ac-b^2/3$, $B=a^2-abc/3+2b^3/27$, $dw/v=dx/y$ and $\beta=aK+(b/3)H$. The normalized quotient at a rational root $q$ is $(A',B')=(-4A-15q^2,-8Aq-22q^3)$ with $H'=H$ and $\beta'=2\beta-qH$. A verified input-to-easy path gives $\beta=H\sum_iq_i/2^{i+1}$ without dividing by $H$. The branch formula is $T_f(\mu)=a\mu(\mu H-K)/f'(\mu)$.

For benchmarks, compare identical outputs and moduli, charge mandatory preparation and reconstruction, and distinguish complete runs from cached queries. No new timing claim is made. An original weighted-sum result needs $B_L$ and $a_L$; nothing here supplies them. Proof correctness and novelty remain subject to independent human review; the second worker's adversarial report is retained but is not a referee report.
