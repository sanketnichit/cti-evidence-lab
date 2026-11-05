"""Validation helpers for human-authored CTI pilot CSV annotations.

This module validates structure and evidence offsets. It does not decide whether
an event identity, ATT&CK mapping, or temporal relation is semantically correct.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence

try:
    from src.source_text_integrity import frozen_source_sha256, read_frozen_source
except ModuleNotFoundError:  # Also support direct execution from the src directory.
    from source_text_integrity import frozen_source_sha256, read_frozen_source


INSTANCE_STATUSES = {
    "RESOLVED", "UNRESOLVED", "GENERIC_BEHAVIOUR", "NOT_AN_EVENT"
}
POSITIVE_TEMPORAL = {
    "BEFORE", "AFTER", "OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"
}
ASSESSMENT_LABELS = {
    "NO_TEMPORAL_CLAIM", "VAGUE_OR_AMBIGUOUS", "NOT_ASSESSABLE"
}
NON_TEMPORAL_LABELS = {
    "CAUSES_OR_ENABLES", "DEPENDS_ON", "PRECONDITION_OF", "NARRATIVE_ORDER_ONLY"
}
ALL_RELATION_LABELS = POSITIVE_TEMPORAL | ASSESSMENT_LABELS | NON_TEMPORAL_LABELS
EVIDENCE_SCOPES = {"SENTENCE", "CROSS_SENTENCE", "DOCUMENT_CONTEXT"}


def _populated(row: Mapping[str, str]) -> bool:
    return any((value or "").strip() for value in row.values())


def _for_report(rows: Iterable[Mapping[str, str]], report_id: str) -> list[dict[str, str]]:
    selected = []
    exact_source_text_fields = {"mention_text", "evidence_text"}
    for row in rows:
        if not _populated(row):
            continue
        if (row.get("report_id") or "").strip() == report_id:
            selected.append({
                key: (value or "") if key in exact_source_text_fields else (value or "").strip()
                for key, value in row.items()
            })
    return selected


def _check_span(
    *,
    text: str,
    start_value: str,
    end_value: str,
    expected_text: str,
    label: str,
    errors: list[str],
) -> bool:
    try:
        start = int(start_value)
        end = int(end_value)
    except (TypeError, ValueError):
        errors.append(f"{label}: start/end must be integer character offsets.")
        return False

    if start < 0 or end <= start or end > len(text):
        errors.append(
            f"{label}: invalid half-open span [{start}, {end}) for "
            f"source text length {len(text)}."
        )
        return False

    actual = text[start:end]
    if actual != expected_text:
        errors.append(
            f"{label}: source_text[{start}:{end}] does not equal the supplied "
            "mention/evidence text."
        )
        return False
    return True


def validate_annotation_rows(
    *,
    report_id: str,
    report_text: str,
    mention_rows: Sequence[Mapping[str, str]],
    mapping_rows: Sequence[Mapping[str, str]],
    relation_rows: Sequence[Mapping[str, str]],
) -> dict:
    """Validate rows for one report and return errors/warnings plus counts."""

    if not report_id.strip():
        raise ValueError("report_id must be non-empty.")

    errors: list[str] = []
    warnings: list[str] = []
    mentions = _for_report(mention_rows, report_id)
    mappings = _for_report(mapping_rows, report_id)
    relations = _for_report(relation_rows, report_id)

    mention_ids: set[str] = set()
    resolved_events: set[str] = set()
    instance_mentions: dict[str, int] = defaultdict(int)

    for row_number, row in enumerate(mentions, start=2):
        prefix = f"event_mentions.csv row {row_number}"
        mention_id = row.get("mention_id", "")
        if not mention_id:
            errors.append(f"{prefix}: mention_id is required.")
        elif mention_id in mention_ids:
            errors.append(f"{prefix}: duplicate mention_id {mention_id!r}.")
        mention_ids.add(mention_id)

        if not _check_span(
            text=report_text,
            start_value=row.get("char_start", ""),
            end_value=row.get("char_end", ""),
            expected_text=row.get("mention_text", ""),
            label=prefix,
            errors=errors,
        ):
            pass

        status = row.get("instance_status", "")
        if status not in INSTANCE_STATUSES:
            errors.append(
                f"{prefix}: instance_status must be one of "
                f"{sorted(INSTANCE_STATUSES)}."
            )
            continue

        event_id = row.get("event_instance_id", "")
        if status == "RESOLVED":
            if not event_id:
                errors.append(f"{prefix}: RESOLVED mention requires event_instance_id.")
            else:
                resolved_events.add(event_id)
                instance_mentions[event_id] += 1
        elif event_id:
            errors.append(
                f"{prefix}: {status} mention must not have a resolved "
                "event_instance_id."
            )

    # A mapping record is either a MAPPED technique mapping (one row per
    # supporting evidence span) or an explicit UNMAPPED declaration.
    mapping_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    event_mapping_declarations: dict[str, set[str]] = defaultdict(set)

    for row_number, row in enumerate(mappings, start=2):
        prefix = f"event_mappings.csv row {row_number}"
        event_id = row.get("event_instance_id", "")
        mapping_id = row.get("mapping_id", "")
        status = row.get("mapping_status", "")

        if event_id not in resolved_events:
            errors.append(
                f"{prefix}: event_instance_id {event_id!r} is not a RESOLVED "
                "event instance in event_mentions.csv."
            )
        if not mapping_id:
            errors.append(f"{prefix}: mapping_id is required.")
        if status not in {"MAPPED", "UNMAPPED"}:
            errors.append(f"{prefix}: mapping_status must be MAPPED or UNMAPPED.")
            continue

        event_mapping_declarations[event_id].add(status)

        if status == "UNMAPPED":
            if any(row.get(key, "") for key in (
                "technique_id", "technique_name", "attack_version",
                "evidence_span_id", "evidence_start", "evidence_end",
                "evidence_text",
            )):
                errors.append(
                    f"{prefix}: UNMAPPED rows must leave technique and evidence "
                    "fields empty."
                )
            continue

        required = (
            "technique_id", "technique_name", "attack_version",
            "evidence_span_id", "evidence_start", "evidence_end", "evidence_text",
        )
        missing = [field for field in required if not row.get(field, "")]
        if missing:
            errors.append(f"{prefix}: MAPPED row is missing {missing}.")
            continue

        _check_span(
            text=report_text,
            start_value=row.get("evidence_start", ""),
            end_value=row.get("evidence_end", ""),
            expected_text=row.get("evidence_text", ""),
            label=prefix + " mapping evidence",
            errors=errors,
        )
        mapping_groups[mapping_id].append(row)

    for event_id in sorted(resolved_events):
        if not event_mapping_declarations.get(event_id):
            errors.append(
                f"Resolved event {event_id!r} needs at least one MAPPED or "
                "UNMAPPED mapping declaration."
            )
        elif len(event_mapping_declarations[event_id]) > 1:
            errors.append(
                f"Resolved event {event_id!r} cannot be both MAPPED and UNMAPPED."
            )

    for mapping_id, rows in mapping_groups.items():
        signatures = {
            (
                row.get("event_instance_id", ""),
                row.get("technique_id", ""),
                row.get("technique_name", ""),
                row.get("attack_version", ""),
            )
            for row in rows
        }
        if len(signatures) > 1:
            errors.append(
                f"mapping_id {mapping_id!r} has inconsistent event/technique/version "
                "values across its evidence-span rows."
            )
        span_ids = [row.get("evidence_span_id", "") for row in rows]
        if len(span_ids) != len(set(span_ids)):
            errors.append(
                f"mapping_id {mapping_id!r} contains duplicate evidence_span_id values."
            )

    # Temporal relation records are represented as one row per evidence span.
    # NO_TEMPORAL_CLAIM / NOT_ASSESSABLE can have no evidence text.
    relation_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    relation_span_ids: set[str] = set()

    for row_number, row in enumerate(relations, start=2):
        prefix = f"temporal_relations.csv row {row_number}"
        relation_id = row.get("relation_id", "")
        event_a = row.get("event_a_id", "")
        event_b = row.get("event_b_id", "")
        label = row.get("relation_label", "")

        if not relation_id:
            errors.append(f"{prefix}: relation_id is required.")
        if label not in ALL_RELATION_LABELS:
            errors.append(f"{prefix}: unsupported relation_label {label!r}.")
        if not event_a or event_a not in resolved_events:
            errors.append(
                f"{prefix}: event_a_id {event_a!r} is not a RESOLVED event instance."
            )
        if not event_b or event_b not in resolved_events:
            errors.append(
                f"{prefix}: event_b_id {event_b!r} is not a RESOLVED event instance."
            )
        if event_a and event_b and event_a == event_b:
            errors.append(f"{prefix}: relation endpoints must be distinct event instances.")

        evidence_text = row.get("evidence_text", "")
        evidence_span_id = row.get("evidence_span_id", "")
        has_any_evidence = any(
            row.get(key, "")
            for key in ("evidence_span_id", "evidence_start", "evidence_end", "evidence_text")
        )

        if label in POSITIVE_TEMPORAL | NON_TEMPORAL_LABELS:
            if not has_any_evidence or not all(
                row.get(key, "")
                for key in ("evidence_span_id", "evidence_start", "evidence_end", "evidence_text")
            ):
                errors.append(
                    f"{prefix}: {label} requires a relation-specific evidence span."
                )
        elif label == "VAGUE_OR_AMBIGUOUS" and not evidence_text:
            errors.append(
                f"{prefix}: VAGUE_OR_AMBIGUOUS requires the ambiguous cue/span."
            )

        if has_any_evidence:
            if not evidence_span_id:
                errors.append(f"{prefix}: evidence_span_id is required with evidence.")
            elif evidence_span_id in relation_span_ids:
                errors.append(
                    f"{prefix}: duplicate evidence_span_id {evidence_span_id!r}."
                )
            relation_span_ids.add(evidence_span_id)
            _check_span(
                text=report_text,
                start_value=row.get("evidence_start", ""),
                end_value=row.get("evidence_end", ""),
                expected_text=evidence_text,
                label=prefix + " relation evidence",
                errors=errors,
            )

        scope = row.get("evidence_scope", "")
        if has_any_evidence and scope not in EVIDENCE_SCOPES:
            errors.append(
                f"{prefix}: evidence_scope must be one of {sorted(EVIDENCE_SCOPES)}."
            )
        relation_groups[relation_id].append(row)

    for relation_id, rows in relation_groups.items():
        signatures = {
            (
                row.get("event_a_id", ""),
                row.get("event_b_id", ""),
                row.get("relation_label", ""),
            )
            for row in rows
        }
        if len(signatures) > 1:
            errors.append(
                f"relation_id {relation_id!r} has inconsistent event endpoints "
                "or relation labels across evidence-span rows."
            )

    if not mentions:
        warnings.append("No event mention rows were supplied for this report.")
    if not relations:
        warnings.append(
            "No event-pair assessments were supplied; this is not evidence that "
            "the report contains no temporal relations."
        )

    return {
        "report_id": report_id,
        "source_text_characters": len(report_text),
        "source_text_sha256": frozen_source_sha256(report_text),
        "counts": {
            "mention_rows": len(mentions),
            "resolved_event_instances": len(resolved_events),
            "mapping_rows": len(mappings),
            "mapped_relation_rows": len(relations),
        },
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def _read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate human annotation offsets and event/relation IDs."
    )
    parser.add_argument("--report-id", required=True)
    parser.add_argument("--text", required=True, help="Path to frozen UTF-8 report text")
    parser.add_argument("--mentions", required=True, help="event_mentions.csv")
    parser.add_argument("--mappings", required=True, help="event_mappings.csv")
    parser.add_argument("--relations", required=True, help="temporal_relations.csv")
    args = parser.parse_args()

    report_text = read_frozen_source(args.text)
    result = validate_annotation_rows(
        report_id=args.report_id,
        report_text=report_text,
        mention_rows=_read_csv(args.mentions),
        mapping_rows=_read_csv(args.mappings),
        relation_rows=_read_csv(args.relations),
    )

    print(f"Report: {result['report_id']}")
    print(f"Characters: {result['source_text_characters']}")
    print(f"SHA-256: {result['source_text_sha256']}")
    print(f"Valid: {result['valid']}")
    for warning in result["warnings"]:
        print(f"WARNING: {warning}")
    for error in result["errors"]:
        print(f"ERROR: {error}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
