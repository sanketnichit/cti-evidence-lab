# CTI Evidence Lab — Researcher Decision Register v0.1

**Prepared:** 3 November 2026  
**Status:** Decision aid only. Nothing in this register is researcher-approved or protocol-frozen.  
**Purpose:** Separate decisions already grounded in available documents from provisional recommendations and choices that require explicit researcher approval before formal annotation.

## 1. How to read this register

- **Source-grounded:** explicitly stated by an available project artifact. This does not mean the researcher has approved it.
- **Recommended:** the current best methodological recommendation, open for researcher approval or revision.
- **Blocked by missing original:** the exact wording or field design in Protocol v0.4.1 / Schema v0.4.2 cannot be verified because those original files are unavailable.

The current executable package is `CTI_Annotation_Schema_RECON_v0.1`. It is a reconstruction, not the original v0.4.2 schema, and must not be used for formal annotation until the decisions below are reviewed and the schema is approved/frozen.

## 2. Decisions and current recommendations

| # | Decision | Source-grounded position | Current recommendation | Status |
|---|---|---|---|---|
| 1 | Sampling population | The official manifest has 120 GNE+CyNE reports and 112 with an existing valid ATT&CK link. The 112 count is a linking-layer statistic, not the source-annotation frame. | Keep all 120 in the frame. Preserve the two no-CyNE reports as content-based genre-exclusion candidates pending researcher decision; retain the six other no-link reports for source-first annotation if other gates pass. | **Recommended; researcher confirmation pending** |
| 2 | Base feasibility selection | Five rank-1 candidates were selected by deterministic within-vendor hash priority, one per donor. They are candidate reports, not selected reports. | Keep the five rank-1 candidates in order. Advance only for predeclared source identity, completeness, scope, provenance/rights or practical local-use failure—not for event yield or a missing positive edge. | **Method correction adopted; 0/5 human eligibility decisions** |
| 3 | Primary mapping vocabulary | ChronoCTI source has 120 selected technique IDs. The exact source file is pinned in the repo; an ordered ID-only extraction is included in RECON. | Use accepted, source-supported parent-level `A_120` mappings for primary comparability. Keep exact/sub-technique `A_exact` as a separate sensitivity analysis. | **Strongly supported; researcher approval pending** |
| 4 | Positive temporal labels in primary incidence | Available Protocol v0.4-draft includes `BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` as positive temporal labels. Audit v1.4 describes the v0.4.1 primary within-technique outcome using these five. | Count all five labels for the broad within-technique temporal-relation report outcome, only when relation basis is `direct_source` or `direct_timestamp`, endpoints are distinct resolved atomic event leaves, and scope is compatible. | **Recommended; researcher approval pending** |
| 5 | Strict-order cycle analysis | Protocol and audits distinguish temporal relation labels from strict ordering. | Use only `BEFORE`/`AFTER` for strict-order cycles; normalize `AFTER(A,B)` to `BEFORE(B,A)` only in a derived analysis view. Keep raw labels and source endpoint order unchanged. | **Source-grounded rule; normalization implementation is provisional** |
| 6 | Report-level denominator | Audit v1.4 says the denominator and missingness policy require approval; it distinguishes eligible reports, zero-event outcomes and `NOT_ASSESSABLE`. | Track `N_eligible` and `N_assessable` separately. Proposed primary incidence denominator: assessable eligible reports after completed full-report review. Report assessability coverage as `N_assessable / N_eligible`. Keep zero-event-leaf but otherwise assessable reports in the primary denominator; do not treat `NOT_ASSESSABLE` as zero. | **Proposed; explicit approval required** |
| 7 | Pair opportunity versus positive relation | Audit v1.4 says the repeated-occurrence measure is opportunity, not the primary temporal outcome. | Report separate rates: (a) same-technique pair opportunity; (b) positive within-technique temporal relation. Never use pair opportunity as a proxy for a positive temporal result. | **Strongly supported; metric naming/formula approval pending** |
| 8 | Negative pair labels | Available protocol describes full-report positive-relation discovery separately from optional candidate-pair assessments. Missing pairs are not necessarily reviewed negatives. | Do not construct an exhaustive all-pairs negative matrix. Use `NO_TEMPORAL_CLAIM` only in a declared candidate-pair assessment frame with a frozen generation rule/version. `NOT_ASSESSABLE`, missing rows and unresolved pairs remain distinct. | **Recommended from source protocol; final enums blocked by v0.4.1 absence** |
| 9 | Primary event graph eligibility | Recovered Protocol v0.4-draft and audits restrict the primary graph to resolved atomic `event_leaf` activity units. | Require distinct endpoints, `event_leaf`, `atomic_event`, `RESOLVED`, compatible recorded scope, relation-specific evidence, and direct source/timestamp relation basis. Keep series, episodes, aggregates, generic behaviour and unresolved units visible outside the primary graph. | **Source-grounded; exact cross-register status rules still need approval** |
| 10 | Evidence scope | Recovered v0.4 draft contains `evidence_scope`; audit v0.4.2 says explicit values should include `SENTENCE`, `CROSS_SENTENCE`, `DOCUMENT_CONTEXT`. The v0.4.2 schema audit says the column was absent from the missing schema draft. | Retain explicit evidence scope on temporal relations. Do not rely on sentence IDs alone to imply `DOCUMENT_CONTEXT`. | **Recommended; exact v0.4.1 wording blocked** |
| 11 | Mapping acceptance | Audit v0.4.2 requires mapping basis and accepted-vs-alternative semantics; public v0.3 does not encode them. | Only accepted source-supported mapping decisions enter `A_exact`/`A_120`. `workbook_only`, rejected, unresolved and alternative-only records remain excluded from primary projection. | **Recommended; reconstruction enum choices need approval** |
| 12 | Human agreement | No independent human second annotation has been completed. AI-assisted review is not an independent human rater. | Arrange a genuinely independent second annotator for an overlapping subset if feasible. Otherwise state that IAA was not measured; a same-researcher washout pass is intra-annotator consistency only. | **Open researcher/workflow decision** |
| 13 | Rights and outputs | AnnoCTR corpus license is CC BY-SA 4.0, but report-specific publisher provenance/redistribution cautions remain AMBER. Local research use and public reuse are separate. | Keep raw reports and long source spans local. Record source-scope eligibility, local-use permission and public-reuse status separately. Clarify Lab52/S2 Grupo and Intel471 first. | **Open; no legal conclusion** |
| 14 | Novelty claim | Audit v1.4 documents substantial adjacent work and says novelty remains unproven. | Position the candidate niche around the human evidence standard plus explicit measurement of occurrence-level information under a named distinct-technique-pair projection. Do not claim general CTI event extraction, ATT&CK mapping, or attack sequencing as novel. | **Not approved; systematic comparison still needed** |

## 3. Missing-original dependencies

The exact `CTI_Event_Instance_Annotation_Protocol_v0.4.1-draft.md` and original `CTI_Annotation_Schema_v0.4.2-draft.zip` remain unrecovered. Available materials include Protocol v0.4-draft, its migration note, the v0.4.2 conformance audit, project-wide audit v1.4, five-report re-audit v0.1, sampling method v0.3.2, and the public v0.3 repository templates/validator.

Consequently, the following cannot be asserted as exact original v0.4.2 details: all 12 register headers and column order, complete original enum lists, exact required/optional markers, evidence-link key policy, complete candidate-pair labels, exact non-temporal endpoint schema, and whether the ZIP bundled the selected-120 file. RECON v0.1 supplies explicit proposed fields for a new reconstruction, not recovered original headers.

## 4. Current technical readiness versus research readiness

| Area | Status |
|---|---|
| A_120 source provenance | Pinned to ChronoCTI commit and blob; ordered ID-only extraction SHA-256 recorded |
| RECON schema package | 12 blank proposed registers; not original v0.4.2; not approved/frozen |
| Structural validator | 18 synthetic tests pass |
| Projection module | 13 synthetic tests pass |
| Register-to-projection adapter | 9 synthetic tests pass; requires explicit lock confirmation/reference |
| Combined synthetic suite | 40/40 pass; Python compile pass; blank bundle 0 errors + 1 expected empty-bundle warning |
| Real AnnoCTR data through RECON | 0 rows |
| Researcher eligibility decisions | 0/5 |
| Human annotation locks | 0 |
| IAA | Not measured |
| Real-report projection results | 0 |
| Research prevalence estimate | None; five-report sample is feasibility-only |

## 5. Approval boundary and next sequence

1. Researcher reviews/approves or revises the choices in Section 2, especially the denominator, broad temporal-label incidence, `A_120`, and evidence-scope rules.
2. Reconcile the approved choices against the exact protocol and schema originals if recovered; otherwise explicitly approve RECON as a new schema version, never as v0.4.2.
3. Complete the five researcher eligibility records for source-scope eligibility and local research use, keeping public reuse separate.
4. Freeze protocol/schema/version/pass identity, source normalization and offset rules; hash the blank bundle and the final approved package.
5. Only then begin source-first annotation. AI triage remains separate from human labels. Projection requires a real human-approved immutable annotation lock reference.

**No formal annotation should begin solely because the 39 synthetic tests pass.** These tests show that the proposed structure behaves as coded on synthetic fixtures; they do not establish semantic validity, protocol approval, source eligibility, human agreement, or research findings.
