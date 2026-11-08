# CTI Annotation Schema RECON v0.4 — activity-stratum extension

**Status:** Draft extension; researcher review and protocol freeze remain required.  
**Parent layers:** RECON v0.1 base registers, v0.2 temporal evidence/selected-final partitions, and v0.3 comparison-scope assignments.  
**Real activity-stratum decisions:** 0.  
**Purpose:** distinguish incident-linked attack-action occurrences from auxiliary report-local event strata and ensure only attack-action endpoints enter primary ChronoCTI-comparable metrics.

## Why v0.4 is additive

RECON v0.1 is a reconstruction with a fixed, checksum-controlled activity_units header. It is not edited in place. This extension stores the logical activity_unit.activity_stratum field in a one-to-one companion register, activity_unit_strata.csv, keyed by report/annotator/pass/activity_unit_id. Every activity unit must have exactly one stratum row. Treat this field as part of the v0.4 annotation schema; do not omit it because a source unit is inconvenient to classify.

This normalized extension preserves the v0.1 base package and its existing validators. A future full schema package may inline the field in activity_units.csv, but must preserve the same controlled values, one-to-one invariant, lock semantics and projection gates.

## Controlled activity_stratum values

- ATTACK_ACTION — a concrete report-local action that conducts, enables, or completes a specific cyberattack/incident. This is medium-neutral and may include adversary, malware, or induced user/system actions.
- THREAT_ACTOR_COMMUNICATION — a forum launch, public post, claim, response blog, or disclosure not established as an operational step in a specific attack.
- ANALYST_OBSERVATION — sample detection/submission, discovery, reverse engineering, or lab analysis.
- GENERIC_CAPABILITY — generalized malware function, command handler, or TTP without a resolved report-local execution.
- OTHER_NON_PRIMARY — report-local activity retained for description but outside the primary attack-action estimand.
- UNRESOLVED_CLASSIFICATION — the evidence does not support a defensible stratum assignment.

Classification is independent of ATT&CK mapping. An attack action remains in the primary event universe when no defensible technique mapping exists; the unmapped outcome remains visible. A technique label does not promote a communication, observation, or generic capability into ATTACK_ACTION.

## Registers

- registers/activity_unit_strata.csv — one evidence-backed stratum decision per activity unit and annotation partition.
- registers/activity_stratum_locks.csv — lock of all stratum decisions in each selected-final partition, bound to the RECON v0.2 selected-analysis lock reference.

## Validation and analysis

Run the structural extension validator:

    python research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/validator/validate_activity_strata.py --base-bundle research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1 --strata-file research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/registers/activity_unit_strata.csv

Create stratum locks only after a selected-final analysis partition and all its activity-unit stratum decisions are complete:

    python research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/analysis/create_activity_stratum_locks.py --selection-file research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.2/registers/analysis_partition_selection.csv --strata-file research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/registers/activity_unit_strata.csv --output research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/registers/activity_stratum_locks.csv --locked-by YOUR_RESEARCHER_ID --lock-date YYYY-MM-DD

The primary projection helper filters the event universe, mapping rows, and relation edges before projection. Auxiliary same-stratum relations and mixed-stratum relations remain countable in separate diagnostics but cannot enter primary attack-action projections or denominators.

## Safety gates

- Every base activity unit must have one and only one stratum decision; missing, duplicate, and orphan rows fail.
- Every decision requires a source evidence span and rationale; unresolved classification uses basis UNRESOLVED.
- GENERIC_CAPABILITY cannot be represented as a resolved atomic event leaf.
- Both endpoints of a primary positive temporal edge must be ATTACK_ACTION. Same-stratum auxiliary edges and mixed-stratum edges are retained but routed outside primary analysis.
- Mapping rows for auxiliary events never contribute to the primary A_120 mapping sets.
- Stratum decisions are bound to the selected-analysis lock; post-lock edits invalidate the lock.

## Research-readiness boundary

The package contains blank registers and synthetic tests only. It creates no human annotations, selected final partitions, real-report projections, IAA measurements, or empirical findings. The v0.4 extension does not settle the comparison-scope rule, temporal label semantics, alternative-mapping lifecycle, or scope-assignment adjudication. Do not begin formal annotation until the protocol and complete schema package are reviewed, versioned, approved and frozen.
