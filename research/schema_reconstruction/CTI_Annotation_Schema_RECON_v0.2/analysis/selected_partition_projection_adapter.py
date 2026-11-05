"""Projection adapter gated by the v0.2 selected-final partition register.

This versioned adapter leaves the RECON v0.1 adapter unchanged. It validates
v0.2 temporal evidence, resolves exactly one SELECTED_FINAL partition, checks
a lock covering the v0.1 partition lock plus v0.2 evidence/selection metadata,
and only then delegates projection to the v0.1 adapter.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
BASE_PACKAGE_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.1"
sys.path.insert(0, str(BASE_PACKAGE_ROOT / "analysis"))
sys.path.insert(0, str(BASE_PACKAGE_ROOT / "validator"))
sys.path.insert(0, str(PACKAGE_ROOT / "validator"))

from annotation_projection_adapter import (  # noqa: E402
    AdapterError,
    build_projection_for_partition,
    compute_annotation_lock_reference,
)
from validate_temporal_evidence import (  # noqa: E402
    HEADERS as TEMPORAL_EVIDENCE_HEADERS,
    SELECTION_HEADERS,
    validate_analysis_partition_selection,
    validate_bundle as validate_temporal_evidence_bundle,
)


class SelectedPartitionAdapterError(AdapterError):
    """Raised when no uniquely selected, locked v0.2 partition is safe to project."""


def _read_csv(path: Path, expected_headers: list[str]) -> list[dict[str, str]]:
    if not path.is_file():
        raise SelectedPartitionAdapterError(f"Required v0.2 register is missing: {path}")
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != expected_headers:
                raise SelectedPartitionAdapterError(
                    f"Header mismatch in {path.name}; expected {expected_headers}"
                )
            rows = []
            for line, row in enumerate(reader, 2):
                if row is None or all((value or "").strip() == "" for value in row.values()):
                    continue
                if None in row:
                    raise SelectedPartitionAdapterError(
                        f"Row-width mismatch in {path.name}:{line}"
                    )
                rows.append({key: (value or "").strip() for key, value in row.items()})
            return rows
    except (OSError, csv.Error, UnicodeError) as exc:
        raise SelectedPartitionAdapterError(f"Cannot read {path.name}: {exc}") from exc


def _selected_final_row(selection_rows: list[dict[str, str]], report_id: str) -> dict[str, str]:
    selected = [
        row for row in selection_rows
        if row.get("report_id") == report_id
        and row.get("selection_status") == "SELECTED_FINAL"
    ]
    if len(selected) != 1:
        raise SelectedPartitionAdapterError(
            f"Expected exactly one SELECTED_FINAL partition for report {report_id!r}; found {len(selected)}"
        )
    return selected[0]


def _partition_from_selection(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("report_id", ""),
        row.get("annotator_id", ""),
        row.get("annotation_pass_id", ""),
    )


def compute_analysis_lock_reference(
    bundle_root: str | Path,
    *,
    report_id: str,
    source_text: str,
) -> str:
    """Compute a v0.2 lock for the selected partition and its full evidence trail.

    The digest layers the existing v0.1 source/register lock with every v0.2
    temporal-evidence row for that partition and the selected-final decision.
    The selection row's lock_reference is excluded to avoid self-reference.
    """
    if not report_id:
        raise SelectedPartitionAdapterError("report_id is required")
    root = Path(bundle_root)
    selection_path = root / "registers" / "analysis_partition_selection.csv"
    evidence_path = root / "registers" / "temporal_relation_evidence.csv"
    selection_rows = _read_csv(selection_path, SELECTION_HEADERS)
    evidence_rows = _read_csv(evidence_path, TEMPORAL_EVIDENCE_HEADERS)
    selected = _selected_final_row(selection_rows, report_id)
    partition = _partition_from_selection(selected)
    if not all(partition):
        raise SelectedPartitionAdapterError("Selected partition is missing report/annotator/pass identity")

    base_root = root.parent / "CTI_Annotation_Schema_RECON_v0.1"
    base_lock = compute_annotation_lock_reference(
        base_root,
        report_id=partition[0],
        annotator_id=partition[1],
        annotation_pass_id=partition[2],
        source_text=source_text,
    )
    partition_evidence = [
        row for row in evidence_rows
        if (
            row.get("report_id"), row.get("annotator_id"), row.get("annotation_pass_id")
        ) == partition
    ]
    selection_decision = {
        key: value for key, value in selected.items() if key != "lock_reference"
    }
    payload = {
        "lock_format": "CTI-EVIDENCE-LAB-SELECTED-ANALYSIS-LOCK-v2",
        "partition": {
            "report_id": partition[0],
            "annotator_id": partition[1],
            "annotation_pass_id": partition[2],
        },
        "base_annotation_lock_reference": base_lock,
        "temporal_evidence_register_headers": TEMPORAL_EVIDENCE_HEADERS,
        "temporal_relation_evidence": partition_evidence,
        "analysis_partition_selection": selection_decision,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_projection_for_selected_report(
    bundle_root: str | Path,
    *,
    report_id: str,
    source_text: str,
    analysis_lock_confirmed: bool = False,
    analysis_lock_reference: str = "",
) -> dict[str, Any]:
    """Project only the report's one validated, locked SELECTED_FINAL partition.

    The caller cannot supply annotator/pass IDs. Those are resolved from the
    register, preventing callers from accidentally projecting a development,
    repeat, or otherwise unselected partition.
    """
    if not report_id:
        raise SelectedPartitionAdapterError("report_id is required")
    if analysis_lock_confirmed is not True or not analysis_lock_reference.strip():
        raise SelectedPartitionAdapterError(
            "Explicit selected-analysis-lock confirmation and a non-empty lock reference are required"
        )

    root = Path(bundle_root)
    base_root = root.parent / "CTI_Annotation_Schema_RECON_v0.1"
    selection_path = root / "registers" / "analysis_partition_selection.csv"
    evidence_path = root / "registers" / "temporal_relation_evidence.csv"

    selection_rows = _read_csv(selection_path, SELECTION_HEADERS)
    evidence_rows = _read_csv(evidence_path, TEMPORAL_EVIDENCE_HEADERS)
    selection_errors, _ = validate_analysis_partition_selection(base_root, selection_path)
    if selection_errors:
        details = "; ".join(
            f"{item['code']}:{item['message']}" for item in selection_errors[:12]
        )
        raise SelectedPartitionAdapterError(
            f"Analysis partition selection validation failed ({len(selection_errors)} errors): {details}"
        )

    selected = _selected_final_row(selection_rows, report_id)
    partition = _partition_from_selection(selected)

    temporal_validation = validate_temporal_evidence_bundle(
        base_root, evidence_path, selection_path
    )
    if not temporal_validation["ok"]:
        details = "; ".join(
            f"{item['code']}:{item['message']}"
            for item in temporal_validation["errors"][:12]
        )
        raise SelectedPartitionAdapterError(
            f"v0.2 temporal evidence validation failed ({temporal_validation['error_count']} errors): {details}"
        )

    expected_lock = compute_analysis_lock_reference(
        root, report_id=report_id, source_text=source_text
    )
    if selected.get("lock_reference") != expected_lock:
        raise SelectedPartitionAdapterError(
            "Selected partition lock_reference does not match the current source, base registers, v0.2 temporal evidence, and selection decision"
        )
    if analysis_lock_reference != expected_lock:
        raise SelectedPartitionAdapterError(
            "Supplied selected-analysis lock does not match the selected partition's current lock"
        )

    base_lock = compute_annotation_lock_reference(
        base_root,
        report_id=partition[0],
        annotator_id=partition[1],
        annotation_pass_id=partition[2],
        source_text=source_text,
    )
    result = build_projection_for_partition(
        base_root,
        report_id=partition[0],
        annotator_id=partition[1],
        annotation_pass_id=partition[2],
        source_text=source_text,
        annotation_lock_confirmed=True,
        annotation_lock_reference=base_lock,
    )
    result["analysis_partition_selection"] = {
        "analysis_partition_id": selected["analysis_partition_id"],
        "partition_role": selected["partition_role"],
        "selection_status": selected["selection_status"],
        "selection_date": selected["selection_date"],
        "selection_rationale": selected["selection_rationale"],
    }
    result["analysis_lock_reference"] = expected_lock
    result["analysis_lock_verified"] = True
    result["temporal_evidence_validation"] = {
        "relation_count": temporal_validation["relation_count"],
        "evidence_link_count": temporal_validation["evidence_link_count"],
        "primary_direct_positive_relation_count": temporal_validation[
            "primary_direct_positive_relation_count"
        ],
    }
    return result
