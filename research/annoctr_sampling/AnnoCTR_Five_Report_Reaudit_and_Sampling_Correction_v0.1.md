# AnnoCTR five-report re-audit and sampling correction v0.1

**Review date:** 3 November 2026  
**Purpose:** reconcile the five rank-1 source reviews, annotation triage, sample-adequacy audit, rights checkpoint, and Protocol v0.4-draft.  
**Status:** AI-assisted source and method re-audit. This document does not create human gold labels, make the researcher's final eligibility decisions, or freeze the sample.

## 1. Executive decision

The five rank-1 candidates should **remain in the current base-feasibility candidate queue** while the researcher completes eligibility decisions. Do not reject or replace a report simply because the AI source pass has not identified two resolved event leaves or a positive same-technique temporal edge.

The later `AnnoCTR_Sample_Adequacy_and_Fallback_Audit_v0.1` introduced a per-report event-enumerability gate and a recommendation to advance to rank 2 when rank 1 did not meet it. That rule is **not consistent with the earlier sampling method or the stated research question as currently written**. It would condition the base sample on reports being event-rich, which changes the estimand and can bias the pilot toward reports that are easier to represent as event graphs.

The correct separation is:

1. **Sample eligibility:** can the source be faithfully reviewed and annotated under the protocol, with identity, scope, provenance, and uncertainty preserved?
2. **Annotation result:** how many mentions, resolved atomic events, series, episodes, aggregates, and generic behaviours does the report actually support?
3. **Temporal result:** which positive temporal relations, if any, are explicitly supported between resolved event leaves?
4. **Projection result:** for those supported event edges, what happens when endpoint mappings are projected to distinct ATT&CK technique pairs?

A report with no resolved event pair may still be an important negative/unknown outcome in the base feasibility sample. A report does not need a positive same-technique pair to qualify.

## 2. What the current AnnoCTR work has established

### 2.1 Corpus and frame

The official AnnoCTR manifest contains 400 report IDs: 70 train, 16 dev, 34 test, and 280 ext. The pilot's manifest-defined GNE+CyNE subset is the 120 train/dev/test reports. Vendor counts in that subset are Intel471 30, Lab52/S2 Grupo 23, Proofpoint 28, QuoIntelligence 12, and ZScaler 27.

The screening found:

- all 400 manifest reports have the expected base text, full-linking, MITRE-only-linking, and TimeML files;
- 118/120 GNE+CyNE reports have cyber-specific linking records;
- 112/120 have at least one valid canonical ATT&CK technique link;
- eight reports have no valid ATT&CK technique link;
- two manifest entries have no cyber-specific linking records and remain documented frame edge cases;
- across the TimeML exports there are 3,324 TIMEX3 tags and no EVENT, MAKEINSTANCE, TLINK, or SIGNAL tags.

Therefore the supplied TimeML does not provide event-instance or event-to-event temporal-relation gold. Those annotations must come from source review. The repeated technique-link counts are retrieval/mention cues, not event counts.

### 2.2 Candidate selection method

The frame uses the fixed priority seed `CTI-EVIDENCE-LAB-ANNOCTR-PILOT-2026-11-03-v1` and ascending SHA-256 order within each vendor stratum. The five reports below are rank 1 in their respective strata. The method document describes a **five-report feasibility pilot**, not a prevalence study. The candidates have not yet become the selected/frozen sample.

The current sampling method says to advance to the next hash-ranked report only if the current candidate fails source identity, provenance/rights, or practical annotation eligibility. It also expressly says that a positive same-technique temporal pair is not required.

## 3. Reconciled five-report source review

| Vendor / candidate | What the source actually supports | What must not be inferred | AI triage status (not final human decision) |
|---|---|---|---|
| **Intel471 — Groove/Babuk/RaaS ecosystem** | Several separate contexts: RaaS ecosystem and forum history; old Babuk victim/leak references; a BlackMatter victim's data on the same server; a Groove victim; and a broad behaviour/TTP description. The report explicitly says its TTP list is compiled from older Babuk cases and recent Groove-linked cases. | Do not merge all victims, forum events, actor claims, and generic TTP phases into one incident timeline. The repeated T1486 link mentions are not ransomware-execution counts. Victim/leak references do not automatically resolve two attack-event instances in a shared scope. | **LIKELY ANNOTATABLE — high scope/provenance risk.** Retain as a useful mixed-scope report. Researcher eligibility pending. |
| **Lab52 — TokyoX Part 2** | One reverse-engineered sample. The text describes its mutex check, victim-ID construction, first C2 packet, six command codes/functions, and a five-minute sleep/re-request code path for an unsupported command. It states that the C2 server was unavailable during analysis. | The command handlers are capabilities/code paths, not proof that an operator invoked each command on a victim. The five-minute sleep is code timing, not evidence of repeated victim-side beacon events. Part 1 and Part 2 are related posts but should not be merged without explicit scope reasoning. | **LIKELY ANNOTATABLE — generic-behaviour heavy.** Retain as a useful test of capability-versus-execution and unknown-count handling. Researcher eligibility pending. |
| **Proofpoint — Privacy Tools / Smoke Loader** | One described privacy-themed campaign. The source explicitly describes Smoke Loader being downloaded first and its infection subsequently downloading follow-on data-stealing malware, with RedLine and Raccoon identified as second-stage payloads. It also mentions related samples publicly shared by other researchers since March 2021. | Do not treat malware-family names, domains, C2 URLs, or externally shared related samples as separate report-local executions. Do not infer that RedLine and Raccoon were both installed in the same host infection or order them relative to each other. The loader-to-payload wording is an explicit chain/stage sequence, but it is not automatically a pair of resolved host-specific event leaves. | **LIKELY ANNOTATABLE — campaign/chain scope.** Keep the described sequence as a chain-level temporal cue pending researcher granularity decision; do not force it into the strict event graph. Researcher eligibility pending. |
| **QuoIntelligence — Winnti historical analysis** | Separate German chemical-company and South Korean gaming-company sample/target contexts, with historical Winnti references and a separate APT41 campaign discussion. The German case includes a reported attack-awareness interval in the second half of 2019, sample detection in January 2020, and 2015 compilation metadata. The South Korean sample is described as detected/submitted on 21 February, with the year not restated in that sentence, and a likely Gravity target assessment. | Do not merge the two sample/target contexts or historical campaigns. Do not treat compilation, upload/detection, or media-awareness time as attack execution time. The report's “Friday, 13 January” sentence omits a year and does not align with the executive summary's January 2020 statement; preserve the ambiguity rather than repairing it. The 21 February year must also remain unstated unless the source itself supplies it. | **LIKELY ANNOTATABLE — multi-case/date uncertainty.** Strong protocol-debugging value; no source-grounded event-pair conclusion yet. Researcher eligibility pending. |
| **ZScaler — Netwire RAT spear-phishing campaign** | The source gives one specific email-send candidate at 30 June 2021, 10:44 AM PKT, with a named subject and attachment. It separately says multiple documents were delivered in various spear-phishing attacks and describes three distinct document artifacts/hashes. It describes a conditional macro → VBA/PowerShell → payload process and later Netwire functionality. | The three hashes prove three file artifacts, not three separate email sends or executions. Only one email is individually timestamped. The other deliveries remain an unenumerated series unless further evidence distinguishes them. The macro/payload description is conditional technical behaviour, not a timestamped host-event log. The article's “campaign beginning July 2021” statement and 30 June email date should both be preserved as a scope/time tension; they do not establish a clean event order. | **LIKELY ANNOTATABLE — multi-artifact campaign.** One atomic email event candidate, one repeated-series container, and conditional/report-level behaviour units are proposed. Researcher eligibility pending. |

### 3.1 Canonical publisher-page verification — 5 November 2026

The five rank-1 candidate records already contain canonical URLs. A separate publisher-page check confirmed the source title and publication date for each record. This establishes source identity/provenance only; it does not make a source-scope, local-research-use or public-reuse decision.

| Candidate | Official publisher page | Publication date | Identity note |
|---|---|---|---|
| Intel471 — Groove/Babuk/RaaS | https://www.intel471.com/blog/groove-gang-ransomware-babuk-revil-blackmatter | 9 September 2021 | The publisher page confirms the article and explicitly notes that it also ran on McAfee Enterprise ATR. Treat the McAfee version as syndication of this article, not a second report. |
| Lab52 — TokyoX Part 2 | https://lab52.io/blog/tokyox-dll-side-loading-an-unknown-artifact-part-2/ | 12 January 2022 | The official Lab52 archive lists Part 2 on 12 January and the separate Part 1 on 10 January. Keep the two posts separate unless an explicit scope rule justifies combining them. |
| Proofpoint — Privacy Tools / Smoke Loader | https://www.proofpoint.com/us/blog/threat-insight/malware-masquerades-privacy-tool | 1 July 2021 | Publisher title and date match the AnnoCTR source record. |
| QuoIntelligence — Winnti historical analysis | https://quointelligence.eu/2020/04/winnti-group-insights-from-the-past/ | 20 April 2020 | Publisher title and date match the AnnoCTR source record. |
| Zscaler — Netwire RAT spear-phishing | https://www.zscaler.com/blogs/security-research/targeted-attack-government-organizations-delivers-netwire-rat | 14 July 2021 | Publisher title and date match the AnnoCTR source record. |

All five `canonical_source_url` fields were already populated in the sample-frame CSV; no sample-frame URL values needed to be changed. The Intel471 syndication relationship remains a provenance/rights question. The Lab52 item is Part 2, not the separately dated Part 1.

### 3.2 Mapping-provenance checks

The MITRE-only AnnoCTR link exports contain 63 records / 20 unique IDs for Intel471; 15 / 10 for Lab52; 8 / 8 for Proofpoint; 41 / 14 for QuoIntelligence; and 69 / 17 for ZScaler. These are annotation-layer link mentions, not executions or event-instance mappings.

Publisher-explicit ATT&CK tables are not uniform across the five sources:

- Intel471 has a report-level TTP list explicitly compiled from older Babuk and recent Groove-linked cases, plus a conditional T1486 item if a ransomware partnership is achieved.
- Lab52 does not provide a publisher-authored ATT&CK-ID table in the article; its TTP descriptions are prose about the sample.
- Proofpoint does not provide a publisher-authored ATT&CK-ID table in the article.
- QuoIntelligence provides seven publisher-explicit IDs in its report-level table: T1215, T1068, T1009, T1014, T1116, T1022, and T1048.
- ZScaler provides eight publisher-explicit IDs in its report-level table: T1547, T1056, T1036, T1113, T1082, T1055, T1555, and T1074. AnnoCTR mention links such as T1566 and T1059 are not entries in that publisher table and require separate source-supported analyst mapping before use.

No report-level TTP table or AnnoCTR mention count should be copied automatically onto every activity unit or event leaf.

## 4. The methodological correction

### 4.1 Retire the per-report event-enumerability eligibility gate

The later adequacy audit asks for at least two potentially distinguishable activity occurrences or bounded episodes before a report can advance to the primary event-pair test. That requirement should **not** control inclusion in the five-report base feasibility sample under the current research question and sampling plan.

Why:

- The research asks how often the source reports support the target structure. A report with no resolved event pair is part of that answer.
- Selecting only reports with two or more distinguishable events conditions the sample on an outcome-related property and changes the denominator.
- The protocol already defines `GENERIC_BEHAVIOUR`, `UNRESOLVED`, `repeated_event_series`, and aggregate/episode containers so these cases can be recorded without fabricating events.
- The protocol states that only resolved atomic `event_leaf` units enter the primary event-instance graph. Episodes and other containers are kept separate; they are not substitutes for atomic event leaves in the primary graph.

The event-enumerability audit remains useful as a **descriptive diagnostic** of how much of each report is usable for primary graph construction. It is not a pre-selection exclusion rule for the base sample.

### 4.2 Keep distinct analysis denominators

Report separately:

1. all substantively eligible sampled reports;
2. reports with at least one resolved atomic event leaf;
3. reports with at least two resolved atomic event leaves within a compatible scope;
4. reports with at least one source-supported positive temporal edge between resolved event leaves;
5. reports with at least one positive edge whose endpoint mapping sets intersect (a shared technique);
6. event edges that are fully omitted, partially represented, or have no diagonal mapping after projection.

This prevents a denominator for an edge-level projection statistic from being confused with the report-level sample denominator. No complete all-pairs negative matrix is required; the protocol's primary temporal product is positive relation discovery.

### 4.3 Keep episode analyses separate

The protocol allows a separate episode-level sensitivity/exploratory view, but episode containers must not be pooled with atomic event leaves in primary event counts or edge denominators. If the project later wants to compare bounded activity episodes, define and report that analysis separately.

### 4.4 When advancing to rank 2 is legitimate

Advance to the next hash-ranked candidate only when the current candidate fails a pre-specified source/identity/provenance or practical annotation eligibility rule. Do **not** advance because the candidate has no positive same-technique pair, no repeated mapping mention, or too few atomic events. Additional rank-2 reports can be added later as part of a larger pre-specified sample, not used as event-rich replacements for rank-1 reports.

## 5. Rights and publication handling

The AnnoCTR repository README identifies the corpus folder as CC BY-SA 4.0. Keep the attribution and licence evidence. The licence question is separate from whether a report can be annotated locally.

The current item-level scan leaves public text reuse at **AMBER**:

- Intel471's current site terms and the McAfee cross-post create an unresolved publisher/donor scope question.
- Lab52/S2 Grupo's legal notice is the strongest apparent conflict with the corpus-level CC BY-SA statement; clarify before reproducing or adapting its report text publicly.
- For Proofpoint, QuoIntelligence, and ZScaler, no article-specific open licence was verified in the existing rights scan. Do not assume unrelated product or desktop terms govern the blog articles.

Continue local analysis with provenance. For public outputs, prefer report ID, title, publisher, URL, source-text hash, concise paraphrase, and line/paragraph locators. Do not publish raw reports or lengthy source excerpts until rights are clarified. CTI Evidence Lab's MIT code licence does not relicense the report content.

## 6. What is and is not done

### Done

- Official AnnoCTR corpus archive integrity checked and extracted locally.
- 400-report manifest and 120-report GNE+CyNE frame screened.
- Valid ATT&CK mapping availability inventoried; TimeML limitations recorded.
- Five vendor-stratified rank-1 candidates identified using a fixed hash-priority seed.
- Common source triage completed for all five, including scope, activity-unit, time-type, mapping-provenance, and rights cautions.
- Separate working ZScaler source-pass and comparison workbooks were prepared locally. They are not distributed in this repository; the text-free frame CSV and this report are the version-controlled summary of candidate identity, status and source-review cautions.

### Not done

- No researcher eligibility decision has been locked for any of the five reports (0/5).
- No final base report has been selected or frozen.
- No source mention/event-instance annotation has been human-locked.
- No primary event graph, same-technique temporal-edge count, or projection-loss result has been produced from this five-report batch.
- No inter-annotator agreement evidence exists.
- The five-report pilot cannot support a population prevalence estimate.

## 7. Recommended next sequence

1. Mark the event-enumerability eligibility gate in `AnnoCTR_Sample_Adequacy_and_Fallback_Audit_v0.1` as superseded for base-sample selection; preserve the file as an audit trail rather than deleting it.
2. Keep the five rank-1 candidates in their current order. Complete the researcher eligibility decisions based on faithful annotatability, source identity, and the rights/provenance handling appropriate to local annotation and planned publication.
3. For any report accepted into the pilot, complete human source annotation in this order: scope boundaries → mentions and evidence spans → activity units/granularity/instance status → mapping provenance → positive temporal relations → annotation lock.
4. Build the event graph and technique projection only from locked `RESOLVED` atomic event leaves and source-supported positive relations. Keep series, episodes, aggregates, and generic behaviours in separate registers.
5. Report both the full report denominator and the narrower event/edge denominators. Keep the pilot explicitly feasibility-oriented.

**Bottom line:** the five candidates are still useful and should not be discarded for failing to produce the desired structure. The research outcome is not “find five reports with same-technique temporal pairs”; it is to measure what the source reports actually support, including when they do not resolve event identities or temporal relations.
## Rights/source-terms verification addendum — 5 November 2026

**Purpose:** record current primary-source terms that affect two of the fixed rank-1 candidates. This is a provenance and permissions checkpoint, not legal advice and not a final legal determination.

### Corpus-level licence evidence

The AnnoCTR repository README states that the `AnnoCTR` corpus is licensed under **CC BY-SA 4.0** and identifies Intel471 and Lab52/S2 Grupo among the report donors. The repository was archived on 19 February 2026. This is the licence statement attached to the distributed corpus; it does not by itself resolve any conflict with a donor's separate website terms or establish the exact scope of permissions granted for every downstream annotation/reuse scenario.

Source: https://github.com/boschresearch/anno-ctr-lrec-coling-2024

### Intel471 — current terms require clarification

The current Intel471 Terms of Service state that website content is owned or licensed by Intel471, that use of the website does not grant content rights, and that copying, reproducing, downloading or distributing content requires prior written authorization unless expressly provided by the terms. The AnnoCTR report itself says it also ran on McAfee Enterprise ATR, which adds a syndication/rights-chain question.

Sources:
- https://www.intel471.com/legal/terms-of-service
- https://www.intel471.com/blog/groove-gang-ransomware-babuk-revil-blackmatter

**Disposition:** do not infer that the corpus-level CC BY-SA statement is invalid, and do not infer that it resolves all present uses. Record the report-level rights state as **UNRESOLVED** for local research use and public reuse pending clarification of the donor authorization and any applicable McAfee rights. Do not publish raw text or extended spans.

### Lab52 / S2 Grupo — direct reproduction restriction requires clarification

The current Lab52 legal notice states that a user may download one copy of a page for offline viewing for personal, non-commercial purposes. It separately prohibits reproducing all or part of the site and prohibits reproduction, distribution, copying or transformation of site content without prior written authorization.

Source: https://lab52.io/legal_note

**Disposition:** this is a material conflict to reconcile with the AnnoCTR corpus-level CC BY-SA 4.0 statement and the repository's acknowledgement that Lab52/S2 Grupo donated reports. Do not conclude that local research annotation is either permitted or prohibited solely from these two records. Keep both local research use and public reuse **UNRESOLVED** pending written clarification of the donation/licence scope. Do not publish raw text or extended spans.

### Proofpoint — no public-blog reuse grant established

The public threat-intelligence article carries a current copyright footer. Its linked Proofpoint Terms and Conditions page is a directory for customer agreements, product/API terms and support-service terms; it does not state a general licence for public blog content. A separate login.portal End User Terms page last modified in 2014 governs Proofpoint Services and registered-user contexts, so it was not treated as the governing rights instrument for this public article. No article-specific reuse grant was verified.

Sources:
- https://www.proofpoint.com/us/blog/threat-insight/malware-masquerades-privacy-tool
- https://www.proofpoint.com/us/legal/license
- https://login.proofpoint.com/termsconditions/

**Disposition:** the absence of a located article-specific grant is not a legal conclusion that research use is prohibited. Keep local research use and public reuse **UNRESOLVED** pending confirmation of the corpus/donor permission chain.

### QuoIntelligence — portal terms do not cover the public article

The public Winnti article footer links to Terms and Conditions expressly scoped to the Mercury client portal and registered users. Those portal terms do not establish the licence for the public blog article. The current QuoIntelligence privacy policy concerns personal-data processing, not content reuse. A similarly named Quintel Intelligence Ltd terms page on a different domain and legal entity was not treated as applicable to this QuoIntelligence GmbH article. No article-specific reuse grant was verified.

Sources:
- https://quointelligence.eu/2020/04/winnti-group-insights-from-the-past/
- https://quointelligence.eu/terms-conditions/
- https://quointelligence.eu/privacy-policy/
- https://www.quintelintelligence.com/terms-of-use/

**Disposition:** the portal terms and privacy policy do not settle article-reuse permission. Keep local research use and public reuse **UNRESOLVED** pending confirmation of the corpus/donor permission chain.

### Zscaler — blog disclaimer but no content reuse grant

The public Netwire article contains an informational/as-is disclaimer and says content may change, but the page does not state a reuse licence. Zscaler's current Legal Overview points to an End User Subscription Agreement for purchased Zscaler products; that customer-product agreement is not a general licence for blog content. The article carries a Zscaler copyright footer. No article-specific reuse grant was verified.

Sources:
- https://www.zscaler.com/blogs/security-research/targeted-attack-government-organizations-delivers-netwire-rat
- https://www.zscaler.com/legal/overview
- https://www.zscaler.com/legal/end-user-subscription-agreement

**Disposition:** the absence of a located article-specific grant is not a legal conclusion that research use is prohibited. Keep local research use and public reuse **UNRESOLVED** pending confirmation of the corpus/donor permission chain.


### Operational rule pending clarification

- Keep raw report text outside Git.
- Keep exact/extended source spans out of public project files.
- Continue to record report IDs, source URLs, source hashes and concise source-grounded paraphrases.
- Do not convert `rights_review_status` prose into `local_research_use_status=PERMITTED` or `public_reuse_status=PERMITTED`.
- Keep these permissions separate from source-scope eligibility and from the scientific question of whether a report contains resolvable event instances.

This addendum does not alter the five-report candidate order, the 120-row sampling frame, source-scope eligibility decisions, local-use decisions, public-reuse decisions or human annotation status.

## Dataset-maintainer licence clarification addendum — 5 November 2026

The rights/source-terms review above records what was found on individual publisher sites before the dataset maintainer's response. A written reply from the AnnoCTR dataset contact was received on 5 November 2026. He stated, to the best of his recollection, that the source-material licences had been carefully checked and permit redistribution under the dataset licence; he also said researchers may add annotations or change reports and publish derivative works under the same CC BY-SA licence. He expressly noted that this was not legal advice.

This response changes the project-level permission decision: for the five rank-one reports included in AnnoCTR, the sampling frame now records `local_research_use_status=PERMITTED` and `public_reuse_status=PERMITTED`, subject to the AnnoCTR CC BY-SA 4.0 attribution and ShareAlike conditions. The reply did not enumerate individual reports or provide an exception list. The earlier publisher-site findings remain factual descriptions of those sites' terms, but they do not override the dataset maintainer's clarification about the corpus contribution/licence chain. Reopen only if later evidence identifies a specific exception or different rights holder.

The permission clarification does **not** select any report, resolve source-scope eligibility, validate event identities, or approve human annotations. The five researcher/source-scope eligibility decisions remain pending (0/5); human-locked annotations remain 0. Keep raw corpus files and extended verbatim excerpts out of Git. The project MIT licence applies to its original software/documentation, not source reports or adapted annotation material; publish derivatives under the same CC BY-SA licence with attribution and ShareAlike.
