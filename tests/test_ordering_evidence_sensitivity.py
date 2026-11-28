import unittest

from examples.ordering_evidence_sensitivity import evaluate


class OrderingEvidenceSensitivityTests(unittest.TestCase):
    def test_shared_source_unit_can_remove_both_alternative_witnesses(self):
        mappings = {"a": {"A"}, "b1": {"B"}, "b2": {"B"}, "c": {"C"}}
        relations = [
            {"relation_id": identifier, "source_event": first, "target_event": last, "evidence_ids": [citation]}
            for identifier, first, last, citation in (
                ("r1", "a", "b1", "s1"), ("r2", "a", "b2", "s2"),
                ("r3", "b1", "c", "s3"), ("r4", "b2", "c", "s4"),
            )
        ]
        evidence = [{"evidence_id": identifier, "page": page}
                    for identifier, page in (("s1", 1), ("s2", 1), ("s3", 2), ("s4", 3))]
        result = evaluate(mappings, relations, evidence)
        self.assertEqual(result["known_witnesses"], 2)
        self.assertEqual(result["single_row"]["fragile_supported_queries"], [])
        removed = result["source_unit"]["interventions"]["page 1"]
        self.assertEqual(removed["removed_rows"], ["r1", "r2"])
        self.assertEqual(removed["supported_to_unsupported"], [("A", "B", "C")])
        self.assertEqual(result["last_citation_overrides"], {})

    def test_last_citation_rule_counts_unique_source_units(self):
        mappings = {"a": {"A"}, "b": {"B"}, "c": {"C"}}
        relations = [
            {"relation_id": "r1", "source_event": "a", "target_event": "b", "evidence_ids": ["s1", "s2", "s3"]},
            {"relation_id": "r2", "source_event": "b", "target_event": "c", "evidence_ids": ["s4", "s5"]},
        ]
        evidence = [{"evidence_id": identifier, "page": page}
                    for identifier, page in (("s1", 1), ("s2", 1), ("s3", 2), ("s4", 3), ("s5", 3))]
        result = evaluate(mappings, relations, evidence)
        self.assertEqual(set(result["last_citation_overrides"]), {"page 1", "page 2"})
        self.assertEqual(result["source_unit"]["interventions"]["page 1"]["supported_to_unsupported"],
                         [("A", "B", "C")])
        self.assertEqual(result["last_citation_overrides"]["page 1"]["removed_rows"], [])
        self.assertEqual(result["last_citation_overrides"]["page 1"]["supported_to_unsupported"], [])
        self.assertEqual(result["source_unit"]["interventions"]["page 3"]["removed_rows"], ["r2"])

        evidence[-1]["page"] = 4
        cuts = evaluate(mappings, relations, evidence)["minimum_source_unit_cuts"]
        self.assertEqual(cuts, [{"query": ("A", "B", "C"), "first_citation": ("page 1",),
                                 "last_citation": ("page 1", "page 2")}])
