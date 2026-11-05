# CTI Annotation Schema RECON v0.2 — temporal evidence extension

Status: draft for researcher review; not approved, frozen, or ready for real-report annotation. Prepared 5 November 2026. Parent: RECON v0.1.

## Purpose

The parent package stores one primary evidence span for each temporal relation and supports generic additional links. It does not distinguish evidence for endpoint A, endpoint B, and contextual material. This additive extension introduces those distinctions without changing v0.1 or claiming to recover the missing original v0.4.2 schema or exact v0.4.1 protocol.

## Evidence roles

The parent temporal relation's primary_evidence_span_id is the required RELATION_CUE; it is not duplicated in the extension register. The new register stores EVENT_A_SUPPORT, EVENT_B_SUPPORT, and optional RELATION_CONTEXT rows. Endpoint support must identify the matching event endpoint. Context rows must leave supported_event_id empty. One source span may serve more than one role through separate rows.

Every positive direct_source or direct_timestamp relation entering the primary graph requires at least one A-support and one B-support row. A separate context span is optional for sentence and cross-sentence claims, but required with a non-empty rationale for DOCUMENT_CONTEXT claims. Section order alone is not temporal evidence.

## Validation and limits

The extension validator checks partition-local references, link identity, roles, endpoint alignment, cue presence/type, and evidence-scope completeness. SENTENCE requires cue and both endpoint-support roles to resolve to one sentence; CROSS_SENTENCE requires linked support outside the cue sentence with an explanatory argument/coreference note; DOCUMENT_CONTEXT requires a contextual span in a distinct section/paragraph passage, span-level evidence notes, and relation-level rationale. These are structural traceability checks, not semantic proof.

For direct-timestamp relations, the validator requires preserved raw time text and precision, explicit timezone status/text, populated normalized timezone, timezone-aware ISO-8601 bounds, and documented non-point intervals. Retained timestamp candidates that are not normalized are errors rather than silently ignored. Strict BEFORE/AFTER ordering must hold for every retained A/B interval combination; overlapping or uncertain windows cannot create a strict timestamp edge.

Run tests with:

    python -m unittest discover -s research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.2/tests -v

Validate the blank extension with the command shown in SCHEMA_MANIFEST.md.

## Files

- registers/temporal_relation_evidence.csv
- registers/analysis_partition_selection.csv
- validator/validate_temporal_evidence.py
- tests/test_temporal_evidence.py
- tests/test_analysis_partition_selection.py
- analysis/selected_partition_projection_adapter.py
- tests/test_selected_partition_projection_adapter.py
- docs/SELECTED_PARTITION_PROJECTION_ADAPTER_v0.2.md
- analysis/report_level_aggregation.py
- tests/test_report_level_aggregation.py
- docs/REPORT_LEVEL_AGGREGATION_v0.1.md
- SCHEMA_MANIFEST.md

The protocol-to-schema comparison and remaining implementation limits are recorded in research/protocol/PROTOCOL_V0_5_RECON_V0_2_CONFORMANCE_AUDIT_v0.1.md.

This is a testable design candidate, not an operational annotation instruction. Researcher review and protocol approval are still required.

## Final analysis partition selection

analysis_partition_selection.csv records the report-level partition chosen for analysis. It allows at most one SELECTED_FINAL partition per report. A final selection must resolve to an existing report/annotator/pass row, and the underlying report must be eligible, permitted for local use, assessable, and fully reviewed. A final selection also records a role, rationale, date, and SHA-256 lock reference. Solo work is labelled SINGLE_ANNOTATOR_FINAL; repeated passes are not independent annotators.

The selection register remains header-only. A v0.2 projection wrapper is implemented and synthetic-tested. It resolves exactly one selected-final row, validates the temporal evidence register, and verifies a lock that covers the v0.1 source/register lock, v0.2 temporal-evidence rows, and final-selection decision. It delegates only after those checks to the unchanged v0.1 adapter.

## Report-level aggregation

analysis/report_level_aggregation.py aggregates one selected-final partition per assessable report. It separates N_eligible, N_assessable, the mandatory N_assessable/N_eligible coverage rate, and successful selected-final projection coverage. It reports one-report-one-count distributions for source-scope, local-use, assessability and review states, plus IDs/reasons for pending, excluded, unreviewed, source-unverified and conflicting cases. It verifies the exact frozen source hash and character count, excludes report-level decision/source-version conflicts, and withholds primary rates until every N_assessable report has a valid selected-final projection. Per-report projection diagnostics are summed within reports and are never merged into cross-report technique-pair keys.

The opportunity measure needs an approved operational scope-pair rule. The current code uses the nearest common resolved non-report ancestor, which can count event pairs under separate incident nodes when they share a broader campaign/operation ancestor. Candidate resolutions are (a) a shared nearest resolved INCIDENT ancestor, or (b) an explicit comparison-scope assignment on each event that both endpoints must share. These choices also need to align primary relation eligibility and the conditional-rate numerator/denominator. Neither has been approved or implemented; pair-opportunity rates remain withheld. A synthetic test now reproduces the cross-incident inclusion under the current broad rule. See docs/REPORT_LEVEL_AGGREGATION_v0.1.md.

The aggregation layer has synthetic helper tests and an end-to-end selected-final fixture test. There are no human AnnoCTR annotations, selected final partitions, or real-report projections. The current blank package therefore returns zero denominators and null rates, not empirical zero outcomes.

The output also includes count-status-by-granularity, mention and relation missingness, `A_exact` versus `A_120` coverage, occurrence compression by technique, and report-scoped collision/cycle provenance. Conditional rates that depend on the provisional scope-pair rule are withheld until approval. The CLI path is covered by a blank-package smoke test and never writes frozen source text to JSON.


## RECON v0.3 explicit comparison-scope assignment candidate

A sibling RECON v0.3 draft is available at ../CTI_Annotation_Schema_RECON_v0.3/. It adds source-evidence-backed per-event comparison-scope assignments and a lock bound to the v0.2 selected-analysis lock. The v0.2 aggregator can compare the legacy broad rule, a shared-INCIDENT rule, and the v0.3 explicit-assignment candidate. The v0.3 extension remains unapproved and synthetic-only; do not start human annotation until the protocol and scope policy are reviewed and frozen.
