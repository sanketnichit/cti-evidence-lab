# Dataset Feasibility and Task-Gap Audit

**Status:** discovery evidence, not a final dataset selection.  
**Last checked:** 2026-11-01. Recheck paper versions, data files, and licences before any release.

## 1. Why dataset design is central

The candidate task is not simply “extract ATT&CK techniques” or “build a temporal attack graph.” Those tasks already have direct prior work. The potential distinction is the unit of representation:

- An **ATT&CK technique** is a reusable taxonomy concept.
- An **event mention** is a specific text span describing an action.
- An **event instance** is one actual occurrence in the incident being described. Several mentions may refer to one occurrence; one technique may describe multiple distinct occurrences.
- A **temporal relation** belongs between event instances, not automatically between taxonomy concepts.

A system that merges every occurrence of a technique within a report into a single node may lose which occurrence happened first, which occurrence overlapped with another action, or which action a particular temporal statement refers to. Whether this happens often enough to matter is the empirical question.

## 2. Candidate corpora

### ChronoCTI — direct temporal baseline

Paper: https://doi.org/10.1007/s10115-025-02491-6  
Code: https://github.com/rayhanur-rahman/ChronoCTI  
Data DOI: https://doi.org/10.6084/m9.figshare.26039518.v3

What the paper establishes:
- It manually constructs temporal ground truth for 94 CTI reports.
- The task is defined over pairs of ATT&CK techniques in a report.
- The paper describes a graph where techniques are nodes and temporal relations between technique pairs are edges.
- The report-level split is 73 training reports and 21 evaluation reports.
- Temporal labels include BEFORE, SIMULTANEOUS-OVERLAP, CONCURRENT, and NULL (the implementation uses label names such as NEXT for the forward-order class).
- The paper reports macro precision/recall/F1 of 0.75/0.46/0.54 for the relation classifier and MUC-5 graph P/R/F1 of 0.58/0.25/0.34.
- The authors describe severe class imbalance and low recall for minority temporal relations.

The paper's current Data Availability section points to a public Figshare DOI (version 3). An earlier internal note in this project described the item as private; that note is superseded by the paper's explicit data-availability record. We still need to inspect the actual Figshare files, version metadata, and per-file licences before reusing any artifact.

**Implication:** ChronoCTI is a direct baseline and a useful comparison point, but its task is report-level technique-pair relation classification. It does not, as defined in the paper, distinguish multiple occurrences of the same technique as separate graph nodes.

### AnnoCTR — candidate full-document English CTI corpus

Paper: https://aclanthology.org/2024.lrec-main.103/  
Repository: https://github.com/boschresearch/anno-ctr-lrec-coling-2024  
Dataset: https://huggingface.co/datasets/priamai/AnnoCTR

The project README describes 400 English CTI reports from commercial intelligence vendors, with named entities, temporal expressions, and ATT&CK-related concept annotations. It provides report text, TimeML temporal annotations, and document-level splits. The corpus is declared CC BY-SA 4.0 in the dataset README and paper.

Potential value:
- Full report context makes cross-sentence analysis possible.
- Existing temporal-expression and ATT&CK annotations can help seed a pilot.
- It offers substantially more report documents than ChronoCTI's relation-labelled subset.

Limitations:
- The corpus was annotated by a domain expert; this is not a substitute for independent agreement on our new event-relation labels.
- It does not provide the event-instance-to-event-instance temporal relations required by the candidate task.
- ATT&CK concept annotations are not necessarily exact event-trigger spans.
- Underlying source-report terms and the corpus licence must be reviewed before redistribution or publication of derived text.

### SMAH-CTI — recent sentence-level action evidence

Paper: https://aclanthology.org/2026.findings-emnlp.1180/  
Project page: https://seal.cs.ucf.edu/projects/smah-cti.html  
Repository: https://github.com/davidmohaisen/SMAH-CTI

The public release documents 100 CTI reports, 12,304 sentence instances, 15,487 exact NER spans, including 6,546 Action spans, ATT&CK tactic/technique assignments, and grounded procedure descriptions. It publishes fixed report-level train/dev/test splits (70/10/20 reports). NER spans use zero-based, end-exclusive offsets into each sentence. Dataset files are licensed CC BY-NC 4.0; code is MIT.

Potential value:
- High-quality action spans and ATT&CK mappings could support event-mention seeding.
- Explicit data schema, provenance, split manifests, and validation checks are available.
- Exact offsets make it useful for evidence-span experiments.

Limitations:
- Its annotation unit is a sentence with a preceding-sentence context field, not a full document-level event graph.
- It has no event-to-event temporal relation labels.
- Its CC BY-NC data licence is distinct from its MIT code licence; do not copy the dataset into this MIT project repository or assume commercial reuse.

### APTIE — Chinese CTI multi-task extraction

Paper: https://doi.org/10.1038/s41597-026-07487-7  
Dataset DOI: https://doi.org/10.5281/zenodo.17129303

The 2026 Scientific Data paper describes 116 Chinese CTI reports, 808 sentences, 2,574 entities, 1,506 entity relations, and 139 event instances. It includes separate entity, relation, and event-extraction modules aligned with STIX 2.1.

Potential value:
- Shows active work on event extraction and richer structured CTI annotations.
- Useful as an adjacent multilingual precedent.

Limitations:
- Chinese language and dataset construction differ from the proposed English CTI setting.
- The relation module is described as relations between entities; it should not be treated as a labelled event-to-event temporal relation dataset without schema-level confirmation.

### CASIE and CySecED — event extraction precedents

- CASIE: https://doi.org/10.1609/aaai.v34i05.6401. English cybersecurity event extraction corpus with event types, triggers, and arguments; the 2026 survey describes it as lacking explicit event-relation labels.
- CySecED: the 2026 survey describes an English cybersecurity event-detection corpus with 30 event classes, but not full event-relation annotation.

These can inform event schemas and baseline methods, but they are not direct CTI document-level temporal relation datasets.

## 3. What the recent survey says—and what it does not say

A 2026 survey in IET Communications reports that cybersecurity event-relation extraction is relatively underdeveloped and that it found no unified, publicly available, widely adopted benchmark for event-relation extraction. It notes that existing studies often use privately constructed datasets with differing corpora, relation schemas, and annotation standards.

This statement must be interpreted carefully:
- ChronoCTI has a publicly referenced temporal relation dataset, but its labels are at the report/technique-pair level.
- The survey's event-relation framing concerns relations between event instances, which is a different annotation unit.
- APTIE has entity relations and event extraction modules, but that does not by itself establish event-to-event temporal relation labels.

The apparent difference is not a contradiction once the task and unit of annotation are distinguished. We must verify the survey's exact definition and coverage before citing it as a definitive gap.

Survey DOI: https://doi.org/10.1049/cmu2.70187

## 4. Recommended feasibility sequence

Do not commit to a 400-report annotation exercise yet.

### Pilot A — schema and data audit
1. Download ChronoCTI Figshare version 3 and inspect every file, its metadata, and licence.
2. Inspect the actual workbook columns and report IDs; do not infer a schema from code names alone.
3. Inspect AnnoCTR's linking/time/text formats and SMAH-CTI's action-span schema.
4. Select 5–8 reports with repeated technique mentions, explicit event descriptions, and sufficient temporal content.
5. Check duplicate and syndicated report families.

### Pilot B — annotation feasibility
For each selected report, annotate:
- report-local event mentions with exact source offsets;
- event-instance identity, including whether separate mentions refer to the same occurrence;
- ATT&CK concept link, when supported;
- event-instance pair and temporal relation;
- relation-specific supporting span(s);
- uncertainty / unresolved case.

Use a second independent annotator for an overlapping subset and adjudicate disagreements. If no qualified second annotator is available, label the pilot exploratory and do not claim a gold-standard benchmark.

### Expansion gate
Expand beyond the pilot only if:
- event-instance boundaries are consistently annotatable;
- enough reports contain repeated occurrences to test the representation question;
- positive temporal relations are sufficiently frequent for meaningful evaluation;
- the rights and source provenance support the intended research use;
- the annotation cost is manageable.

## 5. Candidate research question

> How much does representing a CTI report as ATT&CK technique nodes, rather than distinct report-local event instances, distort the temporal structure of the described incident?

A secondary systems question may test whether evidence-linked event-instance extraction can reconstruct those relations reliably. This should remain secondary until the annotation pilot is feasible.

## 6. Stop / pivot criteria

Pivot the project if:
- the selected corpus does not contain repeated instances often enough;
- existing labels already capture event-instance identity at the needed granularity;
- temporal relations cannot be annotated with acceptable agreement;
- data rights do not permit the intended analysis or release;
- the sample size is too small to support the planned comparisons.

A negative feasibility result is better than manufacturing a novelty claim.
