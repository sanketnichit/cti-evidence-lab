# CTI Annotation Schema RECON v0.2 — temporal evidence extension

Status: draft for researcher review; not approved, frozen, or ready for real-report annotation. Prepared 5 November 2026. Parent: RECON v0.1.

## Purpose

The parent package stores one primary evidence span for each temporal relation and supports generic additional links. It does not distinguish evidence for endpoint A, endpoint B, and contextual material. This additive extension introduces those distinctions without changing v0.1 or claiming to recover the missing original v0.4.2 schema or exact v0.4.1 protocol.

## Evidence roles

The parent temporal relation's `primary_evidence_span_id` is the required `RELATION_CUE`; it is not duplicated in the extension register. The new register stores `EVENT_A_SUPPORT`, `EVENT_B_SUPPORT`, and optional `RELATION_CONTEXT` rows. Endpoint support must identify the matching event endpoint. Context rows must leave `supported_event_id` empty. One source span may serve more than one role through separate rows.

Every positive `direct_source` or `direct_timestamp` relation entering the primary graph requires at least one A-support and one B-support row. A separate context span is optional for sentence and cross-sentence claims, but required with a non-empty rationale for `DOCUMENT_CONTEXT` claims. Section order alone is not temporal evidence.

## Validation and limits

The extension validator checks partition-local references, link identity, roles, endpoint alignment, cue presence/type, A/B completeness, and direct-timestamp support linkage. Strict `BEFORE`/`AFTER` timestamp relations require timezone-aware ISO-8601 bounds, explicit timezone status, a populated normalized timezone, and documented non-point intervals. The ordering must hold for every retained A/B interval combination; overlapping or uncertain windows cannot create a strict timestamp edge. This remains a structural check, not a semantic judgement that source text entails the relation.

Run tests with `python -m unittest discover -s research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.2/tests -v`.

Validate the blank extension with the command shown in `SCHEMA_MANIFEST.md`.

## Files

- `registers/temporal_relation_evidence.csv`
- `registers/analysis_partition_selection.csv`
- `validator/validate_temporal_evidence.py`
- `tests/test_temporal_evidence.py`
- `tests/test_analysis_partition_selection.py`
- `SCHEMA_MANIFEST.md`

This is a testable design candidate, not an operational annotation instruction. Researcher review and protocol approval are still required.
## Final analysis partition selection

`analysis_partition_selection.csv` records the report-level partition chosen for analysis. It allows at most one `SELECTED_FINAL` partition per report. A final selection must resolve to an existing report/annotator/pass row, and the underlying report must be eligible, permitted for local use, assessable, and fully reviewed. A final selection also records a role, rationale, date, and SHA-256 lock reference. Solo work is labelled `SINGLE_ANNOTATOR_FINAL`; repeated passes are not independent annotators.

The selection register is header-only. The current projection adapter has not yet been migrated to consume the selected-final register and verify its lock against frozen source and partition rows. **Do not use the adapter to create study projection results until that migration is complete.**
