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
