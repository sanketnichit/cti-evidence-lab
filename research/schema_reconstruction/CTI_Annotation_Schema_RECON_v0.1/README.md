# CTI Annotation Schema RECON v0.1

<badge>RECONSTRUCTION / NOT ORIGINAL v0.4.2</badge>

**Status:** draft reconstruction; not approved, frozen, or ready for human annotation.  
**Prepared:** 3 November 2026  
**Purpose:** a coherent replacement schema design based on recovered Protocol v0.4-draft, its migration note, the v0.4.2 conformance audit, and public v0.3 templates.

## Important provenance warning

The original `CTI_Annotation_Schema_v0.4.2-draft.zip` and exact `CTI_Event_Instance_Annotation_Protocol_v0.4.1-draft.md` were not recovered. These are newly designed register templates, not recovered original headers. Do not cite, publish, or describe this package as the original v0.4.2. The exact original may differ.

## Contents

- `registers/` — 12 blank CSV templates (header rows only; no annotations).
- `vocabulary/A_120_ChronoCTI_Selected_Technique_IDs_derived_v0.1.json` — ordered, identifier-only extraction from the ChronoCTI temporal learner's selected-120 source file.
- `docs/FIELD_DICTIONARY.md` — field definitions, requiredness, types, and evidence status.
- `docs/CONTROLLED_VOCABULARIES.md` — confirmed v0.4 vocabularies and explicitly provisional reconstruction enums.
- `docs/DATA_MODEL_AND_VALIDATION_RULES.md` — keys, foreign keys, eligibility gates, and cross-register invariants.
- `docs/METRIC_CONTRACT_REFERENCE.md` — current provisional metric contract.
- `docs/PROJECTION_METRICS_RECON_v0.1.md` — projection metric definitions and implementation limits.
- `docs/ANNOTATION_PROJECTION_ADAPTER_RECON_v0.1.md` — adapter gates, lock requirement and limitations.
- `validator/validate_annotations.py` — structural validator for the reconstructed schema.
- `analysis/projection_metrics_recon.py` — provisional event-to-technique projection metrics (only accepts validated primary input).
- `analysis/annotation_projection_adapter.py` — fail-closed adapter from one validated, explicitly locked report/annotator/pass partition to projection input.
- `tests/` — synthetic positive and negative tests for schema validation, projection metrics, and the annotation-to-projection adapter (no human labels).
- `schema_manifest.json` and `SHA256SUMS.txt` — package identity and integrity manifest.

## Register grain

| Register | Row grain |
|---|---|
| `report_registry.csv` | one report × annotator × annotation pass |
| `report_scopes.csv` | one report-local scope × annotator × pass |
| `activity_units.csv` | one report-local activity unit × annotator × pass |
| `event_mentions.csv` | one source-text mention × annotator × pass |
| `evidence_spans.csv` | one exact source evidence span × annotator × pass |
| `record_evidence_links.csv` | one record-to-evidence link × annotator × pass |
| `event_mappings.csv` | one mapping decision for one activity unit × annotator × pass |
| `time_evidence.csv` | one typed time observation × annotator × pass |
| `temporal_relations.csv` | one event-pair temporal relation × annotator × pass |
| `candidate_pair_assessments.csv` | one candidate pair assessed under one rule/version × annotator × pass |
| `non_temporal_relations.csv` | one non-temporal relation between activity units × annotator × pass |
| `adjudication_log.csv` | one append-only adjudication decision |

## Evidence handling

`evidence_spans.csv` is the canonical store for exact text spans. Direct `primary_evidence_span_id` fields identify the primary evidence span on mentions, times, temporal relations and non-temporal relations. `record_evidence_links.csv` stores additional spans, not duplicates of the primary span. Source text uses strict UTF-8; an optional leading UTF-8 BOM is removed, CRLF/LF line endings are preserved, and no Unicode normalization is applied. `source_text_sha256` hashes the UTF-8 bytes of that exact decoded annotation text. Offsets are zero-based, end-exclusive Python Unicode code-point indices into the same decoded text; they are not byte or UTF-16 offsets.

## Primary analysis gates

Only resolved `event_leaf` activity units with `atomic_event` granularity may enter the primary event graph. Temporal edges additionally require distinct endpoints, compatible recorded comparison scope, relation-specific evidence and `direct_source` or `direct_timestamp` relation basis. Primary mapping comparisons use accepted source-supported IDs from the pinned A_120 list; `workbook_only` and alternative-only mappings are excluded.

## Validator and synthetic tests

Run the synthetic test suite from this directory with Python 3.10 or later (58 tests across the validator, projection module, and fail-closed adapter: 31 validator, 16 projection, 11 adapter):

```bash
python -m unittest discover -s tests -v
```

The suite covers the schema validator, provisional projection module and annotation-to-projection adapter; it currently contains 58 synthetic tests. None are real report annotations. The projection module is not the public GitHub implementation and has not been run on real annotations.

Run the validator against the blank package (this should report an empty-bundle warning, not an annotation success):

```bash
python validator/validate_annotations.py --bundle .
```

For a populated copy, place frozen UTF-8 source files at `sources/REPORT_ID.txt` and run:

```bash
python validator/validate_annotations.py --bundle . --sources-dir sources --json-out validation_report.json
```

The validator checks structure, identifiers, cross-register references, report/annotator/pass isolation, source hashes and exact offsets (when text is supplied), A_120 membership, activity-unit eligibility, evidence links, temporal relation eligibility, and denominator bookkeeping. It does **not** judge semantic correctness or whether a human interpretation is genuinely supported by the report. Synthetic tests do not validate real annotations.

## Not yet approved

This package encodes a provisional set of design choices. In particular, report-assessability enums, some scope/time/evidence-role enums, mapping decision states, and selected-120 vocabulary linkage must be reviewed and approved before the schema is frozen. The test suite is synthetic only. Do not annotate the five AnnoCTR candidates using these templates until the protocol decisions and validator gates are completed.
