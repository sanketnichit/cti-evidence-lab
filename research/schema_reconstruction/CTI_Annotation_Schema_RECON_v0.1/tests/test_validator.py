from __future__ import annotations

import csv
import hashlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "validator"))
import validate_annotations as validator  # noqa: E402

SOURCE_TEXT = "Event A precedes Event B."
SOURCE_HASH = hashlib.sha256(SOURCE_TEXT.encode("utf-8")).hexdigest()
A120_HASH = "97b599ffdcfcc5864a9352cf1467de0f6cac92f9141053a76098e4f2d33fb1bc"
PARTITION = {"report_id": "r-test", "annotator_id": "annotator-1", "annotation_pass_id": "pass-1"}


def write_register(root: Path, name: str, rows: list[dict[str, str]]) -> None:
    path = root / "registers" / f"{name}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=validator.HEADERS[name])
        writer.writeheader()
        writer.writerows(rows)


def make_fixture(root: Path) -> dict[str, list[dict[str, str]]]:
    """Create a minimal, valid two-event example with one direct BEFORE edge."""
    shutil.copytree(PACKAGE_ROOT, root, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    rows = {name: [] for name in validator.HEADERS}
    rows["report_registry"] = [{
        **PARTITION,
        "protocol_version": "v0.4-draft",
        "schema_version": "RECON-v0.1",
        "source_title": "Synthetic validation fixture",
        "source_vendor": "Synthetic",
        "source_url": "https://example.invalid/report",
        "source_path": "r-test.txt",
        "retrieval_date": "2026-11-03",
        "publication_date": "2026-01-01",
        "corpus_name": "synthetic",
        "corpus_release": "test-1",
        "split": "test",
        "language": "en",
        "source_text_sha256": SOURCE_HASH,
        "source_text_char_count": str(len(SOURCE_TEXT)),
        "extraction_method": "synthetic literal text",
        "transformation_notes": "none",
        "source_scope_eligibility": "ELIGIBLE",
        "source_scope_reason": "Synthetic fixture",
        "local_research_use_status": "PERMITTED",
        "local_research_use_basis": "Synthetic only",
        "public_reuse_status": "NOT_PLANNED",
        "rights_notes": "Synthetic text",
        "report_assessability": "ASSESSABLE",
        "assessability_reason": "Complete synthetic report",
        "full_report_review_status": "COMPLETE",
        "prior_exposure_status": "UNEXPOSED",
        "annotator_notes": "test fixture",
    }]
    rows["report_scopes"] = [{
        **PARTITION, "scope_id": "scope-incident", "parent_scope_id": "",
        "scope_type": "INCIDENT", "scope_label": "Synthetic incident",
        "scope_description": "Single synthetic incident", "scope_status": "RESOLVED",
        "scope_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "scope_notes": "",
    }]
    for unit_id in ("event-a", "event-b"):
        rows["activity_units"].append({
            **PARTITION, "activity_unit_id": unit_id, "scope_id": "scope-incident",
            "parent_activity_unit_id": "", "granularity": "atomic_event", "unit_role": "event_leaf",
            "instance_status": "RESOLVED", "count_status": "unknown", "count_exact": "",
            "count_min": "", "count_max": "", "count_qualitative": "", "recurrence_pattern": "",
            "unit_summary": unit_id, "actor_ref": "", "host_or_asset_ref": "",
            "annotator_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "unit_notes": "",
        })
    spans = [
        ("span-a", 0, 7, "Event A"),
        ("span-b", 17, 24, "Event B"),
        ("span-relation", 0, 25, SOURCE_TEXT),
    ]
    for span_id, start, end, text in spans:
        rows["evidence_spans"].append({
            **PARTITION, "evidence_span_id": span_id, "char_start": str(start), "char_end": str(end),
            "evidence_text": text, "sentence_id": "s1", "section_locator": "Synthetic",
            "paragraph_locator": "p1", "figure_locator": "", "source_text_sha256": SOURCE_HASH,
            "span_kind": "RELATION" if span_id == "span-relation" else "MENTION", "span_notes": "",
        })
    for mention_id, unit_id, span_id, text in [
        ("mention-a", "event-a", "span-a", "Event A"),
        ("mention-b", "event-b", "span-b", "Event B"),
    ]:
        rows["event_mentions"].append({
            **PARTITION, "mention_id": mention_id, "activity_unit_id": unit_id,
            "primary_evidence_span_id": span_id, "sentence_id": "s1", "section_locator": "Synthetic",
            "mention_kind": "ACTION", "instance_status": "RESOLVED",
            "resolved_event_instance_id": unit_id, "event_type_text": "synthetic action",
            "actor_text": "actor", "target_text": "target", "asset_or_host_text": "host",
            "time_expression": "", "mention_unit_status_note": "", "annotator_confidence": "HIGH",
            "adjudication_status": "UNREVIEWED", "mention_notes": "",
        })
    for map_id, unit_id, technique in [
        ("map-a", "event-a", "T1059"),
        ("map-b", "event-b", "T1059"),
    ]:
        rows["event_mappings"].append({
            **PARTITION, "mapping_id": map_id, "activity_unit_id": unit_id,
            "event_instance_id": unit_id, "exact_technique_id": technique,
            "exact_technique_name": "Command and Scripting Interpreter", "attack_version": "synthetic",
            "mapping_basis": "report_explicit_parent", "mapping_decision_status": "ACCEPTED",
            "alternative_group_id": "", "alternative_to_mapping_id": "",
            "baseline_vocabulary_id": "CTI Evidence Lab A_120 selected-technique identifier vocabulary",
            "baseline_vocabulary_sha256": A120_HASH, "baseline_parent_technique_id": technique,
            "baseline_mapping_status": "IN_VOCAB", "annotator_confidence": "HIGH",
            "adjudication_status": "UNREVIEWED", "mapping_notes": "synthetic",
        })
    rows["temporal_relations"] = [{
        **PARTITION, "relation_id": "rel-a-b", "event_a_id": "event-a", "event_b_id": "event-b",
        "comparison_scope_id": "scope-incident", "scope_compatibility": "COMPATIBLE",
        "relation_label": "BEFORE", "relation_basis": "direct_source", "evidence_scope": "SENTENCE",
        "primary_evidence_span_id": "span-relation", "annotator_confidence": "HIGH",
        "adjudication_status": "UNREVIEWED", "relation_notes": "synthetic",
    }]
    rows["record_evidence_links"] = [{
        **PARTITION, "link_id": "link-map-a", "record_type": "event_mappings", "record_id": "map-a",
        "evidence_span_id": "span-a", "evidence_role": "MAPPING", "link_notes": "additional mapping evidence",
    }, {
        **PARTITION, "link_id": "link-map-b", "record_type": "event_mappings", "record_id": "map-b",
        "evidence_span_id": "span-b", "evidence_role": "MAPPING", "link_notes": "additional mapping evidence",
    }]
    for name, data in rows.items():
        write_register(root, name, data)
    return rows


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.bundle = Path(self.temp.name) / "bundle"
        self.rows = make_fixture(self.bundle)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def validate(self, source_texts: bool = True):
        sources = {(
            PARTITION["report_id"], PARTITION["annotator_id"], PARTITION["annotation_pass_id"]
        ): SOURCE_TEXT} if source_texts else {}
        return validator.validate_bundle(self.bundle, sources)

    def save(self, name: str) -> None:
        write_register(self.bundle, name, self.rows[name])

    def test_valid_two_event_positive_before_edge(self):
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.issues if x.severity == "ERROR"])
        self.assertEqual(result.primary_positive_temporal_edges, 1)
        self.assertEqual(result.accepted_a120_mappings, 2)

    def test_missing_source_text_is_warning_not_false_error(self):
        result = self.validate(source_texts=False)
        self.assertTrue(result.ok)
        self.assertTrue(any(x.code == "SOURCE_TEXT_NOT_SUPPLIED" for x in result.warnings))

    def test_self_event_relation_rejected(self):
        self.rows["temporal_relations"][0]["event_b_id"] = "event-a"
        self.save("temporal_relations")
        result = self.validate()
        self.assertIn("SELF_EVENT_RELATION", {x.code for x in result.errors})

    def test_container_endpoint_rejected_from_primary_graph(self):
        unit = next(x for x in self.rows["activity_units"] if x["activity_unit_id"] == "event-b")
        unit.update(granularity="repeated_event_series", unit_role="series_container")
        self.save("activity_units")
        result = self.validate()
        self.assertIn("INELIGIBLE_PRIMARY_ENDPOINT", {x.code for x in result.errors})

    def test_endpoint_outside_comparison_scope_rejected(self):
        self.rows["report_scopes"].append({
            **PARTITION, "scope_id": "other-scope", "parent_scope_id": "", "scope_type": "INCIDENT",
            "scope_label": "Other incident", "scope_description": "Distinct context", "scope_status": "RESOLVED",
            "scope_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "scope_notes": "",
        })
        next(x for x in self.rows["activity_units"] if x["activity_unit_id"] == "event-b")["scope_id"] = "other-scope"
        self.save("report_scopes")
        self.save("activity_units")
        result = self.validate()
        self.assertIn("ENDPOINT_OUTSIDE_COMPARISON_SCOPE", {x.code for x in result.errors})

    def test_workbook_only_cannot_be_accepted(self):
        self.rows["event_mappings"][0]["mapping_basis"] = "workbook_only"
        self.save("event_mappings")
        result = self.validate()
        self.assertIn("UNSUPPORTED_ACCEPTED_MAPPING", {x.code for x in result.errors})

    def test_accepted_mapping_requires_its_own_evidence_link(self):
        self.rows["record_evidence_links"] = [
            row for row in self.rows["record_evidence_links"] if row["record_id"] != "map-a"
        ]
        self.save("record_evidence_links")
        result = self.validate()
        self.assertIn("ACCEPTED_MAPPING_NO_EVIDENCE_LINK", {x.code for x in result.errors})

    def test_scope_hierarchy_cycle_rejected(self):
        self.rows["report_scopes"][0]["parent_scope_id"] = "scope-incident"
        self.save("report_scopes")
        result = self.validate()
        self.assertIn("SCOPE_HIERARCHY_CYCLE", {x.code for x in result.errors})

    def test_technique_outside_a120_rejected(self):
        mapping = self.rows["event_mappings"][0]
        mapping.update(exact_technique_id="T9999", baseline_parent_technique_id="T9999")
        self.save("event_mappings")
        result = self.validate()
        self.assertIn("A120_MEMBERSHIP_FAILURE", {x.code for x in result.errors})

    def test_evidence_text_must_match_frozen_source(self):
        self.rows["evidence_spans"][0]["evidence_text"] = "Event X"
        self.save("evidence_spans")
        result = self.validate()
        self.assertIn("EVIDENCE_TEXT_MISMATCH", {x.code for x in result.errors})

    def test_duplicate_evidence_link_rejected(self):
        self.rows["record_evidence_links"].append(dict(self.rows["record_evidence_links"][0]))
        self.rows["record_evidence_links"][-1]["link_id"] = "link-map-a-duplicate"
        self.save("record_evidence_links")
        result = self.validate()
        self.assertIn("DUPLICATE_EVIDENCE_LINK", {x.code for x in result.errors})

    def test_no_temporal_claim_belongs_in_pair_assessment_not_relation(self):
        self.rows["temporal_relations"][0]["relation_label"] = "NO_TEMPORAL_CLAIM"
        self.save("temporal_relations")
        result = self.validate()
        self.assertIn("NO_TEMPORAL_CLAIM_WRONG_REGISTER", {x.code for x in result.errors})

    def test_no_temporal_claim_assessment_is_permitted_with_rule(self):
        self.rows["candidate_pair_assessments"].append({
            **PARTITION, "assessment_id": "assessment-a-b", "event_a_id": "event-a", "event_b_id": "event-b",
            "candidate_rule_id": "same-scope-event-pairs", "candidate_rule_version": "0.1",
            "comparison_scope_id": "scope-incident", "scope_compatibility": "COMPATIBLE",
            "assessment_label": "NO_TEMPORAL_CLAIM", "related_relation_id": "",
            "assessment_reason": "Reviewed under synthetic candidate-pair rule", "adjudication_status": "UNREVIEWED",
            "assessment_notes": "",
        })
        self.save("candidate_pair_assessments")
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.errors])

    def test_accepted_a120_count_excludes_container_mapping(self):
        self.rows["activity_units"].append({
            **PARTITION, "activity_unit_id": "series-unit", "scope_id": "scope-incident",
            "parent_activity_unit_id": "", "granularity": "repeated_event_series", "unit_role": "series_container",
            "instance_status": "RESOLVED", "count_status": "qualitative_only", "count_exact": "",
            "count_min": "", "count_max": "", "count_qualitative": "repeated activity",
            "recurrence_pattern": "repeated", "unit_summary": "repeated actions", "actor_ref": "",
            "host_or_asset_ref": "", "annotator_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "unit_notes": "",
        })
        self.rows["event_mappings"].append({
            **PARTITION, "mapping_id": "map-series", "activity_unit_id": "series-unit", "event_instance_id": "",
            "exact_technique_id": "T1105", "exact_technique_name": "Ingress Tool Transfer", "attack_version": "synthetic",
            "mapping_basis": "report_explicit_parent", "mapping_decision_status": "ACCEPTED", "alternative_group_id": "",
            "alternative_to_mapping_id": "", "baseline_vocabulary_id": "CTI Evidence Lab A_120 selected-technique identifier vocabulary",
            "baseline_vocabulary_sha256": A120_HASH, "baseline_parent_technique_id": "T1105",
            "baseline_mapping_status": "IN_VOCAB", "annotator_confidence": "HIGH",
            "adjudication_status": "UNREVIEWED", "mapping_notes": "container mapping",
        })
        self.rows["record_evidence_links"].append({
            **PARTITION, "link_id": "link-map-series", "record_type": "event_mappings", "record_id": "map-series",
            "evidence_span_id": "span-a", "evidence_role": "MAPPING", "link_notes": "synthetic",
        })
        self.save("activity_units")
        self.save("event_mappings")
        self.save("record_evidence_links")
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.errors])
        self.assertEqual(result.accepted_a120_mappings, 2)

    def test_zero_edge_assessable_report_remains_in_eligible_denominator(self):
        self.rows["temporal_relations"] = []
        self.save("temporal_relations")
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.errors])
        self.assertEqual(result.eligible_reports, 1)
        self.assertEqual(result.assessable_reports, 1)
        self.assertEqual(result.primary_positive_temporal_edges, 0)

    def test_non_temporal_edge_does_not_enter_temporal_graph_count(self):
        self.rows["non_temporal_relations"].append({
            **PARTITION, "non_temporal_relation_id": "causal-a-b", "activity_unit_a_id": "event-a",
            "activity_unit_b_id": "event-b", "relation_label": "CAUSES_OR_ENABLES", "evidence_scope": "SENTENCE",
            "primary_evidence_span_id": "span-relation", "annotator_confidence": "HIGH",
            "adjudication_status": "UNREVIEWED", "relation_notes": "synthetic causal relation",
        })
        self.save("non_temporal_relations")
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.errors])
        self.assertEqual(result.primary_positive_temporal_edges, 1)

    def test_annotation_pass_partition_isolation(self):
        # A second annotator/pass can use the same local IDs without collision.
        second_partition = {"report_id": "r-test", "annotator_id": "annotator-2", "annotation_pass_id": "pass-1"}
        second_registry = dict(self.rows["report_registry"][0])
        second_registry.update(second_partition)
        self.rows["report_registry"].append(second_registry)
        for register in ("report_scopes", "activity_units", "evidence_spans", "event_mentions", "event_mappings", "temporal_relations", "record_evidence_links"):
            self.rows[register].extend([{**row, **second_partition} for row in self.rows[register]])
        for register in self.rows:
            self.save(register)
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.errors])
        self.assertEqual(result.primary_positive_temporal_edges, 2)
        # One report with two annotation partitions remains one report in the
        # report-level denominator; partition counts remain separately visible.
        self.assertEqual(result.eligible_reports, 1)
        self.assertEqual(result.assessable_reports, 1)
        self.assertEqual(result.eligible_report_partitions, 2)
        self.assertEqual(result.assessable_report_partitions, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)