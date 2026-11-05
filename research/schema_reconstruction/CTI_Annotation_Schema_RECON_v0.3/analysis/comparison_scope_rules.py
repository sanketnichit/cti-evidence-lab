"""Compare the legacy, incident-bounded and explicit-assignment scope rules."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
V1_ROOT = PACKAGE_ROOT.parent / "CTI_Annotation_Schema_RECON_v0.1"
sys.path.insert(0, str(V1_ROOT / "validator"))

from validate_annotations import (  # noqa: E402
    nearest_common_resolved_comparison_scope,
    shared_resolved_comparison_scope_ids,
)

LEGACY_RULE_ID = "NEAREST_COMMON_RESOLVED_NON_REPORT_SCOPE_v0.1"
INCIDENT_RULE_ID = "SHARED_RESOLVED_INCIDENT_SCOPE_v0.1"
EXPLICIT_RULE_ID = "EXPLICIT_SHARED_EVENT_COMPARISON_SCOPE_ASSIGNMENT_v0.3"


def evaluate_scope_pair_rules(
    event_a: dict[str, str],
    event_b: dict[str, str],
    scope_rows: list[dict[str, str]],
    assignment_rows: list[dict[str, str]],
) -> dict[str, dict[str, Any]]:
    """Return the decision and selected scope under all three candidate rules."""
    common_ids = shared_resolved_comparison_scope_ids(
        event_a.get("scope_id", ""), event_b.get("scope_id", ""), scope_rows
    )
    by_id = {row.get("scope_id", ""): row for row in scope_rows}
    legacy = nearest_common_resolved_comparison_scope(
        event_a.get("scope_id", ""), event_b.get("scope_id", ""), scope_rows
    )
    incident = next(
        (scope_id for scope_id in common_ids if by_id.get(scope_id, {}).get("scope_type") == "INCIDENT"),
        None,
    )
    assigned_a = {
        row.get("comparison_scope_id", "")
        for row in assignment_rows
        if row.get("activity_unit_id") == event_a.get("activity_unit_id")
        and row.get("assignment_status") == "ASSIGNED"
    }
    assigned_b = {
        row.get("comparison_scope_id", "")
        for row in assignment_rows
        if row.get("activity_unit_id") == event_b.get("activity_unit_id")
        and row.get("assignment_status") == "ASSIGNED"
    }
    explicit = next(
        (scope_id for scope_id in common_ids if scope_id in assigned_a and scope_id in assigned_b),
        None,
    )
    return {
        LEGACY_RULE_ID: {"eligible": legacy is not None, "comparison_scope_id": legacy},
        INCIDENT_RULE_ID: {"eligible": incident is not None, "comparison_scope_id": incident},
        EXPLICIT_RULE_ID: {"eligible": explicit is not None, "comparison_scope_id": explicit},
    }
