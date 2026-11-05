#!/usr/bin/env python3
"""Structural validator for the RECON v0.2 temporal-evidence extension."""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

HEADERS = [
    "report_id", "annotator_id", "annotation_pass_id", "relation_evidence_id",
    "relation_id", "evidence_span_id", "evidence_role", "supported_event_id",
    "evidence_notes",
]
REQUIRED = {
    "temporal_relations": {
        "report_id", "annotator_id", "annotation_pass_id", "relation_id",
        "event_a_id", "event_b_id", "relation_label", "relation_basis", "evidence_scope",
        "primary_evidence_span_id", "relation_notes",
    },
    "evidence_spans": {
        "report_id", "annotator_id", "annotation_pass_id", "evidence_span_id",
        "span_kind", "sentence_id", "section_locator", "paragraph_locator",
    },
    "activity_units": {
        "report_id", "annotator_id", "annotation_pass_id", "activity_unit_id",
    },
    "time_evidence": {
        "report_id", "annotator_id", "annotation_pass_id", "time_evidence_id",
        "activity_unit_id", "raw_time_text", "time_type", "time_precision",
        "timezone_text", "normalization_status", "normalized_start",
        "normalized_end", "normalized_timezone", "timezone_status",
        "uncertainty_notes", "primary_evidence_span_id",
    },
}
POSITIVE = {"BEFORE", "AFTER", "OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"}
DIRECT = {"direct_source", "direct_timestamp"}
ROLES = {"EVENT_A_SUPPORT", "EVENT_B_SUPPORT", "RELATION_CONTEXT"}
TIME_PRECISIONS = {"YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND", "INTERVAL", "QUALITATIVE", "UNKNOWN"}
TIMEZONE_STATUSES = {"EXPLICIT", "INFERRED", "UNKNOWN", "NOT_APPLICABLE"}

SELECTION_HEADERS = [
    "report_id", "analysis_partition_id", "annotator_id", "annotation_pass_id",
    "partition_role", "selection_status", "lock_reference",
    "selection_rationale", "selection_date",
]
PARTITION_ROLES = {
    "DEVELOPMENT", "REPEAT", "INDEPENDENT", "CONSENSUS",
    "ADJUDICATED_FINAL", "SINGLE_ANNOTATOR_FINAL",
}
SELECTION_STATES = {"PENDING", "NOT_SELECTED", "SELECTED_FINAL"}
FINAL_ROLES = {"CONSENSUS", "ADJUDICATED_FINAL", "SINGLE_ANNOTATOR_FINAL"}
LOCK_REFERENCE = re.compile(r"^sha256:[0-9a-f]{64}$")


def part(row):
    return (row.get("report_id", ""), row.get("annotator_id", ""), row.get("annotation_pass_id", ""))


def load(path, required, exact=False):
    if not path.is_file():
        return [], f"missing file: {path}"
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            names = reader.fieldnames or []
            missing = set(required) - set(names)
            if missing or (exact and names != list(required)):
                return [], f"header mismatch in {path.name}; missing={sorted(missing)}"
            rows = []
            for line, row in enumerate(reader, 2):
                if row is None or all((v or "").strip() == "" for v in row.values()):
                    continue
                if None in row:
                    return [], f"row-width mismatch in {path.name}:{line}"
                rows.append({k: (v or "").strip() for k, v in row.items()})
            return rows, None
    except (OSError, csv.Error, UnicodeError) as exc:
        return [], f"cannot read {path}: {exc}"


def _parse_aware_timestamp(value: str):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(timezone.utc)


def validate_analysis_partition_selection(base_bundle: Path, selection_file: Path):
    """Validate the report-level selection of one final analysis partition."""
    errors = []
    selections, error = load(selection_file, SELECTION_HEADERS, exact=True)
    if error:
        return [{"code": "PARTITION_SELECTION_REGISTER_INVALID", "message": error}], 0

    registry, error = load(
        base_bundle / "registers" / "report_registry.csv",
        {
            "report_id", "annotator_id", "annotation_pass_id",
            "source_scope_eligibility", "local_research_use_status",
            "report_assessability", "full_report_review_status",
        },
    )
    if error:
        errors.append({"code": "PARTITION_SELECTION_BASE_INVALID", "message": error})
        registry = []
    adjudications, error = load(
        base_bundle / "registers" / "adjudication_log.csv",
        {
            "report_id", "annotation_pass_id", "target_annotator_id",
            "target_register", "target_record_id", "decision_status",
        },
    )
    if error:
        errors.append({"code": "PARTITION_SELECTION_BASE_INVALID", "message": error})
        adjudications = []

    registry_by_partition = {part(row): row for row in registry}
    annotators_by_report = {}
    for row in registry:
        if row.get("annotator_id"):
            annotators_by_report.setdefault(row.get("report_id", ""), set()).add(row["annotator_id"])
    target_id_fields = {
        "report_registry": "report_id",
        "report_scopes": "scope_id",
        "activity_units": "activity_unit_id",
        "event_mentions": "mention_id",
        "evidence_spans": "evidence_span_id",
        "record_evidence_links": "link_id",
        "event_mappings": "mapping_id",
        "time_evidence": "time_evidence_id",
        "temporal_relations": "relation_id",
        "candidate_pair_assessments": "assessment_id",
        "non_temporal_relations": "non_temporal_relation_id",
    }
    target_rows_cache = {}
    adjudicated = set()
    for decision in adjudications:
        if decision.get("decision_status") != "ADJUDICATED":
            continue
        register_name = decision.get("target_register", "")
        target_field = target_id_fields.get(register_name)
        target_id = decision.get("target_record_id", "")
        if not target_field or not target_id:
            continue
        if register_name not in target_rows_cache:
            target_rows_cache[register_name], target_error = load(
                base_bundle / "registers" / f"{register_name}.csv",
                {"report_id", "annotator_id", "annotation_pass_id", target_field},
            )
            if target_error:
                target_rows_cache[register_name] = []
        resolved = any(
            target.get("report_id") == decision.get("report_id")
            and target.get("annotator_id") == decision.get("target_annotator_id")
            and target.get("annotation_pass_id") == decision.get("annotation_pass_id")
            and target.get(target_field) == target_id
            for target in target_rows_cache[register_name]
        )
        if resolved:
            adjudicated.add((
                decision.get("report_id", ""),
                decision.get("target_annotator_id", ""),
                decision.get("annotation_pass_id", ""),
            ))

    selected_report_ids = {
        row.get("report_id", "")
        for row in selections
        if row.get("selection_status") == "SELECTED_FINAL" and row.get("report_id")
    }
    decisions_by_report = {}
    for row in registry:
        decisions_by_report.setdefault(row.get("report_id", ""), set()).add((
            row.get("source_scope_eligibility", ""),
            row.get("local_research_use_status", ""),
            row.get("report_assessability", ""),
        ))
    for selected_report_id in sorted(selected_report_ids):
        if len(decisions_by_report.get(selected_report_id, set())) > 1:
            errors.append({
                "code": "REPORT_LEVEL_DECISION_CONFLICT",
                "message": (
                    f"report {selected_report_id!r} has conflicting source eligibility, "
                    "local-use or assessability decisions across registered partitions"
                ),
            })

    seen_ids = set()
    selected_by_report = {}
    for line, row in enumerate(selections, 2):
        report_id = row.get("report_id", "")
        selection_id = row.get("analysis_partition_id", "")
        p = part(row)
        if not report_id or not selection_id or not all(p):
            errors.append({
                "code": "PARTITION_SELECTION_KEY_MISSING",
                "message": f"line {line}: report, selection, annotator and pass IDs are required",
            })
        id_key = (report_id, selection_id)
        if id_key in seen_ids:
            errors.append({
                "code": "DUPLICATE_PARTITION_SELECTION_ID",
                "message": f"line {line}: analysis_partition_id is duplicated within the report",
            })
        seen_ids.add(id_key)
        selected_partition = registry_by_partition.get(p)
        if selected_partition is None:
            errors.append({
                "code": "UNKNOWN_SELECTED_PARTITION",
                "message": f"line {line}: selected partition does not resolve in report_registry",
            })

        role = row.get("partition_role", "")
        state = row.get("selection_status", "")
        if role not in PARTITION_ROLES:
            errors.append({"code": "INVALID_PARTITION_ROLE", "message": f"line {line}: invalid partition_role {role!r}"})
        if state not in SELECTION_STATES:
            errors.append({"code": "INVALID_SELECTION_STATUS", "message": f"line {line}: invalid selection_status {state!r}"})

        if state == "SELECTED_FINAL":
            selected_by_report[report_id] = selected_by_report.get(report_id, 0) + 1
            if role not in FINAL_ROLES:
                errors.append({"code": "NONFINAL_ROLE_SELECTED", "message": f"line {line}: only a final role may be SELECTED_FINAL"})
            if not LOCK_REFERENCE.fullmatch(row.get("lock_reference", "")):
                errors.append({"code": "FINAL_PARTITION_LOCK_INVALID", "message": f"line {line}: SELECTED_FINAL requires sha256:<64 lowercase hex>"})
            if not row.get("selection_rationale", "").strip():
                errors.append({"code": "FINAL_PARTITION_RATIONALE_MISSING", "message": f"line {line}: SELECTED_FINAL requires a rationale"})
            try:
                date.fromisoformat(row.get("selection_date", ""))
            except ValueError:
                errors.append({"code": "FINAL_PARTITION_DATE_INVALID", "message": f"line {line}: SELECTED_FINAL requires YYYY-MM-DD selection_date"})

            if selected_partition is not None:
                if selected_partition.get("source_scope_eligibility") != "ELIGIBLE":
                    errors.append({"code": "FINAL_PARTITION_SOURCE_NOT_ELIGIBLE", "message": f"line {line}: final selection requires source_scope_eligibility=ELIGIBLE"})
                if selected_partition.get("local_research_use_status") != "PERMITTED":
                    errors.append({"code": "FINAL_PARTITION_LOCAL_USE_NOT_PERMITTED", "message": f"line {line}: final selection requires local_research_use_status=PERMITTED"})
                if selected_partition.get("report_assessability") != "ASSESSABLE" or selected_partition.get("full_report_review_status") != "COMPLETE":
                    errors.append({"code": "FINAL_PARTITION_REPORT_NOT_ASSESSABLE", "message": f"line {line}: final selection requires ASSESSABLE and COMPLETE report review"})

            annotator_count = len(annotators_by_report.get(report_id, set()))
            if role == "SINGLE_ANNOTATOR_FINAL" and annotator_count != 1:
                errors.append({"code": "SINGLE_ANNOTATOR_FINAL_MISMATCH", "message": f"line {line}: SINGLE_ANNOTATOR_FINAL requires exactly one registered annotator ID"})
            if role == "CONSENSUS":
                if annotator_count < 2:
                    errors.append({"code": "CONSENSUS_WITHOUT_MULTIPLE_ANNOTATORS", "message": f"line {line}: CONSENSUS requires at least two registered annotator IDs"})
                independent_annotators = set()
                for source_row in selections:
                    if (
                        source_row.get("report_id") != report_id
                        or source_row.get("partition_role") != "INDEPENDENT"
                        or source_row.get("selection_status") != "NOT_SELECTED"
                    ):
                        continue
                    source_partition = registry_by_partition.get(part(source_row))
                    if source_partition and (
                        source_partition.get("source_scope_eligibility") == "ELIGIBLE"
                        and source_partition.get("local_research_use_status") == "PERMITTED"
                        and source_partition.get("report_assessability") == "ASSESSABLE"
                        and source_partition.get("full_report_review_status") == "COMPLETE"
                    ):
                        independent_annotators.add(source_row.get("annotator_id", ""))
                independent_annotators.discard("")
                if len(independent_annotators) < 2:
                    errors.append({
                        "code": "CONSENSUS_INDEPENDENT_PARTITIONS_MISSING",
                        "message": f"line {line}: CONSENSUS requires at least two distinct, registered, completed INDEPENDENT input partitions marked NOT_SELECTED",
                    })
            if role == "ADJUDICATED_FINAL" and p not in adjudicated:
                errors.append({"code": "ADJUDICATED_FINAL_WITHOUT_LOG", "message": f"line {line}: selected partition requires an ADJUDICATED log row resolving a target record in the same report/annotator/pass partition"})
        else:
            if row.get("lock_reference", "").strip():
                errors.append({"code": "NONFINAL_PARTITION_HAS_LOCK", "message": f"line {line}: lock_reference is reserved for SELECTED_FINAL"})
            if state == "NOT_SELECTED" and not row.get("selection_rationale", "").strip():
                errors.append({"code": "PARTITION_SELECTION_RATIONALE_MISSING", "message": f"line {line}: NOT_SELECTED requires a rationale"})

    for report_id, count in selected_by_report.items():
        if count > 1:
            errors.append({
                "code": "MULTIPLE_FINAL_PARTITIONS",
                "message": f"report {report_id!r} has {count} SELECTED_FINAL rows",
            })
    return errors, len(selections)


def validate_bundle(base_bundle: Path, evidence_file: Path, selection_file: Path | None = None):
    errors = []
    tables = {}
    for name, required in REQUIRED.items():
        tables[name], error = load(base_bundle / "registers" / f"{name}.csv", required)
        if error:
            errors.append({"code": "BASE_REGISTER_INVALID", "message": error})
    links, error = load(evidence_file, HEADERS, exact=True)
    if error:
        errors.append({"code": "EXTENSION_REGISTER_INVALID", "message": error})
        links = []

    relations = {(*part(r), r["relation_id"]): r for r in tables.get("temporal_relations", []) if r.get("relation_id")}
    spans = {(*part(r), r["evidence_span_id"]): r for r in tables.get("evidence_spans", []) if r.get("evidence_span_id")}
    units = {(*part(r), r["activity_unit_id"]) for r in tables.get("activity_units", []) if r.get("activity_unit_id")}
    grouped = {}
    seen_ids, seen_assignments = set(), set()

    for line, row in enumerate(links, 2):
        p = part(row)
        key = (*p, row.get("relation_id", ""))
        relation = relations.get(key)
        span_id = row.get("evidence_span_id", "")
        role = row.get("evidence_role", "")
        event_id = row.get("supported_event_id", "")
        link_id = row.get("relation_evidence_id", "")
        id_key = (*p, link_id)
        if not link_id:
            errors.append({"code": "MISSING_LINK_ID", "message": f"line {line}: relation_evidence_id is required"})
        elif id_key in seen_ids:
            errors.append({"code": "DUPLICATE_LINK_ID", "message": f"line {line}: duplicate relation_evidence_id"})
        seen_ids.add(id_key)
        if relation is None:
            errors.append({"code": "UNKNOWN_RELATION", "message": f"line {line}: relation does not resolve in the same partition"})
            continue
        if (*p, span_id) not in spans:
            errors.append({"code": "UNKNOWN_EVIDENCE_SPAN", "message": f"line {line}: evidence span does not resolve in the same partition"})
        if role not in ROLES:
            errors.append({"code": "INVALID_EVIDENCE_ROLE", "message": f"line {line}: unsupported role {role!r}"})
            continue
        if role == "EVENT_A_SUPPORT":
            if not event_id or event_id != relation.get("event_a_id"):
                errors.append({"code": "EVENT_A_SUPPORT_MISMATCH", "message": f"line {line}: supported_event_id must equal event_a_id"})
            if event_id and (*p, event_id) not in units:
                errors.append({"code": "UNKNOWN_SUPPORTED_EVENT", "message": f"line {line}: supported event does not resolve"})
        elif role == "EVENT_B_SUPPORT":
            if not event_id or event_id != relation.get("event_b_id"):
                errors.append({"code": "EVENT_B_SUPPORT_MISMATCH", "message": f"line {line}: supported_event_id must equal event_b_id"})
            if event_id and (*p, event_id) not in units:
                errors.append({"code": "UNKNOWN_SUPPORTED_EVENT", "message": f"line {line}: supported event does not resolve"})
        elif role == "RELATION_CONTEXT":
            if event_id:
                errors.append({"code": "CONTEXT_EVENT_ID_FORBIDDEN", "message": f"line {line}: context must not set supported_event_id"})
            if not row.get("evidence_notes"):
                errors.append({"code": "CONTEXT_RATIONALE_MISSING", "message": f"line {line}: context requires an explanatory note"})
        assignment = (*p, row.get("relation_id", ""), span_id, role, event_id)
        if assignment in seen_assignments:
            errors.append({"code": "DUPLICATE_RELATION_EVIDENCE", "message": f"line {line}: duplicate relation/span/role assignment"})
        seen_assignments.add(assignment)
        grouped.setdefault(key, []).append(row)

    for key, relation in relations.items():
        if relation.get("relation_label") not in POSITIVE or relation.get("relation_basis") not in DIRECT:
            continue
        rid, p = relation.get("relation_id", ""), part(relation)
        cue_id = relation.get("primary_evidence_span_id", "")
        cue = spans.get((*p, cue_id))
        if cue is None:
            errors.append({"code": "RELATION_CUE_MISSING", "message": f"{rid}: primary relation cue is missing or unresolved"})
        elif cue.get("span_kind") != "RELATION":
            errors.append({"code": "RELATION_CUE_WRONG_SPAN_KIND", "message": f"{rid}: cue span must have span_kind=RELATION"})
        rows = grouped.get(key, [])
        a_rows = [r for r in rows if r.get("evidence_role") == "EVENT_A_SUPPORT" and r.get("supported_event_id") == relation.get("event_a_id") and (*p, r.get("evidence_span_id", "")) in spans]
        b_rows = [r for r in rows if r.get("evidence_role") == "EVENT_B_SUPPORT" and r.get("supported_event_id") == relation.get("event_b_id") and (*p, r.get("evidence_span_id", "")) in spans]
        if not a_rows:
            errors.append({"code": "EVENT_A_SUPPORT_MISSING", "message": f"{rid}: EVENT_A_SUPPORT is required"})
        if not b_rows:
            errors.append({"code": "EVENT_B_SUPPORT_MISSING", "message": f"{rid}: EVENT_B_SUPPORT is required"})
        evidence_scope = relation.get("evidence_scope", "")
        if evidence_scope not in {"SENTENCE", "CROSS_SENTENCE", "DOCUMENT_CONTEXT"}:
            errors.append({
                "code": "INVALID_EVIDENCE_SCOPE",
                "message": f"{rid}: unsupported evidence_scope {evidence_scope!r}",
            })

        a_span_rows = [
            spans[(*p, row["evidence_span_id"])]
            for row in a_rows if (*p, row.get("evidence_span_id", "")) in spans
        ]
        b_span_rows = [
            spans[(*p, row["evidence_span_id"])]
            for row in b_rows if (*p, row.get("evidence_span_id", "")) in spans
        ]
        cue_sentence = cue.get("sentence_id", "") if cue else ""
        a_sentences = {row.get("sentence_id", "") for row in a_span_rows if row.get("sentence_id", "")}
        b_sentences = {row.get("sentence_id", "") for row in b_span_rows if row.get("sentence_id", "")}

        if evidence_scope == "SENTENCE":
            if not cue_sentence or cue_sentence not in a_sentences or cue_sentence not in b_sentences:
                errors.append({
                    "code": "SENTENCE_SCOPE_ARGUMENTS_NOT_COLOCATED",
                    "message": f"{rid}: SENTENCE requires the cue and at least one A- and B-support span in the same non-empty sentence_id",
                })

        elif evidence_scope == "CROSS_SENTENCE":
            if not cue_sentence:
                errors.append({
                    "code": "CROSS_SENTENCE_CUE_LOCATOR_MISSING",
                    "message": f"{rid}: CROSS_SENTENCE requires a sentence_id for the relation cue",
                })
            support_links = [
                row for row in rows
                if row.get("evidence_role") in {"EVENT_A_SUPPORT", "EVENT_B_SUPPORT"}
                and row.get("supported_event_id") in {relation.get("event_a_id"), relation.get("event_b_id")}
                and (*p, row.get("evidence_span_id", "")) in spans
            ]
            cross_sentence_links = [
                row for row in support_links
                if spans[(*p, row["evidence_span_id"])].get("sentence_id", "")
                and spans[(*p, row["evidence_span_id"])].get("sentence_id", "") != cue_sentence
            ]
            if len({cue_sentence} | a_sentences | b_sentences) < 2 or not cross_sentence_links:
                errors.append({
                    "code": "CROSS_SENTENCE_ARGUMENT_SPAN_MISSING",
                    "message": f"{rid}: CROSS_SENTENCE requires linked endpoint support from at least one sentence distinct from the cue sentence",
                })
            for row in cross_sentence_links:
                if not row.get("evidence_notes", "").strip():
                    errors.append({
                        "code": "CROSS_SENTENCE_ARGUMENT_RATIONALE_MISSING",
                        "message": f"{rid}: endpoint support outside the cue sentence requires evidence_notes explaining the reference/coreference",
                    })

        context_rows = [
            row for row in rows
            if row.get("evidence_role") == "RELATION_CONTEXT"
            and not row.get("supported_event_id")
            and row.get("evidence_notes", "").strip()
            and (*p, row.get("evidence_span_id", "")) in spans
        ]
        if evidence_scope == "DOCUMENT_CONTEXT":
            if not context_rows:
                errors.append({
                    "code": "RELATION_CONTEXT_MISSING",
                    "message": f"{rid}: DOCUMENT_CONTEXT requires a contextual span and explanatory evidence_notes",
                })
            if not relation.get("relation_notes", "").strip():
                errors.append({
                    "code": "DOCUMENT_CONTEXT_RATIONALE_MISSING",
                    "message": f"{rid}: DOCUMENT_CONTEXT requires relation_notes explaining the connection across passages",
                })
            cue_location = (
                cue.get("section_locator", "") if cue else "",
                cue.get("paragraph_locator", "") if cue else "",
            )
            if not any(cue_location) or not any(
                (
                    spans[(*p, row["evidence_span_id"])].get("section_locator", ""),
                    spans[(*p, row["evidence_span_id"])].get("paragraph_locator", ""),
                ) != cue_location
                and any((
                    spans[(*p, row["evidence_span_id"])].get("section_locator", ""),
                    spans[(*p, row["evidence_span_id"])].get("paragraph_locator", ""),
                ))
                for row in context_rows
            ):
                errors.append({
                    "code": "DOCUMENT_CONTEXT_NOT_DISTINCT_PASSAGE",
                    "message": f"{rid}: at least one RELATION_CONTEXT span must have a section/paragraph locator distinct from the relation-cue passage",
                })
        if relation.get("relation_basis") == "direct_timestamp":
            def endpoint_intervals(endpoint_id, support_rows, prefix):
                support_spans = {r.get("evidence_span_id", "") for r in support_rows}
                candidates = [
                    t for t in tables.get("time_evidence", [])
                    if part(t) == p
                    and t.get("activity_unit_id") == endpoint_id
                    and t.get("time_type") == "ATTACK_OCCURRENCE"
                    and t.get("primary_evidence_span_id") in support_spans
                ]
                intervals = []
                for time_row in candidates:
                    if time_row.get("normalization_status") != "NORMALIZED":
                        errors.append({
                            "code": f"{prefix}_TIMESTAMP_CANDIDATE_NOT_NORMALIZED",
                            "message": f"{rid}: retained time record {time_row.get('time_evidence_id', '')!r} for {endpoint_id} is not normalized; it cannot be silently ignored for a direct-timestamp relation",
                        })
                        continue
                    if not time_row.get("raw_time_text", "").strip() or not time_row.get("time_precision", "").strip():
                        errors.append({
                            "code": f"{prefix}_RAW_TIME_FIELDS_MISSING",
                            "message": f"{rid}: direct timestamp evidence for {endpoint_id} must preserve raw_time_text and time_precision",
                        })
                        continue
                    if time_row.get("time_precision") not in TIME_PRECISIONS:
                        errors.append({
                            "code": f"{prefix}_TIME_PRECISION_INVALID",
                            "message": f"{rid}: unsupported time_precision {time_row.get('time_precision')!r} for {endpoint_id}",
                        })
                        continue
                    if time_row.get("timezone_status") not in TIMEZONE_STATUSES:
                        errors.append({
                            "code": f"{prefix}_TIMEZONE_STATUS_INVALID",
                            "message": f"{rid}: unsupported timezone_status {time_row.get('timezone_status')!r} for {endpoint_id}",
                        })
                        continue
                    if time_row.get("timezone_status") != "EXPLICIT" or not time_row.get("timezone_text", "").strip() or not time_row.get("normalized_timezone", "").strip():
                        errors.append({
                            "code": f"{prefix}_TIMEZONE_NOT_EXPLICIT",
                            "message": f"{rid}: {endpoint_id} requires timezone_status=EXPLICIT, timezone_text, and normalized_timezone",
                        })
                        continue
                    start = _parse_aware_timestamp(time_row.get("normalized_start", ""))
                    end = _parse_aware_timestamp(time_row.get("normalized_end", ""))
                    if start is None or end is None:
                        errors.append({
                            "code": f"{prefix}_TIMESTAMP_NOT_TIMEZONE_AWARE",
                            "message": f"{rid}: normalized bounds for {endpoint_id} must be timezone-aware ISO-8601",
                        })
                        continue
                    if start > end:
                        errors.append({
                            "code": f"{prefix}_TIMESTAMP_INTERVAL_REVERSED",
                            "message": f"{rid}: normalized_start is after normalized_end for {endpoint_id}",
                        })
                        continue
                    if start != end and not time_row.get("uncertainty_notes", "").strip():
                        errors.append({
                            "code": f"{prefix}_UNCERTAINTY_NOT_DOCUMENTED",
                            "message": f"{rid}: non-point interval for {endpoint_id} requires uncertainty_notes",
                        })
                        continue
                    intervals.append((start, end))
                if not intervals:
                    errors.append({
                        "code": f"{prefix}_TIMESTAMP_SUPPORT_MISSING",
                        "message": f"{rid}: {endpoint_id} has no comparable normalized ATTACK_OCCURRENCE interval linked to its endpoint support",
                    })
                return intervals

            intervals_a = endpoint_intervals(relation.get("event_a_id", ""), a_rows, "EVENT_A")
            intervals_b = endpoint_intervals(relation.get("event_b_id", ""), b_rows, "EVENT_B")
            if relation.get("relation_label") in {"BEFORE", "AFTER"} and intervals_a and intervals_b:
                if relation.get("relation_label") == "BEFORE":
                    invariant = all(
                        a_end < b_start
                        for a_start, a_end in intervals_a
                        for b_start, b_end in intervals_b
                    )
                else:
                    invariant = all(
                        b_end < a_start
                        for a_start, a_end in intervals_a
                        for b_start, b_end in intervals_b
                    )
                if not invariant:
                    errors.append({
                        "code": "STRICT_TIMESTAMP_ORDER_NOT_INVARIANT",
                        "message": f"{rid}: {relation.get('relation_label')} is not true for every retained interval pair",
                    })

    selection_count = 0
    if selection_file is not None:
        selection_errors, selection_count = validate_analysis_partition_selection(base_bundle, selection_file)
        errors.extend(selection_errors)

    return {
        "ok": not errors, "error_count": len(errors), "errors": errors,
        "relation_count": len(relations), "evidence_link_count": len(links),
        "analysis_partition_selection_count": selection_count,
        "primary_direct_positive_relation_count": sum(
            1 for r in tables.get("temporal_relations", [])
            if r.get("relation_label") in POSITIVE and r.get("relation_basis") in DIRECT
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-bundle", type=Path, required=True)
    parser.add_argument("--evidence-file", type=Path, required=True)
    parser.add_argument(
        "--selection-file", type=Path,
        default=Path(__file__).resolve().parents[1] / "registers" / "analysis_partition_selection.csv",
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    result = validate_bundle(args.base_bundle, args.evidence_file, args.selection_file)
    output = json.dumps(result, indent=2)
    print(output)
    if args.json_out:
        args.json_out.write_text(output + "\n", encoding="utf-8")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
