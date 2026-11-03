# Controlled vocabularies — CTI Annotation Schema RECON v0.1

`CONFIRMED v0.4-draft` means the values appear in the recovered Protocol v0.4-draft. `PROVISIONAL RECONSTRUCTION` means the value set is proposed because the exact original schema dictionary or Protocol v0.4.1 could not be recovered.

## Confirmed in recovered Protocol v0.4-draft

### `instance_status`
`RESOLVED`, `UNRESOLVED`, `GENERIC_BEHAVIOUR`, `NOT_AN_EVENT`

### `granularity`
`atomic_event`, `repeated_event_series`, `activity_episode`, `report_level_aggregate`, `unresolved`

### `unit_role`
`event_leaf`, `series_container`, `episode_container`, `aggregate_container`, `unresolved_unit`

### `count_status`
`exact`, `minimum`, `range`, `qualitative_only`, `unknown`

### `mapping_basis`
`report_explicit_subtechnique`, `report_explicit_parent`, `source_supported_analyst_candidate`, `workbook_only`, `unresolved`

### `relation_label`
`BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, `CONCURRENT_UNSPECIFIED`, `NO_TEMPORAL_CLAIM`, `VAGUE_OR_AMBIGUOUS`, `NOT_ASSESSABLE`

### `relation_basis`
`direct_source`, `direct_timestamp`, `derived_transitive`, `inference`, `unresolved`

### `evidence_scope`
`SENTENCE`, `CROSS_SENTENCE`, `DOCUMENT_CONTEXT`

### `annotator_confidence`
`HIGH`, `MEDIUM`, `LOW`

### `adjudication_status`
`UNREVIEWED`, `AGREED`, `ADJUDICATED`

### `non_temporal_relations.relation_label`
`CAUSES_OR_ENABLES`, `DEPENDS_ON`, `PRECONDITION_OF`, `NARRATIVE_ORDER_ONLY`

### Baseline alignment labels
`supported`, `multiple_candidate_pairs`, `ambiguous`, `unmapped`, `not_assessable`

## Provisional reconstruction enums — researcher approval required

These are introduced to make the replacement schema executable. They are **not asserted to be the original v0.4.2 enums**.

- `source_scope_eligibility`: `ELIGIBLE`, `INELIGIBLE`, `PENDING`
- `local_research_use_status`: `PERMITTED`, `NOT_PERMITTED`, `UNRESOLVED`
- `public_reuse_status`: `PERMITTED`, `RESTRICTED`, `UNRESOLVED`, `NOT_PLANNED`
- `report_assessability`: `ASSESSABLE`, `NOT_ASSESSABLE`, `PENDING`
- `full_report_review_status`: `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`
- `prior_exposure_status`: `UNEXPOSED`, `AI_EXPOSED`, `HUMAN_EXPOSED`, `MIXED`, `UNKNOWN`
- `scope_type`: `INCIDENT`, `CAMPAIGN`, `ACTOR_OPERATION`, `VICTIM_ORGANISATION`, `HOST`, `REPORT_AGGREGATE`, `OTHER`, `UNRESOLVED`
- `scope_status`: `RESOLVED`, `PROVISIONAL`, `UNRESOLVED`
- `mapping_decision_status`: `ACCEPTED`, `ALTERNATIVE`, `REJECTED`, `UNRESOLVED`
- `baseline_mapping_status`: `IN_VOCAB`, `OUT_OF_VOCAB`, `UNRESOLVED`, `NOT_APPLICABLE`
- `scope_compatibility`: `COMPATIBLE`, `INCOMPATIBLE`, `UNCERTAIN`
- `time_type`: `ATTACK_OCCURRENCE`, `ATTACK_PERIOD`, `DETECTION`, `DISCOVERY`, `SAMPLE_UPLOAD`, `SAMPLE_COMPILATION`, `PUBLICATION`, `REPORT_RETRIEVAL`, `OTHER`, `UNKNOWN`
- `time_precision`: `YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, `SECOND`, `INTERVAL`, `QUALITATIVE`, `UNKNOWN`
- `timezone_status`: `EXPLICIT`, `INFERRED`, `UNKNOWN`, `NOT_APPLICABLE`
- `normalization_status`: `NORMALIZED`, `PARTIALLY_NORMALIZED`, `NOT_NORMALIZABLE`, `UNRESOLVED`
- `span_kind`: `MENTION`, `RELATION`, `TIME`, `SCOPE`, `MAPPING`, `RIGHTS`, `OTHER`
- `evidence_role`: `SOURCE_IDENTITY`, `ELIGIBILITY`, `RIGHTS`, `SCOPE_BOUNDARY`, `ACTIVITY_UNIT`, `MENTION`, `MAPPING`, `TIME`, `TEMPORAL_RELATION`, `NON_TEMPORAL_RELATION`, `ADJUDICATION`, `OTHER`
- `candidate_pair_assessments.assessment_label`: any positive temporal `relation_label`, `NO_TEMPORAL_CLAIM`, `VAGUE_OR_AMBIGUOUS`, `NOT_ASSESSABLE`
- `adjudication_log.decision_status`: `AGREED`, `ADJUDICATED`, `DEFERRED`

No `NULL` is treated as a generic missing/negative label. Empty cell, unresolved, no temporal claim, vague/ambiguous, not assessable, and not reviewed are separate states.
