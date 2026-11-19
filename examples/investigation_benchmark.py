"""Finite query-specific uncertainty check and source-case certificate coverage."""
import json
from itertools import combinations, permutations, product
from pathlib import Path

from scripts.investigate_sequence import CASES, certificate, load_case, profile_graph
from src.sequence_investigation import investigate


def run_checks():
    vertices = ("u", "v", "w")
    pairs = list(combinations(vertices, 2))
    checked = 0
    statuses = {"SUPPORTED": 0, "UNRESOLVED_MAPPING": 0, "NOT_SUPPORTED": 0}
    for choices in product(((), ("A",), ("B",)), repeat=3):
        mappings = dict(zip(vertices, map(set, choices)))
        for flags in product((False, True), repeat=3):
            edges = {e for e, keep in zip(pairs, flags) if keep}
            relations = [dict(relation_id=str(i), source_event=u, target_event=v, relation="BEFORE") for i, (u, v) in enumerate(sorted(edges))]
            paths = [p for p in permutations(vertices) if (p[0], p[1]) in edges and (p[1], p[2]) in edges]
            for query in product(("A", "B"), repeat=3):
                known = any(all(t in mappings[n] for n, t in zip(p, query)) for p in paths)
                # Enumerate label completions independently of the engine's wildcard test.
                possibilities = [tuple(mappings[n]) if mappings[n] else ("A", "B") for n in vertices]
                possible = False
                for completion in product(*possibilities):
                    labels = dict(zip(vertices, completion))
                    if any(tuple(labels[n] for n in p) == query for p in paths):
                        possible = True
                        break
                expected = "SUPPORTED" if known else "UNRESOLVED_MAPPING" if possible else "NOT_SUPPORTED"
                actual = investigate(mappings, relations, query)["status"]
                if expected != actual:
                    raise AssertionError((mappings, edges, query, expected, actual))
                statuses[actual] += 1
                checked += 1
    cases = {}
    for key in CASES:
        case = load_case(key)
        counts = {name: 0 for name in statuses}
        profiles = {}
        for p in case["profiles"]:
            level = p.get("taxonomy_level", "parent")
            vocab = sorted({n["candidate_" + level + "_mapping"] for n in case["occurrences"]})
            pc = {name: 0 for name in statuses}
            for query in product(vocab, repeat=3):
                c = certificate(key, case, p["name"], query)
                answer = c["answer"]
                pc[answer["status"]] += 1
                counts[answer["status"]] += 1
                nodes = {n["event_id"] for n in c["occurrences"]}
                edges = {r["relation_id"] for r in c["relations"]}
                evidence = {e["evidence_id"] for e in c["evidence"]}
                for witness in answer["known_witnesses"] + answer["unresolved_witnesses"]:
                    assert set(witness["occurrence_ids"]) <= nodes
                    assert set(witness["relation_ids"]) <= edges
                assert all(set(item["evidence_ids"]) <= evidence for item in c["occurrences"] + c["relations"])
            profiles[p["name"]] = pc
        cases[key] = {"profiles": profiles, "totals": counts}
    return {"status": "PASS_IMPLEMENTATION_AND_RECORD_COVERAGE_NOT_FIELD_EFFICACY",
            "finite_query_checks": checked, "finite_status_counts": statuses, "source_cases": cases,
            "scope": "Three ordered vertices, two labels, singleton-or-unknown mappings and every forward-edge subset. Case queries enumerate each case's candidate-label vocabulary for every recorded profile. These are constructed checks, not independent semantic validation or analyst task outcomes."}


if __name__ == "__main__":
    result = run_checks()
    output = Path("research/experiments/investigation_v0.1/results.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps(result, indent=2))
