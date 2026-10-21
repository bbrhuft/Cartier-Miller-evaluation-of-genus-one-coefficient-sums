"""Reference checks for the accompanying mathematical brief.

Python 3, standard library only.
Not executed in the originating chat: review and run before relying on it.
This checks algebraic identities, not the fast evaluator or its complexity.
"""
import json
import random


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def remainder(a, b, p):
    a, b = trim(a), trim(b)
    inv = pow(b[-1], -1, p)
    while len(a) >= len(b):
        shift = len(a) - len(b)
        q = a[-1] * inv % p
        for j, v in enumerate(b):
            a[shift + j] = (a[shift + j] - q * v) % p
        a = trim(a)
    return a


def squarefree(f, p):
    derivative = [(i * f[i]) % p for i in range(1, len(f))]
    a, b = trim(f), trim(derivative)
    while b:
        a, b = b, remainder(a, b, p)
    return len(a) == 1


def evaluate(f, x, p):
    value = 0
    for coefficient in reversed(f):
        value = (value * x + coefficient) % p
    return value


def multiply(a, b, p):
    result = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            result[i + j] = (result[i + j] + u * v) % p
    return result


def polynomial_power(f, exponent, p):
    result = [1]
    for _ in range(exponent):
        result = multiply(result, f, p)
    return result


def character(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def inverse(a, p):
    return pow(a % p, -1, p)


def check_model(f, p):
    h = (p - 1) // 2
    epsilon = [character(evaluate(f, x, p), p) for x in range(p)]

    # Independent enumeration of actual affine points.
    fibre_counts = [
        sum((y * y - evaluate(f, x, p)) % p == 0 for y in range(p))
        for x in range(p)
    ]
    assert fibre_counts == [1 + e for e in epsilon]

    n_infinity = 1 if len(f) == 4 else 1 + character(f[-1], p)
    trace = p + 1 - (sum(fibre_counts) + n_infinity)
    assert sum(epsilon) == 1 - n_infinity - trace

    power = polynomial_power(f, h, p)
    truncation = power[:p]
    derivative = [(i * f[i]) % p for i in range(1, len(f))]

    direct = {}
    admissible = []

    for mu in range(p):
        direct[mu] = sum(
            epsilon[x] * inverse(x - mu, p)
            for x in range(p) if x != mu
        ) % p

        point_sum = sum(
            fibre_counts[x] * inverse(x - mu, p)
            for x in range(p) if x != mu
        ) % p
        assert point_sum == direct[mu]

        # Polynomial-division identity, also tested at nonzero branch values.
        if mu:
            identity = (
                (evaluate(truncation, mu, p) - epsilon[mu])
                * inverse(mu, p)
                - evaluate(
                    [(i * power[i]) % p for i in range(1, len(power))],
                    mu, p
                )
            ) % p
            assert identity == direct[mu]

        # The normalized, nonbranch identity from the brief.
        if mu and epsilon[mu]:
            value = evaluate(f, mu, p)
            predicted = (
                (evaluate(truncation, mu, p) - epsilon[mu])
                * inverse(mu, p)
                + epsilon[mu] * evaluate(derivative, mu, p)
                * inverse(2 * value, p)
            ) % p
            assert predicted == direct[mu]
            admissible.append(mu)

    multi_checks = 0
    for size in range(1, min(3, len(admissible)) + 1):
        poles = admissible[:size]
        weights = list(range(1, size + 1))

        finite_parts = [
            sum(
                weights[j] * inverse(poles[k] - poles[j], p)
                for j in range(size) if j != k
            ) % p
            for k in range(size)
        ]

        oracle_part = sum(
            weights[j] * direct[poles[j]] for j in range(size)
        ) % p

        predicted_character = (
            oracle_part
            - sum(epsilon[poles[k]] * finite_parts[k]
                  for k in range(size))
        ) % p

        predicted_points = (
            oracle_part
            - sum(fibre_counts[poles[k]] * finite_parts[k]
                  for k in range(size))
        ) % p

        for constant in (0, 3):
            actual_character = 0
            actual_points = 0
            for x in range(p):
                if x in poles:
                    continue
                weight = (
                    constant
                    + sum(weights[j] * inverse(x - poles[j], p)
                          for j in range(size))
                ) % p
                actual_character += epsilon[x] * weight
                actual_points += fibre_counts[x] * weight

            char_constant = constant * (
                1 - n_infinity - trace
                - sum(epsilon[mu] for mu in poles)
            )
            point_constant = constant * (
                p + 1 - n_infinity - trace
                - sum(fibre_counts[mu] for mu in poles)
            )

            assert actual_character % p == (
                predicted_character + char_constant
            ) % p
            assert actual_points % p == (
                predicted_points + point_constant
            ) % p
            multi_checks += 1

    return {
        "p": p,
        "degree": len(f) - 1,
        "f": f,
        "trace": trace,
        "single_pole_checks": p,
        "admissible_coefficient_checks": len(admissible),
        "multi_pole_constant_checks": multi_checks,
    }


def main():
    rng = random.Random(20261020)
    records = []

    for p in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        for degree in (3, 4):
            accepted = 0
            while accepted < 6:
                f = (
                    [1]
                    + [rng.randrange(p) for _ in range(degree - 1)]
                    + [rng.randrange(1, p)]
                )
                if not squarefree(f, p):
                    continue
                records.append(check_model(f, p))
                accepted += 1

    # Reproduce the example in the originating discussion.
    example = check_model([1, 1, 0, 1], 101)
    p, mu = 101, 2
    value = sum(
        character(1 + x + x**3, p) * inverse(x - mu, p)
        for x in range(p) if x != mu
    ) % p
    assert value == 48

    print(json.dumps({
        "status": "PASS",
        "scope": "Reference identities only; no Miller implementation tested",
        "models": len(records),
        "trace_plus_one_models": sum(r["trace"] == 1 for r in records),
        "trace_minus_one_models": sum(r["trace"] == -1 for r in records),
        "example": {"model": example, "mu": mu, "character_sum": value},
        "records": records,
    }, indent=2))


if __name__ == "__main__":
    main()