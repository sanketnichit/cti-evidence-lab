import copy
import json
import unittest

from scripts.audit_rank_two_review import (
    DIRECTORY, digest, summarize, validate, validate_recorded_audit, verify_spans,
)


class RankTwoReviewTests(unittest.TestCase):
    def setUp(self):
        self.selection = json.loads((DIRECTORY / "selection.json").read_text(encoding="utf-8"))
        self.review = json.loads((DIRECTORY / "review.json").read_text(encoding="utf-8"))

    def test_committed_summary_reproduces_and_preserves_unassessed_errors(self):
        result = summarize(self.selection, self.review)
        self.assertEqual(result, json.loads((DIRECTORY / "results.json").read_text(encoding="utf-8")))
        self.assertEqual(result["selected_reports"], 5)
        self.assertEqual(result["reviewed_reports"], 5)
        self.assertEqual(result["evidence_bindings"], 22)
        self.assertIsNone(result["query_error_count"])

    def test_recorded_audit_is_bound_to_review_and_selection(self):
        recorded = json.loads((DIRECTORY / "source_integrity.json").read_text(encoding="utf-8"))
        validate_recorded_audit(self.selection, self.review, recorded)
        self.review["reports"][0]["remaining_resolution"] += " Changed interpretation."
        with self.assertRaises(ValueError):
            validate_recorded_audit(self.selection, self.review, recorded)

    def test_missing_or_duplicate_review_cannot_shrink_denominator(self):
        for reports in (self.review["reports"][:-1], self.review["reports"] + [self.review["reports"][0]]):
            changed = dict(self.review, reports=reports)
            with self.assertRaises(ValueError):
                validate(self.selection, changed)

    def test_selection_cannot_be_replaced_or_reseeded(self):
        for key, value in (("rank", 3), ("seed", "different"), ("frame_sha256", "0" * 64)):
            with self.assertRaises(ValueError):
                validate(dict(self.selection, **{key: value}), self.review)
        self.selection["reports"][0]["report_id"] = "different-report"
        with self.assertRaises(ValueError):
            validate(self.selection, self.review)

    def test_unresolved_review_cannot_become_zero_error_or_independent(self):
        for key, value in (("query_errors", 0), ("primary_sequence_status", "ESTABLISHED"), ("full_corpus_text_read", "true")):
            changed = copy.deepcopy(self.review)
            changed["reports"][0][key] = value
            with self.assertRaises(ValueError):
                validate(self.selection, changed)
        with self.assertRaises(ValueError):
            validate(self.selection, dict(self.review, independently_validated=True))

    def test_claims_require_known_evidence_and_matching_source(self):
        changed = copy.deepcopy(self.review)
        changed["reports"][0]["strongest_candidate"]["evidence_ids"] = ["missing"]
        with self.assertRaises(ValueError):
            validate(self.selection, changed)
        self.review["reports"][0]["source_text_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            validate(self.selection, self.review)

    def test_span_hash_offsets_and_line_identity_are_checked(self):
        text = "heading\nfirst action\nnext action\n"
        span = dict(evidence_id="E1", char_start=8, char_end=32, line_start=2, line_end=3, span_sha256=digest(text[8:32]))
        self.assertEqual(verify_spans(text, [span]), ["E1"])
        for key, value in (("char_start", 9), ("char_end", 99), ("line_start", 1), ("line_end", 4), ("span_sha256", "0" * 64)):
            with self.assertRaises(ValueError):
                verify_spans(text, [dict(span, **{key: value})])

    def test_recorded_audit_cannot_omit_a_report_or_binding(self):
        recorded = json.loads((DIRECTORY / "source_integrity.json").read_text(encoding="utf-8"))
        missing_report = copy.deepcopy(recorded)
        missing_report["sources"].pop()
        missing_binding = copy.deepcopy(recorded)
        missing_binding["sources"][0]["verified_evidence"].pop()
        for changed in (missing_report, missing_binding):
            with self.assertRaises(ValueError):
                validate_recorded_audit(self.selection, self.review, changed)


if __name__ == "__main__":
    unittest.main()
