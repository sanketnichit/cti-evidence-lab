"""Bind exploratory judgments to a successful source audit; never create gold labels."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "research/feasibility/exploratory_review_v0.1"


def summarize(decisions, audit):
    if decisions["status"] != "EXPLORATORY_NOT_INDEPENDENTLY_VALIDATED":
        raise ValueError("This summary accepts exploratory review only")
    if audit["status"] != "SOURCE_INTEGRITY_ONLY_NOT_SEMANTIC_VALIDATION":
        raise ValueError("Expected a source-integrity audit")
    sources = {r["report_id"]: r for r in audit["sources"] if "anchors" in r}
    reports = decisions["reports"]
    if len(reports) != len(sources) or {r["report_id"] for r in reports} != set(sources):
        raise ValueError("Review must cover the exact audited pilot, without duplicates")
    for row in reports:
        source = sources[row["report_id"]]
        if source["source_text_sha256"] != row["source_text_sha256"]:
            raise ValueError("Review/source hash mismatch")
        anchors = {a["anchor_id"] for a in source["anchors"]}
        if not row["anchors"] or not set(row["anchors"]) <= anchors:
            raise ValueError("Review cites unknown evidence anchors")
        if row["qualifying_pair"] != "NOT_ESTABLISHED":
            raise ValueError("Positive findings require a versioned annotation analysis, not this summary")
        if type(row["candidate_attack_occurrences"]) is not int or row["candidate_attack_occurrences"] < 0:
            raise ValueError("Candidate occurrence count must be a nonnegative integer")
    return {
        "status": decisions["status"],
        "reviewed_text_reports": len(reports),
        "source_verified_anchors": sum(len(r["anchors"]) for r in sources.values()),
        "candidate_attack_occurrences": sum(r["candidate_attack_occurrences"] for r in reports),
        "reports_with_qualifying_pair_not_established": len(reports),
        "formal_annotation_partitions_created": 0,
        "empirical_prevalence": None,
        "inter_annotator_agreement": None,
        "interpretation": "No qualifying pair established in this exploratory reading. This is not a measured 0/5 prevalence or a completed human annotation study.",
        "reports": reports,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=DEFAULT)
    args = parser.parse_args()
    paths = [args.directory / name for name in ("review_decisions.json", "source_integrity.json")]
    result = summarize(*(json.loads(p.read_text(encoding="utf-8")) for p in paths))
    result["input_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    (args.directory / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(result["interpretation"])


if __name__ == "__main__":
    main()
