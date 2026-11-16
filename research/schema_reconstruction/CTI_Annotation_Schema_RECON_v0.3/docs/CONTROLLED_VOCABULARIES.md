# RECON v0.3 extension controlled vocabularies

**Status:** draft extension; researcher review required.

## `assignment_status`

- `ASSIGNED` — the event is affirmatively assigned to the candidate comparison scope.
- `NOT_ASSIGNED` — the candidate scope was explicitly reviewed and rejected for this event. It creates no pair opportunity.
- `UNCERTAIN` — the candidate scope was considered but cannot be resolved. It creates no pair opportunity.

## `assignment_basis`

- `REPORT_EXPLICIT` — the report explicitly identifies the event as belonging to the scope.
- `SOURCE_SUPPORTED_HUMAN_JUDGMENT` — the annotator makes a source-grounded judgement and records the rationale.
- `UNRESOLVED` — the assignment is uncertain and the available evidence does not support a resolved decision.

ASSIGNED and NOT_ASSIGNED require REPORT_EXPLICIT or SOURCE_SUPPORTED_HUMAN_JUDGMENT plus an evidence span. UNCERTAIN requires UNRESOLVED; an evidence span is optional for that state.

## Inherited controlled values

- `annotator_confidence`: HIGH, MEDIUM, LOW (v0.1).
- `adjudication_status`: UNREVIEWED only in this extension draft; v0.3 assignment adjudication is not implemented.
- `comparison_scope_id`: must resolve to a RESOLVED scope in the v0.1 comparable-scope set: INCIDENT, CAMPAIGN, ACTOR_OPERATION, VICTIM_ORGANISATION, HOST, or OTHER. REPORT_AGGREGATE and UNRESOLVED scopes are not eligible.
- `lock_format`: `CTI-EVIDENCE-LAB-COMPARISON-SCOPE-LOCK-v0.3`.

The v0.3 lock path supports `SINGLE_ANNOTATOR_FINAL` only. CONSENSUS and ADJUDICATED_FINAL require a dedicated v0.3 assignment-adjudication register, validator, and procedure before use.
