"""Tests for structural and offset validation of human annotation CSV rows."""

import unittest

from src.annotation_validation import validate_annotation_rows


class AnnotationValidationTests(unittest.TestCase):
    def setUp(self):
        self.text = "The attacker ran a script before downloading a payload."
        self.mentions = [
            {
                "report_id": "r1", "mention_id": "m1",
                "char_start": "13", "char_end": "29",
                "mention_text": "ran a script before",
                "instance_status": "RESOLVED", "event_instance_id": "e1",
            },
            {
                "report_id": "r1", "mention_id": "m2",
                "char_start": "39", "char_end": "58",
                "mention_text": "downloading a payload",
                "instance_status": "RESOLVED", "event_instance_id": "e2",
            },
        ]
        self.mappings = [
            {
                "report_id": "r1", "event_instance_id": "e1",
                "mapping_id": "map1", "mapping_status": "MAPPED",
                "technique_id": "T1059", "technique_name": "Command and Scripting Interpreter",
                "attack_version": "vTEST",
                "evidence_span_id": "me1", "evidence_start": "13",
                "evidence_end": "24", "evidence_text": "ran a script",
            },
            {
                "report_id": "r1", "event_instance_id": "e2",
                "mapping_id": "map2", "mapping_status": "MAPPED",
                "technique_id": "T1105", "technique_name": "Ingress Tool Transfer",
                "attack_version": "vTEST",
                "evidence_span_id": "me2", "evidence_start": "39",
                "evidence_end": "58", "evidence_text": "downloading a payload",
            },
        ]
        self.relations = [
            {
                "report_id": "r1", "relation_id": "rel1",
                "event_a_id": "e1", "event_b_id": "e2",
                "relation_label": "BEFORE",
                "evidence_span_id": "re1", "evidence_start": "13",
                "evidence_end": "33", "evidence_text": "ran a script before",
                "evidence_scope": "SENTENCE",
            }
        ]

    def validate(self):
        return validate_annotation_rows(
            report_id="r1",
            report_text=self.text,
            mention_rows=self.mentions,
            mapping_rows=self.mappings,
            relation_rows=self.relations,
        )

    def test_valid_rows_pass(self):
        self.assertTrue(self.validate()["valid"])

    def test_bad_mention_offset_fails(self):
        self.mentions[0]["char_end"] = "28"
        result = self.validate()
        self.assertFalse(result["valid"])
        self.assertTrue(any("does not equal" in e for e in result["errors"]))

    def test_unresolved_mention_cannot_have_event_id(self):
        self.mentions[0]["instance_status"] = "UNRESOLVED"
        result = self.validate()
        self.assertFalse(result["valid"])
        self.assertTrue(any("must not have a resolved" in e for e in result["errors"]))

    def test_mapped_event_requires_evidence(self):
        self.mappings[0]["evidence_text"] = ""
        result = self.validate()
        self.assertFalse(result["valid"])
        self.assertTrue(any("MAPPED row is missing" in e for e in result["errors"]))

    def test_unmapped_event_is_explicit(self):
        self.mappings[0] = {
            "report_id": "r1", "event_instance_id": "e1",
            "mapping_id": "map1", "mapping_status": "UNMAPPED",
        }
        result = self.validate()
        self.assertTrue(result["valid"], result["errors"])

    def test_positive_temporal_edge_requires_evidence(self):
        self.relations[0]["evidence_text"] = ""
        result = self.validate()
        self.assertFalse(result["valid"])
        self.assertTrue(any("requires a relation-specific evidence span" in e for e in result["errors"]))

    def test_no_temporal_claim_is_not_a_positive_edge(self):
        self.relations = [{
            "report_id": "r1", "relation_id": "rel1",
            "event_a_id": "e1", "event_b_id": "e2",
            "relation_label": "NO_TEMPORAL_CLAIM",
        }]
        result = self.validate()
        self.assertTrue(result["valid"], result["errors"])

    def test_generic_behaviour_cannot_be_in_event_graph(self):
        self.mentions[0]["instance_status"] = "GENERIC_BEHAVIOUR"
        self.mentions[0]["event_instance_id"] = ""
        result = self.validate()
        self.assertFalse(result["valid"])
        self.assertTrue(any("not a RESOLVED event instance" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
