# Occurrence identity in technique-level CTI graphs

## An exploratory feasibility study

**CTI Evidence Lab · Sanket Nichit · 17 November 2026**

**Status:** Research draft. Source review is not independently validated. The representation experiments use synthetic inputs. This is not a completed gold-annotation or prevalence study.

## Abstract

Cyber threat reports mix incident descriptions, campaign summaries, malware capabilities and analyst observations. Representing these statements with ATT&CK technique nodes can obscure the distinction between a behavior category and a particular occurrence. This study examines the prerequisites for measuring that loss. It combines an exploratory reading of five fixed AnnoCTR reports, source-integrity checks against a 120-report frame, and seven deterministic representation controls. All 120 source hashes were reproduced after an explicitly verified line-ending recovery, and 33 pilot evidence pointers passed structural checks. The exploratory reading retains one identifiable attack-occurrence candidate but does not establish a qualifying same-technique temporal pair. Synthetic controls show that distinct-pair projection can omit relations, that self-loops do not preserve occurrence identity, and that projected cycles have more than one cause. These findings support a bounded feasibility study, not a population estimate or a claim of improved extraction accuracy.

## 1. Question and contribution

The question is: **what occurrence identity and temporal information can a distinct-technique-pair graph retain from source-supported attack occurrences?** Two issues must be separated. The mathematical behavior of a specified projection can be tested directly. The frequency and importance of its effects in CTI reports require source-backed annotations and an appropriate sample.

The present deliverable provides reproducible controls, a traceable exploratory source assessment and an independent-review packet. It does not introduce event graphs, claim new ATT&CK extraction methods, train a model, or establish novelty.

## 2. Closest methodological context

ChronoCTI already extracts temporal attack patterns and represents attack actions using ATT&CK techniques. Its paper specifies ATT&CK v12.1. It is a direct motivation for examining technique-level representations, not evidence that this project's annotations or predictions are correct. Our deterministic projection is not a run of ChronoCTI's learned pipeline. See [Rahman et al., 2025](https://link.springer.com/article/10.1007/s10115-025-02491-6).

AnnoCTR provides document-level entity, temporal-expression and cybersecurity concept annotations. Those resources support source retrieval and technique-link inspection; they do not make our proposed occurrence-pair labels gold. See [Lange et al., 2024](https://aclanthology.org/2024.lrec-main.103/).

MATRES demonstrates the importance of defining temporal annotation units carefully, including event axes and start points. Its general-domain scheme is relevant precedent, not a directly interchangeable CTI codebook. See [Ning et al., 2018](https://aclanthology.org/P18-1122/). The broader [related-work matrix](RELATED_WORK_MATRIX.md) remains a working literature map; a complete novelty assessment is still open.

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

This pass identifies one candidate attack occurrence and no established qualifying within-technique pair. The count describes this exploratory interpretation, not an exhaustive validated inventory. In particular, Proofpoint's reported observations are stronger than a mere capability list; rejecting its atomicity without explaining that distinction would lose useful evidence. Zscaler also reports observed activity, but its text does not resolve the required connection to the named email.

No formal denominator is computed. Pending or unresolved review is not a negative label. The formal annotation registers and selection gates remain unchanged. Full judgments and source bindings are in [the review package](feasibility/exploratory_review_v0.1/README.md).

## 5. Representation experiment

Let M(u) and M(v) be the accepted technique sets for two distinct occurrences. The mapping combinations are M(u) × M(v). The primary projection discards diagonal combinations (t,t); the loop-permitting control retains them. The occurrence-preserving control keeps the original event endpoints and relation labels.

For nonempty mapping sets, an edge is fully omitted exactly when both sets contain the same single technique. To see this, if every cross-product pair is diagonal, every member of either set must equal every member of the other. If at least one diagonal and one distinct pair exist, the edge is partially represented. If either endpoint is unmapped, the edge is classified separately as unmapped, not as diagonal omission.

Seven deterministic controls cover distinct mappings, identical singleton mappings, repeated same-technique actions, mixed mappings, an unmapped endpoint, occurrence collapse causing a cycle, and single-edge mapping fan-out causing a cycle. [Generated tables and full provenance](experiments/representation_controls_v0.1/README.md) are reproduced by the supplied command.

Three results matter. First, two successive same-technique relations vanish in the distinct-pair graph but merge into one loop when loops are allowed: permitting loops does not recover endpoint identity. Second, a missing mapping is not evidence of projection-induced omission. Third, both a two-edge occurrence chain and a single multi-mapped edge can create a technique cycle despite an acyclic source graph. A projected cycle alone therefore does not identify its cause.

These are consequences of defined inputs and mappings. They provide no estimate of their frequency in CTI and no performance comparison with published systems. Exact-sub-technique sensitivity on accepted real annotations remains unrun.

## 6. Limitations and next evidence

The sample is small, the protocol is still a draft, the review was exposed to earlier interpretations, and independent review has not yet been returned. Source extraction can omit image evidence. Conservative incident and atomicity rules may reduce usable coverage; broader campaign-level rules answer a different question. The literature comparison is not a completed novelty review.

Two separate answer-free packets now support independent source review of the same fixed five reports. They collect complete-read status, time, uncertainty, candidate activities, temporal evidence and optional technique mappings. Returned first passes must be preserved before reconciliation. Agreement requires aligned units and an explicit scoring rule; two reviewer names alone are not a reliability measurement.

After calibration, revise and accept the protocol, complete the applicable annotation gates, and analyze any genuinely supported pairs. If independent review still cannot resolve such pairs, report the feasibility limitation. A larger incident-narrative study would need its own declared selection method and denominator; it must not replace these five retroactively.

## 7. Reproduction

Use Python 3.11 or later and the local AnnoCTR corpus. The new analysis uses the standard library only.

```text
python scripts/audit_pilot_sources.py --corpus-root /path/to/AnnoCTR/all --recover-crlf --output research/feasibility/exploratory_review_v0.1/source_integrity.json
python scripts/summarize_exploratory_review.py
python -m examples.representation_controls --output-dir research/experiments/representation_controls_v0.1
python -m unittest discover -s tests -v
python scripts/build_reviewer_packets.py --corpus-root /path/to/AnnoCTR/all --recover-crlf
```

The first command verifies bytes and pointers, the second checks the source binding of curated judgments, and the third reruns synthetic controls. None automates semantic truth or independent review. See [the coordinator guide](reviewer_kit/COORDINATOR.md) for handling returned packets and the repository workflow for all RECON test suites.
