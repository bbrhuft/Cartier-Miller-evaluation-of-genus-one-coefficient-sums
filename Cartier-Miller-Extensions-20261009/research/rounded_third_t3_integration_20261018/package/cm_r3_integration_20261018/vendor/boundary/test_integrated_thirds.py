"""Independent end-to-end checks for the retained prefix integration."""
import io
from contextlib import redirect_stdout
from math import comb
from unittest.mock import patch
import unittest

from boundary_framework import BoundaryError, BoundaryRequest, DirectReferencePrefix, UnsupportedPrefixError
from integrated_thirds import ThirdPointPrefixProvider, ThirdPointSession, main
from test_boundary_framework import sieve, original_sum_oracle, binomial_oracle


def scaled_prefix_oracle(p, L):
    # Integer-scaled binomial recurrence with one final inverse. Independent
    # of the geometric prefix, trace normalization, and boundary registry.
    a, b, denominator = 1, 0, 1
    for i in range(L):
        factor = 4*(i+1) % p
        a, b, denominator = (a*(2*i+1) % p,
                             (b+a)*factor % p, denominator*factor % p)
    return b*pow(denominator,-1,p) % p


class IntegratedTests(unittest.TestCase):
    def test_all_third_family_primes_through_10000(self):
        for p in sieve(10000):
            if p < 7:
                continue
            session = ThirdPointSession(p)
            result = session.evaluate()
            self.assertEqual(result['B_L'], scaled_prefix_oracle(p,session.L),p)
            self.assertEqual(result['a_L'], binomial_oracle(p,session.L),p)
            self.assertEqual(result['U_p_L'], original_sum_oracle(p,session.L),p)
            self.assertFalse(result['answer_cache_used'])
            self.assertGreaterEqual(result['cold_total_seconds'],result['warm_total_seconds'])
            if p % 3 == 1:
                self.assertEqual(result['boundary']['reduction'],'ordinary_third_trace')
                self.assertEqual(len(result['boundary']['factorial_calls']),0)
            else:
                self.assertEqual(result['boundary']['reduction'],'rounded_third')
                self.assertEqual(len(result['boundary']['factorial_calls']),1)

    def test_forced_factorial_boundary_and_warm_reuse(self):
        for p in sieve(2000):
            if p < 7:
                continue
            session = ThirdPointSession(p)
            auto = session.evaluate()
            forced = session.evaluate(boundary_policy='factorial',backend='product_tree')
            self.assertEqual((auto['B_L'],auto['a_L'],auto['U_p_L']),
                             (forced['B_L'],forced['a_L'],forced['U_p_L']),p)
            self.assertFalse(forced['answer_cache_used'])
            self.assertEqual(len(forced['boundary']['factorial_calls']),1)

    def test_held_out_primes(self):
        for p in (10007,20021,50021,100003,100019,1000003,1000037):
            session=ThirdPointSession(p)
            result=session.evaluate(backend='product_tree')
            self.assertEqual(result['B_L'],scaled_prefix_oracle(p,session.L),p)
            self.assertEqual(result['a_L'],binomial_oracle(p,session.L),p)
            self.assertEqual(result['U_p_L'],original_sum_oracle(p,session.L),p)

    def test_ordinary_trace_against_direct_curve_count(self):
        for p in sieve(500):
            if p >= 7 and p % 3 == 1:
                provider=ThirdPointPrefixProvider(p)
                trace=0
                for w in range(p):
                    value=(1-pow(w,3,p)*pow(2,-1,p))%p
                    char=0 if value==0 else (1 if pow(value,(p-1)//2,p)==1 else -1)
                    trace-=char
                self.assertEqual(provider.native.trace,trace,p)

    def test_known_regressions_and_strict_prefix(self):
        for p,L,B,a,U in ((11,4,8,1,5),(17,6,6,10,7),(23,8,7,9,17),(29,10,13,21,21)):
            result=ThirdPointSession(p).evaluate()
            self.assertEqual((result['L'],result['B_L'],result['a_L'],result['U_p_L']),(L,B,a,U))
            inclusive=sum(comb(2*i,i)*pow(8,-i,p) for i in range(L+1))%p
            self.assertNotEqual(result['B_L'],inclusive)

    def test_no_reference_prefix_fallback(self):
        with patch.object(DirectReferencePrefix,'prefix',side_effect=AssertionError('reference forbidden')):
            for p in (13,23):
                ThirdPointSession(p).evaluate()

    def test_domain_and_cli_errors(self):
        for p in (2,3,5,9,True,11.0,2**64+13):
            with self.assertRaises(BoundaryError): ThirdPointSession(p)
        s=ThirdPointSession(23)
        with self.assertRaises(UnsupportedPrefixError): s.provider.prefix(23,7)
        with self.assertRaises(BoundaryError): s.evaluate(modulus_power=2)
        with self.assertRaises(BoundaryError): s.evaluate(boundary_policy='unknown')
        for args,status,fragment in ((['--p','23'],0,'"U_p_L": 17'),
                                     (['--p','23','--index','7'],2,'"error"'),
                                     (['--p','23','--modulus-power','2'],2,'"error"')):
            buf=io.StringIO()
            with redirect_stdout(buf): self.assertEqual(main(args),status)
            self.assertIn(fragment,buf.getvalue())


if __name__=='__main__': unittest.main(verbosity=2)
