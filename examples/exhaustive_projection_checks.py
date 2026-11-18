"""Exhaustive finite checks of projection definitions, not corpus estimates."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

from examples.representation_controls import edge, project_report_recon


def run_checks():
    vocabulary = ("T1021", "T1105", "T1059")
    subsets = [set(c) for n in range(4) for c in combinations(vocabulary, n)]
    possible_edges = (("a", "b"), ("a", "c"), ("b", "c"))
    states = Counter()
    graphs = cycles = 0
    for assignment in product(subsets, repeat=3):
        mappings = dict(zip(("a", "b", "c"), assignment))
        for mask in range(8):
            edges = [edge(f"e{i}", a, b) for i, (a, b) in enumerate(possible_edges) if mask & (1 << i)]
            result = project_report_recon(mappings, edges)
            graphs += 1
            assert result["counts"]["source_strict_order_cycle_components"] == 0
            for e in edges:
                a, b = mappings[e.source_event], mappings[e.target_event]
                if not a or not b:
                    expected = "unmapped_endpoint"
                elif a == b and len(a) == 1:
                    expected = "fully_omitted"
                elif a & b:
                    expected = "partially_represented"
                else:
                    expected = "no_diagonal_mapping"
                if result["edge_projection_status"][e.edge_id] != expected:
                    raise AssertionError((mappings, e, expected))
                states[expected] += 1
            # Independent reachability oracle, separate from the SCC implementation.
            reach = {(a, b) for e in edges for a in mappings[e.source_event]
                     for b in mappings[e.target_event] if a != b}
            for k in vocabulary:
                reach |= {(a, b) for a in vocabulary for b in vocabulary
                          if (a, k) in reach and (k, b) in reach}
            expected_cycle = any((t, t) in reach for t in vocabulary)
            observed_cycle = result["counts"]["projected_strict_order_cycle_components"] > 0
            if expected_cycle != observed_cycle:
                raise AssertionError("Cycle oracle disagreement")
            cycles += observed_cycle
    return {
        "status": "EXHAUSTIVE_FINITE_CONTROLS_NOT_REPORT_MEASUREMENTS",
        "design": "Three ordered event vertices; all eight subsets of forward BEFORE edges; all eight subsets of three technique IDs independently assigned to each event, including empty mappings.",
        "graphs_checked": graphs,
        "source_edge_instances_checked": sum(states.values()),
        "edge_states": dict(sorted(states.items())),
        "graphs_with_projected_cycles": cycles,
        "edge_state_oracle_disagreements": 0,
        "cycle_oracle_disagreements": 0,
        "scope_limit": "No assertion about larger graphs, other temporal labels, annotation accuracy, or CTI prevalence. Frequencies depend on this deliberately exhaustive construction.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run_checks(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
