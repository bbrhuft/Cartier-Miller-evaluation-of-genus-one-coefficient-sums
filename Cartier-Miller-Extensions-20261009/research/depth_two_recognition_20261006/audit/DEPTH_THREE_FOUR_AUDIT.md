# Independent audit of higher-depth rational degree-two classes

6 October 2026. This is a bounded computational audit with an explicit normalization argument. It does not revise the manuscript, establish generic fast Cartier-data recovery, or claim priority for classical isogeny constructions.

## What the class quotient means

For a nonsingular short model E(A,B): y²=x³+Ax+B over F_p, p>=7, a base-field isomorphism preserving infinity has x'=u²x and y'=u³y, with u nonzero. Thus the appropriate graph identity is the orbit

\[
(A,B)\longmapsto(d^2A,d^3B),\qquad d=u^2\in(F_p^\times)^2.
\]

The validator uses the lexicographically smallest pair in this orbit. It does not merge all curves with the same j-invariant. In particular, nonsquare quadratic twists are retained as separate F_p classes. Every nonzero coefficient of each permitted easy family is included as a seed; quartic and sextic forms of the special j-invariants are consequently retained too.

The orbit key is only an identity for finite graph enumeration. Every discovered certificate retains its actual, unscaled models and kernel roots, so every quotient has differential scale +1. When a key is compared with its actual model, the square scale d is recorded, H_key=H_model and beta_key=d beta_model are checked independently. A point isomorphism using a chosen square root u has differential pullback scale 1/u; silently replacing an actual certificate model by its key would omit this scale.

## Removing the dual step and preserving completeness

For the explicitly normalized quotient at q,

\[
A'=-4A-15q^2,\qquad B'=-8Aq-22q^3,\qquad
H'=H,\quad\beta'=2\beta-qH.
\]

The distinguished dual kernel is q'=-2q. Its normalized quotient gives (A'',B'')=(16A,64B), the square scaling d=4 of the original model, and beta''=4 beta. This supplies no new isomorphism class.

A path containing these adjacent dual steps can be shortened by deleting them and multiplying every remaining kernel and displayed x-coordinate by the inverse scale 1/4. Its final model is square-isomorphic to the former endpoint; an easy endpoint remains easy under this scaling. Hence deleting immediate dual steps preserves seed reachability on the true isomorphism graph. Breadth-first discovery can also discard a previously visited orbit without changing minimum distances, because scaling carries the entire rational root set and all outgoing edges to their corresponding scaled roots and targets.

The code independently compares pruned and unpruned breadth-first searches at every tested prime. Both the depth-four searches and the fully exhausted finite seeded graphs have identical reachable keys and minimum class depths.

A nondual edge need not add a class. For example, at p=7 the easy model (0,1) has quotient roots 3 and 5. Their targets (5,1) and (3,1) are square-isomorphic and give the same graph class. The respective beta values are 5 and 6; the recorded scale d=4 takes 5 to 6. Counting the two root choices as two newly covered classes would overstate the extension.

After the initial vertex, there are at most two nondual rational roots, rather than three. The unmerged search tree through depth d therefore has at most

\[
1+3\sum_{i=0}^{d-1}2^i=1+3(2^d-1)
\]

vertices. Complete fixed-degree randomized root factoring yields expected O(2^d log p) field work for this search before any isomorphism merging, plus the work needed to maintain and verify certificates. A finite retry cap must still report incomplete splitting. This improved bound applies to a search that actually removes immediate dual steps; the retained earlier production finder still explores an unpruned tree and retains its O(3^d log p) expected bound. The present exhaustive root scan costs O(p) per model and is used only for validation. It supplies no practical timing comparison or fast deterministic discovery implementation.

## Genuine new classes at depths three and four

The audit includes every prime 7<=p<=251, fifty-one primes in total, and every F_p isomorphism class of nonsingular short cubics at those primes. It independently computes H and beta by exact integer multinomial coefficient extraction, not by importing the retained recurrence evaluator. Exact point counts by Legendre-symbol enumeration independently check H=trace mod p on all 12,288 classes. All necessary seed classes and twists are included before any depth comparison.

| Minimum seed distance | Newly reached F_p classes, summed over tested primes | New j-values, summed over tested primes |
| --- | ---: | ---: |
| 0 | 242 | 48 |
| 1 | 96 | 48 |
| 2 | 84 | 42 |
| 3 | 64 | 32 |
| 4 | 32 | 16 |

These totals are counts across different finite fields, not distinct characteristic-zero families or disjoint statistical trials. The 514 retained directed edge checks and 12,974 coefficient-model checks overlap these class counts and should not be added together.

Depth three produces new j-values at p=73,89,97,113,193,233,241. Depth four produces new j-values at p=193,241. Every new class after depth zero in this tested interval also has a j-value absent from all smaller depths. There is no observed additional old-j twist class here, but the stronger F_p orbit computation was necessary to determine that fact.

At p=73 the depth-three certificate is

\[
(0,7)\xrightarrow{42}(39,8)\xrightarrow{54}(50,22)\xrightarrow{1}(4,16).
\]

Its endpoint has H=10, beta=4 and j=20. This j does not occur anywhere in the complete depth-zero, one or two seeded closure at p=73. The target-to-easy normalized certificate has kernels (71,6,43), endpoint (0,7), and

\[
\beta/H=71/2+6/4+43/8=15\pmod{73};\qquad 15\cdot10=4.
\]

Thus this is a genuine depth-three class addition, not a dual return, alternate normalization, or previously covered twist. The target's canonical F_p class is (1,2), reached by square x-scale d=37; its canonical beta is 37*4=2, while H remains 10.

At p=193 the depth-four certificate is

\[
(0,11)\xrightarrow{47}(61,49)\xrightarrow{12}(105,132)
\xrightarrow{118}(125,155)\xrightarrow{56}(131,85).
\]

Its endpoint has H=191, beta=81 and j=61, absent every seeded depth through three at that prime. The inverse normalized kernels are (81,21,2,160), the easy endpoint is (0,74), and the beta/H multiplier is 56. Thus 56*191=81 modulo193. Its canonical F_p class is (1,25), with recorded square scale118 and canonical beta101.

The general reverse-certificate rule used here is explicit. If the forward roots are q_0,...,q_(m-1), the inverse normalized roots are

\[
r_i=-2\,4^i q_{m-1-i},\quad 0<=i<m,
\]

and the endpoint is the easy seed scaled by d=4^m. The inverse beta multiplier equals the forward slope obtained by repeatedly applying c'=2c-q. No division by H is performed by the certificate validator.

## A real obstruction: matching an easy trace is insufficient

At p=13 consider E:y²=x³+x+1. It is ordinary, has exact trace -4, H=9, beta=8, and a rational order-two kernel with q=7. The easy curve y²=x³+7x has the same exact trace -4. Nevertheless the entire rational degree-two component of E consists of only two F_p isomorphism classes:

\[
(1,1)\xrightarrow{7}(2,3)\xrightarrow{12}(3,12)\simeq_{F_{13}}(1,1).
\]

Each displayed model has only the displayed rational root. The second root is the immediate dual, and the terminal model is the d=4 square scaling of the input. Neither class is an easy seed. Therefore even an exact easy-family trace match plus rational two-torsion cannot serve as a seeded recognition certificate. This failure is a genuine component obstruction rather than an insufficient search depth.

Across the tested interval, 780 ordinary classes have the same exact trace as some permitted easy seed but lie outside all rational degree-two seeded components. Of these, 496 have at least one rational two-torsion root, verified by complete root scans, and therefore fall directly within the branch-root setting. The fully exhausted finite graph proves these misses for the individual listed primes. It does not prohibit odd-degree isogenies or other recovery mechanisms.

## Saturation and boundaries of the finding

Full finite-graph exhaustion adds no classes beyond minimum depth four at these fifty-one primes. The seeded component radius is three at p=73,89,97,113,233 and four at p=193,241; the other tested primes have radius at most two. This is an exact finite enumeration statement, not a uniform bound on seeded degree-two depth as p grows. At primes p=11 mod12 neither retained ordinary easy family is available, and this construction has no seeds.

The audit validates genuine depth-three and depth-four additions and eliminates the failed strategy of counting exact model pairs or root choices as new classes. A theoretical parameter classification of all higher-depth characteristic-zero families remains open in this branch. The parent recognition branch is responsible for direct depth-two parameter tests and their small-characteristic collisions; this audit supplies independent finite coverage and counterexamples for the higher-depth decision.

Given a verified path of length m and a certified exact trace, transport and reconstruction cost O(m) field operations. The existing normalized cubic relation K=(beta-(b/3)H)/a still costs O(1), and the retained supplied-root branch evaluation costs O(1) after preparation. Obtaining the exact trace, finding the path, extracting roots, maintaining coordinate scales, and converting the original cubic are preparation costs. No benchmark or production SEA implementation is supplied here, and no arbitrary weighted-sum boundary coefficient is inferred from these class counts.

## Reproduction and current status

Run `python audit_depth_three.py` from this directory with Python3.12 and the standard library. `graph_summary.csv` reports new minimum-depth classes and j-values; `edge_validation.csv` records exact coefficient transport and square scaling; `all_isomorphism_classes.csv` gives every F_p class with exact trace, Cartier coefficients and both bounded and saturated minimum depths; `depth_three_four_certificates.csv` retains every new depth-three and depth-four path; `saturated_closure_summary.csv` records full finite reachability and maximum seed distance. `validation.json` retains the representative certificates, counterexample, environment, source hash, prime interval and validation-only root method. Source and output hashes are recorded separately.

All checks passed. The algebraic normalization argument is stated explicitly, while the coverage findings are finite computational results. Human review of the proof and implementation remains appropriate. No novelty assertion or broad lower-bound claim is made.
