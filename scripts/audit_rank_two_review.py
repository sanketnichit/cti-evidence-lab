"""Audit the fixed source extension without turning unresolved reviews into negatives."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_pilot_sources import FRAME, read_csv, verified_text

DIRECTORY = ROOT / "research/feasibility/rank_two_extension_v0.1"
SEED = "CTI-EVIDENCE-LAB-ANNOCTR-PILOT-2026-11-03-v1"


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode("utf-8")).hexdigest()


def record_hash(value):
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":")))


def validate(selection, review):
    if selection["rank"] != 2 or selection["seed"] != SEED:
        raise ValueError("Selection rank or seed changed")
    if selection["frame_path"] != FRAME.relative_to(ROOT).as_posix() or selection["frame_sha256"] != digest(FRAME.read_bytes()):
        raise ValueError("Selection frame changed")
    frame = read_csv(FRAME)
    for donor in {r["donor"] for r in frame}:
        rows = sorted((r for r in frame if r["donor"] == donor), key=lambda r: r["random_priority_sha256"])
        for rank, row in enumerate(rows, 1):
            if row["random_priority_sha256"] != digest(SEED + "|" + row["report_id"]) or int(row["random_rank_within_vendor"]) != rank:
                raise ValueError("Frame priority or rank does not reproduce")
    expected = {r["report_id"]: r for r in frame if r["random_rank_within_vendor"] == "2"}
    selected = {r["report_id"]: r for r in selection["reports"]}
    if len(selected) != len(selection["reports"]) or set(selected) != set(expected):
        raise ValueError("Selection must retain exactly all five rank-two reports")
    for rid, row in selected.items():
        if any(expected[rid].get(k) != v for k, v in row.items()):
            raise ValueError("Selected metadata disagrees with frame")
    if review["status"] != "EXPLORATORY_TEXT_REVIEW" or review["independently_validated"] is not False:
        raise ValueError("This review is not independent validation")
    reports = {r["report_id"]: r for r in review["reports"]}
    if len(reports) != len(review["reports"]) or set(reports) != set(selected):
        raise ValueError("Review must retain every selected report exactly once")
    for rid, row in reports.items():
        if row["source_text_sha256"] != selected[rid]["source_text_sha256"]:
            raise ValueError("Review source hash differs from selection")
        if row["full_corpus_text_read"] is not True or row["query_errors"] is not None or row["primary_sequence_status"] != "NOT_ESTABLISHED":
            raise ValueError("This version records complete readings with unassessed sequence errors")
        spans = {e["evidence_id"]: e for e in row["evidence"]}
        if not spans or len(spans) != len(row["evidence"]):
            raise ValueError("Empty or duplicate evidence identity")
        for e in spans.values():
            if any(type(e[k]) is not int for k in ("char_start", "char_end", "line_start", "line_end")) or not 0 <= e["char_start"] < e["char_end"] or not 1 <= e["line_start"] <= e["line_end"]:
                raise ValueError("Invalid evidence coordinates")
        for claim in (row["strongest_candidate"], row["counterinterpretation"]):
            if not claim["evidence_ids"] or not set(claim["evidence_ids"]) <= spans.keys() or not claim["assessment"].strip():
                raise ValueError("Unsupported assessment reference")
        if not row["remaining_resolution"].strip() or not row["primary_blocker"].strip():
            raise ValueError("Missing unresolved decision")
    return reports


def summarize(selection, review):
    reports = validate(selection, review)
    return {
        "status": "EXPLORATORY_REVIEW_NOT_GOLD_VALIDATION",
        "selection_sha256": record_hash(selection), "review_sha256": record_hash(review),
        "selected_reports": len(selection["reports"]), "reviewed_reports": len(reports),
        "primary_sequences_established": 0, "query_error_count": None,
        "evidence_bindings": sum(len(r["evidence"]) for r in reports.values()),
        "primary_blockers": dict(sorted(Counter(r["primary_blocker"] for r in reports.values()).items())),
        "interpretation": "No qualifying three-occurrence intrusion sequence established in this text-only pass; not evidence of absence or a prevalence estimate.",
    }


def verify_spans(text, spans):
    verified = []
    for e in spans:
        start, end = e["char_start"], e["char_end"]
        if not 0 <= start < end <= len(text) or digest(text[start:end]) != e["span_sha256"]:
            raise ValueError("Source span hash or bounds mismatch")
        if text.count("\n", 0, start) + 1 != e["line_start"] or text.count("\n", 0, end - 1) + 1 != e["line_end"]:
            raise ValueError("Source line mismatch")
        verified.append(e["evidence_id"])
    return verified


def audit(corpus_root, selection, review, *, recover_crlf=False):
    reports = validate(selection, review)
    sources = []
    for rid, row in reports.items():
        text, metadata = verified_text((Path(corpus_root) / "text" / (rid + ".txt")).read_bytes(), row["source_text_sha256"], recover_crlf)
        sources.append({"report_id": rid, **metadata, "verified_evidence": verify_spans(text, row["evidence"])})
    return {"status": "SOURCE_BINDINGS_VERIFIED_NOT_SEMANTIC_VALIDATION",
            "selection_sha256": record_hash(selection), "review_sha256": record_hash(review),
            "source_text_exported": False, "sources": sources}


def validate_recorded_audit(selection, review, recorded):
    reports = validate(selection, review)
    if recorded["selection_sha256"] != record_hash(selection) or recorded["review_sha256"] != record_hash(review):
        raise ValueError("Recorded audit belongs to different selection or review")
    sources = {s["report_id"]: s for s in recorded["sources"]}
    if len(sources) != len(recorded["sources"]) or set(sources) != set(reports):
        raise ValueError("Recorded audit does not cover every selected report")
    for rid, row in reports.items():
        source = sources[rid]
        if source["source_text_sha256"] != row["source_text_sha256"] or source["verified_evidence"] != [e["evidence_id"] for e in row["evidence"]]:
            raise ValueError("Recorded audit source or binding list changed")
    return recorded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-root", type=Path)
    parser.add_argument("--recover-crlf", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    selection = json.loads((DIRECTORY / "selection.json").read_text(encoding="utf-8"))
    review = json.loads((DIRECTORY / "review.json").read_text(encoding="utf-8"))
    result = audit(args.corpus_root, selection, review, recover_crlf=args.recover_crlf) if args.corpus_root else summarize(selection, review)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="")
    else:
        print(text)


if __name__ == "__main__":
    main()
