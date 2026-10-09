"""Hash manifest check and small independent smoke checks for this release.

Checks SHA256SUMS.json, then verifies the depth-three fixtures with direct
dense polynomial powers and Legendre traces (no recognizer formulas), runs
the recognizer on the p=73 targets, the trusted-trace and the complete CM
preparations, and reverifies the large-prime fixture. This is not the
validation suite or a benchmark.
"""
from pathlib import Path
import csv
import hashlib
import json
import platform
import random
import sys

sys.dont_write_bytecode = True  # leave the export free of __pycache__
root = Path(__file__).resolve().parent
manifest = json.loads((root/'SHA256SUMS.json').read_text())
for rel, want in manifest.items():
    assert hashlib.sha256((root/rel).read_bytes()).hexdigest() == want, rel
sys.path.insert(0, str(root/'research/depth_three_recognition_20261007/core'))
sys.path.insert(0, str(root/'research/depth_two_recognition_20261006/core'))
from depth_three_recognize import (recognize_depth_three, prepare_from_trace, prepare_cm, cm_trace_candidates,  # noqa: E402
                                   verify_supplied_certificate, RecognizedPreparation, CMPreparation)
from recognize import recognize_short  # noqa: E402

fx = json.loads((root/'fixtures/depth_three_recognition_fixtures.json').read_text())
old = json.loads((root/'fixtures/depth_three_p73.json').read_text())
p = 73
t = fx['p73_target']; c = fx['p73_normalized_cubic']


def dense(coeff):
    v = [1]
    for _ in range((p-1)//2):
        n = [0]*(len(v)+len(coeff)-1)
        for i, a in enumerate(v):
            for j, b in enumerate(coeff):
                n[i+j] = (n[i+j]+a*b) % p
        v = n
    return v


def trace(A, B):
    total = 0
    for x in range(p):
        z = (x**3+A*x+B) % p
        total += 0 if z == 0 else 1 if pow(z, (p-1)//2, p) == 1 else -1
    return -total


v = dense([t['B'], t['A'], 0, 1]); assert (v[p-1], v[p-2]) == (t['H'], t['beta'])
assert trace(t['A'], t['B']) == t['trace'] == old['short_target']['trace']
v = dense(c['f_low_to_high']); assert (v[p-1], v[p-2]) == (c['H'], c['K'])
assert sum(v[i]*pow(c['mu'], i, p) for i in range(p)) % p == c['T']
v = dense([c['short_model'][1], c['short_model'][0], 0, 1]); assert (v[p-1], v[p-2]) == (c['H'], c['beta'])
assert recognize_short(t['A'], t['B'], p)['status'] == 'not_in_depth_at_most_two_closure'
rec = recognize_depth_three(t['A'], t['B'], p)
assert rec['status'] == 'recognized'
m = rec['matches'][0]
assert (m['parameters']['e'], m['parameters']['g'], m['parameters']['r']) == (t['e'], t['g'], t['r'])
assert m['beta_multiplier'] == t['beta_multiplier'] and m['forward_roots'] == t['forward_roots']
assert m['reverse_path']['roots'] == t['reverse_roots'] and m['reverse_path']['endpoint'] == t['reverse_endpoint']
assert verify_supplied_certificate(p, t['A'], t['B'], m)['beta_multiplier'] == t['beta_multiplier']
rec2 = recognize_depth_three(*c['short_model'], p)['matches'][0]
assert rec2['parameters']['r'] == c['r'] and rec2['beta_multiplier'] == c['beta_multiplier']
ev = prepare_from_trace(p, c['f_low_to_high'], c['H'], verify_sign=True, rng=random.Random(20261007))
assert isinstance(ev, RecognizedPreparation) and (ev.evaluator.H, ev.evaluator.K) == (c['H'], c['K'])
assert ev.evaluator.query(c['mu'])['T'] == c['T']
cm = prepare_cm(p, c['f_low_to_high'], rng=random.Random(20261007), max_trials=None)
assert isinstance(cm, CMPreparation) and cm.exact_trace == t['trace'] and cm.evaluator.K == c['K']
assert cm.trace_preparation['representation_4p'] == [c['cornacchia']['t0'], c['cornacchia']['y']]
for A, B in fx['p73_B0_chain_depth3_rejected']:
    assert recognize_depth_three(A, B, p)['status'] == 'not_in_depth_three_family'
for q in fx['ineligible_prime_examples']:
    assert recognize_depth_three(1, 1, q)['status'] == 'not_eligible_prime'
L = fx['large_prime_example']
big = recognize_depth_three(L['A'], L['B'], L['p'])['matches'][0]
assert (big['parameters']['e'], big['parameters']['g'], big['parameters']['r']) == (L['e'], L['g'], L['r'])
assert big['beta_multiplier'] == L['beta_multiplier']
t0, f, _ = cm_trace_candidates(L['p'], random.Random(1))
assert (t0, f) == (L['t0'], L['f']) and t0*t0+192*f*f == 4*L['p']
from validate_consolidation import multiply, family
witness_file = root/'research/depth_three_recognition_20261007/core/sign_bound_p97_witnesses.csv'
with witness_file.open() as handle:
    witnesses = [{k:int(v) for k,v in row.items()} for row in csv.DictReader(handle)]
assert len(witnesses)==8
for w in witnesses:
    assert family(w['p'],w['e'],w['g'],w['r'])==(w['A'],w['B'])
    P=(w['P_x'],w['P_y']);R=(w['gP_x'],w['gP_y'])
    assert (P[1]*P[1]-P[0]**3-w['A']*P[0]-w['B']) % w['p']==0
    assert multiply(w['common_gcd'],P,w['A'],w['p'])==R
# Rounded third point (9 October): a_L = 3/(2 (m!)^3) and U_p(L) = 4B_L - 17/(3 (m!)^3),
# checked against the original t_i recurrence at a few primes p = 2 mod 3.
sys.path.insert(0, str(root/'retained'))
import elliptic_prefix  # noqa: E402
for q in (5, 11, 17, 23, 29, 101, 983):
    assert q % 3 == 2
    h, m = (q-1)//2, (q-2)//3
    a = t = 1; B = U = 0
    for i in range(m+1):
        B = (B+a) % q; U = (U+(h+1+i)*t) % q
        t = t*(h+2+i)*pow(2*i+2, -1, q) % q; a = a*(2*i+1)*pow(4*(i+1), -1, q) % q
    fac = 1
    for i in range(2, m+1):
        fac = fac*i % q
    assert a == 3*pow(2*fac**3, -1, q) % q and U == (4*B-17*pow(3*fac**3, -1, q)) % q, q
    assert elliptic_prefix.third(q)['B'] == B, q
print(json.dumps({'status': 'passed', 'hashed_files': len(manifest),
                  'fixtures': 'p=73 target, normalized cubic, B=0-chain rejections, ineligible primes, 63-bit member, eight exact p=97 witnesses, rounded-third boundary at seven primes',
                  'scope': 'hash verification and small correctness smoke check only; not the validation suite',
                  'python': sys.version, 'platform': platform.platform()}, indent=2))
