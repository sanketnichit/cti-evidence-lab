"""Synthetic tests for the AnnoCTR file-level screening script."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.screen_annoctr import infer_vendor, screen_corpus, write_csv


class AnnoCTRScreeningTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "AnnoCTR" / "all"
        for folder in ("text", "linking_mitre_only", "time"):
            (self.root / folder).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write_report(self, report_id, techniques, timeml):
        (self.root / "text" / f"{report_id}.txt").write_text(
            "Synthetic report text.", encoding="utf-8"
        )
        records = []
        for index, (technique_id, mention) in enumerate(techniques):
            records.append({
                "entity_type": "TECHNIQUE",
                "label_id": index,
                "label_title": mention,
                "label_link": f"https://attack.mitre.org/techniques/{technique_id}",
                "mention": mention,
            })
        (self.root / "linking_mitre_only" / f"{report_id}.json").write_text(
            "\n".join(json.dumps(row) for row in records) + "\n",
            encoding="utf-8",
        )
        (self.root / "time" / f"{report_id}.tml").write_text(
            timeml, encoding="utf-8"
        )

    def test_screens_counts_without_labeling_event_instances(self):
        self.write_report(
            "proofpoint_example_2020",
            [("T1059", "script A"), ("T1059", "script B"), ("T1105", "download")],
            "<TimeML><TIMEX3>today</TIMEX3><EVENT>x</EVENT><TLINK/></TimeML>",
        )
        rows = screen_corpus(self.root)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row.source_vendor, "Proofpoint")
        self.assertEqual(row.source_text_characters, len("Synthetic report text."))
        self.assertEqual(row.link_record_count, 3)
        self.assertEqual(row.technique_link_record_count, 3)
        self.assertEqual(row.valid_attack_technique_link_record_count, 3)
        self.assertEqual(row.unresolved_technique_link_record_count, 0)
        self.assertEqual(row.unique_technique_count, 2)
        self.assertEqual(row.cyber_specific_record_count, 3)
        self.assertTrue(row.cyber_specific_layer_present)
        self.assertEqual(row.repeated_technique_ids, "T1059:2")
        self.assertEqual(row.timex3_count, 1)
        self.assertEqual(row.event_tag_count, 1)
        self.assertEqual(row.tlink_tag_count, 1)

    def test_non_attack_link_is_not_counted_as_attack_technique_id(self):
        report_id = "proofpoint_non_attack_link"
        self.write_report(report_id, [("T1059", "script")], "<TimeML/>")
        path = self.root / "linking_mitre_only" / f"{report_id}.json"
        records = [
            {
                "entity_type": "TECHNIQUE",
                "label_id": 1352,
                "label_title": "Buer",
                "label_link": "http://www.bosch.com#node1fuu313m0x3",
                "mention": "Buer",
            }
        ]
        path.write_text("\n".join(json.dumps(row) for row in records), encoding="utf-8")
        row = screen_corpus(self.root)[0]
        self.assertEqual(row.technique_link_record_count, 1)
        self.assertEqual(row.valid_attack_technique_link_record_count, 0)
        self.assertEqual(row.unresolved_technique_link_record_count, 1)
        self.assertEqual(row.unique_technique_count, 0)
        self.assertEqual(row.repeated_technique_ids, "")
        self.assertEqual(row.cyber_specific_record_count, 1)

    def test_quoteintelligence_vendor_alias(self):
        self.assertEqual(infer_vendor("quoteintelligence_2021_report"), "QuoIntelligence")

    def test_ignores_context_and_negative_link_variants(self):
        self.write_report(
            "intel471_primary_report",
            [("T1059", "script")],
            "<TimeML/>",
        )
        variants = (
            "intel471_primary_report_w_con.json",
            "intel471_primary_report_w_neg.json",
            "intel471_primary_report_w_con_w_neg.json",
        )
        for filename in variants:
            (self.root / "linking_mitre_only" / filename).write_text(
                json.dumps({"entity_type": "TECHNIQUE", "label_link": "T1059"}),
                encoding="utf-8",
            )

        rows = screen_corpus(self.root)
        self.assertEqual([row.report_id for row in rows], ["intel471_primary_report"])

    def test_temporal_markup_is_not_inferred_when_file_missing(self):
        (self.root / "text" / "lab52_report.txt").write_text("Example", encoding="utf-8")
        (self.root / "linking_mitre_only" / "lab52_report.json").write_text(
            json.dumps({"entity_type": "TECHNIQUE", "label_link": "T1059"}),
            encoding="utf-8",
        )
        rows = screen_corpus(self.root)
        row = rows[0]
        self.assertEqual(row.source_vendor, "Lab52 / S2 Grupo")
        self.assertIsNone(row.timex3_count)
        self.assertIn("MISSING_TIMEML", row.screening_status)

    def test_csv_contains_aggregate_fields(self):
        self.write_report("intel471_report", [("T1566", "phishing")], "<TimeML/>")
        rows = screen_corpus(self.root)
        output = Path(self.tmp.name) / "result.csv"
        write_csv(rows, output)
        text = output.read_text(encoding="utf-8")
        self.assertIn("report_id,source_vendor", text)
        self.assertIn("intel471_report", text)
        self.assertNotIn("Synthetic report text.", text)


if __name__ == "__main__":
    unittest.main()
