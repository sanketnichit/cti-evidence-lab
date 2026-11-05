# AnnoCTR Candidate Content Review v0.1

**Status:** preliminary content-review queue only. No report has been selected for the formal 5–8 report pilot.
**Date:** 1 November 2026
**Inventory basis:** local scanner output from the 400-report AnnoCTR corpus. The candidate locators below are ranked by repeated canonical ATT&CK technique-link mentions. These counts are not event instances, executions, or temporal relations.

## Important sampling rule

The five `BASE_STRATIFIED` reports must be selected from each vendor's full eligible pool using a recorded random seed or a documented deterministic rule, after the file, hash, source-provenance, rights and duplicate checks. Do **not** simply take the highest repeated-mention report from each vendor.

The reports below form a **manual content-review queue** and a reserve pool for the additional `PURPOSIVE_STRESS` slots. They are not the frozen sample. No positive-edge quota is permitted, and the presence of repeated technique mentions must not be used as evidence that two distinct event instances exist.

## Content-review queue

| Report ID | Vendor | Scanner locator summary | Content-based reason to inspect | Current caveat |
|---|---|---:|---|---|
| `intel471_2021-12-09_emotet-returns-december-2021` | Intel471 | 42 repeated mentions; 14 unique techniques; 13,286 chars | Report on Emotet's return, loader/protocol changes and two newly observed botnets (Epoch4/Epoch5). It may help test whether repeated mentions refer to distinct botnet-specific actions or repeated descriptions of one capability. | Corpus text says 9 Dec 2021; the current Intel471 page search result displays 8 Dec 2021. Resolve the one-day date discrepancy in the provenance record before selection. Official page: https://intel471.com/blog/emotet-returns-december-2021 |
| `lab52_2022-01-24_new-transparentribe-operation-targeting-india` | Lab52 / S2 Grupo | 34 repeated mentions; 12 unique techniques; 8,906 chars | A named operation targeting Indian government and military personnel. The text describes a suspicious IMG file, a COVID-19 lure document and an infection sequence, making it a useful report to test action boundaries across a compact campaign narrative. | Confirm the article's direct canonical permalink and source-text date against the vendor page before freezing. The vendor's archive lists the title and 24 Jan 2022 date: https://lab52.io/blog/page/8/ |
| `proofpoint_2021-10-19_whatta-ta-ta505-ramps-activity` | Proofpoint | 60 repeated mentions; 10 unique techniques; 16,165 chars | Covers September and October 2021 TA505 campaigns and describes a multi-stage chain from email/Excel lures through intermediate loaders to FlawedGrace. Strong candidate for testing whether a long technical chain can be split into distinct, evidence-supported event instances. | Avoid conflating separate campaign waves with one incident or treating each malware stage as a separate event without source evidence. Official page: https://www.proofpoint.com/au/blog/threat-insight/whatta-ta-ta505-ramps-activity-delivers-new-flawedgrace-variant |
| `quoteintelligence_2021-06-30_daily-operations-of-a-nigerian` | QuoIntelligence | 65 repeated mentions; 35 unique techniques; 19,235 chars | Investigation begins with a malicious Word document associated with Agent Tesla and expands into the operations of an eCrime gang. This may exercise the distinction between a concrete report-local incident and broader actor behaviour. | High technique diversity may reflect broad reporting rather than many discrete occurrences. Original canonical article URL was not independently located in this check; keep on hold until provenance is confirmed. |
| `zscaler_2021-04-14_look-hydrojiin-campaign` | ZScaler | 95 repeated mentions; 24 unique techniques; 19,641 chars | Describes a named campaign involving several infostealer RAT families and miner malware, with an ongoing activity window. Good candidate for testing multiple malware families and campaign sub-events without assuming every behaviour statement is an event. | The article itself says the impact of the campaign is unknown; retain uncertainty and avoid inferring victim-side executions. Official page: https://www.zscaler.com/it/blogs/security-research/look-hydrojiin-campaign |
| `proofpoint_2021-07-28_i-knew-you-were-trouble` | Proofpoint | 33 repeated mentions; 16 unique techniques; 12,596 chars | A years-long social-engineering operation followed by a specific June 2021 malware-delivery attempt. Useful stress candidate for long-range relationship-building versus the later intrusion actions. | Do not turn every benign contact or persona activity into an intrusion event. Official page: https://www.proofpoint.com/uk/blog/threat-insight/i-knew-you-were-trouble-ta456-targets-defense-contractor-alluring-social-media |
| `intel471_2021-09-09_groove-gang-ransomware-babuk-revil` | Intel471 | 46 repeated mentions; 20 unique techniques; 23,835 chars | A broader RaaS/affiliate analysis with multiple actor relationships, observed behaviours and victim discussion. Useful stress candidate for attribution ambiguity and whether repeated technique references can be tied to separate report-local incidents. | More than one group/affiliate relationship raises attribution and event-scope risks. The corpus text references a McAfee Enterprise ATR mirror; verify the primary source and any syndication relationship before selection. |
| `zscaler_2021-05-05_catching-rats-over-custom-protocols` | ZScaler | 117 repeated mentions; 27 unique techniques; 24,742 chars | A broad technical comparison of custom command-and-control protocols across RAT families. This is a deliberate challenge case for separating generic capability descriptions and cross-family examples from specific event instances. | It may be too generic to contribute many report-local event instances. A zero-event/zero-relation outcome is valid; do not retain it merely because it has the highest mention count. Official page: https://www.zscaler.com/blogs/security-research/catching-rats-over-custom-protocols |

## Three split-assignment edge cases

The first scanner diagnostic used `linking_mitre_only` to detect cybersecurity-specific annotation presence. That export is not the full CyNE layer: the AnnoCTR paper defines CONCEPT (CON) as a cybersecurity-specific type but states that CON, ORG and LOC are linked to Wikipedia, whereas GROUP, TACTIC and TECHNIQUE are linked to MITRE ATT&CK.

- `intel471_2021-02-12_scada-oldsmar-florida-water-treatment` has five CON records in the full `linking` export and eight CON tokens in `ner_json`. It should not be treated as missing CyNE annotation just because its MITRE-only link file is empty.
- `proofpoint_2021-05-24_compromised-cloud-accounts-cost-firms` has only general-layer labels in the inspected full linking and BIO/JSON files.
- `quoteintelligence_2020-07-09_what-is-tiber-eu-and` likewise has only general-layer labels in the inspected full linking and BIO/JSON files.

The latter two are present in the 120-report split manifest but have zero observed CyNE labels in the released mention-level files. Do not silently remove them from the corpus denominator or describe them as missing files. Record them as split-assigned reports with no observed CyNE mentions, and exclude them from a technique-mention-based candidate pool where appropriate.

## Second-pass source-text review — 5 November 2026

The two split-assigned reports with no observed CyNE labels were re-read from the official AnnoCTR source-text files. This is a source-content assessment, not a formal researcher eligibility decision. Both remain in the 120-report manifest inventory. Their `source_scope_eligibility`, local-use, public-reuse and researcher-review fields in the canonical sample frame remain unchanged pending explicit recording.

| Report | Source identity | Source-grounded content finding | Working source-scope recommendation |
|---|---|---|---|
| `proofpoint_2021-05-24_compromised-cloud-accounts-cost-firms` | Official AnnoCTR text blob `57d13668f0269456d384a7fcb13a1965bfaacb57`; frame source-text SHA-256 `3df25b357989da047e8240475771597675c2d1d63221c85d632ca8c863403f34`. | Sponsored summary of a Ponemon Institute survey of 662 IT/security practitioners. It reports aggregate cloud-account-compromise costs, downtime and security practices. It discusses compromise as an industry risk but does not describe a report-local intrusion, actor operation, campaign or source-grounded sequence of cyber activity. | **Recommend INELIGIBLE for the declared CTI-report source scope.** The basis is the article's survey-summary/marketing genre, not the absence of AnnoCTR CyNE or ATT&CK labels. |
| `quoteintelligence_2020-07-09_what-is-tiber-eu-and` | Official AnnoCTR text blob `87eaa93d19177c90a4a68ca5d3b1c5c78b43c3e5`; frame source-text SHA-256 `3d42974b233e1f0d250b4ff402bccdfb0b85f472334e9660612598541add9e6b`. | Part I of a two-part explainer describing the TIBER-EU ethical red-team testing framework, its objectives and benefits for financial institutions. References to real-life threat scenarios describe the framework's design; the post does not report a specific observed intrusion, threat actor operation or campaign. | **Recommend INELIGIBLE for the declared CTI-report source scope.** The basis is the general framework-explainer genre, not the absence of AnnoCTR CyNE or ATT&CK labels. |

**Sampling consequence:** retain both rows in the official 120-row frame for auditability. If the researcher confirms these recommendations, mark them out of source-scope eligibility and exclude them from `N_eligible`; do not delete them or replace them within the historical frame. The six other no-link reports are unaffected and remain eligible for source-first review if their own gates pass.

## Evidence and rights notes

The AnnoCTR paper describes 400 reports with general-world entity annotations, of which 120 were also annotated with cybersecurity categories. It reports the donor distribution as Intel471 30, Lab52 23, Proofpoint 28, QuoIntelligence 12 and ZScaler 27. The paper states that the commercial CTI vendors agreed to republication of the blog entries under CC BY-SA 4.0. Keep this corpus licence separate from the proceedings PDF's CC BY-NC 4.0 notice.

Paper: https://aclanthology.org/2024.lrec-main.103/
Corpus repository: https://github.com/boschresearch/anno-ctr-lrec-coling-2024

For every report that advances, record the exact original source URL, source title/date, vendor, repository path, SHA-256 hash of the local source text, licence/provenance evidence, and duplicate/syndication review. The corpus-level licence statement is useful evidence but does not replace a per-report provenance record.

## Next decision

1. Sync and run the corrected scanner that counts CyNE types in the full `linking` export and ATT&CK mentions in `linking_mitre_only`.
2. Review the regenerated 400-row CSV and use all eligible report rows—not only the top-five console locators—to form the candidate pool.
3. Verify source URLs, hashes and duplicates.
4. Select the five base reports by a recorded seed/deterministic rule from the eligible pool; then consider up to three stress reports from the review queue above.
5. Freeze no pilot membership until these checks and the human dry run are complete.

**No event instances or temporal relations have been labelled in this review. No prevalence or novelty conclusion follows from it.**
