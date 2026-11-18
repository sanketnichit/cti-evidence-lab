# Five-report exploratory source review

17 November 2026. **Not independently validated; not formal annotation.**

This pass reads the fixed five AnnoCTR report texts against the current draft event/scope rules. It preserves the sample and records counterarguments rather than treating previous draft decisions as ground truth. Judgments are bound to the source texts. Prior project drafts were available, so this is not a blind assessment.

## Findings

| Report | Interpretation in this pass | What prevents a qualifying primary pair |
|---|---|---|
| Intel471 Groove/Babuk | Actor ecosystem, dated communications and multiple victim contexts | Communications are not attack actions; actor-level procedure is not one resolved incident |
| Lab52 TokyoX Part 2 | Malware capability and reverse-engineering description | Control-flow order does not establish distinct victim-side executions |
| Proofpoint Privacy Tools | Explicitly ordered delivery-chain candidate | Individual occurrences, incident identity and both mappings remain unresolved |
| QuoIntelligence Winnti | Multi-target investigation and sample analysis | Artifact dates and analysis observations do not establish attack chronology |
| Zscaler Netwire | One identifiable email-send candidate | No second resolved occurrence linked to that send and a shared incident |

There is **one retained identifiable attack-occurrence candidate** in this reading, not one final annotated event or a census of all asserted actions. A qualifying within-technique temporal pair is not established in any report. This is not a 0/5 prevalence estimate or proof that the sources contain no such relation. No selected-final partition or real-report projection is created.

The [critical second pass](CRITICAL_REVIEW.md) challenges exclusions using 22 source passages, including material outside the initial anchor set. `critical_evidence.json` records their exact source and substring hashes. It sharpens the distinctions between observed activity, particular occurrences, incident linkage and shared mappings. This is an exposed second analysis, not independent replication.

`review_decisions.json` records each judgment, source hash, evidence pointers, strongest counterargument and remaining resolution. `results.json` is generated from those decisions and the integrity audit; it is not automatic semantic verification. Evidence references use the existing [anchor index](../../annotation_drafts/AnnoCTR_Pilot_v0.1/source_anchor_index_draft.csv). Its section labels are navigational hints: for example, P03's recorded offsets are in Campaign Details despite its older Overview label. The verified offsets and line number take precedence.

## Source verification

The local corpus had CRLF line endings in all 120 frame reports, unlike the recorded LF text hashes. Explicit CRLF-to-LF recovery reproduced all 120 expected hashes exactly. The audit never rewrites the originals or updates expected hashes to make mismatches disappear. All **33** existing pilot pointers have valid bounds, line positions and unique source substrings. Their substring hashes are recorded without exporting text. This verifies locators, not their semantic interpretations or completeness.

`source_integrity.json` records original byte hashes, verified text hashes, transformations and the input metadata hashes. This audit establishes equivalence to the frame's source hashes; it does not independently re-download the pinned upstream commit or verify the original archive ZIP hash.

## Reproduction

```text
python scripts/audit_pilot_sources.py --corpus-root /path/to/AnnoCTR/all --recover-crlf --output research/feasibility/exploratory_review_v0.1/source_integrity.json
python scripts/summarize_exploratory_review.py
python -m unittest discover -s tests -v
```

An already exact LF corpus needs no recovery. Its canonical hashes and pointer results will match, but original byte hashes and transformation counts will differ from this Windows-origin audit. The review conclusions are curated judgments; the commands verify their source bindings and regenerate summaries, not repeat the intellectual review.

## Attribution and reuse

Source-derived review decisions in this directory are adaptations of the AnnoCTR report collection and are provided under **CC BY-SA 4.0**, retaining AnnoCTR and publisher attribution. See the source URLs/titles in the [candidate register](../../annotation_drafts/AnnoCTR_Pilot_v0.1/report_assessment_draft.csv), [AnnoCTR](https://github.com/boschresearch/anno-ctr-lrec-coling-2024), and the [licence](https://creativecommons.org/licenses/by-sa/4.0/). No raw reports or extended quotations are included here. The repository MIT licence does not replace these source-derived data terms.

No independent annotation agreement is available. The [calibration workflow](../../reviewer_kit/COORDINATOR.md) specifies separate first passes, prior-exposure records and reconciliation procedures for future validation.
