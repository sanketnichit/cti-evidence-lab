#!/usr/bin/env python3
"""Report-level CTI Evidence Lab aggregation over selected, locked partitions.

This module never treats missing annotations as negative outcomes. It separates
N_eligible, N_assessable, selected-final coverage, and successful projections.
Raw frozen source text is supplied at runtime and is never copied to outputs.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
BASE_PACKAGE_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.1"
REPO_ROOT = PACKAGE_ROOT.parents[2]
sys.path.insert(0, str(BASE_PACKAGE_ROOT / "analysis"))
sys.path.insert(0, str(BASE_PACKAGE_ROOT / "validator"))
sys.path.insert(0, str(PACKAGE_ROOT / "validator"))
sys.path.insert(0, str(REPO_ROOT))

from annotation_projection_adapter import (  # noqa: E402
    TechniqueMapping,
    build_a120_mapping_sets,
)
from selected_partition_projection_adapter import (  # noqa: E402
    build_projection_for_selected_report,
)
from validate_annotations import HEADERS as BASE_HEADERS  # noqa: E402
from validate_temporal_evidence import (  # noqa: E402
    SELECTION_HEADERS,
    validate_analysis_partition_selection,
)
from src.source_text_integrity import frozen_source_sha256, read_frozen_source  # noqa: E402

POSITIVE_LABELS = {
    "BEFORE", "AFTER", "OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"
}
DIRECT_BASES = {"direct_source", "direct_timestamp"}
COMPARABLE_SCOPE_TYPES = {
    "INCIDENT", "CAMPAIGN", "ACTOR_OPERATION", "VICTIM_ORGANISATION", "HOST", "OTHER"
}


def _read_csv(path: Path, expected_headers: Iterable[str] | None = None) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Required register is missing: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"Register has no header: {path}")
        if expected_headers is not None and reader.fieldnames != list(expected_headers):
            raise ValueError(
                f"Header mismatch in {path.name}; expected {list(expected_headers)!r}, "
                f"found {reader.fieldnames!r}"
            )
        rows: list[dict[str, str]] = []
        for line, row in enumerate(reader, 2):
            if row is None or all((value or "").strip() == "" for value in row.values()):
                continue
            if None in row:
                raise ValueError(f"Row-width mismatch in {path.name}:{line}")
            rows.append({key: (value or "").strip() for key, value in row.items()})
        return rows


def _partition(row: Mapping[str, str]) -> tuple[str, str, str]:
    return (row.get("report_id", ""), row.get("annotator_id", ""), row.get("annotation_pass_id", ""))


def _source_matches_registry_row(row: Mapping[str, str], source_text: str | None) -> bool:
    if source_text is None:
        return False
    expected_hash = row.get("source_text_sha256", "").lower()
    expected_count = row.get("source_text_char_count", "")
    try:
        count_matches = int(expected_count) == len(source_text)
    except (TypeError, ValueError):
        return False
    return bool(expected_hash) and frozen_source_sha256(source_text) == expected_hash and count_matches


def summarize_report_denominators(
    report_registry_rows: list[dict[str, str]],
    source_texts: Mapping[str, str],
) -> dict[str, Any]:
    """Compute report-level denominators and coverage without imputing outcomes."""
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in report_registry_rows:
        report_id = row.get("report_id", "")
        if report_id:
            grouped[report_id].append(row)

    eligible_ids: set[str] = set()
    assessable_ids: set[str] = set()
    decision_conflicts: set[str] = set()
    source_version_conflicts: set[str] = set()
    source_unverified: set[str] = set()
    no_completed_review: set[str] = set()
    not_assessable: set[str] = set()
    assessability_pending: set[str] = set()
    scope_ineligible: set[str] = set()
    scope_pending: set[str] = set()
    local_use_blocked: set[str] = set()
    eligible_not_assessable_reasons: dict[str, str] = {}

    def single_status(rows: list[dict[str, str]], field: str) -> str:
        values = {row.get(field, "") or "MISSING" for row in rows}
        return next(iter(values)) if len(values) == 1 else "MULTIPLE_DECISIONS"

    for report_id, rows in grouped.items():
        eligibility_status = single_status(rows, "source_scope_eligibility")
        local_use_status = single_status(rows, "local_research_use_status")
        assessability_status = single_status(rows, "report_assessability")

        if eligibility_status == "INELIGIBLE":
            scope_ineligible.add(report_id)
        elif eligibility_status == "PENDING" or eligibility_status == "MISSING":
            scope_pending.add(report_id)
        if local_use_status in {"NOT_PERMITTED", "UNRESOLVED", "MISSING"}:
            local_use_blocked.add(report_id)
        if assessability_status == "NOT_ASSESSABLE":
            not_assessable.add(report_id)
        elif assessability_status == "PENDING" or assessability_status == "MISSING":
            assessability_pending.add(report_id)

        decisions = {
            (
                row.get("source_scope_eligibility", ""),
                row.get("local_research_use_status", ""),
                row.get("report_assessability", ""),
            )
            for row in rows
        }
        if len(decisions) != 1:
            decision_conflicts.add(report_id)
            continue

        eligibility, local_use, assessability = next(iter(decisions))
        if eligibility != "ELIGIBLE" or local_use != "PERMITTED":
            continue
        eligible_ids.add(report_id)

        source_versions = {
            (row.get("source_text_sha256", "").lower(), row.get("source_text_char_count", ""))
            for row in rows if row.get("source_text_sha256", "")
        }
        if len(source_versions) > 1:
            source_version_conflicts.add(report_id)
            eligible_not_assessable_reasons[report_id] = "SOURCE_VERSION_CONFLICT"
            continue

        if assessability != "ASSESSABLE":
            eligible_not_assessable_reasons[report_id] = (
                "REPORT_NOT_ASSESSABLE" if assessability == "NOT_ASSESSABLE"
                else "ASSESSABILITY_PENDING"
            )
            continue

        reviewed_rows = [
            row for row in rows
            if row.get("report_assessability") == "ASSESSABLE"
            and row.get("full_report_review_status") == "COMPLETE"
            and row.get("annotator_id") and row.get("annotation_pass_id")
        ]
        if not reviewed_rows:
            no_completed_review.add(report_id)
            eligible_not_assessable_reasons[report_id] = "NO_COMPLETED_FULL_REPORT_REVIEW"
            continue

        source_text = source_texts.get(report_id)
        if source_text is None or not any(
            _source_matches_registry_row(row, source_text) for row in reviewed_rows
        ):
            source_unverified.add(report_id)
            eligible_not_assessable_reasons[report_id] = "SOURCE_MISSING_OR_HASH_COUNT_MISMATCH"
            continue
        assessable_ids.add(report_id)

    # Report-level status distributions count each report once. A status that
    # differs across partitions is shown as MULTIPLE_DECISIONS, not duplicated.
    status_counts: dict[str, dict[str, int]] = {}
    for output_name, field in (
        ("source_scope_eligibility", "source_scope_eligibility"),
        ("local_research_use", "local_research_use_status"),
        ("report_assessability", "report_assessability"),
    ):
        counts = Counter(single_status(rows, field) for rows in grouped.values())
        status_counts[output_name] = dict(sorted(counts.items()))

    review_counts: Counter[str] = Counter()
    for rows in grouped.values():
        states = {row.get("full_report_review_status", "") for row in rows}
        if "COMPLETE" in states:
            review_counts["COMPLETE_ON_AT_LEAST_ONE_PARTITION"] += 1
        elif "IN_PROGRESS" in states:
            review_counts["IN_PROGRESS_ONLY"] += 1
        elif states and states <= {"NOT_STARTED", ""}:
            review_counts["NOT_STARTED"] += 1
        else:
            review_counts["UNKNOWN_OR_MISSING"] += 1

    eligible_not_assessable_ids = sorted(eligible_ids - assessable_ids)
    n_eligible = len(eligible_ids)
    n_assessable = len(assessable_ids)
    return {
        "inventory_report_count": len(grouped),
        "N_eligible": n_eligible,
        "N_assessable": n_assessable,
        "assessability_coverage": n_assessable / n_eligible if n_eligible else None,
        "report_status_counts": status_counts,
        "full_report_review_status_counts": dict(sorted(review_counts.items())),
        "eligible_report_ids": sorted(eligible_ids),
        "assessable_report_ids": sorted(assessable_ids),
        "eligible_not_assessable_report_ids": eligible_not_assessable_ids,
        "eligible_not_assessable_reasons": dict(sorted(eligible_not_assessable_reasons.items())),
        "report_level_decision_conflict_ids": sorted(decision_conflicts),
        "source_version_conflict_ids": sorted(source_version_conflicts),
        "source_unverified_ids": sorted(source_unverified),
        "no_completed_full_review_ids": sorted(no_completed_review),
        "source_scope_ineligible_ids": sorted(scope_ineligible),
        "source_scope_pending_ids": sorted(scope_pending),
        "local_research_use_blocked_ids": sorted(local_use_blocked),
        "report_assessability_not_assessable_ids": sorted(not_assessable),
        "report_assessability_pending_ids": sorted(assessability_pending),
    }

def _eligible_event_units(activity_units: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row for row in activity_units
        if row.get("unit_role") == "event_leaf"
        and row.get("granularity") == "atomic_event"
        and row.get("instance_status") == "RESOLVED"
        and row.get("activity_unit_id")
    ]


def _scope_ancestor_chain(scope_id: str, scope_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_id = {row.get("scope_id", ""): row for row in scope_rows if row.get("scope_id")}
    chain: list[dict[str, str]] = []
    visited: set[str] = set()
    current = scope_id
    while current and current not in visited:
        visited.add(current)
        row = by_id.get(current)
        if row is None or row.get("scope_status") != "RESOLVED":
            break
        chain.append(row)
        current = row.get("parent_scope_id", "")
    return chain


def _lowest_common_comparison_scope(
    scope_a: str,
    scope_b: str,
    scope_rows: list[dict[str, str]],
) -> str | None:
    """Return the nearest shared, resolved, non-report-aggregate scope.

    A shared REPORT_AGGREGATE is deliberately insufficient: report co-membership
    alone cannot make activities from separate incidents timeline-comparable.
    """
    chain_a = _scope_ancestor_chain(scope_a, scope_rows)
    chain_b = _scope_ancestor_chain(scope_b, scope_rows)
    positions_b = {row["scope_id"]: i for i, row in enumerate(chain_b)}
    common = []
    for i, row in enumerate(chain_a):
        scope_id = row["scope_id"]
        if scope_id in positions_b:
            other = chain_b[positions_b[scope_id]]
            scope_type = row.get("scope_type", "")
            if (
                scope_type == other.get("scope_type")
                and scope_type in COMPARABLE_SCOPE_TYPES
            ):
                common.append((max(i, positions_b[scope_id]), i + positions_b[scope_id], scope_id))
    if not common:
        return None
    return min(common)[2]


def compute_event_pair_opportunity(
    activity_units: list[dict[str, str]],
    scope_rows: list[dict[str, str]],
    mapping_sets: Mapping[str, set[str]],
) -> dict[str, int | bool]:
    """Count event-pair opportunities using explicit resolved common scopes."""
    leaves = _eligible_event_units(activity_units)
    compatible_pairs = 0
    shared_technique_pairs = 0
    for index, left in enumerate(leaves):
        for right in leaves[index + 1:]:
            common_scope = _lowest_common_comparison_scope(
                left.get("scope_id", ""), right.get("scope_id", ""), scope_rows
            )
            if common_scope is None:
                continue
            compatible_pairs += 1
            left_maps = mapping_sets.get(left["activity_unit_id"], set())
            right_maps = mapping_sets.get(right["activity_unit_id"], set())
            if left_maps.intersection(right_maps):
                shared_technique_pairs += 1
    return {
        "resolved_atomic_event_leaves": len(leaves),
        "has_event_leaf": bool(leaves),
        "compatible_event_pair_count": compatible_pairs,
        "has_compatible_event_pair": compatible_pairs > 0,
        "same_technique_pair_opportunity_count": shared_technique_pairs,
        "has_same_technique_pair_opportunity": shared_technique_pairs > 0,
    }


def _rates(outcomes: list[dict[str, Any]], denominator: int) -> dict[str, Any]:
    if denominator <= 0:
        return {
            "denominator": denominator,
            "event_leaf_presence_rate": None,
            "compatible_event_pair_opportunity_rate": None,
            "same_technique_pair_opportunity_rate": None,
            "positive_temporal_relation_report_rate": None,
            "within_technique_temporal_relation_report_rate": None,
        }
    return {
        "denominator": denominator,
        "event_leaf_presence_rate": sum(bool(x["has_event_leaf"]) for x in outcomes) / denominator,
        "compatible_event_pair_opportunity_rate": sum(bool(x["has_compatible_event_pair"]) for x in outcomes) / denominator,
        "same_technique_pair_opportunity_rate": sum(bool(x["has_same_technique_pair_opportunity"]) for x in outcomes) / denominator,
        "positive_temporal_relation_report_rate": sum(bool(x["has_positive_temporal_relation"]) for x in outcomes) / denominator,
        "within_technique_temporal_relation_report_rate": sum(bool(x["has_within_technique_temporal_relation"]) for x in outcomes) / denominator,
    }


def _load_bundle_tables(bundle_root: Path) -> dict[str, list[dict[str, str]]]:
    tables = {}
    for name, headers in BASE_HEADERS.items():
        tables[name] = _read_csv(bundle_root / "registers" / f"{name}.csv", headers)
    return tables


def aggregate_selected_report_projections(
    bundle_root: str | Path,
    *,
    source_texts: Mapping[str, str],
    confirm_selected_analysis_locks: bool = False,
    approve_scope_pair_rule: bool = False,
) -> dict[str, Any]:
    """Aggregate report outcomes after validating selected-final projections.

    The caller must explicitly set confirm_selected_analysis_locks=True before
    the wrapper will ask the selected-partition adapter to project any report.
    The selection register's own hash is recomputed and verified by that adapter.
    Opportunity counts use a documented provisional scope-pair rule; the
    corresponding report rates remain withheld until explicitly approved.
    """
    root = Path(bundle_root).resolve()
    base_root = root.parent / "CTI_Annotation_Schema_RECON_v0.1"
    tables = _load_bundle_tables(base_root)
    selection_path = root / "registers" / "analysis_partition_selection.csv"
    selections = _read_csv(selection_path, SELECTION_HEADERS)

    denominators = summarize_report_denominators(tables["report_registry"], source_texts)
    selection_errors, selection_count = validate_analysis_partition_selection(
        base_root, selection_path
    )
    selected_by_report: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in selections:
        if row.get("selection_status") == "SELECTED_FINAL":
            selected_by_report[row.get("report_id", "")].append(row)

    rows_by_partition: dict[str, dict[tuple[str, str, str], list[dict[str, str]]]] = {
        name: defaultdict(list) for name in tables
    }
    for name, rows in tables.items():
        for row in rows:
            rows_by_partition[name][_partition(row)].append(row)

    vocab_path = base_root / "vocabulary" / "A_120_ChronoCTI_Selected_Technique_IDs_derived_v0.1.json"
    vocab_doc = json.loads(vocab_path.read_text(encoding="utf-8"))
    a120_ids = vocab_doc["technique_ids"]

    report_outcomes: list[dict[str, Any]] = []
    blocked: dict[str, str] = {}
    projected_ids: set[str] = set()
    projection_count_totals: Counter[str] = Counter()
    relation_label_totals: Counter[str] = Counter()
    within_relation_label_totals: Counter[str] = Counter()
    recurrence_totals: Counter[str] = Counter()

    for report_id in denominators["assessable_report_ids"]:
        candidate_rows = selected_by_report.get(report_id, [])
        if len(candidate_rows) != 1:
            blocked[report_id] = "NO_UNIQUE_SELECTED_FINAL_PARTITION"
            continue
        selected = candidate_rows[0]
        partition = _partition(selected)
        matching_registry = [row for row in tables["report_registry"] if _partition(row) == partition]
        if len(matching_registry) != 1:
            blocked[report_id] = "SELECTED_REGISTRY_PARTITION_NOT_UNIQUE"
            continue
        selected_registry = matching_registry[0]
        source_text = source_texts.get(report_id)
        if not _source_matches_registry_row(selected_registry, source_text):
            blocked[report_id] = "SELECTED_FINAL_SOURCE_NOT_VERIFIED"
            continue
        if selection_errors:
            blocked[report_id] = "SELECTION_REGISTER_VALIDATION_FAILED"
            continue
        if not confirm_selected_analysis_locks:
            blocked[report_id] = "EXPLICIT_LOCK_CONFIRMATION_REQUIRED"
            continue
        try:
            adapter_result = build_projection_for_selected_report(
                root,
                report_id=report_id,
                source_text=source_text or "",
                analysis_lock_confirmed=True,
                analysis_lock_reference=selected.get("lock_reference", ""),
            )
        except Exception as exc:  # fail closed per report; preserve diagnostic text
            blocked[report_id] = f"PROJECTION_VALIDATION_FAILED: {type(exc).__name__}: {exc}"
            continue

        part_rows = {
            name: rows_by_partition[name].get(partition, [])
            for name in tables
        }
        units = part_rows["activity_units"]
        event_leaves = _eligible_event_units(units)
        mapping_rows = [
            TechniqueMapping(
                mapping_id=row.get("mapping_id", ""),
                activity_unit_id=row.get("activity_unit_id", ""),
                baseline_parent_technique_id=row.get("baseline_parent_technique_id", ""),
                mapping_decision_status=row.get("mapping_decision_status", ""),
                mapping_basis=row.get("mapping_basis", ""),
                baseline_mapping_status=row.get("baseline_mapping_status", ""),
            )
            for row in part_rows["event_mappings"]
        ]
        event_ids = {row["activity_unit_id"] for row in event_leaves}
        mapping_sets, mapping_stats = build_a120_mapping_sets(mapping_rows, a120_ids, event_ids)
        opportunity = compute_event_pair_opportunity(
            units, part_rows["report_scopes"], mapping_sets
        )

        primary_relations = [
            row for row in part_rows["temporal_relations"]
            if row.get("relation_label") in POSITIVE_LABELS
            and row.get("relation_basis") in DIRECT_BASES
            and row.get("scope_compatibility") == "COMPATIBLE"
        ]
        within_relations = [
            row for row in primary_relations
            if set(mapping_sets.get(row.get("event_a_id", ""), set())).intersection(
                mapping_sets.get(row.get("event_b_id", ""), set())
            )
        ]
        label_counts = Counter(row.get("relation_label", "") for row in primary_relations)
        projection = adapter_result["projection"]
        projection_counts = projection.get("counts", {})
        for key, value in projection_counts.items():
            if isinstance(value, (int, float)):
                projection_count_totals[key] += value
        for label, value in label_counts.items():
            relation_label_totals[label] += value
        for row in within_relations:
            within_relation_label_totals[row.get("relation_label", "")] += 1
        for row in units:
            if row.get("granularity"):
                recurrence_totals[row["granularity"]] += 1

        outcome = {
            "report_id": report_id,
            "source_vendor": selected_registry.get("source_vendor", ""),
            "prior_exposure_status": selected_registry.get("prior_exposure_status", ""),
            **opportunity,
            "primary_positive_temporal_relation_count": len(primary_relations),
            "has_positive_temporal_relation": bool(primary_relations),
            "within_technique_temporal_relation_count": len(within_relations),
            "has_within_technique_temporal_relation": bool(within_relations),
            "within_technique_relation_label_counts": dict(sorted(
                Counter(row.get("relation_label", "") for row in within_relations).items()
            )),
            "positive_relation_label_counts": dict(sorted(label_counts.items())),
            "event_mapping_coverage": (
                projection_counts.get("mapped_event_instances", 0) / len(event_leaves)
                if event_leaves else None
            ),
            "positive_edge_mapping_coverage": (
                projection_counts.get("mapped_positive_temporal_edges", 0) / len(primary_relations)
                if primary_relations else None
            ),
            "projection_counts": projection_counts,
            "mapping_filter": mapping_stats,
            "analysis_lock_reference": adapter_result.get("analysis_lock_reference"),
            "annotation_lock_reference": adapter_result.get("annotation_lock_reference"),
        }
        report_outcomes.append(outcome)
        projected_ids.add(report_id)

    assessable_ids = set(denominators["assessable_report_ids"])
    projected_assessable = len(projected_ids & assessable_ids)
    n_assessable = denominators["N_assessable"]
    full_coverage = n_assessable > 0 and projected_assessable == n_assessable
    selected_subset_rates = _rates(report_outcomes, projected_assessable)
    primary_rates = _rates(report_outcomes, n_assessable) if full_coverage else {
        "denominator": n_assessable,
        "status": "WITHHELD_UNTIL_EVERY_ASSESSABLE_REPORT_HAS_A_VALID_SELECTED_FINAL_PROJECTION",
        "event_leaf_presence_rate": None,
        "compatible_event_pair_opportunity_rate": None,
        "same_technique_pair_opportunity_rate": None,
        "positive_temporal_relation_report_rate": None,
        "within_technique_temporal_relation_report_rate": None,
    }
    if n_assessable == 0:
        primary_rates["status"] = "NO_ASSESSABLE_REPORTS"

    opportunity_rate_keys = (
        "compatible_event_pair_opportunity_rate",
        "same_technique_pair_opportunity_rate",
    )
    if not approve_scope_pair_rule:
        for key in opportunity_rate_keys:
            primary_rates[key] = None
            selected_subset_rates[key] = None
        primary_rates["scope_pair_opportunity_rate_status"] = "WITHHELD_PENDING_RESEARCHER_APPROVAL_OF_NEAREST_COMMON_RESOLVED_SCOPE_RULE"
        selected_subset_rates["scope_pair_opportunity_rate_status"] = "WITHHELD_PENDING_RESEARCHER_APPROVAL_OF_NEAREST_COMMON_RESOLVED_SCOPE_RULE"
    else:
        primary_rates["scope_pair_opportunity_rate_status"] = "APPROVED_BY_CALLER"
        selected_subset_rates["scope_pair_opportunity_rate_status"] = "APPROVED_BY_CALLER"

    outcome_numerators = {
        "reports_with_event_leaf": sum(bool(x["has_event_leaf"]) for x in report_outcomes),
        "reports_with_compatible_event_pair_opportunity_provisional": sum(bool(x["has_compatible_event_pair"]) for x in report_outcomes),
        "reports_with_same_technique_pair_opportunity_provisional": sum(bool(x["has_same_technique_pair_opportunity"]) for x in report_outcomes),
        "reports_with_positive_temporal_relation": sum(bool(x["has_positive_temporal_relation"]) for x in report_outcomes),
        "reports_with_within_technique_temporal_relation": sum(bool(x["has_within_technique_temporal_relation"]) for x in report_outcomes),
    }
    outcome_counts = {
        "resolved_atomic_event_leaves": sum(int(x["resolved_atomic_event_leaves"]) for x in report_outcomes),
        "compatible_event_pair_opportunities_provisional": sum(int(x["compatible_event_pair_count"]) for x in report_outcomes),
        "same_technique_pair_opportunities_provisional": sum(int(x["same_technique_pair_opportunity_count"]) for x in report_outcomes),
        "primary_positive_temporal_relations": sum(int(x["primary_positive_temporal_relation_count"]) for x in report_outcomes),
        "within_technique_temporal_relations": sum(int(x["within_technique_temporal_relation_count"]) for x in report_outcomes),
    }

    projection_rate_denominator = projection_count_totals.get("mapped_positive_temporal_edges", 0)
    mapping_combo_denominator = projection_count_totals.get("event_edge_to_pair_combinations", 0)
    projection_rates = {
        "mapped_positive_temporal_edges": projection_rate_denominator,
        "full_omission_rate_mapped_edges": (
            projection_count_totals.get("fully_omitted_edges", 0) / projection_rate_denominator
            if projection_rate_denominator else None
        ),
        "partial_representation_rate_mapped_edges": (
            projection_count_totals.get("partially_represented_edges", 0) / projection_rate_denominator
            if projection_rate_denominator else None
        ),
        "same_technique_endpoint_rate_mapped_edges": (
            projection_count_totals.get("same_technique_endpoint_edges", 0) / projection_rate_denominator
            if projection_rate_denominator else None
        ),
        "diagonal_mapping_share": (
            projection_count_totals.get("diagonal_mapping_combinations", 0) / mapping_combo_denominator
            if mapping_combo_denominator else None
        ),
        "note": "Projection-edge rates use mapped positive event edges; unmapped endpoints are reported separately. Per-report collision/SCC counts are summed, never merged across reports.",
    }

    return {
        "status": (
            "AGGREGATED_SELECTED_FINAL_REPORTS"
            if full_coverage else "PARTIAL_OR_EMPTY_SELECTED_FINAL_COVERAGE"
        ),
        "metric_contract": "CTI_Evidence_Lab_Metric_Contract_v0.1_provisional",
        "schema": "CTI_Annotation_Schema_RECON_v0.2_draft",
        "denominators": denominators,
        "selection": {
            "selection_row_count": selection_count,
            "selection_validation_errors": selection_errors,
            "selected_final_report_count": len(selected_by_report),
            "successfully_projected_assessable_reports": projected_assessable,
            "projection_coverage": projected_assessable / n_assessable if n_assessable else None,
            "missing_or_blocked_report_ids": sorted(set(denominators["assessable_report_ids"]) - projected_ids),
            "blocked_report_reasons": dict(sorted(blocked.items())),
            "explicit_lock_confirmation_supplied": confirm_selected_analysis_locks,
        },
        "report_level_primary_rates": primary_rates,
        "selected_subset_descriptive_rates_not_population_estimates": selected_subset_rates,
        "report_outcome_numerators_in_projected_assessable_subset": outcome_numerators,
        "report_outcome_counts_in_projected_assessable_subset": outcome_counts,
        "scope_pair_opportunity_rule": {
            "rule_id": "NEAREST_COMMON_RESOLVED_NON_REPORT_AGGREGATE_SCOPE_v0.1",
            "status": "APPROVED_BY_CALLER" if approve_scope_pair_rule else "PROVISIONAL_NOT_APPROVED",
            "definition": "Two event leaves are treated as a compatible pair when their nearest common ancestor in the selected partition's scope tree is RESOLVED and is not REPORT_AGGREGATE. No shared scope, unresolved/provisional scope paths, or a shared REPORT_AGGREGATE alone yields no pair opportunity.",
            "rates_enabled": approve_scope_pair_rule,
        },
        "projection_rates_and_counts": {
            "counts": dict(sorted(projection_count_totals.items())),
            "rates": projection_rates,
        },
        "positive_relation_label_counts": dict(sorted(relation_label_totals.items())),
        "within_technique_positive_relation_label_counts": dict(sorted(within_relation_label_totals.items())),
        "granularity_counts_in_projected_partitions": dict(sorted(recurrence_totals.items())),
        "per_report_outcomes": sorted(report_outcomes, key=lambda row: row["report_id"]),
        "interpretation_limits": [
            "A five-report feasibility batch is not a prevalence estimate.",
            "No unrecorded pair is treated as NO_TEMPORAL_CLAIM.",
            "Pair opportunity requires a nearest shared RESOLVED scope other than REPORT_AGGREGATE; report co-membership alone is insufficient.",
            "Primary report-level rates are withheld unless every N_assessable report has a valid selected-final projection.",
            "Projection counts aggregate within-report outputs; technique-pair collision keys and cycle components are summed within reports, not merged across reports.",
            "Synthetic validation does not establish semantic validity of human annotations.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate CTI Evidence Lab report-level metrics")
    parser.add_argument("--extension", type=Path, default=PACKAGE_ROOT,
                        help="RECON v0.2 extension package directory")
    parser.add_argument("--sources-dir", type=Path, required=True,
                        help="Local directory containing frozen REPORT_ID.txt source files")
    parser.add_argument("--confirm-selected-analysis-locks", action="store_true",
                        help="Explicitly confirm the selected-analysis locks before projection")
    parser.add_argument("--approve-scope-pair-rule", action="store_true",
                        help="Approve the documented nearest-common-resolved-scope rule for event-pair opportunity rates")
    parser.add_argument("--output", type=Path,
                        help="Optional JSON output path; source text is never written")
    args = parser.parse_args()

    # Keep the extension path configurable while the adapter uses the package
    # default. A non-default extension is not supported by this version.
    if args.extension.resolve() != PACKAGE_ROOT.resolve():
        parser.error("--extension must point to this checked-out RECON v0.2 package")
    sources: dict[str, str] = {}
    for source_path in sorted(args.sources_dir.glob("*.txt")):
        sources[source_path.stem] = read_frozen_source(source_path)
    result = aggregate_selected_report_projections(
        args.extension,
        source_texts=sources,
        confirm_selected_analysis_locks=args.confirm_selected_analysis_locks,
        approve_scope_pair_rule=args.approve_scope_pair_rule,
    )
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
