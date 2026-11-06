# Schema manifest — RECON v0.3 explicit comparison-scope extension

- Version: 0.3
- Prepared: 5 November 2026
- Status: draft; researcher review required; not approved or frozen
- Type: additive extension
- Parent: ../CTI_Annotation_Schema_RECON_v0.2
- Real assignment rows: 0
- Synthetic tests only: yes
- Semantic scope-assignment review: not performed

## Added registers

- registers/event_comparison_scope_assignments.csv
  - Grain: one activity unit × candidate comparison scope × report/annotator/pass.
  - Decisions: ASSIGNED, NOT_ASSIGNED or UNCERTAIN.
  - ASSIGNED rows require a source evidence span, rationale, confidence, a supported basis, a RESOLVED comparable non-report scope, and the scope to be in the event's resolved ancestry.
  - Every eligible resolved non-report ancestor scope requires one explicit row per event; missing decisions block validation. NOT_ASSIGNED is explicit and distinct from missing or UNCERTAIN.
- registers/comparison_scope_assignment_locks.csv
  - Grain: one selected-final report/annotator/pass.
  - Binds the exact v0.3 assignment rows to the v0.2 selected-analysis lock reference.
  - Assignment edits or a changed v0.2 selection lock invalidate the v0.3 lock.

## Candidate scope-pair rules

1. NEAREST_COMMON_RESOLVED_NON_REPORT_SCOPE_v0.1 — legacy broad ancestor rule.
2. SHARED_RESOLVED_INCIDENT_SCOPE_v0.1 — conservative incident-bounded sensitivity rule.
3. EXPLICIT_SHARED_EVENT_COMPARISON_SCOPE_ASSIGNMENT_v0.3 — recommended candidate; both endpoints must have ASSIGNED rows for the same shared scope.

The v0.3 rule does not automatically fall back to either older rule. UNCERTAIN or missing assignments do not qualify. The selected rule must govern the opportunity denominator and primary relation numerator consistently.

## Validation

- Assignment references remain partition-local.
- Only resolved atomic event_leaf units receive assignments.
- ASSIGNED scope must be RESOLVED, non-report, in the provisional comparable-scope type set and present in the event's resolved ancestry.
- ASSIGNED and NOT_ASSIGNED require evidence and rationale; UNCERTAIN requires an unresolved basis and rationale.
- Positive direct temporal relations and COMPATIBLE candidate-pair assessments must use a scope explicitly ASSIGNED to both endpoints.
- A dedicated lock covers the assignment register and the v0.2 analysis lock reference.

## Analysis

The v0.2 report-level aggregator accepts a named scope-pair rule and optional assignment rows. The v0.3 wrapper supplies the explicit rule only after the assignment register passes validation and its lock matches. The caller must still provide explicit selected-analysis and assignment-lock confirmations. Rates dependent on the scope-pair rule remain withheld unless separately approved.

## Limitations

The validator cannot decide semantic scope membership or whether a source supports the analyst's assignment rationale. The explicit-assignment candidate depends on human consistency and complete recording of considered scope assignments. No real data has been entered, and the extension has not been approved or frozen.


## Additional validation correction

The v0.3 validator delegates structural validation to RECON v0.1 and can optionally verify frozen source texts. The v0.3 lock builder and lock validator now validate the v0.2 selected-final partition register before creating or accepting an assignment lock. This draft permits only UNREVIEWED assignment adjudication status; a v0.3 adjudication log is not implemented.
