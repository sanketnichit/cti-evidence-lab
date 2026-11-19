"""Evaluate explicit source interpretations with named mapping/edge profiles."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.analyze_rdp_case import CROSSWALK
from scripts.audit_rdp_case import digest
from src.occurrence_queries import evaluate_with_coverage, validate

CASE = ROOT / "research/case_studies/dfir_html_smuggling_v0.1/case.json"


def unique(items, key):
    result = {item[key]: item for item in items}
    if not result or len(result) != len(items):
        raise ValueError("Empty or duplicate identity list: " + key)
    return result


def analyze(case, selection):
    posts = selection["returned_posts"]
    if not posts or posts != sorted(posts, key=lambda p: (p["date"], p["id"])) or selection["selected_post_id"] != posts[0]["id"] or selection["selected_url"] != posts[0]["link"] or case["source"]["url"] != selection["selected_url"]:
        raise ValueError("Case does not match the declared next-report selection")
    if case["status"] != "EXPLORATORY_SOURCE_INTERPRETATION" or case["independently_validated"] is not False or case["eligible_for_corpus_denominator"] is not False:
        raise ValueError("Exploratory case cannot establish independent or corpus validation")
    if digest(CROSSWALK.read_bytes()) != case["taxonomy"]["crosswalk_sha256"]:
        raise ValueError("Pinned crosswalk changed")
    with CROSSWALK.open(encoding="utf-8-sig", newline="") as handle:
        taxonomy = {r["exact_technique_id"]: r for r in csv.DictReader(handle)}
    evidence = unique(case["evidence"], "evidence_id")
    nodes = unique(case["occurrences"], "event_id")
    relations = unique(case["relations"], "relation_id")
    profiles = unique(case["profiles"], "name")
    for item in list(nodes.values()) + list(relations.values()):
        if not item["evidence_ids"] or not set(item["evidence_ids"]) <= evidence.keys():
            raise ValueError("Missing source evidence")
    for n in nodes.values():
        row = taxonomy.get(n["candidate_exact_mapping"])
        if not row or row["parent_in_A_120"] != "true" or row["parent_technique_id"] != n["candidate_parent_mapping"]:
            raise ValueError("Invalid pinned candidate mapping")
        if n["mapping_status"] not in {"PROPOSED_SOURCE_BEHAVIOR", "PROPOSED_PURPOSE_SENSITIVE"} or n["activity_stratum"] != "REPORTED_INTRUSION_ACTION":
            raise ValueError("Unsupported mapping status or activity stratum")
    all_edges = set()
    for r in relations.values():
        u, v = r["source_event"], r["target_event"]
        if u not in nodes or v not in nodes or not r["incident_id"]:
            raise ValueError("Unknown endpoint or missing incident scope")
        if r["relation"] != "BEFORE" or r["basis"] != "EXPLICIT_SOURCE_ORDERING" or nodes[u]["incident_id"] != r["incident_id"] or nodes[v]["incident_id"] != r["incident_id"]:
            raise ValueError("Unsupported relation or incident scope")
        all_edges.add((u, v))
    validate({key: set() for key in nodes}, all_edges)
    results = {}
    for name, profile in profiles.items():
        ids, edges, withheld = profile["occurrence_ids"], profile["relation_ids"], profile["withheld_mapping_ids"]
        if len(ids) != len(set(ids)) or len(edges) != len(set(edges)) or len(withheld) != len(set(withheld)):
            raise ValueError("Duplicate profile inclusion")
        if not set(ids) <= nodes.keys() or not set(edges) <= relations.keys() or not set(withheld) <= set(ids):
            raise ValueError("Unknown profile inclusion")
        level = profile["taxonomy_level"]
        if level not in {"parent", "exact"}:
            raise ValueError("Unknown taxonomy level")
        mappings = {key: set() if key in withheld else {nodes[key]["candidate_" + level + "_mapping"]} for key in ids}
        before = {(relations[key]["source_event"], relations[key]["target_event"]) for key in edges}
        results[name] = {"taxonomy_level": level, "withheld_mapping_ids": withheld, **evaluate_with_coverage(mappings, before)}
    return {"case_id": case["case_id"], "case_record_sha256": digest(json.dumps(case, sort_keys=True, separators=(",", ":"))),
            "status": "EXPLORATORY_SEQUENCE_SENSITIVITY", "profiles": results,
            "query_semantics": "Three distinct occurrences joined by two supplied BEFORE edges; no transitive closure or immediate adjacency assumed.",
            "negative_answer_semantics": "Unsupported by the retained interpreted graph, not proven absent from the intrusion."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, default=CASE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    selection = json.loads((args.case.parent / "selection.json").read_text(encoding="utf-8"))
    text = json.dumps(analyze(json.loads(args.case.read_text(encoding="utf-8")), selection), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="")
    else:
        print(text)
