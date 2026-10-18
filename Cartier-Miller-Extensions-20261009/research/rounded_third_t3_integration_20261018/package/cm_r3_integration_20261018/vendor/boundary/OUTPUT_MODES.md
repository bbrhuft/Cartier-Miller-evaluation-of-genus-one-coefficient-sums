# Explicit output requirements and boundary acquisition

Version 0.4 adds `output_mode="full"` (the default) and `output_mode="u_only"` to the complete-sum services. The numerical boundary service remains a service that computes a boundary. This is an interface/engineering refinement of the existing identity, not new boundary arithmetic.

## Mathematical reason for skipping

The retained mod-p identity is

$$U_p(n)=4B_n-c_n a_n,\qquad c_n=2n(2n+5)\pmod p.$$

If c_n = 0, computing U requires B_n but does not require acquiring a_n. This statement says nothing about a_n being zero. For example a_6 = 10 at p = 17 and a_12 = 13 at p = 29; these are nonzero values which full-output mode must still return.

Substitution classifies the current special-family exceptions completely:

| Supported point | Multiplier modulo p | Eligible zero case |
|---|---|---|
| Ordinary third n = (p−1)/3 | −26/9 | p = 13 |
| Rounded third n = (p+1)/3 | 34/9 | p = 17 |
| First fifth n = (p+1)/5 | 54/25 | None in p ≥ 19 |
| Second fifth n = 2(p+1)/5 | 116/25 | p = 29 |

The denominators are units in the respective family domains. In the general boundary domain 0 ≤ n < p, the zero condition is n = 0 or 2n+5 = 0 modulo p. The complete-sum service still requires a correctly supported prefix provider. No fast arbitrary-index prefix is inferred.

These family exceptions occur at small primes. This refinement should not be described as a broad speedup at large third/fifth primes. The ordinary default already acquires a from its trace data without a factorial; its p = 13 factorial skip is relevant only when the independent factorial route was explicitly selected. The retained ordinary prefix routine still computes its own native scalar diagnostics internally. The new mode eliminates separate boundary acquisition, not every internal occurrence of the same scalar.

## Output and validation contract

Full-output mode returns the same mathematical values as earlier versions, including B and a when the multiplier is zero. It remains the default in all CLIs and Python calls. Additional metadata fields are additive; fifth full-output rows retain their existing keys and values.

U-only mode returns U while the top-level B_L and a_L fields (or their fifth-row counterparts) are null. The boundary value is also redacted from the boundary-result summary. `boundary_status` is `skipped_zero_multiplier` if no separate boundary was needed, otherwise `computed`. A computed-but-unreturned boundary and a skipped boundary are distinct. Acquisition metadata such as interval/factorial calls and trace preparation remains available for audit. Native prefix value arrays and their a/U diagnostics are omitted from the retained-prefix diagnostic summary in this output mode.

The ordinary/rounded session uses the common complete_sum contract. It performs prime, index, family, backend and precision validation even when the multiplier is zero, then still checks prefix support and its returned residue. A skipped boundary bypasses the acquisition work limit because no acquisition is requested, but invalid configuration/options are not accepted. The zero acquisition time in the skipped summary denotes no acquisition; request validation and prefix computation remain included in overall timing.

The fifth session validates the full requested index sequence first, then acquires only nonzero-multiplier boundaries. It preserves order and duplicates and shares the denominator across remaining boundaries. At p = 29, `[12]` uses zero products, `[6,12]` uses two and `[12,6,12]` also uses two. Full-output requests use two products for `[12]` and three for the pair. An empty request does no prefix or interval work under either mode.

The prefix arithmetic is not replaced with a direct-sum fallback. Every nonempty fifth request still executes the retained genus-two all-prefix pass once. Third sessions still execute their existing retained routine. No persistent answer cache is added.

## Usage

```console
python integrated_thirds.py --p 17 --output-mode u_only
python integrated_fifths.py --p 29 --which second --output-mode u_only
python integrated_fifths.py --p 29 --output-mode u_only
```

```python
from integrated_fifths import FifthPointSession

session = FifthPointSession(29)
result = session.evaluate([12], output_mode="u_only")
assert result["outputs"][0]["U_p_L"] == 10
assert result["outputs"][0]["a_L"] is None
assert result["boundary_details"]["interval_calls"] == []
```

The standalone `boundary_framework.py` CLI accepts the same mode only with `--reference-prefix` or `--prefix`, since a boundary alone cannot determine U. The user-supplied prefix remains explicitly labeled as not independently verified.

## Verification and timing interpretation

The focused tests compare U-only results against the original t recurrence, check full/U-only agreement across bounded prime ranges, and directly intercept backend calls to prove acquisition is skipped. They also check zero acquisition budgets, duplicates, empty requests and invalid prime/family/precision/backend/provider cases. The existing full-output suite continues to run.

`benchmark_output_modes.py` compares cold complete-U outputs under both modes and records actual acquisition counts. It includes ordinary p = 13 with a clearly labeled forced-factorial policy, rounded p = 17, the second fifth and paired fifths at p = 29, and large nonzero-multiplier controls. Tiny-case wall-time ratios are not a useful performance claim; the acquisition-count changes and contract correctness are the substantive results. Preparation is included, and no supplied-prefix preprocessing or hidden answer cache is used in these benchmarks.


## Many-prime forest in version 0.7

The new many-prime forest computes B and a jointly in one integer recurrence. Its U-only rows hide B/a and say computed_jointly; they do not claim separate acquisition skipping. The independent many-prime route retains the original native-service skipping rules. MANY_PRIMES.md defines this separate output contract. Existing single-prime output contracts are unchanged.
