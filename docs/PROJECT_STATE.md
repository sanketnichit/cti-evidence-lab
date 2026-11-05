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
- Two reports have no observed cybersecurity-specific rows in the inspected full linking export. A second-pass read of their official source texts now recommends source-scope exclusion: the Proofpoint row is a sponsored Ponemon survey summary, and the QuoIntelligence row is a TIBER-EU framework explainer. Both remain in the 120-row inventory; formal researcher eligibility fields are still pending.
- Across all 400 TimeML files: 3,324 TIMEX3 tags and zero EVENT, MAKEINSTANCE, TLINK or SIGNAL tags.
- The raw AnnoCTR corpus and full report text are intentionally not committed. The repository contains only the report-level metadata inventory, aggregate summary, source archive hash and reproducible methodology. Raw data stay local under the corpus licence/provenance constraints.

## Sampling and candidate status

- The five rank-1 candidates remain feasibility candidates, one per donor. They are not selected/frozen reports.
- Their five canonical publisher URLs and publication dates were cross-checked against official publisher pages on 5 November 2026. This is source-identity verification only; researcher eligibility remains 0/5, and local research-use/public-reuse decisions remain separate.
- A 5 November 2026 primary-source rights review found terms conflicts requiring clarification for Intel471 and Lab52/S2 Grupo. For Proofpoint, QuoIntelligence and Zscaler, the linked terms found were either scoped to customer/product portals or did not grant public-blog reuse; no article-specific reuse grant was verified. These findings do not determine the scope or validity of the AnnoCTR CC BY-SA 4.0 corpus statement, and absence of a located article licence is not a prohibition. Local research-use and public-reuse fields remain UNRESOLVED for all five candidates. See the rights addendum in `research/annoctr_sampling/AnnoCTR_Five_Report_Reaudit_and_Sampling_Correction_v0.1.md`.
- Source-first feasibility reviewer drafts are now recorded for all five fixed rank-1 reports: Intel471 Groove/Babuk, Lab52 TokyoX Part 2, Proofpoint Privacy Tools, QuoIntelligence Winnti, and Zscaler Netwire RAT (see `research/feasibility/`). These are working source reviews only. They do not alter the 120-row frame, make researcher eligibility or rights decisions, create human-locked annotations, or contribute event/edge/projection results.
- The Zscaler source supports one candidate resolved email-send occurrence with a source-reported timestamp; its later malware chain remains conditional sample behaviour. The other four reports currently provide broad/generic behaviour, sample capabilities, or multi-context reporting without a resolved pair of attack-event leaves. These are source-review observations, not formal annotation outcomes.
- Researcher eligibility decisions: 0/5. Human-locked annotations: 0. The decision register now contains operational recommendations for evidence scope, mapping acceptance, alternatives, prior exposure and candidate-pair negatives; none is recorded as formally approved.
- The five-report batch is for feasibility/protocol debugging only; it cannot estimate vendor or corpus prevalence.
- Do not replace a candidate because it lacks two resolved event leaves, a same-technique pair opportunity or a positive temporal relation. Replacement is allowed only for predeclared source identity, scope, completeness, provenance/rights or practical local-use failure.
- The old event-enumerability gate in the sample-adequacy audit is superseded.

## Protocol and schema versions

- Recovered protocol: `CTI_Event_Instance_Annotation_Protocol_v0.4-draft.md`. It is a draft, not a frozen researcher-approved protocol.
- Exact protocol v0.4.1 was not recovered.
- Original `CTI_Annotation_Schema_v0.4.2-draft.zip` was not recovered. Its conformance audit is available.
- `research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/` is a newly reconstructed replacement design based on the recovered v0.4 draft, migration note, v0.4.2 audit and v0.3 templates. It is explicitly **not** the original v0.4.2 and is not approved for formal annotation.
- The RECON package has 12 blank registers, a field dictionary, controlled vocabularies, validator, projection module, adapter and synthetic tests. The exact original schema headers may differ.

## Implementation verification

- Root synthetic tests: 53/53 passed. RECON synthetic tests: 63/63 passed (36 validator, 16 projection, 11 adapter). The source snapshot at commit `95d802e47dcce5d8a6af18563237f5c764cd9998` was verified by GitHub Actions run [#41979691694](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/41979691694) on 5 November 2026; all steps passed, including root tests, the projection demo, all 29 RECON checksums, all 63 RECON tests and blank-bundle validation.
- Internal SHA256SUMS checks: 29/29 entries matched.
- Blank-bundle validation returns zero errors and an `EMPTY_ANNOTATION_BUNDLE` warning; it validates package structure only, not research annotations.
- The RECON code has not been run on human annotations or real AnnoCTR event graphs. The validator flags report-level eligibility/local-use/assessability conflicts across annotator/pass partitions and excludes conflicting reports from denominator summaries until adjudicated. It also validates prior-exposure values, requires normalized evidence-linked time records at both endpoints of `direct_timestamp`, rejects duplicate/contradictory direct temporal-pair claims, checks positive candidate assessments against their linked relation, and requires top-level exact techniques to map to themselves. The validator now checks accepted exact IDs and sub-technique parents against the pinned v12.1 crosswalk. The validator's synthetic checks do not establish semantic annotation correctness.
- The public v0.3-era CSV schema and root annotation validator remain unchanged. `src/projection_metrics.py` has received separate mechanical corrections for normalized strict-order pair orientation and single-edge cycle-fan-out attribution. RECON remains isolated pending protocol/schema approval.

Source text convention: strict UTF-8; an optional leading UTF-8 BOM is removed; CRLF/LF are preserved; no Unicode normalization is applied; `source_text_sha256` is SHA-256 over the UTF-8 bytes of the exact decoded annotation text; offsets are zero-based, end-exclusive Python Unicode code-point indices. On 4 November 2026, all 120 `source_text_sha256` values in the frame were independently recomputed from the official AnnoCTR repository text files at pinned commit `d510b6949e1938d47c93a43eedd562dc538439dc` and matched 120/120. This verifies the frame hashes against that source revision; it does not recompute the separate downloaded-archive SHA-256. `scripts/hash_annoctr_sources.py` reproduces the check against a local `AnnoCTR/all` directory and can update the frame only with explicit `--write`. Raw report text remains outside this repository.

## Adopted working defaults and remaining research decisions

- Pair opportunity and positive within-technique temporal-relation incidence are separate measures.
- **Adopted working temporal estimand (4 November 2026):** broad within-technique temporal incidence includes directly supported `BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` relations between distinct resolved atomic event leaves, with relation-specific evidence, recorded evidence scope and compatible comparison scope. Strict cycle analysis uses only normalized `BEFORE`/`AFTER`.
- **Adopted working mapping level (4 November 2026):** parent-level `A_120` is the primary analysis vocabulary; exact technique/sub-technique `A_exact` is a separate sensitivity view. Enterprise ATT&CK v12.1 is the working exact-to-parent crosswalk release because it matches ChronoCTI's published version. The 737-row crosswalk is generated, committed and checked by the RECON validator. Revoked/deprecated exact IDs remain visible but are excluded from primary A_120 unless separately resolved.
- **Adopted project default (4 November 2026):** primary report-level rates use `N_assessable`; assessability coverage is `N_assessable / N_eligible`. `N_eligible` requires source/scope eligibility and local-use permission. `N_assessable` additionally requires a complete/readable frozen source, `report_assessability=ASSESSABLE`, and at least one completed eligible human full-report review partition, with report-level conflicts resolved. Count each report once. If multiple annotators or passes exist, calculate report-level outcomes from the designated locked final annotation or agreed/adjudicated consensus partition, not by summing partitions. A fully reviewed assessable report with zero resolved event leaves remains a zero outcome; `NOT_ASSESSABLE`, `PENDING`, incomplete review and unresolved conflicts are disclosed separately and are not recoded as zero. Public-reuse permission is tracked separately.
- The researcher decision register is in `research/metric_contract/CTI_Evidence_Lab_Researcher_Decision_Register_v0.1.md`.

## Literature boundary — refreshed 5 November 2026

The recent-work comparison now explicitly includes APTIE (Scientific Data, 25 May 2026), the cybersecurity event-extraction survey by Yang et al. (IET Communications, first published 21 July 2026), and SMAH-CTI (Findings of EMNLP 2026). APTIE separates semantic entity-relation labels from its event-extraction module; SMAH-CTI provides sentence-level relevance, NER, ATT&CK mapping and grounded procedure descriptions, not event-event temporal links. The survey describes cybersecurity event relation extraction as underdeveloped and reports no unified, widely adopted public benchmark. ChronoCTI remains direct prior art for temporal relations over ATT&CK technique pairs. The project's candidate contribution must therefore be limited to source-grounded report-local occurrence identity, event-to-event temporal evidence and the effects of projection to distinct technique pairs. Novelty remains unproven. See research/RELATED_WORK_MATRIX.md and the 5 November addendum in docs/RESEARCH_GAP_AUDIT_2026-11-01.md.

## ChronoCTI baseline

The current audit is a workbook and selected source-code control-flow audit, not a full feature-table rebuild or model re-training. Preserve raw `NEXT`; any conversion to a BEFORE-like interpretation is a separate hypothesis. ChronoCTI's paper identifies Enterprise ATT&CK v12.1 (Section 4.1) and describes the 120-technique pair task with diagonal pairs excluded (Section 4.5.1). The selected 120 IDs are pinned to ChronoCTI's `selected_techniquesWName.json`; the derived identifier-only list is included in RECON with provenance/hash. We have not run ChronoCTI's learned model on AnnoCTR; our proposed analysis measures source-grounded annotations under a named projection, not ChronoCTI's measured errors on AnnoCTR.

## Current blockers / next sequence

1. Record the formal source-scope disposition for the two no-CyNE reports against the source-based recommendations in `research/ANNOCTR_CANDIDATE_CONTENT_REVIEW_v0.1.md`; keep both rows in the historical 120-report inventory.
2. **Permission clarification route identified.** The AnnoCTR README names the dataset maintainer contact and states that the corpus folder is CC BY-SA 4.0; the licence only grants rights the licensor has authority to license. A precise clarification checklist is recorded at research/rights/AnnoCTR_Research_Use_Permission_Clarification_v0.1.md. The request has not been sent and all five local-use/public-reuse fields remain UNRESOLVED.
3. Review the operational rules proposed in Section 2A of the researcher decision register: evidence-scope thresholds, mapping acceptance/alternatives, prior-exposure coding and candidate-pair negative labels. Formal approval remains pending; keep the two no-CyNE source-scope dispositions pending and retain the original protocol/schema recovery gap.
4. Freeze a new, clearly versioned protocol/schema package only after the decisions are recorded. RECON v0.1 remains a reconstruction, not the original v0.4.2.
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

