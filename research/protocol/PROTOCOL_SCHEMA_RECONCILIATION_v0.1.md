# Protocol v0.5 ↔ Schema RECON v0.1 reconciliation register

**Updated:** 8 November 2026  
**Status:** Reconciliation finding register; not protocol approval, schema approval, or a freeze decision.  
**Compared:** `CTI_Event_Instance_Annotation_Protocol_v0.5-draft.md`, RECON v0.1 field dictionary, controlled vocabularies, data-model rules, validator, projection adapter, projection metrics and synthetic QA.

## 1. Purpose and boundary

This register checks whether each operational requirement in Protocol v0.5 has an identifiable representation in RECON v0.1: a field, a controlled value, a validator invariant, a manual procedure, or an explicit deferral.

RECON v0.1 remains a reconstruction. It is not the missing original Schema v0.4.2 and it is not approved for formal annotation. A passing synthetic validator establishes structural behavior only; it does not establish semantic correctness of a report interpretation.

## 2. Reconciliation summary

| Protocol area | RECON v0.1 coverage | Finding |
|---|---|---|
| Source identity, freeze and rights | `report_registry`, `evidence_spans`, `record_evidence_links` | Covered with a denominator correction now enforced: assessability requires the exact frozen source to be supplied and hash/character-count verified. |
| Scope hierarchy and pair comparability | `report_scopes`, unit `scope_id`, evidence links; v0.2 aggregator; v0.3 assignment extension | The hierarchy is structurally covered. The adopted working primary rule is the nearest shared RESOLVED INCIDENT ancestor, and a primary relation must cite that exact scope. Legacy broad-ancestor and explicit-assignment rules remain separate sensitivities. v0.2/v0.4 defaults and numerator/denominator filters are implemented; final protocol/schema approval remains open. |
| Mentions and occurrence identity | `event_mentions`, `activity_units`, evidence spans | Core representation covered. `mention_kind` remains deliberately open because the original enum was not recovered. |
| Granularity, unit roles and counts | `activity_units` | Covered structurally, including role/granularity pairings, count consistency and acyclic parent hierarchy. |
| Event-universe stratum | RECON v0.4 `activity_unit_strata.csv` one-to-one extension, validator, lock and primary projection filter | Implemented as a draft additive layer without mutating the checksum-controlled v0.1 `activity_units.csv`: every activity unit has exactly one evidence-backed stratum row; selected-final stratum decisions are bound to the v0.2 lock; only ATTACK_ACTION leaves, mappings, edges and pair opportunities enter primary projection. Auxiliary and mixed rows remain visible separately. Thirteen synthetic tests pass; researcher review and protocol/schema freeze remain open. |
| ATT&CK mapping | `event_mappings`, mapping evidence links, pinned A_120 and v12.1 crosswalk | Core structural gates are covered: accepted analyst candidates require rationale/evidence, accepted IDs and parents are checked against v12.1, and alternative groups are checked for membership/target consistency. Human semantic fit and alternative-group resolution remain open. |
| Time evidence | `time_evidence` plus v0.2 temporal-evidence validator | Structural validation now checks aware ISO-8601 bounds, precision/timezone fields, uncertainty notes, retained normalized candidates and invariant strict `BEFORE`/`AFTER` ordering. Timezone equivalence and non-strict label derivation remain semantic/manual boundaries. |
| Temporal relations | v0.1: `temporal_relations`, evidence spans and generic evidence links; v0.2: `temporal_relation_evidence.csv` | v0.1 alone remains partial. The additive v0.2 extension now distinguishes relation cue, Event A support, Event B support and context, with structural scope checks; Protocol v0.5 Section 4.3 now reflects that representation. |
| Episode-level exploratory relations | No dedicated register in v0.1/v0.2 | Protocol v0.5 now proposes deferring episode-to-episode relation records from the initial pilot. This avoids a missing-register mismatch if the researcher approves the deferral; otherwise a separate register is still required. |
| Optional candidate-pair assessment | `candidate_pair_assessments` | Covered structurally. Endpoint eligibility, rule/version pinning, and reasons for all three non-positive outcomes are validated; the candidate universe itself remains a researcher-frozen rule. |
| Lock and benchmark reveal | v0.1 partition lock; v0.2 `analysis_partition_selection` and selected-final wrapper; v0.3 scope-assignment lock | Final analysis partition designation, selection lock and explicit-scope assignment lock are structurally implemented and synthetically tested. The digest is a mutation detector, not an identity signature; annotator identity and benchmark reveal remain human workflow controls. |
| Projection and cycle diagnostics | Projection adapter and `projection_metrics_recon.py` | Core event-edge projection, omission, collision and cycle-provenance logic is represented and synthetically tested. |
| Full metric contract | v0.1 per-report projection metrics; v0.2 `report_level_aggregation.py`; v0.4 attack-action adapter | The v0.1 module does not perform batch aggregation. The v0.2 aggregator defaults to the nearest shared RESOLVED INCIDENT rule and applies it to both opportunity denominator and positive-relation numerator; v0.4 filters the pair universe to ATTACK_ACTION leaves. Rates remain withheld until full protocol/schema approval and reviewed locked data. |
| ChronoCTI baseline alignment | No alignment register in RECON v0.1/v0.2 | Protocol v0.5 proposes deferring record-level benchmark-pair-to-event-pair alignment from the initial pilot. This deferral requires researcher approval; if rejected, a dedicated register and separate validation are needed. |

## 3. Findings requiring implementation or a design decision

### 3.1 Source integrity and `N_assessable` — corrected

The previous validator counted a report as assessable from status fields even when its exact source text was not supplied to the validation call. This did not enforce Protocol Section 7.1's complete/readable frozen-source requirement.

The validator now excludes such a partition from `N_assessable` until its exact source text is supplied and the frozen hash and character count are checked. It emits `ASSESSABLE_SOURCE_NOT_VERIFIED` as a warning. A report with zero event leaves remains assessable when the complete source is verified and the full review is complete.

**Implementation:** RECON validator, data-model rules, QA record, manifest and checksum list.  
**Regression coverage:** source missing → excluded from assessable denominator; source supplied and matching → included.  
**Verification:** 69 RECON v0.1 synthetic tests pass (41 validator, 16 projection, 12 adapter); 31/31 package checksums match. CI run #144 also passed 72 RECON v0.2 tests and 57 root tests (198 successful test executions total). These remain synthetic checks, not report findings.

### 3.2 Temporal evidence roles — v0.1 gap, v0.2 extension implemented

RECON v0.1 has a primary relation evidence span and generic `record_evidence_links`, but its broad `TEMPORAL_RELATION` role cannot reliably distinguish a relation cue from Event A support, Event B support, or wider context. The v0.1 package alone also does not enforce the multi-span requirements for cross-sentence/document-context evidence.

The additive RECON v0.2 extension supplies `temporal_relation_evidence.csv` with `EVENT_A_SUPPORT`, `EVENT_B_SUPPORT`, and `RELATION_CONTEXT` roles. The relation's `primary_evidence_span_id` is the `RELATION_CUE`; exact source text and offsets remain stored once in `evidence_spans`. The extension validator checks endpoint alignment and the structural locator/note requirements for `SENTENCE`, `CROSS_SENTENCE`, and `DOCUMENT_CONTEXT`. Protocol v0.5-draft Section 4.3 has now been reconciled to this representation and no longer requires duplicate `cue_text` or `argument_support` fields.

These checks establish traceability and structural completeness only. They do not establish semantic entailment. The v0.2 extension remains a draft and requires researcher approval before annotation.

### 3.3 Episode-level exploratory relations — proposed initial-pilot deferral

RECON v0.1 and v0.2 have no dedicated episode-to-episode temporal relation register. Their primary temporal relation path is for distinct resolved atomic event leaves; containers are not primary graph endpoints.

Protocol v0.5-draft now proposes deferring episode-to-episode relation records from the initial pilot while retaining episode containers and any supported unit/time evidence. This is the recommended way to keep the initial schema bounded without weakening the atomic event gate. The deferral is not yet an adopted researcher decision: explicit approval is required before freeze. If episode-edge analysis is retained instead, it needs a separately versioned register and distinct tests; do not place episode edges in `temporal_relations`.

### 3.4 Alternative mapping groups — structural gate implemented; resolution semantics open

The validator requires an `alternative_group_id` for `ALTERNATIVE` rows, at least two mapping rows per group, one activity unit per group, and any `alternative_to_mapping_id` to resolve within the same group and activity unit. The projection path excludes every non-`ACCEPTED` row. These structural rules are tested.

The remaining issue is not the existence of group checks: the protocol/schema still needs an explicit lifecycle for a group after human adjudication. It must state how the group is marked resolved, whether one alternative is promoted to `ACCEPTED`, how rejected alternatives remain traceable, and whether a promoted row retains or clears the former group ID. The validator cannot decide whether two candidate mappings are genuinely mutually exclusive. Independently supported multiple techniques remain separate `ACCEPTED` rows, not one alternative group. Do not change the schema until this decision is specified.

### 3.5 Analyst-candidate mapping rationale — corrected

The validator now requires non-empty `mapping_notes` for every accepted `source_supported_analyst_candidate` mapping. Accepted source-supported mappings also require a mapping-specific evidence link. This records the human rationale without duplicating the exact source span in another free-text field. The structural gate cannot decide whether the proposed technique is semantically appropriate; that remains the annotator's responsibility.

### 3.6 Candidate-pair assessment reason — corrected

The validator now requires a non-empty `assessment_reason` for each of `NO_TEMPORAL_CLAIM`, `VAGUE_OR_AMBIGUOUS`, and `NOT_ASSESSABLE`. An unassessed pair still receives no assessment row and is not treated as a negative.

### 3.7 Final analysis partition designation — implemented in v0.2; v0.3 final-role boundary remains

RECON v0.2 adds `analysis_partition_selection`, a selected-final adapter and a lock that binds the selected partition to the source/annotation lock, temporal-evidence rows and selection decision. The validator enforces at most one selected-final partition per report. `CONSENSUS` requires two distinct completed independent input partitions; `ADJUDICATED_FINAL` requires an adjudication record that resolves to a record in the selected partition. Report-level aggregation consumes only the selected final partition and does not sum annotator/pass partitions.

RECON v0.3's separate explicit-scope assignment lock currently supports `SINGLE_ANNOTATOR_FINAL` only: consensus/adjudicated final roles are blocked because the v0.1 adjudication log cannot target v0.3 assignment rows. This is the remaining multi-annotator limitation if the explicit-assignment scope rule is selected. A dedicated scope-assignment adjudication mechanism or a clearly bounded single-annotator pilot is needed before using v0.3 assignments with multiple annotators. All lock behavior remains structural and does not authenticate annotator identity or prove agreement.

### 3.8 Baseline pair alignment — proposed initial-pilot deferral

Protocol v0.5-draft previously required explicit alignment labels (`supported`, `multiple_candidate_pairs`, `ambiguous`, `unmapped`, `not_assessable`) after the event-level candidate set was reviewed. RECON v0.1/v0.2 has no dedicated register for correspondence between benchmark technique-pair items and report-local event pairs. Those labels must not be forced into `event_mappings` or `candidate_pair_assessments`.

Protocol v0.5-draft Section 6.3 now proposes deferring record-level ChronoCTI pair-to-event alignment from the initial pilot. Preserve raw benchmark pair IDs, labels, and provenance in the separate baseline reproduction materials. The proposed deferral requires researcher approval. If alignment is later brought into scope, add a dedicated register, candidate-generation rules, evidence requirements, and separate validation; do not treat benchmark edges as source evidence.

### 3.9 Metric coverage — per-report core implemented, report-level analyses incomplete

The current projection module implements the edge-to-pair projection, diagonal/full/partial/unmapped edge outcomes, distinct-pair collisions, label conflicts, source-graph cycle checks, and provenance of projected cycles.

The protocol's metric list also includes:
- same-technique pair-opportunity rate across all distinct compatible event-leaf pairs, whether or not a temporal relation exists;
- occurrence compression / event-leaf count per technique;
- report-level numerator/denominator aggregation across `N_assessable`.

The projection module itself is not the report-level aggregator. RECON v0.2 now supplies `analysis/report_level_aggregation.py` with synthetic coverage for report eligibility/assessability, selected-final projection outcomes, occurrence compression and per-report projection diagnostics. Pair-opportunity-dependent rates remain withheld until the provisional scope-pair opportunity rule is explicitly approved. The aggregator does not decide source semantics or scope compatibility.

**Proposed repair:** define the pair universe and aggregation rules in the metric contract before implementation. Keep this work separate from the annotation validator and do not report rates until real locked partitions exist.

### 3.10 Time normalization — strict-order structural checks implemented; temporal semantics remain open

RECON retains raw expression, type, precision, timezone text/status, normalized start/end/timezone, normalization status and uncertainty notes. The v0.2 temporal-evidence validator requires timezone-aware ISO-8601 bounds, supported precision and timezone metadata, valid interval direction, uncertainty notes for non-point intervals, and evidence links for both endpoints. It rejects retained timestamp candidates that remain unnormalized and checks that strict `BEFORE`/`AFTER` ordering is invariant across all retained endpoint-interval combinations.

The remaining boundaries are semantic: the validator does not prove that a publisher timezone label was correctly converted across daylight-saving/ambiguous abbreviations, or that a timestamp denotes the attack occurrence rather than publication/detection/analysis time. It does not mechanically derive `OVERLAP`, `SIMULTANEOUS` or `CONCURRENT_UNSPECIFIED` from interval overlap. Those labels need a researcher-approved rule and human source review; do not infer them from broad or overlapping uncertainty intervals.

### 3.11 Event-universe stratum — draft implementation in RECON v0.4

The working research-design decision adopted on 8 November 2026 defines incident-linked attack-action occurrences as the primary ChronoCTI-comparable stratum. The decision is medium-neutral: concrete phishing delivery, induced user execution, exploitation, persistence, command and control, collection, exfiltration, impact, and incident-linked operational extortion may qualify. Public commentary/platform events, analyst/sample observations, generic capabilities, and other non-primary activity remain visible in separate descriptive strata.

The reconstructed v0.1 activity_units register has granularity, unit_role, and instance_status, but cannot distinguish an operational attack-action occurrence from a resolved communication or analyst-observation occurrence. RECON v0.4 supplies the logical activity_unit.activity_stratum field in the one-to-one activity_unit_strata.csv companion register. This is a deliberate additive extension: it preserves the v0.1 header and checksum contract rather than changing the reconstructed ancestor in place. Every activity unit must receive exactly one stratum decision with an evidence span and rationale.

The v0.4 validator enforces complete one-to-one coverage, controlled values/bases, same-partition evidence references, and the rule that a generic capability without a resolved execution cannot be a resolved atomic event leaf. The v0.4 lock binds stratum rows to the v0.2 selected-analysis lock reference. The primary projection helper selects only ATTACK_ACTION event leaves, their accepted A_120 mappings, their direct positive scope-compatible relations, and their pair-opportunity universe. Same-stratum auxiliary and mixed-stratum relations remain visible in separate diagnostics but cannot enter the primary graph. Classification remains independent of ATT&CK mapping.

Draft implementation: research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/. The pre-annotation CSV's analysis_stratum_candidate column remains triage metadata only; no individual candidate classification is approved. Thirteen synthetic tests passed in GitHub Actions run #226, including auxiliary/mixed edge exclusion, non-primary mapping exclusion, complete classification, and post-lock mutation rejection. These are structural checks only. Formal annotation remains blocked until the v0.4 layer is reviewed with the other protocol decisions and the complete package is approved/frozen.

### 3.12 Comparison-scope rule — incident-bounded primary default

ChronoCTI frames its input as a textual description of an attack incident and selects reports that narrate cyberattack incidents step-by-step (Rahman et al., 2025, Sections 1 and 4.4.2, https://doi.org/10.1007/s10115-025-02491-6). The broad nearest-common-resolved-non-report-ancestor rule can count two distinct INCIDENT nodes merely because they share a campaign, operation, organisation, host or OTHER ancestor. That is too broad for the primary ChronoCTI-comparable estimand.

**Adopted working primary rule:** use the nearest shared `scope_type=INCIDENT`, `scope_status=RESOLVED` ancestor. Count each event pair once. The primary positive-relation numerator must cite that exact nearest shared INCIDENT scope in `comparison_scope_id`. A relation recorded only at a broader ancestor is retained but not counted as a primary edge. If no defensible resolved INCIDENT scope exists, do not create one from broader co-membership; the report remains assessable, but those events do not create primary pair opportunity.

The v0.2 aggregator now defaults to `SHARED_RESOLVED_INCIDENT_SCOPE_v0.1`, selects the nearest shared resolved INCIDENT, and filters the positive-relation numerator to the same exact scope. The v0.4 attack-action projection helper uses the same default and excludes scope-ineligible edges from primary projection while returning their IDs as diagnostics. The legacy nearest common non-report ancestor and the v0.3 explicit-assignment rule remain separate sensitivities and must recompute both numerator and denominator under their own rule. Synthetic regression coverage protects cross-incident campaign exclusion and exact nearest-incident relation scope.

**Source:** Rahman et al., *Mining temporal attack patterns from cyberthreat intelligence reports*, Knowledge and Information Systems (2025), Sections 1 and 4.4.2, https://doi.org/10.1007/s10115-025-02491-6. This is a working project decision; full protocol/schema approval remains pending.

## 4. Requirements already represented

The following protocol concepts have a clear representation and synthetic structural checks:

- report, annotator and pass partitioning;
- source text hash, exact half-open offsets and optional source-text verification;
- report-local scope hierarchy and acyclic unit-parent hierarchy;
- mention status separate from activity-unit status;
- atomic leaves versus series/episode/aggregate containers;
- count-status consistency and non-negative bounds;
- pinned ATT&CK v12.1 exact-to-parent crosswalk and A_120 membership;
- accepted mapping evidence, mapping-level ATT&CK release and lifecycle checks; accepted analyst-candidate rationale; alternative-group membership and target-consistency checks;
- direct timestamp evidence on both endpoints;
- distinct, scope-compatible primary temporal endpoints;
- separate non-temporal relations;
- versioned candidate-pair rules and endpoint eligibility;
- duplicate/contradictory pair claims;
- partition-specific lock verification in the projection adapter;
- projection outcome distinctions, collision provenance and strict-order cycle diagnostics.

Structural checks do not decide source semantics. Human review must still decide event identity, scope, whether a mapping fits, whether a temporal cue relates the two endpoints, and whether a timestamp supports the proposed ordering.

## 5. Recommended resolution order

1. **Complete as a working decision and draft implementation — comparison scope.** The primary rule is the nearest shared RESOLVED INCIDENT ancestor; a positive relation must cite that exact scope. The v0.2 aggregator and v0.4 attack-action adapter now default to it and apply it consistently to opportunity denominators and relation numerators. The legacy broad-ancestor and v0.3 explicit-assignment rules remain separate sensitivity analyses. Synthetic tests verify cross-incident exclusion and nearest-incident scope matching. The protocol/schema still require formal review and freeze; rates remain withheld until reviewed locked annotations exist.
2. **Complete as a draft implementation — event-universe extension.** RECON v0.4 now represents `activity_stratum` in a one-to-one companion register, validates complete evidence-backed coverage, binds selected-final decisions with a lock, and filters primary projection/pair-opportunity inputs to `ATTACK_ACTION` endpoints. Twelve synthetic regression tests passed. The extension remains a draft; do not treat the existing `analysis_stratum_candidate` column as canonical or begin annotation before full protocol/schema approval.
3. Approve or revise the proposed deferrals for episode-to-episode relations and record-level ChronoCTI pair-to-event alignment. If either is retained in the pilot, define its own register and validation rather than overloading the atomic temporal relation register.
4. Specify the lifecycle of `ALTERNATIVE` mapping groups after human adjudication, including accepted/rejected status and group provenance.
5. Approve the relation-label semantics for timestamp-derived evidence, especially `OVERLAP`, `SIMULTANEOUS` and `CONCURRENT_UNSPECIFIED`, and specify how timezone ambiguity is handled. Keep semantic relation decisions human-owned.
6. Decide whether the initial pilot uses one annotator only or whether a second annotator and scope-assignment adjudication are in scope. RECON v0.2 supports selected-final partition roles structurally; the v0.3 scope-assignment lock currently blocks consensus/adjudicated-final roles.
7. After the remaining decisions, reconcile v0.1-v0.4 protocol/schema layers into one reviewed freeze package, confirm field/lock/projection consistency, update manifests/checksums, run CI, and obtain explicit researcher approval before formal annotation.

## 6. Current research boundary

- Five rank-one AnnoCTR reports remain candidates; formal researcher eligibility decisions: 0/5.
- Human-locked report annotations: 0.
- Real-report projections: 0.
- Independent human agreement: not measured.
- Novelty: not established.
- Latest CI run [#226](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/42432454480) on 8 November 2026 passed **241 synthetic test executions**: 60 root, 73 RECON v0.1, 80 RECON v0.2, 15 RECON v0.3 and 13 RECON v0.4. The 31-entry RECON v0.1 checksum manifest passed. The v0.4 tests cover complete evidence-backed stratum classification, primary attack-action projection, auxiliary communication-edge exclusion, mixed-stratum exclusion, non-primary mapping exclusion, and stratum-lock mutation rejection. New v0.2/v0.4 scope tests cover the nearest shared INCIDENT default, cross-incident campaign exclusion and exact relation-scope matching. The blank v0.4 registers passed validation with zero errors and the expected empty-bundle warning. These are structural/code-integrity checks only; they do not validate semantic annotations or prove the research question's empirical contribution.

**Freeze decision:** not ready. The event-universe and incident-bounded comparison-scope boundaries now have draft implementations and synthetic coverage, but have not been formally approved/frozen with the complete protocol. Remaining blockers include timestamp relation semantics, alternative-group lifecycle, pilot deferrals, and the scope-assignment adjudication workflow if the explicit-assignment sensitivity is used with multiple annotators. Do not start formal annotation or claim a frozen schema until those choices are recorded and the complete versioned package is approved.


## RECON v0.2 selected-analysis gate addendum — 5 November 2026

The v0.2 extension now provides a durable `analysis_partition_selection` register and selected-final adapter gate. A selected-final partition is blocked when report-level eligibility, local-use or assessability decisions conflict across any registered annotator/pass partitions. A `CONSENSUS` selection requires two distinct completed `INDEPENDENT` input partitions recorded as not themselves selected-final. An `ADJUDICATED_FINAL` selection requires an `ADJUDICATED` log row whose target register and record ID resolve to an actual record in the selected report/annotator/pass partition.

The v0.1 standalone adapter also blocks report-level eligibility/local-use/assessability conflicts, rather than allowing a warning from the parent validator to be bypassed by a direct projection call. These controls are structurally tested only; they do not authenticate annotator identity, prove semantic agreement, or replace human adjudication.

The RECON v0.1 projection metric now distinguishes cycle components that contain multiple source event edges from those that require multiple source event edges. The legacy root projector rejects self-event edges. CI run #125 passed after refreshing the 31-entry v0.1 package checksum manifest.
