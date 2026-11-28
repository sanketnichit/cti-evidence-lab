"""Withdraw the same ordering-evidence paragraph from every recorded profile."""
import argparse
import json
from itertools import product
from pathlib import Path

from examples.profile_coherence import ROOT
from examples.profile_uncertainty import reference_ranks
from scripts.compare_sequence_profiles import GROUPS, comparison_context
from src.sequence_investigation import investigate

RESULTS = ROOT / "research/experiments/profile_coherence_v0.2/shared_source_results.json"


def evaluate(record, profiles):
    vocabulary = sorted({label for mappings, _ in profiles.values() for labels in mappings.values() for label in labels})
    queries = tuple(product(vocabulary, repeat=3))
    per_profile = {
        name: reference_ranks((mappings, {(row["source_event"], row["target_event"]) for row in relations}), queries)
        for name, (mappings, relations) in profiles.items()
    }
    baseline = {query: {name for name, ranks in per_profile.items() if ranks[query] == 2} for query in queries}
    supported_queries = [query for query, names in baseline.items() if names]
    stable_queries = [query for query in supported_queries if len(baseline[query]) == len(profiles)]
    paragraphs = {row["evidence_id"]: row["paragraph_number"] for row in record["evidence"]}
    cited = {
        name: [{paragraphs[e] for e in row["evidence_ids"]} for row in relations]
        for name, (_, relations) in profiles.items()
    }
    units = sorted({unit for profile in cited.values() for row_units in profile for unit in row_units})
    citations_by_edge = {}
    for name, (_, relations) in profiles.items():
        by_edge = {}
        for row, row_units in zip(relations, cited[name]):
            edge = (row["source_event"], row["target_event"])
            by_edge.setdefault(edge, set()).add(tuple(sorted(row_units)))
        citations_by_edge[name] = by_edge

    provenance = []
    for query in stable_queries:
        profiles_by_witness = {}
        for name, (mappings, relations) in profiles.items():
            answer = investigate(mappings, relations, query)
            for witness in answer["known_witnesses"]:
                path = tuple(witness["occurrence_ids"])
                # Keep the two hops and any parallel relation rows distinct.
                signature = tuple(tuple(sorted(citations_by_edge[name][edge])) for edge in zip(path, path[1:]))
                profiles_by_witness.setdefault((path, signature), []).append(name)
        provenance.append({
            "query": list(query),
            "witnesses": [{
                "occurrences": list(path),
                "ordering_row_paragraphs_by_hop": [[list(row) for row in hop] for hop in signature],
                "profiles": names,
            } for (path, signature), names in sorted(profiles_by_witness.items())],
        })
    losses = {}
    joint = {}
    for rule in ("first_citation", "last_citation"):
        losses[rule] = []
        eligible = 0
        joint_only = []
        partial_losses = 0
        for unit in units:
            remaining = {}
            for name, (mappings, relations) in profiles.items():
                rows = []
                for row, row_units in zip(relations, cited[name]):
                    removed = unit in row_units if rule == "first_citation" else row_units == {unit}
                    if not removed:
                        rows.append(row)
                remaining[name] = (mappings, rows)
            for query in supported_queries:
                statuses = {name: investigate(mappings, relations, query, summary_only=True)["status"]
                            for name, (mappings, relations) in remaining.items()}
                after = {name for name, status in statuses.items() if status == "SUPPORTED"}
                if query in stable_queries and len(after) < len(profiles):
                    losses[rule].append({"paragraph": unit, "query": list(query), "remaining_statuses": statuses})
                if not after:
                    continue
                if after < baseline[query]:
                    partial_losses += 1
                for omitted in profiles:
                    if not baseline[query] - {omitted}:
                        continue
                    eligible += 1
                    if after == {omitted}:
                        joint_only.append({
                            "paragraph": unit, "omitted_profile": omitted, "query": list(query),
                            "baseline_supporters": sorted(baseline[query]),
                            "remaining_statuses": {name: status for name, status in statuses.items() if name != omitted},
                        })
        joint[rule] = {
            "survive_both_separate_interventions": eligible,
            "paragraph_query_pairs_with_partial_support_loss": partial_losses,
            "joint_only_losses": joint_only,
        }
    return {
        "stable_queries": [list(query) for query in stable_queries], "paragraphs": units, "losses": losses,
        "stable_query_provenance": provenance,
        "supported_queries": len(supported_queries),
        "joint_scenarios_per_rule": len(profiles) * len(units) * len(supported_queries),
        "joint": joint,
    }


def run():
    return {group: evaluate(*comparison_context(group)) for group in GROUPS}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    elif result != json.loads(RESULTS.read_bytes()):
        raise SystemExit("Shared-source sensitivity differs from recorded results")
    else:
        print("Reproduced the shared-source sensitivity results.")
