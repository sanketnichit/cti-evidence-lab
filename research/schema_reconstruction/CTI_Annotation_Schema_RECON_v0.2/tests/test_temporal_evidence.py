"""Synthetic tests for the RECON v0.2 temporal-evidence extension."""
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "validator"))
from validate_temporal_evidence import HEADERS, validate_bundle


PART = {"report_id": "r1", "annotator_id": "a1", "annotation_pass_id": "p1"}
REL_H = ["report_id", "annotator_id", "annotation_pass_id", "relation_id", "event_a_id", "event_b_id", "relation_label", "relation_basis", "evidence_scope", "primary_evidence_span_id"]
SPAN_H = ["report_id", "annotator_id", "annotation_pass_id", "evidence_span_id", "span_kind"]
UNIT_H = ["report_id", "annotator_id", "annotation_pass_id", "activity_unit_id"]
TIME_H = ["report_id", "annotator_id", "annotation_pass_id", "time_evidence_id", "activity_unit_id", "time_type", "normalization_status", "normalized_start", "normalized_end", "primary_evidence_span_id"]


def write(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


class TemporalEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.base = self.root / "base"
        self.ext = self.root / "temporal_relation_evidence.csv"
        self.relation = {**PART, "relation_id": "rel1", "event_a_id": "evA", "event_b_id": "evB", "relation_label": "BEFORE", "relation_basis": "direct_source", "evidence_scope": "SENTENCE", "primary_evidence_span_id": "cue"}
        self.spans = [{**PART, "evidence_span_id": "cue", "span_kind": "RELATION"}, {**PART, "evidence_span_id": "a", "span_kind": "MENTION"}, {**PART, "evidence_span_id": "b", "span_kind": "MENTION"}, {**PART, "evidence_span_id": "ctx", "span_kind": "SCOPE"}]
        self.units = [{**PART, "activity_unit_id": "evA"}, {**PART, "activity_unit_id": "evB"}]
        self.times = []
        self.links = [
            {**PART, "relation_evidence_id": "re1", "relation_id": "rel1", "evidence_span_id": "a", "evidence_role": "EVENT_A_SUPPORT", "supported_event_id": "evA", "evidence_notes": ""},
            {**PART, "relation_evidence_id": "re2", "relation_id": "rel1", "evidence_span_id": "b", "evidence_role": "EVENT_B_SUPPORT", "supported_event_id": "evB", "evidence_notes": ""},
        ]
        self.save()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        write(self.base / "registers" / "temporal_relations.csv", REL_H, [self.relation])
        write(self.base / "registers" / "evidence_spans.csv", SPAN_H, self.spans)
        write(self.base / "registers" / "activity_units.csv", UNIT_H, self.units)
        write(self.base / "registers" / "time_evidence.csv", TIME_H, self.times)
        write(self.ext, HEADERS, self.links)

    def report(self):
        return validate_bundle(self.base, self.ext)

    def codes(self):
        return {item["code"] for item in self.report()["errors"]}

    def test_valid_direct_source_pair(self):
        self.assertTrue(self.report()["ok"], self.report()["errors"])

    def test_event_a_support_required(self):
        self.links = [x for x in self.links if x["evidence_role"] != "EVENT_A_SUPPORT"]
        self.save()
        self.assertIn("EVENT_A_SUPPORT_MISSING", self.codes())

    def test_event_b_support_required(self):
        self.links = [x for x in self.links if x["evidence_role"] != "EVENT_B_SUPPORT"]
        self.save()
        self.assertIn("EVENT_B_SUPPORT_MISSING", self.codes())

    def test_event_support_must_match_endpoint(self):
        self.links[0]["supported_event_id"] = "evB"
        self.save()
        self.assertIn("EVENT_A_SUPPORT_MISMATCH", self.codes())

    def test_context_must_not_claim_endpoint(self):
        self.links.append({**PART, "relation_evidence_id": "re3", "relation_id": "rel1", "evidence_span_id": "ctx", "evidence_role": "RELATION_CONTEXT", "supported_event_id": "evA", "evidence_notes": ""})
        self.save()
        self.assertIn("CONTEXT_EVENT_ID_FORBIDDEN", self.codes())

    def test_context_is_optional_and_supported(self):
        self.links.append({**PART, "relation_evidence_id": "re3", "relation_id": "rel1", "evidence_span_id": "ctx", "evidence_role": "RELATION_CONTEXT", "supported_event_id": "", "evidence_notes": "antecedent"})
        self.save()
        self.assertTrue(self.report()["ok"], self.report()["errors"])

    def test_orphan_relation_and_unknown_span_are_rejected(self):
        self.links[0]["relation_id"] = "missing"
        self.save()
        self.assertIn("UNKNOWN_RELATION", self.codes())
        self.links[0]["relation_id"] = "rel1"
        self.links[0]["evidence_span_id"] = "missing"
        self.save()
        self.assertIn("UNKNOWN_EVIDENCE_SPAN", self.codes())

    def test_primary_relation_cue_requires_relation_span_kind(self):
        self.spans[0]["span_kind"] = "MENTION"
        self.save()
        self.assertIn("RELATION_CUE_WRONG_SPAN_KIND", self.codes())

    def test_duplicate_link_id_and_assignment_are_rejected(self):
        self.links[1]["relation_evidence_id"] = "re1"
        self.links.append(dict(self.links[0], relation_evidence_id="re3"))
        self.save()
        self.assertIn("DUPLICATE_LINK_ID", self.codes())
        self.assertIn("DUPLICATE_RELATION_EVIDENCE", self.codes())

    def test_direct_timestamp_requires_each_endpoint_time_span(self):
        self.relation["relation_basis"] = "direct_timestamp"
        self.times = [
            {**PART, "time_evidence_id": "tA", "activity_unit_id": "evA", "time_type": "ATTACK_OCCURRENCE", "normalization_status": "NORMALIZED", "normalized_start": "2026-01-01T08:00:00Z", "normalized_end": "2026-01-01T08:00:00Z", "primary_evidence_span_id": "a"},
            {**PART, "time_evidence_id": "tB", "activity_unit_id": "evB", "time_type": "ATTACK_OCCURRENCE", "normalization_status": "NORMALIZED", "normalized_start": "2026-01-01T09:00:00Z", "normalized_end": "2026-01-01T09:00:00Z", "primary_evidence_span_id": "b"},
        ]
        self.save()
        self.assertTrue(self.report()["ok"], self.report()["errors"])

    def test_direct_timestamp_missing_endpoint_time_support_is_rejected(self):
        self.relation["relation_basis"] = "direct_timestamp"
        self.times = [{**PART, "time_evidence_id": "tA", "activity_unit_id": "evA", "time_type": "ATTACK_OCCURRENCE", "normalization_status": "NORMALIZED", "normalized_start": "2026-01-01T08:00:00Z", "normalized_end": "2026-01-01T08:00:00Z", "primary_evidence_span_id": "a"}]
        self.save()
        self.assertIn("EVENT_B_TIMESTAMP_SUPPORT_MISSING", self.codes())

    def test_rows_from_other_partition_do_not_satisfy_support(self):
        self.links[0]["annotator_id"] = "other"
        self.save()
        self.assertIn("EVENT_A_SUPPORT_MISSING", self.codes())


    def test_document_context_requires_context_span_and_rationale(self):
        self.relation["evidence_scope"] = "DOCUMENT_CONTEXT"
        self.save()
        self.assertIn("RELATION_CONTEXT_MISSING", self.codes())
        self.links.append({**PART, "relation_evidence_id": "re3", "relation_id": "rel1", "evidence_span_id": "ctx", "evidence_role": "RELATION_CONTEXT", "supported_event_id": "", "evidence_notes": "antecedent resolved from an earlier paragraph"})
        self.save()
        self.assertNotIn("RELATION_CONTEXT_MISSING", self.codes())
        self.assertTrue(self.report()["ok"], self.report()["errors"])

    def test_relation_context_requires_explanatory_note(self):
        self.links.append({**PART, "relation_evidence_id": "re3", "relation_id": "rel1", "evidence_span_id": "ctx", "evidence_role": "RELATION_CONTEXT", "supported_event_id": "", "evidence_notes": ""})
        self.save()
        self.assertIn("CONTEXT_RATIONALE_MISSING", self.codes())

    def test_invalid_role_is_rejected(self):
        self.links[0]["evidence_role"] = "TEMPORAL_RELATION"
        self.save()
        self.assertIn("INVALID_EVIDENCE_ROLE", self.codes())


if __name__ == "__main__":
    unittest.main()
