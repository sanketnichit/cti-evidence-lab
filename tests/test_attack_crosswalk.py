"""Synthetic tests for the pinned ATT&CK exact-to-parent crosswalk builder."""

import unittest

from scripts.build_attack_crosswalk import build_crosswalk_records


def attack_pattern(stix_id, external_id, name, is_sub=False, revoked=False, deprecated=False):
    return {
        "type": "attack-pattern",
        "id": stix_id,
        "name": name,
        "external_references": [
            {"source_name": "mitre-attack", "external_id": external_id}
        ],
        "x_mitre_is_subtechnique": is_sub,
        "revoked": revoked,
        "x_mitre_deprecated": deprecated,
    }


def relationship(source, target):
    return {
        "type": "relationship",
        "relationship_type": "subtechnique-of",
        "source_ref": source,
        "target_ref": target,
    }


class AttackCrosswalkTests(unittest.TestCase):
    def setUp(self):
        self.parent = attack_pattern("attack-pattern--parent", "T1000", "Parent")
        self.other = attack_pattern("attack-pattern--other", "T2000", "Other")
        self.sub = attack_pattern(
            "attack-pattern--sub", "T2000.001", "Sub-technique", is_sub=True
        )
        self.bundle = {
            "objects": [
                self.parent,
                self.other,
                self.sub,
                relationship(self.sub["id"], self.parent["id"]),
            ]
        }

    def test_top_level_technique_maps_to_itself(self):
        rows, counts = build_crosswalk_records({"objects": [self.parent]}, ["T1000"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["exact_technique_id"], "T1000")
        self.assertEqual(rows[0]["parent_technique_id"], "T1000")
        self.assertEqual(rows[0]["relationship_type"], "self")
        self.assertEqual(counts["top_level_techniques"], 1)

    def test_subtechnique_parent_comes_from_explicit_relationship(self):
        rows, _ = build_crosswalk_records(self.bundle, ["T1000"])
        sub_row = next(row for row in rows if row["exact_technique_id"] == "T2000.001")
        self.assertEqual(sub_row["parent_technique_id"], "T1000")
        self.assertEqual(sub_row["relationship_type"], "subtechnique-of")
        self.assertEqual(sub_row["relationship_source_object_id"], self.sub["id"])
        self.assertEqual(sub_row["relationship_target_object_id"], self.parent["id"])

    def test_subtechnique_without_parent_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            build_crosswalk_records({"objects": [self.parent, self.sub]}, ["T1000"])

    def test_subtechnique_with_two_parents_fails_closed(self):
        second_parent = attack_pattern("attack-pattern--second", "T3000", "Second")
        bundle = {
            "objects": [
                self.parent,
                self.other,
                second_parent,
                self.sub,
                relationship(self.sub["id"], self.parent["id"]),
                relationship(self.sub["id"], second_parent["id"]),
            ]
        }
        with self.assertRaisesRegex(ValueError, "exactly one"):
            build_crosswalk_records(bundle, ["T1000"])

    def test_subtechnique_cannot_have_subtechnique_parent(self):
        parent_sub = attack_pattern(
            "attack-pattern--parent-sub", "T1000.001", "Parent sub", is_sub=True
        )
        bundle = {
            "objects": [
                self.parent,
                parent_sub,
                self.sub,
                relationship(self.sub["id"], parent_sub["id"]),
                relationship(parent_sub["id"], self.parent["id"]),
            ]
        }
        with self.assertRaisesRegex(ValueError, "itself a sub-technique"):
            build_crosswalk_records(bundle, ["T1000"])

    def test_valid_but_unrelated_a120_parent_is_not_inferred_from_id(self):
        rows, _ = build_crosswalk_records(self.bundle, ["T1000"])
        sub_row = next(row for row in rows if row["exact_technique_id"] == "T2000.001")
        self.assertEqual(sub_row["parent_technique_id"], "T1000")
        self.assertNotEqual(sub_row["parent_technique_id"], "T2000")

    def test_revoked_and_deprecated_flags_are_preserved(self):
        flagged = attack_pattern(
            "attack-pattern--flagged", "T4000", "Flagged", revoked=True, deprecated=True
        )
        rows, _ = build_crosswalk_records({"objects": [flagged]}, ["T4000"])
        self.assertEqual(rows[0]["revoked"], "true")
        self.assertEqual(rows[0]["deprecated"], "true")

    def test_parent_outside_a120_is_retained_and_marked_out_of_vocabulary(self):
        rows, _ = build_crosswalk_records(self.bundle, ["T2000"])
        parent_row = next(row for row in rows if row["exact_technique_id"] == "T1000")
        self.assertEqual(parent_row["parent_in_A_120"], "false")
        self.assertEqual(parent_row["parent_technique_id"], "T1000")

    def test_dangling_relationship_fails_closed(self):
        bad = relationship(self.sub["id"], "attack-pattern--missing")
        with self.assertRaisesRegex(ValueError, "Dangling"):
            build_crosswalk_records({"objects": [self.parent, self.sub, bad]}, ["T1000"])

    def test_duplicate_exact_ids_fail_closed(self):
        duplicate = attack_pattern("attack-pattern--duplicate", "T1000", "Duplicate")
        with self.assertRaisesRegex(ValueError, "Duplicate exact"):
            build_crosswalk_records({"objects": [self.parent, duplicate]}, ["T1000"])


if __name__ == "__main__":
    unittest.main()
