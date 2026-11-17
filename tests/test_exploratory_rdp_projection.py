"""The published-source illustration stays separate from research results."""
import unittest

from examples.exploratory_rdp_projection import run_example


class RdpProjectionIllustrationTests(unittest.TestCase):
    def test_example_is_not_accepted_as_an_empirical_result(self):
        result = run_example()
        self.assertEqual(result["status"], "CONDITIONAL_DEMONSTRATION_NOT_ANNOTATION")
        self.assertEqual(result["sample_membership"], "OUTSIDE_ANNOCTR_PILOT")
        self.assertFalse(result["human_reviewed"])
        self.assertFalse(result["eligible_for_empirical_denominators"])
        self.assertEqual(len(result["assumptions"]), 5)

    def test_two_conditional_occurrences_have_no_distinct_technique_edge(self):
        projection = run_example()["conditional_projection"]
        counts = projection["counts"]
        self.assertEqual(counts["resolved_event_instances"], 2)
        self.assertEqual(counts["unique_techniques"], 1)
        self.assertEqual(counts["positive_temporal_edges"], 1)
        self.assertEqual(counts["fully_omitted_edges"], 1)
        self.assertEqual(counts["unique_distinct_technique_pairs"], 0)
        self.assertEqual(
            projection["projection"]["edge_to_diagonal_pairs"]["attempt_order"],
            [["T1021", "T1021"]])
        self.assertEqual(
            projection["projection"]["edge_to_distinct_pairs"]["attempt_order"],
            [])
        self.assertTrue(
            projection["strict_order_cycle_analysis"]["source_event_graph_is_acyclic"])


if __name__ == "__main__":
    unittest.main()
