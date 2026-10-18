"""Round-2 production API: c_p and A_n'(0) by the half-interval method.

  python3 acquire_charp.py p [--backend std|flint] [--classno forms|pari] [--layout 1|2]

Prime certification is the caller's contract. For p = 17 (mod 24) the method rests on the
CONJECTURAL identity (*) (finite evidence only); the output flags this. Timings include the
class number and the O(log p) conversion to the derivative.
"""
import argparse
import json
import sys
from time import perf_counter
sys.dont_write_bytecode = True
from atkin import derivative_from_c
from charp import classno, halfinterval_c


def acquire(p, backend='std', classno_backend='forms', layout=1):
    t = perf_counter()
    product_fn = None
    if backend == 'flint':
        from flint_backend import flint_rising
        product_fn = flint_rising
    cfn = classno
    if classno_backend == 'pari':
        import cypari2
        pari = cypari2.Pari()
        cfn = lambda D: int(pari.quadclassunit(D)[0])
    c, meta = halfinterval_c(p, layout=layout, classno_fn=cfn, product_fn=product_fn)
    d = derivative_from_c(p, c)
    meta['conditional'] = meta['half_factorial']['route'] == 'h3p' and p % 8 == 1
    return dict(p=p, c=c, derivative=d, backend=backend, classno=classno_backend,
                seconds=perf_counter() - t, metadata=meta)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('p', type=int)
    ap.add_argument('--backend', choices=['std', 'flint'], default='std')
    ap.add_argument('--classno', choices=['forms', 'pari'], default='forms')
    ap.add_argument('--layout', type=int, choices=[1, 2], default=1)
    a = ap.parse_args()
    print(json.dumps(acquire(a.p, a.backend, a.classno, a.layout), indent=2, default=str))
