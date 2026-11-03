# CTI Annotation Schema v0.4.2-draft — Conformance Audit v0.1

**Audit date:** 3 November 2026  
**Compared against:** `CTI_Event_Instance_Annotation_Protocol_v0.4.1-draft.md`, schema package v0.4.2-draft, and current public GitHub v0.3 templates/validator.  
**Status:** Structural design review only. No schema or protocol has been approved or frozen. This audit does not create annotations or decide report eligibility.

## Executive result

Schema v0.4.2 is a meaningful improvement over the public v0.3 templates. It contains all eight minimum registers named by protocol v0.4.1 and adds useful supporting registers for evidence spans/links, non-temporal relations, and adjudication. Its SHA256 manifest verifies, the ZIP passes integrity testing, and its CSV headers are readable.

It is **not yet ready for human annotation**. It is a blank schema proposal with no matching v0.4.2 validator, no validator tests, several missing explicit fields, and cross-register rules that remain in prose rather than enforceable constraints.

The right decision is: **keep v0.4.2 as a draft; do not call it a completed migration and do not start entering the five reports into it yet.**

## 1. What passes the protocol crosswalk

| Protocol v0.4.1 requirement | v0.4.2 register/fields | Assessment |
|---|---|---|
| Report/source identity, frozen text hash, rights and assessability | `report_registry.csv` | Present: source URL/path, dates, text SHA256/character count, extraction/transformation, corpus/split, local/public rights, source-scope eligibility, exposure and report assessability. |
| Report-local scopes and parent scopes | `report_scopes.csv` | Present; evidence can be attached through the evidence-link register. |
| Event/series/episode/aggregate units, hierarchy and counts | `activity_units.csv` | Present: scope, parent, granularity, unit role, instance status, count status/bounds, confidence and adjudication. |
| Exact text mentions and mention-to-unit identity | `event_mentions.csv` + `evidence_spans.csv` | Present: mention span, sentence locator, mention kind, activity-unit link, status and resolved event ID. |
| Exact ATT&CK mappings, evidence and alternatives | `event_mappings.csv` + evidence links | Present: exact ID/version, mapping basis, decision status, alternatives and evidence links. |
| Baseline-compatible parent mapping `A_120` separate from `A_exact` | `event_mappings.csv` | Present: baseline vocabulary ID/hash, baseline parent ID and baseline status. |
| Typed times with raw evidence and justified normalization | `time_evidence.csv` + `evidence_spans.csv` | Present: type, precision, timezone, normalized interval/status and uncertainty. |
| Temporal relation labels, basis, endpoint and scope compatibility | `temporal_relations.csv` | Mostly present: distinct endpoint fields, relation basis, comparison scope, scope compatibility, confidence and adjudication. Evidence can be linked. |
| Optional, rule-generated pair assessments | `candidate_pair_assessments.csv` | Present: candidate rule ID/version, pair IDs, assessment label, relation link and reason. |
| Separate causal/dependency/narrative relations | `non_temporal_relations.csv` | Present as a separate register; these rows should never enter the temporal projection input. |
| Disagreement and adjudication history | `adjudication_log.csv` | Added and useful; preserves original values and a final decision rather than silently overwriting. |

The package is internally intact: all 15 entries in `SHA256SUMS.txt` match, and `unzip -t` reports no ZIP errors.

## 2. Changes required before schema freeze

### P0 — fields and semantics that affect the primary evidence model

1. **Add explicit temporal evidence scope.** Protocol v0.4.1 requires `evidence_scope` with `SENTENCE`, `CROSS_SENTENCE`, or `DOCUMENT_CONTEXT`. The v0.4.2 `temporal_relations.csv` has relation basis and scope compatibility but no `evidence_scope` field. Sentence IDs on linked spans may help derive it, but they do not explicitly represent document-context evidence. Add `evidence_scope` to the temporal-relation record (and, if useful, pair assessments), or specify a fully deterministic equivalent.
2. **Freeze the annotation/version identity.** `report_registry.csv` has report and annotator IDs, but does not store `protocol_version`, `schema_version`, or `annotation_pass_id/date`. Add them, or define a mandatory immutable per-file manifest with those values. This matters when the same report is annotated again after a washout period or protocol revision.
3. **Make evidence-link rows uniquely identifiable.** `record_evidence_links.csv` has no `link_id`. Either add one or formally define and validate a composite key such as `(report_id, annotator_id, record_type, record_id, evidence_span_id, evidence_role)`, with an explicit duplicate policy.
4. **Freeze the cross-register identity constraints.** The field dictionary says the event ID equals the activity-unit ID for a resolved event leaf, but the validator must check this. It must also enforce the primary graph rule: both endpoints are distinct, resolved, atomic `event_leaf` units in a compatible comparison scope.
5. **Freeze unit-role/granularity/status combinations.** At minimum, `event_leaf` must be `atomic_event` + `RESOLVED`; container roles must not become event IDs or primary graph endpoints. Decide whether each container role must match one specific granularity and whether `unresolved_unit` requires `UNRESOLVED`.
6. **Define the authoritative mention/unit status relationship.** `instance_status` appears in both `event_mentions.csv` and `activity_units.csv`. This can be useful because mention-level resolution and unit-level resolution are not always identical, but the protocol must say which register is authoritative for event-graph eligibility and what mismatches are valid.
7. **Define positive temporal relation eligibility as an executable rule.** A primary relation must have (a) distinct event-leaf endpoints, (b) `atomic_event` granularity, (c) `RESOLVED` status, (d) compatible scope with a recorded comparison scope, and (e) `relation_basis` `direct_source` or `direct_timestamp`. Everything else remains candidate, unresolved, inferred, transitive, or exploratory and is excluded from the primary graph.
8. **Bundle or immutably reference the selected-120 baseline vocabulary.** `event_mappings.csv` has a vocabulary ID and SHA256, which is good, but the schema ZIP itself does not include the actual selected-120 ID list. Include the pinned file or specify the exact immutable artifact path/version so `IN_VOCAB` can be checked rather than trusted as free text.

### P1 — consistency and analysis-quality safeguards

9. **Clarify evidence-link versus direct-span handling.** `event_mentions.csv` and `time_evidence.csv` each have a direct `evidence_span_id`, while most other registers use `record_evidence_links.csv`. State that the direct ID is the primary span and that evidence links are for additional spans, or standardize the design. Do not allow two competing ways to attach the same evidence without a duplication rule.
10. **Freeze `record_type` and `evidence_role` enums.** The README gives examples, but the field dictionary should list the full allowed values, including whether report-level eligibility evidence may link to `report_registry` records.
11. **Give candidate-pair assessments a scope rule.** The current table records endpoints and a candidate-generation rule but not `comparison_scope_id` or explicit scope compatibility. Either add those fields or define that the candidate-pair generator can emit only same-scope event-leaf pairs and validate that invariant from `activity_units.csv`.
12. **Clarify non-temporal endpoint granularity.** `non_temporal_relations.csv` uses `event_a_id`/`event_b_id`. Decide whether these relations may connect containers/episodes as well as event leaves. If yes, use `activity_unit_a_id`/`activity_unit_b_id`; if no, document and validate the restriction.
13. **Clarify mapping status/basis combinations.** Keep `workbook_only` mappings non-accepted and out of `A_exact`/`A_120`; only `ACCEPTED` and source-supported mapping decisions should enter the primary projection. Validate alternative links and baseline-parent membership.
14. **Clarify raw versus normalized time.** Retain the source string and precision even when a normalized interval is available. A timezone-uncertain timestamp may support a relation only when the ordering is invariant to that uncertainty; freeze this decision before annotation.
15. **Specify namespace and collision rules.** IDs should be unique within `(report_id, annotator_id, register/type)`; references must resolve within the same report and annotator unless a documented adjudication record intentionally links two annotators' values.

## 3. The validator migration is still missing

The current GitHub validator is v0.3-era. It filters by report ID but does not partition mixed rows by annotator, and it cannot enforce v0.4.2 scopes, activity-unit hierarchy, evidence-link integrity, time typing, accepted/alternative mapping logic, baseline vocabulary membership, or endpoint scope/granularity.

Before formal annotation, implement a validator that:

- loads the full register set and a frozen source text;
- checks exact half-open text offsets and SHA256;
- checks unique IDs, foreign keys and annotator/report partitioning;
- validates unit-role/granularity/status combinations and parent hierarchy;
- validates `event_instance_id == activity_unit_id` for resolved event leaves;
- checks accepted mapping records and `A_120` vocabulary membership;
- validates temporal evidence scope, endpoint distinctness, leaf/atomic/resolved status, comparison-scope compatibility and relation basis;
- keeps pair assessments distinct from positive temporal edges;
- excludes non-temporal relations, inferred/transitive relations and container endpoints from the primary graph;
- emits report-level assessability and annotation coverage without treating missing rows as negatives.

Add synthetic tests for the valid path and each invalid invariant before using it on the five reports. The validator should not make semantic judgments about whether the source text truly supports an event identity or relation; it enforces that the required human decisions and evidence links are present and internally consistent.

## 4. Recommended order

1. Researcher reviews and approves protocol v0.4.1 (or a revised protocol) and the exact schema changes.
2. Freeze the register headers, enums, key constraints, and selected-120 vocabulary reference.
3. Implement the v0.4.2 validator with synthetic positive/negative tests.
4. Dry-run the schema and validator only on synthetic records and on the already AI-exposed development cases, clearly labelled as such.
5. Only then begin source-first annotation of the five AnnoCTR candidates. AI-proposed content stays separate from human labels.

## 5. What this audit does not decide

- It does not approve v0.4.1 or v0.4.2.
- It does not establish report eligibility, local-use permission, or public-reuse rights for any candidate.
- It does not select any report or replace any rank-1 candidate.
- It does not create human annotations, event IDs, mappings, or temporal edges.
- It does not validate the semantic correctness of any existing AI source review or worked annotation.

**Bottom line:** v0.4.2 is a good structural draft and is much closer to the protocol than the public v0.3 templates. It still needs explicit evidence-scope/version/key constraints and a tested cross-register validator. The five AnnoCTR reports should remain unannotated in the new schema until those gates are completed.