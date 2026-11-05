"""Synthetic tests for selected-final report-level aggregation."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "analysis"))
from report_level_aggregation import (  # noqa: E402
    _rates,
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
        # Event absence is an outcome computed later, not a denominator exclusion.

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


if __name__ == "__main__":
    unittest.main()
