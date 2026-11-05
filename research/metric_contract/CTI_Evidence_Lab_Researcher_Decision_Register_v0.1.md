# CTI Evidence Lab — Researcher Decision Register v0.1

**Prepared:** 4 November 2026  
**Status:** Working decision aid. The broad temporal-label estimand and primary mapping-level defaults were adopted under delegated project direction on 4 November 2026. Remaining decisions are open; the protocol and reconstructed schema are not frozen.  
**Purpose:** Separate decisions already grounded in available documents from provisional recommendations and choices that require explicit researcher approval before formal annotation.

## 1. How to read this register

- **Source-grounded:** explicitly stated by an available project artifact.
- **Adopted working default:** selected under delegated project direction; this does not freeze the protocol or reconstructed schema.
- **Recommended:** the current best methodological recommendation, still open for revision.
- **Blocked by missing original:** the exact wording or field design in Protocol v0.4.1 / Schema v0.4.2 cannot be verified because those original files are unavailable.

The current executable package is `CTI_Annotation_Schema_RECON_v0.1`. It is a reconstruction, not the original v0.4.2 schema, and must not be used for formal annotation until the decisions below are reviewed and the schema is approved/frozen.

## 2. Decisions and current recommendations

| # | Decision | Source-grounded position | Current recommendation | Status |
|---|---|---|---|---|
| 1 | Sampling population | The official manifest has 120 GNE+CyNE reports and 112 with an existing valid ATT&CK link. The 112 count is a linking-layer statistic, not the source-annotation frame. A second-pass read of the two no-CyNE source texts found a sponsored Ponemon survey summary (Proofpoint) and a TIBER-EU framework explainer (QuoIntelligence), not report-local CTI incident reporting. | Keep the complete 120-row manifest inventory for auditability. Recommend excluding those two records from the source-scope eligible population if the researcher confirms the CTI-report genre rule; retain the other six no-link reports for source-first annotation if their independent source/scope/local-use gates pass. Missing CyNE/ATT&CK links alone are not an exclusion basis. | **Source review complete; two source-scope exclusion recommendations pending formal researcher disposition** |
| 2 | Base feasibility selection | Five rank-1 candidates were selected by deterministic within-vendor hash priority, one per donor. They are candidate reports, not selected reports. | Keep the five rank-1 candidates in order. Advance only for predeclared source identity, completeness, scope, provenance/rights or practical local-use failure—not for event yield or a missing positive edge. | **Method correction adopted; 0/5 human eligibility decisions** |
| 3 | Primary mapping vocabulary | ChronoCTI's version-of-record paper states in Section 4.1 that its study used Enterprise ATT&CK v12.1 (193 techniques). The selected `A_120` vocabulary is pinned to the exact `selected_techniquesWName.json` source commit/blob in the repo. | Use accepted, source-supported parent-level `A_120` mappings as the primary analysis vocabulary. Keep exact technique/sub-technique `A_exact` results as a separate sensitivity view. Enterprise ATT&CK v12.1 is the pinned working crosswalk release. | **Working default adopted; 737-row crosswalk generated, committed and covered by passing synthetic CI on 5 November 2026; empirical annotation still pending** |
| 4 | Positive temporal labels in primary incidence | Available Protocol v0.4-draft includes `BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` as positive temporal labels. Audit v1.4 describes the v0.4.1 primary within-technique outcome using these five. | Count all five labels for broad within-technique temporal-relation incidence only when relation basis is `direct_source` or `direct_timestamp`, endpoints are distinct resolved atomic event leaves, relation-specific evidence and evidence scope are present, and comparison scope is compatible. Strict cycle analysis remains a separate `BEFORE`/`AFTER`-only subset. | **Working default adopted 4 November 2026 under delegated direction; semantic annotation and protocol freeze remain open** |
| 5 | Strict-order cycle analysis | Protocol and audits distinguish temporal relation labels from strict ordering. | Use only `BEFORE`/`AFTER` for strict-order cycles. In derived pair-key views normalize `AFTER(A,B)` to the same precedence as `BEFORE(B,A)` and treat both as `STRICT_ORDER`; retain the original source label, endpoint order and evidence in the annotation registers. | **Source-grounded rule; synthetic implementation corrected, real-data validation pending** |
| 6 | Report-level denominator | Audit v1.4 distinguishes eligible reports, zero-event outcomes and `NOT_ASSESSABLE`. The report registry separately records source/scope eligibility, local-use permission, report assessability and full-report review completion. | Count each report once. Define `N_eligible` as reports passing source/scope eligibility and local-research-use permission; public-reuse permission is separate. Define `N_assessable` as eligible reports with at least one completed human full-report review partition, a complete/readable frozen source, and `report_assessability=ASSESSABLE`, after report-level eligibility/local-use/assessability conflicts are resolved. If multiple annotators or passes exist, calculate report-level outcomes from the designated locked final annotation or agreed/adjudicated consensus partition, not by summing partitions. Report `N_assessable / N_eligible` coverage. Retain a fully reviewed report with zero resolved event leaves as an assessable zero outcome. Keep `NOT_ASSESSABLE`, `PENDING`, incomplete review and unresolved decision conflicts out of `N_assessable`; report them separately and never recode them as zero. | **Adopted as the project default on 4 November 2026 under delegated decision; protocol/schema remain provisional** |
| 7 | Pair opportunity versus positive relation | Audit v1.4 says the repeated-occurrence measure is opportunity, not the primary temporal outcome. | Report separate rates: (a) same-technique pair opportunity; (b) positive within-technique temporal relation. Never use pair opportunity as a proxy for a positive temporal result. | **Strongly supported; metric naming/formula approval pending** |
| 8 | Negative pair labels | Available protocol describes full-report positive-relation discovery separately from optional candidate-pair assessments. Missing pairs are not necessarily reviewed negatives. | Do not construct an exhaustive all-pairs negative matrix. Use `NO_TEMPORAL_CLAIM` only in a declared candidate-pair assessment frame with a frozen generation rule/version. `NOT_ASSESSABLE`, missing rows and unresolved pairs remain distinct. | **Recommended from source protocol; final enums blocked by v0.4.1 absence** |
| 9 | Primary event graph eligibility | Recovered Protocol v0.4-draft and audits restrict the primary graph to resolved atomic `event_leaf` activity units. | Require distinct endpoints, `event_leaf`, `atomic_event`, `RESOLVED`, compatible recorded scope, relation-specific evidence, and direct source/timestamp relation basis. Keep series, episodes, aggregates, generic behaviour and unresolved units visible outside the primary graph. | **Source-grounded; exact cross-register status rules still need approval** |
| 10 | Evidence scope | Recovered v0.4 draft contains `evidence_scope`; audit v0.4.2 says explicit values should include `SENTENCE`, `CROSS_SENTENCE`, `DOCUMENT_CONTEXT`. The v0.4.2 schema audit says the column was absent from the missing schema draft. | Retain explicit evidence scope on temporal relations. Do not rely on sentence IDs alone to imply `DOCUMENT_CONTEXT`. | **Recommended; exact v0.4.1 wording blocked** |
| 11 | Mapping acceptance | Audit v0.4.2 requires mapping basis and accepted-vs-alternative semantics; public v0.3 does not encode them. | Only accepted source-supported mapping decisions enter `A_exact`/`A_120`. `workbook_only`, rejected, unresolved and alternative-only records remain excluded from primary projection. | **Recommended; reconstruction enum choices need approval** |
| 12 | Human agreement | No independent human second annotation has been completed. AI-assisted review is not an independent human rater. | Arrange a genuinely independent second annotator for an overlapping subset if feasible. Otherwise state that IAA was not measured; a same-researcher washout pass is intra-annotator consistency only. | **Open researcher/workflow decision** |
| 15 | Prior AI triage exposure | Five rank-one candidates were previously reviewed with automated suggestions, including proposed activity units/series. The current protocol explicitly warns against treating prior reconstructions as blind gold labels. | Before the pilot, freeze a rule for annotator exposure. Log `prior_exposure_status` for each pass. Treat any pass exposed to the AI triage or earlier assistant-generated interpretations as non-blind; where feasible, have a genuinely independent human annotator work from the source without seeing those suggestions. Automated suggestions are never a second rater. | **Researcher approval required before pilot** |
| 16 | Source text hashing and offsets | The 120-row frame contains `source_text_sha256`, while raw AnnoCTR report text remains local and excluded from the repository. | Use strict UTF-8; strip only an optional leading BOM; preserve CRLF/LF; no Unicode normalization; hash UTF-8 bytes of the exact decoded text; use zero-based, end-exclusive Python Unicode code-point offsets. | **120/120 frame hashes matched official AnnoCTR text files at pinned source commit `d510b6949e1938d47c93a43eedd562dc538439dc` on 4 November 2026; archive ZIP hash is a separate check** |
| 13 | Rights and outputs | AnnoCTR corpus license is CC BY-SA 4.0, but report-specific publisher provenance/redistribution cautions remain AMBER. Local research use and public reuse are separate. | Keep raw reports and long source spans local. Record source-scope eligibility, local-use permission and public-reuse status separately. Clarify Lab52/S2 Grupo and Intel471 first. | **Open; no legal conclusion** |
| 14 | Novelty claim | Audit v1.4 documents substantial adjacent work and says novelty remains unproven. | Position the candidate niche around the human evidence standard plus explicit measurement of occurrence-level information under a named distinct-technique-pair projection. Do not claim general CTI event extraction, ATT&CK mapping, or attack sequencing as novel. | **Not approved; systematic comparison still needed** |

### Rights review update — 5 November 2026

A focused check of current primary-source terms found that the AnnoCTR repository README states CC BY-SA 4.0 for the corpus and acknowledges Intel471 and Lab52/S2 Grupo as donors. However, the current Intel471 Terms of Service reserve copying/reproduction/download/distribution rights absent written authorization unless otherwise permitted; the current Lab52 legal notice allows one offline personal/non-commercial copy but separately restricts reproduction and transformation without prior written authorization. The five-report audit and canonical frame now record these issues against the relevant candidates. This does **not** decide the validity or scope of the corpus-level licence. Keep Intel471 and Lab52 local research use and public reuse UNRESOLVED until the donor/dataset permission chain is clarified. The remaining three candidates' item-level terms were not newly established in this check and remain unresolved.

Sources:
- https://github.com/boschresearch/anno-ctr-lrec-coling-2024
- https://www.intel471.com/legal/terms-of-service
- https://www.lab52.io/legal_note

## 3. Missing-original dependencies

The exact `CTI_Event_Instance_Annotation_Protocol_v0.4.1-draft.md` and original `CTI_Annotation_Schema_v0.4.2-draft.zip` remain unrecovered. Available materials include Protocol v0.4-draft, its migration note, the v0.4.2 conformance audit, project-wide audit v1.4, five-report re-audit v0.1, sampling method v0.3.2, and the public v0.3 repository templates/validator.

Consequently, the following cannot be asserted as exact original v0.4.2 details: all 12 register headers and column order, complete original enum lists, exact required/optional markers, evidence-link key policy, complete candidate-pair labels, exact non-temporal endpoint schema, and whether the ZIP bundled the selected-120 file. RECON v0.1 supplies explicit proposed fields for a new reconstruction, not recovered original headers.

## 4. Current technical readiness versus research readiness

| Area | Status |
|---|---|
| A_120 source provenance | Pinned to ChronoCTI commit and blob; ordered ID-only extraction SHA-256 recorded |
| RECON schema package | 12 blank proposed registers; not original v0.4.2; not approved/frozen |
| Structural validator | 31 synthetic tests pass |
| Projection module | 16 synthetic tests pass |
| Register-to-projection adapter | 11 synthetic tests pass; requires a matching computed partition/source digest |
| Combined synthetic suite | 58/58 pass (31 validator, 16 projection, 11 adapter); blank bundle 0 errors + 1 expected empty-bundle warning |
| Real AnnoCTR data through RECON | 0 rows |
| Researcher eligibility decisions | 0/5 |
| Human annotation locks | 0 |
| IAA | Not measured |
| Real-report projection results | 0 |
| Research prevalence estimate | None; five-report sample is feasibility-only |

## 5. Approval boundary and next sequence

1. Generate and independently inspect the immutable Enterprise ATT&CK v12.1 exact-to-parent crosswalk; integrate its release and hash checks before accepting sub-technique parent mappings.
2. Review remaining decisions, including the two no-CyNE genre cases, evidence-scope and mapping-acceptance details, and the prior-exposure rule.
3. Reconcile the working defaults against the exact protocol and schema originals if recovered; otherwise explicitly approve or revise RECON as a new schema version, never as v0.4.2.
4. Complete the five candidate source-identity, source/scope eligibility, local research-use and public-reuse records separately.
5. Freeze protocol/schema/version/pass identity and hash the approved package before source-first annotation. AI triage remains separate from human labels; an exposed pass is not blind. Projection requires explicit confirmation and a computed digest matching the selected human-approved source/partition registers.

**No formal annotation should begin solely because the 58 synthetic tests pass.** These tests show that the proposed structure behaves as coded on synthetic fixtures; they do not establish semantic validity, protocol approval, source eligibility, human agreement, or research findings.
