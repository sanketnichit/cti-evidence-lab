"""Synthetic tests for the RECON v0.4 activity-stratum extension."""
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

from test_validator import PARTITION, SOURCE_TEXT, make_fixture  # noqa: E402
from validate_temporal_evidence import SELECTION_HEADERS  # noqa: E402
from validate_activity_strata import (  # noqa: E402
    LOCK_HEADERS,
    STRATUM_HEADERS,
    build_activity_stratum_lock_rows,
    validate_activity_strata,
    validate_activity_stratum_locks,
)
from primary_attack_action_projection import build_primary_attack_action_projection  # noqa: E402

SOURCE = SOURCE_TEXT
BASE = {
    **PARTITION,
    "stratum_basis": "SOURCE_SUPPORTED_HUMAN_JUDGMENT",
    "evidence_span_id": "span-a",
    "stratum_rationale": "Synthetic source-grounded classification.",
    "annotator_confidence": "HIGH",
    "adjudication_status": "UNREVIEWED",
    "stratum_notes": "test",
}


def write_rows(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


class ActivityStratumValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.base = self.root / "CTI_Annotation_Schema_RECON_v0.1"
        self.rows = make_fixture(self.base)
        self.strata_file = self.root / "activity_unit_strata.csv"
        self.strata = [
            {**BASE, "activity_unit_id": "event-a", "activity_stratum": "ATTACK_ACTION"},
            {**BASE, "activity_unit_id": "event-b", "activity_stratum": "ATTACK_ACTION", "evidence_span_id": "span-b"},
        ]
        self.save()

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        write_rows(self.strata_file, STRATUM_HEADERS, self.strata)

    def validate(self):
        return validate_activity_strata(
            self.base, self.strata_file,
            source_texts={(PARTITION["report_id"], PARTITION["annotator_id"], PARTITION["annotation_pass_id"]): SOURCE},
        )

    def test_complete_attack_action_classification_passes(self):
        result = self.validate()
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["stratum_decision_count"], 2)
        self.assertEqual(result["relation_rows_by_route"]["PRIMARY_ATTACK_ACTION"], 1)

    def test_missing_activity_unit_stratum_fails_closed(self):
        self.strata = self.strata[:1]
        self.save()
        result = self.validate()
        self.assertIn("ACTIVITY_STRATUM_MISSING", {row["code"] for row in result["errors"]})

    def test_duplicate_activity_unit_stratum_is_rejected(self):
        self.strata.append(dict(self.strata[0], stratum_notes="duplicate"))
        self.save()
        result = self.validate()
        self.assertIn("DUPLICATE_ACTIVITY_STRATUM", {row["code"] for row in result["errors"]})

    def test_orphan_activity_unit_stratum_is_rejected(self):
        self.strata.append(dict(self.strata[0], activity_unit_id="not-a-unit"))
        self.save()
        result = self.validate()
        self.assertIn("STRATUM_ACTIVITY_UNIT_UNKNOWN", {row["code"] for row in result["errors"]})

    def test_generic_capability_cannot_be_a_resolved_atomic_event_leaf(self):
        self.strata[0]["activity_stratum"] = "GENERIC_CAPABILITY"
        self.save()
        result = self.validate()
        self.assertIn("GENERIC_CAPABILITY_CANNOT_BE_RESOLVED_EVENT", {row["code"] for row in result["errors"]})

    def test_unresolved_classification_requires_unresolved_basis(self):
        self.strata[0]["activity_stratum"] = "UNRESOLVED_CLASSIFICATION"
        self.save()
        result = self.validate()
        self.assertIn("UNRESOLVED_STRATUM_BASIS_MISMATCH", {row["code"] for row in result["errors"]})


class PrimaryProjectionRoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.base = self.root / "CTI_Annotation_Schema_RECON_v0.1"
        make_fixture(self.base)
        self.strata_file = self.root / "activity_unit_strata.csv"
        self.strata = [
            {**BASE, "activity_unit_id": "event-a", "activity_stratum": "ATTACK_ACTION"},
            {**BASE, "activity_unit_id": "event-b", "activity_stratum": "ATTACK_ACTION", "evidence_span_id": "span-b"},
        ]
        write_rows(self.strata_file, STRATUM_HEADERS, self.strata)

    def tearDown(self):
        self.temp.cleanup()

    def project(self):
        return build_primary_attack_action_projection(
            self.base, self.strata_file,
            report_id=PARTITION["report_id"],
            annotator_id=PARTITION["annotator_id"],
            annotation_pass_id=PARTITION["annotation_pass_id"],
        )

    def test_attack_action_edge_is_in_primary_projection(self):
        result = self.project()
        self.assertEqual(result["counts"]["primary_attack_action_event_leaves"], 2)
        self.assertEqual(result["counts"]["primary_direct_positive_attack_action_relations"], 1)
        self.assertEqual(result["projection"]["counts"]["positive_temporal_edges"], 1)
        self.assertEqual(result["pair_opportunity"]["compatible_event_pair_count"], 1)
        self.assertEqual(result["pair_opportunity"]["same_technique_pair_opportunity_count"], 1)

    def test_cross_incident_campaign_pair_is_not_primary(self):
        scopes = [
            {**PARTITION, "scope_id": "report", "parent_scope_id": "", "scope_type": "REPORT_AGGREGATE", "scope_label": "Report", "scope_description": "Synthetic report", "scope_status": "RESOLVED", "scope_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "scope_notes": ""},
            {**PARTITION, "scope_id": "campaign", "parent_scope_id": "report", "scope_type": "CAMPAIGN", "scope_label": "Campaign", "scope_description": "Shared campaign", "scope_status": "RESOLVED", "scope_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "scope_notes": ""},
            {**PARTITION, "scope_id": "incident-a", "parent_scope_id": "campaign", "scope_type": "INCIDENT", "scope_label": "Incident A", "scope_description": "First incident", "scope_status": "RESOLVED", "scope_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "scope_notes": ""},
            {**PARTITION, "scope_id": "incident-b", "parent_scope_id": "campaign", "scope_type": "INCIDENT", "scope_label": "Incident B", "scope_description": "Second incident", "scope_status": "RESOLVED", "scope_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "scope_notes": ""},
        ]
        with (self.base / "registers" / "report_scopes.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["report_id", "annotator_id", "annotation_pass_id", "scope_id", "parent_scope_id", "scope_type", "scope_label", "scope_description", "scope_status", "scope_confidence", "adjudication_status", "scope_notes"])
            writer.writeheader()
            writer.writerows(scopes)
        with (self.base / "registers" / "activity_units.csv").open("r", encoding="utf-8", newline="") as handle:
            units = list(csv.DictReader(handle))
        units[0]["scope_id"] = "incident-a"
        units[1]["scope_id"] = "incident-b"
        write_rows(self.base / "registers" / "activity_units.csv", [
            "report_id", "annotator_id", "annotation_pass_id", "activity_unit_id", "scope_id",
            "parent_activity_unit_id", "granularity", "unit_role", "instance_status", "count_status",
            "count_exact", "count_min", "count_max", "count_qualitative", "recurrence_pattern",
            "unit_summary", "actor_ref", "host_or_asset_ref", "annotator_confidence",
            "adjudication_status", "unit_notes",
        ], units)
        result = self.project()
        self.assertEqual(result["counts"]["primary_direct_positive_attack_action_relations"], 0)
        self.assertEqual(result["counts"]["primary_stratum_relation_ids_excluded_by_scope_rule"], ["rel-a-b"])
        self.assertEqual(result["pair_opportunity"]["compatible_event_pair_count"], 0)
        self.assertEqual(result["projection"]["counts"]["positive_temporal_edges"], 0)

    def test_two_communication_endpoints_are_secondary_not_primary(self):
        self.strata[0]["activity_stratum"] = "THREAT_ACTOR_COMMUNICATION"
        self.strata[1]["activity_stratum"] = "THREAT_ACTOR_COMMUNICATION"
        write_rows(self.strata_file, STRATUM_HEADERS, self.strata)
        result = self.project()
        self.assertEqual(result["counts"]["temporal_relation_rows_by_route"]["AUXILIARY_SAME_STRATUM"], 1)
        self.assertEqual(result["counts"]["primary_direct_positive_attack_action_relations"], 0)
        self.assertEqual(result["projection"]["counts"]["positive_temporal_edges"], 0)
        self.assertEqual(result["pair_opportunity"]["compatible_event_pair_count"], 0)
        self.assertEqual(result["pair_opportunity"]["same_technique_pair_opportunity_count"], 0)
        self.assertIn("rel-a-b", result["counts"]["auxiliary_relation_ids"]["AUXILIARY_SAME_STRATUM"])

    def test_mixed_attack_and_communication_edge_cannot_enter_primary_projection(self):
        self.strata[1]["activity_stratum"] = "THREAT_ACTOR_COMMUNICATION"
        write_rows(self.strata_file, STRATUM_HEADERS, self.strata)
        result = self.project()
        self.assertEqual(result["counts"]["temporal_relation_rows_by_route"]["MIXED_STRATUM"], 1)
        self.assertEqual(result["counts"]["primary_direct_positive_attack_action_relations"], 0)
        self.assertEqual(result["projection"]["counts"]["positive_temporal_edges"], 0)
        self.assertEqual(result["pair_opportunity"]["compatible_event_pair_count"], 0)
        self.assertEqual(result["pair_opportunity"]["same_technique_pair_opportunity_count"], 0)
        self.assertIn("rel-a-b", result["counts"]["auxiliary_relation_ids"]["MIXED_STRATUM"])

    def test_nonprimary_mapping_is_excluded_from_primary_mapping_sets(self):
        self.strata[0]["activity_stratum"] = "THREAT_ACTOR_COMMUNICATION"
        self.strata[1]["activity_stratum"] = "THREAT_ACTOR_COMMUNICATION"
        write_rows(self.strata_file, STRATUM_HEADERS, self.strata)
        result = self.project()
        self.assertEqual(result["mapping_filter"]["accepted_a120_mapping_rows"], 0)
        self.assertEqual(result["projection"]["counts"]["mapped_event_instances"], 0)


class ActivityStratumLockTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.selection_file = self.root / "analysis_partition_selection.csv"
        self.strata_file = self.root / "activity_unit_strata.csv"
        self.locks_file = self.root / "activity_stratum_locks.csv"
        selection = {key: "" for key in SELECTION_HEADERS}
        selection.update({
            "report_id": PARTITION["report_id"],
            "analysis_partition_id": "final-1",
            "annotator_id": PARTITION["annotator_id"],
            "annotation_pass_id": PARTITION["annotation_pass_id"],
            "partition_role": "SINGLE_ANNOTATOR_FINAL",
            "selection_status": "SELECTED_FINAL",
            "lock_reference": "sha256:" + "a" * 64,
            "selection_rationale": "Synthetic selected final",
            "selection_date": "2026-11-08",
        })
        write_rows(self.selection_file, SELECTION_HEADERS, [selection])
        rows = [
            {**BASE, "activity_unit_id": "event-a", "activity_stratum": "ATTACK_ACTION"},
            {**BASE, "activity_unit_id": "event-b", "activity_stratum": "ATTACK_ACTION", "evidence_span_id": "span-b"},
        ]
        write_rows(self.strata_file, STRATUM_HEADERS, rows)
        lock_rows = build_activity_stratum_lock_rows(
            self.selection_file, self.strata_file,
            locked_by="researcher-1", lock_date="2026-11-08",
        )
        write_rows(self.locks_file, LOCK_HEADERS, lock_rows)

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_lock_passes(self):
        result = validate_activity_stratum_locks(self.selection_file, self.strata_file, self.locks_file)
        self.assertTrue(result["ok"], result["errors"])

    def test_post_lock_stratum_change_is_rejected(self):
        with self.strata_file.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0]["activity_stratum"] = "THREAT_ACTOR_COMMUNICATION"
        write_rows(self.strata_file, STRATUM_HEADERS, rows)
        result = validate_activity_stratum_locks(self.selection_file, self.strata_file, self.locks_file)
        self.assertIn("ACTIVITY_STRATUM_LOCK_MISMATCH", {row["code"] for row in result["errors"]})


if __name__ == "__main__":
    unittest.main()
