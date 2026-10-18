"""Round-3 interface: the signed a_L (and m!, c_p, D) from a certified prime p = 5 mod 6.

    python3 -m r3.acquire_r3 p [--mode unconditional|grh] [--q Q] [--route auto|tal|hi|nodal]

Contract: p is a certified prime, p >= 11, p = 5 (mod 6).  (is_prime() in r3.common is a
deterministic Miller-Rabin proof for p < 3.3e24 and may be used to certify.)

Routes and status labels:
  tal_split     unconditional   Rounded-third Tal split specialisation (r3/tal3.py) with a prime
                                q | p-1, 5 <= q <= 89 (frozen range); no class number.
  half_interval unconditional   c = 2 H P^3 with H from Mordell / Williams-Currie and a class
                                number from PARI qfbclassno inside |D| < 2e10 (documented
                                unconditional range) or the reduced-form count outside it.
  half_interval GRH-conditional same, class number from PARI quadclassunit (mode='grh').
  nodal_flint   unconditional   round-1 nodal anchor in the FLINT block engine.
  experimental                  tal_split with a user-forced q outside the frozen range.
The automatic policy (POLICY_R3.json, frozen) picks the admissible q minimising a calibrated cost
model and compares it with the fallback (half_interval if its class number is unconditional and in
range, else nodal_flint; in mode 'grh' the GRH half_interval is the fallback).
"""
import argparse
import json
import math
import sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from r3.common import params, ClassNumberPolicy, flint_rising, is_prime
from r3 import tal3
from r3.halfint import halfinterval_c3

POLICY_PATH = Path(__file__).resolve().parent / 'POLICY_R3.json'
_POLICY = []


def policy():
    if not _POLICY:
        _POLICY.append(json.loads(POLICY_PATH.read_text()))
    return _POLICY[0]


def svp_cost(q):
    tab = {int(k): v for k, v in policy()['svp_table_s'].items()}
    if q in tab:
        return tab[q]
    ks = sorted(tab)
    lo = max(k for k in ks if k < q)
    hi = min(k for k in ks if k > q)
    t = (math.log(q) - math.log(lo)) / (math.log(hi) - math.log(lo))
    return math.exp((1 - t) * math.log(tab[lo]) + t * math.log(tab[hi]))


def interval_cost(L):
    m = policy()['interval_model']
    return 0.0 if L <= 0 else m['B'] * L ** m['gamma']


def tal_cost(p, q):
    anchor = tal3.default_anchor(p)
    R = tal3.residuals(p, q, anchor)
    return svp_cost(q) + interval_cost(R['len_m']) + interval_cost(R['len_a'])


def hi_in_range(p):
    D = p if p % 4 == 3 else 3 * p
    return D < 2 * 10 ** 10


def fallback(p, mode):
    if mode == 'grh':
        return 'half_interval', interval_cost((p + 1) // 6) + policy()['hi_classno_overhead_s']
    if hi_in_range(p):
        return 'half_interval', interval_cost((p + 1) // 6) + policy()['hi_classno_overhead_s']
    m = policy()['nodal_model']
    return 'nodal_flint', m['C'] * p ** m['delta']


def admissible_q(p):
    pol = policy()
    lo, hi = pol['q_range']
    out = []
    for q in range(lo, hi + 1):
        if is_prime(q) and (p - 1) % q == 0 and (p - 1) // q >= pol['K_min']:
            out.append(q)
    return out


def select(p, mode='unconditional'):
    """Frozen decision: (route, q or None, predicted costs)."""
    fb, fcost = fallback(p, mode)
    cands = {q: tal_cost(p, q) for q in admissible_q(p)}
    if cands:
        qbest = min(cands, key=lambda q: (cands[q], -q))
        if cands[qbest] < fcost:
            return 'tal_split', qbest, dict(tal=cands, fallback=(fb, fcost))
    return fb, None, dict(tal=cands, fallback=(fb, fcost))


def nodal_flint_c(p):
    P = params(p)
    N = P['N']
    inv3 = pow(3, p - 2, p)
    chi = 1 if pow(6, (p - 1) // 2, p) == 1 else p - 1
    (num, den), _ = flint_rising(p, N, [4 * inv3 % p, 1])
    return -4 * inv3 * chi * pow(-1, N, p) * num * pow(den, p - 2, p) % p


def acquire_aL(p, mode='unconditional', q=None, route='auto'):
    """Return dict with a_L, c_p, m!, D and metadata (status label, route, timings)."""
    import atkin
    t0 = perf_counter()
    params(p)
    if mode not in ('unconditional', 'grh'):
        raise ValueError(mode)
    meta = {}
    if route == 'auto' and q is None:
        route, q, pred = select(p, mode)
        meta['policy_prediction_s'] = dict(tal={str(k): v for k, v in pred['tal'].items()},
                                           fallback=list(pred['fallback']))
    elif route == 'auto':
        route = 'tal_split'
    if route == 'tal_split' and q is None:
        cands = admissible_q(p)
        if not cands:
            raise ValueError('no admissible prime q in the frozen range divides p-1')
        q = min(cands, key=lambda x: (tal_cost(p, x), -x))
    t_sel = perf_counter()
    if route == 'tal_split':
        lo, hi = policy()['q_range']
        c, m = tal3.acquire(p, q)
        status = 'unconditional' if lo <= q <= hi else 'experimental'
        meta.update(m)
    elif route == 'hi':
        route = 'half_interval'
    if route == 'half_interval':
        c, m = halfinterval_c3(p, ClassNumberPolicy('grh' if mode == 'grh' else 'unconditional'))
        status = m['status']
        meta.update(m)
    elif route in ('nodal', 'nodal_flint'):
        route = 'nodal_flint'
        c = nodal_flint_c(p)
        status = 'unconditional'
    if route not in ('tal_split', 'half_interval', 'nodal_flint'):
        raise ValueError(route)
    aL = 3 * c * pow(4, p - 2, p) % p
    mf = tal3.mfact_from_c(p, c)
    D = atkin.derivative_from_c(p, c)
    t1 = perf_counter()
    meta['route'] = route
    return dict(p=p, a_L=aL, c_p=c, m_factorial=mf, D=D, route=route, q=q, status=status,
                mode=mode, seconds=dict(select=t_sel - t0, total=t1 - t0), metadata=meta)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('p', type=int)
    ap.add_argument('--mode', choices=['unconditional', 'grh'], default='unconditional')
    ap.add_argument('--q', type=int, default=None)
    ap.add_argument('--route', choices=['auto', 'tal', 'hi', 'nodal'], default='auto')
    a = ap.parse_args()
    if not is_prime(a.p):
        sys.exit('p is not prime')
    r = acquire_aL(a.p, a.mode, a.q, {'tal': 'tal_split'}.get(a.route, a.route))
    print(json.dumps(r, indent=2, default=str))
