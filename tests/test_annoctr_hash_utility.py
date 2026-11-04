from __future__ import annotations

import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.hash_annoctr_sources import update_frame


class AnnoCTRHashUtilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.frame = self.root / "frame.csv"
        self.text_dir = self.root / "corpus" / "text"
        self.text_dir.mkdir(parents=True)
        self.report_text = "first line\r\nsecond line\n"
        (self.text_dir / "r-test.txt").write_bytes(self.report_text.encode("utf-8"))
        with self.frame.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["report_id", "source_text_sha256", "note"],
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerow({
                "report_id": "r-test",
                "source_text_sha256": "0" * 64,
                "note": "metadata only",
            })

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_verification_reports_mismatch_without_mutating_frame(self) -> None:
        before = self.frame.read_bytes()
        checked, mismatches = update_frame(self.frame, self.root / "corpus", write=False)
        self.assertEqual(checked, 1)
        self.assertEqual(mismatches, ["r-test"])
        self.assertEqual(self.frame.read_bytes(), before)

    def test_write_replaces_hash_using_preserved_crlf_text(self) -> None:
        expected = hashlib.sha256(self.report_text.encode("utf-8")).hexdigest()
        checked, mismatches = update_frame(self.frame, self.root / "corpus", write=True)
        self.assertEqual(checked, 1)
        self.assertEqual(mismatches, ["r-test"])
        with self.frame.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(rows[0]["source_text_sha256"], expected)
        self.assertEqual(rows[0]["note"], "metadata only")

    def test_missing_source_stops_without_modifying_frame(self) -> None:
        (self.text_dir / "r-test.txt").unlink()
        before = self.frame.read_bytes()
        with self.assertRaises(FileNotFoundError):
            update_frame(self.frame, self.root / "corpus", write=True)
        self.assertEqual(self.frame.read_bytes(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
