import copy
import json
import unittest
from pathlib import Path

from examples.investigation_benchmark import run_checks
from scripts.investigate_sequence import certificate, load_case, verify_certificate
from src.sequence_investigation import investigate


def edge(key, u, v):
    return dict(relation_id=key, source_event=u, target_event=v, relation="BEFORE")


class InvestigationTests(unittest.TestCase):
    def test_disconnected_join_identifies_both_distinct_middle_occurrences(self):
        r = investigate({"u": {"A"}, "v": {"B"}, "w": {"B"}, "x": {"C"}}, [edge("uv", "u", "v"), edge("wx", "w", "x")], ["A", "B", "C"])
        self.assertEqual(r["status"], "NOT_SUPPORTED")
        p = r["projection_comparisons"]["distinct_pairs"]
        self.assertTrue(p["unsupported_positive"])
        self.assertEqual(p["incompatible_joins"][0]["left_occurrences"], ["u", "v"])
        self.assertEqual(p["incompatible_joins"][0]["right_occurrences"], ["w", "x"])

    def test_unknown_mapping_is_query_specific(self):
        m = {"u": {"A"}, "v": set(), "w": {"C"}}
        e = [edge("uv", "u", "v"), edge("vw", "v", "w")]
        self.assertEqual(investigate(m, e, ["A", "B", "C"])["status"], "UNRESOLVED_MAPPING")
        self.assertEqual(investigate(m, e, ["C", "B", "A"])["status"], "NOT_SUPPORTED")

    def test_known_support_survives_another_unmapped_path(self):
        m = {"u": {"A"}, "v": {"B"}, "w": {"C"}, "x": set()}
        r = investigate(m, [edge("uv", "u", "v"), edge("vw", "v", "w"), edge("ux", "u", "x"), edge("xw", "x", "w")], ["A", "B", "C"])
        self.assertEqual(r["status"], "SUPPORTED")
        self.assertEqual(len(r["known_witnesses"]), 1)
        self.assertEqual(len(r["unresolved_witnesses"]), 1)

    def test_diagonal_loss_has_a_real_occurrence_witness(self):
        r = investigate({"u": {"A"}, "v": {"A"}, "w": {"B"}}, [edge("uv", "u", "v"), edge("vw", "v", "w")], ["A", "A", "B"])
        self.assertEqual(r["status"], "SUPPORTED")
        self.assertTrue(r["projection_comparisons"]["distinct_pairs"]["diagonal_suppression"])
        self.assertTrue(r["projection_comparisons"]["loop_pairs"]["returned"])

    def test_reusing_one_edge_is_not_three_occurrences(self):
        r = investigate({"u": {"A"}, "v": {"A"}}, [edge("uv", "u", "v")], ["A", "A", "A"])
        self.assertIn("REUSED_EDGE_IMAGE", r["projection_comparisons"]["loop_pairs"]["incompatible_joins"][0]["reasons"])
        self.assertEqual(r["status"], "NOT_SUPPORTED")

    def test_multiple_mappings_and_duplicate_relation_ids(self):
        m = {"u": {"A", "X"}, "v": {"B"}, "w": {"C"}}
        e = [edge("uv", "u", "v"), edge("vw", "v", "w")]
        self.assertEqual(investigate(m, e, ["X", "B", "C"])["status"], "SUPPORTED")
        with self.assertRaises(ValueError):
            investigate(m, e + [e[0]], ["A", "B", "C"])

    def test_cycle_unknown_endpoint_and_non_temporal_edge_rejected(self):
        for e in ([edge("uv", "u", "v"), edge("vu", "v", "u")], [edge("ux", "u", "x")], [dict(edge("uv", "u", "v"), relation="DEPENDS_ON")]):
            with self.assertRaises(ValueError):
                investigate({"u": {"A"}, "v": {"B"}}, e, ["A", "B", "C"])

    def test_real_case_certificate_recomputes_and_tampering_fails(self):
        c = certificate("domain-controller", load_case("domain-controller"), "extended_script_sequence", ["T1560", "T1059", "T1560"])
        self.assertTrue(verify_certificate(c))
        changed = copy.deepcopy(c)
        changed["answer"]["status"] = "SUPPORTED"
        with self.assertRaises(ValueError):
            verify_certificate(changed)
        c["evidence"][0]["char_start"] += 1
        with self.assertRaises(ValueError):
            verify_certificate(c)

    def test_core_query_remains_supported_with_archive_mapping_withheld(self):
        c = certificate("domain-controller", load_case("domain-controller"), "archive_mapping_withheld", ["T1021", "T1570", "T1218"])
        self.assertEqual(c["answer"]["status"], "SUPPORTED")
        self.assertEqual(c["answer"]["unresolved_witnesses"], [])

    def test_exhaustive_completion_oracle_and_recorded_result(self):
        result = run_checks()
        self.assertEqual(result["finite_query_checks"], 1728)
        path = Path(__file__).resolve().parents[1] / "research/experiments/investigation_v0.1/results.json"
        self.assertEqual(result, json.loads(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
