"""Build answer-free holdout review packets and check returned CSV structure."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_reviewer_packets import csv_text
from scripts.evaluate_incident_holdout import DIRECTORY, FRAME, read_json
from src.occurrence_queries import validate as validate_ordering

VERSION = "incident-holdout-review-v0.1"
POSTS = ("21520", "22587")
FORMS = {
    "reviews.csv": ["post_id", "completion", "prior_exposure", "notes"],
    "actions.csv": ["post_id", "action_id", "description", "eligibility", "outcome",
                    "technique_id", "summary_paragraph", "evidence_paraphrase", "rationale"],
    "relations.csv": ["post_id", "from_action", "to_action", "decision", "summary_paragraph",
                      "evidence_paraphrase", "rationale"],
}


def manifest(reviewer):
    if not re.fullmatch(r"R[0-9]{2,4}", reviewer):
        raise ValueError("Reviewer ID must be pseudonymous, such as R01")
    return {"version": VERSION, "reviewer_id": reviewer, "post_ids": list(POSTS)}


def build(output, reviewer):
    identity = manifest(reviewer)
    sources = [
        {"post_id": post, "title": item["title"]["rendered"], "url": item["link"]}
        for item in read_json(FRAME)["returned_posts"] if (post := str(item["id"])) in POSTS
    ]
    if [row["post_id"] for row in sources] != list(POSTS):
        raise ValueError("Review sources do not match the frozen order")
    files = {
        "REVIEW_GUIDE.md": (DIRECTORY / "REVIEW_GUIDE.md").read_text(encoding="utf-8"),
        "packet.json": json.dumps(identity, indent=2) + "\n",
        "sources.csv": csv_text(["post_id", "title", "url"], sources),
    }
    for name, fields in FORMS.items():
        rows = [{"post_id": post} for post in POSTS] if name == "reviews.csv" else []
        files[name] = csv_text(fields, rows)
    output.mkdir(parents=True, exist_ok=True)
    path = output / f"incident-source-review-{reviewer}.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, text in files.items():
            archive.writestr(name, text.encode("utf-8"))
    return path


def rows(directory, name):
    with (directory / name).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FORMS[name]:
            raise ValueError(f"Unexpected headers in {name}")
        result = list(reader)
    if any(None in row or any(cell is None for cell in row.values()) for row in result):
        raise ValueError(f"Unexpected number of columns in {name}")
    return [{key: value.strip() for key, value in row.items()} for row in result]


def check_evidence(row, paragraph_limits):
    paragraph = row["summary_paragraph"]
    if not re.fullmatch(r"[1-9][0-9]*", paragraph) or not row["evidence_paraphrase"] or not row["rationale"]:
        raise ValueError("Every action and relation needs a summary paragraph, evidence paraphrase and rationale")
    if int(paragraph) > paragraph_limits[row["post_id"]]:
        raise ValueError("Evidence paragraph is outside the recorded Case Summary")


def validate(directory):
    identity = read_json(directory / "packet.json")
    if identity != manifest(identity["reviewer_id"]):
        raise ValueError("Unexpected packet identity or version")
    reviews = rows(directory, "reviews.csv")
    if [row["post_id"] for row in reviews] != list(POSTS):
        raise ValueError("Provide exactly one review per assigned post, in order")
    completion = {}
    paragraph_limits = {}
    for post in POSTS:
        first, last = read_json(DIRECTORY / f"{post}.json")["source"]["summary_paragraph_range"]
        paragraph_limits[post] = last - first + 1
    for row in reviews:
        if row["completion"] not in {"COMPLETE", "PARTIAL", "INACCESSIBLE"}:
            raise ValueError("Record a completion status for each report")
        if row["prior_exposure"] not in {"YES", "NO", "UNSURE"} or not row["notes"]:
            raise ValueError("Record prior exposure and notes for each report")
        completion[row["post_id"]] = row["completion"]
    actions = {}
    for row in rows(directory, "actions.csv"):
        post = row["post_id"]
        key = (post, row["action_id"])
        if post not in POSTS or completion[post] == "INACCESSIBLE" or not row["action_id"] or key in actions:
            raise ValueError("Unexpected or duplicate action identity")
        if row["eligibility"] not in {"RETAINED", "UNCERTAIN", "EXCLUDED"}:
            raise ValueError("Invalid action eligibility")
        if row["outcome"] not in {"REPORTED", "SUCCEEDED", "ATTEMPTED", "UNCERTAIN"} or not row["description"]:
            raise ValueError("Record the action outcome and description")
        if row["technique_id"] and not re.fullmatch(r"T[0-9]{4}", row["technique_id"]):
            raise ValueError("Use a parent technique identifier or leave the mapping empty")
        check_evidence(row, paragraph_limits)
        actions[key] = row
    links = set()
    before = {post: set() for post in POSTS}
    for row in rows(directory, "relations.csv"):
        post, source, target = row["post_id"], row["from_action"], row["to_action"]
        key = (post, source, target)
        if source == target or key in links or (post, source) not in actions or (post, target) not in actions:
            raise ValueError("Relations need unique ordered pairs of distinct known actions")
        if row["decision"] not in {"BEFORE", "UNCERTAIN", "EXCLUDE"}:
            raise ValueError("Invalid ordering decision")
        if row["decision"] == "BEFORE" and any(actions[(post, endpoint)]["eligibility"] != "RETAINED"
                                              for endpoint in (source, target)):
            raise ValueError("A retained BEFORE link requires retained endpoints")
        check_evidence(row, paragraph_limits)
        if row["decision"] == "BEFORE":
            before[post].add((source, target))
        links.add(key)
    for post in POSTS:
        validate_ordering({action: set() for case, action in actions if case == post}, before[post])
    return {"reviewer_id": identity["reviewer_id"], "reports": completion,
            "action_rows": len(actions), "relation_rows": len(links),
            "status": "STRUCTURE_CHECKED"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build", type=Path)
    mode.add_argument("--validate", type=Path)
    parser.add_argument("--reviewer")
    args = parser.parse_args()
    if args.build:
        if not args.reviewer:
            parser.error("--build requires --reviewer")
        print(build(args.build, args.reviewer).name)
    else:
        print(json.dumps(validate(args.validate), indent=2))


if __name__ == "__main__":
    main()
