# RECON v0.4 activity-stratum field dictionary

The v0.1 activity_units header is immutable within its reconstructed package. RECON v0.4 represents the logical activity_unit.activity_stratum field in a one-to-one companion register. This normalized representation is canonical for the v0.4 extension.

## activity_unit_strata.csv — exactly one stratum per activity unit

| Field | Required | Meaning |
|---|---:|---|
| report_id | yes | Report owning the annotation partition. |
| annotator_id | yes | Annotator identity. |
| annotation_pass_id | yes | Pass identity. |
| activity_unit_id | yes | FK to one activity_units.csv row in the same report/annotator/pass partition. |
| activity_stratum | yes | One of the six controlled strata below. |
| stratum_basis | yes | REPORT_EXPLICIT, SOURCE_SUPPORTED_HUMAN_JUDGMENT, or UNRESOLVED. |
| evidence_span_id | yes | FK to an evidence_spans.csv row in the same partition. Evidence grounding for the classification. |
| stratum_rationale | yes | Why the unit belongs to the selected stratum or why it cannot be resolved. |
| annotator_confidence | yes | HIGH, MEDIUM, or LOW. |
| adjudication_status | yes | UNREVIEWED, AGREED, or ADJUDICATED. |
| stratum_notes | no | Additional boundary or uncertainty detail. |

## activity_stratum_locks.csv

| Field | Required | Meaning |
|---|---:|---|
| report_id, annotator_id, annotation_pass_id | yes | Selected-final annotation partition. |
| analysis_lock_reference | yes | RECON v0.2 selected-analysis lock reference bound by this extension. |
| activity_strata_sha256 | yes | SHA-256 of canonical sorted stratum rows for this partition. |
| lock_reference | yes | SHA-256 lock over the format, partition, analysis lock reference and stratum-row digest. |
| lock_format | yes | CTI-EVIDENCE-LAB-ACTIVITY-STRATUM-LOCK-v1. |
| locked_by | yes | Researcher who created the lock. |
| lock_date | yes | ISO YYYY-MM-DD. |
| lock_notes | no | Lock context. |

A stratum lock is a mutation detector, not a digital signature and not proof of annotator identity.
