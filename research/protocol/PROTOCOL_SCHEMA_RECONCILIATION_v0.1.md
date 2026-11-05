# Protocol v0.5 ↔ Schema RECON v0.1 reconciliation register

**Date:** 5 November 2026  
**Status:** Reconciliation finding register; not protocol approval, schema approval, or a freeze decision.  
**Compared:** `CTI_Event_Instance_Annotation_Protocol_v0.5-draft.md`, RECON v0.1 field dictionary, controlled vocabularies, data-model rules, validator, projection adapter, projection metrics and synthetic QA.

## 1. Purpose and boundary

This register checks whether each operational requirement in Protocol v0.5 has an identifiable representation in RECON v0.1: a field, a controlled value, a validator invariant, a manual procedure, or an explicit deferral.

RECON v0.1 remains a reconstruction. It is not the missing original Schema v0.4.2 and it is not approved for formal annotation. A passing synthetic validator establishes structural behavior only; it does not establish semantic correctness of a report interpretation.

## 2. Reconciliation summary

| Protocol area | RECON v0.1 coverage | Finding |
|---|---|---|
| Source identity, freeze and rights | `report_registry`, `evidence_spans`, `record_evidence_links` | Covered with a denominator correction now enforced: assessability requires the exact frozen source to be supplied and hash/character-count verified. |
| Scope hierarchy | `report_scopes`, unit `scope_id`, evidence links | Structurally covered; scope boundaries and cross-scope compatibility remain human judgments. |
| Mentions and occurrence identity | `event_mentions`, `activity_units`, evidence spans | Core representation covered. `mention_kind` remains deliberately open because the original enum was not recovered. |
| Granularity, unit roles and counts | `activity_units` | Covered structurally, including role/granularity pairings, count consistency and acyclic parent hierarchy. |
| ATT&CK mapping | `event_mappings`, mapping evidence links, pinned A_120 and v12.1 crosswalk | Partially covered. Alternative-group consistency is not validated; analyst-candidate rationale is only free text in optional `mapping_notes`. |
| Time evidence | `time_evidence` | Partially covered. Raw text and normalized bounds are represented, but ISO/timezone/precision consistency and uncertainty-invariant ordering are not fully executable. |
| Temporal relations | `temporal_relations`, evidence spans and additional evidence links | Partially covered. Evidence-scope values exist, but cue and endpoint-support roles are not sufficiently distinguished for cross-sentence/document-context evidence. |
| Episode-level exploratory relations | No dedicated register | Missing. Protocol currently asks for a separate episode-level exploratory register, but RECON has no such register. |
| Optional candidate-pair assessment | `candidate_pair_assessments` | Covered structurally. Endpoint eligibility, rule/version pinning, and reasons for all three non-positive outcomes are validated; the candidate universe itself remains a researcher-frozen rule. |
| Lock and benchmark reveal | Adapter computes and checks a partition lock digest | Partially covered. A specific partition can be verified, but no durable register designates the final analysis partition when multiple passes/annotators exist or records the reveal event. |
| Projection and cycle diagnostics | Projection adapter and `projection_metrics_recon.py` | Core event-edge projection, omission, collision and cycle-provenance logic is represented and synthetically tested. |
| Full metric contract | Per-report edge projection metrics | Partially implemented. Same-technique pair opportunity, per-technique occurrence compression, and cross-report report-level aggregation are not implemented in this module. |
| ChronoCTI baseline alignment | No alignment register in RECON | Missing from the annotation package. Protocol requires an explicit alignment outcome after candidate review. |

## 3. Findings requiring implementation or a design decision

### 3.1 Source integrity and `N_assessable` — corrected

The previous validator counted a report as assessable from status fields even when its exact source text was not supplied to the validation call. This did not enforce Protocol Section 7.1's complete/readable frozen-source requirement.

The validator now excludes such a partition from `N_assessable` until its exact source text is supplied and the frozen hash and character count are checked. It emits `ASSESSABLE_SOURCE_NOT_VERIFIED` as a warning. A report with zero event leaves remains assessable when the complete source is verified and the full review is complete.

**Implementation:** RECON validator, data-model rules, QA record, manifest and checksum list.  
**Regression coverage:** source missing → excluded from assessable denominator; source supplied and matching → included.  
**Verification:** 69 RECON v0.1 synthetic tests pass (41 validator, 16 projection, 12 adapter); 31/31 package checksums match. CI run #125 also passed 70 RECON v0.2 tests and 55 root tests (194 successful test executions total). These remain synthetic checks, not report findings.

### 3.2 Temporal evidence roles — partial representation

Protocol Section 4.3 requires evidence that connects the relation cue to both event arguments. It explicitly names `cue_text` and `argument_support`; Sections 4.3 and Pass 5 also require every sentence/passage needed for cross-sentence and document-context support.

RECON has one primary evidence span plus additional spans in `record_evidence_links`, but the current `evidence_role` vocabulary uses only broad values such as `TEMPORAL_RELATION`. It cannot reliably distinguish a cue span from Event A support, Event B support, or wider context. A single span can still support a sentence-level relation, but the schema does not structurally enforce the multi-span evidence requirements for `CROSS_SENTENCE` and `DOCUMENT_CONTEXT`.

**Proposed repair:** retain the canonical evidence-span/link architecture, add precise temporal evidence-link roles (at minimum relation cue, Event A argument support, Event B argument support, and relation context), and document when multiple spans are mandatory. Avoid duplicating raw source text into free-text cue fields when exact evidence spans already preserve it. The protocol's `cue_text` and `argument_support` wording should then be reconciled to this evidence-link representation.

### 3.3 Episode-level exploratory relations — unresolved scope decision

Protocol Pass 5 says episode-to-episode relations may be retained in a separate exploratory register and must not be pooled with atomic event-instance edges. RECON has only the atomic-positive `temporal_relations` register and a non-temporal relation register. The atomic validator correctly rejects containers as primary positive endpoints, but there is no separate place to store episode-level temporal observations.

**Decision needed before freeze:** either (a) add a separate episode-temporal register with explicitly non-primary status and its own tests, or (b) narrow the initial pilot protocol to defer episode-level temporal annotation and retain only a note that such a relation was observed. Do not place episode relations in `temporal_relations` and weaken the atomic event gate.

### 3.4 Alternative mapping constraints — incomplete executable gate

The validator now requires an `alternative_group_id` for `ALTERNATIVE` rows, at least two mapping rows per group, one activity unit per group, and any `alternative_to_mapping_id` to resolve within the same group and activity unit. The projection function continues to exclude non-`ACCEPTED` rows. The validator does not decide whether alternatives are semantically mutually exclusive or resolve a group on behalf of the annotator; those remain human mapping decisions. The protocol/schema owner must still specify how a group is marked resolved and whether an `ACCEPTED` row may retain the former group ID after resolution.

**Proposed repair:** require group membership for alternative rows; validate group membership and target consistency; prevent an unresolved alternative group from contributing an accepted mapping. Preserve multiple independently supported accepted techniques as separate accepted rows without an alternative group.

### 3.5 Analyst-candidate mapping rationale — corrected

The validator now requires non-empty `mapping_notes` for every accepted `source_supported_analyst_candidate` mapping. Accepted source-supported mappings also require a mapping-specific evidence link. This records the human rationale without duplicating the exact source span in another free-text field. The structural gate cannot decide whether the proposed technique is semantically appropriate; that remains the annotator's responsibility.

### 3.6 Candidate-pair assessment reason — corrected

The validator now requires a non-empty `assessment_reason` for each of `NO_TEMPORAL_CLAIM`, `VAGUE_OR_AMBIGUOUS`, and `NOT_ASSESSABLE`. An unassessed pair still receives no assessment row and is not treated as a negative.

### 3.7 Final analysis partition designation — incomplete

The adapter accepts one exact report/annotator/pass partition and verifies a computed lock reference. This protects the specific input that is projected. Protocol Section 7.1 additionally requires report-level outcomes to use a designated locked final annotation or an agreed/adjudicated consensus partition when multiple annotators or passes exist.

The present report registry has no field that designates a partition's analysis role, and the package has no report-level selection manifest. The validator can count eligible/assessable reports after decision conflicts are resolved, but it does not establish which annotation partition is the final analytic record.

**Proposed repair:** add a minimal report-partition designation mechanism before multi-pass or multi-annotator data are analysed. It must distinguish development/repeat/independent/consensus/adjudicated-final partitions and ensure at most one selected final analysis partition per report. Do not sum per-partition edges or events to create report-level outcomes.

### 3.8 Baseline pair alignment — missing from schema

Protocol Section 6.3 requires explicit alignment labels (`supported`, `multiple_candidate_pairs`, `ambiguous`, `unmapped`, `not_assessable`) after the event-level candidate set is reviewed. RECON has no dedicated baseline pair/alignment register. These labels should not be forced into `event_mappings` or `candidate_pair_assessments`; they describe correspondence between a benchmark technique-pair item and one or more report-local event pairs.

**Proposed repair:** decide whether baseline alignment is in scope for the initial five-report feasibility pilot. If it is, add a separate register with raw benchmark IDs/labels, candidate event-pair references, alignment status, and evidence/rationale. Keep raw `NEXT` provenance and any normalization hypothesis separate. Otherwise defer alignment metrics and amend the protocol accordingly.

### 3.9 Metric coverage — per-report core implemented, report-level analyses incomplete

The current projection module implements the edge-to-pair projection, diagonal/full/partial/unmapped edge outcomes, distinct-pair collisions, label conflicts, source-graph cycle checks, and provenance of projected cycles.

The protocol's metric list also includes:
- same-technique pair-opportunity rate across all distinct compatible event-leaf pairs, whether or not a temporal relation exists;
- occurrence compression / event-leaf count per technique;
- report-level numerator/denominator aggregation across `N_assessable`.

Those are not currently emitted by the projection module. The first is not an edge-projection metric and needs a separately defined event-pair universe. The second needs per-technique event counts. The third needs the selected final partition rule above.

**Proposed repair:** define the pair universe and aggregation rules in the metric contract before implementation. Keep this work separate from the annotation validator and do not report rates until real locked partitions exist.

### 3.10 Time normalization — partial executable validation

RECON retains raw expression, type, precision, timezone text/status, normalized start/end/timezone, normalization status and uncertainty notes. Direct-timestamp relations require normalized, evidence-linked times at both endpoints.

The validator currently checks field presence and linkability, but does not fully validate timestamp syntax, precision/timezone consistency, or whether the relation label is invariant across the recorded uncertainty intervals. Those semantic/interval checks need a more explicit manual rule or a tested normalization utility before direct-timestamp edges are used in the primary graph.

## 4. Requirements already represented

The following protocol concepts have a clear representation and synthetic structural checks:

- report, annotator and pass partitioning;
- source text hash, exact half-open offsets and optional source-text verification;
- report-local scope hierarchy and acyclic unit-parent hierarchy;
- mention status separate from activity-unit status;
- atomic leaves versus series/episode/aggregate containers;
- count-status consistency and non-negative bounds;
- pinned ATT&CK v12.1 exact-to-parent crosswalk and A_120 membership;
- accepted mapping evidence, mapping-level ATT&CK release and lifecycle checks; accepted analyst-candidate rationale; alternative-group structure; accepted analyst-candidate rationale and mapping evidence; alternative-group structure;
- direct timestamp evidence on both endpoints;
- distinct, scope-compatible primary temporal endpoints;
- separate non-temporal relations;
- versioned candidate-pair rules and endpoint eligibility;
- duplicate/contradictory pair claims;
- partition-specific lock verification in the projection adapter;
- projection outcome distinctions, collision provenance and strict-order cycle diagnostics.

Structural checks do not decide source semantics. Human review must still decide event identity, scope, whether a mapping fits, whether a temporal cue relates the two endpoints, and whether a timestamp supports the proposed ordering.

## 5. Recommended resolution order

1. Close remaining validator-level omissions: require rationale for accepted analyst-candidate mappings and specify how a resolved versus unresolved alternative group is represented. Alternative-group structure and non-positive pair reasons are now validated.
2. Decide whether episode-level relations and baseline pair alignment are included in the initial pilot. Add dedicated registers only if they are genuinely in scope; otherwise narrow the protocol before freeze.
3. Add multi-partition final-analysis designation before any repeated-pass or second-annotator results are aggregated.
4. Finalize the temporal evidence-link roles and requirements for sentence, cross-sentence and document-context support.
5. Complete the metric contract for pair opportunity, occurrence compression and cross-report aggregation.
6. Reconcile timestamp normalization and uncertainty rules.
7. Issue a new schema version, tests, manifest and checksum list; perform a clean CI run; then obtain explicit researcher approval before annotation.

## 6. Current research boundary

- Five rank-one AnnoCTR reports remain candidates; formal researcher eligibility decisions: 0/5.
- Human-locked report annotations: 0.
- Real-report projections: 0.
- Independent human agreement: not measured.
- Novelty: not established.
- The 69-test RECON v0.1 suite is synthetic only (41 validator, 16 projection, 12 adapter). The separate RECON v0.2 suite has 70 synthetic tests. CI run #125 passed 194 total root/v0.1/v0.2 test executions. These do not validate semantic annotation or prove the research question's empirical contribution.

**Freeze decision:** not ready. RECON v0.1 is useful and increasingly testable, but the gaps above must be resolved or explicitly deferred in the protocol before a new schema version can be approved.


## RECON v0.2 selected-analysis gate addendum — 5 November 2026

The v0.2 extension now provides a durable `analysis_partition_selection` register and selected-final adapter gate. A selected-final partition is blocked when report-level eligibility, local-use or assessability decisions conflict across any registered annotator/pass partitions. A `CONSENSUS` selection requires two distinct completed `INDEPENDENT` input partitions recorded as not themselves selected-final. An `ADJUDICATED_FINAL` selection requires an `ADJUDICATED` log row whose target register and record ID resolve to an actual record in the selected report/annotator/pass partition.

The v0.1 standalone adapter also blocks report-level eligibility/local-use/assessability conflicts, rather than allowing a warning from the parent validator to be bypassed by a direct projection call. These controls are structurally tested only; they do not authenticate annotator identity, prove semantic agreement, or replace human adjudication.

The RECON v0.1 projection metric now distinguishes cycle components that contain multiple source event edges from those that require multiple source event edges. The legacy root projector rejects self-event edges. CI run #125 passed after refreshing the 31-entry v0.1 package checksum manifest.
