import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_reviewer_packets import csv_text
from scripts.compare_incident_reviews import prepare, summarize
from scripts.incident_source_review import FORMS, POSTS, manifest


def fixture_return(directory, reviewer, action_ids, pairs):
    directory.mkdir()
    (directory / "packet.json").write_text(json.dumps(manifest(reviewer)), encoding="utf-8")
    evidence = {"summary_paragraph": "1", "evidence_paraphrase": "Synthetic example.", "rationale": "Test fixture."}
    rows = {
        "reviews.csv": [
            {"post_id": post, "completion": completion, "prior_exposure": "NO", "notes": "Synthetic fixture."}
            for post, completion in zip(POSTS, ("COMPLETE", "INACCESSIBLE"))
        ],
        "actions.csv": [
            {"post_id": POSTS[0], "action_id": action, "description": "Synthetic action",
             "eligibility": "RETAINED", "outcome": "REPORTED", "technique_id": mapping, **evidence}
            for action, mapping in action_ids
        ],
        "relations.csv": [
            {"post_id": POSTS[0], "from_action": a, "to_action": b, "decision": decision, **evidence}
            for a, b, decision in pairs
        ],
    }
    for name, data in rows.items():
        (directory / name).write_text(csv_text(FORMS[name], data), encoding="utf-8")


class IncidentReviewComparisonTests(unittest.TestCase):
    def test_directional_missing_decisions_split_coverage_and_frozen_returns(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left, right = root / "left", root / "right"
            fixture_return(left, "R01", [("a", "T1000"), ("b", ""), ("c", "T1001"), ("d", ""), ("e", "")],
                           [("a", "b", "BEFORE"), ("c", "b", "UNCERTAIN"), ("b", "d", "BEFORE")])
            fixture_return(right, "R02", [("x", "T1000"), ("y", "T1000"), ("z", "T1001"), ("m", ""), ("n", "")],
                           [("y", "x", "BEFORE"), ("z", "y", "EXCLUDE")])
            alignment = root / "alignment.json"
            data = prepare(left, right)
            data["reports"][POSTS[0]].update(source_basis="MATCHING", source_note="Synthetic matching source.")
            data["reports"][POSTS[1]].update(source_basis="UNVERIFIED", source_note="Synthetic unavailable source.")
            groups = data["reports"][POSTS[0]]["groups"]
            for a, b in [(["a"], ["x"]), (["b"], ["y"]), (["c"], ["z"]), (["d"], ["m", "n"]), (["e"], [])]:
                groups.append({"left": a, "right": b, "reason": "Synthetic grouping."})
            alignment.write_text(json.dumps(data), encoding="utf-8")
            result = summarize(left, right, alignment)["reports"]
            report = result[POSTS[0]]
            self.assertEqual(report["alignment_groups"], {"one_to_one": 3, "split": 1, "unmatched_left": 1})
            self.assertEqual(report["relations_outside_aligned_retained_pairs"], [1, 0])
            self.assertEqual(report["candidate_pair_count"], 3)
            self.assertEqual(report["both_recorded_decisions"], 1)
            self.assertEqual(report["matching_recorded_decisions"], 0)
            self.assertIn({"left": "BEFORE", "right": "UNRECORDED", "count": 1}, report["relation_decisions"])
            self.assertIn({"left": "UNRECORDED", "right": "BEFORE", "count": 1}, report["relation_decisions"])
            self.assertIn({"left": "WITHHELD", "right": "T1000", "count": 1}, report["parent_mappings"])
            self.assertEqual(result[POSTS[1]]["comparison_status"], "UNASSESSED")
            self.assertNotIn("candidate_pairs", result[POSTS[1]])
            self.assertEqual(result[POSTS[1]]["profile_audit"]["status"], "UNASSESSED")
            self.assertEqual(report["profile_audit"]["witness_counts"]["possible"]["pooled"], 0)

            original = alignment.read_bytes()
            omitted = groups.pop()
            alignment.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "every submitted action"):
                summarize(left, right, alignment)
            groups.append(omitted)
            alignment.write_bytes(original)
            with (left / "packet.json").open("a", encoding="utf-8") as handle:
                handle.write("\n")
            with self.assertRaisesRegex(ValueError, "exact reviewer returns"):
                summarize(left, right, alignment)

    def test_profile_audit_does_not_promote_uncertain_edges_within_either_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left, right = root / "left", root / "right"
            fixture_return(left, "R01", [("a", "T1000"), ("b", ""), ("c", "T1002")],
                           [("a", "b", "BEFORE"), ("b", "c", "UNCERTAIN")])
            fixture_return(right, "R02", [("x", "T1000"), ("y", "T1001"), ("z", "T1002")],
                           [("x", "y", "EXCLUDE"), ("y", "z", "BEFORE")])
            data = prepare(left, right)
            data["reports"][POSTS[0]].update(
                source_basis="MATCHING", source_note="Synthetic matching source.",
                groups=[{"left": [a], "right": [b], "reason": "Synthetic match."} for a, b in zip("abc", "xyz")],
            )
            data["reports"][POSTS[1]].update(source_basis="UNVERIFIED", source_note="Synthetic unavailable source.")
            alignment = root / "alignment.json"
            alignment.write_text(json.dumps(data), encoding="utf-8")
            audit = summarize(left, right, alignment)["reports"][POSTS[0]]["profile_audit"]
            self.assertEqual(audit["before_edges"], [1, 1])
            self.assertEqual(audit["coherent"]["NOT_SUPPORTED"], 27)
            self.assertEqual(audit["witness_counts"], {
                "known": {"pooled": 1, "pooled_only": 1}, "possible": {"pooled": 3, "pooled_only": 3},
            })
            example = audit["pooled_only_examples"]["known"]
            self.assertEqual(example["query"], ["T1000", "T1001", "T1002"])
            self.assertEqual(example["aligned_actions"], [{"left": a, "right": b} for a, b in zip("abc", "xyz")])
            self.assertIn([1, 2], example["conflict"]["minimum_conflicts"])
