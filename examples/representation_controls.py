"""Deterministic representation controls, not observations from CTI reports.

Compare distinct-technique pairs, technique pairs with loops, and an
occurrence-preserving representation. Source-edge provenance is retained as
an audit sidecar; a bare technique graph does not contain that sidecar.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/analysis"))
from projection_metrics_recon import TemporalEdge, project_report_recon


def compare(mappings, edges):
    primary = project_report_recon(mappings, edges)
    loop_provenance = defaultdict(set)
    for edge in edges:
        for a, b in primary["projection"]["edge_to_pairs"][edge.edge_id]:
            label = edge.relation
            if label == "AFTER":
                a, b, label = b, a, "BEFORE"
            elif label in {"OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"}:
                a, b = sorted((a, b))
            loop_provenance[(label, a, b)].add(edge.edge_id)
    return {
        "primary": primary,
        "loop_permitting": {
            "unique_labeled_pairs": len(loop_provenance),
            "unique_labeled_self_loops": sum(a == b for _, a, b in loop_provenance),
            "collision_keys": sum(len(ids) > 1 for ids in loop_provenance.values()),
            "source_edges_with_any_image": len(set().union(*loop_provenance.values())) if loop_provenance else 0,
            "pair_provenance": [
                {"relation": label, "source_technique": a, "target_technique": b,
                 "source_edge_ids": sorted(ids)}
                for (label, a, b), ids in sorted(loop_provenance.items())
            ],
        },
        "occurrence_preserving": {
            "nodes": len(mappings), "edges": len(edges),
            "edge_endpoints": [
                {"edge_id": e.edge_id, "source_event": e.source_event,
                 "target_event": e.target_event, "relation": e.relation}
                for e in sorted(edges, key=lambda e: e.edge_id)
            ],
        },
    }


def edge(name, a, b, relation="BEFORE"):
    return TemporalEdge(name, a, b, relation, "direct_source", "COMPATIBLE")


def run_controls():
    cases = [
        ("distinct_mapping", {"a": {"T1021"}, "b": {"T1105"}}, [edge("e1", "a", "b")]),
        ("same_technique", {"a": {"T1021"}, "b": {"T1021"}}, [edge("e1", "a", "b")]),
        ("repeated_same_technique", {"a": {"T1021"}, "b": {"T1021"}, "c": {"T1021"}},
         [edge("e1", "a", "b"), edge("e2", "b", "c")]),
        ("mixed_mapping", {"a": {"T1021"}, "b": {"T1021", "T1105"}}, [edge("e1", "a", "b")]),
        ("unmapped_endpoint", {"a": set(), "b": {"T1021"}}, [edge("e1", "a", "b")]),
        ("occurrence_collapse_cycle", {"a": {"T1021"}, "b": {"T1105"}, "c": {"T1021"}},
         [edge("e1", "a", "b"), edge("e2", "b", "c")]),
        ("single_edge_fanout_cycle", {"a": {"T1021", "T1105"}, "b": {"T1021", "T1105"}},
         [edge("e1", "a", "b")]),
    ]
    return {
        "status": "SYNTHETIC_REPRESENTATION_CONTROLS_NOT_EMPIRICAL_RESULTS",
        "scope": "Named finite counterexamples; no learned model, corpus rate, or exhaustive theorem testing",
        "cases": {name: compare(mappings, edges) for name, mappings, edges in cases},
    }


def markdown(result):
    lines = ["# Representation controls", "", result["status"], "",
             "All inputs are synthetic. Counts describe representations, not reports or model accuracy.", "",
             "| Control | Source edges | Fully omitted | Partially represented | Unmapped | Distinct pairs | Loop-inclusive labeled pairs | Loop collision keys | Projected strict cycles |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name, case in result["cases"].items():
        c, loop = case["primary"]["counts"], case["loop_permitting"]
        values = [c[k] for k in ("positive_temporal_edges", "fully_omitted_edges", "partially_represented_edges", "unmapped_endpoint_edges", "unique_distinct_technique_pairs")]
        values += [loop["unique_labeled_pairs"], loop["collision_keys"], c["projected_strict_order_cycle_components"]]
        lines.append("| " + name + " | " + " | ".join(map(str, values)) + " |")
    lines += ["", "Loop-inclusive counts retain relation labels; primary distinct-pair counts are label-agnostic. These controls use only BEFORE, so the counts are comparable here.", "",
              "A self-loop preserves a technique-level image but not which two occurrences it connects. The repeated-same-technique control merges two relations into one loop. An occurrence-preserving graph retains the supplied endpoints even when mappings are absent.", "",
              "Both cycle controls have acyclic source graphs. One needs two source edges; the other is caused by Cartesian mapping fan-out from a single edge. Therefore a projected cycle alone does not diagnose repeated executions or source inconsistency.", "",
              "Reproduce: `python -m examples.representation_controls --output-dir research/experiments/representation_controls_v0.1`", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    result = run_controls()
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
        (args.output_dir / "README.md").write_text(markdown(result), encoding="utf-8", newline="")
    else:
        print(markdown(result))


if __name__ == "__main__":
    main()
