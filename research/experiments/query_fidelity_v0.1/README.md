# Connected-sequence query benchmark

CONTROLLED_QUERY_FIDELITY_NOT_EXTRACTION_PERFORMANCE

The input graphs and all labels are synthetic. Rates measure query fidelity to these inputs, not performance on CTI reports.

| Design | Representation | TP | FP | FN | TN | Precision | Recall |
|---|---|---:|---:|---:|---:|---:|---:|
| four_vertices_singleton_mappings | distinct_pairs | 2064 | 1416 | 2538 | 133950 | 0.5931 | 0.4485 |
| four_vertices_singleton_mappings | loop_pairs | 4602 | 7527 | 0 | 127839 | 0.3794 | 1.0000 |
| four_vertices_singleton_mappings | distinct_pairs_with_endpoint_join | 2064 | 0 | 2538 | 135366 | 1.0000 | 0.4485 |
| four_vertices_singleton_mappings | loop_pairs_with_endpoint_join | 4602 | 0 | 0 | 135366 | 1.0000 | 1.0000 |
| three_vertices_set_valued_mappings | distinct_pairs | 1536 | 4536 | 1920 | 102600 | 0.2530 | 0.4444 |
| three_vertices_set_valued_mappings | loop_pairs | 3456 | 15096 | 0 | 92040 | 0.1863 | 1.0000 |
| three_vertices_set_valued_mappings | distinct_pairs_with_endpoint_join | 1536 | 0 | 1920 | 107136 | 1.0000 | 0.4444 |
| three_vertices_set_valued_mappings | loop_pairs_with_endpoint_join | 3456 | 0 | 0 | 107136 | 1.0000 | 1.0000 |

Full JSON also reports the distinct-adjacent-label stratum, logical storage totals, exact query definition and four inspectable counterexamples.

Reproduce: `python -m examples.query_fidelity_benchmark --output-dir research/experiments/query_fidelity_v0.1`
