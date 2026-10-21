"""Matched residues for character-sum benchmarks; not a timing harness.

Inputs are a prime p>=7, a cubic/quartic with nonzero leading coefficient,
and a residue a. Squarefreeness is part of the benchmark input contract,
although the coefficient identity itself also works for singular inputs.
The module uses no inherited Cartier–Miller code or trace.
"""
from math import comb


def evaluate(f, x, p):
    value = 0
    for c in reversed(f):
        value = (value * x + c) % p
    return value


def derivative(f, p):
    return [(j * f[j]) % p for j in range(1, len(f))]


def taylor_shift(f, a, p):
    """Constant-degree Taylor shift, independent of the inherited helper."""
    d = len(f) - 1
    return [sum(f[i] * comb(i, j) * pow(a, i - j, p)
                for i in range(j, d + 1)) % p for j in range(d + 1)]


def coefficient_scaled(g, h, N, p):
    """[z^N]g^h, 0<=N<p, in O(N) field work at fixed degree.

    Stores u_k=k!g[0]^k e_k and the last deg(g) states. One final
    inversion restores e_N. This is a LINEAR comparator, not BGS.
    """
    if not 0 <= N < p or g[0] % p == 0:
        raise ValueError('require 0 <= N < p and nonzero g[0]')
    d = len(g) - 1
    if d < 1:
        return pow(g[0], h, p) if N == 0 else 0
    powers = [pow(g[0], j, p) for j in range(d)]
    history = [pow(g[0], h, p)] + [0] * (d - 1)
    scale = 1
    for k in range(1, N + 1):
        u, falling = 0, 1
        for j in range(1, min(d, k) + 1):
            if j > 1:
                falling = falling * (k - j + 1) % p
            term = (((h + 1) * j - k) * g[j]) % p
            u = (u + term * powers[j - 1] * falling * history[j - 1]) % p
        history = [u] + history[:-1]
        scale = scale * k % p * g[0] % p
    return history[0] * pow(scale, -1, p) % p


def reverse_coefficient_sum(f, a, p):
    """C_f(a) from one reversed-polynomial coefficient; no trace required.

    Includes zero and branch poles. O(p) field work and O(1) working
    field elements at fixed degree. Not an optimized native baseline.
    """
    f = [c % p for c in f]
    if p < 7 or len(f) not in (4, 5) or not f[-1]:
        raise ValueError('require p>=7 and exact degree 3 or 4')
    a %= p
    h, d = (p - 1) // 2, len(f) - 1
    g = list(reversed(taylor_shift(f, a, p)))
    N = d * h - p
    high_value = coefficient_scaled(g, h, N, p)
    Fprime = h * pow(evaluate(f, a, p), h - 1, p) % p
    Fprime = Fprime * evaluate(derivative(f, p), a, p) % p
    return (-Fprime - high_value) % p


def character_tables(f, p):
    """Independent direct enumeration: enumerate actual y squares, no Euler criterion.

    Tables cost O(p) time/storage. Charge them in cold enumeration workloads.
    """
    counts = [0] * p
    for y in range(p):
        counts[y * y % p] += 1
    fibres = [counts[evaluate(f, x, p)] for x in range(p)]
    epsilon = [nu - 1 for nu in fibres]
    inverses = [0] * p
    inverses[1] = 1
    for t in range(2, p):
        inverses[t] = -(p // t) * inverses[p % t] % p
    return epsilon, fibres, inverses


def direct_single(epsilon, inverses, a, p):
    return sum(epsilon[x] * inverses[(x - a) % p]
               for x in range(p) if x != a) % p


def direct_weighted(values, inverses, poles, weights, constant, p):
    """One common excluded set; zero weights permit extra exclusions."""
    if len(poles) != len(weights) or len(set(poles)) != len(poles):
        raise ValueError('distinct poles and a matching coefficient vector required')
    excluded = set(poles)
    total = 0
    for x in range(p):
        if x in excluded:
            continue
        R = (constant + sum(v * inverses[(x - a) % p]
                            for a, v in zip(poles, weights))) % p
        total = (total + values[x] * R) % p
    return total


def multiply(a, b, p):
    result = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            result[i + j] = (result[i + j] + u * v) % p
    return result


def polynomial_power(f, h, p):
    """Schoolbook reference only. Use FLINT/native arithmetic in headline timings."""
    result, base = [1], list(f)
    while h:
        if h & 1:
            result = multiply(result, base, p)
        h >>= 1
        if h:
            base = multiply(base, base, p)
    return result


def full_power_sum(coefficients, a, p):
    """All-point identity C_f(a)=-H_high(a)-F'(a)."""
    return (-evaluate(coefficients[p:], a, p)
            - evaluate(derivative(coefficients, p), a, p)) % p


def common_domain_from_scalars(single_values, epsilon, poles, weights, constant, p):
    """Exact O(s^2) correction; same adapter can serve each scalar method."""
    finite = [sum(weights[j] * pow((a - poles[j]) % p, -1, p)
                  for j in range(len(poles)) if j != k) % p
              for k, a in enumerate(poles)]
    value = sum(v * single_values[a] for a, v in zip(poles, weights))
    value -= sum(epsilon[a] * finite[k] for k, a in enumerate(poles))
    value += constant * (sum(epsilon) - sum(epsilon[a] for a in poles))
    return value % p, (-constant * len(poles) - sum(finite)) % p


def squarefree(f, p):
    def trim(a):
        while a and a[-1] == 0:
            a.pop()
        return a

    a, b = trim(list(f)), trim(derivative(f, p))
    while b:
        r = a[:]
        inv = pow(b[-1], -1, p)
        while len(r) >= len(b):
            q, offset = r[-1] * inv % p, len(r) - len(b)
            for j, v in enumerate(b):
                r[offset + j] = (r[offset + j] - q * v) % p
            trim(r)
        a, b = b, r
    return len(a) == 1
