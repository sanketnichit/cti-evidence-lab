# Synthetic validation results — CTI Annotation Schema RECON v0.1

**Date:** 3 November 2026  
**Status:** Synthetic structural tests only. No human annotations or real AnnoCTR reports were used.

## Overall result

- Python compilation of all package Python modules: **PASS**
- `python -m unittest discover -s tests -v`: **40 tests passed**
  - Schema validator: 18
  - Projection metrics: 13
  - Annotation-to-projection adapter: 9
- Header-only blank-bundle check: 0 errors and 1 expected `EMPTY_ANNOTATION_BUNDLE` warning.
- Pinned derived A_120 vocabulary: 120 unique identifiers loaded and checked.

## Schema validator tests (1–17)

1. Valid two-event direct `BEFORE` relation is accepted.
2. Missing source text produces a warning rather than silently validating offsets.
3. Self-event temporal relation is rejected.
4. Container endpoint is rejected from the primary event graph.
5. Event endpoint outside the comparison-scope ancestry is rejected.
6. `workbook_only` cannot be accepted as a source mapping.
7. Technique outside A_120 is rejected.
8. Evidence text must equal the frozen source substring.
9. Duplicate evidence-link composite key is rejected.
10. `NO_TEMPORAL_CLAIM` is rejected in the positive relation register.
11. `NO_TEMPORAL_CLAIM` is permitted for a rule-versioned candidate-pair assessment.
12. An assessable eligible report with zero positive edges remains in the denominator.
13. Non-temporal relations do not enter the temporal-edge count.
14. IDs remain isolated by report / annotator / annotation pass; report-level denominator counts deduplicate repeated report IDs and expose partition counts separately.
15. Accepted source-supported mappings require their own mapping evidence link.
16. Scope hierarchy cycles are rejected.
17. Accepted A_120 mapping counts exclude container-unit mappings.

## Projection metric tests (18–30)

18. The four event-edge projection statuses are mutually exclusive and exhaustive.
19. `project_report_recon()` rejects self-event edges itself.
20. Unmapped endpoints are not mislabeled as fully omitted mapped edges.
21. `AFTER` direction is reversed for strict-order projection.
22. Symmetric temporal labels use unordered technique dyads.
23. Distinct-pair collisions and conflicting labels retain source-edge provenance.
24. Technique-cycle components preserve source event-edge provenance.
25. Single-event-edge mapping-fanout cycles are distinguished from multi-edge cycles.
26. Source event-graph cycles invalidate projection-induced cycle diagnostics.
27. Non-positive, inferred/transitive and scope-incompatible edges are rejected.
28. Alternative, workbook-only, out-of-vocabulary and container mappings are excluded from A_120.
29. Duplicate mapping IDs are rejected.
30. Zero-edge input returns undefined (`null`) edge rates rather than divide-by-zero values.

## Annotation-to-projection adapter tests (31–39)

31. A valid exact report/annotator/pass partition projects only eligible primary rows.
32. Mixed annotator rows do not leak across partitions.
33. Container mappings are excluded from the primary event mapping set.
34. Inferred/non-primary temporal relations are not projected.
35. Empty mapping sets keep event relations visible as unmapped-endpoint edges.
36. Scope or structural validation errors stop the adapter.
37. Incomplete report review stops the adapter.
38. Ineligible or locally unpermitted reports are blocked.
39. Explicit annotation-lock confirmation and a non-empty immutable lock reference are required.
40. Conflicting report-level eligibility, local-use or assessability decisions are warned and excluded from report-level denominators until adjudicated.

## Limitations

These tests establish only the synthetic structural behaviours listed above. They do not establish that a source interpretation is semantically correct, that the reconstructed schema is the original v0.4.2 schema, or that the protocol is researcher-approved. No AnnoCTR report has been entered or annotated. The annotation-to-projection adapter has not been run on a real report and its lock argument has only been exercised with a synthetic test reference.