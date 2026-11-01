# Project Status — 2026-11-01

**Current phase:** Research question refinement and dataset feasibility.  
**Implementation status:** Toy projection and annotation-validation prototypes added; real-data ingestion and modelling not started.  
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

Measure how often two distinct report-local event instances mapped to the same ATT&CK technique have an explicitly supported temporal relation, and what event-level temporal information becomes unrepresentable when those occurrences are projected to a distinct-technique-pair representation that excludes diagonal pairs.

This is a descriptive measurement study first. A predictive event-relation model is not currently part of the primary plan; any model extension must be justified by the human pilot and a fresh baseline audit.

This is a hypothesis to test—not a validated gap, novel method, implemented system, or publication claim.

## New working artifact

- Drafted `research/ANNOTATION_PROTOCOL_v0.3.md` to separate text mentions, event instances, ATT&CK concepts, temporal relations, and non-temporal dependencies. It supports multiple ATT&CK mappings per event instance and clarifies the candidate-pair/negative-label frame. It remains a draft for human review, not a validated annotation standard.
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

The researcher owns final research decisions, human annotations, experiment execution/reproduction, interpretation and conclusions. Evaluation labels must be created and verified by humans against the original source evidence.


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
5. Double-annotate a subset with another human if possible; gold labels must be created and verified against the source text.
6. Define projection metrics and test toy cases before coding a complete system.

**Implementation remains not started. Novelty remains not established. Current decision remains NARROW.**


### File-level source inspection completed

- Opened one actual AnnoCTR report and its paired BIO labels, MITRE-only linking annotations and TimeML file. The source report is 15,211 characters, with 32 technique-link records across five ATT&CK techniques; 24 mention/link records map to T1059. Its TimeML has 31 TIMEX3 elements but no EVENT, MAKEINSTANCE or TLINK elements.
- This confirms the per-report files are suitable for a human screening/annotation workflow, but do not provide temporal event relations. Repeated technique-link mentions are not automatically distinct executions.
- Candidate screening seed: `intel471_2020-03-26_analysis-of-an-attempted-attack`. It remains a candidate only; human annotators must decide whether any mentions refer to distinct event instances and whether explicit temporal evidence exists.
- The AnnoCTR GitHub repository was reported as archived on 19 February 2026; this does not itself invalidate the corpus, but maintenance should not be expected.


## Pilot and prototype setup — 1 November 2026

### Source screening
- Screened five AnnoCTR Intel471 reports at file level. Repeated ATT&CK-linked mentions occur in several, but the repeated records are not event-instance labels. Their TimeML files contain TIMEX3 expressions but no EVENT, MAKEINSTANCE or TLINK elements.
- Added `research/ANNOCTR_SCREENING_LOG.md` and `research/PILOT_REPORT_01_STARTER.md`. Report 01 is shortlisted for a first human protocol dry run only; provenance and the source donor details must be verified before treating it as formal pilot data.
- The five screened reports are all Intel471. This is a selection limitation. Do not claim multi-vendor screening or general prevalence.

### Annotation and implementation artifacts
- Annotation protocol v0.3 now allows multiple separately evidenced ATT&CK mappings per event instance and separates specific report-local events from generic behaviour statements.
- Four blank CSV templates are available under `research/templates/`, with row granularity and label instructions in `research/templates/README.md`.
- Added `src/projection_metrics.py`, a pure-Python synthetic projection prototype; `tests/test_projection_metrics.py`; and `examples/toy_projection_demo.py`.
- Added `src/annotation_validation.py` and `tests/test_annotation_validation.py` for source-span, ID and evidence structure checks.
- Added a GitHub Actions workflow for the standard-library tests. [Latest run #15](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/41296800818) passed all 24 synthetic unit tests and smoke-tested the toy projection demo on commit `572fe30`. This verifies the toy code paths only; it is not evidence from real CTI reports.
- These utilities are scaffolding only. They have not been run on human-annotated CTI data and do not establish a research finding.

### Immediate human task
Read Report 01 in full and complete the first event-mention and event-instance decisions against the original source text. Use the starter guide and record annotation time and unresolved decisions. A second human reviewer is strongly preferred.

**Current status:** implementation of toy metric/validation helpers has begun; production pipeline/model not started; human annotations zero; experimental results zero; novelty not established; decision NARROW.


### Full-corpus sampling preparation — 1 November 2026

- Verified the AnnoCTR paper's five-donor counts: Intel471 30, Lab52 23, Proofpoint 28, QuoIntelligence 12 and ZScaler 27 reports in the 120-report cybersecurity-specific subset.
- Confirmed the paper's licence distinction: donor reports were permitted for republication under CC BY-SA 4.0; the proceedings PDF itself carries a CC BY-NC 4.0 notice. Keep those licences separate.
- Confirmed the annotation process distinction: the general layer was annotated by two trained annotators; the cyber-specific layer was produced by one domain specialist. The paper's rough comparison for document-level technique sets gave mean F1 around 0.54, and the authors say it was not a formal agreement study.
- Added `scripts/screen_annoctr.py` and synthetic tests `tests/test_annoctr_screening.py` so the complete local `AnnoCTR/all/` folder can be inventoried by donor before choosing reports. The tool outputs aggregate counts only, not raw text or event labels.
- The official AnnoCTR `splits.tsv` manifest identifies 120 GNE+CyNE reports in `train`, `dev` and `test`, and 280 additional GNE-only reports in `ext`. Vendor counts for the 120 are Intel471 30, Lab52 23, Proofpoint 28, QuoIntelligence 12 and ZScaler 27, matching the paper. The initial scanner's count of 117 referred only to reports with at least one cyber-specific record detected in the `linking_mitre_only` export; it was not the corpus's document-level CyNE denominator.
- The first diagnostic used `linking_mitre_only` to detect CyNE presence. That was incomplete: the paper defines CONCEPT (CON) as a CyNE type linked to Wikipedia, not MITRE ATT&CK. The Intel471 Oldsmar report therefore appeared missing in the MITRE-only export but actually has five CON records in the full `linking` export and eight CON tokens in its BIO/JSON data. Two reports remain with no observed CyNE labels in the inspected full linking and BIO/JSON files: Proofpoint `proofpoint_2021-05-24_compromised-cloud-accounts-cost-firms` and QuoIntelligence `quoteintelligence_2020-07-09_what-is-tiber-eu-and`. They are included in the 120-report split manifest but contain only general-layer tags in the released mention-level files. The scanner now reads the full `linking` export for all CyNE types, while retaining `linking_mitre_only` for technique-link frequencies. It also excludes `_w_con`, `_w_neg` and `_w_con_w_neg` variants, recognizes `quoteintelligence`, and only treats canonical MITRE ATT&CK URLs as technique IDs. GitHub Actions run #23 passed 27 tests and the synthetic projection smoke test. The initial five-report Intel471 screen remains a convenience sample.

- Added `research/ANNOCTR_CANDIDATE_CONTENT_REVIEW_v0.1.md` as a provisional manual-review queue across the five vendors plus challenge cases. It is explicitly not a frozen sample. The base reports still need to be selected from the complete eligible pool by a recorded seed/deterministic rule after provenance, hash and duplicate checks; the console's top-five-by-mention lists are not a sampling frame.

**Next:** sync and run the corrected scanner, review the regenerated full inventory CSV, verify vendor/source file pairing and provenance, then complete the human dry run in `research/PILOT_REPORT_01_STARTER.md`. Report 01 is an initial dry-run candidate, not a confirmed or random sample.


### ChronoCTI pair-universe finding — 1 November 2026

The ChronoCTI paper does not merely use technique-level pairs in general. Section 4.5.2 defines all candidate pairs over 120 techniques as ((120^2-120)/2), which excludes every diagonal pair ((T,T)). The public graph code also loops over technique indices only when `idx1 != idx2`. Thus, if a report contains two distinct event instances mapped to the same technique and a positive temporal relation between them, that relation has no candidate pair under this distinct-technique-pair universe.

The paper's task and pair cardinality are described in Sections 2.3 and 4.5.1–4.5.2: https://doi.org/10.1007/s10115-025-02491-6

This is a verified representational limitation of the inspected ChronoCTI setup. What remains unverified is how often real reports contain such event-instance relations. Our pilot must measure that; the code now reports fully omitted vs partially represented multi-mapped event edges.


### Annotation protocol v0.3 — candidate-pair frame

- Clarified that positive relation discovery is a full-report pass, while NO_TEMPORAL_CLAIM / VAGUE_OR_AMBIGUOUS / NOT_ASSESSABLE can only be assigned to candidate pairs that were actually assessed under a frozen rule.
- Unannotated event pairs are not automatically negatives. If a future prediction task is defined, it requires a separate pair-universe and negative-sampling protocol.


## Current working hypotheses (not established)

- H1: In some CTI reports, two distinct human-resolved event instances map to the same ATT&CK technique and have an explicitly supported temporal relation.
- H2: A unique-technique-per-report projection or distinct-technique-pair candidate universe can make at least some such event-level temporal relations unrepresentable.
- H3: The size and practical significance of this omission can be measured reliably from report text using a transparent human annotation protocol.

The pilot must be allowed to reject all three. No prevalence, accuracy, or performance result exists yet.
