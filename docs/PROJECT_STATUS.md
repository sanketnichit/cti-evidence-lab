# Project Status — 2026-11-01

**Current phase:** Research question refinement and dataset feasibility.  
**Implementation status:** Not started.  
**Novelty status:** Not established.  
**Current decision:** NARROW.

## Completed discovery and verification

- Audited the seven initial project blueprints.
- Verified ChronoCTI as a direct temporal CTI baseline. Its paper represents attack actions as ATT&CK techniques and predicts temporal relations between technique pairs within a report.
- Inspected the official ChronoCTI code. Temporal-pair processing uses report, T1, T2, and relation labels; graph construction creates technique-plus-report nodes, not a separate graph node for every report-local execution.
- Confirmed that the ChronoCTI paper links public Figshare version 3 for data and code: https://doi.org/10.6084/m9.figshare.26039518.v3. The complete Figshare file manifest, exact schemas, and item licence have not yet been independently inspected. The GitHub README says intermediate outputs are not in the code repository and describes a substantial model-storage requirement. Do not assume either that the published data are unavailable or that the complete pipeline is readily reproducible.
- Recorded ChronoCTI's reported evaluation: 94 curated reports / 7,052 sentences, 120 selected ATT&CK techniques, macro precision/recall/F1 of 0.75/0.46/0.54 for relation classification, and MUC-5 precision/recall/F1 of 0.58/0.25/0.34 for graph construction.
- Recorded ChronoCTI's documented limitations: severe class imbalance, upstream error propagation, low recall, restricted technique vocabulary, ground-truth dependence on annotator judgement, and 45–60 minutes of temporal annotation per report.
- Corrected the Attack Flow interpretation: an arrow between actions represents dependency/enabling conditions, not simply temporal BEFORE. Official documentation: https://center-for-threat-informed-defense.github.io/attack-flow/introduction/.
- Inspected the SMAH-CTI public JSON schema. It contains sentence-level records with action spans, ATT&CK tactic/technique labels, preceding-sentence context and grounded procedure text. It does not define document-level event coreference chains or event-to-event temporal links.
- Identified AnnoCTR as a possible English CTI source corpus with cybersecurity entity/ATT&CK linking and TIMEX annotations; TIMEX is not a substitute for event-to-event TLINK or event coreference.
- Identified APTIE as an adjacent Chinese CTI resource with sentence-scoped event annotations, but not document-level temporal event relations.
- Identified MAVEN-ERE as general-domain event coreference and temporal-relation prior art, not a CTI-specific benchmark.
- Added a preliminary research-gap/reproducibility audit at `docs/RESEARCH_GAP_AUDIT_2026-11-01.md`.

## Current candidate

Measure how much event-instance identity and explicitly supported temporal structure is lost, conflated, or made ambiguous when distinct report-local actions are represented using report-level ATT&CK technique nodes or technique-pair relations.

A secondary experiment on evidence-linked event-instance relation extraction may follow only if the annotation pilot is feasible.

This is a hypothesis to test—not a validated gap, novel method, implemented system, or publication claim.

## New working artifact

- Drafted `research/ANNOTATION_PROTOCOL_v0.1.md` to separate text mentions, event instances, ATT&CK concepts, temporal relations, and non-temporal dependencies. It defines evidence-span requirements, uncertainty labels, a 5–8 report feasibility pilot, and stop criteria. This is a draft for human review, not a validated annotation standard.
- Confirmed the repository citation metadata already encodes the author's name correctly: given name `Sanket`, family name `Nichit`. The generated abbreviated citation `Nichit, S.` is the normal family-name-first bibliographic rendering; the README also gives the full-name form `Sanket Nichit`. No author-field correction is required.

## Blocking gates

1. Inspect ChronoCTI Figshare v3 metadata, all files, schemas, versions and licence.
2. Inspect exact AnnoCTR and SMAH-CTI data formats, source provenance and rights for intended use.
3. Identify candidate reports with distinct repeated occurrences of one technique, not merely repeated textual mentions.
4. Run a small 5–8 report annotation feasibility pilot. This is not a prevalence estimate.
5. Measure annotation effort, unresolved cases, positive temporal relation counts and independent annotator agreement where a second annotator is available.
6. Only then select corpus size, baselines, split strategy, metrics and implementation scope.

## Decision rule

If repeated distinct occurrences are rare, source text cannot lawfully be used, or event-instance distinctions cannot be annotated consistently, do not force the hypothesis. Pivot to a benchmark audit or another data-supported CTI question.

## Student-led research

The student researcher owns final research decisions, human annotations, experiment execution/reproduction, interpretation and conclusions. AI may support literature discovery, explanations, debugging and review. AI-generated annotations are not gold labels; AI assistance must be logged and disclosed according to institutional and venue policies.


## Follow-up audit — 1 November 2026

### Important prior-art corrections

- **CASIE (AAAI 2020)** already covers cybersecurity event nuggets, event arguments, semantic roles and realis. The paper says event coreference and full knowledge-graph integration were future work in the presented study. Its public repo README mentions a `link_coref.py` helper; its exact implementation and whether any gold coreference outputs exist have not been verified. Do not describe generic cybersecurity event extraction as our novelty.
- **CSEM-CTI (iScience 2026)** mines evidence tokens for sentence-level ATT&CK technique classification and evaluates rationale faithfulness with ERASER. It does not provide report-level event identity or event-to-event temporal relation labels. Therefore generic “evidence-grounded CTI classification” is also not a novelty claim; our evidence must be tied to a relation between two specific event instances.
- **A July 2026 STIX 2.1 CTI preprint** describes 150 report-level graphs with 1,273 attack-pattern objects mapped to ATT&CK. This could already preserve multiple behavior objects per report. However, the preprint explicitly does not model temporal attack sequences and lists temporal relationships as future work. It says dataset/code will be public upon acceptance; no release was found in this check. Revisit this work and its data release before freezing novelty.
- **AnnoCTR** is now the leading pilot candidate: 400 full-text reports, with cybersecurity-specific technique/entity annotations on 120; corpus licence stated as CC BY-SA 4.0; TimeML temporal-expression files are not event-event TLINKs or event coreference. Exact corpus tree and per-report provenance/alignment still need inspection.
- **SMAH-CTI** schema and data licence have been inspected. It is sentence-level with Action spans and ATT&CK labels, not event-event temporal/coreference gold data; CC BY-NC 4.0 dataset and MIT code.

### Refined research direction

The candidate is narrowed to an empirical question: in CTI reports, how often do two distinct event instances map to the same ATT&CK technique, and what explicitly supported event-to-event temporal information becomes unrepresentable, lost or conflated when the report is projected to a unique-technique-per-report or technique-pair graph?

This is not a proven gap. The 2026 STIX preprint is a direct adjacent work for preserving behavior objects; ChronoCTI is the direct temporal technique-pair baseline; CSEM-CTI covers evidence extraction at sentence/technique-classification granularity; CASIE covers cybersecurity event extraction. The contribution must be about temporal relation preservation/loss and supported by a pilot, not generic extraction or graph creation.

### Current next gates

1. Resolve ChronoCTI Figshare v3 files, schema, licence and access status.
2. Inspect AnnoCTR's actual corpus directory/file structure, text-to-annotation alignment and source provenance.
3. Recheck the STIX preprint's acceptance and data release status.
4. Screen 5–8 AnnoCTR reports with transparent selection criteria and manually annotate mentions, event identity, ATT&CK mapping, event-pair temporal labels and relation-specific evidence.
5. Double-annotate a subset with another human if possible; do not use AI output as gold data.
6. Define projection metrics and test toy cases before coding a complete system.

**Implementation remains not started. Novelty remains not established. Current decision remains NARROW.**
