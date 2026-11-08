# CTI Evidence Lab — Metric Contract v0.1 (provisional)

**Prepared:** 8 November 2026  
**Status:** Updated working metric specification, aligned to the 8 November 2026 attack-action event-universe decision. Not approved, frozen, or computed on real AnnoCTR human annotations.  
**Inputs reconciled:** Protocol v0.4-draft; Project-wide Consistency Audit v1.4; AnnoCTR Sampling Method v0.3.2; Five-report Re-audit and Sampling Correction v0.1.  
**Version caveat:** Exact Protocol v0.4.1 and the original Schema v0.4.2 ZIP remain unrecovered. This note is a provisional metric contract, not a claim that those original artifacts were inspected.

---

## 1. Purpose and measurement boundary

This contract separates three things that must not be collapsed into one statistic:

1. **Report-level occurrence/relation outcome:** what an eligible, assessable CTI report explicitly supports about distinct report-local atomic attack-action occurrences in the primary stratum; other strata are described separately.
2. **ATT&CK mapping overlap:** whether accepted parent-level mapping sets for the two occurrences share a technique in the pinned ChronoCTI 120-technique vocabulary.
3. **Projection consequence:** what happens when a source-supported event relation is represented using distinct technique pairs, which cannot retain a same-technique diagonal pair.

No combined “information-loss percentage” is defined. Report counts, event-edge counts, event-to-technique mapping combinations, and unique projected technique-pair counts have different units.

## 2. Primary analysis unit and mapping level

### 2.1 Eligible event endpoints

The primary event graph contains only activity units satisfying all of the following:

- `unit_role = event_leaf`;
- `granularity = atomic_event`;
- `instance_status = RESOLVED`;
- `activity_stratum = ATTACK_ACTION`;
- distinct endpoint identities;
- both endpoints belong to compatible, explicitly recorded comparison scopes.

Series, episodes, aggregates, generic behaviour, unresolved units, and resolved event units in non-primary strata remain in the annotation data. They are not converted into primary attack-action event leaves and are not included in primary event-pair or edge denominators. Resolved non-primary strata may be reported in separate descriptive results.

**Schema prerequisite:** the current RECON v0.1/v0.2/v0.3 packages have no canonical `activity_stratum` field. The endpoint rule above is the adopted target definition, not an implemented validator guarantee. No metric may be computed until a successor schema adds this field, its controlled vocabulary, and validator/projection-adapter checks for non-primary and mixed-stratum endpoints.

### 2.2 Primary ATT&CK mapping set: `A_120`

For each resolved atomic event leaf `v` classified as `ATTACK_ACTION`, define `A_120(v)` as the set of accepted, source-supported parent-level ATT&CK technique IDs for that event that belong to the pinned 120-technique ChronoCTI vocabulary. An unmapped attack-action remains in the event inventory but cannot contribute to ATT&CK-pair projection inputs.

Rules:

- Only accepted, source-supported mapping decisions enter `A_120`.
- `workbook_only`, rejected, unresolved, or merely alternative mappings do not enter the primary set.
- Preserve exact technique/sub-technique mappings separately as `A_exact` (or the schema's equivalent exact-ID field).
- Primary report rates and projection metrics use `A_120` for comparability with the ChronoCTI distinct-technique-pair representation.
- Exact/sub-technique overlap may be reported as a separate sensitivity analysis; do not mix it into the primary `A_120` result.

**Vocabulary source now recovered for the reconstruction:** the ChronoCTI temporal learner uses `temporal-learner-code/selected_techniquesWName.json` in repository commit `4906a0a5e399b6e2aa10435fd6e3894e041e4549` (Git blob SHA `ca14535ad0b67af4c8297707b4c134c9de2d577f`). It contains 120 unique IDs. The same ID/name order was verified in the `TimeML`, `apriori-features`, and `Neuralcoref` copies. An ordered ID-only extraction is now saved as `A_120_ChronoCTI_Selected_Technique_IDs_derived_v0.1.json`, SHA-256 `97b599ffdcfcc5864a9352cf1467de0f6cac92f9141053a76098e4f2d33fb1bc`. This is a derived membership artifact, not the original ChronoCTI JSON and not a component of the missing v0.4.2 ZIP. The original audit's ZIP-bundling caveat remains true; the reconstruction package now references the external pinned source and includes the derived ID list. Before annotation, preserve both the source commit/blob reference and the derived artifact's SHA-256 in every manifest.

## 3. Positive temporal relation scope

### 3.1 Primary positive relation labels

For the broad research question about temporal relations, count these five labels as positive when directly supported:

- `BEFORE`
- `AFTER`
- `OVERLAP`
- `SIMULTANEOUS`
- `CONCURRENT_UNSPECIFIED`

A qualifying positive relation must additionally satisfy:

- `relation_basis` is `direct_source` or `direct_timestamp`;
- both endpoints meet the primary event-endpoint rules in §2.1, including `activity_stratum = ATTACK_ACTION`;
- the relation has relation-specific evidence and a recorded evidence scope;
- the endpoints have compatible comparison scope.

`derived_transitive`, `inference`, and `unresolved` are not primary positive relations. They may be retained in separate derived, exploratory, or adjudication records.

### 3.2 Strict-order subset

Only `BEFORE` and `AFTER` enter strict precedence analysis. In a derived analysis view, normalize `AFTER(A,B)` to `BEFORE(B,A)` while retaining the original annotation label and endpoint order.

`OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` count in broad temporal-relation incidence, but never enter strict-order cycle detection.

### 3.3 Non-positive and unassessed states

- `NO_TEMPORAL_CLAIM` is permitted only for a pair actually assessed within a frozen candidate-pair assessment rule. It is not the default label for every pair without an edge.
- `VAGUE_OR_AMBIGUOUS` and `NOT_ASSESSABLE` are not positive relations and remain distinct.
- An unrecorded pair is **unassessed**, not a negative example.
- Causal, dependency, precondition, and narrative-order-only relations stay in a separate non-temporal register.

## 4. Report-level denominators and missingness

Use two report denominators rather than quietly dropping non-assessable cases.

### 4.1 Eligible reports (`N_eligible`)

Reports that pass the researcher's source/scope eligibility and local-research-use gates. Public redistribution permission is tracked separately and does not automatically determine local annotation eligibility.

### 4.2 Assessable eligible reports (`N_assessable`)

An eligible report enters `N_assessable` when at least one eligible human annotation partition records a complete/readable frozen source, `report_assessability = ASSESSABLE`, and `full_report_review_status = COMPLETE`, and no unresolved cross-partition conflict remains in source/scope eligibility, local-use permission, or report assessability.

Count each report once, not once per annotator or annotation pass. When multiple passes or annotators exist, calculate report-level outcomes from the designated locked final annotation or agreed/adjudicated consensus partition; do not sum outcomes across passes. An incomplete auxiliary or second-annotator pass does not duplicate or negate a report that already has a completed qualifying review, but agreement status must be reported separately. The primary report-level rate uses `N_assessable` as its denominator. Report assessability coverage is always disclosed as `N_assessable / N_eligible`. Public-reuse permission is tracked separately and is not part of the local-use denominator gate.

A report with zero resolved atomic `ATTACK_ACTION` event leaves can still be assessable. If its source and full-report review meet the conditions above, it remains in `N_assessable`, receives zero for the primary attack-action outcomes, and is separately classified as having no primary event-leaf opportunity. Resolved non-primary events do not change that primary zero. This is an important study outcome, not an exclusion reason.

A report marked `NOT_ASSESSABLE` or `PENDING`, or one whose full-report review is `NOT_STARTED` or `IN_PROGRESS`, is not counted in `N_assessable`. It remains visible in the assessability-coverage and missingness tables and is never silently recoded as a zero-edge report. A report that fails source/scope or local-use eligibility is outside `N_eligible` and must have a documented reason. Conflicting report-level decisions across annotator/pass partitions are excluded until adjudicated.

**Five-report limitation:** these denominators describe a feasibility sample. They do not support corpus or vendor prevalence estimates or conventional population-level confidence intervals.

## 5. Report-level outcome indicators

For each assessable eligible report `r`, calculate separate binary indicators.

### 5.1 Event-leaf presence

`I_event(r) = 1` if the report contains at least one resolved atomic `event_leaf` classified as `ATTACK_ACTION`; otherwise 0.

### 5.2 Compatible event-pair opportunity

`I_pair(r) = 1` if there exists at least one pair of distinct resolved atomic `ATTACK_ACTION` event leaves in a compatible comparison scope; otherwise 0.

### 5.3 Same-technique pair opportunity

`I_shared_pair(r) = 1` if there exists at least one compatible pair `(u,v)` for which:

`A_120(u) ∩ A_120(v) ≠ ∅`.

**Same-technique pair-opportunity report rate**:

`sum(I_shared_pair(r)) / N_assessable`

This is the corrected name for the protocol's earlier “repeated-occurrence report rate”. It measures opportunity only; it does not require a temporal relation.

### 5.4 Positive temporal-relation presence

`I_temporal(r) = 1` if at least one qualifying positive temporal relation (any of the five labels in §3.1) exists between distinct compatible `ATTACK_ACTION` event leaves; otherwise 0. Relations in non-primary strata are summarized separately.

This is a descriptive secondary rate:

`sum(I_temporal(r)) / N_assessable`.

### 5.5 Primary within-technique temporal-relation outcome

`I_within_tech_temporal(r) = 1` if at least one qualifying positive temporal relation `(u,v)` between `ATTACK_ACTION` endpoints exists and:

`A_120(u) ∩ A_120(v) ≠ ∅`.

**Primary within-technique temporal-relation report rate**:

`sum(I_within_tech_temporal(r)) / N_assessable`

This is the report-level outcome most directly aligned with the candidate research question. Report its numerator and denominator, plus a label breakdown (`BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, `CONCURRENT_UNSPECIFIED`). A report is counted once in the binary numerator even if it contains multiple qualifying relations.

### 5.6 Conditional descriptive rates

Also report, without substituting them for the primary rate:

- `reports with I_within_tech_temporal = 1 / reports with I_shared_pair = 1`;
- `reports with I_temporal = 1 / N_assessable`;
- `reports with I_event = 1 / N_assessable`;
- `reports with I_pair = 1 / N_assessable`.

These help distinguish “no event opportunity”, “same-technique opportunity but no positive relation observed”, and “positive relation with shared technique”. All rates above use only the primary `ATTACK_ACTION` stratum; report communication, analyst-observation, and other non-primary stratum counts/relations separately and do not combine them with these numerators or denominators.

## 6. Event-edge-level projection metrics

Count each source event relation once for event-edge metrics, irrespective of how many technique mappings it expands into. Keep a separate count for mapping-pair combinations.

For each qualifying positive temporal `ATTACK_ACTION` event edge `e=(u,v)`, construct a relation-aware mapping image from `A_120(u)` and `A_120(v)`. Do not include non-primary or mixed-stratum edges in this projection:

- directed ordered pairs for `BEFORE` and `AFTER`;
- canonical unordered technique dyads for `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED`.

Split mapping combinations into:

- diagonal: shared technique IDs `(t,t)` where `t ∈ A_120(u) ∩ A_120(v)`;
- distinct: technique pairs where the two technique IDs differ.

Classify each positive temporal event edge into exactly one projection status:

1. `unmapped_endpoint`: one or both endpoints have no accepted `A_120` mapping; keep outside the mapped-edge denominator.
2. `fully_omitted`: both endpoints are mapped, shared-technique diagonal combinations exist, and no distinct technique pair remains.
3. `partially_represented`: both diagonal and at least one distinct technique pair exist.
4. `no_diagonal_mapping`: both endpoints are mapped, but their `A_120` sets do not intersect; all projected pairs are distinct-technique pairs.

For all mapped positive event edges (statuses 2–4), report:

- **Full omission rate** = `fully_omitted edges / mapped positive event edges`.
- **Partial representation rate** = `partially_represented edges / mapped positive event edges`.
- **No-diagonal rate** = `no_diagonal_mapping edges / mapped positive event edges`.
- **Same-technique endpoint rate** = `(fully_omitted + partially_represented) / mapped positive event edges`.

For the subset of positive event edges whose endpoint mapping sets intersect, the outcome is necessarily either `fully_omitted` or `partially_represented`. `no_diagonal_mapping` applies only to the disjoint-mapping subset.

Separately report **diagonal mapping share**:

`number of diagonal event-edge-to-technique-pair combinations / all event-edge-to-technique-pair combinations`.

This is a mapping-combination statistic, not an event-edge rate. Never substitute one for the other.

## 7. Technique-pair collision/conflation

For every projected technique pair, retain provenance to all distinct source event-edge IDs that generated it. Report separately by relation type/orientation:

- number of unique projected technique pairs;
- number of projected pairs supported by more than one distinct source event edge;
- excess edge multiplicity (sum over pairs of `number_of_source_edges - 1`);
- pairs receiving conflicting temporal labels;
- collisions in the target distinct-technique-pair representation only (exclude diagonal combinations from that count).

Do not count a collision among diagonal-only combinations as a collision retained by the target distinct-pair graph. Do not conflate one event edge expanding to multiple mapping pairs with multiple source event edges colliding onto one pair.

## 8. Strict-order cycle diagnostics

Cycle analysis uses only normalized strict-order `BEFORE` edges, including original `AFTER` relations converted in the derived view. Before a technique-level cycle is interpreted as projection-induced:

1. the event-instance strict-order graph must be acyclic;
2. endpoints must pass all primary endpoint/scope rules;
3. diagonal pairs are excluded from the distinct-technique graph but counted separately as projection omission;
4. each projected strongly connected component retains provenance to its source event edges.

Distinguish:

- cycles caused by mapping fan-out from a single source event edge; and
- cycles requiring two or more distinct source event edges.

A single-edge mapping-fanout cycle is not evidence of repeated event occurrences. ChronoCTI workbook `NEXT` cycles remain a separate benchmark observation, not source-level temporal truth.

## 9. Coverage and missingness outputs

Every report summary should include, at minimum:

- source/scope eligibility status and reason;
- local research-use status;
- public-reuse status separately;
- report assessability status;
- full-report review completion status;
- count of mentions by status;
- count of activity units by granularity, role, and instance status;
- resolved atomic `ATTACK_ACTION` event-leaf count;
- resolved counts for each non-primary `activity_stratum` separately;
- count of compatible `ATTACK_ACTION` event-leaf pairs;
- count of same-technique pair opportunities;
- positive temporal edge count by label and relation basis;
- ambiguous, unresolved, inferred, transitive, and not-assessable relations separately;
- accepted `A_exact` and `A_120` mapping coverage;
- mapped and unmapped positive event-edge counts;
- evidence-span validation status.

Missing annotation rows never become automatic negative labels. The full-report source pass is a positive-relation discovery process; optional candidate-pair assessments have their own frozen pair-generation rule and coverage statement.

## 10. Decision status and approval boundary

This v0.1 contract contains design choices with different decision states:

1. Primary mapping level is `A_120`; `A_exact` is a separately reported sensitivity analysis — **adopted as the working project default on 4 November 2026; the exact-to-parent crosswalk remains a technical gate**.
2. Primary within-technique temporal incidence includes all five directly supported positive temporal labels in §3.1 — **adopted as the working project default on 4 November 2026 under delegated direction**.
3. Strict cycle analysis uses only `BEFORE`/`AFTER` after documented normalization — **source-grounded rule; synthetic implementation corrected**.
4. Primary report-level denominator is `N_assessable`; assessability coverage is `N_assessable / N_eligible` — **adopted as the project default on 4 November 2026 under delegated decision**.
5. A report with zero resolved atomic `ATTACK_ACTION` event leaves remains in `N_assessable` only when source/scope and local-use eligibility pass, report assessability is `ASSESSABLE`, and at least one eligible full-report review is `COMPLETE`; `NOT_ASSESSABLE`, `PENDING`, incomplete review and unresolved conflicts are disclosed separately, never recoded as zero. Resolved non-primary events do not change the primary zero — **adopted with the denominator rule**.
6. Pair opportunity and positive temporal-relation outcomes remain separate — **recommended; metric naming/formula approval pending**.

Adopting the denominator rule does not approve or freeze this entire metric contract, protocol, or RECON schema. No real-report metric may be computed until the remaining protocol/schema decisions, exact `A_120` vocabulary artifact, report eligibility decisions and validator gates are resolved.

## 11. Implementation acceptance tests implied by this contract

The future validator / metric adapter must reject or flag:

- an edge with the same event ID at both endpoints;
- container, series, episode, aggregate, generic, or unresolved endpoints in the primary graph;
- event endpoints in incompatible or missing comparison scopes;
- a primary relation or projection input without an explicit `activity_stratum = ATTACK_ACTION` value on both endpoints;
- relation bases other than `direct_source` or `direct_timestamp` entering primary positive-edge counts;
- `NO_TEMPORAL_CLAIM` without a declared candidate-pair assessment frame;
- `workbook_only`, rejected, alternative-only, or out-of-vocabulary mappings entering `A_120`;
- an `A_120` mapping whose ID is not present in the pinned selected-120 vocabulary;
- an otherwise assessable report with `full_report_review_status` other than `COMPLETE` entering `N_assessable`;
- `OVERLAP`, `SIMULTANEOUS`, or `CONCURRENT_UNSPECIFIED` entering strict-order cycle analysis;
- missing or incomplete annotation rows being interpreted as negative event-pair labels;
- projection calls with self-event edges.

Synthetic tests must also verify the four mutually exclusive projection statuses, label-specific orientation rules, collision provenance, and the distinction between event-edge counts and mapping-combination counts.

---

## Source basis and limitations

- `CTI_Event_Instance_Annotation_Protocol_v0.4-draft.md` supplies the current available temporal labels, directness rules, endpoint rule, projection definitions, and initial metric list.
- `CTI_Evidence_Lab_Project_Wide_Consistency_Audit_v1.4.md` identifies the required separation between pair opportunity and within-technique temporal-relation outcome, the `A_120` mapping-level clarification, the broad positive-label versus strict-order distinction, and the denominator/missingness decision.
- `AnnoCTR_Fresh_MultiVendor_Sampling_Method_v0.3.2.md` supplies the corrected 120-report frame and the rule that event yield or positive temporal edges cannot determine base-sample eligibility.
- `AnnoCTR_Five_Report_Reaudit_and_Sampling_Correction_v0.1.md` confirms that the five rank-1 reports remain candidates and that event enumerability is an outcome, not an eligibility gate.

The exact Protocol v0.4.1 draft and original Schema v0.4.2 ZIP were not recovered. Where this note follows an audit's description of those missing artifacts, that dependency is explicit; this note does not claim to reproduce their exact field names or headers.


## 12. Synthetic implementation status (3 November 2026)

A provisional local implementation now exists in `CTI_Annotation_Schema_RECON_v0.1/analysis/projection_metrics_recon.py`. Its mapping adapter filters to accepted, source-supported, in-vocabulary A_120 parent mappings and excludes alternative, rejected/unresolved, workbook-only, out-of-vocabulary and non-event-unit rows. The projection function enforces distinct event IDs, positive direct relation labels and compatible scope; classifies every event edge into exactly one of `unmapped_endpoint`, `fully_omitted`, `partially_represented`, and `no_diagonal_mapping`; retains all distinct-pair provenance; separates retained-graph collisions from diagonal-only combinations and global label conflicts; and reports strict-order cycle provenance.

A fail-closed adapter now connects the 12-register reconstruction to projection. It isolates one report × annotator × annotation pass, runs the structural validator first, requires source/scope eligibility, permitted local research use, assessability and completed full-report review, selects only resolved atomic `event_leaf` units, builds accepted A_120 mapping sets, and admits only direct positive temporal relations in compatible scope. It also requires explicit annotation-lock confirmation and a non-empty immutable lock reference before projection. This is an operational guard, not a cryptographic authentication of the human reviewer; any future lock reference must point to a real read-only human-approved snapshot.

The full synthetic suite now has **39 passing tests**: 17 schema-validator tests, 13 projection-metric tests and 9 adapter tests. Python compilation passed for all package modules. The header-only bundle check returned zero errors and one expected `EMPTY_ANNOTATION_BUNDLE` warning. No AnnoCTR or prior DFIR report has been processed by the reconstruction; no real annotation rows or research metrics were used. The RECON package is local and has not been integrated into public GitHub. Metric choices and schema decisions remain provisional pending researcher approval.