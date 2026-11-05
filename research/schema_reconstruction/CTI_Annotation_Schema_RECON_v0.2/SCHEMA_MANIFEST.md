# Schema manifest — RECON v0.2 temporal evidence extension

- Version: 0.2
- Prepared: 5 November 2026
- Status: draft; researcher review required; not approved or frozen
- Type: additive extension
- Parent: `../CTI_Annotation_Schema_RECON_v0.1`
- Real report rows: 0
- Synthetic tests only: yes
- Semantic evidence review: not performed
- Strict timestamp uncertainty ordering: implemented as a conservative structural gate for direct timestamp BEFORE/AFTER relations

## Evidence roles

- `RELATION_CUE`: required; stored in `temporal_relations.primary_evidence_span_id`.
- `EVENT_A_SUPPORT`: required; stored in `temporal_relation_evidence.csv`.
- `EVENT_B_SUPPORT`: required; stored in `temporal_relation_evidence.csv`.
- `RELATION_CONTEXT`: optional for sentence/cross-sentence claims; required with a non-empty rationale for `DOCUMENT_CONTEXT` claims.

This extension does not replace or alter RECON v0.1 and does not claim equivalence to the missing original v0.4.2 schema.
## Timestamp gate

- Time evidence must have `timezone_status=EXPLICIT` and a populated `normalized_timezone`.
- Normalized bounds must be timezone-aware ISO-8601 values and start must not follow end.
- Non-point intervals require `uncertainty_notes`.
- For direct timestamp `BEFORE`/`AFTER`, the strict order must hold for every retained A/B interval combination.

## Final analysis partition

- Register: `registers/analysis_partition_selection.csv`.
- At most one `SELECTED_FINAL` row per report.
- The selected partition must resolve in `report_registry`, with eligible source scope, permitted local use, assessable report, and complete full-report review.
- Final rows require a role, rationale, ISO date, and `sha256:<64 lowercase hex>` lock reference.
- The v0.2 selected-partition projection wrapper is implemented and covered by synthetic tests.
- The wrapper verifies a second lock over the v0.1 source/register lock, v0.2 temporal-evidence rows, and final-selection decision; it delegates to the unchanged v0.1 adapter only after both v0.2 and v0.1 validation pass.
- The selection register remains header-only; there is no selected report and no real-report projection.
