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
from src.source_text_integrity import read_frozen_source  # noqa: E402

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
            "exact_technique_name": "Command and Scripting Interpreter", "attack_version": "Enterprise ATT&CK v12.1",
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

    def test_candidate_pair_assessment_requires_atomic_resolved_event_leaves(self):
        self.rows["temporal_relations"] = []
        unit = next(x for x in self.rows["activity_units"] if x["activity_unit_id"] == "event-b")
        unit.update(granularity="unresolved", unit_role="unresolved_unit", instance_status="UNRESOLVED")
        self.rows["event_mentions"] = [x for x in self.rows["event_mentions"] if x["activity_unit_id"] != "event-b"]
        self.rows["event_mappings"] = [x for x in self.rows["event_mappings"] if x["activity_unit_id"] != "event-b"]
        self.rows["candidate_pair_assessments"] = [{
            **PARTITION, "assessment_id": "assessment-a-b", "event_a_id": "event-a",
            "event_b_id": "event-b", "candidate_rule_id": "local-temporal-cue",
            "candidate_rule_version": "v1", "comparison_scope_id": "scope-incident",
            "scope_compatibility": "COMPATIBLE", "assessment_label": "NO_TEMPORAL_CLAIM",
            "related_relation_id": "", "assessment_reason": "Synthetic assessed pair",
            "adjudication_status": "UNREVIEWED", "assessment_notes": "synthetic",
        }]
        self.save("activity_units")
        self.save("event_mentions")
        self.save("event_mappings")
        self.save("temporal_relations")
        self.save("candidate_pair_assessments")
        result = self.validate()
        self.assertIn("INELIGIBLE_ASSESSMENT_ENDPOINT", {x.code for x in result.errors})

    def test_missing_source_text_is_warning_not_false_error(self):
        result = self.validate(source_texts=False)
        self.assertTrue(result.ok)
        self.assertTrue(any(x.code == "SOURCE_TEXT_NOT_SUPPLIED" for x in result.warnings))
        self.assertTrue(any(x.code == "ASSESSABLE_SOURCE_NOT_VERIFIED" for x in result.warnings))
        self.assertEqual(result.assessable_reports, 0)

    def test_verified_frozen_source_is_required_for_assessable_denominator(self):
        result = self.validate(source_texts=True)
        self.assertTrue(result.ok, [x for x in result.errors])
        self.assertEqual(result.eligible_reports, 1)
        self.assertEqual(result.assessable_reports, 1)

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

    def test_top_level_exact_technique_must_map_to_itself_as_parent(self):
        mapping = self.rows["event_mappings"][0]
        mapping.update(exact_technique_id="T1105", baseline_parent_technique_id="T1059")
        self.save("event_mappings")
        result = self.validate()
        self.assertIn("TOP_LEVEL_PARENT_MISMATCH", {x.code for x in result.errors})

    def test_subtechnique_parent_is_verified_against_pinned_crosswalk(self):
        mapping = self.rows["event_mappings"][0]
        mapping.update(
            exact_technique_id="T1059.001",
            exact_technique_name="PowerShell",
            attack_version="Enterprise ATT&CK v12.1",
            mapping_basis="report_explicit_subtechnique",
            baseline_parent_technique_id="T1059",
        )
        self.save("event_mappings")
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.errors])
        self.assertEqual(result.accepted_a120_mappings, 2)
        self.assertEqual(result.attack_crosswalk_count, 737)

    def test_subtechnique_wrong_but_valid_a120_parent_is_rejected(self):
        mapping = self.rows["event_mappings"][0]
        mapping.update(
            exact_technique_id="T1059.001",
            exact_technique_name="PowerShell",
            attack_version="Enterprise ATT&CK v12.1",
            mapping_basis="report_explicit_subtechnique",
            baseline_parent_technique_id="T1105",
        )
        self.save("event_mappings")
        result = self.validate()
        self.assertIn("EXACT_PARENT_MISMATCH", {x.code for x in result.errors})

    def test_unknown_exact_technique_cannot_be_promoted_using_a_valid_parent(self):
        mapping = self.rows["event_mappings"][0]
        mapping.update(
            exact_technique_id="T9999",
            baseline_parent_technique_id="T1059",
            attack_version="Enterprise ATT&CK v12.1",
        )
        self.save("event_mappings")
        result = self.validate()
        self.assertIn("EXACT_TECHNIQUE_NOT_IN_PINNED_RELEASE", {x.code for x in result.errors})

    def test_accepted_mapping_requires_the_pinned_attack_release(self):
        mapping = self.rows["event_mappings"][0]
        mapping["attack_version"] = "Enterprise ATT&CK v14.1"
        self.save("event_mappings")
        result = self.validate()
        self.assertIn("ATTACK_VERSION_MISMATCH", {x.code for x in result.errors})

    def test_revoked_subtechnique_is_not_counted_in_primary_a120(self):
        mapping = self.rows["event_mappings"][0]
        mapping.update(
            exact_technique_id="T1053.001",
            exact_technique_name="At (Linux)",
            attack_version="Enterprise ATT&CK v12.1",
            mapping_basis="report_explicit_subtechnique",
            baseline_parent_technique_id="T1053",
        )
        self.save("event_mappings")
        result = self.validate()
        self.assertIn("LIFECYCLE_FLAGGED_PRIMARY_MAPPING", {x.code for x in result.errors})

    def test_crosswalk_file_presence_does_not_bypass_hash_validation(self):
        mapping = self.rows["event_mappings"][0]
        mapping.update(exact_technique_id="T1059.001", baseline_parent_technique_id="T1059")
        self.save("event_mappings")
        (self.bundle / "vocabulary" / "A_120_Exact_to_Parent_Crosswalk_v0.1.csv").write_text(
            "not,a,verified,crosswalk\n", encoding="utf-8"
        )
        result = self.validate()
        self.assertIn("ATTACK_CROSSWALK_HASH_MISMATCH", {x.code for x in result.errors})

    def test_crosswalk_manifest_must_pin_the_verified_source_hash(self):
        manifest_path = self.bundle / "vocabulary" / "A_120_Exact_to_Parent_Crosswalk_v0.1.manifest.json"
        import json
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["source"]["sha256"] = "0" * 64
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        result = self.validate()
        self.assertIn("ATTACK_CROSSWALK_SOURCE_PIN_MISMATCH", {x.code for x in result.errors})

    def test_prior_exposure_status_is_controlled(self):
        self.rows["report_registry"][0]["prior_exposure_status"] = "MAYBE"
        self.save("report_registry")
        result = self.validate()
        self.assertIn("INVALID_PRIOR_EXPOSURE_STATUS", {x.code for x in result.errors})

    def test_direct_timestamp_requires_time_evidence_for_both_endpoints(self):
        self.rows["temporal_relations"][0]["relation_basis"] = "direct_timestamp"
        self.save("temporal_relations")
        result = self.validate()
        self.assertEqual(
            sum(x.code == "DIRECT_TIMESTAMP_ENDPOINT_TIME_MISSING" for x in result.errors),
            2,
        )

    def test_direct_timestamp_passes_with_normalized_evidence_for_both_endpoints(self):
        self.rows["temporal_relations"][0]["relation_basis"] = "direct_timestamp"
        for time_id, event_id, mention_id, span_id, raw, normalized in [
            ("time-a", "event-a", "mention-a", "span-a", "08:00", "2026-01-01T08:00:00Z"),
            ("time-b", "event-b", "mention-b", "span-b", "09:00", "2026-01-01T09:00:00Z"),
        ]:
            self.rows["time_evidence"].append({
                **PARTITION, "time_evidence_id": time_id, "activity_unit_id": event_id,
                "mention_id": mention_id, "raw_time_text": raw, "time_type": "ATTACK_OCCURRENCE",
                "time_precision": "HOUR", "timezone_text": "UTC", "timezone_status": "EXPLICIT",
                "normalized_start": normalized, "normalized_end": normalized,
                "normalized_timezone": "UTC", "normalization_status": "NORMALIZED",
                "uncertainty_notes": "synthetic", "primary_evidence_span_id": span_id,
                "annotator_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "time_notes": "",
            })
        self.save("temporal_relations")
        self.save("time_evidence")
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.errors])

    def test_duplicate_temporal_relation_is_rejected(self):
        duplicate = dict(self.rows["temporal_relations"][0])
        duplicate["relation_id"] = "rel-a-b-duplicate"
        self.rows["temporal_relations"].append(duplicate)
        self.save("temporal_relations")
        result = self.validate()
        self.assertIn("DUPLICATE_TEMPORAL_RELATION", {x.code for x in result.errors})

    def test_reciprocal_before_relations_are_rejected(self):
        reverse = dict(self.rows["temporal_relations"][0])
        reverse.update(relation_id="rel-b-a", event_a_id="event-b", event_b_id="event-a")
        self.rows["temporal_relations"].append(reverse)
        self.save("temporal_relations")
        result = self.validate()
        self.assertIn("CONTRADICTORY_TEMPORAL_RELATION", {x.code for x in result.errors})

    def test_before_and_overlap_for_same_event_pair_are_rejected(self):
        overlap = dict(self.rows["temporal_relations"][0])
        overlap.update(relation_id="rel-a-b-overlap", relation_label="OVERLAP")
        self.rows["temporal_relations"].append(overlap)
        self.save("temporal_relations")
        result = self.validate()
        self.assertIn("CONTRADICTORY_TEMPORAL_RELATION", {x.code for x in result.errors})

    def test_crlf_source_text_hash_and_offsets_are_preserved(self):
        crlf_source = SOURCE_TEXT + "\r\n"
        source_dir = self.bundle / "sources"
        source_dir.mkdir(parents=True, exist_ok=True)
        source_path = source_dir / "r-test.txt"
        source_path.write_bytes(crlf_source.encode("utf-8"))
        loaded_source = read_frozen_source(source_path)
        expected_hash = hashlib.sha256(crlf_source.encode("utf-8")).hexdigest()

        self.rows["report_registry"][0]["source_text_sha256"] = expected_hash
        self.rows["report_registry"][0]["source_text_char_count"] = str(len(crlf_source))
        for span in self.rows["evidence_spans"]:
            span["source_text_sha256"] = expected_hash
        self.save("report_registry")
        self.save("evidence_spans")

        result = validator.validate_bundle(
            self.bundle,
            {(
                PARTITION["report_id"], PARTITION["annotator_id"], PARTITION["annotation_pass_id"]
            ): loaded_source},
        )
        self.assertTrue(result.ok, [x for x in result.errors])
        self.assertEqual(len(loaded_source), len(SOURCE_TEXT) + 2)
        self.assertTrue(loaded_source.endswith("\r\n"))

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

    def test_positive_pair_assessment_must_match_linked_relation(self):
        self.rows["candidate_pair_assessments"].append({
            **PARTITION, "assessment_id": "assessment-a-b", "event_a_id": "event-a", "event_b_id": "event-b",
            "candidate_rule_id": "same-scope-event-pairs", "candidate_rule_version": "0.1",
            "comparison_scope_id": "scope-incident", "scope_compatibility": "COMPATIBLE",
            "assessment_label": "OVERLAP", "related_relation_id": "rel-a-b",
            "assessment_reason": "Synthetic mismatch probe", "adjudication_status": "UNREVIEWED",
            "assessment_notes": "",
        })
        self.save("candidate_pair_assessments")
        result = self.validate()
        self.assertIn("ASSESSMENT_RELATION_MISMATCH", {x.code for x in result.errors})

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
            "exact_technique_id": "T1105", "exact_technique_name": "Ingress Tool Transfer", "attack_version": "Enterprise ATT&CK v12.1",
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

    def test_zero_event_leaf_report_remains_assessable_after_completed_review(self):
        # A fully reviewed report with no resolved event leaves is still an
        # assessable zero outcome; event yield must not determine inclusion.
        for register in (
            "activity_units", "event_mentions", "event_mappings",
            "temporal_relations", "time_evidence", "candidate_pair_assessments",
            "non_temporal_relations", "record_evidence_links",
        ):
            self.rows[register] = []
            self.save(register)
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.errors])
        self.assertEqual(result.eligible_reports, 1)
        self.assertEqual(result.assessable_reports, 1)
        self.assertEqual(result.primary_positive_temporal_edges, 0)

    def test_assessable_report_is_not_in_denominator_until_full_review_complete(self):
        self.rows["report_registry"][0]["full_report_review_status"] = "IN_PROGRESS"
        self.save("report_registry")
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.errors])
        self.assertEqual(result.eligible_reports, 1)
        self.assertEqual(result.assessable_reports, 0)

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

    def test_conflicting_report_level_decisions_are_flagged_and_excluded(self):
        second_partition = {"report_id": "r-test", "annotator_id": "annotator-2", "annotation_pass_id": "pass-1"}
        second_registry = dict(self.rows["report_registry"][0])
        second_registry.update(second_partition)
        second_registry["source_scope_eligibility"] = "INELIGIBLE"
        second_registry["source_scope_reason"] = "Conflicting synthetic decision"
        second_registry["local_research_use_status"] = "NOT_PERMITTED"
        self.rows["report_registry"].append(second_registry)
        self.save("report_registry")
        result = self.validate()
        self.assertTrue(result.ok, [x for x in result.errors])
        self.assertEqual(result.report_level_decision_conflicts, 1)
        self.assertEqual(result.eligible_reports, 0)
        self.assertEqual(result.assessable_reports, 0)
        self.assertEqual(result.eligible_report_partitions, 1)
        self.assertIn("REPORT_LEVEL_DECISION_CONFLICT", {x.code for x in result.warnings})

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
        source_texts = {
            ("r-test", "annotator-1", "pass-1"): SOURCE_TEXT,
            ("r-test", "annotator-2", "pass-1"): SOURCE_TEXT,
        }
        result = validator.validate_bundle(self.bundle, source_texts)
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