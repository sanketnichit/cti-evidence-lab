"""Recompute the frozen Microsoft comparison and optionally verify the two linked PDFs."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.evaluate_cisa_extension import summarize_pdf_case, verify_pdf
from scripts.evaluate_incident_holdout import read_json

DIRECTORY = ROOT / "research/experiments/microsoft_incident_series_v0.1"


def run(pdf_directory=None):
    case = read_json(DIRECTORY / "report-1.json")
    unavailable = read_json(DIRECTORY / "report-2-unavailable.json")
    if case["installment"] != 1 or unavailable["installment"] != 2:
        raise ValueError("Case records do not match the frozen installments")
    if (unavailable["availability"] != "PUBLISHER_LINK_POINTS_TO_DIFFERENT_REPORT"
            or unavailable["linked_document_installment"] != 4):
        raise ValueError("Unavailability record does not match the documented source mismatch")
    if case["source"]["pages_reviewed"] != list(range(1, case["source"]["page_count"] + 1)):
        raise ValueError("Page coverage differs from the recorded review")
    baseline = summarize_pdf_case(case)
    alternative = {**case, "relations": [*case["relations"], case["alternative_relation"]]}
    sensitivity = summarize_pdf_case(alternative)
    if pdf_directory is not None:
        verify_pdf(pdf_directory / "report-1.pdf", case)
        verify_pdf(pdf_directory / "excluded-report-4.pdf", unavailable)
    return {
        "selected_reports": 2,
        "reviewed_reports": 1,
        "cases": [
            {"installment": 1, "availability": "SOURCE_REVIEWED", **baseline,
             "post_review_sensitivity": {"added_relation": case["alternative_relation"]["relation_id"], **sensitivity}},
            {"installment": 2, "availability": unavailable["availability"],
             "linked_document_installment": unavailable["linked_document_installment"],
             "query_assessment": "NOT_EVALUATED_SOURCE_UNAVAILABLE", "query_errors": None},
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.pdf_directory)
    if args.output is not None:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        if result != read_json(DIRECTORY / "results.json"):
            raise SystemExit("Microsoft comparison differs from the published results")
        mode = "incident PDF and mislinked cover verified" if args.pdf_directory else "recorded evidence only"
        print(f"Reproduced both selected Microsoft entries. PDF mode: {mode}.")


if __name__ == "__main__":
    main()
