"""Prepare and summarize a private alignment of two source-review returns."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.incident_source_review import FORMS, POSTS, load_return

METHOD = "incident-holdout-comparison-v0.1"


def file_hashes(directory):
    return {name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
            for name in ("packet.json", *FORMS)}


def read_inputs(left, right):
    submissions, bindings = [], []
    for directory in (left, right):
        hashes = file_hashes(directory)
        identity, reviews, actions, relations = load_return(directory)
        if file_hashes(directory) != hashes:
            raise ValueError("A reviewer return changed while being read")
        submissions.append((reviews, actions, relations))
        bindings.append({"reviewer_id": identity["reviewer_id"], "files_sha256": hashes})
    if bindings[0]["reviewer_id"] == bindings[1]["reviewer_id"]:
        raise ValueError("Use returns from two distinct reviewer IDs")
    return submissions, {"method": METHOD, "returns": bindings}


def prepare(left, right):
    _, header = read_inputs(left, right)
    return {**header, "reports": {
        post: {"source_basis": "", "source_note": "", "groups": []} for post in POSTS
    }}


def align(groups, left, right):
    if not isinstance(groups, list):
        raise ValueError("Alignment groups must be a list")
    available = [set(left), set(right)]
    matched = {}
    coverage = Counter()
    for group in groups:
        sides = [group["left"], group["right"]]
        if any(not isinstance(side, list) or any(not isinstance(action, str) for action in side) for side in sides):
            raise ValueError("Each side of an alignment group must be a list of action IDs")
        if not (sides[0] or sides[1]) or not group["reason"].strip():
            raise ValueError("Every alignment group needs actions and a reason")
        for side, remaining in zip(sides, available):
            if len(set(side)) != len(side) or not set(side) <= remaining:
                raise ValueError("An action ID is unknown or appears twice in the alignment")
            remaining.difference_update(side)
        a, b = sides
        if len(a) == len(b) == 1:
            matched[a[0]] = b[0]
            kind = "one_to_one"
        elif not a or not b:
            if len(a) + len(b) != 1:
                raise ValueError("Use one group per unmatched action")
            kind = "unmatched_left" if a else "unmatched_right"
        elif len(a) == 1:
            kind = "split"
        elif len(b) == 1:
            kind = "merge"
        else:
            kind = "many_to_many"
        coverage[kind] += 1
    if any(available):
        raise ValueError("Alignment does not account for every submitted action")
    return matched, dict(sorted(coverage.items()))


def counts(pairs):
    table = Counter(pairs)
    return [{"left": left, "right": right, "count": count} for (left, right), count in sorted(table.items())]


def report_comparison(post, group, submissions):
    reports, actions, relations = [], [], []
    for reviews, all_actions, all_relations in submissions:
        reports.append(next(row for row in reviews if row["post_id"] == post))
        actions.append({key: row for (case, key), row in all_actions.items() if case == post})
        relations.append({(source, target): row["decision"]
                          for (case, source, target), row in all_relations.items() if case == post})
    source = group["source_basis"]
    if source not in {"MATCHING", "DIFFERENT", "UNVERIFIED"} or not group["source_note"].strip():
        raise ValueError("Document the source basis and a note for every report")
    complete = all(row["completion"] == "COMPLETE" for row in reports)
    result = {
        "source_basis": source,
        "completion": [row["completion"] for row in reports],
        "prior_exposure": [row["prior_exposure"] for row in reports],
        "submitted_actions": [len(side) for side in actions],
        "submitted_relations": [len(side) for side in relations],
    }
    if not complete or source != "MATCHING":
        if group["groups"]:
            raise ValueError("Leave groups empty if either review is incomplete or the source basis is not matching")
        return {**result, "comparison_status": "UNASSESSED"}

    left, right = actions
    matched, coverage = align(group["groups"], left, right)
    retained = {a: b for a, b in matched.items()
                if left[a]["eligibility"] == right[b]["eligibility"] == "RETAINED"}
    reverse = {b: a for a, b in retained.items()}
    left_pairs = {pair: decision for pair, decision in relations[0].items() if set(pair) <= retained.keys()}
    right_pairs = {(reverse[a], reverse[b]): decision for (a, b), decision in relations[1].items()
                   if a in reverse and b in reverse}
    candidates = []
    for a, b in sorted(left_pairs.keys() | right_pairs.keys()):
        candidates.append({
            "left_pair": [a, b], "right_pair": [retained[a], retained[b]],
            "left_decision": left_pairs.get((a, b), "UNRECORDED"),
            "right_decision": right_pairs.get((a, b), "UNRECORDED"),
        })
    decisions = [(row["left_decision"], row["right_decision"]) for row in candidates]
    observed = [(a, b) for a, b in decisions if a != "UNRECORDED" and b != "UNRECORDED"]
    return {
        **result,
        "comparison_status": "DESCRIPTIVE_COMPARISON",
        "alignment_groups": coverage,
        "one_to_one_actions": len(matched),
        "eligibility": counts((left[a]["eligibility"], right[b]["eligibility"]) for a, b in matched.items()),
        "both_retained_actions": len(retained),
        "outcomes": counts((left[a]["outcome"], right[b]["outcome"]) for a, b in retained.items()),
        "parent_mappings": counts((left[a]["technique_id"] or "WITHHELD", right[b]["technique_id"] or "WITHHELD")
                                  for a, b in retained.items()),
        "candidate_pairs": candidates,
        "candidate_pair_count": len(candidates),
        "relation_decisions": counts(decisions),
        "relations_outside_aligned_retained_pairs": [len(relations[0]) - len(left_pairs), len(relations[1]) - len(right_pairs)],
        "both_recorded_decisions": len(observed),
        "matching_recorded_decisions": sum(a == b for a, b in observed),
    }


def summarize(left, right, alignment):
    submissions, header = read_inputs(left, right)
    raw = alignment.read_bytes()
    data = json.loads(raw)
    if any(data.get(field) != value for field, value in header.items()):
        raise ValueError("Alignment does not match the exact reviewer returns or method")
    if set(data["reports"]) != set(POSTS):
        raise ValueError("Alignment does not cover the frozen report set")
    return {**header, "alignment_sha256": hashlib.sha256(raw).hexdigest(), "reports": {
        post: report_comparison(post, data["reports"][post], submissions) for post in POSTS
    }}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--alignment", type=Path, help="Summarize this completed alignment. Omit to prepare a blank one.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = (summarize(args.left, args.right, args.alignment) if args.alignment
              else prepare(args.left, args.right))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
