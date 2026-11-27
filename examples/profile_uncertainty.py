"""Compare pooled and profile-coherent support under open mapping completion."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from itertools import combinations_with_replacement, product
from pathlib import Path

from examples.profile_coherence import ROOT, enumerate_witnesses, finite_profiles, recorded_profile_groups, witness_masks
from src.sequence_investigation import investigate

RESULTS = ROOT / "research/experiments/profile_coherence_v0.2/uncertainty_results.json"
STATUSES = ("NOT_SUPPORTED", "UNRESOLVED_MAPPING", "SUPPORTED")


def supported_queries(witnesses):
    """Distinguish witnesses drawn from one profile and from the pooled facts."""
    coherent = set()
    pooled = set()
    for (_, query), mask in witnesses.items():
        pooled.add(query)
        if mask:
            coherent.add(query)
    return coherent, pooled


def classify(queries, known, possible):
    return {query: 2 if query in known else 1 if query in possible else 0 for query in queries}


def reference_ranks(profile, queries):
    mappings, edges = profile
    relations = [dict(relation_id=f"B{i}", source_event=u, target_event=v, relation="BEFORE")
                 for i, (u, v) in enumerate(sorted(edges))]
    return {query: STATUSES.index(investigate(mappings, relations, query, summary_only=True)["status"])
            for query in queries}


def compare(profiles, vocabulary, reference=None):
    queries = tuple(product(vocabulary, repeat=3))
    known_witnesses = witness_masks(profiles)
    possible_witnesses = witness_masks(profiles, completion_vocabulary=vocabulary)
    known_coherent, known_pool = supported_queries(known_witnesses)
    possible_coherent, possible_pool = supported_queries(possible_witnesses)
    coherent = classify(queries, known_coherent, possible_coherent)
    pooled = classify(queries, known_pool, possible_pool)

    if reference is None:
        reference = [reference_ranks(profile, queries) for profile in profiles]
        for masks, completion in ((known_witnesses, ()), (possible_witnesses, vocabulary)):
            direct = {(path, query) for mappings, edges in profiles
                      for path, query in enumerate_witnesses(
                          {node: labels or completion for node, labels in mappings.items()}, edges)}
            if direct != {witness for witness, mask in masks.items() if mask}:
                raise AssertionError("Coherent witnesses differ from direct per-profile enumeration")
    if coherent != {query: max(row[query] for row in reference) for query in queries}:
        raise AssertionError("Coherent answers differ from direct per-profile investigation")
    possible_facts = defaultdict(set)
    pooled_edges = set()
    for mappings, edges in profiles:
        for node, labels in mappings.items():
            possible_facts[node].update(labels or vocabulary)
        pooled_edges.update(edges)
    if possible_witnesses.keys() != enumerate_witnesses(possible_facts, pooled_edges):
        raise AssertionError("Pooled possibilities differ from explicit distinct-path enumeration")

    coherent_counts = Counter(dict.fromkeys(STATUSES, 0))
    pooled_counts = Counter(dict.fromkeys(STATUSES, 0))
    promotions = defaultdict(list)
    for query in queries:
        before, after = coherent[query], pooled[query]
        if before > after:
            raise AssertionError("Pooling should only add eligible facts")
        coherent_counts[STATUSES[before]] += 1
        pooled_counts[STATUSES[after]] += 1
        if after > before:
            promotions[f"{STATUSES[before]} -> {STATUSES[after]}"].append(list(query))
    return {
        "query_count": len(queries),
        "coherent": dict(coherent_counts),
        "pooled": dict(pooled_counts),
        "witness_counts": {
            kind: {"pooled": len(masks), "pooled_only": sum(not mask for mask in masks.values())}
            for kind, masks in (("known", known_witnesses), ("possible", possible_witnesses))
        },
        "promotions": {key: {"count": len(items), "example_query": items[0]}
                       for key, items in sorted(promotions.items())},
    }


def finite_check():
    profiles = finite_profiles()
    vocabulary = ("A", "B")
    queries = tuple(product(vocabulary, repeat=3))
    direct = [reference_ranks(profile, queries) for profile in profiles]
    cases = list(combinations_with_replacement(range(len(profiles)), 2))
    counts = Counter()
    affected = 0
    for a, b in cases:
        result = compare((profiles[a], profiles[b]), vocabulary, (direct[a], direct[b]))
        affected += bool(result["promotions"])
        counts.update({key: row["count"] for key, row in result["promotions"].items()})
    return {"profile_pairs": len(cases), "pairs_with_promotions": affected,
            "query_instances": len(cases) * len(queries), "promotions": dict(sorted(counts.items()))}


def controls():
    mappings = {"u": {"A"}, "v": set(), "w": {"C"}}
    both_edges = {("u", "v"), ("v", "w")}
    # Each pair has the same pooled facts and per-fact profile counts.
    fixed = {**mappings, "v": {"B"}}
    shared = {**fixed, "x": {"B"}}
    shared_edges = {("u", "x"), ("x", "w")}
    aligned = ((shared, shared_edges | both_edges), (shared, shared_edges))
    split = ((shared, shared_edges | {("u", "v")}), (shared, shared_edges | {("v", "w")}))
    aligned_result = compare(aligned, ("A", "B", "C"))
    split_result = compare(split, ("A", "B", "C"))
    if aligned_result["coherent"] != split_result["coherent"] or split_result["promotions"]:
        raise AssertionError("The shared witness should preserve query status")
    if (aligned_result["witness_counts"]["known"] != {"pooled": 2, "pooled_only": 0}
            or split_result["witness_counts"]["known"] != {"pooled": 2, "pooled_only": 1}):
        raise AssertionError("Only the split interpretation pair should create a false witness")
    return {
        "same_status_different_witnesses": {"aligned_edges": aligned_result, "split_edges": split_result},
        "separate_edges_with_unknown_middle": compare(
            ((mappings, {("u", "v")}), (mappings, {("v", "w")})), ("A", "B", "C")
        ),
        "known_label_in_profile_missing_an_edge": compare(
            ((mappings, both_edges), ({**mappings, "v": {"B"}}, {("u", "v")})), ("A", "B", "C")
        ),
    }


def run():
    recorded = {}
    for group, names, graphs in recorded_profile_groups():
        vocabulary = sorted({label for mappings, _ in graphs for labels in mappings.values() for label in labels})
        recorded[group] = {"profiles": names, "vocabulary": vocabulary, **compare(graphs, vocabulary)}
    return {"finite": finite_check(), "controls": controls(), "recorded_profiles": recorded}


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
            raise SystemExit("Profile uncertainty differs from the published results")
        print("Reproduced pooled and profile-coherent mapping uncertainty.")


if __name__ == "__main__":
    main()
