import json
import unittest

from examples.profile_coherence import witness_masks
from scripts.compare_sequence_profiles import compare_query, export, verify


def before(identifier, u, v):
    return {"relation_id": identifier, "relation": "BEFORE", "source_event": u, "target_event": v}


class ProfileComparisonTests(unittest.TestCase):
    def test_focused_masks_keep_witness_identity_under_completion_and_union_cycles(self):
        query = ("A", "A", "B")
        profiles = (
            ({"u": {"A", "B"}, "v": set(), "w": {"B"}}, {("u", "v"), ("v", "w")}),
            ({"u": {"A"}, "v": {"A"}, "w": {"B"}}, {("v", "u")}),
        )
        for vocabulary in ((), query):
            expected = {key: mask for key, mask in witness_masks(
                profiles, completion_vocabulary=vocabulary).items() if key[1] == query}
            self.assertEqual(witness_masks(profiles, completion_vocabulary=vocabulary, query=query), expected)
        self.assertEqual(witness_masks(profiles, completion_vocabulary=query, query=query),
                         {(("u", "v", "w"), query): 1})

    def test_pooled_known_witness_can_be_possible_in_one_profile(self):
        known = {"u": {"A"}, "v": {"B"}, "w": {"C"}}
        earlier = before("B1", "u", "v")
        later = before("B2", "v", "w")
        result = compare_query({
            "full_path": ({**known, "v": set()}, [earlier, later]),
            "known_label": (known, [earlier]),
        }, ["A", "B", "C"])
        self.assertEqual(result["best_profile_status"], "UNRESOLVED_MAPPING")
        self.assertEqual(result["pooled_status"], "SUPPORTED")
        self.assertEqual(result["pooled_witnesses"]["known"][0]["conflict"]["minimum_conflicts"], [[2, 4]])
        self.assertEqual(result["pooled_witnesses"]["possible"][0]["supporting_profiles"], ["full_path"])

    def test_record_verifies_and_detects_changed_witness(self):
        record = json.loads(json.dumps(export("netsupport-identity", ["T1562", "T1047", "T1053"])))
        self.assertEqual(record["answer"]["pooled_witnesses"]["known"][0]["supporting_profiles"],
                         ["co_referent_execution"])
        verify(record)
        record["answer"]["pooled_witnesses"]["known"][0]["supporting_profiles"].append("recorded")
        with self.assertRaises(ValueError):
            verify(record)

    def test_compact_export_retains_pooled_details_and_verifies_its_counts(self):
        query = ("T1562", "T1047", "T1053")
        full = export("netsupport-identity", query)["answer"]
        record = export("netsupport-identity", query, summary_only=True)
        verify(record)
        compact = record["answer"]
        self.assertEqual(compact["pooled_witnesses"], full["pooled_witnesses"])
        for name, row in full["profile_answers"].items():
            summary = compact["profile_answers"][name]
            self.assertEqual(summary["status"], row["status"])
            self.assertEqual(summary["known_witness_count"], len(row["known_witnesses"]))
        del record["detail"]
        with self.assertRaises(ValueError):
            verify(record)
