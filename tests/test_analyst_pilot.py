import unittest
from collections import Counter

from scripts.analyst_pilot import GROUPS, packet, response_template, score, summarize


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

    def completed_response(self, group, participant, abstain=False):
        _, key = packet(group)
        response = response_template(group, key)
        response["participant_id"] = participant
        for row in response["responses"]:
            expected = key[row["task"]]
            row["status"] = "CANNOT_TELL" if abstain else expected["status"]
            row["relation_ids"] = [] if abstain else next(iter(expected["witnesses"]), [])
        return response

    def test_technique_view_keeps_unknown_mapping_relation_ids(self):
        body, _ = packet("A")
        self.assertIn("UNKNOWN means the technique mapping is unconfirmed", body)
        self.assertTrue("→ UNKNOWN" in body or "UNKNOWN →" in body)
        self.assertIn("Relation locators", body)

    def test_summarize_complete_counterbalanced_participants(self):
        responses = [
            self.completed_response(group, f"P-{index}")
            for index, group in enumerate(GROUPS, 1)
        ]
        result = summarize(responses)
        self.assertEqual(result["participants"], 4)
        self.assertEqual(result["packet_balance"], {group: 1 for group in GROUPS})
        self.assertEqual(result["complete_four_packet_rotations"], 1)
        self.assertEqual(result["participants_in_incomplete_rotation"], 0)
        self.assertEqual(result["overall"]["assigned"], 32)
        self.assertEqual(result["overall"]["status_correct"], 32)
        self.assertEqual(result["overall"]["witness_assigned"], 16)
        self.assertEqual(result["overall"]["status_and_witness_correct"], 16)
        self.assertEqual(result["by_view"]["occurrence"]["assigned"], 16)
        self.assertEqual(result["by_view"]["technique"]["assigned"], 16)
        self.assertEqual(result["by_case"]["rdp"]["assigned"], 16)
        self.assertEqual(result["by_block_order"]["1"]["assigned"], 16)
        for participant in result["per_participant"]:
            self.assertEqual(participant["occurrence_minus_technique_status_accuracy"], 0)
            self.assertEqual(participant["occurrence_minus_technique_witness_accuracy"], 0)

    def test_summarize_keeps_abstentions_and_incomplete_rotations(self):
        responses = [self.completed_response("A", "P1"),
                     self.completed_response("B", "P2", abstain=True)]
        result = summarize(responses)
        self.assertEqual(result["participants"], 2)
        self.assertEqual(result["complete_four_packet_rotations"], 0)
        self.assertEqual(result["participants_in_incomplete_rotation"], 2)
        self.assertEqual(result["overall"]["assigned"], 16)
        self.assertEqual(result["overall"]["cannot_tell"], 8)
        self.assertEqual(result["overall"]["status_correct"], 8)
        self.assertEqual(result["overall"]["witness_assigned"], 8)
        self.assertEqual(result["overall"]["status_and_witness_correct"], 4)

    def test_summarize_requires_real_complete_anonymous_unique_packets(self):
        with self.assertRaisesRegex(ValueError, "At least one"):
            summarize([])
        first = self.completed_response("A", "P1")
        with self.assertRaisesRegex(ValueError, "Duplicate participant_id"):
            summarize([first, first])
        no_id = self.completed_response("B", "P2")
        del no_id["participant_id"]
        with self.assertRaisesRegex(ValueError, "anonymous participant_id"):
            summarize([no_id])
        incomplete = self.completed_response("C", "P3")
        incomplete["responses"].pop()
        with self.assertRaisesRegex(ValueError, "exactly once"):
            summarize([incomplete])

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
