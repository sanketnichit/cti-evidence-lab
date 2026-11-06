"""Synthetic tests for the RECON v0.3 explicit comparison-scope extension."""
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
V1_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.1"
V2_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.2"
sys.path.insert(0, str(V1_ROOT / "tests"))
sys.path.insert(0, str(V2_ROOT / "validator"))
sys.path.insert(0, str(PACKAGE_ROOT / "validator"))
sys.path.insert(0, str(PACKAGE_ROOT / "analysis"))

from test_validator import PARTITION, make_fixture  # noqa: E402
from validate_temporal_evidence import SELECTION_HEADERS  # noqa: E402
from validate_comparison_scope_assignments import (
    ASSIGNMENT_HEADERS, LOCK_HEADERS, build_scope_assignment_lock_rows,
    validate_assignment_register, validate_scope_assignment_locks,
)  # noqa: E402
from comparison_scope_rules import (
    EXPLICIT_RULE_ID, INCIDENT_RULE_ID, LEGACY_RULE_ID, evaluate_scope_pair_rules,
)  # noqa: E402


def assignment_row(event_id, scope_id="scope-incident", span_id="span-a", **overrides):
    row = {
        **PARTITION,
        "assignment_id": f"assign-{event_id}-{scope_id}",
        "activity_unit_id": event_id,
        "comparison_scope_id": scope_id,
        "assignment_status": "ASSIGNED",
        "assignment_basis": "REPORT_EXPLICIT",
        "evidence_span_id": span_id,
        "assignment_rationale": "The report explicitly places this event in the same incident scope.",
        "annotator_confidence": "HIGH",
        "adjudication_status": "UNREVIEWED",
        "assignment_notes": "synthetic fixture",
    }
    row.update(overrides)
    return row


def write_rows(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


class ComparisonScopeAssignmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.base = self.root / "CTI_Annotation_Schema_RECON_v0.1"
        make_fixture(self.base)
        self.assignment_file = self.root / "event_comparison_scope_assignments.csv"
        self.assignments = [
            assignment_row("event-a", span_id="span-a"),
            assignment_row("event-b", span_id="span-b"),
        ]

    def tearDown(self):
        self.temp.cleanup()

    def save_assignments(self):
        write_rows(self.assignment_file, ASSIGNMENT_HEADERS, self.assignments)

    def test_valid_two_event_assignments_pass(self):
        self.save_assignments()
        result = validate_assignment_register(self.base, self.assignment_file)
        self.assertTrue(result["ok"], result["errors"])

    def test_missing_candidate_scope_decision_fails_closed(self):
        self.assignments = self.assignments[:1]
        self.save_assignments()
        result = validate_assignment_register(self.base, self.assignment_file)
        self.assertIn("ASSIGNMENT_REVIEW_INCOMPLETE", {item["code"] for item in result["errors"]})

    def test_not_assigned_is_a_valid_explicit_review_decision(self):
        self.assignments[1]["assignment_status"] = "NOT_ASSIGNED"
        self.save_assignments()
        result = validate_assignment_register(self.base, self.assignment_file)
        codes = {item["code"] for item in result["errors"]}
        self.assertNotIn("INVALID_ASSIGNMENT_STATUS", codes)
        self.assertIn("RELATION_SCOPE_NOT_ASSIGNED_TO_BOTH_ENDPOINTS", codes)

    def test_primary_relation_requires_both_endpoint_assignments(self):
        self.assignments = self.assignments[:1]
        self.save_assignments()
        result = validate_assignment_register(self.base, self.assignment_file)
        self.assertIn("RELATION_SCOPE_NOT_ASSIGNED_TO_BOTH_ENDPOINTS", {item["code"] for item in result["errors"]})

    def test_assigned_scope_must_exist_and_be_in_event_ancestry(self):
        self.assignments[0]["comparison_scope_id"] = "missing-scope"
        self.save_assignments()
        result = validate_assignment_register(self.base, self.assignment_file)
        self.assertIn("ASSIGNMENT_SCOPE_UNKNOWN", {item["code"] for item in result["errors"]})

    def test_uncertain_assignment_does_not_satisfy_positive_relation(self):
        self.assignments[1]["assignment_status"] = "UNCERTAIN"
        self.assignments[1]["assignment_basis"] = "UNRESOLVED"
        self.assignments[1]["evidence_span_id"] = ""
        self.save_assignments()
        result = validate_assignment_register(self.base, self.assignment_file)
        self.assertIn("RELATION_SCOPE_NOT_ASSIGNED_TO_BOTH_ENDPOINTS", {item["code"] for item in result["errors"]})

    def test_duplicate_event_scope_decision_is_rejected(self):
        self.assignments.append(dict(self.assignments[0], assignment_id="another-id"))
        self.save_assignments()
        result = validate_assignment_register(self.base, self.assignment_file)
        self.assertIn("DUPLICATE_EVENT_SCOPE_DECISION", {item["code"] for item in result["errors"]})

    def test_assignment_without_evidence_is_rejected(self):
        self.assignments[0]["evidence_span_id"] = ""
        self.save_assignments()
        result = validate_assignment_register(self.base, self.assignment_file)
        self.assertIn("SCOPE_DECISION_EVIDENCE_MISSING", {item["code"] for item in result["errors"]})


class ScopeAssignmentLockTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.v2 = self.root / "v2"
        self.base = self.root / "CTI_Annotation_Schema_RECON_v0.1"
        make_fixture(self.base)
        self.v2_selection = self.v2 / "registers" / "analysis_partition_selection.csv"
        self.assignments_file = self.root / "assignments.csv"
        self.locks_file = self.root / "locks.csv"
        self.selection = {key: "" for key in SELECTION_HEADERS}
        self.selection.update({
            "report_id": PARTITION["report_id"],
            "analysis_partition_id": "analysis-final",
            "annotator_id": PARTITION["annotator_id"],
            "annotation_pass_id": PARTITION["annotation_pass_id"],
            "partition_role": "SINGLE_ANNOTATOR_FINAL",
            "selection_status": "SELECTED_FINAL",
            "lock_reference": "sha256:" + "a" * 64,
            "selection_rationale": "Synthetic selected final partition",
            "selection_date": "2026-11-05",
        })
        write_rows(self.v2_selection, SELECTION_HEADERS, [self.selection])
        self.assignments = [assignment_row("event-a"), assignment_row("event-b", span_id="span-b")]
        write_rows(self.assignments_file, ASSIGNMENT_HEADERS, self.assignments)
        lock_rows = build_scope_assignment_lock_rows(
            self.v2_selection, self.assignments_file, base_bundle=self.base,
            locked_by="researcher-1", lock_date="2026-11-05",
        )
        write_rows(self.locks_file, LOCK_HEADERS, lock_rows)

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_scope_assignment_lock_passes(self):
        result = validate_scope_assignment_locks(self.v2, self.assignments_file, self.locks_file, self.base)
        self.assertTrue(result["ok"], result["errors"])

    def test_assignment_change_after_lock_is_rejected(self):
        changed = [dict(row) for row in self.assignments]
        changed[0]["assignment_rationale"] = "edited after lock"
        write_rows(self.assignments_file, ASSIGNMENT_HEADERS, changed)
        result = validate_scope_assignment_locks(self.v2, self.assignments_file, self.locks_file, self.base)
        self.assertIn("SCOPE_ASSIGNMENT_LOCK_MISMATCH", {item["code"] for item in result["errors"]})

    def test_lock_builder_rejects_incomplete_scope_review(self):
        write_rows(self.assignments_file, ASSIGNMENT_HEADERS, self.assignments[:1])
        with self.assertRaises(ValueError):
            build_scope_assignment_lock_rows(
                self.v2_selection, self.assignments_file, base_bundle=self.base,
                locked_by="researcher-1", lock_date="2026-11-05",
            )

    def test_lock_validation_rejects_invalid_selected_partition_register(self):
        self.selection["selection_rationale"] = ""
        write_rows(self.v2_selection, SELECTION_HEADERS, [self.selection])
        result = validate_scope_assignment_locks(
            self.v2, self.assignments_file, self.locks_file, self.base
        )
        self.assertIn("SELECTION_REGISTER_VALIDATION_FAILED", {item["code"] for item in result["errors"]})


class ThreeRuleComparisonTests(unittest.TestCase):
    def test_cross_incident_pair_needs_explicit_campaign_assignment(self):
        scopes = [
            {"scope_id": "report", "parent_scope_id": "", "scope_type": "REPORT_AGGREGATE", "scope_status": "RESOLVED"},
            {"scope_id": "campaign", "parent_scope_id": "report", "scope_type": "CAMPAIGN", "scope_status": "RESOLVED"},
            {"scope_id": "incident-a", "parent_scope_id": "campaign", "scope_type": "INCIDENT", "scope_status": "RESOLVED"},
            {"scope_id": "incident-b", "parent_scope_id": "campaign", "scope_type": "INCIDENT", "scope_status": "RESOLVED"},
        ]
        event_a = {"activity_unit_id": "a", "scope_id": "incident-a"}
        event_b = {"activity_unit_id": "b", "scope_id": "incident-b"}
        none = evaluate_scope_pair_rules(event_a, event_b, scopes, [])
        self.assertTrue(none[LEGACY_RULE_ID]["eligible"])
        self.assertFalse(none[INCIDENT_RULE_ID]["eligible"])
        self.assertFalse(none[EXPLICIT_RULE_ID]["eligible"])
        assigned = [
            {"activity_unit_id": "a", "comparison_scope_id": "campaign", "assignment_status": "ASSIGNED"},
            {"activity_unit_id": "b", "comparison_scope_id": "campaign", "assignment_status": "ASSIGNED"},
        ]
        explicit = evaluate_scope_pair_rules(event_a, event_b, scopes, assigned)
        self.assertEqual(explicit[EXPLICIT_RULE_ID]["comparison_scope_id"], "campaign")
        uncertain = [dict(row, assignment_status="UNCERTAIN") for row in assigned]
        self.assertFalse(evaluate_scope_pair_rules(event_a, event_b, scopes, uncertain)[EXPLICIT_RULE_ID]["eligible"])

    def test_unrelated_campaigns_fail_all_three_rules(self):
        scopes = [
            {"scope_id": "report", "parent_scope_id": "", "scope_type": "REPORT_AGGREGATE", "scope_status": "RESOLVED"},
            {"scope_id": "campaign-a", "parent_scope_id": "report", "scope_type": "CAMPAIGN", "scope_status": "RESOLVED"},
            {"scope_id": "campaign-b", "parent_scope_id": "report", "scope_type": "CAMPAIGN", "scope_status": "RESOLVED"},
            {"scope_id": "incident-a", "parent_scope_id": "campaign-a", "scope_type": "INCIDENT", "scope_status": "RESOLVED"},
            {"scope_id": "incident-b", "parent_scope_id": "campaign-b", "scope_type": "INCIDENT", "scope_status": "RESOLVED"},
        ]
        event_a = {"activity_unit_id": "a", "scope_id": "incident-a"}
        event_b = {"activity_unit_id": "b", "scope_id": "incident-b"}
        assignments = [
            {"activity_unit_id": "a", "comparison_scope_id": "campaign-a", "assignment_status": "ASSIGNED"},
            {"activity_unit_id": "b", "comparison_scope_id": "campaign-b", "assignment_status": "ASSIGNED"},
        ]
        results = evaluate_scope_pair_rules(event_a, event_b, scopes, assignments)
        self.assertFalse(any(result["eligible"] for result in results.values()))


if __name__ == "__main__":
    unittest.main()
