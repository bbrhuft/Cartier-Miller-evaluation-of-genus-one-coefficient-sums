"""Round-2 frozen confirmation (characteristic-p half-interval candidate).

Verifies both freezes, selects primes by the rule in CANDIDATE_CHARP.md, and checks every
case against independent references. Requires python-flint (reference factorials, FLINT
engine) and optionally cypari2 (class-number cross-check). Writes
evidence/charp/CONFIRMATION_CHARP.json. No candidate edits during confirmation.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path
from time import perf_counter
sys.dont_write_bytecode = True
from confirm import verify_freeze
from develop import prime
from atkin import nodal_c, factorial_c, parameters
from charp import classno, half_factorial, halfinterval_c
from flint_backend import flint_factorial, flint_rising, flint_version

ROOT = Path(__file__).resolve().parent
CLASSES = {'A_11mod12': (12, 11), 'B_5mod24': (24, 5), 'C_17mod24': (24, 17)}


def verify_freeze_charp():
    fr = json.loads((ROOT / 'evidence/charp/FREEZE_CHARP.json').read_text())
    for name, digest in fr['sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    return fr


def development_set(fr):
    old = json.loads((ROOT / 'evidence/FREEZE.json').read_text())['development_primes']
    oldc = json.loads((ROOT / 'evidence/CONFIRMATION.json').read_text())['selection']
    s = set(old) | set(oldc['small']) | set(oldc['benchmark_primes']) | set(fr['pilot_primes'])
    return s, fr['development_below']


def first(lower, modulus, residue, excluded, below, count=1):
    out, p = [], lower
    while len(out) < count:
        if p % modulus == residue and p not in excluded and p >= below and prime(p):
            out.append(p)
        p += 1
    return out


def select(fr):
    excluded, below = development_set(fr)
    small = {c: first(300001, mo, r, excluded, below, 3) for c, (mo, r) in CLASSES.items()}
    large = {c: [first(2 * 10 ** k, mo, r, excluded, below)[0] for k in range(6, 12)]
             for c, (mo, r) in CLASSES.items()}
    return small, large


def pari_classno():
    try:
        import cypari2
        pari = cypari2.Pari()
        return lambda D: int(pari.quadclassunit(D)[0]), 'PARI ' + '.'.join(map(str, pari.version()))
    except Exception as exc:
        return None, 'unavailable: %s' % exc


def check(p, pari):
    t0 = perf_counter()
    m, h = (p - 2) // 3, (p - 1) // 2
    mf = flint_factorial(m, p)
    c_ref = 2 * pow(mf, 3 * (p - 2), p) % p
    H_ref = flint_factorial(h, p)
    rec = dict(p=p, c_ref=c_ref, H_ref=H_ref, routes={}, classno={}, methods={})
    if p <= 2 * 10 ** 6:
        lin, _ = factorial_c(p, 'linear')
        assert lin == c_ref
        rec['stdlib_linear_reference'] = True
    routes = ['mordell'] if p % 4 == 3 else (['gauss4p', 'h3p'] if p % 8 == 5 else ['h3p'])
    for route in routes:
        H, meta = half_factorial(p, route)
        rec['routes'][route] = dict(H=H, ok=(H == H_ref), D=meta['D'], h=meta['classno'], status=meta['status'])
        assert H == H_ref, (p, route)
        if pari:
            hp = pari(meta['D'])
            rec['classno'][str(meta['D'])] = dict(forms=meta['classno'], pari=hp)
            assert hp == meta['classno']
    for layout in (1, 2):
        c, _ = halfinterval_c(p, layout=layout, product_fn=flint_rising)
        rec['methods']['flint_hi%d' % layout] = (c == c_ref)
        assert c == c_ref
        if p <= 2 * 10 ** 9:
            c, _ = halfinterval_c(p, layout=layout)
            rec['methods']['std_hi%d' % layout] = (c == c_ref)
            assert c == c_ref
    if p <= 2 * 10 ** 9:
        c, _ = nodal_c(p, 'shared')
        rec['methods']['std_nodal_shared'] = (c == c_ref)
        assert c == c_ref
    rec['seconds'] = perf_counter() - t0
    rec['pass_'] = True
    return rec


def main():
    verify_freeze()
    fr = verify_freeze_charp()
    small, large = select(fr)
    pari, pari_name = pari_classno()
    out = dict(status='PASS', python=sys.version, platform=platform.platform(), flint=flint_version(),
               class_number_crosscheck=pari_name,
               role='Round-2 post-freeze exact confirmation; constant-factor method, not an exponent claim',
               selection=dict(small=small, large=large), cases=[])
    for p in sorted({q for v in small.values() for q in v} | {q for v in large.values() for q in v}):
        rec = check(p, pari)
        out['cases'].append(rec)
        print(json.dumps(dict(p=p, routes={k: v['ok'] for k, v in rec['routes'].items()},
                              seconds=round(rec['seconds'], 2))), flush=True)
    verify_freeze_charp()
    (ROOT / 'evidence/charp/CONFIRMATION_CHARP.json').write_text(json.dumps(out, indent=2) + '\n')


if __name__ == '__main__':
    main()
