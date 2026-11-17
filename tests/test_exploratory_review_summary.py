import copy
import hashlib
import json
import unittest

from scripts.summarize_exploratory_review import DEFAULT, summarize


class ExploratoryReviewTests(unittest.TestCase):
    def setUp(self):
        self.decisions = json.loads((DEFAULT / "review_decisions.json").read_text(encoding="utf-8"))
        self.audit = json.loads((DEFAULT / "source_integrity.json").read_text(encoding="utf-8"))

    def test_committed_summary_matches_inputs(self):
        expected = summarize(self.decisions, self.audit)
        expected["input_sha256"] = {name: hashlib.sha256((DEFAULT / name).read_bytes()).hexdigest()
                                    for name in ("review_decisions.json", "source_integrity.json")}
        self.assertEqual(json.loads((DEFAULT / "results.json").read_text(encoding="utf-8")), expected)

    def test_unresolved_is_not_zero_prevalence(self):
        result = summarize(self.decisions, self.audit)
        self.assertEqual(result["reviewed_text_reports"], 5)
        self.assertIsNone(result["empirical_prevalence"])
        self.assertIsNone(result["inter_annotator_agreement"])
        self.assertEqual(result["formal_annotation_partitions_created"], 0)

    def test_rejects_stale_or_untraceable_review(self):
        for patch in ({"source_text_sha256": "0" * 64}, {"anchors": ["invented"]}, {"qualifying_pair": "CONFIRMED"}):
            decisions = copy.deepcopy(self.decisions)
            decisions["reports"][0].update(patch)
            with self.assertRaises(ValueError):
                summarize(decisions, self.audit)
        self.decisions["reports"].pop()
        with self.assertRaises(ValueError):
            summarize(self.decisions, self.audit)

    def test_positive_candidate_does_not_become_a_negative_or_formal_result(self):
        self.decisions["reports"][0]["qualifying_pair"] = "WITHIN_TECHNIQUE_PAIR_CANDIDATE"
        self.decisions["reports"][1]["qualifying_pair"] = "TEMPORAL_PAIR_CANDIDATE_MAPPING_UNRESOLVED"
        result = summarize(self.decisions, self.audit)
        self.assertEqual(result["reports_with_qualifying_pair_not_established"], 3)
        self.assertEqual(result["reports_with_within_technique_pair_candidate"], 1)
        self.assertEqual(result["reports_with_temporal_pair_candidate_mapping_unresolved"], 1)
        self.assertIsNone(result["empirical_prevalence"])


if __name__ == "__main__":
    unittest.main()
