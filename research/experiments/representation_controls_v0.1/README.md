# Representation controls

SYNTHETIC_REPRESENTATION_CONTROLS_NOT_EMPIRICAL_RESULTS

All inputs are synthetic. Counts describe representations, not reports or model accuracy.

| Control | Source edges | Fully omitted | Partially represented | Unmapped | Distinct pairs | Loop-inclusive labeled pairs | Loop collision keys | Projected strict cycles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| distinct_mapping | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| same_technique | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| repeated_same_technique | 2 | 2 | 0 | 0 | 0 | 1 | 1 | 0 |
| mixed_mapping | 1 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| unmapped_endpoint | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| occurrence_collapse_cycle | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 1 |
| single_edge_fanout_cycle | 1 | 0 | 1 | 0 | 2 | 4 | 0 | 1 |

Loop-inclusive counts retain relation labels; primary distinct-pair counts are label-agnostic. These controls use only BEFORE, so the counts are comparable here.

A self-loop preserves a technique-level image but not which two occurrences it connects. The repeated-same-technique control merges two relations into one loop. An occurrence-preserving graph retains the supplied endpoints even when mappings are absent.

Both cycle controls have acyclic source graphs. One needs two source edges; the other is caused by Cartesian mapping fan-out from a single edge. Therefore a projected cycle alone does not diagnose repeated executions or source inconsistency.

Reproduce: `python -m examples.representation_controls --output-dir research/experiments/representation_controls_v0.1`
