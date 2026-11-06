#!/usr/bin/env python3
"""Selected-final aggregation using the locked RECON v0.3 comparison-scope register."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Mapping

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[2]
V1_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.1"
V2_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.2"
sys.path.insert(0, str(V1_ROOT / "analysis"))
sys.path.insert(0, str(V1_ROOT / "validator"))
sys.path.insert(0, str(V2_ROOT / "analysis"))
sys.path.insert(0, str(PACKAGE_ROOT / "validator"))
sys.path.insert(0, str(REPO_ROOT))

import report_level_aggregation as v2_aggregation  # noqa: E402
from validate_comparison_scope_assignments import (  # noqa: E402
    ASSIGNMENT_HEADERS,
    validate_assignment_register,
    validate_scope_assignment_locks,
)
from src.source_text_integrity import read_frozen_source  # noqa: E402

EXPLICIT_RULE_ID = v2_aggregation.EXPLICIT_SCOPE_PAIR_RULE_ID


def _read_assignments(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ASSIGNMENT_HEADERS:
            raise ValueError("comparison-scope assignment register header mismatch")
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
            if row and any((value or "").strip() for value in row.values())
        ]


def aggregate_with_explicit_scope_assignments(
    v2_extension_root: str | Path,
    v3_extension_root: str | Path,
    *,
    source_texts: Mapping[str, str],
    confirm_selected_analysis_locks: bool = False,
    confirm_comparison_scope_assignment_locks: bool = False,
    approve_scope_pair_rule: bool = False,
) -> dict:
    v2_root = Path(v2_extension_root)
    v3_root = Path(v3_extension_root)
    assignment_file = v3_root / "registers" / "event_comparison_scope_assignments.csv"
    lock_file = v3_root / "registers" / "comparison_scope_assignment_locks.csv"

    assignment_validation = validate_assignment_register(V1_ROOT, assignment_file, source_texts=dict(source_texts))
    lock_validation = validate_scope_assignment_locks(v2_root, assignment_file, lock_file, V1_ROOT, source_texts=dict(source_texts))
    if not assignment_validation["ok"] or not lock_validation["ok"]:
        return {
            "status": "BLOCKED_SCOPE_ASSIGNMENT_VALIDATION",
            "schema": "CTI_Annotation_Schema_RECON_v0.3_draft",
            "assignment_validation": assignment_validation,
            "lock_validation": lock_validation,
            "report_level_primary_rates": {
                "compatible_event_pair_opportunity_rate": None,
                "same_technique_pair_opportunity_rate": None,
                "within_technique_temporal_relation_report_rate": None,
            },
        }
    if not confirm_comparison_scope_assignment_locks:
        return {
            "status": "BLOCKED_EXPLICIT_SCOPE_ASSIGNMENT_LOCK_CONFIRMATION_REQUIRED",
            "schema": "CTI_Annotation_Schema_RECON_v0.3_draft",
            "assignment_validation": assignment_validation,
            "lock_validation": lock_validation,
        }

    assignments = _read_assignments(assignment_file)
    result = v2_aggregation.aggregate_selected_report_projections(
        v2_root,
        source_texts=source_texts,
        confirm_selected_analysis_locks=confirm_selected_analysis_locks,
        approve_scope_pair_rule=approve_scope_pair_rule,
        comparison_scope_assignments=assignments,
        scope_pair_rule_id=EXPLICIT_RULE_ID,
    )
    result["schema"] = "CTI_Annotation_Schema_RECON_v0.3_draft"
    result["comparison_scope_assignment_validation"] = assignment_validation
    result["comparison_scope_assignment_lock_validation"] = lock_validation
    result["comparison_scope_assignment_lock_confirmation_supplied"] = True
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate selected-final reports using explicit event comparison-scope assignments")
    parser.add_argument("--v2-extension", type=Path, default=V2_ROOT)
    parser.add_argument("--v3-extension", type=Path, default=PACKAGE_ROOT)
    parser.add_argument("--sources-dir", type=Path, required=True)
    parser.add_argument("--confirm-selected-analysis-locks", action="store_true")
    parser.add_argument("--confirm-comparison-scope-assignment-locks", action="store_true")
    parser.add_argument("--approve-scope-pair-rule", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    sources = {
        path.stem: read_frozen_source(path)
        for path in sorted(args.sources_dir.glob("*.txt"))
    }
    result = aggregate_with_explicit_scope_assignments(
        args.v2_extension, args.v3_extension,
        source_texts=sources,
        confirm_selected_analysis_locks=args.confirm_selected_analysis_locks,
        confirm_comparison_scope_assignment_locks=args.confirm_comparison_scope_assignment_locks,
        approve_scope_pair_rule=args.approve_scope_pair_rule,
    )
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
