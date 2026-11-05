# Lab52 — TokyoX Part 2 source-first feasibility draft v0.1

**Status:** Working source-first review only. This is not a human-locked annotation, is not included in any denominator, and is not an empirical result.  
**Review date:** 5 November 2026  
**Candidate:** Rank-1 Lab52 / S2 Grupo report in the fixed 120-report AnnoCTR frame.

## 1. Source identity and provenance

- **Report ID:** lab52_2022-01-12_tokyox-dll-side-loading-an
- **Title:** *TokyoX: DLL side-loading an unknown artifact (Part 2)*
- **Publication date:** 12 January 2022
- **Canonical publisher page:** https://lab52.io/blog/tokyox-dll-side-loading-an-unknown-artifact-part-2/
- **AnnoCTR text path:** AnnoCTR/all/text/lab52_2022-01-12_tokyox-dll-side-loading-an.txt
- **AnnoCTR source revision:** boschresearch/anno-ctr-lrec-coling-2024, commit d510b6949e1938d47c93a43eedd562dc538439dc
- **Source Git blob:** bdbe4c6b2fef591e268e1dce84b53d42e196d109
- **Frame source_text_sha256:** d76b8fd4959b95c9d85a60adb8c96a14e2a46e1f5930f6323e07db74ea7d0ecc

This is Part 2 of a two-post analysis. It refers back to a separate Part 1 for the loading process. Keep the two publisher posts separate unless the researcher records an explicit scope decision that justifies combining them. The present candidate is Part 2 only.

## 2. Scope assessment

The report is a reverse-engineering analysis of one malware sample referred to as TokyoX. It describes code paths, data structures and command handlers recovered from the sample. The authors state that the command-and-control server was unavailable during analysis.

Use one sample-analysis scope for the code observations in this report. Do not infer a sequence of victim-side actions merely from the order in which functions or switch branches appear in the reverse-engineered code.

## 3. Candidate activity units

| Candidate ID | Source description | Proposed granularity / role | Instance status | Evidence pointer | Review disposition |
|---|---|---|---|---|---|
| TX-U01 | The sample checks for a mutex named “aftdoslm” after its loading process | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | [512, 656) | A sample behaviour described from analysis; no specific victim execution record is supplied |
| TX-U02 | The sample constructs a victim identifier and prepares a first C2 packet using host information | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | [837, 898) and surrounding packet description | The C2 server was unavailable; the report does not provide a captured victim-side session |
| TX-U03 | Command 6010 is interpreted as the initial request and is assumed to be a beacon when no action is intended | unresolved / unresolved_unit | UNRESOLVED | [2605, 2689) | The authors state this as an assumption; do not promote it to an observed beacon event |
| TX-U04 | Unsupported command handling can produce a five-minute sleep followed by another C2 request | repeated_event_series / series_container | GENERIC_BEHAVIOUR | [2697, 2828) | This is a conditional code path, not a count or observation of repeated victim-side requests |
| TX-U05 | Command handlers enumerate drives and list directory contents (7010 / 7011) | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | Command-handler descriptions in the source | The code contains these capabilities; no operator invocation is documented |
| TX-U06 | Command 7017 can receive a file from the operator side and write it to the victim machine | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | [3812, 3835) and following explanation | Capability of the analysed sample; no transfer instance is reported |
| TX-U07 | Command 7018 can read a file from the victim machine and return its contents to C2 | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | [4399, 4428) and following explanation | Capability of the analysed sample; no exfiltration instance is reported |
| TX-U08 | Command 8001 can invoke cmd.exe with redirected input/output to provide a remote shell | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | “8001” command description near the end of the command-handler section | Code capability; no executed operator command or victim session is documented |

The six command codes and their handlers should remain code-level capabilities. The report does not establish that an operator invoked all commands, that all handlers were reached in one infection, or that the code paths were executed against a particular victim. The five-minute sleep is an implementation branch, not evidence of a series of beacon events.

The report also states that the C2 server was unavailable at the time of analysis ([1290, 1367)). This is a key limitation on event observability.

## 4. Time and temporal relations

No attack-event timestamp is supplied for the analysed sample's execution. The publication date is not an attack time. The five-minute interval is a code delay associated with a conditional branch; it is not a source-recorded interval between two observed attack events.

**Primary positive temporal graph:** no candidate edge at this stage.

Do not treat function order, switch-case order, or the sequence of explanations in the article as temporal relations between resolved event instances. The report's reference to Part 1 also does not automatically establish that the two articles describe separate attack events in a shared scope.

## 5. ATT&CK mapping provenance

The article does not provide a publisher-authored ATT&CK technique-ID table. The AnnoCTR MITRE-link inventory is a separate mention-level annotation layer and cannot be used to infer that every described command handler is an accepted technique mapping.

No event-level mapping is accepted in this draft. In particular, do not map the remote shell code path to T1059 or file movement code paths to other techniques without a source-grounded mapping decision tied to a resolved occurrence. A mapping of a capability may be recorded separately if the protocol supports it, but it must not be represented as an observed event mapping.

## 6. Feasibility assessment

This report is a useful challenge case for distinguishing reverse-engineered capabilities from actions actually observed in an intrusion. It also tests how the protocol handles unknown execution counts and unavailable C2 infrastructure.

The source supports a structured inventory of sample behaviours, but it does not currently support a primary event-instance graph. That is not an eligibility failure and must not trigger advancement to the next hash-ranked report.

**Working recommendation:** retain in the rank-1 feasibility queue while source-scope, local-use and rights decisions are completed. Do not treat this recommendation as a formal eligibility decision.

## 7. Researcher decisions and unresolved checks

1. Confirm that a sample reverse-engineering report is within the declared CTI-report scope even when it provides capability analysis rather than a victim-side incident timeline.
2. Keep Part 1 separate from this report unless a documented scope decision requires otherwise.
3. Decide how sample-level code capabilities are recorded so they remain visible without entering the primary event graph.
4. Confirm local research-use permission for the AnnoCTR text.
5. Review Lab52's publisher legal notice against the corpus-level licence evidence before public redistribution of source text, spans or adapted annotations. Do not assume that the corpus-level licence resolves every item-level question.

**No human eligibility decision, event instance, temporal relation, technique mapping, denominator contribution or projection result is created by this draft.**

## 8. Evidence pointer convention

Offsets are zero-based, end-exclusive Unicode code-point indices into the exact decoded AnnoCTR text at the pinned source revision above. They are locators, not labels. Re-open the source text at each pointer before accepting any annotation.
