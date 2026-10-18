"""Build the complete project input ledger (rounds 1-3) -> r3/evidence/LEDGER_R3.json.

Ranges are stored as rules; explicit primes are listed.  Round-3 development inputs include the
scratch probes run before this script existed (regenerated here deterministically from their rules).
"""
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from r3.common import is_prime


def first(S, q):
    p = S
    while not (p % 6 == 5 and p % q == 1 and is_prime(p)):
        p += 1
    return p


def main():
    ev = ROOT / 'evidence'
    fr1 = json.loads((ev / 'FREEZE.json').read_text())
    c1 = json.loads((ev / 'CONFIRMATION.json').read_text())['selection']
    fr2 = json.loads((ev / 'charp/FREEZE_CHARP.json').read_text())
    c2 = json.loads((ev / 'charp/CONFIRMATION_CHARP.json').read_text())['selection']
    explicit = set(fr1['development_primes']) | set(c1['small']) | set(c1['benchmark_primes'])
    explicit |= set(fr2['pilot_primes'])
    for v in c2['small'].values():
        explicit |= set(v)
    for v in c2['large'].values():
        explicit |= set(v)
    r3 = set()
    dt = json.loads((ROOT / 'r3/evidence/DEV_TIMING.json').read_text())
    r3 |= {r['p'] for r in dt['rows']}
    st = json.loads((ROOT / 'r3/evidence/DEV_SVP_TABLE.json').read_text())
    r3 |= {r['p'] for r in st['rows']}
    # scratch probes (before evidence files existed), regenerated from their rules
    for S in (5 * 10 ** 9, 5 * 10 ** 10, 5 * 10 ** 11):          # first (crashed) timing run
        for q in (11, 23, 31, 47, 53, 61, 67, 71):
            r3.add(first(S, q))
    for S in (2 * 10 ** 10, 2 * 10 ** 12):                        # LLL cost probes
        for q in (11, 23, 47, 97, 151, 199):
            r3.add(first(S, q))
    for q in (53, 59, 61, 67, 71, 73, 79, 83, 89):                 # FLINT LLL range probe
        r3.add(first(5 * 10 ** 10 + 7 * q, q))
    r3 |= {5999999993, 19999999943, 2000000063, 2000000033, 2000000141}   # class-number timing probes
    r3 |= {200159}                                                       # selector dry-run probe
    rules = [
        dict(rule='all primes p < 200000', source='round-2 development; round-3 Tal development tests'),
        dict(rule='all primes p = 5 (mod 12), p < 1000000', source='round-3 Williams-Currie check and quarter-sign experiment'),
        dict(rule='all primes p < 3000', source='round-3 brute-force Jacobi-sum tests'),
    ]
    out = dict(role='Complete project input ledger; confirmation inputs must avoid every entry',
               range_rules=rules, explicit_round1_round2=sorted(explicit), explicit_round3_dev=sorted(r3))
    (ROOT / 'r3/evidence/LEDGER_R3.json').write_text(json.dumps(out, indent=1) + '\n')
    print(len(explicit), 'round-1/2 explicit;', len(r3), 'round-3 explicit')


def excluded(p, _cache=[]):
    if not _cache:
        L = json.loads((ROOT / 'r3/evidence/LEDGER_R3.json').read_text())
        _cache.append(set(L['explicit_round1_round2']) | set(L['explicit_round3_dev']))
    if p < 200000:
        return True
    if p % 12 == 5 and p < 1000000:
        return True
    return p in _cache[0]


if __name__ == '__main__':
    main()
