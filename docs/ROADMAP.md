# Research directions

**Updated: 18 November 2026.**

The current study combines controlled representation analysis with exploratory source evidence. The [study status](PROJECT_STATE.md) separates available results from unestablished claims.

## Source-backed query evaluation

The principal extension is a set of small, auditable occurrence graphs supporting the declared temporal and connected-sequence questions. Evaluation must cover both retained and distorted answers, with unresolved cases and source coverage reported alongside query fidelity. The fixed AnnoCTR feasibility cohort and purposive external cases remain separate strata.

## Interpretation sensitivity

Outcome eligibility, occurrence grouping, incident scope, mapping alternatives and missing evidence can change the graph before projection. Separate analyses are needed to distinguish these input decisions from representational loss. The [RDP case](../research/case_studies/dfir_rdp_v0.1/README.md) provides an initial outcome/mapping comparison.

## Comparison with existing methods

Further comparison concerns occurrence identity, relation semantics, provenance and supported queries in published CTI representations. The deterministic projection is not a run of ChronoCTI's learned pipeline; Attack Flow dependencies are not substituted for observed temporal relations.

The [closest-system comparison](../research/RELATED_WORK_MATRIX.md#closest-system-comparison) records the relation and evaluation contracts. The [scaling benchmark](../research/experiments/sequence_scaling_v0.1/README.md) measures compact storage and runtime, including the effect of replacing the investigator’s full triple scan with adjacency traversal.

## Research release criteria

A research release requires a bounded contribution, explicit case selection, traceable evidence, reproducible reported results and an audit of material interpretation errors. Independent review and population estimates may only be reported when supported by actual study procedures and data. Artifact packaging and software tests do not by themselves establish scientific validity.
