# SPDX-License-Identifier: GPL-2.0-or-later
import json
from pathlib import Path
import tempfile
import threading
import unittest
from benchmark_engine import make_primes,prepare,isolated_job,save_outputs
from elliptic_prefix import quarter
from pilot import is_prime,original_values,prefix_values
from point_count import direct_trace,schoof_trace,bsgs_trace,schoof_mod_l,division_polynomial,interval_annihilators,mul


class ArithmeticTests(unittest.TestCase):
    def test_independent_point_counts_and_complete_sum(self):
        count=0
        for p in range(13,1000,4):
            if not is_prime(p):continue
            t=direct_trace(p)
            self.assertEqual(schoof_trace(p),t,p);self.assertEqual(bsgs_trace(p),t,p)
            self.assertEqual(prepare(p,'cornacchia'),t,p)
            z=quarter(p,trace=t);n=(p-1)//4
            self.assertEqual(z['U'],original_values(p)[n],p)
            ref=prefix_values(p)[n]
            self.assertEqual((z['B'],z['a']),(ref['B'],ref['a']),p);count+=1
        self.assertGreater(count,70)
    def test_large_cross_checks(self):
        for p in [10009,100049,1000033,10000121,100000037,1000000009]:
            t=quarter(p)['trace'];self.assertEqual(schoof_trace(p),t);self.assertEqual(bsgs_trace(p),t)
    def test_frobenius_residues(self):
        for p in [13,37,97,1009]:
            t=direct_trace(p)
            for l in [3,5,7,11]:
                self.assertEqual(schoof_mod_l(p,l),t%l)
                self.assertEqual(len(division_polynomial(p,l))-1,(l*l-1)//2)
    def test_bsgs_low_order_all_collisions(self):
        P=(0,0);p=97;lo=79;hi=117
        result=interval_annihilators(P,p,2,lo,hi)
        self.assertEqual(result,{n for n in range(lo,hi+1) if mul(n,P,p) is None})
    def test_prime_grids_and_rejected_example(self):
        self.assertEqual(make_primes(count=8)[-1],1000000009)
        self.assertEqual(len(make_primes('geometric',20,'97','1.5')),20)
        for kwargs in [dict(mode='custom',custom='1000000007'),dict(count=30),dict(mode='geometric',factor='1'),dict(mode='custom',custom='97 97')]:
            with self.assertRaises(ValueError):make_primes(**kwargs)
    def test_deadline_and_exports(self):
        with tempfile.TemporaryDirectory() as d:
            result=isolated_job(1000000009,'schoof',{'repetitions':11,'target_ms':25,'timeout':.001,'output':d},threading.Event())
            self.assertEqual(result['row']['status'],'timeout')
            save_outputs(d,[result['row']],[],{'state':'partial'})
            data=json.loads((Path(d)/'benchmark.json').read_text());self.assertEqual(data['rows'][0]['status'],'timeout')
            self.assertIn('schoof_status',(Path(d)/'paper_table.csv').read_text(encoding='utf-8-sig'))

if __name__=='__main__':unittest.main()
