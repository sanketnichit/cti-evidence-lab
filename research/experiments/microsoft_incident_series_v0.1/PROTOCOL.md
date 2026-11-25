# Microsoft Cyberattack Series incident comparison

Frozen 25 November 2026 before reviewing the linked full reports. The publisher's landing pages and their introductory descriptions were visible during source selection.

## Selection

Use installments 1 and 2 of the original Microsoft Cyberattack Series. The first two entries form a consecutive prefix confirmed by the publisher in its [third installment](https://www.microsoft.com/en-us/security/blog/2023/06/29/patch-me-if-you-can-cyberattack-series/). The cutoff is two reports to keep this comparison at the same report count as the DFIR chronological holdout and CISA comparison. Position in the series determines inclusion.

| Installment | Date | Publisher landing page |
|---|---|---|
| 1 | 8 February 2023 | [Solving one of NOBELIUM’s most novel attacks](https://www.microsoft.com/en-us/security/blog/2023/02/08/solving-one-of-nobeliums-most-novel-attacks-cyberattack-series/) |
| 2 | 26 April 2023 | [Healthy security habits to fight credential breaches](https://www.microsoft.com/en-us/security/blog/2023/04/26/healthy-security-habits-to-fight-credential-breaches-cyberattack-series/) |

The selected artifact for each installment is the full report linked from its landing page through the publisher's report download. Retain both entries in the results. Record an unavailable, ambiguous or non-extractable report with its reason. A landing-page summary or another installment cannot substitute for an unavailable report. Record the resolved PDF URL, retrieval date, byte hash, extraction version and pages reviewed.

## Evidence and comparison

Review the narrative prose describing observed incident activity across the PDF. Record explicit exclusions for recommendations, generic attacker procedures, incident response actions, and forecasts of what could have happened. Figures and tables are outside this text-only comparison. Keep scope explicit for different incidents or independent actors and retain only ordering supported within each scope. Timestamp evidence can establish an order when both times refer to the identified actions on the same time axis. Chapter order and adjacency of sentences do not establish a relation.

Bind each retained action and each explicit BEFORE edge to a PDF page and a character range in its canonical text. Use the [CISA PDF audit convention](../cisa_incident_extension_v0.1/README.md#reproduction) for extraction and hashing. Record repeated actions separately only when the text distinguishes the occurrences. Retain outcome uncertainty and withhold parent ATT&CK v12.1 labels where a mapping requires an unsupported assumption. Include source-based rationales and plausible alternative readings in the case record.

Use the existing [incident comparison](../incident_holdout_v0.1/README.md#reproduction) with the same query contract. Enumerate three-label queries from the known parent vocabulary in each retained graph. Compare the occurrence reference with ordinary distinct pairs, ordinary loop-inclusive pairs and both endpoint joins. Report supported, unsupported and mapping-unresolved queries separately. Where the graph cannot support an assessable three-action query, publish the evidence and exclusions with the comparison marked unassessed. Use report-level outcomes and show each comparison separately.

This sample adds a commercial incident-response publisher and a different editorial series. Its findings will remain conditional on the retained interpretations. Publisher selection and the two-report prefix do not support a population estimate or a released benchmark of independent annotations.
