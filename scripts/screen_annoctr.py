"""Inventory AnnoCTR report files for a human annotation feasibility pilot.

This script performs file-level screening only. It does not infer event
instances, temporal relations, or annotation quality. A repeated technique
mention is a candidate locator, never evidence of repeated execution.

Expected input directory is the AnnoCTR/all folder containing:
  text/*.txt
  linking_mitre_only/*.json
  time/*.tml

Example:
  python scripts/screen_annoctr.py \
      --root /path/to/anno-ctr-lrec-coling-2024/AnnoCTR/all \
      --output data/annoctr_screening.csv

Only aggregate report-level counts are written to the CSV. Raw report text is
not copied, printed, or uploaded.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


TAG_NAMES = ("TIMEX3", "EVENT", "MAKEINSTANCE", "TLINK", "SIGNAL")
CYBER_SPECIFIC_TYPES = {"CON", "GROUP", "MALWARE", "TACTIC", "TECHNIQUE", "TOOL"}
VENDOR_MARKERS = {
    "intel471": "Intel471",
    "lab52": "Lab52 / S2 Grupo",
    "proofpoint": "Proofpoint",
    "quointelligence": "QuoIntelligence",
    "quoteintelligence": "QuoIntelligence",
    "zscaler": "ZScaler",
}


@dataclass
class ReportScreen:
    report_id: str
    source_vendor: str
    source_text_characters: int | None
    link_record_count: int | None
    technique_link_record_count: int | None
    valid_attack_technique_link_record_count: int | None
    unresolved_technique_link_record_count: int | None
    unique_technique_count: int | None
    cyber_specific_record_count: int | None
    cyber_specific_layer_present: bool | None
    repeated_technique_ids: str
    repeated_technique_mention_count: int | None
    timex3_count: int | None
    event_tag_count: int | None
    makeinstance_tag_count: int | None
    tlink_tag_count: int | None
    signal_tag_count: int | None
    text_file_present: bool
    linking_file_present: bool
    timeml_file_present: bool
    screening_status: str


def infer_vendor(report_id: str) -> str:
    """Infer a donor from the report identifier where the marker is explicit."""
    normalized = report_id.lower().replace("-", "_")
    for marker, vendor in VENDOR_MARKERS.items():
        if marker in normalized:
            return vendor
    return "UNKNOWN"


def read_json_records(path: Path) -> list[dict[str, Any]]:
    """Read either JSON/JSON-array or newline-delimited JSON link records."""
    content = path.read_text(encoding="utf-8-sig")
    if not content.strip():
        return []

    try:
        parsed = json.loads(content)
        if isinstance(parsed, list):
            return [row for row in parsed if isinstance(row, dict)]
        if isinstance(parsed, dict):
            return [parsed]
    except json.JSONDecodeError:
        pass

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"{path}: invalid JSON on line {line_number}: {exc}"
            ) from exc
        if isinstance(row, dict):
            records.append(row)
    return records


def extract_attack_technique_id(label_link: str) -> str | None:
    """Return an ATT&CK technique ID only for a canonical ATT&CK URL.

    Do not fall back to label_id: it is an AnnoCTR internal entity identifier,
    not an ATT&CK technique ID. Some TECHNIQUE rows have non-ATT&CK concept
    links and must not be treated as mapped ATT&CK techniques.
    """
    match = re.search(
        r"https?://attack\.mitre\.org/techniques/(T\d{4}(?:\.\d{3})?)(?:/|$)",
        label_link.strip(),
        flags=re.IGNORECASE,
    )
    return match.group(1).upper() if match else None


def count_timeml_tags(path: Path) -> dict[str, int]:
    """Count TimeML tags in source markup; no event relation is inferred."""
    content = path.read_text(encoding="utf-8-sig")
    return {
        name: len(re.findall(rf"<\s*{name}\b", content, flags=re.IGNORECASE))
        for name in TAG_NAMES
    }


def screen_one(
    report_id: str,
    *,
    text_dir: Path,
    linking_dir: Path,
    time_dir: Path,
) -> ReportScreen:
    text_path = text_dir / f"{report_id}.txt"
    linking_path = linking_dir / f"{report_id}.json"
    time_path = time_dir / f"{report_id}.tml"

    text_present = text_path.is_file()
    linking_present = linking_path.is_file()
    timeml_present = time_path.is_file()

    char_count = (
        len(text_path.read_text(encoding="utf-8-sig"))
        if text_present
        else None
    )

    link_records: list[dict[str, Any]] | None = None
    if linking_present:
        link_records = read_json_records(linking_path)

    technique_records = (
        [
            row for row in link_records
            if str(row.get("entity_type", "")).upper() == "TECHNIQUE"
        ]
        if link_records is not None
        else None
    )

    technique_frequency: Counter[str] = Counter()
    if technique_records is not None:
        for row in technique_records:
            technique_id = extract_attack_technique_id(
                str(row.get("label_link", ""))
            )
            if technique_id:
                technique_frequency[technique_id] += 1

    cyber_specific_records = (
        [
            row for row in link_records
            if str(row.get("entity_type", "")).upper() in CYBER_SPECIFIC_TYPES
        ]
        if link_records is not None
        else None
    )

    repeated = sorted(
        (technique_id, count)
        for technique_id, count in technique_frequency.items()
        if count > 1
    )
    repeated.sort(key=lambda item: (-item[1], item[0]))

    tags = (
        count_timeml_tags(time_path)
        if timeml_present
        else {name: -1 for name in TAG_NAMES}
    )

    missing = []
    if not text_present:
        missing.append("TEXT")
    if not linking_present:
        missing.append("LINKING")
    if not timeml_present:
        missing.append("TIMEML")

    return ReportScreen(
        report_id=report_id,
        source_vendor=infer_vendor(report_id),
        source_text_characters=char_count,
        link_record_count=len(link_records) if link_records is not None else None,
        technique_link_record_count=(
            len(technique_records) if technique_records is not None else None
        ),
        valid_attack_technique_link_record_count=(
            sum(technique_frequency.values()) if technique_records is not None else None
        ),
        unresolved_technique_link_record_count=(
            len(technique_records) - sum(technique_frequency.values())
            if technique_records is not None else None
        ),
        unique_technique_count=(
            len(technique_frequency) if technique_records is not None else None
        ),
        cyber_specific_record_count=(
            len(cyber_specific_records) if cyber_specific_records is not None else None
        ),
        cyber_specific_layer_present=(
            bool(cyber_specific_records) if cyber_specific_records is not None else None
        ),
        repeated_technique_ids=";".join(
            f"{technique_id}:{count}" for technique_id, count in repeated
        ),
        repeated_technique_mention_count=sum(
            count for _, count in repeated
        ) if technique_records is not None else None,
        timex3_count=tags["TIMEX3"] if timeml_present else None,
        event_tag_count=tags["EVENT"] if timeml_present else None,
        makeinstance_tag_count=tags["MAKEINSTANCE"] if timeml_present else None,
        tlink_tag_count=tags["TLINK"] if timeml_present else None,
        signal_tag_count=tags["SIGNAL"] if timeml_present else None,
        text_file_present=text_present,
        linking_file_present=linking_present,
        timeml_file_present=timeml_present,
        screening_status="OK" if not missing else "MISSING_" + "_".join(missing),
    )


def screen_corpus(root: Path) -> list[ReportScreen]:
    """Screen all report IDs present in the MITRE-only linking folder."""
    text_dir = root / "text"
    linking_dir = root / "linking_mitre_only"
    time_dir = root / "time"

    if not linking_dir.is_dir():
        raise FileNotFoundError(
            f"Expected linking folder not found: {linking_dir}"
        )

    # The public corpus also ships context/negative sampling variants for
    # some reports (e.g. *_w_con.json, *_w_neg.json,
    # *_w_con_w_neg.json). They are not separate reports and must not
    # inflate the inventory or appear as missing text/TimeML files.
    variant_suffix = re.compile(r"_w_(?:con|neg)(?:_w_neg)?$")
    report_ids = sorted(
        path.stem
        for path in linking_dir.glob("*.json")
        if not variant_suffix.search(path.stem)
    )
    results = [
        screen_one(
            report_id,
            text_dir=text_dir,
            linking_dir=linking_dir,
            time_dir=time_dir,
        )
        for report_id in report_ids
    ]
    return results


def write_csv(results: Iterable[ReportScreen], output: Path) -> None:
    """Write aggregate counts only; never copy source text to the report."""
    rows = [asdict(row) for row in results]
    output.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No report files were found to screen.")
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def print_summary(results: list[ReportScreen], top_per_vendor: int) -> None:
    print(f"Reports screened (full corpus): {len(results)}")
    cyber_reports = [row for row in results if row.cyber_specific_layer_present]
    print(f"Reports with cybersecurity-specific annotations: {len(cyber_reports)}")
    print(f"Reports with general-layer-only / no cyber-specific link records: {len(results) - len(cyber_reports)}")
    vendor_counts = Counter(row.source_vendor for row in results)
    for vendor, count in sorted(vendor_counts.items()):
        cyber_count = sum(
            1 for row in results
            if row.source_vendor == vendor and row.cyber_specific_layer_present
        )
        print(f"  {vendor}: {count} total ({cyber_count} with cyber-specific annotations)")

    print("\nReports with missing paired files:")
    missing = [row for row in results if row.screening_status != "OK"]
    if not missing:
        print("  none")
    else:
        for row in missing:
            print(f"  {row.report_id}: {row.screening_status}")

    print("\nCandidate locators by vendor (not event-instance labels):")
    for vendor in sorted(vendor_counts):
        candidates = [
            row for row in results
            if row.source_vendor == vendor
            and row.screening_status == "OK"
            and (row.repeated_technique_mention_count or 0) > 1
        ]
        candidates.sort(
            key=lambda row: (
                row.repeated_technique_mention_count or 0,
                row.technique_link_record_count or 0,
                row.source_text_characters or 0,
            ),
            reverse=True,
        )
        print(f"  {vendor}:")
        if not candidates:
            print("    no repeated technique-link mention candidates")
        for row in candidates[:top_per_vendor]:
            print(
                f"    {row.report_id} | "
                f"repeated_mentions={row.repeated_technique_mention_count} | "
                f"valid_attack_technique_links={row.valid_attack_technique_link_record_count} | "
                f"techniques={row.unique_technique_count} | "
                f"chars={row.source_text_characters} | "
                f"repeats={row.repeated_technique_ids}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Screen AnnoCTR files for human pilot candidate selection."
    )
    parser.add_argument(
        "--root",
        required=True,
        help="Path to AnnoCTR/all (not the repository root).",
    )
    parser.add_argument(
        "--output",
        default="data/annoctr_screening.csv",
        help="Output aggregate CSV path (default: data/annoctr_screening.csv).",
    )
    parser.add_argument(
        "--top-per-vendor",
        type=int,
        default=5,
        help="Number of candidate locators printed per vendor.",
    )
    args = parser.parse_args()

    if args.top_per_vendor < 1:
        parser.error("--top-per-vendor must be at least 1.")

    try:
        results = screen_corpus(Path(args.root).expanduser().resolve())
        output = Path(args.output).expanduser().resolve()
        write_csv(results, output)
        print_summary(results, args.top_per_vendor)
        print(f"\nAggregate screening CSV: {output}")
        print(
            "Reminder: repeated technique-linked mentions are candidate locators, "
            "not evidence of distinct executions."
        )
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
