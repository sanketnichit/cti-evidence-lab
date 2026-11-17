# Research roadmap

**Updated: 17 November 2026**

The research question is whether a graph whose nodes are ATT&CK techniques and edges connect only distinct technique IDs can retain source-supported temporal relations between separate occurrences of the same technique. We are investigating this on report text, not claiming that event extraction or ATT&CK graph construction is new.

The detailed status of each workstream is in [the completion matrix](../research/PROJECT_COMPLETION_MATRIX_v0.1.md). This roadmap is deliberately short so that the next piece of work is easy to identify.

**Delivered 17 November:** [Exploratory feasibility report](../research/FEASIBILITY_REPORT_v0.1.md), [verified source review](../research/feasibility/exploratory_review_v0.1/README.md), seven [representation controls](../research/experiments/representation_controls_v0.1/README.md), and two independent [review packets](../research/reviewer_kit/COORDINATOR.md). The next input is completed first-pass forms from reviewers. Preserve those before comparing answers; do not treat this exploratory pass as completed human annotation.

## 1. Research and data foundations — mostly prepared

- [x] Define the descriptive event-instance versus technique-pair comparison question.
- [x] Inventory AnnoCTR: 400 reports and the 120-report train/dev/test sampling frame.
- [x] Fix five deterministic rank-one feasibility candidates, one per donor.
- [x] Check source provenance and document the corpus-level reuse clarification.
- [x] Review the five rank-one reports at the preliminary source-first level.
- [ ] Finish the literature/schema comparison and document what existing methods already establish.
- [ ] Record actual source-scope eligibility and exact-source verification for each candidate.

## 2. First source-grounded pilot — NEXT

- [ ] Settle the smallest sufficient version of the event, incident-scope, mapping and temporal-evidence rules; preserve the reconstruction status until explicitly accepted.
- [ ] Carry out the full-source human pass on all fixed rank-one candidates, regardless of event yield.
- [ ] Record accepted, rejected, unsupported and unresolved events and relations with exact source evidence.
- [ ] Validate and lock any genuine single-annotator final partitions. Never use a hash as a substitute for review.
- [ ] Record missingness, source hours and ambiguous cases, including reports without identifiable attack-event pairs.
- [ ] Obtain a second independently completed human pass for an overlapping subset if feasible; otherwise state that agreement is not measured.

The earlier five source-review drafts are not completed pilot annotation. See [the feasibility synthesis](../research/feasibility/FIVE_REPORT_FEASIBILITY_SYNTHESIS_v0.1.md). A previously discussed DFIR case is a [separate conditional exercise](../research/exploratory/DFIR_Repeated_RDP_Source_Contrast_v0.1.md), not part of the sample.

## 3. Reproducible comparison

- [x] Implement and synthetic-test A_120 mapping, four projection states, collision provenance and strict-order cycle diagnostics.
- [x] Separate report opportunity denominators, direct temporal relations and within-technique relation outcomes.
- [ ] Run the existing toolchain on validated, source-backed human annotations.
- [ ] Compare primary distinct-pair projection with declared sensitivity representations (including same-technique loops and accepted exact sub-technique mappings where supported).
- [ ] Keep ChronoCTI's published predictions distinct from our own deterministic projection. Cross-corpus scores are not directly comparable.

## 4. Decision after pilot

- [ ] If evidence supports the event-instance task, design a separately justified larger study and a report-level leakage-safe split. Fix sample size, source selection and statistical plan **before** evaluating desired outcomes.
- [ ] If the reports cannot support stable event identity or reliable temporal labels, report that limitation and narrow the scientific question. Do not manufacture positives or quietly replace the original sample.
- [ ] Keep prevalence, confidence intervals, model performance and novelty claims off the table until they can be measured and checked.

## 5. Final research write-up

- [ ] Freeze a versioned protocol, code and source-access record, then rerun CI and integrity checks.
- [ ] Prepare results tables from reproducible scripts, with unresolved cases, uncertainty and negative findings.
- [ ] Explain mapping-level assumptions and limitations, discuss competing literature and possible dataset bias.
- [ ] Write a clear report/paper and presentation that accurately distinguish preparation, illustrative examples and measured research results.

**Current boundary:** Software and synthetic fixtures are developed. Human-locked AnnoCTR annotations, IAA and real-report projection results do not yet exist. The project is not complete until it produces verifiable source-backed evidence or a defensible negative feasibility conclusion.
