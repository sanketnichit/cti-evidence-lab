# Data model and validation rules — CTI Annotation Schema RECON v0.1

**Status:** proposed executable invariants, not a reconstruction of original v0.4.2 validation code.

## Record identity / uniqueness

All annotation rows are partitioned by `(report_id, annotator_id, annotation_pass_id)` except adjudication records, which target an explicit report/pass/annotator record.

| Register | Primary key within its partition |
|---|---|
| report_registry | report_id + annotator_id + annotation_pass_id |
| report_scopes | scope_id |
| activity_units | activity_unit_id |
| event_mentions | mention_id |
| evidence_spans | evidence_span_id |
| record_evidence_links | link_id; also enforce unique composite link tuple |
| event_mappings | mapping_id |
| time_evidence | time_evidence_id |
| temporal_relations | relation_id |
| candidate_pair_assessments | assessment_id |
| non_temporal_relations | non_temporal_relation_id |
| adjudication_log | adjudication_id |

## Foreign keys

- `report_scopes.parent_scope_id` -> `report_scopes.scope_id` in the same report/annotator/pass.
- `activity_units.scope_id` -> `report_scopes.scope_id`.
- `activity_units.parent_activity_unit_id` -> `activity_units.activity_unit_id`; parent hierarchy must be acyclic.
- `event_mentions.activity_unit_id` -> `activity_units.activity_unit_id`.
- `event_mentions.primary_evidence_span_id` -> `evidence_spans.evidence_span_id`.
- `time_evidence.activity_unit_id` and `mention_id` -> corresponding registers when non-empty; at least one link must be present.
- `time_evidence.primary_evidence_span_id` -> `evidence_spans.evidence_span_id`.
- `temporal_relations.event_a_id`, `event_b_id` -> `activity_units.activity_unit_id`; `comparison_scope_id` -> `report_scopes.scope_id`.
- `candidate_pair_assessments` event IDs and comparison scope -> matching registers; `related_relation_id` -> `temporal_relations.relation_id` where populated.
- `non_temporal_relations.activity_unit_a_id/b_id` -> activity units; `primary_evidence_span_id` -> evidence spans.
- `record_evidence_links.evidence_span_id` -> evidence spans; `record_type`/`record_id` must resolve to the correct register.
- All cross-register references must remain within the same report, annotator and pass unless an adjudication record explicitly documents a cross-annotator reference.

## Source-text integrity

1. Every source text is frozen and hashed in `report_registry.csv`.
2. Every evidence span has the same `source_text_sha256` as its report/pass registry row.
3. Offsets are zero-based and half-open: `0 <= char_start < char_end <= source_text_char_count`.
4. `evidence_text` must equal the exact source substring at `[char_start:char_end]`.
5. Any whitespace normalization or extraction transformation must be frozen and described before offsets are generated.

## Activity-unit invariants

1. `event_leaf` requires `atomic_event` + `RESOLVED`.
2. `series_container` is intended for `repeated_event_series`; `episode_container` for `activity_episode`; `aggregate_container` for `report_level_aggregate`; `unresolved_unit` for `unresolved`. These pairings are provisional reconstruction choices and should be approved.
3. Container units are not primary event graph nodes or event-edge endpoints.
4. A resolved event instance is identified by its activity-unit ID. If `event_mentions.resolved_event_instance_id` is populated for a primary event leaf, it must equal the linked `activity_unit_id`.
5. Unit-level `activity_units.instance_status` controls event-graph eligibility. Mention-level `event_mentions.instance_status` describes that mention; mismatches require an explanatory note and are not silently overwritten.
6. Count fields must agree with `count_status`: `exact` -> `count_exact`; `minimum` -> `count_min`; `range` -> both `count_min` and `count_max`; `qualitative_only` -> `count_qualitative`; `unknown` -> no numeric value. Bounds must be non-negative and `count_min <= count_max`.

## Mapping invariants

1. `event_mappings.activity_unit_id` must resolve within the same partition.
2. Only `mapping_decision_status=ACCEPTED` with source-supported `mapping_basis` may enter primary mapping sets.
3. `mapping_basis=workbook_only` must never be accepted into `A_exact` or `A_120`.
4. `ALTERNATIVE`, `REJECTED`, or `UNRESOLVED` decisions are excluded from primary mapping sets.
5. Every `baseline_mapping_status=IN_VOCAB` must have `baseline_parent_technique_id` present in the pinned A_120 list and matching `baseline_vocabulary_sha256`.
6. Exact technique/sub-technique IDs are retained separately from parent technique IDs.

## Evidence-link invariants

1. `primary_evidence_span_id` fields identify primary evidence.
2. `record_evidence_links.csv` is reserved for additional evidence spans.
3. A primary span must not be duplicated in the link register for the same target record and role.
4. `link_id` is unique; the composite `(report_id, annotator_id, annotation_pass_id, record_type, record_id, evidence_span_id, evidence_role)` is also unique.
5. `record_type` is a known register; `record_id` resolves in that register.

## Temporal relation eligibility

A row enters the primary positive temporal graph only when:

- endpoints are different IDs;
- both endpoints are `event_leaf` + `atomic_event` + `RESOLVED`;
- both endpoint activity units resolve to the recorded comparison scope, or an approved scope-compatibility rule records their compatibility;
- `scope_compatibility=COMPATIBLE`;
- `relation_label` is one of `BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, `CONCURRENT_UNSPECIFIED`;
- `relation_basis` is `direct_source` or `direct_timestamp`;
- relation-specific primary evidence span and `evidence_scope` are present.

`NO_TEMPORAL_CLAIM` is permitted only in candidate pair assessments with a frozen rule/version. `VAGUE_OR_AMBIGUOUS` and `NOT_ASSESSABLE` are non-positive states. `derived_transitive`, `inference`, and `unresolved` are excluded from primary positive-edge counts.

## Candidate-pair, non-temporal and time rules

- Candidate pair assessment does not define the positive relation discovery universe; no unassessed pair is negative.
- Both assessed endpoints must be distinct, resolved atomic `event_leaf` units; containers and unresolved units are not candidate event pairs.
- Candidate-pair rules must be versioned and scope-aware.
- Non-temporal relations may connect broader activity units, including containers, but must never enter the temporal projection.
- Raw time text and precision are always retained. Normalize only when justified. Strict ordering from uncertain timezone data is allowed only if order is invariant under the recorded uncertainty.
- `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` are positive temporal relations for broad incidence but never enter strict-order cycle analysis.

## Report denominator rules

- Source-scope eligibility, local research-use permission, public reuse permission and report assessability are distinct fields.
- Primary report-level rates use eligible reports with `report_assessability=ASSESSABLE` and at least one completed full-report review; each report is counted once after report-level conflicts are resolved. Assessability coverage is reported against eligible reports. A zero-event-leaf report remains in the denominator when these conditions hold; `NOT_ASSESSABLE`, `PENDING`, incomplete review and unresolved conflicts are not zero outcomes.
- `N_assessable` additionally requires the exact frozen source text to be supplied to validation and to pass source-hash and character-count checks. A syntactically valid SHA-256 field without the source bytes does not establish a complete/readable verified source; such a partition remains outside `N_assessable` until verified.
- An assessable report with zero event leaves remains in the denominator.
- `NOT_ASSESSABLE` is not a zero-edge report.
- A report with no resolved event leaves must not be excluded for that reason alone.


## Frozen source-text convention\n\nSource text is decoded as strict UTF-8. An optional leading UTF-8 BOM is removed; CRLF/LF line endings are preserved; no Unicode normalization is applied. `source_text_sha256` is SHA-256 over the UTF-8 bytes of the exact decoded annotation text. `source_text_char_count` and zero-based end-exclusive offsets count Python Unicode code points in that same text. The source hash/offset check must use the exact frozen text; do not normalize line endings after annotations have been created.\n\nFor `direct_timestamp`, both event endpoints require normalized time evidence with their own source evidence spans. Candidate-pair positive assessments must match the linked temporal relation's unordered event pair and relation label. Duplicate or contradictory direct temporal claims for one event pair are rejected by the reconstruction validator.\n\n## Executable validator scope

`validator/validate_annotations.py` enforces the structural checks listed above for this reconstructed package. Its synthetic test suite is in `tests/test_validator.py`. It deliberately does not decide whether the report semantically supports an activity-unit identity, ATT&CK mapping, scope boundary, or temporal relation. A valid validator result means only that recorded values are structurally consistent under this reconstructed contract.
