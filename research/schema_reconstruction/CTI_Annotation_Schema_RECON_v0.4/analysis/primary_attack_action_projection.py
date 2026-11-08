#!/usr/bin/env python3
"""Build a ChronoCTI-comparable projection from ATTACK_ACTION units only.

This is an analysis filter, not an annotation validator or lock verifier. Call
validate_activity_strata and validate the selected-analysis/stratum locks
before using this function on a reviewed partition.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[2]
V1_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.1"
V2_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.2"
sys.path.insert(0, str(V1_ROOT / "analysis"))
sys.path.insert(0, str(V1_ROOT / "validator"))
sys.path.insert(0, str(V2_ROOT / "analysis"))
sys.path.insert(0, str(REPO_ROOT))

from annotation_projection_adapter import (  # noqa: E402
    TechniqueMapping,
    build_a120_mapping_sets,
)
from projection_metrics_recon import (  # noqa: E402
    TemporalEdge,
    project_report_recon,
)
from validate_activity_strata import STRATUM_HEADERS, _partition  # noqa: E402
from validate_annotations import HEADERS as BASE_HEADERS  # noqa: E402
import report_level_aggregation as v2_aggregation  # noqa: E402


def _read_csv(path: Path, headers: list[str]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != headers:
            raise ValueError(f"Header mismatch in {path.name}")
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
            if row and any((value or "").strip() for value in row.values())
        ]


def build_primary_attack_action_projection(
    base_bundle: str | Path,
    strata_file: str | Path,
    *,
    report_id: str,
    annotator_id: str,
    annotation_pass_id: str,
    comparison_scope_assignments: list[dict[str, str]] | None = None,
    scope_pair_rule_id: str = v2_aggregation.INCIDENT_SCOPE_PAIR_RULE_ID,
) -> dict[str, Any]:
    """Project and count pair opportunities using ATTACK_ACTION units only.

    The caller must validate the base bundle, stratum decisions, and selected
    analysis/stratum locks before using this function on a reviewed partition.
    """
    if (
        scope_pair_rule_id == v2_aggregation.EXPLICIT_SCOPE_PAIR_RULE_ID
        and comparison_scope_assignments is None
    ):
        raise ValueError("The explicit scope-pair rule requires assignment rows")
    root = Path(base_bundle)
    partition = (report_id, annotator_id, annotation_pass_id)
    tables = {
        name: _read_csv(root / "registers" / f"{name}.csv", headers)
        for name, headers in BASE_HEADERS.items()
    }
    strata = _read_csv(Path(strata_file), STRATUM_HEADERS)
    part_units = [row for row in tables["activity_units"] if _partition(row) == partition]
    part_strata = [row for row in strata if _partition(row) == partition]
    part_scopes = [row for row in tables["report_scopes"] if _partition(row) == partition]
    stratum_by_id = {row["activity_unit_id"]: row["activity_stratum"] for row in part_strata}
    unit_by_id = {row["activity_unit_id"]: row for row in part_units}

    eligible_leaves = [
        row for row in part_units
        if row.get("unit_role") == "event_leaf"
        and row.get("granularity") == "atomic_event"
        and row.get("instance_status") == "RESOLVED"
    ]
    primary_units = [
        row for row in eligible_leaves
        if stratum_by_id.get(row.get("activity_unit_id", "")) == "ATTACK_ACTION"
    ]
    primary_ids = {row["activity_unit_id"] for row in primary_units}
    auxiliary_leaf_counts = Counter(
        stratum_by_id.get(row.get("activity_unit_id", ""), "MISSING")
        for row in eligible_leaves if row.get("activity_unit_id") not in primary_ids
    )

    routes = Counter()
    primary_relations = []
    scope_excluded_primary_stratum_relation_ids: list[str] = []
    part_assignments = [
        row for row in (comparison_scope_assignments or [])
        if _partition(row) == partition and row.get("activity_unit_id") in primary_ids
    ]
    assigned_by_event: dict[str, set[str]] = {}
    for assignment in part_assignments:
        if assignment.get("assignment_status") == "ASSIGNED":
            assigned_by_event.setdefault(assignment.get("activity_unit_id", ""), set()).add(
                assignment.get("comparison_scope_id", "")
            )
    auxiliary_relation_ids: dict[str, list[str]] = {
        "AUXILIARY_SAME_STRATUM": [],
        "MIXED_STRATUM": [],
    }
    for row in tables["temporal_relations"]:
        if _partition(row) != partition:
            continue
        stratum_a = stratum_by_id.get(row.get("event_a_id", ""), "")
        stratum_b = stratum_by_id.get(row.get("event_b_id", ""), "")
        if stratum_a == "ATTACK_ACTION" and stratum_b == "ATTACK_ACTION":
            route = "PRIMARY_ATTACK_ACTION"
        elif stratum_a and stratum_a == stratum_b:
            route = "AUXILIARY_SAME_STRATUM"
        else:
            route = "MIXED_STRATUM"
        routes[route] += 1
        if route == "PRIMARY_ATTACK_ACTION":
            if not (
                row.get("relation_label") in {"BEFORE", "AFTER", "OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"}
                and row.get("relation_basis") in {"direct_source", "direct_timestamp"}
                and row.get("scope_compatibility") == "COMPATIBLE"
                and row.get("event_a_id") in primary_ids
                and row.get("event_b_id") in primary_ids
            ):
                continue

            event_a = unit_by_id.get(row.get("event_a_id", ""))
            event_b = unit_by_id.get(row.get("event_b_id", ""))
            comparison_scope_id = row.get("comparison_scope_id", "")
            if scope_pair_rule_id == v2_aggregation.INCIDENT_SCOPE_PAIR_RULE_ID:
                expected_scope = (
                    v2_aggregation.nearest_shared_resolved_incident_scope(
                        event_a.get("scope_id", ""), event_b.get("scope_id", ""), part_scopes
                    )
                    if event_a is not None and event_b is not None else None
                )
                scope_eligible = bool(expected_scope) and comparison_scope_id == expected_scope
            elif scope_pair_rule_id == v2_aggregation.EXPLICIT_SCOPE_PAIR_RULE_ID:
                scope_eligible = (
                    comparison_scope_id in assigned_by_event.get(row.get("event_a_id", ""), set())
                    and comparison_scope_id in assigned_by_event.get(row.get("event_b_id", ""), set())
                )
            elif scope_pair_rule_id == v2_aggregation.LEGACY_SCOPE_PAIR_RULE_ID:
                common_scope_ids = v2_aggregation.shared_resolved_comparison_scope_ids(
                    event_a.get("scope_id", "") if event_a else "",
                    event_b.get("scope_id", "") if event_b else "",
                    part_scopes,
                )
                scope_eligible = comparison_scope_id in common_scope_ids
            else:
                raise ValueError(f"Unknown scope-pair rule: {scope_pair_rule_id}")
            if scope_eligible:
                primary_relations.append(row)
            else:
                scope_excluded_primary_stratum_relation_ids.append(row.get("relation_id", ""))
        else:
            auxiliary_relation_ids[route].append(row.get("relation_id", ""))

    a120_path = root / "vocabulary" / "A_120_ChronoCTI_Selected_Technique_IDs_derived_v0.1.json"
    a120_doc = json.loads(a120_path.read_text(encoding="utf-8"))
    a120_ids = a120_doc["technique_ids"]
    part_mappings = [
        row for row in tables["event_mappings"]
        if _partition(row) == partition and row.get("activity_unit_id") in primary_ids
    ]
    mapping_rows = [
        TechniqueMapping(
            mapping_id=row.get("mapping_id", ""),
            activity_unit_id=row.get("activity_unit_id", ""),
            baseline_parent_technique_id=row.get("baseline_parent_technique_id", ""),
            mapping_decision_status=row.get("mapping_decision_status", ""),
            mapping_basis=row.get("mapping_basis", ""),
            baseline_mapping_status=row.get("baseline_mapping_status", ""),
        )
        for row in part_mappings
    ]
    mapping_sets, mapping_stats = build_a120_mapping_sets(mapping_rows, a120_ids, primary_ids)
    edges = [
        TemporalEdge(
            edge_id=row["relation_id"],
            source_event=row["event_a_id"],
            target_event=row["event_b_id"],
            relation=row["relation_label"],
            relation_basis=row["relation_basis"],
            scope_compatibility=row["scope_compatibility"],
        )
        for row in primary_relations
    ]
    projection = project_report_recon(mapping_sets, edges)
    pair_opportunity = v2_aggregation.compute_event_pair_opportunity(
        primary_units,
        part_scopes,
        mapping_sets,
        comparison_scope_assignments=(
            part_assignments if scope_pair_rule_id == v2_aggregation.EXPLICIT_SCOPE_PAIR_RULE_ID else None
        ),
        scope_pair_rule_id=scope_pair_rule_id,
    )

    return {
        "status": "PRIMARY_ATTACK_ACTION_STRATUM_ONLY",
        "partition": {
            "report_id": report_id,
            "annotator_id": annotator_id,
            "annotation_pass_id": annotation_pass_id,
        },
        "counts": {
            "all_resolved_atomic_event_leaves": len(eligible_leaves),
            "primary_attack_action_event_leaves": len(primary_ids),
            "auxiliary_event_leaves_by_stratum": dict(sorted(auxiliary_leaf_counts.items())),
            "temporal_relation_rows_by_route": {
                "PRIMARY_ATTACK_ACTION": routes["PRIMARY_ATTACK_ACTION"],
                "AUXILIARY_SAME_STRATUM": routes["AUXILIARY_SAME_STRATUM"],
                "MIXED_STRATUM": routes["MIXED_STRATUM"],
            },
            "primary_direct_positive_attack_action_relations": len(primary_relations),
            "primary_stratum_relation_ids_excluded_by_scope_rule": scope_excluded_primary_stratum_relation_ids,
            "auxiliary_relation_ids": auxiliary_relation_ids,
            "primary_attack_action_mapping_rows": len(part_mappings),
        },
        "mapping_filter": mapping_stats,
        "pair_opportunity": pair_opportunity,
        "projection": projection,
    }
