"""A minimal strict-prefix adapter; replace the callback with your real engine."""
from boundary_framework import BoundaryRequest, complete_sum


class CartierMillerAdapter:
    name = "external_cartier_miller_callback"
    assurance = "external_engine_responsibility"

    def __init__(self, supports_callback, strict_prefix_callback):
        self._supports = supports_callback
        self._prefix = strict_prefix_callback

    def supports(self, p, L):
        return bool(self._supports(p, L))

    def prefix(self, p, L):
        return self._prefix(p, L)


if __name__ == "__main__":
    # Known supplied regression value only. This is not a fast CM evaluator.
    provider = CartierMillerAdapter(lambda p,L: (p,L) == (11,4), lambda p,L: 8)
    result = complete_sum(BoundaryRequest(11,4), provider)
    print({key:result[key] for key in ("p", "L", "B_L", "a_L", "U_p_L")})
