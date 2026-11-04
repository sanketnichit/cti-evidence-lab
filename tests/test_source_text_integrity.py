from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from src.source_text_integrity import (
    decode_frozen_source,
    frozen_source_metadata,
    frozen_source_sha256,
    read_frozen_source,
)


class SourceTextIntegrityTests(unittest.TestCase):
    def test_crlf_is_preserved_and_hashed_without_universal_newline_translation(self):
        raw = b"alpha\r\nbeta\r\n"
        text = decode_frozen_source(raw)
        self.assertEqual(text, "alpha\r\nbeta\r\n")
        self.assertEqual(frozen_source_sha256(text), hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(text), 13)

    def test_optional_utf8_bom_is_removed_but_other_bytes_are_preserved(self):
        text = decode_frozen_source(b"\xef\xbb\xbfalpha\r\nbeta")
        self.assertEqual(text, "alpha\r\nbeta")
        self.assertEqual(frozen_source_sha256(text), hashlib.sha256(b"alpha\r\nbeta").hexdigest())

    def test_unicode_is_not_normalized_and_offsets_are_code_points(self):
        text = "A😀e\u0301"
        self.assertEqual(len(text), 4)
        self.assertNotEqual(frozen_source_sha256(text), frozen_source_sha256("A😀é"))

    def test_metadata_reads_original_line_endings(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.txt"
            path.write_bytes(b"one\r\ntwo")
            metadata = frozen_source_metadata(path)
            self.assertEqual(metadata["source_text_sha256"], hashlib.sha256(b"one\r\ntwo").hexdigest())
            self.assertEqual(metadata["source_text_char_count"], 8)
            self.assertEqual(read_frozen_source(path), "one\r\ntwo")


if __name__ == "__main__":
    unittest.main(verbosity=2)
