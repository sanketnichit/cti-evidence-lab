# AnnoCTR five-report pilot — annotation draft v0.1

**Prepared:** 6 November 2026  
**Status:** Pre-annotation proposal only. Not human-reviewed, not adjudicated, not locked, and not a real-report projection.  
**Fixed order:** Intel471 → Lab52 → Proofpoint → QuoIntelligence → Zscaler.

## Purpose

This package structures candidate scopes, activity units, source anchors, ATT&CK mapping triage and temporal-relation triage for the five fixed rank-one feasibility candidates. It does not populate canonical annotation registers and must not be counted as human annotations or empirical results.

## Files

- `report_assessment_draft.csv`: report-level eligibility recommendations and outstanding gates.
- `scope_candidates_draft.csv`: proposed scope hierarchy.
- `activity_unit_candidates_draft.csv`: candidate units, granularity, parent containers and primary-graph treatment.
- `source_anchor_index_draft.csv`: exact zero-based, end-exclusive source offsets and hashes. Source quotations are not reproduced; inspect each pinned source using its offsets.
- `mapping_triage_draft.csv`: report-level ATT&CK material and event-mapping restrictions.
- `mapping_source_label_audit_draft.csv`: source ID/name discrepancies against the pinned Enterprise ATT&CK v12.1 crosswalk.
- `temporal_triage_draft.csv`: report-level review; no positive primary relation is proposed in this pass.

## Source integrity and attribution

All offsets refer to AnnoCTR source text at corpus revision `d510b6949e1938d47c93a43eedd562dc538439dc`. The source SHA-256 is carried in the report and anchor registers. Source files are not copied into this package.

The source material is distributed by AnnoCTR under CC BY-SA 4.0. Report title, publisher and original source URL are recorded for attribution. Adapted annotation material intended for public distribution must retain attribution and ShareAlike. This package does not relicense source reports. The repository MIT software licence does not replace source-material terms.

## Interpretation rules

1. A sample, binary, file hash, malware family or tool capability is not automatically a victim-side event.
2. Reverse-engineered command handlers are not proof that each command executed.
3. A campaign/incident description may be retained as an episode or series container without inventing atomic event leaves.
4. Dated communications, sample submissions, compilation timestamps and publication dates are not interchangeable with attack-event times.
5. Report-level ATT&CK lists are not copied to individual activity units.
6. Missing or ambiguous evidence is not converted into a negative temporal label.
7. Researcher prior exposure for these five candidates remains `AI_EXPOSED` under the existing project rule.

## Consistency findings to preserve

- The Zscaler article describes a campaign beginning in July 2021 while identifying a specific spear-phishing email sent on 30 June 2021 at 10:44 PKT. This is recorded as a campaign-boundary/date consistency question, not silently normalised into an event sequence.
- The Intel471 source writes one TTP token as `T1021:002`; the pinned crosswalk contains `T1021.002`. Preserve the source form and keep any normalisation explicit.
- The Zscaler mapping table pairs `T1055`, `T1555`, and `T1074` with labels corresponding to v12.1 sub-techniques rather than the listed parent IDs. The discrepancy register records the crosswalk entries. No source mapping has been silently corrected or accepted.

## Draft summary

- Five reports receive a source-scope recommendation of ELIGIBLE, pending researcher decision.
- One possible atomic primary event leaf is proposed: the timestamped Zscaler email. It is not accepted.
- Positive primary temporal relations proposed: zero.
- Event-level ATT&CK mappings accepted: zero.
- Human annotations, selected final partitions and real-report projections created by this package: zero.

## Required next steps

1. Researcher reviews source-scope eligibility and each proposed activity-unit boundary.
2. Validate every source offset against the local frozen source text.
3. Reconcile the approved pilot protocol and schema version.
4. Populate canonical registers only after the approval/freeze gate.
5. Lock only researcher-reviewed final partitions; project only from valid locks.
