"""Verify the fixed pilot's source bytes and evidence pointers without exporting text.

CRLF recovery is opt-in and accepted only when it reproduces the existing frame
hash exactly. Originals and the frame are never modified. This is an integrity
audit, not semantic annotation or a selected-final analysis adapter.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.source_text_integrity import decode_frozen_source, frozen_source_sha256

FRAME = ROOT / "research/annoctr_sampling/AnnoCTR_Fresh_MultiVendor_Sample_Frame_v1.0.csv"
DRAFT = ROOT / "research/annotation_drafts/AnnoCTR_Pilot_v0.1"


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def verified_text(raw, expected_hash, recover_crlf=False):
    text = decode_frozen_source(raw)
    original_hash = frozen_source_sha256(text)
    operation = "NONE"
    if original_hash != expected_hash:
        candidate = text.replace("\r\n", "\n")
        if not recover_crlf or frozen_source_sha256(candidate) != expected_hash:
            raise ValueError("Source hash mismatch; no unverified text may enter this audit")
        text = candidate
        operation = "CRLF_TO_LF_VERIFIED_AGAINST_FRAME"
    return text, {
        "raw_bytes_sha256": hashlib.sha256(raw).hexdigest(),
        "decoded_original_sha256": original_hash,
        "source_text_sha256": expected_hash,
        "transformation": operation,
        "source_text_char_count": len(text),
    }


def audit_anchor(text, row):
    start, end = int(row["char_start"]), int(row["char_end"])
    if not 0 <= start < end <= len(text):
        raise ValueError(f"Invalid offsets for {row['anchor_id']}")
    span = text[start:end]
    line = text.count("\n", 0, start) + 1
    if line != int(row["source_line_number"]):
        raise ValueError(f"Line mismatch for {row['anchor_id']}")
    # Count overlapping occurrences too; str.count would undercount them.
    occurrences = sum(text.startswith(span, i) for i in range(len(text) - len(span) + 1))
    if row["anchor_occurrences_in_source"] == "UNIQUE" and occurrences != 1:
        raise ValueError(f"Non-unique anchor {row['anchor_id']}")
    return {
        "anchor_id": row["anchor_id"], "char_start": start, "char_end": end,
        "source_line_number": line, "occurrences": occurrences,
        "span_sha256": frozen_source_sha256(span),
    }


def audit(corpus_root, *, recover_crlf=False, frame_path=FRAME, draft_path=DRAFT):
    frame = read_csv(frame_path)
    ids = [r["report_id"] for r in frame]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate report ID in frame")
    pilot = read_csv(draft_path / "report_assessment_draft.csv")
    fixed_ids = {r["report_id"] for r in frame if r["random_rank_within_vendor"] == "1"}
    if len(pilot) != 5 or {r["report_id"] for r in pilot} != fixed_ids:
        raise ValueError("Draft reports must match all five fixed rank-one candidates")
    anchors = read_csv(draft_path / "source_anchor_index_draft.csv")
    keys = [(r["report_id"], r["anchor_id"]) for r in anchors]
    if len(keys) != len(set(keys)) or any(rid not in fixed_ids for rid, _ in keys):
        raise ValueError("Duplicate or out-of-pilot anchor")
    pilot_by_id = {r["report_id"]: r for r in pilot}
    sources = []
    for row in frame:
        rid = row["report_id"]
        if Path(rid).name != rid or "/" in rid or "\\" in rid or rid in {".", ".."}:
            raise ValueError("Unsafe report ID")
        raw = (Path(corpus_root) / "text" / (rid + ".txt")).read_bytes()
        text, metadata = verified_text(raw, row["source_text_sha256"], recover_crlf)
        entry = {"report_id": rid, **metadata}
        if rid in fixed_ids:
            if pilot_by_id[rid]["source_text_sha256"] != row["source_text_sha256"]:
                raise ValueError(f"Pilot/frame hash disagreement: {rid}")
            report_anchors = [a for a in anchors if a["report_id"] == rid]
            if not report_anchors:
                raise ValueError(f"Missing pilot evidence pointers: {rid}")
            for a in report_anchors:
                if a["source_text_sha256"] != row["source_text_sha256"]:
                    raise ValueError(f"Anchor/frame hash disagreement: {rid}")
            entry["anchors"] = [audit_anchor(text, a) for a in report_anchors]
        sources.append(entry)
    inputs = [Path(frame_path), draft_path / "report_assessment_draft.csv",
              draft_path / "source_anchor_index_draft.csv"]
    return {
        "status": "SOURCE_INTEGRITY_ONLY_NOT_SEMANTIC_VALIDATION",
        "frame_reports_verified": len(sources),
        "fixed_pilot_reports_verified": len(fixed_ids),
        "anchors_verified": len(anchors),
        "crlf_recoveries": sum(s["transformation"] != "NONE" for s in sources),
        "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        "source_text_exported": False,
        "sources": sources,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-root", type=Path, required=True)
    parser.add_argument("--recover-crlf", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = audit(args.corpus_root, recover_crlf=args.recover_crlf)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Audit failed: {exc}\n")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(f"Verified {result['frame_reports_verified']} reports and {result['anchors_verified']} pilot anchors; no source text exported.")


if __name__ == "__main__":
    main()
