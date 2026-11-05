#!/usr/bin/env python3
"""Structural validator for the RECON v0.2 temporal-evidence extension."""
from __future__ import annotations

import argparse
import csv
import json
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
        "primary_evidence_span_id",
    },
    "evidence_spans": {
        "report_id", "annotator_id", "annotation_pass_id", "evidence_span_id",
        "span_kind",
    },
    "activity_units": {
        "report_id", "annotator_id", "annotation_pass_id", "activity_unit_id",
    },
    "time_evidence": {
        "report_id", "annotator_id", "annotation_pass_id", "time_evidence_id",
        "activity_unit_id", "time_type", "normalization_status",
        "normalized_start", "normalized_end", "primary_evidence_span_id",
    },
}
POSITIVE = {"BEFORE", "AFTER", "OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"}
DIRECT = {"direct_source", "direct_timestamp"}
ROLES = {"EVENT_A_SUPPORT", "EVENT_B_SUPPORT", "RELATION_CONTEXT"}


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


def validate_bundle(base_bundle: Path, evidence_file: Path):
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
        context_rows = [
            row for row in rows
            if row.get("evidence_role") == "RELATION_CONTEXT"
            and not row.get("supported_event_id")
            and row.get("evidence_notes")
            and (*p, row.get("evidence_span_id", "")) in spans
        ]
        if relation.get("evidence_scope") == "DOCUMENT_CONTEXT" and not context_rows:
            errors.append({"code": "RELATION_CONTEXT_MISSING", "message": f"{rid}: DOCUMENT_CONTEXT requires a contextual span and rationale"})
        if relation.get("relation_basis") == "direct_timestamp":
            timed = {
                (r.get("activity_unit_id", ""), r.get("primary_evidence_span_id", ""))
                for r in tables.get("time_evidence", [])
                if part(r) == p and r.get("time_type") == "ATTACK_OCCURRENCE"
                and r.get("normalization_status") == "NORMALIZED"
                and r.get("normalized_start") and r.get("normalized_end")
            }
            if a_rows and not any((relation.get("event_a_id"), r.get("evidence_span_id")) in timed for r in a_rows):
                errors.append({"code": "EVENT_A_TIMESTAMP_SUPPORT_MISSING", "message": f"{rid}: event A support must link to normalized ATTACK_OCCURRENCE time evidence"})
            if b_rows and not any((relation.get("event_b_id"), r.get("evidence_span_id")) in timed for r in b_rows):
                errors.append({"code": "EVENT_B_TIMESTAMP_SUPPORT_MISSING", "message": f"{rid}: event B support must link to normalized ATTACK_OCCURRENCE time evidence"})

    return {
        "ok": not errors, "error_count": len(errors), "errors": errors,
        "relation_count": len(relations), "evidence_link_count": len(links),
        "primary_direct_positive_relation_count": sum(
            1 for r in tables.get("temporal_relations", [])
            if r.get("relation_label") in POSITIVE and r.get("relation_basis") in DIRECT
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-bundle", type=Path, required=True)
    parser.add_argument("--evidence-file", type=Path, required=True)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    result = validate_bundle(args.base_bundle, args.evidence_file)
    output = json.dumps(result, indent=2)
    print(output)
    if args.json_out:
        args.json_out.write_text(output + "\n", encoding="utf-8")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
