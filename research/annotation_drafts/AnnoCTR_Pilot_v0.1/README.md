# AnnoCTR five-report pilot — annotation draft v0.2

**Prepared:** 6 November 2026  
**Status:** Pre-annotation proposal only. Not human-reviewed, not adjudicated, not locked, and not a real-report projection.  
**Fixed order:** Intel471 → Lab52 → Proofpoint → QuoIntelligence → Zscaler.

## Purpose

This package structures candidate scopes, activity units, source anchors, ATT&CK mapping triage and temporal-relation triage for the five fixed rank-one feasibility candidates. It does not populate canonical annotation registers and must not be counted as human annotations or empirical results.

## Files

- `report_assessment_draft.csv`: report-level eligibility recommendations and outstanding gates.
- `scope_candidates_draft.csv`: proposed scope hierarchy.
- `activity_unit_candidates_draft.csv`: candidate units, granularity, stratum and primary-graph treatment.
- `source_anchor_index_draft.csv`: exact zero-based, end-exclusive source offsets and hashes. Source quotations are not reproduced; inspect each pinned source using its offsets.
- `mapping_triage_draft.csv`: report-level ATT&CK material and event-mapping restrictions.
- `mapping_source_label_audit_draft.csv`: source ID/name and lifecycle audit against the pinned Enterprise ATT&CK v12.1 crosswalk.
- `report_level_mapping_detail_draft.csv`: the seven publisher-explicit QuoIntelligence technique IDs and their lifecycle states.
- `temporal_triage_draft.csv`: report-level review, separating communication-relation candidates from attack-action candidates.
- `temporal_relation_candidates_draft.csv`: Intel471's dated-communication pair candidate; not accepted.
- `chronoCTI_label_crosswalk_draft.csv`: proposed label mapping to the ChronoCTI baseline; not approved.
- `EVENT_UNIVERSE_AND_CHRONOCTI_BOUNDARY_v0.2.md`: adopted working event-universe boundary and schema requirements. The v0.1 note is retained as the superseded proposal.

## Source integrity and attribution

All offsets refer to AnnoCTR source text at corpus revision `d510b6949e1938d47c93a43eedd562dc538439dc`. The source SHA-256 is carried in the report and anchor registers. The Proofpoint SHA-256 is corrected to the independently recomputed 64-character digest `b3653c517baef27621db962ef305875e6d71ee44e40403d0892e22fe5e76e517`; the historical sample frame already contains this correct value.

The 5 November 2026 AnnoCTR dataset-maintainer response is the current project-level permission basis for local research and derivative publication by the five rank-one candidates, subject to attribution and ShareAlike. The earlier Lab52 legal-notice conflict remains documented as historical website-terms evidence; the later maintainer clarification supersedes the earlier unresolved project permission fields for the AnnoCTR-contributed corpus material. The response was qualified by the maintainer's recollection and supplied no report-level exception schedule. Do not publish raw reports or extended verbatim spans. The repository MIT software licence does not replace source-material terms.

## Event-universe boundary — working decision adopted 8 November 2026

The primary ChronoCTI-comparable stratum is **incident-linked attack-action occurrences**: concrete report-local actions that form part of conducting, enabling, or completing a specific cyberattack. This is not attacker-only or victim-side-only. It can include targeted phishing delivery and user execution induced by the attack, as well as other incident-linked operational steps.

Classify communications by function, not medium. A targeted phishing message or incident-linked extortion communication can qualify when it is itself an operational step. Forum creation, public source-code posts, response blogs and public claims remain in a separate communication/platform stratum unless the source establishes that the communication itself performs an operational step in a specific attack.

Keep analyst/sample observations, generic capabilities and other non-primary report-local activity in separate descriptive strata. Stratum assignment is independent of ATT&CK mapping: do not remove an otherwise qualifying attack action because it lacks a mapping, and do not promote commentary or observations merely because a technique label appears elsewhere in the report.

ChronoCTI's published inclusion rules focus on step-by-step cyberattack incident narratives and exclude social-media posts, generic malware features/capabilities, and non-attack content. Its example includes phishing followed by a user's execution of a malicious macro, supporting a medium-neutral, incident-linked definition rather than an attacker-only rule. Reference: Rahman et al. (2025), https://doi.org/10.1007/s10115-025-02491-6. The proposed label mapping remains separate in `chronoCTI_label_crosswalk_draft.csv` and is not approved by this event-universe decision.

### Intel471 communication candidate

The article dates a dyadka0220 source-code post to 3 September 2021 and a Groove response blog to 7 September 2021. These are two distinct communication occurrences. The candidate direct-timestamp BEFORE relation remains available for secondary descriptive review; it is not currently a primary attack-action edge. Do not convert it into an intrusion chronology.

## ATT&CK mapping cautions

- Intel471's closing list is expressly drawn from older Babuk and recent Groove-linked cases; preserve it at report level unless a technique is tied to a specific resolved activity unit. Preserve source token `T1021:002`; normalisation to `T1021.002` must remain explicit.
- Zscaler's table has three ID/name mismatches against v12.1: T1055 vs Process Hollowing (v12.1 sub-technique T1055.012), T1555 vs Credentials from Web Browsers (T1555.003), and T1074 vs Local Data Staging (T1074.001). Preserve source labels and do not silently correct them.
- QuoIntelligence explicitly lists seven Enterprise ATT&CK IDs: T1215, T1068, T1009, T1014, T1116, T1022 and T1048. Four (T1215, T1009, T1116 and T1022) are revoked in the pinned v12.1 crosswalk; the other three are active and in A_120. None is assigned to a particular event leaf in this draft; do not invent successor mappings for revoked IDs.
- A_120 is a subset of the 193 active v12.1 top-level techniques. The reported 111/154 distinct linked-parent coverage figure has not yet been independently reproduced in a committed script/register; treat it as a verification task, not a project fact.

## Interpretation rules

1. A sample, binary, file hash, malware family or tool capability is not automatically a victim-side event.
2. Reverse-engineered command handlers are not proof that each command executed.
3. A campaign/incident description may be retained as an episode or series container without inventing atomic event leaves.
4. Dated communications, sample submissions, compilation timestamps and publication dates are not interchangeable with attack-event times.
5. Report-level ATT&CK lists are not copied to individual activity units.
6. Missing or ambiguous evidence is not converted into a negative temporal label.
7. The researcher's first pass on these five candidates is `AI_EXPOSED` under the adopted project exposure rule; this pre-annotation package itself is not a human annotation.

## Draft summary

- Five reports receive a source-scope recommendation of ELIGIBLE, pending researcher decision.
- Three Intel471 communication/platform event-leaf candidates are proposed; one Zscaler operational email event candidate is proposed. All remain unaccepted.
- One Intel471 communication BEFORE pair is a candidate for separate review; no ChronoCTI-comparable attack-action temporal relation is accepted.
- Event-level ATT&CK mappings accepted: zero.
- Human annotations, selected final partitions and real-report projections created by this package: zero.
- Five reports remain a feasibility pilot only; there is no confirmatory sample-size design or population-inference basis.

## Required next steps

1. Reclassify the candidate units against the adopted medium-neutral attack-action rule without treating any draft classification as human-approved.
2. After protocol approval, populate the canonical v0.4 activity_unit_strata.csv with exactly one evidence-backed decision per activity unit; validate complete coverage and create activity-stratum locks for selected-final partitions. The existing draft CSV column remains non-authoritative triage metadata.
3. Validate every source offset against the local frozen source text.
4. Reconcile and freeze the approved pilot protocol/schema before populating canonical annotation registers.
5. Lock only researcher-reviewed final partitions; project only after the v0.2 analysis lock and v0.4 activity-stratum lock validate.
