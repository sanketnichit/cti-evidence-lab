import json
import unittest
from pathlib import Path

from examples.query_fidelity_benchmark import counterexamples, run_benchmark
from examples.representation_controls import edge, project_report_recon
from src.occurrence_queries import evaluate


class OccurrenceQueryTests(unittest.TestCase):
    def test_identical_pair_graphs_have_different_connected_answers(self):
        cases = counterexamples()
        disconnected = cases["disconnected_occurrences"]
        connected = cases["connected_occurrences_same_technique_graph"]
        self.assertEqual(disconnected["storage"], connected["storage"])
        self.assertEqual(disconnected["answers"]["loop_pairs"], connected["answers"]["loop_pairs"])
        self.assertEqual(disconnected["source_answers"], [])
        self.assertEqual(len(connected["source_answers"]), 1)
        self.assertEqual(disconnected["answers"]["loop_pairs_with_endpoint_join"], [])

    def test_self_loop_cannot_be_reused_as_second_occurrence_edge(self):
        case = counterexamples()["single_edge_reused_as_two_hops"]
        self.assertEqual(len(case["answers"]["loop_pairs"]), 1)
        self.assertEqual(case["answers"]["loop_pairs_with_endpoint_join"], [])

    def test_diagonal_removal_is_a_separate_recall_failure(self):
        case = counterexamples()["genuine_repeated_technique_chain"]
        self.assertEqual(case["answers"]["distinct_pairs_with_endpoint_join"], [])
        self.assertEqual(case["answers"]["loop_pairs_with_endpoint_join"], case["source_answers"])
        self.assertEqual(len(case["source_answers"]), 1)

    def test_empty_mapping_is_not_a_false_technique_negative(self):
        result = evaluate({"a": {"T1059"}, "b": set(), "c": {"T1105"}}, [("a", "b"), ("b", "c")])
        self.assertEqual(result["truth"], set())
        self.assertEqual(result["storage"]["source_edges"], 2)
        self.assertEqual(result["storage"]["endpoint_rows"], 0)

    def test_cycle_and_unknown_endpoint_fail_closed(self):
        for edges in [[("a", "b"), ("b", "a")], [("a", "a")], [("a", "missing")]]:
            with self.assertRaises(ValueError):
                evaluate({"a": {"T1059"}, "b": {"T1105"}}, edges)

    def test_label_and_occurrence_renaming_preserve_answers(self):
        a = evaluate({"a": {"T1059", "T1105"}, "b": {"T1105"}, "c": {"T1021"}}, [("a", "b"), ("b", "c")])
        b = evaluate({"y": {"Y"}, "z": {"Z"}, "x": {"X", "Y"}}, [("y", "z"), ("x", "y")])
        labels = {"T1059": "X", "T1105": "Y", "T1021": "Z"}
        for name, answers in a["answers"].items():
            self.assertEqual({tuple(labels[t] for t in q) for q in answers}, b["answers"][name])

    def test_pair_counts_match_existing_projection_on_counterexamples(self):
        for case in counterexamples().values():
            mappings = {k: set(v) for k, v in case["mappings"].items()}
            edges = [edge(str(i), u, v) for i, (u, v) in enumerate(case["before_edges"])]
            original = project_report_recon(mappings, edges)
            self.assertEqual(case["storage"]["distinct_pair_keys"], original["counts"]["unique_distinct_technique_pairs"])

    def test_exhaustive_outputs_and_fidelity_invariants(self):
        result = run_benchmark()
        path = Path(__file__).resolve().parents[1] / "research/experiments/query_fidelity_v0.1/results.json"
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), json.loads(json.dumps(result)))
        self.assertEqual(result["designs"]["four_vertices_singleton_mappings"]["graphs"], 5184)
        self.assertEqual(result["designs"]["three_vertices_set_valued_mappings"]["graphs"], 4096)
        for design in result["designs"].values():
            for stratum, models in design["confusion"].items():
                for model, counts in models.items():
                    self.assertEqual(sum(counts[k] for k in ("tp", "fp", "fn", "tn")), design["graphs"] * design["queries_per_graph"][stratum])
                    if "endpoint_join" in model:
                        self.assertEqual(counts["fp"], 0)
                    if model.startswith("loop_pairs") or stratum == "distinct_adjacent_labels":
                        self.assertEqual(counts["fn"], 0)


if __name__ == "__main__":
    unittest.main()
