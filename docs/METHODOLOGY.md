# Experimental Methodology — Feasibility Draft

No annotation schema, baseline, or model is frozen. The first objective is to establish whether the representation-loss question can be tested on legally usable CTI reports. This is a pilot design, not an approved full experiment.

## 1. Provisional primary study

For a report with human-annotated event instances, compare:

- **Technique-set representation:** the set of ATT&CK concepts assigned to the report, where distinct instances with the same concept collapse to one concept.
- **Technique-pair representation:** a report-level graph whose nodes are ATT&CK concepts and whose edges are typed relations between technique pairs, similar in granularity to ChronoCTI.
- **Event-instance representation:** separate report-local nodes for distinct action occurrences, with one or more textual mentions linked to each instance and evidence-supported temporal relations between instances.

The primary outcome is representational loss or ambiguity induced by projection—not model performance.

## 2. Keep annotation units separate

1. **Report:** a source CTI document or version.
2. **Event mention:** a span of text describing an action.
3. **Event instance:** one action occurrence described by the report. Multiple mentions may refer to the same occurrence.
4. **ATT&CK concept:** a taxonomy technique/sub-technique ID assigned to an event instance where evidence supports it.
5. **Temporal relation:** relation between two event instances, not merely two technique IDs.
6. **Relation evidence:** source span(s) supporting the relation between the two event instances.

Repeated mentions are not automatically repeated occurrences. Shared ATT&CK IDs do not imply coreference.

## 3. Temporal semantics

Keep these distinctions explicit:
- `BEFORE` / `AFTER`: explicit or strongly text-supported temporal precedence.
- `OVERLAP` / `SIMULTANEOUS`: only where the chosen relation scheme and evidence justify it.
- `CAUSAL_DEPENDENCY`: causal/enabling dependency, not automatically temporal ordering.
- `NARRATIVE_ORDER_ONLY`: order in the report's exposition, not confirmed execution chronology.
- `NO_TEMPORAL_CLAIM`: report does not state a temporal relation.
- `UNRESOLVED`: human annotator cannot decide from the available evidence.
- `ABSTAIN`: model decision not to predict.

MITRE Attack Flow arrows encode dependency, not the same semantics as a BEFORE relation. Attack Flow may inform action-object design but its dependency edges must not be directly relabelled as temporal gold labels.

## 4. Pilot procedure

- Inspect ChronoCTI Figshare version 3 metadata, file manifest, schemas, version and licence before depending on it.
- Inspect candidate AnnoCTR and SMAH-CTI formats and source text provenance/rights.
- Identify 5–8 candidate reports containing detailed descriptions and potential repeated technique occurrences. This small sample checks feasibility only; do not use it to estimate corpus-wide prevalence.
- Annotate event mentions, event-instance identity, ATT&CK concepts, temporal relations and relation-specific evidence.
- Double-annotate an overlapping subset with a second human annotator where possible; adjudicate disagreements.
- Record annotation time, ambiguous/unresolved cases, repeated-instance counts, relation-label distribution and agreement.
- Revise the guide before any larger annotation effort.

Only human-created and adjudicated labels may serve as evaluation ground truth. Any candidate passage or mapping suggestion must be checked against the original report before annotation.

## 5. Candidate representation-loss outcomes

These remain candidate metrics and require formal definitions before use:

- **Repeated-instance prevalence:** number/fraction of reports with at least two distinct event instances mapped to one ATT&CK concept.
- **Instance-collision count:** number of distinct event nodes merged by a within-report ATT&CK projection.
- **Same-technique relation loss:** event-pair temporal relations whose endpoints map to the same technique and therefore cannot be represented as an ordinary edge between distinct technique nodes.
- **Relation conflation:** distinct event-pair relations that collapse to one technique pair, obscuring which event occurrences they connect.
- **Ordering distortion:** whether projected strict-BEFORE relations induce cycles or contradictions at the technique level.

Do not mix strict temporal order with overlap, concurrency or causal dependency when testing DAG properties. Node counts from graphs with different node universes cannot be compared directly without a clearly defined mapping, denominator and interpretation.

## 6. Baselines to investigate after pilot

1. **Technique-set aggregation:** deduplicate event instances by ATT&CK concept within a report.
2. **Technique-pair projection:** derive the report-level technique-pair representation from the same human event-instance annotations.
3. **ChronoCTI:** reproduce or re-evaluate the published technique-pair system only if Figshare assets, schema, dependencies and rights permit a fair comparison.
4. **Temporal cue baseline:** only if the secondary relation-extraction task is included.
5. **Event-pair learned/evidence-linked model:** defer until enough reliable human-labelled examples exist.

Do not compare scores across incompatible corpora or relation schemas as if they were a controlled head-to-head evaluation.

## 7. Data integrity and leakage

- Split at report level, not sentence/event-pair level.
- Group syndicated, duplicated, translated and near-duplicate reports before splitting.
- Do not use held-out reports for prompt tuning, threshold selection or model selection.
- Preserve source document version, dataset version and ATT&CK release.
- Keep raw source files outside Git unless redistribution permission is confirmed.

## 8. Statistical analysis (only after sample design)

- Report report-level counts and distributions, not only pooled event-pair counts.
- Use report-clustered bootstrap intervals or another justified clustered method.
- Report per-class support and uncertainty for rare relations.
- Avoid pair-level independent significance tests where many pairs come from one report.
- Predefine primary outcomes before looking at test results.

## 9. Threats to validity

- Distinguishing repeated event occurrences from repeated descriptions.
- Event mention and coreference annotation error.
- Temporal underspecification and narrative-order bias.
- Overlap/concurrency/causality relation-schema mismatch.
- Sparse positives and class imbalance.
- Report-source and campaign leakage.
- Candidate-pair generation bias.
- Annotator expertise, sample size and agreement.
- Domain and time-period shift.
- Baseline incompatibility and incomplete artifacts.
- Source-text copyright and redistribution restrictions.

## 10. Reproducibility record

Each run must record repository commit, data version and licence, report split, ATT&CK release, model/tokenizer revision, prompt hash if applicable, random seed, environment, hardware, evaluation command and raw result artifacts.
