"""Independent depth-three/four rational 2-isogeny audit; no timing claim.

True F_p isomorphism keys use square x-scalings. Exact path models remain
unscaled so every displayed quotient retains differential scale +1.
Root scans and complete short-model enumeration are validation-only O(p).
"""
from collections import deque
from pathlib import Path
import csv
import hashlib
import json
from math import factorial
import platform
import sys

MAX_P = 251
MAX_DEPTH = 4


def prime(p):
    return p >= 2 and all(p % d for d in range(2, int(p ** 0.5) + 1))


def invariant(A, B, p):
    disc = (4 * A ** 3 + 27 * B * B) % p
    assert disc
    return 1728 * 4 * A ** 3 * pow(disc, -1, p) % p


def coefficients(A, B, p):
    """Exact integer multinomial coefficients reduced mod p, O(p) terms."""
    h = (p - 1) // 2
    facts = [factorial(i) for i in range(h + 1)]
    out = []
    for k in (p - 1, p - 2):
        total = 0
        for i in range(h + 1):
            j = k - 3 * i
            ell = h - i - j
            if j >= 0 and ell >= 0:
                term = facts[h] // (facts[i] * facts[j] * facts[ell])
                total += term * pow(A, j, p) * pow(B, ell, p)
        out.append(total % p)
    return tuple(out)


def trace(A, B, p):
    h = (p - 1) // 2
    total = 0
    for x in range(p):
        f = (x ** 3 + A * x + B) % p
        chi = 0 if f == 0 else (1 if pow(f, h, p) == 1 else -1)
        total += chi
    return -total


def roots(A, B, p):
    return [q for q in range(p) if (q ** 3 + A * q + B) % p == 0]


def quotient(A, B, q, p):
    assert (q ** 3 + A * q + B) % p == 0
    return ((-4 * A - 15 * q * q) % p, (-8 * A * q - 22 * q ** 3) % p)


class Audit:
    def __init__(self, p):
        self.p = p
        self.square_scales = sorted({u * u % p for u in range(1, p)})
        self.key_cache = {}
        self.coeff_cache = {}

    def canonical(self, A, B):
        p = self.p
        A %= p
        B %= p
        if (A, B) not in self.key_cache:
            orbit = [(d * d * A % p, d ** 3 * B % p, d) for d in self.square_scales]
            aa, bb, scale = min(orbit)
            self.key_cache[(A, B)] = ((aa, bb), scale)
        return self.key_cache[(A, B)]

    def coeff(self, A, B):
        key = (A % self.p, B % self.p)
        if key not in self.coeff_cache:
            self.coeff_cache[key] = coefficients(*key, self.p)
        return self.coeff_cache[key]

    def seeds(self):
        p = self.p
        models = []
        if p % 3 == 1:
            models.extend((0, b) for b in range(1, p))
        if p % 4 == 1:
            models.extend((a, 0) for a in range(1, p))
        return sorted({self.canonical(*model)[0] for model in models})

    def graph(self, prune_dual=True, retain_edges=True, max_depth=MAX_DEPTH):
        p = self.p
        states = {}
        queue = deque()
        edges = []
        for seed in self.seeds():
            H, beta = self.coeff(*seed)
            assert H != 0 and beta == 0
            states[seed] = {'model': seed, 'seed': seed, 'depth': 0, 'forward_roots': [], 'slope': 0}
            queue.append(seed)
        while queue:
            key = queue.popleft()
            state = states[key]
            if max_depth is not None and state['depth'] == max_depth:
                continue
            A, B = state['model']
            H, beta = self.coeff(A, B)
            assert beta == state['slope'] * H % p
            for q in roots(A, B, p):
                target = quotient(A, B, q, p)
                target_key, scale = self.canonical(*target)
                dual = bool(state['forward_roots']) and q == -2 * state['forward_roots'][-1] % p
                if dual:
                    assert target_key == self.canonical(*self.path_models(state)[-2])[0]
                if prune_dual and dual:
                    continue
                Ht, bt = self.coeff(*target)
                assert Ht == H and bt == (2 * beta - q * H) % p
                Hc, bc = self.coeff(*target_key)
                assert Hc == Ht and bc == scale * bt % p
                # Canonical key is only graph identity; exact model stores +1 scales.
                first = target_key not in states
                if first:
                    states[target_key] = {'model': target, 'seed': state['seed'], 'depth': state['depth'] + 1,
                                          'forward_roots': state['forward_roots'] + [q],
                                          'slope': (2 * state['slope'] - q) % p}
                    queue.append(target_key)
                if retain_edges:
                    edges.append({'p': p, 'source_depth': state['depth'], 'source_A': A, 'source_B': B,
                                  'kernel_q': q, 'target_A': target[0], 'target_B': target[1],
                                  'target_key_A': target_key[0], 'target_key_B': target_key[1],
                                  'target_square_scale_to_key': scale, 'immediate_dual': dual,
                                  'first_class_discovery': first, 'H': H, 'beta': beta, 'target_beta': bt,
                                  'canonical_target_beta': bc})
        return states, edges

    def path_models(self, state):
        models = [state['seed']]
        for q in state['forward_roots']:
            models.append(quotient(*models[-1], q, self.p))
        return models

    def certificate(self, state):
        p = self.p
        path = self.path_models(state)
        inv_roots = []
        model = state['model']
        multiplier = 0
        for i, q in enumerate(reversed(state['forward_roots'])):
            root = -2 * pow(4, i, p) * q % p
            inv_roots.append(root)
            multiplier = (multiplier + root * pow(pow(2, i + 1, p), -1, p)) % p
            model = quotient(*model, root, p)
        m = state['depth']
        d = pow(4, m, p)
        expected_endpoint = (d * d * state['seed'][0] % p, d ** 3 * state['seed'][1] % p)
        assert model == expected_endpoint
        assert multiplier == state['slope']
        H, beta = self.coeff(*state['model'])
        assert beta == H * multiplier % p
        key, scale = self.canonical(*state['model'])
        return {'p': p, 'depth': m, 'seed': list(state['seed']), 'forward_models': [list(x) for x in path],
                'forward_roots': state['forward_roots'], 'target': list(state['model']),
                'target_canonical_key': list(key), 'target_square_scale_to_key': scale,
                'j': invariant(*state['model'], p), 'H': H, 'beta': beta,
                'inverse_roots': inv_roots, 'inverse_endpoint': list(model),
                'inverse_beta_multiplier': multiplier, 'differential_scales': [1] * m}

    def all_classes(self):
        p = self.p
        seen = set()
        classes = []
        for A in range(p):
            for B in range(p):
                if (A, B) in seen or (4 * A ** 3 + 27 * B * B) % p == 0:
                    continue
                orbit = {(d * d * A % p, d ** 3 * B % p) for d in self.square_scales}
                key = min(orbit)
                seen.update(orbit)
                tau = trace(*key, p)
                H, beta = self.coeff(*key)
                assert tau % p == H
                classes.append({'p': p, 'A': key[0], 'B': key[1], 'j': invariant(*key, p),
                                'trace': tau, 'H': H, 'beta': beta, 'ordinary': H != 0,
                                'rational_two_torsion_roots': len(roots(*key, p))})
        assert len(seen) == p * p - p
        return classes


def write_csv(path, rows):
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    out = Path(__file__).resolve().parent
    summaries = []
    all_edges = []
    all_classes = []
    certificates = []
    misses = []
    saturated_summary = []
    total_coeff_models = 0
    first_twist_only = []
    for p in [p for p in range(7, MAX_P + 1) if prime(p)]:
        audit = Audit(p)
        states, edges = audit.graph(prune_dual=True)
        baseline, _ = audit.graph(prune_dual=False, retain_edges=False)
        assert set(states) == set(baseline)
        assert {key: value['depth'] for key, value in states.items()} == {key: value['depth'] for key, value in baseline.items()}
        saturated, saturated_edges = audit.graph(prune_dual=True, retain_edges=True, max_depth=None)
        saturated_baseline, _ = audit.graph(prune_dual=False, retain_edges=False, max_depth=None)
        assert {key: value['depth'] for key, value in saturated.items()} == {key: value['depth'] for key, value in saturated_baseline.items()}
        classes = audit.all_classes()
        seed_traces = {trace(*seed, p) for seed in audit.seeds()}
        saturated_summary.append({'p': p, 'reachable_classes_all_depths': len(saturated),
                                  'maximum_minimal_depth': max((state['depth'] for state in saturated.values()), default=0),
                                  'classes_added_after_depth4': len(saturated)-len(states),
                                  'seed_trace_values': sorted(seed_traces)})
        depths = [{key for key, value in states.items() if value['depth'] == d} for d in range(MAX_DEPTH + 1)]
        j_depths = [{invariant(*key, p) for key in layer} for layer in depths]
        ordinary = [entry for entry in classes if entry['ordinary']]
        summary = {'p': p, 'seed_classes': len(depths[0]), 'all_classes': len(classes),
                   'ordinary_classes': len(ordinary), 'supersingular_classes': len(classes) - len(ordinary)}
        seen_j = set()
        for d in range(MAX_DEPTH + 1):
            summary[f'new_classes_depth{d}'] = len(depths[d])
            summary[f'new_j_depth{d}'] = len(j_depths[d] - seen_j)
            summary[f'new_classes_old_j_depth{d}'] = sum(invariant(*key, p) in seen_j for key in depths[d])
            seen_j |= j_depths[d]
        summary['unreached_ordinary_depth4'] = len(ordinary) - len(states)
        summaries.append(summary)
        for row in classes:
            row['minimum_depth_through4'] = states[(row['A'], row['B'])]['depth'] if (row['A'], row['B']) in states else ''
            row['minimum_depth_saturated'] = saturated[(row['A'], row['B'])]['depth'] if (row['A'], row['B']) in saturated else ''
            row['matches_seed_trace'] = row['trace'] in seed_traces
        all_classes += classes
        all_edges += edges
        for d in (3, 4):
            for key in sorted(depths[d]):
                cert = audit.certificate(states[key])
                cert['new_j_at_depth'] = invariant(*key, p) not in set().union(*j_depths[:d])
                certificates.append(cert)
                if not cert['new_j_at_depth']:
                    first_twist_only.append(cert)
        absent = [entry for entry in ordinary if (entry['A'], entry['B']) not in states]
        misses += absent[:3]
        total_coeff_models += len(audit.coeff_cache)
    write_csv(out / 'graph_summary.csv', summaries)
    write_csv(out / 'edge_validation.csv', all_edges)
    write_csv(out / 'all_isomorphism_classes.csv', all_classes)
    write_csv(out / 'saturated_closure_summary.csv', saturated_summary)
    cert_rows = []
    for cert in certificates:
        cert_rows.append({k: json.dumps(v, separators=(',', ':')) if isinstance(v, list) else v for k, v in cert.items()})
    if cert_rows:
        write_csv(out / 'depth_three_four_certificates.csv', cert_rows)
    obstruction_audit = Audit(13)
    component_queue = deque([(1, 1)])
    component_models = {}
    while component_queue:
        A, B = component_queue.popleft()
        key, scale = obstruction_audit.canonical(A, B)
        if key in component_models:
            continue
        outgoing = []
        for q in roots(A, B, 13):
            target = quotient(A, B, q, 13)
            target_key, target_scale = obstruction_audit.canonical(*target)
            outgoing.append({'root': q, 'target_model': list(target), 'target_class': list(target_key)})
            component_queue.append(target)
        component_models[key] = {'model': [A, B], 'outgoing': outgoing}
    assert set(component_models) == {(1, 1), (2, 3)}
    assert not set(component_models) & set(obstruction_audit.seeds())
    assert trace(1, 1, 13) == trace(7, 0, 13) == -4
    obstruction = {'p': 13, 'input': [1, 1], 'easy_seed_same_trace': [7, 0], 'exact_trace': -4,
                   'input_H_beta': list(coefficients(1, 1, 13)),
                   'full_rational_two_isogeny_component': list(component_models.values()),
                   'status': 'same trace and rational two-torsion do not imply easy-seed reachability'}
    result = {'status': 'passed', 'prime_range': 'all primes 7 <= p <= 251', 'maximum_depth': MAX_DEPTH,
              'class_key': 'minimum coefficient pair over (A,B)->(d^2 A,d^3 B), d nonzero square',
              'seed_scope': 'every nonzero A for B=0,p=1mod4 and every nonzero B for A=0,p=1mod3; all special twists',
              'root_discovery': 'independent brute-force F_p scan, O(p) per displayed model; validation only',
              'pruned_equals_unpruned_minimal_class_depths': True, 'checked_edges': len(all_edges),
              'coefficient_models': total_coeff_models, 'all_isomorphism_classes': len(all_classes),
              'depth3_new_classes': sum(s['new_classes_depth3'] for s in summaries),
              'depth4_new_classes': sum(s['new_classes_depth4'] for s in summaries),
              'depth3_new_j_total': sum(s['new_j_depth3'] for s in summaries),
              'depth4_new_j_total': sum(s['new_j_depth4'] for s in summaries),
              'depth3_primes_with_new_j': [s['p'] for s in summaries if s['new_j_depth3']],
              'depth4_primes_with_new_j': [s['p'] for s in summaries if s['new_j_depth4']],
              'saturated_maximum_minimal_depth': max(s['maximum_minimal_depth'] for s in saturated_summary),
              'saturated_classes_added_after_depth4': sum(s['classes_added_after_depth4'] for s in saturated_summary),
              'saturation_scope': 'finite true F_p isomorphism graph completely exhausted at these primes only',
              'ordinary_seed_trace_but_unreachable_classes': sum(row['ordinary'] and row['matches_seed_trace'] and row['minimum_depth_saturated'] == '' for row in all_classes),
              'ordinary_seed_trace_but_unreachable_with_rational_two_torsion': sum(row['ordinary'] and row['matches_seed_trace'] and row['minimum_depth_saturated'] == '' and row['rational_two_torsion_roots'] > 0 for row in all_classes),
              'depth3_first_new_j_example': next((c for c in certificates if c['depth'] == 3 and c['new_j_at_depth']), None),
              'depth4_first_new_j_example': next((c for c in certificates if c['depth'] == 4 and c['new_j_at_depth']), None),
              'same_trace_reachability_counterexample': obstruction,
              'old_j_new_isomorphism_class_examples': first_twist_only[:4],
              'unreached_ordinary_examples': misses[:12],
              'environment': {'python': sys.version, 'platform': platform.platform()},
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'benchmark': False}
    (out / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('old_j_new_isomorphism_class_examples', 'unreached_ordinary_examples')}, indent=2))


if __name__ == '__main__':
    main()
