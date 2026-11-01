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
