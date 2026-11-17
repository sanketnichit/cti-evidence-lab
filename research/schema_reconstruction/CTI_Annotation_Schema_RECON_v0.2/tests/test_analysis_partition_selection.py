"""Synthetic tests for report-level final analysis partition selection."""
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "validator"))
from validate_temporal_evidence import SELECTION_HEADERS, validate_analysis_partition_selection

REGISTRY_HEADERS = [
    "report_id", "annotator_id", "annotation_pass_id", "source_scope_eligibility",
    "local_research_use_status", "report_assessability", "full_report_review_status",
]
ADJUDICATION_HEADERS = [
    "report_id", "annotation_pass_id", "adjudication_id", "target_annotator_id",
    "reviewer_id", "target_register", "target_record_id", "field_name",
    "original_value", "proposed_value", "final_value", "decision_status",
    "rationale", "decision_date", "primary_evidence_span_id", "adjudication_notes",
]
TARGET_HEADERS = ["report_id", "annotator_id", "annotation_pass_id", "mention_id", "instance_status"]


def write(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


class AnalysisPartitionSelectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.base = self.root / "base"
        self.selection_file = self.root / "analysis_partition_selection.csv"
        self.registry = [
            self.registry_row("human-1", "pass-1"),
            self.registry_row("human-1", "pass-2"),
        ]
        self.adjudications = []
        self.target_records = [{
            "report_id": "r1", "annotator_id": "human-1",
            "annotation_pass_id": "pass-2", "mention_id": "mention-1",
            "instance_status": "RESOLVED",
        }]
        self.rows = []
        self.save()

    def tearDown(self):
        self.tmp.cleanup()

    def registry_row(self, annotator, pass_id):
        return {
            "report_id": "r1", "annotator_id": annotator, "annotation_pass_id": pass_id,
            "source_scope_eligibility": "ELIGIBLE", "local_research_use_status": "PERMITTED",
            "report_assessability": "ASSESSABLE", "full_report_review_status": "COMPLETE",
        }

    def save(self):
        write(self.base / "registers" / "report_registry.csv", REGISTRY_HEADERS, self.registry)
        completed_adjudications = []
        for index, supplied in enumerate(self.adjudications, 1):
            row = {
                "report_id": "r1",
                "annotation_pass_id": "pass-2",
                "adjudication_id": f"adj-{index}",
                "target_annotator_id": "human-1",
                "reviewer_id": "reviewer-1",
                "target_register": "event_mentions",
                "target_record_id": "mention-1",
                "field_name": "instance_status",
                "original_value": "UNRESOLVED",
                "proposed_value": "RESOLVED",
                "final_value": "RESOLVED",
                "decision_status": "ADJUDICATED",
                "rationale": "Synthetic adjudication.",
                "decision_date": "2026-11-05",
                "primary_evidence_span_id": "",
                "adjudication_notes": "",
            }
            row.update(supplied)
            completed_adjudications.append(row)
        write(self.base / "registers" / "adjudication_log.csv", ADJUDICATION_HEADERS, completed_adjudications)
        write(self.base / "registers" / "event_mentions.csv", TARGET_HEADERS, self.target_records)
        write(self.selection_file, SELECTION_HEADERS, self.rows)

    def selection(self, **overrides):
        row = {
            "report_id": "r1", "analysis_partition_id": "sel-1",
            "annotator_id": "human-1", "annotation_pass_id": "pass-2",
            "partition_role": "SINGLE_ANNOTATOR_FINAL", "selection_status": "SELECTED_FINAL",
            "lock_reference": "sha256:" + "a" * 64,
            "selection_rationale": "Reviewed final pass.", "selection_date": "2026-11-05",
        }
        row.update(overrides)
        return row

    def codes(self):
        return {x["code"] for x in validate_analysis_partition_selection(self.base, self.selection_file)[0]}

    def test_header_only_register_is_valid(self):
        self.assertEqual(set(), self.codes())

    def test_single_annotator_final_is_valid_across_repeat_passes(self):
        self.rows = [self.selection()]
        self.save()
        self.assertEqual(set(), self.codes())

    def test_only_one_final_partition_per_report(self):
        self.rows = [
            self.selection(),
            self.selection(analysis_partition_id="sel-2", annotation_pass_id="pass-1"),
        ]
        self.save()
        self.assertIn("MULTIPLE_FINAL_PARTITIONS", self.codes())

    def test_repeat_role_cannot_be_selected_as_final(self):
        self.rows = [self.selection(partition_role="REPEAT")]
        self.save()
        self.assertIn("NONFINAL_ROLE_SELECTED", self.codes())

    def test_final_requires_sha256_lock_and_rationale_and_date(self):
        self.rows = [self.selection(lock_reference="bad", selection_rationale="", selection_date="yesterday")]
        self.save()
        codes = self.codes()
        self.assertIn("FINAL_PARTITION_LOCK_INVALID", codes)
        self.assertIn("FINAL_PARTITION_RATIONALE_MISSING", codes)
        self.assertIn("FINAL_PARTITION_DATE_INVALID", codes)

    def test_single_annotator_final_rejects_multiple_registered_annotators(self):
        self.registry.append(self.registry_row("human-2", "pass-1"))
        self.rows = [self.selection()]
        self.save()
        self.assertIn("SINGLE_ANNOTATOR_FINAL_MISMATCH", self.codes())

    def test_consensus_requires_recorded_independent_input_partitions(self):
        self.registry.append(self.registry_row("human-2", "pass-1"))
        self.rows = [self.selection(partition_role="CONSENSUS")]
        self.save()
        self.assertIn("CONSENSUS_INDEPENDENT_PARTITIONS_MISSING", self.codes())

    def test_consensus_accepts_two_distinct_completed_independent_partitions(self):
        self.registry.append(self.registry_row("human-2", "pass-1"))
        self.rows = [
            self.selection(analysis_partition_id="ind-1", annotation_pass_id="pass-1", partition_role="INDEPENDENT", selection_status="NOT_SELECTED", lock_reference="", selection_rationale="Independent input pass retained."),
            self.selection(analysis_partition_id="ind-2", annotator_id="human-2", annotation_pass_id="pass-1", partition_role="INDEPENDENT", selection_status="NOT_SELECTED", lock_reference="", selection_rationale="Independent input pass retained."),
            self.selection(analysis_partition_id="sel-final", partition_role="CONSENSUS"),
        ]
        self.save()
        self.assertEqual(set(), self.codes())

    def test_adjudicated_final_requires_adjudication_record(self):
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        self.assertIn("ADJUDICATED_FINAL_WITHOUT_LOG", self.codes())

    def test_adjudicated_final_accepts_matching_adjudication_record(self):
        self.adjudications = [{
            "report_id": "r1", "annotation_pass_id": "pass-2",
            "target_annotator_id": "human-1", "target_register": "event_mentions",
            "target_record_id": "mention-1", "field_name": "instance_status",
            "decision_status": "ADJUDICATED", "rationale": "Synthetic adjudication.",
        }]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        self.assertEqual(set(), self.codes())

    def test_adjudication_history_requires_reviewer_id(self):
        for status in ("AGREED", "ADJUDICATED", "DEFERRED"):
            with self.subTest(status=status):
                self.adjudications = [{
                    "reviewer_id": "",
                    "decision_status": status,
                    "original_value": "UNRESOLVED",
                    "final_value": "RESOLVED" if status == "ADJUDICATED" else "UNRESOLVED",
                }]
                self.rows = [self.selection()]
                self.save()
                self.assertIn("ADJUDICATION_REVIEWER_ID_MISSING", self.codes())

    def test_adjudicated_final_requires_reviewer_distinct_from_target_annotator(self):
        self.adjudications = [{
            "reviewer_id": "human-1",
            "target_annotator_id": "human-1",
            "decision_status": "ADJUDICATED",
            "original_value": "UNRESOLVED",
            "proposed_value": "RESOLVED",
            "final_value": "RESOLVED",
        }]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        codes = self.codes()
        self.assertIn("ADJUDICATION_REVIEWER_NOT_INDEPENDENT", codes)
        self.assertIn("ADJUDICATED_FINAL_WITHOUT_LOG", codes)

    def test_adjudicated_final_rejects_final_value_not_persisted_on_target(self):
        self.adjudications = [{
            "final_value": "UNRESOLVED",
        }]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        codes = self.codes()
        self.assertIn("ADJUDICATION_FINAL_VALUE_MISMATCH", codes)
        self.assertIn("ADJUDICATED_FINAL_WITHOUT_LOG", codes)

    def test_append_only_adjudication_history_uses_date_and_value_chain(self):
        self.adjudications = [
            {
                "adjudication_id": "adj-1",
                "original_value": "UNRESOLVED",
                "proposed_value": "INCOMPLETE",
                "final_value": "INCOMPLETE",
                "decision_date": "2026-11-05",
            },
            {
                "adjudication_id": "adj-2",
                "original_value": "INCOMPLETE",
                "proposed_value": "RESOLVED",
                "final_value": "RESOLVED",
                "decision_date": "2026-11-06",
            },
        ]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        self.assertEqual(set(), self.codes())

    def test_append_only_adjudication_history_rejects_broken_value_chain(self):
        self.adjudications = [
            {
                "adjudication_id": "adj-1",
                "original_value": "UNRESOLVED",
                "final_value": "INCOMPLETE",
                "decision_date": "2026-11-05",
            },
            {
                "adjudication_id": "adj-2",
                "original_value": "UNRESOLVED",
                "final_value": "RESOLVED",
                "decision_date": "2026-11-06",
            },
        ]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        self.assertIn("ADJUDICATION_HISTORY_CHAIN_BROKEN", self.codes())

    def test_append_only_adjudication_history_rejects_same_day_ambiguity(self):
        self.adjudications = [
            {
                "adjudication_id": "adj-1",
                "original_value": "UNRESOLVED",
                "final_value": "INCOMPLETE",
                "decision_date": "2026-11-05",
            },
            {
                "adjudication_id": "adj-2",
                "original_value": "INCOMPLETE",
                "final_value": "RESOLVED",
                "decision_date": "2026-11-05",
            },
        ]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        self.assertIn("ADJUDICATION_HISTORY_ORDER_AMBIGUOUS", self.codes())

    def test_adjudicated_decision_must_change_field_value(self):
        self.adjudications = [{
            "decision_status": "ADJUDICATED",
            "original_value": "RESOLVED",
            "proposed_value": "UNRESOLVED",
            "final_value": "RESOLVED",
        }]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        codes = self.codes()
        self.assertIn("ADJUDICATION_VALUE_NOT_CHANGED", codes)
        self.assertIn("ADJUDICATED_FINAL_WITHOUT_LOG", codes)

    def test_agreed_and_deferred_decisions_cannot_change_field_value(self):
        for status in ("AGREED", "DEFERRED"):
            with self.subTest(status=status):
                self.adjudications = [{
                    "decision_status": status,
                    "original_value": "RESOLVED",
                    "proposed_value": "UNRESOLVED",
                    "final_value": "UNRESOLVED",
                }]
                self.rows = [self.selection()]
                self.save()
                self.assertIn("ADJUDICATION_NONVALUE_DECISION_CHANGES_FIELD", self.codes())

    def test_agreed_or_deferred_history_does_not_satisfy_adjudicated_final(self):
        for status in ("AGREED", "DEFERRED"):
            with self.subTest(status=status):
                self.adjudications = [{
                    "decision_status": status,
                    "original_value": "RESOLVED",
                    "proposed_value": "RESOLVED",
                    "final_value": "RESOLVED",
                }]
                self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
                self.save()
                self.assertIn("ADJUDICATED_FINAL_WITHOUT_LOG", self.codes())

    def test_nonvalue_outcomes_participate_in_append_only_value_chain(self):
        self.adjudications = [
            {
                "adjudication_id": "adj-1",
                "original_value": "UNRESOLVED",
                "proposed_value": "INCOMPLETE",
                "final_value": "INCOMPLETE",
                "decision_status": "ADJUDICATED",
                "decision_date": "2026-11-05",
            },
            {
                "adjudication_id": "adj-2",
                "original_value": "INCOMPLETE",
                "proposed_value": "RESOLVED",
                "final_value": "INCOMPLETE",
                "decision_status": "DEFERRED",
                "decision_date": "2026-11-06",
            },
            {
                "adjudication_id": "adj-3",
                "original_value": "INCOMPLETE",
                "proposed_value": "RESOLVED",
                "final_value": "RESOLVED",
                "decision_status": "ADJUDICATED",
                "decision_date": "2026-11-07",
            },
        ]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        self.assertEqual(set(), self.codes())

    def test_nonvalue_outcome_cannot_break_history_chain(self):
        self.adjudications = [
            {
                "adjudication_id": "adj-1",
                "original_value": "UNRESOLVED",
                "proposed_value": "INCOMPLETE",
                "final_value": "INCOMPLETE",
                "decision_status": "ADJUDICATED",
                "decision_date": "2026-11-05",
            },
            {
                "adjudication_id": "adj-2",
                "original_value": "UNRESOLVED",
                "proposed_value": "INCOMPLETE",
                "final_value": "UNRESOLVED",
                "decision_status": "DEFERRED",
                "decision_date": "2026-11-06",
            },
            {
                "adjudication_id": "adj-3",
                "original_value": "UNRESOLVED",
                "proposed_value": "RESOLVED",
                "final_value": "RESOLVED",
                "decision_status": "ADJUDICATED",
                "decision_date": "2026-11-07",
            },
        ]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        self.assertIn("ADJUDICATION_HISTORY_CHAIN_BROKEN", self.codes())

    def test_adjudication_cannot_change_partition_or_record_identity(self):
        identity_fields = {
            "report_id": "r1",
            "annotator_id": "human-1",
            "annotation_pass_id": "pass-2",
            "mention_id": "mention-1",
        }
        for field_name, value in identity_fields.items():
            with self.subTest(field_name=field_name):
                self.adjudications = [{
                    "field_name": field_name,
                    "original_value": value,
                    "proposed_value": value,
                    "final_value": value,
                }]
                self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
                self.save()
                codes = self.codes()
                self.assertIn("ADJUDICATION_IDENTITY_FIELD_FORBIDDEN", codes)
                self.assertIn("ADJUDICATED_FINAL_WITHOUT_LOG", codes)

    def test_adjudicated_final_rejects_field_not_present_in_target_register(self):
        self.adjudications = [{
            "report_id": "r1", "annotation_pass_id": "pass-2",
            "target_annotator_id": "human-1", "target_register": "event_mentions",
            "target_record_id": "mention-1", "field_name": "not_a_real_field",
            "decision_status": "ADJUDICATED", "rationale": "Synthetic adjudication.",
        }]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        codes = self.codes()
        self.assertIn("ADJUDICATION_FIELD_NOT_IN_TARGET_REGISTER", codes)
        self.assertIn("ADJUDICATED_FINAL_WITHOUT_LOG", codes)

    def test_adjudication_field_validation_also_applies_to_agreed_rows(self):
        self.adjudications = [{
            "report_id": "r1", "annotation_pass_id": "pass-2",
            "target_annotator_id": "human-1", "target_register": "event_mentions",
            "target_record_id": "mention-1", "field_name": "unknown_field",
            "decision_status": "AGREED", "rationale": "Synthetic agreement.",
        }]
        self.rows = [self.selection()]
        self.save()
        self.assertIn("ADJUDICATION_FIELD_NOT_IN_TARGET_REGISTER", self.codes())

    def test_adjudicated_final_rejects_log_for_unrelated_target_record(self):
        self.adjudications = [{
            "report_id": "r1", "annotation_pass_id": "pass-2",
            "target_annotator_id": "human-1", "target_register": "event_mentions",
            "target_record_id": "not-a-real-mention", "field_name": "instance_status",
            "decision_status": "ADJUDICATED", "rationale": "Synthetic adjudication.",
        }]
        self.rows = [self.selection(partition_role="ADJUDICATED_FINAL")]
        self.save()
        self.assertIn("ADJUDICATED_FINAL_WITHOUT_LOG", self.codes())

    def test_selected_final_is_blocked_by_cross_partition_decision_conflict(self):
        self.registry[0]["local_research_use_status"] = "UNRESOLVED"
        self.rows = [self.selection()]
        self.save()
        self.assertIn("REPORT_LEVEL_DECISION_CONFLICT", self.codes())

    def test_selection_must_resolve_registered_partition(self):
        self.rows = [self.selection(annotation_pass_id="missing")]
        self.save()
        self.assertIn("UNKNOWN_SELECTED_PARTITION", self.codes())

    def test_ineligible_report_cannot_be_selected_final(self):
        self.registry[1]["source_scope_eligibility"] = "PENDING"
        self.rows = [self.selection()]
        self.save()
        self.assertIn("FINAL_PARTITION_SOURCE_NOT_ELIGIBLE", self.codes())

    def test_incomplete_report_review_cannot_be_selected_final(self):
        self.registry[1]["full_report_review_status"] = "IN_PROGRESS"
        self.rows = [self.selection()]
        self.save()
        self.assertIn("FINAL_PARTITION_REPORT_NOT_ASSESSABLE", self.codes())


if __name__ == "__main__":
    unittest.main()
