# Direct examination of the four requested sources

21 October 2026. The supplied PDFs close the four specific access gaps identified in the previous request. This is a targeted comparison, not a claim that the historical literature has been exhaustively searched. No web abstract or secondary description substitutes for a body read in this ledger.

| Source and supplied file | Directly examined material | Findings relevant to the manuscript |
|---|---|---|
| Gunji (1976), BF01224654.pdf, 11 pages | Article pp. 148–158; explicit visual verification of pp. 152–154 to resolve damaged extraction | Ordinary curves over an algebraically closed field, not just anomalous curves. Functions with divisor p(P)-p(O), logarithmic differentials, Cartier eigenvalues, differential-operator eigenvectors, and explicit p-division coordinates are classical here. No base-field general-trace high-block evaluator with a logarithmic-cost claim was located. |
| Rück (1999), S0025-5718-99-01043-1.pdf, 2 pages | Entire article pp. 805–806 | Direct, explicit local-coefficient cocycle and repeated-doubling computation. His stated discrete-logarithm theorem is on p-primary divisor classes, with O(n² log p) field operations for p^n torsion and fixed genus. The coefficient machinery is an important classical antecedent to our implementation. |
| Semaev (1998), S0025-5718-98-00887-4.pdf, 4 pages | Entire article pp. 353–356, especially Lemmas 1–3 and equations (1)–(2) | An order-p subgroup, a logarithmic-derivative embedding, and differentiated addition-chain evaluation in O(log p) field operations. The auxiliary 2-torsion point needs extension degree at most 3. The stated output is the p-torsion transfer, rather than our general-trace character-sum scalar. |
| Blake, Seroussi, and Smart (1999), supplied compressed book, 218 PDF pages | Chapter V: targeted Sections V.2 and V.3; anomalous attack pp. 88–91 (PDF pp. 102–105). Search of extracted text for Cartier, logarithmic derivatives, Gunji, Semaev, and Voloch | V.2 treats multiplicative pairing/descent with a torsion order coprime to the field characteristic. V.3 explains Smart/Satoh–Araki p-adic lifting for trace-one curves and mentions Semaev's related order-p attack. Its group/order and scalar-multiplication complexity is classical. No complete general-trace weighted-sum formula was located in these passages. |

## Gunji: exact overlap and limitations of the comparison

Equation (2.4) fixes functions z_i with divisor p(P_i)-p(O). Equations (2.8)–(2.10), pp. 151–152, identify their logarithmic differentials and eigenvalues for D=y d/dx. Lemma 2.11 and its corollary give the Cartier action and c_i^(p-1)=A. Theorem 2.1 gives the characteristic polynomial X^p-A X on L(pO); Theorem 2.2 constructs the functions by differential iterates. Theorems 3.2 and 4 express p-division coordinates using polynomial coefficients and determinants.

The differential in equation (2.9) is dx/y. Our short-model convention is omega=dx/(2y). Therefore the same function's logarithmic scalar is alpha_p(P_i)=2c_i in our convention. This factor must be shown rather than silently identified away.

Gunji's ordinary hypothesis A nonzero does not imply trace one over F_p. His nonzero eigenvalue c, satisfying c^(p-1)=A, need not lie in F_p. Indeed, for A in F_p*, c^p=A c, so its field degree is the multiplicative order of A in F_p*. This last observation is a deduction here. His coordinate construction and its potentially extended-field parameters should not be confused with our trace-supplied rational-point query. His displayed matrices have size proportional to p; the paper does not establish an O(log p) algorithm for our target scalar. This is a statement about what is presented, not a lower bound on every possible implementation.

## Rück: the closest explicit computational antecedent

Page 806 extracts the coefficients of f^(-1) partial_t f up to degree 2g-2, and uses these coefficients to define an additive cocycle extending divisor-class addition. It explicitly allows the differential of the addition function to have a pole at the expansion point. Repeated doubling then obtains the transfer coefficient in O(log p) field operations. In genus one, only the constant coefficient is needed.

This is substantially closer to our differentiated Miller computation than merely a shared use of elliptic curves. The manuscript should attribute this computational device explicitly. Its p-torsion theorem and the general-trace fixed-divisor scalar must nevertheless remain distinct. The extension of the scalar identity to the curve order N is proved in UNIFORM_ORDER_PROOF.md, rather than attributed as an explicit formula in Rück.

## Semaev: verify the stated normalization

Semaev's map is phi(Q)=(f_Q'/f_Q)(R), with prime denoting d/dx, where R lies in the nonzero order-p subgroup. Lemma 2 proves the embedding, and Lemma 3 differentiates the function recurrence. His chosen parameter at infinity is x/y. Our parameter is -x/y, and our invariant differential is dx/(2y). From dlog f_Q=alpha_p(Q) omega, the affine evaluation is phi(Q)=alpha_p(Q)/(2y_R). Thus an infinity coefficient must be compared with its parameter sign stated, while the affine evaluation has the displayed differential conversion.

The normalization and short-chain construction have direct primary support; we no longer need to rely on Opus's report of having read them. This does not identify the ordinary-curve coefficient with an additive discrete-logarithm embedding.

## The book: what was checked

The anomalous section gives the exact-sequence/formal-group description, reduction and p-adic lifts, an elliptic logarithm, the quotient recovering a discrete logarithm, the possible failed-lift case, and an explicit example over F_43. Its neighboring pairing/descent section uses coprime torsion and multiplicative output in an extension. These are relevant attribution and scope checks. The entire book was not audited, and the absence finding is confined to the targeted passages and extracted-text searches.

## Consequence for publication claims

The local-coefficient circuit, its differentiated Miller evaluation, and its additive-cocycle interpretation must be presented as classical. The project's mathematical target is the explicit relation to selected high coefficients and weighted sums, with trace preparation, model changes, normalization, and admissible exclusions charged and proved. A formulation with an unfamiliar name is not evidence of a new algorithm.

The four sources do not settle the publication priority of the full scalar identity or weighted-sum adapter. The appropriate statement is that this comparison derives and validates the identities while attributing the classical construction; it does not establish a first-ever O(log p) elliptic computation. The known access gaps are closed, and a qualified revision can proceed without treating those texts as unread.

## References

Gunji, H. (1976). The Hasse invariant and p-division points of an elliptic curve. *Archiv der Mathematik, 27*, 148–158. https://doi.org/10.1007/BF01224654.

Rück, H.-G. (1999). On the discrete logarithm in the divisor class group of curves. *Mathematics of Computation, 68*(226), 805–806. https://doi.org/10.1090/S0025-5718-99-01043-1.

Semaev, I. A. (1998). Evaluation of discrete logarithms in a group of p-torsion points of an elliptic curve in characteristic p. *Mathematics of Computation, 67*(221), 353–356. https://doi.org/10.1090/S0025-5718-98-00887-4.

Blake, I. F., Seroussi, G., & Smart, N. P. (1999). *Elliptic curves in cryptography*. Cambridge University Press. Chapter V, pp. 79–100; targeted sections as recorded above. https://doi.org/10.1017/CBO9781107360211.
