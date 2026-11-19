"""Explain and verify sequence-query answers against the recorded source cases."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.analyze_sequence_case import CASE as RDP_CASE, analyze as analyze_rdp
from scripts.analyze_incident_sequences import CASE as DC_CASE, analyze as analyze_dc
from scripts.audit_rdp_case import digest
from src.sequence_investigation import investigate

CASES = {"rdp": RDP_CASE, "domain-controller": DC_CASE}


def load_case(key):
    path = CASES[key]
    case = json.loads(path.read_text(encoding="utf-8"))
    if key == "rdp":
        analyze_rdp(case)
    else:
        analyze_dc(case, json.loads((path.parent / "selection.json").read_text(encoding="utf-8")))
    return case


def profile_graph(case, name):
    profiles = {p["name"]: p for p in case["profiles"]}
    if name not in profiles:
        raise ValueError("Unknown profile: " + name)
    profile = profiles[name]
    nodes = {n["event_id"]: n for n in case["occurrences"] if n["event_id"] in profile["occurrence_ids"]}
    level = profile.get("taxonomy_level", "parent")
    withheld = set(profile.get("withheld_mapping_ids", []))
    for key, node in nodes.items():
        if node["mapping_status"] == "UNRESOLVED_CLEANUP_PURPOSE" and not profile.get("assume_cleanup_mapping", False):
            withheld.add(key)
    mappings = {key: set() if key in withheld else {node["candidate_" + level + "_mapping"]} for key, node in nodes.items()}
    relations = [r for r in case["relations"] if r["relation_id"] in profile["relation_ids"]]
    return profile, nodes, mappings, relations


def certificate(key, case, profile_name, query):
    profile, nodes, mappings, relations = profile_graph(case, profile_name)
    answer = investigate(mappings, relations, query)
    body = {"certificate_version": "1.0", "case_key": key, "case_id": case["case_id"],
            "case_record_sha256": digest(json.dumps(case, sort_keys=True, separators=(",", ":"))),
            "profile": profile, "source": case["source"], "interpretation_status": case["status"],
            "independently_validated": case["independently_validated"], "answer": answer,
            "occurrences": [{**node, "active_mappings": sorted(mappings[nid])} for nid, node in nodes.items()],
            "relations": relations, "evidence": case["evidence"],
            "verification_scope": "Recomputation checks agreement with repository case records; source bytes require the separate source audit. No semantic validation or digital signature is implied."}
    body["certificate_sha256"] = digest(json.dumps(body, sort_keys=True, separators=(",", ":")))
    return body


def verify_certificate(value):
    key = value["case_key"]
    expected = certificate(key, load_case(key), value["profile"]["name"], value["answer"]["query"])
    if value != expected:
        raise ValueError("Certificate differs from recomputation against current case records")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=sorted(CASES), default="domain-controller")
    parser.add_argument("--profile", default="extended_script_sequence")
    parser.add_argument("--query", nargs=3)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.verify:
        verify_certificate(json.loads(args.verify.read_text(encoding="utf-8")))
        print("PASS: certificate matches current case records; semantic correctness is not established by this check.")
        return
    if not args.query:
        parser.error("--query requires three technique identifiers")
    result = certificate(args.case, load_case(args.case), args.profile, args.query)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="")
    else:
        print(text)


if __name__ == "__main__":
    main()
