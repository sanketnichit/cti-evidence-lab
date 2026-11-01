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


## Addendum — 1 November 2026 follow-up checks

| ID | Claim / finding | Evidence checked | Limit / safe interpretation |
|---|---|---|---|
| E-13 | ChronoCTI's inspected graph implementation uses report-local technique nodes and excludes same-technique candidate pairs. | Official code: `temporal-learner-code/learn_graph_ML_imbalanced_multilabel-v2.py`; node name pattern is `technique@report`; pair list uses `idx1 != idx2`. | Applies to this public graph/pair construction. Do not generalize to every intermediate file. Same-technique temporal-edge omission is an inference to test against actual annotated reports. |
| E-14 | CASIE establishes cybersecurity event extraction and semantic-role/argument annotation. | Satyapanich et al. AAAI 2020 paper: https://doi.org/10.1609/aaai.v34i05.6401; screenshot of the relevant PDF page checked. Paper states event coreference and full KG integration were future work for the study. | Its public repo README mentions a `link_coref.py` helper. Inspect actual code and annotation outputs before saying it implements validated coreference. No corpus reuse licence confirmed. |
| E-15 | CSEM-CTI is prior work on evidence-token mining for sentence-level ATT&CK technique classification. | Peng et al., iScience 2026: https://doi.org/10.1016/j.isci.2026.116466; full text https://pmc.ncbi.nlm.nih.gov/articles/PMC13320542/. Uses SeqMask, LLM-TIKG and CTIBench; reports ERASER evidence faithfulness. | All described corpora are sentence-level; ERASER evaluated on SeqMask only. Does not establish event-instance identity or event-pair temporal-edge evidence. Do not claim novelty for generic CTI evidence extraction. Code deposit is stated, but repository URL wasn't identified in the key-resources table checked. |
| E-16 | A 2026 STIX CTI preprint already represents report-level attack-pattern objects mapped to ATT&CK, without modeling temporal attack sequences. | Das et al., arXiv:2607.23312: https://arxiv.org/abs/2607.23312; full text reviewed. 150 reports, 4,777 entities, 5,817 edges, 1,273 attack-pattern objects, 269 unique ATT&CK IDs. | Could preserve multiple behavior objects per report, so this is close prior art for occurrence representation. Paper says dataset/code are to be released upon acceptance; no release found in this check. 25/150 reports were independently human reviewed. Reassess when data become available. |
| E-17 | AnnoCTR includes full report text and a cybersecurity-specific label subset, but not event-event temporal links. | Official paper https://aclanthology.org/2024.lrec-main.103/ and official repo README/LICENSE. 400 reports total; 120 cyber-specific; CC BY-SA 4.0 corpus; TimeML `time` files for temporal expressions. | The exact data file tree and per-report provenance/alignment still need inspection. Cyber-specific annotations were mainly single-expert; limited second-annotator comparison reported ~0.54 document-level technique-set F1. |
| E-18 | SMAH-CTI's public schema is sentence-scoped and has no event-coreference or event-event temporal relation fields. | Official repository `schema/schema.json`, README and LICENSE-DATA. Data CC BY-NC 4.0; code MIT. | Preceding-sentence context and sentence IDs are not temporal relation labels. Third-party source conditions still matter. |
| E-19 | APTIE's described annotations are sentence-scoped; entity semantic links are not event-event temporal links. | Sun et al., Scientific Data 2026: https://doi.org/10.1038/s41597-026-07487-7. | Chinese resource; no direct English CTI temporal-pair benchmark. Verify Zenodo licence before reuse. |
| E-20 | The 2026 event-relation survey's statement that no public cybersecurity ERE dataset exists must be narrowed when discussing ChronoCTI. | Survey DOI https://doi.org/10.1049/cmu2.70187 plus ChronoCTI paper's Figshare v3 availability statement. | Survey may define ERE differently from technique-pair temporal prediction. Do not make a blanket absence claim. Safe phrase: no located public benchmark jointly provides report-level event mentions, event-instance/coreference identity, ATT&CK mapping and evidence-grounded event-event temporal relations. |

## Current project-level implication

The candidate is no longer “CTI event extraction” or “evidence-grounded ATT&CK mapping.” Those have substantial prior work. The potential value is a measurement study of **occurrence-to-technique projection and temporal relation loss/conflation**, with relation-specific source evidence. It remains unproven until a pilot demonstrates repeated distinct instances and enough explicit temporal relations.

## Unresolved data gates

1. ChronoCTI Figshare v3 manifest, file schemas, release permissions/licence and current accessibility. A previous audit attempt recorded a restricted/shared-privately state; the current state was not independently resolved in this pass.
2. AnnoCTR exact file tree, report text, annotation alignment, and per-report source/provenance details.
3. Current acceptance/release status of the 2026 STIX dataset preprint.
4. CASIE actual `link_coref.py` functionality and corpus reuse permissions, if CASIE is considered as a candidate.
