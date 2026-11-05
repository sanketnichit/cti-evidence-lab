# QuoIntelligence — Winnti historical analysis source-first feasibility draft v0.1

**Status:** Working source-first review only. This is not a human-locked annotation, is not included in any denominator, and is not an empirical result.  
**Review date:** 5 November 2026  
**Candidate:** Rank-1 QuoIntelligence report in the fixed 120-report AnnoCTR frame.

## 1. Source identity and provenance

- **Report ID:** quoteintelligence_2020-04-20_winnti-group-insights-from-the
- **Title:** *WINNTI GROUP: Insights From the Past*
- **Publication date:** 20 April 2020
- **Canonical publisher page:** https://quointelligence.eu/2020/04/winnti-group-insights-from-the-past/
- **AnnoCTR text path:** AnnoCTR/all/text/quoteintelligence_2020-04-20_winnti-group-insights-from-the.txt
- **AnnoCTR source revision:** boschresearch/anno-ctr-lrec-coling-2024, commit d510b6949e1938d47c93a43eedd562dc538439dc
- **Source Git blob:** c136697d8c01006890a25be2c98a0acc2aa252ae
- **Frame source_text_sha256:** f35eb1fc7314de99fa4ddd52883f09f61b8f26151c230ed1549c6b0bcf48f825

## 2. Scope assessment

The report is a historical and technical analysis that combines at least two sample/target contexts with broader Winnti group background. They must remain separate:

| Scope candidate | Source content | Scope caution |
|---|---|---|
| WI-S01 — German chemical-company sample | Winnti-related DLL and embedded drivers; the authors assess that the sample was used to target a previously unreported German chemical company | The source does not resolve when or how long the malware was used |
| WI-S02 — South Korean gaming-company sample | A separate 64-bit Winnti executable submitted to a public scanner; its configuration is assessed as likely targeting Gravity Co., Ltd. | The payload was not recovered; the year for “21 February” is not stated in that sentence |
| WI-S03 — Historical Winnti activity | Prior campaigns, group history and earlier targeting across sectors | Background context, not one report-local incident |
| WI-S04 — Technical capability analysis | Driver-signature enforcement bypass, rootkit functionality, DNS tunnelling and sample/dropper behaviour | Reverse-engineered capabilities; not proof that each capability was invoked in a victim environment |

Do not join the German chemical-company and South Korean gaming-company samples into one campaign timeline. The report discusses a possible group relationship, but shared attribution does not make the two sample contexts one incident.

## 3. Candidate activity units and observations

| Candidate ID | Source description | Proposed granularity / role | Instance status | Evidence pointer | Review disposition |
|---|---|---|---|---|---|
| WI-U01 | German chemical company was reportedly aware of an attack in the second half of 2019 | unresolved / unresolved_unit | UNRESOLVED | [939, 1023) | This is an awareness statement, not an attack execution description; the underlying attack timing remains unknown |
| WI-U02 | A Winnti sample was detected after upload to a public scanner in January 2020 | report_level_aggregate / aggregate_container | NOT_AN_EVENT for the primary attack-event graph | [2536, 2671) | Analyst discovery/submission context; do not count as a victim-side intrusion event |
| WI-U03 | Sample compilation metadata suggests a 2015 build date | unresolved / unresolved_unit | NOT_AN_EVENT for the primary attack-event graph | [6429, 6500) | Compilation time is an artifact property, not an attack timestamp |
| WI-U04 | The report describes DSEFix and vulnerable driver use to bypass driver-signature enforcement | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | “Binary Analysis” section | Reverse-engineered capability; the source explicitly cautions that sample compilation does not establish the attack timeframe |
| WI-U05 | The report describes an embedded iodine implementation used for DNS tunnelling | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | [12815, 12883) and the DNS-tunnelling section | Technical capability analysis, not a timestamped C2 event series |
| WI-U06 | A separate Winnti executable was submitted to a public scanner on “21 February” | report_level_aggregate / aggregate_container | NOT_AN_EVENT for the primary attack-event graph | [20031, 20152) | Detection/submission observation; year is not restated |
| WI-U07 | The South Korean sample is assessed as likely targeting Gravity, but the intended payload was not recovered | unresolved / unresolved_unit | UNRESOLVED | [20626, 20715) and surrounding target analysis | Target assessment is qualified; no completed intrusion or payload execution is established |

The report says the German-company malware was likely developed in 2015, but it also says that it is not possible to determine when and how long attackers used it ([6552, 6634)). Do not convert compilation timestamps into execution dates or treat detection/upload dates as the date of compromise.

The source has an internal date issue that must remain visible: the executive summary places discovery in January 2020, while the introduction says “Friday, 13 January” without stating a year. Do not silently fill in a year or repair the weekday/date combination. The South Korean sample paragraph says “21 February” without restating a year; do not infer one from nearby metadata.

## 4. Time and temporal relations

The German company's awareness in the second half of 2019, the later sample discovery, the sample compilation timestamps, and the South Korean sample submission are different kinds of time references. They must not be merged into a single attack timeline.

**Primary positive temporal graph:** no candidate edge at this stage.

There are no two resolved atomic attack-event endpoints in a compatible scope with a relation-specific source cue. The report's malware-analysis narrative and the ordering of technical subsections do not create a BEFORE relation between victim-side actions. A relationship between sample compilation, upload, detection and awareness is not equivalent to a sequence of attack-event executions.

## 5. ATT&CK mapping provenance

The publisher includes a report-level MITRE ATT&CK table with T1215, T1068, T1009, T1014, T1116, T1022 and T1048. The table is presented as part of the report's overall analysis and recommendations; it does not assign each ID to a specific sample, target context, or resolved atomic event.

Keep those IDs as publisher-explicit, report-level mapping evidence. Do not propagate them automatically to WI-U01–WI-U07 or use them to claim a shared technique between the German and South Korean contexts. No event-level mapping is accepted in this draft.

## 6. Feasibility assessment

This report is valuable for testing multi-scope separation, uncertainty about attack times, and the distinction between malware artifact metadata, analyst detection events and victim-side attack activity. It has substantial technical detail, but detail about a sample is not itself evidence of a particular victim-side execution.

The current source review does not identify a resolved pair of atomic attack events with a source-grounded temporal relation. That is an informative feasibility observation, not a basis for replacing the rank-1 candidate.

**Working recommendation:** retain in the rank-1 feasibility queue while the researcher completes scope, local-use and rights decisions. Do not treat this recommendation as a formal eligibility decision.

## 7. Researcher decisions and unresolved checks

1. Confirm that the report's two separate sample/target contexts can be represented without conflating them.
2. Decide how analyst observations (sample submission, scanner detection, disclosure and victim awareness) are kept distinct from attack-event annotations.
3. Preserve date ambiguity exactly as written; do not infer years for “21 February” or the “Friday, 13 January” sentence.
4. Keep the publisher's report-level ATT&CK table separate from event-level mapping decisions.
5. Confirm local research-use permission and review item-level publisher terms before public reuse. The corpus-level CC BY-SA statement is evidence about the corpus distribution, but the item-level public-reuse decision remains separate and unresolved.

**No human eligibility decision, event instance, temporal relation, technique mapping, denominator contribution or projection result is created by this draft.**

## 8. Evidence pointer convention

Offsets are zero-based, end-exclusive Unicode code-point indices into the exact decoded AnnoCTR text at the pinned source revision above. They are locators, not labels. Re-open the source text at each pointer before accepting any annotation.
