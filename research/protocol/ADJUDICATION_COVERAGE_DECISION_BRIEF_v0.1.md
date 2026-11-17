# CTI Evidence Lab — Adjudication Coverage Decision Brief v0.1

**Prepared:** 17 November 2026  
**Status:** Proposed design for researcher review — NOT APPROVED, NOT FROZEN  
**Applies to:** Protocol v0.5-draft; RECON v0.1 base records and adjudication log; v0.2 final-partition selection.

## Decision required

The base annotation records each have one `adjudication_status` (`UNREVIEWED`, `AGREED`, `ADJUDICATED`), while `adjudication_log.csv` records `AGREED`, `ADJUDICATED`, and `DEFERRED` outcomes for individual fields. Those vocabularies cannot unambiguously report mixed, partial, or deferred field review. An `ADJUDICATED` change to one field cannot establish that every relevant record or field in the partition has been reviewed.

The existing draft validator verifies target identity, reviewer-ID distinction, field-value changes, and append-only history. It does **not** establish the coverage universe or whether review is complete. As a safety measure, the v0.2 selected-partition validator fails closed for every selected `ADJUDICATED_FINAL` role until this decision and its implementation are complete. This safeguards analysis but does not itself resolve the research-design question.

## Design options

| Option | Benefits | Problems / obligations |
|---|---|---|
| A. Define the existing record-level status as a derived summary | Smaller data-model change | The current enum has no explicit DEFERRED/PARTIAL state; needs full deterministic roll-up and a review-completeness register. |
| B. Make field-level review log authoritative and retire record-level status in a new schema version | Avoids two independent sources of truth | Requires versioned migration, and field log alone still does not prove that unlogged fields were reviewed. |
| C. Add an explicit review-coverage register and derive record/partition completion | Makes omissions, non-changing reviews and deferred fields independently auditable | Adds a versioned register, explicit coverage universe, reviewer workflow and full cross-register validation. |

**Recommended for researcher consideration: Option C**, combined with a derived (not freely editable) record-level status, or a later versioned retirement of that status. This is a recommendation, not an adopted methodological rule.

## Questions that must be approved before implementing Option C

1. **Review universe.** Which register types and which fields are in-scope for independent adjudication? Distinguish immutable IDs, source provenance, optional notes, and material analytical fields. State whether every record or only a predeclared candidate set must be covered. Never define this after looking at positive result yield.
2. **Coverage unit.** Decide whether a complete coverage assertion is at field, record, and/or partition grain; define unique keys and treatment of records added or deleted after review.
3. **Review outcome.** Define exhaustive terminal outcomes (e.g. agreed unchanged, adjudicated changed, explicitly not applicable) and non-terminal outcomes (unreviewed, deferred). Declare whether a terminal DEFERRED is ever allowed; the safest provisional answer is **no**.
4. **Record-level status.** Decide whether it is computed from review outcomes or is a separately signed assertion; if computed, specify mixed/partial and deferred behavior and how to represent that under a versioned vocabulary.
5. **Independent identity and audit trail.** Decide who may review, how reviewer IDs are authenticated outside the CSV, how duplicate/superseded reviews are ordered, and how corrections preserve an append-only trail.
6. **Final selection.** Define exactly when a whole partition qualifies for `ADJUDICATED_FINAL`, including zero-record partitions and records created after a review. Preserve the independent source/eligibility, timestamp, mapping and lock gates.
7. **Human workflow.** Specify who signs off full coverage, how a reviewer can challenge a decision, how disagreements are resolved, and what remains an unresolved outcome. A hash or distinct string ID is not proof of human review.

## Required acceptance tests for the approved version

- Reject a partition with one valid adjudicated field but other unreviewed in-scope fields or records.
- Reject missing coverage rows, duplicated coverage keys, orphaned targets, non-terminal DEFERRED rows, and self-review where independence is required.
- Reject a record with internally inconsistent derived status or a changed persisted field without a matching append-only history.
- Reject any new/modified record after coverage is finalized unless the review state is invalidated and recalculated.
- Accept a complete reviewed partition containing a mix of AGREED (unchanged) and ADJUDICATED (changed) fields **only after** an approved coverage model and all other final-selection gates pass.
- Verify exact source, source-hash and selected-final lock references; never use the presence of a signature-shaped digest to substitute for actual source and review verification.
- Keep `SINGLE_ANNOTATOR_FINAL`, `CONSENSUS`, and RECON v0.3/v0.4 extension-specific gates separate; none is silently promoted to adjudication.

## Researcher disposition (currently blank)

- Selected design option:
- Explicit review universe / exclusions:
- Completeness and DEFERRED policy:
- Record-level status policy:
- Reviewer identity / sign-off method:
- Approved version and date:
- Required migration and acceptance criteria:
- Approval evidence / location:

Until this section is completed by the researcher, the current gate must remain fail-closed. No eligibility decision, human annotation, real-report projection, IAA, or novelty claim is created by this brief.
