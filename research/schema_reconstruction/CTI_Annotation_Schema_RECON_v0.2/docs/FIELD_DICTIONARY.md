# RECON v0.2 extension field dictionary

**Status:** working reconstruction documentation; researcher review required.  
**Parent:** RECON v0.1.  
**Scope:** the two additive registers introduced by RECON v0.2. Base-register fields remain defined by the v0.1 field dictionary.

## `temporal_relation_evidence.csv` — endpoint and context evidence links

| Field | Requiredness | Meaning |
|---|---|---|
| `report_id` | yes | Report owning the annotation partition. |
| `annotator_id` | yes | Annotator partition identity. |
| `annotation_pass_id` | yes | Annotation pass identity. |
| `relation_evidence_id` | yes | Unique ID for this relation/evidence-role link within the partition. |
| `relation_id` | yes | FK to `temporal_relations.relation_id` in the same partition. |
| `evidence_span_id` | yes | FK to `evidence_spans.evidence_span_id` in the same partition. |
| `evidence_role` | yes | `EVENT_A_SUPPORT`, `EVENT_B_SUPPORT`, or `RELATION_CONTEXT`. The primary relation cue remains in `temporal_relations.primary_evidence_span_id`; it is not duplicated here. |
| `supported_event_id` | conditional | Must equal `event_a_id` for EVENT_A_SUPPORT or `event_b_id` for EVENT_B_SUPPORT. Must be blank for RELATION_CONTEXT. |
| `evidence_notes` | conditional | Explanation for contextual spans, cross-sentence endpoint support, and any other evidence link whose locator/role needs explanation. Required for RELATION_CONTEXT; validator-specific evidence-scope rules require it for cross-sentence support. |

The composite relation/span/role/event assignment must be unique. A positive direct-source or direct-timestamp relation entering the primary graph requires at least one A-support and one B-support row. These are structural traceability rules; they do not establish that a span semantically entails a relation.

## `analysis_partition_selection.csv` — report-level selected analysis partition

| Field | Requiredness | Meaning |
|---|---|---|
| `report_id` | yes | Report being assigned one analysis-partition decision. |
| `analysis_partition_id` | yes | Unique selection-row ID within the report. |
| `annotator_id` | yes | Annotator whose report/pass partition is being considered. |
| `annotation_pass_id` | yes | Pass whose report partition is being considered. |
| `partition_role` | yes | `DEVELOPMENT`, `REPEAT`, `INDEPENDENT`, `CONSENSUS`, `ADJUDICATED_FINAL`, or `SINGLE_ANNOTATOR_FINAL`. |
| `selection_status` | yes | `PENDING`, `NOT_SELECTED`, or `SELECTED_FINAL`. |
| `lock_reference` | conditional | Required for SELECTED_FINAL and must be `sha256:` followed by 64 lowercase hexadecimal characters. Must be blank for PENDING and NOT_SELECTED. |
| `selection_rationale` | conditional | Required for NOT_SELECTED and SELECTED_FINAL. May be blank while PENDING. |
| `selection_date` | conditional | Required for SELECTED_FINAL; must be ISO `YYYY-MM-DD`. |

The selected row must resolve to an existing report/annotator/pass record in the v0.1 `report_registry`. A report may have at most one SELECTED_FINAL row. A selected-final partition requires source-scope eligibility, local research-use permission, ASSESSABLE report status, and COMPLETE full-report review. SINGLE_ANNOTATOR_FINAL requires exactly one registered annotator ID for the report. CONSENSUS requires at least two distinct completed INDEPENDENT input partitions, each recorded as NOT_SELECTED. ADJUDICATED_FINAL requires a valid ADJUDICATED field-history entry in the same report/annotator/pass partition.

The selected-analysis lock binds the v0.1 annotation/source lock, all v0.2 temporal-relation evidence rows for the selected partition, and the selected-final decision. It detects changes; it is not an identity signature or proof of human review.
