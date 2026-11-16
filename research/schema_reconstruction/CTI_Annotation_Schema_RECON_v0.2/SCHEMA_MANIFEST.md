# Schema manifest — RECON v0.2 temporal evidence extension

- Version: 0.2
- Prepared: 5 November 2026
- Updated: 16 November 2026
- Latest main-branch verification: GitHub Actions run #299 passed 99 RECON v0.2 synthetic tests as part of 283 total tests; base package checksums and all workflow steps passed. The selected-final suite includes append-only field history across ADJUDICATED/AGREED/DEFERRED outcomes, non-value-changing outcome enforcement and immutable identity-field regressions.
- Status: draft; researcher review required; not approved or frozen
- Type: additive extension
- Parent: ../CTI_Annotation_Schema_RECON_v0.1
- Real report rows: 0
- Synthetic tests only: yes
- Semantic evidence review: not performed
- Evidence-scope completeness: implemented as structural locator/role checks for SENTENCE, CROSS_SENTENCE and DOCUMENT_CONTEXT
- Strict timestamp uncertainty ordering: implemented as a conservative structural gate for direct timestamp BEFORE/AFTER relations
- Report-level aggregation: implemented; synthetic fixtures only; not run on human annotations

## Evidence roles

- RELATION_CUE: required; stored in temporal_relations.primary_evidence_span_id.
- EVENT_A_SUPPORT: required; stored in temporal_relation_evidence.csv.
- EVENT_B_SUPPORT: required; stored in temporal_relation_evidence.csv.
- RELATION_CONTEXT: optional for sentence/cross-sentence claims; required with a non-empty rationale for DOCUMENT_CONTEXT claims.

This extension does not replace or alter RECON v0.1 and does not claim equivalence to the missing original v0.4.2 schema.

## Timestamp gate — working semantics and structural enforcement

- A direct-timestamp endpoint requires `time_type=ATTACK_OCCURRENCE`, explicit timezone status/text, preserved raw expression/precision, and a linked endpoint-support span.
- Time evidence may link to an activity unit, a mention, or both. Mention-only rows resolve through `event_mentions.activity_unit_id`; dual targets must identify the same unit. The direct-timestamp endpoint check uses the resolved unit before matching endpoint-support spans.
- Normalized bounds are closed bounds on possible occurrence instants, not action-duration intervals. Non-point bounds require `uncertainty_notes`.
- The source zone/offset is preserved in `timezone_text`; normalized bounds must use UTC-offset ISO-8601 values and `normalized_timezone=UTC`.
- Retained but non-normalized timestamp candidates are rejected rather than ignored.
- Timestamp-only positives are restricted to `BEFORE`/`AFTER`; strict order must hold for every retained A/B interval combination (`A_end < B_start`, or the reverse for AFTER).
- `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` require an explicit source assertion and `relation_basis=direct_source`; equal timestamps and overlapping uncertainty bounds are not sufficient.
- Ambiguous abbreviations, inferred zones, and unresolved daylight-saving folds/gaps cannot support a timestamp-derived edge.
- Human review remains responsible for confirming that time evidence identifies the attack occurrence and that the source entails the relation. See `research/protocol/TIMESTAMP_RELATION_SEMANTICS_v0.1.md`.

### Time-evidence target resolution

- `time_evidence` may target `activity_unit_id`, `mention_id`, or both, as defined by the v0.1 field dictionary.
- A `mention_id` must resolve in the same report/annotator/pass and maps through `event_mentions.activity_unit_id` to an activity unit.
- If both IDs are populated, they must resolve to the same unit; contradictory targets are rejected.
- The direct-timestamp endpoint gate resolves mention-only time rows through the mention's activity unit before matching endpoint-support spans.

## Evidence-scope gate

- SENTENCE: cue and at least one A- and B-support span must share a non-empty sentence_id.
- CROSS_SENTENCE: at least one endpoint-support span must be outside the cue sentence, and every such support link requires an explanatory evidence_notes value.
- DOCUMENT_CONTEXT: requires a separate contextual span, a distinct section/paragraph locator from the cue, span-level evidence_notes, and relation-level relation_notes.
- These checks establish locator/role completeness only; human review remains responsible for semantic entailment.

## Final analysis partition

- Register: registers/analysis_partition_selection.csv.
- At most one SELECTED_FINAL row per report.
- The selected partition must resolve in report_registry, with eligible source scope, permitted local use, assessable report, and complete full-report review.
- Final rows require a role, rationale, ISO date, and sha256 plus a 64-character lowercase hex digest.
- The v0.2 selected-partition projection wrapper is implemented and covered by synthetic tests.
- The wrapper verifies a second lock over the v0.1 source/register lock, v0.2 temporal-evidence rows, and final-selection decision; it delegates to the unchanged v0.1 adapter only after both v0.2 and v0.1 validation pass.
- The selection register remains header-only; there is no selected report and no real-report projection.

## Field-level adjudication synchronization

The selected-final validator checks that `ADJUDICATED`, `AGREED`, and `DEFERRED` rows for a target field form one date-ordered append-only value history. `AGREED` and `DEFERRED` must keep `original_value` and `final_value` identical; every later history row must begin from the preceding `final_value`; and the latest value must equal the persisted target field. Same-day entries are rejected when at least one is value-changing (`ADJUDICATED`); same-day non-value-changing entries are order-independent only when they preserve the same value. Only a valid history containing an `ADJUDICATED` row satisfies `ADJUDICATED_FINAL`. This is a reconstruction proposal requiring researcher review; the missing original v0.4.2 adjudication contract was not recovered. The first history row's starting `original_value` remains a historical value that cannot be independently verified without a prior row.

Field-level adjudication may change annotation content, but not partition identity or the target register's primary record ID. Those fields are immutable through this path because changing them would invalidate record keys and dependent references. Identity corrections require a separately controlled migration.

## Report-level aggregation

- Module: analysis/report_level_aggregation.py.
- Tests: tests/test_report_level_aggregation.py.
- Documentation: docs/REPORT_LEVEL_AGGREGATION_v0.1.md.
- N_eligible is counted once per report after consistent source-scope eligibility and local-use permission decisions.
- N_assessable additionally requires a completed human full-report review, ASSESSABLE status, exact frozen-source SHA-256 and character-count verification, and no report-level decision or source-version conflict.
- Outcomes are calculated only from the selected-final partition. Passes and annotators are never summed.
- Primary report-level rates are withheld until every N_assessable report has a successful selected-final projection.
- Projection counts are summed within reports; technique-pair collision keys and SCCs are never merged across different reports.
- The report-level opportunity counter now defaults to `SHARED_RESOLVED_INCIDENT_SCOPE_v0.1`: a pair requires the nearest shared RESOLVED INCIDENT ancestor, and a primary positive relation must cite that exact scope. This rule is implemented in the v0.2 aggregator and v0.4 primary projection helper. The legacy nearest common RESOLVED non-report ancestor remains a broader-context sensitivity; it can include cross-incident pairs sharing a campaign/operation ancestor. The v0.3 explicit event-to-scope assignment is a separately reported sensitivity and is supported only for `SINGLE_ANNOTATOR_FINAL` in the initial pilot. Each sensitivity applies its own rule to both numerator and denominator. Pair-opportunity-dependent rates remain withheld unless the caller explicitly enables `approve_scope_pair_rule`; this caller flag is not proof of researcher approval.
- Raw source text is loaded from a local source directory at runtime and is never written to the result JSON.
- The blank package has no annotations or selected partitions. A blank aggregation result is structural output, not empirical zero-outcome data.

## Research-readiness boundary

The aggregator is structural and arithmetic. It does not decide semantic event identity, temporal entailment, mapping correctness, scope meaning, or reviewer independence. The current schema has no machine-verifiable annotator-type field; human ownership of annotation partitions remains a documented workflow assumption, not an automated identity check. It does not calculate IAA, prevalence confidence intervals, or ChronoCTI event-level alignment. No real annotations, human agreement results, or empirical metrics exist.

## Extended metric-contract coverage

- Per-report report-registry status/reason fields, mention states, activity-unit granularity/role/instance status and count status by granularity are included.
- Temporal relations are counted by label and basis; primary direct-positive labels/bases are broken out from non-primary and non-positive records. Optional candidate-pair labels are summarized separately.
- `A_exact` and `A_120` mapping coverage and occurrence compression per technique are reported separately.
- Per-report collision provenance, excess edge multiplicity, diagonal/distinct pair mappings, label conflicts and strict-order cycle provenance are retained without merging pair keys across reports.
- The conditional within-technique relation given same-technique opportunity is withheld until the provisional scope-pair rule is approved.
- CLI smoke testing covers JSON output from a blank bundle without emitting source text.


## RECON v0.3 explicit comparison-scope assignment sensitivity

The sibling RECON v0.3 draft adds event-level comparison-scope assignments and assignment locks. The v0.2 aggregator exposes three named scope-pair rules: nearest common resolved non-report scope (legacy sensitivity), shared resolved INCIDENT scope (working primary rule), and explicit shared event comparison-scope assignment (broader-context sensitivity). The v0.3 wrapper uses the explicit-assignment rule only after assignment and lock validation, and the initial-pilot workflow supports `SINGLE_ANNOTATOR_FINAL` only. The rule is not primary and its rate gate remains separately approval-controlled. See ../CTI_Annotation_Schema_RECON_v0.3/.
