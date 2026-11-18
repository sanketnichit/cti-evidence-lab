"""Two-edge BEFORE queries on supplied occurrence DAGs and their projections.

These functions measure representational fidelity, not extraction accuracy.
Inputs are explicitly directed BEFORE edges, never inferred dependency edges.
"""
from itertools import permutations, product


def validate(mappings, edges):
    if any(not isinstance(v, str) or not v.strip() for v in mappings):
        raise ValueError("Occurrence identifiers must be nonempty strings")
    if any(not isinstance(t, str) or not t.strip() for ts in mappings.values() for t in ts):
        raise ValueError("Technique identifiers must be nonempty strings")
    successors = {v: set() for v in mappings}
    incoming = {v: 0 for v in mappings}
    for u, v in set(edges):
        if u not in mappings or v not in mappings:
            raise ValueError("Unknown occurrence endpoint")
        successors[u].add(v)
        incoming[v] += 1
    ready = [v for v in mappings if incoming[v] == 0]
    visited = 0
    while ready:
        u = ready.pop()
        visited += 1
        for v in successors[u]:
            incoming[v] -= 1
            if incoming[v] == 0:
                ready.append(v)
    if visited != len(mappings):
        raise ValueError("BEFORE input must be acyclic")


def source_answers(mappings, edges):
    """Independent oracle: enumerate distinct occurrence triples directly."""
    edges = set(edges)
    return {labels for u, v, w in permutations(mappings, 3)
            if (u, v) in edges and (v, w) in edges
            for labels in product(mappings[u], mappings[v], mappings[w])}


def technique_answers(pairs):
    """Ordinary two-hop graph traversal, including walks through self-loops."""
    return {(a, b, c) for a, b in pairs for middle, c in pairs if b == middle}


def compatible_answers(rows):
    """Join edge images only when their intermediate occurrence IDs agree."""
    by_source = {}
    for a, b, u, v in rows:
        by_source.setdefault((u, a), []).append((b, v))
    return {(a, b, c) for a, b, u, v in rows
            for c, w in by_source.get((v, b), []) if len({u, v, w}) == 3}


def evaluate(mappings, before_edges):
    edges = set(before_edges)
    validate(mappings, edges)
    rows = {(a, b, u, v) for u, v in edges for a in mappings[u] for b in mappings[v]}
    distinct_rows = {row for row in rows if row[0] != row[1]}
    pairs = {(a, b) for a, b, _, _ in rows}
    distinct_pairs = {(a, b) for a, b, _, _ in distinct_rows}
    return {
        "truth": source_answers(mappings, edges),
        "answers": {
            "distinct_pairs": technique_answers(distinct_pairs),
            "loop_pairs": technique_answers(pairs),
            "distinct_pairs_with_endpoint_join": compatible_answers(distinct_rows),
            "loop_pairs_with_endpoint_join": compatible_answers(rows),
        },
        "storage": {"source_edges": len(edges), "distinct_pair_keys": len(distinct_pairs),
                    "loop_pair_keys": len(pairs), "endpoint_rows": len(rows)},
    }
