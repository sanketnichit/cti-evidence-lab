"""Adapter from RECON v0.1 registers to the provisional projection module.

The adapter is intentionally fail-closed. It only builds projection inputs for
one exact report/annotator/annotation-pass partition after structural
validation against the exact frozen source text and report-level eligibility,
local-use and review-completion gates.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from projection_metrics_recon import TechniqueMapping, TemporalEdge, build_a120_mapping_sets, project_report_recon
import validate_annotations

POSITIVE_LABELS = {
    "BEFORE", "AFTER", "OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"
}
DIRECT_BASES = {"direct_source", "direct_timestamp"}


class AdapterError(ValueError):
    """Raised when a report partition is not safe to project."""


def _read_rows(root: Path, register: str) -> list[dict[str, str]]:
    path = root / "registers" / f"{register}.csv"
    if not path.exists():
        raise AdapterError(f"Missing register {path.name}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
            if row and any((value or "").strip() for value in row.values())
        ]


def _partition_matches(row: dict[str, str], report_id: str, annotator_id: str, annotation_pass_id: str) -> bool:
    row_annotator = row.get("annotator_id") or row.get("target_annotator_id", "")
    return (
        row.get("report_id") == report_id
        and row_annotator == annotator_id
        and row.get("annotation_pass_id") == annotation_pass_id
    )


def compute_annotation_lock_reference(
    bundle_root: str | Path,
    *,
    report_id: str,
    annotator_id: str,
    annotation_pass_id: str,
    source_text: str,
) -> str:
    """Return deterministic SHA-256 for one exact annotation partition.

    The digest covers the frozen source-text hash and all register rows for
    the selected report/annotator/pass partition. It detects later edits but
    is not a digital signature or proof of human authorship.
    """
    if not all((report_id, annotator_id, annotation_pass_id)):
        raise AdapterError("report_id, annotator_id and annotation_pass_id are required")
    root = Path(bundle_root)
    partition = (report_id, annotator_id, annotation_pass_id)
    partition_registers = {}
    for name in validate_annotations.HEADERS:
        rows = _read_rows(root, name)
        partition_registers[name] = [
            row for row in rows if _partition_matches(row, *partition)
        ]
    payload = {
        "lock_format": "CTI-EVIDENCE-LAB-ANNOTATION-LOCK-v1",
        "partition": {
            "report_id": report_id,
            "annotator_id": annotator_id,
            "annotation_pass_id": annotation_pass_id,
        },
        "source_text_sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
        "registers": partition_registers,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_projection_for_partition(
    bundle_root: str | Path,
    *,
    report_id: str,
    annotator_id: str,
    annotation_pass_id: str,
    source_text: str,
    annotation_lock_confirmed: bool = False,
    annotation_lock_reference: str = "",
) -> dict[str, Any]:
    """Validate and project one exact report/annotator/pass partition.

    No report text is stored or emitted in the result. The caller supplies the
    frozen source text so registry SHA-256 and evidence offsets can be checked.
    This function refuses ineligible, non-permitted, non-assessable or
    incomplete report partitions and fails if the bundle validator finds any
    structural error.
    """
    if not all((report_id, annotator_id, annotation_pass_id)):
        raise AdapterError("report_id, annotator_id and annotation_pass_id are required")
    if annotation_lock_confirmed is not True or not annotation_lock_reference.strip():
        raise AdapterError("Explicit annotation-lock confirmation and a non-empty immutable lock reference are required")
    root = Path(bundle_root)
    partition = (report_id, annotator_id, annotation_pass_id)
    expected_lock_reference = compute_annotation_lock_reference(
        root,
        report_id=report_id,
        annotator_id=annotator_id,
        annotation_pass_id=annotation_pass_id,
        source_text=source_text,
    )
    if annotation_lock_reference != expected_lock_reference:
        raise AdapterError("Annotation-lock reference does not match the current source and partition registers")
    source_texts = {partition: source_text}
    validation = validate_annotations.validate_bundle(root, source_texts)
    if validation.errors:
        details = "; ".join(f"{item.code}:{item.register}:{item.row}" for item in validation.errors[:12])
        raise AdapterError(f"Schema validation failed ({len(validation.errors)} errors): {details}")

    tables = {
        name: _read_rows(root, name)
        for name in validate_annotations.HEADERS
    }
    registry = [row for row in tables["report_registry"] if _partition_matches(row, *partition)]
    if len(registry) != 1:
        raise AdapterError(f"Expected exactly one report_registry row for {partition}; found {len(registry)}")
    report = registry[0]
    if report.get("source_scope_eligibility") != "ELIGIBLE":
        raise AdapterError("Report does not pass source_scope_eligibility=ELIGIBLE")
    if report.get("local_research_use_status") != "PERMITTED":
        raise AdapterError("Report does not pass local_research_use_status=PERMITTED")
    if report.get("report_assessability") != "ASSESSABLE":
        raise AdapterError("Report is not marked report_assessability=ASSESSABLE")
    if report.get("full_report_review_status") != "COMPLETE":
        raise AdapterError("Full-report review is not marked COMPLETE")

    partition_rows = {
        name: [row for row in rows if _partition_matches(row, *partition)]
        for name, rows in tables.items()
    }
    eligible_units = [
        row for row in partition_rows["activity_units"]
        if row.get("unit_role") == "event_leaf"
        and row.get("granularity") == "atomic_event"
        and row.get("instance_status") == "RESOLVED"
    ]
    eligible_event_ids = {row["activity_unit_id"] for row in eligible_units}

    a120_path = root / "vocabulary" / "A_120_ChronoCTI_Selected_Technique_IDs_derived_v0.1.json"
    if not a120_path.exists():
        raise AdapterError("Pinned derived A_120 vocabulary file is missing")
    raw_a120 = a120_path.read_bytes()
    a120_sha = hashlib.sha256(raw_a120).hexdigest()
    try:
        a120_doc = json.loads(raw_a120.decode("utf-8"))
        a120_ids = a120_doc["technique_ids"]
    except (UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise AdapterError(f"Pinned A_120 file is invalid: {exc}") from exc
    if (
        a120_doc.get("status") != "DERIVED_ID_EXTRACTION_NOT_ORIGINAL_CHRONOCTI_JSON"
        or len(a120_ids) != 120
        or len(set(a120_ids)) != 120
    ):
        raise AdapterError("Pinned A_120 file failed provenance/cardinality check")

    mapping_rows = [
        TechniqueMapping(
            mapping_id=row.get("mapping_id", ""),
            activity_unit_id=row.get("activity_unit_id", ""),
            baseline_parent_technique_id=row.get("baseline_parent_technique_id", ""),
            mapping_decision_status=row.get("mapping_decision_status", ""),
            mapping_basis=row.get("mapping_basis", ""),
            baseline_mapping_status=row.get("baseline_mapping_status", ""),
        )
        for row in partition_rows["event_mappings"]
    ]
    mapping_sets, mapping_filter_stats = build_a120_mapping_sets(
        mapping_rows, a120_ids, eligible_event_ids
    )

    # The validator accepts and retains derived/inferred temporal records with
    # warnings; the primary projection adapter includes only direct positive
    # relations. Non-positive pair assessments live in a separate register.
    primary_relation_rows = [
        row for row in partition_rows["temporal_relations"]
        if row.get("relation_label") in POSITIVE_LABELS
        and row.get("relation_basis") in DIRECT_BASES
        and row.get("scope_compatibility") == "COMPATIBLE"
    ]
    edges = [
        TemporalEdge(
            edge_id=row["relation_id"],
            source_event=row["event_a_id"],
            target_event=row["event_b_id"],
            relation=row["relation_label"],
            relation_basis=row["relation_basis"],
            scope_compatibility=row["scope_compatibility"],
        )
        for row in primary_relation_rows
    ]

    projection = project_report_recon(mapping_sets, edges)
    return {
        "status": "SYNTHETIC_OR_REVIEWED_PARTITION_PROJECTION_NOT_A_RESEARCH_FINDING",
        "partition": {
            "report_id": report_id,
            "annotator_id": annotator_id,
            "annotation_pass_id": annotation_pass_id,
        },
        "annotation_lock_reference": annotation_lock_reference,
        "annotation_lock_verified": True,
        "prior_exposure_status": report.get("prior_exposure_status"),
        "prior_exposure_requires_caution": report.get("prior_exposure_status") != "UNEXPOSED",
        "source_text_sha256": report.get("source_text_sha256"),
        "a120_vocabulary_sha256": a120_sha,
        "counts": {
            "eligible_resolved_atomic_event_leaves": len(eligible_event_ids),
            "accepted_a120_mapping_rows": mapping_filter_stats["accepted_a120_mapping_rows"],
            "excluded_mapping_rows": sum(
                value for key, value in mapping_filter_stats.items()
                if key.startswith("excluded_")
            ),
            "primary_direct_positive_temporal_relations": len(edges),
            "retained_nonprimary_or_nonpositive_temporal_relation_rows": len(partition_rows["temporal_relations"]) - len(edges),
        },
        "mapping_filter": mapping_filter_stats,
        "validation": {
            "error_count": len(validation.errors),
            "warning_count": len(validation.warnings),
            "bundle_warnings": [
                {
                    "code": item.code,
                    "message": item.message,
                    "register": item.register,
                    "row": item.row,
                }
                for item in validation.warnings
            ],
        },
        "projection": projection,
    }
