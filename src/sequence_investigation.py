"""Inspectable two-edge query answers on supplied occurrence interpretations.

Empty mapping sets mean unknown labels, not confirmed absence of a technique.
All conclusions are relative to retained occurrences and explicit BEFORE edges.
"""
from itertools import permutations

from src.occurrence_queries import evaluate, validate


def investigate(mappings, relations, query):
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
    witnesses, unresolved = [], []
    for path in sorted(permutations(mappings, 3)):
        u, v, w = path
        if (u, v) not in edges or (v, w) not in edges:
            continue
        if any(mappings[node] and label not in mappings[node] for node, label in zip(path, query)):
            continue
        missing = [{"occurrence_id": n, "required_technique": t} for n, t in zip(path, query) if not mappings[n]]
        item = {"occurrence_ids": list(path), "relation_ids": sorted(by_edge[(u, v)] + by_edge[(v, w)])}
        if missing:
            unresolved.append({**item, "required_mappings": missing})
        else:
            witnesses.append(item)
    result = evaluate(mappings, edges)
    comparisons = {}
    for name, retain_loops in (("distinct_pairs", False), ("loop_pairs", True)):
        joins = []
        if retain_loops or (query[0] != query[1] and query[1] != query[2]):
            left = sorted((u, v) for u, v in edges if query[0] in mappings[u] and query[1] in mappings[v])
            right = sorted((u, v) for u, v in edges if query[1] in mappings[u] and query[2] in mappings[v])
            for a in left:
                for b in right:
                    if a[1] == b[0] and len({a[0], a[1], b[1]}) == 3:
                        continue
                    reasons = []
                    if a[1] != b[0]:
                        reasons.append("MIDDLE_OCCURRENCE_MISMATCH")
                    if a == b:
                        reasons.append("REUSED_EDGE_IMAGE")
                    if len(set(a + b)) < 3:
                        reasons.append("FEWER_THAN_THREE_OCCURRENCES")
                    joins.append({"left_occurrences": list(a), "right_occurrences": list(b),
                                  "left_relation_ids": sorted(by_edge[a]), "right_relation_ids": sorted(by_edge[b]),
                                  "reasons": reasons})
        returned = query in result["answers"][name]
        comparisons[name] = {
            "returned": returned,
            "endpoint_join_returned": query in result["answers"][name + "_with_endpoint_join"],
            "incompatible_joins": joins,
            "diagonal_suppression": bool(witnesses) and not returned and not retain_loops,
            "unsupported_positive": returned and not witnesses and not unresolved,
        }
    status = "SUPPORTED" if witnesses else "UNRESOLVED_MAPPING" if unresolved else "NOT_SUPPORTED"
    return {"query": list(query), "status": status, "known_witnesses": witnesses,
            "unresolved_witnesses": unresolved, "projection_comparisons": comparisons,
            "scope": "Retained occurrence graph and declared mappings only; not proof of absence in the intrusion.",
            "uncertainty_semantics": "Unknown mappings may take any queried label; known mapping sets and supplied edges remain fixed. This does not model missing events, edges, or incorrect annotations."}
