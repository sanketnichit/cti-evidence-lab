# CTI Evidence Lab — Register, Version and Lock Crosswalk v0.1

**Date:** 15 November 2026  
**Status:** Technical crosswalk for freeze preparation — not approval, not a frozen schema  
**Scope:** RECON v0.1 base registers and the additive RECON v0.2, v0.3 and v0.4 layers.

## 1. Purpose and provenance

This document maps each physical CSV register to its record grain, partition key, validating layer, downstream consumer and lock dependency. It is intended to prevent register/version ambiguity when the protocol and reconstructed schema are reviewed as one package.

RECON v0.1 is a new reconstruction based on recovered protocol/audit materials. It is **not** the unrecovered original Schema v0.4.2. The exact Protocol v0.4.1 draft and original Schema v0.4.2 ZIP remain unavailable. The extension layers are additive: v0.1's 12 register headers are checksum-controlled and are not changed by v0.2–v0.4.

All registers are currently header-only. There are no real report annotations, selected-final partitions, v0.3 assignments, v0.4 stratum decisions, or lock rows. The crosswalk describes implementation and workflow dependencies, not evidence that any report has been annotated.

## 2. Version and dependency model

| Layer | Physical role | Direct parent / required inputs | Main validation / analysis entrypoints | Lock contribution |
|---|---|---|---|---|
| RECON v0.1 | Base report-partitioned annotation model; 12 registers | Reconstructed base design; pinned A_120 vocabulary and Enterprise ATT&CK v12.1 exact-to-parent crosswalk | `validator/validate_annotations.py`; `analysis/annotation_projection_adapter.py`; `analysis/projection_metrics_recon.py` | Computes the base annotation-partition digest from the frozen source-text hash and every v0.1 register row in the selected report/annotator/pass partition. |
| RECON v0.2 | Additive temporal-evidence and final-analysis selection layer | v0.1 base registers and validator | `validator/validate_temporal_evidence.py`; `analysis/selected_partition_projection_adapter.py`; `analysis/report_level_aggregation.py` | Adds the selected-analysis lock: v0.1 base lock + v0.2 temporal-relation-evidence rows + selected-final decision. |
| RECON v0.3 | Optional event-to-comparison-scope assignment sensitivity | v0.1 base + v0.2 selected-final register/lock | `validator/validate_comparison_scope_assignments.py`; `analysis/aggregate_selected_report_projections.py` | Adds a scope-assignment lock over canonical assignment rows, bound to the v0.2 selected-analysis lock. Supports `SINGLE_ANNOTATOR_FINAL` only. |
| RECON v0.4 | Required primary event-universe stratum extension | v0.1 base + v0.2 selected-final register/lock; v0.3 assignments/lock are additionally required only for the explicit-assignment sensitivity | `validator/validate_activity_strata.py`; `analysis/primary_attack_action_projection.py` | Adds an activity-stratum lock over canonical stratum rows, bound directly to the v0.2 selected-analysis lock. It is not cryptographically chained through the v0.3 assignment lock. |

**Important dependency distinction:** v0.3 and v0.4 are separate additive extensions over the selected v0.2 analysis partition. The v0.4 manifest lists v0.3 among its parent layers because it forms part of the combined working package, but the v0.4 stratum lock itself binds to the v0.2 selected-analysis lock. The v0.3 assignment lock is separately required only when the v0.3 explicit-scope sensitivity is invoked. Do not treat the v0.4 lock as proof that v0.3 assignments were validated or locked.

## 3. RECON v0.1 — base register crosswalk

The common annotation partition is:

`(report_id, annotator_id, annotation_pass_id)`

Except for the adjudication log, every base register stores these three fields directly. The register-local record ID is unique within that partition.

| Register | Record grain / purpose | Partition-local record key | Main protocol mapping | Downstream use |
|---|---|---|---|---|
| `registers/report_registry.csv` | One report × annotator × pass; source identity, rights, eligibility, assessability, review completion and exposure | `(report_id, annotator_id, annotation_pass_id)` | Protocol §§1, 5, 7; provenance and denominator rules | Base validator; N_eligible/N_assessable; selected-final eligibility and source verification. |
| `registers/report_scopes.csv` | One report-local scope node; parent links establish incident/campaign/operation/victim/host hierarchy | Partition + `scope_id` | Protocol §2.2 and incident-bounded comparison-scope rule | Scope ancestry, temporal-relation compatibility, candidate-pair checks and pair-opportunity computation. |
| `registers/activity_units.csv` | One report-local activity unit; event leaf or series/episode/aggregate/unresolved container | Partition + `activity_unit_id` | Protocol §§2.4–2.6 | Event endpoint eligibility; scope/parent hierarchy; mappings, time evidence and relation endpoints; projection adapter. |
| `registers/event_mentions.csv` | One source mention/reference linked to an activity unit | Partition + `mention_id` | Protocol §§2.3–2.4, Pass 2 | Mention-to-unit identity and evidence; supports event resolution but does not itself create multiple event instances. |
| `registers/evidence_spans.csv` | One exact frozen-source span with offsets and locators | Partition + `evidence_span_id` | Protocol §§4.3, 5 and source text convention | Primary/additional evidence for mentions, mappings, scope, temporal relations, time records and adjudication. |
| `registers/record_evidence_links.csv` | One additional evidence link from a typed annotation record to a source span | Partition + `link_id` | Protocol §4.3 and register-specific evidence rules | Base validator checks target/role/span references, composite uniqueness and required mapping evidence. |
| `registers/event_mappings.csv` | One exact technique/sub-technique mapping decision for an activity unit | Partition + `mapping_id` | Protocol §3.1–3.2 | Accepted source-supported A_exact/A_120 mapping sets; alternative-group lifecycle; projection metrics. |
| `registers/time_evidence.csv` | One typed time observation associated with a unit and/or mention | Partition + `time_evidence_id` | Protocol §§2.6, 4.2.1 | v0.2 temporal-evidence validator checks normalized intervals and endpoint linkage for direct-timestamp relations. |
| `registers/temporal_relations.csv` | One direct/derived/unresolved temporal relation between event-unit endpoints | Partition + `relation_id` | Protocol §4 and timestamp rule §4.2.1 | Temporal graph, evidence extension, pair metrics, projection and strict-order cycles. |
| `registers/candidate_pair_assessments.csv` | One explicitly assessed event pair under a declared candidate-generation rule | Partition + `assessment_id` | Protocol §4.1, Pass 5 and §7 | Optional assessed-negative/ambiguous coverage; not an exhaustive all-pairs matrix. |
| `registers/non_temporal_relations.csv` | One causal/dependency/narrative-order-only relation between activity units | Partition + `non_temporal_relation_id` | Protocol §4.4 | Kept separate from temporal edges; excluded from temporal graph and projection. |
| `registers/adjudication_log.csv` | One reviewer decision for a target annotation record/field | `(report_id, target_annotator_id, annotation_pass_id, adjudication_id)` | Protocol annotation/adjudication workflow | Resolves selected target-record values where supported. It does not contain targets in the v0.3 scope-assignment register. |

### Base package invariants

- v0.1's `schema_manifest.json` declares exactly 12 base registers. `SHA256SUMS.txt` contains the controlled file digests; v0.2–v0.4 must not edit the v0.1 register headers or package files in place.
- `validate_annotations.py` validates the base registers, partition-local references, evidence links, source text hash/offsets, event-leaf constraints, mapping status and the pinned ATT&CK vocabulary/crosswalk.
- `compute_annotation_lock_reference` hashes the exact frozen source text plus all v0.1 register rows for one report/annotator/pass. `build_projection_for_partition` requires an explicit caller confirmation and the exact recomputed digest before base projection.
- This digest is a mutation detector, not a digital signature or proof of human authorship, reviewer independence or that a human completed the pass.

## 4. RECON v0.2 — temporal evidence and selected-final analysis

| Register | Record grain / purpose | Key | Validator / consumer | Lock relationship |
|---|---|---|---|---|
| `registers/temporal_relation_evidence.csv` | One relation × evidence span × support role; distinguishes relation cue, Event A support, Event B support and context | Partition + `relation_evidence_id` | `validate_temporal_evidence.py`; `selected_partition_projection_adapter.py` | All rows for the selected partition enter the v0.2 analysis-lock payload. |
| `registers/analysis_partition_selection.csv` | One candidate final-partition decision for one report; records annotator/pass, role, selection state, rationale/date and lock reference | `(report_id, analysis_partition_id)`; selected annotator/pass resolves against v0.1 `report_registry` | `validate_analysis_partition_selection` in `validate_temporal_evidence.py`; selected-partition adapter and report aggregator | The selected decision (excluding its own `lock_reference`) enters the v0.2 lock payload. At most one `SELECTED_FINAL` per report. |

The v0.2 evidence validator revalidates the v0.1 base and adds role/locator checks for `RELATION_CUE`, `EVENT_A_SUPPORT`, `EVENT_B_SUPPORT` and optional/required `RELATION_CONTEXT`. Timestamp rules are also enforced at this layer.

The v0.2 selected-analysis adapter recomputes the v0.1 base annotation lock, filters all temporal-evidence rows to the selected report/annotator/pass partition, and adds the selection decision. The resulting `CTI-EVIDENCE-LAB-SELECTED-ANALYSIS-LOCK-v2` is a second lock. It then validates the base and temporal layer and requires explicit confirmation plus a matching lock reference before projection. The selected-partition adapter does not accept caller-supplied annotator/pass IDs; it resolves them from the final-selection register.

The report-level aggregator consumes selected-final projection outputs. It keeps N_eligible/N_assessable handling, pair opportunities, positive temporal outcomes and projection diagnostics separate. Its primary scope rule defaults to the nearest shared resolved INCIDENT. Pair-opportunity-dependent rates remain withheld unless `approve_scope_pair_rule` is explicitly enabled by the caller. This explicit caller flag is not itself proof that the researcher approved the scientific rule.

## 5. RECON v0.3 — explicit comparison-scope sensitivity

| Register | Record grain / purpose | Key | Validator / consumer | Lock relationship |
|---|---|---|---|---|
| `registers/event_comparison_scope_assignments.csv` | One event activity unit × candidate comparison scope × report/annotator/pass decision; states ASSIGNED/NOT_ASSIGNED/UNCERTAIN | Partition + `assignment_id`; event × scope must also be unique | `validate_comparison_scope_assignments.py`; v0.3 aggregate wrapper | Canonical assignment rows are hashed for each selected-final partition. |
| `registers/comparison_scope_assignment_locks.csv` | One v0.3 assignment-lock record per selected-final partition | Partition + `lock_id` | `validate_scope_assignment_locks`; v0.3 aggregate wrapper | Stores v0.2 `analysis_lock_reference`, `assignment_rows_sha256`, lock format/owner/date, and a lock digest binding both. |

The validator first validates v0.1 base and v0.2 selection, then requires complete explicit decisions for every eligible resolved non-report ancestor scope for each resolved atomic event leaf. Missing rows block validation; they are not NOT_ASSIGNED. Positive temporal relations and compatible candidate-pair assessments under this rule must name a scope ASSIGNED to both endpoints.

The v0.3 lock builder and validator support `SINGLE_ANNOTATOR_FINAL` only. There is no v0.3-specific adjudication register, so CONSENSUS and ADJUDICATED_FINAL selections are blocked. The v0.3 aggregation wrapper validates the assignment rows and their lock, explicitly confirms both selected-analysis and scope-assignment locks, and then calls the v0.2 aggregator using the explicit-assignment scope rule. In the initial pilot this remains a separately reported sensitivity, not the primary rule.

## 6. RECON v0.4 — activity-stratum extension and primary event-universe filter

| Register | Record grain / purpose | Key | Validator / consumer | Lock relationship |
|---|---|---|---|---|
| `registers/activity_unit_strata.csv` | Exactly one activity-stratum decision for every v0.1 activity unit in a report/annotator/pass partition | Partition + `activity_unit_id` | `validate_activity_strata.py`; `primary_attack_action_projection.py` | Canonical stratum rows in a selected partition are hashed for the v0.4 lock. |
| `registers/activity_stratum_locks.csv` | One stratum-lock record per selected-final partition | Partition | `validate_activity_stratum_locks`; caller of primary projection helper | Stores v0.2 `analysis_lock_reference`, `activity_strata_sha256`, lock format/owner/date and the digest binding those values. |

The v0.4 validator enforces one-to-one coverage of the v0.1 activity-unit universe, valid stratum vocabularies/bases, partition-local evidence references and non-primary generic-capability restrictions. The lock binds all partition stratum rows directly to the v0.2 selected-analysis reference. The primary projection helper filters eligible event leaves, mappings, positive temporal relations and pair-opportunity inputs to `ATTACK_ACTION`, then applies the chosen scope-pair rule consistently to numerator and denominator. It returns IDs of primary-stratum relations excluded by the scope rule for diagnostics.

The projection helper is not a lock-verification substitute. Before use on a reviewed partition, the caller must validate the v0.1 bundle, v0.2 selected-final partition/analysis lock, and v0.4 strata register/lock. If the explicit-assignment sensitivity is selected, separately validate and confirm the v0.3 assignment register and lock. The v0.4 lock alone does not prove the v0.3 sensitivity layer is valid.

## 7. Integrated protocol-to-register map

| Protocol area | Authoritative representation | Version | Review / scope |
|---|---|---|---|
| Report provenance, eligibility, rights, assessability and prior exposure | `report_registry.csv` | v0.1 | One report/annotator/pass partition; source text must be verified before assessability. |
| Scope hierarchy and primary pair comparability | `report_scopes.csv`, `activity_units.scope_id`, `temporal_relations.comparison_scope_id` | v0.1 + v0.2 logic + v0.4 filter | Primary nearest shared resolved INCIDENT; broader rules are separate sensitivities. |
| Mentions versus report-local activity identity | `event_mentions.csv`, `activity_units.csv` | v0.1 | `mention_kind` remains descriptive free text; atomic event identity needs source support. |
| Attack-action event-universe stratum | `activity_unit_strata.csv` | v0.4 | Required one-to-one classification; only ATTACK_ACTION event leaves enter primary graph. |
| ATT&CK mapping decisions | `event_mappings.csv`, `record_evidence_links.csv`, pinned A_120 and v12.1 crosswalk | v0.1 | Mapping status and alternative-group lifecycle validated in v0.1; human semantic fit remains manual. |
| Time observations and timestamp order | `time_evidence.csv`, `temporal_relations.csv`, `temporal_relation_evidence.csv` | v0.1 + v0.2 | Only attack-occurrence times support timestamp-derived strict BEFORE/AFTER. |
| Temporal relation cue and endpoint support | `temporal_relations.csv`, `temporal_relation_evidence.csv`, `evidence_spans.csv` | v0.1 + v0.2 | Role-coded evidence for cue, both endpoints and context; semantic entailment remains human-reviewed. |
| Non-temporal relations | `non_temporal_relations.csv` | v0.1 | Kept out of temporal graph and temporal projection. |
| Optional assessed candidate-pair negatives | `candidate_pair_assessments.csv` | v0.1 | Requires declared generation rule/version; absent row is not a negative. |
| Human adjudication | `adjudication_log.csv` | v0.1 | Does not target v0.3 scope-assignment rows; scope-assignment adjudication is deferred. |
| Final annotation partition choice | `analysis_partition_selection.csv` | v0.2 | At most one selected-final per report; selection binds a v0.1 annotation partition. |
| Optional explicit event-to-scope sensitivity | `event_comparison_scope_assignments.csv`, `comparison_scope_assignment_locks.csv` | v0.3 | Single-annotator only in the initial pilot; not used for multi-annotator consensus/adjudication. |
| Projection and report-level metrics | v0.1 adapter/metrics; v0.2 selected adapter/aggregator; v0.4 primary stratum helper | v0.1–v0.4 | Uses selected-final locked partitions; primary ATTACK_ACTION and incident-bounded rules; scope-pair rate gate requires explicit approval. |

## 8. Known limitations and crosswalk review items

1. The exact Protocol v0.4.1 and original Schema v0.4.2 ZIP remain unrecovered. This crosswalk records the current reconstruction; it does not restore or prove the original field/enum definitions.
2. `report_registry.protocol_version` and `schema_version` are partition metadata fields. The final freeze must specify the exact composite protocol/schema version identifier applied to each annotation partition; this document does not silently assign one.
3. v0.3 adjudication is not implemented. Do not use its scope-assignment sensitivity with multi-annotator consensus or adjudicated-final data.
4. v0.3 and v0.4 locks each bind directly to v0.2 selected-analysis lock; neither lock authenticates identity or substitutes for a documented human sign-off.
5. The v0.2/v0.3 manifests and v0.4 README were reconciled during this crosswalk revision to state the incident-bounded primary rule, broader/explicit sensitivity roles and the single-annotator v0.3 limitation. The current text should be checked again at final freeze, alongside the protocol/metric version crosswalk.
6. All extension registers are currently header-only. No lock has been generated, and all real-report/empirical counts remain zero.

## 9. Freeze use

This crosswalk is a technical readiness artifact. It does not grant approval to begin annotation. Before freeze, review it against Protocol v0.5-draft, Metric Contract v0.1, Decision Register v0.2, all RECON manifests and validators. Resolve any field/enum/lock mismatch, explicitly accept the reconstructed package as a new replacement for the unavailable originals, generate a single freeze manifest with exact file hashes, obtain researcher approval, tag the package, and rerun the full CI workflow. Only then may source-first human annotation begin under the frozen version.
