# CTI Annotation Schema RECON v0.3 — explicit comparison-scope extension

**Status:** draft extension; researcher review required; not approved or frozen.  
**Parent:** RECON v0.2 temporal-evidence and selected-partition extension.  
**Real assignment rows:** 0.  
**Purpose:** replace automatic common-ancestor eligibility with evidence-backed, event-level comparison-scope assignments while keeping alternative candidate rules available for sensitivity comparison.

## What v0.3 adds

- registers/event_comparison_scope_assignments.csv: one decision for one event instance × candidate comparison scope × annotation partition.
- registers/comparison_scope_assignment_locks.csv: a separate lock over the assignment rows and the v0.2 selected-analysis lock reference.
- validator/validate_comparison_scope_assignments.py: validates assignments, relation-scope consistency and the v0.3 lock.
- analysis/comparison_scope_rules.py: evaluates the legacy, incident-bounded and explicit-assignment rules on the same pair.
- analysis/create_scope_assignment_locks.py: creates lock rows for SELECTED_FINAL partitions after assignment review.
- analysis/aggregate_selected_report_projections.py: calls the v0.2 aggregator with the explicit-assignment rule after validating the v0.3 register and lock.

The v0.1 reconstructed schema remains unchanged. The extension does not claim to recover the missing original v0.4.2 package.

## Assignment semantics

A row is attached to one resolved atomic event_leaf and one report-local candidate comparison scope.

- ASSIGNED means the annotator affirmatively assigns that event to the comparison scope.
- NOT_ASSIGNED is an explicit reviewed negative decision. UNCERTAIN preserves a considered but unresolved candidate. Neither creates pair opportunity. Missing decisions block validation.
- Every eligible resolved non-report ancestor scope in an event's scope chain requires one explicit decision. A missing row is incomplete review and blocks validation; it is never interpreted as NOT_ASSIGNED.
- An event may have multiple scope decisions, but at most one decision per event × comparison scope × report/annotator/pass partition. Every eligible resolved comparable ancestor scope must be reviewed.
- ASSIGNED and NOT_ASSIGNED require a RESOLVED scope of a non-report comparable type, a source evidence span, a rationale, confidence and an allowed basis. NOT_ASSIGNED is an explicit human negative decision and never creates pair opportunity.
- The assigned scope must be in the event's resolved scope ancestry. This lets events in separate incident branches share an explicitly assigned campaign or operation ancestor, but does not permit arbitrary cross-links to unrelated scopes.
- A primary direct-positive temporal relation and a COMPATIBLE candidate-pair assessment must name a comparison scope that is ASSIGNED to both endpoints.

Assignment basis values are REPORT_EXPLICIT, SOURCE_SUPPORTED_HUMAN_JUDGMENT and UNRESOLVED. ASSIGNED and NOT_ASSIGNED rows must use one of the first two. UNCERTAIN rows must use UNRESOLVED. The structural validator checks references and decision consistency; it does not determine whether the report semantically supports the assignment.

## Three candidate rules

| Rule | Eligibility condition | Main limitation |
|---|---|---|
| NEAREST_COMMON_RESOLVED_NON_REPORT_SCOPE_v0.1 | Any nearest shared resolved non-report ancestor | Can include cross-incident events under a broad campaign or operation |
| SHARED_RESOLVED_INCIDENT_SCOPE_v0.1 | A shared resolved INCIDENT ancestor | Excludes events from separate incidents within one operation |
| EXPLICIT_SHARED_EVENT_COMPARISON_SCOPE_ASSIGNMENT_v0.3 | Both event endpoints have ASSIGNED rows for the same shared resolved non-report ancestor | Requires human decisions and evidence; can miss valid pairs if assignments are incomplete |

The explicit-assignment rule is the recommended candidate for researcher review, not an adopted scientific decision. It is deliberately conservative: missing or uncertain assignments do not create pair opportunities.

## Locking

The v0.3 lock hashes all assignment decisions for a selected report partition and binds them to the v0.2 analysis lock reference. The current draft supports only SINGLE_ANNOTATOR_FINAL; CONSENSUS and ADJUDICATED_FINAL are blocked because v0.3 has no scope-assignment adjudication log. The lock builder first validates the base bundle, v0.2 selected-final register and complete assignment review. Create the lock only after the assignment register is complete for that selected pass:

    python analysis/create_scope_assignment_locks.py --base-bundle ../CTI_Annotation_Schema_RECON_v0.1 --v2-extension ../CTI_Annotation_Schema_RECON_v0.2 --assignment-file registers/event_comparison_scope_assignments.csv --output registers/comparison_scope_assignment_locks.csv --locked-by YOUR_RESEARCHER_ID --lock-date YYYY-MM-DD

Validate the extension:

    python validator/validate_comparison_scope_assignments.py --base-bundle ../CTI_Annotation_Schema_RECON_v0.1 --v2-extension ../CTI_Annotation_Schema_RECON_v0.2 --assignment-file registers/event_comparison_scope_assignments.csv --lock-file registers/comparison_scope_assignment_locks.csv

Run the v0.3 aggregation wrapper with the local frozen source directory, explicitly confirming both lock layers. Pair-opportunity and conditional rates remain withheld unless the scope rule is separately approved by the researcher:

    python analysis/aggregate_selected_report_projections.py --sources-dir PATH_TO_FROZEN_SOURCES --confirm-selected-analysis-locks --confirm-comparison-scope-assignment-locks

Add --approve-scope-pair-rule only after the scientific rule has been formally approved. Do not use it during protocol development.

## Research-readiness boundary

The package currently contains header-only registers and synthetic tests only. It creates no event assignments, annotations, selected partitions, real-report projections, IAA measurements or empirical findings. The extension and the protocol must be reviewed and frozen before human annotation begins.
