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

    def test_stratum_adjudication_state_is_unreviewed_until_extension_exists(self):
        for value in ("AGREED", "ADJUDICATED"):
            self.strata[0]["adjudication_status"] = value
            self.save()
            result = self.validate()
            self.assertIn(
                "INVALID_STRATUM_ADJUDICATION_STATUS",
                {row["code"] for row in result["errors"]},
                value,
            )
            self.strata[0]["adjudication_status"] = "UNREVIEWED"

    def test_base_confidence_and_adjudication_enums_are_enforced(self):
        mutations = {
            "activity_units": ("annotator_confidence", "CERTAIN"),
            "event_mentions": ("adjudication_status", "REVIEWED"),
            "report_scopes": ("adjudication_status", "PENDING"),
        }
        for register, (field, value) in mutations.items():
            path = self.base / "registers" / f"{register}.csv"
            with path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            rows[0][field] = value
            write_rows(path, list(rows[0].keys()), rows)
        result = self.validate()
        codes = {row["code"] for row in result["errors"]}
        self.assertIn("INVALID_ANNOTATOR_CONFIDENCE", codes)
        self.assertIn("INVALID_ADJUDICATION_STATUS", codes)

    def test_evidence_span_kind_must_use_controlled_vocabulary(self):
        path = self.base / "registers" / "evidence_spans.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0]["span_kind"] = "UNSPECIFIED"
        write_rows(path, list(rows[0].keys()), rows)
        result = self.validate()
        self.assertIn("INVALID_SPAN_KIND", {row["code"] for row in result["errors"]})

    def test_time_evidence_mention_only_target_is_valid_but_dual_targets_must_agree(self):
        path = self.base / "registers" / "time_evidence.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = list(reader.fieldnames or [])
        row = {field: "" for field in headers}
        row.update({
            **PARTITION,
            "time_evidence_id": "time-mention-a",
            "activity_unit_id": "",
            "mention_id": "mention-a",
            "raw_time_text": "2026-01-01",
            "time_type": "ATTACK_OCCURRENCE",
            "time_precision": "DAY",
            "timezone_status": "UNKNOWN",
            "normalization_status": "UNRESOLVED",
            "primary_evidence_span_id": "span-a",
            "annotator_confidence": "HIGH",
            "adjudication_status": "UNREVIEWED",
        })
        write_rows(path, headers, [row])
        mention_only = self.validate()
        self.assertNotIn("TIME_WITHOUT_TARGET", {issue["code"] for issue in mention_only["errors"]})
        self.assertNotIn("TIME_TARGET_MISMATCH", {issue["code"] for issue in mention_only["errors"]})

        row["activity_unit_id"] = "event-b"
        write_rows(path, headers, [row])
        mismatched = self.validate()
        self.assertIn("TIME_TARGET_MISMATCH", {issue["code"] for issue in mismatched["errors"]})

    def test_required_descriptive_and_mapping_fields_cannot_be_blank(self):
        cases = [
            ("report_registry", "source_title"),
            ("report_scopes", "scope_description"),
            ("activity_units", "unit_summary"),
            ("event_mentions", "mention_kind"),
            ("evidence_spans", "evidence_text"),
            ("event_mappings", "attack_version"),
        ]
        for register, field in cases:
            path = self.base / "registers" / f"{register}.csv"
            with path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            rows[0][field] = ""
            write_rows(path, list(rows[0].keys()), rows)
        result = self.validate()
        required_messages = {
            issue["message"] for issue in result["errors"]
            if issue["code"] == "REQUIRED_FIELD_EMPTY"
        }
        for register, field in cases:
            self.assertTrue(
                any(register in message and field in message for message in required_messages),
                f"missing required-field error for {register}.{field}",
            )

    def test_required_comparison_scope_is_enforced_for_relations_and_assessments(self):
        assessment = {
            **PARTITION,
            "assessment_id": "assessment-a-b",
            "event_a_id": "event-a",
            "event_b_id": "event-b",
            "candidate_rule_id": "synthetic-rule",
            "candidate_rule_version": "1",
            "comparison_scope_id": "",
            "scope_compatibility": "INCOMPATIBLE",
            "assessment_label": "NO_TEMPORAL_CLAIM",
            "related_relation_id": "",
            "assessment_reason": "Synthetic negative assessment.",
            "adjudication_status": "UNREVIEWED",
            "assessment_notes": "",
        }
        path = self.base / "registers" / "candidate_pair_assessments.csv"
        write_rows(path, [
            "report_id", "annotator_id", "annotation_pass_id", "assessment_id",
            "event_a_id", "event_b_id", "candidate_rule_id", "candidate_rule_version",
            "comparison_scope_id", "scope_compatibility", "assessment_label",
            "related_relation_id", "assessment_reason", "adjudication_status", "assessment_notes",
        ], [assessment])
        relation_path = self.base / "registers" / "temporal_relations.csv"
        with relation_path.open("r", encoding="utf-8", newline="") as handle:
            relations = list(csv.DictReader(handle))
        relations[0]["comparison_scope_id"] = ""
        write_rows(relation_path, list(relations[0].keys()), relations)
        result = self.validate()
        messages = [
            issue["message"] for issue in result["errors"]
            if issue["code"] == "REQUIRED_FIELD_EMPTY"
        ]
        self.assertTrue(any("temporal_relations" in message and "comparison_scope_id" in message for message in messages))
        self.assertTrue(any("candidate_pair_assessments" in message and "comparison_scope_id" in message for message in messages))

    def test_required_adjudication_metadata_cannot_be_blank(self):
        row = {
            "report_id": PARTITION["report_id"],
            "annotation_pass_id": PARTITION["annotation_pass_id"],
            "adjudication_id": "adj-1",
            "target_annotator_id": PARTITION["annotator_id"],
            "reviewer_id": "",
            "target_register": "event_mappings",
            "target_record_id": "map-a",
            "field_name": "",
            "original_value": "T1059",
            "proposed_value": "T1059",
            "final_value": "T1059",
            "decision_status": "AGREED",
            "rationale": "",
            "decision_date": "",
            "primary_evidence_span_id": "",
            "adjudication_notes": "",
        }
        path = self.base / "registers" / "adjudication_log.csv"
        write_rows(path, [
            "report_id", "annotation_pass_id", "adjudication_id", "target_annotator_id",
            "reviewer_id", "target_register", "target_record_id", "field_name",
            "original_value", "proposed_value", "final_value", "decision_status",
            "rationale", "decision_date", "primary_evidence_span_id", "adjudication_notes",
        ], [row])
        result = self.validate()
        messages = [
            issue["message"] for issue in result["errors"]
            if issue["code"] == "REQUIRED_FIELD_EMPTY"
        ]
        for field in ("reviewer_id", "field_name", "rationale", "decision_date"):
            self.assertTrue(
                any("adjudication_log" in message and field in message for message in messages),
                f"missing required-field error for adjudication_log.{field}",
            )

    def test_retrieval_date_must_be_iso_date(self):
        path = self.base / "registers" / "report_registry.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0]["retrieval_date"] = "yesterday"
        write_rows(path, list(rows[0].keys()), rows)
        result = self.validate()
        self.assertIn("INVALID_RETRIEVAL_DATE", {row["code"] for row in result["errors"]})

    def test_out_of_vocabulary_mapping_requires_baseline_provenance(self):
        path = self.base / "registers" / "event_mappings.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0].update(
            exact_technique_id="T1002",
            exact_technique_name="Data Compressed",
            baseline_parent_technique_id="T1002",
            baseline_mapping_status="OUT_OF_VOCAB",
            baseline_vocabulary_id="",
            baseline_vocabulary_sha256="",
        )
        write_rows(path, list(rows[0].keys()), rows)
        result = self.validate()
        messages = [
            issue["message"] for issue in result["errors"]
            if issue["code"] == "REQUIRED_FIELD_EMPTY"
        ]
        self.assertTrue(any("baseline_vocabulary_id" in message for message in messages))
        self.assertTrue(any("baseline_vocabulary_sha256" in message for message in messages))

    def test_report_registry_decision_reasons_are_required_conditionally(self):
        path = self.base / "registers" / "report_registry.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0].update(
            source_scope_eligibility="PENDING",
            source_scope_reason="",
            local_research_use_basis="",
            report_assessability="NOT_ASSESSABLE",
            assessability_reason="",
        )
        write_rows(path, list(rows[0].keys()), rows)
        result = self.validate()
        messages = [
            issue["message"] for issue in result["errors"]
            if issue["code"] == "CONDITIONAL_REASON_MISSING"
        ]
        for field in ("source_scope_reason", "local_research_use_basis", "assessability_reason"):
            self.assertTrue(
                any(field in message for message in messages),
                "missing conditional-reason error for report_registry." + field,
            )

    def test_eligible_assessable_source_does_not_require_ineligibility_reasons(self):
        path = self.base / "registers" / "report_registry.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0].update(
            source_scope_eligibility="ELIGIBLE",
            source_scope_reason="",
            report_assessability="ASSESSABLE",
            assessability_reason="",
        )
        write_rows(path, list(rows[0].keys()), rows)
        result = self.validate()
        conditional = [
            issue["message"] for issue in result["errors"]
            if issue["code"] == "CONDITIONAL_REASON_MISSING"
        ]
        self.assertFalse(any(
            "source_scope_reason" in message or "assessability_reason" in message
            for message in conditional
        ))


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
        self.base = self.root / "CTI_Annotation_Schema_RECON_v0.1"
        make_fixture(self.base)
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
            self.base, self.selection_file, self.strata_file,
            locked_by="researcher-1", lock_date="2026-11-08",
        )
        write_rows(self.locks_file, LOCK_HEADERS, lock_rows)

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_lock_passes(self):
        result = validate_activity_stratum_locks(self.base, self.selection_file, self.strata_file, self.locks_file)
        self.assertTrue(result["ok"], result["errors"])

    def test_post_lock_stratum_change_is_rejected(self):
        with self.strata_file.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0]["activity_stratum"] = "THREAT_ACTOR_COMMUNICATION"
        write_rows(self.strata_file, STRATUM_HEADERS, rows)
        result = validate_activity_stratum_locks(self.base, self.selection_file, self.strata_file, self.locks_file)
        self.assertIn("ACTIVITY_STRATUM_LOCK_MISMATCH", {row["code"] for row in result["errors"]})

    def test_lock_creation_rejects_ineligible_selected_partition(self):
        report_registry = self.base / "registers" / "report_registry.csv"
        with report_registry.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0]["source_scope_eligibility"] = "PENDING"
        write_rows(report_registry, list(rows[0].keys()), rows)
        with self.assertRaisesRegex(ValueError, "selected-final partition validation failed"):
            build_activity_stratum_lock_rows(
                self.base, self.selection_file, self.strata_file,
                locked_by="researcher-1", lock_date="2026-11-08",
            )

    def test_lock_validation_rechecks_selected_partition_eligibility(self):
        report_registry = self.base / "registers" / "report_registry.csv"
        with report_registry.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0]["source_scope_eligibility"] = "PENDING"
        write_rows(report_registry, list(rows[0].keys()), rows)
        result = validate_activity_stratum_locks(self.base, self.selection_file, self.strata_file, self.locks_file)
        self.assertIn("SELECTED_FINAL_PARTITION_INVALID", {row["code"] for row in result["errors"]})

    def test_lock_creation_rejects_consensus_final_without_stratum_adjudication(self):
        with self.selection_file.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0]["partition_role"] = "CONSENSUS"
        write_rows(self.selection_file, SELECTION_HEADERS, rows)
        with self.assertRaisesRegex(ValueError, "no activity-stratum adjudication log"):
            build_activity_stratum_lock_rows(
                self.base, self.selection_file, self.strata_file,
                locked_by="researcher-1", lock_date="2026-11-08",
            )

    def test_lock_validation_rejects_consensus_final_without_stratum_adjudication(self):
        with self.selection_file.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        rows[0]["partition_role"] = "CONSENSUS"
        write_rows(self.selection_file, SELECTION_HEADERS, rows)
        result = validate_activity_stratum_locks(
            self.base, self.selection_file, self.strata_file, self.locks_file
        )
        self.assertIn(
            "ACTIVITY_STRATUM_FINAL_ROLE_UNSUPPORTED",
            {row["code"] for row in result["errors"]},
        )


if __name__ == "__main__":
    unittest.main()
