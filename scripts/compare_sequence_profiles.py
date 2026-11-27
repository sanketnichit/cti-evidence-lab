"""Export and verify a sequence answer across aligned case interpretations."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from examples.netsupport_identity_sensitivity import identity_profiles
from examples.profile_coherence import witness_masks
from examples.profile_conflicts import explain
from examples.profile_uncertainty import STATUSES
from scripts.audit_rdp_case import digest
from scripts.investigate_sequence import load_case, profile_graph
from src.sequence_investigation import investigate

GROUPS = ("domain-controller", "rdp", "netsupport-identity")


def compare_query(profiles, query, *, summary_only=False):
    query = tuple(query)
    graphs = [(mappings, {(row["source_event"], row["target_event"]) for row in relations})
              for mappings, relations in profiles.values()]
    results = {name: investigate(mappings, relations, query, summary_only=summary_only)
               for name, (mappings, relations) in profiles.items()}
    vocabulary = set(query)
    completed = [({node: labels or vocabulary for node, labels in mappings.items()}, edges)
                 for mappings, edges in graphs]
    pooled = {}
    for kind, inputs in (("known", graphs), ("possible", completed)):
        candidates = []
        for (path, _), mask in sorted(witness_masks(inputs, query=query).items()):
            item = {"occurrence_ids": list(path), "supporting_profiles": [
                name for i, name in enumerate(profiles) if mask & (1 << i)
            ]}
            if not mask:
                item["conflict"] = explain(inputs, path, query)
            candidates.append(item)
        pooled[kind] = candidates
    return {
        "query": list(query),
        "best_profile_status": max((answer["status"] for answer in results.values()), key=STATUSES.index),
        "pooled_status": STATUSES[2 if pooled["known"] else 1 if pooled["possible"] else 0],
        "profile_order": list(profiles),
        "profile_answers": results,
        "pooled_witnesses": pooled,
    }


def comparison_context(group, case=None):
    if group not in GROUPS:
        raise ValueError("Unknown profile group")
    key = "dfir-netsupport" if group == "netsupport-identity" else group
    if case is None:
        case = load_case(key)
    if group == "netsupport-identity":
        profiles = identity_profiles()
    else:
        profiles = {}
        for row in case["profiles"]:
            if row.get("taxonomy_level", "parent") == "parent":
                _, _, mappings, relations = profile_graph(case, row["name"])
                profiles[row["name"]] = (mappings, relations)
    record = {
        "record_version": "1.0", "profile_group": group, "case_key": key,
        "case_sha256": digest(json.dumps(case, sort_keys=True, separators=(",", ":"))),
        "source": case["source"], "evidence": case["evidence"], "occurrences": case["occurrences"],
        "profile_mappings": {
            name: {node: sorted(labels) for node, labels in mappings.items()}
            for name, (mappings, _) in profiles.items()
        }, "relations": {
            name: relations for name, (_, relations) in profiles.items()
        }, "taxonomy_level": "parent",
        "verification_scope": "Exact recomputation against recorded profiles and declared sensitivity alternatives.",
    }
    return record, profiles


def export(group, query, *, summary_only=False):
    record, profiles = comparison_context(group)
    record["answer"] = compare_query(profiles, query, summary_only=summary_only)
    if summary_only:
        record["detail"] = "summary"
    return record


def verify(value):
    if value != export(value["profile_group"], value["answer"]["query"],
                       summary_only=value.get("detail") == "summary"):
        raise ValueError("Comparison differs from recomputation")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--query", nargs=3)
    mode.add_argument("--verify", type=Path)
    parser.add_argument("--group", choices=GROUPS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-only", action="store_true", help="Count per-profile details without listing them")
    args = parser.parse_args()
    if args.verify:
        if args.group or args.output or args.summary_only:
            parser.error("--verify uses only the exported record")
        verify(json.loads(args.verify.read_bytes()))
        print("Verified the profile comparison.")
        return
    if not args.group:
        parser.error("--query requires --group")
    output = json.dumps(export(args.group, args.query, summary_only=args.summary_only), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8", newline="\n")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
