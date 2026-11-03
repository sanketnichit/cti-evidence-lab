# Annotation-to-projection adapter — RECON v0.1

**Status:** Local, provisional integration layer. Synthetic tests only. Not connected to the public GitHub project and not run on AnnoCTR candidate reports.

## Purpose

`analysis/annotation_projection_adapter.py` is the narrow bridge between the reconstructed 12-register schema and `analysis/projection_metrics_recon.py`. It prevents the metric function from being called directly on arbitrary/unvalidated CSV rows.

## Required inputs

- exact `report_id`, `annotator_id`, and `annotation_pass_id`;
- the exact frozen source text for that report;
- explicit `annotation_lock_confirmed=True` and a non-empty immutable `annotation_lock_reference` (for example, the checksum/reference for the read-only locked annotation snapshot).

The explicit lock arguments default to false/empty, and the adapter refuses to proceed without them. A completed report-review status alone is not treated as an annotation lock.

## Fail-closed gates

1. Run `validate_annotations.validate_bundle()` with the supplied source text before building projection inputs.
2. Stop if any structural validation error exists.
3. Require exactly one matching report registry row.
4. Require `source_scope_eligibility=ELIGIBLE`, `local_research_use_status=PERMITTED`, `report_assessability=ASSESSABLE`, and `full_report_review_status=COMPLETE`.
5. Select only `event_leaf` + `atomic_event` + `RESOLVED` activity units.
6. Build A_120 only from accepted, source-supported mappings with `baseline_mapping_status=IN_VOCAB` and pinned vocabulary membership/hash.
7. Pass only positive temporal labels with `direct_source`/`direct_timestamp` basis and `scope_compatibility=COMPATIBLE` to projection. Other temporal records remain in the source registers and are not treated as negative examples.
8. Pass the exact report/annotator/pass partition only; other annotation partitions cannot leak into the calculation.

## Output and limits

The adapter returns counts, mapping-filter exclusions, source and A_120 hashes, validator warnings, the annotation-lock reference, and projection results. It does not include raw source text. It does not decide semantic correctness. Any annotation-lock reference supplied by a future caller must correspond to an actual human-approved, immutable annotation snapshot; a synthetic test string is used only inside tests.

## Synthetic coverage

Nine adapter tests cover valid projection, mixed-annotator partition isolation, container mapping exclusion, non-primary relation filtering, empty mapping sets, scope/structural error blocking, incomplete report blocking, local-use eligibility blocking, and the required explicit annotation-lock reference. No AnnoCTR data were used.
