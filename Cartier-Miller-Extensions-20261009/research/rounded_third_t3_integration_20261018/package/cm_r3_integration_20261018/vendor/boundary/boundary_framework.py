"""Exact, dependency-free Cartier--Miller boundary prototype (Python >= 3.10).

Scope: a_L = binom(2L,L) / 8**L modulo an odd prime p < 2**64,
0 <= L < p. See MATHEMATICS.md for proofs and algorithm limitations.
The bgs backend uses scalar BGS value shifts; product_tree remains available.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from math import isqrt
from time import perf_counter
from typing import Callable, Protocol

__version__ = "1.0.0rc1"


class BoundaryError(ValueError):
    """Invalid or unsupported mathematical request."""


class ResourceLimitError(BoundaryError):
    """A configured work limit would be exceeded."""


class UnsupportedPrefixError(BoundaryError):
    """A prefix provider does not support the requested (p,L)."""


def _integer(x: int, name: str) -> None:
    if type(x) is not int:
        raise BoundaryError(f"{name} must be an integer (not bool or float)")


def is_prime64(n: int) -> bool:
    """Deterministic Miller--Rabin in the explicitly bounded range n < 2**64."""
    _integer(n, "n")
    if n >= 2**64:
        raise BoundaryError("primality validation is restricted to n < 2**64")
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue
        x = pow(base, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _trim(a: list[int]) -> list[int]:
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def _mul(a: list[int], b: list[int], p: int) -> list[int]:
    """Polynomial product in F_p[x], low coefficient first.

    Large products use exact Kronecker packing. The radix exceeds
    min(len(a),len(b))*(p-1)**2, so convolution digits cannot carry.
    """
    if a == [0] or b == [0]:
        return [0]
    size = len(a) + len(b) - 1
    if min(len(a), len(b)) < 16:
        c = [0] * size
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                c[i + j] += x * y
        return _trim([x % p for x in c])
    bound = min(len(a), len(b)) * (p - 1)**2
    width = (bound.bit_length() + 7) // 8
    aa = int.from_bytes(b"".join(x.to_bytes(width, "little") for x in a), "little")
    bb = int.from_bytes(b"".join(x.to_bytes(width, "little") for x in b), "little")
    packed = (aa * bb).to_bytes(size * width, "little")
    return _trim([int.from_bytes(packed[i * width:(i + 1) * width], "little") % p
                  for i in range(size)])


def _inverse_series(f: list[int], n: int, p: int) -> list[int]:
    """Newton inversion modulo x**n; only f[0] must be nonzero."""
    g = [pow(f[0], -1, p)]
    while len(g) < n:
        k = min(2 * len(g), n)
        fg = _mul(f[:k], g, p)[:k]
        fg += [0] * (k - len(fg))
        correction = [(-x) % p for x in fg]
        correction[0] = (correction[0] + 2) % p
        g = _mul(g, correction, p)[:k]
        g += [0] * (k - len(g))
    return g


def _remainder(a: list[int], monic: list[int], p: int) -> list[int]:
    if monic[-1] != 1:
        raise ValueError("internal polynomial divisor must be monic")
    if len(a) < len(monic):
        return a[:]
    if len(monic) == 1:
        return [0]
    degree = len(monic) - 1
    count = len(a) - len(monic) + 1
    if degree < 16 or count < 16:
        r = a[:]
        for k in range(len(r) - 1, degree - 1, -1):
            c = r[k]
            if c:
                for j in range(degree):
                    r[k - degree + j] = (r[k - degree + j] - c * monic[j]) % p
        return _trim(r[:degree])
    inv = _inverse_series(monic[::-1], count, p)
    q = _mul(a[::-1][:count], inv, p)[:count]
    q += [0] * (count - len(q))
    correction = _mul(q[::-1], monic, p)
    return _trim([(a[i] - (correction[i] if i < len(correction) else 0)) % p
                  for i in range(degree)])


def _product_tree(leaves: list[list[int]], p: int) -> list[list[list[int]]]:
    levels = [leaves]
    while len(levels[-1]) > 1:
        row = levels[-1]
        levels.append([_mul(row[i], row[i + 1], p) if i + 1 < len(row) else row[i]
                       for i in range(0, len(row), 2)])
    return levels


def _multipoint(f: list[int], tree: list[list[list[int]]], p: int) -> list[int]:
    rem = [_remainder(f, tree[-1][0], p)]
    for level in range(len(tree) - 2, -1, -1):
        rem = [_remainder(rem[j // 2], node, p)
               for j, node in enumerate(tree[level])]
    return [r[0] for r in rem]


def _batch_inverse_nonzero(values, p):
    """Invert nonzero field elements with one inversion; zero maps to zero."""
    prefixes = []
    product = 1
    for value in values:
        prefixes.append(product)
        if value:
            product = product * value % p
    inverse = pow(product, -1, p)
    result = [0] * len(values)
    for i in range(len(values) - 1, -1, -1):
        if values[i]:
            result[i] = inverse * prefixes[i] % p
            inverse = inverse * values[i] % p
    return result


class _APShiftPlan:
    """From P(0..d) obtain P(alpha..alpha+d), deg(P)<=d<p.

    Known-node collisions are copied explicitly; their reciprocal kernel
    entries are zero placeholders, never inverses of zero.
    """
    def __init__(self, d, alpha, p):
        if type(d) is not int or not 0 <= d < p:
            raise BoundaryError('AP interpolation requires 0 <= degree < p')
        self.d, self.p, self.alpha = d, p, alpha % p
        facts = [1] * (d + 1)
        for j in range(1, d + 1):
            facts[j] = facts[j - 1] * j % p
        invfacts = [1] * (d + 1)
        invfacts[d] = pow(facts[d], -1, p)
        for j in range(d, 0, -1):
            invfacts[j - 1] = invfacts[j] * j % p
        self.weights = [invfacts[j] * invfacts[d - j] *
                        (-1 if (d - j) % 2 else 1) % p for j in range(d + 1)]
        factors = [(self.alpha - d + j) % p for j in range(2 * d + 1)]
        self.kernel = _batch_inverse_nonzero(factors, p)
        # Rolling product Delta(alpha+i) = prod_j(alpha+i-j).
        # Track zeros separately so a window can recover after a zero leaves.
        product, zeros = 1, 0
        for value in factors[:d + 1]:
            if value:
                product = product * value % p
            else:
                zeros += 1
        self.deltas = []
        for i in range(d + 1):
            self.deltas.append(0 if zeros else product)
            if i < d:
                old, new = factors[i], factors[i + d + 1]
                if old:
                    product = product * self.kernel[i] % p
                else:
                    zeros -= 1
                if new:
                    product = product * new % p
                else:
                    zeros += 1

    def apply(self, values):
        d, p = self.d, self.p
        if len(values) != d + 1:
            raise BoundaryError('AP shift sample count must equal degree + 1')
        weighted = [v * w % p for v, w in zip(values, self.weights)]
        convolution = _mul(weighted, self.kernel, p)
        # _mul trims trailing zeros, including the identically zero case.
        convolution += [0] * (3 * d + 1 - len(convolution))
        return [values[t] if (t := (self.alpha + i) % p) <= d
                else self.deltas[i] * convolution[d + i] % p
                for i in range(d + 1)]


def _block_values(start, size, p):
    """F_size(i*size), i=0..size; F_k(X)=prod_{j<k}(X+start+j)."""
    inverse_step = pow(size, -1, p)

    def build(k):
        if k == 1:
            return [start % p, (start + size) % p]
        d = k // 2
        values = build(d)
        extend = _APShiftPlan(d, d + 1, p)
        shifted = _APShiftPlan(d, d * inverse_step % p, p).apply(values)
        left = values + extend.apply(values)
        right = shifted + extend.apply(shifted)
        result = [left[i] * right[i] % p for i in range(k + 1)]
        if k % 2:
            result = [v * (start + 2 * d + i * size) % p
                      for i, v in enumerate(result)]
        return result

    return build(size)


def _bgs_interval_product(p, start, length, max_degree=8192):
    """Return (value, degree, setup_seconds, evaluation_seconds).

    Caller validates p as prime. Domain is a unit interval in 1..p-1.
    Both setup and evaluation are charged; no cross-call cache is used.
    """
    if (type(start) is not int or type(length) is not int or
            start < 1 or length < 0 or start + length > p):
        raise BoundaryError('unit interval requires start >= 1, length >= 0, start+length <= p')
    if type(max_degree) is not int or max_degree < 1:
        raise BoundaryError('max_degree must be a positive integer')
    degree = isqrt(length)
    if degree > max_degree:
        raise ResourceLimitError(f'BGS degree {degree} exceeds limit {max_degree}')
    begin = perf_counter()
    if not length:
        return 1, 0, 0.0, perf_counter() - begin
    # degree < p follows from length < p, so the grid step is a unit.
    values = _block_values(start, degree, p)
    setup = perf_counter() - begin
    begin = perf_counter()
    value = 1
    for block in values[:degree]:
        value = value * block % p
    for j in range(degree * degree, length):
        value = value * (start + j) % p
    return value, degree, setup, perf_counter() - begin


@dataclass(frozen=True)
class FactorialResult:
    n: int
    value: int
    backend: str
    effective_n: int
    reflected: bool
    block_degree: int
    setup_seconds: float
    evaluation_seconds: float


class FactorialBackend(Protocol):
    name: str

    def factorial(self, n: int, p: int) -> FactorialResult: ...


def _factorial_domain(n: int, p: int) -> tuple[int, bool]:
    # Backend protocol expects a prime already checked by BoundaryEvaluator.
    _integer(n, "factorial index")
    if not 0 <= n < p:
        raise BoundaryError("factorial backend requires 0 <= n < p")
    reflected = n > (p - 1) // 2
    return (p - 1 - n if reflected else n), reflected


def _unreflect(value: int, n: int, p: int, reflected: bool) -> int:
    if not reflected:
        return value
    # Wilson: n! * (p-1-n)! = (-1)**(n+1) modulo p.
    sign = -1 if n % 2 == 0 else 1
    return sign * pow(value, -1, p) % p


class DirectFactorialBackend:
    name = "direct"

    def __init__(self, max_terms: int = 2_000_000):
        _integer(max_terms, "max_terms")
        if max_terms < 0:
            raise BoundaryError("max_terms must be nonnegative")
        self.max_terms = max_terms

    def factorial(self, n: int, p: int) -> FactorialResult:
        effective, reflected = _factorial_domain(n, p)
        if effective > self.max_terms:
            raise ResourceLimitError(f"direct factorial needs {effective} terms; limit {self.max_terms}")
        start = perf_counter()
        value = 1
        for j in range(2, effective + 1):
            value = value * j % p
        value = _unreflect(value, n, p, reflected)
        return FactorialResult(n, value, self.name, effective, reflected, 0,
                               0.0, perf_counter() - start)


class ProductTreeFactorialBackend:
    name = "product_tree"

    def __init__(self, max_degree: int = 8192):
        _integer(max_degree, "max_degree")
        if max_degree < 1:
            raise BoundaryError("max_degree must be positive")
        self.max_degree = max_degree

    def factorial(self, n: int, p: int) -> FactorialResult:
        effective, reflected = _factorial_domain(n, p)
        s = isqrt(effective)
        if s > self.max_degree:
            raise ResourceLimitError(f"product-tree degree {s} exceeds limit {self.max_degree}")
        start = perf_counter()
        if effective < 2:
            return FactorialResult(n, _unreflect(1, n, p, reflected), self.name,
                                   effective, reflected, 0, 0.0, perf_counter() - start)
        f = _product_tree([[j % p, 1] for j in range(1, s + 1)], p)[-1][0]
        tree = _product_tree([[(-i * s) % p, 1] for i in range(s)], p)
        setup = perf_counter() - start
        start = perf_counter()
        values = _multipoint(f, tree, p)
        value = 1
        for x in values:
            value = value * x % p
        for j in range(s * s + 1, effective + 1):
            value = value * j % p
        value = _unreflect(value, n, p, reflected)
        return FactorialResult(n, value, self.name, effective, reflected, s,
                               setup, perf_counter() - start)


class BGSFactorialBackend:
    name = "bgs"

    def __init__(self, max_degree: int = 8192):
        _integer(max_degree, "max_degree")
        if max_degree < 1:
            raise BoundaryError("max_degree must be positive")
        self.max_degree = max_degree

    def factorial(self, n: int, p: int) -> FactorialResult:
        effective, reflected = _factorial_domain(n, p)
        value, degree, setup, elapsed = _bgs_interval_product(p, 1, effective, self.max_degree)
        begin = perf_counter()
        value = _unreflect(value, n, p, reflected)
        return FactorialResult(n, value, self.name, effective, reflected, degree,
                               setup, elapsed + perf_counter() - begin)


@dataclass(frozen=True)
class BoundaryRequest:
    p: int
    L: int
    family: str = "auto"
    backend: str = "auto"
    modulus_power: int = 1


@dataclass(frozen=True)
class ReductionPlan:
    name: str
    formula: str
    proof_reference: str
    factorial_indices: tuple[int, ...]
    finish: Callable[[tuple[int, ...]], int]


Reducer = Callable[[int, int], ReductionPlan | None]


def _ordinary_third(p: int, L: int) -> ReductionPlan | None:
    if p >= 7 and p % 3 == 1 and 3 * L == p - 1:
        return ReductionPlan("ordinary_third", "a_L = -(L!)^(-3) mod p",
                             "MATHEMATICS.md: ordinary third", (L,),
                             lambda fs: -pow(fs[0], -3, p) % p)
    return None


def _rounded_third(p: int, L: int) -> ReductionPlan | None:
    if p >= 11 and p % 3 == 2 and 3 * L == p + 1:
        return ReductionPlan("rounded_third", "a_L = (3/2)*((L-1)!)^(-3) mod p",
                             "MATHEMATICS.md: rounded third", (L - 1,),
                             lambda fs: 3 * pow(2, -1, p) * pow(fs[0], -3, p) % p)
    return None


def _generic(p: int, L: int) -> ReductionPlan:
    return ReductionPlan("central_binomial", "a_L = (2L)!/(L!)^2 * 8^(-L) mod p",
                         "definition; unit factorials since 2L < p", (2 * L, L),
                         lambda fs: fs[0] * pow(fs[1], -2, p) * pow(8, -L, p) % p)


@dataclass(frozen=True)
class BoundaryResult:
    request: BoundaryRequest
    value: int
    reduction: str
    formula: str
    proof_reference: str
    factorial_calls: tuple[FactorialResult, ...]
    validation_seconds: float
    reduction_seconds: float
    normalization_seconds: float
    total_seconds: float
    assurance: str = "exact_mod_p_algorithm; finite_validation_is_not_formal_verification"

    def to_dict(self) -> dict:
        return asdict(self)


class BoundaryEvaluator:
    """Registry + dispatcher. A new instance has no cross-request cache."""

    def __init__(self, direct_cutoff: int = 262144, max_degree: int = 8192,
                 max_direct_terms: int = 2_000_000):
        _integer(direct_cutoff, "direct_cutoff")
        if direct_cutoff < 0:
            raise BoundaryError("direct_cutoff must be nonnegative")
        self.direct_cutoff = direct_cutoff
        self.backends: dict[str, FactorialBackend] = {
            "direct": DirectFactorialBackend(max_direct_terms),
            "product_tree": ProductTreeFactorialBackend(max_degree),
            "bgs": BGSFactorialBackend(max_degree),
        }
        self.reducers: dict[str, Reducer] = {
            "ordinary_third": _ordinary_third, "rounded_third": _rounded_third,
        }

    def register_backend(self, name: str, backend: FactorialBackend) -> None:
        if not isinstance(name, str) or not name or name == "auto" or name in self.backends:
            raise BoundaryError("backend name must be new, nonempty, and not auto")
        self.backends[name] = backend

    def register_reduction(self, name: str, reducer: Reducer) -> None:
        if not isinstance(name, str) or not name or name in {"auto", "generic"} or name in self.reducers:
            raise BoundaryError("reduction name must be new and not auto/generic")
        self.reducers[name] = reducer

    def _prepare_plan(self, request: BoundaryRequest) -> tuple[ReductionPlan, float, float]:
        """Validate domain/options and plan reduction without boundary acquisition."""
        start = perf_counter()
        p, L = request.p, request.L
        _integer(p, "p")
        _integer(L, "L")
        _integer(request.modulus_power, "modulus_power")
        if not isinstance(request.family, str) or not isinstance(request.backend, str):
            raise BoundaryError("family and backend must be strings")
        if request.modulus_power != 1:
            raise BoundaryError("this boundary interface supports modulo p only; prime powers require different reductions")
        if p < 3 or p % 2 == 0 or not is_prime64(p):
            raise BoundaryError("p must be an odd prime less than 2**64")
        if not 0 <= L < p:
            raise BoundaryError("index requires 0 <= L < p")
        if request.backend != "auto" and request.backend not in self.backends:
            raise BoundaryError(f"unknown backend: {request.backend}")
        if request.family not in {"auto", "generic"} and request.family not in self.reducers:
            raise BoundaryError(f"unknown family: {request.family}")
        validation = perf_counter() - start
        rstart = perf_counter()
        # An explicitly named family must satisfy its hypotheses, even for trivial values.
        plan = None
        if request.family not in {"auto", "generic"}:
            plan = self.reducers[request.family](p, L)
            if plan is None:
                raise BoundaryError(f"hypotheses fail for family {request.family}")
        if L == 0:
            plan = ReductionPlan("empty_index", "a_0 = 1", "definition", (), lambda fs: 1)
        elif L > (p - 1) // 2:
            plan = ReductionPlan("upper_half_zero", "a_L = 0 mod p", "MATHEMATICS.md: valuation", (), lambda fs: 0)
        elif plan is None:
            if request.family == "auto":
                for reducer in self.reducers.values():
                    plan = reducer(p, L)
                    if plan is not None:
                        break
            if plan is None:
                plan = _generic(p, L)
        reduction_time = perf_counter() - rstart
        return plan, validation, reduction_time

    def evaluate(self, request: BoundaryRequest) -> BoundaryResult:
        start = perf_counter()
        plan, validation, reduction_time = self._prepare_plan(request)
        p = request.p
        calls: list[FactorialResult] = []
        cache: dict[int, int] = {}
        factorials = []
        for n in plan.factorial_indices:
            if n in cache:
                factorials.append(cache[n])
                continue
            backend_name = request.backend
            if backend_name == "auto":
                effective = min(n, p - 1 - n)
                backend_name = "direct" if effective <= self.direct_cutoff else "bgs"
            result = self.backends[backend_name].factorial(n, p)
            if type(result.value) is not int or not 0 < result.value < p:
                raise BoundaryError("factorial backend returned a noncanonical or zero unit")
            cache[n] = result.value
            calls.append(result)
            factorials.append(result.value)
        nstart = perf_counter()
        value = plan.finish(tuple(factorials)) % p
        normalization = perf_counter() - nstart
        return BoundaryResult(request, value, plan.name, plan.formula,
                              plan.proof_reference, tuple(calls), validation,
                              reduction_time, normalization, perf_counter() - start)


class PrefixProvider(Protocol):
    """Adapter contract: return the strict prefix B_L, not an inclusive prefix."""
    name: str
    assurance: str

    def supports(self, p: int, L: int) -> bool: ...

    def prefix(self, p: int, L: int) -> int: ...


class DirectReferencePrefix:
    """O(L) correctness/demo provider; not the fast Cartier--Miller algorithm."""
    name = "direct_reference_prefix"
    assurance = "direct_recurrence_reference"

    def __init__(self, max_terms: int = 2_000_000):
        _integer(max_terms, "max_terms")
        if max_terms < 0:
            raise BoundaryError("max_terms must be nonnegative")
        self.max_terms = max_terms

    def supports(self, p: int, L: int) -> bool:
        return 0 <= L < p and L <= self.max_terms

    def prefix(self, p: int, L: int) -> int:
        if not self.supports(p, L):
            raise UnsupportedPrefixError("reference prefix work limit exceeded")
        a, total = 1, 0
        for i in range(L):
            total = (total + a) % p
            if i + 1 < L:
                a = a * (2 * i + 1) * pow(4 * (i + 1), -1, p) % p
        return total


@dataclass(frozen=True)
class SuppliedPrefix:
    p: int
    L: int
    value: int
    name: str = "caller_supplied_prefix"
    assurance: str = "caller_supplied_value_not_independently_verified"

    def supports(self, p: int, L: int) -> bool:
        return (p, L) == (self.p, self.L)

    def prefix(self, p: int, L: int) -> int:
        if not self.supports(p, L):
            raise UnsupportedPrefixError("supplied prefix belongs to a different (p,L)")
        return self.value


def complete_sum(request: BoundaryRequest, provider: PrefixProvider,
                 evaluator: BoundaryEvaluator | None = None, *, output_mode: str = "full") -> dict:
    """Combine a supported B_L with the retained mod-p project identity.

    Provider correctness is the caller's responsibility. No p**2 transfer and
    no claim of a logarithmic-time prefix unless a real provider supplies it.
    """
    start = perf_counter()
    if output_mode not in ("full", "u_only"):
        raise BoundaryError("output_mode must be full or u_only")
    engine = evaluator or BoundaryEvaluator()
    boundary = None
    # All domain, family, backend and precision checks remain active even if
    # the arithmetic target makes the boundary unnecessary.
    if output_mode == "u_only":
        engine._prepare_plan(request)
    else:
        boundary = engine.evaluate(request)
    p, L = request.p, request.L
    multiplier = 2*L*(2*L+5) % p
    skipped = output_mode == "u_only" and multiplier == 0
    if skipped:
        boundary_value = None
        boundary_data = {"value": None, "reduction": "not_required_zero_multiplier",
                         "factorial_calls": [], "total_seconds": 0.0}
    else:
        if boundary is None:
            boundary = engine.evaluate(request)
        boundary_value = boundary.value
        boundary_data = boundary.to_dict()
        if output_mode == "u_only":
            boundary_data["value"] = None
    if not provider.supports(p, L):
        raise UnsupportedPrefixError(f"prefix provider {provider.name} does not support (p,L)")
    pstart = perf_counter()
    prefix = provider.prefix(p, L)
    _integer(prefix, "prefix")
    if not 0 <= prefix < p:
        raise BoundaryError("prefix provider must return a canonical residue 0 <= B_L < p")
    pseconds = perf_counter() - pstart
    value = (4 * prefix - (0 if skipped else multiplier * boundary_value)) % p
    return {"p": p, "L": L, "B_L": prefix if output_mode == "full" else None,
            "a_L": boundary_value if output_mode == "full" else None, "U_p_L": value,
            "output_mode": output_mode, "boundary_multiplier": multiplier,
            "boundary_status": "skipped_zero_multiplier" if skipped else "computed",
            "prefix_provider": provider.name, "prefix_assurance": provider.assurance,
            "prefix_seconds": pseconds, "boundary": boundary_data,
            "identity": "U_p(L) = 4*B_L - 2*L*(2*L+5)*a_L mod p",
            "total_seconds": perf_counter() - start}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, required=True)
    parser.add_argument("--index", type=int, help="L; inferred when a third family is named")
    parser.add_argument("--family", default="auto", choices=("auto", "generic", "ordinary_third", "rounded_third"))
    parser.add_argument("--backend", default="auto", choices=("auto", "direct", "product_tree", "bgs"))
    parser.add_argument("--modulus-power", type=int, default=1)
    parser.add_argument("--max-degree", type=int, default=8192)
    parser.add_argument("--direct-cutoff", type=int, default=262144)
    parser.add_argument("--output-mode", choices=("full", "u_only"), default="full")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--reference-prefix", action="store_true")
    group.add_argument("--prefix", type=int, help="caller-supplied B_L, reported as unverified input")
    args = parser.parse_args(argv)
    L = args.index
    if L is None:
        if args.family == "ordinary_third":
            L = (args.p - 1) // 3
        elif args.family == "rounded_third":
            L = (args.p + 1) // 3
        else:
            parser.error("--index is required unless a third family is named")
    request = BoundaryRequest(args.p, L, args.family, args.backend, args.modulus_power)
    try:
        evaluator = BoundaryEvaluator(args.direct_cutoff, args.max_degree)
        if args.reference_prefix or args.prefix is not None:
            provider = DirectReferencePrefix() if args.reference_prefix else SuppliedPrefix(args.p, L, args.prefix)
            output = complete_sum(request, provider, evaluator, output_mode=args.output_mode)
        else:
            if args.output_mode != "full":
                raise BoundaryError("u_only requires a prefix provider (--reference-prefix or --prefix)")
            output = evaluator.evaluate(request).to_dict()
    except BoundaryError as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
