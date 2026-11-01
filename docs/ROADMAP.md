# Research Roadmap

This roadmap is gate-driven rather than feature-driven. Dates are planning placeholders; the gates must be satisfied before later work begins.

## Phase 0 — Research integrity and provenance

- [x] Create a separate repository for the project.
- [x] Record the provisional scope and explicit no-novelty-claim status.
- [x] Establish raw-data and secret exclusions in Git.
- [ ] Complete primary-source verification for all high-impact related work.
- [ ] Resolve legal access and redistribution constraints for candidate datasets.

**Exit condition:** sources and data rights are documented sufficiently to choose an evaluation corpus.

## Phase 1 — Dataset feasibility

- [ ] Inspect candidate dataset schemas and annotation guidelines.
- [ ] Check duplicate/syndicated report families and available source text.
- [ ] Quantify report length, event/temporal annotation density, and repeated technique mentions.
- [ ] Determine whether event-to-event relation labels and evidence spans already exist.
- [ ] Select a lawful corpus and document its exact version and access route.

**Exit condition:** dataset supports a reproducible, non-leaky, sufficiently powered pilot.

## Phase 2 — Annotation pilot

- [ ] Freeze an initial annotation guide with positive, negative, and unresolved examples.
- [ ] Independently annotate a small sample with at least two annotators if feasible.
- [ ] Adjudicate disagreements and calculate agreement appropriate to the label structure.
- [ ] Revise or abandon categories that are not consistently annotatable.
- [ ] Estimate full-study annotation cost.

**Exit condition:** label definitions are stable enough for evaluation.

## Phase 3 — Research design

- [ ] State the exact question and hypotheses.
- [ ] Choose baselines and ensure task/data comparability.
- [ ] Predefine candidate-pair generation and negative sampling.
- [ ] Predefine primary metrics, coverage levels, confidence intervals, and error analysis.
- [ ] Specify report-level splits and leakage checks.
- [ ] Record model versions, random seeds, hardware, and experiment configs.

**Exit condition:** experiment can be reproduced by another researcher from the written protocol.

## Phase 4 — Minimal implementation

Only after Phase 0–3 exit conditions pass:
- [ ] Implement parsing/offset preservation and data validation.
- [ ] Implement a deterministic baseline before adding learned components.
- [ ] Add event mention and temporal edge schemas.
- [ ] Add evidence-span validation and abstention evaluation.
- [ ] Unit-test offsets, labels, taxonomy versioning, and serialization.

## Phase 5 — Evaluation and writing

- [ ] Run baseline and ablation experiments.
- [ ] Report precision/recall/F1 and evidence-span metrics.
- [ ] Report coverage-risk / precision-coverage curves and calibration.
- [ ] Conduct error analysis, confidence intervals, and sensitivity analysis.
- [ ] Document negative results and limitations.
- [ ] Draft a paper only if results and contribution merit it.
