# Intel471 — Groove / Babuk / RaaS source-first feasibility draft v0.1

**Status:** Working source-first review only. This is not a human-locked annotation, is not included in any denominator, and is not an empirical result.  
**Review date:** 5 November 2026  
**Candidate:** Rank-1 Intel471 report in the fixed 120-report AnnoCTR frame.

## 1. Source identity and provenance

- **Report ID:** intel471_2021-09-09_groove-gang-ransomware-babuk-revil
- **Title:** *How Groove Gang is shaking up the Ransomware-as-a-Service market to empower affiliates*
- **Publication date:** 9 September 2021
- **Canonical publisher page:** https://www.intel471.com/blog/groove-gang-ransomware-babuk-revil-blackmatter
- **AnnoCTR text path:** AnnoCTR/all/text/intel471_2021-09-09_groove-gang-ransomware-babuk-revil.txt
- **AnnoCTR source revision:** boschresearch/anno-ctr-lrec-coling-2024, commit d510b6949e1938d47c93a43eedd562dc538439dc
- **Source Git blob:** d73ab04a0f7f466912edcc53d346cdf759f4492e
- **Frame source_text_sha256:** 87e1e45070dffc9ae446013754ae6466c28cc5910c56501c4d8f1dcb573e7d56

The AnnoCTR text identifies the article as also having run on McAfee Enterprise ATR. This is a syndication relationship, not a second independent report. The source identity is verified; the publisher/donor and reuse implications remain a separate rights question.

## 2. Scope assessment

This is a CTI report, but it is not a single intrusion narrative. It combines RaaS ecosystem history, forum communications, disputed actor claims, historical Babuk victim/leak references, a BlackMatter victim context, a Groove victim context, and a broad TTP profile.

For source review, keep at least these contexts separate:

| Scope candidate | What the report covers | Primary attack-event status |
|---|---|---|
| GB-S01 — RaaS / forum ecosystem | RAMP history, Orange, affiliate relationships, forum posts and changes in the RaaS model | Contextual reporting; not an intrusion scope |
| GB-S02 — Babuk / Groove history | Babuk affiliate fallout, public statements and alleged transition to Groove | Historical actor context; no victim-side event chain established here |
| GB-S03 — BlackMatter victim reference | Data from a Thai IT service provider is reported as hosted on the “wyyad” server | Victim/leak association; attack occurrence, actor responsibility and timing are not resolved |
| GB-S04 — Groove victim reference | A German printing company is identified as the single leak on Groove’s own site at the time of writing | A reported leak context, not a documented intrusion sequence |
| GB-S05 — Groove TTP profile | Initial access, discovery, lateral movement, privilege escalation, exfiltration and ransomware deployment are discussed at actor/profile level | Generic cross-case behaviour; not a report-local incident timeline |

Do not combine these contexts into one scope simply because the article discusses relationships between the groups. Attribution and shared infrastructure do not establish that the behaviours happened in one campaign, one victim environment or one chronological sequence.

## 3. Candidate activity units

The following are reviewable behaviour mentions, not accepted event instances.

| Candidate ID | Source description | Proposed granularity / role | Instance status | Evidence pointer | Review disposition |
|---|---|---|---|---|---|
| GB-U01 | Exploitation of vulnerable VPN services is said to have been used several times | repeated_event_series / series_container | GENERIC_BEHAVIOUR | [16383, 16483) | Repetition is asserted, but the report does not enumerate the affected cases, hosts or executions |
| GB-U02 | Ad-Find and NetScan are described as network-discovery tools used by the actor | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | [16935, 16979) and surrounding paragraph | Capability/profile statement; no specific invocation or target is identified |
| GB-U03 | RDP is described as a frequently observed lateral-movement method | repeated_event_series / series_container | GENERIC_BEHAVIOUR | [17219, 17303) | Frequency is qualitative; no individual RDP sessions are identified |
| GB-U04 | Brute force, credential dumping and EternalBlue are listed as privilege-escalation options | report_level_aggregate / aggregate_container | GENERIC_BEHAVIOUR | “Lateral Movement, Discovery and Privilege Escalation” section | Alternatives are not proof that every method occurred in one target environment |
| GB-U05 | WinSCP is described as a data-exfiltration tool, followed by bulk ransomware deployment using several possible methods | report_level_aggregate / aggregate_container | GENERIC_BEHAVIOUR | [17857, 17908) and [18003, 18092) | A generalized attack-phase description; no specific victim execution or timestamp is supplied |

A unit may be promoted to a resolved atomic event only if the original report identifies a particular report-local occurrence. Repeated technique mentions, the number of named victims, or the presence of an ATT&CK table cannot supply that missing identity.

The September 3 Babuk developer statement and September 7 Groove response are actor communications described in the report. They are not attack-event leaves for the present technique-mapped intrusion study. Likewise, the publication, hosting and disclosure of victim data are not interchangeable with the underlying intrusion or exfiltration event.

## 4. Time and temporal relations

The source contains dates for historical forum/actor developments, but those dates do not establish a sequence of victim-side attack events. The generalized TTP section uses procedural language, including a sequence from access to movement, exfiltration and ransomware deployment. That describes a typical or observed pattern across cases; it does not provide two resolved event endpoints in a shared scope.

**Primary positive temporal graph:** no candidate edge at this stage.

Do not create BEFORE edges from the order of the article sections, from the order of steps in a generalized attack description, or from the fact that one leaked dataset is discussed after another.

## 5. ATT&CK mapping provenance

The publisher's final “MITRE TTPs” list expressly says it was compiled from older Babuk cases and some recent cases linked to Groove. It lists T1190, T1003, T1078.002, T1059, T1021:002, T1210, T1087, T1482, T1562, T1537 and T1567. T1486 is conditional on a ransomware partnership being achieved.

These are report-level/profile mappings with mixed historical provenance. They must not be copied onto GB-U01–GB-U05 as if each technique had been observed in a specific event. The unusual T1021:002 formatting should be preserved in the provenance note and checked against the pinned ATT&CK release before any mapping normalization; do not silently rewrite it.

No event-level mapping set is accepted in this draft. The AnnoCTR technique-link counts are mention-level inventory data and do not resolve which actor, victim, incident or occurrence a link refers to.

## 6. Feasibility assessment

This report is useful for testing whether the protocol keeps an actor-level TTP profile separate from incident-level event identity. It is also a difficult case for scope separation and attribution discipline.

The source currently supports a substantial generic-behaviour inventory, but no clear pair of distinct, resolved intrusion event leaves in a common scope. That is a legitimate feasibility outcome, not a reason to replace the rank-1 candidate with a report that is more likely to yield positive edges.

**Working recommendation:** retain in the rank-1 feasibility queue while the researcher completes source-scope and local-use decisions. Do not treat this recommendation as a formal eligibility decision.

## 7. Researcher decisions and unresolved checks

1. Decide whether the report’s mixed actor, victim and historical contexts can be annotated faithfully under the declared report/scope model without joining them into a synthetic campaign.
2. Confirm the local research-use basis for the AnnoCTR text.
3. Resolve the McAfee syndication and applicable publisher terms before any public reproduction of text or derived spans.
4. Keep public reuse separate from local annotation permission.
5. If annotation proceeds, lock scope boundaries first, then review mentions and generic behaviour. Do not begin by assigning the publisher's report-level TTP list to candidate events.

**No human eligibility decision, event instance, temporal relation, technique mapping, denominator contribution or projection result is created by this draft.**

## 8. Evidence pointer convention

Offsets are zero-based, end-exclusive Unicode code-point indices into the exact decoded AnnoCTR text at the pinned source revision above. They are locators, not labels. The source text must be re-opened at the pointer before any annotation is accepted.
