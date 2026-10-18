"""Connect retained fast third-point prefixes to the boundary framework.

Python standard library only. Ordinary thirds reuse the trace boundary when
available. Rounded thirds retain a separate factorial boundary acquisition.
"""
from __future__ import annotations

import argparse
import json
from time import perf_counter

from boundary_framework import (
    BoundaryError, BoundaryEvaluator, BoundaryRequest, ReductionPlan,
    UnsupportedPrefixError, complete_sum, is_prime64, __version__,
)
from retained_cm.ordinary_third import ThirdPointEvaluator
from retained_cm.hyperelliptic_prefix import prefixes


class ThirdPointPrefixProvider:
    """A prepared provider; supports exactly one family/index at its prime.

    Miller work is rerun on every prefix call. No complete-answer cache is
    used, so a warm-session result measures arithmetic, not an answer lookup.
    """
    assurance = "retained_project_theorem_and_exact_code; unrefereed; independently_tested"

    def __init__(self, p: int):
        start = perf_counter()
        if not __debug__:
            raise BoundaryError("retained prefix kernels require assertion checks; run without -O")
        if type(p) is not int or p < 7 or not is_prime64(p):
            raise BoundaryError("require an odd prime 7 <= p < 2**64")
        self.p = p
        self.native = None
        self.last_metadata = None
        if p % 3 == 1:
            self.family, self.L = "ordinary_third", (p-1)//3
            self.name = "retained_ordinary_third_miller"
            try:
                self.native = ThirdPointEvaluator(p)
            except (ArithmeticError, AssertionError, ValueError) as exc:
                raise BoundaryError(f"ordinary-third preparation failed: {exc}") from exc
            self.preparation = {"trace": self.native.trace,
                                "trace_source": self.native.trace_source,
                                **self.native.preparation}
        elif p % 3 == 2 and p >= 11:
            self.family, self.L = "rounded_third", (p+1)//3
            self.name = "retained_genus_one_cantor_miller"
            self.preparation = {"annihilator": p+1, "trace_acquisition": "not_required"}
        else:
            raise BoundaryError("no supported third family at this prime")
        self.setup_seconds = perf_counter() - start

    def supports(self, p: int, L: int) -> bool:
        return type(p) is int and type(L) is int and (p,L) == (self.p,self.L)

    def prefix(self, p: int, L: int) -> int:
        if not self.supports(p,L):
            raise UnsupportedPrefixError("retained third provider supports only its prepared prime/index")
        try:
            if self.native is not None:
                self.last_metadata = self.native.evaluate()
                return self.last_metadata["B"]
            self.last_metadata = prefixes(p, 3, all_prefixes=True)
            if self.last_metadata["indices"] != [L]:
                raise BoundaryError("retained rounded prefix returned an unexpected index")
            return self.last_metadata["B"][0]
        except (ArithmeticError, AssertionError, ValueError) as exc:
            raise BoundaryError(f"retained prefix evaluation failed: {exc}") from exc


class ThirdPointSession:
    """Prepare one third-family prime and provide complete U_p(L) evaluations.

    cold_total_seconds charges preparation to every result for comparison.
    warm_total_seconds measures only that call after session construction.
    Neither total includes imports, serialization, or prime selection.
    """

    def __init__(self, p: int, *, direct_cutoff: int = 262144,
                 max_degree: int = 8192, max_direct_terms: int = 2_000_000):
        start = perf_counter()
        self.evaluator = BoundaryEvaluator(direct_cutoff, max_degree, max_direct_terms)
        self.provider = ThirdPointPrefixProvider(p)
        self.p, self.L = p, self.provider.L
        self.family = self.provider.family
        if self.provider.native is not None:
            H = self.provider.native.H
            def trace_boundary(p0, L0):
                if (p0,L0) != (self.p,self.L):
                    return None
                return ReductionPlan(
                    "ordinary_third_trace", "a_L = H = trace mod p",
                    "INTEGRATION.md: ordinary-third trace boundary", (), lambda fs: H)
            self.evaluator.register_reduction("ordinary_third_trace", trace_boundary)
        self.setup_seconds = perf_counter() - start

    def evaluate(self, *, backend: str = "auto", boundary_policy: str = "auto",
                 modulus_power: int = 1, output_mode: str = "full") -> dict:
        start = perf_counter()
        if boundary_policy not in ("auto", "factorial"):
            raise BoundaryError("boundary_policy must be auto or factorial")
        # Request validation occurs inside complete_sum before any prefix call.
        family = ("ordinary_third_trace" if self.provider.native is not None
                  and boundary_policy == "auto" else self.family)
        request = BoundaryRequest(self.p, self.L, family, backend, modulus_power)
        result = complete_sum(request, self.provider, self.evaluator, output_mode=output_mode)
        metadata = self.provider.last_metadata
        if self.provider.native is not None:
            if (output_mode == "full" and result["a_L"] != metadata["a"]) or result["U_p_L"] != metadata["U"]:
                raise BoundaryError("retained ordinary evaluator and integrated result disagree")
            checks = {"retained_boundary_matches": True if output_mode == "full" else None,
                      "retained_complete_sum_matches": True}
        else:
            checks = {"retained_boundary_matches": None, "retained_complete_sum_matches": None}
        result.update({"version": __version__, "family": self.family,
                       "boundary_policy": boundary_policy,
                       "preparation": self.provider.preparation,
                       "retained_diagnostics": (metadata if output_mode == "full" else
                                                {k:v for k,v in metadata.items() if k not in ("B","a","U","S")}),
                       "retained_consistency_checks": checks,
                       "session_setup_seconds": self.setup_seconds,
                       "warm_total_seconds": perf_counter()-start,
                       "answer_cache_used": False})
        result["cold_total_seconds"] = self.setup_seconds + result["warm_total_seconds"]
        return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", required=True, type=int)
    parser.add_argument("--index", type=int, help="optional; must equal the supported third index")
    parser.add_argument("--backend", choices=("auto","direct","product_tree","bgs"), default="auto")
    parser.add_argument("--boundary-policy", choices=("auto","factorial"), default="auto")
    parser.add_argument("--modulus-power", type=int, default=1)
    parser.add_argument("--max-degree", type=int, default=8192)
    parser.add_argument("--direct-cutoff", type=int, default=262144)
    parser.add_argument("--output-mode", choices=("full", "u_only"), default="full")
    args = parser.parse_args(argv)
    try:
        if args.modulus_power != 1:
            raise BoundaryError("integrated thirds support modulo p only")
        session = ThirdPointSession(args.p, direct_cutoff=args.direct_cutoff, max_degree=args.max_degree)
        if args.index is not None and args.index != session.L:
            raise UnsupportedPrefixError("fast prefix is supported only at the third index")
        result = session.evaluate(backend=args.backend, boundary_policy=args.boundary_policy,
                                  modulus_power=args.modulus_power, output_mode=args.output_mode)
        print(json.dumps(result, indent=2))
        return 0
    except BoundaryError as exc:
        print(json.dumps({"error":str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
