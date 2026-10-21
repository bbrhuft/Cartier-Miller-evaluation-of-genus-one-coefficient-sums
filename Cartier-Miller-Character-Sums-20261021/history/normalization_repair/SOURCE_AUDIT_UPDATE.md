# Primary-source update, 21 October 2026

This supplements, rather than overwrites, Opus's SOURCE_LEDGER.md. A successful search is not recorded as a body read. The historical search remains incomplete where subscription access prevented reading. Paper bytes obtained locally are hashed in results/source_file_hashes.json; the accompanying package does not redistribute third-party papers or OCR transcriptions.

| Source | Material actually read in this follow-up | Consequence |
|---|---|---|
| Harvey (2007), supplied arXiv math/0610973v2 | Section 6, Theorems 9 and 10 and the proof of Theorem 10, printed pp. 9–11; introduction and relation to BGS | The interval-product comparator has a directly verified theorem-level foundation. It does not state the weighted-character-sum adapter. |
| Miller (2004) | Publisher PDF, Section 4.1, printed pp. 239–241, divisor functions and recurrence (5)–(8), binary/addition-chain construction; Proposition 4 on p. 242 | The general Miller function and short evaluation circuit are classical. The local differential coefficient in this repair is independently derived with its own explicit uniformizer. |
| Galbraith (2012), author-hosted extended version 2.0 | Chapter 26, Section 26.4.1, printed pp. 584–585, Lemmas 26.4.3 and 26.4.5 and the following computational paragraph | Explicitly describes the p-torsion differential homomorphism and obtaining its desired local coefficient using Miller/power-series arithmetic, including Rück's formulation. This is stronger support for the exceptional computational antecedent than an abstract-only attribution. |
| Cassels (1971) | Institute-hosted scanned PDF; OCR of article plus visual inspection of pp. 40–41, 48–51; targeted review of Sections 1, 5–7 and the corrigendum on p. 51 | Equation (1.5) supplies the high-block Artin–Schreier construction with Cassels's sign/differential conventions. Sections 5–6 develop its quasi-period analogy. Theorem 2 concerns identifying p-division points in a lifting setting and is qualified by the corrigendum. The targeted passages do not state the general-trace Miller evaluator (9). |
| Voloch (1997) | Journal PDF, pp. 2–4, polynomial block, characteristic-p zeta definition, Propositions 1–3, and conventions | A close structural antecedent. The repaired normalization proof does not depend on assigning a sign to the printed quasi-period/logarithmic-differential sentence. |
| Schoof (1995) | Numdam body, introduction pp. 219–221, Frobenius relation p. 225, Section 5 pp. 233–235, targeted trace-preparation discussion | Confirms separation of point counting from the query and the Frobenius characteristic relation used in the proof. The introduction states O(log^8 p) for its deterministic algorithm. This is a historical complexity statement in that paper, not a newly measured trace backend. |
| Gunji (1976) | Publisher metadata/reference page only; direct PDF attempt did not supply a PDF | Full text remains unread. Publication metadata confirms pp. 148–158 and DOI 10.1007/BF01224654. No positive or negative assertion about the target algorithm is inferred from its title or citations. |
| Blake, Seroussi, and Smart (1999), Chapter V | Publisher contents/access page only | Chapter V is pp. 79–100. Full text remains unread; subscription access is required on the available publisher route. Galbraith's accessible treatment is additional evidence, not a substitute for claiming this chapter was checked. |
| Semaev (1998), Rück (1999) | Renewed AMS PDF attempts failed; alternative indexed copies were found, but full body retrieval failed in this follow-up | Opus's previous Semaev reading is inherited, not relabelled as independently reread here. Rück remains a direct-body gap. Galbraith explicitly explains the relevant p-torsion construction and coefficient extraction. |

## Harvey's theorem, matched precisely to the coefficient adapter

Harvey works over a commutative ring R, counts ring operations, and lets M(T) be an m by m matrix linear in T. For disjoint ordered intervals 0<=K1<L1<=K2<L2<=...<=Kr<Lr<=K, put s=floor(log_4 K). Theorem 10 assumes that 2,...,2^s+1 are units, that the inverse of the interpolation product D(1,2^s,2^s) is known, and that r<K^(1/2-epsilon) for a fixed epsilon in (0,1/2). It computes the interval products in

\[
O\left(\mathsf{MM}(m)\sqrt K+m^2\mathsf M(\sqrt K)\right)
\]

ring operations. The product order in the statement is M(L)...M(K+1). A software kernel choosing the opposite order must transpose/reverse its interface consistently. Matrix factors need not be invertible.

For the selected coefficient in the audit, h=(p-1)/2, G_a(z)=z^D f(a+1/z), and N=Dh-p. The identity H(a)=[z^N]G_a(z)^h and the differential recurrence are proved in Opus's report. Clearing denominators by k!G_a(0)^k gives a constant-size matrix linear in k. Here N=(p-3)/2 or p-2, so N<p, and the optional next coefficient has index N+1<p. These facts keep the factorial denominators nonzero; G_a(0) is the nonzero leading coefficient of f, including at a branch pole.

Use Theorem 10 for one interval, with K=N or N+1; handle K<=1 directly. Since 2^s+1<p in the remaining prime-field cases, Harvey's sufficient unit condition holds. The inverse D can be acquired explicitly from its defining interpolation factors, within the soft-square-root budget; its acquisition is not free preprocessing. The scalar denominator product is a second one-dimensional interval product. For fixed D this supplies soft-O(sqrt p) field operations without trace preparation. Nothing in the theorem alone supplies the character-sum conversion or an O(log p) query.

The printed v2 paper explicitly identifies its Theorem 9 with BGS's published Theorem 15. Opus's BGS author-preprint uses Theorem 14 for the corresponding result; this resolves the numbering issue as a version difference rather than an additional theorem. The numerical comparator is still a particular implementation of this machinery, not a universal speed baseline.

## Publication priority after these checks

The p-torsion local-coefficient calculation has explicit classical computational antecedents. The high polynomial block also has strong classical antecedents. The present audit derives the complete general-trace weighted-sum evaluator by combining classical facts, but no source read here was located that explicitly states that evaluator with its adapters and cost. This is a search result, not proof that no such source exists. Conversely, the existence of a short derivation from classical facts is not a publication-priority proof against the present project.

The inaccessible Gunji and Blake–Seroussi–Smart texts, and Rück's full body, prevent describing the remaining source audit as complete. No access restriction was bypassed, and no manuscript novelty claim was substantially narrowed on the strength of unread sources.

## References and access routes

Harvey, D. (2007). Kedlaya's algorithm in larger characteristic. *International Mathematics Research Notices, 2007*, rnm095. https://doi.org/10.1093/imrn/rnm095. Supplied preprint: https://arxiv.org/abs/math/0610973v2.

Miller, V. S. (2004). The Weil pairing, and its efficient calculation. *Journal of Cryptology, 17*, 235–261. https://doi.org/10.1007/s00145-004-0315-8. Body read at https://link.springer.com/content/pdf/10.1007/s00145-004-0315-8.pdf.

Galbraith, S. D. (2012). *Mathematics of public key cryptography*. Cambridge University Press. Extended author version 2.0, Chapter 26: https://www.math.auckland.ac.nz/~sgal018/crypto-book/ch26.pdf.

Cassels, J. W. S. (1971). Some elliptic function identities. *Acta Arithmetica, 18*, 37–52. https://doi.org/10.4064/aa-18-1-37-52. Institute scan: https://matwbn.icm.edu.pl/ksiazki/aa/aa18/aa1816.pdf.

Voloch, J. F. (1997). An analogue of the Weierstrass zeta-function in characteristic p. *Acta Arithmetica, 79*, 1–6. https://doi.org/10.4064/aa-79-1-1-6. Journal scan read at https://pdfs.semanticscholar.org/1021/c71f3f49278218ba383a442497768d3eafff.pdf.

Schoof, R. (1995). Counting points on elliptic curves over finite fields. *Journal de Theorie des Nombres de Bordeaux, 7*, 219–254. https://doi.org/10.5802/jtnb.142. https://www.numdam.org/article/JTNB_1995__7_1_219_0.pdf.

Gunji, H. (1976). The Hasse invariant and p-division points of an elliptic curve. *Archiv der Mathematik, 27*, 148–158. https://doi.org/10.1007/BF01224654. Metadata only in this follow-up.

Blake, I., Seroussi, G., & Smart, N. (1999). *Elliptic curves in cryptography*. Cambridge University Press. Chapter V, pp. 79–100. https://doi.org/10.1017/CBO9781107360211. Contents/access only in this follow-up.

Semaev, I. A. (1998). Evaluation of discrete logarithms in a group of p-torsion points of an elliptic curve in characteristic p. *Mathematics of Computation, 67*, 353–356. https://doi.org/10.1090/S0025-5718-98-00887-4. Direct reread blocked in this follow-up.

Rück, H.-G. (1999). On the discrete logarithm in the divisor class group of curves. *Mathematics of Computation, 68*, 805–806. https://doi.org/10.1090/S0025-5718-99-01043-1. Direct reread blocked in this follow-up.
