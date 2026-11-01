# Annotation Template Files

These blank CSV files are data-entry templates for the human pilot. They contain no report text or AI-generated labels.

## Files and row granularity

- `report_registry.csv`: one row per report and annotator/reviewer provenance check.
- `event_mentions.csv`: one row per text mention. Character offsets are zero-based and end-exclusive into the frozen source text.
- `event_mappings.csv`: one row per mapping evidence span. Multiple rows can share a `mapping_id` when one mapping needs multiple evidence spans. For an event without a supported ATT&CK mapping, use one row with `mapping_status=UNMAPPED` and leave technique/evidence fields blank.
- `temporal_relations.csv`: one row per relation evidence span. Multiple rows can share a `relation_id` when a cross-sentence relation needs multiple spans. For `NO_TEMPORAL_CLAIM` or `NOT_ASSESSABLE`, evidence can remain empty. Positive temporal and non-temporal relations require evidence.

## Labels

Use the exact labels and distinctions in `research/ANNOTATION_PROTOCOL_v0.2.md`. Do not infer event order from sentence order. Do not count repeated technique mentions as multiple executions. Do not treat an ATT&CK technique as an event instance.

The projection prototype accepts only these positive temporal labels:
`BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, `CONCURRENT_UNSPECIFIED`.
It rejects assessment labels such as `NO_TEMPORAL_CLAIM`, `VAGUE_OR_AMBIGUOUS` and `NOT_ASSESSABLE`, as well as dependency/narrative labels. These remain in the annotation CSV but are not positive temporal graph edges.

## Validation

Once the CSV files are populated, run from the repository root:

```bash
python -m src.annotation_validation \
  --report-id REPORT_ID \
  --text path/to/frozen_report.txt \
  --mentions research/templates/event_mentions.csv \
  --mappings research/templates/event_mappings.csv \
  --relations research/templates/temporal_relations.csv
```

The validator checks source-span integrity, identifier references, event status consistency, mapping evidence, and relation evidence. It does not determine whether a human's semantic decision is correct.
