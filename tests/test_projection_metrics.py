"""Toy tests for event-instance to ATT&CK projection metrics."""

import unittest

from src.projection_metrics import TemporalEdge, project_report


class ProjectionMetricsTests(unittest.TestCase):
    def test_same_technique_before_edge_becomes_diagonal(self):
        result = project_report(
            {"event-1": {"T1059"}, "event-2": {"T1059"}},
            [TemporalEdge("r1", "event-1", "event-2", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE")],
        )
        self.assertEqual(result["counts"]["shared_technique_endpoint_edges"], 1)
        self.assertEqual(result["counts"]["self_only_edges"], 1)
        self.assertEqual(result["counts"]["diagonal_pair_mappings"], 1)
        self.assertEqual(result["counts"]["distinct_technique_pairs"], 0)
        self.assertEqual(result["counts"]["event_edges_without_distinct_technique_pair"], 1)
        self.assertEqual(
            result["projection"]["distinct_technique_pairs"], []
        )
        self.assertEqual(
            result["projection"]["edge_ids_without_distinct_technique_pair"],
            ["r1"],
        )
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
                TemporalEdge("r1", "a1", "b1", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
                TemporalEdge("r2", "a2", "b2", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
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
            [TemporalEdge("r1", "a", "b", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE")],
        )
        self.assertEqual(result["counts"]["resolved_event_instances"], 2)
        self.assertEqual(
            result["projection"]["technique_pairs"],
            [["T1059", "T1071"], ["T1105", "T1071"]],
        )

    def test_multilabel_edge_is_partially_representable_after_diagonal_exclusion(self):
        result = project_report(
            {"a": {"T1059", "T1105"}, "b": {"T1059", "T1071"}},
            [TemporalEdge("r1", "a", "b", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE")],
        )
        self.assertEqual(result["counts"]["diagonal_pair_mappings"], 1)
        self.assertEqual(result["counts"]["distinct_technique_pair_mappings"], 3)
        self.assertEqual(result["counts"]["event_edges_with_distinct_technique_pair"], 1)
        self.assertEqual(result["counts"]["event_edges_without_distinct_technique_pair"], 0)
        self.assertEqual(
            result["projection"]["distinct_technique_pairs"],
            [["T1059", "T1071"], ["T1105", "T1059"], ["T1105", "T1071"]],
        )

    def test_unmapped_endpoint_is_counted_not_silently_dropped(self):
        result = project_report(
            {"a": {"T1059"}, "b": set()},
            [TemporalEdge("r1", "a", "b", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE")],
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
                TemporalEdge("r1", "a1", "b1", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
                TemporalEdge("r2", "b1", "a2", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
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

    def test_multimapping_fanout_cycle_is_not_mistaken_for_multiple_event_edges(self):
        result = project_report(
            {
                "event_a": {"T_A", "T_B"},
                "event_b": {"T_A", "T_B"},
            },
            [TemporalEdge("r1", "event_a", "event_b", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE")],
        )
        self.assertTrue(
            result["strict_before_cycle_analysis"]["source_event_graph_is_acyclic"]
        )
        self.assertEqual(result["counts"]["projected_before_cycle_components"], 1)
        self.assertEqual(
            result["counts"]["projected_cycle_components_from_single_source_event_edge"],
            1,
        )
        self.assertEqual(
            result["counts"]["projected_cycle_components_with_multiple_source_event_edges"],
            0,
        )
        provenance = result["strict_before_cycle_analysis"]["projected_cycle_provenance"][0]
        self.assertEqual(provenance["source_event_edge_ids"], ["r1"])
        self.assertTrue(provenance["single_event_edge_mapping_fanout"])

    def test_symmetric_relation_canonicalizes_technique_pair(self):
        result = project_report(
            {"a": {"T_A"}, "b": {"T_B"}},
            [
                TemporalEdge("r1", "a", "b", "OVERLAP", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
                TemporalEdge("r2", "b", "a", "OVERLAP", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
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
                [TemporalEdge("r1", "a", "b", "NO_TEMPORAL_CLAIM", relation_basis="direct_source", scope_compatibility="COMPATIBLE")],
            )

    def test_inverse_after_and_before_share_normalized_pair_without_label_conflict(self):
        result = project_report(
            {"a": {"T_A"}, "b": {"T_B"}, "c": {"T_A"}, "d": {"T_B"}},
            [
                TemporalEdge("r1", "a", "b", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
                TemporalEdge("r2", "d", "c", "AFTER", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
            ],
        )
        self.assertEqual(result["counts"]["projected_technique_pairs"], 1)
        self.assertEqual(result["counts"]["collision_technique_pairs"], 1)
        self.assertEqual(result["counts"]["label_conflated_technique_pairs"], 0)
        self.assertEqual(result["projection"]["technique_pairs"], [["T_A", "T_B"]])
        self.assertEqual(result["projection"]["edge_to_pairs"]["r2"], [["T_B", "T_A"]])

    def test_before_and_overlap_for_same_projected_pair_remain_label_conflict(self):
        result = project_report(
            {"a": {"T_A"}, "b": {"T_B"}, "c": {"T_A"}, "d": {"T_B"}},
            [
                TemporalEdge("r1", "a", "b", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
                TemporalEdge("r2", "c", "d", "OVERLAP", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
            ],
        )
        self.assertEqual(result["counts"]["label_conflated_technique_pairs"], 1)

    def test_redundant_source_edge_does_not_hide_single_edge_mapping_fanout(self):
        event_mappings = {
            "event_a": {"T_A", "T_B"},
            "event_b": {"T_A", "T_B"},
            "event_c": {"T_A"},
        }
        edges = [
            TemporalEdge("r1", "event_a", "event_b", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
            TemporalEdge("r2", "event_c", "event_b", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
        ]
        result = project_report(event_mappings, edges)
        self.assertEqual(result["counts"]["projected_before_cycle_components"], 1)
        self.assertEqual(result["counts"]["projected_cycle_components_from_single_source_event_edge"], 1)
        self.assertEqual(result["counts"]["projected_cycle_components_requiring_multiple_source_event_edges"], 0)
        provenance = result["strict_before_cycle_analysis"]["projected_cycle_provenance"][0]
        self.assertEqual(provenance["source_event_edge_count"], 2)
        self.assertIn("r1", provenance["single_source_edges_inducing_cycle"])
        self.assertTrue(provenance["single_event_edge_mapping_fanout"])

    def test_after_is_normalized_for_strict_order_cycle_analysis(self):
        result = project_report(
            {
                "a1": {"T_A"},
                "b1": {"T_B"},
                "a2": {"T_A"},
            },
            [
                TemporalEdge("r1", "a1", "b1", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
                TemporalEdge("r2", "a2", "b1", "AFTER", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
            ],
        )
        self.assertTrue(
            result["strict_before_cycle_analysis"]["source_event_graph_is_acyclic"]
        )
        self.assertEqual(result["counts"]["projected_before_cycle_components"], 1)
        self.assertEqual(result["counts"]["non_before_temporal_edges"], 0)
        self.assertEqual(
            result["strict_before_cycle_analysis"]["projected_cycle_components"],
            [["T_A", "T_B"]],
        )

    def test_overlap_does_not_create_strict_before_cycle(self):
        result = project_report(
            {"a": {"T_A"}, "b": {"T_B"}},
            [TemporalEdge("r1", "a", "b", "OVERLAP", relation_basis="direct_source", scope_compatibility="COMPATIBLE")],
        )
        self.assertEqual(result["counts"]["non_before_temporal_edges"], 1)
        self.assertEqual(result["counts"]["projected_before_cycle_components"], 0)

    def test_already_cyclic_source_graph_invalidates_induced_cycle_claim(self):
        result = project_report(
            {"a": {"T_A"}, "b": {"T_B"}},
            [
                TemporalEdge("r1", "a", "b", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
                TemporalEdge("r2", "b", "a", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE"),
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
                [TemporalEdge("r1", "a", "missing", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE")],
            )


    def test_self_event_edge_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "endpoints must be distinct"):
            project_report(
                {"a": {"T_A"}},
                [TemporalEdge("r1", "a", "a", "BEFORE", relation_basis="direct_source", scope_compatibility="COMPATIBLE")],
            )


    def test_diagonal_only_pairs_do_not_count_as_collisions_or_label_conflation(self):
        result = project_report(
            {"a1": {"T1059"}, "b1": {"T1059"}, "a2": {"T1059"}, "b2": {"T1059"}},
            [
                TemporalEdge("r1", "a1", "b1", "BEFORE"),
                TemporalEdge("r2", "a2", "b2", "OVERLAP"),
            ],
        )
        self.assertEqual(result["counts"]["diagonal_pair_mappings"], 2)
        self.assertEqual(result["counts"]["distinct_technique_pairs"], 0)
        self.assertEqual(result["counts"]["collision_technique_pairs"], 0)
        self.assertEqual(result["counts"]["label_conflated_technique_pairs"], 0)
        self.assertEqual(result["rates"]["collision_pair_share"], None)

    def test_label_conflation_is_independent_of_technique_id_order(self):
        result = project_report(
            {"a": {"T_B"}, "b": {"T_A"}, "c": {"T_A"}, "d": {"T_B"}},
            [
                TemporalEdge("before", "a", "b", "BEFORE"),
                TemporalEdge("overlap", "c", "d", "OVERLAP"),
            ],
        )
        self.assertEqual(result["counts"]["label_conflated_technique_pairs"], 1)
        self.assertEqual(
            result["projection"]["label_conflation"],
            {"T_A -> T_B": ["OVERLAP", "STRICT_ORDER"]},
        )

    def test_missing_or_empty_technique_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            project_report({"a": {"T1059", None}}, [])
        with self.assertRaises(ValueError):
            project_report({"a": {"T1059", ""}}, [])

if __name__ == "__main__":
    unittest.main()
