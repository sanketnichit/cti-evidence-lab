# Report-level aggregation layer v0.1

**Date:** 5 November 2026  
**Status:** implemented and synthetic-tested; metric contract and scope-pair operationalization remain provisional. Not used on real AnnoCTR human annotations.  
**Consumes:** RECON v0.1 registers plus RECON v0.2 temporal-evidence and selected-partition registers.

## Purpose

The selected-partition adapter projects one validated report at a time. This module aggregates those report outputs without summing annotator/pass partitions and without converting missing annotations into negative outcomes.

It reports three separate stages:

1. **N_eligible** — distinct reports with a consistent report-level decision of source_scope_eligibility=ELIGIBLE and local_research_use_status=PERMITTED.
2. **N_assessable** — eligible reports with at least one human partition marked ASSESSABLE and full_report_review_status=COMPLETE, an exact frozen source whose SHA-256 and code-point count match the register, and no report-level decision or source-version conflict.
3. **Selected-final projection coverage** — assessable reports with exactly one selected final partition whose source, annotation lock, temporal-evidence extension, and selection lock pass the v0.2 adapter.

A fully reviewed, source-verified report with zero resolved event leaves remains in N_assessable. It contributes a zero event-leaf outcome after a valid final partition is selected; it is not dropped from the denominator.

## Report-level measures

For each successfully projected assessable report, the module computes:

- resolved atomic event_leaf presence;
- compatible event-pair opportunity;
- same-technique pair opportunity using accepted A_120 mapping intersections;
- any qualifying direct positive temporal relation;
- any qualifying within-technique positive temporal relation;
- positive relation-label counts and within-technique label counts;
- event mapping and positive-edge mapping coverage.

It also sums per-report projection counts for mapped/unmapped positive edges, fully omitted/partially represented/no-diagonal outcomes, diagonal mapping combinations, technique-pair collisions, and projected strict-order cycle diagnostics. Pair keys and SCCs are never merged across different reports; per-report diagnostic counts are summed.

## Denominator and missingness behaviour

- A report is counted once, regardless of annotator/pass count.
- Conflicting source_scope_eligibility, local_research_use_status, or report_assessability values across partitions exclude that report from both report-level denominators until resolved.
- Different non-empty frozen-source hash/count pairs across partitions are reported as a source-version conflict and block N_assessable.
- A source is verified only when the exact decoded source text matches both source_text_sha256 and source_text_char_count in a completed assessable human partition.
- public_reuse_status is not used as a local-research denominator gate.
- Missing rows and unselected partitions are not negative results.
- Primary report-level rates are withheld unless every N_assessable report has a successful selected-final projection. A selected-subset rate is still shown but is explicitly descriptive and not substituted for the primary denominator.

## Scope-pair opportunity rule — approval still required

The protocol requires scope-compatible event pairs but the metric contract does not fully operationalize every possible pair in a hierarchical scope tree. This implementation provides a conservative, explicit candidate rule:

> Two event leaves are a compatible pair when their nearest common ancestor in the selected partition's scope tree is RESOLVED and is not REPORT_AGGREGATE.

Unresolved/provisional scope paths, no shared scope, and a shared report aggregate alone do not create pair opportunity. This permits two host-scoped activities under one resolved incident scope to be compared. However, the implementation also treats a shared non-report ancestor such as `CAMPAIGN`, `ACTOR_OPERATION`, `VICTIM_ORGANISATION`, or `OTHER` as sufficient. Consequently, events under two distinct incident nodes can still count as a compatible pair when those incident nodes share one of these broader ancestors. That is broader than an incident-bounded comparison and is not proven semantically safe by the current synthetic tests.

**Recommended rule for approval:** define the primary pair opportunity as two resolved event leaves that share the same nearest resolved `INCIDENT` ancestor. This keeps cross-host pairs within one incident while excluding pairs that only share a campaign/operation/report-level parent. Where no resolved incident ancestor exists, do not count a primary pair opportunity unless an explicit scope-compatibility decision mechanism is added. Preserve the existing nearest-common-non-report-ancestor rule as a separately labelled sensitivity analysis, not the primary denominator. This recommendation is not yet approved or implemented.

This is a **provisional operationalization**, not a researcher-approved scientific decision. The current module still computes the broad common-ancestor count and withholds compatible-pair and same-technique-pair opportunity rates unless the caller explicitly approves that rule with --approve-scope-pair-rule (or approve_scope_pair_rule=True in Python). Do not pass that approval flag for primary results until the scope rule is decided.

## Running the aggregator

Frozen source files remain local and are named REPORT_ID.txt in a source directory. No raw report text is written to the JSON result or committed to the repository.

From the repository root:

    python research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.2/analysis/report_level_aggregation.py \
      --sources-dir /path/to/local/frozen_sources \
      --confirm-selected-analysis-locks \
      --output /path/to/local/report_level_results.json

The --confirm-selected-analysis-locks flag is an explicit confirmation gate. It does not create or repair a lock: the adapter still recomputes the source/register/evidence/selection digest and requires an exact match to the SELECTED_FINAL row.

Only after the researcher approves the scope-pair rule, add:

    --approve-scope-pair-rule

Omitting either confirmation keeps the corresponding analysis blocked or its pair-opportunity rates withheld. A report-level JSON output can be created from a blank package, but it will correctly contain zero denominators and null rates rather than fabricated zero outcomes.

## Output interpretation

- denominators: N_eligible, N_assessable, and IDs explaining exclusions/conflicts.
- selection: selected-final coverage, blocked report IDs, validation errors, and explicit lock confirmation state.
- report_level_primary_rates: report-level rates on N_assessable, only when final-projection coverage is complete; otherwise null with a blocking status.
- selected_subset_descriptive_rates_not_population_estimates: descriptive rates for the subset already projected; never a replacement primary denominator.
- report_outcome_numerators and report_outcome_counts: counts for the successfully projected assessable subset.
- scope_pair_opportunity_rule: rule definition and approval state.
- projection_rates_and_counts: event-edge and event-to-technique-pair outcomes; unmapped endpoints are separate from omission.
- per_report_outcomes: one row per successfully projected report, with prior-exposure status retained for interpretation.

## Validation limits

The aggregator is a structural and arithmetic layer. It does not decide event identity, whether two scope descriptions are substantively comparable, whether a source entails a relation, whether a mapping is semantically correct, or whether a reviewer was genuinely independent. Those remain human research decisions. The current schema has an annotator_id but no machine-verifiable annotator-type field; the pipeline relies on the protocol/workflow convention that registered annotation partitions are human-owned and records AI assistance as prior exposure. It cannot authenticate a human identity or prevent a mislabelled automated partition by itself. It does not calculate inter-annotator agreement, prevalence confidence intervals, or benchmark alignment.

The implementation is currently synthetic-tested only. The selection register remains empty; there are no human annotations, selected final partitions, or real-report projections. A five-report feasibility batch is not a prevalence study.


## Extended metric-contract outputs

Per-report output now also carries source-scope/local-use/public-reuse/assessability/review states and reasons; mention status counts; activity-unit counts by granularity, role and instance status; count-status-by-granularity tables; temporal-relation counts by label and basis (including non-primary/inferred/transitive/ambiguous/not-assessable rows); and optional candidate-pair assessment label counts.

Mapping outputs separate accepted source-supported `A_exact` event coverage from baseline `A_120` coverage. Occurrence compression is reported as resolved event-leaf counts per exact and parent-level technique. The report-level and projected-subset outputs include relation-label breakdowns and the conditional within-technique-temporal-relation / same-technique-opportunity ratio; this conditional ratio is withheld until the scope-pair opportunity rule is approved.

Each per-report output preserves edge status, event-edge-to-technique-pair mappings, diagonal and distinct pairs, distinct-pair provenance, collision keys, excess edge multiplicity, label conflicts, and strict-order cycle provenance. These diagnostics remain nested under report IDs; the aggregator does not merge technique-pair keys or SCCs across reports.

The command-line entry point is exercised by a synthetic CLI test. It accepts a local source directory and writes JSON without copying source text. A custom extension path is supported when its RECON v0.1 base package is the sibling directory expected by the package layout.
