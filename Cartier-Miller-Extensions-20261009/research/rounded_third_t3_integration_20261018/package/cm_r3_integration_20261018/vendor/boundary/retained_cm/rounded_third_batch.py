"""Exact rounded-third batch evaluation. Python >= 3.10; no required dependencies.

Later recurrence matrices multiply on the LEFT. The forest retains only one
prefix matrix, reduced modulo the product of primes still to be processed.
The independent verification code is deliberately outside this module.
"""
from __future__ import annotations

from math import isqrt
from typing import NamedTuple

VERSION = "1.0.0"
HEADER = ("p", "B_L", "a_L", "U_p_L", "G")


class Row(NamedTuple):
    p: int
    B_L: int
    a_L: int
    U_p_L: int
    G: int


def _positive_integer(value, name, minimum=1):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def branch_primes(bound: int) -> list[int]:
    """All primes 11 <= p < bound with p == 2 (mod 3), by an exact sieve."""
    _positive_integer(bound, "bound", 0)
    if bound <= 11:
        return []
    sieve = bytearray(b"\x01") * bound
    sieve[0:2] = b"\x00\x00"
    for q in range(2, isqrt(bound - 1) + 1):
        if sieve[q]:
            sieve[q * q:bound:q] = b"\x00" * len(range(q * q, bound, q))
    return [p for p in range(11, bound, 6) if sieve[p]]


def mul(left, right):
    """Upper-triangular matrix multiplication; triples encode (A,B,D)."""
    a, b, d = left
    e, f, g = right
    return a * e, a * f + b * g, d * g


def reduce_matrix(matrix, modulus):
    return tuple(c % modulus for c in matrix)


def balanced_product(values, integer=int):
    level = [integer(v) for v in values]
    if not level:
        return integer(1)
    while len(level) > 1:
        level = [level[i] * level[i + 1] for i in range(0, len(level) - 1, 2)] + (
            level[-1:] if len(level) % 2 else [])
    return level[0]


def interval_product(start, stop, integer=int):
    """Exact M_(stop-1)...M_start; balanced recursion for longer intervals."""
    if not 0 <= start <= stop:
        raise ValueError("need 0 <= start <= stop")
    if stop - start <= 16:
        a, b, d = integer(1), integer(0), integer(1)
        for j in range(start, stop):
            t = 4 * (j + 1)
            a, b, d = t * a, t * (b + d), (2 * j + 1) * d
        return a, b, d
    mid = (start + stop) // 2
    return mul(interval_product(mid, stop, integer), interval_product(start, mid, integer))


def remainder_tree(products, moduli, carry):
    """Inclusive prefix residues and exact full product, preserving leaf order."""
    if not products or len(products) != len(moduli):
        raise ValueError("nonempty products and moduli must have the same length")
    pt, nt = [list(products)], [list(moduli)]
    while len(pt[-1]) > 1:
        p, n = pt[-1], nt[-1]
        pp, nn = [], []
        for i in range(0, len(p) - 1, 2):
            pp.append(mul(p[i + 1], p[i]))
            nn.append(n[i] * n[i + 1])
        if len(p) % 2:
            pp.append(p[-1])
            nn.append(n[-1])
        pt.append(pp)
        nt.append(nn)
    top = pt[-1][0]
    residues = [reduce_matrix(carry, nt[-1][0])]
    for level in range(len(pt) - 1, 0, -1):
        child_p, child_n = pt[level - 1], nt[level - 1]
        next_residues = []
        for i, r in enumerate(residues):
            k = 2 * i
            next_residues.append(reduce_matrix(r, child_n[k]))
            if k + 1 < len(child_p):
                next_residues.append(reduce_matrix(mul(child_p[k], r), child_n[k + 1]))
        residues = next_residues
        pt[level] = nt[level] = None
    result = [reduce_matrix(mul(p, r), n) for p, r, n in zip(products, residues, moduli)]
    return result, top


def decode(p, matrix):
    denominator, prefix, boundary = (int(c) for c in matrix)
    L = (p + 1) // 3
    inverse = pow(denominator, -1, p)
    B, a = prefix * inverse % p, boundary * inverse % p
    G = denominator * pow(pow(4, L, p) * L % p, -1, p) % p
    U = (4 * B - 2 * L * (2 * L + 5) * a) % p
    return Row(p, B, a, U, G)


def integer_backend(name):
    if name not in ("python", "auto", "gmpy2"):
        raise ValueError("backend must be python, auto, or gmpy2")
    if name != "python":
        try:
            import gmpy2
        except ImportError:
            if name == "gmpy2":
                raise ImportError("gmpy2 requested but not installed") from None
        else:
            return gmpy2.mpz, f"gmpy2 {gmpy2.version()} (GMP {gmpy2.mp_version()})"
    return int, "python-int"


def _iter_rows(primes, chunks, backend, stats):
    _positive_integer(chunks, "chunks")
    integer, backend_label = integer_backend(backend)
    n = len(primes)
    stats.update(version=VERSION, backend=backend_label, rows=n, chunks_requested=chunks,
                 chunks_used=0, carry_updates=0, old_carry_multiplications=0,
                 recurrence_steps=0, largest_chunk_steps=0,
                 largest_chunk_modulus_bits=0, largest_remaining_modulus_bits=0)
    if not n:
        return
    size = (n + min(chunks, n) - 1) // min(chunks, n)
    remaining = balanced_product(primes, integer)
    stats["largest_remaining_modulus_bits"] = int(remaining.bit_length())
    carry = (integer(1), integer(0), integer(1))
    last_L = 0
    for lo in range(0, n, size):
        selected = primes[lo:lo + size]
        starts_at = last_L
        leaves = []
        for p in selected:
            L = (p + 1) // 3
            leaves.append(interval_product(last_L, L, integer))
            last_L = L
        moduli = [integer(p) for p in selected]
        current_modulus = balanced_product(moduli, integer)
        residues, top = remainder_tree(leaves, moduli, reduce_matrix(carry, current_modulus))
        stats["chunks_used"] += 1
        stats["recurrence_steps"] = last_L
        stats["largest_chunk_steps"] = max(stats["largest_chunk_steps"], last_L - starts_at)
        stats["largest_chunk_modulus_bits"] = max(
            stats["largest_chunk_modulus_bits"], int(current_modulus.bit_length()))
        remaining, rem = divmod(remaining, current_modulus)
        if rem:
            raise ArithmeticError("remaining modulus was not divisible by chunk modulus")
        if remaining != 1:
            carry = reduce_matrix(mul(top, carry), remaining)
            stats["carry_updates"] += 1
        # All chunk trees are gone before rows are yielded; no earlier C_j is retained.
        del leaves, moduli, top
        for p, matrix in zip(selected, residues):
            yield decode(p, matrix)
    k = stats["chunks_used"]
    stats["old_carry_multiplications"] = k * (k - 1) // 2


def iter_rows(bound, *, chunks=32, backend="python", stats=None):
    """Stream the complete tuples for all branch primes below an exclusive bound.

    The sieve and sorted prime list remain resident; tuples stream one chunk at
    a time. Passing chunks=1 gives a single accumulating remainder tree.
    """
    return _iter_rows(branch_primes(bound), chunks, backend, {} if stats is None else stats)


def evaluate(bound, *, chunks=32, backend="python", stats=None):
    return list(iter_rows(bound, chunks=chunks, backend=backend, stats=stats))
