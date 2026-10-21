# Independent review of the Opus prior-work and benchmark audit

21 October 2026

The package supports a useful and much more precise account of applicability and measured performance. Its general-trace derivation is mathematically promising. The historical conclusion should, however, distinguish a derivation newly found in this audit from an algorithm demonstrably published before the Cartier–Miller work. The audit expressly says that neither the regular-case theorem nor identity (A7′) was located in the sources read.

## What I checked

All 871 entries in the archive checksum manifest matched, and the supplied 15-file freeze verifier passed. I reviewed the comparison adapters, timing design, proof of (A7′), and relevant passages of Voloch’s 1997 primary paper. I recalculated the headline W1 medians from the archived validated timing CSV; these agree with the report.

I compiled the native C comparison kernel afresh and ran a bounded correctness suite using python-flint 0.9.0, supplying independently counted traces. This exercised enumeration, convolution, linear recurrences, polynomial powering, polynomial recurrences, the transparent BGS adapter, the frozen inherited evaluator, weighted-domain corrections, branch handling, and the stated scope corrections. No asserted comparison failed. These were correctness runs, not fresh performance measurements. I did not reproduce the PARI trace backend, the published Harvey binary, or the full archived confirmation campaign.

A separate fresh-seed comparison of the new general-trace evaluator against direct character enumeration covered 110 models over eleven primes from 7 through 211. All 4,948 values agreed: 4,610 general-route and 338 exceptional-route evaluations. Overlapping edge-case counts included 849 chains through the identity, 1,085 supersingular evaluations, and 156 evaluations in which the adapted point R was 2-torsion. Finite checks support the implementation; they do not replace proofs or establish historical priority.

## Historical interpretation

The identification of the exceptional case with Voloch’s high polynomial block and Semaev’s differentiated Miller construction is a substantial antecedent. The twist, translation, quartic adaptation, and exact normalization still need explicit attribution and proof. In particular, a sign selected by exhaustive small examples is not a symbolic normalization proof. If manuscript Lemma 3 supplies that proof, cite and verify the precise connection rather than treating the experiments as its replacement.

The general-trace identity

\[
bV(a)=(A-1)\alpha_p([p^{-1}\bmod n]P)
\]

has a persuasive short Cartier-operator argument. Its use of a Miller function at a point not necessarily of order p must remain explicit: this constant term is not automatically the anomalous-curve homomorphic transfer. The definition must handle every intermediate chain case, including passage through the identity.

Voloch’s 1997 paper supplies the high-block equation and a related characteristic-p zeta construction and addition law. That makes it a strong conceptual antecedent. It does not, by itself, establish that this exact scalar-evaluation algorithm, its complete adapters, and its complexity statement were previously published. The report itself labels (A7′)/(A7″) newly derived and leaves important sources unread.

I would replace the recommendation to “withdraw any suggestion that the O(log p) query is new” with this narrower statement:

> The exceptional specialization has close classical antecedents in Voloch and Semaev. This audit also derives a general-trace evaluator from classical Cartier and Miller constructions, with the same asymptotic query cost. We have not yet established whether that evaluator, or an equivalent algorithm, was explicitly published previously. Claims of algorithmic novelty and historical priority therefore remain provisional.

This wording does not establish novelty for Cartier–Miller. It preserves the distinction between mathematical dependence on classical facts and demonstrated publication priority.

## A reproduced small-field implementation failure

The general-route implementation branches only on twisted trace equal to 1 before attempting to invert p modulo the twisted curve order. For p at least 7, the Hasse bound makes this sufficient to detect divisibility by p. For p=5 it does not: a trace of -4 gives order 10.

Explicitly, take p=5, f=x^3+3x, and a=1. This cubic is squarefree, every nonzero x has chi(f(x))=1, its trace is -4, and direct evaluation gives C_f(1)=1. Calling the supplied `voloch_zeta_route.value(5, [0,3,0,1], 1, -4)` raises `ValueError: base is not invertible for the given modulus` at the inversion of 5 modulo 10. This is a reproduced failure outside the successful p>=7 sample above.

Proposition (A7′) itself correctly assumes p does not divide n; the unconditional use of twisted trace not equal to 1 in the subsequent adapter needs correction. State p>=7 for that route, or test gcd(p,n)=1 and supply a direct small-field fallback. This does not affect the archived large-field timings.

## A quartic proof omission and its repair

Section 4.2(v) divides by Y_R. The point R obtained from a nonbranch quartic input can nevertheless satisfy Y_R=0: for example, normalized even quartics can produce a nonzero 2-torsion R. Proposition (A7′), as stated, assumes the corresponding ordinate is nonzero. The quartic reduction therefore needs a separate paragraph.

When R is nonzero 2-torsion on the short model, put

\[
h_R=Y/(X-X_R).
\]

On E(F_p) minus {O,R}, negation pairs terms with opposite values; other fixed 2-torsion points contribute zero. Thus the sum of h_R is zero. From the already established decomposition

\[
1/z=\tfrac12h_R-g_1/4,
\]

the resulting character sum is

\[
C_f(a)=-\chi(f(a))\,g_1(n-2)/4,
\]

where n is the order of the normalized twisted curve. For the general route n is even and prime to p, so [p^{-1} mod n]R=R. A Miller function for p at R is proportional to (X-X_R)^{(p-1)/2}; its logarithmic differential has zero constant term at O in t=-X/Y. Hence alpha_p(R)=0. Since n-2 is congruent to -1 minus the twisted trace modulo p, this agrees with (A7″).

The exceptional anomalous case has n=p odd and cannot contain nonzero rational 2-torsion. Thus this omission does not invalidate its separate formula. The 156 fresh successful checks support the proposed repair, but the paragraph belongs in the proof.

## What the performance evidence supports

| Workload | Supported observation |
|---|---|
| Cold scalar queries at 20 bits | The measured Python Cartier–Miller implementation, including its trace preparation, beats the named BGS implementations by about 26 times for cubics and 62 times for quartics. |
| Cold scalar queries at 40 bits | Archived medians are about 1 ms for Cartier–Miller versus 7–16 seconds for BGS on the tested cases. |
| Very small fields | Native linear or polynomial methods can win. |
| Many poles on one small-field curve | Polynomial preparation and convolution can amortize; dense-query methods win decisively in some tested regimes. |
| Branch poles | The BGS implementation beats the tested Python second-kind implementation. |
| Fixed poles, coefficient-only queries | The methods reduce to comparable cached dot products. |

These are matched-output implementation comparisons on the recorded host, not universal algorithm rankings. At large bit sizes trace acquisition dominates the cold timings. PARI used the reported CM/BSGS paths; the package does not supply a measured SEA/Schoof comparison, a native Cartier–Miller implementation, or a many-prime benchmark. The post-freeze alternative-route timings are exploratory and must remain separate from the frozen comparison.

The disclosed host interruption, reconstructed deterministic case metadata, and memory-budget overruns limit how tightly one should interpret the experiment. In particular, do not use over-budget jobs as evidence of winning under a 512 MiB limit. The fifteen-file freeze is narrower than a freeze of the entire timing harness. These qualifications do not erase the validated results, but should accompany strong performance claims.

## Recommended next revision

Retain the measured sparse-query advantage and the workload-dependent comparisons. Repair the reproduced p=5 failure. Complete a self-contained proof of (A7′)/(A7″), its Miller constant-term convention, and the 2-torsion case. Finish the symbolic exceptional normalization. Then complete the identified primary-source gaps before making a definitive priority claim or deciding how far to narrow the paper’s central contribution.

Treat the newly found general-trace route as an alternative derivation within this research project until its publication history is established. It may simplify the implementation and presentation considerably. The current evidence warrants revising and strengthening the manuscript, not deciding that its main algorithmic contribution has already been shown to be previously published.

The supplied manuscript and proposed application section were not edited during this review.
