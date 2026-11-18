# Fixed rank-two source extension

**Declared: 18 November 2026. Exploratory source review.**

This extension examines the five rank-two reports in the existing 120-report AnnoCTR frame, one per donor. Selection uses the unchanged seed and within-donor priority ordering of sampling method v0.3.3. It does not replace any rank-one report, broaden the original five-report cohort, or select reports by temporal yield. The external DFIR case remains separate.

`selection.json` fixes report identities, source hashes and priority metadata before source-text inspection for this extension. The declaration is committed before review results. This is a prospective work-order record, not an externally preregistered study or a claim that the reports were never encountered during earlier inventory work. Existing eligibility and annotation locks are unchanged.

## Review scope

Read each complete corpus text after verifying its recorded source hash. CRLF-to-LF recovery is permitted only when the recovered text exactly reproduces that hash. Do not edit original sources. Record inaccessible or mismatched sources rather than replacing them. Linked images, external follow-up reports and underlying telemetry are outside this text-only pass.

For every report, record genre, observation level, strongest sequence candidate, evidence bindings, a contrary interpretation and the unresolved decision. Distinguish particular intrusion actions from campaign aggregates, capability/control flow, sample-analysis activity and publication chronology. A named victim is not required; a coherent source-supported incident scope is. An explicit attempt may be retained without inventing successful execution.

A connected-sequence opportunity requires three distinct attack-action occurrences and two source-supported BEFORE links sharing an intermediate occurrence. Narrative placement, numbered technique lists, dependencies and different payload names alone do not establish those conditions. Record occurrence identity, shared scope, ordering and mapping separately. Do not copy report-level ATT&CK labels onto occurrences. Use the pinned ATT&CK v12.1 vocabulary if an event-level mapping is proposed, with mapping uncertainty retained explicitly.

## Reporting rules

Retain all five dispositions, including unresolved and no-established-sequence outcomes. No substitution, stopping after a positive finding, or enlargement based on event yield is allowed in this extension. A partial chain is not a three-occurrence sequence. An unestablished sequence is not proof of absence. Counts summarize this review only; no corpus prevalence, independent agreement, extraction accuracy or gold-annotation status is inferred.

Store short original assessments and exact source offsets/hashes without redistributing raw text. Adapted corpus-derived records retain AnnoCTR attribution and CC BY-SA 4.0 terms; original software retains the project license. Source verification checks identity and bindings, not semantic correctness.

## Artifacts

- `selection.json`: fixed selection and provenance.
- `review.json`: all five assessments and unresolved alternatives.
- `source_integrity.json`: local source verification and evidence-binding results.
- `README.md`: source coverage, findings and limitations.

References: [sampling method](../../annoctr_sampling/AnnoCTR_Fresh_MultiVendor_Sampling_Method_v0.3.3.md), [original cohort](../exploratory_review_v0.1/README.md), [AnnoCTR](https://github.com/boschresearch/anno-ctr-lrec-coling-2024).
