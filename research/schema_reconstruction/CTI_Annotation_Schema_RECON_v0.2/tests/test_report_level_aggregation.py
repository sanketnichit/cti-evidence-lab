"""Synthetic tests for selected-final report-level aggregation."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "analysis"))
V0_1_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.1"
sys.path.insert(0, str(V0_1_ROOT / "tests"))
from test_validator import PARTITION, SOURCE_TEXT, make_fixture  # noqa: E402
from selected_partition_projection_adapter import compute_analysis_lock_reference  # noqa: E402
from validate_temporal_evidence import HEADERS as EVIDENCE_HEADERS, SELECTION_HEADERS  # noqa: E402

from report_level_aggregation import (  # noqa: E402
    _rates,
    _conditional_within_technique_opportunity_rate,
    compute_event_pair_opportunity,
    summarize_report_denominators,
    PACKAGE_ROOT as EXTENSION_ROOT,
    aggregate_selected_report_projections,
)
from src.source_text_integrity import frozen_source_sha256  # noqa: E402

SOURCE = "Synthetic frozen CTI report text.\n"
SOURCE_HASH = frozen_source_sha256(SOURCE)


def registry_row(report_id="r1", annotator="human1", pass_id="p1", **overrides):
    row = {
        "report_id": report_id,
        "annotator_id": annotator,
        "annotation_pass_id": pass_id,
        "source_text_sha256": SOURCE_HASH,
        "source_text_char_count": str(len(SOURCE)),
        "source_scope_eligibility": "ELIGIBLE",
        "local_research_use_status": "PERMITTED",
        "report_assessability": "ASSESSABLE",
        "full_report_review_status": "COMPLETE",
        "prior_exposure_status": "UNEXPOSED",
    }
    row.update(overrides)
    return row


class ReportDenominatorTests(unittest.TestCase):
    def test_eligible_and_assessable_count_reports_not_partitions(self):
        rows = [registry_row(pass_id="p1"), registry_row(annotator="human2", pass_id="p2")]
        result = summarize_report_denominators(rows, {"r1": SOURCE})
        self.assertEqual(result["N_eligible"], 1)
        self.assertEqual(result["N_assessable"], 1)
        self.assertEqual(result["assessable_report_ids"], ["r1"])

    def test_fully_reviewed_zero_event_report_remains_assessable(self):
        result = summarize_report_denominators([registry_row()], {"r1": SOURCE})
        self.assertEqual(result["N_assessable"], 1)
        self.assertEqual(result["assessability_coverage"], 1.0)
        # Event absence is an outcome computed later, not a denominator exclusion.

    def test_assessability_coverage_and_status_breakdown_are_explicit(self):
        rows = [
            registry_row(report_id="eligible"),
            registry_row(report_id="pending", report_assessability="PENDING", full_report_review_status="NOT_STARTED"),
            registry_row(report_id="excluded", source_scope_eligibility="INELIGIBLE"),
        ]
        sources = {report_id: SOURCE for report_id in ("eligible", "pending", "excluded")}
        result = summarize_report_denominators(rows, sources)
        self.assertEqual(result["inventory_report_count"], 3)
        self.assertEqual(result["N_eligible"], 2)
        self.assertEqual(result["N_assessable"], 1)
        self.assertEqual(result["assessability_coverage"], 0.5)
        self.assertEqual(result["report_status_counts"]["source_scope_eligibility"]["INELIGIBLE"], 1)
        self.assertEqual(result["report_assessability_pending_ids"], ["pending"])
        self.assertEqual(result["eligible_not_assessable_report_ids"], ["pending"])
        self.assertEqual(result["eligible_not_assessable_reasons"]["pending"], "ASSESSABILITY_PENDING")

    def test_incomplete_review_is_eligible_but_not_assessable(self):
        row = registry_row(full_report_review_status="IN_PROGRESS")
        result = summarize_report_denominators([row], {"r1": SOURCE})
        self.assertEqual(result["N_eligible"], 1)
        self.assertEqual(result["N_assessable"], 0)
        self.assertEqual(result["no_completed_full_review_ids"], ["r1"])

    def test_source_hash_or_character_count_mismatch_blocks_assessable(self):
        result = summarize_report_denominators([registry_row()], {"r1": SOURCE + "changed"})
        self.assertEqual(result["N_eligible"], 1)
        self.assertEqual(result["N_assessable"], 0)
        self.assertEqual(result["source_unverified_ids"], ["r1"])

    def test_cross_partition_decision_conflict_excludes_report_from_denominators(self):
        rows = [
            registry_row(pass_id="p1"),
            registry_row(pass_id="p2", report_assessability="PENDING"),
        ]
        result = summarize_report_denominators(rows, {"r1": SOURCE})
        self.assertEqual(result["N_eligible"], 0)
        self.assertEqual(result["N_assessable"], 0)
        self.assertEqual(result["report_level_decision_conflict_ids"], ["r1"])

    def test_different_frozen_source_versions_block_assessable_not_eligibility(self):
        changed_hash = frozen_source_sha256("different frozen source")
        rows = [registry_row(pass_id="p1"), registry_row(
            pass_id="p2", source_text_sha256=changed_hash,
            source_text_char_count=str(len("different frozen source")),
        )]
        result = summarize_report_denominators(rows, {"r1": SOURCE})
        self.assertEqual(result["N_eligible"], 1)
        self.assertEqual(result["N_assessable"], 0)
        self.assertEqual(result["source_version_conflict_ids"], ["r1"])

    def test_unpermitted_or_ineligible_report_is_not_eligible(self):
        rows = [
            registry_row(report_id="r1", source_scope_eligibility="INELIGIBLE"),
            registry_row(report_id="r2", local_research_use_status="UNRESOLVED"),
        ]
        result = summarize_report_denominators(rows, {"r1": SOURCE, "r2": SOURCE})
        self.assertEqual(result["N_eligible"], 0)
        self.assertEqual(result["N_assessable"], 0)


class EventPairOpportunityTests(unittest.TestCase):
    def setUp(self):
        self.scopes = [
            {"scope_id": "report", "parent_scope_id": "", "scope_type": "REPORT_AGGREGATE", "scope_status": "RESOLVED"},
            {"scope_id": "incident", "parent_scope_id": "report", "scope_type": "INCIDENT", "scope_status": "RESOLVED"},
            {"scope_id": "host-a", "parent_scope_id": "incident", "scope_type": "HOST", "scope_status": "RESOLVED"},
            {"scope_id": "host-b", "parent_scope_id": "incident", "scope_type": "HOST", "scope_status": "RESOLVED"},
            {"scope_id": "incident-2", "parent_scope_id": "report", "scope_type": "INCIDENT", "scope_status": "RESOLVED"},
        ]
        self.units = [
            {"activity_unit_id": "a", "scope_id": "host-a", "unit_role": "event_leaf", "granularity": "atomic_event", "instance_status": "RESOLVED"},
            {"activity_unit_id": "b", "scope_id": "host-b", "unit_role": "event_leaf", "granularity": "atomic_event", "instance_status": "RESOLVED"},
            {"activity_unit_id": "c", "scope_id": "incident-2", "unit_role": "event_leaf", "granularity": "atomic_event", "instance_status": "RESOLVED"},
            {"activity_unit_id": "series", "scope_id": "incident", "unit_role": "series_container", "granularity": "repeated_event_series", "instance_status": "RESOLVED"},
        ]

    def test_cross_host_events_share_resolved_incident_scope(self):
        result = compute_event_pair_opportunity(
            self.units, self.scopes, {"a": {"T1059"}, "b": {"T1059"}, "c": set()}
        )
        self.assertEqual(result["resolved_atomic_event_leaves"], 3)
        self.assertEqual(result["compatible_event_pair_count"], 1)
        self.assertEqual(result["same_technique_pair_opportunity_count"], 1)

    def test_report_aggregate_alone_does_not_make_pair_compatible(self):
        units = [self.units[0], self.units[2]]
        result = compute_event_pair_opportunity(units, self.scopes, {"a": {"T1059"}, "c": {"T1059"}})
        self.assertEqual(result["compatible_event_pair_count"], 0)
        self.assertEqual(result["same_technique_pair_opportunity_count"], 0)

    def test_distinct_incidents_under_shared_campaign_count_under_current_broad_rule(self):
        self.scopes.append({"scope_id": "campaign", "parent_scope_id": "report", "scope_type": "CAMPAIGN", "scope_status": "RESOLVED"})
        self.scopes[1]["parent_scope_id"] = "campaign"
        self.scopes[4]["parent_scope_id"] = "campaign"
        result = compute_event_pair_opportunity(
            [self.units[0], self.units[2]], self.scopes,
            {"a": {"T1059"}, "c": {"T1059"}},
        )
        # This pins the current broad provisional behaviour for review: a
        # shared campaign ancestor currently makes separate incident leaves
        # count as an opportunity pair. The primary rule is still unapproved.
        self.assertEqual(result["compatible_event_pair_count"], 1)
        self.assertEqual(result["same_technique_pair_opportunity_count"], 1)

    def test_series_container_is_not_an_atomic_event_leaf(self):
        result = compute_event_pair_opportunity(self.units, self.scopes, {})
        self.assertEqual(result["resolved_atomic_event_leaves"], 3)

    def test_only_accepted_a120_mapping_intersections_are_passed_to_opportunity(self):
        result = compute_event_pair_opportunity(
            self.units[:2], self.scopes, {"a": {"T1059"}, "b": {"T1105"}}
        )
        self.assertEqual(result["compatible_event_pair_count"], 1)
        self.assertEqual(result["same_technique_pair_opportunity_count"], 0)


class RateAndBlankBundleTests(unittest.TestCase):
    def test_conditional_rate_counts_only_reports_with_opportunity(self):
        rows = [
            {
                "has_same_technique_pair_opportunity": True,
                "has_within_technique_temporal_relation": True,
            },
            {
                "has_same_technique_pair_opportunity": True,
                "has_within_technique_temporal_relation": False,
            },
            {
                "has_same_technique_pair_opportunity": False,
                "has_within_technique_temporal_relation": True,
            },
        ]
        result = _conditional_within_technique_opportunity_rate(rows)
        self.assertEqual(
            result["within_technique_temporal_relation_given_same_technique_pair_opportunity"],
            0.5,
        )
        self.assertEqual(result["numerator_reports_with_both"], 1)
        self.assertEqual(result["denominator_reports_with_same_technique_pair_opportunity"], 2)

    def test_rates_use_distinct_report_outcomes(self):
        rows = [
            {"has_event_leaf": True, "has_compatible_event_pair": True,
             "has_same_technique_pair_opportunity": True,
             "has_positive_temporal_relation": True,
             "has_within_technique_temporal_relation": True},
            {"has_event_leaf": False, "has_compatible_event_pair": False,
             "has_same_technique_pair_opportunity": False,
             "has_positive_temporal_relation": False,
             "has_within_technique_temporal_relation": False},
        ]
        result = _rates(rows, 2)
        self.assertEqual(result["same_technique_pair_opportunity_rate"], 0.5)
        self.assertEqual(result["within_technique_temporal_relation_report_rate"], 0.5)

    def test_empty_bundle_is_not_relabelled_as_zero_outcome_data(self):
        result = aggregate_selected_report_projections(
            EXTENSION_ROOT, source_texts={}, confirm_selected_analysis_locks=False
        )
        self.assertEqual(result["denominators"]["N_eligible"], 0)
        self.assertEqual(result["denominators"]["N_assessable"], 0)
        self.assertEqual(result["status"], "PARTIAL_OR_EMPTY_SELECTED_FINAL_COVERAGE")
        self.assertIsNone(result["report_level_primary_rates"]["same_technique_pair_opportunity_rate"])
        self.assertEqual(result["report_level_primary_rates"]["status"], "NO_ASSESSABLE_REPORTS")




class SelectedFinalAggregationIntegrationTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.temp = tempfile.TemporaryDirectory()
        self.extension = Path(self.temp.name) / "CTI_Annotation_Schema_RECON_v0.2"
        self.base = self.extension.parent / "CTI_Annotation_Schema_RECON_v0.1"
        self.rows = make_fixture(self.base)
        self.source_text = SOURCE_TEXT
        self.source_texts = {PARTITION["report_id"]: SOURCE_TEXT}
        self.evidence_rows = [
            {**PARTITION, "relation_evidence_id": "support-a", "relation_id": "rel-a-b",
             "evidence_span_id": "span-a", "evidence_role": "EVENT_A_SUPPORT",
             "supported_event_id": "event-a", "evidence_notes": "Synthetic endpoint A."},
            {**PARTITION, "relation_evidence_id": "support-b", "relation_id": "rel-a-b",
             "evidence_span_id": "span-b", "evidence_role": "EVENT_B_SUPPORT",
             "supported_event_id": "event-b", "evidence_notes": "Synthetic endpoint B."},
        ]
        self.selection_rows = [{
            **PARTITION, "analysis_partition_id": "final-1",
            "partition_role": "SINGLE_ANNOTATOR_FINAL",
            "selection_status": "SELECTED_FINAL", "lock_reference": "",
            "selection_rationale": "Synthetic end-to-end fixture.",
            "selection_date": "2026-11-05",
        }]
        self._save_csv(self.extension / "registers" / "temporal_relation_evidence.csv",
                       EVIDENCE_HEADERS, self.evidence_rows)
        self._save_selection()

    def tearDown(self):
        self.temp.cleanup()

    def _save_csv(self, path, headers, rows):
        import csv
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def _save_selection(self):
        self._save_csv(self.extension / "registers" / "analysis_partition_selection.csv",
                       SELECTION_HEADERS, self.selection_rows)

    def _create_selection_lock(self):
        lock = compute_analysis_lock_reference(
            self.extension, report_id=PARTITION["report_id"], source_text=self.source_text
        )
        self.selection_rows[0]["lock_reference"] = lock
        self._save_selection()
        return lock

    def test_complete_selected_final_path_aggregates_report_metrics(self):
        self._create_selection_lock()
        result = aggregate_selected_report_projections(
            self.extension,
            source_texts=self.source_texts,
            confirm_selected_analysis_locks=True,
            approve_scope_pair_rule=True,
        )
        self.assertEqual(result["denominators"]["N_eligible"], 1)
        self.assertEqual(result["denominators"]["N_assessable"], 1)
        self.assertEqual(result["denominators"]["assessability_coverage"], 1.0)
        self.assertEqual(result["selection"]["projection_coverage"], 1.0)
        self.assertEqual(result["report_outcome_numerators_in_projected_assessable_subset"]["reports_with_within_technique_temporal_relation"], 1)
        self.assertEqual(result["report_level_primary_rates"]["within_technique_temporal_relation_report_rate"], 1.0)
        self.assertEqual(result["report_level_primary_rates"]["same_technique_pair_opportunity_rate"], 1.0)
        self.assertEqual(result["projection_rates_and_counts"]["counts"]["fully_omitted_edges"], 1)
        self.assertEqual(result["conditional_descriptive_rates_in_projected_subset"]["within_technique_temporal_relation_given_same_technique_pair_opportunity"], 1.0)
        self.assertEqual(len(result["per_report_outcomes"]), 1)
        outcome = result["per_report_outcomes"][0]
        self.assertEqual(outcome["mapping_coverage"]["A_exact"]["event_coverage_rate"], 1.0)
        self.assertEqual(outcome["mapping_coverage"]["A_120"]["event_coverage_rate"], 1.0)
        self.assertEqual(outcome["occurrence_compression_by_technique"]["A_120_parent_technique"], {"T1059": 2})
        self.assertEqual(outcome["activity_unit_counts"]["count_status_by_granularity"]["atomic_event|unknown"], 2)
        self.assertEqual(outcome["mention_instance_status_counts"]["RESOLVED"], 2)
        self.assertEqual(outcome["primary_positive_relation_label_basis_counts"], {"BEFORE|direct_source": 1})
        self.assertEqual(outcome["source_scope_eligibility"], "ELIGIBLE")
        self.assertEqual(outcome["projection_provenance_diagnostics"]["edge_projection_status"]["rel-a-b"], "fully_omitted")
        self.assertEqual(outcome["projection_provenance_diagnostics"]["edge_to_pairs"]["rel-a-b"], [["T1059", "T1059"]])

    def test_missing_selected_final_withholds_primary_report_rates(self):
        self.selection_rows = []
        self._save_selection()
        result = aggregate_selected_report_projections(
            self.extension,
            source_texts=self.source_texts,
            confirm_selected_analysis_locks=True,
            approve_scope_pair_rule=True,
        )
        self.assertEqual(result["denominators"]["N_assessable"], 1)
        self.assertEqual(result["selection"]["projection_coverage"], 0.0)
        self.assertIsNone(result["report_level_primary_rates"]["within_technique_temporal_relation_report_rate"])
        self.assertEqual(result["selection"]["missing_or_blocked_report_ids"], [PARTITION["report_id"]])

    def test_scope_pair_rates_remain_withheld_without_approval(self):
        self._create_selection_lock()
        result = aggregate_selected_report_projections(
            self.extension,
            source_texts=self.source_texts,
            confirm_selected_analysis_locks=True,
            approve_scope_pair_rule=False,
        )
        self.assertIsNone(result["report_level_primary_rates"]["same_technique_pair_opportunity_rate"])
        self.assertIsNone(result["conditional_descriptive_rates_in_projected_subset"]["within_technique_temporal_relation_given_same_technique_pair_opportunity"])
        self.assertEqual(result["conditional_descriptive_rates_in_projected_subset"]["status"], "WITHHELD_PENDING_APPROVAL_OF_SCOPE_PAIR_OPPORTUNITY_RULE")
        self.assertEqual(result["scope_pair_opportunity_rule"]["status"], "PROVISIONAL_NOT_APPROVED")


class AggregatorCliTests(unittest.TestCase):
    def test_cli_writes_blank_structural_json_without_source_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sources = root / "sources"
            sources.mkdir()
            output = root / "result.json"
            command = [
                sys.executable,
                str(PACKAGE_ROOT / "analysis" / "report_level_aggregation.py"),
                "--extension", str(EXTENSION_ROOT),
                "--sources-dir", str(sources),
                "--output", str(output),
            ]
            completed = subprocess.run(
                command,
                cwd=PACKAGE_ROOT.parents[2],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["denominators"]["N_eligible"], 0)
            self.assertIsNone(result["denominators"]["assessability_coverage"])
            self.assertEqual(result["status"], "PARTIAL_OR_EMPTY_SELECTED_FINAL_COVERAGE")
            self.assertNotIn("Synthetic frozen CTI report text", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
