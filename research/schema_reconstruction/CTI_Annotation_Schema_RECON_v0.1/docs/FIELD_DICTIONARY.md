# Field dictionary — CTI Annotation Schema RECON v0.1

**Status labels:** `CONFIRMED v0.4-draft` means the concept/value is explicitly in the recovered protocol; `AUDIT-DESCRIBED` means the missing v0.4.2 conformance audit describes it; `RECONSTRUCTION PROPOSAL` means this package introduces a consistent field/enum that still needs approval. None of the headers below are asserted to be original v0.4.2 headers.

## Common conventions

- All registers except `adjudication_log.csv` carry `report_id`, `annotator_id`, and `annotation_pass_id`.
- IDs are strings; numeric-looking report IDs and technique IDs must remain strings.
- Dates use ISO 8601 `YYYY-MM-DD`; timestamps use ISO 8601 with explicit timezone where available.
- Boolean-like decisions use controlled values, not free-form `yes/no` text.
- Empty cells mean unavailable/not applicable only where the field definition permits it. They never imply a negative event-pair label.
- Character offsets are zero-based and end-exclusive.

## `report_registry.csv` — one row per report × annotator × pass

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `report_id` | string | yes | Stable corpus report ID. |
| `annotator_id` | string | yes | Human annotator identifier; do not use AI as an independent rater. |
| `annotation_pass_id` | string | yes | Identifies first pass, washout pass, adjudication pass, etc. |
| `protocol_version`, `schema_version` | string | yes | Exact versions used for this pass. |
| `source_title`, `source_vendor`, `source_url`, `source_path` | string | yes | Source identity and canonical retrieval location. |
| `retrieval_date`, `publication_date` | ISO date/string | retrieval required | Record actual retrieval and publisher date separately. |
| `corpus_name`, `corpus_release`, `split`, `language` | string | where known | Corpus provenance. |
| `source_text_sha256` | 64-char SHA-256 | yes | Hash of exact frozen annotation text. |
| `source_text_char_count` | integer | yes | Character count of that exact text representation. |
| `extraction_method`, `transformation_notes` | string | yes | Extraction and normalization/transformation history. |
| `source_scope_eligibility` | `ELIGIBLE`, `INELIGIBLE`, `PENDING` | yes | Researcher decision on declared CTI-report scope/source identity. **RECONSTRUCTION PROPOSAL.** |
| `source_scope_reason` | string | conditional | Reason for ineligible or pending decision. |
| `local_research_use_status` | `PERMITTED`, `NOT_PERMITTED`, `UNRESOLVED` | yes | Local annotation/use gate, separate from public reuse. **RECONSTRUCTION PROPOSAL.** |
| `local_research_use_basis` | string | conditional | Evidence/rationale for local use. |
| `public_reuse_status` | `PERMITTED`, `RESTRICTED`, `UNRESOLVED`, `NOT_PLANNED` | yes | Separate planned-publication/reuse status. **RECONSTRUCTION PROPOSAL.** |
| `rights_notes` | string | optional | Publisher/donor/licence caveats. |
| `report_assessability` | `ASSESSABLE`, `NOT_ASSESSABLE`, `PENDING` | yes | Whether the complete source can support the study's report-level determination. **RECONSTRUCTION PROPOSAL based on audit-described field.** |
| `assessability_reason` | string | conditional | Reason for not assessable/pending. |
| `full_report_review_status` | `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE` | yes | Coverage state of source-first full report review. **RECONSTRUCTION PROPOSAL.** |
| `prior_exposure_status` | `UNEXPOSED`, `AI_EXPOSED`, `HUMAN_EXPOSED`, `MIXED`, `UNKNOWN` | yes | Prior exposure relevant to blinding. **RECONSTRUCTION PROPOSAL.** |
| `annotator_notes` | string | optional | Other report-level notes. |

## `report_scopes.csv` — one row per scope

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `scope_id` | string | yes | Report-local scope identifier. |
| `parent_scope_id` | string/blank | optional | Parent scope; must resolve within report/annotator/pass. |
| `scope_type` | proposed enum below | yes | `INCIDENT`, `CAMPAIGN`, `ACTOR_OPERATION`, `VICTIM_ORGANISATION`, `HOST`, `REPORT_AGGREGATE`, `OTHER`, `UNRESOLVED`. **RECONSTRUCTION PROPOSAL.** |
| `scope_label`, `scope_description` | string | yes | Human-readable label and boundaries. |
| `scope_status` | `RESOLVED`, `PROVISIONAL`, `UNRESOLVED` | yes | Status of the scope boundary. **RECONSTRUCTION PROPOSAL.** |
| `scope_confidence` | `HIGH`, `MEDIUM`, `LOW` | yes | Annotator confidence. |
| `adjudication_status` | `UNREVIEWED`, `AGREED`, `ADJUDICATED` | yes | Review state; values are from the v0.4 relation-review vocabulary and applied here provisionally. |
| `scope_notes` | string | optional | Scope ambiguity and evidence notes. Evidence links attach through `record_evidence_links.csv`. |

## `activity_units.csv` — one row per report-local unit

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `activity_unit_id` | string | yes | Stable unit identity; event ID equals this ID for a resolved event leaf under the proposed identity invariant. |
| `scope_id` | FK to `report_scopes.scope_id` | yes | Scope containing the unit. |
| `parent_activity_unit_id` | FK/blank | optional | Series/episode/aggregate parent, if any. |
| `granularity` | v0.4 values | yes | `atomic_event`, `repeated_event_series`, `activity_episode`, `report_level_aggregate`, `unresolved`. **CONFIRMED v0.4-draft.** |
| `unit_role` | v0.4 values | yes | `event_leaf`, `series_container`, `episode_container`, `aggregate_container`, `unresolved_unit`. **CONFIRMED v0.4-draft.** |
| `instance_status` | v0.4 values | yes | `RESOLVED`, `UNRESOLVED`, `GENERIC_BEHAVIOUR`, `NOT_AN_EVENT`. **CONFIRMED v0.4-draft.** |
| `count_status` | v0.4 values | yes | `exact`, `minimum`, `range`, `qualitative_only`, `unknown`. **CONFIRMED v0.4-draft.** |
| `count_exact`, `count_min`, `count_max` | non-negative integer/blank | conditional | Numeric bounds consistent with count_status. |
| `count_qualitative`, `recurrence_pattern` | string | conditional | Retain qualitative repetition without inventing event counts. |
| `unit_summary` | string | yes | Concise report-grounded description of the unit. |
| `actor_ref`, `host_or_asset_ref` | string/blank | optional | Report-local references; unknown remains blank/unknown, never invented. |
| `annotator_confidence` | `HIGH`, `MEDIUM`, `LOW` | yes | Confidence. |
| `adjudication_status` | `UNREVIEWED`, `AGREED`, `ADJUDICATED` | yes | Review state. |
| `unit_notes` | string | optional | Rationale/uncertainty. |

## `event_mentions.csv` — one row per text mention

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `mention_id` | string | yes | Mention identifier. |
| `activity_unit_id` | FK | yes | Unit to which this mention is linked; may be a container or event leaf. |
| `primary_evidence_span_id` | FK to evidence spans | yes | Canonical exact span for this mention. |
| `sentence_id`, `section_locator` | string | where available | Stable source locators. |
| `mention_kind` | string | yes | Mention type; enum intentionally not frozen because exact v0.4.2 enum is unavailable. |
| `instance_status` | v0.4 values | yes | Mention-level assessment. Unit-level `activity_units.instance_status` is authoritative for primary graph eligibility; mismatches require `mention_unit_status_note`. |
| `resolved_event_instance_id` | string/blank | conditional | Equals `activity_unit_id` for a resolved atomic event leaf; blank for non-leaf/unresolved mentions. |
| `event_type_text`, `actor_text`, `target_text`, `asset_or_host_text`, `time_expression` | string/blank | optional | Source wording extracted without upgrading it to a resolved event. |
| `mention_unit_status_note` | string | conditional | Explains any mention-level/unit-level status mismatch. |
| `annotator_confidence`, `adjudication_status` | controlled | yes | Confidence and review state. |
| `mention_notes` | string | optional | Additional notes. |

## `evidence_spans.csv` — one row per exact source span

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `evidence_span_id` | string | yes | Evidence span identifier. |
| `char_start`, `char_end` | integer | yes | Zero-based half-open offsets into exact frozen source text. Require `0 <= char_start < char_end <= source_text_char_count`. |
| `evidence_text` | string | yes | Exact substring; must equal frozen source slice. |
| `sentence_id`, `section_locator`, `paragraph_locator`, `figure_locator` | string/blank | where available | Human-readable locators. |
| `source_text_sha256` | 64-char SHA-256 | yes | Must equal report registry hash for same report/pass. |
| `span_kind` | string | yes | `MENTION`, `RELATION`, `TIME`, `SCOPE`, `MAPPING`, `RIGHTS`, `OTHER` proposed labels. |
| `span_notes` | string | optional | Additional locator/context. |

## `record_evidence_links.csv` — one row per additional evidence link

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `link_id` | string | yes | Unique row identifier; added to resolve audit's missing link key. |
| `record_type` | register name | yes | One of the 12 register names, including `report_registry` for report-level eligibility evidence. |
| `record_id` | string | yes | ID of the record within `record_type`. |
| `evidence_span_id` | FK | yes | Linked evidence span. |
| `evidence_role` | proposed enum | yes | `SOURCE_IDENTITY`, `ELIGIBILITY`, `RIGHTS`, `SCOPE_BOUNDARY`, `ACTIVITY_UNIT`, `MENTION`, `MAPPING`, `TIME`, `TEMPORAL_RELATION`, `NON_TEMPORAL_RELATION`, `ADJUDICATION`, `OTHER`. |
| `link_notes` | string | optional | Explain link role where needed. |

Primary evidence spans referenced in direct `primary_evidence_span_id` fields must not be duplicated in this table. The composite tuple `(report_id, annotator_id, annotation_pass_id, record_type, record_id, evidence_span_id, evidence_role)` is also unique.

## `event_mappings.csv` — one row per mapping decision

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `mapping_id` | string | yes | Stable mapping decision ID. Multiple evidence spans attach via link table. |
| `activity_unit_id` | FK | yes | Unit receiving the mapping. Primary mapping metrics require eligible event leaves. |
| `event_instance_id` | string/blank | conditional | For resolved event leaves, must equal activity_unit_id. |
| `exact_technique_id`, `exact_technique_name` | string | conditional | Source-supported parent or sub-technique. Preserve exact mapping level. |
| `attack_version` | string | yes | Pinned ATT&CK release/version used for mapping. |
| `mapping_basis` | v0.4 values | yes | `report_explicit_subtechnique`, `report_explicit_parent`, `source_supported_analyst_candidate`, `workbook_only`, `unresolved`. **CONFIRMED v0.4-draft.** |
| `mapping_decision_status` | `ACCEPTED`, `ALTERNATIVE`, `REJECTED`, `UNRESOLVED` | yes | **RECONSTRUCTION PROPOSAL**; exact v0.4.2 enum unavailable. |
| `alternative_group_id`, `alternative_to_mapping_id` | string/blank | conditional | Link mutually exclusive alternatives; alternatives do not enter primary mapping set. |
| `baseline_vocabulary_id`, `baseline_vocabulary_sha256` | string | yes for baseline analysis | Must identify the pinned derived A_120 artifact and SHA-256. |
| `baseline_parent_technique_id` | string/blank | conditional | Parent technique ID used in the ChronoCTI 120-term vocabulary. |
| `baseline_mapping_status` | `IN_VOCAB`, `OUT_OF_VOCAB`, `UNRESOLVED`, `NOT_APPLICABLE` | yes | **RECONSTRUCTION PROPOSAL.** `IN_VOCAB` requires membership in pinned A_120. |
| `annotator_confidence`, `adjudication_status` | controlled | yes | Confidence and review state. |
| `mapping_notes` | string | optional | Rationale/alternatives. |

## `time_evidence.csv` — one row per typed time observation

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `time_evidence_id` | string | yes | Time observation ID. |
| `activity_unit_id`, `mention_id` | FK/blank | at least one | Link to relevant unit/mention when the source establishes it. |
| `raw_time_text` | string | yes | Exact source time expression; never discard after normalization. |
| `time_type` | proposed enum | yes | `ATTACK_OCCURRENCE`, `ATTACK_PERIOD`, `DETECTION`, `DISCOVERY`, `SAMPLE_UPLOAD`, `SAMPLE_COMPILATION`, `PUBLICATION`, `REPORT_RETRIEVAL`, `OTHER`, `UNKNOWN`. **RECONSTRUCTION PROPOSAL; validate against researcher decision.** |
| `time_precision` | proposed enum | yes | `YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, `SECOND`, `INTERVAL`, `QUALITATIVE`, `UNKNOWN`. |
| `timezone_text` | string/blank | optional | Timezone phrase exactly as source gives it. |
| `timezone_status` | `EXPLICIT`, `INFERRED`, `UNKNOWN`, `NOT_APPLICABLE` | yes | Whether timezone is explicit. **RECONSTRUCTION PROPOSAL.** |
| `normalized_start`, `normalized_end`, `normalized_timezone` | ISO timestamp/blank | conditional | Normalized interval; only fill when justified. |
| `normalization_status` | `NORMALIZED`, `PARTIALLY_NORMALIZED`, `NOT_NORMALIZABLE`, `UNRESOLVED` | yes | **RECONSTRUCTION PROPOSAL.** |
| `uncertainty_notes` | string | conditional | Preserve uncertainty and alternative interpretations. |
| `primary_evidence_span_id` | FK | yes | Primary time evidence span; further support may be linked in link register. |
| `annotator_confidence`, `adjudication_status` | controlled | yes | Confidence/review. |
| `time_notes` | string | optional | Additional notes. |

## `temporal_relations.csv` — one row per event-pair relation

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `relation_id` | string | yes | Relation identifier. |
| `event_a_id`, `event_b_id` | FK to activity_units | yes | Distinct resolved atomic event-leaf IDs for primary relations. Self-relations forbidden. |
| `comparison_scope_id` | FK | yes | Scope within which pair is compared. |
| `scope_compatibility` | `COMPATIBLE`, `INCOMPATIBLE`, `UNCERTAIN` | yes | **RECONSTRUCTION PROPOSAL** made explicit for validator. |
| `relation_label` | v0.4 values | yes | The eight values in Controlled Vocabularies. **CONFIRMED v0.4-draft.** |
| `relation_basis` | v0.4 values | yes | `direct_source`, `direct_timestamp`, `derived_transitive`, `inference`, `unresolved`. **CONFIRMED v0.4-draft.** |
| `evidence_scope` | v0.4 values | yes | `SENTENCE`, `CROSS_SENTENCE`, `DOCUMENT_CONTEXT`. **CONFIRMED v0.4-draft; audit says missing from original v0.4.2 table.** |
| `primary_evidence_span_id` | FK | required for positive relations | Relation-specific primary evidence span. |
| `annotator_confidence`, `adjudication_status` | controlled | yes | Confidence/review. |
| `relation_notes` | string | optional | Uncertainty/rationale. |

## `candidate_pair_assessments.csv` — optional assessed pair frame

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `assessment_id` | string | yes | Assessment row ID. |
| `event_a_id`, `event_b_id` | FK | yes | Distinct candidate event-leaf endpoints. |
| `candidate_rule_id`, `candidate_rule_version` | string | yes | Frozen candidate-generation rule and version. |
| `comparison_scope_id`, `scope_compatibility` | FK/controlled | yes | Scope rule must be explicit; require compatible pairs unless rule deliberately assesses scope incompatibility. |
| `assessment_label` | positive temporal label or `NO_TEMPORAL_CLAIM`, `VAGUE_OR_AMBIGUOUS`, `NOT_ASSESSABLE` | yes | Only assessed pairs appear; never generate all-pairs negatives by default. |
| `related_relation_id` | FK/blank | conditional | Links to positive relation record where applicable. |
| `assessment_reason` | string | conditional | Explanation for negative/ambiguous/not-assessable assessment. |
| `adjudication_status`, `assessment_notes` | controlled/string | yes/optional | Review state/notes. |

## `non_temporal_relations.csv` — separate causal/dependency/narrative layer

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `non_temporal_relation_id` | string | yes | Relation ID. |
| `activity_unit_a_id`, `activity_unit_b_id` | FK | yes | May reference containers or leaves; not automatically graph endpoints. |
| `relation_label` | v0.4 values | yes | `CAUSES_OR_ENABLES`, `DEPENDS_ON`, `PRECONDITION_OF`, `NARRATIVE_ORDER_ONLY`. **CONFIRMED v0.4-draft.** |
| `evidence_scope` | v0.4 values | yes | Source evidence scope. |
| `primary_evidence_span_id` | FK | yes | Primary evidence span. |
| `annotator_confidence`, `adjudication_status` | controlled | yes | Confidence/review. |
| `relation_notes` | string | optional | Additional rationale. |

## `adjudication_log.csv` — append-only decision history

| Field | Type / values | Required | Definition |
|---|---|---:|---|
| `report_id`, `annotation_pass_id` | string | yes | Target report/pass. |
| `adjudication_id` | string | yes | Unique decision ID. |
| `target_annotator_id`, `reviewer_id` | string | yes | Whose record was reviewed and who reviewed it. |
| `target_register`, `target_record_id`, `field_name` | string | yes | Exact target field. |
| `original_value`, `proposed_value`, `final_value` | string/blank | yes | Preserve initial and final values. |
| `decision_status` | `AGREED`, `ADJUDICATED`, `DEFERRED` | yes | **RECONSTRUCTION PROPOSAL.** |
| `rationale`, `decision_date` | string/date | yes | Explain decision and record date. |
| `primary_evidence_span_id` | FK/blank | optional | Decision-specific evidence. |
| `adjudication_notes` | string | optional | Other notes. |
