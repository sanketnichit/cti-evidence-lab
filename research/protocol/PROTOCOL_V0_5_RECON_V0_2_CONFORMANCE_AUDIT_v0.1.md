# Protocol v0.5-draft ↔ RECON v0.2 conformance audit v0.1

**Date:** 5 November 2026  
**Status:** technical audit of the current draft implementation; not protocol approval, schema freeze, or permission to begin formal annotation.  
**Compared artifacts:** `research/protocol/CTI_Event_Instance_Annotation_Protocol_v0.5-draft.md`, `research/metric_contract/CTI_Evidence_Lab_Researcher_Decision_Register_v0.2.md`, RECON v0.1, RECON v0.2, and the v0.1 projection adapter/metric module.

## 1. Executive result

The research question and the current data/projection architecture are substantially aligned on the primary object: **a direct, source-supported temporal relation between two distinct, resolved atomic event leaves**, with technique mapping applied only after event identity has been established.

The projection implementation already handles the protocol's key information-loss distinctions: directed versus symmetric relation projection, diagonal same-technique combinations, partial versus full omission, unmapped endpoints, many-to-many source-edge provenance, and single-edge fan-out cycles. The batch report-level aggregator is also implemented and synthetically tested; pair-opportunity rates remain withheld unless the provisional scope-pair rule is explicitly approved.

This audit found two implementation gaps in RECON v0.2 and closes them in the accompanying validator revision:

1. The protocol defines operationally different `SENTENCE`, `CROSS_SENTENCE`, and `DOCUMENT_CONTEXT` evidence scopes, while the prior validator enforced only the document-context case.
2. The timestamp validator silently skipped a retained non-normalized time candidate if another normalized candidate existed for the same endpoint.

The new checks improve evidence traceability and fail-closed behaviour. They do not determine whether a source semantically entails a temporal relation.

The protocol representation is now reconciled to the extension architecture: the relation's primary evidence span is the cue; exact text/offsets live once in `evidence_spans`; A/B/context support is linked through the v0.2 extension register. The draft also proposes, pending researcher approval, to defer episode-to-episode relation records and record-level ChronoCTI pair alignment from the initial pilot.

## 2. Conformance matrix

| Protocol requirement | Current implementation | Audit outcome |
|---|---|---|
| Mentions are distinct from occurrences; only resolved atomic `event_leaf` units enter the primary graph | RECON v0.1 validator plus projection adapter eligibility filter | Implemented in parent package |
| Temporal edges have distinct endpoints, compatible scope, positive label and direct basis | Parent validator and projection adapter | Implemented in parent package |
| Separate cue, Event A support and Event B support | v0.2 extension register; parent relation's primary span is the cue | Implemented |
| `SENTENCE` evidence scope | New check requires cue and at least one A- and B-support span to share a non-empty `sentence_id` | Implemented structurally |
| `CROSS_SENTENCE` evidence scope | New check requires support in a sentence distinct from the cue sentence and an explanatory note on each cross-sentence support link | Implemented structurally |
| `DOCUMENT_CONTEXT` evidence scope | New check requires a contextual span in a distinct section/paragraph passage, span-level notes, and relation-level rationale | Implemented structurally |
| Timestamp normalization preserves raw expression/precision/timezone and uncertainty | New check requires raw fields, explicit timezone status/text, normalized timezone, timezone-aware bounds, and uncertainty notes for non-point intervals | Implemented structurally |
| Strict timestamp `BEFORE`/`AFTER` survives retained interval uncertainty | All retained normalized A/B interval combinations are checked; unnormalized retained candidates now fail | Implemented conservatively |
| Multiple accepted mappings do not multiply events | Mapping sets are grouped by activity-unit ID | Implemented in parent projection module |
| Directed and symmetric technique-pair projection differ | Ordered Cartesian product for `BEFORE`/`AFTER`; unordered canonical dyads for symmetric labels | Implemented in parent projection module |
| Diagonal technique pairs are separated from distinct technique pairs | Diagonal, distinct, fully omitted, partially represented, and unmapped outcomes are returned separately | Implemented in parent projection module |
| Projected pair provenance is many-to-many | Source event-edge IDs are retained for each projected pair and SCC | Implemented in parent projection module |
| Episode-to-episode temporal relations | No episode-edge register in RECON v0.1/v0.2 | Initial-pilot deferral is proposed in Protocol v0.5; do not place container endpoints in the atomic temporal register | Deferred from initial pilot; researcher approval required |
| Benchmark pair is not assumed to be one source event pair | Baseline alignment is deferred and absent from the current adapter | Protocol now explicitly proposes deferring record-level alignment and preserving raw benchmark provenance separately | Deferred from initial pilot; researcher approval required |
| One final analysis partition per report | Selection validator enforces at most one selected-final row and validates the selected partition | Implemented |
| Selected analysis is locked before projection | v0.2 wrapper layers a digest over the v0.1 partition/source lock, v0.2 evidence rows and selection decision | Implemented; digest is a mutation detector, not a signature |
| Report-level denominator and study rates | `analysis/report_level_aggregation.py` aggregates one selected-final partition per assessable report and withholds rates until projection coverage is complete | Implemented and synthetically tested; scope-pair-opportunity-dependent rates remain approval-gated |

## 3. Changes made in this revision

### 3.1 Evidence-scope completeness

The validator now rejects a positive direct relation if its evidence-scope label is unsupported. For the three accepted labels:

- `SENTENCE`: at least one Event A support and one Event B support must share the cue's sentence ID.
- `CROSS_SENTENCE`: at least one endpoint-support span must be in a different sentence from the cue; every such support link must explain the cross-sentence reference/coreference in `evidence_notes`.
- `DOCUMENT_CONTEXT`: at least one `RELATION_CONTEXT` span must be located in a different section/paragraph passage from the cue; it needs span-level `evidence_notes`, and the relation requires `relation_notes` explaining how the passages connect.

The validator does not inspect language meaning. A human still decides whether the reference is genuinely unambiguous and whether the relation is directly asserted.

### 3.2 Timestamp candidate handling

For a direct-timestamp relation, the validator now requires raw time text, a supported precision value, explicit timezone status/text, and a populated normalized timezone. It rejects a retained candidate time row that is not normalized instead of ignoring it while comparing some other normalized row. It continues to require aware ISO-8601 bounds, valid interval direction, uncertainty notes for non-point intervals, and invariant strict ordering for all retained endpoint-interval combinations.

### 3.3 Test and documentation updates

Synthetic tests now cover all three evidence scopes, missing cross-sentence argument rationale, context passage separation, missing relation-level context rationale, invalid time precision, and a non-normalized timestamp candidate beside a normalized one. Package README and manifest have been aligned with the implemented checks.

## 4. Important boundaries that remain open

1. **Semantic entailment remains human-owned.** A valid sentence ID or evidence note cannot prove that the report actually identifies the two event leaves or asserts the relation.
2. **Non-strict timestamp label algebra is not fully formalized.** The current direct-timestamp validator checks endpoint time support for all positive labels, but only applies strict interval-order consistency to `BEFORE` and `AFTER`. Operational rules for deriving `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` from timestamp intervals still need explicit approval. Until then, do not infer those labels mechanically from broad/overlapping uncertainty windows.
3. **Timezone equivalence is not inferred.** The validator requires explicit raw and normalized timezone fields and offset-aware normalized bounds, but it does not prove that a publisher's timezone string and the normalized IANA/UTC offset are equivalent across daylight-saving or ambiguous abbreviations. Preserve the source expression and use manual review where conversion is ambiguous.
4. **Pair negatives remain optional and rule-bound.** The primary discovery task is full-report positive-relation review. No missing pair row is a negative label. A separate candidate-pair rule/version and its coverage must be frozen before assigning `NO_TEMPORAL_CLAIM`.
5. **Scope-pair opportunity rule remains provisional.** The report-level aggregator withholds pair-opportunity-dependent rates unless the nearest-common-resolved-non-report-aggregate scope rule is explicitly approved. Do not treat a passing synthetic aggregator test as approval of that rule.
6. **Episode-edge and benchmark-alignment deferrals require researcher approval.** The current protocol draft proposes not to collect episode-to-episode temporal edges or record-level ChronoCTI pair-to-event alignments in the initial pilot. Preserve episode containers and raw benchmark provenance without forcing them into the atomic relation schema.
7. **Approval is still required.** Protocol v0.5 is a draft, RECON v0.1 is a reconstruction, and RECON v0.2 is an additive draft extension. Synthetic correctness is not semantic validity or researcher approval.

## 5. Research readiness snapshot

At this audit point:

- human AnnoCTR annotation rows: 0;
- selected final analysis partitions: 0;
- real-report projections: 0;
- inter-annotator agreement: not measured;
- prevalence estimate: none;
- protocol/schema freeze: not approved.

The five rank-one AnnoCTR reports remain feasibility candidates, not selected reports. The three historical DFIR cases remain AI-exposed protocol-development material.

## 6. Recommended next sequence

1. Review and approve/revise the v0.5 event identity, relation, evidence-scope, timestamp and exact span-link representation.
2. Decide explicitly whether to accept the proposed initial-pilot deferrals for episode-to-episode edges and record-level benchmark alignment.
3. Approve RECON v0.2 as a new project schema version (not as recovered v0.4.2), including its required fields and manual semantic review procedure.
4. Validate the existing report-level aggregation layer against the approved metric contract; keep scope-pair-opportunity rates withheld until the rule is approved.
5. Only then make human source-scope eligibility decisions and run the first controlled source-first annotation pass on the fixed feasibility candidates. Do not select candidates based on event yield or positive-edge presence.
