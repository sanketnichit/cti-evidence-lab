"""Compare exact answer-only encodings with endpoint rows and ordinary pairs."""
from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

from examples.sequence_scaling import representations, size_bytes, workload
from scripts.investigate_sequence import AVAILABLE_CASES, ROOT, load_case, profile_graph
from src.occurrence_queries import compatible_answers, middle_label_signatures, signature_answers, source_answers
from src.sequence_investigation import investigate

RESULTS = ROOT / "research/experiments/sequence_scaling_v0.1/answer_index_storage.json"


def measure(mappings, edges):
    truth = source_answers(mappings, edges)
    rows, pairs = representations(mappings, edges)
    signatures = middle_label_signatures(mappings, edges)
    triples = signature_answers(signatures)
    if triples != truth or compatible_answers(rows) != truth:
        raise AssertionError("An exact answer encoding disagrees with the independent occurrence oracle")
    return {
        "occurrences": len(mappings), "edges": len(edges),
        "unknown_occurrences": sum(not labels for labels in mappings.values()),
        "encodings": {
            name: {"records": len(data), "json_bytes": size_bytes(data)}
            for name, data in (("ordinary_pairs", pairs), ("endpoint_rows", rows),
                               ("middle_signatures", signatures), ("materialized_triples", triples))
        },
    }


def wide_hub(width):
    left = {f"l{i:03}": {f"T{i + 2000}"} for i in range(width)}
    right = {f"r{i:03}": {f"T{i + 3000}"} for i in range(width)}
    edges = {(node, "middle") for node in left} | {("middle", node) for node in right}
    return {**left, "middle": {"T1000"}, **right}, edges


def witness_counterexample():
    mappings = {"u1": {"A"}, "u2": {"A"}, "v": {"B"}, "w": {"C"}}
    graphs = [{(start, "v"), ("v", "w")} for start in ("u1", "u2")]
    signatures = [middle_label_signatures(mappings, edges) for edges in graphs]
    answers = []
    for edges in graphs:
        relations = [{"relation_id": f"L{i}", "source_event": u, "target_event": v, "relation": "BEFORE"}
                     for i, (u, v) in enumerate(sorted(edges))]
        answers.append(investigate(mappings, relations, ("A", "B", "C"))["known_witnesses"][0]["occurrence_ids"])
    if signatures[0] != signatures[1] or answers[0] == answers[1]:
        raise AssertionError("Expected identical signatures and different witnesses")
    return {"same_answer_only_encoding": True, "query": ["A", "B", "C"], "witnesses": answers}


def run():
    synthetic = [
        {"shape": shape, "labels_per_occurrence": labels, **measure(*workload(size, shape, labels))}
        for size, shape, labels in product((16, 32, 64, 128), ("chain", "hub"), (1, 2))
    ]
    for width in (8, 32, 128):
        row = measure(*wide_hub(width))
        if row["encodings"]["materialized_triples"]["records"] != width ** 2:
            raise AssertionError("The wide hub should support the full label cross product")
        synthetic.append({"shape": "wide_label_hub", "labels_per_occurrence": 1, "width_per_side": width, **row})
    profiles = []
    for key in AVAILABLE_CASES:
        case = load_case(key)
        for profile in case["profiles"]:
            _, _, mappings, relations = profile_graph(case, profile["name"])
            edges = {(row["source_event"], row["target_event"]) for row in relations}
            profiles.append({"case": key, "profile": profile["name"], **measure(mappings, edges)})
    return {"synthetic_workloads": synthetic, "recorded_profiles": profiles,
            "witness_counterexample": witness_counterexample()}


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
            raise SystemExit("Answer-index storage differs from the published results")
        print("Reproduced exact answer-index storage measurements.")


if __name__ == "__main__":
    main()
