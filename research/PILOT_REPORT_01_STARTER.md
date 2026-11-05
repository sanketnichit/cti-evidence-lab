# Feasibility Dry-Run — Candidate 01

**Status:** rank-one candidate only; not formally selected or approved for annotation. This is a protocol-debugging dry-run, not a result or prevalence observation.
**Working protocol:** `research/protocol/CTI_Event_Instance_Annotation_Protocol_v0.5-draft.md`.
**Working schema:** `research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/` (reconstruction only; not frozen or approved).

## Source identity

- **Report ID:** `intel471_2021-09-09_groove-gang-ransomware-babuk-revil`
- **Title:** *How Groove Gang is shaking up the Ransomware-as-a-Service market to empower affiliates*
- **Publisher/date:** Intel471, 9 September 2021
- **Canonical publisher page:** https://www.intel471.com/blog/groove-gang-ransomware-babuk-revil-blackmatter
- **AnnoCTR source revision:** `d510b6949e1938d47c93a43eedd562dc538439dc`
- **Source-text SHA-256:** `87e1e45070dffc9ae446013754ae6466c28cc5910c56501c4d8f1dcb573e7d56`

Source files at the pinned AnnoCTR revision:
- [Full report text](https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/d510b6949e1938d47c93a43eedd562dc538439dc/AnnoCTR/all/text/intel471_2021-09-09_groove-gang-ransomware-babuk-revil.txt)
- [MITRE-only linking records](https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/d510b6949e1938d47c93a43eedd562dc538439dc/AnnoCTR/all/linking_mitre_only/intel471_2021-09-09_groove-gang-ransomware-babuk-revil.json)
- [TimeML file](https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/d510b6949e1938d47c93a43eedd562dc538439dc/AnnoCTR/all/time/intel471_2021-09-09_groove-gang-ransomware-babuk-revil.tml)

The source identifies that the article also ran on McAfee Enterprise ATR. Treat that as a syndication/source-family note, not a second independent report. Review the original source and report identity before any derived material is published.

## Eligibility and rights are separate

- The frame records local research use and derivative-publication reuse as `PERMITTED` based on the AnnoCTR maintainer's qualified 5 November 2026 clarification; attribution and ShareAlike conditions apply.
- `source_scope_eligibility` remains `PENDING` and `researcher_review_status` remains `NOT_REVIEWED` in the canonical frame. This starter does not approve the report.
- The report remains one of five rank-one candidates, not a selected final sample member.
- Do not commit raw report text or extended verbatim spans. The repository MIT licence does not relicense AnnoCTR material.

## Exposure warning

This candidate has already been the subject of a source-first feasibility review. The researcher’s pass must therefore be recorded as `AI_EXPOSED`, not blind. A later reread or washout does not remove that exposure. The existing feasibility draft is a locator for protocol issues only; it is not an annotation, a gold label, or a source of event IDs to copy.

## What this report is useful for testing

The article combines RaaS ecosystem history, forum communications, Babuk/Groove background, victim references, and generalized actor-level TTP descriptions. Do not collapse those contexts into one incident or one timeline. In particular:

1. Separate contextual actor/forum communications from intrusion activity.
2. Keep the different victim references in distinct scopes unless the source explicitly connects them.
3. Distinguish actor-profile behaviour, repeated series, episode containers, and particular resolved occurrences.
4. Do not assign every technique in the report-level TTP list to every candidate activity unit.
5. Do not infer a positive temporal edge from the order of sections or from the order of a generalized attack-phase description.

The preliminary feasibility draft currently identifies no clearly resolved pair of intrusion event leaves in a shared scope. Re-open the source and decide independently; do not force a positive edge. A zero-event-leaf or zero-edge outcome is acceptable if supported by the complete source review.

## Dry-run procedure

1. Save the exact pinned source locally and verify that its decoded text hash matches the value above. Preserve its original line endings and do not normalize Unicode.
2. Record source provenance, hash, extraction method, scope boundaries and `prior_exposure_status=AI_EXPOSED` in the RECON report registry.
3. Read the complete source. Record candidate action mentions as exact zero-based, end-exclusive source spans.
4. Assign mention status, then create activity units. Only `RESOLVED` atomic `event_leaf` units may enter the primary event graph.
5. Record ATT&CK mappings only when the report supports them for the specific activity unit. Treat the AnnoCTR linking export as a candidate locator, not ground truth.
6. Search for explicit temporal relations only after event identity and scope are resolved. Every positive relation needs relation-specific evidence and a direct source/timestamp basis.
7. Record uncertainty rather than inventing execution counts, host identity, attribution, event identity or chronology.

Use the 12 blank registers under `research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/registers/`. Do not use the older v0.3 CSV templates with the RECON validator.

## Stop point

This is protocol debugging only. Do not lock the annotation partition or run projection metrics until Protocol v0.5 and a new schema version have been explicitly approved and frozen. If another human is available, an independent overlapping review is needed to measure IAA; AI is not a second annotator.

**Current status:** no human annotations, no accepted event instances, no accepted mappings, no temporal relations, and no projection results have been produced for this candidate.
