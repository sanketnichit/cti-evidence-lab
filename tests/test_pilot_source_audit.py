import unittest

from scripts.audit_pilot_sources import audit_anchor, verified_text
from src.source_text_integrity import frozen_source_sha256


class PilotSourceAuditTests(unittest.TestCase):
    def test_crlf_requires_explicit_recovery_and_exact_known_hash(self):
        expected = frozen_source_sha256("α\nb\n")
        raw = "α\r\nb\r\n".encode()
        with self.assertRaises(ValueError):
            verified_text(raw, expected)
        text, metadata = verified_text(raw, expected, True)
        self.assertEqual(text, "α\nb\n")
        self.assertEqual(metadata["transformation"], "CRLF_TO_LF_VERIFIED_AGAINST_FRAME")
        with self.assertRaises(ValueError):
            verified_text(raw.replace(b"b", b"c"), expected, True)

    def test_existing_exact_crlf_is_preserved_and_bom_is_only_encoding_marker(self):
        text = "α\r\nb"
        result, metadata = verified_text(b"\xef\xbb\xbf" + text.encode(), frozen_source_sha256(text), True)
        self.assertEqual(result, text)
        self.assertEqual(metadata["transformation"], "NONE")

    def test_code_point_offsets_and_line_are_verified_without_exporting_text(self):
        row = dict(anchor_id="x", char_start="2", char_end="4", source_line_number="2", anchor_occurrences_in_source="UNIQUE")
        result = audit_anchor("α\n😀b", row)
        self.assertEqual(result["span_sha256"], frozen_source_sha256("😀b"))
        self.assertNotIn("😀b", str(result))
        for patch in ({"char_end": "9"}, {"source_line_number": "1"}, {"char_start": "4"}):
            with self.assertRaises(ValueError):
                audit_anchor("α\n😀b", {**row, **patch})

    def test_overlapping_duplicate_anchor_rejected(self):
        row = dict(anchor_id="x", char_start="0", char_end="2", source_line_number="1", anchor_occurrences_in_source="UNIQUE")
        with self.assertRaises(ValueError):
            audit_anchor("aaa", row)


if __name__ == "__main__":
    unittest.main()
