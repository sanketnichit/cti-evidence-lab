import json
import unittest

from examples.representation_controls import ROOT, compare, edge, markdown, run_controls


class RepresentationControlsTests(unittest.TestCase):
    def test_committed_tables_reproduce(self):
        folder = ROOT / "research/experiments/representation_controls_v0.1"
        result = run_controls()
        self.assertEqual(json.loads((folder / "results.json").read_text(encoding="utf-8")), result)
        self.assertEqual((folder / "README.md").read_text(encoding="utf-8"), markdown(result))

    def test_loop_retention_is_not_occurrence_retention(self):
        case = run_controls()["cases"]["repeated_same_technique"]
        self.assertEqual(case["primary"]["counts"]["fully_omitted_edges"], 2)
        self.assertEqual(case["loop_permitting"]["unique_labeled_pairs"], 1)
        self.assertEqual(case["loop_permitting"]["collision_keys"], 1)
        self.assertEqual(case["occurrence_preserving"]["edges"], 2)

    def test_missing_mapping_is_not_diagonal_omission(self):
        case = run_controls()["cases"]["unmapped_endpoint"]
        self.assertEqual(case["primary"]["counts"]["unmapped_endpoint_edges"], 1)
        self.assertEqual(case["primary"]["counts"]["fully_omitted_edges"], 0)
        self.assertIsNone(case["primary"]["rates"]["full_omission_rate_mapped_edges"])
        self.assertEqual(case["loop_permitting"]["source_edges_with_any_image"], 0)

    def test_distinct_mechanisms_produce_projected_cycles(self):
        cases = run_controls()["cases"]
        for name in ("occurrence_collapse_cycle", "single_edge_fanout_cycle"):
            c = cases[name]["primary"]["counts"]
            self.assertEqual(c["source_strict_order_cycle_components"], 0)
            self.assertEqual(c["projected_strict_order_cycle_components"], 1)
        self.assertEqual(cases["occurrence_collapse_cycle"]["primary"]["counts"]["projected_cycle_components_requiring_multiple_source_edges"], 1)
        self.assertEqual(cases["single_edge_fanout_cycle"]["primary"]["counts"]["projected_cycle_components_from_single_edge_fanout"], 1)

    def test_inverse_and_symmetric_labels_share_keys_but_not_other_labels(self):
        mappings = {"a": {"T1021"}, "b": {"T1105"}}
        case = compare(mappings, [edge("x", "a", "b"), edge("y", "b", "a", "AFTER"),
                                  edge("z", "b", "a", "OVERLAP"), edge("w", "a", "b", "OVERLAP")])
        self.assertEqual(case["loop_permitting"]["unique_labeled_pairs"], 2)
        self.assertEqual(case["loop_permitting"]["collision_keys"], 2)


if __name__ == "__main__":
    unittest.main()
