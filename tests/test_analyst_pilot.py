import unittest
from collections import Counter

from scripts.analyst_pilot import GROUPS, packet, response_template, score


class AnalystPilotTests(unittest.TestCase):
    def test_assignment_crosses_case_view_and_block_order(self):
        counts = Counter((index, case, view) for blocks in GROUPS.values()
                         for index, (case, view) in enumerate(blocks))
        self.assertEqual(len(counts), 8)
        self.assertTrue(all(count == 1 for count in counts.values()))
        keys = {}
        for group in GROUPS:
            body, key = packet(group)
            self.assertEqual(len(key), 8)
            self.assertNotIn("first_removal_to_second_attempt", body)
            for view in ("technique", "occurrence"):
                self.assertEqual(Counter(t["status"] for t in key.values() if t["view"] == view),
                                 {"SUPPORTED": 1, "UNRESOLVED_MAPPING": 1, "NOT_SUPPORTED": 2})
            for task, item in key.items():
                signature = (item["status"], item["witnesses"])
                self.assertEqual(keys.setdefault(task, signature), signature)

    def test_scores_witnesses_and_abstention_separately(self):
        _, key = packet("A")
        response = response_template("A", key)
        for row in response["responses"]:
            expected = key[row["task"]]
            row["status"] = expected["status"]
            row["relation_ids"] = next(iter(expected["witnesses"]), [])
        correct = score(response)["items"]
        self.assertTrue(all(row["status_correct"] for row in correct))
        self.assertEqual(sum(row["status_and_witness_correct"] is True for row in correct), 4)
        response["responses"][0]["relation_ids"] = ["L999"]
        response["responses"][1].update(status="CANNOT_TELL", relation_ids=[])
        items = score(response)["items"]
        self.assertTrue(items[0]["status_correct"])
        self.assertFalse(items[0]["status_and_witness_correct"])
        self.assertTrue(items[1]["cannot_tell"])
        self.assertFalse(items[1]["status_correct"])
        response["responses"].reverse()
        with self.assertRaises(ValueError):
            score(response)
