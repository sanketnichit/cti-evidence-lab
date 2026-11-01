# Related-Work Matrix

“Potential gap” is an interpretation to test, not proof of novelty.

| Work / resource | Year / status | Task / representation | Overlap | Limitation for this project | Assessment |
|---|---|---|---|---|---|
| Glavaš & Šnajder, event graphs: https://doi.org/10.1017/S1351324914000060 | 2015 journal | Event-mention nodes with temporal/coreference edges | Establishes event graphs | Not CTI-specific or ATT&CK-grounded | Event graph representation is not novel |
| TIMELINE: https://aclanthology.org/2023.emnlp-main.1016/ | EMNLP 2023 | Long-distance document-level temporal relation annotation | Full-document temporal relations | Not CTI data | Annotation precedent |
| ChronoCTI: https://doi.org/10.1007/s10115-025-02491-6 | 2025 peer-reviewed | Sentence-to-ATT&CK mapping, temporal technique-pair relations, temporal attack graphs | Direct CTI temporal graph baseline | Exact workbook schema and data access/licence need inspection | Primary CTI baseline |
| CSEM-CTI: https://doi.org/10.1016/j.isci.2026.116466 | iScience 2026 | Contrastive evidence mining for CTI classification and tactic/technique prediction | Evidence-aware CTI analysis | Not currently known to provide report-level temporal pair labels | Strong adjacent competitor |
| SMAH-CTI: https://aclanthology.org/2026.findings-emnlp.1180/ | Findings of EMNLP 2026 | Sentence relevance, NER, ATT&CK mapping, grounded procedure descriptions | Recent human-annotated CTI benchmark | No temporal-edge gold labels as currently understood | Extraction-stage benchmark |
| AnnoCTR: https://arxiv.org/abs/2404.07765 | LREC-COLING 2024 | CTI entity, time-expression, cybersecurity-concept annotations | Report-level CTI corpus | No event-pair temporal labels known | Candidate corpus, subject to rights audit |
| CTI-HAL: https://github.com/dessertlab/CTI-HAL | 2025 workshop | Human passage-to-ATT&CK annotations | Evidence localization | No temporal edges; no licence declared in initial repo inspection | Do not reuse without permission |
| AttacKG: https://github.com/li-zhenyuan/Knowledge-enhanced-Attack-Graph | 2022 | CTI report attack graph construction | Attack graphs from CTI | Not necessarily temporal-edge evidence attribution | Graph construction is not novel |
| MITRE TRAM: https://github.com/center-for-threat-informed-defense/tram | Open source | Report-to-ATT&CK mapping | Practical mapping baseline | Not the same temporal edge task | Established tool |
| Structured STIX CTI dataset: https://arxiv.org/abs/2607.23312 | 2026 preprint | Report-level STIX 2.1 graphs | CTI entities/relations and human review | Temporal-edge labels and licence need checking | Important adjacent work |
| APTIE: https://doi.org/10.1038/s41597-026-07487-7 | Scientific Data 2026 | Chinese CTI entity/relation/event extraction | Event-instance and relation annotations | Language/task mismatch to English temporal CTI | Adjacent work |
| Open LLM ATT&CK mapping evaluation: https://arxiv.org/abs/2606.18166 | 2026 preprint | Sentence-level technique classification | Mapping difficulty and baselines | Not event-pair temporal relation extraction | Baseline context |
| Digital Precognition: https://doi.org/10.1109/ICAIC67076.2026.11395807 | IEEE ICAIC 2026 | Retrieval plus cross-encoder ATT&CK mapping | Efficient technique retrieval | Not temporal relation extraction | Related mapping work |
| Büchel et al., USENIX Security SoK: https://www.usenix.org/conference/usenixsecurity25/presentation/buechel | 2025 peer-reviewed SoK | Systematizes automated TTP extraction across 40+ papers and evaluates methods in a common setting | Highlights task/ontology/dataset comparability and TTP extraction limits | Does not supply the event-instance temporal relation labels required here | Important framing and reproducibility work; not a direct temporal-edge benchmark |
| AttackSeqBench: https://arxiv.org/abs/2503.03170 | 2025 arXiv preprint | Builds ordered TTP sequences from 408 CTI reports and evaluates LLM sequence understanding through generated Q&A tasks | Directly overlaps attack-sequence reasoning from CTI reports | Sequences are produced by an LLM-based KG pipeline; it is not a human gold dataset of event-instance coreference and pairwise temporal relations | Close adjacent benchmark; distinguish sequence QA from relation annotation |
| Hou et al., reachable attack chains: https://arxiv.org/abs/2607.19742 | 2026 arXiv preprint | Extracts attack units as preconditions, behavior and postconditions; uses Datalog for dependency and reachability reasoning; 20 reports and 334 human-validated steps | CTI attack-chain reconstruction and dependencies among steps | Focuses on executable state transitions and reachability, not a benchmark of same-technique event-instance temporal relations | Close adjacent work; compare dependency semantics carefully |
| MATRES / Ning et al.: https://aclanthology.org/P18-1122/ | ACL 2018 | Multi-axis temporal annotation for main-axis verb events using start-point relations | Provides a clearer relation scheme and IAA precedent | General-domain news events; main-axis verb restriction may omit CTI actions and does not directly solve event identity in CTI | Useful annotation-design precedent, not a drop-in CTI schema |


## Candidate empirical opportunity

A potential study is to measure whether collapsing repeated report-local event mentions into technique-level nodes loses temporal information, then test relation-specific source evidence and selective abstention.

This is a CTI-specific empirical hypothesis, not a proven gap or novel representation. Before proceeding:

1. Obtain lawful access to ChronoCTI temporal labels and inspect their exact schema.
2. Check whether existing data already encode event identity and edge evidence.
3. Compare against temporal event-graph and long-distance relation work outside cybersecurity.
4. Inspect CSEM-CTI and structured STIX graph methods in full.
5. Pilot the annotation design and evaluate inter-annotator agreement.

## Fair comparison rule

Do not compare scores from different corpora, pair-generation methods, label schemes, or scoring definitions as if they were a head-to-head benchmark.


## Addendum — source checks completed 1 November 2026

The rows above are an initial map. The following checks materially change the framing and should be read together with them.

### ChronoCTI: code-level representation check

- The paper describes temporal relations over ATT&CK technique pairs within CTI reports. It points to a Figshare v3 release: https://doi.org/10.6084/m9.figshare.26039518.v3.
- In the public code file `temporal-learner-code/learn_graph_ML_imbalanced_multilabel-v2.py`, graph node names are constructed as `technique@report`. This is one node per technique per report in that graph construction, rather than one node per distinct report-local execution instance.
- The public pair construction uses `idx1 != idx2`, so same-technique pairs are excluded from that candidate pair list. This gives a concrete reason to test whether temporal relations between two separate occurrences of the same technique are omitted by that abstraction.
- This is a code-specific observation. It does not establish what every uninspected intermediate artifact may contain. The paper links Figshare v3, but the full manifest, exact schemas, versioned files and item licence have not yet been inspected in this audit. An earlier audit attempt recorded restricted/private access; current access status remains unresolved.

### CASIE: cybersecurity event extraction is established prior work

Satyapanich et al. (AAAI 2020) annotate 1,000 English cybersecurity news articles with event nuggets, arguments, semantic roles and realis values across five event subtypes. Importantly, the paper says its reported study concentrates on the first four pipeline steps and leaves event coreference and full knowledge-graph integration for future work. The public repository README mentions a later `link_coref.py` helper; inspect that exact code and its data before characterizing its functionality. The README alone is not evidence of a document-level gold coreference or temporal-link benchmark.

Paper: https://doi.org/10.1609/aaai.v34i05.6401  
Repository: https://github.com/Ebiquity/CASIE

**Implication:** do not claim novel cybersecurity event extraction. The candidate needs to isolate occurrence identity under ATT&CK normalization and, especially, the fate of explicit event-to-event temporal relations. A corpus licence for reuse was not confirmed in this check.

### CSEM-CTI: evidence-based technique classification is also prior art

Peng et al., *LLM-guided contrastive evidence mining for explainable cyber threat intelligence classification*, iScience 29(7), 116466 (published 25 June 2026), introduces CSEM-CTI. It mines evidence tokens for sentence-level ATT&CK technique classification and evaluates faithfulness with ERASER. It uses SeqMask (15,300 labelled procedure descriptions), LLM-TIKG (38,946 instances) and CTIBench's CTI-ATE task (approximately 600 real reports). The paper says all corpora are sentence-level and that ERASER results are computed on SeqMask only; faithfulness is therefore corpus-specific. The method does **not** provide event-instance identity or event-to-event temporal-link supervision.

Paper: https://doi.org/10.1016/j.isci.2026.116466  
Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC13320542/

**Implication:** generic “evidence-grounded CTI classification” or “faithful technique evidence” is not a defensible novelty claim. Our evidence requirement must be relation-specific: evidence must support the temporal relation between two specific event instances, not only a technique label. The article states that code is publicly deposited, but its key-resources table did not identify a repository URL in the material checked; repository identity still needs verification before reuse.

### 2026 STIX 2.1 CTI graph dataset preprint: occurrence-like attack-pattern objects exist

Das et al., arXiv:2607.23312 (submitted 25 July 2026), describe 150 English CTI reports represented as per-report STIX-style graphs, with 4,777 entities, 5,817 relationships and 1,273 attack-pattern objects manually mapped to 269 unique ATT&CK identifiers. Each report has node and edge CSV files; attack-pattern objects have report-local IDs, descriptions and ATT&CK mappings. This representation may already preserve multiple behavior objects associated with a technique, so the project must not assume that technique identity is the only available granularity in all CTI graph work.

The paper explicitly states that it does not model temporal attack sequences and lists temporal relationships as future work. It also says the complete dataset, code and other materials will be made public upon acceptance; no public release was located in this check. Human review covers a random sample of 25 reports, with reported weighted kappa values of 0.64 for entity type, 0.67 for ATT&CK mapping and 0.62 for relationship correctness.

Preprint: https://arxiv.org/abs/2607.23312

**Implication:** this is a particularly close adjacent work. Revisit it if a release appears. Our question should centre on explicit occurrence-to-occurrence temporal relations and their projection/omission, not merely on representing individual attack-pattern objects.

### AnnoCTR: strongest current human-annotation pilot candidate, with caveats

The official paper and repository show 400 English cyber threat reports; 120 receive the cybersecurity-specific annotation layer. The repository contains full report text, cybersecurity linking, general entity annotations and TimeML files for temporal expressions. These TimeML annotations are not event-event TLINKs or event-coreference chains. The paper says report donors permitted republication under CC BY-SA 4.0, and the repository labels the corpus CC BY-SA 4.0. This is separate from the licence shown for the conference paper PDF itself.

Paper: https://aclanthology.org/2024.lrec-main.103/  
Repository: https://github.com/boschresearch/anno-ctr-lrec-coling-2024

The cyber-specific labels on the 120-report subset were produced by one domain expert. The paper reports a limited second-annotator comparison with average document-level technique-set F1 around 0.54. The exact data tree, per-report provenance and raw-text/annotation alignment have not yet been inspected file by file; do that before selecting reports or redistributing anything.

**Implication:** likely the best starting point for a small human pilot because it includes report context and technique spans, but not ready-made temporal or event-identity gold data.

### SMAH-CTI and APTIE: exact schema boundaries

- SMAH-CTI's public JSON schema contains report ID, page/sentence IDs, sentence text, preceding-sentence context, sentence-level Action spans and ATT&CK tactic/technique labels. It contains no event-coreference chains or event-event temporal links. The dataset licence is CC BY-NC 4.0; code is MIT. Underlying source terms still need checking.
  - https://github.com/davidmohaisen/SMAH-CTI
  - https://aclanthology.org/2026.findings-emnlp.1180/
- APTIE is a 2026 Chinese CTI resource with sentence-scoped event and entity-relation annotations. Its paper says cross-sentence aggregation and document-level reasoning are excluded; semantic entity relations such as exploits/targets are not event-event temporal relations.
  - https://doi.org/10.1038/s41597-026-07487-7
  - https://doi.org/10.5281/zenodo.17129303

### Revised gap wording

The reviewed resources establish CTI event extraction (CASIE and others), CTI technique-pair temporal prediction (ChronoCTI), sentence-level ATT&CK evidence mining (CSEM-CTI), and report-level STIX graphs with attack-pattern objects (the 2026 preprint). General-domain event coreference and temporal relation annotation are also established (MAVEN-ERE).

A bounded, testable question remains: **in real CTI reports, how often do two distinct event instances map to the same ATT&CK technique, and how much explicitly supported event-to-event temporal information becomes unrepresentable, lost or conflated when the report is projected to a unique-technique-per-report or technique-pair graph?**

This remains a hypothesis, not a proven research gap. The STIX preprint is a direct competitor for the occurrence-object part of the representation and must be revisited when its dataset is released. A pilot must establish the phenomenon's prevalence before any larger study or model work.


### File-level AnnoCTR screening: one candidate report (not an annotation result)

A first per-document example was opened from the official repository:
- Raw report: `AnnoCTR/all/text/intel471_2020-03-26_analysis-of-an-attempted-attack.txt`
- Token labels: corresponding `AnnoCTR/all/ner_bio/*.bio` and `ner_json/*.json`
- MITRE-linked concepts: corresponding `AnnoCTR/all/linking_mitre_only/*.json`
- Temporal expressions: corresponding `AnnoCTR/all/time/*.tml`

Observed for this single report: 15,211 characters of text; 32 ATT&CK technique-link records across five unique techniques; 24 mention/link records map to T1059; 31 TIMEX3 elements; zero TimeML EVENT, MAKEINSTANCE or TLINK elements. This confirms that the resource can supply full report context plus technique-linked mention candidates, while its TimeML layer does not supply event-event temporal gold links.

**Do not count the 24 mentions as 24 executions.** A repeated linked mention can refer to the same attack occurrence, a different occurrence, an artefact/description, or a general explanatory statement. A human annotator must resolve this from context. This report is a useful candidate for the 5–8 report pilot, but it is not yet selected as a pilot item and is not evidence of repeated-instance prevalence.


### AnnoCTR corpus counts and licence distinction checked against the paper PDF

The AnnoCTR paper's Table 2 reports the 120 cybersecurity-plus-general-layer reports split across five donors: Intel471 30, Lab52 23, Proofpoint 28, QuoIntelligence 12 and ZScaler 27. These five-vendor counts matter for transparent pilot sampling. The paper describes 400 reports with the general layer and 120 with cybersecurity-specific annotations. The Table 1 corpus entry reports 120 documents, 12,179 sentences and 13,244 annotations for the full multi-layer/cybersecurity subset. The paper's Table 3 also reports 3,375 technique mention annotations across that subset (1,098 explicit and 2,292 implicit; sum 3,390, so verify the table's apparent arithmetic discrepancy against the original PDF before quoting a combined total).

**Licence distinction:** the paper proceedings PDF carries a CC BY-NC 4.0 copyright line, while the authors explicitly state that the underlying CTI vendor reports were donated by copyright holders and permitted for republication under CC BY-SA 4.0. The repository likewise labels the corpus folder CC BY-SA 4.0. Do not confuse the paper-PDF licence with the corpus licence; retain attribution and verify any per-report terms/provenance for the actual use. The report text itself is not to be copied into this project repository.

**Annotation reliability caveat:** the general layer (TIMEX, ORG, LOC, SECTOR, CodeSnippet) was annotated by two trained annotators. The cybersecurity-specific layer was created by one specialist annotator. A second professional's document-level technique-set comparison produced average F1 about 0.54, but the paper explicitly says this was not a proper agreement study due to limited training/time. This makes independent human annotation and careful adjudication essential for our new event-instance layer.

Primary source: Lange et al., LREC-COLING 2024, pp. 1147–1160: https://aclanthology.org/2024.lrec-main.103.pdf


### ChronoCTI: same-technique event-pair exclusion is explicit in the paper

Section 4.5.2 defines the possible pair universe over 120 techniques as ((120^2-120)/2), excluding ((T,T)) diagonal pairs. The public code's pair construction confirms `idx1 != idx2`. Thus, an explicitly temporal relation between two distinct event instances carrying the same technique ID cannot be represented in this candidate-pair universe. This is a specific, inspectable limitation we can empirically evaluate; it is not proof that the limitation is common enough to be important.

Paper: https://doi.org/10.1007/s10115-025-02491-6


## Addendum — ChronoCTI agreement materials and cycle-audit prerequisite (1 November 2026)

The ChronoCTI repository includes `temporal-learner-code/IRR_data/` with the final temporal relation workbook and separate `BW` and `QM` annotation workbooks, plus `IRR.py` with a `calculate_IRR_temporal_dataset()` routine. This means an agreement analysis is present in the public repository and must be audited before saying that ChronoCTI has no relation-annotation agreement materials.

The paper reports:
- median Cohen's κ = 0.83 for a 15% sample of ATT&CK procedure-to-technique mappings (Section 4.2); this is mapping agreement, not the temporal relation task;
- Cohen's κ = 0.49 for categorizing the 124 temporal attack patterns (Section 6.3); this is pattern-category agreement, not the 94-report pair labels.

The temporal-relation IRR calculation in the public code and the exact intersection/alignment of the BW and QM pair annotations have not yet been independently reproduced. Audit the workbook schemas, pair-ID overlap, label definitions, duplicates, and the denominator used by `IRR.py` before citing a temporal-label agreement score.

ChronoCTI paper: https://doi.org/10.1007/s10115-025-02491-6  
IRR code: https://github.com/rayhanur-rahman/ChronoCTI/blob/main/temporal-learner-code/IRR.py  
IRR data directory: https://github.com/rayhanur-rahman/ChronoCTI/tree/main/temporal-learner-code/IRR_data
