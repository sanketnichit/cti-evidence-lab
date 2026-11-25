"""Measure the effect of frozen discovery-role bounds on three incident graphs."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from itertools import product
from pathlib import Path

from scripts.evaluate_incident_holdout import TAXONOMY_SHA256, read_json
from scripts.investigate_sequence import AVAILABLE_CASES, ROOT, constraint_domains, digest, load_case, profile_graph
from src.sequence_investigation import investigate

DIRECTORY = ROOT / "research/experiments/bounded_mapping_v0.1"
DESIGN = DIRECTORY / "discovery_design.json"
RESULTS = DIRECTORY / "discovery_results.json"
STATUSES = ("NOT_SUPPORTED", "UNRESOLVED_MAPPING", "SUPPORTED")
VIEWS = ("distinct_pairs", "loop_pairs")


def json_digest(record):
    return digest(json.dumps(record, sort_keys=True, separators=(",", ":")))


def taxonomy_sets(design, taxonomy_path):
    if design["taxonomy"]["sha256"] != TAXONOMY_SHA256:
        raise ValueError("Unexpected pinned taxonomy")
    stored = design["taxonomy"]["parent_techniques"]
    tactics = ("discovery", "execution")
    if set(stored) != set(tactics) or any(
        not labels or labels != sorted(set(labels)) or any(not re.fullmatch(r"T[0-9]{4}", label) for label in labels)
        for labels in stored.values()
    ):
        raise ValueError("Invalid frozen taxonomy lists")
    groups = {tactic: set(stored[tactic]) for tactic in tactics}
    if taxonomy_path is not None:
        raw = taxonomy_path.read_bytes()
        if digest(raw) != TAXONOMY_SHA256:
            raise ValueError("Taxonomy bytes differ from the pinned release")
        observed = {tactic: set() for tactic in tactics}
        for obj in json.loads(raw)["objects"]:
            if obj["type"] != "attack-pattern" or any(obj.get(flag) for flag in (
                "x_mitre_is_subtechnique", "revoked", "x_mitre_deprecated"
            )):
                continue
            phases = {p["phase_name"] for p in obj.get("kill_chain_phases", ())
                      if p["kill_chain_name"] == "mitre-attack"}
            for tactic in phases & observed.keys():
                observed[tactic].update(ref["external_id"] for ref in obj["external_references"]
                                        if ref["source_name"] == "mitre-attack")
        if observed != groups:
            raise ValueError("Frozen parent lists differ from pinned tactic membership")
    return groups


def evaluate_case(key, scoped_occurrences, groups):
    case = load_case(key)
    if case["query_assessment"] == "UNASSESSED":
        raise ValueError("Frozen comparison requires a case with an assessable sequence")
    profile, nodes, mappings, relations = profile_graph(case, "recorded_parent_profile")
    for item in scoped_occurrences:
        occurrence = nodes[item["occurrence_id"]]
        if not set(item["evidence_ids"]) <= set(occurrence["evidence_ids"]):
            raise ValueError("A role bound must cite evidence for the affected occurrence")
    conditions = {
        "open": None,
        "discovery_or_execution": groups["discovery"] | groups["execution"],
        "discovery_only": groups["discovery"],
    }
    domains = {"open": None}
    for condition, labels in conditions.items():
        if labels is None:
            continue
        constraint = {"version": "1.0", "semantics": "ALLOWED_LABEL_UPPER_BOUND",
                      "constraints": [{**item, "allowed_techniques": sorted(labels)}
                                      for item in scoped_occurrences]}
        domains[condition] = constraint_domains(constraint, nodes, mappings, case["evidence"],
                                                profile["taxonomy_level"])
    narrower = domains["discovery_only"]
    omissions = {omitted: {node: labels for node, labels in narrower.items() if node != omitted} or None
                 for omitted in narrower}
    restored = Counter({node: 0 for node in omissions})
    status_counts = {condition: Counter(dict.fromkeys(STATUSES, 0)) for condition in conditions}
    projected_cases = []
    vocabulary = sorted(set().union(*mappings.values()))
    for query in product(vocabulary, repeat=3):
        answers = {name: investigate(mappings, relations, query, mapping_domains=bounds, summary_only=True)
                   for name, bounds in domains.items()}
        open_answer = answers["open"]
        statuses = {name: answer["status"] for name, answer in answers.items()}
        ranking = [STATUSES.index(status) for status in statuses.values()]
        if ranking != sorted(ranking, reverse=True):
            raise AssertionError(f"Nested bounds became more permissive for {key} {query}")
        for name, answer in answers.items():
            if answer["known_witness_count"] != open_answer["known_witness_count"]:
                raise AssertionError(f"A mapping bound changed a known witness for {key} {query}")
            status_counts[name][answer["status"]] += 1
        if statuses["open"] != "UNRESOLVED_MAPPING":
            continue
        projected_views = [view for view in VIEWS if open_answer["projection_comparisons"][view]["returned"]]
        if projected_views:
            projected_cases.append({"query": list(query), "views": projected_views, "statuses": statuses})
        if statuses["discovery_only"] == "NOT_SUPPORTED":
            for node, relaxed in omissions.items():
                result = investigate(mappings, relations, query, mapping_domains=relaxed, summary_only=True)
                restored[node] += result["status"] == "UNRESOLVED_MAPPING"
    return {
        "source_case_sha256": json_digest(read_json(AVAILABLE_CASES[key])),
        "vocabulary": vocabulary,
        "query_count": len(vocabulary) ** 3,
        "withheld_occurrences": sum(not labels for labels in mappings.values()),
        "bounded_occurrences": sorted(narrower),
        "allowed_labels_in_query_vocabulary": {
            name: sorted(set(vocabulary) & labels) for name, labels in conditions.items() if labels is not None
        },
        "statuses": status_counts,
        "open_unresolved_becoming_unsupported": {
            name: status_counts["open"]["UNRESOLVED_MAPPING"] - status_counts[name]["UNRESOLVED_MAPPING"]
            for name in conditions if name != "open"
        },
        "unresolved_restored_when_one_discovery_bound_removed": dict(sorted(restored.items())),
        "originally_projected_unresolved": projected_cases,
    }


def run(taxonomy_path=None):
    design = read_json(DESIGN)
    groups = taxonomy_sets(design, taxonomy_path)
    return {
        "design_sha256": json_digest(design),
        "allowed_parent_labels": {"discovery_only": len(groups["discovery"]),
                                  "discovery_or_execution": len(groups["discovery"] | groups["execution"])},
        "cases": {key: evaluate_case(key, scoped, groups) for key, scoped in design["cases"].items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--taxonomy", type=Path, help="Verify the frozen tactic lists against the pinned release")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.taxonomy)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    else:
        if result != read_json(RESULTS):
            raise SystemExit("Discovery bounds differ from the published results")
        print(f"Reproduced discovery bounds on {len(result['cases'])} recorded cases.")


if __name__ == "__main__":
    main()
