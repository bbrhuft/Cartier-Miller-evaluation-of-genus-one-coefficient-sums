"""Optional optimized comparator: FLINT 3 (C) through ctypes, using the libflint shipped
inside the python-flint wheel (pip install python-flint). Not needed by the stdlib core.

Provides
  flint_factorial(n, p)              FLINT's own n_factorial_fast_mod2_preinv (n! mod p)
  flint_rising(p, L, starts)         prod_{i<L}(a+i) mod p for each a in starts, block method:
                                     one product-roots polynomial per channel, ONE shared
                                     subproduct tree of evaluation points, FLINT fast
                                     multipoint evaluation (_nmod_poly_evaluate_nmod_vec_fast_precomp).
All arithmetic is word-size (p < 2^63 here). Cold calls: every call builds its own trees.
"""
import ctypes as C
import glob
import os
from math import isqrt

_lib = None


def lib():
    global _lib
    if _lib is None:
        import flint  # noqa: F401  (locates the wheel)
        base = os.path.join(os.path.dirname(os.path.dirname(flint.__file__)), 'python_flint.libs')
        path = sorted(glob.glob(os.path.join(base, 'libflint*.so*')))[0]
        L = C.CDLL(path)
        L.n_preinvert_limb.restype = C.c_ulong
        L.n_preinvert_limb.argtypes = [C.c_ulong]
        L.n_factorial_fast_mod2_preinv.restype = C.c_ulong
        L.n_factorial_fast_mod2_preinv.argtypes = [C.c_ulong, C.c_ulong, C.c_ulong]
        L.nmod_init.argtypes = [C.POINTER(_nmod_t), C.c_ulong]
        L._nmod_poly_tree_alloc.restype = C.POINTER(C.POINTER(C.c_ulong))
        L._nmod_poly_tree_alloc.argtypes = [C.c_long]
        L._nmod_poly_tree_free.argtypes = [C.POINTER(C.POINTER(C.c_ulong)), C.c_long]
        L._nmod_poly_tree_build.argtypes = [C.POINTER(C.POINTER(C.c_ulong)), C.POINTER(C.c_ulong),
                                            C.c_long, _nmod_t]
        L._nmod_poly_product_roots_nmod_vec.argtypes = [C.POINTER(C.c_ulong), C.POINTER(C.c_ulong),
                                                        C.c_long, _nmod_t]
        L._nmod_poly_evaluate_nmod_vec_fast_precomp.argtypes = [
            C.POINTER(C.c_ulong), C.POINTER(C.c_ulong), C.c_long,
            C.POINTER(C.POINTER(C.c_ulong)), C.c_long, _nmod_t]
        _lib = L
    return _lib


class _nmod_t(C.Structure):
    _fields_ = [('n', C.c_ulong), ('ninv', C.c_ulong), ('norm', C.c_ulong)]


def flint_version():
    import flint
    return dict(python_flint=flint.__version__)


def flint_factorial(n, p):
    L = lib()
    return L.n_factorial_fast_mod2_preinv(n, p, L.n_preinvert_limb(p))


def flint_rising(p, length, starts, block_size=None):
    """Block rising products with a shared evaluation tree (all channels same length)."""
    if p >= 1 << 63:
        raise ValueError('word-size prime required')
    if length == 0:
        return [1] * len(starts), dict(block_size=0, blocks=0, backend='flint')
    L = lib()
    mod = _nmod_t()
    L.nmod_init(C.byref(mod), p)
    w = block_size or max(1, isqrt(length))
    q = length // w
    out = []
    if q >= 1:
        xs = (C.c_ulong * q)(*[(k * w) % p for k in range(q)])
        tree = L._nmod_poly_tree_alloc(q)
        L._nmod_poly_tree_build(tree, xs, q, mod)
        ys = (C.c_ulong * q)()
        for a in starts:
            roots = (C.c_ulong * w)(*[(-(a + i)) % p for i in range(w)])
            poly = (C.c_ulong * (w + 1))()
            L._nmod_poly_product_roots_nmod_vec(poly, roots, w, mod)   # prod (X - root)
            L._nmod_poly_evaluate_nmod_vec_fast_precomp(ys, poly, w + 1, tree, q, mod)
            r = 1
            for v in ys:
                r = r * v % p
            for j in range(w * q, length):
                r = r * ((a + j) % p) % p
            out.append(r)
        L._nmod_poly_tree_free(tree, q)
    else:
        for a in starts:
            r = 1
            for j in range(length):
                r = r * ((a + j) % p) % p
            out.append(r)
    return out, dict(block_size=w, blocks=q, channels=len(starts), backend='flint', shared_tree=True)
