# Occurrence identity in technique-level CTI graphs

## An exploratory feasibility study

**CTI Evidence Lab · Sanket Nichit · 18 November 2026**

**Status:** Exploratory feasibility and controlled query-fidelity study. Source review is not independently validated. The representation experiments use synthetic inputs. This is not a completed gold-annotation or prevalence study.

## Abstract

Cyber threat reports mix incident descriptions, campaign summaries, malware capabilities and analyst observations. Representing these statements with ATT&CK technique nodes can obscure the distinction between a behavior category and a particular occurrence. This study examines the prerequisites for measuring that loss. It combines an exploratory reading of five fixed AnnoCTR reports, source-integrity checks against a 120-report frame, and seven deterministic representation controls. All 120 source hashes were reproduced after an explicitly verified line-ending recovery, and 33 pilot evidence pointers passed structural checks. The exploratory reading retains one identifiable attack-occurrence candidate but does not establish a qualifying same-technique temporal pair. Synthetic controls show that distinct-pair projection can omit relations, that self-loops do not preserve occurrence identity, and that projected cycles have more than one cause. A connected-sequence query experiment further demonstrates unsupported paths in acyclic technique graphs and separates the effects of diagonal retention and occurrence-compatible joins. These findings support a bounded representation and feasibility study, not a population estimate or a claim of improved extraction accuracy.

## 1. Question and contribution

The question is: **what occurrence identity and temporal information can a distinct-technique-pair graph retain from source-supported attack occurrences?** Two issues must be separated. The mathematical behavior of a specified projection can be tested directly. The frequency and importance of its effects in CTI reports require source-backed annotations and an appropriate sample.

The present study provides reproducible controls, a traceable exploratory source assessment and a connected-sequence query benchmark. It tests not only what edges disappear, but whether a projected path supports the same answer as the source occurrence graph. It does not introduce event graphs, claim new ATT&CK extraction methods, train a model, or establish novelty.

## 2. Closest methodological context

ChronoCTI already extracts temporal attack patterns and represents attack actions using ATT&CK techniques. Its paper specifies ATT&CK v12.1. It is a direct motivation for examining technique-level representations, not evidence that this project's annotations or predictions are correct. Our deterministic projection is not a run of ChronoCTI's learned pipeline. See [Rahman et al., 2025](https://link.springer.com/article/10.1007/s10115-025-02491-6).

AnnoCTR provides document-level entity, temporal-expression and cybersecurity concept annotations. Those resources support source retrieval and technique-link inspection; they do not make our proposed occurrence-pair labels gold. See [Lange et al., 2024](https://aclanthology.org/2024.lrec-main.103/).

MATRES demonstrates the importance of defining temporal annotation units carefully, including event axes and start points. Its general-domain scheme is relevant precedent, not a directly interchangeable CTI codebook. See [Ning et al., 2018](https://aclanthology.org/P18-1122/).

[Attack Flow](https://center-for-threat-informed-defense.github.io/attack-flow/language/) already distinguishes individual actions from technique identifiers. Its effect edges describe dependencies and outcomes; we do not reinterpret them as source-observed BEFORE relations. [AttacKG+](https://doi.org/10.1016/j.cose.2024.104220) also organizes behavior and technique labels across temporal steps. Keeping occurrence identity is therefore established prior art. Our comparison concerns query fidelity under a specified abstraction, not superiority over these systems. The broader [related-work matrix](RELATED_WORK_MATRIX.md) remains a working literature map; a complete novelty assessment is still open.

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

## 6. Limitations and next evidence

The sample is small, the protocol is still a draft, the review was exposed to earlier interpretations, and independent review has not yet been returned. Source extraction can omit image evidence. Conservative incident and atomicity rules may reduce usable coverage; broader campaign-level rules answer a different question. The literature comparison is not a completed novelty review.

Independent review is not available for this deliverable. The critical second pass is a challenge to the existing interpretation with prior exposure, not an independent replication. The exploratory analysis and report can therefore be delivered now with these limitations. Two answer-free packets remain optional resources for future validation; they are not a prerequisite for reproducing the representation controls or inspecting the source assessments.

For a future formal annotation study, revise and accept the protocol, complete the applicable annotation gates, and analyze genuinely supported pairs. The present result is already reportable as an exploratory feasibility limitation. A larger incident-narrative study would need its own declared selection method and denominator; it must not replace these five retroactively.

## 7. Reproduction

Use Python 3.11 or later and Git. From a clean checkout, the standard-library command below runs all five test suites, verifies the base-package checksums, regenerates the seven controls, 4,096-case check and two query-fidelity constructions, checks the curated review bindings, and packages the repository and generated results with a SHA-256 manifest.

```text
python scripts/reproduce_study.py
```

Without a corpus path, source verification is explicitly recorded as a reused audit. To recheck the 120 source files, 33 pilot pointers and 22 critical-review passages locally, append `--corpus-root /path/to/AnnoCTR/all --recover-crlf`. To include a rendered report, install ReportLab and append `--pdf`. The output is `outputs/submission/CTI_Evidence_Lab_Submission.zip`; raw report text and private review packets are excluded. See the [submission guide](../docs/SUBMISSION_GUIDE.md) for artifact contents and a short demonstration. Passing checks establish reproducibility and code integrity, not semantic truth or independent review.
