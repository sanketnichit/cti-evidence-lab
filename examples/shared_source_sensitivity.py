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
    per_profile = [
        reference_ranks((mappings, {(row["source_event"], row["target_event"]) for row in relations}), queries)
        for mappings, relations in profiles.values()
    ]
    stable_queries = [query for query in queries if all(ranks[query] == 2 for ranks in per_profile)]
    paragraphs = {row["evidence_id"]: row["paragraph_number"] for row in record["evidence"]}
    cited = {
        name: [{paragraphs[e] for e in row["evidence_ids"]} for row in relations]
        for name, (_, relations) in profiles.items()
    }
    units = sorted({unit for profile in cited.values() for row_units in profile for unit in row_units})
    losses = {}
    for rule in ("first_citation", "last_citation"):
        losses[rule] = []
        for unit in units:
            remaining = {}
            for name, (mappings, relations) in profiles.items():
                rows = []
                for row, row_units in zip(relations, cited[name]):
                    removed = unit in row_units if rule == "first_citation" else row_units == {unit}
                    if not removed:
                        rows.append(row)
                remaining[name] = (mappings, rows)
            for query in stable_queries:
                statuses = {name: investigate(mappings, relations, query, summary_only=True)["status"]
                            for name, (mappings, relations) in remaining.items()}
                if any(status != "SUPPORTED" for status in statuses.values()):
                    losses[rule].append({"paragraph": unit, "query": list(query), "remaining_statuses": statuses})
    return {"stable_queries": [list(query) for query in stable_queries], "paragraphs": units, "losses": losses}


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
