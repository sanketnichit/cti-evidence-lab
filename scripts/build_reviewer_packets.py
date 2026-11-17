"""Create separate, answer-free local calibration packets from verified sources.

Packets contain licensed source text and MUST stay under ignored outputs/.
They are not RECON partitions and cannot create formal analysis locks.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_pilot_sources import DRAFT, read_csv, verified_text

GUIDE = ROOT / "research/reviewer_kit/REVIEW_GUIDE.md"
FORMS = {
    "report_reviews.csv": ["report_id", "reviewer_id", "review_date", "minutes_spent", "prior_exposure", "source_read_completely", "text_sufficient", "report_genre", "source_scope_eligible", "resolved_attack_occurrences", "qualifying_temporal_pair", "uncertainty_or_missing_information", "rationale"],
    "activity_units.csv": ["report_id", "reviewer_id", "activity_id", "description", "activity_class", "occurrence_status", "incident_id", "evidence_start", "evidence_end", "confidence", "rationale"],
    "temporal_relations.csv": ["report_id", "reviewer_id", "relation_id", "source_activity_id", "target_activity_id", "relation", "evidence_basis", "evidence_start", "evidence_end", "shared_incident_supported", "confidence", "rationale"],
    "technique_mappings.csv": ["report_id", "reviewer_id", "activity_id", "technique_id", "mapping_status", "evidence_start", "evidence_end", "rationale"],
    "questions.csv": ["report_id", "reviewer_id", "question_id", "evidence_start", "evidence_end", "question"],
}


def csv_text(fields, rows=()):
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue()


def build(corpus_root, output_dir, recover_crlf=False):
    output_dir = Path(output_dir).resolve()
    allowed = (ROOT / "outputs").resolve()
    if not output_dir.is_relative_to(allowed):
        raise ValueError("Source-bearing review packets must be written under ignored outputs/")
    reports = read_csv(DRAFT / "report_assessment_draft.csv")
    # Prepare and verify every source before writing any packet.
    sources = {}
    metadata = []
    for report in reports:
        rid = report["report_id"]
        raw = (Path(corpus_root) / "text" / (rid + ".txt")).read_bytes()
        text, record = verified_text(raw, report["source_text_sha256"], recover_crlf)
        sources[f"sources/{rid}.txt"] = text
        metadata.append({"report_id": rid, "title": report["source_title"],
                         "publisher": report["donor"], "publisher_url": report["source_url"],
                         "corpus_revision": report["corpus_revision"], **record})
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for reviewer in ("R1", "R2"):
        files = {**sources, "REVIEW_GUIDE.md": GUIDE.read_text(encoding="utf-8")}
        files["START_HERE.md"] = (
            f"# CTI Evidence Lab — reviewer {reviewer}\n\n"
            "Thank you for helping review five cybersecurity reports. This is a protocol-calibration exercise, not a test with a hidden answer key.\n\n"
            "1. Read REVIEW_GUIDE.md. Use only your assigned reviewer ID.\n"
            "2. Open the five files in sources/ and complete report_reviews.csv for each.\n"
            "3. Record evidence-backed activity candidates and relations in the other forms. Uncertainty is a valid answer.\n"
            "4. Work independently. Do not view the other reviewer's forms, repository draft annotations, or proposed answers before returning your first pass.\n"
            "5. Zip the completed CSV forms plus manifest.json and return them to Sanket. Keep a copy of your original submission.\n\n"
            "Use a text editor or spreadsheet application for the CSV files; preserve the headers and UTF-8 encoding. Do not alter source files. Put questions in questions.csv.\n\n"
            "Do not claim you read a report completely unless you did. Record interruptions, prior exposure and time honestly. No signature or personal contact details are requested.\n"
        )
        for name, fields in FORMS.items():
            rows = [{"report_id": r["report_id"], "reviewer_id": reviewer} for r in reports] if name == "report_reviews.csv" else []
            files[name] = csv_text(fields, rows)
        files["ATTRIBUTION.md"] = (
            "# Source attribution and licence\n\n"
            "Corpus: AnnoCTR, by Lukas Lange and collaborators, Bosch Research and collaborators. "
            "https://github.com/boschresearch/anno-ctr-lrec-coling-2024\n\n"
            "Pinned revision: d510b6949e1938d47c93a43eedd562dc538439dc. "
            "Corpus text is supplied under CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/ . "
            "Original publishers retain their respective rights. Publisher titles and URLs are listed in manifest.json. "
            "The repository's software MIT licence does not relicense these texts. "
            "Source-derived annotation forms, when filled, must retain this attribution and the applicable ShareAlike terms.\n\n"
            "No source wording is edited. Where a local file has CRLF line endings, a derived LF copy is used only if it exactly reproduces the pinned source-text hash; the transformation and original hash are recorded in manifest.json.\n"
        )
        manifest = {
            "packet_version": "0.1", "reviewer_id": reviewer,
            "purpose": "INDEPENDENT_PROTOCOL_CALIBRATION_NOT_FORMAL_GOLD",
            "contains_proposed_answers": False, "sources": metadata,
            "files_sha256": {name: hashlib.sha256(text.encode()).hexdigest() for name, text in sorted(files.items())},
        }
        files["manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        path = output_dir / f"CTI_Evidence_Lab_Reviewer_{reviewer}_v0.1.zip"
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, text in sorted(files.items()):
                info = zipfile.ZipInfo(name, date_time=(2026, 11, 17, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, text.encode("utf-8"))
        paths.append(path)
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs/reviewer_packets")
    parser.add_argument("--recover-crlf", action="store_true")
    args = parser.parse_args()
    for path in build(args.corpus_root, args.output_dir, args.recover_crlf):
        print(path.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
