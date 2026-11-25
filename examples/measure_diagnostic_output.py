"""Measure exact count-only and expanded sequence diagnostics under output pressure."""
import argparse
import json
import os
import platform
from pathlib import Path

from examples.sequence_scaling import samples_ms
from src.sequence_investigation import investigate

QUERY = ("A", "A", "A")
MODES = ("disjoint_edges", "mapped_hub", "unmapped_hub", "bounded_hub")


def workload(width, mode):
    left = [f"l{i:05d}" for i in range(width)]
    right = [f"r{i:05d}" for i in range(width)]
    mappings = {node: {"A"} for node in left + right}
    if mode == "disjoint_edges":
        edges = list(zip(left, right))
    else:
        mappings["hub"] = {"A"} if mode == "mapped_hub" else set()
        edges = [(node, "hub") for node in left] + [("hub", node) for node in right]
    relations = [dict(relation_id=f"L{i}", source_event=u, target_event=v, relation="BEFORE")
                 for i, (u, v) in enumerate(edges)]
    domains = {"hub": {"B"}} if mode == "bounded_hub" else None
    return mappings, relations, domains


def measure(width, mode, *, expanded, repeats):
    mappings, relations, domains = workload(width, mode)
    square = width ** 2
    # Closed-form graph counts serve as a separate check on both implementations.
    expected = {
        "disjoint_edges": ("NOT_SUPPORTED", 0, 0, 0, square),
        "mapped_hub": ("SUPPORTED", square, 0, 0, 3 * square),
        "unmapped_hub": ("UNRESOLVED_MAPPING", 0, square, 0, 0),
        "bounded_hub": ("NOT_SUPPORTED", 0, 0, square, 0),
    }[mode]
    row = dict(mode=mode, width=width, occurrences=len(mappings), edges=len(relations),
               status=expected[0], known=expected[1], unresolved=expected[2],
               excluded=expected[3], incompatible_loop_joins=expected[4])

    def answer(summary):
        return investigate(mappings, relations, QUERY, mapping_domains=domains, summary_only=summary)

    def encode(summary):
        return json.dumps(answer(summary), separators=(",", ":")).encode("utf-8")

    full = answer(False) if expanded else None
    compact = answer(True)
    loop = compact["projection_comparisons"]["loop_pairs"]
    distinct = compact["projection_comparisons"]["distinct_pairs"]
    if (compact["status"], compact["known_witness_count"], compact["unresolved_witness_count"],
        compact.get("domain_excluded_witness_count", 0), loop["incompatible_join_count"]) != expected:
        raise AssertionError(f"Closed-form counts differ for {mode} at width {width}")
    if distinct["incompatible_join_count"] or distinct["returned"]:
        raise AssertionError("Distinct pairs should suppress the repeated label")
    if full is not None:
        full["known_witness_count"] = len(full.pop("known_witnesses"))
        full["unresolved_witness_count"] = len(full.pop("unresolved_witnesses"))
        if domains:
            full["domain_excluded_witness_count"] = len(full.pop("domain_excluded_witnesses"))
        for comparison in full["projection_comparisons"].values():
            comparison["incompatible_join_count"] = len(comparison.pop("incompatible_joins"))
        if full != compact:
            raise AssertionError(f"Expanded and count-only records differ for {mode} at width {width}")

    methods = [("counts", True)]
    if expanded:
        methods.append(("expanded", False))
    if (width // 16 + MODES.index(mode)) % 2:
        methods.reverse()
    for name, summary in methods:
        row[name] = {"json_bytes": len(encode(summary)),
                     "query_and_json_ms": samples_ms(lambda: encode(summary), repeats)}
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repeats = 7
    rows = [measure(width, mode, expanded=width <= 128, repeats=repeats)
            for width in (16, 64, 128, 4096) for mode in MODES]
    result = dict(python=platform.python_version(), system=platform.system(),
                  machine=platform.machine(), logical_cpus=os.cpu_count(),
                  query=QUERY, repeats=repeats, workloads=rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="")
    print(f"Measured {len(rows)} workloads and checked their closed-form counts.")


if __name__ == "__main__":
    main()
