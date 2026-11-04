"""Recompute/verify AnnoCTR source-text hashes in the canonical 120-report frame.

This script prints report IDs and mismatch counts only; it never prints report
text. It preserves CRLF/LF through strict decoding and uses the shared UTF-8
BOM/no-normalization/code-point convention in src/source_text_integrity.py.
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.source_text_integrity import frozen_source_metadata  # noqa: E402

FRAME_DEFAULT = ROOT / "research/annoctr_sampling/AnnoCTR_Fresh_MultiVendor_Sample_Frame_v0.9.csv"


def update_frame(frame_path: Path, corpus_root: Path, *, write: bool = False) -> tuple[int, list[str]]:
    with frame_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "report_id" not in reader.fieldnames or "source_text_sha256" not in reader.fieldnames:
            raise ValueError("Frame must contain report_id and source_text_sha256 columns")
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    mismatches: list[str] = []
    checked = 0
    for row in rows:
        report_id = (row.get("report_id") or "").strip()
        if not report_id:
            raise ValueError("Frame contains a blank report_id")
        source_path = corpus_root / "text" / f"{report_id}.txt"
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing source text for {report_id}: {source_path}")
        metadata = frozen_source_metadata(source_path)
        checked += 1
        if (row.get("source_text_sha256") or "").strip().lower() != metadata["source_text_sha256"]:
            mismatches.append(report_id)
        if write:
            row["source_text_sha256"] = str(metadata["source_text_sha256"])

    if write and mismatches:
        fd, temporary_name = tempfile.mkstemp(prefix=frame_path.name + ".", suffix=".tmp", dir=frame_path.parent)
        os.close(fd)
        temporary = Path(temporary_name)
        try:
            with temporary.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
            temporary.replace(frame_path)
        finally:
            temporary.unlink(missing_ok=True)
    return checked, mismatches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-root", required=True, type=Path, help="AnnoCTR/all directory containing text/")
    parser.add_argument("--frame", type=Path, default=FRAME_DEFAULT)
    parser.add_argument("--write", action="store_true", help="Replace frame source_text_sha256 values with canonical hashes")
    args = parser.parse_args()
    checked, mismatches = update_frame(args.frame, args.corpus_root, write=args.write)
    print(f"Reports checked: {checked}")
    print(f"Hash mismatches: {len(mismatches)}")
    if mismatches:
        print("Affected report IDs: " + ", ".join(mismatches))
        if not args.write:
            print("No files changed. Re-run with --write only after reviewing the convention change.")
    return 1 if mismatches and not args.write else 0


if __name__ == "__main__":
    raise SystemExit(main())
