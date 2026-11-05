import sys
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "analysis"))
from projection_metrics_recon import (  # noqa: E402
    TechniqueMapping, TemporalEdge, build_a120_mapping_sets, project_report_recon,
)

VOCAB = {"T1059", "T1105", "T1113", "T1005"}


class ProjectionMetricsReconTests(unittest.TestCase):
    def test_four_mutually_exclusive_edge_outcomes(self):
        mapping_sets = {
            "e1": {"T1059"}, "e2": {"T1059"},       # fully omitted
            "e3": {"T1059", "T1105"}, "e4": {"T1059"},  # partially represented
            "e5": {"T1059"}, "e6": {"T1113"},       # no diagonal
            "e7": {"T1005"}, "e8": set(),            # unmapped endpoint
        }
        edges = [
            TemporalEdge("full", "e1", "e2", "BEFORE"),
            TemporalEdge("partial", "e3", "e4", "BEFORE"),
            TemporalEdge("no-diagonal", "e5", "e6", "BEFORE"),
            TemporalEdge("unmapped", "e7", "e8", "BEFORE"),
        ]
        result = project_report_recon(mapping_sets, edges)
        self.assertEqual(result["edge_projection_status"], {
            "full": "fully_omitted",
            "no-diagonal": "no_diagonal_mapping",
            "partial": "partially_represented",
            "unmapped": "unmapped_endpoint",
        })
        self.assertEqual(result["counts"]["mapped_positive_temporal_edges"], 3)
        self.assertEqual(result["counts"]["fully_omitted_edges"], 1)
        self.assertEqual(result["counts"]["partially_represented_edges"], 1)
        self.assertEqual(result["counts"]["no_diagonal_mapping_edges"], 1)
        self.assertEqual(result["counts"]["unmapped_endpoint_edges"], 1)

    def test_self_event_edge_rejected_in_projection_function(self):
        with self.assertRaisesRegex(ValueError, "Self-event edge"):
            project_report_recon({"e1": {"T1059"}}, [TemporalEdge("loop", "e1", "e1", "BEFORE")])

    def test_unmapped_endpoint_not_counted_as_full_omission(self):
        result = project_report_recon({"e1": {"T1059"}, "e2": set()}, [TemporalEdge("u", "e1", "e2", "BEFORE")])
        self.assertEqual(result["edge_projection_status"]["u"], "unmapped_endpoint")
        self.assertEqual(result["counts"]["fully_omitted_edges"], 0)
        self.assertEqual(result["counts"]["unmapped_endpoint_edges"], 1)

    def test_after_is_reversed_for_strict_order_projection(self):
        result = project_report_recon(
            {"e1": {"T1059"}, "e2": {"T1105"}},
            [TemporalEdge("after", "e1", "e2", "AFTER")],
        )
        pairs = result["projection"]["distinct_pair_provenance_by_relation_class"]
        self.assertIn("STRICT_ORDER|T1105->T1059", pairs)

    def test_symmetric_relations_use_unordered_pairs(self):
        result = project_report_recon(
            {"e1": {"T1105"}, "e2": {"T1059"}},
            [TemporalEdge("overlap", "e1", "e2", "OVERLAP")],
        )
        self.assertIn("OVERLAP|T1059->T1105", result["projection"]["distinct_pair_provenance_by_relation_class"])

    def test_distinct_pair_collisions_are_counted_and_label_conflicts_retained(self):
        result = project_report_recon(
            {"a": {"T1059"}, "b": {"T1105"}, "c": {"T1059"}, "d": {"T1105"}},
            [
                TemporalEdge("r1", "a", "b", "BEFORE"),
                TemporalEdge("r2", "c", "d", "BEFORE"),
                TemporalEdge("r3", "a", "b", "OVERLAP"),
            ],
        )
        self.assertEqual(result["counts"]["distinct_pair_collision_keys_global"], 1)
        self.assertEqual(result["counts"]["distinct_pair_label_conflicts"], 1)
        self.assertEqual(result["projection"]["distinct_pair_collisions_global"]["T1059->T1105"], ["r1", "r2", "r3"])

    def test_technique_cycles_have_source_edge_provenance(self):
        result = project_report_recon(
            {"a": {"T1059"}, "b": {"T1105"}, "c": {"T1059"}, "d": {"T1105"}},
            [
                TemporalEdge("r1", "a", "b", "BEFORE"),
                TemporalEdge("r2", "c", "d", "BEFORE"),
                TemporalEdge("r3", "b", "c", "BEFORE"),
            ],
        )
        # The technique projection has T1059 -> T1105 and T1105 -> T1059.
        self.assertGreaterEqual(result["counts"]["projected_strict_order_cycle_components"], 1)
        prov = result["strict_order_cycle_analysis"]["projected_cycle_provenance"][0]
        self.assertGreaterEqual(prov["source_event_edge_count"], 2)
        self.assertFalse(prov["single_event_edge_mapping_fanout"])

    def test_cycle_from_single_event_edge_mapping_fanout_is_flagged(self):
        result = project_report_recon(
            {"a": {"T1059", "T1105"}, "b": {"T1059", "T1105"}},
            [TemporalEdge("r1", "a", "b", "BEFORE")],
        )
        # Cartesian expansion of a single relation can create reciprocal pair edges.
        fanout = [x for x in result["strict_order_cycle_analysis"]["projected_cycle_provenance"] if x["single_event_edge_mapping_fanout"]]
        self.assertTrue(fanout)

    def test_redundant_source_edge_does_not_hide_single_edge_fanout(self):
        result = project_report_recon(
            {"a": {"T1059", "T1105"}, "b": {"T1059", "T1105"}},
            [
                TemporalEdge("r1", "a", "b", "BEFORE"),
                TemporalEdge("r2", "a", "b", "BEFORE"),
            ],
        )
        component = result["strict_order_cycle_analysis"]["projected_cycle_provenance"][0]
        self.assertEqual(component["source_event_edge_count"], 2)
        self.assertEqual(component["single_source_edges_inducing_cycle"], ["r1", "r2"])
        self.assertTrue(component["single_event_edge_mapping_fanout"])
        self.assertEqual(result["counts"]["projected_cycle_components_with_multiple_source_edges"], 1)
        self.assertEqual(result["counts"]["projected_cycle_components_requiring_multiple_source_edges"], 0)

    def test_before_and_inverse_after_are_not_a_label_conflict(self):
        result = project_report_recon(
            {"a": {"T1059"}, "b": {"T1105"}},
            [
                TemporalEdge("r1", "a", "b", "BEFORE"),
                TemporalEdge("r2", "b", "a", "AFTER"),
            ],
        )
        self.assertEqual(result["counts"]["distinct_pair_label_conflicts"], 0)
        self.assertTrue(result["strict_order_cycle_analysis"]["source_event_graph_is_acyclic"])

    def test_before_and_overlap_remain_a_label_conflict(self):
        result = project_report_recon(
            {"a": {"T1059"}, "b": {"T1105"}},
            [
                TemporalEdge("r1", "a", "b", "BEFORE"),
                TemporalEdge("r2", "a", "b", "OVERLAP"),
            ],
        )
        self.assertEqual(result["counts"]["distinct_pair_label_conflicts"], 1)

    def test_source_event_cycle_makes_projection_cycle_diagnostic_invalid(self):
        result = project_report_recon(
            {"a": {"T1059"}, "b": {"T1105"}},
            [TemporalEdge("r1", "a", "b", "BEFORE"), TemporalEdge("r2", "b", "a", "BEFORE")],
        )
        self.assertFalse(result["strict_order_cycle_analysis"]["source_event_graph_is_acyclic"])
        self.assertFalse(result["strict_order_cycle_analysis"]["projection_cycle_analysis_valid"])

    def test_nonpositive_and_non_direct_edges_rejected(self):
        with self.assertRaises(ValueError):
            project_report_recon({"a": {"T1059"}, "b": {"T1105"}}, [TemporalEdge("x", "a", "b", "NO_TEMPORAL_CLAIM")])
        with self.assertRaises(ValueError):
            project_report_recon({"a": {"T1059"}, "b": {"T1105"}}, [TemporalEdge("x", "a", "b", "BEFORE", relation_basis="inference")])
        with self.assertRaises(ValueError):
            project_report_recon({"a": {"T1059"}, "b": {"T1105"}}, [TemporalEdge("x", "a", "b", "BEFORE", scope_compatibility="UNCERTAIN")])

    def test_mapping_adapter_excludes_alternative_workbook_and_out_of_vocab(self):
        rows = [
            TechniqueMapping("m1", "e1", "T1059", "ACCEPTED", "report_explicit_parent", "IN_VOCAB"),
            TechniqueMapping("m2", "e1", "T1105", "ALTERNATIVE", "report_explicit_parent", "IN_VOCAB"),
            TechniqueMapping("m3", "e2", "T1059", "ACCEPTED", "workbook_only", "IN_VOCAB"),
            TechniqueMapping("m4", "e2", "T9999", "ACCEPTED", "report_explicit_parent", "OUT_OF_VOCAB"),
            TechniqueMapping("m5", "container", "T1113", "ACCEPTED", "report_explicit_parent", "IN_VOCAB"),
        ]
        sets, stats = build_a120_mapping_sets(rows, VOCAB, {"e1", "e2"})
        self.assertEqual(sets, {"e1": {"T1059"}, "e2": set()})
        self.assertEqual(stats["accepted_a120_mapping_rows"], 1)
        self.assertEqual(stats["excluded_nonaccepted"], 1)
        self.assertEqual(stats["excluded_unsupported_basis"], 1)
        self.assertEqual(stats["excluded_out_of_vocab_or_unresolved"], 1)
        self.assertEqual(stats["excluded_non_event_unit"], 1)

    def test_duplicate_mapping_id_rejected(self):
        duplicate = TechniqueMapping("m1", "e1", "T1059", "ACCEPTED", "report_explicit_parent", "IN_VOCAB")
        with self.assertRaisesRegex(ValueError, "Duplicate mapping_id"):
            build_a120_mapping_sets([duplicate, duplicate], VOCAB, {"e1"})

    def test_zero_edges_returns_null_edge_rates(self):
        result = project_report_recon({"e1": {"T1059"}}, [])
        self.assertEqual(result["counts"]["positive_temporal_edges"], 0)
        self.assertIsNone(result["rates"]["full_omission_rate_mapped_edges"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
