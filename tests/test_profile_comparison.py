import json
import unittest

from scripts.compare_sequence_profiles import compare_query, export, verify


def before(identifier, u, v):
    return {"relation_id": identifier, "relation": "BEFORE", "source_event": u, "target_event": v}


class ProfileComparisonTests(unittest.TestCase):
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
