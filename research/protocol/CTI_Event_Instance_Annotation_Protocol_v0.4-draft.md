# CTI Evidence Lab — Event-Instance Annotation Protocol v0.4 (Draft)

**Project:** CTI Evidence Lab  
**Protocol version:** 0.4-draft  
**Date:** 3 November 2026  
**Status:** Consolidation draft — not frozen, not human-approved, not validated  
**Replaces for future pilot work:** neither v0.2 nor v0.3 until the researcher approves and tags this version  
**Primary purpose:** a source-grounded, reproducible descriptive study of report-local activity identity, temporal relations, and ATT&CK technique projection.

> **Important:** This protocol does not turn the existing AI-assisted three-case reconstructions into gold labels. The cases `r-dfir-1`, `r-dfir-8`, and `r-dfir-2` are protocol-development material and have already been exposed to prior AI-assisted analysis. They must not be described as a blind human first pass.

---

## 1. Research question and boundaries

### 1.1 Provisional research question

Across a transparently sampled set of cyber threat intelligence (CTI) reports, how often does a report explicitly support a temporal relation between two distinct, resolved activity occurrences that share one or more ATT&CK technique mappings, and what occurrence identity or temporal information is retained, partially represented, or lost when those occurrences are projected to a representation that permits only distinct technique pairs?

This is a candidate empirical question, not an established novelty claim.

### 1.2 What this study is and is not

The initial study is descriptive. It does not require a learned classifier.

The study may establish:

- whether the annotation scheme can distinguish mentions, occurrences, series, episodes, and aggregates;
- how often sampled reports explicitly describe repeated, distinct occurrences mapped to the same technique;
- which positive, evidence-supported temporal relations are omitted or partially represented by a distinct-technique-pair projection;
- how occurrence granularity, multiple mappings, scope, and missing evidence affect that projection;
- where technique-level cycles are consistent with a multi-edge event projection, mapping fan-out, or remain unexplained.

The study must not claim from the current three purposively selected cases:

- population prevalence of repeated same-technique occurrences or projection loss;
- that all ChronoCTI cycles are caused by occurrence collapse;
- that all source units are atomic events;
- inter-annotator reliability from AI assistance or a single annotator;
- one-to-one identity between a ChronoCTI technique-pair row and a source event pair;
- a validated contribution or publication-ready novelty claim.

### 1.3 Existing three-case set

`r-dfir-1`, `r-dfir-8`, and `r-dfir-2` remain a **protocol-development / mechanism-exploration set**. Their prior reconstructions and benchmark status have already been examined. They can be used to test definitions, scripts, and reporting, but not as a clean blind validation sample or a prevalence sample.

The separate six-case alias kit (`CASE_01`–`CASE_06`) is not automatically a fresh blind set for the researcher: several reports in it have appeared in prior AI-assisted analyses. An independent human annotator who has not seen those analyses may still use the packets under a controlled procedure, but the researcher must disclose the prior exposure.

---

## 2. Core units: keep the levels separate

### 2.1 Report

The frozen source document used as one annotation unit. Record its stable report ID, title, publisher/vendor, source URL or archive path, retrieval/publication dates, source hash, language, and licence/usage status.

### 2.2 Scope

A scope is the context in which two activities can reasonably be compared. Possible scopes include incident, campaign, actor operation, victim organisation, host, or a report-level aggregate.

- Different hosts do not automatically imply different incidents.
- A report can combine multiple incidents, campaigns, actors, victims, or historical periods.
- Do not force every statement into one coherent timeline.
- Record evidence and uncertainty for scope boundaries.
- A temporal relation whose endpoints are not comparable in scope is not a positive edge in the primary within-scope event graph.

### 2.3 Text mention

A text mention is a span or reference that describes an action or activity. Multiple mentions may refer to one occurrence. Repeated wording does not itself prove repeated execution.

### 2.4 Event instance

An event instance is one distinguishable report-local occurrence. A technique, tool, malware family, actor, host, sentence, or mention is not itself an event instance.

Use `instance_status`:

- `RESOLVED` — the report supports one particular report-local occurrence.
- `UNRESOLVED` — the report describes activity, but the identity or number of underlying occurrences cannot be determined.
- `GENERIC_BEHAVIOUR` — the report describes a capability, modus operandi, or recurring pattern without asserting a particular report-local occurrence.
- `NOT_AN_EVENT` — the span is not an action/event mention.

Only `RESOLVED` event instances may enter the primary event-instance graph. Keep unresolved, generic-behaviour, and non-event mentions in separate counts.

### 2.5 Activity-unit granularity and unit role

Granularity and event-instance status are separate fields. A source can describe a broad activity unit without resolving its underlying atomic events.

Use exactly one `granularity` value for each activity unit:

- `atomic_event` — one distinguishable occurrence supported by the report;
- `repeated_event_series` — repeated activity is asserted, but individual executions or exact count are not separable;
- `activity_episode` — a bounded time period or phase that may contain multiple executions;
- `report_level_aggregate` — a summary spanning multiple hosts, actors, incidents, campaigns, or periods;
- `unresolved` — the available evidence does not support a more specific unit.

Also record a `unit_role`:

- `event_leaf` — a resolved atomic occurrence eligible for the primary event-instance graph;
- `series_container` — a grouping parent for one or more repeated actions; not itself an additional execution;
- `episode_container` — a period/phase container; not automatically an atomic event;
- `aggregate_container` — a report-level grouping; not an atomic event;
- `unresolved_unit` — a unit whose identity/granularity remains unresolved.

**Primary graph rule:** only resolved `event_leaf` units with `atomic_event` granularity enter the primary event-instance graph. `series_container`, `episode_container`, and `aggregate_container` units are retained and analysed separately. They must not be pooled with atomic event instances in a primary occurrence count or edge denominator. Episode-level analyses may be reported as a clearly separate exploratory/sensitivity view.

If a repeated series can be decomposed into separately identifiable occurrences, create event-leaf children and keep a series container as their parent. If the report does not distinguish the executions, retain one series container and do not invent child event IDs.

### 2.6 Count status

Record count separately from granularity:

- `exact`
- `minimum`
- `range`
- `qualitative_only`
- `unknown`

Unknown is a valid result, not a missing number to be guessed. Do not infer one execution per day, host, command, or mention.

---

## 3. ATT&CK mapping

### 3.1 Mapping multiplicity

An event leaf may have zero, one, or multiple evidence-backed ATT&CK mappings. Every mapping is a separate record with its own evidence and confidence. Multiple mappings do not create multiple events.

Required mapping fields:

- `mapping_id`
- `event_instance_id`
- `technique_id`
- `technique_name`
- `attack_version`
- `mapping_basis`
- `mapping_evidence_spans`
- `mapping_confidence`
- `alternative_mapping_ids` / note, where appropriate

Use `mapping_basis`:

- `report_explicit_subtechnique`
- `report_explicit_parent`
- `source_supported_analyst_candidate`
- `workbook_only`
- `unresolved`

A technique appearing only in the ChronoCTI workbook is `workbook_only`; it is not automatically supported by the source report. Malware family names or tool names alone are not enough to force a technique mapping.

### 3.2 Baseline-compatible mapping

For the primary ChronoCTI comparison:

- preserve the source-supported technique/sub-technique mapping;
- separately record the parent-level technique ID used by ChronoCTI's selected vocabulary;
- pin and record the exact 120-technique list and its SHA-256;
- do not silently map a newer technique or sub-technique into the baseline vocabulary if the mapping is unsupported;
- treat parent/sub-technique collapsing as a sensitivity analysis, not an implicit transformation.

The current supplied selected-technique file contains 120 top-level technique IDs. The archive SHA and selected-list SHA are recorded in the baseline audit package.

### 3.3 ChronoCTI label/provenance caution

The paper uses `BEFORE`, `SIMULTANEOUS-OVERLAP`, `CONCURRENT`, and `NULL`; the released workbook uses `NEXT`, `OVERLAP`, `CONCURRENT`, and blank relation cells. Preserve the literal source label and maintain a separate, documented normalization map. Do not silently assume `NEXT` or blank is equivalent to a paper label without recording the code path and uncertainty.

For the current baseline comparison, record `NEXT` as a directed benchmark relation from workbook `T1` to `T2`; the released graph code creates that directed edge. Its relation to the paper's conceptual `BEFORE` label is a **baseline normalization hypothesis**, not a human source annotation and not proof that every `NEXT` edge is a physically strict chronology claim. Therefore:

- retain `benchmark_relation_raw = NEXT` in all baseline records;
- store any `NEXT` → `BEFORE-like` normalization in a separate field with its rationale and status;
- call cycles calculated from the workbook the **ChronoCTI NEXT-graph cycles**;
- reserve **strict BEFORE/AFTER event-graph cycle** for human-annotated, source-evidenced strict temporal relations;
- do not use a benchmark `NEXT` edge as evidence that a particular pair of report-local event instances occurred in that order.

The focused baseline audit found:

- 7,140 unordered distinct-technique dyads in the paper's formula;
- 14,280 ordered orientations in the released graph-generation loop;
- zero diagonal same-technique pairs;
- 11 raw workbook keys with multiple nonblank labels, becoming 22 orientation-specific conflicts after reverse expansion;
- 110 blank workbook rows, mostly incomplete endpoint rows.

The released loader's last-row-wins and blank-row behaviour is documented in `CTI_ChronoCTI_Baseline_Reproduction_Audit_v0.1`. Until the missing intermediate feature file is obtained, do not claim the exact final model-row effect or recomputed performance effect. Keep the released data and any corrected-loader sensitivity analysis separate.

---

## 4. Temporal relations and evidence

### 4.1 Temporal labels

Use the v0.3 vocabulary:

| Label | Meaning | Graph treatment |
|---|---|---|
| `BEFORE` | Event A is explicitly stated to occur before event B | Directed positive strict-order edge A → B |
| `AFTER` | Event A is explicitly stated to occur after event B | Preserve source direction; normalize to BEFORE(B,A) only in derived strict-order analysis |
| `OVERLAP` | The report explicitly supports temporal overlap | Symmetric positive temporal relation; not a strict precedence edge |
| `SIMULTANEOUS` | The report explicitly states both occur at the same time | Symmetric positive temporal relation; not a strict precedence edge |
| `CONCURRENT_UNSPECIFIED` | The report says the activities are concurrent but does not establish their interval relation | Symmetric positive temporal relation; not a strict precedence edge |
| `NO_TEMPORAL_CLAIM` | An assessed pair is mentioned, but the report makes no relative-time claim | Not a positive edge |
| `VAGUE_OR_AMBIGUOUS` | A temporal claim appears to exist but cannot be resolved | Not a positive edge |
| `NOT_ASSESSABLE` | Available report context is insufficient to assess the pair | Not a positive edge |

These labels are not interchangeable. `NO_TEMPORAL_CLAIM` is allowed only for a pair actually assessed under a declared candidate-pair rule; it is not the default for every unannotated pair. `VAGUE_OR_AMBIGUOUS` and `NOT_ASSESSABLE` must remain distinct.

### 4.2 Relation directness / basis

Record relation basis separately from the relation label:

- `direct_source` — source text explicitly relates the two endpoints using a temporal statement/cue or an unambiguous cross-sentence reference;
- `direct_timestamp` — explicit timestamps or intervals support the relation;
- `derived_transitive` — the relation follows only through a path of other temporal links;
- `inference` — analyst interpretation not directly supported by relation-specific source evidence;
- `unresolved` — the relation basis cannot be decided.

Only `direct_source` and `direct_timestamp` relations with resolved event-leaf endpoints enter the primary positive temporal graph. `derived_transitive` may be stored in a separate derived view, but it is not a second direct annotation. `inference` and `unresolved` do not enter primary positive-edge metrics.

A sentence that merely mentions both endpoints is insufficient. The evidence span(s) must support the relation between them. Sentence order alone does not establish physical chronology. A source may assert causality or dependency without asserting temporal precedence.

### 4.3 Required relation evidence fields

- `relation_id`
- `report_id`
- `event_a_id`, `event_b_id`
- `relation_label`
- `relation_basis`
- `evidence_start`, `evidence_end` (zero-based, half-open offsets into the frozen source)
- `evidence_text`
- `cue_text`
- `argument_support`
- `evidence_scope` (`SENTENCE`, `CROSS_SENTENCE`, `DOCUMENT_CONTEXT`)
- `annotator_confidence` (`HIGH`, `MEDIUM`, `LOW`)
- `adjudication_status` (`UNREVIEWED`, `AGREED`, `ADJUDICATED`, as applicable)

### 4.4 Non-temporal relations

Record these separately; never convert them automatically into BEFORE:

- `CAUSES_OR_ENABLES`
- `DEPENDS_ON`
- `PRECONDITION_OF`
- `NARRATIVE_ORDER_ONLY`

MITRE Attack Flow dependency arrows are not temporal BEFORE labels.

---

## 5. Source freeze, mention, and scope annotation

### Pass 0 — Provenance and source integrity

1. Record source URL/archive path, title, publisher, publication/retrieval dates, language, and licence/terms status.
2. Save a local frozen source copy for annotation and calculate SHA-256.
3. Record any transformations (HTML extraction, markdown conversion, whitespace normalization) and preserve the original text.
4. Do not redistribute raw report text or derived excerpts publicly until the report and dataset rights have been checked. The repository's MIT licence does not license third-party CTI reports or source datasets.

### Pass 1 — Source read and scopes

1. Read the complete frozen report before examining benchmark labels or prior AI reconstructions.
2. Record all incident/campaign/actor/victim/host/report scopes and the evidence for each boundary.
3. Preserve raw temporal expressions. Normalize only where date/time precision and timezone support it.
4. Do not assume a single report equals one incident or one timeline.

### Pass 2 — Mentions

1. Record action/activity mentions as exact source spans with zero-based, half-open character offsets.
2. Check that `source_text[start:end]` equals the stored mention text.
3. Assign an `instance_status` to every mention.
4. Group co-referring mentions only when source evidence supports a shared occurrence.
5. Keep generic behaviour and unresolved activity visible; do not convert either into event leaves.

### Pass 3 — Activity units and event identity

1. Create activity-unit records after mention review.
2. Assign `granularity` and `unit_role` before creating event IDs.
3. Resolve atomic event leaves only when the report distinguishes a particular occurrence.
4. Use series/episode/aggregate containers when the source supports only those levels.
5. Record count status separately. Leave host, actor, time, execution count, or campaign identity unknown when the source does not establish it.
6. Preserve grouping relationships without counting a container as an additional event.

### Pass 4 — ATT&CK mapping

1. Map each resolved event leaf independently.
2. Assign zero or more technique/sub-technique mappings; do not force one mapping.
3. Record evidence and mapping basis for each mapping.
4. Preserve the source-specific mapping and the baseline parent-level mapping separately.
5. Pin the ATT&CK release and selected baseline technique-list hash.

### Pass 5 — Positive temporal relation discovery

1. Read the complete report for every explicitly asserted or unambiguously supported temporal relation between resolved event leaves.
2. Link relation endpoints to event IDs, not merely to technique labels or mention strings.
3. Attach relation-specific evidence and scope compatibility.
4. Record directness/basis. Do not infer order from narrative position alone.
5. Do not create every possible event pair and mark all unlabelled pairs negative.
6. Keep episode-to-episode relations in a separate episode-level exploratory register; do not pool them with atomic event-instance edges.

### Pass 6 — Optional candidate-pair assessment

Positive relation discovery is the primary descriptive product and does not require a complete all-pairs matrix.

If candidate pairs are separately assessed, freeze the candidate-generation rule before annotation (for example, pairs linked by a temporal cue, a cross-sentence reference, or a specified local-context rule). For each assessed pair, use:

- a positive temporal label;
- `NO_TEMPORAL_CLAIM`;
- `VAGUE_OR_AMBIGUOUS`;
- `NOT_ASSESSABLE`.

Record the candidate frame, selection rationale, report-level coverage, and sampling limitations. A later classifier project needs its own pair universe, negative sampling, report-level split, and sampling weights.

### Pass 7 — Lock and reveal baseline

1. Save a read-only first-pass annotation and its hash before inspecting benchmark pair labels, cycle status, or the Researcher Key.
2. For the existing `r-dfir-1`, `r-dfir-8`, and `r-dfir-2` development cases, explicitly mark the annotation as AI-exposed/protocol-development; do not label it blind.
3. For a fresh sample, keep benchmark labels hidden until the source annotation is locked.
4. Only after lock, build the event graph, technique projection, and benchmark comparison.

---

## 6. Projection definitions

For one report, let:

- \(V\) be the set of resolved atomic event-leaf instances;
- \(A(v)\) be the set of evidence-backed **baseline-compatible parent technique IDs** assigned to event instance \(v\) for the primary ChronoCTI comparison; retain exact sub-technique mappings separately;
- \(E^+\) be the set of positive, evidence-supported temporal relations between resolved event leaves.

For an event relation \(e=(u,v)\), calculate a mapping image from the endpoint mapping sets. Pair orientation depends on relation type:

- For directed `BEFORE` and `AFTER`, retain the ordered Cartesian product \(A(u)\times A(v)\).
- For symmetric `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED`, canonicalize each technique pair as an unordered dyad (for example, sort the two technique IDs) so the pair is not double-counted in opposite orientations. Preserve the original event endpoints and relation label in the source annotation.

For concise notation, let \(Q(e)\) denote the relation-aware mapping image produced by that rule. For strict-order cycle analysis, normalize `AFTER(A,B)` to `BEFORE(B,A)` while preserving the original annotation.

Split this mapping image into:

\[
Q_{diag}(e)=\{(t,t):t\in A(u)\cap A(v)\}
\]

\[
Q_{distinct}(e)=Q(e)\setminus Q_{diag}(e)
\]

Keep the event relation and its provenance even if the technique projection cannot represent it. Keep a map from every projected technique pair back to all source event-edge IDs.

### 6.1 Edge projection outcomes

For each mapped positive event edge:

- `fully_omitted` — no non-diagonal technique pair remains (`Q_distinct` is empty);
- `partially_represented` — at least one diagonal and at least one non-diagonal mapping pair exist;
- `no_diagonal_mapping` — no shared-technique diagonal pair is created;
- `unmapped_endpoint` — one or both event endpoints have no supported baseline technique mapping; report separately and do not count as same-technique omission.

A shared technique at the endpoints does not mean the whole edge is lost when another distinct technique pair remains.

### 6.2 Strict-order cycle analysis

- Use only `BEFORE` and `AFTER`, with `AFTER(A,B)` normalized to `BEFORE(B,A)` in the derived cycle view.
- Preserve the original label and endpoints in the annotation data.
- Exclude `OVERLAP`, `SIMULTANEOUS`, `CONCURRENT_UNSPECIFIED`, causal/dependency labels, narrative order, ambiguous links, and unresolved links.
- Verify that the source event-instance strict-order graph is acyclic before interpreting a technique-graph cycle as projection-induced.
- Exclude diagonal technique pairs from the distinct-technique cycle graph but report them as information loss separately.
- Retain source-event-edge provenance for each projected SCC.
- Distinguish cycles generated by mapping fan-out from a single source event edge from cycles requiring two or more distinct source event edges. A single-edge fan-out cycle is not evidence of repeated occurrences.

### 6.3 Baseline alignment constraint

ChronoCTI's released pair data has no report-local event IDs or relation-specific source spans. A benchmark technique edge therefore cannot be assigned one-to-one to an event pair without additional evidence. Record baseline alignment as `supported`, `multiple_candidate_pairs`, `ambiguous`, `unmapped`, or `not_assessable` only after the event-level candidate set has been reviewed. Do not infer the cause of a benchmark cycle from topology alone.

---

## 7. Metrics and denominators

Do not combine the measures below into one overall “information-loss percentage.” They count different objects and can overlap.

1. **Repeated-occurrence report rate:** reports with at least two resolved atomic event leaves sharing one or more technique IDs / eligible sampled reports. Report numerator, denominator, granularity exclusions, and confidence interval only for a probability sample of adequate size.
2. **Occurrence compression:** number of resolved atomic event leaves per technique before projection, with series/episode/aggregate containers reported separately.
3. **Same-technique endpoint rate:** mapped positive event-edge count whose endpoint mapping sets intersect / all mapped positive event edges. Count each source edge once.
4. **Full omission rate:** fully omitted mapped positive event edges / mapped positive event edges. Report unmapped edges separately.
5. **Partial diagonal rate:** partially represented mapped positive event edges / mapped positive event edges.
6. **Diagonal mapping share:** diagonal event-edge-to-technique-pair combinations / all event-edge-to-technique-pair combinations. This counts mapping combinations, not source edges.
7. **Technique-pair collision/conflation:** projected technique pairs receiving multiple distinct source event edges, excess edge multiplicity, and any conflicting temporal labels. Preserve provenance.
8. **Projection-induced cycle diagnostics:** event graph acyclicity, projected SCCs, number requiring multiple source event edges, and number generated by single-edge mapping fan-out.
9. **Recurrence cardinality:** counts by `exact`, `minimum`, `range`, `qualitative_only`, and `unknown`, stratified by granularity.
10. **Coverage/missingness:** event mapping coverage, positive edge mapping coverage, unresolved/generic mention counts, and evidence-span validity.

A 5–8 report protocol-development pilot is not a prevalence estimate. Do not pool atomic events and episode containers to increase denominators.

---

## 8. Sampling and study phases

### Phase A — Existing protocol-development cases

Use `r-dfir-1`, `r-dfir-8`, and `r-dfir-2` to debug the schema and analysis logic. Label them AI-exposed and purposive. Do not use them to estimate rates.

### Phase B — Fresh multi-vendor feasibility sample

Before selecting fresh reports:

1. choose and document the sampling frame;
2. confirm the underlying report-text and dataset rights for research and intended publication;
3. use a vendor-stratified random selection rule where feasible;
4. do not stratify or select on ChronoCTI cycle status;
5. record random seed, frame version, strata, inclusion/exclusion, and replacement rules;
6. keep the researcher key and benchmark labels separate until annotations are locked.

AnnoCTR's official cyber-specific report frame is a candidate, subject to exact source and licence verification. A repeated-technique text scan may help prioritize a separate exploratory set, but scanner positives and negatives are not event-instance labels. For any two-stage screen, manually assess a random subset of screen-negative reports and account for selection probabilities.

The initial 5–8 reports, if used, are only a protocol-debugging sample. A later prevalence estimate requires a separately justified sample size and probability sampling design.

---

## 9. Human annotation and tool assistance

- The researcher owns final event identities, scopes, mapping decisions, temporal labels, adjudication, experiment execution, and interpretation.
- AI may help locate spans, check code, summarize source evidence, and audit consistency. AI suggestions must be visibly separated from human annotations.
- AI is not an independent human annotator and cannot create human gold labels or inter-rater reliability.
- If only one human annotator is available, conduct a washout repeat pass on a subset and report intra-annotator consistency only.
- If a second human annotator is recruited, keep the annotations independent until both passes are locked. Select layer-appropriate agreement measures; do not collapse event coreference, mapping, and temporal relation annotation into one score.
- Preserve disagreements and adjudication decisions; do not silently overwrite them.

---

## 10. Quality-control checklist

- [ ] Source URL/path, retrieval date, licence status, transformation history, and SHA-256 are recorded.
- [ ] Mention offsets are zero-based, half-open, and match the frozen source text.
- [ ] Mentions are not equated with occurrences.
- [ ] Every mention has `instance_status`.
- [ ] Granularity, unit role, and count status are recorded separately.
- [ ] Series/episode/aggregate containers are not counted as extra atomic event leaves.
- [ ] Every mapping is separately evidenced and version-pinned.
- [ ] Multiple mappings do not create multiple event instances.
- [ ] Every positive temporal relation has relation-specific evidence and resolved event-leaf endpoints.
- [ ] Sentence order, causality, dependency, and Attack Flow arrows are not mistaken for BEFORE.
- [ ] Derived-transitive and inferred relations are excluded from primary direct-edge counts.
- [ ] Candidate-pair assessment rules are frozen before negative labels are assigned.
- [ ] Unmapped and missing endpoints are reported separately from diagonal omissions.
- [ ] Projection provenance is retained from technique pairs to source event edges.
- [ ] Single-edge mapping fan-out cycles are separated from multi-edge projection cycles.
- [ ] Benchmark edge matching is not assumed to be one-to-one with source event pairs.
- [ ] Reports selected for development are not described as a blind or prevalence sample.

---

## 11. Stop/go criteria

Proceed to a larger study only if:

1. the researcher can apply mention, event-instance, container, and granularity definitions without repeatedly changing them;
2. source text can lawfully be used for the intended research and publication;
3. a transparent sample contains enough resolved repeated occurrences and positive temporal relations for the intended measures;
4. the baseline relation-label semantics and pair universe are documented, including known loader discrepancies;
5. the projection implementation passes the synthetic tests and preserves many-to-many source-edge provenance;
6. annotation time and quality-control burden are practical;
7. a fair comparison can be defined without treating technique-level benchmark edges as event-level ground truth.

If these conditions fail, revise or abandon the candidate question. Do not inflate the sample, count episodes as atomic events, or relax evidence rules just to obtain positive findings.

---

## 12. Version consolidation and migration

This draft consolidates:

- **v0.2:** activity-unit granularity, count status, scope, mapping basis, directness, and the three-case workflow;
- **v0.3:** mention/event-instance separation, exact offsets, `instance_status`, multi-mapping, relation-specific evidence, temporal/non-temporal label separation, candidate-pair frame, and positive-edge denominator;
- **Baseline audit v0.1:** ordered versus unordered pair counts, diagonal exclusion, last-row-wins label collisions, blank-row treatment, and missing intermediate feature outputs.

### Migration rules

1. Preserve all v0.2/v0.3 documents as historical versions; do not overwrite them.
2. Do not mark this v0.4 draft frozen until the researcher reviews and approves the definitions.
3. Existing three-case workbooks must be tagged `AI_EXPOSED_PROTOCOL_DEVELOPMENT` and reclassified by granularity before any primary event-instance metric is reported.
4. Recompute combined three-case metrics after separating atomic event leaves from series, episode, and aggregate containers. Earlier pooled counts are exploratory bookkeeping, not primary harmonized event-instance results.
5. Keep the original ChronoCTI data and original loader output separate from any corrected-loader sensitivity run.
6. No report text, source workbook, or derived annotation should be added to the public repository until source licences and redistribution rights are checked.

## 13. Researcher decisions still open

This protocol draft does not decide the annotations. The researcher must still review, among others:

- `r-dfir-1`: grouping-parent versus separate leaf representation; direct versus derived classification of the attempt-to-attempt relation; mapping evidence basis;
- `r-dfir-8`: internal SMB transfer mapping alternatives; whether the candidate download-to-execution relation is directly supported; strict temporal interpretation of service registration/execution steps;
- `r-dfir-2`: whether the four LSASS periods are activity episodes rather than atomic executions; which episode-level order links are directly supported; mapping basis.

Until these decisions are reviewed and recorded, all existing case reconstructions remain provisional and not human-locked.

---

## 14. References and implementation anchors

- Rahman et al. (2025), *Mining temporal attack patterns from cyberthreat intelligence reports*, Knowledge and Information Systems. DOI: https://doi.org/10.1007/s10115-025-02491-6.
- ChronoCTI archival dataset DOI: https://doi.org/10.6084/m9.figshare.26039518.v3.
- ChronoCTI public repository: https://github.com/rayhanur-rahman/ChronoCTI.
- Current CTI Evidence Lab protocol v0.3: `research/ANNOTATION_PROTOCOL_v0.3.md`.
- Projection metric definitions: `research/PROJECTION_METRICS_v0.1.md`.
- Baseline reproduction audit: `CTI_ChronoCTI_Baseline_Reproduction_Audit_v0.1.zip`.