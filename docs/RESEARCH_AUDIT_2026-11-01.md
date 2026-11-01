# Research Audit — 2026-11-01

## Purpose

This document records the independent audit of the seven project directions in the uploaded Gemini research report and the follow-up literature/dataset checks that led to the current candidate. It is a working research record, not a systematic review or proof of novelty.

## Overall assessment

The report contains technically interesting directions, but sophistication of terminology should not be confused with a defensible research contribution. Several proposals combine multiple hard research problems, overstate what existing datasets measure, or omit recent and directly overlapping work.

The most important lesson from the audit is to select a narrow, measurable task only after checking primary literature, actual data files, licences, annotation design, and reproducibility.

## Audit of the seven proposals

| Proposal | Assessment | Main issue / defensible narrowing |
|---|---|---|
| Mechanistic interpretability and circuit discovery in small LLMs | Legitimate research area, but claims about SAE features being monosemantic or preventing hallucinations are too strong. | Narrow to causal faithfulness of identified features in controlled tasks; distinguish correlation, intervention, and behavioural effect. |
| Continuous causal discovery with counterfactual GNNs | Combines several difficult areas; observational graph recovery is not automatically causal truth. | Define the causal estimand, intervention assumptions, and one distribution-shift setting. CausalTime is relevant but must be checked against the actual target task. |
| Symbolic execution and microarchitectural side channels | Very hardware- and toolchain-dependent. | Juliet is a software weakness/static-analysis suite, not a side-channel benchmark. A credible side-channel study needs a tightly controlled hardware threat model and suitable measurements. |
| eBPF provenance graph forensics | Strong systems direction but overlaps with prior provenance-based attack investigation, including KAIROS (IEEE S&P 2024). | Narrow to a specific source of incomplete/noisy telemetry and evaluate reconstruction under controlled event loss or ordering uncertainty. |
| Certified GNN robustness | Graph robustness and randomized smoothing have substantial prior work, including GNNCert (ICLR 2024). | Define a security-relevant graph threat model and a certification objective; general citation-network datasets alone do not demonstrate cyber relevance. |
| Neuro-symbolic CTI extraction | Promising applied area, but a generic ATT&CK mapper is not novel. MITRE TRAM, ChronoCTI, SMAH-CTI, and CSEM-CTI are relevant prior work. | Investigate a precisely defined CTI task only after comparing existing annotations and evidence/relationship outputs. Current candidate: report-local temporal event relations with relation-specific evidence and selective prediction. |
| Byzantine-robust and differentially private federated learning | Combines competing objectives and multiple threat models; ambitious for a student project. | Isolate one adversary model and one privacy/robustness objective; define utility and privacy accounting before implementation. |

## Strongest broad directions

- **AI:** causal and mechanistic questions can be meaningful, but need narrow intervention-based designs and sufficient experimental controls.
- **Cybersecurity systems:** provenance forensics has strong practical relevance, but the existing systems literature requires a carefully isolated failure mode.
- **AI + Cybersecurity:** CTI is a promising bridge, but simple extraction/mapping is already active. The candidate must be defined at the level of event relations, provenance, and evaluation rather than a generic AI wrapper.

This repository records the selected working candidate only. The complete ten-project shortlist and weighted comparison are not frozen in this working repository and should not be represented as final until the primary-source checks are complete.

## CTI research audit

### Direct and adjacent prior work

- **MITRE TRAM:** established open-source report-to-ATT&CK mapping. It prevents a generic mapper from being claimed as novel.
- **ChronoCTI:** direct CTI temporal relation and attack-graph baseline. It prevents claiming temporal CTI graph extraction itself as new. The initial audit recorded low graph recall and an unresolved Figshare access status; both details need rechecking from the paper and live data record before publication.
- **SMAH-CTI (Findings of EMNLP 2026):** recent human-annotated CTI benchmark for sentence relevance, NER, ATT&CK mapping, and grounded procedure descriptions. It narrows the extraction-stage gap.
- **CSEM-CTI (iScience 2026):** evidence mining for CTI classification and tactic/technique prediction. It narrows broad evidence/rationale claims.
- **AnnoCTR (2024):** CTI report annotations for entities, time expressions, and cybersecurity concepts. It is a candidate resource, not known temporal event-pair gold data.
- **CTI-HAL (2025):** human passage-to-ATT&CK annotations, but initial GitHub inspection did not show a licence; do not redistribute or assume reuse rights.
- **General event graphs (Glavaš & Šnajder, 2015):** event mentions as graph nodes with temporal/coreference edges. Event-instance graph representation is not novel.
- **TIMELINE (EMNLP 2023):** long-distance document-level temporal relation annotation. Cross-sentence relation extraction is not novel.
- **Structured STIX CTI graph work (2026 preprint):** report-level entities and relations with human review; relevant to graph support and validation, although not necessarily the same temporal-edge task.
- **APTIE (Scientific Data 2026):** CTI event/entity/relation dataset in Chinese; adjacent evidence that event-instance extraction in CTI is emerging, but language and label semantics may not match an English temporal task.

### Candidate study — not a novelty claim

Measure whether collapsing repeated report-local event mentions into ATT&CK technique nodes loses temporal information, then test whether relation-specific source evidence and selective abstention improve edge reliability at a stated level of coverage.

Potential research question:

> For temporal relations between ATT&CK-grounded event mentions in CTI reports, does evidence-constrained relation prediction with calibrated abstention reduce unsupported temporal edges compared with a fair text-only or ChronoCTI-style baseline at useful graph-edge coverage?

Potentially differentiating aspects to test, not assume:
1. Report-local event identity maintained separately from ATT&CK concepts.
2. Evidence spans required to support the relation between the two event instances, not merely each event independently.
3. Explicit separation of source-supported chronology from narrative order and domain priors.
4. Selective prediction evaluated with both coverage and error.
5. Measurement of whether technique-node aggregation loses information in reports with repeated technique occurrences.

### Major unresolved risks

- ChronoCTI's actual temporal workbook may already include fields that reduce the proposed gap; inspect it.
- Data access and rights are not confirmed. A repository licence does not license third-party report content.
- CTI-HAL has no licence declared in the initial repository inspection.
- AnnoCTR's corpus licence does not automatically settle every underlying third-party report right; verify its terms.
- Relation labels such as overlap and concurrency may not be consistently annotatable.
- Relation-specific evidence may be difficult to annotate reliably.
- Positive temporal edges may be rare, creating severe class imbalance.
- Candidate-pair generation can bias evaluation if annotators see only model-proposed pairs.
- A small hand-labelled pilot may support feasibility analysis but not broad performance claims.

## Data and implementation decision

Do not start an LLM pipeline, graph dashboard, or production-style app yet. First:
1. obtain and inspect the exact ChronoCTI workbook schema and access terms;
2. verify candidate corpus rights and report-source restrictions;
3. compare existing temporal labels and evidence annotations;
4. pilot the event/evidence manual with independent annotators;
5. freeze the task, baselines, split, metrics, and statistical analysis plan.

## References to verify against primary sources

- ChronoCTI: https://doi.org/10.1007/s10115-025-02491-6
- ChronoCTI code: https://github.com/rayhanur-rahman/ChronoCTI
- MITRE TRAM: https://github.com/center-for-threat-informed-defense/tram
- SMAH-CTI: https://aclanthology.org/2026.findings-emnlp.1180/
- CSEM-CTI: https://doi.org/10.1016/j.isci.2026.116466
- AnnoCTR: https://arxiv.org/abs/2404.07765
- AnnoCTR dataset: https://huggingface.co/datasets/priamai/AnnoCTR
- CTI-HAL: https://github.com/dessertlab/CTI-HAL
- Event graphs: https://doi.org/10.1017/S1351324914000060
- TIMELINE: https://aclanthology.org/2023.emnlp-main.1016/
- Structured STIX CTI graph dataset: https://arxiv.org/abs/2607.23312
- APTIE: https://doi.org/10.1038/s41597-026-07487-7

**Caution:** Links and bibliographic records are discovery pointers. Recheck versions, dates, licence, exact claims, and primary-source wording before citing in a manuscript.
