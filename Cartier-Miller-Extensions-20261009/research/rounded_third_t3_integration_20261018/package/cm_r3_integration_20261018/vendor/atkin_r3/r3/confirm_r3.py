"""Round-3 frozen confirmation.  Run only after r3/FREEZE_R3.json exists and verifies.

Selection rule (CANDIDATE_R3.md, Section "Confirmation rule"): classes A (p = 11 mod 12),
B (p = 5 mod 24), C (p = 17 mod 24); every prime is the first one at or above the stated bound
with the stated congruences that is NOT in r3/evidence/LEDGER_R3.json (range rules included).
  S  small (defining-binomial checks):  bound 2e6, q in QS = primes 5..47.
  M  medium (FLINT references):         bound 3e9, q in QM = primes 5..89.
  L  large (FLINT references):          bound 3e11, q in {11, 23, 47, 89}.
  E1 no admissible q (fallback):        bound 4e10, two per class, no prime 5<=q<=89 divides p-1.
  E2 q^2 | p-1:                          bound 3e9, q in {5, 7, 11}, one per class.
  E3 K < K_min (class A only):          bound 3e5, two primes such that some prime 5<=q<=89 divides
                                        p-1 but every such q has (p-1)/q < K_min  -> fallback.
  E4 generic p-only sample:             bound 1e10, first 10 primes of each class (any divisors).
Checks per prime (all must hold exactly):
  tal_split with the default anchor and, for p = 5 mod 12, also the other anchor, for every
  q in the prime's q-list that divides p-1 with (p-1)/q >= K_min:  m!, c_p, a_L, D agree with the
  reference; set S additionally: a_L = binom(2L,L) 8^{-L} by an independent O(L) product loop,
  m! by an independent linear loop, D by the round-1 Wronskian product and the Atkin recurrence;
  every applicable half-interval route (Mordell / Williams-Currie, and Gauss for class B) with the
  unconditional class-number policy, cross-checked against the reduced-form count when
  |D| < 2e9 and against PARI quadclassunit always; the GRH half-interval and FLINT nodal routes;
  the p-only API (acquire_aL) in both modes, recording its route and status label.
Writes r3/evidence/CONFIRMATION_R3.json.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from r3.common import (is_prime, params, flint_factorial, c_from_mfact, a_from_c, ClassNumberPolicy,
                       classno_forms, classno_grh)
from r3.research.ledger import excluded
from r3 import tal3
from r3.halfint import half_factorial3, halfinterval_c3
from r3.acquire_r3 import acquire_aL, admissible_q, nodal_flint_c, policy

CLASSES = {'A': (12, 11), 'B': (24, 5), 'C': (24, 17)}
QS = [q for q in range(5, 48) if is_prime(q)]
QM = [q for q in range(5, 90) if is_prime(q)]
QL = [11, 23, 47, 89]


def verify_freeze_r3():
    fr = json.loads((ROOT / 'r3/FREEZE_R3.json').read_text())
    for name, digest in fr['sha256'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise SystemExit('FREEZE_R3 mismatch: %s' % name)
    return fr


def first(bound, mod, res, extra=lambda p: True, count=1):
    out, p = [], bound
    while len(out) < count:
        if p % mod == res and extra(p) and not excluded(p) and is_prime(p):
            out.append(p)
        p += 1
    return out


def select():
    sel = dict(S={}, M={}, L={}, E1={}, E2={}, E3={}, E4={})
    for X, (mo, r) in CLASSES.items():
        sel['S'][X] = {q: first(2 * 10 ** 6, mo, r, lambda p, q=q: p % q == 1)[0] for q in QS}
        sel['M'][X] = {q: first(3 * 10 ** 9, mo, r, lambda p, q=q: p % q == 1)[0] for q in QM}
        sel['L'][X] = {q: first(3 * 10 ** 11, mo, r, lambda p, q=q: p % q == 1)[0] for q in QL}
        sel['E1'][X] = first(4 * 10 ** 10, mo, r, lambda p: all((p - 1) % q for q in QM), 2)
        sel['E2'][X] = {q: first(3 * 10 ** 9, mo, r, lambda p, q=q: (p - 1) % (q * q) == 0)[0] for q in (5, 7, 11)}
        sel['E4'][X] = first(10 ** 10, mo, r, count=10)
    sel['E3']['A'] = first(3 * 10 ** 5, 12, 11,
                           lambda p: any((p - 1) % q == 0 for q in QM) and not admissible_q(p), 2)
    return sel


class CachedPolicy:
    """Confirmation-only cache of class numbers by discriminant (not used in any timing)."""
    def __init__(self, pol):
        self.pol, self.c = pol, {}

    def __call__(self, D):
        if D not in self.c:
            self.c[D] = self.pol(D)
        return self.c[D]


def binom_aL(p):
    L = (p + 1) // 3
    num = den = 1
    for j in range(1, L + 1):
        num = num * (L + j) % p
        den = den * j % p
    return num * pow(den, p - 2, p) * pow(pow(8, L, p), p - 2, p) % p


def check_prime(p, qlist, small=False):
    import atkin
    t0 = perf_counter()
    P = params(p)
    m = P['m']
    mf = flint_factorial(m, p)
    c_ref = c_from_mfact(p, mf)
    a_ref, D_ref = a_from_c(p, c_ref), atkin.derivative_from_c(p, c_ref)
    rec = dict(p=p, cls='A' if p % 12 == 11 else ('B' if p % 24 == 5 else 'C'), tal={}, hi={}, api={})
    if small:
        lin = 1
        for j in range(1, m + 1):
            lin = lin * j % p
        assert lin == mf, 'linear m!'
        assert binom_aL(p) == a_ref, 'defining binomial'
        assert atkin.wronskian_endpoint(p) == D_ref, 'Wronskian D'
        assert atkin.atkin_endpoint(p) == D_ref, 'Atkin recurrence D'
        rec['independent'] = ['linear m!', 'binom(2L,L)8^-L', 'Wronskian D', 'Atkin recurrence D']
    for q in qlist:
        if (p - 1) % q or (p - 1) // q < policy()['K_min']:
            continue
        anchors = ['dup6', 'dup12'] if p % 12 == 5 else ['dup6']
        for an in anchors:
            c, md = tal3.acquire(p, q, an)
            mfx = tal3.mfact_from_c(p, c)
            ok = (c == c_ref and mfx == mf and a_from_c(p, c) == a_ref and atkin.derivative_from_c(p, c) == D_ref)
            assert ok, ('tal', p, q, an)
            rec['tal']['%d/%s' % (q, an)] = dict(ok=True, k=md['k'], kind=md['anchor_kind'],
                                                 lengths=md['residual_lengths'], fallbacks=md['enumeration_fallbacks'])
    H_ref = flint_factorial(P['h'], p)
    unc = CachedPolicy(ClassNumberPolicy('unconditional'))
    routes = ['mordell'] if p % 4 == 3 else (['williams_currie', 'gauss4p'] if p % 8 == 5 else ['williams_currie'])
    for route in routes:
        H, hm = half_factorial3(p, unc, route)
        assert H == H_ref, ('H', p, route)
        D = hm.get('D')
        hg = classno_grh(D)
        assert hg == hm['classno']
        xf = None
        if abs(D) < 2 * 10 ** 9:
            xf = classno_forms(D)
            assert xf == hm['classno']
        rec['hi'][route] = dict(ok=True, D=D, h=hm['classno'], backend=hm['backend'],
                                status=hm['classno_status'], forms_crosscheck=xf is not None)
    c, hm = halfinterval_c3(p, unc)
    assert c == c_ref
    c, hm2 = halfinterval_c3(p, ClassNumberPolicy('grh'))
    assert c == c_ref and hm2['status'] == 'GRH-conditional'
    assert nodal_flint_c(p) == c_ref
    rec['hi']['hi_uncond_status'] = hm['status']
    for mode in ('unconditional', 'grh'):
        r = acquire_aL(p, mode)
        assert (r['a_L'], r['c_p'], r['m_factorial'], r['D']) == (a_ref, c_ref, mf, D_ref)
        rec['api'][mode] = dict(route=r['route'], q=r['q'], status=r['status'])
    rec['seconds'] = perf_counter() - t0
    return rec


def main():
    import confirm, confirm_charp
    confirm.verify_freeze()
    confirm_charp.verify_freeze_charp()
    fr = verify_freeze_r3()
    sel = select()
    out = dict(status='RUNNING', python=sys.version, platform=platform.platform(),
               freeze_timestamp=fr['timestamp_utc'], selection=sel, cases=[])
    jobs = []
    for X in CLASSES:
        jobs += [(p, [q], True, 'S') for q, p in sel['S'][X].items()]
        jobs += [(p, [q], False, 'M') for q, p in sel['M'][X].items()]
        jobs += [(p, [q], False, 'L') for q, p in sel['L'][X].items()]
        jobs += [(p, QM, False, 'E1') for p in sel['E1'][X]]
        jobs += [(p, [q], False, 'E2') for q, p in sel['E2'][X].items()]
        jobs += [(p, QM, False, 'E4') for p in sel['E4'][X]]
    jobs += [(p, QM, True, 'E3') for p in sel['E3']['A']]
    for p, ql, small, tag in jobs:
        rec = check_prime(p, ql, small)
        rec['set'] = tag
        if tag == 'E1':
            assert not admissible_q(p) and rec['api']['unconditional']['route'] != 'tal_split'
        if tag == 'E3':
            assert not admissible_q(p) and rec['api']['unconditional']['route'] != 'tal_split'
        out['cases'].append(rec)
        print(json.dumps(dict(set=tag, p=p, cls=rec['cls'], tal=len(rec['tal']), api=rec['api']['unconditional'],
                              s=round(rec['seconds'], 2))), flush=True)
    verify_freeze_r3()
    out['status'] = 'PASS'
    out['n_cases'] = len(out['cases'])
    out['n_tal_checks'] = sum(len(r['tal']) for r in out['cases'])
    (ROOT / 'r3/evidence/CONFIRMATION_R3.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
    print('PASS', out['n_cases'], 'primes', out['n_tal_checks'], 'tal checks')


if __name__ == '__main__':
    main()
