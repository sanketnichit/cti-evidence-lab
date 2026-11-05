# CTI Evidence Lab — Project State

**Snapshot date:** 5 November 2026  
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

- Latest verification on 5 November 2026: GitHub Actions run [#125](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/42049025391) passed on commit `bf504818c7150ff7699a1c2b2a947952f11f79a9`. It ran 55 root tests, 69 RECON v0.1 tests (41 validator, 16 projection, 12 adapter), and 70 RECON v0.2 tests: 194 successful synthetic test executions in total. All 31 RECON v0.1 checksum entries, the projection demo, blank v0.1/v0.2 bundle validations, temporal-evidence tests and selected-final partition validation passed.
- Internal SHA256SUMS checks: 31/31 entries matched.
- Blank-bundle validation returns zero errors and an `EMPTY_ANNOTATION_BUNDLE` warning; it validates package structure only, not research annotations.
- The RECON code has not been run on human annotations or real AnnoCTR event graphs. The validator flags report-level eligibility/local-use/assessability conflicts across annotator/pass partitions and excludes conflicting reports from denominator summaries until adjudicated. It also validates prior-exposure values, requires normalized evidence-linked time records at both endpoints of `direct_timestamp`, rejects duplicate/contradictory direct temporal-pair claims, checks positive candidate assessments against their linked relation, and requires top-level exact techniques to map to themselves. The validator now checks accepted exact IDs and sub-technique parents against the pinned v12.1 crosswalk. The validator's synthetic checks do not establish semantic annotation correctness.
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
4. Reconcile the v0.5 protocol with RECON v0.1, close remaining field/invariant gaps, and issue a newly versioned schema package. Do not relabel RECON v0.1 as the original v0.4.2.
5. Begin the first source-first human feasibility annotation only after that freeze. Do not replace candidates because of event yield or absence of positive relations.
6. Add a second human annotator for an overlapping subset if available; otherwise report that IAA was not measured. AI is not a second annotator.

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

Primary report-level rates are withheld unless every `N_assessable` report has a valid selected-final projection. The compatible event-pair opportunity measure uses a documented provisional nearest-common-resolved-non-report-aggregate scope rule; pair-opportunity rates remain withheld unless that rule is explicitly approved. The aggregator does not adjudicate semantic event identity, scope meaning, temporal entailment, mapping correctness or reviewer independence.

End-to-end synthetic fixtures exercise source verification, analysis-lock creation, selected-final validation, projection, aggregation, denominator coverage, missing-final withholding and the scope-rule approval gate. The selection register in the real package remains header-only. No human annotations, selected final partitions, real-report projections, empirical rates or IAA measurements exist. The aggregation tests remain synthetic checks, not research findings.


## Update — 5 November 2026: metric-contract coverage expanded

The report-level aggregator now covers additional contract outputs: per-report registry status/reasons, mention-state counts, activity-unit counts by granularity/role/instance status, count-status-by-granularity, temporal relation counts by label and basis, optional candidate-pair label counts, separate `A_exact` and `A_120` mapping coverage, occurrence compression by technique, and per-report collision/cycle provenance. Excess edge multiplicity is counted only for collisions in the retained distinct-technique-pair graph. Conditional within-technique-temporal-relation given same-technique opportunity is withheld until the scope-pair opportunity rule is approved. The CLI entry point is now covered by a synthetic blank-package test and never writes source text into output JSON.


## Latest technical remediation — 5 November 2026

The repository's current `main` head is `bf504818c7150ff7699a1c2b2a947952f11f79a9`.

The annotation workflow now blocks selected-final projection when report-level source eligibility, local-use permission or assessability conflicts across passes. Consensus selection requires two distinct completed independent input partitions; an adjudicated-final selection must reference an actual adjudicated record in the selected report/annotator/pass. The standalone v0.1 adapter applies the same report-conflict stop.

Projection safeguards now reject self-event edges in the legacy root API and report separately (a) cycle components containing multiple source event edges and (b) cycle components that require multiple source edges. The AnnoCTR source-hash utility and its test use the canonical v1.0 frame; old v0.3 annotation templates/protocol are explicitly marked historical.

**CI run #125 passed:** 55 root tests, 69 RECON v0.1 tests (41 validator, 16 projection, 12 adapter), and 70 RECON v0.2 tests; 194 successful test executions. All 31 v0.1 package checksums and the workflow's validation steps passed.

Research readiness is unchanged: the five rank-one reports remain candidates, researcher eligibility is 0/5, human-locked annotations are 0, IAA is not measured, real-report projections are 0, and novelty is not established. The protocol and reconstructed schema remain drafts, not approved/frozen for formal annotation.
