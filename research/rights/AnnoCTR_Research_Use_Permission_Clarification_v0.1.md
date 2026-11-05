# AnnoCTR research-use permission clarification v0.1

**Prepared:** 5 November 2026  
**Status:** Request checklist prepared; no request has been sent and no permission response has been received.  
**Purpose:** Identify the exact rights questions that must be resolved before using AnnoCTR report text for new source annotation or publishing derived research outputs.

## 1. What the public record currently says

The official AnnoCTR repository README states that:

- the dataset contains 400 cyber threat reports obtained from commercial CTI vendors;
- reports were donated by Intel471, Lab52 / S2 Grupo, Proofpoint, QuoIntelligence and Zscaler;
- the corpus located in the AnnoCTR folder is licensed under CC BY-SA 4.0;
- questions about the dataset should be directed to the named dataset contact.

The AnnoCTR paper's abstract also describes the dataset as CC BY-SA-licensed. The repository includes the standard CC BY-SA 4.0 legal code in LICENSE.txt.

This is a meaningful public licence statement. It should not be ignored or treated as though no licence exists. The remaining question is whether the licensor had authority to grant every right needed for the particular third-party report texts and intended downstream uses. The CC BY-SA 4.0 legal code defines Licensed Rights as rights the licensor has authority to license; its general considerations also tell licensors to secure necessary rights and clearly identify material not subject to the licence.

Sources:
- AnnoCTR repository README: https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/main/README.md
- AnnoCTR repository licence: https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/main/LICENSE.txt
- AnnoCTR paper: https://aclanthology.org/2024.lrec-main.103/
- CC BY-SA 4.0 legal code: https://creativecommons.org/licenses/by-sa/4.0/

## 2. Questions for the dataset maintainer

Ask the dataset maintainer to clarify the following points in writing:

1. **Scope of the corpus licence:** Does the CC BY-SA 4.0 statement apply to every original report text file in the AnnoCTR folder, including all 400 vendor reports, or are any report texts, figures, extracts or individual records excluded or subject to different conditions?
2. **Authority and donor permissions:** Did each named vendor/rightsholder expressly authorize redistribution of its contributed report(s) under CC BY-SA 4.0, and is there a report-level exception list?
3. **Local academic research:** Does the published permission cover non-commercial academic use of the report text for source review, manual annotation and analysis?
4. **New annotations and adaptations:** Does it cover creation of new report-local event/occurrence identities, activity-unit groupings, evidence-span references, ATT&CK mappings, time observations and event-to-event temporal-relation labels?
5. **Derived data and publication:** May a researcher publish new annotation tables, event/temporal graphs, report identifiers, source citations, source hashes, methodology and aggregate statistics without republishing report text?
6. **Verbatim evidence excerpts:** Are short source quotations or exact evidence spans with offsets permitted in a paper, appendix, thesis or supplementary material? If yes, are there length, report-count or vendor-specific restrictions? If not, confirm that paraphrased explanations and non-textual span references should be used instead.
7. **ShareAlike and attribution:** If the new annotations qualify as Adapted Material, what attribution and ShareAlike treatment does the maintainer recommend for the derived dataset? Is there a preferred citation/attribution line?
8. **Vendor-specific or syndicated reports:** For any report with a known syndication or third-party rights chain (including the Intel471 Groove/Babuk report that also appeared on McAfee Enterprise ATR), does the corpus grant cover the copy included in AnnoCTR, or is additional permission required from the syndicator or another rights holder?

If the maintainer cannot confirm the rights for all publishers, request the relevant vendor/report exceptions and the correct rights-holder contact route. Do not assume that a general product-portal or website terms page overrides or resolves the dataset-specific grant.

## 3. Planned uses to classify separately

| Intended use | Current status | What must be confirmed |
|---|---|---|
| Keep the original AnnoCTR files in a private local research directory | UNRESOLVED for the five rank-one reports in this project | Whether the dataset grant covers local academic review and annotation |
| Read complete report text for source-first human annotation | UNRESOLVED | Whether the grant covers this research activity |
| Create new occurrence identities, activity-unit records and temporal labels | UNRESOLVED | Whether annotation/adaptation is permitted and any ShareAlike condition |
| Store report IDs, publisher URLs, hashes and non-verbatim metadata in project records | UNRESOLVED as part of the project-specific permission review | Confirm any limits on derivative metadata and disclosure |
| Publish aggregate counts, rates and statistical findings | UNRESOLVED pending confirmation | Whether aggregate outputs may be published; avoid source text |
| Publish derived annotation tables or graphs without source excerpts | UNRESOLVED pending confirmation | Whether these are shareable derived materials and under what licence |
| Publish exact or extended source-text spans | NOT PLANNED unless expressly cleared | Obtain explicit permission and observe any quoting restrictions |
| Redistribute the raw report corpus | NOT PLANNED | No redistribution is proposed by this project |

These are separate use decisions. Permission to conduct local research does not automatically establish permission to reproduce source excerpts or redistribute new annotations.

## 4. Candidate-specific follow-up

The initial request should go to the dataset maintainer because the central question is the scope of the published AnnoCTR licence and the donor permissions behind it. Follow-up with individual vendors only where the maintainer identifies a missing grant, exception or uncertainty.

- **Intel471 / McAfee syndication:** confirm the specific Groove/Babuk report's rights chain and whether the AnnoCTR copy is covered by the dataset licence.
- **Lab52 / S2 Grupo:** confirm the TokyoX Part 2 contribution is included in the donor permission for the corpus release.
- **Proofpoint, QuoIntelligence and Zscaler:** confirm their contributed reports are covered by the same corpus-level grant and identify any exceptions.

Do not contact every vendor with a generic request before the maintainer clarifies what was actually granted.

## 5. Decision rule pending response

- Keep local_research_use_status=UNRESOLVED and public_reuse_status=UNRESOLVED for all five rank-one candidates until adequate written clarification is obtained and reviewed.
- Do not begin formal source annotation merely because the corpus is publicly downloadable or labelled CC BY-SA 4.0.
- Do not infer that use is prohibited merely because current vendor website terms restrict copying of website content; the relationship between those terms and the dataset-specific donation/licence is precisely what needs clarification.
- Keep raw report text and extended source spans outside Git.
- Record the response, date, responding rights-holder, report/vendor coverage, permitted uses, exclusions and attribution conditions before changing any permission field.
- If the response remains ambiguous for one report, keep that report unresolved and assess another fixed candidate only under the already-declared source/rights failure rule. Do not replace it because of event yield.

**Current outcome:** no permission decision has changed. This document prepares a precise clarification request; it does not itself grant permission, record approval or constitute legal advice.