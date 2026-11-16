# RECON v0.3 extension field dictionary

**Status:** draft extension; researcher review required.  
**Parent:** RECON v0.2 selected-analysis partition and temporal-evidence layer.  
**Scope:** the two additive v0.3 registers. The v0.1/v0.2 field definitions are inherited unchanged.

## `event_comparison_scope_assignments.csv` — per-event comparison-scope decisions

| Field | Requiredness | Meaning |
|---|---|---|
| `report_id` | yes | Report owning the annotation partition. |
| `annotator_id` | yes | Annotator partition identity. |
| `annotation_pass_id` | yes | Annotation pass identity. |
| `assignment_id` | yes | Unique assignment-row ID within the partition. |
| `activity_unit_id` | yes | FK to a RESOLVED atomic `event_leaf` in the same partition. |
| `comparison_scope_id` | yes | FK to a RESOLVED comparable non-report scope in the same partition and in the event's resolved scope ancestry. |
| `assignment_status` | yes | `ASSIGNED`, `NOT_ASSIGNED`, or `UNCERTAIN`. |
| `assignment_basis` | yes | `REPORT_EXPLICIT`, `SOURCE_SUPPORTED_HUMAN_JUDGMENT`, or `UNRESOLVED`. |
| `evidence_span_id` | conditional | Required for ASSIGNED and NOT_ASSIGNED. UNCERTAIN may leave it blank; any populated value must resolve in the same partition. |
| `assignment_rationale` | yes | Non-empty explanation for the decision. |
| `annotator_confidence` | yes | HIGH, MEDIUM, or LOW. |
| `adjudication_status` | yes | UNREVIEWED only in this draft; the v0.3 assignment register has no dedicated adjudication log. |
| `assignment_notes` | no | Additional context or uncertainty detail. |

Every eligible resolved non-report comparable ancestor scope for every RESOLVED atomic event leaf must receive one explicit decision in the partition. Missing decisions are incomplete review, not implicit NOT_ASSIGNED. Duplicate assignment IDs and duplicate event/scope decisions fail validation. ASSIGNED and NOT_ASSIGNED require source evidence and a REPORT_EXPLICIT or SOURCE_SUPPORTED_HUMAN_JUDGMENT basis. UNCERTAIN requires basis UNRESOLVED. A primary positive temporal relation or COMPATIBLE candidate-pair assessment using the explicit-scope rule must cite a scope assigned to both endpoints.

## `comparison_scope_assignment_locks.csv` — assignment-register lock

| Field | Requiredness | Meaning |
|---|---|---|
| `report_id` | yes | Report owning the selected analysis partition. |
| `annotator_id` | yes | Selected annotator. |
| `annotation_pass_id` | yes | Selected annotation pass. |
| `lock_id` | yes | Unique ID for the scope-assignment lock within the lock file. |
| `analysis_lock_reference` | yes | The selected partition's v0.2 analysis-lock reference. |
| `assignment_rows_sha256` | yes | SHA-256 of canonical sorted assignment rows for the partition. |
| `lock_reference` | yes | SHA-256 digest binding the v0.3 lock format, partition, v0.2 analysis-lock reference, and assignment-row digest. |
| `lock_format` | yes | Fixed value `CTI-EVIDENCE-LAB-COMPARISON-SCOPE-LOCK-v0.3`. |
| `locked_by` | yes | Non-empty lock creator/researcher identifier. |
| `lock_date` | yes | ISO `YYYY-MM-DD` lock date. |
| `lock_notes` | no | Additional lock context. |

One lock is required for each SELECTED_FINAL partition when the v0.3 explicit-assignment sensitivity is used. The lock is bound to the v0.2 selected-analysis lock and the complete assignment register. It is a mutation detector, not a digital signature or proof of annotator identity.
