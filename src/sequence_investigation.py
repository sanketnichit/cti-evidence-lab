"""Inspectable two-edge query answers on supplied occurrence interpretations.

Empty mapping sets mean unknown labels, not confirmed absence of a technique.
All conclusions are relative to retained occurrences and explicit BEFORE edges.
"""
from collections import Counter, defaultdict

from src.occurrence_queries import validate


def _count_paths(edges, candidates):
    # Every eligible incoming edge can pair with every eligible outgoing edge
    # at the same middle occurrence. Acyclicity rules out repeated endpoints.
    first, middle, last = candidates
    incoming = Counter(v for u, v in edges if u in first and v in middle)
    outgoing = Counter(u for u, v in edges if u in middle and v in last)
    return sum(count * outgoing[node] for node, count in incoming.items())


def investigate(mappings, relations, query, *, mapping_domains=None, summary_only=False):
    """Return inspectable evidence, or exact counts without listing its members."""
    if not isinstance(query, (list, tuple)) or len(query) != 3 or any(not isinstance(t, str) or not t.strip() for t in query):
        raise ValueError("A query requires three nonempty technique identifiers")
    query = tuple(query)
    ids = [r["relation_id"] for r in relations]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate relation identity")
    by_edge = {}
    for r in relations:
        if r["relation"] != "BEFORE":
            raise ValueError("Only explicit BEFORE relations are supported")
        by_edge.setdefault((r["source_event"], r["target_event"]), []).append(r["relation_id"])
    edges = set(by_edge)
    validate(mappings, edges)
    domains = {}
    if mapping_domains is not None:
        if not isinstance(mapping_domains, dict) or not mapping_domains:
            raise ValueError("Mapping domains must be a nonempty occurrence-to-label-set dictionary")
        for node, labels in mapping_domains.items():
            if node not in mappings or mappings[node]:
                raise ValueError("Domains may constrain only retained occurrences with unknown mappings")
            if not isinstance(labels, (set, frozenset, list, tuple)) or not labels or any(not isinstance(t, str) or not t.strip() for t in labels):
                raise ValueError("Each domain requires a nonempty collection of technique identifiers")
            if len(labels) != len(set(labels)):
                raise ValueError("Duplicate domain label")
            domains[node] = set(labels)
    possible_nodes = [
        {node for node, labels in mappings.items() if not labels or technique in labels}
        for technique in query
    ]
    if summary_only:
        mapped = {node for node, labels in mappings.items() if labels}
        known = [nodes & mapped for nodes in possible_nodes]
        feasible = [{node for node in nodes if node not in domains or technique in domains[node]}
                    for nodes, technique in zip(possible_nodes, query)] if domains else possible_nodes
        witnesses = _count_paths(edges, known)
        possible = _count_paths(edges, feasible)
        excluded = _count_paths(edges, possible_nodes) - possible if domains else 0
        first, middle, last = known
        left = sum(u in first and v in middle for u, v in edges)
        right = sum(u in middle and v in last for u, v in edges)
        # Every compatible pair of known edge images yields one known witness.
        return _answer_record(query, witnesses, possible - witnesses, left, right,
                              left * right - witnesses, domains, excluded, summary_only=True)

    ordered_edges = sorted(edges)
    successors = defaultdict(list)
    for u, v in ordered_edges:
        successors[u].append(v)
    # Validation guarantees a DAG, so a connected two-edge path has three
    # distinct endpoints. Sorted traversal preserves witness order in exports.
    first, middle, last = possible_nodes
    paths = ((u, v, w) for u, v in ordered_edges if u in first and v in middle
             for w in successors.get(v, ()) if w in last)
    witnesses, unresolved, excluded = [], [], []
    for path in paths:
        u, v, w = path
        missing = [{"occurrence_id": n, "required_technique": t} for n, t in zip(path, query) if not mappings[n]]
        item = {"occurrence_ids": list(path), "relation_ids": sorted(by_edge[(u, v)] + by_edge[(v, w)])}
        blocked = [{"occurrence_id": n, "required_technique": t, "allowed_techniques": sorted(domains[n])}
                   for n, t in zip(path, query) if n in domains and t not in domains[n]]
        if blocked:
            excluded.append({**item, "excluded_requirements": blocked})
            continue
        if missing:
            unresolved.append({**item, "required_mappings": missing})
        else:
            witnesses.append(item)
    left = [(u, v) for u, v in ordered_edges if query[0] in mappings[u] and query[1] in mappings[v]]
    right = [(u, v) for u, v in ordered_edges if query[1] in mappings[u] and query[2] in mappings[v]]
    joins = []
    for a in left:
        for b in right:
            if a[1] == b[0]:
                continue  # A shared middle in a DAG gives a valid three-action witness.
            reasons = ["MIDDLE_OCCURRENCE_MISMATCH"]
            if a == b:
                reasons.append("REUSED_EDGE_IMAGE")
            if len(set(a + b)) < 3:
                reasons.append("FEWER_THAN_THREE_OCCURRENCES")
            joins.append({"left_occurrences": list(a), "right_occurrences": list(b),
                          "left_relation_ids": sorted(by_edge[a]), "right_relation_ids": sorted(by_edge[b]),
                          "reasons": reasons})
    return _answer_record(query, witnesses, unresolved, len(left), len(right), joins, domains, excluded)


def _answer_record(query, witnesses, unresolved, left, right, joins, domains, excluded, *, summary_only=False):
    witness_field = "known_witness_count" if summary_only else "known_witnesses"
    unresolved_field = "unresolved_witness_count" if summary_only else "unresolved_witnesses"
    joins_field = "incompatible_join_count" if summary_only else "incompatible_joins"
    empty = 0 if summary_only else []
    comparisons = {}
    has_diagonal = query[0] == query[1] or query[1] == query[2]
    for name, retain_loops in (("distinct_pairs", False), ("loop_pairs", True)):
        allowed = retain_loops or not has_diagonal
        returned = allowed and bool(left and right)
        comparisons[name] = {
            "returned": returned,
            "endpoint_join_returned": allowed and bool(witnesses),
            joins_field: joins if allowed else empty,
            "diagonal_suppression": bool(witnesses) and not returned and not retain_loops,
            "unsupported_positive": returned and not witnesses and not unresolved,
        }
    status = "SUPPORTED" if witnesses else "UNRESOLVED_MAPPING" if unresolved else "NOT_SUPPORTED"
    answer = {"query": list(query), "status": status, witness_field: witnesses,
            unresolved_field: unresolved, "projection_comparisons": comparisons,
            "scope": "Retained occurrence graph and declared mappings only; not proof of absence in the intrusion.",
            "uncertainty_semantics": "Unknown mappings may take any queried label; known mapping sets and supplied edges remain fixed. This does not model missing events, edges, or incorrect annotations."}
    if domains:
        answer.update({
            "mapping_domains": {n: sorted(ts) for n, ts in sorted(domains.items())},
                     ("domain_excluded_witness_count" if summary_only else "domain_excluded_witnesses"): excluded,
            "scope": "Retained occurrence graph, known mappings and declared allowed-label bounds only; not proof of absence in the intrusion.",
            "uncertainty_semantics": "Listed domains are assumed upper bounds on possible labels, not accepted mappings. Unlisted unknown occurrences remain unrestricted. A singleton domain remains unresolved. Known sets and edges stay fixed; incorrect bounds may exclude a real possibility.",
        })
    return answer
