"""Measure sensitivity to removing recorded ordering rows and citation units."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from examples.profile_coherence import enumerate_witnesses, witness_masks
from scripts.investigate_sequence import AVAILABLE_CASES, ROOT, load_case, profile_graph

RESULTS = ROOT / "research/experiments/profile_coherence_v0.2/ordering_evidence_results.json"


def evaluate(mappings, relations, evidence):
    vocabulary = sorted({label for labels in mappings.values() for label in labels})
    completion = {node: labels or vocabulary for node, labels in mappings.items()}
    edge_by_id = {row["relation_id"]: (row["source_event"], row["target_event"]) for row in relations}
    citations = {row["evidence_id"]: (f"page {row['page']}" if 'page' in row else
                                     f"paragraph {row['paragraph_number']}") for row in evidence}
    rows_by_unit = defaultdict(set)
    sole_unit_rows = defaultdict(set)
    units_by_row = {}
    for relation in relations:
        units = {citations[citation] for citation in relation["evidence_ids"]}
        units_by_row[relation["relation_id"]] = units
        for unit in units:
            rows_by_unit[unit].add(relation["relation_id"])
            if len(units) == 1:
                sole_unit_rows[unit].add(relation["relation_id"])

    def remaining_edges(removed):
        return {edge for identifier, edge in edge_by_id.items() if identifier not in removed}

    def witnesses(removed):
        edges = remaining_edges(removed)
        known = enumerate_witnesses(mappings, edges)
        possible = enumerate_witnesses(completion, edges)
        if (known != set(witness_masks([(mappings, edges)])) or
                possible != set(witness_masks([(mappings, edges)], completion_vocabulary=vocabulary))):
            raise AssertionError("Distinct-path enumeration and profile masks disagree")
        return known, possible

    known, possible = witnesses(set())
    baseline_known = {query for _, query in known}
    baseline_possible = {query for _, query in possible}
    paths_by_query = defaultdict(list)
    for path, query in known:
        paths_by_query[query].append(set(zip(path, path[1:])))

    def minimum_cuts(last_citation):
        units = sorted(rows_by_unit)
        pending = set(baseline_known)
        cuts = dict.fromkeys(pending)
        for size in range(1, len(units) + 1):
            for withdrawal in combinations(units, size):
                removed_units = set(withdrawal)
                removed = {row for row, cited in units_by_row.items() if cited and
                           (cited <= removed_units if last_citation else bool(cited & removed_units))}
                edges = remaining_edges(removed)
                lost = {q for q in pending if all(not path <= edges for path in paths_by_query[q])}
                for query in lost:
                    cuts[query] = withdrawal
                pending.difference_update(lost)
                if not pending:
                    return cuts
        return cuts

    def sweep(interventions):
        fragile = set()
        records = {}
        for name, removed in sorted(interventions.items()):
            remaining_known, remaining_possible = witnesses(removed)
            mapped_queries = {query for _, query in remaining_known}
            possible_queries = {query for _, query in remaining_possible}
            lost_support = baseline_known - mapped_queries
            fragile.update(lost_support)
            records[name] = {
                "removed_rows": sorted(removed),
                "evidence_ids": sorted({citation for row in relations if row["relation_id"] in removed
                                        for citation in row["evidence_ids"]}),
                "known_witnesses_lost": len(known - remaining_known),
                "possible_witnesses_lost": len(possible - remaining_possible),
                "supported_to_unresolved": sorted(lost_support & possible_queries),
                "supported_to_unsupported": sorted(lost_support - possible_queries),
                "unresolved_to_unsupported": len((baseline_possible - baseline_known) - possible_queries),
            }
        return {"fragile_supported_queries": sorted(fragile), "interventions": records}

    first_cuts = minimum_cuts(last_citation=False)
    last_cuts = minimum_cuts(last_citation=True)
    return {
        "status": "ASSESSED", "query_count": len(vocabulary) ** 3, "vocabulary": vocabulary,
        "ordering_rows": len(relations), "known_witnesses": len(known), "possible_witnesses": len(possible),
        "supported_queries": len(baseline_known), "unresolved_queries": len(baseline_possible - baseline_known),
        "single_row": sweep({identifier: {identifier} for identifier in edge_by_id}),
        "source_unit": sweep(rows_by_unit),
        "last_citation_overrides": sweep({unit: sole_unit_rows[unit] for unit, rows in rows_by_unit.items()
                                          if rows != sole_unit_rows[unit]})["interventions"],
        "minimum_source_unit_cuts": [
            {"query": query, "first_citation": first_cuts[query], "last_citation": last_cuts[query]}
            for query in sorted(baseline_known)
        ],
    }


def run():
    cases = {}
    for key in AVAILABLE_CASES:
        case = load_case(key)
        cases[key] = {}
        for row in case["profiles"]:
            if row.get("taxonomy_level", "parent") != "parent":
                continue
            _, _, mappings, relations = profile_graph(case, row["name"])
            result = ({"status": "UNASSESSED", "ordering_rows": len(relations)}
                      if case.get("query_assessment") == "UNASSESSED"
                      else evaluate(mappings, relations, case["evidence"]))
            cases[key][row["name"]] = result
    # Normalize tuples so the in-memory result can verify directly against JSON.
    return json.loads(json.dumps(cases))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    elif result != json.loads(RESULTS.read_bytes()):
        raise SystemExit("Ordering-evidence sensitivity differs from recorded results")
    else:
        print("Reproduced ordering-evidence sensitivity across six cases.")


if __name__ == "__main__":
    main()
