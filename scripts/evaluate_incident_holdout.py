"""Recompute the fixed chronological holdout and optionally verify source bytes."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_rdp_case import digest, verify
from src.occurrence_queries import validate
from src.sequence_investigation import investigate

DIRECTORY = ROOT / "research/experiments/incident_holdout_v0.1"
FRAME = ROOT / "research/case_studies/dfir_html_smuggling_v0.1/selection.json"
TAXONOMY_SHA256 = "e84679af4bc46bba2ba92f60182101f146d5b966898e47924de7321e6bffeaa1"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def by_id(items, field):
    indexed = {item[field]: item for item in items}
    if len(indexed) != len(items):
        raise ValueError(f"Duplicate {field}")
    return indexed


def summarize(case, post):
    if case["post_id"] != post["id"] or case["source"]["url"] != post["link"]:
        raise ValueError("Case does not match the declared selection")
    if case["independently_validated"] is not False or case["taxonomy"]["sha256"] != TAXONOMY_SHA256:
        raise ValueError("Unexpected interpretation status or taxonomy")
    evidence = by_id(case["evidence"], "evidence_id")
    nodes = by_id(case["occurrences"], "event_id")
    relations = list(by_id(case["relations"], "relation_id").values())
    first, last = case["source"]["summary_paragraph_range"]
    for span in evidence.values():
        if not 0 <= span["char_start"] < span["char_end"] or not re.fullmatch("[0-9a-f]{64}", span["span_sha256"]):
            raise ValueError("Invalid evidence locator")
    for claim in [*nodes.values(), *relations, *case["exclusions"]]:
        refs = claim["evidence_ids"]
        if not refs or not set(refs) <= evidence.keys():
            raise ValueError("Claim has missing source evidence")
    for claim in [*nodes.values(), *relations]:
        if not any(first <= evidence[ref]["paragraph_number"] <= last for ref in claim["evidence_ids"]):
            raise ValueError("Primary action or relation lacks Case Summary evidence")
    if any(not r["ordering_rationale"].strip() for r in relations):
        raise ValueError("Missing ordering rationale")
    for node in nodes.values():
        if node["outcome"] not in {"REPORTED", "SUCCEEDED", "ATTEMPTED"} or not node["mapping_rationale"].strip():
            raise ValueError("Missing outcome or mapping rationale")
        label = node["mapping"]
        if label is not None and (not re.fullmatch(r"T[0-9]{4}", label) or label not in case["taxonomy"]["parent_definitions"]):
            raise ValueError("Mapping absent from the recorded parent definitions")
    recorded = case["recorded_source_audit"]
    for field in ("paragraph_text_sha256", "raw_html_sha256"):
        if recorded[field] != case["source"][field]:
            raise ValueError("Recorded source audit does not match the case")
    if recorded["evidence_verified"] != list(evidence):
        raise ValueError("Recorded source audit did not cover every locator")

    mappings = {key: {node["mapping"]} if node["mapping"] else set() for key, node in nodes.items()}
    return {"post_id": post["id"], "evidence_locators": len(evidence),
            **compare_graph(mappings, relations)}


def compare_graph(mappings, relations, *, explain_unresolved=False):
    """Compare label triples on one retained incident graph."""
    edges = {(row["source_event"], row["target_event"]) for row in relations}
    if any(row["relation"] != "BEFORE" for row in relations):
        raise ValueError("Holdout comparisons require explicit BEFORE edges")
    validate(mappings, edges)
    vocabulary = sorted(set().union(*mappings.values()))
    # An unknown-only path has no case-derived query vocabulary.
    coverage = {
        "actions": len(mappings), "relations": len(relations),
        "unknown_mappings": sum(not labels for labels in mappings.values()),
        "vocabulary": vocabulary,
    }
    if not vocabulary or not {u for u, _ in edges} & {v for _, v in edges}:
        return {**coverage, "query_assessment": "UNASSESSED", "query_errors": None}
    statuses = Counter()
    counts = {view: Counter({"returned": 0, "unsupported": 0, "unresolved": 0, "missed_supported": 0})
              for view in ("distinct_pairs", "loop_pairs", "distinct_endpoint_join", "loop_endpoint_join")}
    supported_witnesses = []
    unsupported_projected = []
    unresolved_projected = []
    for query in product(vocabulary, repeat=3):
        answer = investigate(mappings, relations, query)
        status = answer["status"]
        statuses[status] += 1
        if status == "SUPPORTED":
            supported_witnesses.append({"query": query, "witnesses": answer["known_witnesses"]})
        for prefix in ("distinct", "loop"):
            comparison = answer["projection_comparisons"][f"{prefix}_pairs"]
            for view, field in ((f"{prefix}_pairs", "returned"), (f"{prefix}_endpoint_join", "endpoint_join_returned")):
                returned = comparison[field]
                counts[view]["returned"] += returned
                counts[view]["unsupported"] += returned and status == "NOT_SUPPORTED"
                counts[view]["unresolved"] += returned and status == "UNRESOLVED_MAPPING"
                counts[view]["missed_supported"] += not returned and status == "SUPPORTED"
                if returned and status == "NOT_SUPPORTED":
                    unsupported_projected.append({"query": query, "view": view,
                                                  "joins": comparison["incompatible_joins"]})
                if explain_unresolved and returned and status == "UNRESOLVED_MAPPING":
                    unresolved_projected.append({
                        "query": query, "view": view, "joins": comparison["incompatible_joins"],
                        "unresolved_witnesses": answer["unresolved_witnesses"],
                    })
    return {
        **coverage, "query_assessment": "CONDITIONAL_ON_RECORDED_GRAPH",
        "query_count": len(vocabulary) ** 3,
        "statuses": dict(sorted(statuses.items())), "representations": counts,
        "supported_witnesses": supported_witnesses, "unsupported_projected": unsupported_projected,
        **({"unresolved_projected": unresolved_projected} if explain_unresolved else {}),
    }


def run(source_directory=None):
    frame = read_json(FRAME)
    ordered = sorted(frame["returned_posts"], key=lambda row: (row["date"], row["id"]))
    index = next(i for i, row in enumerate(ordered) if row["id"] == frame["selected_post_id"])
    posts = ordered[index + 1:index + 3]
    if [row["id"] for row in posts] != [21520, 22587]:
        raise ValueError("Saved metadata no longer matches the declared holdout")
    results = []
    for post in posts:
        case = read_json(DIRECTORY / f"{post['id']}.json")
        result = summarize(case, post)
        if post["id"] == 22587:
            alternatives = {}
            for edge in ("B12", "B21"):
                retained = [row for row in case["relations"] if row["relation_id"] != edge]
                alternative = summarize({**case, "relations": retained}, post)
                alternatives[f"omit_{edge}"] = {
                    "statuses": alternative["statuses"], "representations": alternative["representations"],
                }
            result["post_review_edge_sensitivity"] = alternatives
        if source_directory is not None:
            verify((source_directory / f"{post['id']}.html").read_bytes(), case)
        results.append(result)
    return {"selected_reports": len(posts), "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.source_directory)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8", newline="")
    else:
        if json.loads(serialized) != read_json(DIRECTORY / "results.json"):
            raise SystemExit("Holdout results do not match recomputation")
        print(f"Reproduced {result['selected_reports']} holdout reports. "
              f"Source mode: {'local source rechecked' if args.source_directory else 'recorded audit only'}.")


if __name__ == "__main__":
    main()
