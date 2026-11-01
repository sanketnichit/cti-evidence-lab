# Experimental Methodology (Draft)

No annotation schema, baseline, or model is frozen yet. The project begins with a feasibility pilot, not full-scale model training.

## 1. Primary study design

Compare two representations of the same manually annotated CTI report:
- technique-level representation, where event occurrences sharing an ATT&CK concept are aggregated within a report;
- event-instance representation, where each distinct action occurrence remains a separate node and multiple text mentions may corefer to it.

The first outcome is a measurement of representation loss. A model comparison is secondary and only proceeds if the pilot is feasible.

## 2. Annotation units

1. Report and report version.
2. Event mention (text span with offsets).
3. Event instance (underlying occurrence; one or more mentions may refer to it).
4. ATT&CK concept link.
5. Event-instance pair with temporal relation and relation-specific evidence.

Do not confuse repeated mentions, repeated occurrences, or repeated technique IDs.

## 3. Pilot

- Inspect ChronoCTI's Figshare version 3 files and metadata.
- Inspect candidate AnnoCTR and SMAH-CTI schemas and data rights.
- Select 5–8 candidate reports with multiple action descriptions and repeated technique mentions.
- Independently annotate event mentions, event-instance identity, ATT&CK links, temporal relations, and relation evidence.
- Double-annotate an overlapping subset with a second annotator if available; adjudicate disagreements.
- Record annotation time, unresolved cases, relation distribution, and inter-annotator agreement.

Do not scale until the pilot establishes that the target phenomena occur often enough and can be annotated consistently.

## 4. Baselines to investigate

1. **Technique aggregation baseline:** collapse event instances by ATT&CK ID within a report and derive the technique-pair graph.
2. **Temporal cue baseline:** deterministic temporal markers and local syntactic patterns.
3. **ChronoCTI baseline:** reproduce the published technique-pair system if data, dependencies, and model artifacts are accessible and licensed.
4. **Text-only event-pair model:** classify candidate event-instance pairs from report context.
5. **Evidence-linked variant:** same candidate pairs with relation-specific evidence supervision or evidence verification.

Do not compare results across incompatible corpora or relation schemas as though they were head-to-head results.

## 5. Primary outcomes

Representation:
- number of distinct event instances and event mentions per technique per report;
- fraction of reports containing repeated distinct occurrences of a technique;
- temporal edges that become ambiguous, merged, or lost after technique-level aggregation;
- edge and ordering agreement between event-instance ground truth and aggregated graph.

Relation quality (if model evaluation is feasible):
- per-class precision, recall, F1 and macro-F1;
- edge-level precision/recall/F1 with an explicit matching rule;
- report-level graph fidelity and contradiction analysis.

Evidence quality:
- relation evidence span exact/overlap precision, recall, and F1;
- unsupported positive-edge rate;
- human judgement of whether the evidence supports the relation between both event instances.

Selective prediction is optional secondary analysis:
- coverage-risk or precision-coverage curves;
- precision at predeclared coverage points;
- report coverage alongside errors, so abstention cannot hide poor recall.

## 6. Data splitting and leakage control

- Split by report, not by sentence or event pair.
- Group syndicated, duplicated, translated, and near-duplicate reports before splitting.
- Do not use held-out reports for prompt tuning, threshold selection, or model selection.
- Preserve source document version, dataset version, and ATT&CK release.
- If using an existing report-level test partition, do not silently alter it.

## 7. Statistical analysis

- Use report-level bootstrap or another justified clustered confidence interval method.
- Report class support and uncertainty, especially for rare relations.
- Avoid significance claims from pair-level independent tests when many pairs come from the same report.
- Predefine primary metrics before looking at test results.

## 8. Threats to validity

- Event mention detection and event coreference errors.
- Ambiguous distinction between separate occurrences and repeated descriptions.
- Relation schema disagreement, especially overlap vs concurrency.
- Class imbalance and sparse positive temporal relations.
- Report-source and campaign leakage.
- Candidate-pair generation bias.
- Limited annotator expertise and pilot size.
- Domain shift across vendors, years, and report styles.
- Baseline incompatibility or irreproducible dependencies.
- Source-text redistribution restrictions.

## 9. Reproducibility record

Every run must record repository commit, dataset version and licence, report split, ATT&CK release, model/tokenizer revision, prompt hash if applicable, random seed, environment, hardware, evaluation command, and raw result artifacts.
