# Research prompt: normalized CM-to-Cartier comparison and one new certified seed

Investigate a bounded extension of David Jordan's Cartier–Miller evaluation project. Establish, correct or refute the proposed normalized CM-to-Cartier comparison, recover the existing depth-one, depth-two and depth-three formulas through it, and certify one additional class-number-one CM seed, preferably discriminant -7, with -8 as the alternative. Aim for a modest theorem and an auditable evaluator that a computational number theorist could review.

Read START_HERE.md, PROJECT_STATE.md, knowledge/CM_Eisenstein_Proposal_Assessment_20261012.md and the supplied depth-three review before developing a new method. Run unpack_retained.py if file execution is available. It makes the original manuscript, retained implementations, historical failed branches, current depth-three code and adversarial checks available in their expected directory structure. The two original easy seeds and all six non-seed families through depth three have already been researched. Do not spend the task rediscovering their parameterizations.

Treat all inherited proofs, numerical outputs and AI assessments critically. The CM comparison is not established by the retained package; an 80-digit numerical check only supports its normalization. Existing results remain unrefereed. No repository URL or commit is supplied: do not invent one, claim GitHub inspection, publish anything, or revise the published manuscript. Write a separate extension note and ledger.

## Exact conventions and the question to prove

Let p>=7 be prime, E/F_p be nonsingular with short equation y^2=F(x)=x^3+Ax+B, and h=(p-1)/2. Define

$$H=[x^{p-1}]F^h,\qquad \beta=[x^{p-2}]F^h,\qquad
\omega=dx/y,\qquad\eta=x\,dx/y.$$

The retained formulas are C(omega)=H omega and C(eta)=beta omega. On ordinary inputs H is nonzero, so the candidate slope is c=beta/H and the Cartier-killed line is represented by eta-c omega. H is the Hasse invariant, congruent to the exact Frobenius trace modulo p; it is not a chosen twist or normalization constant. Establish explicitly how the meromorphic second-kind representatives map into de Rham cohomology and how this Cartier line relates to the reduction of the unit-root line. Do not silently identify different Frobenius or Verschiebung conventions.

For a characteristic-zero CM lift, use a lattice Lambda=lambda(Z+tau Z), x=wp(z), y=wp'(z)/2, so omega=2 dz, g_2=-4A and g_3=-4B. Define

$$E_2^*(\tau)=E_2(\tau)-\frac3{\pi\operatorname{Im}\tau},\qquad
s_2(\tau)=\frac{E_2^*(\tau)E_4(\tau)}{E_6(\tau)}.$$

The proposed model-normalized comparison, for AB nonzero, is

$$\boxed{\frac\beta H\equiv-\frac{3B}{2A}s_2(\tau)\pmod{\mathfrak p}.}$$

This is a target, not a premise. Derive every sign and constant from the chosen lattice, differential and full-period convention; correct the target if necessary. A proposed complex argument uses the line eta+G_2^*(Lambda) omega, with G_2^*=pi^2 E_2^*/(3lambda^2). Verify it rather than copying it. Identify an exact algebraic representation of s_2, specify its field, conjugate and reduction prime, and prove that it reduces to the coefficient slope of the actual supplied model. State all exclusions: bad reduction, nonordinary primes, CM conductor/discriminant, p-adic integrality, eigenvalue separation, model and CM-value denominators, and collisions. Handle A=0 and B=0 separately; the displayed quotient cannot be used there.

The true model-independent quantity in this chart is A beta/(BH), not beta/H by itself. Under the finite-field quadratic twist (A,B)->(d^2 A,d^3 B), beta/H transforms by multiplication by d. Your new recognition, formulas and tests must include both square and nonsquare d.

## Literature and proof audit

Use the precise source pointers in knowledge/SOURCE_GUIDE.md. Katz's Sections 1.3 and 5.7, Comparison Theorem 8.0.9 and Lemma 8.0.13 are the central leads. Bruinier–Ono–Sutherland's Class polynomials for nonholomorphic modular functions gives a concrete algebraic route using Masser's observation. Its simplest formula excludes D=-3d^2; this affects -12 and every A=0-seed depth discriminant. Do not apply a non-special formula outside its hypotheses. Obtain and verify the special treatment, or use another exact CM/endomorphism argument for those cases.

Do not state that raw E_2^*(tau) is an algebraic j-invariant. Separate period normalization from weight-zero CM values. Verify literature claims in the actual primary sources and give exact section/theorem/page references, keeping inaccessible sources explicitly unverified. Check whether the proposed identity, algorithm or even its computational interpretation is already standard. Existing class-polynomial algorithms have conditional complexity statements; do not drop GRH hypotheses or promote them to an unconditional complexity theorem.

A route using an exact de Rham matrix of a certified CM endomorphism is acceptable if it proves the same normalized line and yields the needed coefficient without a hidden expensive oracle. The objective is a correct comparison and useful application, not allegiance to one analytic formula.

## Recover the completed six families

Read the existing recognizers and proof notes before adding code. Derive the CM value independently of the retained isogeny slope; then compare with the six targets in knowledge/EXISTING_FAMILIES.md. Merely defining s_2 from the desired slope and comparing it back is circular. The retained paths may be used as independent checks and to explain why the established special cases agree.

The first normalization control is D=-12, tau=i sqrt(3), A=-15r^2, B=-22r^3, whose established coefficient is beta/(rH)=-1. The proposed comparison predicts s_2=5/11. The retained Decimal calculation agrees numerically, but is not an exact proof. Prove the exact value through a certified algebraic identity or another legitimate argument. Recover the other five cases with matching algebraic conjugates, scales and twists, without replacing their exact all-prime claims by finite agreement. If an obstruction prevents full recovery, locate it precisely and report which cases are proved, conditional, numerically supported or unresolved.

An exact table (j,s_2), a rational function R_D(J) in Q[J]/(H_D(J)), or a certified equivalent representation is suitable. Separate class polynomials for j and s_2 alone do not pair their roots: provide the correspondence. For fixed D, record degrees, coefficient sizes, denominators, finite exceptional primes and recognition/reduction cost. Do not describe precomputing a growing-degree algebra as constant work.

## Certify one new seed

Prefer D=-7 unless a documented source or normalization issue makes D=-8 materially simpler. Use exactly one as the principal new result; the other may be a control. Candidate short models are y^2=x^3-35x-98 (j=-3375) and y^2=x^3-30x+56 (j=8000). Verify their CM identification, good-reduction domain and model normalization from exact arithmetic and primary sources before relying on them. These examples are suggestions, not supplied new-seed certificates.

For the selected seed, obtain an exact slope formula, a parameter-checked model/twist recognizer, an explicit admissible-prime criterion and a complete list or justified handling of exceptional primes. Verify that the result adds classes outside the existing six families at admissible primes; account for modular j-collisions rather than assuming distinct characteristic-zero j-values stay distinct modulo every prime. A fixed j test may suffice at nonexceptional primes only if the model scale/twist and coefficient reconstruction are also checked.

The new evaluator must return normalized data for the original cubic, not just a j-value or a slope. For f=1+cw+bw^2+aw^3, a nonzero, v^2=f(w), use

$$x=aw+b/3,\quad y=av,\quad
A=ac-b^2/3,\quad B=a^2-abc/3+2b^3/27,$$
$$\beta=aK+(b/3)H,\quad K=(\beta-(b/3)H)/a.$$

The differential equality dw/v=dx/y is exact. If f(w)^h=sum_i d_i w^i, define T_f(mu)=sum_(i=0)^(p-1) d_i mu^i. The manuscript's equivalent reciprocal-parameter notation is S_f(1/mu)=T_f(mu). After preparation a nonzero rational root mu gives the retained branch query

$$T_f(\mu)=\frac{a\mu(\mu H-K)}{f'(\mu)}.$$

Keep this mu convention consistent with the retained code and its definitions of T and S. Explicitly check that the root is nonzero and simple. If you restate the formula using another convention, derive the conversion and signs.

Specify separately the costs of obtaining exact CM values, recognizing the supplied model, certifying p and any input trace, preparing the trace, selecting/reducing the algebraic conjugate, reconstructing H and K, and querying a supplied branch root. A new classical signed trace route is welcome if it can be verified within scope. Otherwise retain the unconditional Schoof setup and state its cost; a supplied trace or practical PARI ellap does not eliminate that cost in a complete theoretical claim. SEA/PARI may be practical comparators or checks. The source includes experimental Schoof and point-count BSGS backends, not a production SEA implementation.

## Independent validation and execution honesty

Before implementing, inspect the retained code and historical branches. The known p=1 modulo 3 third-point evaluator, restricted higher-genus fast prefixes and complete precision-two Witt/BGS recurrence products are already present; none solves the missing rounded-third boundary or a sum-avoiding Witt correction. The historical precision-two direct-lift and unit-root-substitution counterexamples, including p=13, must remain recorded. Do not reopen the rounded-third problem in this task.

If execution is available, write a small exact validation suite. Compare literal multinomial or dense-polynomial H,beta against your independently prepared CM value, and compare original-cubic K and branch queries against retained O(p) recurrences or direct coefficient sums. Cover all admissible small primes through a stated bound, both twist types, each conjugate in the recovered families, exceptional/ineligible primes, wrong supplied traces, altered certificates and matching/disjointness with the old recognizers. Include fresh cases beyond the retained fixtures. Larger controls are useful only when their independent reference and certification are clearly stated.

If execution is unavailable, continue the theory and provide runnable source and test recipes, but label every numerical result unexecuted. Never print a fabricated PASS table or call expected output observed output. A tool failure is not a mathematical counterexample. A floating approximation or integer-relation guess must be followed by an exact certificate before becoming a theorem.

Benchmarks are optional and secondary. Any performance claim must compare identical complete outputs and moduli, charge mandatory setup/reconstruction/representation and input certification, distinguish cached queries from full runs, and retain raw CSVs, repetitions, source hashes, environment and validation. A branch-point result is not a result for the original weighted sum unless both B_L and its boundary a_L are computed. No generic K lower bound is established by the existing reference backends.

## Scope and deliverable

Deliver a proof note or explicit counterexample with assumptions and normalization spelled out; an exact CM-value representation and admissible-prime certificate; recovery records for the six established families; one new certified seed and its original-cubic evaluator if the theorem supports it; runnable validation code and actual results where tools permit; and a ledger recording the question, sources, derivation, independent checks, counterexamples and present status. Put essential proofs in the note rather than only in generated scripts or opaque computer-algebra output.

Separate established classical facts, newly derived unrefereed statements, finite tests, conjectures and failures in the report. If the broad comparison is already classical, say so and identify the genuinely new application, if any. If the comparison fails in this normalization, preserve the obstruction and narrow the result. If only part of the task is settled, make the unresolved bridge explicit instead of claiming that all CM curves or depth four are routine.

The minimum useful outcome is a critically reviewed normalization/reduction argument plus a concrete decision on whether exact fixed-discriminant CM data can provide the coefficient more directly. The intended stronger bounded outcome is the recovered six-family formulas and one new seed. Do not expand to growing depth, generic CM-order discovery, precision two or BSD during this pass. Work toward that outcome autonomously and return a reviewable report suitable for a separate adversarial check by another AI and ultimately human specialists.
