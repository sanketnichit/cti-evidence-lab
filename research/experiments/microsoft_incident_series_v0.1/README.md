# Microsoft Cyberattack Series results

The first two installments were fixed in the [protocol](PROTOCOL.md) and published in [5b5297c](https://github.com/sanketnichit/cti-evidence-lab/commit/5b5297c5910210554e31b2bd071ae24ff46360b7) before reviewing the full reports. One of the two selected PDFs was available for review.

| Installment | Source evidence | Primary result |
|---|---|---|
| 1 · NOBELIUM | Six pages reviewed. Three reported actions, one explicit ordering link and two withheld mappings. | Unassessed. The retained graph has no connected two-edge path. |
| 2 · Credential breaches | The landing-page download leads to a PDF whose cover identifies it as installment 4. | Selected report unavailable through the recorded link. |

The prose in installment 1 identifies a prior compromise and a later implant that modified authentication. It also describes actor-attributed authentication activity from captured requests. The retained prose gives no explicit ordering link between the implant and those particular requests. Pages 2 and 5 carry more detailed ordering in an attack-flow diagram and a numbered recap panel. The primary frame covers narrative prose, so their chronology stays outside the primary graph. Page 4 mixes narrative, responder actions, technical analysis and recommendations. The source record describes which column and evidence role each locator refers to because layout extraction interleaves some lines.

A post-review sensitivity check adds implant-before-request if the captured requests are interpreted as exercising the installed implant. This creates one candidate path. With the single known parent label T1556, its only constructed query is three repetitions of that label. The first and last actions have withheld mappings, so the open rule yields one unresolved answer. None of the four projected views returns it. The assumption changes the assessment from unassessed to mapping-unresolved without establishing a fully mapped witness.

The [case record](report-1.json) stores eight page locators, the mapping decisions and the excluded readings. The [unavailability record](report-2-unavailable.json) stores the mislinked PDF hash and a cover locator. The latter document contributes only evidence of the link mismatch. Both installments remain visible in [results.json](results.json). The sample illustrates the effect of publication format and source availability on assessability. It supplies no estimate of sequence prevalence or annotation reliability.

## Reproduction

```sh
python scripts/evaluate_microsoft_series.py
python scripts/evaluate_microsoft_series.py --pdf-directory outputs/microsoft-incident-series
```

The first command reproduces the results from the case records. The second requires `pypdf==6.21.4`, the verified installment 1 PDF saved as `report-1.pdf`, and the mislinked PDF saved as `excluded-report-4.pdf`. It checks both byte hashes and all nine recorded spans. Offsets count Unicode code points in whitespace-normalized layout text, with an exclusive end. For semantic review, inspect the rendered pages to separate the columns. Neither PDF is redistributed. [Installment 1 publisher PDF](https://download.microsoft.com/download/4/6/5/4650b04f-7db6-4a87-bf82-8ed1ad1c001c/MS%20Security%20Experts%20Cyberattack%20MagicWeb%202023.pdf), [installment 2 landing page](https://www.microsoft.com/en-us/security/blog/2023/04/26/healthy-security-habits-to-fight-credential-breaches-cyberattack-series/).
