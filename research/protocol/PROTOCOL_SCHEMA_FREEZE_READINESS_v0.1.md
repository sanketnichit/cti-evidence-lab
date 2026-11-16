# CTI Evidence Lab — Protocol and Schema Freeze Readiness v0.1

**Date:** 16 November 2026  
**Status:** Readiness audit only — NOT APPROVED, NOT FROZEN, NOT READY FOR HUMAN ANNOTATION  
**Applies to:** Protocol v0.5-draft; Metric Contract v0.1; Decision Register v0.2; RECON v0.1 base plus v0.2 temporal/selected-final, v0.3 explicit-scope assignment, and v0.4 activity-stratum extensions.

## 1. Executive status

The main working research-design decisions now have corresponding protocol text, implementation boundaries, and synthetic regression coverage. The remaining problem is no longer an unbounded list of unresolved methodological choices. It is a controlled approval and provenance process:

1. The exact Protocol v0.4.1 and original Schema v0.4.2 files were not recovered. The current package is a reconstruction and must be explicitly accepted as a new replacement package.
2. The researcher must approve the whole protocol, metric contract and reconstructed schema as one coherent versioned package. Individual working decisions do not equal package approval.
3. Five rank-one report eligibility decisions remain 0/5. No human-locked annotations, selected-final report partitions, or real-report projection results exist.
4. The human-rater workflow must be stated for the feasibility pilot. If no independent second annotator is used, report that IAA was not measured.
5. The scope-pair rate gate must remain closed until the incident-bounded rule is formally approved for the frozen analysis package.

**No annotation should begin on the strength of synthetic tests alone.**

## 2. Working decisions reconciled across the documents

The following are adopted working defaults for the pilot. They are not represented as recovered text from the missing original files, nor as approval of the whole package.

| Area | Working rule | Current representation |
|---|---|---|
| Primary event universe | Only resolved atomic `event_leaf` units classified as incident-linked `ATTACK_ACTION` enter the primary graph. Classification is independent of ATT&CK mapping. | Protocol v0.5 §2.5; RECON v0.4 activity-stratum register, lock, validator and projection filter. |
| Primary comparison scope | Use the nearest shared `scope_type=INCIDENT`, `scope_status=RESOLVED` ancestor. A primary positive relation must cite that same scope. Do not invent incident scopes from broader co-membership. | Protocol v0.5 §2 and §7; v0.2 aggregation default; v0.4 projection filter and regressions. |
| Timestamp-derived relations | Timestamp bounds are closed ranges of possible occurrence instants, not action durations. Timestamp-only positives are strict `BEFORE`/`AFTER`; non-strict labels require explicit `direct_source` wording. Accepted bounds normalize to UTC with source timezone preserved. | Protocol v0.5 §4.2.1; timestamp semantics note; v0.2 validator and tests. |
| Time-evidence target linkage | `time_evidence` may point to an activity unit, a mention, or both. A mention resolves to its unit through `event_mentions.activity_unit_id`; both targets must agree when populated. | RECON v0.2 now resolves mention-only time evidence for `direct_timestamp` endpoint checks; RECON v0.4 rejects contradictory dual targets. CI #272 regressions. |
| Alternative mapping groups | Pending groups contain only `ALTERNATIVE` rows. Resolved groups contain one `ACCEPTED` plus `REJECTED` competitors, or all `REJECTED`. Preserve group IDs and rejected rows. Partial/multiple-winner states are invalid. | Protocol v0.5 §3.1; RECON v0.1 validator and regression tests. |
| Episode relations | Retain episode containers and supported time evidence; defer episode-to-episode edges and metrics from the initial pilot. Do not create synthetic atomic event leaves. | Protocol v0.5 §2.5; no episode relation register is added. |
| ChronoCTI pair alignment | Defer record-level benchmark technique-pair to source event-pair alignment. Preserve raw benchmark pair IDs, labels and provenance separately; never treat benchmark edges as source evidence. | Protocol v0.5 §6.3; separate baseline reproduction materials remain the source for raw benchmark records. |
| Explicit-scope sensitivity | RECON v0.3 explicit event-to-scope assignment remains a single-annotator sensitivity only. Multi-annotator consensus/adjudicated use requires a dedicated assignment-adjudication extension. | Protocol v0.5 sensitivity rules; Decision Register rows 22; reconciliation §3.7. |
| Mention kind | Keep required `mention_kind` as short descriptive free text, not an invented controlled enum. It does not determine event identity, stratum, mapping or metrics. | Protocol v0.5 §2.3; RECON field dictionary preserves it as a string because the original enum is unavailable. |
| Report-level metrics | Keep compatible pair opportunity, same-technique opportunity, positive temporal-relation presence and within-technique temporal-relation presence separate. The conditional rate is descriptive, not the primary outcome. | Metric Contract v0.1 §§5–6; RECON v0.2 report-level aggregator. |
| Register/version/lock crosswalk | A technical crosswalk now maps all 12 v0.1 base registers and the 6 v0.2–v0.4 extension/lock registers to their keys, validators, consumers, protocol areas and lock dependencies. It records the sibling v0.3/v0.4 lock relationship. | `research/protocol/PROTOCOL_SCHEMA_REGISTER_VERSION_LOCK_CROSSWALK_v0.1.md`; technical mapping complete, but whole-package field/enum/semantic review remains open. |
| Activity-stratum lock preconditions | RECON v0.4 lock creation and verification revalidate the v0.2 selected-final register against the base report registry and revalidate complete v0.4 stratum coverage. The v0.2 selected-analysis digest still requires source-backed verification through the v0.2 selected-partition adapter before projection. | RECON v0.4 validator/lock CLI; CI #268. This closes the eligibility bypass, not the full package freeze or source/semantic review. |

## 3. Implementation evidence

The latest verified main-branch workflow is GitHub Actions run [#272](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/43873129990), on 16 November 2026, commit `9f1adcb574ee5c66cee2fd97b6c011302a99d0b4`. It passed **266 synthetic test executions**:

- Root repository: 60
- RECON v0.1: 78
- RECON v0.2: 88
- RECON v0.3: 15
- RECON v0.4: 25

The workflow also passed the RECON v0.1 package checksum verification, blank-bundle and extension validators, projection smoke test, and source snapshot packaging. The v0.2 suite now covers mention-only timestamp targets and endpoint-target matching; v0.4 tests dual-target consistency alongside selected-final lock preconditions, base review metadata enums, required-cell checks and conditional report-registry reasons.

These tests validate code paths and synthetic fixtures only. They do not establish semantic validity, human agreement, source eligibility, report findings, or empirical research results.

## 4. Approval and readiness gates still open

| Gate | Evidence/status | Required before |
|---|---|---|
| Accept reconstruction provenance | The exact Protocol v0.4.1 and original Schema v0.4.2 ZIP remain unrecovered. Protocol v0.5 and RECON v0.1-v0.4 are newly consolidated working artifacts. | Formal freeze. The researcher must accept the reconstructed package as a new replacement, not as the missing original. |
| Whole-package field, enum and requiredness review | The 12 RECON v0.1 CSV headers were compared with the field dictionary; shared partition keys are documented centrally and no header mismatch was found. The v0.4 full-package validator now rejects invalid/blank base confidence, adjudication and span-kind values; blank cells for the remaining clearly required fields; and missing conditional report-registry reasons/bases for source eligibility, local-use permission and assessability decisions. Retrieval dates and OUT_OF_VOCAB baseline provenance are also checked. `mention_kind` remains required descriptive free text. | Formal freeze. Complete the remaining semantic crosswalk and researcher review of provisional/reconstructed choices, cross-register meaning, lock dependencies, versions and protocol-to-field fit together. |
| Metric contract approval | Metric Contract v0.1 and the v0.2 aggregator now align on the principal report-level outcomes. The aggregator still requires an explicit scope-pair approval flag before pair-opportunity-dependent rates are enabled. | Formal freeze and before reporting any pair-opportunity rates. |
| Candidate eligibility | Formal researcher/source-scope eligibility decisions remain 0/5. A report cannot be selected merely because it yields useful events or positive edges. | Any source-first annotation of the five candidates. |
| Human annotation workflow | Human-locked annotations: 0. IAA: not measured. The selected-final mechanism supports single-annotator and certain consensus/adjudicated workflows; the v0.3 scope-assignment sensitivity remains single-annotator only. | Before annotation. State whether the first pilot is single-annotator; recruit an independent second annotator only if one is genuinely available and unexposed. |
| Source freeze and identity controls | The validator checks exact source hash/character count and lock references, and v0.4 lock creation/verification now rechecks selected-final eligibility and complete stratum coverage. The v0.2 selected-analysis lock digest must still be independently verified by the v0.2 adapter against the exact frozen source. Lock digests do not authenticate annotator identity or prove that a human review occurred. | Before each annotation pass and selected-final projection. Maintain the source copy, access controls, benchmark reveal discipline and human sign-off record. |
| Novelty and claims | Novelty remains unproven; no real-report results or event graphs exist. | Before any novelty, prevalence, effectiveness or publication-ready claim. |

## 5. Required freeze sequence

1. Review Protocol v0.5, Metric Contract v0.1, Decision Register v0.2, RECON v0.1-v0.4, the protocol/schema reconciliation register and `PROTOCOL_SCHEMA_REGISTER_VERSION_LOCK_CROSSWALK_v0.1.md` as one package.
2. Resolve any remaining differences in headers, requiredness, enum definitions, IDs, lock references, relation/scope rules and metric outputs. The exact original schema must not be silently reconstructed or renamed.
3. Obtain the researcher's explicit acceptance of the reconstructed package as a new replacement for the unavailable originals. Record any edits and the final approved scope.
4. Confirm the human annotation/rater workflow and approve the incident-bounded scope-pair rule for metric purposes.
5. Obtain individual eligibility decisions for candidate reports and freeze their exact local source text with hashes.
6. Create a single freeze manifest containing the exact protocol, metric contract, decision register, all schema-layer versions, code/test versions and SHA-256 digests. Tag the approved package and rerun full CI on that tagged commit.
7. Only then begin source-first human annotation. Preserve the separation between working design decisions, human annotations, selected-final locks and empirical outputs.

## 6. Explicit stop conditions

Do not begin formal annotation or calculate real-report rates when any of the following is true:

- the researcher has not approved the complete reconstructed package;
- any required schema layer or lock/version reference is missing or inconsistent;
- a candidate report has not passed its own eligibility, local-use and source-integrity gates;
- the exact frozen source text cannot be verified;
- a selected-final partition lacks a valid lock and complete review;
- pair-opportunity rates are requested without approval of the selected comparison-scope rule;
- a sensitivity analysis is reported outside its supported workflow (in particular, RECON v0.3 explicit scope assignment with multi-annotator consensus/adjudication);
- synthetic test results are described as real annotation results, IAA, prevalence or evidence of novelty.

## 7. Current research result status

- Rank-one candidate eligibility: **0/5**
- Human-locked annotations: **0**
- Selected-final partitions: **0**
- Real-report projections: **0**
- IAA: **not measured**
- Prevalence estimate: **none**
- Validated novelty claim: **none**

This document is a readiness control, not an approval signature. The project remains in research-design and tooling preparation until the gates above are explicitly satisfied.
