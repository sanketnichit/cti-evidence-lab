"""Systematic source-interpretation stress test on the two recorded cases."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

from scripts.investigate_sequence import CASES, ROOT, load_case, profile_graph
from src.sequence_investigation import investigate

PROFILES = {"rdp": "proposed_cleanup_full_edges",
            "domain-controller": "extended_script_sequence"}


def interventions(mappings, relations):
    operations = [("omit_relation", row["relation_id"]) for row in relations]
    operations.extend(("withhold_mapping", node) for node, labels in mappings.items() if labels)
    operations.extend(("exclude_occurrence", node) for node in mappings)
    endpoints = {row["relation_id"]: {row["source_event"], row["target_event"]}
                 for row in relations}
    for size in (1, 2):
        for changes in combinations(sorted(operations), size):
            excluded = {value for kind, value in changes if kind == "exclude_occurrence"}
            if any((kind == "withhold_mapping" and value in excluded)
                   or (kind == "omit_relation" and endpoints[value] & excluded)
                   for kind, value in changes):
                continue
            withheld = {value for kind, value in changes if kind == "withhold_mapping"}
            omitted = {value for kind, value in changes if kind == "omit_relation"}
            remaining_mappings = {
                node: set() if node in withheld else labels
                for node, labels in mappings.items() if node not in excluded
            }
            remaining_relations = [
                row for row in relations if row["relation_id"] not in omitted
                and not endpoints[row["relation_id"]] & excluded
            ]
            yield changes, remaining_mappings, remaining_relations


def evaluate_case(name, profile):
    case = load_case(name)
    _, _, mappings, relations = profile_graph(case, profile)
    vocabulary = sorted({label for labels in mappings.values() for label in labels})
    queries = list(product(vocabulary, repeat=3))
    baseline = {q: investigate(mappings, relations, q) for q in queries}
    supported = {q for q in queries if baseline[q]["status"] == "SUPPORTED"}
    projected_only = {
        q for q in queries if baseline[q]["projection_comparisons"]["loop_pairs"]["unsupported_positive"]
    }
    scenarios = []
    for changes, modified_mappings, modified_relations in interventions(mappings, relations):
        transitions = Counter()
        support_losses = []
        projected_outcomes = []
        for query, original in baseline.items():
            answer = investigate(modified_mappings, modified_relations, query)
            status = answer["status"]
            if status == "SUPPORTED" and query not in supported:
                raise AssertionError("Removing evidence cannot create a known witness")
            for view, comparison in answer["projection_comparisons"].items():
                if comparison["returned"] and not original["projection_comparisons"][view]["returned"]:
                    raise AssertionError("Removing evidence cannot create a projected edge pair")
            transitions[f"{original['status']} -> {status}"] += 1
            if query in supported and status != "SUPPORTED":
                support_losses.append({"query": query, "status": status})
            if query in projected_only:
                projected_outcomes.append({
                    "query": query, "status": status,
                    "still_returned": answer["projection_comparisons"]["loop_pairs"]["returned"],
                })
        scenarios.append({"changes": changes, "transitions": dict(sorted(transitions.items())),
                          "support_losses": support_losses, "baseline_projected_only": projected_outcomes})
    return {
        "profile": profile, "vocabulary": vocabulary, "query_count": len(queries),
        "baseline_supported": sorted(supported), "baseline_projected_only": sorted(projected_only),
        "scenarios": scenarios,
    }


def run():
    return {
        "scope": "Deterministic interpretation stress test on two recorded parent-level case graphs.",
        "case_records": {name: CASES[name].relative_to(ROOT).as_posix() for name in PROFILES},
        "cases": {name: evaluate_case(name, profile) for name, profile in PROFILES.items()},
    }


def summarize(result):
    summary = {}
    for name, case in result["cases"].items():
        families = {}
        for scenario in case["scenarios"]:
            family = " + ".join(change[0] for change in scenario["changes"])
            counts = families.setdefault(family, Counter())
            counts["scenarios"] += 1
            counts["scenarios_losing_supported_query"] += bool(scenario["support_losses"])
            for loss in scenario["support_losses"]:
                counts[f"support_loss_to_{loss['status']}"] += 1
            for outcome in scenario["baseline_projected_only"]:
                disposition = outcome["status"] if outcome["still_returned"] else "NO_RETURN"
                counts[f"baseline_projected_only_{disposition}"] += 1
        summary[name] = {key: value for key, value in case.items() if key != "scenarios"}
        summary[name]["by_intervention_family"] = families
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", action="store_true", help="Write counts by intervention family")
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summarize(result) if args.summary else result, indent=2)
                           + "\n", encoding="utf-8", newline="")


if __name__ == "__main__":
    main()
