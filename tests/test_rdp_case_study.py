import copy
import json
import unittest

from scripts.audit_rdp_case import CASE, canonical_text, digest, verify
from scripts.analyze_rdp_case import analyze


class RdpCaseStudyTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(CASE.read_text(encoding="utf-8"))

    def test_recorded_analysis_reproduces(self):
        recorded = json.loads((CASE.parent / "results.json").read_text(encoding="utf-8"))
        self.assertEqual(recorded, analyze(self.case))

    def test_outcome_and_mapping_sensitivities_are_distinct(self):
        p = analyze(self.case)["profiles"]
        self.assertEqual(p["attempts_included"]["fully_omitted_edges"], 1)
        self.assertEqual(p["successful_actions_only"]["included_occurrences"], 0)
        self.assertEqual(p["mapping_withheld"]["unmapped_endpoint_edges"], 1)
        self.assertEqual(p["mapping_withheld"]["fully_omitted_edges"], 0)

    def test_missing_evidence_and_taxonomy_mismatch_are_rejected(self):
        for field, value in [("evidence_ids", ["missing"]), ("parent_mapping", "T1059")]:
            case = copy.deepcopy(self.case)
            case["occurrences"][0][field] = value
            with self.assertRaises(ValueError):
                analyze(case)

    def test_corpus_and_validation_claims_cannot_be_promoted(self):
        for field in ("independently_validated", "eligible_for_corpus_denominator"):
            case = copy.deepcopy(self.case)
            case[field] = True
            with self.assertRaises(ValueError):
                analyze(case)

    def test_endpoint_identity_is_required(self):
        for endpoint in ("missing", "rdp_attempt_1"):
            case = copy.deepcopy(self.case)
            case["relations"][0]["target_event"] = endpoint
            with self.assertRaises(ValueError):
                analyze(case)

    def test_paragraph_canonicalization(self):
        raw = b'<script><p>hidden</p></script><p> A &amp; <b>B</b><br>C </p><p> </p><p>D</p>'
        self.assertEqual(canonical_text(raw), "A & B C\nD\n")

    def test_source_and_span_mutation_fail(self):
        raw = b'<p>A before B.</p>'
        text = canonical_text(raw)
        case = {"source": {"raw_html_sha256": digest(raw), "paragraph_text_sha256": digest(text)},
                "evidence": [{"evidence_id": "E1", "char_start": 0, "char_end": 11,
                              "span_sha256": digest(text[:11]), "paragraph_number": 1}]}
        self.assertEqual(verify(raw, case)["evidence_verified"], ["E1"])
        self.assertTrue(verify(raw, case)["raw_html_matches_retrieval"])
        self.assertFalse(verify(b'<p>A before <b>B.</b></p>', case)["raw_html_matches_retrieval"])
        with self.assertRaises(ValueError):
            verify(b'<p>B before A.</p>', case)
        case["evidence"][0]["char_end"] = 10
        with self.assertRaises(ValueError):
            verify(raw, case)

    def test_recorded_audit_binds_to_case(self):
        audit = json.loads((CASE.parent / "source_integrity.json").read_text(encoding="utf-8"))
        self.assertEqual(audit["paragraph_text_sha256"], self.case["source"]["paragraph_text_sha256"])
        self.assertEqual(audit["evidence_verified"], [r["evidence_id"] for r in self.case["evidence"]])


if __name__ == "__main__":
    unittest.main()
