# CTI Evidence Lab — Annotation Schema Reconstruction Specification v0.1

**Prepared:** 3 November 2026  
**Status:** Reconstruction design note with an executable provisional package and synthetic validator now produced — not the original Schema v0.4.2, not frozen, and not annotation-ready.  
**Purpose:** establish what can safely be reconstructed from the available sources before creating any replacement CSV package or validator.

> **Critical provenance statement:** The original `CTI_Annotation_Schema_v0.4.2-draft.zip` and exact `CTI_Event_Instance_Annotation_Protocol_v0.4.1-draft.md` have not been recovered. This document does not recreate their exact headers, exact field dictionary, or exact ZIP contents. It separates facts in recovered sources from requirements merely described by the conformance audit and from decisions that remain unknown.

---

## 1. Source hierarchy used for this reconstruction

| Source | What it can establish | Limitation |
|---|---|---|
| `CTI_Event_Instance_Annotation_Protocol_v0.4-draft.md` | Current available conceptual units, status/granularity vocabularies, relation labels/bases, evidence requirements, projection rules and workflow | It is v0.4-draft, not the missing v0.4.1; do not silently equate them |
| `CTI_Protocol_v0.4_Migration_Note.md` inside `CTI_Evidence_Lab_Baseline_and_Protocol_Kit_v0.2.zip` | Why v0.4 separates mentions, occurrences, containers, mapping provenance, temporal relations and optional pair assessment | Design summary, not a complete schema dictionary |
| `CTI_Annotation_Schema_v0.4.2_Conformance_Audit_v0.1.md` | Names of 12 registers; broad field coverage; P0/P1 omissions; intended validator invariants | Audit of a ZIP that is now missing; it does not reproduce every header or enum |
| Public GitHub `research/templates/*.csv` and README | Exact v0.3 headers and row granularity for four older registers | These are v0.3 templates, not the v0.4.2 schema |
| Project-wide audit v1.4 and sampling corrections | Current research-level decisions and outstanding blockers | They are audits/recommendations, not schema source files |

The duplicate Project-wide Audit v1.1 uploads are historical records. The later Project-wide Audit v1.4, Sampling Method v0.3.2, frame v0.9, and Five-report Re-audit v0.1 are the more current project-level references.

## 2. Evidence labels used below

- **CONFIRMED — v0.4 draft:** explicitly present in the recovered Protocol v0.4-draft.
- **CONFIRMED — public v0.3:** exact header or behaviour visible in the current public GitHub v0.3 templates/README.
- **AUDIT-DESCRIBED — v0.4.2:** register or field semantics reported by the v0.4.2 conformance audit, but not independently inspected in the original missing ZIP.
- **RECONSTRUCTION REQUIREMENT:** a rule needed to make the schema coherent and executable, supported by the audit/protocol, but not asserted to be an exact original v0.4.2 header.
- **UNKNOWN — original unavailable:** exact original header, enum, key or implementation cannot be verified from the sources in hand.

---

## 3. Confirmed protocol vocabularies (v0.4 draft)

These values are present in the recovered v0.4 draft and can be carried forward provisionally. They still require researcher approval in a frozen protocol.

### 3.1 Mention / instance status

`instance_status`:
- `RESOLVED`
- `UNRESOLVED`
- `GENERIC_BEHAVIOUR`
- `NOT_AN_EVENT`

### 3.2 Activity-unit granularity

`granularity`:
- `atomic_event`
- `repeated_event_series`
- `activity_episode`
- `report_level_aggregate`
- `unresolved`

### 3.3 Activity-unit role

`unit_role`:
- `event_leaf`
- `series_container`
- `episode_container`
- `aggregate_container`
- `unresolved_unit`

Primary event graph eligibility requires all three: `unit_role=event_leaf`, `granularity=atomic_event`, `instance_status=RESOLVED`. Containers are retained but excluded from primary atomic occurrence counts and edges.

### 3.4 Count status

`count_status`:
- `exact`
- `minimum`
- `range`
- `qualitative_only`
- `unknown`

### 3.5 ATT&CK mapping basis

`mapping_basis`:
- `report_explicit_subtechnique`
- `report_explicit_parent`
- `source_supported_analyst_candidate`
- `workbook_only`
- `unresolved`

The v0.4 draft requires source evidence per mapping and preserves exact technique/sub-technique identity separately from the parent technique used for ChronoCTI comparison. The v0.4.2 audit describes accepted/alternative decision status and selected-120 vocabulary metadata, but exact original enum strings are **UNKNOWN** until the ZIP is recovered.

### 3.6 Temporal relation labels

`relation_label`:
- `BEFORE`
- `AFTER`
- `OVERLAP`
- `SIMULTANEOUS`
- `CONCURRENT_UNSPECIFIED`
- `NO_TEMPORAL_CLAIM`
- `VAGUE_OR_AMBIGUOUS`
- `NOT_ASSESSABLE`

`NO_TEMPORAL_CLAIM` is permitted only for a pair actually assessed under a declared candidate-pair rule. An unrecorded pair is not a negative.

### 3.7 Temporal relation basis

`relation_basis`:
- `direct_source`
- `direct_timestamp`
- `derived_transitive`
- `inference`
- `unresolved`

Only `direct_source` and `direct_timestamp` can enter primary positive relation metrics, and only with eligible distinct atomic event-leaf endpoints in compatible scope.

### 3.8 Evidence scope and review fields

Confirmed in v0.4 draft:
- `evidence_scope`: `SENTENCE`, `CROSS_SENTENCE`, `DOCUMENT_CONTEXT`
- `annotator_confidence`: `HIGH`, `MEDIUM`, `LOW`
- `adjudication_status`: `UNREVIEWED`, `AGREED`, `ADJUDICATED` (as applicable)

Important discrepancy: the v0.4.2 conformance audit says the schema's `temporal_relations.csv` lacked explicit `evidence_scope`, although v0.4.1 required it. Therefore the reconstructed schema must include it unless a deterministic equivalent is deliberately approved. This is a documented schema defect, not a field that can safely be assumed present in the missing ZIP.

### 3.9 Non-temporal relation labels

The v0.4 draft keeps these separate from temporal edges:
- `CAUSES_OR_ENABLES`
- `DEPENDS_ON`
- `PRECONDITION_OF`
- `NARRATIVE_ORDER_ONLY`

### 3.10 Baseline alignment labels

The v0.4 draft names these baseline-alignment outcomes:
- `supported`
- `multiple_candidate_pairs`
- `ambiguous`
- `unmapped`
- `not_assessable`

The exact register/column that stores these values in the missing v0.4.2 package is unknown.

---

## 4. Exact v0.3 public template headers (confirmed, not the target schema)

The current public repository has four CSV templates. Their headers are recorded here to make the migration delta explicit.

### 4.1 `report_registry.csv`

```csv
report_id,report_title,source_collection,source_vendor,source_url,publication_date,repository_path,repository_file_sha256,local_source_text_sha256,corpus_release,licence,source_terms_reviewed,source_text_complete,offset_alignment_checked,pilot_inclusion_status,selection_basis,exclusion_reason,annotator_id,reviewer_notes
```

### 4.2 `event_mentions.csv`

```csv
report_id,annotator_id,mention_id,char_start,char_end,mention_text,sentence_id,instance_status,event_instance_id,event_type_text,actor_text,target_text,asset_or_host_text,time_expression,annotator_confidence,adjudication_status,annotator_note
```

### 4.3 `event_mappings.csv`

```csv
report_id,annotator_id,event_instance_id,mapping_id,mapping_status,technique_id,technique_name,attack_version,evidence_span_id,evidence_start,evidence_end,evidence_text,mapping_confidence,annotator_note
```

### 4.4 `temporal_relations.csv`

```csv
report_id,annotator_id,relation_id,event_a_id,event_b_id,relation_label,evidence_span_id,evidence_start,evidence_end,evidence_text,cue_text,argument_support,evidence_scope,annotator_confidence,adjudication_status,annotator_note
```

The v0.3 README establishes these row grains: one report/annotator provenance row; one row per text mention; one row per mapping evidence span (multiple rows may share a mapping ID); and one row per relation evidence span (multiple rows may share a relation ID). It also states that offsets are zero-based, end-exclusive into frozen source text. Do not copy the v0.3 headers into a v0.4 reconstruction and assume the missing activity-unit/scope model has been implemented.

---

## 5. Registers described by the v0.4.2 conformance audit

The audit describes **eight core registers** and **four supporting registers**. The register names below are audit-described; their exact original headers remain unverified.

| Register | Role / fields described by audit | Evidence status |
|---|---|---|
| `report_registry.csv` | Report/source identity; source URL/path; dates; frozen text SHA-256 and character count; extraction/transformation; corpus/split; local/public rights; source-scope eligibility; exposure; report assessability | AUDIT-DESCRIBED — v0.4.2 |
| `report_scopes.csv` | Report-local scope identity and parent scopes; evidence attached through evidence links | AUDIT-DESCRIBED — v0.4.2 |
| `activity_units.csv` | Unit identity, scope, parent hierarchy, granularity, unit role, instance status, count status/bounds, confidence and adjudication | AUDIT-DESCRIBED — v0.4.2 |
| `event_mentions.csv` | Exact mention span, sentence locator, mention kind, activity-unit link, mention status, resolved event ID | AUDIT-DESCRIBED — v0.4.2 |
| `event_mappings.csv` | Exact ATT&CK ID/version, mapping basis, decision status, alternatives/equivalences, baseline vocabulary ID/hash, baseline parent ID/status, evidence links | AUDIT-DESCRIBED — v0.4.2 |
| `time_evidence.csv` | Time type, raw expression/evidence, precision, timezone, normalized interval/status and uncertainty | AUDIT-DESCRIBED — v0.4.2 |
| `temporal_relations.csv` | Distinct endpoint fields, relation label/basis, comparison scope, scope compatibility, confidence, adjudication and linked evidence | AUDIT-DESCRIBED — v0.4.2; audit flags missing explicit `evidence_scope` |
| `candidate_pair_assessments.csv` | Candidate rule ID/version, pair IDs, assessment label, relation link and reason | AUDIT-DESCRIBED — v0.4.2 |
| `evidence_spans.csv` | Supporting evidence spans with frozen-source offsets and locators | AUDIT-DESCRIBED — supporting register |
| `record_evidence_links.csv` | Links evidence spans to records through record type, record ID and evidence role | AUDIT-DESCRIBED — supporting register |
| `non_temporal_relations.csv` | Causal, dependency, precondition and narrative relations kept out of temporal projection | AUDIT-DESCRIBED — supporting register |
| `adjudication_log.csv` | Original values, decisions and final adjudication history | AUDIT-DESCRIBED — supporting register |

The audit says the ZIP contained 15 entries in its checksum manifest. It does not provide a complete, independently recoverable list of all filenames and contents in the materials currently available. Do not infer the exact three non-register packaging filenames or claim to reconstruct the 15-entry archive.

---

## 6. Required reconstruction invariants (must be made executable)

These are requirements from the conformance audit and protocol logic. They are **not proof that the missing v0.4.2 ZIP already implemented them**.

### P0 — primary evidence-model integrity

1. Every record belongs to a single report, annotator, protocol version, schema version and annotation pass. Store version/pass identity in `report_registry` or a mandatory immutable manifest.
2. IDs are unique within the documented report/annotator/register namespace. Every foreign key resolves within the same report and annotator unless an explicit adjudication record documents cross-annotator linkage.
3. Evidence spans use zero-based, half-open character offsets into the exact frozen source text. The registry freezes source hash, character count, extraction/transformation and the exact text representation against which offsets were made.
4. Every mention links to an activity unit. Mention-level status and unit-level status are separate; the protocol must define which status controls event graph eligibility and which mismatches are allowed.
5. A resolved event leaf must satisfy `unit_role=event_leaf`, `granularity=atomic_event`, `instance_status=RESOLVED`. For a resolved leaf, the event-instance identifier must be identical to its activity-unit identifier if the researcher adopts the v0.4.2 audit's described identity convention.
6. Container roles (`series_container`, `episode_container`, `aggregate_container`) cannot be primary event-graph endpoints. Container parents and child units must have valid same-report references and an acyclic hierarchy.
7. A primary temporal relation has distinct endpoints, both eligible event leaves, an explicit comparison scope, compatible scope, relation-specific evidence, `evidence_scope`, and `relation_basis` equal to `direct_source` or `direct_timestamp`.
8. `derived_transitive`, `inference`, `unresolved`, `NO_TEMPORAL_CLAIM`, `VAGUE_OR_AMBIGUOUS`, and `NOT_ASSESSABLE` are not primary positive graph edges.
9. `A_120` membership must be validated against an immutable selected-120 vocabulary file and hash. Only accepted and source-supported mappings enter `A_120`; `workbook_only` and alternative-only mappings do not.
10. Candidate-pair assessments remain separate from positive temporal relation discovery. A missing pair assessment does not imply a negative relation.

### P1 — evidence, time and cross-register consistency

1. Define whether a direct `evidence_span_id` is the primary span and `record_evidence_links` holds additional spans, or standardize to one approach. Reject accidental duplicate evidence attachments under a declared policy.
2. Define a unique evidence-link key. Preferred reconstruction: add `link_id`; alternatively define and validate a composite key over report, annotator, record type/ID, span ID and evidence role.
3. Freeze complete `record_type` and `evidence_role` enums, including report-level eligibility evidence.
4. Candidate-pair assessment rows must have a deterministic compatible-scope rule and retain the candidate-generation rule/version.
5. Non-temporal relation endpoints must be typed as activity units if containers/episodes may be connected; otherwise explicitly restrict and validate them as event leaves.
6. Retain raw time text and precision alongside normalized intervals. A timezone-uncertain time may support strict ordering only when the order is invariant over its allowed uncertainty interval.
7. Keep original adjudication values and final adjudicated values; do not silently overwrite annotator decisions.

---

## 7. Proposed reconstructed register model (implemented provisionally as RECON v0.1, not v0.4.2)

The following model is recommended for a new, clearly named reconstruction (for example, `CTI_Annotation_Schema_RECON_v0.1`). It is a design proposal and must not be represented as the exact missing original.

1. `report_registry`: one row per report × annotator × annotation pass; source identity, source and frozen-text hashes, corpus/split, extraction transformation, rights gates, source-scope eligibility, assessability, exposure, protocol/schema/pass identity.
2. `report_scopes`: one row per report-local scope and annotator; scope ID/type, parent scope, description, evidence links/locator, confidence, adjudication and status.
3. `activity_units`: one row per report-local activity unit and annotator; unit ID, scope ID, optional parent unit, granularity, unit role, instance status, count status and bounds, source summary, confidence and adjudication.
4. `event_mentions`: one row per mention span; mention ID, exact offsets/text, sentence/section locator, mention kind, activity-unit ID, mention-level status and resolved event ID where applicable.
5. `evidence_spans`: one row per exact source evidence span; span ID, report/annotator, offsets, exact text, sentence/section/figure locator and source hash linkage.
6. `record_evidence_links`: one row per evidence-to-record link; unique link ID, report/annotator, record type/ID, evidence span ID and evidence role.
7. `event_mappings`: one row per event-to-technique mapping decision (evidence spans attached by link register); exact technique/sub-technique ID/name, ATT&CK release, mapping basis, accepted/alternative/rejected decision, alternative group/reference, confidence, A_120 vocabulary ID/hash, baseline parent ID and baseline membership/status.
8. `time_evidence`: one row per typed time observation; raw expression, time type, precision, timezone, normalized interval bounds, normalization status/uncertainty, source span and event/activity-unit association where known.
9. `temporal_relations`: one row per event-pair relation; relation ID, distinct event endpoints, comparison scope ID, scope compatibility, relation label, relation basis, evidence scope, confidence and adjudication.
10. `candidate_pair_assessments` (optional): one row per assessed candidate pair under a frozen rule; candidate rule ID/version, endpoints, scope rule/status, assessment label, related positive relation ID and reason.
11. `non_temporal_relations`: one row per causal/dependency/precondition/narrative relation, with endpoint typing appropriate to the allowed unit granularity and separate evidence.
12. `adjudication_log`: append-only decision history with target register/record, original value, proposed/final value, rationale, reviewer/annotator, timestamp and links to evidence as appropriate.

The separate `CTI_Annotation_Schema_RECON_v0.1` package now contains explicit **proposed** CSV headers and a matching field dictionary, controlled vocabularies, data model, validator and synthetic tests. Those headers are not frozen or researcher-approved. They are a newly designed reconstruction, not recovered v0.4.2 source code or metadata.

---

## 8. Exact unknowns that remain blocked by missing originals

The following cannot be honestly recovered from the current sources:

- exact v0.4.2 header strings and column order for all 12 registers;
- exact original field dictionary wording and all optional/required markers;
- exact `record_type` and `evidence_role` enums;
- exact mapping decision-status and baseline-status enums;
- exact report-assessability enum and how it interacts with source eligibility/local-use eligibility;
- exact candidate-pair assessment labels and rule-version key design;
- exact non-temporal relation endpoint key names and allowed endpoint granularity;
- whether source evidence is represented by direct span columns, link rows, or both in each register;
- exact evidence-link unique-key policy;
- exact selected-120 vocabulary file as originally bundled (if any) in the missing v0.4.2 ZIP. However, the operational ChronoCTI source file has now been identified at `temporal-learner-code/selected_techniquesWName.json` in pinned commit `4906a0a5e399b6e2aa10435fd6e3894e041e4549`, Git blob SHA `ca14535ad0b67af4c8297707b4c134c9de2d577f`; it contains 120 unique IDs. A derived ID-only artifact is available in the reconstruction package with SHA-256 `97b599ffdcfcc5864a9352cf1467de0f6cac92f9141053a76098e4f2d33fb1bc`. The exact original package-v0.4.2 inclusion and any v0.4.1 reference string remain unknown.
- exact filenames of all 15 ZIP entries;
- whether the missing Protocol v0.4.1 changed any of the recovered v0.4 rules.

Do not fill these gaps by assuming typical database conventions or by copying guessed column names into production code.

---

## 9. Current implementation gate and next sequence

The separate `CTI_Annotation_Schema_RECON_v0.1` package has now been built locally. It contains 12 blank proposed CSV registers, field dictionary, controlled vocabularies, data-model rules, the derived pinned A_120 ID list, structural validator, projection module, annotation-to-projection adapter, synthetic QA report, manifest and checksums. The combined 39-test synthetic suite passes. This completes the current technical prototype block, not protocol approval or annotation readiness.

1. Researcher reviews the `CTI_Evidence_Lab_Researcher_Decision_Register_v0.1.md` and either approves or revises the choices, especially the primary relation-label scope, assessable denominator/missingness policy, A_120 mapping level, source-evidence requirements, and evidence-scope handling.
2. Reconcile approved choices against the exact originals if Protocol v0.4.1 / Schema v0.4.2 are recovered. If they remain missing, approve RECON explicitly as a new schema/protocol version; never relabel it as the original v0.4.2.
3. Freeze headers, controlled vocabularies, source normalization, offset semantics, ID namespace, report/annotator/pass identity, version manifest, and annotation-lock format.
4. Record the five researcher source-scope and local-use eligibility decisions separately. Public-reuse rights remain a separate status. Current status is 0/5 decisions.
5. Only after these gates are complete should source-first human annotation begin. The fail-closed adapter may project only a structurally valid, explicitly human-locked report/annotator/pass snapshot. No AI triage content becomes a human label.
6. Keep the five-report pilot feasibility-only. It cannot support prevalence; a larger probability-sampling design would require separate pre-specification and sample-size justification.

---

## 10. Provenance references

- Recovered protocol: `CTI_Event_Instance_Annotation_Protocol_v0.4-draft.md` (local recovery; SHA-256 `52ba0e094a322f8b8454cfedea0ce4589c7c729f1bbb99e6d28f02147f86bb76`).
- Migration note: `CTI_Protocol_v0.4_Migration_Note.md` inside `CTI_Evidence_Lab_Baseline_and_Protocol_Kit_v0.2.zip`.
- Conformance audit: `CTI_Annotation_Schema_v0.4.2_Conformance_Audit_v0.1.md` (available; multiple uploads are duplicates).
- Project-wide audit: v1.4 (newer than the duplicate uploaded v1.1 audits).
- Public v0.3 templates: `https://github.com/sanketnichit/cti-evidence-lab/tree/main/research/templates`.
- Public v0.3 validator: `https://github.com/sanketnichit/cti-evidence-lab/blob/main/src/annotation_validation.py`.

**End of specification.** This document is a reconstruction aid, not a claim of exact recovery.


## 9. Reconstruction package and synthetic validation status

A separate `CTI_Annotation_Schema_RECON_v0.1.zip` has now been assembled. It contains 12 proposed blank CSV registers, field dictionary, controlled vocabularies, data-model rules, the derived pinned A_120 ID list, a structural validator, a provisional projection-metrics module, a fail-closed annotation-to-projection adapter, and a synthetic test suite. The validator passed 18 synthetic tests, the projection module passed 13, and the annotation-to-projection adapter passed 9 (**40/40 total**). Python compilation passed for all package modules. The blank-package validation correctly produces zero errors and one explicit empty-bundle warning. This verifies package structure and the tested invariants only; it does not validate human semantics, approve the reconstruction, or replace the missing original v0.4.2 ZIP / v0.4.1 protocol.
