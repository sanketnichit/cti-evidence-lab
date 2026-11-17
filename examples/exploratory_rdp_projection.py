"""Conditional projection using a published intrusion narrative.

This example does not constitute an accepted event annotation or an empirical
result. The source is The DFIR Report, 12 June 2023:
https://thedfirreport.com/2023/06/12/a-truly-graceful-wipe-out/

Its Case Summary describes two unsuccessful tunneled RDP attempts in order.
Event identities, incident scope, mappings and final evidence remain subject
to the project's full annotation and review procedure.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research" / "schema_reconstruction"
                       / "CTI_Annotation_Schema_RECON_v0.1" / "analysis"))
from projection_metrics_recon import TemporalEdge, project_report_recon  # noqa: E402

SOURCE = "https://thedfirreport.com/2023/06/12/a-truly-graceful-wipe-out/"


def run_example() -> dict:
    """Show what follows if two source-supported RDP occurrences are accepted."""
    mappings = {
        "attempt_1": {"T1021"},
        "attempt_2": {"T1021"},
    }
    relations = [
        TemporalEdge("attempt_order", "attempt_1", "attempt_2", "BEFORE",
                     relation_basis="direct_source",
                     scope_compatibility="COMPATIBLE")
    ]
    projection = project_report_recon(mappings, relations)
    return {
        "status": "CONDITIONAL_DEMONSTRATION_NOT_ANNOTATION",
        "source_url": SOURCE,
        "sample_membership": "OUTSIDE_ANNOCTR_PILOT",
        "human_reviewed": False,
        "eligible_for_empirical_denominators": False,
        "assumptions": [
            "two distinct atomic attack occurrences are independently validated",
            "both occurrences belong to the same resolved incident scope",
            "the BEFORE relation has accepted direct source evidence",
            "both events independently receive accepted T1021.001-to-T1021 mappings",
            "the exact source and report annotation lock pass validation",
        ],
        "conditional_projection": projection,
    }


if __name__ == "__main__":
    print(json.dumps(run_example(), sort_keys=True, indent=2))
