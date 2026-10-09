# Questions for independent human review

The intended contribution is a modest computational specialization using classical isogeny, Cartier and CM machinery. The complete proofs and evidence should be assessed independently of their AI provenance or numerical agreement.

| Review target | Concrete question |
|---|---|
| Branch reduction | Does the global exact subtraction give the displayed T formula with the correct coefficient cutoff, signs and normalization? |
| Rooted transport | Are the map, scale +1, exact correction and Cartier naturality valid in the stated characteristic range, including both poles? |
| Closure evidence | The original closure validator was not retained; is the replacement in research/isogeny_closure_20261006/replacement_validation_20261009/ an adequate substitute for the documented scope? |
| Depth-two completeness | Does the root case split exhaust all rational paths from the stated seeds after removing dual scaling? |
| Recognition and twists | Do parameter extraction, prime congruences and exact norms exclude every admissible denominator failure and collision? Are base-field twists kept distinct? |
| Depth-three family | Do the three-step constants, reverse chain, relative norms and exact integer collision certificates establish soundness and completeness for precisely the claimed family? |
| CM trace candidates | Does the conductor-eight volcano argument justify 4p=t0²+192f² for every accepted model, including the special j=0 surface and twists? |
| Trace-sign bound | Is the proper-subgroup argument valid, do the eight p=97 witnesses cover the finite exception, and does the actual raw-x sampler have success at least 1/5? |
| Costs | Are prime validation, random sampling, square roots, Cornacchia, reconstruction and capped inconclusive outputs charged consistently? |
| Prior art | Is explicit recognition plus coefficient recovery already stated or immediate from prior work? What, if anything, is a useful original algorithmic contribution? |
| Scope | Are the deferred chain, generic/supersingular K, all stopping indices and Witt correction visibly unresolved? |
| Rounded third point | Do Theorem R, the p=17 exception and the equivalence in Rounded_Third_Boundary_Note_20261009.md hold? Are the Γ_p(1/3) step and the Gross–Koblitz assessment correct? Do Coleman (1990) or Ogus (1990) already identify the supersingular second-kind coefficient? |

Retained CSVs and source hashes support reproduction; they are not a substitute for these mathematical checks. Historical checks from the external AI worker and later checks using separate arithmetic code are identified as such, not represented as independent human refereeing. No timing comparison accompanies this release. Reviewers can open a GitHub issue for each question, quoting the file and equation concerned.
