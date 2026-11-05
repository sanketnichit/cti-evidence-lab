# Synthetic validation results — CTI Annotation Schema RECON v0.1

**Date:** 5 November 2026  
**Status:** Synthetic structural tests only. No human annotations or real AnnoCTR reports were used.

## Overall result

- Python compilation of all package Python modules: **PASS**
- `python -m unittest discover -s tests -v`: **64 tests**
  - Schema validator: 37
  - Projection metrics: 16
  - Annotation-to-projection adapter: 11
- ATT&CK v12.1 crosswalk: 737 unique exact IDs; 333 top-level; 404 sub-techniques; all 404 resolve to valid explicit parent rows; 120/120 A_120 members are top-level self-mappings. Independent CSV SHA-256 recomputation matched the manifest.
- Header-only blank-bundle check: 0 errors and 1 expected `EMPTY_ANNOTATION_BUNDLE` warning.
- Pinned derived A_120 vocabulary: 120 unique identifiers loaded and checked.

## Schema validator tests (1–37)

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
19. Sub-technique parent comes from the pinned v12.1 STIX crosswalk.
20. A wrong but valid A_120 parent is rejected.
21. An exact ID absent from the pinned release is rejected.
22. ATT&CK release mismatch is rejected.
23. A revoked sub-technique cannot be counted in primary A_120.
24. Crosswalk hash mismatch is rejected.
25. Crosswalk manifest source pins are checked.
26. Prior-exposure status is a controlled value.
27. `direct_timestamp` requires normalized, evidence-linked time records for both endpoints.
28. A valid `direct_timestamp` relation passes when both endpoints have normalized, evidence-linked time records.
29. Duplicate temporal relations are rejected.
30. Reciprocal `BEFORE` relations for the same event pair are rejected.
31. Contradictory `BEFORE` and `OVERLAP` claims for the same event pair are rejected.
32. Conflicting report-level eligibility/local-use/assessability decisions are warned and excluded from report-level denominators until adjudicated.
33. CRLF source text is hashed and offset-checked without newline translation.
34. Positive candidate-pair assessments must match their linked temporal relation's event pair and label.
35. A fully reviewed assessable report with zero resolved event leaves remains in `N_assessable`.
36. An otherwise assessable report with an incomplete full-report review is not yet counted in `N_assessable`.
37. Candidate-pair assessment endpoints must be resolved atomic event leaves; unresolved/container endpoints are rejected.

## Projection metric tests (38–53)

38. The four event-edge projection statuses are mutually exclusive and exhaustive.
39. `project_report_recon()` rejects self-event edges itself.
40. Unmapped endpoints are not mislabeled as fully omitted mapped edges.
41. `AFTER` direction is reversed for strict-order projection.
42. Symmetric temporal labels use unordered technique dyads.
43. Distinct-pair collisions and conflicting labels retain source-edge provenance.
44. Technique-cycle components preserve source event-edge provenance.
45. Single-event-edge mapping-fanout cycles are distinguished from multi-edge cycles.
46. Source event-graph cycles invalidate projection-induced cycle diagnostics.
47. Non-positive, inferred/transitive and scope-incompatible edges are rejected.
48. Alternative, workbook-only, out-of-vocabulary and container mappings are excluded from A_120.
49. Duplicate mapping IDs are rejected.
50. Zero-edge input returns undefined (`null`) edge rates rather than divide-by-zero values.
51. Inverse `AFTER` and `BEFORE` claims normalize to one strict-order pair and do not create a label conflict.
52. A strict-order claim and `OVERLAP` remain a pair-level label conflict.
53. Adding a redundant source edge does not hide a cycle induced by one source edge's mapping fan-out.

## Annotation-to-projection adapter tests (54–64)

54. A valid exact report/annotator/pass partition projects only eligible primary rows.
55. Mixed annotator rows do not leak across partitions.
56. Container mappings are excluded from the primary event mapping set.
57. Inferred/non-primary temporal relations are not projected.
58. Empty mapping sets keep event relations visible as unmapped-endpoint edges.
59. Scope or structural validation errors stop the adapter.
60. Incomplete report review stops the adapter.
61. Ineligible or locally unpermitted reports are blocked.
62. Explicit annotation-lock confirmation and a non-empty lock reference are required.
63. Arbitrary or stale lock references are rejected against the computed partition digest.
64. Prior-exposure status and the associated caution flag are exposed in projection output.

## Lifecycle flags in Enterprise ATT&CK v12.1

T1053.001 is revoked and T1053.004 is deprecated; both resolve to A_120 parent T1053. They remain in the crosswalk/A_exact record but cannot contribute to primary A_120 unless separately resolved.

## Limitations

These tests establish only the synthetic structural behaviours listed above. They do not establish that a source interpretation is semantically correct, that the reconstructed schema is the original v0.4.2 schema, or that the protocol is researcher-approved. No AnnoCTR report has been entered or annotated. The annotation-to-projection adapter has not been run on a real report and its lock has only been exercised with synthetic fixture rows and source text.
