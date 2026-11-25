"""Measure query runtime and compact JSON size on deterministic synthetic DAGs."""
from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import time
from itertools import product
from pathlib import Path

from src.occurrence_queries import compatible_answers, source_answers, technique_answers
from src.sequence_investigation import investigate


def workload(size, shape, labels_per_node):
    nodes = [f"o{i:04}" for i in range(size)]
    labels = [f"T{i:04}" for i in range(1000, 1012)]
    mappings = {node: {labels[(i + 5 * j) % len(labels)] for j in range(labels_per_node)}
                for i, node in enumerate(nodes)}
    if shape == "chain":
        edges = set(zip(nodes, nodes[1:]))
    else:
        middle = size // 2
        edges = {(node, nodes[middle]) for node in nodes[:middle]}
        edges.update((nodes[middle], node) for node in nodes[middle + 1:])
    return mappings, edges


def representations(mappings, edges):
    rows = {(left, right, u, v) for u, v in edges
            for left, right in product(mappings[u], mappings[v])}
    return rows, {(left, right) for left, right, _, _ in rows}


def size_bytes(records):
    return len(json.dumps(sorted(records), separators=(",", ":")).encode("utf-8"))


def samples_ms(operation, repeats):
    operation()
    samples = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        operation()
        samples.append((time.perf_counter_ns() - start) / 1e6)
    return {"median": round(statistics.median(samples), 6),
            "samples": [round(value, 6) for value in samples]}


def measure(size, shape, width, repeats):
    mappings, edges = workload(size, shape, width)
    rows, pairs = representations(mappings, edges)
    source = source_answers(mappings, edges)
    compatible = compatible_answers(rows)
    ordinary = technique_answers(pairs)
    if compatible != source or not source <= ordinary:
        raise AssertionError("The workload disagrees with the occurrence oracle")
    query = min(source)
    relations = [{"relation_id": f"L{i}", "source_event": u, "target_event": v, "relation": "BEFORE"}
                 for i, (u, v) in enumerate(sorted(edges))]
    answer = investigate(mappings, relations, query)
    if answer["status"] != "SUPPORTED":
        raise AssertionError("Expected a supported diagnostic query")
    return {
        "occurrences": size, "edges": len(edges), "shape": shape, "labels_per_node": width,
        "pair_keys": len(pairs), "endpoint_rows": len(rows),
        "pair_json_bytes": size_bytes(pairs), "endpoint_json_bytes": size_bytes(rows),
        "source_answers": len(source), "ordinary_extra_answers": len(ordinary - source),
        "diagnostic_query": query, "diagnostic_witnesses": len(answer["known_witnesses"]),
        "diagnostic_incompatible_joins": sum(len(row["incompatible_joins"])
                                            for row in answer["projection_comparisons"].values()),
        "milliseconds": {
            "encode_both_representations": samples_ms(lambda: representations(mappings, edges), repeats),
            "technique_all_answers": samples_ms(lambda: technique_answers(pairs), repeats),
            "endpoint_all_answers": samples_ms(lambda: compatible_answers(rows), repeats),
            "source_oracle_all_answers": samples_ms(lambda: source_answers(mappings, edges), repeats),
            "investigator_one_query": samples_ms(lambda: investigate(mappings, relations, query), repeats),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=7)
    args = parser.parse_args()
    if args.repeats < 3:
        parser.error("--repeats must be at least three")
    result = {
        "python": platform.python_version(), "system": platform.system(),
        "machine": platform.machine(), "logical_cpus": os.cpu_count(),
        "repeats": args.repeats,
        "workloads": [measure(size, shape, width, args.repeats)
                      for size, shape, width in product((16, 32, 64, 128), ("chain", "hub"), (1, 2))],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="")
    print(f"Measured {len(result['workloads'])} workloads.")


if __name__ == "__main__":
    main()
