# AnnoCTR research-use permission clarification v0.1

**Prepared:** 5 November 2026  
**Status:** Written dataset-maintainer clarification received 5 November 2026; current working decision and limits are recorded in Section 6.  
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

These are separate use decisions. The maintainer clarification supports local academic annotation and publication of derivative works under the dataset licence. The project still does not plan to redistribute the raw corpus or publish extended verbatim source spans.

## 4. Candidate-specific follow-up

The dataset maintainer has now responded that source-material licences were checked and permit redistribution under the dataset licence, and that annotations/adaptations may be published under the same ShareAlike licence. No separate vendor follow-up is currently required by that response. Reopen a report-specific inquiry only if new evidence identifies an exception or inconsistent rights-holder chain.

- **Intel471 / McAfee syndication:** confirm the specific Groove/Babuk report's rights chain and whether the AnnoCTR copy is covered by the dataset licence.
- **Lab52 / S2 Grupo:** confirm the TokyoX Part 2 contribution is included in the donor permission for the corpus release.
- **Proofpoint, QuoIntelligence and Zscaler:** confirm their contributed reports are covered by the same corpus-level grant and identify any exceptions.

Do not contact every vendor with a generic request before the maintainer clarifies what was actually granted.

## 5. Decision rule after the maintainer response

- For the five rank-one AnnoCTR candidates, set `local_research_use_status=PERMITTED` and `public_reuse_status=PERMITTED`, with the dated response recorded as the basis.
- Treat public reuse as permission to publish derivative works under the same AnnoCTR CC BY-SA licence, not as permission to remove attribution, ignore ShareAlike or relicense adapted report material under MIT.
- Attribute AnnoCTR and each original report/publisher, identify modifications, and apply CC BY-SA 4.0 to adapted annotation material where the licence applies.
- Keep raw report files and extended verbatim source spans outside Git. This project does not plan to republish the raw corpus.
- Keep source-scope eligibility, researcher review, report assessability and annotation readiness separate from the rights fields. Permission does not make a report substantively eligible or annotatable.
- Reopen a candidate-specific rights question only if new evidence identifies a report exception, a different rights-holder chain or a rights-holder objection. Do not replace a candidate because of event yield.

**Current outcome:** the maintainer clarification supports local research annotation and publication of derivative works under the dataset's CC BY-SA licence. This is a working decision based on the maintainer's qualified recollection, not a legal opinion or a separately executed grant from each vendor.

## 6. Written dataset-maintainer clarification — 5 November 2026

A written email response was received from the AnnoCTR dataset contact on 5 November 2026. The response stated, in substance, that the source-material licences had been carefully checked and allow redistribution under the dataset licence; that researchers may add annotations or change reports; and that derivative works may be published provided they remain under the same CC BY-SA licence. The maintainer qualified this with “if I remember correctly” and stated that it was not legal advice.

### Working interpretation

- The clarification supports private local academic source review and manual annotation of reports included in AnnoCTR, including the five fixed rank-one candidates, subject to any later-identified exception.
- It supports publication of derivative annotation material under the same CC BY-SA licence (the AnnoCTR repository identifies this as CC BY-SA 4.0).
- The reply did not list each report or vendor individually and did not provide an exception schedule. No report-specific exception is currently known from the response; if one is later identified, revisit only the affected report.
- Continue to attribute AnnoCTR and each original report/publisher, identify modifications, and apply ShareAlike to adapted material. The repository's MIT software licence does not relicense source reports or derivative annotation datasets.
- This project will not commit the raw AnnoCTR corpus or extended verbatim report excerpts. Exact internal evidence spans remain in local annotation materials unless a later publication plan separately verifies the appropriate attribution and reuse treatment.

### Candidate status update

For the five fixed rank-one candidates, the working permissions fields are now `local_research_use_status=PERMITTED` and `public_reuse_status=PERMITTED`, with this dated response as the basis. `source_scope_eligibility` and `researcher_review_status` remain pending; no candidate is thereby selected or formally approved for annotation.

**Limitations:** this records the substance of the email, not the email itself. It is not legal advice, a legal opinion, or independent confirmation from each vendor/rightsholder.
