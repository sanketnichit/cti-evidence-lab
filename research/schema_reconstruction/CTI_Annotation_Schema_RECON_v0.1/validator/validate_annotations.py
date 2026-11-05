#!/usr/bin/env python3
"""Structural validator for CTI Annotation Schema RECON v0.1.

This validates only the explicitly recorded structure and decisions. It does not
judge whether source text semantically supports an event, mapping, scope or relation.
It is intentionally tied to the reconstructed schema, not original Schema v0.4.2.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[2]
sys.path.insert(0, str(REPO_ROOT))
from src.source_text_integrity import frozen_source_sha256, read_frozen_source  # noqa: E402

REGISTER_DIR = PACKAGE_ROOT / "registers"
VOCAB_PATH = PACKAGE_ROOT / "vocabulary" / "A_120_ChronoCTI_Selected_Technique_IDs_derived_v0.1.json"
ATTACK_RELEASE = "Enterprise ATT&CK v12.1"
ATTACK_CROSSWALK_RELATIVE_PATH = (
    "vocabulary/A_120_Exact_to_Parent_Crosswalk_v0.1.csv"
)
ATTACK_CROSSWALK_MANIFEST_RELATIVE_PATH = (
    "vocabulary/A_120_Exact_to_Parent_Crosswalk_v0.1.manifest.json"
)
ATTACK_CROSSWALK_SHA256 = (
    "f449ff8bd1551b6d6656d2f25a82b7c55a0b134bbecd4215f0f10330ec85be29"
)
ATTACK_SOURCE_SHA256 = (
    "e84679af4bc46bba2ba92f60182101f146d5b966898e47924de7321e6bffeaa1"
)
ATTACK_SOURCE_GIT_BLOB_SHA1 = "7a99efb3a8c89b06dd9db1a9a17e4201160ac4ee"
ATTACK_SOURCE_SIZE_BYTES = 38207821
ATTACK_CROSSWALK_HEADERS = [
    "attack_release",
    "exact_technique_id",
    "exact_technique_name",
    "stix_object_id",
    "is_subtechnique",
    "parent_technique_id",
    "parent_technique_name",
    "parent_in_A_120",
    "revoked",
    "deprecated",
    "relationship_type",
    "relationship_source_object_id",
    "relationship_target_object_id",
]

HEADERS = {
    "report_registry": ["report_id","annotator_id","annotation_pass_id","protocol_version","schema_version","source_title","source_vendor","source_url","source_path","retrieval_date","publication_date","corpus_name","corpus_release","split","language","source_text_sha256","source_text_char_count","extraction_method","transformation_notes","source_scope_eligibility","source_scope_reason","local_research_use_status","local_research_use_basis","public_reuse_status","rights_notes","report_assessability","assessability_reason","full_report_review_status","prior_exposure_status","annotator_notes"],
    "report_scopes": ["report_id","annotator_id","annotation_pass_id","scope_id","parent_scope_id","scope_type","scope_label","scope_description","scope_status","scope_confidence","adjudication_status","scope_notes"],
    "activity_units": ["report_id","annotator_id","annotation_pass_id","activity_unit_id","scope_id","parent_activity_unit_id","granularity","unit_role","instance_status","count_status","count_exact","count_min","count_max","count_qualitative","recurrence_pattern","unit_summary","actor_ref","host_or_asset_ref","annotator_confidence","adjudication_status","unit_notes"],
    "event_mentions": ["report_id","annotator_id","annotation_pass_id","mention_id","activity_unit_id","primary_evidence_span_id","sentence_id","section_locator","mention_kind","instance_status","resolved_event_instance_id","event_type_text","actor_text","target_text","asset_or_host_text","time_expression","mention_unit_status_note","annotator_confidence","adjudication_status","mention_notes"],
    "evidence_spans": ["report_id","annotator_id","annotation_pass_id","evidence_span_id","char_start","char_end","evidence_text","sentence_id","section_locator","paragraph_locator","figure_locator","source_text_sha256","span_kind","span_notes"],
    "record_evidence_links": ["report_id","annotator_id","annotation_pass_id","link_id","record_type","record_id","evidence_span_id","evidence_role","link_notes"],
    "event_mappings": ["report_id","annotator_id","annotation_pass_id","mapping_id","activity_unit_id","event_instance_id","exact_technique_id","exact_technique_name","attack_version","mapping_basis","mapping_decision_status","alternative_group_id","alternative_to_mapping_id","baseline_vocabulary_id","baseline_vocabulary_sha256","baseline_parent_technique_id","baseline_mapping_status","annotator_confidence","adjudication_status","mapping_notes"],
    "time_evidence": ["report_id","annotator_id","annotation_pass_id","time_evidence_id","activity_unit_id","mention_id","raw_time_text","time_type","time_precision","timezone_text","timezone_status","normalized_start","normalized_end","normalized_timezone","normalization_status","uncertainty_notes","primary_evidence_span_id","annotator_confidence","adjudication_status","time_notes"],
    "temporal_relations": ["report_id","annotator_id","annotation_pass_id","relation_id","event_a_id","event_b_id","comparison_scope_id","scope_compatibility","relation_label","relation_basis","evidence_scope","primary_evidence_span_id","annotator_confidence","adjudication_status","relation_notes"],
    "candidate_pair_assessments": ["report_id","annotator_id","annotation_pass_id","assessment_id","event_a_id","event_b_id","candidate_rule_id","candidate_rule_version","comparison_scope_id","scope_compatibility","assessment_label","related_relation_id","assessment_reason","adjudication_status","assessment_notes"],
    "non_temporal_relations": ["report_id","annotator_id","annotation_pass_id","non_temporal_relation_id","activity_unit_a_id","activity_unit_b_id","relation_label","evidence_scope","primary_evidence_span_id","annotator_confidence","adjudication_status","relation_notes"],
    "adjudication_log": ["report_id","annotation_pass_id","adjudication_id","target_annotator_id","reviewer_id","target_register","target_record_id","field_name","original_value","proposed_value","final_value","decision_status","rationale","decision_date","primary_evidence_span_id","adjudication_notes"],
}

INSTANCE_STATUSES = {"RESOLVED", "UNRESOLVED", "GENERIC_BEHAVIOUR", "NOT_AN_EVENT"}
GRANULARITIES = {"atomic_event", "repeated_event_series", "activity_episode", "report_level_aggregate", "unresolved"}
UNIT_ROLES = {"event_leaf", "series_container", "episode_container", "aggregate_container", "unresolved_unit"}
COUNT_STATUSES = {"exact", "minimum", "range", "qualitative_only", "unknown"}
MAPPING_BASES = {"report_explicit_subtechnique", "report_explicit_parent", "source_supported_analyst_candidate", "workbook_only", "unresolved"}
MAPPING_DECISIONS = {"ACCEPTED", "ALTERNATIVE", "REJECTED", "UNRESOLVED"}
BASELINE_MAPPING_STATUSES = {"IN_VOCAB", "OUT_OF_VOCAB", "UNRESOLVED", "NOT_APPLICABLE"}
TEMPORAL_LABELS = {"BEFORE", "AFTER", "OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED", "NO_TEMPORAL_CLAIM", "VAGUE_OR_AMBIGUOUS", "NOT_ASSESSABLE"}
POSITIVE_TEMPORAL_LABELS = {"BEFORE", "AFTER", "OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"}
DIRECT_RELATION_BASES = {"direct_source", "direct_timestamp"}
RELATION_BASES = DIRECT_RELATION_BASES | {"derived_transitive", "inference", "unresolved"}
EVIDENCE_SCOPES = {"SENTENCE", "CROSS_SENTENCE", "DOCUMENT_CONTEXT"}
CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}
ADJUDICATION_STATUSES = {"UNREVIEWED", "AGREED", "ADJUDICATED"}
NON_TEMPORAL_LABELS = {"CAUSES_OR_ENABLES", "DEPENDS_ON", "PRECONDITION_OF", "NARRATIVE_ORDER_ONLY"}
SCOPE_COMPATIBILITY = {"COMPATIBLE", "INCOMPATIBLE", "UNCERTAIN"}
ASSESSABILITY = {"ASSESSABLE", "NOT_ASSESSABLE", "PENDING"}
ELIGIBILITY = {"ELIGIBLE", "INELIGIBLE", "PENDING"}
LOCAL_USE = {"PERMITTED", "NOT_PERMITTED", "UNRESOLVED"}
PUBLIC_REUSE = {"PERMITTED", "RESTRICTED", "UNRESOLVED", "NOT_PLANNED"}
FULL_REVIEW = {"NOT_STARTED", "IN_PROGRESS", "COMPLETE"}
PRIOR_EXPOSURE = {"UNEXPOSED", "AI_EXPOSED", "HUMAN_EXPOSED", "MIXED", "UNKNOWN"}
DECISION_REGISTER = {"report_registry", "report_scopes", "activity_units", "event_mentions", "evidence_spans", "record_evidence_links", "event_mappings", "time_evidence", "temporal_relations", "candidate_pair_assessments", "non_temporal_relations"}


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    register: str = ""
    row: int = 0


@dataclass
class ValidationReport:
    issues: list[Issue]
    rows_by_register: dict[str, int]
    primary_positive_temporal_edges: int
    accepted_a120_mappings: int
    assessable_reports: int
    eligible_reports: int
    eligible_report_partitions: int
    assessable_report_partitions: int
    report_level_decision_conflicts: int
    vocabulary_count: int
    vocabulary_sha256: str
    attack_release: str
    attack_crosswalk_count: int
    attack_crosswalk_sha256: str

    @property
    def errors(self) -> list[Issue]:
        return [x for x in self.issues if x.severity == "ERROR"]

    @property
    def warnings(self) -> list[Issue]:
        return [x for x in self.issues if x.severity == "WARNING"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "rows_by_register": self.rows_by_register,
            "primary_positive_temporal_edges": self.primary_positive_temporal_edges,
            "accepted_a120_mappings": self.accepted_a120_mappings,
            "eligible_reports": self.eligible_reports,
            "assessable_reports": self.assessable_reports,
            "eligible_report_partitions": self.eligible_report_partitions,
            "assessable_report_partitions": self.assessable_report_partitions,
            "report_level_decision_conflicts": self.report_level_decision_conflicts,
            "a120_vocabulary_count": self.vocabulary_count,
            "a120_vocabulary_sha256": self.vocabulary_sha256,
            "attack_release": self.attack_release,
            "attack_crosswalk_count": self.attack_crosswalk_count,
            "attack_crosswalk_sha256": self.attack_crosswalk_sha256,
            "issues": [asdict(x) for x in self.issues],
        }


def _add(issues: list[Issue], severity: str, code: str, message: str, register: str = "", row: int = 0) -> None:
    issues.append(Issue(severity, code, message, register, row))


def _partition(row: dict[str, str]) -> tuple[str, str, str]:
    """Return the data-owning annotation partition for a register row."""
    annotator = row.get("annotator_id", "")
    if not annotator and row.get("target_annotator_id"):
        annotator = row.get("target_annotator_id", "")
    return (row.get("report_id", ""), annotator, row.get("annotation_pass_id", ""))


def _read_table(root: Path, name: str, issues: list[Issue]) -> list[dict[str, str]]:
    path = root / "registers" / f"{name}.csv"
    if not path.exists():
        _add(issues, "ERROR", "MISSING_REGISTER", f"Missing register file: {path.name}", name)
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != HEADERS[name]:
                _add(issues, "ERROR", "HEADER_MISMATCH", f"Expected exact header {HEADERS[name]!r}; got {reader.fieldnames!r}", name, 1)
                return []
            rows: list[dict[str, str]] = []
            for line_no, row in enumerate(reader, start=2):
                if row is None or all((v or "").strip() == "" for v in row.values()):
                    continue
                if None in row:
                    _add(issues, "ERROR", "ROW_WIDTH_MISMATCH", "Row contains more cells than header columns", name, line_no)
                    continue
                rows.append({k: (v or "").strip() for k, v in row.items()})
            return rows
    except (OSError, csv.Error, UnicodeError) as e:
        _add(issues, "ERROR", "CSV_READ_ERROR", str(e), name)
        return []


def _index(rows: list[dict[str, str]], field: str, register: str, issues: list[Issue], partitioned: bool = True) -> dict[tuple, dict[str, str]]:
    out: dict[tuple, dict[str, str]] = {}
    for row_no, row in enumerate(rows, start=2):
        rid = row.get(field, "")
        if not rid:
            _add(issues, "ERROR", "MISSING_ID", f"Missing {field}", register, row_no)
            continue
        key = (*_partition(row), rid) if partitioned else (rid,)
        if key in out:
            _add(issues, "ERROR", "DUPLICATE_ID", f"Duplicate {field}={rid!r} within partition", register, row_no)
        else:
            out[key] = row
    return out


def _has_ref(index: dict[tuple, dict[str, str]], row: dict[str, str], ref: str) -> bool:
    return bool(ref) and (*_partition(row), ref) in index


def _int_value(value: str, register: str, field: str, row_no: int, issues: list[Issue], allow_blank: bool = False) -> int | None:
    if value == "" and allow_blank:
        return None
    try:
        n = int(value)
        return n
    except (TypeError, ValueError):
        _add(issues, "ERROR", "INVALID_INTEGER", f"{field} must be an integer; got {value!r}", register, row_no)
        return None


def _load_a120(root: Path, issues: list[Issue]) -> tuple[set[str], str, str]:
    path = root / "vocabulary" / "A_120_ChronoCTI_Selected_Technique_IDs_derived_v0.1.json"
    if not path.exists():
        _add(issues, "ERROR", "MISSING_A120", "Pinned A_120 vocabulary file is missing", "event_mappings")
        return set(), "", ""
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    try:
        data = json.loads(raw.decode("utf-8"))
        ids = data["technique_ids"]
        if data.get("status") != "DERIVED_ID_EXTRACTION_NOT_ORIGINAL_CHRONOCTI_JSON":
            _add(issues, "ERROR", "A120_PROVENANCE_STATUS", "A_120 artifact is not labelled as a derived extraction", "event_mappings")
        if len(ids) != 120 or len(set(ids)) != 120:
            _add(issues, "ERROR", "A120_CARDINALITY", f"Expected 120 unique IDs; found {len(ids)} records / {len(set(ids))} unique", "event_mappings")
        source = data.get("source", {})
        if source.get("commit") != "4906a0a5e399b6e2aa10435fd6e3894e041e4549" or source.get("path") != "temporal-learner-code/selected_techniquesWName.json":
            _add(issues, "ERROR", "A120_SOURCE_PIN", "A_120 source commit/path differs from the pinned ChronoCTI source", "event_mappings")
        return set(ids), digest, data.get("artifact_name", "")
    except (UnicodeError, json.JSONDecodeError, KeyError, TypeError) as e:
        _add(issues, "ERROR", "A120_INVALID_JSON", str(e), "event_mappings")
        return set(), digest, ""


def _load_attack_crosswalk(
    root: Path,
    a120: set[str],
    a120_sha: str,
    issues: list[Issue],
) -> tuple[dict[str, dict[str, str]], str]:
    """Load and structurally verify the immutable Enterprise ATT&CK v12.1 crosswalk."""
    csv_path = root / "vocabulary" / "A_120_Exact_to_Parent_Crosswalk_v0.1.csv"
    manifest_path = root / "vocabulary" / "A_120_Exact_to_Parent_Crosswalk_v0.1.manifest.json"
    before = len(issues)

    if not csv_path.is_file():
        _add(issues, "ERROR", "MISSING_ATTACK_CROSSWALK", "Pinned A_120 exact-to-parent crosswalk CSV is missing", "event_mappings")
        return {}, ""
    if not manifest_path.is_file():
        _add(issues, "ERROR", "MISSING_ATTACK_CROSSWALK_MANIFEST", "Pinned ATT&CK crosswalk source manifest is missing", "event_mappings")
        return {}, ""

    try:
        csv_raw = csv_path.read_bytes()
        csv_sha = hashlib.sha256(csv_raw).hexdigest()
        if csv_sha != ATTACK_CROSSWALK_SHA256:
            _add(
                issues,
                "ERROR",
                "ATTACK_CROSSWALK_HASH_MISMATCH",
                f"Crosswalk SHA-256 mismatch: expected {ATTACK_CROSSWALK_SHA256}, got {csv_sha}",
                "event_mappings",
            )

        manifest_raw = manifest_path.read_bytes()
        manifest = json.loads(manifest_raw.decode("utf-8"))
        if not isinstance(manifest, dict):
            _add(issues, "ERROR", "ATTACK_CROSSWALK_MANIFEST_INVALID", "Crosswalk manifest root must be a JSON object", "event_mappings")
            return {}, csv_sha
        if manifest.get("artifact_version") != "v0.1":
            _add(issues, "ERROR", "ATTACK_CROSSWALK_VERSION_MISMATCH", "Crosswalk artifact version must be v0.1", "event_mappings")
        if manifest.get("status") != "GENERATED_FROM_HASH_VERIFIED_ENTERPRISE_ATTACK_V12_1":
            _add(issues, "ERROR", "ATTACK_CROSSWALK_STATUS_INVALID", "Crosswalk manifest does not record a hash-verified Enterprise ATT&CK v12.1 source", "event_mappings")
        if manifest.get("attack_release") != ATTACK_RELEASE:
            _add(issues, "ERROR", "ATTACK_CROSSWALK_RELEASE_MISMATCH", f"Crosswalk release must be {ATTACK_RELEASE!r}", "event_mappings")

        source = manifest.get("source") or {}
        if not isinstance(source, dict):
            _add(issues, "ERROR", "ATTACK_CROSSWALK_MANIFEST_INVALID", "Crosswalk source metadata must be a JSON object", "event_mappings")
            return {}, csv_sha
        expected_source = {
            "repository": "https://github.com/mitre-attack/attack-stix-data",
            "path": "enterprise-attack/enterprise-attack-12.1.json",
            "git_blob_sha1": ATTACK_SOURCE_GIT_BLOB_SHA1,
            "sha256": ATTACK_SOURCE_SHA256,
            "size_bytes": ATTACK_SOURCE_SIZE_BYTES,
        }
        for field, expected in expected_source.items():
            if source.get(field) != expected:
                _add(
                    issues,
                    "ERROR",
                    "ATTACK_CROSSWALK_SOURCE_PIN_MISMATCH",
                    f"Crosswalk source {field} must equal {expected!r}; got {source.get(field)!r}",
                    "event_mappings",
                )

        a120_meta = manifest.get("a120") or {}
        if not isinstance(a120_meta, dict):
            _add(issues, "ERROR", "ATTACK_CROSSWALK_MANIFEST_INVALID", "Crosswalk A_120 metadata must be a JSON object", "event_mappings")
            return {}, csv_sha
        if (
            a120_meta.get("path")
            != "research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/"
            "vocabulary/A_120_ChronoCTI_Selected_Technique_IDs_derived_v0.1.json"
            or a120_meta.get("sha256") != a120_sha
            or a120_meta.get("record_count") != 120
        ):
            _add(issues, "ERROR", "ATTACK_CROSSWALK_A120_PIN_MISMATCH", "Crosswalk manifest does not identify the pinned 120-ID A_120 artifact", "event_mappings")

        output_meta = manifest.get("output") or {}
        if not isinstance(output_meta, dict):
            _add(issues, "ERROR", "ATTACK_CROSSWALK_MANIFEST_INVALID", "Crosswalk output metadata must be a JSON object", "event_mappings")
            return {}, csv_sha
        expected_output_path = (
            "research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/"
            "vocabulary/A_120_Exact_to_Parent_Crosswalk_v0.1.csv"
        )
        if (
            output_meta.get("path") != expected_output_path
            or output_meta.get("sha256") != csv_sha
            or output_meta.get("sha256") != ATTACK_CROSSWALK_SHA256
        ):
            _add(issues, "ERROR", "ATTACK_CROSSWALK_OUTPUT_MANIFEST_MISMATCH", "Crosswalk output path or SHA-256 does not match its pinned artifact", "event_mappings")

        generation = manifest.get("generation") or {}
        if not isinstance(generation, dict):
            _add(issues, "ERROR", "ATTACK_CROSSWALK_MANIFEST_INVALID", "Crosswalk generation metadata must be a JSON object", "event_mappings")
            return {}, csv_sha
        if generation.get("script") != "scripts/build_attack_crosswalk.py":
            _add(issues, "ERROR", "ATTACK_CROSSWALK_GENERATOR_MISMATCH", "Crosswalk generation script path is not the pinned builder", "event_mappings")
        if generation.get("record_count") != 737:
            _add(issues, "ERROR", "ATTACK_CROSSWALK_MANIFEST_COUNT_MISMATCH", "Crosswalk manifest must record 737 exact technique rows", "event_mappings")

        import io

        reader = csv.DictReader(io.StringIO(csv_raw.decode("utf-8"), newline=""))
        if reader.fieldnames != ATTACK_CROSSWALK_HEADERS:
            _add(issues, "ERROR", "ATTACK_CROSSWALK_HEADER_MISMATCH", "Crosswalk CSV header does not match the pinned schema", "event_mappings")
            return {}, csv_sha
        rows = list(reader)
    except (OSError, UnicodeError, csv.Error, json.JSONDecodeError, TypeError) as exc:
        _add(issues, "ERROR", "ATTACK_CROSSWALK_READ_ERROR", str(exc), "event_mappings")
        return {}, ""

    by_exact: dict[str, dict[str, str]] = {}
    by_stix: dict[str, dict[str, str]] = {}
    for row_no, row in enumerate(rows, start=2):
        exact_id = row.get("exact_technique_id", "")
        stix_id = row.get("stix_object_id", "")
        if not re.fullmatch(r"T\d{4}(?:\.\d{3})?", exact_id):
            _add(issues, "ERROR", "ATTACK_CROSSWALK_INVALID_EXACT_ID", f"Invalid exact technique ID {exact_id!r}", "event_mappings", row_no)
            continue
        if exact_id in by_exact:
            _add(issues, "ERROR", "ATTACK_CROSSWALK_DUPLICATE_EXACT_ID", f"Duplicate exact technique ID {exact_id!r}", "event_mappings", row_no)
            continue
        if not stix_id.startswith("attack-pattern--") or stix_id in by_stix:
            _add(issues, "ERROR", "ATTACK_CROSSWALK_DUPLICATE_OR_INVALID_STIX_ID", f"Duplicate or invalid STIX attack-pattern ID {stix_id!r}", "event_mappings", row_no)
            continue
        if row.get("attack_release") != ATTACK_RELEASE:
            _add(issues, "ERROR", "ATTACK_CROSSWALK_ROW_RELEASE_MISMATCH", f"Row release for {exact_id} is not {ATTACK_RELEASE!r}", "event_mappings", row_no)
        if row.get("is_subtechnique") not in {"true", "false"}:
            _add(issues, "ERROR", "ATTACK_CROSSWALK_INVALID_SUBTECHNIQUE_FLAG", f"Invalid is_subtechnique for {exact_id}", "event_mappings", row_no)
        for field in ("parent_in_A_120", "revoked", "deprecated"):
            if row.get(field) not in {"true", "false"}:
                _add(issues, "ERROR", "ATTACK_CROSSWALK_INVALID_BOOLEAN", f"Invalid {field} flag for {exact_id}", "event_mappings", row_no)
        if not row.get("exact_technique_name") or not row.get("parent_technique_id") or not row.get("parent_technique_name"):
            _add(issues, "ERROR", "ATTACK_CROSSWALK_INCOMPLETE_ROW", f"Crosswalk row for {exact_id} is missing a name or parent identifier", "event_mappings", row_no)
        by_exact[exact_id] = row
        by_stix[stix_id] = row

    top_level_count = sum(row.get("is_subtechnique") == "false" for row in by_exact.values())
    subtechnique_count = sum(row.get("is_subtechnique") == "true" for row in by_exact.values())
    relationship_count = sum(row.get("relationship_type") == "subtechnique-of" for row in by_exact.values())
    a120_found = sum(exact_id in by_exact for exact_id in a120)
    a120_top_level = sum(
        exact_id in by_exact and by_exact[exact_id].get("is_subtechnique") == "false"
        for exact_id in a120
    )

    for exact_id, row in by_exact.items():
        parent_id = row.get("parent_technique_id", "")
        parent_in_a120 = parent_id in a120
        if row.get("parent_in_A_120") != str(parent_in_a120).lower():
            _add(issues, "ERROR", "ATTACK_CROSSWALK_A120_FLAG_MISMATCH", f"parent_in_A_120 is inconsistent for {exact_id}", "event_mappings")
        if row.get("is_subtechnique") == "false":
            if (
                parent_id != exact_id
                or row.get("parent_technique_name") != row.get("exact_technique_name")
                or row.get("relationship_type") != "self"
                or row.get("relationship_source_object_id") != row.get("stix_object_id")
                or row.get("relationship_target_object_id") != row.get("stix_object_id")
            ):
                _add(issues, "ERROR", "ATTACK_CROSSWALK_TOP_LEVEL_PARENT_MISMATCH", f"Top-level technique {exact_id} does not map to itself", "event_mappings")
        elif row.get("is_subtechnique") == "true":
            parent_stix = row.get("relationship_target_object_id", "")
            parent_row = by_stix.get(parent_stix)
            if (
                row.get("relationship_type") != "subtechnique-of"
                or row.get("relationship_source_object_id") != row.get("stix_object_id")
                or parent_row is None
                or parent_row.get("is_subtechnique") != "false"
                or parent_row.get("exact_technique_id") != parent_id
                or parent_row.get("exact_technique_name") != row.get("parent_technique_name")
            ):
                _add(issues, "ERROR", "ATTACK_CROSSWALK_EXPLICIT_PARENT_MISMATCH", f"Sub-technique {exact_id} does not resolve to its explicit top-level STIX parent", "event_mappings")

    actual_counts = {
        "attack_pattern_objects": len(by_exact),
        "unique_exact_technique_ids": len(by_exact),
        "top_level_techniques": top_level_count,
        "sub_techniques": subtechnique_count,
        "subtechnique_of_relationships": relationship_count,
        "A_120_ids_found": a120_found,
        "A_120_ids_top_level": a120_top_level,
    }
    expected_counts = {
        "attack_pattern_objects": 737,
        "unique_exact_technique_ids": 737,
        "top_level_techniques": 333,
        "sub_techniques": 404,
        "subtechnique_of_relationships": 404,
        "A_120_ids_found": 120,
        "A_120_ids_top_level": 120,
    }
    manifest_counts = (manifest.get("generation") or {}).get("counts") or {}
    if not isinstance(manifest_counts, dict):
        _add(issues, "ERROR", "ATTACK_CROSSWALK_MANIFEST_INVALID", "Crosswalk generation counts must be a JSON object", "event_mappings")
        return {}, csv_sha
    if actual_counts != expected_counts or any(manifest_counts.get(k) != v for k, v in expected_counts.items()):
        _add(issues, "ERROR", "ATTACK_CROSSWALK_COUNT_MISMATCH", f"Crosswalk counts differ from pinned release expectations: {actual_counts}", "event_mappings")

    for exact_id in a120:
        row = by_exact.get(exact_id)
        if (
            row is None
            or row.get("is_subtechnique") != "false"
            or row.get("revoked") != "false"
            or row.get("deprecated") != "false"
        ):
            _add(issues, "ERROR", "ATTACK_CROSSWALK_A120_INVALID_MEMBER", f"A_120 member {exact_id} is missing, sub-technique, revoked or deprecated in the pinned release", "event_mappings")

    if any(item.severity == "ERROR" for item in issues[before:]):
        return {}, csv_sha
    return by_exact, csv_sha


def validate_bundle(
    bundle_root: str | Path,
    source_texts: dict[tuple[str, str, str], str] | None = None,
) -> ValidationReport:
    root = Path(bundle_root)
    issues: list[Issue] = []
    source_texts = source_texts or {}
    tables = {name: _read_table(root, name, issues) for name in HEADERS}
    rows_by_register = {k: len(v) for k, v in tables.items()}
    a120, a120_sha, a120_name = _load_a120(root, issues)
    attack_crosswalk, attack_crosswalk_sha = _load_attack_crosswalk(root, a120, a120_sha, issues)

    # Partition and primary-key checks.
    if tables["report_registry"]:
        reg_index: dict[tuple[str, str, str], dict[str, str]] = {}
        for i, r in enumerate(tables["report_registry"], 2):
            part = _partition(r)
            if not all(part):
                _add(issues, "ERROR", "MISSING_PARTITION_KEY", "report_id, annotator_id and annotation_pass_id are required", "report_registry", i)
            if part in reg_index:
                _add(issues, "ERROR", "DUPLICATE_REPORT_PASS", f"Duplicate report registry partition {part}", "report_registry", i)
            reg_index[part] = r
            if r.get("source_scope_eligibility") not in ELIGIBILITY:
                _add(issues, "ERROR", "INVALID_SCOPE_ELIGIBILITY", f"Invalid source_scope_eligibility {r.get('source_scope_eligibility')!r}", "report_registry", i)
            if r.get("local_research_use_status") not in LOCAL_USE:
                _add(issues, "ERROR", "INVALID_LOCAL_USE", f"Invalid local_research_use_status {r.get('local_research_use_status')!r}", "report_registry", i)
            if r.get("public_reuse_status") not in PUBLIC_REUSE:
                _add(issues, "ERROR", "INVALID_PUBLIC_REUSE", f"Invalid public_reuse_status {r.get('public_reuse_status')!r}", "report_registry", i)
            if r.get("report_assessability") not in ASSESSABILITY:
                _add(issues, "ERROR", "INVALID_ASSESSABILITY", f"Invalid report_assessability {r.get('report_assessability')!r}", "report_registry", i)
            if r.get("full_report_review_status") not in FULL_REVIEW:
                _add(issues, "ERROR", "INVALID_REVIEW_STATUS", f"Invalid full_report_review_status {r.get('full_report_review_status')!r}", "report_registry", i)
            if r.get("prior_exposure_status") not in PRIOR_EXPOSURE:
                _add(issues, "ERROR", "INVALID_PRIOR_EXPOSURE_STATUS", f"Invalid prior_exposure_status {r.get('prior_exposure_status')!r}", "report_registry", i)
            if not re.fullmatch(r"[0-9a-fA-F]{64}", r.get("source_text_sha256", "")):
                _add(issues, "ERROR", "INVALID_SOURCE_HASH", "source_text_sha256 must be a 64-character SHA-256 hex digest", "report_registry", i)
            count = _int_value(r.get("source_text_char_count", ""), "report_registry", "source_text_char_count", i, issues)
            key = part
            if key in source_texts:
                text = source_texts[key]
                actual_hash = frozen_source_sha256(text)
                if r.get("source_text_sha256", "").lower() != actual_hash:
                    _add(issues, "ERROR", "SOURCE_HASH_MISMATCH", "Frozen source text SHA-256 does not match report registry", "report_registry", i)
                if count is not None and count != len(text):
                    _add(issues, "ERROR", "SOURCE_CHAR_COUNT_MISMATCH", f"Expected {len(text)} characters, found {count}", "report_registry", i)
            else:
                _add(issues, "WARNING", "SOURCE_TEXT_NOT_SUPPLIED", "Source text not supplied; text hash and exact offsets cannot be fully verified", "report_registry", i)

    reg_partitions = {_partition(r) for r in tables["report_registry"]}
    for name, rows in tables.items():
        if name == "report_registry":
            continue
        for i, row in enumerate(rows, 2):
            part = _partition(row)
            if not all(part):
                if name == "adjudication_log":
                    message = "report_id, target_annotator_id and annotation_pass_id are required"
                else:
                    message = "report_id, annotator_id and annotation_pass_id are required"
                _add(issues, "ERROR", "MISSING_PARTITION_KEY", message, name, i)
            elif part not in reg_partitions:
                _add(issues, "ERROR", "UNKNOWN_REPORT_PARTITION", f"No report_registry row for partition {part}", name, i)

    # Build indexes in partition scope.
    id_fields = {
        "report_scopes": "scope_id", "activity_units": "activity_unit_id", "event_mentions": "mention_id",
        "evidence_spans": "evidence_span_id", "record_evidence_links": "link_id", "event_mappings": "mapping_id",
        "time_evidence": "time_evidence_id", "temporal_relations": "relation_id",
        "candidate_pair_assessments": "assessment_id", "non_temporal_relations": "non_temporal_relation_id"
    }
    indexes = {name: _index(tables[name], field, name, issues) for name, field in id_fields.items()}
    # report_registry is keyed by its full report/annotator/pass partition; it is
    # also addressable from evidence links using report_id as the record ID.
    indexes["report_registry"] = _index(tables["report_registry"], "report_id", "report_registry", issues)
    indexes["adjudication_log"] = _index(tables["adjudication_log"], "adjudication_id", "adjudication_log", issues)

    # Evidence spans: offsets, source hash, exact source substring when text supplied.
    evidence_index = indexes["evidence_spans"]
    for i, r in enumerate(tables["evidence_spans"], 2):
        start = _int_value(r.get("char_start", ""), "evidence_spans", "char_start", i, issues)
        end = _int_value(r.get("char_end", ""), "evidence_spans", "char_end", i, issues)
        if start is not None and end is not None and (start < 0 or end <= start):
            _add(issues, "ERROR", "INVALID_OFFSETS", f"Expected 0 <= char_start < char_end; got {start}, {end}", "evidence_spans", i)
        reg = next((x for x in tables["report_registry"] if _partition(x) == _partition(r)), None)
        if reg and r.get("source_text_sha256", "").lower() != reg.get("source_text_sha256", "").lower():
            _add(issues, "ERROR", "SPAN_SOURCE_HASH_MISMATCH", "Evidence span hash differs from report registry", "evidence_spans", i)
        if _partition(r) in source_texts and start is not None and end is not None:
            text = source_texts[_partition(r)]
            if end > len(text):
                _add(issues, "ERROR", "OFFSET_OUT_OF_RANGE", f"char_end {end} exceeds source length {len(text)}", "evidence_spans", i)
            elif text[start:end] != r.get("evidence_text", ""):
                _add(issues, "ERROR", "EVIDENCE_TEXT_MISMATCH", "evidence_text is not the exact frozen source substring", "evidence_spans", i)

    # Scope hierarchy.
    scopes = indexes["report_scopes"]
    for i, r in enumerate(tables["report_scopes"], 2):
        if r.get("scope_status") not in {"RESOLVED", "PROVISIONAL", "UNRESOLVED"}:
            _add(issues, "ERROR", "INVALID_SCOPE_STATUS", f"Invalid scope_status {r.get('scope_status')!r}", "report_scopes", i)
        if r.get("scope_confidence") not in CONFIDENCE:
            _add(issues, "ERROR", "INVALID_CONFIDENCE", f"Invalid scope_confidence {r.get('scope_confidence')!r}", "report_scopes", i)
        if r.get("scope_type") not in {"INCIDENT", "CAMPAIGN", "ACTOR_OPERATION", "VICTIM_ORGANISATION", "HOST", "REPORT_AGGREGATE", "OTHER", "UNRESOLVED"}:
            _add(issues, "ERROR", "INVALID_SCOPE_TYPE", f"Invalid scope_type {r.get('scope_type')!r}", "report_scopes", i)
        parent = r.get("parent_scope_id", "")
        if parent and not _has_ref(scopes, r, parent):
            _add(issues, "ERROR", "UNKNOWN_PARENT_SCOPE", f"Unknown parent_scope_id {parent!r}", "report_scopes", i)
    for i, r in enumerate(tables["report_scopes"], 2):
        seen = {r.get("scope_id", "")}
        parent_id = r.get("parent_scope_id", "")
        while parent_id:
            if parent_id in seen:
                _add(issues, "ERROR", "SCOPE_HIERARCHY_CYCLE", f"Parent chain for {r.get('scope_id')!r} contains a cycle", "report_scopes", i)
                break
            seen.add(parent_id)
            parent_row = scopes.get((*_partition(r), parent_id))
            if not parent_row:
                break
            parent_id = parent_row.get("parent_scope_id", "")

    # Activity unit structure, count semantics and parent references.
    units = indexes["activity_units"]
    expected_granularity = {
        "event_leaf": "atomic_event", "series_container": "repeated_event_series",
        "episode_container": "activity_episode", "aggregate_container": "report_level_aggregate",
        "unresolved_unit": "unresolved"
    }
    for i, r in enumerate(tables["activity_units"], 2):
        role, gran, status = r.get("unit_role"), r.get("granularity"), r.get("instance_status")
        if role not in UNIT_ROLES:
            _add(issues, "ERROR", "INVALID_UNIT_ROLE", f"Invalid unit_role {role!r}", "activity_units", i)
        if gran not in GRANULARITIES:
            _add(issues, "ERROR", "INVALID_GRANULARITY", f"Invalid granularity {gran!r}", "activity_units", i)
        if status not in INSTANCE_STATUSES:
            _add(issues, "ERROR", "INVALID_INSTANCE_STATUS", f"Invalid instance_status {status!r}", "activity_units", i)
        if role in expected_granularity and gran != expected_granularity[role]:
            _add(issues, "ERROR", "ROLE_GRANULARITY_MISMATCH", f"{role} requires {expected_granularity[role]}, got {gran}", "activity_units", i)
        if role == "event_leaf" and status != "RESOLVED":
            _add(issues, "ERROR", "EVENT_LEAF_NOT_RESOLVED", "event_leaf must have instance_status=RESOLVED", "activity_units", i)
        if role == "event_leaf" and status == "GENERIC_BEHAVIOUR":
            _add(issues, "ERROR", "GENERIC_AS_EVENT_LEAF", "GENERIC_BEHAVIOUR cannot be a primary event leaf", "activity_units", i)
        if status == "GENERIC_BEHAVIOUR" and role == "event_leaf":
            _add(issues, "ERROR", "GENERIC_AS_EVENT_LEAF", "Generic behaviour cannot be a primary event leaf", "activity_units", i)
        if not r.get("scope_id"):
            _add(issues, "ERROR", "UNIT_SCOPE_MISSING", "Every activity unit must reference a report-local scope", "activity_units", i)
        elif not _has_ref(scopes, r, r["scope_id"]):
            _add(issues, "ERROR", "UNKNOWN_UNIT_SCOPE", f"Unknown scope_id {r['scope_id']!r}", "activity_units", i)
        parent = r.get("parent_activity_unit_id", "")
        if parent and not _has_ref(units, r, parent):
            _add(issues, "ERROR", "UNKNOWN_PARENT_UNIT", f"Unknown parent_activity_unit_id {parent!r}", "activity_units", i)
        cs = r.get("count_status")
        if cs not in COUNT_STATUSES:
            _add(issues, "ERROR", "INVALID_COUNT_STATUS", f"Invalid count_status {cs!r}", "activity_units", i)
        numeric = {k: _int_value(r.get(k, ""), "activity_units", k, i, issues, allow_blank=True) for k in ("count_exact", "count_min", "count_max")}
        if cs == "exact" and (numeric["count_exact"] is None or numeric["count_min"] is not None or numeric["count_max"] is not None):
            _add(issues, "ERROR", "COUNT_EXACT_FIELDS", "count_status=exact requires count_exact only", "activity_units", i)
        if cs == "minimum" and (numeric["count_min"] is None or numeric["count_exact"] is not None or numeric["count_max"] is not None):
            _add(issues, "ERROR", "COUNT_MINIMUM_FIELDS", "count_status=minimum requires count_min only", "activity_units", i)
        if cs == "range" and (numeric["count_min"] is None or numeric["count_max"] is None or numeric["count_exact"] is not None):
            _add(issues, "ERROR", "COUNT_RANGE_FIELDS", "count_status=range requires count_min and count_max", "activity_units", i)
        if cs in {"qualitative_only", "unknown"} and any(v is not None for v in numeric.values()):
            _add(issues, "ERROR", "COUNT_UNEXPECTED_NUMERIC", f"count_status={cs} must not include numeric count values", "activity_units", i)
        if cs == "qualitative_only" and not r.get("count_qualitative"):
            _add(issues, "ERROR", "COUNT_QUALITATIVE_MISSING", "count_status=qualitative_only requires count_qualitative", "activity_units", i)
        if cs != "qualitative_only" and r.get("count_qualitative"):
            _add(issues, "ERROR", "COUNT_QUALITATIVE_UNEXPECTED", "count_qualitative is only allowed with count_status=qualitative_only", "activity_units", i)
        if any(v is not None and v < 0 for v in numeric.values()):
            _add(issues, "ERROR", "NEGATIVE_COUNT", "Count values cannot be negative", "activity_units", i)
        if numeric["count_min"] is not None and numeric["count_max"] is not None and numeric["count_min"] > numeric["count_max"]:
            _add(issues, "ERROR", "COUNT_BOUNDS_INVERTED", "count_min cannot exceed count_max", "activity_units", i)

    # Check that unit-parent chains are acyclic within each annotation partition.
    for i, r in enumerate(tables["activity_units"], 2):
        seen = {r.get("activity_unit_id", "")}
        parent_id = r.get("parent_activity_unit_id", "")
        while parent_id:
            if parent_id in seen:
                _add(issues, "ERROR", "ACTIVITY_UNIT_HIERARCHY_CYCLE", f"Parent chain for {r.get('activity_unit_id')!r} contains a cycle", "activity_units", i)
                break
            seen.add(parent_id)
            parent_row = units.get((*_partition(r), parent_id))
            if not parent_row:
                break
            parent_id = parent_row.get("parent_activity_unit_id", "")

    # Mention links and unit status relationship.
    for i, r in enumerate(tables["event_mentions"], 2):
        if not _has_ref(units, r, r.get("activity_unit_id", "")):
            _add(issues, "ERROR", "UNKNOWN_MENTION_UNIT", f"Unknown activity_unit_id {r.get('activity_unit_id')!r}", "event_mentions", i)
        if not _has_ref(evidence_index, r, r.get("primary_evidence_span_id", "")):
            _add(issues, "ERROR", "UNKNOWN_MENTION_EVIDENCE", f"Unknown primary_evidence_span_id {r.get('primary_evidence_span_id')!r}", "event_mentions", i)
        if r.get("instance_status") not in INSTANCE_STATUSES:
            _add(issues, "ERROR", "INVALID_MENTION_STATUS", f"Invalid mention instance_status {r.get('instance_status')!r}", "event_mentions", i)
        unit = units.get((*_partition(r), r.get("activity_unit_id", "")))
        resolved_id = r.get("resolved_event_instance_id", "")
        if resolved_id:
            if resolved_id != r.get("activity_unit_id"):
                _add(issues, "ERROR", "EVENT_ID_NOT_UNIT_ID", "resolved_event_instance_id must equal activity_unit_id for event leaves", "event_mentions", i)
            if not unit or unit.get("unit_role") != "event_leaf" or unit.get("granularity") != "atomic_event" or unit.get("instance_status") != "RESOLVED":
                _add(issues, "ERROR", "MENTION_EVENT_ID_NONLEAF", "resolved_event_instance_id can only reference a resolved atomic event_leaf", "event_mentions", i)
        if unit and r.get("instance_status") != unit.get("instance_status") and not r.get("mention_unit_status_note"):
            _add(issues, "ERROR", "MENTION_UNIT_STATUS_MISMATCH", "Mention/unit instance_status differs; provide mention_unit_status_note", "event_mentions", i)

    # Event mappings: exact-to-parent mapping is checked against the pinned v12.1 STIX crosswalk.
    accepted_a120 = 0
    for i, r in enumerate(tables["event_mappings"], 2):
        unit_id = r.get("activity_unit_id", "")
        if not _has_ref(units, r, unit_id):
            _add(issues, "ERROR", "UNKNOWN_MAPPING_UNIT", f"Unknown activity_unit_id {unit_id!r}", "event_mappings", i)
        basis, decision = r.get("mapping_basis"), r.get("mapping_decision_status")
        if basis not in MAPPING_BASES:
            _add(issues, "ERROR", "INVALID_MAPPING_BASIS", f"Invalid mapping_basis {basis!r}", "event_mappings", i)
        if decision not in MAPPING_DECISIONS:
            _add(issues, "ERROR", "INVALID_MAPPING_DECISION", f"Invalid mapping_decision_status {decision!r}", "event_mappings", i)
        if decision == "ACCEPTED" and basis in {"workbook_only", "unresolved"}:
            _add(issues, "ERROR", "UNSUPPORTED_ACCEPTED_MAPPING", f"Accepted mapping cannot use mapping_basis={basis}", "event_mappings", i)
        if decision == "ACCEPTED" and not r.get("exact_technique_id"):
            _add(issues, "ERROR", "ACCEPTED_MAPPING_NO_TECHNIQUE", "Accepted mapping requires exact_technique_id", "event_mappings", i)

        exact_id = r.get("exact_technique_id", "")
        parent_id = r.get("baseline_parent_technique_id", "")
        status = r.get("baseline_mapping_status")
        exact_row = attack_crosswalk.get(exact_id)

        if decision == "ACCEPTED":
            if r.get("attack_version") != ATTACK_RELEASE:
                _add(issues, "ERROR", "ATTACK_VERSION_MISMATCH", f"Accepted primary mapping must use {ATTACK_RELEASE!r}", "event_mappings", i)
            if not re.fullmatch(r"T\d{4}(?:\.\d{3})?", exact_id):
                _add(issues, "ERROR", "INVALID_EXACT_TECHNIQUE_ID", f"Invalid exact ATT&CK technique ID {exact_id!r}", "event_mappings", i)
            if exact_row is None:
                _add(issues, "ERROR", "EXACT_TECHNIQUE_NOT_IN_PINNED_RELEASE", f"Exact technique {exact_id!r} is not present in the pinned {ATTACK_RELEASE} crosswalk", "event_mappings", i)
            else:
                if r.get("exact_technique_name") != exact_row.get("exact_technique_name"):
                    _add(
                        issues,
                        "ERROR",
                        "EXACT_TECHNIQUE_NAME_MISMATCH",
                        f"Exact technique name for {exact_id} does not match the pinned {ATTACK_RELEASE} name",
                        "event_mappings",
                        i,
                    )
                if (
                    exact_row.get("is_subtechnique") == "false"
                    and parent_id != exact_id
                ):
                    _add(
                        issues,
                        "ERROR",
                        "TOP_LEVEL_PARENT_MISMATCH",
                        "A top-level technique must map to itself as its parent",
                        "event_mappings",
                        i,
                    )
                elif parent_id != exact_row.get("parent_technique_id"):
                    _add(
                        issues,
                        "ERROR",
                        "EXACT_PARENT_MISMATCH",
                        f"Exact technique {exact_id} maps to {exact_row.get('parent_technique_id')!r} in the pinned STIX crosswalk, not {parent_id!r}",
                        "event_mappings",
                        i,
                    )
                if exact_row.get("revoked") == "true" or exact_row.get("deprecated") == "true":
                    if status == "IN_VOCAB":
                        _add(
                            issues,
                            "ERROR",
                            "LIFECYCLE_FLAGGED_PRIMARY_MAPPING",
                            f"Exact technique {exact_id} is revoked or deprecated in {ATTACK_RELEASE}; retain it in A_exact but do not count it in primary A_120 without separate resolution",
                            "event_mappings",
                            i,
                        )
                if status == "IN_VOCAB" and exact_row.get("parent_in_A_120") != "true":
                    _add(issues, "ERROR", "A120_STATUS_CONTRADICTION", f"Exact technique {exact_id} resolves outside A_120 but is marked IN_VOCAB", "event_mappings", i)
                if status == "OUT_OF_VOCAB" and exact_row.get("parent_in_A_120") == "true":
                    _add(issues, "ERROR", "A120_STATUS_CONTRADICTION", f"Exact technique {exact_id} resolves inside A_120 but is marked OUT_OF_VOCAB", "event_mappings", i)
                if status == "IN_VOCAB" and parent_id not in a120:
                    _add(issues, "ERROR", "A120_MEMBERSHIP_FAILURE", f"baseline_parent_technique_id {parent_id!r} is not in pinned A_120", "event_mappings", i)
                if status == "OUT_OF_VOCAB" and parent_id in a120:
                    _add(issues, "ERROR", "A120_STATUS_CONTRADICTION", "Technique is in A_120 but baseline_mapping_status says OUT_OF_VOCAB", "event_mappings", i)

        if r.get("event_instance_id") and r.get("event_instance_id") != unit_id:
            _add(issues, "ERROR", "MAPPING_EVENT_ID_NOT_UNIT_ID", "event_instance_id must equal activity_unit_id for resolved event leaves", "event_mappings", i)
        if status not in BASELINE_MAPPING_STATUSES:
            _add(issues, "ERROR", "INVALID_BASELINE_MAPPING_STATUS", f"Invalid baseline_mapping_status {status!r}", "event_mappings", i)

        if status == "IN_VOCAB":
            technique = parent_id
            if not technique or technique not in a120:
                _add(issues, "ERROR", "A120_MEMBERSHIP_FAILURE", f"baseline_parent_technique_id {technique!r} is not in pinned A_120", "event_mappings", i)
            if r.get("baseline_vocabulary_sha256", "").lower() != a120_sha:
                _add(issues, "ERROR", "A120_HASH_MISMATCH", "baseline_vocabulary_sha256 differs from pinned local A_120 artifact", "event_mappings", i)
            if r.get("baseline_vocabulary_id") != a120_name:
                _add(issues, "ERROR", "A120_ID_MISMATCH", f"baseline_vocabulary_id must equal pinned artifact name {a120_name!r}", "event_mappings", i)
            mapped_unit = units.get((*_partition(r), unit_id))
            if (
                decision == "ACCEPTED"
                and basis not in {"workbook_only", "unresolved"}
                and exact_row is not None
                and exact_row.get("parent_in_A_120") == "true"
                and exact_row.get("revoked") == "false"
                and exact_row.get("deprecated") == "false"
                and technique in a120
                and mapped_unit
                and mapped_unit.get("unit_role") == "event_leaf"
                and mapped_unit.get("granularity") == "atomic_event"
                and mapped_unit.get("instance_status") == "RESOLVED"
            ):
                accepted_a120 += 1

    # Time evidence.
    time_types = {"ATTACK_OCCURRENCE", "ATTACK_PERIOD", "DETECTION", "DISCOVERY", "SAMPLE_UPLOAD", "SAMPLE_COMPILATION", "PUBLICATION", "REPORT_RETRIEVAL", "OTHER", "UNKNOWN"}
    time_precisions = {"YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND", "INTERVAL", "QUALITATIVE", "UNKNOWN"}
    for i, r in enumerate(tables["time_evidence"], 2):
        if not r.get("activity_unit_id") and not r.get("mention_id"):
            _add(issues, "ERROR", "TIME_WITHOUT_TARGET", "time_evidence must reference an activity unit or mention", "time_evidence", i)
        if r.get("activity_unit_id") and not _has_ref(units, r, r.get("activity_unit_id")):
            _add(issues, "ERROR", "UNKNOWN_TIME_UNIT", f"Unknown activity_unit_id {r.get('activity_unit_id')!r}", "time_evidence", i)
        if r.get("mention_id") and not _has_ref(indexes["event_mentions"], r, r.get("mention_id")):
            _add(issues, "ERROR", "UNKNOWN_TIME_MENTION", f"Unknown mention_id {r.get('mention_id')!r}", "time_evidence", i)
        if r.get("time_type") not in time_types:
            _add(issues, "ERROR", "INVALID_TIME_TYPE", f"Invalid time_type {r.get('time_type')!r}", "time_evidence", i)
        if r.get("time_precision") not in time_precisions:
            _add(issues, "ERROR", "INVALID_TIME_PRECISION", f"Invalid time_precision {r.get('time_precision')!r}", "time_evidence", i)
        if r.get("timezone_status") not in {"EXPLICIT", "INFERRED", "UNKNOWN", "NOT_APPLICABLE"}:
            _add(issues, "ERROR", "INVALID_TIMEZONE_STATUS", f"Invalid timezone_status {r.get('timezone_status')!r}", "time_evidence", i)
        if r.get("normalization_status") not in {"NORMALIZED", "PARTIALLY_NORMALIZED", "NOT_NORMALIZABLE", "UNRESOLVED"}:
            _add(issues, "ERROR", "INVALID_NORMALIZATION_STATUS", f"Invalid normalization_status {r.get('normalization_status')!r}", "time_evidence", i)
        if not r.get("raw_time_text"):
            _add(issues, "ERROR", "RAW_TIME_MISSING", "raw_time_text must be preserved", "time_evidence", i)
        if not r.get("primary_evidence_span_id"):
            _add(issues, "ERROR", "TIME_EVIDENCE_SPAN_MISSING", "Every time_evidence row requires a primary source evidence span", "time_evidence", i)
        elif not _has_ref(evidence_index, r, r.get("primary_evidence_span_id")):
            _add(issues, "ERROR", "UNKNOWN_TIME_EVIDENCE", f"Unknown primary_evidence_span_id {r.get('primary_evidence_span_id')!r}", "time_evidence", i)
        if r.get("normalization_status") == "NORMALIZED" and (not r.get("normalized_start") or not r.get("normalized_end")):
            _add(issues, "ERROR", "NORMALIZED_TIME_BOUNDS_MISSING", "NORMALIZED time requires normalized_start and normalized_end", "time_evidence", i)

    # Scope helpers: activity units may be attached to a child scope while the
    # temporal relation names a compatible parent comparison scope.
    scope_index = indexes["report_scopes"]

    def _scope_within_partition(partition: tuple[str, str, str], child_scope: str, ancestor_scope: str) -> bool:
        if not child_scope or not ancestor_scope:
            return False
        current = child_scope
        visited: set[str] = set()
        while current and current not in visited:
            if current == ancestor_scope:
                return True
            visited.add(current)
            scope_row = scope_index.get((*partition, current))
            if not scope_row:
                return False
            current = scope_row.get("parent_scope_id", "")
        return False

    # Temporal relations and positive edge eligibility. Pair-level invariants
    # use canonical event-pair semantics: AFTER(A,B) is the same precedence
    # as BEFORE(B,A); symmetric labels use unordered pairs.
    primary_edges = 0
    temporal_pair_signatures: dict[tuple[tuple[str, str, str], tuple[str, str]], dict[tuple, int]] = {}
    time_rows_by_unit: dict[tuple[str, str, str, str], list[dict[str, str]]] = {}
    for time_row in tables["time_evidence"]:
        if time_row.get("activity_unit_id"):
            key = (*_partition(time_row), time_row["activity_unit_id"])
            time_rows_by_unit.setdefault(key, []).append(time_row)
        elif time_row.get("mention_id"):
            mention = indexes["event_mentions"].get((*_partition(time_row), time_row["mention_id"]))
            if mention and mention.get("activity_unit_id"):
                key = (*_partition(time_row), mention["activity_unit_id"])
                time_rows_by_unit.setdefault(key, []).append(time_row)

    for i, r in enumerate(tables["temporal_relations"], 2):
        a, b = r.get("event_a_id", ""), r.get("event_b_id", "")
        if not _has_ref(units, r, a):
            _add(issues, "ERROR", "UNKNOWN_RELATION_ENDPOINT", f"Unknown event_a_id {a!r}", "temporal_relations", i)
        if not _has_ref(units, r, b):
            _add(issues, "ERROR", "UNKNOWN_RELATION_ENDPOINT", f"Unknown event_b_id {b!r}", "temporal_relations", i)
        if a and b and a == b:
            _add(issues, "ERROR", "SELF_EVENT_RELATION", "Temporal relation endpoints must be distinct", "temporal_relations", i)
        label, basis = r.get("relation_label"), r.get("relation_basis")
        if label not in TEMPORAL_LABELS:
            _add(issues, "ERROR", "INVALID_RELATION_LABEL", f"Invalid relation_label {label!r}", "temporal_relations", i)
        if label == "NO_TEMPORAL_CLAIM":
            _add(issues, "ERROR", "NO_TEMPORAL_CLAIM_WRONG_REGISTER", "NO_TEMPORAL_CLAIM belongs in candidate_pair_assessments, not temporal_relations", "temporal_relations", i)
        if label in POSITIVE_TEMPORAL_LABELS and basis in DIRECT_RELATION_BASES and a and b and a != b:
            unordered_pair = tuple(sorted((a, b)))
            if label == "BEFORE":
                signature = ("STRICT_ORDER", a, b)
            elif label == "AFTER":
                signature = ("STRICT_ORDER", b, a)
            else:
                signature = (label, unordered_pair[0], unordered_pair[1])
            partition_pair = (_partition(r), unordered_pair)
            prior = temporal_pair_signatures.setdefault(partition_pair, {})
            if signature in prior:
                _add(issues, "ERROR", "DUPLICATE_TEMPORAL_RELATION", f"Temporal relation duplicates normalized pair claim from row {prior[signature]}", "temporal_relations", i)
            elif prior:
                _add(issues, "ERROR", "CONTRADICTORY_TEMPORAL_RELATION", "The same event pair has multiple incompatible temporal relation claims", "temporal_relations", i)
            prior[signature] = i
        if basis not in RELATION_BASES:
            _add(issues, "ERROR", "INVALID_RELATION_BASIS", f"Invalid relation_basis {basis!r}", "temporal_relations", i)
        if r.get("evidence_scope") not in EVIDENCE_SCOPES:
            _add(issues, "ERROR", "INVALID_EVIDENCE_SCOPE", f"Invalid evidence_scope {r.get('evidence_scope')!r}", "temporal_relations", i)
        if r.get("scope_compatibility") not in SCOPE_COMPATIBILITY:
            _add(issues, "ERROR", "INVALID_SCOPE_COMPATIBILITY", f"Invalid scope_compatibility {r.get('scope_compatibility')!r}", "temporal_relations", i)
        if r.get("comparison_scope_id") and not _has_ref(scope_index, r, r.get("comparison_scope_id")):
            _add(issues, "ERROR", "UNKNOWN_COMPARISON_SCOPE", f"Unknown comparison_scope_id {r.get('comparison_scope_id')!r}", "temporal_relations", i)
        if label in POSITIVE_TEMPORAL_LABELS and basis in DIRECT_RELATION_BASES:
            if not r.get("primary_evidence_span_id") or not _has_ref(evidence_index, r, r.get("primary_evidence_span_id")):
                _add(issues, "ERROR", "DIRECT_RELATION_NO_EVIDENCE", "Direct positive temporal relation requires primary evidence span", "temporal_relations", i)
            if basis == "direct_timestamp":
                for endpoint_id in (a, b):
                    endpoint_times = time_rows_by_unit.get((*_partition(r), endpoint_id), [])
                    normalized_times = [
                        time_row for time_row in endpoint_times
                        if time_row.get("normalization_status") == "NORMALIZED"
                        and time_row.get("normalized_start") and time_row.get("normalized_end")
                        and time_row.get("primary_evidence_span_id")
                        and _has_ref(evidence_index, time_row, time_row.get("primary_evidence_span_id"))
                    ]
                    if not normalized_times:
                        _add(issues, "ERROR", "DIRECT_TIMESTAMP_ENDPOINT_TIME_MISSING", f"direct_timestamp requires normalized, evidence-linked time_evidence for endpoint {endpoint_id!r}", "temporal_relations", i)
            ua = units.get((*_partition(r), a))
            ub = units.get((*_partition(r), b))
            for endpoint_name, unit in (("event_a_id", ua), ("event_b_id", ub)):
                if unit and (unit.get("unit_role") != "event_leaf" or unit.get("granularity") != "atomic_event" or unit.get("instance_status") != "RESOLVED"):
                    _add(issues, "ERROR", "INELIGIBLE_PRIMARY_ENDPOINT", f"{endpoint_name} must be a RESOLVED atomic_event event_leaf", "temporal_relations", i)
            comparison_scope = r.get("comparison_scope_id", "")
            if r.get("scope_compatibility") != "COMPATIBLE" or not comparison_scope:
                _add(issues, "ERROR", "PRIMARY_RELATION_SCOPE_INVALID", "Direct positive relation requires COMPATIBLE recorded comparison scope", "temporal_relations", i)
            else:
                for endpoint_name, unit in (("event_a_id", ua), ("event_b_id", ub)):
                    if unit and not _scope_within_partition(_partition(r), unit.get("scope_id", ""), comparison_scope):
                        _add(issues, "ERROR", "ENDPOINT_OUTSIDE_COMPARISON_SCOPE", f"{endpoint_name} scope is not within comparison_scope_id", "temporal_relations", i)
            if ua and ub and ua.get("unit_role") == "event_leaf" and ub.get("unit_role") == "event_leaf" and ua.get("granularity") == "atomic_event" and ub.get("granularity") == "atomic_event" and ua.get("instance_status") == "RESOLVED" and ub.get("instance_status") == "RESOLVED" and r.get("scope_compatibility") == "COMPATIBLE" and comparison_scope and _scope_within_partition(_partition(r), ua.get("scope_id", ""), comparison_scope) and _scope_within_partition(_partition(r), ub.get("scope_id", ""), comparison_scope):
                primary_edges += 1
        elif label in POSITIVE_TEMPORAL_LABELS:
            _add(issues, "WARNING", "NON_PRIMARY_RELATION", f"Positive relation with basis {basis!r} is retained but excluded from primary direct-positive graph", "temporal_relations", i)

    # Candidate pair assessments.
    for i, r in enumerate(tables["candidate_pair_assessments"], 2):
        a, b = r.get("event_a_id", ""), r.get("event_b_id", "")
        if not _has_ref(units, r, a) or not _has_ref(units, r, b):
            _add(issues, "ERROR", "UNKNOWN_ASSESSMENT_ENDPOINT", "Candidate pair endpoints must resolve to activity units", "candidate_pair_assessments", i)
        if a and b and a == b:
            _add(issues, "ERROR", "SELF_ASSESSED_PAIR", "Candidate pair endpoints must be distinct", "candidate_pair_assessments", i)
        if not r.get("candidate_rule_id") or not r.get("candidate_rule_version"):
            _add(issues, "ERROR", "CANDIDATE_RULE_UNPINNED", "Candidate pair requires a rule ID and version", "candidate_pair_assessments", i)
        if r.get("scope_compatibility") not in SCOPE_COMPATIBILITY:
            _add(issues, "ERROR", "INVALID_ASSESSMENT_SCOPE_COMPATIBILITY", "Invalid candidate pair scope_compatibility", "candidate_pair_assessments", i)
        if r.get("comparison_scope_id") and not _has_ref(scope_index, r, r.get("comparison_scope_id")):
            _add(issues, "ERROR", "UNKNOWN_ASSESSMENT_SCOPE", "Unknown comparison_scope_id", "candidate_pair_assessments", i)
        if r.get("assessment_label") not in TEMPORAL_LABELS:
            _add(issues, "ERROR", "INVALID_ASSESSMENT_LABEL", f"Invalid assessment_label {r.get('assessment_label')!r}", "candidate_pair_assessments", i)
        if r.get("scope_compatibility") == "COMPATIBLE":
            if not r.get("comparison_scope_id"):
                _add(issues, "ERROR", "ASSESSMENT_SCOPE_MISSING", "COMPATIBLE candidate pair requires comparison_scope_id", "candidate_pair_assessments", i)
            else:
                for endpoint_name, endpoint_id in (("event_a_id", a), ("event_b_id", b)):
                    endpoint = units.get((*_partition(r), endpoint_id))
                    if endpoint and not _scope_within_partition(_partition(r), endpoint.get("scope_id", ""), r["comparison_scope_id"]):
                        _add(issues, "ERROR", "ASSESSMENT_ENDPOINT_OUTSIDE_SCOPE", f"{endpoint_name} scope is not within comparison_scope_id", "candidate_pair_assessments", i)
        if r.get("assessment_label") == "NO_TEMPORAL_CLAIM" and not r.get("assessment_reason"):
            _add(issues, "ERROR", "NO_CLAIM_REASON_MISSING", "NO_TEMPORAL_CLAIM requires assessment_reason", "candidate_pair_assessments", i)
        if r.get("assessment_label") in POSITIVE_TEMPORAL_LABELS:
            if not r.get("related_relation_id") or not _has_ref(indexes["temporal_relations"], r, r.get("related_relation_id")):
                _add(issues, "ERROR", "POSITIVE_ASSESSMENT_NO_RELATION", "Positive candidate assessment must link to temporal_relations row", "candidate_pair_assessments", i)
            else:
                linked = indexes["temporal_relations"].get((*_partition(r), r.get("related_relation_id", "")))
                if linked:
                    same_pair = {r.get("event_a_id"), r.get("event_b_id")} == {linked.get("event_a_id"), linked.get("event_b_id")}
                    if not same_pair or r.get("assessment_label") != linked.get("relation_label"):
                        _add(issues, "ERROR", "ASSESSMENT_RELATION_MISMATCH", "Positive candidate assessment must match the linked relation's event pair and label", "candidate_pair_assessments", i)

    # Non-temporal relations stay separate and never count as temporal graph edges.
    for i, r in enumerate(tables["non_temporal_relations"], 2):
        for field in ("activity_unit_a_id", "activity_unit_b_id"):
            if not _has_ref(units, r, r.get(field, "")):
                _add(issues, "ERROR", "UNKNOWN_NON_TEMPORAL_ENDPOINT", f"Unknown {field} {r.get(field)!r}", "non_temporal_relations", i)
        if r.get("relation_label") not in NON_TEMPORAL_LABELS:
            _add(issues, "ERROR", "INVALID_NON_TEMPORAL_LABEL", f"Invalid relation_label {r.get('relation_label')!r}", "non_temporal_relations", i)
        if r.get("evidence_scope") not in EVIDENCE_SCOPES:
            _add(issues, "ERROR", "INVALID_NON_TEMPORAL_EVIDENCE_SCOPE", f"Invalid evidence_scope {r.get('evidence_scope')!r}", "non_temporal_relations", i)
        if not _has_ref(evidence_index, r, r.get("primary_evidence_span_id", "")):
            _add(issues, "ERROR", "NON_TEMPORAL_EVIDENCE_MISSING", "Non-temporal relation requires primary evidence span", "non_temporal_relations", i)

    # Additional evidence link constraints, including composite uniqueness and no duplicate primary span.
    composite_seen: set[tuple] = set()
    primary_registers = {"event_mentions", "time_evidence", "temporal_relations", "non_temporal_relations"}
    allowed_link_targets = DECISION_REGISTER | {"adjudication_log"}
    for i, r in enumerate(tables["record_evidence_links"], 2):
        rt, rid, sid = r.get("record_type", ""), r.get("record_id", ""), r.get("evidence_span_id", "")
        if rt not in allowed_link_targets:
            _add(issues, "ERROR", "UNKNOWN_LINK_RECORD_TYPE", f"record_type {rt!r} is not an allowed evidence-link target", "record_evidence_links", i)
        if r.get("evidence_role") not in {"SOURCE_IDENTITY", "ELIGIBILITY", "RIGHTS", "SCOPE_BOUNDARY", "ACTIVITY_UNIT", "MENTION", "MAPPING", "TIME", "TEMPORAL_RELATION", "NON_TEMPORAL_RELATION", "ADJUDICATION", "OTHER"}:
            _add(issues, "ERROR", "INVALID_EVIDENCE_ROLE", f"Invalid evidence_role {r.get('evidence_role')!r}", "record_evidence_links", i)
        elif not _has_ref(indexes.get(rt, {}), r, rid):
            _add(issues, "ERROR", "UNKNOWN_LINK_RECORD", f"Unknown {rt} record ID {rid!r}", "record_evidence_links", i)
        if not _has_ref(evidence_index, r, sid):
            _add(issues, "ERROR", "UNKNOWN_LINK_EVIDENCE", f"Unknown evidence_span_id {sid!r}", "record_evidence_links", i)
        comp = (*_partition(r), rt, rid, sid, r.get("evidence_role", ""))
        if comp in composite_seen:
            _add(issues, "ERROR", "DUPLICATE_EVIDENCE_LINK", "Duplicate composite evidence link tuple", "record_evidence_links", i)
        composite_seen.add(comp)
        if rt in primary_registers:
            target = indexes[rt].get((*_partition(r), rid))
            if target and target.get("primary_evidence_span_id") == sid:
                _add(issues, "ERROR", "PRIMARY_SPAN_DUPLICATED_AS_ADDITIONAL", "Primary evidence span must not be duplicated in additional-link register", "record_evidence_links", i)

    # Accepted/source-supported mapping decisions must have linked mapping evidence.
    for i, mapping in enumerate(tables["event_mappings"], 2):
        if mapping.get("mapping_decision_status") == "ACCEPTED" and mapping.get("mapping_basis") in {"report_explicit_subtechnique", "report_explicit_parent", "source_supported_analyst_candidate"}:
            has_mapping_evidence = any(
                link.get("record_type") == "event_mappings"
                and link.get("record_id") == mapping.get("mapping_id")
                and link.get("evidence_role") == "MAPPING"
                and _partition(link) == _partition(mapping)
                for link in tables["record_evidence_links"]
            )
            if not has_mapping_evidence:
                _add(issues, "ERROR", "ACCEPTED_MAPPING_NO_EVIDENCE_LINK", "Accepted source-supported mapping requires at least one MAPPING evidence link", "event_mappings", i)

    # Adjudication targets must resolve in the named target register and target annotator partition.
    for i, r in enumerate(tables["adjudication_log"], 2):
        if r.get("decision_date"):
            try:
                date.fromisoformat(r["decision_date"])
            except ValueError:
                _add(issues, "ERROR", "INVALID_ADJUDICATION_DATE", "decision_date must use ISO YYYY-MM-DD", "adjudication_log", i)
        rt = r.get("target_register", "")
        if rt not in DECISION_REGISTER:
            _add(issues, "ERROR", "INVALID_ADJUDICATION_TARGET_REGISTER", f"Unknown target_register {rt!r}", "adjudication_log", i)
        else:
            key = (r.get("report_id", ""), r.get("target_annotator_id", ""), r.get("annotation_pass_id", ""), r.get("target_record_id", ""))
            if key not in indexes.get(rt, {}):
                _add(issues, "ERROR", "UNKNOWN_ADJUDICATION_TARGET", f"Cannot resolve target {rt}:{r.get('target_record_id')!r}", "adjudication_log", i)
        if r.get("decision_status") not in {"AGREED", "ADJUDICATED", "DEFERRED"}:
            _add(issues, "ERROR", "INVALID_ADJUDICATION_DECISION", f"Invalid decision_status {r.get('decision_status')!r}", "adjudication_log", i)
        if r.get("primary_evidence_span_id") and not _has_ref(evidence_index, {**r, "annotator_id": r.get("target_annotator_id", "")}, r.get("primary_evidence_span_id")):
            _add(issues, "ERROR", "UNKNOWN_ADJUDICATION_EVIDENCE", "Unknown adjudication evidence span", "adjudication_log", i)

    eligible_partitions = [
        r for r in tables["report_registry"]
        if r.get("source_scope_eligibility") == "ELIGIBLE"
        and r.get("local_research_use_status") == "PERMITTED"
    ]
    # N_assessable requires an assessable source and at least one completed
    # eligible full-report review partition. Source suitability alone is not
    # enough while the review remains pending or in progress.
    assessable_partitions = [
        r for r in eligible_partitions
        if r.get("report_assessability") == "ASSESSABLE"
        and r.get("full_report_review_status") == "COMPLETE"
    ]

    # A report may have multiple annotator/pass partitions. Never choose one
    # partition as the canonical report-level decision implicitly. If source
    # eligibility, local-use permission, or assessability differs across its
    # partitions, flag the conflict and exclude that report from denominators
    # until a researcher/adjudicator resolves it.
    decisions_by_report: dict[str, set[tuple[str, str, str]]] = {}
    for row in tables["report_registry"]:
        decisions_by_report.setdefault(row.get("report_id", ""), set()).add((
            row.get("source_scope_eligibility", ""),
            row.get("local_research_use_status", ""),
            row.get("report_assessability", ""),
        ))
    conflicted_report_ids = {
        report_id for report_id, decisions in decisions_by_report.items()
        if report_id and len(decisions) > 1
    }
    for report_id in sorted(conflicted_report_ids):
        _add(
            issues, "WARNING", "REPORT_LEVEL_DECISION_CONFLICT",
            "Conflicting source eligibility, local-use, or assessability decisions across annotator/pass partitions; exclude from report-level denominators until adjudicated",
            "report_registry",
        )

    eligible_reports = len({
        r.get("report_id", "") for r in eligible_partitions
        if r.get("report_id", "") not in conflicted_report_ids
    })
    assessable_reports = len({
        r.get("report_id", "") for r in assessable_partitions
        if r.get("report_id", "") not in conflicted_report_ids
    })

    if not any(rows_by_register.values()):
        _add(issues, "WARNING", "EMPTY_ANNOTATION_BUNDLE", "All registers are header-only; this validates the package shape only, not an annotation dataset")

    return ValidationReport(
        issues=issues,
        rows_by_register=rows_by_register,
        primary_positive_temporal_edges=primary_edges,
        accepted_a120_mappings=accepted_a120,
        assessable_reports=assessable_reports,
        eligible_reports=eligible_reports,
        eligible_report_partitions=len(eligible_partitions),
        assessable_report_partitions=len(assessable_partitions),
        report_level_decision_conflicts=len(conflicted_report_ids),
        vocabulary_count=len(a120),
        vocabulary_sha256=a120_sha,
        attack_release=ATTACK_RELEASE,
        attack_crosswalk_count=len(attack_crosswalk),
        attack_crosswalk_sha256=attack_crosswalk_sha,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CTI Annotation Schema RECON v0.1 data")
    parser.add_argument("--bundle", type=Path, default=PACKAGE_ROOT, help="Reconstructed schema package directory")
    parser.add_argument("--sources-dir", type=Path, help="Optional directory with frozen source files named REPORT_ID.txt")
    parser.add_argument("--json-out", type=Path, help="Optional path for JSON validation report")
    args = parser.parse_args()
    source_texts: dict[tuple[str, str, str], str] = {}
    if args.sources_dir:
        registry_path = args.bundle / "registers" / "report_registry.csv"
        with registry_path.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                report_id = row.get("report_id", "")
                source_path = args.sources_dir / f"{report_id}.txt"
                if source_path.exists():
                    source_texts[(report_id, row.get("annotator_id", ""), row.get("annotation_pass_id", ""))] = read_frozen_source(source_path)
    result = validate_bundle(args.bundle, source_texts)
    payload = result.to_dict()
    rendered = json.dumps(payload, indent=2)
    print(rendered)
    if args.json_out:
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())