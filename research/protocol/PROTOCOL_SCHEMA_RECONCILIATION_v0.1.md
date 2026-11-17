# Protocol v0.5 ↔ Schema RECON v0.1 reconciliation register

**Updated:** 16 November 2026  
**Status:** Reconciliation finding register; not protocol approval, schema approval, or a freeze decision.  
**Compared:** Protocol v0.5-draft; Metric Contract v0.1; Decision Register v0.2; RECON v0.1 field dictionary, controlled vocabularies, data-model rules, validator and projection adapter; RECON v0.2 temporal/selected-final/aggregation layer; RECON v0.3 comparison-scope assignment layer; RECON v0.4 activity-stratum layer; synthetic QA; and the register/version/lock crosswalk v0.1.

## 1. Purpose and boundary

This register checks whether each operational requirement in Protocol v0.5 has an identifiable representation in RECON v0.1: a field, a controlled value, a validator invariant, a manual procedure, or an explicit deferral.

RECON v0.1 remains a reconstruction. It is not the missing original Schema v0.4.2 and it is not approved for formal annotation. A passing synthetic validator establishes structural behavior only; it does not establish semantic correctness of a report interpretation.

## 2. Reconciliation summary

| Protocol area | RECON v0.1 coverage | Finding |
|---|---|---|
| Source identity, freeze and rights | `report_registry`, `evidence_spans`, `record_evidence_links` | Covered with a denominator correction now enforced: assessability requires the exact frozen source to be supplied and hash/character-count verified. |
| Scope hierarchy and pair comparability | `report_scopes`, unit `scope_id`, evidence links; v0.2 aggregator; v0.3 assignment extension | The hierarchy is structurally covered. The adopted working primary rule is the nearest shared RESOLVED INCIDENT ancestor, and a primary relation must cite that exact scope. Legacy broad-ancestor and explicit-assignment rules remain separate sensitivities. v0.2/v0.4 defaults and numerator/denominator filters are implemented; final protocol/schema approval remains open. |
| Mentions and occurrence identity | `event_mentions`, `activity_units`, evidence spans | Core representation covered. The exact original `mention_kind` enum was not recovered; the field remains required short descriptive free text in the working protocol and is not used for event identity, activity stratum, mapping or metrics. A controlled vocabulary would require a separately versioned codebook before any quantitative use. |
| Confidence, review state and evidence-span kind | v0.1 `annotator_confidence`, `adjudication_status`, `evidence_spans.span_kind` | These were controlled in the field dictionary but not all were checked by the base validator. The combined v0.4 full-package validator now checks every applicable base register and fails on blank/unknown values. The checksum-controlled v0.1 files remain unchanged; synthetic tests cover invalid values. This is structural enforcement, not a judgment of annotator independence or annotation quality. |
| Required-cell completeness | v0.1 field dictionary requiredness across report provenance, scope, unit, mention, evidence, mapping, relation, assessment and adjudication registers | The v0.4 combined validator now rejects blank values for the remaining clearly required cells not covered by base key/enum/foreign-key rules; validates retrieval-date format and OUT_OF_VOCAB baseline provenance; and leaves optional/conditional cells to their field-specific gates. The v0.1 headers/package remain checksum-controlled and unchanged. This is a structural completeness check, not semantic evidence validation. |
| Granularity, unit roles and counts | `activity_units` | Covered structurally, including role/granularity pairings, count consistency and acyclic parent hierarchy. |
| Event-universe stratum | RECON v0.4 `activity_unit_strata.csv` one-to-one extension, validator, lock and primary projection filter | Implemented as a draft additive layer without mutating the checksum-controlled v0.1 `activity_units.csv`: every activity unit has exactly one evidence-backed stratum row; selected-final stratum decisions are bound to the v0.2 lock; only ATTACK_ACTION leaves, mappings, edges and pair opportunities enter primary projection. Auxiliary and mixed rows remain visible separately. Twenty-eight synthetic tests pass (CI #278). The v0.4 validator enforces base confidence/adjudication/span-kind vocabularies, required-cell completeness, retrieval-date and OUT_OF_VOCAB provenance checks, conditional report-registry reason pairings, time-evidence target consistency, and the single-annotator-only/UNREVIEWED stratum adjudication boundary. Researcher review and protocol/schema freeze remain open. |
| ATT&CK mapping | `event_mappings`, mapping evidence links, pinned A_120 and v12.1 crosswalk | Core structural gates are covered: accepted analyst candidates require rationale/evidence, accepted IDs and parents are checked against v12.1, and alternative groups are checked for membership, lifecycle state and traceable resolution. Human semantic fit and the decision that candidate interpretations are truly mutually exclusive remain open. |
| Time evidence | `time_evidence`, `event_mentions`, activity units and v0.2 temporal-evidence validator | Structural validation checks aware ISO-8601 bounds, precision/timezone fields, uncertainty notes, retained normalized candidates and invariant strict `BEFORE`/`AFTER` ordering. A time record may target a unit, a mention, or both; mention-only records resolve through `event_mentions.activity_unit_id`, and populated dual targets must agree. The v0.2 direct-timestamp gate uses that resolved unit when matching endpoint evidence. Timezone equivalence and non-strict label derivation remain semantic/manual boundaries. |
| Temporal relations | v0.1: `temporal_relations`, evidence spans and generic evidence links; v0.2: `temporal_relation_evidence.csv` | v0.1 alone remains partial. The additive v0.2 extension now distinguishes relation cue, Event A support, Event B support and context, with structural scope checks; Protocol v0.5 Section 4.3 now reflects that representation. |
| Episode-level exploratory relations | No dedicated register in v0.1/v0.2 | **Adopted working pilot deferral (15 November 2026):** retain episode containers and supported time evidence, but do not annotate episode-to-episode temporal edges or report episode metrics in the initial pilot. Atomic event-leaf relations remain eligible under existing rules. |
| Optional candidate-pair assessment | `candidate_pair_assessments` | Covered structurally. Endpoint eligibility, rule/version pinning, and reasons for all three non-positive outcomes are validated. Positive assessments must match the linked temporal relation's normalized claim: `BEFORE(A,B)` equals `AFTER(B,A)`, strict order remains directional, and `OVERLAP`/`SIMULTANEOUS`/`CONCURRENT_UNSPECIFIED` are symmetric under endpoint reversal. Reversed strict endpoints without the inverse label fail validation. The candidate universe itself remains a researcher-frozen rule. |
| Lock and benchmark reveal | v0.1 partition lock; v0.2 `analysis_partition_selection` and selected-final wrapper; v0.3 scope-assignment lock; v0.4 activity-stratum lock | Final analysis partition designation and the three lock types are structurally represented. The new register/version/lock crosswalk maps their exact register grains, keys, validator entrypoints, consumers and chain dependencies. The v0.3 and v0.4 locks are sibling extensions bound directly to the v0.2 selected-analysis lock; the v0.4 lock does not substitute for v0.3 assignment validation. Digests detect changes but are not identity signatures; human sign-off remains a workflow control. |
| Projection and cycle diagnostics | Projection adapter and `projection_metrics_recon.py` | Core event-edge projection, omission, collision and cycle-provenance logic is represented and synthetically tested. |
| Full metric contract | Metric Contract v0.1; v0.2 `report_level_aggregation.py`; v0.4 attack-action adapter | The contract defines separate report-level event presence, compatible pair opportunity, same-technique pair opportunity, positive relation, within-technique relation and conditional descriptive outcomes. The v0.2 aggregator implements these outcomes with selected-final and denominator gates; v0.4 filters the primary pair/event universe to ATTACK_ACTION leaves and incident-bounded scope. Scope-pair-dependent opportunity rates remain withheld unless the caller explicitly approves the scope rule; no real-report metrics exist. |
| ChronoCTI baseline alignment | No alignment register in RECON v0.1/v0.2 | **Adopted working pilot deferral (15 November 2026):** preserve benchmark pair IDs/labels/provenance separately; do not create event-pair alignment labels or repurpose existing registers. A later alignment study requires a dedicated register and evidence/validation plan. |

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

### 3.3 Episode-level exploratory relations — adopted working pilot deferral, 15 November 2026

RECON v0.1 and v0.2 have no dedicated episode-to-episode temporal relation register. Their primary temporal relation path is for distinct resolved atomic event leaves; containers are not primary graph endpoints.

Protocol v0.5-draft adopts a working deferral for this pilot: retain episode containers and any supported unit/time evidence, but do not create episode-to-episode relation records or episode metrics. This keeps the initial schema bounded without weakening the atomic event gate. Atomic event leaves remain the only relation-register endpoints. A later episode-edge study requires a separately versioned register, distinct tests and a protocol amendment. This is a working boundary, not formal freeze approval.

### 3.4 Alternative mapping groups — working lifecycle decision adopted 15 November 2026

The existing row fields are sufficient for a conservative lifecycle; no new group register or columns are needed in this reconstruction.

- **Pending:** every member of a group is `ALTERNATIVE`. Each row has a distinct mapping ID, one exact candidate technique ID, mapping-specific evidence link and rationale. Pending members never contribute to the accepted mapping set.
- **Resolved with a winner:** exactly one member becomes `ACCEPTED`; every other member becomes `REJECTED`.
- **Resolved without a winner:** every member becomes `REJECTED`.
- A group with a mixture of `ALTERNATIVE` and final statuses is partially resolved and invalid. More than one `ACCEPTED` member is invalid. `UNRESOLVED` rows are not group members; when no candidate can be specified, retain a separate `UNRESOLVED` mapping decision instead of inventing a candidate.
- Preserve the same `alternative_group_id` on all members, including the winner and rejected alternatives. Preserve rejected rows. `alternative_to_mapping_id` is an optional within-group trace link, not the resolution mechanism.
- A separate reviewer records each adjudicated member decision in `adjudication_log` against `event_mappings.mapping_decision_status`. Do not label a single annotator's own choice as independent adjudication.
- Two independently supported techniques remain separate `ACCEPTED` mappings with no alternative group.

The v0.1 validator now enforces group membership, single-unit ownership, source-supported candidate basis, exact candidate IDs, per-member rationale/evidence, pending-vs-resolved status consistency, at-most-one accepted winner and stable group lineage. Accepted A_120 mapping counts exclude any member of an unresolved or invalid group. The projection function already excludes non-`ACCEPTED` rows and continues to rely on successful validation before use.

These rules are a new working interpretation of the reconstructed fields, not recovered original v0.4.2 semantics. The validator cannot decide whether candidates are truly mutually exclusive or whether a winner is semantically correct; those remain human judgments.

### 3.5 Analyst-candidate mapping rationale — corrected

The validator now requires non-empty `mapping_notes` for every accepted `source_supported_analyst_candidate` mapping. Accepted source-supported mappings also require a mapping-specific evidence link. This records the human rationale without duplicating the exact source span in another free-text field. The structural gate cannot decide whether the proposed technique is semantically appropriate; that remains the annotator's responsibility.

### 3.6 Candidate-pair assessment reason — corrected

The validator now requires a non-empty `assessment_reason` for each of `NO_TEMPORAL_CLAIM`, `VAGUE_OR_AMBIGUOUS`, and `NOT_ASSESSABLE`. An unassessed pair still receives no assessment row and is not treated as a negative.

### 3.7 Final analysis partition designation — implemented in v0.2; v0.3 final-role boundary remains

RECON v0.2 adds `analysis_partition_selection`, a selected-final adapter and a lock that binds the selected partition to the source/annotation lock, temporal-evidence rows and selection decision. The validator enforces at most one selected-final partition per report. `CONSENSUS` requires two distinct completed independent input partitions; `ADJUDICATED_FINAL` requires a valid `ADJUDICATED` log entry whose target record and `field_name` resolve. `ADJUDICATED`, `AGREED`, and `DEFERRED` rows now form one date-ordered per-field history: `ADJUDICATED` must change the value (`original_value != final_value`); `AGREED` and `DEFERRED` must keep `original_value == final_value`; each later entry must begin from the preceding `final_value`; and the latest value must match the persisted target-register field. Same-day entries are rejected when at least one is value-changing; non-value-changing same-day entries are valid only when the field value remains consistent. Only a valid history containing `ADJUDICATED` satisfies `ADJUDICATED_FINAL`. Partition keys and target record IDs cannot be changed through field-level adjudication. These are reconstruction proposals, not recovered original v0.4.2 semantics; the first history entry's `original_value` cannot be independently checked in the absence of a prior history row. CI #306 passed 100 RECON v0.2 synthetic tests as part of 284 total, including a regression that rejects an ADJUDICATED outcome whose original and final field values are identical. Report-level aggregation consumes only the selected final partition and does not sum annotator/pass partitions.

RECON v0.3's separate explicit-scope assignment lock supports `SINGLE_ANNOTATOR_FINAL` only: consensus/adjudicated-final roles are blocked because the v0.1 adjudication log cannot target v0.3 assignment rows. **Adopted pilot boundary (15 November 2026):** retain this approach as a single-annotator sensitivity only; do not use it for multi-annotator results in the current pilot. The primary incident-bounded rule does not depend on this extension. If future work requires multi-annotator scope assignments, a dedicated assignment-adjudication register, validator and protocol procedure must be designed before use. All lock behavior remains structural and does not authenticate annotator identity or prove agreement.

### 3.8 Baseline pair alignment — adopted working initial-pilot deferral, 15 November 2026

Protocol v0.5-draft previously required explicit alignment labels (`supported`, `multiple_candidate_pairs`, `ambiguous`, `unmapped`, `not_assessable`) after the event-level candidate set was reviewed. RECON v0.1/v0.2 has no dedicated register for correspondence between benchmark technique-pair items and report-local event pairs. Those labels must not be forced into `event_mappings` or `candidate_pair_assessments`.

Protocol v0.5-draft Section 6.3 now adopts a working deferral of record-level ChronoCTI pair-to-event alignment from the initial pilot. Preserve raw benchmark pair IDs, labels and provenance in the separate baseline reproduction materials. Do not treat benchmark edges as source evidence. If alignment is later brought into scope, add a dedicated register, candidate-generation rules, evidence requirements and separate validation. This is a working boundary, not formal protocol/schema freeze.

### 3.9 Metric coverage — report-level definitions and aggregation implemented; empirical outputs pending

The projection module implements event-edge-to-technique-pair projection, diagonal/full/partial/unmapped edge outcomes, distinct-pair collisions, label conflicts, source-graph cycle checks and projected-cycle provenance.

Metric Contract v0.1 defines separate report-level indicators and formulas for event-leaf presence, compatible event-pair opportunity, same-technique pair opportunity, positive temporal-relation presence, within-technique temporal-relation presence and the conditional descriptive rate. It also defines occurrence compression, mapping coverage, edge projection outcomes, omitted diagonal combinations, distinct-pair collisions and strict-order cycle diagnostics. These outcomes have different units and must not be collapsed into a single information-loss percentage.

RECON v0.2 `analysis/report_level_aggregation.py` implements the report-level numerator/denominator handling, selected-final partition gate, assessability coverage, occurrence compression, label breakdowns and projection diagnostics. It requires verified source texts and a valid selected-final projection for each assessable report before publishing the complete report-rate set. It withholds pair-opportunity-dependent rates unless the caller explicitly sets the scope-pair approval gate; the incident-bounded rule is the working default, not yet formal researcher freeze approval. The v0.4 adapter filters the primary calculation to ATTACK_ACTION event leaves and applies the same incident-bounded scope rule to the pair-opportunity denominator and positive-relation numerator.

**Disposition:** the earlier repair proposal is complete as a working metric specification and synthetic implementation. Full metric-contract approval, valid human-locked partitions, complete source verification and all empirical outputs remain pending. The aggregator does not decide event semantics, source entailment or scope correctness.

### 3.10 Time normalization and timestamp-derived relation semantics — working rule adopted; implementation extended

RECON v0.2 retains raw expression, time type, precision, source timezone text/status, normalized bounds/timezone, normalization status and uncertainty notes. The validator requires timezone-aware ISO-8601 bounds, explicit source timezone metadata, UTC-normalized bounds, valid interval direction, uncertainty notes for non-point intervals, and endpoint-evidence links. It rejects retained timestamp candidates that remain unnormalized and checks that strict `BEFORE`/`AFTER` ordering is invariant across every retained endpoint-interval combination.

**Working semantic rule adopted 14 November 2026:** normalized bounds represent closed ranges of possible occurrence instants, not action durations. Timestamp-only evidence (`direct_timestamp`) may establish only strict `BEFORE`/`AFTER`, with `A_end < B_start` across all A/B interval combinations (or the reverse for AFTER). The validator now rejects `direct_timestamp` for `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED`. Those non-strict positive labels require an explicit source assertion and `direct_source`; equal timestamps, identical dates and overlapping uncertainty windows cannot establish them. Only time records typed `ATTACK_OCCURRENCE` can supply endpoint timestamp ordering.

Preserve the exact source zone/offset in `timezone_text`; do not infer it from publisher or incident geography. Ambiguous abbreviations, inferred zones, and unresolved daylight-saving folds/gaps cannot support timestamp-derived edges. Normalize accepted bounds to UTC. The structural validator checks the UTC representation, but human review remains responsible for whether the source timezone was correctly interpreted, whether the time truly identifies the attack occurrence, and whether source wording entails the selected relation. Detailed rule: `research/protocol/TIMESTAMP_RELATION_SEMANTICS_v0.1.md`.

### 3.11 Event-universe stratum — draft implementation in RECON v0.4

The working research-design decision adopted on 8 November 2026 defines incident-linked attack-action occurrences as the primary ChronoCTI-comparable stratum. The decision is medium-neutral: concrete phishing delivery, induced user execution, exploitation, persistence, command and control, collection, exfiltration, impact, and incident-linked operational extortion may qualify. Public commentary/platform events, analyst/sample observations, generic capabilities, and other non-primary activity remain visible in separate descriptive strata.

The reconstructed v0.1 activity_units register has granularity, unit_role, and instance_status, but cannot distinguish an operational attack-action occurrence from a resolved communication or analyst-observation occurrence. RECON v0.4 supplies the logical activity_unit.activity_stratum field in the one-to-one activity_unit_strata.csv companion register. This is a deliberate additive extension: it preserves the v0.1 header and checksum contract rather than changing the reconstructed ancestor in place. Every activity unit must receive exactly one stratum decision with an evidence span and rationale.

The v0.4 validator enforces complete one-to-one coverage, controlled values/bases, same-partition evidence references, and the rule that a generic capability without a resolved execution cannot be a resolved atomic event leaf. The v0.4 lock binds stratum rows to the v0.2 selected-analysis lock reference. The primary projection helper selects only ATTACK_ACTION event leaves, their accepted A_120 mappings, their direct positive scope-compatible relations, and their pair-opportunity universe. Same-stratum auxiliary and mixed-stratum relations remain visible in separate diagnostics but cannot enter the primary graph. Classification remains independent of ATT&CK mapping.

**Adjudication boundary:** the companion register has no dedicated adjudication log. The v0.4 draft therefore accepts `adjudication_status=UNREVIEWED` only and permits activity-stratum locks only for `SINGLE_ANNOTATOR_FINAL`. `CONSENSUS` and `ADJUDICATED_FINAL` use is blocked until a separately versioned stratum adjudication register, validator and procedure can identify reviewed stratum rows and their final values.

Draft implementation: research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/. The pre-annotation CSV's analysis_stratum_candidate column remains triage metadata only; no individual candidate classification is approved. Synthetic tests cover auxiliary/mixed edge exclusion, non-primary mapping exclusion, complete classification, lock preconditions, metadata requiredness, time-target identity and adjudication-boundary failures. These are structural checks only. Formal annotation remains blocked until the v0.4 layer is reviewed with the other protocol decisions and the complete package is approved/frozen.

### 3.12 Comparison-scope rule — incident-bounded primary default

ChronoCTI frames its input as a textual description of an attack incident and selects reports that narrate cyberattack incidents step-by-step (Rahman et al., 2025, Sections 1 and 4.4.2, https://doi.org/10.1007/s10115-025-02491-6). The broad nearest-common-resolved-non-report-ancestor rule can count two distinct INCIDENT nodes merely because they share a campaign, operation, organisation, host or OTHER ancestor. That is too broad for the primary ChronoCTI-comparable estimand.

**Adopted working primary rule:** use the nearest shared `scope_type=INCIDENT`, `scope_status=RESOLVED` ancestor. Count each event pair once. The primary positive-relation numerator must cite that exact nearest shared INCIDENT scope in `comparison_scope_id`. A relation recorded only at a broader ancestor is retained but not counted as a primary edge. If no defensible resolved INCIDENT scope exists, do not create one from broader co-membership; the report remains assessable, but those events do not create primary pair opportunity.

The v0.2 aggregator now defaults to `SHARED_RESOLVED_INCIDENT_SCOPE_v0.1`, selects the nearest shared resolved INCIDENT, and filters the positive-relation numerator to the same exact scope. The v0.4 attack-action projection helper uses the same default and excludes scope-ineligible edges from primary projection while returning their IDs as diagnostics. The legacy nearest common non-report ancestor and the v0.3 explicit-assignment rule remain separate sensitivities and must recompute both numerator and denominator under their own rule. Synthetic regression coverage protects cross-incident campaign exclusion and exact nearest-incident relation scope.

**Source:** Rahman et al., *Mining temporal attack patterns from cyberthreat intelligence reports*, Knowledge and Information Systems (2025), Sections 1 and 4.4.2, https://doi.org/10.1007/s10115-025-02491-6. This is a working project decision; full protocol/schema approval remains pending.




### 3.13 Mention kind — working free-text representation, 15 November 2026

The required `event_mentions.mention_kind` field is a string in RECON v0.1. The exact enum in the unrecovered v0.4.2 package cannot be verified, and the recovered Protocol v0.4-draft does not supply a controlled list. The working decision is to keep it as a short descriptive free-text tag, not invent a closed vocabulary. It must not determine event identity, stratum, ATT&CK mapping or metric eligibility. If future analysis requires category-level comparison of mention forms, develop a separately versioned codebook and add its validation before collecting those labels. This resolves the initial-pilot representation without claiming to recover the original enum.

### 3.14 Record-level adjudication status versus field-level history — open semantic contract

The base annotation registers carry one `adjudication_status` value per annotation record (`UNREVIEWED`, `AGREED`, or `ADJUDICATED`). By contrast, `adjudication_log.csv` records decisions at the target-field level, with potentially multiple rows for one record and outcomes `AGREED`, `ADJUDICATED`, or `DEFERRED`.

The current combined validation path checks the record-level status against its enum and separately checks field-level log targets, date ordering, value changes and append-only history. It does not define or enforce a cross-register rule that derives the single record-level status from a set of field-level outcomes. Consequently, structurally valid data may contain a record marked `ADJUDICATED` without a corresponding `ADJUDICATED` field-history row, a record still marked `UNREVIEWED` while a field history exists, or mixed field outcomes (`AGREED`, `DEFERRED`, and `ADJUDICATED`) without a defined record-level summary.

This is not safely resolved by assuming that one field-level `ADJUDICATED` row promotes the whole record, or that a record-level status must equal every individual field outcome. The reconstructed package does not specify how to summarize partially reviewed records or mixed outcomes. A related coverage gap exists in the selected-final gate: `ADJUDICATED_FINAL` currently requires any one valid `ADJUDICATED` field-history entry in the selected partition, not a defined minimum set of records/fields or proof that the complete annotation was reviewed. The role label therefore must not be interpreted as full-partition adjudication coverage. The v0.4 activity-stratum extension avoids this ambiguity for its own rows by requiring `UNREVIEWED` only and supporting `SINGLE_ANNOTATOR_FINAL` only.

**Researcher decision required before formal freeze:** choose and document whether (a) `adjudication_status` is a record-level summary with explicit aggregation/completeness rules (including `DEFERRED` and partially reviewed fields), (b) field-level history is authoritative and the record-level status is retired or made explicitly non-authoritative in a versioned design, or (c) a separate record-review/coverage register is needed. Until resolved, do not use record-level status alone as proof that all fields were reviewed or adjudicated, and do not infer record-level completion from a single field-level decision.

## 4. Requirements already represented

The following protocol concepts have a clear representation and synthetic structural checks:

- report, annotator and pass partitioning;
- required descriptive `mention_kind` field retained as free text rather than an unrecovered enum;
- source text hash, exact half-open offsets and optional source-text verification;
- report-local scope hierarchy and acyclic unit-parent hierarchy;
- mention status separate from activity-unit status;
- atomic leaves versus series/episode/aggregate containers;
- count-status consistency and non-negative bounds;
- pinned ATT&CK v12.1 exact-to-parent crosswalk and A_120 membership;
- accepted mapping evidence, mapping-level ATT&CK release and lifecycle checks; accepted analyst-candidate rationale; alternative-group membership, pending/resolved state, evidence and traceable resolution checks;
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
2. **Complete as a draft implementation — event-universe extension.** RECON v0.4 now represents `activity_stratum` in a one-to-one companion register, validates complete evidence-backed coverage, binds selected-final decisions with a lock, and filters primary projection/pair-opportunity inputs to `ATTACK_ACTION` endpoints. Twenty-eight synthetic tests pass in CI #278. The draft supports `SINGLE_ANNOTATOR_FINAL` and `UNREVIEWED` stratum decisions only because no v0.4 adjudication log exists; multi-annotator consensus/adjudicated-final use requires a separate versioned extension. Do not treat the existing `analysis_stratum_candidate` column as canonical or begin annotation before full protocol/schema approval.
3. **Complete as working pilot decisions — initial boundaries (15 November 2026).** Defer episode-to-episode edges/metrics while retaining episode containers and supported time evidence. Defer record-level ChronoCTI pair-to-event alignment while preserving benchmark IDs/labels/provenance separately. Any later extension needs a dedicated register and validation; neither deferred item is improvised into the atomic temporal schema.
4. **Complete as a working decision and draft implementation — alternative mapping lifecycle.** Pending groups contain only `ALTERNATIVE` members; resolved groups contain one `ACCEPTED` plus `REJECTED` members, or all `REJECTED`. Preserve group lineage; partial and multiple-winner groups are invalid. Human mutual-exclusivity and winner decisions remain open.
5. **Complete as a working decision and draft implementation — timestamp semantics.** Timestamp-only evidence is restricted to invariant strict BEFORE/AFTER; the three non-strict positive labels require explicit direct-source wording. Normalized occurrence-time bounds are closed possibility ranges and accepted normalized values use UTC. Ambiguous/inferred zones and unresolved DST interpretations do not support timestamp-derived edges. The v0.2 validator and synthetic tests enforce the structural parts; human review remains responsible for semantic correctness.
6. **Complete as a working workflow boundary — v0.3 scope-assignment sensitivity.** Use v0.3 explicit event-to-scope assignment only with `SINGLE_ANNOTATOR_FINAL` in this pilot. It is not eligible for multi-annotator consensus/adjudicated-final use until a dedicated assignment-adjudication register, validator and procedure are implemented. The primary incident-bounded analysis does not depend on v0.3.
7. **Complete as a technical artifact — register/version/lock crosswalk.** The companion `PROTOCOL_SCHEMA_REGISTER_VERSION_LOCK_CROSSWALK_v0.1.md` maps all 12 base registers and six extension/lock registers to their record grain, key, validator, consumer, protocol area and lock dependencies. It clarifies that v0.3 assignment and v0.4 stratum locks are sibling extensions bound directly to v0.2; it does not make either extension an approved annotation layer.
8. **Freeze-preparation audit.** Cross-check the complete Protocol v0.5-draft, Metric Contract v0.1, Decision Register v0.2 and RECON v0.1-v0.4 fields, enums, locks, validation gates, projection inputs and metric outputs. Record all accepted reconstruction proposals and any remaining open field or workflow decisions; do not imply recovery of the missing original v0.4.1/v0.4.2 artifacts.
9. **Formal approval gate.** The researcher must explicitly accept Protocol v0.5 and the reconstructed schema/extensions as a new replacement package, approve the metric contract and applicable scope-pair rule, and confirm the human annotation/IAA workflow. Create and tag a single versioned freeze manifest only after those approvals; regenerate its file hashes and run the full CI suite.
10. Begin source-first human feasibility annotation only after each candidate has passed its individual eligibility/source gates and the versioned package is approved/frozen. No real-report metrics or novelty claims precede the locked data.

## 6. Current research boundary

- Five rank-one AnnoCTR reports remain candidates; formal researcher eligibility decisions: 0/5.
- Human-locked report annotations: 0.
- Real-report projections: 0.
- Independent human agreement: not measured.
- Novelty: not established.
- Latest verified main-branch workflow [#306](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/44031832696) on 17 November 2026 passed **284 synthetic test executions**: 60 root, 81 RECON v0.1, 100 RECON v0.2, 15 RECON v0.3 and 28 RECON v0.4. The 31-entry RECON v0.1 checksum manifest passed. It includes direction-aware positive pair-assessment linkage; complete field-level adjudication history across ADJUDICATED/AGREED/DEFERRED outcomes; ADJUDICATED value-change enforcement and non-value-changing AGREED/DEFERRED outcome enforcement; immutable-identity validation; selected-final activity-stratum lock prerequisites; base review metadata enums; required-cell completeness; conditional report-decision rationale; mention-only timestamp target resolution and dual-target consistency; and single-annotator-only v0.4 adjudication regressions alongside alternative-mapping lifecycle, timestamp, scope and projection tests. All blank-extension validators and source-snapshot packaging passed. These remain structural/code-integrity checks only; they do not validate semantic annotations or establish empirical findings.

**Freeze decision:** not ready. The key working method decisions and corresponding synthetic safeguards are now in place, including event stratum, incident-bounded scope, timestamp semantics, alternative-mapping lifecycle and initial-pilot boundaries. The remaining blockers are approval/provenance gates rather than those already completed design decisions: the original Protocol v0.4.1 and Schema v0.4.2 artifacts remain unrecovered; the researcher must explicitly accept the reconstructed Protocol v0.5/RECON v0.1-v0.4 package as a new replacement; field/enumeration and lock crosswalks still require a final whole-package review; candidate eligibility decisions remain 0/5; human-locked annotations and real-report projections remain 0; IAA is not measured; novelty is not established. Do not start annotation or claim a frozen schema until the new package is explicitly reviewed, approved, version-locked and tagged.


## RECON v0.2 selected-analysis gate addendum — 5 November 2026

The v0.2 extension now provides a durable `analysis_partition_selection` register and selected-final adapter gate. A selected-final partition is blocked when report-level eligibility, local-use or assessability decisions conflict across any registered annotator/pass partitions. A `CONSENSUS` selection requires two distinct completed `INDEPENDENT` input partitions recorded as not themselves selected-final. An `ADJUDICATED_FINAL` selection requires an `ADJUDICATED` log row whose target register and record ID resolve to an actual record in the selected report/annotator/pass partition.

The v0.1 standalone adapter also blocks report-level eligibility/local-use/assessability conflicts, rather than allowing a warning from the parent validator to be bypassed by a direct projection call. These controls are structurally tested only; they do not authenticate annotator identity, prove semantic agreement, or replace human adjudication.

The RECON v0.1 projection metric now distinguishes cycle components that contain multiple source event edges from those that require multiple source event edges. The legacy root projector rejects self-event edges. CI run #125 passed after refreshing the 31-entry v0.1 package checksum manifest.