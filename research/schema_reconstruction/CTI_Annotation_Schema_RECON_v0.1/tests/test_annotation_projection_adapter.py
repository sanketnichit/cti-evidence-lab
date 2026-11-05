import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "analysis"))
sys.path.insert(0, str(PACKAGE_ROOT / "validator"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from annotation_projection_adapter import AdapterError, build_projection_for_partition, compute_annotation_lock_reference  # noqa: E402
from test_validator import PARTITION, SOURCE_TEXT, make_fixture, write_register  # noqa: E402


class AnnotationProjectionAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.bundle = Path(self.temp.name) / "bundle"
        self.rows = make_fixture(self.bundle)

    def tearDown(self):
        self.temp.cleanup()

    def save(self, name):
        write_register(self.bundle, name, self.rows[name])

    def run_adapter(self, **overrides):
        args = {
            "report_id": PARTITION["report_id"],
            "annotator_id": PARTITION["annotator_id"],
            "annotation_pass_id": PARTITION["annotation_pass_id"],
            "source_text": SOURCE_TEXT,
            "annotation_lock_confirmed": True,
            "annotation_lock_reference": compute_annotation_lock_reference(
                self.bundle,
                report_id=PARTITION["report_id"],
                annotator_id=PARTITION["annotator_id"],
                annotation_pass_id=PARTITION["annotation_pass_id"],
                source_text=SOURCE_TEXT,
            ),
        }
        args.update(overrides)
        return build_projection_for_partition(self.bundle, **args)

    def test_projection_requires_explicit_annotation_lock(self):
        with self.assertRaisesRegex(AdapterError, "annotation-lock confirmation"):
            build_projection_for_partition(
                self.bundle,
                report_id=PARTITION["report_id"],
                annotator_id=PARTITION["annotator_id"],
                annotation_pass_id=PARTITION["annotation_pass_id"],
                source_text=SOURCE_TEXT,
            )

    def test_arbitrary_or_stale_lock_reference_is_rejected(self):
        original = compute_annotation_lock_reference(
            self.bundle, report_id=PARTITION["report_id"],
            annotator_id=PARTITION["annotator_id"],
            annotation_pass_id=PARTITION["annotation_pass_id"], source_text=SOURCE_TEXT,
        )
        self.rows["event_mentions"][0]["mention_notes"] = "changed after lock"
        self.save("event_mentions")
        with self.assertRaisesRegex(AdapterError, "does not match the current source"):
            self.run_adapter(annotation_lock_reference=original)

    def test_prior_exposure_is_surface_in_projection_output(self):
        self.rows["report_registry"][0]["prior_exposure_status"] = "AI_EXPOSED"
        self.save("report_registry")
        result = self.run_adapter()
        self.assertEqual(result["prior_exposure_status"], "AI_EXPOSED")
        self.assertTrue(result["prior_exposure_requires_caution"])

    def test_valid_partition_projects_only_primary_rows(self):
        result = self.run_adapter()
        self.assertEqual(result["status"], "SYNTHETIC_OR_REVIEWED_PARTITION_PROJECTION_NOT_A_RESEARCH_FINDING")
        self.assertEqual(result["counts"]["eligible_resolved_atomic_event_leaves"], 2)
        self.assertEqual(result["counts"]["accepted_a120_mapping_rows"], 2)
        self.assertEqual(result["counts"]["primary_direct_positive_temporal_relations"], 1)
        self.assertEqual(result["projection"]["counts"]["fully_omitted_edges"], 1)

    def test_mixed_annotator_rows_do_not_leak_across_partitions(self):
        p2 = {"report_id": "r-test", "annotator_id": "annotator-2", "annotation_pass_id": "pass-1"}
        registry = dict(self.rows["report_registry"][0]); registry.update(p2)
        self.rows["report_registry"].append(registry)
        for register in ("report_scopes", "activity_units", "event_mentions", "evidence_spans", "event_mappings", "temporal_relations", "record_evidence_links"):
            clones = [{**row, **p2} for row in self.rows[register]]
            self.rows[register].extend(clones)
        for mapping in self.rows["event_mappings"]:
            if mapping["annotator_id"] == "annotator-2":
                mapping["exact_technique_id"] = "T1105"
                mapping["exact_technique_name"] = "Ingress Tool Transfer"
                mapping["baseline_parent_technique_id"] = "T1105"
        for register in self.rows:
            self.save(register)
        result = self.run_adapter()
        self.assertEqual(result["counts"]["accepted_a120_mapping_rows"], 2)
        self.assertEqual(result["projection"]["counts"]["unique_techniques"], 1)

    def test_container_mapping_is_not_used_for_primary_event_mapping(self):
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
            "baseline_vocabulary_sha256": "97b599ffdcfcc5864a9352cf1467de0f6cac92f9141053a76098e4f2d33fb1bc",
            "baseline_parent_technique_id": "T1105", "baseline_mapping_status": "IN_VOCAB",
            "annotator_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "mapping_notes": "container mapping",
        })
        self.rows["record_evidence_links"].append({
            **PARTITION, "link_id": "link-series", "record_type": "event_mappings", "record_id": "map-series",
            "evidence_span_id": "span-a", "evidence_role": "MAPPING", "link_notes": "synthetic",
        })
        for register in ("activity_units", "event_mappings", "record_evidence_links"):
            self.save(register)
        result = self.run_adapter()
        self.assertEqual(result["counts"]["eligible_resolved_atomic_event_leaves"], 2)
        self.assertEqual(result["counts"]["accepted_a120_mapping_rows"], 2)
        self.assertEqual(result["mapping_filter"]["excluded_non_event_unit"], 1)

    def test_nonprimary_temporal_relation_is_not_projected(self):
        inferred = dict(self.rows["temporal_relations"][0])
        inferred.update(relation_id="rel-inferred", relation_basis="inference")
        self.rows["temporal_relations"].append(inferred)
        self.save("temporal_relations")
        result = self.run_adapter()
        self.assertEqual(result["counts"]["primary_direct_positive_temporal_relations"], 1)
        self.assertEqual(result["counts"]["retained_nonprimary_or_nonpositive_temporal_relation_rows"], 1)

    def test_empty_mapping_sets_keep_relation_as_unmapped_endpoint(self):
        self.rows["event_mappings"] = []
        self.rows["record_evidence_links"] = []
        self.save("event_mappings")
        self.save("record_evidence_links")
        result = self.run_adapter()
        self.assertEqual(result["counts"]["accepted_a120_mapping_rows"], 0)
        self.assertEqual(result["projection"]["counts"]["unmapped_endpoint_edges"], 1)

    def test_scope_or_structure_error_stops_adapter(self):
        other_scope = {
            **PARTITION, "scope_id": "other-scope", "parent_scope_id": "", "scope_type": "INCIDENT",
            "scope_label": "Other", "scope_description": "Other event context", "scope_status": "RESOLVED",
            "scope_confidence": "HIGH", "adjudication_status": "UNREVIEWED", "scope_notes": "",
        }
        self.rows["report_scopes"].append(other_scope)
        next(row for row in self.rows["activity_units"] if row["activity_unit_id"] == "event-b")["scope_id"] = "other-scope"
        self.save("report_scopes"); self.save("activity_units")
        with self.assertRaisesRegex(AdapterError, "Schema validation failed"):
            self.run_adapter()

    def test_incomplete_report_is_blocked(self):
        self.rows["report_registry"][0]["full_report_review_status"] = "IN_PROGRESS"
        self.save("report_registry")
        with self.assertRaisesRegex(AdapterError, "not marked COMPLETE"):
            self.run_adapter()

    def test_ineligible_or_unpermitted_report_is_blocked(self):
        self.rows["report_registry"][0]["local_research_use_status"] = "UNRESOLVED"
        self.save("report_registry")
        with self.assertRaisesRegex(AdapterError, "local_research_use_status"):
            self.run_adapter()


if __name__ == "__main__":
    unittest.main(verbosity=2)
