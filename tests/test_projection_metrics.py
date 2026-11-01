"""Toy tests for event-instance to ATT&CK projection metrics."""

import unittest

from src.projection_metrics import TemporalEdge, project_report


class ProjectionMetricsTests(unittest.TestCase):
    def test_same_technique_before_edge_becomes_diagonal(self):
        result = project_report(
            {"event-1": {"T1059"}, "event-2": {"T1059"}},
            [TemporalEdge("r1", "event-1", "event-2", "BEFORE")],
        )
        self.assertEqual(result["counts"]["same_technique_overlap_edges"], 1)
        self.assertEqual(result["counts"]["self_only_edges"], 1)
        self.assertEqual(result["counts"]["diagonal_pair_mappings"], 1)
        self.assertEqual(result["projection"]["technique_pairs"], [["T1059", "T1059"]])

    def test_distinct_event_pairs_collapse_to_one_technique_pair(self):
        result = project_report(
            {
                "a1": {"T1059"},
                "a2": {"T1059"},
                "b1": {"T1105"},
                "b2": {"T1105"},
            },
            [
                TemporalEdge("r1", "a1", "b1", "BEFORE"),
                TemporalEdge("r2", "a2", "b2", "BEFORE"),
            ],
        )
        self.assertEqual(result["counts"]["projected_technique_pairs"], 1)
        self.assertEqual(result["counts"]["collision_technique_pairs"], 1)
        self.assertEqual(result["counts"]["excess_event_edge_multiplicity"], 1)
        self.assertEqual(
            result["projection"]["collision_pairs"],
            {"T1059 -> T1105": ["r1", "r2"]},
        )

    def test_multilabel_event_fans_out_without_duplicating_event(self):
        result = project_report(
            {"a": {"T1059", "T1105"}, "b": {"T1071"}},
            [TemporalEdge("r1", "a", "b", "BEFORE")],
        )
        self.assertEqual(result["counts"]["resolved_event_instances"], 2)
        self.assertEqual(
            result["projection"]["technique_pairs"],
            [["T1059", "T1071"], ["T1105", "T1071"]],
        )

    def test_unmapped_endpoint_is_counted_not_silently_dropped(self):
        result = project_report(
            {"a": {"T1059"}, "b": set()},
            [TemporalEdge("r1", "a", "b", "BEFORE")],
        )
        self.assertEqual(result["counts"]["unmapped_temporal_edges"], 1)
        self.assertEqual(result["rates"]["temporal_edge_mapping_coverage"], 0.0)
        self.assertEqual(result["projection"]["unmapped_edge_ids"], ["r1"])

    def test_projection_can_create_cycle_from_acyclic_event_graph(self):
        result = project_report(
            {
                "a1": {"T_A"},
                "b1": {"T_B"},
                "a2": {"T_A"},
            },
            [
                TemporalEdge("r1", "a1", "b1", "BEFORE"),
                TemporalEdge("r2", "b1", "a2", "BEFORE"),
            ],
        )
        self.assertTrue(
            result["strict_before_cycle_analysis"]["source_event_graph_is_acyclic"]
        )
        self.assertTrue(
            result["strict_before_cycle_analysis"]["projection_cycle_analysis_valid"]
        )
        self.assertEqual(result["counts"]["projected_before_cycle_components"], 1)
        self.assertEqual(
            result["strict_before_cycle_analysis"]["projected_cycle_components"],
            [["T_A", "T_B"]],
        )

    def test_symmetric_relation_canonicalizes_technique_pair(self):
        result = project_report(
            {"a": {"T_A"}, "b": {"T_B"}},
            [
                TemporalEdge("r1", "a", "b", "OVERLAP"),
                TemporalEdge("r2", "b", "a", "OVERLAP"),
            ],
        )
        self.assertEqual(result["counts"]["projected_technique_pairs"], 1)
        self.assertEqual(result["counts"]["collision_technique_pairs"], 1)
        self.assertEqual(
            result["projection"]["technique_pairs"],
            [["T_A", "T_B"]],
        )

    def test_no_temporal_claim_is_rejected_as_an_edge(self):
        with self.assertRaises(ValueError):
            project_report(
                {"a": {"T_A"}, "b": {"T_B"}},
                [TemporalEdge("r1", "a", "b", "NO_TEMPORAL_CLAIM")],
            )

    def test_overlap_does_not_create_strict_before_cycle(self):
        result = project_report(
            {"a": {"T_A"}, "b": {"T_B"}},
            [TemporalEdge("r1", "a", "b", "OVERLAP")],
        )
        self.assertEqual(result["counts"]["non_before_temporal_edges"], 1)
        self.assertEqual(result["counts"]["projected_before_cycle_components"], 0)

    def test_already_cyclic_source_graph_invalidates_induced_cycle_claim(self):
        result = project_report(
            {"a": {"T_A"}, "b": {"T_B"}},
            [
                TemporalEdge("r1", "a", "b", "BEFORE"),
                TemporalEdge("r2", "b", "a", "BEFORE"),
            ],
        )
        self.assertFalse(
            result["strict_before_cycle_analysis"]["source_event_graph_is_acyclic"]
        )
        self.assertFalse(
            result["strict_before_cycle_analysis"]["projection_cycle_analysis_valid"]
        )

    def test_unknown_event_reference_is_rejected(self):
        with self.assertRaises(ValueError):
            project_report(
                {"a": {"T_A"}},
                [TemporalEdge("r1", "a", "missing", "BEFORE")],
            )


if __name__ == "__main__":
    unittest.main()
