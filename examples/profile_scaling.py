"""Measure the cost of comparing one sequence across synthetic profile groups."""

import argparse
import gc
import gzip
import json
import os
import platform
import tracemalloc
from pathlib import Path
from statistics import median
from time import perf_counter_ns

from examples.profile_coherence import witness_masks
from scripts.compare_sequence_profiles import compare_query, export, verify

QUERY = ("A0", "B0", "C0")
DESIGN = ((2, 8, 4), (2, 32, 4), (2, 64, 4), (8, 32, 4), (16, 32, 4), (2, 32, 1))
REPEATS = 7


def workload(profile_count, motifs, labels_per_action):
    profiles = {}
    for profile in range(profile_count):
        mappings, relations = {}, []
        for motif in range(motifs):
            nodes = tuple(f"m{motif:03}-{prefix}" for prefix in "ABC")
            for position, (node, prefix) in enumerate(zip(nodes, "ABC")):
                unknown = motif % 8 == 7 and position == 1
                mappings[node] = set() if unknown else {f"{prefix}{j}" for j in range(labels_per_action)}
            for side, (first, second) in enumerate(zip(nodes, nodes[1:])):
                if motif % 4 == 0 and side != profile % 2:
                    continue
                relations.append({"relation_id": f"B{motif:03}-{side}", "relation": "BEFORE",
                                  "source_event": first, "target_event": second})
        profiles[f"profile-{profile:02}"] = (mappings, relations)
    return profiles


def measure(operations):
    # Keep construction, validation of results, and memory tracing outside timing.
    for operation in operations.values():
        operation()
    samples = {name: [] for name in operations}
    names = list(operations)
    for trial in range(REPEATS):
        for name in names[trial % len(names):] + names[:trial % len(names)]:
            start = perf_counter_ns()
            result = operations[name]()
            samples[name].append(perf_counter_ns() - start)
            del result
    measurements = {}
    for name, operation in operations.items():
        gc.collect()
        tracemalloc.start()
        try:
            result = operation()
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        del result
        measurements[name] = {"median_ns": int(median(samples[name])), "samples_ns": samples[name],
                              "peak_python_bytes": peak}
    return measurements


def storage(value):
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return {"json_bytes": len(data), "gzip_bytes": len(gzip.compress(data, mtime=0))}


def evaluate(profile_count, motifs, labels_per_action):
    profiles = workload(profile_count, motifs, labels_per_action)
    graphs = [(mappings, {(r["source_event"], r["target_event"]) for r in relations})
              for mappings, relations in profiles.values()]

    def exhaustive():
        return [witness_masks(graphs, completion_vocabulary=vocabulary)
                for vocabulary in ((), QUERY)]

    def focused():
        return [witness_masks(graphs, completion_vocabulary=vocabulary, query=QUERY)
                for vocabulary in ((), QUERY)]

    full_masks = exhaustive()
    exact = [{key: mask for key, mask in masks.items() if key[1] == QUERY} for masks in full_masks]
    if focused() != exact:
        raise AssertionError("Focused masks differ from exhaustive enumeration")
    answer = compare_query(profiles, QUERY)
    compact = compare_query(profiles, QUERY, summary_only=True)
    if compact["pooled_witnesses"] != answer["pooled_witnesses"]:
        raise AssertionError("Compact comparison changed the pooled explanation")
    for name, full_profile in answer["profile_answers"].items():
        summary = compact["profile_answers"][name]
        if (summary["status"] != full_profile["status"]
                or summary["known_witness_count"] != len(full_profile["known_witnesses"])
                or summary["unresolved_witness_count"] != len(full_profile["unresolved_witnesses"])):
            raise AssertionError("Compact comparison changed the per-profile answer")
        for projection, comparison in full_profile["projection_comparisons"].items():
            counts = summary["projection_comparisons"][projection]
            if counts["incompatible_join_count"] != len(comparison["incompatible_joins"]):
                raise AssertionError("Compact comparison changed the incompatible join count")
    for kind, expected in zip(("known", "possible"), exact):
        rows = answer["pooled_witnesses"][kind]
        actual = {tuple(row["occurrence_ids"]): set(row["supporting_profiles"]) for row in rows}
        expected = {path: {name for i, name in enumerate(profiles) if mask & (1 << i)}
                    for (path, _), mask in expected.items()}
        if actual != expected:
            raise AssertionError("Exported support differs from exhaustive masks")

    snapshot = {name: {"mappings": {node: sorted(labels) for node, labels in mappings.items()},
                       "relations": relations} for name, (mappings, relations) in profiles.items()}
    return {
        "profiles": profile_count,
        "actions_per_profile": 3 * motifs,
        "labels_per_mapped_action": labels_per_action,
        "total_relations": sum(len(relations) for _, relations in profiles.values()),
        "exhaustive_witness_entries": sum(map(len, full_masks)),
        "focused_witness_entries": sum(map(len, exact)),
        "pooled_only_known": sum(not mask for mask in exact[0].values()),
        "listed_incompatible_joins": sum(len(row["projection_comparisons"]["loop_pairs"]["incompatible_joins"])
                                         for row in answer["profile_answers"].values()),
        "storage": {
            "inputs": storage(snapshot),
            "inputs_and_full_answer": storage({"inputs": snapshot, "answer": answer}),
            "inputs_and_compact_answer": storage({"inputs": snapshot, "answer": compact}),
        },
        "measurements": measure({"exhaustive_masks": exhaustive, "focused_masks": focused,
                                 "full_comparison": lambda: compare_query(profiles, QUERY),
                                 "compact_comparison": lambda: compare_query(profiles, QUERY, summary_only=True)}),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    query = ("T1562", "T1047", "T1053")
    recorded_sizes = {}
    for name, summary_only in (("full", False), ("compact", True)):
        record = export("netsupport-identity", query, summary_only=summary_only)
        verify(record)
        recorded_sizes[name] = storage(record)
    result = {
        "runtime": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                    "os": platform.system(), "os_release": platform.release(), "architecture": platform.machine(),
                    "processor": platform.processor(), "logical_cpus": os.cpu_count()},
        "timed_trials_per_operation": REPEATS,
        "synthetic_query": list(QUERY),
        "workloads": [evaluate(*row) for row in DESIGN],
        "netsupport_export_storage": recorded_sizes,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
