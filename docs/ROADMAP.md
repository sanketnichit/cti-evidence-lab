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

- [x] Inspect AnnoCTR per-report text/NER/linking/TimeML formats and SMAH-CTI JSON schema.
- [ ] Check duplicate/syndicated report families and available source text.
- [x] Run a five-report AnnoCTR Intel471 convenience screen for report lengths, repeated technique-link mentions and TIMEX3 density.\n- [ ] Screen at least two additional donor sources and assess event identity/temporal evidence manually.
- [x] Confirm the five inspected AnnoCTR TimeML files contain TIMEX3 but no EVENT / MAKEINSTANCE / TLINK tags.\n- [ ] Inspect ChronoCTI Figshare v3 workbooks and exact temporal label schema.
- [ ] Verify AnnoCTR provenance workbook and per-report source terms; formally select reports only after review.

**Exit condition:** dataset supports a reproducible, non-leaky, sufficiently powered pilot.

## Phase 2 — Annotation pilot

- [x] Draft annotation protocol v0.2 and blank annotation templates.\n- [ ] Add human-authored worked examples and review the guide with a second annotator.
- [ ] Independently annotate a small sample with at least two annotators if feasible.
- [ ] Adjudicate disagreements and calculate agreement appropriate to the label structure.
- [ ] Revise or abandon categories that are not consistently annotatable.
- [ ] Estimate full-study annotation cost.

**Exit condition:** label definitions are stable enough for evaluation.

## Phase 3 — Research design

- [ ] State the exact question and hypotheses.
- [ ] Choose baselines and ensure task/data comparability.
- [ ] Predefine candidate-pair generation and negative sampling.
- [x] Draft projection metrics v0.1 and a pure-Python toy prototype.\n- [ ] Human-review metric definitions and validate additional toy cases before freezing denominators.
- [ ] Specify report-level splits and leakage checks.
- [ ] Record model versions, random seeds, hardware, and experiment configs.

**Exit condition:** experiment can be reproduced by another researcher from the written protocol.

## Phase 4 — Minimal implementation

Only after Phase 0–3 exit conditions pass:
- [x] Add a CSV annotation validator for offsets, event IDs, mapping and relation evidence.\n- [ ] Run tests in CI and validate against manually entered sample rows.
- [ ] Implement a deterministic baseline before adding learned components.
- [ ] Add event mention and temporal edge schemas.
- [ ] Add evidence-span validation and abstention evaluation.
- [ ] Confirm CI execution, then expand tests for taxonomy versioning, CSV round-trips and multi-evidence relations.

## Phase 5 — Evaluation and writing

- [ ] Run baseline and ablation experiments.
- [ ] Report precision/recall/F1 and evidence-span metrics.
- [ ] Report coverage-risk / precision-coverage curves and calibration.
- [ ] Conduct error analysis, confidence intervals, and sensitivity analysis.
- [ ] Document negative results and limitations.
- [ ] Draft a paper only if results and contribution merit it.
