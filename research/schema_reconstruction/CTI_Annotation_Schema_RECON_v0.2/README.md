# CTI Annotation Schema RECON v0.2 — temporal evidence extension

Status: draft for researcher review; not approved, frozen, or ready for real-report annotation. Prepared 5 November 2026. Parent: RECON v0.1.

## Purpose

The parent package stores one primary evidence span for each temporal relation and supports generic additional links. It does not distinguish evidence for endpoint A, endpoint B, and contextual material. This additive extension introduces those distinctions without changing v0.1 or claiming to recover the missing original v0.4.2 schema or exact v0.4.1 protocol.

## Evidence roles

The parent temporal relation's `primary_evidence_span_id` is the required `RELATION_CUE`; it is not duplicated in the extension register. The new register stores `EVENT_A_SUPPORT`, `EVENT_B_SUPPORT`, and optional `RELATION_CONTEXT` rows. Endpoint support must identify the matching event endpoint. Context rows must leave `supported_event_id` empty. One source span may serve more than one role through separate rows.

Every positive `direct_source` or `direct_timestamp` relation entering the primary graph requires at least one A-support and one B-support row. Context is optional.

## Validation and limits

The extension validator checks partition-local references, link identity, roles, endpoint alignment, cue presence/type, A/B completeness, and direct-timestamp support linkage to normalized `ATTACK_OCCURRENCE` time records. It is structural only: it does not judge semantic evidence quality, infer event identity or relation direction, or determine whether timestamp uncertainty permits strict order. Interval-based uncertainty validation remains open. No real-report rows or human annotations are included.

Run tests with `python -m unittest discover -s research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.2/tests -v`.

Validate the blank extension with the command shown in `SCHEMA_MANIFEST.md`.

## Files

- `registers/temporal_relation_evidence.csv`
- `validator/validate_temporal_evidence.py`
- `tests/test_temporal_evidence.py`
- `SCHEMA_MANIFEST.md`

This is a testable design candidate, not an operational annotation instruction. Researcher review and protocol approval are still required.