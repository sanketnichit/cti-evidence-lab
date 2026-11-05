# CTI Annotation Schema RECON v0.2 — temporal evidence extension

Status: draft for researcher review; not approved, frozen, or ready for real-report annotation.
Prepared: 5 November 2026
Parent: CTI Annotation Schema RECON v0.1.

## Purpose

The parent package records one primary evidence span for a temporal relation and permits generic additional evidence links. It does not distinguish evidence supporting endpoint A, endpoint B, or contextual material. This additive extension makes those roles explicit while leaving the v0.1 reconstruction unchanged. It does not claim to recover the missing original v0.4.2 schema or exact v0.4.1 protocol.

## Evidence roles

The primary_evidence_span_id on temporal_relations is the required RELATION_CUE. It is not repeated in the new register. The extension register stores EVENT_A_SUPPORT, EVENT_B_SUPPORT, and optional RELATION_CONTEXT rows. For endpoint-support rows, supported_event_id must equal the corresponding temporal relation endpoint. For context rows, supported_event_id must be empty. A single source span may support multiple functions through separate role rows.

Every positive direct_source or direct_timestamp relation eligible for the primary graph requires at least one EVENT_A_SUPPORT and one EVENT_B_SUPPORT. RELATION_CONTEXT is optional.

## Validation

The validator checks partition-local relation and span references, identifiers, role values, endpoint-role alignment, relation-cue presence and type, A/B completeness, and direct-timestamp linkage to normalized ATTACK_OCCURRENCE time evidence for each endpoint. The parent v0.1 validator continues to handle the existing schema checks.

This is structural validation only. It does not judge semantic evidence quality, infer event identity or relation direction, or decide whether timestamp uncertainty permits strict ordering. Interval-based uncertainty validation remains open. No real-report rows or human annotations are included.

## Files

- registers/temporal_relation_evidence.csv
- validator/validate_temporal_evidence.py
- tests/test_temporal_evidence.py
- schema_manifest.json

This extension is a testable design candidate, not an operational annotation instruction. Researcher review and protocol approval are still required.