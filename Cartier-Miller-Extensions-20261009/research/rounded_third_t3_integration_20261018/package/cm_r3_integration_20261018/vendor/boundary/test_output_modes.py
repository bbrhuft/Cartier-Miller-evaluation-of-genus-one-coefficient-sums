"""Output-contract and real acquisition-skip checks."""
from contextlib import redirect_stdout
import io
import unittest
from unittest.mock import patch

from boundary_framework import (BoundaryError,BoundaryEvaluator,BoundaryRequest,
    DirectReferencePrefix,SuppliedPrefix,ResourceLimitError,complete_sum)
from integrated_thirds import ThirdPointSession,main as third_main
from integrated_fifths import FifthPointSession,main as fifth_main
from test_boundary_framework import sieve,original_sum_oracle


class OutputModeTests(unittest.TestCase):
    def test_generic_u_only_against_original_sum(self):
        provider=DirectReferencePrefix()
        for p in sieve(127):
            if p==2:continue
            for L in range(p):
                r=complete_sum(BoundaryRequest(p,L),provider,output_mode='u_only')
                self.assertEqual(r['U_p_L'],original_sum_oracle(p,L),(p,L))
                self.assertIsNone(r['B_L']);self.assertIsNone(r['a_L'])
                self.assertIsNone(r['boundary']['value'])
                self.assertEqual(r['boundary_status']=='skipped_zero_multiplier',2*L*(2*L+5)%p==0)

    def test_third_modes_preserve_values(self):
        for p in sieve(2000):
            if p<7:continue
            s=ThirdPointSession(p);full=s.evaluate();u=s.evaluate(output_mode='u_only')
            self.assertEqual(full['U_p_L'],u['U_p_L'],p)
            self.assertEqual(u['U_p_L'],original_sum_oracle(p,s.L),p)
            self.assertIsNone(u['a_L']);self.assertIsNone(u['B_L'])
            self.assertNotIn('B',u['retained_diagnostics'])

    def test_fifth_modes_preserve_values(self):
        for p in sieve(2000):
            if p%5!=4:continue
            s=FifthPointSession(p);full=s.evaluate();u=s.evaluate(output_mode='u_only')
            for f,row in zip(full['outputs'],u['outputs']):
                self.assertEqual(f['U_p_L'],row['U_p_L'],(p,row['L']))
                self.assertEqual(row['U_p_L'],original_sum_oracle(p,row['L']))
                self.assertIsNone(row['B_L']);self.assertIsNone(row['a_L'])

    def test_skipped_third_calls_no_boundary_evaluator(self):
        for p in (13,17):
            s=ThirdPointSession(p)
            with patch.object(s.evaluator,'evaluate',side_effect=AssertionError('boundary acquired')):
                r=s.evaluate(boundary_policy='factorial',output_mode='u_only')
                self.assertEqual(r['boundary_status'],'skipped_zero_multiplier')
                self.assertEqual(r['boundary']['factorial_calls'],[])

    def test_fifth_skip_is_real_and_mixed_pair_still_shares(self):
        s=FifthPointSession(29)
        with patch.object(s.boundaries.intervals,'product',side_effect=AssertionError('interval acquired')):
            r=s.evaluate([12,12],output_mode='u_only')
            self.assertEqual([v['U_p_L'] for v in r['outputs']],[10,10])
            self.assertEqual(r['boundary_details']['interval_calls'],[])
            self.assertEqual(r['skipped_boundary_indices'],[12])
        native=s.boundaries.intervals.product
        with patch.object(s.boundaries.intervals,'product',wraps=native) as mocked:
            r=s.evaluate([12,6,12],output_mode='u_only')
            self.assertEqual(mocked.call_count,2)
            self.assertEqual([v['U_p_L'] for v in r['outputs']],[10,8,10])
            self.assertEqual(r['computed_boundary_indices'],[6])

    def test_full_output_retains_required_boundary(self):
        third=ThirdPointSession(17).evaluate()
        self.assertEqual(third['a_L'],10)
        self.assertEqual(len(third['boundary']['factorial_calls']),1)
        fifth=FifthPointSession(29).evaluate([12])
        self.assertEqual(fifth['outputs'][0]['a_L'],13)
        self.assertEqual(len(fifth['boundary_details']['interval_calls']),2)

    def test_skipping_allows_zero_acquisition_budget(self):
        third=ThirdPointSession(17,max_direct_terms=0)
        self.assertEqual(third.evaluate(backend='direct',output_mode='u_only')['U_p_L'],7)
        with self.assertRaises(ResourceLimitError):third.evaluate(backend='direct')
        fifth=FifthPointSession(29,max_direct_terms=0)
        self.assertEqual(fifth.evaluate([12],backend='direct',output_mode='u_only')['outputs'][0]['U_p_L'],10)
        with self.assertRaises(ResourceLimitError):fifth.evaluate([12],backend='direct')
        with self.assertRaises(ResourceLimitError):fifth.evaluate([6],backend='direct',output_mode='u_only')

    def test_skip_still_validates_domain_options_and_provider(self):
        for mode in ('full','u_only'):
            for request in (BoundaryRequest(0,0),BoundaryRequest(9,2),BoundaryRequest(17,6,backend='unknown'),
                            BoundaryRequest(17,6,family='ordinary_third'),BoundaryRequest(17,6,modulus_power=2)):
                with self.assertRaises(BoundaryError):complete_sum(request,DirectReferencePrefix(),output_mode=mode)
        s=ThirdPointSession(17)
        with self.assertRaises(BoundaryError):s.evaluate(output_mode='bad')
        with self.assertRaises(BoundaryError):s.evaluate(output_mode='u_only',backend='bad')
        with self.assertRaises(BoundaryError):s.evaluate(output_mode='u_only',modulus_power=2)
        f=FifthPointSession(29)
        with self.assertRaises(BoundaryError):f.evaluate([12],output_mode='u_only',backend='bad')
        with self.assertRaises(BoundaryError):f.evaluate([12],output_mode='u_only',modulus_power=2)
        with self.assertRaises(BoundaryError):f.evaluate([12],output_mode='bad')
        with self.assertRaises(BoundaryError):complete_sum(BoundaryRequest(17,6),SuppliedPrefix(17,6,17),output_mode='u_only')

    def test_empty_and_duplicate_contracts(self):
        f=FifthPointSession(29)
        empty=f.evaluate([],output_mode='u_only')
        self.assertEqual(empty['outputs'],[]);self.assertEqual(empty['prefix_passes'],0)
        self.assertEqual(empty['computed_boundary_indices'],[])
        pair=f.evaluate([12,6,12],output_mode='u_only')
        self.assertEqual([r['L'] for r in pair['outputs']],[12,6,12])

    def test_cli_output_modes(self):
        for entry,args,expected in ((third_main,['--p','17','--output-mode','u_only'],'"U_p_L": 7'),
                                    (fifth_main,['--p','29','--which','second','--output-mode','u_only'],'"U_p_L": 10')):
            buf=io.StringIO()
            with redirect_stdout(buf):self.assertEqual(entry(args),0)
            self.assertIn(expected,buf.getvalue());self.assertIn('"a_L": null',buf.getvalue())


if __name__=='__main__':unittest.main(verbosity=2)
