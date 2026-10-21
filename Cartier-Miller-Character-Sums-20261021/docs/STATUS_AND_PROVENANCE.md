# Status and provenance at handover

21 October 2026. The hierarchy below resolves conflicting status statements in preserved earlier reports. Their original text and frozen code have not been rewritten to match later findings.

| Material | Status |
|---|---|
| proofs/UNIFORM_ORDER_PROOF.md | Current uniform scalar identity and nonbranch adapter, valid for p>=5 and all traces |
| src/uniform_order.py and src/FREEZE.json | Current scalar implementation; the original three-file freeze is unchanged |
| src/weighted_sums.py | New packaging adapter for the already proved common-domain formulas; correctness checked, not benchmarked |
| proofs/FOUNDATION_PROOFS.md | Detailed retained proofs; its preceding case-split algorithm and p=5 fallback are superseded |
| proofs/SOURCE_LEDGER_FINAL.md | Final direct-source check for the four texts supplied by the user; closes earlier access gaps |
| history/normalization_repair/SOURCE_AUDIT_UPDATE.md | Earlier source ledger; unread Gunji/Rück/book status is obsolete and superseded by the final ledger |
| historical_benchmark/REPORT.md and EXECUTIVE_REPORT.md | Preserved earlier interpretations and measured results; broad novelty recommendations are qualified by the final source check and current paper |
| historical_benchmark/code/source_audit/voloch_zeta_route.py | Earlier p-inverse route, globally documented for p>=7; not the current API |
| historical_benchmark/inherited/character_sums/src/cmcs.py | The older frozen application framework actually measured in the main comparisons |
| manuscript_reference/Cartier_Miller_Paper_Updated_20261021.* | Available complete paper snapshot, not a command to overwrite any newer user draft |
| manuscript_reference/Relation_to_Prior_Work_20261021.* | Later replacement section, supplied separately; it is not yet inserted into the complete snapshot |

## Numerical records

The uniform core's development record has 14,037 direct character-sum queries and 47,712 additional cubic scalar-identity point checks. Its confirmation record has 5,400 direct queries on nine primes disjoint from that verifier's development set. The code freeze is e5bc223964ef30239410a64cd1b7cc4c1b828aa993a30a8fcdfcae9c8fb7b373. Its files are unchanged, including the prior evaluator used as a comparison and helper implementation.

The new weighted adapter's development and confirmation selections each have 120 cubic/quartic models, 960 weighted queries and 960 cached coefficient-change queries. Across both selections this gives 3,840 weighted queries and 11,520 output-residue comparisons against direct enumeration. Twelve distinct malformed or unsupported inputs are rejected in each mode; those repeated checks should not be added as distinct invalid inputs. The selections also check the earlier extra-exclusion counterexample and the p=5 order-2p example. Confirmation primes are disjoint from this adapter's development set; they are not claimed to be disjoint from the entire project's historical prime sets. The adapter has its own separate source commitment in verification/ADAPTER_FREEZE.json.

The historical comparator freeze has digest 09202ac1edab4f3eadfa68a8c50e0d77c695328891e889c8a744fc8b28c28ac0 and the inherited application freeze has digest 4302b56426a6160fbc5027659632bac7ad6cc0ab755c5fcb00d8c9502aa99bd3. Both frozen file sets are retained, including the small original Linux native-library snapshot needed to verify the first digest. It is a historical binary, not a portable runtime dependency of the current API.

All archived timing samples, raw per-job outputs, reconstructed case pools, validation reports, environment metadata and analysis are retained under historical_benchmark/results/. The prior quick smoke campaign, incomplete hidden temporary file, third-party kernel-source copies and caches are omitted. No reported benchmark result depends on the omitted quick campaign. The original report's top-level SHA256SUMS manifest is not copied because this is a selected, newly organized handover; MANIFEST.json authenticates this package and the original implementation freezes still verify.

The full paper snapshot has SHA-256 7caab564172f979502216e908211f1ad4bb8b4efe373db98bc5f77b22fae70c6. The manuscript revision keeps the original main theorem's p>=7 statement and separately proves the p>=5 nonbranch character-sum extension. The earlier p=5 API failure was outside the older report's p>=7 theorem range; it is not a counterexample to that theorem. The current uniform engine removes the p-inverse obstruction altogether.

## Claims to retain

The current acceleration is an O(log p) field-operation query after a separately supplied exact trace. Its classical bit bound is O((log p)^3). Multiple supplied nonbranch simple poles use the proved corrections. All traces, zero coordinates, arbitrary original constant term, small p=5 and rational two-torsion model images are covered within that contract. Zero-residue branch exclusions are permitted by the new adapter.

The local-coefficient cocycle, Miller circuit and order-p logarithmic transfer are classical. The targeted primary-source work does not establish historical priority for the complete scalar formula or its adapters. No new general elliptic-curve discrete-logarithm attack is claimed. The current scalar engine and new adapter have correctness evidence, while the timing claims belong to the named older implementations. Higher-order poles, polynomial parts and active branch poles in historical experiments do not inherit the logarithmic query bound automatically.

## Manuscript handling

Use any newer draft supplied by David as authoritative. Compare it with the snapshot instead of replacing it. If the later prior-work section has not yet been merged, replace the earlier heading and prose, retain Notation/Table 1, retain finite-logarithm equation (6), and add Miller's 1986 bibliography entry. The replacement distinguishes the 1986 manuscript from the 2004 exposition and credits the composition identities used by the new proof. Its comments and Word bibliography note explain this insertion. No manuscript is modified by verification commands in this supplement.
