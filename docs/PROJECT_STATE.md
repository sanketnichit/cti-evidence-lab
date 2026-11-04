# CTI Evidence Lab — Project State

**Snapshot date:** 4 November 2026  
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
- Two reports have no observed cybersecurity-specific rows in the inspected full linking export. They remain in the 120-row inventory pending the researcher's content-scope decision.
- Across all 400 TimeML files: 3,324 TIMEX3 tags and zero EVENT, MAKEINSTANCE, TLINK or SIGNAL tags.
- The raw AnnoCTR corpus and full report text are intentionally not committed. The repository contains only the report-level metadata inventory, aggregate summary, source archive hash and reproducible methodology. Raw data stay local under the corpus licence/provenance constraints.

## Sampling and candidate status

- The five rank-1 candidates remain feasibility candidates, one per donor. They are not selected/frozen reports.
- Researcher eligibility decisions: 0/5. Human-locked annotations: 0.
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

- Root synthetic tests: 43/43 passed. RECON synthetic tests: 56/56 passed (29 validator, 16 projection, 11 adapter tests).
- Internal SHA256SUMS checks: 29/29 entries matched.
- Blank-bundle validation returns zero errors and an `EMPTY_ANNOTATION_BUNDLE` warning; it validates package structure only, not research annotations.
- The RECON code has not been run on human annotations or real AnnoCTR event graphs. The validator flags report-level eligibility/local-use/assessability conflicts across annotator/pass partitions and excludes conflicting reports from denominator summaries until adjudicated. It also validates prior-exposure values, requires normalized evidence-linked time records at both endpoints of `direct_timestamp`, rejects duplicate/contradictory direct temporal-pair claims, checks positive candidate assessments against their linked relation, and requires top-level exact techniques to map to themselves. Accepted sub-technique mapping rows remain fail-closed until a real version-pinned exact-to-parent crosswalk is integrated. The validator's synthetic checks do not establish semantic annotation correctness.
- The public v0.3-era CSV schema and root annotation validator remain unchanged. `src/projection_metrics.py` has received separate mechanical corrections for normalized strict-order pair orientation and single-edge cycle-fan-out attribution. RECON remains isolated pending protocol/schema approval.

Source text convention: strict UTF-8; an optional leading UTF-8 BOM is removed; CRLF/LF are preserved; no Unicode normalization is applied; `source_text_sha256` is SHA-256 over the UTF-8 bytes of the exact decoded annotation text; offsets are zero-based, end-exclusive Python Unicode code-point indices. On 4 November 2026, all 120 `source_text_sha256` values in the frame were independently recomputed from the official AnnoCTR repository text files at pinned commit `d510b6949e1938d47c93a43eedd562dc538439dc` and matched 120/120. This verifies the frame hashes against that source revision; it does not recompute the separate downloaded-archive SHA-256. `scripts/hash_annoctr_sources.py` reproduces the check against a local `AnnoCTR/all` directory and can update the frame only with explicit `--write`. Raw report text remains outside this repository.

## Metrics and open researcher decisions

- Pair opportunity and positive within-technique temporal-relation incidence are separate measures.
- Proposed primary relation labels: direct-source/direct-timestamp `BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, `CONCURRENT_UNSPECIFIED`; strict cycle analysis uses only normalized `BEFORE`/`AFTER`.
- The assessable-report denominator and treatment of reports that are eligible but `NOT_ASSESSABLE` remain explicit researcher decisions. Do not silently count them as zero-edge outcomes.
- The researcher decision register is in `research/metric_contract/CTI_Evidence_Lab_Researcher_Decision_Register_v0.1.md`.

## ChronoCTI baseline

The current audit is a workbook and selected source-code control-flow audit, not a full feature-table rebuild or model re-training. Preserve raw `NEXT`; any conversion to a BEFORE-like interpretation is a separate hypothesis. ChronoCTI's paper identifies Enterprise ATT&CK v12.1 (Section 4.1) and describes the 120-technique pair task with diagonal pairs excluded (Section 4.5.1). The selected 120 IDs are pinned to ChronoCTI's `selected_techniquesWName.json`; the derived identifier-only list is included in RECON with provenance/hash. We have not run ChronoCTI's learned model on AnnoCTR; our proposed analysis measures source-grounded annotations under a named projection, not ChronoCTI's measured errors on AnnoCTR.

## Current blockers / next sequence

1. Resolve the open P0 researcher decisions in the decision register (metric denominator/assessability, temporal-label estimand, mapping level, and the two no-CyNE genre cases).
2. Review the reconstructed schema against the missing original v0.4.1/v0.4.2 artifacts if they ever become available; otherwise approve or revise RECON explicitly as a new version.
3. Make separate researcher eligibility, local research-use and public-reuse decisions for each of the five rank-1 candidates.
4. Only after protocol/schema freeze, start source-first human annotation. Keep raw sources and long excerpts local.
5. Add a second human annotator for an overlapping subset if available; otherwise state that IAA was not measured. AI is not a second annotator.
6. Lock and hash human annotation files before any projection analysis. Only then compute real-report metrics.

## Research integrity status

No human annotations, real-report projection results, prevalence estimates, IAA measurements, validated novelty claim or publication-ready result currently exist. Synthetic test success establishes only code-path behavior on synthetic fixtures.

## Update — 4 November 2026

The ChronoCTI version-of-record paper identifies Enterprise ATT&CK v12.1 in Section 4.1, so v12.1 is the source-aligned primary crosswalk candidate. A non-freezing preflight against the official versioned v12.1 STIX bundle (Git blob SHA-1 `7a99efb3a8c89b06dd9db1a9a17e4201160ac4ee`; retrieved-file SHA-256 `ad169215c75f94271124d3888791323e43aaedad2755f7d7eea8d4185af7f536`) found 737 attack-pattern objects: 333 top-level techniques and 404 sub-techniques with 404 explicit, valid parent relationships. All 120 ChronoCTI `A_120` IDs were present exactly once as top-level techniques; none were missing, duplicated, sub-techniques, revoked or deprecated. The separate v14.1 inspection remains a non-primary compatibility preflight only. No ATT&CK release is approved, no crosswalk has been generated/added to RECON, and exact-to-parent sub-technique classification remains fail-closed until a release is approved and its crosswalk is generated, inspected and integrated.

## Repository checkpoint — 3 November 2026

The current project artifacts are version-controlled on `main`: the text-free 400-report AnnoCTR screening inventory and summary, the 120-row multi-vendor frame, Sampling Method v0.3.2, the five-report source re-audit, the provisional metric contract and decision register, and the separate RECON v0.1 schema reconstruction. The original public v0.3 implementation remains unchanged.

Independent verification on the frozen AnnoCTR archive reproduced the screening CSV byte-for-byte (400 rows; SHA-256 `9691ef5cbd9f5e83a0c6337bf2470f232f342377b745596499cfe62d9ae50c79`). The official archive hash matched the recorded value. The 120-row frame was checked against the fixed seed, all 120 source-text hashes were matched against the local corpus, and donor counts and within-vendor ranks were consistent.

The current checked code state passed 33 root tests and 40 RECON synthetic tests; the toy projection demo ran and Python compilation passed. GitHub Actions run #41693198880 passed the root suite, sampling-frame checks, RECON checksums, RECON tests, and blank-bundle validation. The RECON checksum manifest contains 29 package entries and all 29 match. These are reproducibility and synthetic-code checks only; no human source annotation or real-report projection result exists.

`docs/PROJECT_STATUS.md` is a historical 1 November snapshot. This file is the current project-state record. The project-wide audit v1.4 below has a 3 November repository-synchronization addendum clarifying which earlier statements described the pre-sync state.

