# RECON v0.2 extension controlled vocabularies

**Status:** working reconstruction documentation; researcher review required. Values inherited from v0.1 remain defined in the v0.1 controlled-vocabulary document.

## `temporal_relation_evidence.csv`

### `evidence_role`

- `EVENT_A_SUPPORT` — source span supporting the event named by `temporal_relations.event_a_id`.
- `EVENT_B_SUPPORT` — source span supporting the event named by `temporal_relations.event_b_id`.
- `RELATION_CONTEXT` — source span providing contextual evidence for the relation; `supported_event_id` must be blank and `evidence_notes` must explain the contextual connection.

The relation cue is the base relation's `primary_evidence_span_id` and has `span_kind=RELATION`; it is not an extension-register evidence role.

## `analysis_partition_selection.csv`

### `partition_role`

- `DEVELOPMENT`
- `REPEAT`
- `INDEPENDENT`
- `CONSENSUS`
- `ADJUDICATED_FINAL`
- `SINGLE_ANNOTATOR_FINAL`

Only CONSENSUS, ADJUDICATED_FINAL and SINGLE_ANNOTATOR_FINAL are final roles eligible for SELECTED_FINAL. The validator imposes additional evidence requirements on each final role.

### `selection_status`

- `PENDING` — no final selection decision has been made.
- `NOT_SELECTED` — the partition was reviewed/considered but is not the report's final analysis partition.
- `SELECTED_FINAL` — the single partition selected for report-level analysis.

A report may have at most one SELECTED_FINAL row. Non-final rows cannot carry a lock reference.

## Inherited temporal values used by the extension

The v0.2 validator uses v0.1 temporal-relation labels, relation bases, evidence scopes, time types, and confidence values. The v0.2 timestamp gate further restricts timestamp-derived positives to strict BEFORE/AFTER; OVERLAP, SIMULTANEOUS, and CONCURRENT_UNSPECIFIED require an explicit direct-source assertion. Time precision and timezone-status sets are repeated in the v0.2 validator to validate endpoint intervals; see the v0.1 vocabulary file and `research/protocol/TIMESTAMP_RELATION_SEMANTICS_v0.1.md` for the inherited definitions and working timestamp semantics.

These vocabularies describe the current reconstructed implementation. They do not claim to recover the missing original v0.4.2 schema.
