"""Independent arithmetic and interface checks; run python -m unittest -v."""
import io
from contextlib import redirect_stdout
from math import comb, factorial
import random
import unittest

from boundary_framework import (
    BoundaryError, BoundaryEvaluator, BoundaryRequest, DirectFactorialBackend,
    DirectReferencePrefix, ProductTreeFactorialBackend, ResourceLimitError,
    SuppliedPrefix, UnsupportedPrefixError, _mul, _multipoint, _product_tree,
    _remainder, complete_sum, is_prime64, main,
)


def sieve(limit):
    flags = bytearray(b"\x01") * (limit + 1)
    flags[:2] = b"\x00\x00"
    for n in range(2, int(limit**0.5) + 1):
        if flags[n]:
            flags[n*n::n] = b"\x00" * ((limit - n*n) // n + 1)
    return [n for n in range(2, limit + 1) if flags[n]]


def binomial_oracle(p, L):
    # Integer binomial, independent of factorial reductions/polynomial code.
    return comb(2 * L, L) * pow(8, -L, p) % p


def original_sum_oracle(p, L):
    # The original t recurrence; does not use B_L or a_L.
    h, t, total = (p - 1) // 2, 1, 0
    for i in range(L):
        total = (total + (h + 1 + i) * t) % p
        if i + 1 < L:
            t = t * (h + 2 + i) * pow(2 * i + 2, -1, p) % p
    return total


class ArithmeticTests(unittest.TestCase):
    def test_primality_against_sieve_and_large_controls(self):
        primes = set(sieve(50000))
        for n in range(50001):
            self.assertEqual(is_prime64(n), n in primes, n)
        for n in (341550071728321, 3825123056546413051, 2**64 - 1):
            self.assertFalse(is_prime64(n))
        for n in (4294967291, 18446744073709551557):
            self.assertTrue(is_prime64(n))

    def test_polynomial_primitives_against_schoolbook_and_horner(self):
        rng = random.Random(20261015)
        for p in (101, 10007, 4294967291):
            for length in (1, 15, 16, 31, 64, 127):
                a = [rng.randrange(p) for _ in range(length)]
                b = [rng.randrange(p) for _ in range(length + 7)]
                expected = [0] * (len(a) + len(b) - 1)
                for i, x in enumerate(a):
                    for j, y in enumerate(b):
                        expected[i+j] = (expected[i+j] + x*y) % p
                while len(expected) > 1 and expected[-1] == 0:
                    expected.pop()
                self.assertEqual(_mul(a, b, p), expected)
                points = [rng.randrange(p) for _ in range(length)]
                tree = _product_tree([[(-x) % p, 1] for x in points], p)
                values = []
                for x in points:
                    value = 0
                    for c in a[::-1]:
                        value = (value*x+c) % p
                    values.append(value)
                self.assertEqual(_multipoint(a, tree, p), values)
                divisor = b[:max(2, length//2)] + [1]
                r = a[:]
                degree = len(divisor)-1
                for k in range(len(r)-1, degree-1, -1):
                    lead = r[k]
                    for j in range(degree+1):
                        r[k-degree+j] = (r[k-degree+j] - lead*divisor[j]) % p
                r = r[:degree]
                while len(r) > 1 and r[-1] == 0:
                    r.pop()
                self.assertEqual(_remainder(a, divisor, p), r)

    def test_every_factorial_small_primes_both_backends(self):
        backends = (DirectFactorialBackend(), ProductTreeFactorialBackend())
        for p in sieve(127):
            if p == 2:
                continue
            for n in range(p):
                expected = factorial(n) % p
                for backend in backends:
                    self.assertEqual(backend.factorial(n, p).value, expected, (p, n, backend.name))

    def test_every_boundary_small_primes_all_routes(self):
        evaluator = BoundaryEvaluator()
        for p in sieve(257):
            if p == 2:
                continue
            for L in range(p):
                expected = binomial_oracle(p, L)
                for family, backend in (("auto", "direct"), ("auto", "product_tree"),
                                        ("generic", "product_tree")):
                    result = evaluator.evaluate(BoundaryRequest(p, L, family, backend))
                    self.assertEqual(result.value, expected, (p, L, family, backend))

    def test_both_third_families_through_10000(self):
        evaluator = BoundaryEvaluator()
        for p in sieve(10000):
            if p < 7:
                continue
            if p % 3 == 1:
                family, L = "ordinary_third", (p-1)//3
            else:
                family, L = "rounded_third", (p+1)//3
            expected = binomial_oracle(p, L)
            for backend in ("direct", "product_tree", "bgs"):
                result = evaluator.evaluate(BoundaryRequest(p, L, family, backend))
                self.assertEqual(result.value, expected, (p, L, backend))
                self.assertEqual(result.reduction, family)
                self.assertEqual(len(result.factorial_calls), 1)

    def test_held_out_larger_indices(self):
        rng = random.Random(77359)
        evaluator = BoundaryEvaluator()
        for p in (10007, 20021, 50021, 100003, 1000003):
            indices = {0, 1, (p-1)//2, (p+1)//2, p-1}
            indices.update(rng.randrange(p) for _ in range(6))
            for L in sorted(indices):
                result = evaluator.evaluate(BoundaryRequest(p, L, backend="product_tree"))
                self.assertEqual(result.value, binomial_oracle(p, L), (p, L))

    def test_complete_sum_against_original_recurrence(self):
        evaluator = BoundaryEvaluator()
        provider = DirectReferencePrefix()
        for p in sieve(127):
            if p == 2:
                continue
            for L in range(p):
                result = complete_sum(BoundaryRequest(p, L), provider, evaluator)
                self.assertEqual(result["U_p_L"], original_sum_oracle(p, L), (p, L))

    def test_p17_vanishing_boundary_multiplier(self):
        result = complete_sum(BoundaryRequest(17, 6), SuppliedPrefix(17, 6, 6))
        self.assertEqual(result["a_L"], 10)
        self.assertEqual(result["U_p_L"], 7)


class InterfaceTests(unittest.TestCase):
    def test_reject_invalid_inputs(self):
        evaluator = BoundaryEvaluator()
        bad = [BoundaryRequest(2, 0), BoundaryRequest(9, 1), BoundaryRequest(1, 0),
               BoundaryRequest(11, -1), BoundaryRequest(11, 11), BoundaryRequest(11.0, 1),
               BoundaryRequest(11, True), BoundaryRequest(11, 4, modulus_power=2),
               BoundaryRequest(11, 4, modulus_power=True), BoundaryRequest(2**64+13, 1),
               BoundaryRequest(11, 4, family="unknown"), BoundaryRequest(11, 4, backend="unknown"),
               BoundaryRequest(11, 4, family=[]), BoundaryRequest(11, 4, backend=[]),
               BoundaryRequest(11, 4, family="ordinary_third"),
               BoundaryRequest(5, 2, family="rounded_third")]
        for request in bad:
            with self.assertRaises(BoundaryError, msg=str(request)):
                evaluator.evaluate(request)

    def test_resource_limits(self):
        with self.assertRaises(ResourceLimitError):
            BoundaryEvaluator(max_direct_terms=10).evaluate(BoundaryRequest(101, 33, backend="direct"))
        with self.assertRaises(ResourceLimitError):
            BoundaryEvaluator(max_degree=2).evaluate(BoundaryRequest(101, 33, backend="product_tree"))

    def test_prefix_support_and_assurance(self):
        with self.assertRaises(UnsupportedPrefixError):
            complete_sum(BoundaryRequest(11, 4), SuppliedPrefix(17, 6, 6))
        with self.assertRaises(UnsupportedPrefixError):
            complete_sum(BoundaryRequest(11, 4), DirectReferencePrefix(max_terms=2))
        for value in (-1, 11, True, 8.0):
            with self.assertRaises(BoundaryError):
                complete_sum(BoundaryRequest(11, 4), SuppliedPrefix(11, 4, value))
        result = complete_sum(BoundaryRequest(11, 4), SuppliedPrefix(11, 4, 8))
        self.assertEqual((result["B_L"], result["a_L"], result["U_p_L"]), (8, 1, 5))
        self.assertIn("not_independently_verified", result["prefix_assurance"])

    def test_registration_and_selected_backend(self):
        evaluator = BoundaryEvaluator()
        evaluator.register_backend("my_direct", DirectFactorialBackend())
        self.assertEqual(evaluator.evaluate(BoundaryRequest(11, 4, backend="my_direct")).value, 1)
        for name in ("auto", "", "direct"):
            with self.assertRaises(BoundaryError):
                evaluator.register_backend(name, DirectFactorialBackend())
        evaluator.register_reduction("never", lambda p, L: None)
        with self.assertRaises(BoundaryError):
            evaluator.evaluate(BoundaryRequest(11, 4, family="never"))
        with self.assertRaises(BoundaryError):
            evaluator.register_reduction("generic", lambda p, L: None)

    def test_cli_success_and_error(self):
        for args, expected_status, fragment in (
            (["--p", "11", "--family", "rounded_third", "--reference-prefix"], 0, '"U_p_L": 5'),
            (["--p", "17", "--family", "rounded_third", "--prefix", "6"], 0, '"U_p_L": 7'),
            (["--p", "9", "--index", "1"], 2, '"error"'),
            (["--p", "11", "--index", "4", "--modulus-power", "2"], 2, '"error"'),
        ):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                self.assertEqual(main(args), expected_status)
            self.assertIn(fragment, buffer.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
