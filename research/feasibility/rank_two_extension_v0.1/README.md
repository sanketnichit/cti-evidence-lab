# Fixed rank-two source review

**Five additional reports, selected before this review by the existing donor ranks.** The original rank-one cohort remains unchanged. The [selection and protocol commit](https://github.com/sanketnichit/cti-evidence-lab/commit/14c0355bb478eb23e613ce018d387815b50891d6) precedes the review records. This is an exploratory extension, not independent validation or an externally preregistered study.

## Findings

All five complete corpus texts were read, including their captions and tables. The pass establishes no qualifying three-occurrence intrusion sequence. It does preserve explicit temporal claims and sample-execution observations that must not be reduced to an undifferentiated absence of evidence.

| Source | Evidence retained | Why primary sequence queries are not assessed |
|---|---|---|
| Intel471, DarkSide overview (10 May 2021) | Observed affiliate procedures, including exfiltration before ransomware deployment | Generalized affiliate activity is not bound to one three-action intrusion; the named Colonial incident does not supply that linkage |
| Lab52, China and the Persian Gulf (18 February 2020) | Reconnaissance explicitly placed two weeks before phishing receipt | A partial, aggregate chain; document execution is conditional and a third observed action is unresolved |
| Proofpoint, TA505 activity (19 October 2021) | Observed campaign waves and detailed loader transitions | Multiple campaigns and an optional KiXtart stage; no selected particular execution binds the full chain |
| QuoIntelligence, Zebrocy (22 September 2020) | Specific executable, copy/task sequence and live POST observations during analysis | Analysis-environment execution is explicit; victim-side execution and individual action boundaries remain unresolved |
| Zscaler, PurpleWave (14 August 2020) | Configuration requests, module retrieval and an observed downloaded payload | Several binaries/configurations; no selected run binds all three actions in a victim intrusion |

The QuoIntelligence result is especially relevant to interpretation: sample execution is evidence of execution, although it answers a different question from execution in a victim intrusion. Lab52 similarly contains an explicit temporal claim even though the report is largely geopolitical. Neither case should be discarded merely because it does not supply a primary three-action graph.

No event-level ATT&CK mappings are accepted in this pass. Report-level labels, campaign membership, dated email exemplars and sample hashes are not substitutes for resolved occurrences and compatible scope. The review records a strongest candidate, contrary interpretation, separate identity/scope/order/mapping judgments, and remaining resolution for every report.

## Coverage and integrity

- Selected: **5** reports; complete text readings: **5**; replacements: **0**.
- Source identities verified against the frozen frame: **5**.
- Passage bindings verified: **22**; raw source text redistributed: **0**.
- Primary three-occurrence sequences established: **0**; query errors: **not assessed**.

These counts describe this review. Zero established sequences does not mean zero sequences in the reports or corpus. The original five reports, these five additional reports and the separate DFIR intrusion are distinct records with different selection histories; their outcomes are not pooled into a prevalence estimate.

The local corpus requires CRLF-to-LF recovery to match the recorded source hashes exactly. Original files are unchanged. Hashes and offsets verify source identity and locators, not the semantic assessments or completeness of evidence selection. Images and external links were not inspected. The five frozen frame rows lack canonical publisher URLs; this pass verifies corpus identities, not independently resolved publisher-page provenance.

## Artifacts and reproduction

The [protocol](PROTOCOL.md) and [selection](selection.json) fix scope and membership. [Review records](review.json) contain judgments and source offsets; [integrity results](source_integrity.json) verify the bindings; [summary results](results.json) preserve unassessed query errors as `null`.

```sh
python scripts/audit_rank_two_review.py
python scripts/audit_rank_two_review.py --corpus-root /path/to/AnnoCTR/all --recover-crlf
python scripts/reproduce_study.py --corpus-root /path/to/AnnoCTR/all --recover-crlf
```

Without source files, the first command checks complete selection coverage and regenerates the summary. The second rechecks source hashes and all passage bindings. The full reproduction includes both the original cohort and this extension, recording whether audits were reused or freshly run.

Source-derived records are adapted from [AnnoCTR, Bosch Research](https://github.com/boschresearch/anno-ctr-lrec-coling-2024) and the five publishers named above, and retain [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) terms. The project's MIT license does not relicense the source reports. No raw text or extended quotations are distributed here.
