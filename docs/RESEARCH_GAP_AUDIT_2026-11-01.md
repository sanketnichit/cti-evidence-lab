# Research Gap and Reproducibility Audit — 1 November 2026

**Project:** CTI Evidence Lab  
**Audit status:** Preliminary, source-checked; novelty not established  
**Decision:** NARROW  
**Implementation:** Not started

This audit records what has been checked so far and separates published facts from our interpretation. It is not a claim that the research gap has been proven.

## 1. Current candidate question

> In CTI reports containing multiple distinct occurrences of the same ATT&CK technique, what event-instance identity and explicitly supported temporal distinctions are lost, conflated, or made ambiguous when the report is reduced to a report-level technique-node or technique-pair representation?

The secondary question—whether evidence-linked extraction with explicit abstention improves temporal-edge reliability—remains a possible follow-on study. It is not part of the primary experiment unless the annotation pilot supports it.

## 2. What ChronoCTI already does

**Published facts**

- Rahman et al., *Mining temporal attack patterns from cyberthreat intelligence reports*, appeared in *Knowledge and Information Systems* (2025), DOI: https://doi.org/10.1007/s10115-025-02491-6.
- ChronoCTI represents reported attack actions with MITRE ATT&CK techniques and predicts temporal relations between technique pairs.
- The evaluation uses a curated set of 94 CTI reports (7,052 sentences) and a selected vocabulary of 120 techniques.
- Its temporal labels include BEFORE, SIMULTANEOUS-OVERLAP, CONCURRENT and NULL.
- The paper reports severe class imbalance, low recall, upstream error propagation and approximately 45–60 minutes of manual temporal annotation per report.
- The authors acknowledge that ground truth depends partly on annotator judgement and that the restricted 120-technique vocabulary limits coverage.

**Code inspection**

The official repository is https://github.com/rayhanur-rahman/ChronoCTI.

In `temporal-learner-code/Utils.py`, the processing code uses report, T1 and T2 as pair identifiers and constructs labels from the temporal relation spreadsheet. In `temporal-learner-code/learn_graph_ML_imbalanced_multilabel-v2.py`, graph nodes are named using a technique identifier plus report identifier. This is a technique-per-report representation, not a graph with a separately identified node for every report-local execution.

This makes ChronoCTI a relevant baseline and a concrete place to study representation granularity. It does **not** yet prove that a new event-instance study is novel.

**Reproducibility caveat**

The paper points to Figshare version 3 for code and data: https://doi.org/10.6084/m9.figshare.26039518.v3. The official GitHub README says intermediate outputs are not present in that code repository and describes a large model-storage requirement. The Figshare record is linked by the paper, but its complete file manifest, schema and applicable licence have not yet been independently inspected in this audit. We must not claim that the released files are unavailable, nor claim that they are fully reproducible, until this gate is completed.

## 3. Attack Flow: useful, but not temporal ground truth

Official MITRE documentation defines an Attack Flow action as an adversary executing a specific technique. However, an arrow between actions indicates a dependency: the later action requires the earlier action to complete successfully. MITRE explicitly warns that this is not equivalent to saying one action happened before another.

Reference: https://center-for-threat-informed-defense.github.io/attack-flow/introduction/

Therefore:
- Attack Flow is useful as a model for distinct action objects and source attribution.
- Its dependency edges must not be relabelled as temporal BEFORE edges.
- Its sample flows are not automatically report text paired with human-annotated event mentions and temporal links.
- Do not use Attack Flow graphs as the primary temporal gold standard without a separate, justified mapping.

## 4. Dataset landscape: precise boundaries

### ChronoCTI
Direct CTI temporal technique-pair baseline. Its graph abstraction is relevant, but we still need to inspect Figshare version 3 files, actual schema and licence.

### AnnoCTR
The 2024 AnnoCTR corpus provides CTI reports, cybersecurity entity/ATT&CK annotations and TimeML temporal-expression information. TIMEX expressions are not the same as event-to-event TLINK labels or event-coreference chains. It is a candidate source only after checking the exact files, source-text rights and report availability.

Paper: https://aclanthology.org/2024.lrec-main.103/  
Repository: https://github.com/boschresearch/anno-ctr-lrec-coling-2024

### SMAH-CTI
The EMNLP 2026 Findings benchmark has 100 public reports and 12,304 sentence instances. It provides relevance labels, CTI NER (including Action spans), ATT&CK mapping and annotator-written grounded procedures. The resource is sentence-level; its released schema is not a document-level event-coreference and event-temporal relation benchmark. Dataset files are CC BY-NC 4.0; code is MIT.

Project and release details: https://seal.cs.ucf.edu/projects/smah-cti.html

### APTIE
APTIE (Scientific Data, 2026; DOI https://doi.org/10.1038/s41597-026-07487-7) includes 116 Chinese CTI reports, 808 sentences, entity/relation/event modules and 139 event-triggering sentences. Its methods explicitly treat sentences as independent annotation units and exclude cross-sentence aggregation and document-level reasoning. Its relation module annotates semantic relations between entities (for example, exploits/targets); these are not event-to-event temporal links.

Paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC13226696/  
Dataset: https://doi.org/10.5281/zenodo.17129303

### MAVEN-ERE
MAVEN-ERE (EMNLP 2022) supplies large-scale general-domain event coreference, temporal, causal and subevent relations. It is important prior work and a methodological reference, but does not provide CTI-specific ATT&CK-grounded event annotations.

Paper: https://aclanthology.org/2022.emnlp-main.60/

### Cybersecurity event-relation survey
A 2026 survey describes cybersecurity event relation extraction as underdeveloped and reports no unified, widely adopted public benchmark. This should be stated carefully alongside APTIE and other adjacent resources, not simplified into “there are no cybersecurity event datasets.”

Survey: https://doi.org/10.1049/cmu2.70187

## 5. What can be measured without pretending the graph mathematics is the contribution

The first experiment should measure real-report consequences of projecting manually annotated event instances to technique categories.

Candidate descriptive outcomes:
1. **Repeated-instance prevalence:** fraction of sampled reports in which one ATT&CK concept maps to two or more distinct event instances.
2. **Instance-collision count:** number of distinct event instances merged into a single technique node.
3. **Same-technique relation loss:** event-pair temporal relations whose endpoints map to the same technique and therefore become a self-relation or disappear in a unique-technique graph.
4. **Relation conflation:** distinct event-pair relations that collapse to the same technique pair, including cases where the technique pair cannot identify which event occurrences the relation concerns.
5. **Ordering distortion:** whether strict BEFORE relations induce cycles after technique projection. Only strict ordering edges belong in this analysis; OVERLAP, SIMULTANEOUS and dependency relations must not be mixed into a strict temporal DAG.

Metric definitions must be formalized and tested on toy graphs before they are reported. Counts over event-node and technique-node graphs cannot simply be compared without a defined mapping and denominator. A graph-contraction result alone is not enough: the study must show that the phenomenon occurs in real reports and occurs often enough to matter.

## 6. Attack Flow and temporal semantics must stay separate

Use distinct labels for:
- explicit temporal ordering (e.g. BEFORE),
- temporal overlap/simultaneity where directly supported,
- causal or enabling dependency,
- narrative/discourse order only,
- no stated relation,
- unresolved/ambiguous annotation.

Do not infer physical execution order from the order in which an analyst writes a report. Do not treat an Attack Flow dependency arrow as a temporal timestamp relation.

## 7. Feasibility pilot: gate before full implementation

Do not commit to Gemini's proposed 50-report corpus yet.

First:
1. Inspect ChronoCTI Figshare v3 metadata, files, schema and licence.
2. Inspect the exact AnnoCTR and SMAH-CTI schemas and source-report provenance/licences.
3. Select a small 5–8 report pilot that includes candidate repeated-technique cases and sufficient report context. This is a feasibility sample, not a prevalence estimate for all CTI reports.
4. Annotate separate objects for event mentions, event instances, ATT&CK links, event-pair temporal relations and relation-specific evidence spans.
5. Double-annotate an overlapping subset with a second human annotator if available; otherwise report that independent agreement was not measured.
6. Record repeated-instance frequency, positive relation counts, unresolved cases, annotation time and disagreements.
7. Proceed only if the task is consistently annotatable, source rights are acceptable and the phenomenon appears sufficiently often.

Do not use an LLM-generated annotation as ground truth. AI may help explore candidate interpretations, but the gold labels must be human-reviewed and independently adjudicated.

## 8. Baselines to consider after the pilot

- **Technique aggregation baseline:** project each human-annotated event instance onto its ATT&CK concept within a report.
- **ChronoCTI:** reproduce or re-evaluate its technique-pair representation only if its released data/schema/licence make that scientifically and legally possible.
- **Deterministic temporal-cue baseline:** only if temporal relation extraction becomes a measured secondary task.
- **Event-pair learned model / evidence-linked model:** defer until there is enough reliable human-labelled data.

Do not compare methods across incompatible relation schemas or report subsets as if this were a controlled head-to-head evaluation.

## 9. Stop and pivot conditions

Narrow or abandon the event-instance experiment if:
- repeated distinct occurrences are rare in the accessible corpus;
- human annotators cannot reliably distinguish separate occurrences from repeated mentions;
- explicit temporal evidence is too sparse;
- data rights or source provenance are unresolved;
- ChronoCTI data cannot be lawfully/reproducibly inspected and no fair alternative baseline exists.

A negative feasibility result is valuable. It prevents us building a system around an untestable claim.

## 10. Student-led research and AI assistance

The student researcher owns the final question, data-selection decisions, human annotation, experiment execution/reproduction, interpretation and conclusions. AI tools may assist with source discovery, explanations, code review, debugging and language editing. AI-generated annotations are not ground truth. All results must be generated by executed experiments; AI assistance must be disclosed in accordance with university and venue rules.

Maintain a lightweight AI assistance log recording material assistance, accepted/rejected suggestions and verification. The manuscript must not claim work the student cannot explain or reproduce.

## 11. Primary sources checked

- ChronoCTI journal article: https://doi.org/10.1007/s10115-025-02491-6
- ChronoCTI code: https://github.com/rayhanur-rahman/ChronoCTI
- ChronoCTI Figshare v3: https://doi.org/10.6084/m9.figshare.26039518.v3
- MITRE Attack Flow introduction: https://center-for-threat-informed-defense.github.io/attack-flow/introduction/
- AnnoCTR paper: https://aclanthology.org/2024.lrec-main.103/
- SMAH-CTI benchmark: https://seal.cs.ucf.edu/projects/smah-cti.html
- APTIE paper: https://doi.org/10.1038/s41597-026-07487-7
- MAVEN-ERE paper: https://aclanthology.org/2022.emnlp-main.60/
- Cybersecurity event-extraction survey: https://doi.org/10.1049/cmu2.70187

**Current conclusion:** NARROW. The representation-granularity problem is worth a controlled feasibility study, but the exact novelty, data sufficiency and baseline reproducibility remain unproven. No implementation or publication claim should begin before those gates are resolved.


## 12. Follow-up prior-art audit — 1 November 2026

The following studies change the novelty boundary and must be included before any research proposal or paper draft.

### CASIE: cybersecurity event extraction already exists

CASIE (Satyapanich et al., AAAI 2020) annotates 1,000 English cybersecurity news articles with event nuggets, arguments, semantic roles and realis values across five event subtypes. The original paper explicitly says the presented work focuses on the first four components and leaves event coreference and full knowledge-graph integration to future work. Its public repository README mentions a later `link_coref.py` helper; the code and any corresponding annotation output must be inspected before describing that capability as implemented or evaluated.

Paper: https://doi.org/10.1609/aaai.v34i05.6401  
Repository: https://github.com/Ebiquity/CASIE

**Consequence:** generic “cybersecurity event extraction” is not our contribution. The corpus licence is also unverified for our potential use.

### CSEM-CTI: evidence extraction for ATT&CK mapping already exists

Peng et al. (iScience, published 25 June 2026) propose CSEM-CTI for evidence-token mining and sentence-level ATT&CK technique classification. The paper uses SeqMask, LLM-TIKG and CTIBench, and evaluates evidence faithfulness with ERASER. It states the corpora are sentence-level and that ERASER results are computed on SeqMask only, so the evidence claims are corpus-specific. It does not address event-instance coreference or temporal relations between two event occurrences.

Paper: https://doi.org/10.1016/j.isci.2026.116466  
Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC13320542/

**Consequence:** generic “evidence-grounded CTI classification” is not novel. Our positive temporal edge must carry evidence connecting two identified event instances; evidence supporting a single technique classification is not enough.

### A 2026 STIX 2.1 dataset preprint already contains report-local behavior objects

Das et al. (arXiv:2607.23312, submitted 25 July 2026) describe 150 English CTI reports as directed heterogeneous STIX graphs, including 1,273 attack-pattern objects mapped to 269 unique ATT&CK identifiers. Each report has a nodes file and an edges file; each node has a report-local identifier, object type, instance and source-derived description. This may preserve multiple attack-pattern objects in a report even when several map to the same ATT&CK technique.

The paper explicitly says the dataset does not model temporal attack sequences and lists temporal relations as future work. It says complete data/code/materials will be made public upon acceptance; no public release was located in this check. Twenty-five reports were independently human-reviewed, with weighted kappa values of 0.64 (entity type), 0.67 (ATT&CK mapping) and 0.62 (relationship correctness). The full dataset therefore must not be treated as fully independently verified from the 25-report audit subset.

Preprint: https://arxiv.org/abs/2607.23312

**Consequence:** do not claim that preserving report-local attack-pattern objects is novel. The candidate should examine whether explicit occurrence-to-occurrence temporal relations can be annotated and how much those relations are lost or conflated when occurrence objects are normalized to ATT&CK technique nodes/pairs or omitted from existing graph schemas. Reassess the paper if its dataset becomes available.

### AnnoCTR and SMAH-CTI: confirmed annotation boundaries

AnnoCTR has 400 reports; its cybersecurity-specific layer covers 120. The corpus repository includes report text and TimeML temporal-expression files. It does not supply event-event temporal TLINKs or event-instance coreference. The corpus is labelled CC BY-SA 4.0 in the official repository, and the paper says vendors permitted republication under that licence. The cyber-specific labels were created primarily by one domain expert, with a limited second-annotator comparison reporting approximately 0.54 average document-level technique-set F1. Inspect exact file tree and report provenance before sampling.

SMAH-CTI's public schema was inspected directly. It stores report/sentence/page IDs, preceding-sentence context, Action spans, ATT&CK labels and grounded procedure text. The data are licensed CC BY-NC 4.0 and code MIT. This is useful for CTI extraction, but the schema does not include event-instance coreference or event-event temporal links.

### Revised bounded research question

> In a sample of CTI reports with human-resolved event instances, how often do distinct event instances map to the same ATT&CK technique, and how much explicitly supported event-to-event temporal information becomes unrepresentable, lost or conflated when event instances are projected to report-level technique nodes or technique pairs?

This is an empirical question, not yet a novelty claim. It is deliberately narrower than event extraction, event graph construction, or evidence-grounded technique classification.

### Candidate measurement definitions to formalize before the pilot

Let (V) be the set of human-resolved event instances in a report, (f:V\to T) map each instance to an ATT&CK technique, and (E_{before}\subseteq V\times V) be only explicitly supported strict BEFORE relations.

1. **Repeated-instance prevalence:** proportion of reports where at least one technique has two or more distinct event instances.
2. **Same-technique edge-loss rate:** proportion of strict BEFORE edges ((u,v)) for which (f(u)=f(v)). Such edges become self-relations and disappear if the projected graph disallows self-edges.
3. **Technique-pair conflation:** count distinct event-instance edges that map to the same ordered technique pair, with denominators clearly reported. Preserve relation labels and evidence separately; do not deduplicate silently.
4. **Projection-induced cycle rate:** proportion of reports where the projected strict-BEFORE graph contains a directed cycle even though the source event-instance graph is acyclic. Test only strict ordering edges; never include overlap, simultaneity, concurrency or dependencies.

These are candidate definitions, not finalized metrics. Test them on manually constructed toy graphs first. Also examine whether event-level BEFORE labels are transitive in the report or only locally stated; do not add inferred/transitive edges to the primary gold layer without an explicit rule.

### Current decision and stop rules

Remain at **NARROW**. Do not build a predictive model until the Figshare and AnnoCTR source gates are resolved and a 5–8 report pilot demonstrates (a) enough repeated distinct instances, (b) enough explicit temporal relations, (c) consistent human annotation and (d) usable source rights. A second human annotator is preferred; absent one, state that inter-annotator agreement was not measured. AI may help locate candidate passages or audit schema consistency, but must not generate gold labels.
