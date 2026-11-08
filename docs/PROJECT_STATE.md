# CTI Evidence Lab — Project State

**Snapshot date:** 6 November 2026  
**Status:** Research design and tooling preparation; no human-locked AnnoCTR annotations or real-report projection results exist.

## Research question

> Across a transparently sampled set of CTI reports, how often does a report explicitly support a temporal relation between two distinct, resolved activity occurrences that share one or more ATT&CK technique mappings, and what occurrence identity or temporal information is retained, partially represented, or lost when those occurrences are projected to a representation that permits only distinct technique pairs?

This remains a candidate empirical question, not an established novelty claim. The primary mapping comparison is intended to use the parent-level `A_120` vocabulary selected by ChronoCTI; exact technique/sub-technique results are a separate sensitivity analysis.

## Data inventory

- Official AnnoCTR archive SHA-256: `118549e9ce885559cd0c07a8de42b321892754cc2e4f07fea0230eaefe4cea35`.
- Archive ZIP integrity passed; all 400 manifest reports have their expected text, full-linking, MITRE-only-linking and TimeML files.
- Official split manifest: 70 train, 16 dev, 34 test, 280 ext. The 120 train/dev/test reports define the GNE+CyNE sampling frame.
- Donor counts in the 120-report frame: Intel471 30, Lab52/S2 Grupo 23, Proofpoint 28, QuoIntelligence 12, ZScaler 27.
- 118/120 have cybersecurity-specific records in the full linking export; 112/120 have at least one valid canonical ATT&CK technique link. These are inventory statistics, not sampling filters.
- Two reports have no observed cybersecurity-specific rows in the inspected full linking export. Their source texts were reviewed and both were dispositioned `INELIGIBLE` for the declared CTI-report scope on 5 November 2026: the Proofpoint row is a sponsored Ponemon survey summary; the QuoIntelligence row is a TIBER-EU framework explainer. Both remain in the historical 120-row inventory. The successor frame records the reasons; this decision is about document genre/scope, not missing CyNE/ATT&CK links.
- Across all 400 TimeML files: 3,324 TIMEX3 tags and zero EVENT, MAKEINSTANCE, TLINK or SIGNAL tags.
- The raw AnnoCTR corpus and full report text are intentionally not committed. The repository contains only the report-level metadata inventory, aggregate summary, source archive hash and reproducible methodology. Raw data stay local under the corpus licence/provenance constraints.

## Sampling and candidate status

- The five rank-1 candidates remain feasibility candidates, one per donor. They are not selected/frozen reports. Two other no-CyNE documents have been excluded from the declared CTI-report source scope but remain in the historical inventory.
- Their five canonical publisher URLs and publication dates were cross-checked against official publisher pages on 5 November 2026. A written response from the AnnoCTR dataset maintainer was also received on 5 November: he stated that source-material licences had been checked and permit redistribution under the dataset licence, and that annotations/adaptations may be published under the same CC BY-SA licence. This supports local research use and derivative publication for the five AnnoCTR candidates, subject to attribution and ShareAlike. The response was qualified by the maintainer's recollection and did not enumerate per-report exceptions; it is not legal advice. The five reports remain candidates, not formally selected; researcher/source-scope eligibility remains 0/5.
- The 5 November 2026 primary-source rights scan found publisher-site terms that appeared restrictive or did not independently establish article reuse rights. On the same date, the AnnoCTR dataset maintainer clarified in writing that source-material licences had been checked and allow redistribution under the dataset licence, and that annotations/changes and derivative works may be published under the same CC BY-SA licence. The working local-use and derivative-publication fields for the five rank-one candidates are therefore PERMITTED, subject to attribution and ShareAlike. The response is qualified, does not enumerate exceptions and is not legal advice. Keep raw reports and extended excerpts out of Git; do not treat the MIT software licence as applying to source-derived annotation material. See `research/rights/AnnoCTR_Research_Use_Permission_Clarification_v0.1.md`.
- Source-first feasibility reviewer drafts are now recorded for all five fixed rank-1 reports: Intel471 Groove/Babuk, Lab52 TokyoX Part 2, Proofpoint Privacy Tools, QuoIntelligence Winnti, and Zscaler Netwire RAT (see `research/feasibility/`). These are working source reviews only. They do not alter the 120-row frame, make researcher eligibility or rights decisions, create human-locked annotations, or contribute event/edge/projection results.
- The Zscaler source supports one candidate resolved email-send occurrence with a source-reported timestamp; its later malware chain remains conditional sample behaviour. The other four reports currently provide broad/generic behaviour, sample capabilities, or multi-context reporting without a resolved pair of attack-event leaves. These are source-review observations, not formal annotation outcomes.
- Rank-one candidate eligibility decisions: 0/5. The two no-CyNE genre/scope dispositions are recorded separately. Working rules for evidence scope, mapping acceptance, prior exposure and candidate-pair negatives are adopted in Decision Register v0.2 and incorporated into Protocol v0.5-draft. Human-locked annotations: 0.
- The five-report batch is for feasibility/protocol debugging only; it cannot estimate vendor or corpus prevalence.
- Do not replace a candidate because it lacks two resolved event leaves, a same-technique pair opportunity or a positive temporal relation. Replacement is allowed only for predeclared source identity, scope, completeness, provenance/rights or practical local-use failure.
- The old event-enumerability gate in the sample-adequacy audit is superseded.

## Protocol and schema versions

- Recovered protocol: `CTI_Event_Instance_Annotation_Protocol_v0.4-draft.md`. It is a draft, not a frozen researcher-approved protocol.
- Exact protocol v0.4.1 was not recovered.
- Original `CTI_Annotation_Schema_v0.4.2-draft.zip` was not recovered. Its conformance audit is available.
- `research/protocol/CTI_Event_Instance_Annotation_Protocol_v0.5-draft.md` is a new working draft that consolidates adopted pilot controls from the recovered v0.4 draft and the decision register. It does not claim to recover Protocol v0.4.1 and is not frozen.
- `research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/` is a newly reconstructed replacement design based on the recovered v0.4 draft, migration note, v0.4.2 audit and v0.3 templates. It is explicitly **not** the original v0.4.2 and is not approved for formal annotation.
- The RECON package has 12 blank registers, a field dictionary, controlled vocabularies, validator, projection module, adapter and synthetic tests. The exact original schema headers may differ.

## Implementation verification

- Latest executable-code verification on 8 November 2026: GitHub Actions run [#183](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/42430969469) passed on documentation head `31793084ae028594035376dcb01adf0f1c695ad9`, with executable sources unchanged from code commit `fcf0bb11009e45cc861eafb457373ee8f00c47c6`. It ran 60 root tests, 73 RECON v0.1 tests, 78 RECON v0.2 tests and 15 RECON v0.3 tests: **226 successful synthetic test executions**. All workflow steps passed, including checksum verification, synthetic projection/validator suites, blank-bundle validation, temporal-evidence validation, selected-final partition validation, explicit comparison-scope extension validation, scope-numerator/denominator parity regressions and all five Mobile ATT&CK non-primary retention cases. The subsequent changes are documentation-only. The 5 November run #144/198-test result remains historical.
- Internal SHA256SUMS checks: 31/31 entries matched.
- Blank-bundle validation returns zero errors and an `EMPTY_ANNOTATION_BUNDLE` warning; it validates package structure only, not research annotations.
- The RECON code has not been run on human annotations or real AnnoCTR event graphs. The validator flags report-level eligibility/local-use/assessability conflicts across annotator/pass partitions and excludes conflicting reports from denominator summaries until adjudicated. It also validates prior-exposure values, requires normalized evidence-linked time records at both endpoints of `direct_timestamp`, rejects duplicate/contradictory direct temporal-pair claims, checks positive candidate assessments against their linked relation, and requires top-level exact techniques to map to themselves. The validator now checks accepted exact IDs and sub-technique parents against the pinned v12.1 crosswalk. The validator's synthetic checks do not establish semantic annotation correctness. A regression test also confirms that the five Mobile ATT&CK IDs observed in the frame (`T1437`, `T1509`, `T1623.001`, `T1629`, `T1631.001`) can be retained as rejected non-primary source records with zero accepted A_120 mappings.
- The public v0.3-era CSV schema and root annotation validator remain unchanged. The legacy `src/projection_metrics.py` now also rejects self-event temporal edges; RECON's projection metric separately distinguishes cycle components that contain multiple source edges from those that require multiple edges. These remain synthetic safeguards. RECON is isolated pending protocol/schema approval.

Source text convention: strict UTF-8; an optional leading UTF-8 BOM is removed; CRLF/LF are preserved; no Unicode normalization is applied; `source_text_sha256` is SHA-256 over the UTF-8 bytes of the exact decoded annotation text; offsets are zero-based, end-exclusive Python Unicode code-point indices. On 4 November 2026, all 120 `source_text_sha256` values in the frame were independently recomputed from the official AnnoCTR repository text files at pinned commit `d510b6949e1938d47c93a43eedd562dc538439dc` and matched 120/120. This verifies the frame hashes against that source revision; it does not recompute the separate downloaded-archive SHA-256. `scripts/hash_annoctr_sources.py` reproduces the check against a local `AnnoCTR/all` directory and can update the frame only with explicit `--write`. Raw report text remains outside this repository.

## Adopted working defaults and remaining research decisions

- Pair opportunity and positive within-technique temporal-relation incidence are separate measures.
- **Adopted working temporal estimand (4 November 2026):** broad within-technique temporal incidence includes directly supported `BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` relations between distinct resolved atomic event leaves, with relation-specific evidence, recorded evidence scope and compatible comparison scope. Strict cycle analysis uses only normalized `BEFORE`/`AFTER`.
- **Adopted working mapping level (4 November 2026):** parent-level `A_120` is the primary analysis vocabulary; exact technique/sub-technique `A_exact` is a separate sensitivity view. Enterprise ATT&CK v12.1 is the working exact-to-parent crosswalk release because it matches ChronoCTI's published version. The 737-row crosswalk is generated, committed and checked by the RECON validator. Revoked/deprecated exact IDs remain visible but are excluded from primary A_120 unless separately resolved.
- **Adopted project default (4 November 2026):** primary report-level rates use `N_assessable`; assessability coverage is `N_assessable / N_eligible`. `N_eligible` requires source/scope eligibility and local-use permission. `N_assessable` additionally requires a complete/readable frozen source, `report_assessability=ASSESSABLE`, and at least one completed eligible human full-report review partition, with report-level conflicts resolved. Count each report once. If multiple annotators or passes exist, calculate report-level outcomes from the designated locked final annotation or agreed/adjudicated consensus partition, not by summing partitions. A fully reviewed assessable report with zero resolved event leaves remains a zero outcome; `NOT_ASSESSABLE`, `PENDING`, incomplete review and unresolved conflicts are disclosed separately and are not recoded as zero. Public-reuse permission is tracked separately.
- The researcher decision register is in `research/metric_contract/CTI_Evidence_Lab_Researcher_Decision_Register_v0.2.md`.

## Literature boundary — refreshed 5 November 2026

The recent-work comparison now explicitly includes APTIE (Scientific Data, 25 May 2026), the cybersecurity event-extraction survey by Yang et al. (IET Communications, first published 21 July 2026), and SMAH-CTI (Findings of EMNLP 2026). APTIE separates semantic entity-relation labels from its event-extraction module; SMAH-CTI provides sentence-level relevance, NER, ATT&CK mapping and grounded procedure descriptions, not event-event temporal links. The survey describes cybersecurity event relation extraction as underdeveloped and reports no unified, widely adopted public benchmark. ChronoCTI remains direct prior art for temporal relations over ATT&CK technique pairs. The project's candidate contribution must therefore be limited to source-grounded report-local occurrence identity, event-to-event temporal evidence and the effects of projection to distinct technique pairs. Novelty remains unproven. See research/RELATED_WORK_MATRIX.md and the 5 November addendum in docs/RESEARCH_GAP_AUDIT_2026-11-01.md.

## ChronoCTI baseline

The current audit is a workbook and selected source-code control-flow audit, not a full feature-table rebuild or model re-training. Preserve raw `NEXT`; any conversion to a BEFORE-like interpretation is a separate hypothesis. ChronoCTI's paper identifies Enterprise ATT&CK v12.1 (Section 4.1) and describes the 120-technique pair task with diagonal pairs excluded (Section 4.5.1). The selected 120 IDs are pinned to ChronoCTI's `selected_techniquesWName.json`; the derived identifier-only list is included in RECON with provenance/hash. We have not run ChronoCTI's learned model on AnnoCTR; our proposed analysis measures source-grounded annotations under a named projection, not ChronoCTI's measured errors on AnnoCTR.

## Current blockers / next sequence

1. **Complete — source-scope dispositions.** The two no-CyNE documents are recorded `INELIGIBLE` for the declared CTI-report scope; both remain in the historical 120-row frame. The reasons are genre/content, not absent ATT&CK labels.
2. **Permission clarification received — working permission gate cleared.** The AnnoCTR README names the dataset maintainer contact and states that the corpus folder is CC BY-SA 4.0; the licence only grants rights the licensor has authority to license. A precise clarification checklist is recorded at research/rights/AnnoCTR_Research_Use_Permission_Clarification_v0.1.md. The 5 November written maintainer response supports local report annotation and publication of derivative works under the AnnoCTR CC BY-SA licence. The five rank-one candidate rows now record local research use and derivative public reuse as PERMITTED, subject to attribution/ShareAlike and the stated qualification. Source-scope eligibility and formal researcher selection remain pending.
3. **Complete — working annotation controls adopted.** Evidence scope, mapping acceptance/alternatives, prior-exposure coding and candidate-pair negative rules are recorded in Decision Register v0.2 and Protocol v0.5-draft.
4. **Complete — primary event-universe working decision (8 November 2026).** Use incident-linked attack-action occurrences as the primary ChronoCTI-comparable stratum, with a medium-neutral rule that includes induced user/system actions where they form part of the attack chain. Keep actor communications, analyst/sample observations, generic capabilities and other non-primary activity in separate descriptive strata. The decision is recorded in Decision Register v0.2 and event-universe note v0.2; no individual candidate labels are approved.
5. **New schema blocker — activity stratum.** RECON v0.1/v0.2/v0.3 has no canonical activity_stratum field. Add it, its controlled vocabulary, and validator/projection rules in a newly versioned schema. Primary pair denominators and projections must use attack-action endpoints only; non-primary strata remain separately reportable. Do not annotate or freeze using the draft CSV column as a substitute.
6. Resolve the primary comparison-scope rule, non-strict timestamp-label semantics, alternative-group lifecycle, and whether scope-assignment adjudication is needed for a second annotator. Approve or revise the proposed pilot deferrals for episode-to-episode relations and record-level ChronoCTI pair alignment. Then issue a newly versioned schema package with updated tests, manifest and checksums. Do not relabel RECON v0.1 as the original v0.4.2.
7. Begin the first source-first human feasibility annotation only after all protocol/schema decisions are reconciled and the package is approved/frozen. Do not replace candidates because of event yield or absence of positive relations.
8. Add a second human annotator for an overlapping subset if available; otherwise report that IAA was not measured.

## Research integrity status

No human annotations, real-report projection results, prevalence estimates, IAA measurements, validated novelty claim or publication-ready result currently exist. Synthetic test success establishes only code-path behavior on synthetic fixtures.

## Update — 4 November 2026

Enterprise ATT&CK v12.1 is the selected working crosswalk release under delegated project direction on 4 November 2026 because it matches the version identified by the ChronoCTI version-of-record paper in Section 4.1. A non-freezing preflight against the official versioned v12.1 STIX bundle (Git blob SHA-1 `7a99efb3a8c89b06dd9db1a9a17e4201160ac4ee`; retrieved-file SHA-256 `e84679af4bc46bba2ba92f60182101f146d5b966898e47924de7321e6bffeaa1`) found 737 attack-pattern objects: 333 top-level techniques and 404 sub-techniques with 404 explicit, valid parent relationships. All 120 ChronoCTI `A_120` IDs were present exactly once as top-level techniques; none were missing, duplicated, sub-techniques, revoked or deprecated. The separate v14.1 inspection remains a non-primary compatibility preflight only. The generated v12.1 crosswalk is committed at `research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/vocabulary/A_120_Exact_to_Parent_Crosswalk_v0.1.csv` (SHA-256 `f449ff8bd1551b6d6656d2f25a82b7c55a0b134bbecd4215f0f10330ec85be29`). Its manifest pins source Git blob SHA-1 `7a99efb3a8c89b06dd9db1a9a17e4201160ac4ee` and retrieved-byte SHA-256 `e84679af4bc46bba2ba92f60182101f146d5b966898e47924de7321e6bffeaa1`. The validator and synthetic regression tests use this crosswalk; current CI is the acceptance check.

## Repository checkpoint — 3 November 2026

The current project artifacts are version-controlled on `main`: the text-free 400-report AnnoCTR screening inventory and summary, the 120-row multi-vendor frame, Sampling Method v0.3.2, the five-report source re-audit, the provisional metric contract and decision register, and the separate RECON v0.1 schema reconstruction. The original public v0.3 implementation remains unchanged.

Independent verification on the frozen AnnoCTR archive reproduced the screening CSV byte-for-byte (400 rows; SHA-256 `9691ef5cbd9f5e83a0c6337bf2470f232f342377b745596499cfe62d9ae50c79`). The official archive hash matched the recorded value. The 120-row frame was checked against the fixed seed, all 120 source-text hashes were matched against the local corpus, and donor counts and within-vendor ranks were consistent.

The current checked code state passed 33 root tests and 40 RECON synthetic tests; the toy projection demo ran and Python compilation passed. GitHub Actions run #41693198880 passed the root suite, sampling-frame checks, RECON checksums, RECON tests, and blank-bundle validation. The RECON checksum manifest contains 29 package entries and all 29 match. These are reproducibility and synthetic-code checks only; no human source annotation or real-report projection result exists.

`docs/PROJECT_STATUS.md` is a historical 1 November snapshot. This file is the current project-state record. The project-wide audit v1.4 below has a 3 November repository-synchronization addendum clarifying which earlier statements described the pre-sync state.



## Update — 5 November 2026: AnnoCTR maintainer clarification

The dataset maintainer replied in writing that, to the best of his recollection, the source-material licences had been checked and allow redistribution under the dataset licence. He also stated that researchers may add annotations or change reports and may publish derivative works provided they remain under the same CC BY-SA licence. The response was qualified (“if I remember correctly”) and was expressly not legal advice. The project records the five fixed rank-one AnnoCTR candidates as permitted for local research use and derivative publication under CC BY-SA 4.0, with attribution and ShareAlike. The response did not provide a report-by-report exception list. Raw corpus files and extended verbatim excerpts remain excluded from Git. The MIT licence applies to project software, not source reports or adapted annotation material.

This clarification does not select the five reports, resolve the two source-scope dispositions, approve/freeze the reconstructed schema, produce human annotations, or create real-report projection results. Those gates remain open.


## Update — 5 November 2026: candidate-pair validation gate

The RECON validator now requires both endpoints of a candidate-pair assessment to be distinct, resolved atomic `event_leaf` units. Unresolved units and series/episode/aggregate containers cannot be assessed as event pairs. A synthetic regression test covers this condition. The change is implemented in RECON v0.1 and its data-model documentation, package manifest, QA record and SHA256SUMS file. It does not establish semantic correctness of any report annotation.

The updated package has 68 synthetic tests (41 validator, 16 projection, 11 adapter) and 31/31 package checksum entries. GitHub Actions run #41998772656 passed on commit `e0237e9bae2538d42936f888e414cac0ddad3809`. The five-rank-one Intel471 pilot starter now points to the actual rank-one Groove/Babuk report in the 120-row frame; the source pass remains explicitly AI-exposed. No candidate eligibility decision, human annotation or real-report projection has been created by these changes.

## Update — 5 November 2026: source-scope and annotation controls

Two no-CyNE documents have been formally dispositioned `INELIGIBLE` for the declared CTI-report scope on genre/content grounds and retained in the historical 120-report inventory. The successor frame v1.0 records both decisions and their reasons. The remaining 118 frame records are not automatically eligible.

The working evidence-scope, mapping-acceptance, prior-exposure and candidate-pair assessment rules have been adopted and consolidated into `research/protocol/CTI_Event_Instance_Annotation_Protocol_v0.5-draft.md`, with a decision log in `research/metric_contract/CTI_Evidence_Lab_Researcher_Decision_Register_v0.2.md`. The five rank-one candidates remain unselected; their source-scope/researcher eligibility decisions are pending (0/5), human-locked annotations are 0, and RECON v0.1 remains an unapproved schema reconstruction.


## Update — 5 November 2026: protocol/schema reconciliation

The RECON v0.1 validator now requires the exact frozen source text to be supplied and checked before a completed report partition enters `N_assessable`. It also validates alternative-mapping group structure and requires reasons for `NO_TEMPORAL_CLAIM`, `VAGUE_OR_AMBIGUOUS` and `NOT_ASSESSABLE` pair assessments. Synthetic coverage now stands at 67 RECON tests (40 validator, 16 projection, 11 adapter), with 31/31 package checksums verified. CI run #41998301083 passed on commit `514056fa3f2e784d827c4246b8350088a5956bdb`. The protocol/schema reconciliation register is `research/protocol/PROTOCOL_SCHEMA_RECONCILIATION_v0.1.md`. Episode-level relation storage, final-partition designation, temporal evidence roles, baseline-pair alignment and some report-level metrics remain unresolved; RECON is not ready to freeze.


## Update — 5 November 2026: mapping and candidate-pair validation

The RECON validator now requires a human rationale in `mapping_notes` for every accepted `source_supported_analyst_candidate` mapping, alongside the mapping-specific evidence link. Alternative mapping groups must be explicitly identified, contain at least two rows for one activity unit, and keep any `alternative_to_mapping_id` reference within the group. Candidate-pair assessments with `NO_TEMPORAL_CLAIM`, `VAGUE_OR_AMBIGUOUS`, or `NOT_ASSESSABLE` must include a reason. CI run #41998772656 passed on commit `e0237e9bae2538d42936f888e414cac0ddad3809`: 68 RECON synthetic tests (41 validator, 16 projection, 11 adapter), 31/31 checksums, projection demo and blank-bundle validation. These remain synthetic checks only. The protocol/schema reconciliation register tracks the remaining design decisions; no human annotation or real-report projection has been produced.


## Update — 5 November 2026: selected-final report-level aggregation

The RECON v0.2 package now includes `analysis/report_level_aggregation.py`, which consumes the selected-partition projection adapter and produces report-level outcomes without summing annotator/pass partitions. It separately reports `N_eligible`, `N_assessable`, assessability coverage (`N_assessable / N_eligible`), selected-final projection coverage, event-leaf and pair-opportunity outcomes, positive temporal-relation outcomes, within-technique temporal-relation outcomes, mapping coverage, and projection-loss diagnostics. Pending, ineligible, unreviewed, source-unverified and report-level-conflict cases remain visible with IDs/reasons. A fully reviewed, source-verified report with zero resolved event leaves remains in `N_assessable`.

Primary report-level rates are withheld unless every `N_assessable` report has a valid selected-final projection. The compatible event-pair opportunity measure currently uses a provisional nearest-common-resolved-non-report-aggregate scope rule. A further review identified that this includes campaign/operation ancestors above distinct incident nodes. Candidate resolutions are an incident-bounded rule or an explicit per-event comparison-scope assignment; the chosen scope must also align temporal-edge eligibility and the conditional-rate numerator/denominator. Neither candidate is approved, and pair-opportunity rates remain withheld. The aggregator does not adjudicate semantic event identity, scope meaning, temporal entailment, mapping correctness or reviewer independence.

End-to-end synthetic fixtures exercise source verification, analysis-lock creation, selected-final validation, projection, aggregation, denominator coverage, missing-final withholding and the scope-rule approval gate. The selection register in the real package remains header-only. No human annotations, selected final partitions, real-report projections, empirical rates or IAA measurements exist. The aggregation tests remain synthetic checks, not research findings.


## Update — 5 November 2026: metric-contract coverage expanded

The report-level aggregator now covers additional contract outputs: per-report registry status/reasons, mention-state counts, activity-unit counts by granularity/role/instance status, count-status-by-granularity, temporal relation counts by label and basis, optional candidate-pair label counts, separate `A_exact` and `A_120` mapping coverage, occurrence compression by technique, and per-report collision/cycle provenance. Excess edge multiplicity is counted only for collisions in the retained distinct-technique-pair graph. Conditional within-technique-temporal-relation given same-technique opportunity is withheld until the scope-pair opportunity rule is approved. The CLI entry point is now covered by a synthetic blank-package test and never writes source text into output JSON.


## Latest technical remediation — 5 November 2026

This checkpoint records the technical remediation completed before the later source-integrity and protocol-reconciliation updates below.

The annotation workflow now blocks selected-final projection when report-level source eligibility, local-use permission or assessability conflicts across passes. Consensus selection requires two distinct completed independent input partitions; an adjudicated-final selection must reference an actual adjudicated record in the selected report/annotator/pass. The standalone v0.1 adapter applies the same report-conflict stop.

Projection safeguards now reject self-event edges in the legacy root API and report separately (a) cycle components containing multiple source event edges and (b) cycle components that require multiple source edges. The AnnoCTR source-hash utility and its test use the canonical v1.0 frame; old v0.3 annotation templates/protocol are explicitly marked historical.

**At this checkpoint, CI run #144 passed:** 57 root tests, 69 RECON v0.1 tests (41 validator, 16 projection, 12 adapter), and 72 RECON v0.2 tests; 198 successful test executions. All 31 v0.1 package checksums and the workflow's validation steps passed.

Research readiness is unchanged: the five rank-one reports remain candidates, researcher eligibility is 0/5, human-locked annotations are 0, IAA is not measured, real-report projections are 0, and novelty is not established. The protocol and reconstructed schema remain drafts, not approved/frozen for formal annotation.


## Update — 5 November 2026: frozen-source validation and protocol/schema alignment

The legacy root annotation validator now reads report text through the shared frozen-source reader. This preserves CRLF/LF line endings, removes only the optional leading UTF-8 BOM, and uses the shared canonical SHA-256 function. Its report-row adapter preserves `mention_text` and `evidence_text` exactly instead of trimming evidence-span boundary whitespace. Two regression tests cover CRLF/hash preservation in the CLI and exact source-span matching with leading/trailing whitespace.

The legacy annotation validator now preserves frozen-source line endings and evidence-span whitespace. The report-level conditional metric now explicitly intersects reports with both same-technique pair opportunity and a within-technique temporal relation, and emits its numerator/denominator. Regression tests cover the cross-incident scope-pair behaviour and conditional-rate subset logic.

**Current-head verification:** GitHub Actions run [#159](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/42069718811) passed on `fbcb62ac20dd340566990ad738b1a05f9ec93fdb`: 57 root tests, 69 RECON v0.1 tests, 75 RECON v0.2 tests, and 10 RECON v0.3 tests (211 total); all workflow steps passed, including v0.3 assignment/lock tests and blank-register validation. Current main is CI-verified. These are synthetic/code-integrity checks only, not human-annotation results.

Protocol v0.5-draft Section 4.3 now represents the relation cue through `temporal_relations.primary_evidence_span_id`, stores exact source text/offsets once in `evidence_spans`, and links Event A, Event B and contextual support through the RECON v0.2 temporal-evidence extension. The v0.1 reconciliation register now distinguishes the v0.1 limitation from the additive v0.2 implementation. The report-level aggregator is implemented and synthetically tested; rates dependent on the provisional scope-pair opportunity rule remain withheld pending approval. The current broad common-ancestor implementation's cross-incident behavior and the recommended incident-bounded primary alternative are documented in the v0.2 aggregation rule note and researcher decision register; a synthetic regression test now makes the current cross-incident inclusion explicit.

The protocol now proposes deferring episode-to-episode temporal relation records and record-level ChronoCTI pair-to-event alignment from the initial pilot. These are **proposals requiring researcher approval**, not adopted decisions. Episode containers remain represented separately; raw benchmark pair labels/provenance remain in the separate baseline materials. Neither is to be improvised into the atomic temporal relation register.

Research readiness is unchanged: human-locked annotations 0, selected final partitions 0, real-report projections 0, IAA not measured, and novelty not established. Protocol v0.5 and RECON v0.1/v0.2/v0.3 remain drafts pending researcher approval and freeze.


## Update — 5 November 2026: scope-comparability validator parity

The RECON v0.1 validator and v0.2 report-level opportunity counter now call the same resolved-scope ancestry helper. A primary direct-positive temporal relation and a compatible candidate-pair assessment must identify a shared RESOLVED, non-REPORT_AGGREGATE ancestor from the same provisional comparison-type set used by pair-opportunity counting. Regression coverage rejects a report aggregate used as the comparison scope even when both endpoints descend from it. The opportunity counter still selects the nearest eligible common ancestor and counts each event pair once; a relation may identify any shared eligible ancestor. This closes a structural numerator/denominator eligibility gap but does not decide whether broad campaign, operation, victim-organisation, host or other scopes are scientifically appropriate. The incident-bounded and explicit per-event comparison-scope alternatives remain open; pair-opportunity and conditional rates remain withheld pending researcher approval. No annotations or empirical results were created by this change.


## Update — 5 November 2026: RECON v0.3 comparison-scope assignment candidate

An additive RECON v0.3 draft now implements an explicit event-to-comparison-scope assignment candidate without changing the v0.1 reconstruction or v0.2 temporal-evidence package. The new assignment register permits one event to be considered against multiple scopes, records ASSIGNED or UNCERTAIN decisions, requires source evidence and a rationale for affirmative assignments, and never treats a missing row as a negative. The assigned comparison scope must be a shared resolved non-report ancestor of the event's existing scope.

The v0.2 aggregator now evaluates three named rules: the existing nearest-common-resolved-non-report rule, a shared-resolved-INCIDENT sensitivity rule, and the v0.3 explicit-assignment rule. Under the explicit rule, both event endpoints must have ASSIGNED rows for the same scope; positive temporal relations and compatible candidate-pair assessments are restricted to that same assigned-scope universe. A separate v0.3 lock binds assignment rows to the v0.2 selected-analysis lock, and the v0.3 aggregation wrapper requires explicit confirmation of both lock layers.

This is a draft technical candidate, not a researcher-approved scope definition. The assignment and lock registers are header-only; no human assignment, annotation, selected final partition, real-report projection, IAA result, or empirical rate was created. CI run #159 passed all 211 synthetic test executions and the blank v0.3 assignment/lock validation. The next gate is researcher review of the three scope rules and approval of the protocol/schema before any annotation workflow adopts one.


## Update — 6 November 2026: RECON v0.3 completeness and lock audit

A critical gap was found in the initial explicit comparison-scope extension: missing assignment rows could be treated as no pair opportunity even though they might simply be unreviewed. RECON v0.3 now requires one explicit decision for every eligible RESOLVED non-report ancestor scope of every resolved atomic event leaf. Decision states are ASSIGNED, NOT_ASSIGNED and UNCERTAIN. ASSIGNED/NOT_ASSIGNED require an evidence span and rationale; UNCERTAIN remains non-qualifying. Missing decisions block validation. The v0.2 opportunity counter continues to count a pair only when both endpoints have ASSIGNED rows for the same shared scope.

The v0.3 validator now delegates structural validation to RECON v0.1 and can accept frozen source texts for source-span validation. The v0.3 lock builder and verifier validate the v0.2 selected-final register and the complete assignment review before creating or accepting locks. The lock path reports unsupported final roles before returning other register errors; the creator CLI also passes any supplied frozen source texts into the source-span validator. A further safeguard blocks CONSENSUS and ADJUDICATED_FINAL roles: the existing v0.1 adjudication log cannot target v0.3 assignment rows. The current draft therefore supports SINGLE_ANNOTATOR_FINAL only, pending design of a dedicated scope-assignment adjudication register. This boundary is explicit and must be resolved before a multi-annotator final annotation workflow uses v0.3.

No human assignments or annotations were created. The rule is still a researcher decision, not a frozen scientific choice. CI run #167 passed on the current main head: 57 root tests, 69 RECON v0.1, 76 RECON v0.2 and 15 RECON v0.3 tests (217 successful synthetic executions). This includes the explicit NOT_ASSIGNED opportunity check and the v0.3 role guard. All workflow steps passed. These remain synthetic/code-integrity tests only.

## Update — 6 November 2026: five-report source-first pre-annotation draft

A structured pre-annotation draft has been added under `research/annotation_drafts/AnnoCTR_Pilot_v0.1/` for the five fixed rank-one AnnoCTR candidates, preserving the predeclared vendor order (Intel471, Lab52, Proofpoint, QuoIntelligence, Zscaler). The package contains five report assessments, nine proposed scopes, 18 candidate activity units, 26 source-anchor offsets, five mapping triage records, four source-ID/label discrepancy records, and five temporal triage records.

All 26 source anchors were matched uniquely against the pinned AnnoCTR text revision `d510b6949e1938d47c93a43eedd562dc538439dc`. Offsets are zero-based, end-exclusive Unicode code-point positions. A cross-file check found no broken anchor-to-unit, parent-unit, or unit-to-scope references; source hashes on anchor rows agree with the report assessment rows. The source text and extended report excerpts are not copied into Git.

The draft recommends source-scope eligibility for all five reports but leaves all five researcher decisions pending. It proposes one possible atomic primary event leaf (the specifically timestamped Zscaler phishing email), with human review still required. It proposes no positive primary temporal relation and accepts no event-level ATT&CK mapping. It flags (a) the Zscaler campaign description beginning in July 2021 versus one email dated 30 June 2021 10:44 PKT, and (b) four source-level ATT&CK ID/label discrepancies against the pinned Enterprise ATT&CK v12.1 crosswalk. Those discrepancies are recorded, not silently corrected.

This is a source-review/pre-annotation artifact, not a canonical annotation partition, human annotation, adjudication, projection, or empirical result. The project's human annotation count remains 0; selected final partitions 0; real-report projections 0; IAA not measured; empirical findings none. The user's prior exposure remains `AI_EXPOSED` as already specified in the project decision record.

The latest executable-code CI run remains [#168](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/42164908914), which passed 217 synthetic test executions on code commit `9c11e146bb06acd15f92c9e19562052d38d5239b`. The subsequent annotation-draft commits modify only Markdown/CSV research materials; no new projection-test workflow was triggered for them.


## Update — 6 November 2026: scope-rule numerator/denominator parity

A targeted selected-final integration test found that the v0.2 aggregator could count a positive relation at a broad campaign scope while evaluating pair opportunity under the incident-bounded rule, which excludes cross-incident pairs. The aggregator now filters primary relations to the selected incident universe when the incident-bounded rule is used: a positive relation recorded only at a broader campaign/operation scope cannot enter the numerator if its endpoints have no shared resolved INCIDENT ancestor. Under the legacy rule, the protocol continues to permit a relation to cite any shared eligible ancestor for an event pair whose nearest shared eligible ancestor establishes pair opportunity. The explicit v0.3 rule continues to require the same comparison scope to be ASSIGNED to both endpoints. A synthetic integration test reproduces the incident-bounded mismatch, and another protects the documented legacy behaviour.

This is a technical parity correction; all three scope rules remain researcher-review candidates and none is approved. GitHub Actions run #177 passed all 226 synthetic tests on commit `ec29f371`, including the two new integration tests and the scope-numerator/denominator parity correction. The correction is therefore CI-verified, but it does not approve any scope rule or establish empirical results. No annotations or real-report measurements were created.


## Update — 8 November 2026: primary event-universe decision

The primary analytical stratum is now defined as incident-linked attack-action occurrences: concrete report-local actions that conduct, enable or complete a specific cyberattack. This is medium-neutral and not attacker-only: it can include phishing delivery and induced user execution. Threat-actor communications/platform events, analyst/sample observations, generic capabilities and other non-primary activity remain in separate descriptive strata. Classification is independent of ATT&CK mapping, and the fixed five-report feasibility set is not changed because of event yield.

This decision follows ChronoCTI's published target and source-selection criteria, while avoiding an overly narrow victim-side/attacker-only restriction. The Intel471 post/blog pair remains a separate communication-relation candidate; it is not promoted to an attack-action chronology. The specifically dated Zscaler phishing email remains a candidate primary attack-action unit, pending human review. No primary positive temporal relation is currently proposed in the five-report pre-annotation drafts; this is a feasibility-draft observation, not an empirical finding.

A schema gap was identified: RECON v0.1/v0.2/v0.3 does not store analytical stratum on activity units. The next schema version must add a controlled activity_stratum field and validation/projection rules for primary, auxiliary and mixed-stratum relations. The v0.2 decision note and protocol draft record the rule; the reconciliation register records the field as a freeze blocker. Human-locked annotations remain 0, selected final partitions 0, real-report projections 0, IAA not measured and empirical findings none.
