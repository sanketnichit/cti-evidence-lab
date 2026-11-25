# Occurrence identity in technique-level CTI graphs

## An exploratory feasibility study

**CTI Evidence Lab · Sanket Nichit · 19 November 2026**

**Status:** Exploratory feasibility and controlled query-fidelity study. Source review is not independently validated. The representation experiments use synthetic inputs. This is not a completed gold-annotation or prevalence study.

## Abstract

Cyber threat reports mix incident descriptions, campaign summaries, malware capabilities and analyst observations. Representing these statements with ATT&CK technique nodes can obscure the distinction between a behavior category and a particular occurrence. This study examines the prerequisites for measuring that loss. It combines an original five-report AnnoCTR review, two fixed five-report extensions, source-integrity checks against a 120-report frame, and seven deterministic representation controls. All 120 source hashes were reproduced after an explicitly verified line-ending recovery, and 33 pilot evidence pointers passed structural checks. The original five-report reading retains one identifiable attack-occurrence candidate but does not establish a qualifying same-technique temporal pair. Synthetic controls show that distinct-pair projection can omit relations, that self-loops do not preserve occurrence identity, and that projected cycles have more than one cause. A connected-sequence query experiment further demonstrates unsupported paths in acyclic technique graphs and separates the effects of diagonal retention and occurrence-compatible joins. These findings support a bounded representation and feasibility study, not a population estimate or a claim of improved extraction accuracy.

## 1. Question and contribution

The question is: **what occurrence identity and temporal information can a distinct-technique-pair graph retain from source-supported attack occurrences?** Two issues must be separated. The mathematical behavior of a specified projection can be tested directly. The frequency and importance of its effects in CTI reports require source-backed annotations and an appropriate sample.

The present study provides reproducible controls, a traceable exploratory source assessment and a connected-sequence query benchmark. It tests not only what edges disappear, but whether a projected path supports the same answer as the source occurrence graph. It does not introduce event graphs, claim new ATT&CK extraction methods, train a model, or establish novelty.

## 2. Closest methodological context

ChronoCTI already extracts temporal attack patterns and represents attack actions using ATT&CK techniques. Its paper specifies ATT&CK v12.1. It is a direct motivation for examining technique-level representations, not evidence that this project's annotations or predictions are correct. Our deterministic projection is not a run of ChronoCTI's learned pipeline. See [Rahman et al., 2025](https://link.springer.com/article/10.1007/s10115-025-02491-6).

AnnoCTR provides document-level entity, temporal-expression and cybersecurity concept annotations. Those resources support source retrieval and technique-link inspection; they do not make our proposed occurrence-pair labels gold. See [Lange et al., 2024](https://aclanthology.org/2024.lrec-main.103/).

MATRES demonstrates the importance of defining temporal annotation units carefully, including event axes and start points. Its general-domain scheme is relevant precedent, not a directly interchangeable CTI codebook. See [Ning et al., 2018](https://aclanthology.org/P18-1122/).

[Attack Flow](https://center-for-threat-informed-defense.github.io/attack-flow/language/) represents separate action identities, optional times and potential effects. [AttacKG+](https://doi.org/10.1016/j.cose.2024.104220) organizes behavior graphs, technique labels and state summaries across temporal steps. [AttackSeqBench](https://arxiv.org/html/2503.03170v3) tests reasoning about reconstructed tactic, technique and procedure sequences. The [closest-system comparison](RELATED_WORK_MATRIX.md#closest-system-comparison) distinguishes their units, link semantics and evaluation targets. This study contributes a controlled comparison of a specified projection and source cases that show where it changes connected-query answers.

## 3. Data and procedure

The existing frame contains 120 AnnoCTR train/dev/test reports and fixes one rank-one candidate per donor by the recorded within-donor ordering. The five candidates were retained regardless of apparent event yield. They are a feasibility set, not a prevalence sample. Two earlier genre exclusions elsewhere in the historical frame do not change the five-report queue.

The source audit reads the local corpus using strict UTF-8, removes only an optional leading BOM, and preserves text unless an explicit CRLF recovery reproduces the frame hash exactly. All 120 local files required that recovery. The original files remain untouched. All 33 existing pilot anchors were checked for source hash, bounds, line position and uniqueness. Hash equality verifies source identity under the stated convention; it cannot verify a reading of the text.

The exploratory pass examined the supplied report text, captions and tables with prior draft exposure. It did not inspect linked images or incident telemetry. Each report has a recorded interpretation, contrary reading, and remaining resolution. No human review completion, independent adjudication, or protocol freeze is asserted. The raw text stays outside Git; source-derived decisions retain AnnoCTR/publisher attribution and CC BY-SA terms.

The primary working rules require distinct resolved attack occurrences, supported incident compatibility, accepted event-level mappings and relation-specific source evidence. Generic capabilities, sample analysis, actor communications and cross-incident narratives remain visible but are not silently converted into primary event pairs. An unnamed victim or missing exact timestamp alone does not disqualify an otherwise identifiable occurrence.

## 4. Exploratory source findings

| Report | Strongest useful evidence | Remaining obstacle |
|---|---|---|
| Intel471 Groove/Babuk | Dated communications and multiple victim contexts | Actor-level TTPs and publication activity cannot be combined into one intrusion timeline |
| Lab52 TokyoX Part 2 | Detailed command behavior and internal ordering | Implemented behavior is not proof of particular victim-side command invocations |
| Proofpoint Privacy Tools | Initial delivery followed by further malware download | Atomic occurrence identity, shared incident and both endpoint mappings are unresolved |
| QuoIntelligence Winnti | Target assessments, sample metadata and DNS behavior | Separate target contexts and uncertain compromise timing prevent an accepted occurrence pair |
| Zscaler Netwire | A particular email send with a reported timestamp | Subsequent sample behavior is not tied to a second resolved occurrence in the same incident |

This pass retains one identifiable attack-occurrence candidate and no established qualifying within-technique pair. This is not a census of all asserted actions. The [critical second pass](feasibility/exploratory_review_v0.1/CRITICAL_REVIEW.md) checks 22 source passages, including evidence outside the initial anchor set. It preserves Proofpoint's observed chain and website creation, considers QuoIntelligence's code signing as a possible preparatory action, and distinguishes Zscaler's email exemplar from a recipient-level transmission count. These checks strengthen the unresolved interpretation without turning missing occurrence or incident linkage into evidence of absence.

No formal denominator is computed. Pending or unresolved review is not a negative label. The formal annotation registers and selection gates remain unchanged. Full judgments and source bindings are in [the review package](feasibility/exploratory_review_v0.1/README.md).

### Fixed five-report extension

A separate extension retains all five rank-two entries in the existing donor order. Its selection and review protocol were committed before source-text inspection for this extension; this is not an external preregistration or an assertion of no earlier inventory exposure. It replaces none of the original reports. All five complete texts were read and 22 additional passage bindings verified against their frozen corpus hashes.

No primary three-occurrence intrusion sequence is established in this pass. Intel471 and Proofpoint describe aggregated affiliate or campaign chains. Lab52 explicitly places reconnaissance two weeks before phishing, but a third observed action and individual occurrence scope remain unresolved. QuoIntelligence explicitly reports live sample execution during analysis; that is execution evidence, although it does not establish victim-side execution. Zscaler describes observed configurations and module retrieval across multiple samples without resolving one complete run. These distinctions preserve positive evidence at its supported level instead of treating unresolved primary graphs as negative labels. Query errors remain unassessed. The [extension records](feasibility/rank_two_extension_v0.1/README.md) retain all candidates, contrary readings, evidence bindings and provenance limitations. The two five-report groups and external intrusion are not pooled into a prevalence estimate.

### Separate source-bound sequence case

A purposive extension of the previously examined DFIR intrusion distinguishes two RDP attempts and their associated account removals. Four narrated ordering relations yield three paths containing two supplied BEFORE edges. The case is outside AnnoCTR and is not an independent validation sample. Seven source-passage bindings, occurrence decisions, mapping alternatives and unresolved candidate chains are recorded in the [sequence case study](case_studies/dfir_rdp_sequence_v0.2/README.md).

The conservative interpretation leaves the cleanup technique mapping unresolved, so none of the three paths is fully mapped and technique-query errors are not assessed. If the proposed cleanup mapping is adopted, distinct pairs miss one supported query, while loop-inclusive pairs return two unsupported queries. Endpoint-compatible joins with loops retain the three supported answers. Removing the original attempt-order shortcut in a declared local-edge sensitivity yields two supported queries that all four representations answer correctly. These are conditional results for the recorded graph, not an unqualified empirical error rate. The pinned v12.1 taxonomy definition, rather than newer wording, governs the mapping assessment.

The second external case was selected as the next report in the publisher's chronological metadata before content review. It supports a core chain of RDP session initiation, internal DLL transfer and rundll32 execution. All four representations preserve its one connected-sequence answer. A six-action extension adds two distinct batch invocations separated by archiving. Ordinary pair graphs return four supported answers and one unsupported archive-script-archive query, while endpoint-compatible joins return only the four supported answers. The failure remains with exact technique IDs and involves no diagonal loss. The archive mapping is purpose-sensitive: withholding it leaves two of four paths fully mapped and errors unassessed. Thirteen source bindings and all sensitivities are recorded in the [second case study](case_studies/dfir_html_smuggling_v0.1/README.md). This adds a separate intrusion, not independent annotation validation.

## 5. Representation experiment

Let M(u) and M(v) be the accepted technique sets for two distinct occurrences. The mapping combinations are M(u) × M(v). The primary projection discards diagonal combinations (t,t); the loop-permitting control retains them. The occurrence-preserving control keeps the original event endpoints and relation labels.

For nonempty mapping sets, an edge is fully omitted exactly when both sets contain the same single technique. To see this, if every cross-product pair is diagonal, every member of either set must equal every member of the other. If at least one diagonal and one distinct pair exist, the edge is partially represented. If either endpoint is unmapped, the edge is classified separately as unmapped, not as diagonal omission.

Seven deterministic controls cover distinct mappings, identical singleton mappings, repeated same-technique actions, mixed mappings, an unmapped endpoint, occurrence collapse causing a cycle, and single-edge mapping fan-out causing a cycle. [Generated tables and full provenance](experiments/representation_controls_v0.1/README.md) are reproduced by the supplied command.

Three results matter. First, two successive same-technique relations vanish in the distinct-pair graph but merge into one loop when loops are allowed: permitting loops does not recover endpoint identity. Second, a missing mapping is not evidence of projection-induced omission. Third, both a two-edge occurrence chain and a single multi-mapped edge can create a technique cycle despite an acyclic source graph. A projected cycle alone therefore does not identify its cause.

These are consequences of defined inputs and mappings. They provide no estimate of their frequency in CTI and no performance comparison with published systems. Exact-sub-technique sensitivity on accepted real annotations remains unrun.

### Exhaustive finite check

To test beyond the seven illustrations, we enumerate three ordered event vertices, all eight subsets of their forward BEFORE edges, and all eight subsets of a three-technique vocabulary independently assigned to each vertex. This includes empty mappings and yields 8 x 8^3 = 4,096 graph inputs with 6,144 source-edge instances. A separate set-based classification oracle and a reachability-based cycle oracle agree with the projection implementation in every case.

| Source-edge state | Instances |
|---|---|
| Fully omitted | 288 |
| Partially represented | 3,264 |
| No diagonal mapping | 1,152 |
| Unmapped endpoint | 1,440 |

Of the 4,096 constructed acyclic source graphs, 1,102 produce a technique-level cycle. These counts describe this finite construction only: they are neither a corpus prevalence estimate nor a general coverage claim for larger graphs or other temporal relations. The [finite check output](experiments/representation_controls_v0.1/finite_checks.json) records the scope and exact totals. These are implementation checks; the following experiment examines a consequence for queries.

### Connected-sequence queries

Ask whether three distinct occurrences u,v,w support two supplied BEFORE edges u→v and v→w with technique labels A,B,C. Two disconnected edges u:A→v:B and w:B→x:C produce the same technique graph A→B→C as the connected edges u:A→v:B→x:C. The former has no connected source sequence; the latter does. Both technique graphs are acyclic and have the same pair multiplicities. Thus a technique path, even with edge counts, is insufficient evidence of a connected occurrence sequence.

![Two occurrence graphs with the same technique projection](experiments/query_fidelity_v0.1/sequence_counterexample.svg)

A two-factor comparison tests whether to retain diagonal images and whether to join edge images only when their intermediate occurrence IDs match. An independent oracle enumerates occurrence triples. With four ordered occurrences, three singleton technique choices per vertex and all forward edge subsets, there are 5,184 graphs and 139,968 graph-query instances. The complete triple universe includes repeated labels.

| Representation | Unsupported answers (FP) | Missed answers (FN) |
|---|---|---|
| Distinct technique pairs | 1,416 | 2,538 |
| Loop-inclusive technique pairs | 7,527 | 0 |
| Distinct pairs + endpoint join | 0 | 2,538 |
| Loop-inclusive pairs + endpoint join | 0 | 0 |

These comparisons isolate different mechanisms: retaining diagonals recovers valid repeated-technique queries, while endpoint compatibility prevents disconnected occurrences from being joined. The loop-inclusive graph can also reuse one edge image as two hops when only two source occurrences exist. A second construction with three occurrences and all set-valued mappings, including empty sets, yields 4,096 graphs and confirms the same qualitative distinction. Results restricted to distinct adjacent query labels isolate joining errors from diagonal removal.

Exact endpoint joins preserve this query by construction: every returned pair of edges shares a source occurrence, and every source witness has retained edge images when loops are allowed. This is a conditional fidelity guarantee, not perfect extraction or a new event representation. Source errors remain errors, and missing mappings can remove entire paths from the technique-query universe. [The full study](QUERY_FIDELITY_STUDY_v0.1.md) gives the proof, denominators, confusion matrices, storage tradeoff, counterexamples and scope limits.

### Fixed five-publisher extension

A separate rank-three cohort was fixed before source review using the existing donor order. All five complete texts were read and 17 passage bindings verified. No qualifying three-action incident sequence was established under the explicit-edge rule, so primary query errors remain unassessed. Two reports support four conditional procedure interpretations, kept separate from incident observations. Their 70 constructed queries comprise two supported, four mapping-unresolved and 64 not supported in the retained graphs. All four representations agree on the decidable queries: this extension establishes no accuracy advantage. Ordinary loop traversal additionally returns one unresolved repeated-credential query, illustrating the limits of open mapping completion rather than a proven false positive. Action granularity and excluded alternative readings are recorded in the [full comparison](experiments/external_sequence_evaluation_v0.1/README.md). Query totals are not independent sample sizes or extraction scores.

## 6. Limitations and next evidence

The [interpretation sensitivity analysis](experiments/interpretation_sensitivity_v0.1/README.md) applies 203 single or paired evidence-removal scenarios to the two incident cases. Each scenario changes at least one supported answer. A single mapping withdrawal makes affected witnesses unresolved, while a single relation omission or occurrence exclusion removes their support from the retained graph. In the extended domain-controller graph, a projected return can persist while a separate path becomes possible under the open mapping rule. This distinction matters when interpreting projected errors under uncertainty. The scenarios characterize two recorded graphs and do not measure the frequency of interpretation errors.

The [investigation prototype](INVESTIGATION_WORKFLOW_v0.1.md) makes the query comparison inspectable: each answer exposes occurrence witnesses, incompatible projected joins, source locators and mapping requirements. It distinguishes a query with a known witness from one that could be supported only after unknown mappings are resolved. Thus the core transfer/execution query remains supported when the separate archive mapping is withheld, while the aggregate profile error score remains unassessed. An independent completion enumeration checks 1,728 finite graph-query inputs; the interface covers 532 case/profile/query combinations. These are implementation and record-coverage checks, not independent observations or evidence of analyst time savings. Exported answer records can be recomputed against the repository. Action identities and source references already exist in Attack Flow; no novelty is claimed for those features alone.

The sample is small, the protocol is still a draft, the review was exposed to earlier interpretations, and independent review has not yet been returned. Source extraction can omit image evidence. Conservative incident and atomicity rules may reduce usable coverage. Broader campaign-level rules answer a different question. The targeted literature comparison positions the contribution against the closest systems identified and leaves room for additional comparable work.

Independent review has not been completed. The critical second pass challenges the existing interpretation with prior exposure and does not constitute independent replication. Calibration packets are available as research instruments; no completed review or agreement statistic is inferred from their existence.

Further formal annotation requires an accepted protocol, completed annotation checks and source-supported occurrence pairs. The current evidence supports an exploratory feasibility conclusion. A larger incident-narrative study requires a separately declared selection method and denominator; the original five-report cohort remains unchanged.

## 7. Reproduction

Use Python 3.11 or later and Git. From a clean checkout, the standard-library command below runs all five test suites, verifies the base-package checksums, regenerates the seven controls, 4,096-case check and two query-fidelity constructions, checks the curated review bindings, and packages the repository and generated results with a SHA-256 manifest.

```text
python scripts/reproduce_study.py
```

Without a corpus path, source verification is explicitly recorded as a reused audit. To recheck the 120 source files, 33 pilot pointers and 22 critical-review passages locally, append `--corpus-root /path/to/AnnoCTR/all --recover-crlf`. To include a rendered report, install ReportLab and append `--pdf`. The output is `outputs/submission/CTI_Evidence_Lab_Submission.zip`; raw report text and private review packets are excluded. See the [reproduction documentation](../docs/REPRODUCIBILITY.md) for commands and artifact formats. Passing checks establish reproducibility and code integrity, not semantic truth or independent review.
