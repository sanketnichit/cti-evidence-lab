# Synthetic validation results — CTI Annotation Schema RECON v0.1

**Date:** 4 November 2026  
**Status:** Synthetic structural tests only. No human annotations or real AnnoCTR reports were used.

## Overall result

- Python compilation of all package Python modules: **PASS**
- `python -m unittest discover -s tests -v`: **56 tests passed**
  - Schema validator: 29
  - Projection metrics: 16
  - Annotation-to-projection adapter: 11
- Header-only blank-bundle check: 0 errors and 1 expected `EMPTY_ANNOTATION_BUNDLE` warning.
- Pinned derived A_120 vocabulary: 120 unique identifiers loaded and checked.

## Schema validator tests (1–29)

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
18. A top-level exact technique must map to itself as its parent.
19. Sub-technique parent classification fails closed until a verified crosswalk is integrated.
20. Merely placing a crosswalk file at the expected path does not bypass validation.
21. Prior-exposure status is a controlled value.
22. `direct_timestamp` requires normalized, evidence-linked time records for both endpoints.
23. A valid `direct_timestamp` relation passes when both endpoints have normalized, evidence-linked time records.
24. Duplicate temporal relations are rejected.
25. Reciprocal `BEFORE` relations for the same event pair are rejected.
26. Contradictory `BEFORE` and `OVERLAP` claims for the same event pair are rejected.
27. Conflicting report-level eligibility/local-use/assessability decisions are warned and excluded from report-level denominators until adjudicated.
28. CRLF source text is hashed and offset-checked without newline translation.
29. Positive candidate-pair assessments must match their linked temporal relation's event pair and label.

## Projection metric tests (30–45)

30. The four event-edge projection statuses are mutually exclusive and exhaustive.
31. `project_report_recon()` rejects self-event edges itself.
32. Unmapped endpoints are not mislabeled as fully omitted mapped edges.
33. `AFTER` direction is reversed for strict-order projection.
34. Symmetric temporal labels use unordered technique dyads.
35. Distinct-pair collisions and conflicting labels retain source-edge provenance.
36. Technique-cycle components preserve source event-edge provenance.
37. Single-event-edge mapping-fanout cycles are distinguished from multi-edge cycles.
38. Source event-graph cycles invalidate projection-induced cycle diagnostics.
39. Non-positive, inferred/transitive and scope-incompatible edges are rejected.
40. Alternative, workbook-only, out-of-vocabulary and container mappings are excluded from A_120.
41. Duplicate mapping IDs are rejected.
42. Zero-edge input returns undefined (`null`) edge rates rather than divide-by-zero values.
43. Inverse `AFTER` and `BEFORE` claims normalize to one strict-order pair and do not create a label conflict.
44. A strict-order claim and `OVERLAP` remain a pair-level label conflict.
45. Adding a redundant source edge does not hide a cycle induced by one source edge's mapping fan-out.

## Annotation-to-projection adapter tests (46–56)

46. A valid exact report/annotator/pass partition projects only eligible primary rows.
47. Mixed annotator rows do not leak across partitions.
48. Container mappings are excluded from the primary event mapping set.
49. Inferred/non-primary temporal relations are not projected.
50. Empty mapping sets keep event relations visible as unmapped-endpoint edges.
51. Scope or structural validation errors stop the adapter.
52. Incomplete report review stops the adapter.
53. Ineligible or locally unpermitted reports are blocked.
54. Explicit annotation-lock confirmation and a non-empty lock reference are required.
55. Arbitrary or stale lock references are rejected against the computed partition digest.
56. Prior-exposure status and the associated caution flag are exposed in projection output.

## Limitations

These tests establish only the synthetic structural behaviours listed above. They do not establish that a source interpretation is semantically correct, that the reconstructed schema is the original v0.4.2 schema, or that the protocol is researcher-approved. No AnnoCTR report has been entered or annotated. The annotation-to-projection adapter has not been run on a real report and its lock has only been exercised with synthetic fixture rows and source text.
