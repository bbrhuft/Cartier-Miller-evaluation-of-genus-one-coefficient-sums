"""Shared boundary batches at one validated prime; no persistent answer cache.

Computes a_L=binom(2L,L)*8^(-L) mod p. Auto recognizes third and fifth
reductions; arbitrary indices use the generic ratio. See SHARED_BOUNDARIES.md.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from time import perf_counter

from boundary_framework import (
    BoundaryError, BoundaryEvaluator, DirectReferencePrefix, PrefixProvider,
    UnsupportedPrefixError, _batch_inverse_nonzero, _integer, is_prime64, __version__,
)
from integrated_fifths import IntervalProductEvaluator


@dataclass(frozen=True)
class _RatioPlan:
    L: int
    reduction: str
    scalar: int
    terms: tuple[tuple[tuple[int, int], int], ...]
    known_value: int | None = None


class BoundaryBatchSession:
    """Plan and share built-in boundary reductions at a single odd prime.

    Product tokens are unit intervals (start,length). Prefix intervals (1,n)
    represent n!. Wilson reflection is pushed into exponents before work.
    ``sharing='adjacent'`` shares sorted prefix products via disjoint gaps;
    ``sharing='exact'`` shares identical product tokens only.
    """
    def __init__(self, p, *, direct_cutoff=262144, max_degree=8192,
                 max_direct_terms=2_000_000):
        begin = perf_counter()
        _integer(p, 'p')
        if p < 3 or p % 2 == 0 or not is_prime64(p):
            raise BoundaryError('p must be an odd prime less than 2**64')
        self.p = p
        self.factorials = BoundaryEvaluator(direct_cutoff, max_degree, max_direct_terms)
        self.intervals = IntervalProductEvaluator(direct_cutoff, max_degree, max_direct_terms)
        self.setup_seconds = perf_counter() - begin

    def _prepare(self, indices, family, backend, sharing, modulus_power):
        if type(modulus_power) is not int or modulus_power != 1:
            raise BoundaryError('shared boundary batches support modulo p only')
        if not isinstance(family, str) or family not in (
                'auto', 'generic', 'ordinary_third', 'rounded_third', 'fifth'):
            raise BoundaryError('unknown batch family')
        if not isinstance(backend, str) or backend not in ('auto', 'direct', 'product_tree', 'bgs'):
            raise BoundaryError('unknown batch backend')
        if not isinstance(sharing, str) or sharing not in ('adjacent', 'exact'):
            raise BoundaryError('sharing must be adjacent or exact')
        try:
            wanted = tuple(indices)
        except TypeError as exc:
            raise BoundaryError('indices must be an iterable of integers') from exc
        plans = []
        p = self.p
        for L in wanted:
            _integer(L, 'index')
            if not 0 <= L < p:
                raise BoundaryError('index requires 0 <= L < p')
            ordinary = p >= 7 and p % 3 == 1 and 3 * L == p - 1
            rounded = p >= 11 and p % 3 == 2 and 3 * L == p + 1
            fifth = p >= 19 and p % 5 == 4 and L in ((p + 1) // 5, 2 * (p + 1) // 5)
            if ((family == 'ordinary_third' and not ordinary) or
                    (family == 'rounded_third' and not rounded) or
                    (family == 'fifth' and not fifth)):
                raise BoundaryError(f'hypotheses fail for family {family}')
            if L == 0:
                plans.append(_RatioPlan(L, 'empty_index', 1, (), 1))
                continue
            if L > (p - 1) // 2:
                plans.append(_RatioPlan(L, 'upper_half_zero', 0, (), 0))
                continue
            selected = family
            if selected == 'auto':
                selected = ('ordinary_third' if ordinary else 'rounded_third' if rounded
                            else 'fifth' if fifth else 'generic')
            terms = {}
            scalar = 1

            def interval(start, length, exponent):
                if length == 0 or (start == 1 and length == 1):
                    return
                token = (start, length)
                terms[token] = terms.get(token, 0) + exponent

            def factorial(n, exponent):
                nonlocal scalar
                effective = min(n, p - 1 - n)
                if effective != n:
                    # n! = (-1)^(n+1) / effective!; signs are self-inverse.
                    if n % 2 == 0 and exponent % 2:
                        scalar = -scalar
                    exponent = -exponent
                interval(1, effective, exponent)

            if selected == 'ordinary_third':
                scalar = -1
                factorial(L, -3)
                reduction = selected
            elif selected == 'rounded_third':
                scalar = 3 * pow(2, p - 2, p) % p
                factorial(L - 1, -3)
                reduction = selected
            elif selected == 'fifth':
                ell, first = (p + 1) // 10, (p + 1) // 5
                sign = -1 if ell % 2 else 1
                scalar = sign * pow(2, (-2 * first) % (p - 1), p)
                start = 3 * ell
                reduction = 'fifth_first'
                if L == 2 * first:
                    scalar = sign * pow(2, (2 * first - 4) % (p - 1), p)
                    start, reduction = ell + 1, 'fifth_second'
                interval(1, ell, -1)
                interval(start, ell, 1)
            else:
                scalar = pow(8, (-L) % (p - 1), p)
                factorial(2 * L, 1)
                factorial(L, -2)
                reduction = 'central_binomial'
            plans.append(_RatioPlan(L, reduction, scalar % p,
                                    tuple(sorted((token, exponent) for token, exponent in terms.items()
                                                 if exponent))))
        return tuple(plans)

    def _evaluate_plans(self, plans, backend, sharing):
        begin = perf_counter()
        p = self.p
        unique = {plan.L: plan for plan in plans}
        products = {(1, 0): 1, (1, 1): 1}
        calls, derivations = [], []

        def acquire(token):
            if token in products:
                return products[token]
            start, length = token
            selected = backend
            if selected == 'auto':
                selected = 'direct' if length <= self.factorials.direct_cutoff else 'bgs'
            if start == 1:
                result = self.factorials.backends[selected].factorial(length, p)
                kind = 'factorial'
            else:
                result = self.intervals.product(p, start, length, selected)
                kind = 'interval'
            if type(result.value) is not int or not 0 < result.value < p:
                raise BoundaryError('product backend must return a canonical nonzero unit')
            products[token] = result.value
            calls.append({'kind': kind, 'start': start, 'length': length, 'result': asdict(result)})
            return result.value

        tokens = {token for plan in unique.values() for token, exponent in plan.terms}
        prefix_lengths = sorted(length for start, length in tokens if start == 1)
        previous = 0
        for length in prefix_lengths:
            if sharing == 'adjacent' and previous >= 2:
                gap = (previous + 1, length - previous)
                products[(1, length)] = products[(1, previous)] * acquire(gap) % p
                derivations.append({'factorial_index': length, 'from_factorial': previous,
                                    'gap_start': gap[0], 'gap_length': gap[1]})
            else:
                acquire((1, length))
            previous = length
        for token in sorted(tokens):
            acquire(token)
        acquisition_seconds = perf_counter() - begin
        begin = perf_counter()
        ratios, denominators = {}, {}
        for L, plan in unique.items():
            numerator, denominator = plan.scalar, 1
            for token, exponent in plan.terms:
                value = pow(products[token], abs(exponent), p)
                if exponent > 0:
                    numerator = numerator * value % p
                else:
                    denominator = denominator * value % p
            ratios[L] = (numerator, denominator)
            if denominator != 1:
                denominators[denominator] = None
        inverses = {1: 1}
        if denominators:
            inverses.update(zip(denominators, _batch_inverse_nonzero(list(denominators), p)))
        values = {L: (plan.known_value if plan.known_value is not None else
                      ratios[L][0] * inverses[ratios[L][1]] % p)
                  for L, plan in unique.items()}
        normalization_seconds = perf_counter() - begin
        return {'p': p, 'indices': [plan.L for plan in plans],
                'values': [values[plan.L] for plan in plans],
                'reductions': [plan.reduction for plan in plans],
                'unique_boundaries': len(unique), 'sharing': sharing, 'backend': backend,
                'product_calls': calls, 'product_acquisitions': len(calls),
                'requested_product_tokens': len(tokens),
                'factorial_derivations': derivations,
                'denominator_inversions': int(bool(denominators)),
                'distinct_nontrivial_denominators': len(denominators),
                'acquisition_seconds': acquisition_seconds,
                'normalization_seconds': normalization_seconds,
                'answer_cache_used': False,
                'proof_reference': 'SHARED_BOUNDARIES.md',
                'assurance': 'exact_mod_p_algorithm; finite_validation_is_not_formal_verification'}

    def evaluate(self, indices, *, family='auto', backend='auto', sharing='adjacent',
                 modulus_power=1):
        begin = perf_counter()
        plans = self._prepare(indices, family, backend, sharing, modulus_power)
        preparation = perf_counter() - begin
        result = self._evaluate_plans(plans, backend, sharing)
        elapsed = perf_counter() - begin
        result.update(preparation_seconds=preparation, warm_total_seconds=elapsed,
                      session_setup_seconds=self.setup_seconds,
                      cold_total_seconds=self.setup_seconds + elapsed)
        return result

    def complete_many(self, indices, provider: PrefixProvider, *, family='auto', backend='auto',
                      sharing='adjacent', modulus_power=1, output_mode='full'):
        """Complete U values using the existing strict-prefix provider contract.

        Duplicate indices share one provider call. A supported arbitrary boundary
        does not imply that the provider supports its prefix or computes it fast.
        """
        begin = perf_counter()
        if not isinstance(output_mode, str) or output_mode not in ('full', 'u_only'):
            raise BoundaryError('output_mode must be full or u_only')
        plans = self._prepare(indices, family, backend, sharing, modulus_power)
        wanted = tuple(dict.fromkeys(plan.L for plan in plans))
        for L in wanted:
            if not provider.supports(self.p, L):
                raise UnsupportedPrefixError(f'prefix provider {provider.name} does not support (p,L)')
        prefix_begin = perf_counter()
        prefixes = {}
        for L in wanted:
            value = provider.prefix(self.p, L)
            _integer(value, 'prefix')
            if not 0 <= value < self.p:
                raise BoundaryError('prefix provider must return a canonical residue 0 <= B_L < p')
            prefixes[L] = value
        prefix_seconds = perf_counter() - prefix_begin
        skipped = {L for L in wanted if output_mode == 'u_only' and
                   2 * L * (2 * L + 5) % self.p == 0}
        details = self._evaluate_plans(tuple(plan for plan in plans if plan.L not in skipped),
                                       backend, sharing)
        boundaries = dict(zip(details['indices'], details['values']))
        outputs = []
        for plan in plans:
            L = plan.L
            multiplier = 2 * L * (2 * L + 5) % self.p
            value = (4 * prefixes[L] - multiplier * boundaries.get(L, 0)) % self.p
            outputs.append({'L': L, 'B_L': prefixes[L] if output_mode == 'full' else None,
                            'a_L': boundaries[L] if output_mode == 'full' else None,
                            'U_p_L': value, 'boundary_multiplier': multiplier,
                            'boundary_status': 'skipped_zero_multiplier' if L in skipped else 'computed'})
        if output_mode == 'u_only':
            details['values'] = [None] * len(details['values'])
        elapsed = perf_counter() - begin
        return {'p': self.p, 'outputs': outputs, 'output_mode': output_mode,
                'prefix_provider': provider.name, 'prefix_assurance': provider.assurance,
                'prefix_calls': len(prefixes), 'prefix_seconds': prefix_seconds,
                'boundary_details': details, 'skipped_boundary_indices': sorted(skipped),
                'computed_boundary_indices': sorted(boundaries),
                'answer_cache_used': False, 'warm_total_seconds': elapsed,
                'session_setup_seconds': self.setup_seconds,
                'cold_total_seconds': self.setup_seconds + elapsed}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--p', type=int, required=True)
    parser.add_argument('--indices', type=int, nargs='*', required=True)
    parser.add_argument('--family', choices=('auto', 'generic', 'ordinary_third', 'rounded_third', 'fifth'), default='auto')
    parser.add_argument('--backend', choices=('auto', 'direct', 'product_tree', 'bgs'), default='auto')
    parser.add_argument('--sharing', choices=('adjacent', 'exact'), default='adjacent')
    parser.add_argument('--modulus-power', type=int, default=1)
    parser.add_argument('--direct-cutoff', type=int, default=262144)
    parser.add_argument('--max-degree', type=int, default=8192)
    parser.add_argument('--max-direct-terms', type=int, default=2_000_000)
    parser.add_argument('--reference-prefix', action='store_true')
    parser.add_argument('--output-mode', choices=('full', 'u_only'), default='full')
    args = parser.parse_args(argv)
    try:
        if args.output_mode == 'u_only' and not args.reference_prefix:
            raise BoundaryError('u_only requires a prefix provider; boundary-only queries compute a_L')
        session = BoundaryBatchSession(args.p, direct_cutoff=args.direct_cutoff,
                                       max_degree=args.max_degree, max_direct_terms=args.max_direct_terms)
        options = dict(family=args.family, backend=args.backend, sharing=args.sharing,
                       modulus_power=args.modulus_power)
        result = (session.complete_many(args.indices, DirectReferencePrefix(args.max_direct_terms),
                                       output_mode=args.output_mode, **options)
                  if args.reference_prefix else session.evaluate(args.indices, **options))
        print(json.dumps({'version': __version__, **result}, indent=2))
        return 0
    except BoundaryError as exc:
        print(json.dumps({'error': str(exc)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
