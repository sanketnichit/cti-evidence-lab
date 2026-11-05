# Zscaler — Netwire RAT spear-phishing source-first feasibility draft v0.1

**Status:** Working source-first review only. This is not a human-locked annotation, is not included in any denominator, and is not an empirical result.  
**Review date:** 5 November 2026  
**Candidate:** Rank-1 Zscaler report in the fixed 120-report AnnoCTR frame.

## 1. Source identity and provenance

- **Report ID:** zscaler_2021-07-14_targeted-attack-government-organizations-delivers
- **Title:** *Targeted Attack on Government Organizations Delivers Netwire RAT*
- **Publication date:** 14 July 2021
- **Canonical publisher page:** https://www.zscaler.com/blogs/security-research/targeted-attack-government-organizations-delivers-netwire-rat
- **AnnoCTR text path:** AnnoCTR/all/text/zscaler_2021-07-14_targeted-attack-government-organizations-delivers.txt
- **AnnoCTR source revision:** boschresearch/anno-ctr-lrec-coling-2024, commit d510b6949e1938d47c93a43eedd562dc538439dc
- **Source Git blob:** cbd93ca399e1dc698606d5caf33d53083b489ea8
- **Frame source_text_sha256:** fb95cbd80a60f2aa41a29bd453bf6215b601c061e7fa64bb4bf1bddc18d0c989

## 2. Scope assessment

The article describes a spear-phishing campaign targeting organizations in Pakistan, including government and other industry sectors. It names one specific email send and then describes multiple documents and a malware chain. Keep the identified email, the broader repeated delivery activity and the sample-level malware analysis distinct.

The source says the campaign was beginning in July 2021, but it dates one of the latest emails to 30 June 2021. Preserve this tension as written; do not change the email date or silently redefine the campaign start.

## 3. Candidate activity units

| Candidate ID | Source description | Proposed granularity / role | Instance status | Evidence pointer | Review disposition |
|---|---|---|---|---|---|
| ZN-E01 | One identified spear-phishing email was sent on 30 June 2021 at 10:44 AM PKT, with a named subject and the attachment NSCP-DRAFT-Final.docm | atomic_event / event_leaf | RESOLVED — candidate pending researcher review | [2187, 2265) and the surrounding paragraph | The report identifies one particular send and gives a timestamp; keep recipient multiplicity separate from the send event |
| ZN-U01 | Multiple documents were delivered in various spear-phishing attacks | repeated_event_series / series_container | UNRESOLVED | [3519, 3604) | Repetition is explicit, but the number of distinct email sends and recipient-side executions is not enumerated |
| ZN-U02 | Three document artifacts are analysed, with separate filenames and MD5 hashes | report_level_aggregate / aggregate_container | NOT_AN_EVENT as a send/execution count | “Distribution Strategy” section | Three file artifacts do not establish three separate emails, recipients, document openings or executions |
| ZN-U03 | A document opened and the user enabling macros can trigger AutoOpen, VBA and PowerShell payload download/execution | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | [5351, 5446), [5478, 5545), [5641, 5758) | Conditional sample behaviour; no particular victim host or successful macro execution is identified |
| ZN-U04 | NetwiredRC copies itself to a specified path, uses memory techniques and establishes persistence | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | [6644, 6746), [8322, 8424), [9454, 9538) | Malware-analysis findings; not a sequence of timestamped victim-side event instances |
| ZN-U05 | The malware collects sensitive information and sends it to command and control | unresolved / unresolved_unit | GENERIC_BEHAVIOUR | [11077, 11206) | Capability/behaviour description without a specific victim-side execution timestamp or report-local exfiltration occurrence |

### Event identity cautions

The three MD5 values identify three document artifacts. They do not prove that three emails were sent, that all three documents reached the same victim, or that any of the recipients opened them. Keep ZN-E01 as one identified send candidate. Keep all other deliveries in the repeated series unless the source distinguishes individual send events.

The article describes the later macro and payload process conditionally: once a document is opened and macros are enabled, the code runs. Do not convert a conditional execution path into a resolved event leaf. The fact that the article reverses a malware sample does not establish that every described capability occurred on a particular victim host in this campaign.

## 4. Candidate ATT&CK mapping

The publisher's report-level “MITRE ATT&CK TTP Mapping” table lists T1547, T1056, T1036, T1113, T1082, T1055, T1555 and T1074. It does not list T1566.001.

For ZN-E01, **T1566.001 — Spearphishing Attachment** is a plausible analyst mapping candidate because the source identifies a spear-phishing email carrying a macro-enabled document attachment. The pinned Enterprise ATT&CK v12.1 crosswalk maps T1566.001 to the parent technique T1566 (Phishing), which is in the A_120 vocabulary. This is a vocabulary-compatible candidate, not an accepted mapping. It must be separately reviewed against the event evidence and the project's mapping rules.

Do not assign the publisher's other report-level TTP IDs to ZN-E01 or the unresolved sample-behaviour units automatically. The AnnoCTR link mentions for T1566/T1059 are not a substitute for a source-grounded mapping decision.

## 5. Time and temporal relations

ZN-E01 has a source-reported timestamp: 30 June 2021, 10:44 AM PKT. This timestamp belongs to the email send, not to macro execution, payload download, persistence or data exfiltration.

The broader campaign is described as beginning in July 2021. The source also dates the identified email to 30 June. Preserve both statements and record the scope/time tension for researcher review.

**Primary positive temporal graph:** no candidate edge at this stage.

Only one candidate resolved event leaf is currently identified. The conditional macro/payload behaviour does not provide a second resolved endpoint, so do not create an email-send BEFORE macro-execution or download edge. A sequence in the reverse-engineered code is not enough to establish that the corresponding events occurred in a particular victim environment.

## 6. Feasibility assessment

This report offers the strongest concrete occurrence candidate among the four reviewed here: one identified spear-phishing email with a precise timestamp. It also gives a useful test of how to represent repeated deliveries, multiple artefacts, conditional execution, and report-level versus event-level ATT&CK provenance.

The current source does not yet provide two resolved atomic event leaves with a source-grounded temporal edge. The single email candidate is still useful for protocol feasibility and should not be treated as evidence of a same-technique temporal pair.

**Working recommendation:** retain in the rank-1 feasibility queue while the researcher completes scope and local-use decisions. Do not treat this recommendation or the candidate mapping as a formal eligibility or annotation decision.

## 7. Researcher decisions and unresolved checks

1. Confirm whether the identified email send is accepted as one resolved attack occurrence at the report's stated scope.
2. Record the 30 June timestamp exactly and preserve the article's “campaign beginning July 2021” statement as a separate scope/time note.
3. Keep the additional deliveries as an unresolved repeated series unless individual sends are distinguishable from source evidence.
4. Keep the three document hashes as artifact identities, not message or execution counts.
5. Decide whether T1566.001 is accepted for ZN-E01; preserve its status as an analyst mapping candidate until then.
6. Keep all conditional macro, PowerShell, payload, persistence and C2 behaviours out of the primary event graph unless the report supports a particular victim-side occurrence.
7. Confirm local research-use permission. Public reuse of raw text, spans or adapted annotations remains a separate rights decision.

**No human eligibility decision, locked event annotation, positive temporal relation, denominator contribution or projection result is created by this draft.**

## 8. Evidence pointer convention

Offsets are zero-based, end-exclusive Unicode code-point indices into the exact decoded AnnoCTR text at the pinned source revision above. They are locators, not labels. Re-open the source text at each pointer before accepting any annotation.
