"""Finite, controlled evaluation of connected two-step sequence queries."""
from __future__ import annotations

import argparse
import json
from itertools import combinations, product
from pathlib import Path

from src.occurrence_queries import evaluate

VOCABULARY = ("T1059", "T1105", "T1021")
QUERIES = set(product(VOCABULARY, repeat=3))


def confusion(truth, answers, universe):
    truth, answers = truth & universe, answers & universe
    return {"tp": len(truth & answers), "fp": len(answers - truth),
            "fn": len(truth - answers), "tn": len(universe - (truth | answers))}


def run_design(vertices, mapping_options):
    possible_edges = list(combinations(vertices, 2))
    totals = {}
    graph_count = 0
    storage = {}
    strata = {"all_queries": QUERIES,
              "distinct_adjacent_labels": {q for q in QUERIES if q[0] != q[1] and q[1] != q[2]}}
    for assignment in product(mapping_options, repeat=len(vertices)):
        mappings = dict(zip(vertices, assignment))
        for mask in range(2 ** len(possible_edges)):
            edges = [e for i, e in enumerate(possible_edges) if mask & (1 << i)]
            result = evaluate(mappings, edges)
            graph_count += 1
            for key, value in result["storage"].items():
                storage[key] = storage.get(key, 0) + value
            for stratum, universe in strata.items():
                for name, answers in result["answers"].items():
                    bucket = totals.setdefault(stratum, {}).setdefault(name, {k: 0 for k in ("tp", "fp", "fn", "tn")})
                    for key, value in confusion(result["truth"], answers, universe).items():
                        bucket[key] += value
    for models in totals.values():
        for bucket in models.values():
            tp, fp, fn = (bucket[k] for k in ("tp", "fp", "fn"))
            bucket["precision"] = tp / (tp + fp) if tp + fp else None
            bucket["recall"] = tp / (tp + fn) if tp + fn else None
    return {"graphs": graph_count, "queries_per_graph": {k: len(v) for k, v in strata.items()},
            "confusion": totals, "storage_row_totals": storage}


def counterexamples():
    a, b, c = VOCABULARY
    mappings = {"u": {a}, "v": {b}, "w": {b}, "x": {c}}
    cases = {
        "disconnected_occurrences": (mappings, [("u", "v"), ("w", "x")]),
        "connected_occurrences_same_technique_graph": (mappings, [("u", "v"), ("v", "x")]),
        "single_edge_reused_as_two_hops": ({"u": {a}, "v": {a}}, [("u", "v")]),
        "genuine_repeated_technique_chain": ({"u": {a}, "v": {a}, "w": {a}}, [("u", "v"), ("v", "w")]),
    }
    output = {}
    for name, (mapping, edges) in cases.items():
        result = evaluate(mapping, edges)
        output[name] = {"mappings": {k: sorted(v) for k, v in mapping.items()}, "before_edges": edges,
                        "source_answers": sorted(result["truth"]),
                        "answers": {k: sorted(v) for k, v in result["answers"].items()},
                        "storage": result["storage"]}
    return output


def run_benchmark():
    subsets = [set(c) for n in range(4) for c in combinations(VOCABULARY, n)]
    return {
        "status": "CONTROLLED_QUERY_FIDELITY_NOT_EXTRACTION_PERFORMANCE",
        "query": "Existence of three distinct occurrences u,v,w with supplied BEFORE edges u->v and v->w and respective technique labels A,B,C. No inferred transitive edges.",
        "weighting": "One vote per (generated graph, technique triple); graphs are exhaustive under a fixed vertex order, not sampled CTI incidents or uniformly weighted isomorphism classes.",
        "designs": {
            "four_vertices_singleton_mappings": run_design(("a", "b", "c", "d"), [{v} for v in VOCABULARY]),
            "three_vertices_set_valued_mappings": run_design(("a", "b", "c"), subsets),
        },
        "counterexamples": counterexamples(),
        "limits": ["Supplied occurrences, mappings and BEFORE edges are assumed correct; no extraction or semantic validation is evaluated.",
                   "Only length-two paths in finite DAGs with three technique IDs are covered.",
                   "Exact endpoint joins preserve the defined query by construction; perfect fidelity is not a novel prediction result.",
                   "Storage counts are logical records, not measured memory or runtime.",
                   "Empty mapping sets cannot answer technique queries; zero query error is not full source coverage."]
    }


def markdown(result):
    lines = ["# Connected-sequence query benchmark", "", result["status"], "",
             "The input graphs and all labels are synthetic. Rates measure query fidelity to these inputs, not performance on CTI reports.", "",
             "| Design | Representation | TP | FP | FN | TN | Precision | Recall |",
             "|---|---|---:|---:|---:|---:|---:|---:|"]
    for design, values in result["designs"].items():
        for model, counts in values["confusion"]["all_queries"].items():
            line = [design, model] + [str(counts[k]) for k in ("tp", "fp", "fn", "tn")]
            line += [f"{counts[k]:.4f}" if counts[k] is not None else "undefined" for k in ("precision", "recall")]
            lines.append("| " + " | ".join(line) + " |")
    lines += ["", "Full JSON also reports the distinct-adjacent-label stratum, logical storage totals, exact query definition and four inspectable counterexamples.", "",
              "Reproduce: `python -m examples.query_fidelity_benchmark --output-dir research/experiments/query_fidelity_v0.1`", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    result = run_benchmark()
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
        (args.output_dir / "README.md").write_text(markdown(result), encoding="utf-8", newline="")
    else:
        print(markdown(result))
