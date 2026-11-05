"""Tests for structural and offset validation of human annotation CSV rows."""

import hashlib
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from src.annotation_validation import main as run_annotation_validation
from src.annotation_validation import validate_annotation_rows


class AnnotationValidationTests(unittest.TestCase):
    def setUp(self):
        self.text = "The attacker ran a script before downloading a payload."
        self.mentions = [
            {
                "report_id": "r1", "mention_id": "m1",
                "char_start": "13", "char_end": "32",
                "mention_text": "ran a script before",
                "instance_status": "RESOLVED", "event_instance_id": "e1",
            },
            {
                "report_id": "r1", "mention_id": "m2",
                "char_start": "33", "char_end": "54",
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
                "evidence_end": "25", "evidence_text": "ran a script",
            },
            {
                "report_id": "r1", "event_instance_id": "e2",
                "mapping_id": "map2", "mapping_status": "MAPPED",
                "technique_id": "T1105", "technique_name": "Ingress Tool Transfer",
                "attack_version": "vTEST",
                "evidence_span_id": "me2", "evidence_start": "33",
                "evidence_end": "54", "evidence_text": "downloading a payload",
            },
        ]
        self.relations = [
            {
                "report_id": "r1", "relation_id": "rel1",
                "event_a_id": "e1", "event_b_id": "e2",
                "relation_label": "BEFORE",
                "evidence_span_id": "re1", "evidence_start": "13",
                "evidence_end": "32", "evidence_text": "ran a script before",
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

    def test_source_span_text_preserves_boundary_whitespace(self):
        self.mentions[0]["char_start"] = "12"
        self.mentions[0]["mention_text"] = " ran a script before"
        self.mappings[0]["evidence_end"] = "26"
        self.mappings[0]["evidence_text"] = "ran a script "
        self.relations[0]["evidence_start"] = "12"
        self.relations[0]["evidence_text"] = " ran a script before"

        result = self.validate()
        self.assertTrue(result["valid"], result["errors"])

    def test_cli_preserves_crlf_source_text_for_offsets_and_hash(self):
        raw_source = b"alpha\r\nbeta\r\n"
        expected_hash = hashlib.sha256(raw_source).hexdigest()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            text_path = root / "report.txt"
            text_path.write_bytes(raw_source)
            mentions_path = root / "mentions.csv"
            mappings_path = root / "mappings.csv"
            relations_path = root / "relations.csv"
            for path in (mentions_path, mappings_path, relations_path):
                path.write_text("report_id\n", encoding="utf-8")

            argv = [
                "annotation_validation.py",
                "--report-id", "r1",
                "--text", str(text_path),
                "--mentions", str(mentions_path),
                "--mappings", str(mappings_path),
                "--relations", str(relations_path),
            ]
            output = io.StringIO()
            with patch("sys.argv", argv), redirect_stdout(output):
                exit_code = run_annotation_validation()

        self.assertEqual(exit_code, 0)
        self.assertIn("Characters: 13", output.getvalue())
        self.assertIn(f"SHA-256: {expected_hash}", output.getvalue())

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
