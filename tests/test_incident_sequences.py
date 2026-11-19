import copy
import json
import unittest

from scripts.analyze_incident_sequences import CASE, analyze
from src.occurrence_queries import evaluate_with_coverage


class IncidentSequenceTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(CASE.read_text(encoding="utf-8"))
        self.selection = json.loads((CASE.parent / "selection.json").read_text(encoding="utf-8"))

    def results(self):
        return analyze(self.case, self.selection)

    def test_recorded_results_reproduce(self):
        recorded = json.loads((CASE.parent / "results.json").read_text(encoding="utf-8"))
        self.assertEqual(json.loads(json.dumps(self.results())), recorded)

    def test_core_case_is_an_ordinary_success_for_all_representations(self):
        p = self.results()["profiles"]["core_transfer_execution"]
        self.assertEqual(len(p["source_paths"]), 1)
        self.assertEqual(p["path_mapping_coverage"], 1)
        for model in p["representations"].values():
            self.assertEqual(model["returned_queries"], [("T1021", "T1570", "T1218")])
            self.assertEqual(model["unsupported_queries"], [])
            self.assertEqual(model["missed_queries"], [])

    def test_extended_graph_has_one_join_error_and_no_diagonal_loss(self):
        p = self.results()["profiles"]["extended_script_sequence"]
        self.assertEqual(len(p["source_paths"]), 4)
        for name in ("distinct_pairs", "loop_pairs"):
            self.assertEqual(p["representations"][name]["unsupported_queries"], [("T1560", "T1059", "T1560")])
            self.assertEqual(p["representations"][name]["missed_queries"], [])
        for name in ("distinct_pairs_with_endpoint_join", "loop_pairs_with_endpoint_join"):
            self.assertEqual(p["representations"][name]["unsupported_queries"], [])
            self.assertEqual(len(p["representations"][name]["returned_queries"]), 4)

    def test_exact_mapping_sensitivity_retains_the_same_failure(self):
        p = self.results()["profiles"]["extended_exact_techniques"]
        self.assertEqual(p["representations"]["distinct_pairs"]["unsupported_queries"], [("T1560.001", "T1059.003", "T1560.001")])

    def test_partial_mapping_coverage_does_not_score_hidden_paths_as_absent(self):
        p = self.results()["profiles"]["archive_mapping_withheld"]
        self.assertEqual(p["path_mapping_coverage"], 0.5)
        self.assertEqual(len(p["fully_mapped_source_paths"]), 2)
        for model in p["representations"].values():
            self.assertIsNone(model["unsupported_queries"])
            self.assertIsNone(model["missed_queries"])

    def test_source_selection_and_mapping_cannot_silently_change(self):
        changed = copy.deepcopy(self.case)
        changed["source"]["url"] = "https://example.org/other"
        with self.assertRaises(ValueError):
            analyze(changed, self.selection)
        changed = copy.deepcopy(self.case)
        changed["occurrences"][0]["candidate_parent_mapping"] = "T9999"
        with self.assertRaises(ValueError):
            analyze(changed, self.selection)

    def test_unknown_evidence_scope_cycle_and_profile_endpoint_fail(self):
        cases = [copy.deepcopy(self.case) for _ in range(4)]
        cases[0]["relations"][0]["evidence_ids"] = ["missing"]
        cases[1]["occurrences"][0]["incident_id"] = "another-case"
        cases[2]["relations"].append(dict(cases[2]["relations"][0], relation_id="reverse", source_event="transfer_beacon", target_event="rdp_dc"))
        cases[3]["profiles"][0]["occurrence_ids"].pop()
        for case in cases:
            with self.assertRaises(ValueError):
                analyze(case, self.selection)

    def test_no_path_is_unassessed_and_isolated_unmapped_node_is_not_a_path(self):
        self.assertIsNone(evaluate_with_coverage({"u": {"A"}}, set())["path_mapping_coverage"])
        p = evaluate_with_coverage({"u": {"A"}, "v": {"B"}, "w": {"C"}, "isolated": set()}, {("u", "v"), ("v", "w")})
        self.assertEqual(p["path_mapping_coverage"], 1)
        self.assertEqual(p["representations"]["distinct_pairs"]["unsupported_queries"], [])


if __name__ == "__main__":
    unittest.main()
