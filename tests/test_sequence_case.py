import copy
import json
import unittest

from scripts.analyze_sequence_case import CASE, analyze


class SequenceCaseTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(CASE.read_text(encoding="utf-8"))

    def test_results_reproduce(self):
        recorded = json.loads((CASE.parent / "results.json").read_text(encoding="utf-8"))
        self.assertEqual(recorded, json.loads(json.dumps(analyze(self.case))))

    def test_mapping_uncertainty_does_not_become_perfect_fidelity(self):
        p = analyze(self.case)["profiles"]["unresolved_cleanup"]
        self.assertEqual(len(p["source_paths"]), 3)
        self.assertEqual(p["path_mapping_coverage"], 0)
        self.assertTrue(p["assessment_status"].startswith("NOT_ASSESSED"))
        for r in p["representations"].values():
            self.assertIsNone(r["unsupported_queries"])
            self.assertIsNone(r["missed_queries"])

    def test_full_edge_profile_distinguishes_precision_and_recall_errors(self):
        p = analyze(self.case)["profiles"]["proposed_cleanup_full_edges"]
        self.assertEqual(p["path_mapping_coverage"], 1)
        self.assertEqual(len(p["supported_queries_from_mapped_paths"]), 3)
        r = p["representations"]
        self.assertEqual(len(r["distinct_pairs"]["missed_queries"]), 1)
        self.assertEqual(len(r["loop_pairs"]["unsupported_queries"]), 2)
        self.assertEqual(r["loop_pairs_with_endpoint_join"]["unsupported_queries"], [])
        self.assertEqual(r["loop_pairs_with_endpoint_join"]["missed_queries"], [])

    def test_local_edge_profile_retains_ordinary_correct_answers(self):
        p = analyze(self.case)["profiles"]["proposed_cleanup_local_edges"]
        self.assertEqual(len(p["source_paths"]), 2)
        for r in p["representations"].values():
            self.assertEqual(r["unsupported_queries"], [])
            self.assertEqual(r["missed_queries"], [])

    def test_no_opportunity_is_not_a_zero_error_result(self):
        p = analyze(self.case)["profiles"]["reported_completed_actions"]
        self.assertEqual(p["source_paths"], [])
        self.assertIsNone(p["path_mapping_coverage"])
        self.assertIsNone(p["representations"]["distinct_pairs"]["missed_queries"])

    def test_unresolved_scope_or_missing_evidence_is_rejected(self):
        for field, value in [("incident_id", "other-incident"), ("evidence_ids", ["missing"])]:
            case = copy.deepcopy(self.case)
            case["occurrences"][0][field] = value
            with self.assertRaises(ValueError):
                analyze(case)

    def test_cyclic_input_duplicate_profile_and_implicit_assumption_fail(self):
        cases = [copy.deepcopy(self.case) for _ in range(3)]
        cases[0]["relations"].append(dict(cases[0]["relations"][0], relation_id="cycle", source_event="rdp_attempt_2", target_event="rdp_attempt_1"))
        cases[1]["profiles"].append(copy.deepcopy(cases[1]["profiles"][0]))
        cases[2]["profiles"][0]["assume_cleanup_mapping"] = "false"
        for case in cases:
            with self.assertRaises(ValueError):
                analyze(case)


if __name__ == "__main__":
    unittest.main()
