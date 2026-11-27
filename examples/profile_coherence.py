"""Verify known sequence witnesses across alternative interpretations of one incident."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path

from scripts.investigate_sequence import AVAILABLE_CASES, ROOT, load_case, profile_graph
from src.occurrence_queries import validate

RESULTS = ROOT / "research/experiments/profile_coherence_v0.2/results.json"


def witness_masks(profiles):
    """Index pooled witnesses by the profiles that contain all their facts."""
    labels = defaultdict(set)
    label_profiles = defaultdict(int)
    edge_profiles = defaultdict(int)
    successors = defaultdict(set)
    for index, (mappings, edges) in enumerate(profiles):
        validate(mappings, edges)
        bit = 1 << index
        for node, techniques in mappings.items():
            for technique in techniques:
                labels[node].add(technique)
                label_profiles[node, technique] |= bit
        for first, second in edges:
            successors[first].add(second)
            edge_profiles[first, second] |= bit

    witnesses = {}
    for first, middle in edge_profiles:
        for last in successors[middle]:
            if first == last:
                continue  # A union can contain a cycle even if its profiles are DAGs.
            path = (first, middle, last)
            edge_mask = edge_profiles[first, middle] & edge_profiles[middle, last]
            for query in product(*(labels[node] for node in path)):
                mask = edge_mask
                for fact in zip(path, query):
                    mask &= label_profiles[fact]
                witnesses[path, query] = mask
    return witnesses


def enumerate_witnesses(mappings, edges):
    """Reference enumeration without profile masks or adjacency indexing."""
    return {(path, query)
            for path in permutations(mappings, 3)
            if (path[0], path[1]) in edges and (path[1], path[2]) in edges
            for query in product(*(mappings[node] for node in path))}


def compare(profiles):
    masks = witness_masks(profiles)
    pooled_mappings = defaultdict(set)
    pooled_edges = set()
    expected = defaultdict(int)
    for index, (mappings, edges) in enumerate(profiles):
        for node, labels in mappings.items():
            pooled_mappings[node].update(labels)
        pooled_edges.update(edges)
        for witness in enumerate_witnesses(mappings, edges):
            expected[witness] |= 1 << index
    for witness in enumerate_witnesses(pooled_mappings, pooled_edges):
        expected.setdefault(witness, 0)
    if masks != expected:
        raise AssertionError("Profile masks disagree with independent witness enumeration")

    all_profiles = (1 << len(profiles)) - 1
    query_support = defaultdict(int)
    shared_witness_queries = set()
    for (_, query), mask in masks.items():
        query_support[query] |= mask
        if mask == all_profiles:
            shared_witness_queries.add(query)
    return {
        "pooled_supported_queries": len(query_support),
        "supported_in_some_profile": sum(bool(mask) for mask in query_support.values()),
        "supported_in_every_profile": sum(mask == all_profiles for mask in query_support.values()),
        "queries_with_one_witness_in_every_profile": len(shared_witness_queries),
        "union_only_queries": [list(q) for q, mask in sorted(query_support.items()) if not mask],
        "pooled_witnesses": len(masks),
        "witnesses_in_no_profile": sum(not mask for mask in masks.values()),
    }


def finite_check():
    nodes = ("u", "v", "w")
    possible_edges = (("u", "v"), ("v", "w"))
    profiles = [
        (dict(zip(nodes, labels)), {edge for edge, retained in zip(possible_edges, flags) if retained})
        for labels in product((set(), {"A"}, {"B"}), repeat=3)
        for flags in product((False, True), repeat=2)
    ]
    counts = defaultdict(int)
    for first, second in combinations_with_replacement(profiles, 2):
        result = compare((first, second))
        counts["profile_pairs"] += 1
        counts["pairs_with_union_only_queries"] += bool(result["union_only_queries"])
        counts["union_only_query_instances"] += len(result["union_only_queries"])
        counts["pooled_witness_instances_in_no_profile"] += result["witnesses_in_no_profile"]
    return dict(counts)


def controls():
    mapping = {"u": {"A"}, "v": {"B"}, "w": {"C"}}
    return {
        "separate_edges": compare(((mapping, {("u", "v")}), (mapping, {("v", "w")}))),
        "missing_middle_mapping": compare((
            ({**mapping, "v": set()}, {("u", "v"), ("v", "w")}),
            (mapping, {("u", "v")}),
        )),
        "different_witnesses": compare((
            (mapping, {("u", "v"), ("v", "w")}),
            ({**mapping, "x": {"B"}}, {("u", "x"), ("x", "w")}),
        )),
        "pooled_cycle": compare(((mapping, {("u", "v")}), (mapping, {("v", "u")}))),
    }


def run():
    recorded = {}
    for key in AVAILABLE_CASES:
        case = load_case(key)
        by_taxonomy = defaultdict(list)
        for profile in case["profiles"]:
            _, _, mappings, relations = profile_graph(case, profile["name"])
            edges = {(row["source_event"], row["target_event"]) for row in relations}
            by_taxonomy[profile.get("taxonomy_level", "parent")].append((profile["name"], (mappings, edges)))
        for taxonomy, profiles in by_taxonomy.items():
            if len(profiles) >= 2:
                names, graphs = zip(*profiles)
                recorded[f"{key}/{taxonomy}"] = {"profiles": list(names), **compare(graphs)}
    return {"finite": finite_check(), "synthetic_controls": controls(), "recorded_profiles": recorded}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    else:
        if result != json.loads(RESULTS.read_text(encoding="utf-8")):
            raise SystemExit("Profile coherence differs from the published results")
        print("Reproduced the profile-coherence comparison and finite oracle.")


if __name__ == "__main__":
    main()
