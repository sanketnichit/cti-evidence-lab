#!/usr/bin/env python3
"""Create v0.3 scope-assignment lock records after a selected-final partition is frozen."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "validator"))
from validate_comparison_scope_assignments import LOCK_HEADERS, build_scope_assignment_lock_rows  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Create comparison-scope assignment locks for SELECTED_FINAL partitions")
    parser.add_argument("--v2-extension", type=Path, required=True)
    parser.add_argument("--base-bundle", type=Path, default=PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.1")
    parser.add_argument("--assignment-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--locked-by", required=True)
    parser.add_argument("--lock-date", required=True, help="ISO date, YYYY-MM-DD")
    args = parser.parse_args()
    rows = build_scope_assignment_lock_rows(
        args.v2_extension / "registers" / "analysis_partition_selection.csv",
        args.assignment_file,
        locked_by=args.locked_by,
        lock_date=args.lock_date,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOCK_HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created {len(rows)} comparison-scope assignment lock row(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
