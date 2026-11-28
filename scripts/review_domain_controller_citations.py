"""Generate a blank citation review packet and replay a completed review."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from examples.domain_controller_citation_roles import SUPPORT, run
from scripts.audit_rdp_case import verify
from scripts.investigate_sequence import load_case

GUIDE = """# Review of ordering citations

Open the publisher report linked in the form. Paragraph numbers count nonempty
HTML paragraphs from the start of the saved report, including the introductory
paragraphs. The case record uses collapsed whitespace and excludes captions
that are outside HTML paragraphs. Use nearby text to locate each passage.

Assess each proposed ordering using the two stated actions. For each row, list
every smallest-by-inclusion group of listed evidence IDs that establishes the
order. A group can contain one passage, or several passages when they are
jointly necessary. For example, use [["X1"], ["X2", "X3"]] if X1 alone suffices
and X2 plus X3 suffice together. Use [] if no listed set establishes the order.
Leave null if you cannot decide. Explain your reading and flag any uncertainty
about whether the passages describe the stated actions. Keep the form fields
and case identifiers intact. Fill only prior_exposure, support_sets and rationale.

Record prior_exposure as YES, NO or UNSURE based on whether you have seen the
project's answers for these citations. Work through the packet before opening
the project analysis. Return the completed JSON and, if available, the HTML
snapshot you used. Use only your assigned reviewer ID in the form.
"""


def form(case, reviewer):
    if not re.fullmatch(r"R[0-9]{2,4}", reviewer):
        raise ValueError("Use a pseudonymous reviewer ID such as R01")
    actions = {row["event_id"]: row["description"] for row in case["occurrences"]}
    paragraphs = {row["evidence_id"]: row["paragraph_number"] for row in case["evidence"]}
    return {
        "protocol": "domain-controller-citations-v1",
        "reviewer": reviewer,
        "source": case["source"]["url"],
        "paragraph_text_sha256": case["source"]["paragraph_text_sha256"],
        "prior_exposure": None,
        "rows": [{
            "id": row["relation_id"],
            "earlier_action": actions[row["source_event"]],
            "later_action": actions[row["target_event"]],
            "candidates": {e: paragraphs[e] for e in row["evidence_ids"]},
            "support_sets": None,
            "rationale": "",
        } for row in case["relations"]],
    }


def analyze(case, raw, source_html):
    submitted = json.loads(raw)
    expected = form(case, submitted["reviewer"])
    fields = {"support_sets", "rationale"}
    fixed_rows = [{k: v for k, v in row.items() if k not in fields} for row in submitted["rows"]]
    expected_rows = [{k: v for k, v in row.items() if k not in fields} for row in expected["rows"]]
    if (fixed_rows != expected_rows or
            {k: v for k, v in expected.items() if k not in {"rows", "prior_exposure"}} !=
            {k: v for k, v in submitted.items() if k not in {"rows", "prior_exposure"}}):
        raise ValueError("The return does not match the issued case form")
    if submitted.get("prior_exposure") not in ("YES", "NO", "UNSURE"):
        raise ValueError("Record prior exposure as YES, NO or UNSURE")
    support = {}
    for row in submitted["rows"]:
        groups = row["support_sets"]
        if groups is not None and (not isinstance(groups, list) or any(
            not isinstance(group, list) or not group or any(
                not isinstance(e, str) or e not in row["candidates"] for e in group
            ) or len(group) != len(set(group)) for group in groups
        )):
            raise ValueError(f"Invalid evidence groups for {row['id']}")
        if groups is not None:
            sets = [set(group) for group in groups]
            if any(left <= right for i, left in enumerate(sets) for j, right in enumerate(sets) if i != j):
                raise ValueError(f"Remove duplicate or redundant groups for {row['id']}")
        if not isinstance(row["rationale"], str) or not row["rationale"].strip():
            raise ValueError(f"Explain the judgment for {row['id']}")
        support[row["id"]] = groups
    complete = all(groups is not None for groups in support.values())
    return {
        "reviewer": submitted["reviewer"],
        "prior_exposure": submitted["prior_exposure"],
        "return_sha256": hashlib.sha256(raw).hexdigest(),
        "snapshot_check": verify(source_html.read_bytes(), case) if source_html else None,
        "matching_rows": [row for row, groups in support.items() if groups is not None and
                          {frozenset(g) for g in groups} == {frozenset(g) for g in SUPPORT[row]}],
        "unknown_rows": [row for row, groups in support.items() if groups is None],
        "query_cuts": run(support) if complete else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--reviewer")
    mode.add_argument("--return-form", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-html", type=Path)
    args = parser.parse_args()
    case = load_case("domain-controller")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.reviewer:
        with ZipFile(args.output, "x", ZIP_DEFLATED) as packet:
            packet.writestr("REVIEW_GUIDE.md", GUIDE)
            packet.writestr("review.json", json.dumps(form(case, args.reviewer), indent=2) + "\n")
    else:
        result = analyze(case, args.return_form.read_bytes(), args.source_html)
        with args.output.open("x", encoding="utf-8") as file:
            file.write(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
