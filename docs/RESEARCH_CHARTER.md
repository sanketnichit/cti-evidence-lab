# Research Charter

## Working title

**Evidence-Constrained Temporal Cyber Threat Intelligence Reconstruction**

The title is provisional and may change after the literature and dataset audit.

## Problem context

Cyber threat intelligence (CTI) reports describe attacker actions across prose, tables, timelines, and technical appendices. Extracting ATT&CK techniques from individual sentences is not the same task as reconstructing the sequence or temporal relationships between particular action occurrences in a report.

A report may mention one technique several times, refer to an earlier event indirectly, describe background before describing an earlier incident action, or state that two actions were concurrent. A graph that connects taxonomy concepts without retaining report-local event identity can obscure these distinctions. A graph edge can also be plausible but unsupported by the report.

These are candidate failure modes to measure. Their frequency and operational significance have not yet been established for the available datasets.

## Provisional research question

For temporal relations between ATT&CK-grounded event mentions in CTI reports, does relation-specific evidence supervision and explicit abstention improve temporal-edge reliability at useful coverage compared with a fair and reproducible baseline?

## Candidate hypotheses

- **H1 — Event identity:** Collapsing multiple report-local mentions into one technique node causes measurable temporal-edge ambiguity or incorrect edge attribution in reports containing repeated technique occurrences.
- **H2 — Evidence:** Requiring a relation-specific source span reduces unsupported positive temporal edges relative to a text-only relation predictor.
- **H3 — Selective prediction:** A calibrated accept/abstain policy improves precision among accepted edges, with a measurable coverage trade-off.

No hypothesis is accepted in advance. Null or negative results are valid research outcomes.

## Scope boundaries

In scope for discovery:
- Event-mention identity and source offsets.
- ATT&CK concept grounding as metadata, not a substitute for event identity.
- Candidate temporal relation definitions.
- Report-level evidence localization.
- Selective prediction and calibration.
- Dataset provenance, licensing, annotation agreement, and leakage control.

Out of scope until separately justified:
- Production SOC deployment.
- Live threat feeds or autonomous response.
- Malware execution or exploit development.
- A general-purpose CTI chatbot.
- A large language model trained from scratch.
- A dashboard-first deliverable.
- Claims of threat prediction or incident attribution.

## Research integrity requirements

1. Every factual claim in the literature review must be tied to a primary source or clearly marked as an inference.
2. Treat repository licences, dataset licences, and third-party report rights as distinct.
3. Preserve original text offsets through normalization and segmentation.
4. Distinguish ground-truth `NO_TEMPORAL_CLAIM` from system `ABSTAIN`.
5. Evaluate relation correctness and evidence correctness separately.
6. Group related, syndicated, and duplicate reports before train/test splitting.
7. Report coverage alongside accepted-edge precision/recall.
8. Compare systems only on equivalent reports, candidate pairs, labels, and scoring rules.
9. Do not claim novelty, deployment readiness, or publication potential as facts before evidence supports them.

## Decision rule

Proceed to implementation only if the discovery phase establishes:
- lawful and sufficiently documented data access;
- a meaningful, annotatable task not already fully covered by an existing benchmark;
- feasible annotation agreement;
- reproducible baselines;
- metrics that expose both correctness and abstention trade-offs.

If any gate fails, narrow or replace the project rather than forcing the original idea.
