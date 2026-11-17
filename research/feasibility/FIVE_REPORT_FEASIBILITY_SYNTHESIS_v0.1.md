# Five rank-one reports: feasibility synthesis

**17 November 2026. Status: assessment of preliminary source-review notes, not final annotation.**

The five rank-one AnnoCTR candidates were selected by fixed within-donor hash priority, not by positive temporal-relation yield. Their five existing source-first notes are working drafts. None has a completed human eligibility decision, reviewed and locked event annotation, or accepted event-edge projection.

| Source | What the source-first draft actually supports | Main risk for the primary question |
|---|---|---|
| Intel471, Groove/Babuk | RaaS history, actor descriptions, mixed victim examples and generic TTP profile | Descriptions from different operations cannot be combined into a single event sequence |
| Lab52, TokyoX Part 2 | Malware sample and reverse-engineered command capabilities | Implemented code paths are not proof that commands ran on an observed victim |
| Proofpoint, Privacy Tools | A possible download chain with two proposed stages | Distinct event instances, incident scope and both accepted ATT&CK mappings remain unresolved |
| QuoIntelligence, Winnti | More than one sample/target context and uneven temporal detail | Source contexts and event occurrence identity remain ambiguous |
| Zscaler, Netwire RAT | One identifiable phishing-email send with a source-reported time | A single send does not make a temporal pair; document hashes do not count sends |

**No accepted within-technique relation is established in these drafts.** This is **not** a 0/5 measured rate, because the source-scope eligibility gate and complete human annotation are still open. Incomplete review and no positive relation are different outcomes.

## What the sample can establish

A complete review could show whether a protocol can accurately separate attack occurrences, actor-level generalizations, sample capabilities, analyst observations, and report sections describing multiple operations. Even if no qualifying pair survives, that is valuable *feasibility evidence* and a warning against estimating prevalence from a convenience sample.

## What to do next

1. Keep the five candidate IDs and hash ordering fixed. Do not replace reports just because an event relation is missing.
2. Complete a short first-pass, full-source report-genre and event-evidence review for each candidate, recording the real reviewer and source hash. Record negative and unresolved outcomes explicitly.
3. Use `SINGLE_ANNOTATOR_FINAL` for the first feasibility pass only when the actual source review, source lock, protocol and selection conditions are satisfied. Do not label an ordinary repeated pass as independent.
4. Keep a separate overlapping independent review plan for IAA. If no second human reviewer participates, explicitly say agreement was not measured.
5. If the fixed sample yields no convincing event pair, make a **separate predeclared incident-narrative feasibility cohort**, based on source genre and narrative detail—not by searching for examples that show the desired loss. Report such a cohort separately, not as a replacement for the first five.
6. If source evidence or agreement cannot support the main relation, narrow the study to evidence limitations rather than forcing event graphs.

## Relation to the exploratory DFIR example

The earlier case [A Truly Graceful Wipe Out](../exploratory/DFIR_Repeated_RDP_Source_Contrast_v0.1.md) illustrates a conditional repeated-occurrence projection, but is not in this sample and is not an independent annotation. It adds no candidate to the five-donor frame and makes no denominator contribution.

For detailed source notes, refer to the five separate files in `research/feasibility/` and the canonical frame `research/annoctr_sampling/AnnoCTR_Fresh_MultiVendor_Sample_Frame_v1.0.csv`.
