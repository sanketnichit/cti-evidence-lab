"""Explain and verify sequence-query answers against the recorded source cases."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.analyze_sequence_case import CASE as RDP_CASE, analyze as analyze_rdp
from scripts.analyze_incident_sequences import CASE as DC_CASE, analyze as analyze_dc
from scripts.audit_rdp_case import digest
from scripts.evaluate_incident_holdout import DIRECTORY as HOLDOUT, run as check_holdout
from scripts.evaluate_cisa_extension import DIRECTORY as CISA, run as check_cisa
from src.sequence_investigation import investigate

CASES = {"rdp": RDP_CASE, "domain-controller": DC_CASE}
EXTENSION_CASES = {
    "dfir-hive": HOLDOUT / "21520.json",
    "dfir-netsupport": HOLDOUT / "22587.json",
    "cisa-former-account": CISA / "AA24-046A.json",
    "cisa-federal-agency": CISA / "AA25-266A.json",
}
AVAILABLE_CASES = {**CASES, **EXTENSION_CASES}


def extension_case(case):
    is_pdf = "product_id" in case
    identifier = case.get("product_id", case.get("post_id"))
    results = (check_cisa() if is_pdf else check_holdout())["cases"]
    result = next(row for row in results if row.get("product_id" if is_pdf else "post_id") == identifier)
    source = {**case["source"]}
    if is_pdf:
        source["title"] = {
            "AA24-046A": "CISA AA24-046A · Former employee account",
            "AA25-266A": "CISA AA25-266A · Incident response engagement",
        }[identifier]
    nodes = [{
        **record,
        "candidate_parent_mapping": record["mapping"],
        "mapping_rationale": record.get("mapping_rationale", record.get("rationale")),
        "mapping_status": "PROPOSED_SOURCE_BEHAVIOR" if record["mapping"] else "WITHHELD",
    } for record in case["occurrences"]]
    return {
        **case,
        "source": source,
        "case_id": str(identifier),
        "status": "EXPLORATORY_SOURCE_INTERPRETATION",
        "query_assessment": result["query_assessment"],
        "occurrences": nodes,
        "profiles": [{
            "name": "recorded_parent_profile",
            "taxonomy_level": "parent",
            "occurrence_ids": [node["event_id"] for node in nodes],
            "relation_ids": [row["relation_id"] for row in case["relations"]],
            "withheld_mapping_ids": [node["event_id"] for node in nodes if not node["mapping"]],
        }],
    }


def load_case(key):
    path = AVAILABLE_CASES[key]
    case = json.loads(path.read_text(encoding="utf-8"))
    if key in EXTENSION_CASES:
        return extension_case(case)
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


def constraint_domains(record, nodes, mappings, evidence, level):
    """Validate explicit assumptions; evidence references do not prove a bound."""
    if not isinstance(record, dict) or set(record) != {"version", "semantics", "constraints"} or record["version"] != "1.0" or record["semantics"] != "ALLOWED_LABEL_UPPER_BOUND":
        raise ValueError("Expected version 1.0 ALLOWED_LABEL_UPPER_BOUND constraint record")
    entries = record["constraints"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("At least one mapping constraint is required")
    domains = {}
    evidence_ids = {e["evidence_id"] for e in evidence}
    pattern = r"T\d{4}" if level == "parent" else r"T\d{4}(?:\.\d{3})?"
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"occurrence_id", "allowed_techniques", "rationale", "evidence_ids"}:
            raise ValueError("Constraint fields must include occurrence, allowed techniques, rationale and evidence IDs")
        node = entry["occurrence_id"]
        if not isinstance(node, str) or node not in nodes or mappings[node] or node in domains:
            raise ValueError("Constraint occurrence must be unique, retained and unmapped in the selected profile")
        labels = entry["allowed_techniques"]
        if not isinstance(labels, list) or not labels or any(not isinstance(t, str) or not re.fullmatch(pattern, t) for t in labels) or len(labels) != len(set(labels)):
            raise ValueError("Allowed labels must be unique ATT&CK identifiers at the profile taxonomy level")
        if not isinstance(entry["rationale"], str) or not entry["rationale"].strip():
            raise ValueError("A constraint requires an explicit rationale")
        refs = entry["evidence_ids"]
        if not isinstance(refs, list) or not refs or any(not isinstance(e, str) for e in refs) or len(refs) != len(set(refs)) or not set(refs) <= evidence_ids:
            raise ValueError("A constraint requires valid, unique source-evidence references")
        domains[node] = set(labels)
    return domains


def record_context(key, case, profile, nodes, mappings, relations):
    return {"certificate_version": "1.0", "case_key": key, "case_id": case["case_id"],
            "case_record_sha256": digest(json.dumps(case, sort_keys=True, separators=(",", ":"))),
            "profile": profile, "source": case["source"], "interpretation_status": case["status"],
            "independently_validated": case["independently_validated"],
            "occurrences": [{**node, "active_mappings": sorted(mappings[nid])} for nid, node in nodes.items()],
            "relations": relations, "evidence": case["evidence"],
            "verification_scope": "Recomputation checks agreement with repository case records; source bytes require the separate source audit. No semantic validation or digital signature is implied."}


def certificate(key, case, profile_name, query, *, mapping_constraints=None):
    if case.get("query_assessment") == "UNASSESSED":
        raise ValueError("This case has no assessable three-action sequence")
    profile, nodes, mappings, relations = profile_graph(case, profile_name)
    domains = None if mapping_constraints is None else constraint_domains(mapping_constraints, nodes, mappings, case["evidence"], profile.get("taxonomy_level", "parent"))
    answer = investigate(mappings, relations, query, mapping_domains=domains)
    body = record_context(key, case, profile, nodes, mappings, relations)
    body["answer"] = answer
    if domains is not None:
        body.update({"certificate_version": "2.0", "mapping_constraints": mapping_constraints,
                     "unrestricted_answer": investigate(mappings, relations, query),
                     "constraint_validation": "Declared assumptions with checked references, not independently established exhaustive candidate sets. Identifier syntax does not validate taxonomy membership or semantic correctness.",
                     "verification_scope": "Recomputation checks current case records and the constraints embedded in this record. It does not authenticate the constraint author, prove the bounds, or establish semantic truth. Raw source bytes require a separate audit."})
    body["certificate_sha256"] = digest(json.dumps(body, sort_keys=True, separators=(",", ":")))
    return body


def verify_certificate(value):
    key = value["case_key"]
    expected = certificate(key, load_case(key), value["profile"]["name"], value["answer"]["query"], mapping_constraints=value.get("mapping_constraints"))
    if value != expected:
        raise ValueError("Certificate differs from recomputation against current case records")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=sorted(AVAILABLE_CASES), default="domain-controller")
    parser.add_argument("--profile")
    parser.add_argument("--query", nargs=3)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--mapping-constraints", type=Path, help="Explicit allowed-label bounds for unknown occurrences; export includes the unrestricted answer")
    args = parser.parse_args()
    if args.verify:
        if args.query or args.mapping_constraints or args.output:
            parser.error("--verify uses the exported record and cannot be combined with query, constraints or output")
        verify_certificate(json.loads(args.verify.read_text(encoding="utf-8")))
        print("PASS: certificate matches current case records; semantic correctness is not established by this check.")
        return
    if not args.query:
        parser.error("--query requires three technique identifiers")
    constraints = None
    if args.mapping_constraints:
        def unique_keys(pairs):
            value = {}
            for key, item in pairs:
                if key in value:
                    raise ValueError("Duplicate JSON key: " + key)
                value[key] = item
            return value
        constraints = json.loads(args.mapping_constraints.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
    case = load_case(args.case)
    if case.get("query_assessment") == "UNASSESSED":
        parser.error("This case has no assessable three-action sequence")
    profile_name = args.profile or ("extended_script_sequence" if args.case == "domain-controller"
                                    else case["profiles"][0]["name"])
    result = certificate(args.case, case, profile_name, args.query, mapping_constraints=constraints)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="")
    else:
        print(text)


if __name__ == "__main__":
    main()
