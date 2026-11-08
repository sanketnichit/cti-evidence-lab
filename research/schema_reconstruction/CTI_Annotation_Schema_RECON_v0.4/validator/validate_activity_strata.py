#!/usr/bin/env python3
"""Validator for the RECON v0.4 activity-stratum extension.

The v0.1 base bundle remains unchanged. Each activity unit receives exactly
one evidence-backed stratum row in the v0.4 companion register.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Mapping

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[2]
V1_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.1"
V2_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.2"
sys.path.insert(0, str(V1_ROOT / "validator"))
sys.path.insert(0, str(V2_ROOT / "validator"))
sys.path.insert(0, str(REPO_ROOT))

import validate_annotations as base_validator  # noqa: E402
from validate_temporal_evidence import SELECTION_HEADERS  # noqa: E402
from src.source_text_integrity import read_frozen_source  # noqa: E402

STRATUM_HEADERS = [
    "report_id", "annotator_id", "annotation_pass_id", "activity_unit_id",
    "activity_stratum", "stratum_basis", "evidence_span_id",
    "stratum_rationale", "annotator_confidence", "adjudication_status",
    "stratum_notes",
]
LOCK_HEADERS = [
    "report_id", "annotator_id", "annotation_pass_id",
    "analysis_lock_reference", "activity_strata_sha256", "lock_reference",
    "lock_format", "locked_by", "lock_date", "lock_notes",
]
ACTIVITY_STRATA = {
    "ATTACK_ACTION",
    "THREAT_ACTOR_COMMUNICATION",
    "ANALYST_OBSERVATION",
    "GENERIC_CAPABILITY",
    "OTHER_NON_PRIMARY",
    "UNRESOLVED_CLASSIFICATION",
}
STRATUM_BASES = {"REPORT_EXPLICIT", "SOURCE_SUPPORTED_HUMAN_JUDGMENT", "UNRESOLVED"}
LOCK_FORMAT = "CTI-EVIDENCE-LAB-ACTIVITY-STRATUM-LOCK-v1"
LOCK_REFERENCE_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def _partition(row: Mapping[str, str]) -> tuple[str, str, str]:
    return (
        row.get("report_id", ""),
        row.get("annotator_id", ""),
        row.get("annotation_pass_id", ""),
    )


def _read_exact(path: Path, headers: list[str]) -> tuple[list[dict[str, str]], str | None]:
    if not path.is_file():
        return [], f"missing file: {path}"
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != headers:
                return [], f"header mismatch in {path.name}: expected {headers!r}, got {reader.fieldnames!r}"
            rows = []
            for line, row in enumerate(reader, 2):
                if row is None or all((value or "").strip() == "" for value in row.values()):
                    continue
                if None in row:
                    return [], f"row-width mismatch in {path.name}:{line}"
                rows.append({key: (value or "").strip() for key, value in row.items()})
            return rows, None
    except (OSError, csv.Error, UnicodeError) as exc:
        return [], f"cannot read {path.name}: {exc}"


def _read_base_tables(base_bundle: Path) -> dict[str, list[dict[str, str]]]:
    tables = {}
    for name, headers in base_validator.HEADERS.items():
        rows, error = _read_exact(base_bundle / "registers" / f"{name}.csv", headers)
        if error:
            raise ValueError(error)
        tables[name] = rows
    return tables


def _canonical_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    normalized = [{key: row.get(key, "") for key in STRATUM_HEADERS} for row in rows]
    return sorted(normalized, key=lambda row: (
        row["report_id"], row["annotator_id"], row["annotation_pass_id"],
        row["activity_unit_id"],
    ))


def _sha256_json(payload: Any) -> str:
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def _route(stratum_a: str, stratum_b: str) -> str:
    if stratum_a == "ATTACK_ACTION" and stratum_b == "ATTACK_ACTION":
        return "PRIMARY_ATTACK_ACTION"
    if stratum_a == stratum_b:
        return "AUXILIARY_SAME_STRATUM"
    return "MIXED_STRATUM"


def validate_activity_strata(
    base_bundle: str | Path,
    strata_file: str | Path,
    *,
    source_texts: Mapping[tuple[str, str, str], str] | None = None,
) -> dict[str, Any]:
    """Validate complete, evidence-backed one-to-one activity-unit classification."""
    base_root = Path(base_bundle).resolve()
    base_validation = base_validator.validate_bundle(base_root, dict(source_texts or {}))
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    rows, read_error = _read_exact(Path(strata_file), STRATUM_HEADERS)
    if read_error:
        errors.append({"code": "STRATUM_REGISTER_INVALID", "message": read_error})
        rows = []

    try:
        tables = _read_base_tables(base_root)
    except ValueError as exc:
        tables = {name: [] for name in base_validator.HEADERS}
        errors.append({"code": "BASE_REGISTERS_INVALID", "message": str(exc)})

    units = {
        (*_partition(row), row.get("activity_unit_id", "")): row
        for row in tables["activity_units"]
    }
    evidence = {
        (*_partition(row), row.get("evidence_span_id", "")): row
        for row in tables["evidence_spans"]
    }
    seen: set[tuple[str, str, str, str]] = set()
    stratum_by_unit: dict[tuple[tuple[str, str, str], str], str] = {}
    unit_counts: dict[str, int] = {}
    for line, row in enumerate(rows, 2):
        partition = _partition(row)
        unit_id = row.get("activity_unit_id", "")
        key = (partition, unit_id)
        if not all(partition) or not unit_id:
            errors.append({"code": "STRATUM_PARTITION_OR_UNIT_ID_MISSING", "message": f"row {line}: report/annotator/pass and activity_unit_id are required"})
            continue
        if key in seen:
            errors.append({"code": "DUPLICATE_ACTIVITY_STRATUM", "message": f"row {line}: duplicate activity-unit stratum decision"})
            continue
        seen.add((*partition, unit_id))
        unit = units.get((*partition, unit_id))
        if unit is None:
            errors.append({"code": "STRATUM_ACTIVITY_UNIT_UNKNOWN", "message": f"row {line}: activity_unit_id does not resolve in the same report/annotator/pass partition"})
            continue

        stratum = row.get("activity_stratum", "")
        basis = row.get("stratum_basis", "")
        if stratum not in ACTIVITY_STRATA:
            errors.append({"code": "INVALID_ACTIVITY_STRATUM", "message": f"row {line}: activity_stratum is not in the controlled vocabulary"})
        if basis not in STRATUM_BASES:
            errors.append({"code": "INVALID_STRATUM_BASIS", "message": f"row {line}: stratum_basis is not controlled"})
        if not row.get("stratum_rationale"):
            errors.append({"code": "STRATUM_RATIONALE_MISSING", "message": f"row {line}: stratum_rationale is required"})
        span_id = row.get("evidence_span_id", "")
        if not span_id or (*partition, span_id) not in evidence:
            errors.append({"code": "STRATUM_EVIDENCE_MISSING_OR_UNKNOWN", "message": f"row {line}: evidence_span_id must resolve in the same partition"})
        if row.get("annotator_confidence") not in base_validator.CONFIDENCE:
            errors.append({"code": "INVALID_STRATUM_CONFIDENCE", "message": f"row {line}: annotator_confidence is invalid"})
        if row.get("adjudication_status") not in base_validator.ADJUDICATION_STATUSES:
            errors.append({"code": "INVALID_STRATUM_ADJUDICATION_STATUS", "message": f"row {line}: adjudication_status is invalid"})
        if stratum == "UNRESOLVED_CLASSIFICATION" and basis != "UNRESOLVED":
            errors.append({"code": "UNRESOLVED_STRATUM_BASIS_MISMATCH", "message": f"row {line}: UNRESOLVED_CLASSIFICATION requires stratum_basis=UNRESOLVED"})
        elif stratum and stratum != "UNRESOLVED_CLASSIFICATION" and basis == "UNRESOLVED":
            errors.append({"code": "RESOLVED_STRATUM_BASIS_MISMATCH", "message": f"row {line}: a resolved stratum requires report-explicit or source-supported human judgment"})
        if (
            stratum == "GENERIC_CAPABILITY"
            and unit.get("unit_role") == "event_leaf"
            and unit.get("granularity") == "atomic_event"
            and unit.get("instance_status") == "RESOLVED"
        ):
            errors.append({"code": "GENERIC_CAPABILITY_CANNOT_BE_RESOLVED_EVENT", "message": f"row {line}: a generic capability without a resolved execution cannot be a resolved atomic event leaf"})
        if stratum in ACTIVITY_STRATA:
            stratum_by_unit[key] = stratum
            unit_counts[stratum] = unit_counts.get(stratum, 0) + 1

    for key, unit in units.items():
        if key not in seen:
            errors.append({"code": "ACTIVITY_STRATUM_MISSING", "message": f"activity unit {key[1]!r} in partition {key[0]} has no stratum decision"})

    relation_routes: dict[str, int] = {
        "PRIMARY_ATTACK_ACTION": 0,
        "AUXILIARY_SAME_STRATUM": 0,
        "MIXED_STRATUM": 0,
    }
    relation_rows_by_route: dict[str, list[str]] = {key: [] for key in relation_routes}
    for line, row in enumerate(tables["temporal_relations"], 2):
        partition = _partition(row)
        a = stratum_by_unit.get((partition, row.get("event_a_id", "")))
        b = stratum_by_unit.get((partition, row.get("event_b_id", "")))
        if a is None or b is None:
            errors.append({"code": "RELATION_STRATUM_ENDPOINT_MISSING", "message": f"temporal_relations row {line}: both endpoints require a valid activity_stratum decision"})
            continue
        route = _route(a, b)
        relation_routes[route] += 1
        relation_rows_by_route[route].append(row.get("relation_id", ""))
        if route != "PRIMARY_ATTACK_ACTION" and (
            row.get("relation_label") in base_validator.POSITIVE_TEMPORAL_LABELS
            and row.get("relation_basis") in base_validator.DIRECT_RELATION_BASES
            and row.get("scope_compatibility") == "COMPATIBLE"
        ):
            warnings.append({
                "code": "NONPRIMARY_RELATION_ROUTED_OUT_OF_PRIMARY_GRAPH",
                "message": f"temporal relation {row.get('relation_id', '')!r} is {route} and cannot enter primary attack-action metrics",
            })

    assessment_routes = {"PRIMARY_ATTACK_ACTION": 0, "AUXILIARY_SAME_STRATUM": 0, "MIXED_STRATUM": 0}
    for line, row in enumerate(tables["candidate_pair_assessments"], 2):
        partition = _partition(row)
        a = stratum_by_unit.get((partition, row.get("event_a_id", "")))
        b = stratum_by_unit.get((partition, row.get("event_b_id", "")))
        if a is None or b is None:
            errors.append({"code": "ASSESSMENT_STRATUM_ENDPOINT_MISSING", "message": f"candidate_pair_assessments row {line}: both endpoints require a valid activity_stratum decision"})
            continue
        assessment_routes[_route(a, b)] += 1

    base_errors = [
        {"code": issue.code, "message": issue.message, "register": issue.register, "row": str(issue.row)}
        for issue in base_validation.errors
    ]
    return {
        "ok": not errors and base_validation.ok,
        "error_count": len(errors) + len(base_errors),
        "warning_count": len(warnings) + len(base_validation.warnings),
        "activity_unit_count": len(units),
        "stratum_decision_count": len(rows),
        "stratum_counts": dict(sorted(unit_counts.items())),
        "relation_rows_by_route": relation_routes,
        "relation_ids_by_route": relation_rows_by_route,
        "candidate_pair_assessment_rows_by_route": assessment_routes,
        "errors": errors + base_errors,
        "warnings": warnings + [
            {"code": issue.code, "message": issue.message}
            for issue in base_validation.warnings
        ],
    }


def build_activity_stratum_lock_rows(
    selection_file: str | Path,
    strata_file: str | Path,
    *,
    locked_by: str,
    lock_date: str,
    lock_notes: str = "",
) -> list[dict[str, str]]:
    selections, error = _read_exact(Path(selection_file), SELECTION_HEADERS)
    if error:
        raise ValueError(error)
    strata, error = _read_exact(Path(strata_file), STRATUM_HEADERS)
    if error:
        raise ValueError(error)
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
        analysis_ref = selection.get("lock_reference", "")
        if not LOCK_REFERENCE_RE.fullmatch(analysis_ref):
            raise ValueError(f"selected partition {partition} has an invalid v0.2 analysis lock reference")
        part_rows = [row for row in strata if _partition(row) == partition]
        strata_sha = _sha256_json(_canonical_rows(part_rows))
        payload = {
            "lock_format": LOCK_FORMAT,
            "partition": {
                "report_id": partition[0],
                "annotator_id": partition[1],
                "annotation_pass_id": partition[2],
            },
            "analysis_lock_reference": analysis_ref,
            "activity_strata_sha256": strata_sha,
        }
        lock_reference = "sha256:" + _sha256_json(payload)
        result.append({
            "report_id": partition[0],
            "annotator_id": partition[1],
            "annotation_pass_id": partition[2],
            "analysis_lock_reference": analysis_ref,
            "activity_strata_sha256": strata_sha,
            "lock_reference": lock_reference,
            "lock_format": LOCK_FORMAT,
            "locked_by": locked_by.strip(),
            "lock_date": lock_date,
            "lock_notes": lock_notes.strip(),
        })
    return result


def validate_activity_stratum_locks(
    selection_file: str | Path,
    strata_file: str | Path,
    lock_file: str | Path,
) -> dict[str, Any]:
    selections, selection_error = _read_exact(Path(selection_file), SELECTION_HEADERS)
    strata, strata_error = _read_exact(Path(strata_file), STRATUM_HEADERS)
    locks, lock_error = _read_exact(Path(lock_file), LOCK_HEADERS)
    errors = []
    for code, message in (
        ("SELECTION_REGISTER_INVALID", selection_error),
        ("STRATUM_REGISTER_INVALID", strata_error),
        ("STRATUM_LOCK_REGISTER_INVALID", lock_error),
    ):
        if message:
            errors.append({"code": code, "message": message})
    if errors:
        return {"ok": False, "error_count": len(errors), "lock_rows": len(locks), "errors": errors}

    selected = {
        _partition(row): row for row in selections
        if row.get("selection_status") == "SELECTED_FINAL"
    }
    lock_by_partition = {}
    for line, row in enumerate(locks, 2):
        partition = _partition(row)
        if partition in lock_by_partition:
            errors.append({"code": "DUPLICATE_ACTIVITY_STRATUM_LOCK", "message": f"row {line}: duplicate lock for selected partition"})
        lock_by_partition[partition] = row
        if partition not in selected:
            errors.append({"code": "ACTIVITY_STRATUM_LOCK_NOT_SELECTED", "message": f"row {line}: lock does not match a SELECTED_FINAL partition"})
        if row.get("lock_format") != LOCK_FORMAT:
            errors.append({"code": "ACTIVITY_STRATUM_LOCK_FORMAT_INVALID", "message": f"row {line}: unexpected lock_format"})
        if not row.get("locked_by"):
            errors.append({"code": "ACTIVITY_STRATUM_LOCK_OWNER_MISSING", "message": f"row {line}: locked_by is required"})
        try:
            date.fromisoformat(row.get("lock_date", ""))
        except ValueError:
            errors.append({"code": "ACTIVITY_STRATUM_LOCK_DATE_INVALID", "message": f"row {line}: lock_date must be YYYY-MM-DD"})
        if partition in selected:
            selection = selected[partition]
            analysis_ref = selection.get("lock_reference", "")
            part_rows = [item for item in strata if _partition(item) == partition]
            expected_sha = _sha256_json(_canonical_rows(part_rows))
            payload = {
                "lock_format": LOCK_FORMAT,
                "partition": {
                    "report_id": partition[0],
                    "annotator_id": partition[1],
                    "annotation_pass_id": partition[2],
                },
                "analysis_lock_reference": analysis_ref,
                "activity_strata_sha256": expected_sha,
            }
            expected_lock = "sha256:" + _sha256_json(payload)
            if row.get("analysis_lock_reference") != analysis_ref:
                errors.append({"code": "ACTIVITY_STRATUM_BASE_LOCK_MISMATCH", "message": f"row {line}: v0.2 selected-analysis lock reference changed"})
            if row.get("activity_strata_sha256") != expected_sha or row.get("lock_reference") != expected_lock:
                errors.append({"code": "ACTIVITY_STRATUM_LOCK_MISMATCH", "message": f"row {line}: activity-unit stratum rows changed after locking"})
    for partition in selected:
        if partition not in lock_by_partition:
            errors.append({"code": "ACTIVITY_STRATUM_LOCK_MISSING", "message": f"selected partition {partition} has no v0.4 activity-stratum lock"})
    return {"ok": not errors, "error_count": len(errors), "lock_rows": len(locks), "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate RECON v0.4 activity-stratum classifications and locks")
    parser.add_argument("--base-bundle", type=Path, required=True)
    parser.add_argument("--strata-file", type=Path, required=True)
    parser.add_argument("--selection-file", type=Path)
    parser.add_argument("--lock-file", type=Path)
    parser.add_argument("--sources-dir", type=Path)
    args = parser.parse_args()

    source_texts = {}
    if args.sources_dir:
        for source_path in sorted(args.sources_dir.glob("*.txt")):
            source_text = read_frozen_source(source_path)
            # v0.1 accepts exact annotation partitions as keys; the CLI can
            # verify report hashes only when partition IDs are supplied below.
            for row in _read_base_tables(args.base_bundle)["report_registry"]:
                if row.get("report_id") == source_path.stem and row.get("annotator_id") and row.get("annotation_pass_id"):
                    source_texts[(
                        row["report_id"], row["annotator_id"], row["annotation_pass_id"]
                    )] = source_text
    validation = validate_activity_strata(args.base_bundle, args.strata_file, source_texts=source_texts)
    lock_validation = None
    if args.selection_file or args.lock_file:
        if not args.selection_file or not args.lock_file:
            parser.error("--selection-file and --lock-file must be supplied together")
        lock_validation = validate_activity_stratum_locks(
            args.selection_file, args.strata_file, args.lock_file
        )
    result = {"validation": validation, "locks": lock_validation, "ok": validation["ok"] and (lock_validation is None or lock_validation["ok"])}
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
