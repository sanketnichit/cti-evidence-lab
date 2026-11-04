"""Build the pinned Enterprise ATT&CK v12.1 exact-to-parent crosswalk.

The script never guesses a parent from an ID string. Sub-technique parents are
resolved only through explicit STIX relationship objects of type
subtechnique-of.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "Enterprise ATT&CK v12.1"
SOURCE_RELATIVE_PATH = "enterprise-attack/enterprise-attack-12.1.json"
SOURCE_URL = (
    "https://github.com/mitre-attack/attack-stix-data/blob/master/"
    "enterprise-attack/enterprise-attack-12.1.json"
)
SOURCE_RAW_URL = (
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/"
    "enterprise-attack/enterprise-attack-12.1.json"
)
EXPECTED_STIX_GIT_BLOB_SHA1 = "7a99efb3a8c89b06dd9db1a9a17e4201160ac4ee"
EXPECTED_STIX_SHA256 = "e84679af4bc46bba2ba92f60182101f146d5b966898e47924de7321e6bffeaa1"
A120_RELATIVE_PATH = (
    "research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/"
    "vocabulary/A_120_ChronoCTI_Selected_Technique_IDs_derived_v0.1.json"
)
EXPECTED_A120_SHA256 = "97b599ffdcfcc5864a9352cf1467de0f6cac92f9141053a76098e4f2d33fb1bc"
EXPECTED_COUNTS = {
    "attack_pattern_objects": 737,
    "unique_exact_technique_ids": 737,
    "top_level_techniques": 333,
    "sub_techniques": 404,
    "subtechnique_of_relationships": 404,
}
ID_PATTERN = re.compile(r"^T[0-9]{4}(?:\.[0-9]{3})?$")

FIELDNAMES = [
    "attack_release",
    "exact_technique_id",
    "exact_technique_name",
    "stix_object_id",
    "is_subtechnique",
    "parent_technique_id",
    "parent_technique_name",
    "parent_in_A_120",
    "revoked",
    "deprecated",
    "relationship_type",
    "relationship_source_object_id",
    "relationship_target_object_id",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def resolve_stix_path(stix_path: Path | None, download: bool) -> Path:
    if not download:
        if stix_path is None:
            raise ValueError("Pass --stix PATH or use --download")
        return stix_path

    if stix_path is None:
        import tempfile

        stix_path = (
            Path(tempfile.gettempdir())
            / "cti-evidence-lab"
            / "enterprise-attack-12.1.json"
        )
    if stix_path.is_file():
        existing = stix_path.read_bytes()
        if (
            sha256_bytes(existing) == EXPECTED_STIX_SHA256
            and git_blob_sha1(existing) == EXPECTED_STIX_GIT_BLOB_SHA1
        ):
            return stix_path

    request = Request(
        SOURCE_RAW_URL,
        headers={
            "User-Agent": "CTI-Evidence-Lab-crosswalk-builder/0.1",
            "Accept-Encoding": "identity",
        },
    )
    with urlopen(request, timeout=180) as response:
        source_bytes = response.read()
    actual_sha256 = sha256_bytes(source_bytes)
    actual_blob_sha1 = git_blob_sha1(source_bytes)
    if (
        actual_sha256 != EXPECTED_STIX_SHA256
        or actual_blob_sha1 != EXPECTED_STIX_GIT_BLOB_SHA1
    ):
        raise ValueError(
            "Downloaded STIX file did not match the pinned input: "
            f"bytes={len(source_bytes)}, sha256={actual_sha256}, "
            f"git_blob_sha1={actual_blob_sha1}, "
            f"expected_sha256={EXPECTED_STIX_SHA256}, "
            f"expected_git_blob_sha1={EXPECTED_STIX_GIT_BLOB_SHA1}"
        )
    stix_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = stix_path.with_name(stix_path.name + ".download")
    try:
        temporary_path.write_bytes(source_bytes)
        temporary_path.replace(stix_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return stix_path


def load_a120(path: Path) -> tuple[list[str], str]:
    raw = path.read_bytes()
    digest = sha256_bytes(raw)
    if digest != EXPECTED_A120_SHA256:
        raise ValueError(
            f"A_120 artifact SHA-256 mismatch: expected {EXPECTED_A120_SHA256}, got {digest}"
        )
    payload = json.loads(raw.decode("utf-8"))
    ids = payload.get("technique_ids")
    if not isinstance(ids, list) or len(ids) != 120:
        raise ValueError("A_120 artifact must contain exactly 120 technique_ids")
    if any(not isinstance(value, str) or not ID_PATTERN.fullmatch(value) for value in ids):
        raise ValueError("A_120 contains an invalid ATT&CK technique identifier")
    if len(set(ids)) != 120:
        raise ValueError("A_120 contains duplicate identifiers")
    return ids, digest


def _external_attack_id(obj: dict[str, Any]) -> str:
    refs = obj.get("external_references")
    if not isinstance(refs, list):
        raise ValueError(f"Missing external_references for {obj.get('id')}")
    values = {
        ref.get("external_id")
        for ref in refs
        if isinstance(ref, dict)
        and ref.get("source_name") == "mitre-attack"
        and isinstance(ref.get("external_id"), str)
        and ID_PATTERN.fullmatch(ref["external_id"])
    }
    if len(values) != 1:
        raise ValueError(
            f"Expected exactly one MITRE ATT&CK external ID for {obj.get('id')}; found {sorted(values)}"
        )
    return next(iter(values))


def build_crosswalk_records(
    bundle: dict[str, Any], a120_ids: list[str]
) -> tuple[list[dict[str, str]], dict[str, int]]:
    """Validate STIX parent links and return one row for every exact technique ID."""
    objects = bundle.get("objects")
    if not isinstance(objects, list):
        raise ValueError("STIX bundle must contain an objects list")

    attack_patterns: dict[str, dict[str, Any]] = {}
    exact_to_object: dict[str, str] = {}
    for obj in objects:
        if not isinstance(obj, dict) or obj.get("type") != "attack-pattern":
            continue
        stix_id = obj.get("id")
        if not isinstance(stix_id, str) or not stix_id.startswith("attack-pattern--"):
            raise ValueError("Attack-pattern object has a missing or invalid STIX id")
        if stix_id in attack_patterns:
            raise ValueError(f"Duplicate STIX attack-pattern object id: {stix_id}")
        exact_id = _external_attack_id(obj)
        if exact_id in exact_to_object:
            raise ValueError(f"Duplicate exact ATT&CK external id: {exact_id}")
        attack_patterns[stix_id] = obj
        exact_to_object[exact_id] = stix_id

    parent_relations: dict[str, list[dict[str, Any]]] = {}
    relationship_count = 0
    for obj in objects:
        if not isinstance(obj, dict):
            continue
        if obj.get("type") != "relationship" or obj.get("relationship_type") != "subtechnique-of":
            continue
        relationship_count += 1
        source = obj.get("source_ref")
        target = obj.get("target_ref")
        if source not in attack_patterns or target not in attack_patterns:
            raise ValueError(
                f"Dangling subtechnique-of relationship: {source!r} -> {target!r}"
            )
        parent_relations.setdefault(source, []).append(obj)

    a120 = set(a120_ids)
    rows: list[dict[str, str]] = []
    top_level = 0
    sub_techniques = 0

    for exact_id, stix_id in sorted(exact_to_object.items()):
        obj = attack_patterns[stix_id]
        is_sub = obj.get("x_mitre_is_subtechnique") is True
        links = parent_relations.get(stix_id, [])
        if is_sub:
            sub_techniques += 1
            if len(links) != 1:
                raise ValueError(
                    f"Sub-technique {exact_id} must have exactly one subtechnique-of relationship; found {len(links)}"
                )
            link = links[0]
            parent_stix_id = link["target_ref"]
            parent_obj = attack_patterns[parent_stix_id]
            if parent_obj.get("x_mitre_is_subtechnique") is True:
                raise ValueError(f"Sub-technique parent is itself a sub-technique: {exact_id}")
            parent_id = _external_attack_id(parent_obj)
            relation_type = "subtechnique-of"
            relation_source = link["source_ref"]
            relation_target = link["target_ref"]
        else:
            top_level += 1
            if links:
                raise ValueError(
                    f"Top-level technique {exact_id} incorrectly has a subtechnique-of source relationship"
                )
            parent_id = exact_id
            parent_obj = obj
            relation_type = "self"
            relation_source = stix_id
            relation_target = stix_id

        rows.append(
            {
                "attack_release": RELEASE,
                "exact_technique_id": exact_id,
                "exact_technique_name": str(obj.get("name") or ""),
                "stix_object_id": stix_id,
                "is_subtechnique": str(is_sub).lower(),
                "parent_technique_id": parent_id,
                "parent_technique_name": str(parent_obj.get("name") or ""),
                "parent_in_A_120": str(parent_id in a120).lower(),
                "revoked": str(bool(obj.get("revoked", False))).lower(),
                "deprecated": str(bool(obj.get("x_mitre_deprecated", False))).lower(),
                "relationship_type": relation_type,
                "relationship_source_object_id": relation_source,
                "relationship_target_object_id": relation_target,
            }
        )

    missing_a120 = sorted(a120 - set(exact_to_object))
    if missing_a120:
        raise ValueError(f"A_120 ids missing from the pinned release: {missing_a120}")
    wrongly_subtechnique = [
        row["exact_technique_id"]
        for row in rows
        if row["exact_technique_id"] in a120 and row["is_subtechnique"] == "true"
    ]
    if wrongly_subtechnique:
        raise ValueError(f"A_120 IDs must be top-level techniques: {wrongly_subtechnique}")

    counts = {
        "attack_pattern_objects": len(attack_patterns),
        "unique_exact_technique_ids": len(exact_to_object),
        "top_level_techniques": top_level,
        "sub_techniques": sub_techniques,
        "subtechnique_of_relationships": relationship_count,
        "A_120_ids_found": len(a120 & set(exact_to_object)),
        "A_120_ids_top_level": len(a120) - len(wrongly_subtechnique),
    }
    return rows, counts


def verify_release_counts(counts: dict[str, int]) -> None:
    for key, expected in EXPECTED_COUNTS.items():
        observed = counts.get(key)
        if observed != expected:
            raise ValueError(
                f"Pinned v12.1 preflight count mismatch for {key}: expected {expected}, got {observed}"
            )
    if counts.get("A_120_ids_found") != 120 or counts.get("A_120_ids_top_level") != 120:
        raise ValueError("The pinned A_120 vocabulary is not fully represented as top-level techniques")


def write_crosswalk(
    rows: list[dict[str, str]],
    source_path: Path,
    a120_path: Path,
    output_csv: Path,
    manifest_path: Path,
    counts: dict[str, int],
    a120_sha256: str,
) -> dict[str, Any]:
    import io

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    csv_bytes = buffer.getvalue().encode("utf-8")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_csv.write_bytes(csv_bytes)

    source_bytes = source_path.read_bytes()
    manifest = {
        "artifact_name": "CTI Evidence Lab A_120 exact-to-parent crosswalk",
        "artifact_version": "v0.1",
        "status": "GENERATED_FROM_HASH_VERIFIED_ENTERPRISE_ATTACK_V12_1",
        "attack_release": RELEASE,
        "source": {
            "repository": "https://github.com/mitre-attack/attack-stix-data",
            "path": SOURCE_RELATIVE_PATH,
            "url": SOURCE_URL,
            "git_blob_sha1": git_blob_sha1(source_bytes),
            "sha256": sha256_bytes(source_bytes),
            "size_bytes": len(source_bytes),
        },
        "a120": {
            "path": str(a120_path),
            "sha256": a120_sha256,
            "record_count": 120,
        },
        "generation": {
            "script": "scripts/build_attack_crosswalk.py",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "record_count": len(rows),
            "counts": counts,
        },
        "output": {
            "path": str(output_csv),
            "sha256": sha256_bytes(csv_bytes),
        },
        "policy": {
            "top_level_parent": "self",
            "subtechnique_parent": "explicit STIX subtechnique-of relationship only",
            "no_id_truncation": True,
            "revoked_and_deprecated": "preserved as flags; no automatic replacement",
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )
    return manifest


def main() -> int:
    default_a120 = ROOT / A120_RELATIVE_PATH
    default_output = (
        ROOT
        / "research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/"
        / "vocabulary/A_120_Exact_to_Parent_Crosswalk_v0.1.csv"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stix", type=Path, help="Local Enterprise ATT&CK v12.1 STIX JSON file")
    parser.add_argument("--download", action="store_true", help="Download the official release and verify its pinned hashes")
    parser.add_argument("--a120", type=Path, default=default_a120)
    parser.add_argument("--output-csv", type=Path, default=default_output)
    parser.add_argument("--manifest", type=Path, default=default_output.with_suffix(".manifest.json"))
    args = parser.parse_args()

    try:
        stix_path = resolve_stix_path(args.stix, args.download)
        source_bytes = stix_path.read_bytes()
        actual_sha256 = sha256_bytes(source_bytes)
        actual_blob_sha1 = git_blob_sha1(source_bytes)
        if actual_sha256 != EXPECTED_STIX_SHA256:
            raise ValueError(
                f"STIX SHA-256 mismatch: expected {EXPECTED_STIX_SHA256}, got {actual_sha256}"
            )
        if actual_blob_sha1 != EXPECTED_STIX_GIT_BLOB_SHA1:
            raise ValueError(
                f"STIX Git blob SHA-1 mismatch: expected {EXPECTED_STIX_GIT_BLOB_SHA1}, got {actual_blob_sha1}"
            )
        a120_ids, a120_sha = load_a120(args.a120)
        bundle = json.loads(source_bytes.decode("utf-8"))
        rows, counts = build_crosswalk_records(bundle, a120_ids)
        verify_release_counts(counts)
        manifest = write_crosswalk(
            rows, stix_path, args.a120, args.output_csv, args.manifest, counts, a120_sha
        )
        print(f"Release: {RELEASE}")
        print(f"Exact technique rows: {len(rows)}")
        print(f"Top-level techniques: {counts['top_level_techniques']}")
        print(f"Sub-techniques: {counts['sub_techniques']}")
        print(f"A_120 ids present/top-level: {counts['A_120_ids_found']}/120")
        print(f"Crosswalk SHA-256: {manifest['output']['sha256']}")
        return 0
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
