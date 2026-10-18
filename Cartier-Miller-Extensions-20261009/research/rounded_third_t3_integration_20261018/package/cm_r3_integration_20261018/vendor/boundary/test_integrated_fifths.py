"""Independent fifth-boundary and complete-output tests."""
from contextlib import redirect_stdout
import io
from math import prod
import random
import unittest
from unittest.mock import patch

from boundary_framework import BoundaryError, ResourceLimitError, UnsupportedPrefixError
import integrated_fifths as fifths
from integrated_fifths import FifthBoundaryEvaluator,FifthPointSession,IntervalProductEvaluator,main
from test_boundary_framework import sieve,binomial_oracle,original_sum_oracle
from test_integrated_thirds import scaled_prefix_oracle


class FifthTests(unittest.TestCase):
    def test_intervals_against_integer_products(self):
        rng=random.Random(20261015)
        evaluator=IntervalProductEvaluator()
        for p in (101,10007,4294967291):
            for length in (0,1,4,17,63,100,1024,4096):
                if length>=p:continue
                for _ in range(3):
                    start=rng.randrange(1,p-length+1)
                    expected=prod(range(start,start+length))%p
                    for backend in ('direct','product_tree','bgs'):
                        self.assertEqual(evaluator.product(p,start,length,backend).value,expected)

    def test_both_boundaries_all_fifth_primes_through_10000(self):
        for p in sieve(10000):
            if p%5!=4:continue
            evaluator=FifthBoundaryEvaluator(p)
            for backend in ('direct','product_tree','bgs'):
                result=evaluator.evaluate(backend=backend)
                self.assertEqual(len(result['interval_calls']),3)
                self.assertEqual(result['denominator_inversions'],1)
                for n,a in zip(result['indices'],result['values']):
                    self.assertEqual(a,binomial_oracle(p,n),(p,n,backend))

    def test_complete_pair_all_fifth_primes_through_10000(self):
        for p in sieve(10000):
            if p%5!=4:continue
            result=FifthPointSession(p).evaluate()
            self.assertEqual(result['prefix_passes'],1)
            self.assertEqual(len(result['boundary_details']['interval_calls']),3)
            for row in result['outputs']:
                n=row['L']
                self.assertEqual(row['B_L'],scaled_prefix_oracle(p,n),(p,n))
                self.assertEqual(row['a_L'],binomial_oracle(p,n),(p,n))
                self.assertEqual(row['U_p_L'],original_sum_oracle(p,n),(p,n))

    def test_held_out_complete_pairs(self):
        for p in (10009,20029,50069,100019,1000039):
            session=FifthPointSession(p)
            result=session.evaluate(backend='product_tree')
            for row in result['outputs']:
                n=row['L']
                self.assertEqual(row['B_L'],scaled_prefix_oracle(p,n),(p,n))
                self.assertEqual(row['a_L'],binomial_oracle(p,n),(p,n))
                self.assertEqual(row['U_p_L'],original_sum_oracle(p,n),(p,n))

    def test_single_duplicate_and_empty_requests(self):
        session=FifthPointSession(199);L=session.L
        pair=session.evaluate()
        for n,row in zip((L,2*L),pair['outputs']):
            single=session.evaluate([n])
            self.assertEqual(single['outputs'],[row])
            self.assertEqual(len(single['boundary_details']['interval_calls']),2)
        duplicate=session.evaluate([2*L,L,2*L])
        self.assertEqual(duplicate['outputs'],[pair['outputs'][1],pair['outputs'][0],pair['outputs'][1]])
        self.assertEqual(len(duplicate['boundary_details']['interval_calls']),3)
        with patch.object(fifths,'prefixes',side_effect=AssertionError('empty prefix call')):
            empty=session.evaluate([])
            self.assertEqual(empty['outputs'],[])
            self.assertEqual(empty['prefix_passes'],0)
            self.assertEqual(empty['boundary_details']['denominator_inversions'],0)

    def test_one_prefix_call_and_no_persistent_answer_cache(self):
        native=fifths.prefixes
        with patch.object(fifths,'prefixes',wraps=native) as mocked:
            session=FifthPointSession(199)
            first=session.evaluate();second=session.evaluate()
            self.assertEqual(mocked.call_count,2)
            self.assertEqual(first['outputs'],second['outputs'])
            self.assertFalse(second['answer_cache_used'])
            self.assertEqual(second['boundary_details']['unique_boundaries'],2)

    def test_interval_sharing_is_real(self):
        session=FifthPointSession(199)
        native=session.boundaries.intervals.product
        with patch.object(session.boundaries.intervals,'product',wraps=native) as mocked:
            session.evaluate()
            self.assertEqual(mocked.call_count,3)
        with patch.object(session.boundaries.intervals,'product',wraps=native) as mocked:
            session.evaluate([session.L]);session.evaluate([2*session.L])
            self.assertEqual(mocked.call_count,4)

    def test_p29_vanishing_multiplier_still_returns_boundary(self):
        second=FifthPointSession(29).evaluate()['outputs'][1]
        self.assertEqual(second,{'L':12,'B_L':17,'a_L':13,'U_p_L':10,'boundary_multiplier':0})

    def test_input_rejection_and_budgets(self):
        for p in (2,5,9,13,49,10019,True,19.0,2**64+13):
            with self.assertRaises(BoundaryError):FifthPointSession(p)
        session=FifthPointSession(199)
        for indices in ([0],[session.L+1],[True],1):
            with self.assertRaises(BoundaryError):session.evaluate(indices)
        for power in (2,True,1.0):
            with self.assertRaises(BoundaryError):session.evaluate(modulus_power=power)
        with self.assertRaises(BoundaryError):session.evaluate(backend='unknown')
        with patch.object(fifths,'prefixes',side_effect=AssertionError('prefix before limit check')):
            with self.assertRaises(ResourceLimitError):
                FifthPointSession(199,max_degree=1).evaluate(backend='product_tree')
            with self.assertRaises(ResourceLimitError):
                FifthPointSession(199,max_direct_terms=1).evaluate(backend='direct')

    def test_cli(self):
        for args,code,fragment in ((['--p','19'],0,'"U_p_L": 16'),
                                   (['--p','29','--which','second'],0,'"U_p_L": 10'),
                                   (['--p','19','--modulus-power','2'],2,'"error"'),
                                   (['--p','49'],2,'"error"')):
            buf=io.StringIO()
            with redirect_stdout(buf):self.assertEqual(main(args),code)
            self.assertIn(fragment,buf.getvalue())


if __name__=='__main__':unittest.main(verbosity=2)
