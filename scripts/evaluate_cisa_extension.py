"""Compare explicit incident ordering in the two fixed CISA reports."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_rdp_case import digest
from scripts.evaluate_incident_holdout import TAXONOMY_SHA256, by_id, compare_graph, read_json

DIRECTORY = ROOT / "research/experiments/cisa_incident_extension_v0.1"
PRODUCTS = ("AA24-046A", "AA25-266A")
EXTRACTOR_VERSION = "6.21.4"


def canonical_page(page):
    return " ".join(page.extract_text(extraction_mode="layout").split())


def verify_pdf(path, case):
    from pypdf import PdfReader, __version__

    if __version__ != EXTRACTOR_VERSION:
        raise ValueError(f"Use pypdf {EXTRACTOR_VERSION} for the recorded page offsets")
    if digest(path.read_bytes()) != case["source"]["pdf_sha256"]:
        raise ValueError("PDF snapshot differs from the recorded advisory")
    with path.open("rb") as handle:
        reader = PdfReader(handle)
        pages = {e["page"]: canonical_page(reader.pages[e["page"] - 1]) for e in case["evidence"]}
    for span in case["evidence"]:
        page = pages[span["page"]]
        start, end = span["char_start"], span["char_end"]
        if digest(page) != span["page_sha256"] or not 0 <= start < end <= len(page):
            raise ValueError("Page text or evidence bounds differ")
        if digest(page[start:end]) != span["span_sha256"]:
            raise ValueError("Evidence span differs")


def run(pdf_directory=None):
    results = []
    for product_id in PRODUCTS:
        case = read_json(DIRECTORY / f"{product_id}.json")
        if case["product_id"] != product_id or case["independently_validated"] is not False:
            raise ValueError("Unexpected case identity or review status")
        if case["taxonomy"]["sha256"] != TAXONOMY_SHA256:
            raise ValueError("Unexpected taxonomy revision")
        if case["source"]["extractor_version"] != EXTRACTOR_VERSION:
            raise ValueError("Unexpected page extractor revision")
        evidence = by_id(case["evidence"], "evidence_id")
        nodes = by_id(case["occurrences"], "event_id")
        relations = list(by_id(case["relations"], "relation_id").values())
        for span in evidence.values():
            if span["page"] < 1 or not 0 <= span["char_start"] < span["char_end"]:
                raise ValueError("Invalid page evidence span")
            for field in ("page_sha256", "span_sha256"):
                if not re.fullmatch("[0-9a-f]{64}", span[field]):
                    raise ValueError("Invalid source hash")
        for row in [*nodes.values(), *relations, *case["exclusions"]]:
            if not row["evidence_ids"] or not set(row["evidence_ids"]) <= evidence.keys() or not row["rationale"].strip():
                raise ValueError("Missing evidence or interpretation rationale")
        mappings = {}
        for key, node in nodes.items():
            label = node["mapping"]
            if node["outcome"] not in {"REPORTED", "ATTEMPTED"}:
                raise ValueError("Unexpected action outcome")
            if label is not None and (not re.fullmatch(r"T[0-9]{4}", label)
                                      or label not in case["taxonomy"]["parent_definitions"]):
                raise ValueError("Mapping absent from recorded parent techniques")
            mappings[key] = {label} if label else set()
        if pdf_directory is not None:
            verify_pdf(pdf_directory / f"{product_id}.pdf", case)
        results.append({"product_id": product_id, "evidence_locators": len(evidence),
                        **compare_graph(mappings, relations, explain_unresolved=True)})
    return {"selected_reports": len(PRODUCTS), "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.pdf_directory)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized, encoding="utf-8", newline="")
    else:
        if json.loads(serialized) != read_json(DIRECTORY / "results.json"):
            raise SystemExit("CISA extension differs from the published results")
        count = sum(row["evidence_locators"] for row in result["cases"])
        print(f"Reproduced {len(result['cases'])} CISA reports and {count} locator records. "
              f"PDF mode: {'local bytes and spans rechecked' if args.pdf_directory else 'recorded locators only'}.")


if __name__ == "__main__":
    main()
