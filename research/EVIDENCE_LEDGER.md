# Research Evidence Ledger

**Access date recorded in initial audit:** 2026-11-01. Recheck sources before publication or any claim about current availability.

| Source | Evidence role | Key point recorded | Limit / action |
|---|---|---|---|
| ChronoCTI paper, DOI: https://doi.org/10.1007/s10115-025-02491-6 | Direct CTI temporal-graph baseline | Extracts sentence-to-ATT&CK mappings, predicts relations between technique pairs, constructs temporal attack graphs. Reported graph-level MUC-5 P/R/F1 in the reviewed account: 0.58/0.25/0.34. | Confirm exact split, metric implementation, and paper/repo alignment. Obtain workbook lawfully; inspect schema. |
| ChronoCTI code: https://github.com/rayhanur-rahman/ChronoCTI | Reproducibility and implementation | Public repository; README notes substantial disk/model requirements and legacy dependencies. | Repository licence does not automatically license report corpus or each dataset artifact. |
| ChronoCTI Figshare record | Data access | Initial check indicated record marked “shared privately”. | Recheck access status; request author access or identify alternative. |
| SMAH-CTI, Findings of EMNLP 2026: https://aclanthology.org/2026.findings-emnlp.1180/ | Recent CTI benchmark | Sentence relevance, entity extraction, ATT&CK mapping, grounded procedure descriptions. Initial audit records 100 reports, 12,304 sentence instances, and 15,487 entity annotations. | Inspect full paper/data licence and determine exact overlap. Not temporal edge gold data as currently understood. |
| SMAH-CTI repository: https://github.com/davidmohaisen/SMAH-CTI | Code/data access | Public project repository. | Verify dataset files, licences, and version in the current checkout before use. |
| CSEM-CTI, iScience 2026: https://doi.org/10.1016/j.isci.2026.116466 | Evidence mining prior work | Contrastive evidence mining for CTI classification / tactic and technique prediction. | Read full method and evidence evaluation; distinguish sentence classification evidence from temporal-edge evidence. |
| AnnoCTR paper: https://arxiv.org/abs/2404.07765 | Annotation precedent | 400 English CTI reports with entity, time-expression, and cybersecurity concept annotations. | No event-pair temporal edge labels known; check exact hosted version and annotation fields. |
| AnnoCTR dataset: https://huggingface.co/datasets/priamai/AnnoCTR | Candidate corpus | Dataset card records CC BY-SA 4.0. | Check source-report rights, data version, splits, and whether text redistribution is permissible in the intended use. |
| CTI-HAL: https://github.com/dessertlab/CTI-HAL | Human annotation precedent | Passage-to-ATT&CK mapping annotations by multiple annotators. | Repository declares no licence in initial inspection; seek permission before reuse. |
| MITRE TRAM: https://github.com/center-for-threat-informed-defense/tram | Existing mapping system | Open-source research/analyst tool for mapping CTI reports to ATT&CK. | Code licence is not the same as all underlying model/data rights; task is not temporal edge extraction. |
| Event graphs (Glavaš & Šnajder): https://doi.org/10.1017/S1351324914000060 | General NLP prior work | Event mentions as graph nodes with temporal/coreference edges. | Read exact task, graph construction, and evaluation to avoid overstating novelty. |
| TIMELINE, EMNLP 2023: https://aclanthology.org/2023.emnlp-main.1016/ | Temporal annotation precedent | Document-level long-distance temporal relations and nominalized events. | Inspect annotation schema and agreement methodology. |
| Structured STIX CTI graphs (2026 preprint): https://arxiv.org/abs/2607.23312 | Adjacent CTI graph prior | 150 reports represented as STIX graphs; reported entities, relations, and a human-reviewed subset. | Preprint status; verify public data availability, licence, and relationship evaluation details. |
| APTIE, Scientific Data 2026: https://doi.org/10.1038/s41597-026-07487-7 | Adjacent CTI event/relationship dataset | Chinese CTI entity/relation/event extraction with STIX 2.1 alignment. | Language mismatch; inspect actual event and temporal semantics before using as comparable data. |
| Open-source LLM ATT&CK mapping evaluation (2026): https://arxiv.org/abs/2606.18166 | Baseline context | Initial audit records seven open LLMs evaluated on 2,076 annotated sentences from 83 reports. | Preprint; verify version and methodology. |
| Digital Precognition (IEEE ICAIC 2026): https://doi.org/10.1109/ICAIC67076.2026.11395807 | Retrieval/reranking prior | Retrieval plus fine-tuned cross-encoder for ATT&CK mapping. | Review paper for data size, protocol, and performance before comparison. |

## Citation and verification policy

- Prefer the published paper over secondary summaries.
- Record version, publication status, date checked, and licence separately.
- Do not treat GitHub repository visibility as data reuse permission.
- Do not cite numbers from this ledger in a paper until rechecked against the primary source.
- Add negative findings and contradictory evidence, not just supportive sources.
