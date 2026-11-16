# RECON v0.4 data model and validation rules

## One-to-one extension invariant

For every activity unit in RECON v0.1 activity_units.csv, RECON v0.4 requires exactly one activity_unit_strata.csv row with the same report_id, annotator_id, annotation_pass_id and activity_unit_id. Missing, duplicate and orphan rows are errors. This is the canonical v0.4 representation of the logical activity_unit.activity_stratum field; the v0.1 register is not modified.

Every row requires a controlled stratum, controlled basis, source evidence span, non-empty rationale, confidence and adjudication status. UNRESOLVED_CLASSIFICATION requires basis UNRESOLVED. Other strata require REPORT_EXPLICIT or SOURCE_SUPPORTED_HUMAN_JUDGMENT.

GENERIC_CAPABILITY cannot be attached to a RESOLVED atomic event_leaf. A capability description with no resolved report-local execution is not an event occurrence.

## Cross-layer base review metadata enums

The v0.1 field dictionary declares `annotator_confidence` and `adjudication_status` as required controlled values on the applicable base registers, and `evidence_spans.span_kind` as a controlled value. The original v0.1 validator does not reject invalid values for all of those fields. The v0.4 full-package validator therefore adds fail-closed checks for:

- `annotator_confidence`: HIGH, MEDIUM, or LOW on activity units, mentions, mappings, time evidence, temporal relations, and non-temporal relations
- `adjudication_status`: UNREVIEWED, AGREED, or ADJUDICATED on scopes, activity units, mentions, mappings, time evidence, temporal relations, candidate-pair assessments, and non-temporal relations
- `evidence_spans.span_kind`: MENTION, RELATION, TIME, SCOPE, MAPPING, RIGHTS, or OTHER

Blank and unknown values fail validation. This is an additive v0.4 validation gate; the checksum-controlled v0.1 package files and register headers remain unchanged.

## Temporal relation routing

Temporal relation rows are routed using the stratum of both endpoints:

- PRIMARY_ATTACK_ACTION — both endpoints are ATTACK_ACTION. This is the only route eligible for primary attack-action projection and pair-opportunity metrics, subject to existing v0.1/v0.2/v0.3 event-leaf, evidence, selected-final, and scope rules.
- AUXILIARY_SAME_STRATUM — both endpoints have the same non-primary stratum. Retain for a parallel descriptive view; exclude from primary metrics.
- MIXED_STRATUM — endpoints have different strata. Retain for review/diagnostics; exclude from primary metrics.

The validator emits a warning for direct positive auxiliary or mixed relations. It does not delete these records or recode them as negative. The projection helper filters relation endpoints before constructing the primary edge list.

## Pair opportunities and mappings

The primary pair-opportunity function receives only ATTACK_ACTION resolved atomic event leaves. Therefore auxiliary and mixed pairs cannot enter its numerator or denominator. Accepted A_120 mapping rows are passed to the primary projection only when their activity_unit_id belongs to the ATTACK_ACTION event-leaf set. Stratum classification is independent of ATT&CK mapping status; unmapped attack actions remain eligible event units with no technique mapping.

## Locking

The activity-stratum lock binds the canonical sorted v0.4 stratum rows to the v0.2 selected-analysis lock reference. Every selected-final report partition must have exactly one stratum lock. If a stratum row changes after locking, the digest check fails. The lock detects edits; it does not authenticate the lock owner.

Call validate_activity_strata before creating the lock. The create_activity_stratum_locks.py CLI enforces that check. The selected-analysis lock must still be validated using the v0.2 selected-partition adapter before projection. If the explicit v0.3 scope rule is selected, its own assignment completeness and lock checks also remain mandatory.
