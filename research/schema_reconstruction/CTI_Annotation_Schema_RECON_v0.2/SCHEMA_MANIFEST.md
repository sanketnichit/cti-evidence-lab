# Schema manifest — RECON v0.2 temporal evidence extension

- Version: 0.2
- Prepared: 5 November 2026
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

## Timestamp gate

- Time evidence must have timezone_status=EXPLICIT and a populated normalized_timezone.
- Normalized bounds must be timezone-aware ISO-8601 values and start must not follow end.
- Non-point intervals require uncertainty_notes.
- Retained but non-normalized timestamp candidates are rejected rather than ignored.
- Direct-timestamp evidence must preserve raw_time_text, time_precision, and explicit timezone_text.
- For direct timestamp BEFORE/AFTER, the strict order must hold for every retained A/B interval combination.

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

## Report-level aggregation

- Module: analysis/report_level_aggregation.py.
- Tests: tests/test_report_level_aggregation.py.
- Documentation: docs/REPORT_LEVEL_AGGREGATION_v0.1.md.
- N_eligible is counted once per report after consistent source-scope eligibility and local-use permission decisions.
- N_assessable additionally requires a completed human full-report review, ASSESSABLE status, exact frozen-source SHA-256 and character-count verification, and no report-level decision or source-version conflict.
- Outcomes are calculated only from the selected-final partition. Passes and annotators are never summed.
- Primary report-level rates are withheld until every N_assessable report has a successful selected-final projection.
- Projection counts are summed within reports; technique-pair collision keys and SCCs are never merged across different reports.
- Compatible event-pair opportunity currently uses the nearest common RESOLVED scope other than REPORT_AGGREGATE. This is provisional; pair-opportunity rates are withheld unless the caller explicitly approves the rule.
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
