"""Source-bound sequence sensitivity with explicit mapping coverage.

Results are conditional on an exploratory interpretation. Unmapped paths do
not become negative answers or a perfect-fidelity score.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_rdp_case import digest
from scripts.analyze_rdp_case import CROSSWALK
from src.occurrence_queries import evaluate_with_coverage, validate

CASE = ROOT / "research/case_studies/dfir_rdp_sequence_v0.2/case.json"


def analyze(case):
    if case["status"] != "EXPLORATORY_SOURCE_INTERPRETATION" or case["independently_validated"] or case["eligible_for_corpus_denominator"]:
        raise ValueError("This case cannot establish gold validation or population inclusion")
    if digest(CROSSWALK.read_bytes()) != case["taxonomy"]["crosswalk_sha256"]:
        raise ValueError("Taxonomy crosswalk changed")
    with CROSSWALK.open(encoding="utf-8-sig", newline="") as handle:
        taxonomy = {r["exact_technique_id"]: r for r in csv.DictReader(handle)}
    evidence_ids = {e["evidence_id"] for e in case["evidence"]}
    nodes = {e["event_id"]: e for e in case["occurrences"]}
    relations = {e["relation_id"]: e for e in case["relations"]}
    if len(nodes) != len(case["occurrences"]) or len(relations) != len(case["relations"]):
        raise ValueError("Duplicate event or relation identity")
    for item in case["occurrences"] + case["relations"]:
        if not item["evidence_ids"] or not set(item["evidence_ids"]) <= evidence_ids:
            raise ValueError("Missing source evidence reference")
    for node in nodes.values():
        if node["mapping_status"] not in {"PROPOSED_ATTEMPTED_BEHAVIOR", "UNRESOLVED_CLEANUP_PURPOSE"}:
            raise ValueError("Unsupported mapping status")
        row = taxonomy.get(node["candidate_exact_mapping"])
        if not row or row["parent_technique_id"] != node["candidate_parent_mapping"] or row["parent_in_A_120"] != "true":
            raise ValueError("Invalid exact-to-parent candidate mapping")
    for r in relations.values():
        if r["relation"] != "BEFORE" or r["basis"] != "DIRECT_NARRATIVE_ORDERING":
            raise ValueError("Only explicitly interpreted BEFORE edges are in scope")
    all_edges = {(r["source_event"], r["target_event"]) for r in relations.values()}
    validate({k: set() for k in nodes}, all_edges)
    for r in relations.values():
        if not r["incident_id"] or nodes[r["source_event"]]["incident_id"] != r["incident_id"] or nodes[r["target_event"]]["incident_id"] != r["incident_id"]:
            raise ValueError("Sequence crosses an unresolved or mismatched incident scope")
    names = [p["name"] for p in case["profiles"]]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate profile name")
    profiles = {}
    for profile in case["profiles"]:
        if type(profile["assume_cleanup_mapping"]) is not bool:
            raise ValueError("Mapping assumption must be an explicit Boolean")
        ids = profile["occurrence_ids"]
        edge_ids = profile["relation_ids"]
        if len(ids) != len(set(ids)) or len(edge_ids) != len(set(edge_ids)):
            raise ValueError("Duplicate profile inclusion")
        if not set(ids) <= nodes.keys() or not set(edge_ids) <= relations.keys():
            raise ValueError("Unknown profile inclusion")
        mappings = {}
        for key in ids:
            n = nodes[key]
            unresolved = n["mapping_status"] == "UNRESOLVED_CLEANUP_PURPOSE"
            mappings[key] = set() if unresolved and not profile["assume_cleanup_mapping"] else {n["candidate_parent_mapping"]}
        edges = {(relations[k]["source_event"], relations[k]["target_event"]) for k in edge_ids}
        profiles[profile["name"]] = {
            "assume_cleanup_mapping": profile["assume_cleanup_mapping"],
            **evaluate_with_coverage(mappings, edges),
        }
    return {"case_id": case["case_id"], "status": "EXPLORATORY_SEQUENCE_SENSITIVITY",
            "case_record_sha256": digest(json.dumps(case, sort_keys=True, separators=(",", ":"))),
            "query_semantics": "Two supplied BEFORE edges sharing an intermediate occurrence; not necessarily adjacent actions; no transitive closure added.",
            "negative_answer_semantics": "Unsupported by the retained interpreted graph, not proven absent from the intrusion.",
            "profiles": profiles}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, default=CASE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(analyze(json.loads(args.case.read_text(encoding="utf-8"))), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="")
    else:
        print(text)
