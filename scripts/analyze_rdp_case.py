"""Evaluate a source-bound exploratory case under declared inclusion choices.

This does not create selected-final annotations, gold labels or corpus rates.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from examples.representation_controls import compare, edge
from scripts.audit_rdp_case import CASE, digest

CROSSWALK = ROOT / "research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/vocabulary/A_120_Exact_to_Parent_Crosswalk_v0.1.csv"


def analyze(case):
    if case["status"] != "EXPLORATORY_SOURCE_INTERPRETATION" or case["sample_membership"] != "PURPOSIVE_OUTSIDE_ANNOCTR":
        raise ValueError("This analysis is scoped to the separately selected exploratory case")
    if case["independently_validated"] or case["eligible_for_corpus_denominator"]:
        raise ValueError("Independent validation and corpus inclusion are not established by this case")
    if digest(CROSSWALK.read_bytes()) != case["taxonomy"]["crosswalk_sha256"]:
        raise ValueError("Pinned taxonomy crosswalk changed")
    with CROSSWALK.open(encoding="utf-8-sig", newline="") as handle:
        taxonomy = {r["exact_technique_id"]: r for r in csv.DictReader(handle)}
    evidence_ids = {s["evidence_id"] for s in case["evidence"]}
    events = {e["event_id"]: e for e in case["occurrences"]}
    if len(events) != len(case["occurrences"]):
        raise ValueError("Duplicate occurrence IDs")
    for item in case["occurrences"] + case["relations"]:
        if not item["evidence_ids"] or not set(item["evidence_ids"]) <= evidence_ids:
            raise ValueError("Missing evidence binding")
    for event in events.values():
        row = taxonomy.get(event["exact_mapping"])
        if not row or row["parent_technique_id"] != event["parent_mapping"] or row["parent_in_A_120"] != "true":
            raise ValueError("Case mapping does not match the pinned parent crosswalk")
    for relation in case["relations"]:
        if relation["source_event"] not in events or relation["target_event"] not in events:
            raise ValueError("Unknown occurrence endpoint")
        if relation["source_event"] == relation["target_event"] or relation["relation"] != "BEFORE":
            raise ValueError("Expected two distinct occurrences with a BEFORE relation")
    profiles = {}
    for name in ("attempts_included", "successful_actions_only", "mapping_withheld"):
        selected = {k: v for k, v in events.items() if name != "successful_actions_only" or v["outcome"] == "SUCCESS_CONFIRMED"}
        mappings = {k: set() if name == "mapping_withheld" else {v["parent_mapping"]} for k, v in selected.items()}
        edges = [edge(r["relation_id"], r["source_event"], r["target_event"]) for r in case["relations"]
                 if r["source_event"] in selected and r["target_event"] in selected]
        compared = compare(mappings, edges)
        c = compared["primary"]["counts"]
        profiles[name] = {"included_occurrences": len(selected), "included_before_edges": len(edges),
                          "fully_omitted_edges": c["fully_omitted_edges"],
                          "unmapped_endpoint_edges": c["unmapped_endpoint_edges"],
                          "distinct_technique_pairs": c["unique_distinct_technique_pairs"],
                          "loop_inclusive_pairs": compared["loop_permitting"]["unique_labeled_pairs"],
                          "occurrence_endpoints": compared["occurrence_preserving"]["edge_endpoints"]}
    return {"status": "EXPLORATORY_CASE_SENSITIVITY_NOT_POPULATION_ESTIMATE",
            "case_id": case["case_id"], "independently_validated": False,
            "source_verification": "RECORDED_BINDINGS; recheck the saved publisher HTML with audit_rdp_case.py",
            "case_record_sha256": digest(json.dumps(case, sort_keys=True, separators=(",", ":"))),
            "profiles": profiles,
            "two_step_query_evaluation": "NOT_APPLICABLE: the retained case has two occurrences and one supplied edge, not a three-occurrence chain"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, default=CASE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(analyze(json.loads(args.case.read_text(encoding="utf-8"))), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8", newline="")
    else:
        print(result)
