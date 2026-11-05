"""Synthetic tests for the v0.2 selected-partition projection adapter."""
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

V0_1_ROOT = Path(__file__).resolve().parents[2] / "CTI_Annotation_Schema_RECON_v0.1"
sys.path.insert(0, str(V0_1_ROOT / "tests"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))

from test_validator import PARTITION, SOURCE_TEXT, make_fixture, write_register  # noqa: E402
from selected_partition_projection_adapter import (  # noqa: E402
    SelectedPartitionAdapterError,
    build_projection_for_selected_report,
    compute_analysis_lock_reference,
)
from validate_temporal_evidence import HEADERS as EVIDENCE_HEADERS, SELECTION_HEADERS  # noqa: E402


class SelectedPartitionProjectionAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "CTI_Annotation_Schema_RECON_v0.2"
        self.base = self.root.parent / "CTI_Annotation_Schema_RECON_v0.1"
        self.rows = make_fixture(self.base)
        self.root.joinpath("registers").mkdir(parents=True, exist_ok=True)
        self.evidence_rows = [
            {
                "report_id": PARTITION["report_id"],
                "annotator_id": PARTITION["annotator_id"],
                "annotation_pass_id": PARTITION["annotation_pass_id"],
                "relation_evidence_id": "rel-evidence-a",
                "relation_id": "rel-a-b",
                "evidence_span_id": "span-a",
                "evidence_role": "EVENT_A_SUPPORT",
                "supported_event_id": "event-a",
                "evidence_notes": "Synthetic endpoint support.",
            },
            {
                "report_id": PARTITION["report_id"],
                "annotator_id": PARTITION["annotator_id"],
                "annotation_pass_id": PARTITION["annotation_pass_id"],
                "relation_evidence_id": "rel-evidence-b",
                "relation_id": "rel-a-b",
                "evidence_span_id": "span-b",
                "evidence_role": "EVENT_B_SUPPORT",
                "supported_event_id": "event-b",
                "evidence_notes": "Synthetic endpoint support.",
            },
        ]
        self.selection_rows = [self.selection()]
        self.save_v0_2_registers()

    def tearDown(self):
        self.temp.cleanup()

    def selection(self, **overrides):
        row = {
            "report_id": PARTITION["report_id"],
            "analysis_partition_id": "selection-final-1",
            "annotator_id": PARTITION["annotator_id"],
            "annotation_pass_id": PARTITION["annotation_pass_id"],
            "partition_role": "SINGLE_ANNOTATOR_FINAL",
            "selection_status": "SELECTED_FINAL",
            "lock_reference": "",
            "selection_rationale": "Synthetic final-pass fixture.",
            "selection_date": "2026-11-05",
        }
        row.update(overrides)
        return row

    def write_csv(self, path, headers, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def save_v0_2_registers(self):
        self.write_csv(
            self.root / "registers" / "temporal_relation_evidence.csv",
            EVIDENCE_HEADERS, self.evidence_rows,
        )
        self.write_csv(
            self.root / "registers" / "analysis_partition_selection.csv",
            SELECTION_HEADERS, self.selection_rows,
        )

    def make_current_lock(self):
        lock = compute_analysis_lock_reference(
            self.root, report_id=PARTITION["report_id"], source_text=SOURCE_TEXT
        )
        self.selection_rows[0]["lock_reference"] = lock
        self.save_v0_2_registers()
        return lock

    def run_adapter(self, **overrides):
        lock = self.selection_rows[0]["lock_reference"]
        args = {
            "report_id": PARTITION["report_id"],
            "source_text": SOURCE_TEXT,
            "analysis_lock_confirmed": True,
            "analysis_lock_reference": lock,
        }
        args.update(overrides)
        return build_projection_for_selected_report(self.root, **args)

    def test_projection_requires_explicit_selected_analysis_lock(self):
        with self.assertRaisesRegex(SelectedPartitionAdapterError, "Explicit selected-analysis-lock"):
            build_projection_for_selected_report(
                self.root, report_id=PARTITION["report_id"], source_text=SOURCE_TEXT
            )

    def test_report_without_selected_final_partition_is_blocked(self):
        self.selection_rows = [self.selection(
            partition_role="REPEAT", selection_status="NOT_SELECTED",
            lock_reference="", selection_rationale="Repeat pass only.",
        )]
        self.save_v0_2_registers()
        with self.assertRaisesRegex(SelectedPartitionAdapterError, "exactly one SELECTED_FINAL"):
            self.run_adapter(analysis_lock_reference="sha256:" + "0" * 64)

    def test_valid_selected_final_partition_projects(self):
        lock = self.make_current_lock()
        result = self.run_adapter()
        self.assertTrue(result["analysis_lock_verified"])
        self.assertEqual(lock, result["analysis_lock_reference"])
        self.assertEqual("SINGLE_ANNOTATOR_FINAL", result["analysis_partition_selection"]["partition_role"])
        self.assertEqual("pass-1", result["partition"]["annotation_pass_id"])
        self.assertEqual(2, result["counts"]["eligible_resolved_atomic_event_leaves"])
        self.assertEqual(2, result["counts"]["accepted_a120_mapping_rows"])
        self.assertEqual(2, result["temporal_evidence_validation"]["evidence_link_count"])

    def test_change_to_temporal_evidence_after_lock_is_rejected(self):
        original = self.make_current_lock()
        self.evidence_rows[0]["evidence_notes"] = "Changed after lock."
        self.save_v0_2_registers()
        with self.assertRaisesRegex(SelectedPartitionAdapterError, "lock_reference does not match"):
            self.run_adapter(analysis_lock_reference=original)

    def test_change_to_selection_decision_after_lock_is_rejected(self):
        original = self.make_current_lock()
        self.selection_rows[0]["selection_rationale"] = "Changed after lock."
        self.save_v0_2_registers()
        with self.assertRaisesRegex(SelectedPartitionAdapterError, "lock_reference does not match"):
            self.run_adapter(analysis_lock_reference=original)

    def test_selected_repeat_partition_cannot_be_promoted_to_final(self):
        self.selection_rows = [self.selection(partition_role="REPEAT")]
        self.save_v0_2_registers()
        lock = self.make_current_lock()
        with self.assertRaisesRegex(SelectedPartitionAdapterError, "selection validation failed"):
            self.run_adapter(analysis_lock_reference=lock)

    def test_invalid_temporal_endpoint_support_blocks_projection(self):
        self.make_current_lock()
        self.evidence_rows[1]["supported_event_id"] = "event-a"
        self.save_v0_2_registers()
        with self.assertRaisesRegex(SelectedPartitionAdapterError, "temporal evidence validation failed"):
            self.run_adapter()

    def test_base_annotation_change_after_lock_is_rejected(self):
        original = self.make_current_lock()
        self.rows["event_mentions"][0]["mention_notes"] = "Changed after lock."
        write_register(self.base, "event_mentions", self.rows["event_mentions"])
        with self.assertRaisesRegex(SelectedPartitionAdapterError, "lock_reference does not match"):
            self.run_adapter(analysis_lock_reference=original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
