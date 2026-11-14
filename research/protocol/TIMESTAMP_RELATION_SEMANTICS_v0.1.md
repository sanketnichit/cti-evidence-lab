# Timestamp-derived relation semantics v0.1

**Date:** 14 November 2026  
**Status:** Adopted working rule for the pilot draft; not a frozen or researcher-approved protocol.  
**Applies to:** Protocol v0.5-draft and the additive RECON v0.2 temporal-evidence extension.

## 1. Purpose

Prevent uncertain or coarse timestamp data from being treated as stronger temporal evidence than the source supports. Keep occurrence-time ordering separate from event duration and from explicit source statements about overlap, simultaneity, or concurrency.

## 2. What a timestamp must identify

A time record can support a timestamp-derived event relation only when:

- `time_type=ATTACK_OCCURRENCE`;
- the time record is linked to the correct event endpoint and its endpoint-support evidence span;
- the source expression is explicitly tied to that particular attack occurrence;
- the raw expression, precision, source timezone literal, normalization status, normalized bounds and uncertainty are preserved.

Detection, discovery, publication, report retrieval, sample upload, sample compilation and general attack-period times remain useful descriptive evidence, but they are not substitutes for attack-occurrence time.

## 3. Meaning of normalized bounds

`normalized_start` and `normalized_end` are **closed bounds on the possible instant of occurrence**. They do not represent how long the action lasted.

A precise point time has equal bounds. A coarse time expression (year, month, day, hour or minute) must be represented by the full range of instants consistent with that precision, not a midpoint or an assumed exact instant. A non-point interval needs an uncertainty note explaining the range and its source basis.

The interval is intentionally conservative: a broad range means the exact occurrence time is not known. Its overlap with another broad range does not mean the actions overlapped.

## 4. Which relation labels timestamps can support

### Strict order

A timestamp-only positive relation uses `relation_basis=direct_timestamp` and can be labelled only `BEFORE` or `AFTER`.

For `BEFORE(A,B)`, every retained A interval must end strictly before every retained B interval begins:

`A_end < B_start`

For `AFTER(A,B)`, reverse the endpoints:

`B_end < A_start`

Apply the test to every Cartesian combination of retained `ATTACK_OCCURRENCE` intervals for A and B. The strict inequality matters because the bounds are closed. If the intervals overlap, touch at a boundary, or leave any combination with uncertain order, the timestamps do not establish strict order. Do not select only the convenient timestamp record or silently discard another retained candidate.

### Non-strict positive relations

`OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` require explicit source wording and `relation_basis=direct_source`.

- `OVERLAP`: the source explicitly supports overlapping activity intervals.
- `SIMULTANEOUS`: the source explicitly states that both activities occur at the same time.
- `CONCURRENT_UNSPECIFIED`: the source explicitly states that the activities are concurrent but does not establish their interval relation.

Do not derive these labels from matching timestamps, same-day dates, a common reporting period, equal coarse precision, or overlapping timestamp-uncertainty bounds. Equal timestamps do not prove simultaneity; overlapping possible-time windows do not prove overlapping activity duration.

## 5. Timezone interpretation and normalization

Preserve the timezone phrase or offset exactly as reported in `timezone_text`. A timestamp-derived edge requires an explicit and unambiguous source timezone or UTC offset. Do not infer a zone from the publisher, victim/actor geography, analyst location, report language or customary regional practice.

Ambiguous abbreviations such as `IST`, `CST` or `BST` do not uniquely identify a timezone without source context that resolves them. When unresolved, retain the raw time expression and mark normalization unresolved; do not use it for a `direct_timestamp` edge.

Normalize accepted values to UTC. Store `normalized_timezone=UTC` and UTC-offset ISO-8601 bounds (preferably `Z`); preserve the original source-zone literal in `timezone_text`. For a named IANA timezone, apply the date-specific offset. A daylight-saving fold or gap that makes a local wall-clock time ambiguous or nonexistent must not be resolved by silently choosing one offset. Require an explicit source offset or another unambiguous source basis.

`timezone_status=INFERRED` or `UNKNOWN` is not sufficient for timestamp-derived relations. A source may explicitly print an ambiguous abbreviation; preserve the text, but do not treat its meaning as resolved merely because the abbreviation is present.

## 6. Conflicts and human review

If source wording conflicts with timestamps, first verify that both timestamps identify the correct event occurrences and are not publication/detection/analysis times. Preserve the discrepancy in notes. Do not silently prefer the timestamp or the prose. If human review cannot resolve the conflict, retain the uncertainty and do not count an unqualified primary positive edge.

The validator checks structural constraints and arithmetic invariance. It cannot establish event identity, timezone correctness, daylight-saving interpretation, source entailment or the semantic difference between two activity intervals. Those remain human decisions.

## 7. Implementation

RECON v0.2 now:

- rejects `direct_timestamp` with `OVERLAP`, `SIMULTANEOUS` or `CONCURRENT_UNSPECIFIED`;
- requires `normalized_timezone=UTC` and UTC-offset normalized bounds;
- continues to require explicit timezone metadata, raw time preservation, normalized endpoint time records, and uncertainty notes for non-point ranges;
- continues to require strict order across every retained A/B interval combination.

Synthetic regression tests cover the non-strict-label restriction, direct-source acceptance, inferred timezone rejection, UTC-normalized representation and the distinction between publication time and attack-occurrence time.

This is a working pilot rule, not empirical evidence and not approval to begin formal annotation. It does not change the primary temporal-incidence estimand: all five positive labels remain eligible when their relation basis and source evidence satisfy these rules.
