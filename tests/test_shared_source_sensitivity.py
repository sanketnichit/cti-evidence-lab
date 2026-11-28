import unittest

from examples.shared_source_sensitivity import evaluate


class SharedSourceSensitivityTests(unittest.TestCase):
    def test_combined_omission_can_erase_support_that_survives_each_change(self):
        labels = {"u": {"A"}, "v": {"B"}, "w": {"C"}}
        profiles = {}
        for name, citation in (("first", "p1"), ("second", "p2")):
            profiles[name] = (labels, [
                {"relation_id": f"B{i}", "source_event": source, "target_event": target,
                 "relation": "BEFORE", "evidence_ids": [citation]}
                for i, (source, target) in enumerate((("u", "v"), ("v", "w")), start=1)
            ])
        record = {"evidence": [{"evidence_id": "p1", "paragraph_number": 1},
                               {"evidence_id": "p2", "paragraph_number": 2}]}
        result = evaluate(record, profiles)
        for value in result["joint"].values():
            self.assertEqual(value["survive_both_separate_interventions"], 4)
            self.assertEqual(
                [(row["paragraph"], row["omitted_profile"]) for row in value["joint_only_losses"]],
                [(1, "second"), (2, "first")],
            )
