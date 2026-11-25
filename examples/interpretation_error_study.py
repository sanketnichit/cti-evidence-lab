"""Measure how single input errors change query answers on recorded profiles."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

from examples.interpretation_sensitivity import PROFILES
from scripts.investigate_sequence import load_case, profile_graph
from src.occurrence_queries import evaluate, validate


def candidates(mappings, edges):
    nodes = sorted(mappings)
    vocabulary = sorted(set().union(*mappings.values()))
    for u, v in permutations(nodes, 2):
        if (u, v) not in edges:
            yield {"kind": "add_ordering", "source": u, "target": v}, mappings, edges | {(u, v)}
    for node in nodes:
        for label in vocabulary:
            if label not in mappings[node]:
                yield {"kind": "substitute_label", "action": node, "label": label}, {**mappings, node: {label}}, edges
    for keep, remove in combinations(nodes, 2):
        if mappings[keep] == mappings[remove]:
            merged_mappings = {node: labels for node, labels in mappings.items() if node != remove}
            merged_edges = {(keep if u == remove else u, keep if v == remove else v) for u, v in edges}
            yield {"kind": "merge_same_label", "actions": [keep, remove]}, merged_mappings, merged_edges


def compare(name, profile):
    _, _, mappings, relations = profile_graph(load_case(name), profile)
    if any(len(labels) != 1 for labels in mappings.values()):
        raise ValueError("This experiment requires a complete singleton baseline")
    edges = {(relation["source_event"], relation["target_event"]) for relation in relations}
    baseline = evaluate(mappings, edges)
    reference = baseline["truth"]
    scenario_rows = []
    for change, modified, modified_edges in candidates(mappings, edges):
        try:
            validate(modified, modified_edges)
        except ValueError as error:
            if str(error) != "BEFORE input must be acyclic":
                raise
            scenario_rows.append({"change": change, "status": "REJECTED_CYCLE"})
            continue
        result = evaluate(modified, modified_edges)
        supported = result["truth"]
        if result["answers"]["loop_pairs_with_endpoint_join"] != supported:
            raise AssertionError("Endpoint joins disagree with the mutated occurrence oracle")
        gained, lost = supported - reference, reference - supported
        scenario_rows.append({
            "change": change, "status": "ASSESSED",
            "supported_only_after_edit": sorted(gained),
            "supported_only_before_edit": sorted(lost),
            "previously_projected_only_now_supported": sorted(
                gained & baseline["answers"]["loop_pairs"]
            ),
            "views": {
                view: {
                    "outside_baseline_support": len(answers - reference),
                    "supported_only_after_edit": len(answers & gained),
                    "unsupported_in_both_graphs": len(answers - (reference | supported)),
                    "missed_baseline_supported": len(reference - answers),
                }
                for view, answers in result["answers"].items()
            },
        })
    return {
        "profile": profile, "baseline_supported": sorted(reference),
        "scenarios": scenario_rows,
    }


def run():
    # Use the manuscript's indistinguishable-projection counterexample as a
    # positive control for a mistaken identity merge that remains acyclic.
    mappings = {"u": {"A"}, "v": {"B"}, "w": {"B"}, "x": {"C"}}
    edges = {("u", "v"), ("w", "x")}
    change, merged, redirected = next(
        item for item in candidates(mappings, edges) if item[0]["kind"] == "merge_same_label")
    before = evaluate(mappings, edges)
    after = evaluate(merged, redirected)
    query = ("A", "B", "C")
    if query in before["truth"] or query not in after["answers"]["loop_pairs_with_endpoint_join"]:
        raise AssertionError("Acyclic merge control did not create the expected witness")
    return {
        "cases": {name: compare(name, profile) for name, profile in PROFILES.items()},
        "synthetic_merge_control": {
            "change": change, "query": query, "supported_before": False,
            "supported_after": True, "merged_graph_is_acyclic": True,
        },
    }


def summarize(result):
    summary = {}
    for name, case in result["cases"].items():
        rows = {}
        for scenario in case["scenarios"]:
            counts = rows.setdefault(scenario["change"]["kind"], Counter({
                "candidates": 0, "rejected_cycle": 0, "assessed": 0,
                "scenarios_with_new_support": 0, "scenarios_with_lost_support": 0,
                "new_supported_instances": 0, "lost_supported_instances": 0,
                "previously_projected_only_now_supported_instances": 0,
            }))
            counts["candidates"] += 1
            if scenario["status"] == "REJECTED_CYCLE":
                counts["rejected_cycle"] += 1
                continue
            counts["assessed"] += 1
            gained = len(scenario["supported_only_after_edit"])
            lost = len(scenario["supported_only_before_edit"])
            counts["scenarios_with_new_support"] += bool(gained)
            counts["scenarios_with_lost_support"] += bool(lost)
            counts["new_supported_instances"] += gained
            counts["lost_supported_instances"] += lost
            counts["previously_projected_only_now_supported_instances"] += len(
                scenario["previously_projected_only_now_supported"])
        summary[name] = rows
    return {"cases": summary, "synthetic_merge_control": result["synthetic_merge_control"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summarize(result) if args.summary else result, indent=2)
                           + "\n", encoding="utf-8", newline="")


if __name__ == "__main__":
    main()
