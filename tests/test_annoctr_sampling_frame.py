from __future__ import annotations

import csv
import hashlib
import unittest
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAME_PATH = ROOT / "research" / "annoctr_sampling" / "AnnoCTR_Fresh_MultiVendor_Sample_Frame_v1.0.csv"
METHOD_PATH = ROOT / "research" / "annoctr_sampling" / "AnnoCTR_Fresh_MultiVendor_Sampling_Method_v0.3.3.md"
PRIORITY_SEED = "CTI-EVIDENCE-LAB-ANNOCTR-PILOT-2026-11-03-v1"
EXPECTED_DONORS = {
    "Intel471": 30,
    "Lab52 / S2 Grupo": 23,
    "Proofpoint": 28,
    "QuoIntelligence": 12,
    "ZScaler": 27,
}
REQUIRED_FIELDS = {
    "report_id",
    "donor",
    "official_split",
    "random_priority_sha256",
    "random_rank_within_vendor",
    "source_text_sha256",
    "ai_triage_status",
    "source_scope_eligibility",
    "local_research_use_status",
    "public_reuse_status",
    "researcher_review_status",
}


def load_frame() -> tuple[list[str], list[dict[str, str]]]:
    with FRAME_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return reader.fieldnames or [], rows


class AnnoCTRSamplingFrameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fields, cls.rows = load_frame()

    def test_frame_schema_separates_automated_triage_and_researcher_decisions(self):
        self.assertTrue(REQUIRED_FIELDS.issubset(set(self.fields)))
        self.assertNotIn("eligibility_status", self.fields)
        self.assertEqual(len(self.fields), len(set(self.fields)))
        for row in self.rows:
            self.assertNotEqual(row["ai_triage_status"], "")
            self.assertIn(row["source_scope_eligibility"], {"PENDING", "ELIGIBLE", "INELIGIBLE"})
            self.assertIn(row["local_research_use_status"], {"UNRESOLVED", "PERMITTED", "NOT_PERMITTED"})
            self.assertIn(row["public_reuse_status"], {"UNRESOLVED", "PERMITTED", "RESTRICTED", "NOT_PLANNED"})
            self.assertIn(row["researcher_review_status"], {"NOT_REVIEWED", "IN_REVIEW", "DECISION_RECORDED"})

    def test_frame_has_120_unique_manifest_report_ids_and_expected_donor_counts(self):
        report_ids = [row["report_id"] for row in self.rows]
        self.assertEqual(len(self.rows), 120)
        self.assertEqual(len(report_ids), len(set(report_ids)))
        self.assertEqual(dict(Counter(row["donor"] for row in self.rows)), EXPECTED_DONORS)
        self.assertTrue(all(row["official_split"] in {"TRAIN", "DEV", "TEST"} for row in self.rows))

    def test_priority_hashes_recompute_from_the_pinned_seed(self):
        for row in self.rows:
            expected = hashlib.sha256(f"{PRIORITY_SEED}|{row['report_id']}".encode("utf-8")).hexdigest()
            self.assertEqual(row["random_priority_sha256"], expected, row["report_id"])
            self.assertRegex(row["source_text_sha256"], r"^[0-9a-f]{64}$")

    def test_within_donor_ranks_match_ascending_priority_hash_order(self):
        grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in self.rows:
            grouped[row["donor"]].append(row)
        self.assertEqual(set(grouped), set(EXPECTED_DONORS))
        for donor, rows in grouped.items():
            ranked = sorted(rows, key=lambda row: row["random_priority_sha256"])
            actual = [int(row["random_rank_within_vendor"]) for row in ranked]
            self.assertEqual(actual, list(range(1, len(rows) + 1)), donor)

    def test_exactly_one_rank_one_base_candidate_is_recorded_per_donor(self):
        rank_one = [row for row in self.rows if row["random_rank_within_vendor"] == "1"]
        self.assertEqual(len(rank_one), len(EXPECTED_DONORS))
        self.assertEqual({row["donor"] for row in rank_one}, set(EXPECTED_DONORS))
        self.assertTrue(all(row["selection_type"] == "BASE_STRATIFIED_PRIORITY_1_REVIEW" for row in rank_one))
        self.assertTrue(all(row["researcher_review_status"] == "NOT_REVIEWED" for row in rank_one))
        self.assertIn(PRIORITY_SEED, METHOD_PATH.read_text(encoding="utf-8"))


    def test_current_frame_records_the_two_source_scope_exclusions(self):
        statuses = Counter(row["source_scope_eligibility"] for row in self.rows)
        self.assertEqual(statuses["PENDING"], 118)
        self.assertEqual(statuses["INELIGIBLE"], 2)
        decided = [
            row for row in self.rows
            if row["source_scope_eligibility"] == "INELIGIBLE"
        ]
        self.assertEqual(len(decided), 2)
        self.assertTrue(all(row["researcher_review_status"] == "DECISION_RECORDED" for row in decided))

if __name__ == "__main__":
    unittest.main(verbosity=2)
