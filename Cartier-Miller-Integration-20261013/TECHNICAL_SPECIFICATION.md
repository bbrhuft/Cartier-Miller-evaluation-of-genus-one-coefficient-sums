# Mathematical and software specification

Cartier–Miller consolidation, 13 October 2026. This specification fixes interfaces and verifies assembly of retained results. Project theorems remain unrefereed; finite checks are not mathematical proofs or novelty certification.

## Canonical target and modulus

For a prime $p$, put $h=(p-1)/2$ and retain the ORIGINAL rational definitions

```math
\begin{aligned}
t_0 &= 1,\\
t_{i+1} &= t_i \frac{h+2+i}{2i+2},\\
U_p(L) &= \sum_{0 \leq i < L}(h+1+i)t_i.
\end{aligned}
```

The integrated sum domain is $5\le p<2^{64}$, $0\le L\le h$, and precision $r\in\{1,2\}$. Rational denominators are units modulo $p^r$. The output is an exact residue modulo $q=p^r$. Python booleans are rejected as integer inputs. Unsupported hypotheses and budget exhaustion raise errors; the CLI returns status `error` and exit code 2.

Define $a_i=\binom{2i}{i}8^{-i}$ and the STRICT prefix $B_L=\sum_{i<L}a_i$. Modulo $p$,

$$U_p(L)=4B_L-2L(2L+5)a_L.$$

This formula does not redefine the original sum at precision two. There,

$$
U_p(L)\equiv4B_L-2L(2L+5)a_L+p\mathcal H_L\pmod{p^2},
$$

with the odd-harmonic correction from the retained p-adic report. The complete precision-two fallback evaluates the original rational recurrence directly through matrix products, avoiding a separate harmonic sum without claiming a geometric shortcut.

## Service contracts

| Service | Input | Exact output | Preparation and limits |
|---|---|---|---|
| `evaluate` / `Session.evaluate` | $p,L,r$, method, budget | Original $U_p(L)$; optional prefix/boundary diagnostics | Prime validation and all uncached acquisition included in a fresh call |
| `Session.evaluate_many` | Several indices at one prime | Ordered outputs, including duplicates | Direct mode shares one pass; higher mode shares one prefix pass and lazy fifth intervals; tree mode uses separate original-sum products |
| `RowSession.query` | Normalized squarefree cubic/quartic, trace setup, $\lambda\in\mathbb F_p$ | $S_f(\lambda)=\sum_{m<p}[w^m]f^h\lambda^{p-1-m}$ | Direct point counting capped at 5000 by default; supplied traces are trusted; quartic branch poles not integrated |
| `cartier_data` | Short model $A,B$, optional trace | $H,\beta,\kappa=\beta/H$ when ordinary | Fixed-D formulas where recognized; otherwise $O(p)$ coefficient recurrence, capped by budget |
| `branch_query` | Normalized cubic and supplied simple nonzero root | $H,K,T_f(\mu)$ | Root finding excluded; model/basis conversion included |
| `quarter_precision_diagnostics` | Quarter-family prime, direct/tree method | $B_n,a_n,U_p(n),K_p,\Gamma,d,\mathcal H_n,J_p$ | Computes sums before recovering corrections; no sum-avoiding claim |
| `weighted_sum` | Falling-factorial polynomial weights | $\sum_{i<L}P(i)a_i\bmod p$ | Shares $B_L,a_L$ acquisition; degree cap 31 |
| `general_weight_prefixes` | Genus and allowed prime/weight | All allowed general-weight prefixes | Does not return a formal derivative or original $U$ |
| `CharacterSumSession.single_pole` (added 21 Oct) | Squarefree cubic/quartic $f$, any constant term, nonbranch pole $a$ | $C_f(a)=\sum_{x\ne a}\chi(f(x))/(x-a)\bmod p$ | Exact signed projective trace supplied (trusted) or counted directly up to the point-count budget; $O(\log p)$ field operations per query after the trace |
| `CharacterSumSession.prepare(U).evaluate` (added 21 Oct) | Complete excluded set $U$, residues, constant | Character, affine-point and projective-point sums of $c+\sum_i r_i/(x-a_i)$ over $x\notin U$ | Preparation $O(s\log p+s^2)$, then $O(s)$ per coefficient vector; active branch residues refused |

Input prime testing uses the retained deterministic unsigned-64-bit Miller–Rabin witness set. This is an implementation domain, not a restriction of all project theorems. Native precision-two sources have the narrower $p<2^{32}$ word-modulus domain and a pinned FLINT ABI. They are not selected by this prototype.

## Sum dispatch and exact assembly

The planner recognises complete mod-$p$ endpoints, quarter points and ordinary third points. Endpoints use $U_p(0)=0$ and $U_p(h)=4(2/p)$. The quarter family requires $p\ge13$, $p\equiv1\pmod4$, $L=(p-1)/4$. Ordinary third points require $p\equiv1\pmod3$, $L=(p-1)/3$, $p\ge7$. Their evaluator uses the undivided characteristic-$p$ formula, including the exceptional trace/character equality. The older divided third evaluator is not used for this service.

For $d=2g+1$, $p\equiv-1\pmod d$, the higher-genus pass supplies all $B_{j(p+1)/d}$ with $1\le j\le g$. It includes its family-specific setup and does not count points. The explicit hybrid then obtains the boundaries using products. At genus one it uses the retained rounded-third factorial identity $a_{(p+1)/3}=3/(2(m!)^3)$, $m=(p-2)/3$. At genus two it uses the accepted tenth-point formulas. With $L=(p+1)/5$ and $\ell=L/2$,

$$
a_L=(-1)^\ell2^{-2L}\binom{2L-1}{\ell},\qquad
a_{2L}=(-1)^\ell\frac{2^{2L}}{16}\binom L\ell.
$$

Only $\ell!$, the interval $[3\ell,4\ell-1]$, and $[\ell+1,2\ell]$ are needed. The prototype acquires two intervals for a single boundary and three for the pair, reusing the denominator. At higher genus the boundary uses $(L+1)\cdots(2L)/(L!)8^L$. These are exact product methods, not logarithmic boundary methods. If $2L(2L+5)=0\bmod p$, the boundary is unnecessary for the original sum and is skipped; its diagnostic `a` is then null. The $p=29$, second fifth-point example is retained.

Automatic selection does not select a higher-genus hybrid merely because its prefix is logarithmic. It prefers complete structural methods, then direct work for $L\le128$, otherwise the product tree. The 128-term rule is a reproducible conservative policy, not a platform-calibrated optimum. Explicit methods remain available. Requests exceeding the selected method's budget are refused; no hidden slow computation or estimate substitutes for an answer.

## Weighted character and elliptic-point sums (added 21 October 2026)

`cm_system/character_sums.py` exposes the supplement adapter of `Cartier-Miller-Character-Sums-20261021/`. Its arithmetic is in `cm_system/backends/character_sums/`, copies of the frozen supplement sources whose only change is package-relative imports; `PROVENANCE.json` records both hashes. The mathematics and proofs are in that folder's `proofs/UNIFORM_ORDER_PROOF.md` and `docs/MATHEMATICS.md`.

For a nonbranch pole $a$, put $e=\chi(f(a))$, $g(z)=f(a+z)/f(a)$, $g_1=f'(a)/f(a)$ and $N=p+1-e\tau_f$. With $R$ the image of $(0,-1)$ on the short model of $v^2=g(z)$,

$$
C_f(a)=e\left(-\frac{g_1}{4}(N-2)-\frac{\alpha_N(R)}{2}\right),
$$

where $\alpha_N$ is the Laurent constant of $d\log f_{N,R}$ at the origin. One differentiated Miller chain of length $O(\log p)$ is used, for every trace and for $p\ge5$. The prepared state adds the common-domain corrections $D_i(v)=\sum_{j\ne i}v_j/(a_i-a_j)$ and the constants $K_f-\sum_iw_i$ and $K_f-s-\sum_iw_i$, with $K_f=1-N_\infty-\tau_f$. A cubic has one rational point at infinity and a quartic has $1+\chi(\text{leading coefficient})$; no character value is assigned at infinity. Every excluded coordinate stays excluded, even with zero residue.

The service keeps the adapter's contract and adds only this layer's conventions: deterministic primality for $5\le p<2^{64}$, rejection of booleans, the `conditional_on_trusted_trace` label for supplied traces, and an optional direct trace count. The count evaluates $\chi(f(x))$ at all $p$ points, $O(p\log p)$ field operations, and is refused above `Budget.point_count_prime` (default 5000). For larger $p$ the caller supplies an exact signed trace from a point-counting method; neither the Hasse interval nor the Miller endpoint certifies it. The standalone supplement package has no 64-bit limit but leaves primality to the caller. Active branch poles, higher-order poles, polynomial parts, nonrational or unfactored denominators, integer or interval character sums and nonlinear $\chi(Rf)$ sums are outside this service. The proved polynomial-tree correction is not implemented; preparation uses pairwise differences with one batch inversion and $O(s^2)$ temporary storage.

`validate_character_sums.py` compares the service with an independent enumeration and the adapted backend with the frozen sources, and checks the refusals; `recorded_results/validation_character_sums_20261021.json` is its recorded run. No timing of this code has been measured. The benchmark medians in the manuscript and in `Cartier-Miller-Character-Sums-20261021/historical_benchmark/` belong to the older frozen implementation.

## Recurrence backend and cost

The standard-library fallback reuses the historical polynomial matrix block/remainder tree, adapted only for package imports. For the original sum, the state $V_i=2^ii!(t_i,it_i,U_p(i),1)^T$ has the degree-one recurrence in the p-adic report. Products are ordered $M(L-1)\cdots M(0)$ and the initial state is $(1,0,0,1)^T$. A final inversion removes the denominator. Empty products give the $L=0$ identity.

The same product engine computes binomial states and interval products over $\mathbb Z/q\mathbb Z$. Monic remainder divisions invert no nonunits. Default width is $\lfloor\sqrt L\rfloor$ beyond the direct base case, with a configured cap of 4096. The engine is a conventional product/remainder tree, not the later native shifted-interpolation BGS implementation. Its algebraic cost is described with the chosen polynomial multiplication function, conventionally $O(\mathsf M_R(\sqrt L)\log L)$ at fixed matrix dimension, and tree storage $O(\sqrt L\log L)$ coefficients. Python integer packing and multiplication have their own bit costs; timings do not count abstract ring operations. No quadratic field, trace or Miller setup is needed by original-sum fallback queries.

Special-family Miller query work is logarithmic at fixed genus after the appropriate preparation. The maximal higher-genus bound is $O(g^3\log p)$ including its special setup. Generic row trace acquisition in this prototype uses a direct count and can dominate; Schoof's theoretical guarantee is not a delivered generic implementation here. Cornacchia setup retains its nonresidue-search qualification. Fixed-D CM table acquisition is historical precomputation; the table is fixed-size only for the fixed retained discriminants. Growing CM orders and table construction are not free inputs.

## Models, scalars and trust

For a short model, $H=[x^{p-1}](x^3+Ax+B)^h$, $\beta=[x^{p-2}](x^3+Ax+B)^h$, and the required basis is $\omega=dx/y$, $\eta=x\,dx/y$. The ordinary slope is $\kappa=\beta/H$. This is not the differential scale named `kappa` in the older row-model code; that scale is $-2$. This naming collision is confined to internal backends and explained in results/specification rather than merged.

For $f=1+cw+bw^2+aw^3$, the branch chart is $x=aw+b/3$, $y=av$, so $dw/v=dx/y$ and

$$
A=ac-b^2/3,\quad B=a^2-abc/3+2b^3/27,\quad K=(\beta-(b/3)H)/a.
$$

At a supplied nonzero simple root $\mu$,

$$T_f(\mu)=\frac{a\mu(\mu H-K)}{f'(\mu)}.$$

The generic cubic coefficient fallback translates $x=u+s$ to make the constant term nonzero, choosing among $s=0,1,2,3$. A cubic cannot vanish at all four distinct residues for $p\ge7$. After normalization and scaled coefficient extraction, translation gives $H_{\rm shifted}=H$ and $\beta_{\rm shifted}=\beta-sH$. Higher polynomial terms give no contribution to these two coefficients by their binomial residues. The implementation converts back before returning the specified basis. Supersingular models return $H,\beta$ and null slope, rather than dividing by zero.

The fixed-D table unifies the six depth families and the -7/-8 controls where eligible. Both corrected depth-three recognizers, including D=-256, are retained and cross-checked against it. The CM comparison's separation, integrality and basis qualifications remain in `evidence/CM_review.md`. No arbitrary characteristic-$p$ meromorphic quotient is asserted to be the project's de Rham realization. The public coefficient service is not a generic fast CM discovery routine.

A Hasse bound is only a necessary condition on a supplied trace. The status `conditional_on_trusted_trace` is retained unless the implemented D=-7 shape/sign certificate applies or the trace was acquired internally. A row's internally acquired trace is reused at cubic branch queries through the two model isomorphisms. The project’s other trace-sign algorithms are retained evidence, not silently advertised as the coefficient service’s selected backend.

## Precision two and combined correction

The integral quarter model and local parameter are fixed. The prime-to-$p$ torsion lift, moving pole $z=1+pd$, corrected coefficient $\varepsilon$, boundary and $\Gamma$ follow the retained p-adic report. Its formula is

$$B_n=\Gamma-p(K_p+2d(b+a))\pmod{p^2},$$

where $b=B_n\bmod p$ and $a=a_n\bmod p$. Its Witt $K_p$ is not the cubic branch coefficient $K$ and not the ordinary short-model $\beta$. The live diagnostics compute $B_n$ first and use the reverse identity to recover $K_p$. Independent full-series extraction supplies small-prime validation. The acquisition route remains square-root-style product work, not a fast extraction theorem.

Combining retained formulas gives

$$
U_p(n)=4\Gamma+\frac94a_n+pJ_p\pmod{p^2},\qquad
J_p=\mathcal H_n-2a-4K_p-8d(b+a)\pmod p.
$$

This is an algebraic combined target. The prototype recovers it from independent complete sums for diagnostics; it does not provide a new extraction algorithm. Cancellation remains a possible research question.

## General weights and differentiation

The general-weight polynomial $S_L(\lambda)=\sum_{i<L}\binom{2i}{i}(\lambda/4)^i$ satisfies

$$a_L=\frac{B_L-S_L'(1/2)}{4L}\pmod p.$$

This identity is useful but not a new research shortcut. The recovered fifth-point report already proves the equivalent identity and diagnoses the gap: adding $\lambda^p-\lambda$ preserves finite-field values but changes the formal derivative. The finite-field divisor annihilation does not persist under arbitrary infinitesimal movement, because the differential of $[p+1]$ is the identity on the tangent space. A valid derivative method must acquire and account for its endpoint correction. Automatic differentiation of the numerical value circuit alone is not justified. The exact $p=19$ false-derivative boundary 8 versus true 15 is retained.

## Reproducibility and operational boundaries

The final validation checks exact binomial and rational references, model scaling, branch formulas, exceptional queries, split-algebra paths, forced product widths, correction residues, duplicate indices, trust labels, caps and nonzero failure exits. It includes seeded sampling and exhaustive bounded ranges. `results/validation.json` reports actual overlapping check counts, not a count of independent proofs.

Benchmarks compare identical complete original-sum outputs. Each timed evaluation creates a fresh Session; imports and serialization are excluded, prime checks and acquisition are included. Multi-output direct work is shared, higher prefixes and fifth intervals are shared, and product-tree original-sum baselines run separate products per index; that unshared baseline is explicitly disclosed. Memory runs occur separately in fresh child processes and report both Python allocation peaks and absolute process RSS where available. Cached repeated-answer lookups and fresh-process timings are separate observations, not combined into arithmetic speedups.

There is no native Windows test, generic canonical-lift implementation, fast formal derivative, sum-avoiding Witt extractor, Tal backend, tuned universal dispatch, repository publication or new lower-bound claim. The later native packages and Tal audit remain separately identified rather than relabelled as this prototype’s implementation.
