#!/usr/bin/env python3
"""Create v0.4 activity-stratum locks for selected-final report partitions."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "validator"))
from validate_activity_strata import (  # noqa: E402
    LOCK_HEADERS,
    build_activity_stratum_lock_rows,
    validate_activity_stratum_locks,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create RECON v0.4 activity-stratum locks")
    parser.add_argument("--selection-file", type=Path, required=True)
    parser.add_argument("--strata-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--locked-by", required=True)
    parser.add_argument("--lock-date", required=True)
    parser.add_argument("--lock-notes", default="")
    args = parser.parse_args()

    rows = build_activity_stratum_lock_rows(
        args.selection_file, args.strata_file,
        locked_by=args.locked_by, lock_date=args.lock_date,
        lock_notes=args.lock_notes,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOCK_HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    validation = validate_activity_stratum_locks(
        args.selection_file, args.strata_file, args.output
    )
    print(f"created {len(rows)} activity-stratum lock(s); valid={validation['ok']}")
    if not validation["ok"]:
        print(validation["errors"])
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
