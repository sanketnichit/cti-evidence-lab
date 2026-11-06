#!/usr/bin/env python3
"""Structural validation for the additive RECON v0.3 comparison-scope extension."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[2]
V1_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.1"
V2_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.2"
sys.path.insert(0, str(V1_ROOT / "validator"))
sys.path.insert(0, str(V2_ROOT / "validator"))
sys.path.insert(0, str(REPO_ROOT))

import validate_annotations as base_validator  # noqa: E402
from validate_temporal_evidence import (  # noqa: E402
    SELECTION_HEADERS,
    validate_analysis_partition_selection,
)

ASSIGNMENT_HEADERS = [
    "report_id", "annotator_id", "annotation_pass_id", "assignment_id",
    "activity_unit_id", "comparison_scope_id", "assignment_status",
    "assignment_basis", "evidence_span_id", "assignment_rationale",
    "annotator_confidence", "adjudication_status", "assignment_notes",
]
LOCK_HEADERS = [
    "report_id", "annotator_id", "annotation_pass_id", "lock_id",
    "analysis_lock_reference", "assignment_rows_sha256", "lock_reference",
    "lock_format", "locked_by", "lock_date", "lock_notes",
]
LOCK_FORMAT = "CTI-EVIDENCE-LAB-COMPARISON-SCOPE-LOCK-v0.3"
ASSIGNMENT_STATUSES = {"ASSIGNED", "NOT_ASSIGNED", "UNCERTAIN"}
ASSIGNMENT_BASES = {
    "REPORT_EXPLICIT", "SOURCE_SUPPORTED_HUMAN_JUDGMENT", "UNRESOLVED"
}
ASSIGNMENT_ADJUDICATION_STATUSES = {"UNREVIEWED"}
ASSIGNMENT_COMPARABLE_SCOPE_TYPES = set(base_validator.COMPARABLE_SCOPE_TYPES)


def _partition(row: dict[str, str]) -> tuple[str, str, str]:
    return base_validator._partition(row)


def _load_exact(path: str | Path, headers: list[str]) -> tuple[list[dict[str, str]], str | None]:
    source = Path(path)
    if not source.exists():
        return [], f"missing file: {source}"
    try:
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            actual = reader.fieldnames or []
            if actual != headers:
                return [], f"header mismatch in {source.name}: expected {headers}, got {actual}"
            rows = []
            for line_number, row in enumerate(reader, 2):
                if row is None or all((value or "").strip() == "" for value in row.values()):
                    continue
                if None in row:
                    return [], f"row-width mismatch in {source.name}:{line_number}"
                rows.append({key: (value or "").strip() for key, value in row.items()})
            return rows, None
    except (OSError, csv.Error, UnicodeError) as exc:
        return [], f"cannot read {source}: {exc}"


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_assignment_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    canonical = [
        {key: row.get(key, "") for key in ASSIGNMENT_HEADERS}
        for row in rows
    ]
    return sorted(
        canonical,
        key=lambda row: (
            row["assignment_id"], row["activity_unit_id"],
            row["comparison_scope_id"], row["assignment_status"],
        ),
    )


def _read_base_tables(base_bundle: Path) -> tuple[dict[str, list[dict[str, str]]], list[str]]:
    tables: dict[str, list[dict[str, str]]] = {}
    errors = []
    for name, headers in base_validator.HEADERS.items():
        rows, error = _load_exact(base_bundle / "registers" / f"{name}.csv", headers)
        if error:
            errors.append(error)
            rows = []
        tables[name] = rows
    return tables, errors


def validate_assignment_register(
    base_bundle: str | Path,
    assignment_file: str | Path,
    *,
    source_texts: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Validate event-to-comparison-scope decisions and their downstream use."""
    assignments, read_error = _load_exact(assignment_file, ASSIGNMENT_HEADERS)
    errors: list[dict[str, str]] = []
    if read_error:
        errors.append({"code": "ASSIGNMENT_REGISTER_INVALID", "message": read_error})
        return {"ok": False, "error_count": len(errors), "rows": 0, "errors": errors}

    tables, base_errors = _read_base_tables(Path(base_bundle))
    for message in base_errors:
        errors.append({"code": "BASE_REGISTER_INVALID", "message": message})
    partition_sources = {}
    for registry_row in tables["report_registry"]:
        report_id = registry_row.get("report_id", "")
        if source_texts and report_id in source_texts:
            partition_sources[_partition(registry_row)] = source_texts[report_id]
    base_validation = base_validator.validate_bundle(base_bundle, partition_sources)
    for issue in base_validation.errors:
        errors.append({
            "code": "BASE_SCHEMA_VALIDATION_FAILED",
            "message": f"{issue.register or 'bundle'}:{issue.row}: {issue.code}: {issue.message}",
        })
    registry_partitions = {_partition(row) for row in tables["report_registry"]}
    units = {
        (*_partition(row), row.get("activity_unit_id", "")): row
        for row in tables["activity_units"]
    }
    scopes = {
        (*_partition(row), row.get("scope_id", "")): row
        for row in tables["report_scopes"]
    }
    evidence = {
        (*_partition(row), row.get("evidence_span_id", "")): row
        for row in tables["evidence_spans"]
    }

    seen_ids: set[tuple[tuple[str, str, str], str]] = set()
    seen_decisions: set[tuple[tuple[str, str, str], str, str]] = set()
    for line_number, row in enumerate(assignments, 2):
        partition = _partition(row)
        assignment_id = row.get("assignment_id", "")
        event_id = row.get("activity_unit_id", "")
        scope_id = row.get("comparison_scope_id", "")
        status = row.get("assignment_status", "")
        basis = row.get("assignment_basis", "")
        if not all(partition):
            errors.append({"code": "ASSIGNMENT_PARTITION_KEY_MISSING", "message": f"row {line_number}: report/annotator/pass is required"})
        elif partition not in registry_partitions:
            errors.append({"code": "ASSIGNMENT_PARTITION_UNKNOWN", "message": f"row {line_number}: report partition is not registered"})
        if not assignment_id:
            errors.append({"code": "ASSIGNMENT_ID_MISSING", "message": f"row {line_number}: assignment_id is required"})
        elif (partition, assignment_id) in seen_ids:
            errors.append({"code": "DUPLICATE_ASSIGNMENT_ID", "message": f"row {line_number}: assignment_id repeats in its partition"})
        seen_ids.add((partition, assignment_id))
        decision_key = (partition, event_id, scope_id)
        if decision_key in seen_decisions:
            errors.append({"code": "DUPLICATE_EVENT_SCOPE_DECISION", "message": f"row {line_number}: event/comparison-scope decision repeats"})
        seen_decisions.add(decision_key)

        unit = units.get((*partition, event_id))
        scope = scopes.get((*partition, scope_id))
        if not unit:
            errors.append({"code": "ASSIGNMENT_EVENT_UNKNOWN", "message": f"row {line_number}: activity_unit_id does not resolve in the same partition"})
        elif (
            unit.get("unit_role") != "event_leaf"
            or unit.get("granularity") != "atomic_event"
            or unit.get("instance_status") != "RESOLVED"
        ):
            errors.append({"code": "ASSIGNMENT_EVENT_INELIGIBLE", "message": f"row {line_number}: only RESOLVED atomic event_leaf units may receive comparison-scope assignments"})
        if not scope:
            errors.append({"code": "ASSIGNMENT_SCOPE_UNKNOWN", "message": f"row {line_number}: comparison_scope_id does not resolve in the same partition"})
        if status not in ASSIGNMENT_STATUSES:
            errors.append({"code": "INVALID_ASSIGNMENT_STATUS", "message": f"row {line_number}: assignment_status must be ASSIGNED, NOT_ASSIGNED or UNCERTAIN"})
        if basis not in ASSIGNMENT_BASES:
            errors.append({"code": "INVALID_ASSIGNMENT_BASIS", "message": f"row {line_number}: assignment_basis is not controlled"})
        if not row.get("assignment_rationale"):
            errors.append({"code": "ASSIGNMENT_RATIONALE_MISSING", "message": f"row {line_number}: assignment_rationale is required"})
        if row.get("annotator_confidence") not in base_validator.CONFIDENCE:
            errors.append({"code": "INVALID_ASSIGNMENT_CONFIDENCE", "message": f"row {line_number}: annotator_confidence is invalid"})
        if row.get("adjudication_status") not in ASSIGNMENT_ADJUDICATION_STATUSES:
            errors.append({"code": "INVALID_ASSIGNMENT_ADJUDICATION_STATUS", "message": f"row {line_number}: v0.3 records independent decisions only; adjudication is not implemented"})
        span_id = row.get("evidence_span_id", "")
        if span_id and (*partition, span_id) not in evidence:
            errors.append({"code": "ASSIGNMENT_EVIDENCE_UNKNOWN", "message": f"row {line_number}: evidence_span_id does not resolve in the same partition"})

        if status in {"ASSIGNED", "NOT_ASSIGNED"}:
            if basis not in {"REPORT_EXPLICIT", "SOURCE_SUPPORTED_HUMAN_JUDGMENT"}:
                errors.append({"code": "SCOPE_DECISION_BASIS_INVALID", "message": f"row {line_number}: ASSIGNED and NOT_ASSIGNED require report-explicit or source-supported human judgment"})
            if not span_id:
                errors.append({"code": "SCOPE_DECISION_EVIDENCE_MISSING", "message": f"row {line_number}: ASSIGNED and NOT_ASSIGNED require an evidence span"})
        elif status == "UNCERTAIN" and basis != "UNRESOLVED":
            errors.append({"code": "UNCERTAIN_SCOPE_BASIS_INVALID", "message": f"row {line_number}: UNCERTAIN requires assignment_basis=UNRESOLVED"})

        if scope:
            if scope.get("scope_status") != "RESOLVED":
                errors.append({"code": "CANDIDATE_SCOPE_NOT_RESOLVED", "message": f"row {line_number}: candidate comparison scope must be RESOLVED"})
            if scope.get("scope_type") not in ASSIGNMENT_COMPARABLE_SCOPE_TYPES:
                errors.append({"code": "CANDIDATE_SCOPE_TYPE_INELIGIBLE", "message": f"row {line_number}: report aggregate/unresolved scope types cannot be candidate comparison scopes"})
        if unit and scope:
            ancestors = {
                item.get("scope_id", "")
                for item in base_validator.resolved_scope_ancestor_chain(
                    unit.get("scope_id", ""),
                    [candidate for candidate in tables["report_scopes"] if _partition(candidate) == partition],
                )
            }
            if scope_id not in ancestors:
                errors.append({"code": "CANDIDATE_SCOPE_NOT_EVENT_ANCESTOR", "message": f"row {line_number}: candidate scope must be in the event's resolved scope ancestry"})

    # Every resolved atomic event leaf must carry one explicit decision for
    # every eligible resolved non-report scope in its ancestry. Missing rows
    # are incomplete review, never an implicit NOT_ASSIGNED decision.
    expected_scope_ids_by_event = {}
    for unit in tables["activity_units"]:
        if (
            unit.get("unit_role") != "event_leaf"
            or unit.get("granularity") != "atomic_event"
            or unit.get("instance_status") != "RESOLVED"
        ):
            continue
        partition = _partition(unit)
        chain = base_validator.resolved_scope_ancestor_chain(
            unit.get("scope_id", ""),
            [candidate for candidate in tables["report_scopes"] if _partition(candidate) == partition],
        )
        expected_scope_ids = {
            item.get("scope_id", "")
            for item in chain
            if item.get("scope_type") in ASSIGNMENT_COMPARABLE_SCOPE_TYPES
        }
        expected_scope_ids_by_event[(partition, unit.get("activity_unit_id", ""))] = expected_scope_ids
    for (partition, event_id), expected_scope_ids in expected_scope_ids_by_event.items():
        for scope_id in sorted(expected_scope_ids):
            if (partition, event_id, scope_id) not in seen_decisions:
                errors.append({
                    "code": "ASSIGNMENT_REVIEW_INCOMPLETE",
                    "message": (
                        f"{partition[0]}/{partition[1]}/{partition[2]} event {event_id!r} "
                        f"has no explicit decision for candidate scope {scope_id!r}"
                    ),
                })

    assigned_by_event: dict[tuple[tuple[str, str, str], str], set[str]] = {}
    for row in assignments:
        if row.get("assignment_status") == "ASSIGNED":
            key = (_partition(row), row.get("activity_unit_id", ""))
            assigned_by_event.setdefault(key, set()).add(row.get("comparison_scope_id", ""))

    for line_number, row in enumerate(tables["temporal_relations"], 2):
        if (
            row.get("relation_label") in base_validator.POSITIVE_TEMPORAL_LABELS
            and row.get("relation_basis") in base_validator.DIRECT_RELATION_BASES
            and row.get("scope_compatibility") == "COMPATIBLE"
        ):
            partition = _partition(row)
            a, b, scope_id = row.get("event_a_id", ""), row.get("event_b_id", ""), row.get("comparison_scope_id", "")
            if (
                not scope_id
                or scope_id not in assigned_by_event.get((partition, a), set())
                or scope_id not in assigned_by_event.get((partition, b), set())
            ):
                errors.append({"code": "RELATION_SCOPE_NOT_ASSIGNED_TO_BOTH_ENDPOINTS", "message": f"temporal_relations row {line_number}: primary positive relation scope must be explicitly ASSIGNED to both endpoint events"})
    for line_number, row in enumerate(tables["candidate_pair_assessments"], 2):
        if row.get("scope_compatibility") == "COMPATIBLE":
            partition = _partition(row)
            a, b, scope_id = row.get("event_a_id", ""), row.get("event_b_id", ""), row.get("comparison_scope_id", "")
            if (
                not scope_id
                or scope_id not in assigned_by_event.get((partition, a), set())
                or scope_id not in assigned_by_event.get((partition, b), set())
            ):
                errors.append({"code": "ASSESSMENT_SCOPE_NOT_ASSIGNED_TO_BOTH_ENDPOINTS", "message": f"candidate_pair_assessments row {line_number}: COMPATIBLE assessment scope must be explicitly ASSIGNED to both endpoint events"})

    return {"ok": not errors, "error_count": len(errors), "rows": len(assignments), "errors": errors}


def _partition_assignment_rows(rows: list[dict[str, str]], partition: tuple[str, str, str]) -> list[dict[str, str]]:
    return [row for row in rows if _partition(row) == partition]


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_assignment_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    canonical = [{key: row.get(key, "") for key in ASSIGNMENT_HEADERS} for row in rows]
    return sorted(canonical, key=lambda row: (
        row["assignment_id"], row["activity_unit_id"],
        row["comparison_scope_id"], row["assignment_status"],
    ))


def build_scope_assignment_lock_rows(
    selection_file: str | Path,
    assignment_file: str | Path,
    *,
    base_bundle: str | Path,
    locked_by: str,
    lock_date: str,
    lock_notes: str = "",
) -> list[dict[str, str]]:
    selections, error = _load_exact(selection_file, SELECTION_HEADERS)
    if error:
        raise ValueError(error)
    assignments, error = _load_exact(assignment_file, ASSIGNMENT_HEADERS)
    if error:
        raise ValueError(error)
    selection_errors, _ = validate_analysis_partition_selection(
        Path(base_bundle), Path(selection_file)
    )
    if selection_errors:
        raise ValueError(f"selected analysis partition register is invalid: {selection_errors}")
    assignment_validation = validate_assignment_register(base_bundle, assignment_file)
    if not assignment_validation["ok"]:
        raise ValueError(f"comparison-scope assignment register is invalid: {assignment_validation['errors']}")
    if not locked_by.strip():
        raise ValueError("locked_by is required")
    try:
        date.fromisoformat(lock_date)
    except ValueError as exc:
        raise ValueError("lock_date must use ISO YYYY-MM-DD") from exc
    result = []
    for selection in selections:
        if selection.get("selection_status") != "SELECTED_FINAL":
            continue
        partition = _partition(selection)
        partition_rows = _partition_assignment_rows(assignments, partition)
        analysis_reference = selection.get("lock_reference", "")
        if not analysis_reference:
            raise ValueError(f"selected partition {partition} has no v0.2 analysis lock reference")
        rows_sha = _sha256_text(_canonical_json(canonical_assignment_rows(partition_rows)))
        payload = {
            "lock_format": LOCK_FORMAT,
            "partition": {"report_id": partition[0], "annotator_id": partition[1], "annotation_pass_id": partition[2]},
            "analysis_lock_reference": analysis_reference,
            "assignment_rows_sha256": rows_sha,
        }
        lock_reference = "sha256:" + _sha256_text(_canonical_json(payload))
        result.append({
            "report_id": partition[0],
            "annotator_id": partition[1],
            "annotation_pass_id": partition[2],
            "lock_id": "scope-assignment-lock-" + "-".join(partition),
            "analysis_lock_reference": analysis_reference,
            "assignment_rows_sha256": rows_sha,
            "lock_reference": lock_reference,
            "lock_format": LOCK_FORMAT,
            "locked_by": locked_by.strip(),
            "lock_date": lock_date,
            "lock_notes": lock_notes.strip(),
        })
    return result


def validate_scope_assignment_locks(
    v2_extension_root: str | Path,
    assignment_file: str | Path,
    lock_file: str | Path,
    base_bundle: str | Path,
    *,
    source_texts: dict[str, str] | None = None,
) -> dict[str, Any]:
    selection_file = Path(v2_extension_root) / "registers" / "analysis_partition_selection.csv"
    selections, selection_error = _load_exact(selection_file, SELECTION_HEADERS)
    assignments, assignment_error = _load_exact(assignment_file, ASSIGNMENT_HEADERS)
    locks, lock_error = _load_exact(lock_file, LOCK_HEADERS)
    errors = []
    selection_validation_errors, _ = validate_analysis_partition_selection(
        Path(base_bundle), selection_file
    )
    if selection_validation_errors:
        errors.append({
            "code": "SELECTION_REGISTER_VALIDATION_FAILED",
            "message": str(selection_validation_errors),
        })
    assignment_validation = validate_assignment_register(
        base_bundle, assignment_file, source_texts=source_texts
    )
    if not assignment_validation["ok"]:
        errors.append({
            "code": "ASSIGNMENT_REGISTER_VALIDATION_FAILED",
            "message": str(assignment_validation["errors"]),
        })
    for code, message in (
        ("SELECTION_REGISTER_INVALID", selection_error),
        ("ASSIGNMENT_REGISTER_INVALID", assignment_error),
        ("ASSIGNMENT_LOCK_REGISTER_INVALID", lock_error),
    ):
        if message:
            errors.append({"code": code, "message": message})
    if errors:
        return {"ok": False, "error_count": len(errors), "lock_rows": len(locks), "errors": errors}

    selected = {
        _partition(row): row for row in selections
        if row.get("selection_status") == "SELECTED_FINAL"
    }
    locks_by_partition = {}
    lock_ids = set()
    for line_number, row in enumerate(locks, 2):
        partition = _partition(row)
        if partition in locks_by_partition:
            errors.append({"code": "DUPLICATE_SCOPE_ASSIGNMENT_LOCK", "message": f"lock row {line_number}: duplicate lock for selected partition"})
        locks_by_partition[partition] = row
        lock_id = row.get("lock_id", "")
        if not lock_id or lock_id in lock_ids:
            errors.append({"code": "SCOPE_ASSIGNMENT_LOCK_ID_INVALID", "message": f"lock row {line_number}: lock_id is missing or duplicated"})
        lock_ids.add(lock_id)
        if partition not in selected:
            errors.append({"code": "SCOPE_ASSIGNMENT_LOCK_NOT_SELECTED", "message": f"lock row {line_number}: lock does not match a SELECTED_FINAL partition"})
        if row.get("lock_format") != LOCK_FORMAT:
            errors.append({"code": "SCOPE_ASSIGNMENT_LOCK_FORMAT_INVALID", "message": f"lock row {line_number}: unexpected lock format"})
        if not row.get("locked_by"):
            errors.append({"code": "SCOPE_ASSIGNMENT_LOCK_OWNER_MISSING", "message": f"lock row {line_number}: locked_by is required"})
        try:
            date.fromisoformat(row.get("lock_date", ""))
        except ValueError:
            errors.append({"code": "SCOPE_ASSIGNMENT_LOCK_DATE_INVALID", "message": f"lock row {line_number}: lock_date must use ISO YYYY-MM-DD"})
        if partition in selected:
            expected_analysis = selected[partition].get("lock_reference", "")
            if row.get("analysis_lock_reference") != expected_analysis:
                errors.append({"code": "SCOPE_ASSIGNMENT_BASE_LOCK_MISMATCH", "message": f"lock row {line_number}: v0.2 analysis lock reference changed"})
            part_rows = _partition_assignment_rows(assignments, partition)
            expected_rows = _sha256_text(_canonical_json(canonical_assignment_rows(part_rows)))
            payload = {
                "lock_format": LOCK_FORMAT,
                "partition": {"report_id": partition[0], "annotator_id": partition[1], "annotation_pass_id": partition[2]},
                "analysis_lock_reference": expected_analysis,
                "assignment_rows_sha256": expected_rows,
            }
            expected_lock = "sha256:" + _sha256_text(_canonical_json(payload))
            if row.get("assignment_rows_sha256") != expected_rows or row.get("lock_reference") != expected_lock:
                errors.append({"code": "SCOPE_ASSIGNMENT_LOCK_MISMATCH", "message": f"lock row {line_number}: assignment rows or v0.2 analysis lock changed after locking"})
    for partition in selected:
        if partition not in locks_by_partition:
            errors.append({"code": "SCOPE_ASSIGNMENT_LOCK_MISSING", "message": f"selected partition {partition} has no v0.3 comparison-scope assignment lock"})
    return {"ok": not errors, "error_count": len(errors), "lock_rows": len(locks), "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate RECON v0.3 event comparison-scope assignments")
    parser.add_argument("--base-bundle", type=Path, required=True)
    parser.add_argument("--v2-extension", type=Path, required=True)
    parser.add_argument("--assignment-file", type=Path, required=True)
    parser.add_argument("--lock-file", type=Path, required=True)
    parser.add_argument("--sources-dir", type=Path, help="Optional frozen source directory with REPORT_ID.txt files")
    args = parser.parse_args()
    source_texts = {}
    if args.sources_dir:
        from src.source_text_integrity import read_frozen_source
        source_texts = {
            path.stem: read_frozen_source(path)
            for path in sorted(args.sources_dir.glob("*.txt"))
        }
    assignments = validate_assignment_register(
        args.base_bundle, args.assignment_file, source_texts=source_texts
    )
    locks = validate_scope_assignment_locks(
        args.v2_extension, args.assignment_file, args.lock_file,
        args.base_bundle, source_texts=source_texts
    )
    result = {
        "ok": assignments["ok"] and locks["ok"],
        "assignment_validation": assignments,
        "lock_validation": locks,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
