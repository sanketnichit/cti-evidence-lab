# Projection metrics — RECON v0.1

**Status:** Provisional research implementation; synthetic tests only. Not a real-report result, not a publication result, and not yet integrated into the public GitHub project.

## Entry conditions

`analysis/projection_metrics_recon.py` expects data that has already passed the reconstructed schema validator and has been human-locked. Its `techniques_by_event` argument must contain only accepted, source-supported parent-level `A_120` mappings for resolved atomic `event_leaf` units. Its temporal-edge input must contain only distinct, directly supported positive temporal relations in compatible scope. The function re-checks these structural conditions that can be represented in its input (`relation_basis`, `scope_compatibility`, distinct IDs, positive relation label, endpoint existence), but it cannot re-evaluate source evidence, unit granularity or scope ancestry.

The mapping adapter `build_a120_mapping_sets()` filters mapping records to:

- `mapping_decision_status=ACCEPTED`;
- mapping basis `report_explicit_subtechnique`, `report_explicit_parent`, or `source_supported_analyst_candidate`;
- `baseline_mapping_status=IN_VOCAB` and membership in the supplied pinned A_120 vocabulary;
- event IDs explicitly supplied as eligible event leaves.

Excluded rows are counted by reason. This prevents `workbook_only`, alternative, rejected, unresolved, out-of-vocabulary, and container mappings from entering primary mapping sets.

## Four mutually exclusive event-edge outcomes

Each positive temporal event edge receives exactly one status:

1. `unmapped_endpoint` — at least one endpoint has no accepted A_120 mapping. Excluded from the mapped-edge denominator.
2. `fully_omitted` — both endpoints are mapped, share at least one technique, and the projected mapping image contains no distinct-technique pair (only diagonal `(T,T)` pairs).
3. `partially_represented` — both endpoints are mapped, share at least one technique, and at least one distinct-technique pair also remains.
4. `no_diagonal_mapping` — both endpoints are mapped, but their A_120 sets do not intersect; all retained pairs are distinct-technique pairs.

Counts and rates are reported separately. The mapped-positive-event-edge denominator is the sum of statuses 2–4. Unmapped edges are reported separately and are not silently treated as projection omissions.

## Relation orientation and collisions

- Source endpoint order and original labels are preserved in `edge_to_pairs`. For derived strict-order pair keys, `AFTER(A,B)` is normalized to the same precedence orientation as `BEFORE(B,A)`. Both are treated as one `STRICT_ORDER` label class for conflict detection; the original annotation label and endpoint order remain unchanged in registers.
- `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` use canonical unordered technique dyads.
- `distinct_pair_provenance_by_relation_class` records provenance for every retained pair by relation class/orientation.
- `distinct_pair_collisions_by_relation_class` counts multiple distinct source event edges that map to the same target distinct pair within the same relation class.
- `distinct_pair_collisions_global` reports pair collisions across relation classes; `distinct_pair_label_conflicts` separately highlights pairs receiving different temporal labels.
- Diagonal pairs are excluded from the target graph's collision counts.

One event edge expanding into multiple technique pairs is not itself a collision. A collision requires at least two distinct source event-edge IDs to support the same projected pair.

## Strict-order cycle diagnostics

Cycle analysis uses only `BEFORE` and normalized `AFTER` edges. It first checks whether the source event-instance strict-order graph is acyclic. A projected cycle is not interpretable as projection-induced if the source event graph is already cyclic. For each projected component, the implementation tests each contributing source event edge in isolation. `single_event_edge_mapping_fanout` is true if at least one individual source edge alone induces a cycle, even if redundant edges also contribute. `single_source_edges_inducing_cycle` lists those individually sufficient edges. A component is counted as requiring multiple source edges only when no single contributing edge is sufficient.

## Test status and limitations

The combined RECON synthetic suite currently has 56 passing tests: 29 schema-validator tests, 16 projection-metric tests, and 11 annotation-to-projection adapter tests. No AnnoCTR report, prior DFIR worked case, or human annotation has been passed through this module. The public `src/projection_metrics.py` has also received separate synthetic-tested corrections for strict-order orientation and single-edge fan-out attribution; the two implementations remain separate, and RECON is not the original v0.4.2 schema.
