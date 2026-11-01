# Annotation Protocol v0.2 — CTI Event Instances and Temporal Evidence

**Project:** CTI Evidence Lab  
**Version:** 0.2-draft  
**Date:** 2026-11-01  
**Status:** Pilot protocol for human review; not validated

> This is a feasibility protocol, not a validated benchmark or claim of novelty. Do not annotate a large corpus until the pilot has been reviewed.

## 1. Keep four levels separate

1. **Text mention:** a span of text that refers to an action/event.
2. **Event instance:** the particular occurrence being described. Several mentions may refer to one occurrence; repeated executions may be distinct instances even when they use the same technique.
3. **ATT&CK concept:** the taxonomy technique/sub-technique associated with an event instance. A technique is not itself an event instance.
4. **Relation:** a relation between two event instances, supported by report evidence.

Same technique does not imply same event instance. Same malware/tool does not imply same event instance. Repeated mention does not imply repeated execution. A generic statement about what a malware family or actor typically does is not automatically a report-local event instance. If the text cannot resolve whether mentions refer to one or multiple occurrences, mark the identity unresolved rather than guessing.

## 2. Annotation workflow

1. Read the complete report. Record source identifier, title, publication/retrieval dates, language, provenance and licence.
2. Freeze the source text and calculate a source hash. Mark candidate event/action mentions using exact character offsets in this unmodified text.
3. Group co-referring mentions into event instances only when the text supports that decision.
4. Assign zero or more ATT&CK technique/sub-technique mappings to each resolved event instance only when report evidence supports each mapping. Store each mapping separately with its own evidence span(s), and record the pinned ATT&CK version. Do not force a single mapping if the report supports multiple techniques, and do not infer multiple executions from multiple mappings.
5. Identify temporal expressions and relation cues.
6. Create event-instance pairs only when a temporal relation is explicitly stated or supported by an unambiguous construction in the report.
7. Attach the smallest useful evidence span(s) supporting the relation, including the cue and enough context to resolve its arguments.
8. Record uncertainty and adjudication notes rather than forcing a label.

Do not use external threat-intelligence knowledge to fill gaps in the report. External enrichment, if any, must be stored separately and must not silently become gold evidence.

## 3. Event mention and event-instance fields

| Field | Meaning |
|---|---|
| report_id | Stable local report identifier |
| mention_id | Unique ID for a text mention |
| mention_text | Exact source substring |
| char_start, char_end | Zero-based, half-open offsets into frozen source text |
| sentence_id | Sentence containing the mention, if available |
| event_instance_id | ID shared by mentions referring to the same occurrence; null when there is no resolved instance |
| instance_status | RESOLVED, UNRESOLVED, GENERIC_BEHAVIOUR, or NOT_AN_EVENT |
| event_type_text | Short normalized action description, without adding facts |
| actor, target, asset_or_host | Text-grounded values or null/unknown |
| time_expression | Exact time phrase, if present |
| technique_mappings | Zero or more evidence-backed ATT&CK technique/sub-technique mapping records; each has its own ID, name, pinned version and mapping evidence |
| mapping_evidence | Evidence spans stored separately for each mapping record |
| mapping_confidence | HIGH, MEDIUM, or LOW per mapping; record UNMAPPED when the event has no supported mapping |
| annotator_note | Concise explanation of difficult decisions |

Offsets must match the exact frozen source text. Every proposed merge of mentions needs textual evidence that they refer to the same occurrence; every proposed split needs evidence of distinct occurrences. Two actions on different hosts are not automatically separate occurrences unless the report supports that distinction. Use GENERIC_BEHAVIOUR when the report states a general capability or recurring pattern but does not assert a specific occurrence in the report. Use NOT_AN_EVENT for non-action material. Do not assign an event_instance_id to either status.

## 4. Temporal relation labels

| Label | Definition | Direction |
|---|---|---|
| BEFORE | Event A is explicitly stated to occur before event B | A → B |
| AFTER | Event A is explicitly stated to occur after event B | A → B, preserving written direction |
| OVERLAP | The report explicitly supports temporal overlap | Symmetric |
| SIMULTANEOUS | The report explicitly states both occur at the same time | Symmetric |
| CONCURRENT_UNSPECIFIED | The report says both occur concurrently but does not establish exact interval relation | Symmetric |
| NO_TEMPORAL_CLAIM | Both events are mentioned, but the report makes no claim about their relative timing | Not a positive edge |
| VAGUE_OR_AMBIGUOUS | A temporal claim appears to exist but cannot be resolved | Not a positive edge |
| NOT_ASSESSABLE | Available text/context is insufficient to assess the pair | Not a positive edge |

For a derived representation, AFTER(A,B) may be normalized to BEFORE(B,A), but preserve the original annotation and evidence.

These labels are not interchangeable. NO_TEMPORAL_CLAIM describes what the report says; VAGUE_OR_AMBIGUOUS describes unresolved meaning; NOT_ASSESSABLE describes insufficient available context; model ABSTAIN is a system decision not to predict.

## 5. Keep non-temporal relations separate

Record these separately; never convert them automatically into BEFORE:

- CAUSES_OR_ENABLES
- DEPENDS_ON
- PRECONDITION_OF
- NARRATIVE_ORDER_ONLY

A causal/dependency relation may coincide with temporal ordering in reality, but do not infer that ordering unless the report supports it. In particular, MITRE Attack Flow dependency arrows are not temporal BEFORE labels.

## 6. Relation evidence fields

| Field | Meaning |
|---|---|
| relation_id | Unique relation record ID |
| event_a_id, event_b_id | Resolved event-instance IDs |
| relation_label | One of the temporal labels above |
| evidence_start, evidence_end | Character offsets of relation evidence |
| evidence_text | Exact source substring |
| cue_text | Temporal cue, if present |
| argument_support | How the cue links event A and event B |
| evidence_scope | SENTENCE, CROSS_SENTENCE, or DOCUMENT_CONTEXT |
| annotator_confidence | HIGH, MEDIUM, or LOW |
| adjudication_status | UNREVIEWED, AGREED, or ADJUDICATED |

A span that merely mentions both endpoints is insufficient: it must support the relation between them. For cross-sentence relations, record the minimal set of spans and explain the link.

## 7. Difficult cases

- Sentence A appearing before sentence B does not establish that event A happened first.
- Do not invent anchors for relative dates or normalize timestamps when timezone/precision is unclear.
- Preserve ranges and temporal uncertainty; do not reduce a range to a point timestamp.
- Repeated technique labels may map to multiple event instances.
- Repeated mentions may refer to one instance; resolve coreference before counting instances.
- Do not create event instances solely from ATT&CK labels without action evidence.
- Contradictory statements should be retained and flagged for adjudication, not silently reconciled.
- Inferred chronology from analyst knowledge is excluded from primary gold labels unless the report explicitly supports it.

## 8. Pilot design and measurements

Start with **5–8 reports** selected to include apparent repeated occurrences of one technique, clear temporal cues, cross-sentence references, and ambiguous/no-relation cases. This is a protocol/debugging sample, not a representative sample or prevalence estimate.

Obtain independent annotations from a second human annotator for an overlapping subset if possible. If this is not possible, state plainly that inter-annotator agreement was not measured. Do not present self-consistency as inter-annotator agreement.

Record:
- annotation time per report and per layer;
- event mention count;
- resolved and unresolved event-instance count;
- reports with repeated distinct instances of the same technique;
- positive temporal relation counts by label;
- ambiguous and not-assessable pair counts;
- disagreements by decision type;
- evidence-span completeness;
- source/provenance/licence problems.

Do not collapse event spans, coreference, ATT&CK mapping and temporal relations into one agreement score. Select layer-appropriate measures after reviewing annotation literature.

## 9. Quality-control checklist

- [ ] Every event mention has exact offsets and a matching source substring.
- [ ] Mentions are grouped by occurrence, not merely by technique.
- [ ] Every resolved event instance has a defensible identity decision.
- [ ] ATT&CK mappings are version-pinned and evidence-backed.
- [ ] Every positive temporal edge has relation-specific evidence.
- [ ] Narrative order is not mistaken for event chronology.
- [ ] Causal/dependency relations remain separate.
- [ ] Uncertainty is represented rather than forced into a positive label.
- [ ] Cross-sentence evidence includes all necessary spans.
- [ ] Provenance and licence are recorded.

## 10. Pilot exit criteria

Proceed to a larger study only if:
1. Annotators can distinguish mentions from event instances with acceptable, explainable consistency.
2. Repeated occurrences of the same technique exist in enough accessible reports to support the planned descriptive analysis.
3. Positive temporal relations and evidence spans occur often enough for the intended measurements.
4. Source text can lawfully be used for the intended research/publication.
5. A fair baseline can be defined without conflating technique-level and event-instance-level labels.

If these conditions fail, revise or abandon the candidate question. Do not inflate the dataset or relax definitions just to obtain positive results.

## 11. Student-led research and AI assistance

The student researcher owns final annotation decisions, adjudication, experiment execution and interpretation. AI may help find candidate passages, explain rules, check schema consistency and review code, but AI-generated labels must never be treated as gold annotations. Any AI-proposed label must be checked by a human against the original report.

Maintain an assistance log recording tool, date, task, suggestions accepted/rejected and verification. Follow university and publication policies for disclosure.


## 12. Mapping multiplicity and non-instance behaviour (v0.2 clarification)

An event instance may have:
- one supported ATT&CK technique/sub-technique mapping;
- multiple supported mappings, each separately evidenced;
- no supported mapping (UNMAPPED).

Represent mappings as a list, not a single technique field. Each mapping record should include `technique_id`, `technique_name`, `attack_version`, `mapping_evidence_spans`, and `mapping_confidence`. A single event instance with multiple mappings remains one event instance. Multiple linked mentions or mappings do not prove multiple executions.

Distinguish:
- `RESOLVED`: one report-local occurrence has been identified;
- `UNRESOLVED`: the text describes an occurrence, but whether this mention refers to one or multiple instances cannot be determined;
- `GENERIC_BEHAVIOUR`: a general capability, modus operandi, or recurring-pattern statement that does not assert a specific report-local occurrence;
- `NOT_AN_EVENT`: the span is not an action/event mention.

For the projection study, only `RESOLVED` event instances enter the primary event-instance graph. Report counts of unresolved and generic-behaviour mentions separately so they do not silently disappear.
