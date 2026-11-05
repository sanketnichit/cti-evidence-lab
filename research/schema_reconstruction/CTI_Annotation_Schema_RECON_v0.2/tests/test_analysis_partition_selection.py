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
    "report_id", "annotation_pass_id", "target_annotator_id", "target_register",
    "target_record_id", "field_name", "decision_status", "rationale",
]
TARGET_HEADERS = ["report_id", "annotator_id", "annotation_pass_id", "mention_id"]


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
        write(self.base / "registers" / "adjudication_log.csv", ADJUDICATION_HEADERS, self.adjudications)
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
