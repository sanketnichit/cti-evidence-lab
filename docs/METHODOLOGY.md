# Experimental Methodology (Draft)

No benchmark, annotation scheme, model, or method is frozen yet.

## 1. Unit of analysis

Candidate primary unit: a directed pair of report-local event instances, with a temporal relation label and relation-specific evidence span(s). Reports—not individual sentences or pairs—are the grouping unit for data splitting and statistical resampling.

A technique ID is a taxonomy concept, not an event instance. Repeated occurrences may require separate event nodes. This representation is not novel in general NLP; event-mention graphs and long-distance temporal relation extraction predate this project.

## 2. Candidate hypotheses

- Does technique-node aggregation obscure repeated event occurrences or lead to incorrect temporal attribution?
- Does relation-specific evidence supervision reduce unsupported positive edges?
- Can calibrated abstention improve precision among accepted edges without collapsing coverage?

## 3. Baselines to investigate

1. Deterministic temporal-cue baseline.
2. Text-only relation classifier.
3. Closest reproducible ChronoCTI-style relation baseline, if its code/data can be lawfully and technically reproduced.
4. Evidence-supervised classifier or verifier.
5. Selective prediction layer using a calibration split.

Do not compare scores across different corpora or label schemes as though they were a head-to-head evaluation.

## 4. Data design

- Use only a corpus with documented access and rights.
- Keep report families, syndicated versions, near-duplicates, and translated copies in the same split.
- Split by report (and preferably campaign/source family where possible), never randomly by sentence or candidate pair.
- Preserve original character offsets and a mapping through normalized text.
- Do not use held-out reports for prompt tuning, threshold selection, or model selection.
- Pin dataset versions and ATT&CK release.

## 5. Candidate evaluation

Relation quality:
- Per-class precision, recall, and F1.
- Macro-F1 and confusion matrix.
- Graph-edge precision/recall/F1 under a clearly specified matching rule.

Evidence quality:
- Exact or overlap-based evidence-span precision/recall/F1.
- Evidence sufficiency judged by annotators.
- Unsupported-edge rate: accepted positive edges without adequate relation support.

Selective prediction:
- Coverage and risk/precision curves.
- Precision at predeclared coverage points.
- Calibration metrics (e.g. Brier score or expected calibration error) only with a stated calibration method and enough data.
- Compare abstention against a non-abstaining baseline on the same examples.

Reliability:
- Confidence intervals using report-level bootstrap or another justified clustered method.
- Error analysis by relation type, distance between event mentions, explicit vs implicit cue, and repeated technique mention.
- Annotation agreement and adjudication statistics.

## 6. Ablations

Potential ablations, subject to task feasibility:
- With vs without relation-specific evidence supervision.
- With vs without event-instance identity.
- With vs without explicit abstention.
- Local-sentence context vs full-document context.
- Text-only evidence vs ATT&CK/domain-prior features.

## 7. Threats to validity

- Label ambiguity and disagreement, especially for inferred concurrency.
- Low frequency of positive temporal relations.
- Event mention extraction errors propagating into relation metrics.
- Report-source and campaign leakage.
- Duplicate/syndicated documents.
- Baseline incompatibility and inaccessible annotations.
- Model/context-window differences.
- Annotator expertise and limited sample size.
- Evidence span can be plausible without proving event relation.

## 8. Minimum reproducibility record

Every run should record:
- Repository commit SHA.
- Dataset name, version, licence, and access method.
- Report-level split manifest or its hash.
- ATT&CK release.
- Model name/revision and tokenizer.
- Prompt/template hash where applicable.
- Random seed and environment.
- Hardware and runtime.
- Evaluation command and raw result artifacts.
