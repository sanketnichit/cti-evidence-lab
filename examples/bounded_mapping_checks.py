"""Exhaustive small-graph check of declared mapping bounds, not field efficacy."""
import json
from itertools import combinations, permutations, product
from pathlib import Path

from src.sequence_investigation import investigate


def run_checks():
    vertices = ('u', 'v', 'w')
    labels = ('A', 'B')
    # Unknown: open, A-only, B-only, A-or-B. Known: A, B, A-and-B.
    states = (((), None), ((), ('A',)), ((), ('B',)), ((), labels),
              (('A',), None), (('B',), None), (labels, None))
    counts = {s: 0 for s in ('SUPPORTED', 'UNRESOLVED_MAPPING', 'NOT_SUPPORTED')}
    changed = 0
    for choices in product(states, repeat=3):
        mappings = {n: set(s[0]) for n, s in zip(vertices, choices)}
        domains = {n: set(s[1]) for n, s in zip(vertices, choices) if s[1] is not None}
        completions = [(mappings[n],) if mappings[n] else tuple({t} for t in domains.get(n, labels)) for n in vertices]
        for flags in product((False, True), repeat=3):
            edges = {e for e, keep in zip(combinations(vertices, 2), flags) if keep}
            relations = [dict(relation_id=str(i), source_event=u, target_event=v, relation='BEFORE') for i, (u, v) in enumerate(sorted(edges))]
            paths = [p for p in permutations(vertices) if (p[0], p[1]) in edges and (p[1], p[2]) in edges]
            known = {q for p in paths for q in product(*(mappings[n] for n in p))}
            possible = set()
            for completion in product(*completions):
                assigned = dict(zip(vertices, completion))
                possible.update(q for p in paths for q in product(*(assigned[n] for n in p)))
            for query in product(labels, repeat=3):
                expected = 'SUPPORTED' if query in known else 'UNRESOLVED_MAPPING' if query in possible else 'NOT_SUPPORTED'
                answer = investigate(mappings, relations, query, mapping_domains=domains or None)
                unrestricted = investigate(mappings, relations, query)
                if answer['status'] != expected:
                    raise AssertionError((choices, edges, query, expected, answer))
                if answer['known_witnesses'] != unrestricted['known_witnesses']:
                    raise AssertionError('Bounds changed a known witness')
                if answer['status'] != unrestricted['status']:
                    if (unrestricted['status'], answer['status']) != ('UNRESOLVED_MAPPING', 'NOT_SUPPORTED'):
                        raise AssertionError('Unexpected status promotion')
                    changed += 1
                counts[answer['status']] += 1
    return {'status': 'PASS_BOUNDED_IMPLEMENTATION_CHECK_NOT_FIELD_EFFICACY',
            'finite_query_checks': sum(counts.values()), 'status_counts': counts,
            'unresolved_to_not_supported_under_bounds': changed,
            'scope': 'Three ordered vertices, every forward-edge subset, two query labels and seven per-vertex known/unknown/domain states. Direct enumeration of unknown-label assignments checks classification; known witnesses must remain unchanged. Changes are consequences of assumed bounds, not corrected field errors.'}


if __name__ == '__main__':
    result = run_checks()
    path = Path('research/experiments/bounded_mapping_v0.1/results.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='')
    print(json.dumps(result, indent=2))
