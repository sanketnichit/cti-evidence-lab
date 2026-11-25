# Sequence query runtime and storage

This experiment measures the cost of retaining endpoint IDs and distinguishes query answering from the richer investigator diagnostic. The workloads are deterministic synthetic DAGs with 16, 32, 64 and 128 occurrences. A chain and a hub both have n − 1 edges. The hub concentrates incoming and outgoing edges at one occurrence, producing quadratic two-edge path counts. Each graph uses a fixed pool of twelve labels and either one or two labels per occurrence.

Run the benchmark from the repository root:

```sh
python -m examples.sequence_scaling --output outputs/sequence_scaling.json
```

Each operation gets one warm-up and seven measured runs on one machine. The [recorded run](results.json) retains every timing sample and environment metadata. Both answer implementations enumerate all distinct supported label triples from their prepared representation. The full investigator handles one supported query and also produces witnesses, incompatible joins and projection diagnostics. Its time includes input validation and reference evaluation. These workloads have complete mappings. The reference oracle enumerates occurrence triples and checks that the endpoint join agrees on every workload.

Compact UTF-8 JSON sizes cover sorted pair keys and sorted endpoint rows. They exclude source text, occurrence metadata, indexes, compression and Python object overhead. Each endpoint row stores two labels and two occurrence IDs. With two labels per occurrence the encoding can generate four rows per source edge. A fixed label vocabulary limits pair-key growth, even as endpoint rows grow with the input.

| Workload | Pair JSON | Endpoint JSON | All pair answers, ms | All endpoint answers, ms | One full diagnostic, ms |
|---|---:|---:|---:|---:|---:|
| 16-action chain, one label | 217 B | 511 B | 0.004 | 0.005 | 0.73 |
| 128-action chain, one label | 217 B | 4,319 B | 0.009 | 0.093 | 583 |
| 128-action hub, one label | 415 B | 4,319 B | 0.033 | 0.524 | 612 |
| 128-action hub, two labels | 793 B | 17,273 B | 0.093 | 6.832 | 574 |

The endpoint encoding uses about 10–27 times the compact pair bytes at 128 actions in these workloads. The endpoint join agrees with the source oracle in all 16 graphs. The ordinary projection returns 40 additional answers in the 128-action two-label hub and none in the 128-action single-label chain. The cost depends on both the mapping width and the concentration of edges around shared endpoints.

The small endpoint-query times and much larger diagnostic times measure different operations. The original investigator sorted all ordered occurrence triples before filtering for edges and called the cubic source oracle through its projection comparison. It also materialized incompatible joins, whose output size can grow with the product of two matching edge sets. Current timings describe these synthetic workloads and this implementation.

## Investigator optimization

The optimized implementation walks sorted adjacency lists and computes the projected answer for the requested labels. The known witnesses give the endpoint-join answer whenever the projection retains both label pairs. The all-query representation benchmark still runs the independent oracle. Witness order and relation IDs remain part of the exported record.

A paired rerun used the same 16 graphs and the same supported query per graph, defined as the first supported label triple in lexicographic order. Both versions ran in one Python process, with the starting version alternating by workload. Each version ran once to warm up and seven times for measurement. The baseline is pinned to `95ad3a8`. The [remeasurement](investigator_remeasurement.json) contains raw samples. The earlier table reports its original run, where the baseline was slower. Use the paired measurements for the speed comparison.

| 128-action workload | Baseline median | Optimized median |
|---|---:|---:|
| Chain, one label | 351.360 ms | 0.255 ms |
| Chain, two labels | 354.608 ms | 0.471 ms |
| Hub, one label | 363.882 ms | 0.187 ms |
| Hub, two labels | 362.759 ms | 0.249 ms |

Full answer records matched on all 532 bundled case queries, 600 deterministic synthetic comparisons with and without mapping bounds, and all 16 timed workloads. The synthetic comparison used seed 835 and included shuffled relation order, multiple relation IDs per edge, unknown mappings and multiple known labels. The paired run loads the pinned baseline from Git history.

```sh
python -m examples.compare_investigator_runtime --output outputs/investigator_remeasurement.json
```

The adjacency scan avoids all-triples enumeration. Sorting costs scale with the edge count, and connected-path work scales with the paths visited. Listing incompatible projected joins still examines the cross-product of the two matching edge sets. Highly repetitive labels or graphs with many witnesses can therefore increase both latency and response size. Measurements cover engine execution on synthetic graphs up to 128 actions.

## Cost of expanding query evidence

The investigator also exposes a count-only mode through `investigate(..., summary_only=True)`. It preserves the answer status, the projection flags and the exact number of entries in each evidence list. Counts use distinct occurrence edges even if several source relations document the same edge. The offline artifact and existing certificate exports continue to include individual witnesses and relation IDs.

For each eligible middle occurrence, multiply the number of eligible incoming edges by the number of eligible outgoing edges and sum over middle occurrences. The DAG constraint ensures that every counted path has three distinct actions. Counting only known labels gives the supported witness count. Comparing it with the count that admits unknown labels under the supplied bounds gives the unresolved count. Comparing the bounded and open counts gives the number excluded by the bounds. For projected known-label edges, subtract the supported witness count from the product of the two matching edge-set sizes. The difference is the number of joins with incompatible middle IDs. The distinct-pair view still suppresses same-technique edges.

The [output benchmark](diagnostic_output.json) fixes the query to `A → A → A`. At each width *w*, it uses *w* disconnected edges or a hub with *w* incoming and *w* outgoing edges. The hub is mapped to A, withheld with no bounds, or withheld with B as its only allowed label. All other actions are mapped to A. The disconnected graph has *w*² combinations, all incompatible. The mapped hub has *w*² connected witnesses and 3*w*² incompatible combinations. In the other two hub settings, *w*² paths are unresolved or excluded, respectively. These closed-form counts are checked at every size. The code also checks every expanded record against its count-only counterpart at widths 16, 64 and 128.

The timings include query validation, answer construction and compact UTF-8 JSON encoding. Each operation has one warm-up and seven measured repetitions on a Windows x86-64 machine with Python 3.12.14. They exclude source metadata, browser rendering and network transfer.

| Workload at width 128 | Dominant evidence entries | Expanded JSON | Count-only JSON | Median expanded / count-only |
|---|---:|---:|---:|---:|
| Disconnected edges | 16,384 incompatible joins | 2.94 MB | 727 B | 102.54 / 0.80 ms |
| Mapped hub | 16,384 witnesses and 49,152 incompatible joins | 9.80 MB | 726 B | 519.43 / 1.27 ms |
| Unmapped hub | 16,384 unresolved witnesses | 2.40 MB | 734 B | 129.77 / 0.91 ms |
| Bounded hub | 16,384 excluded witnesses | 2.90 MB | 911 B | 143.20 / 1.08 ms |

At width 4,096, the mapped hub has 8,193 occurrences. Its count-only result reports 16,777,216 witnesses and 50,331,648 incompatible joins in 732 bytes, with a median of 69.05 ms. Only count-only results are measured at that width. Once the graph is validated, path counting requires a fixed number of vertex and edge passes for this three-label query. The counts are exact for the supplied graph. The expanded record is required to inspect individual occurrences, relation evidence or mismatch reasons. These workloads isolate output size using deliberately repetitive labels. They do not measure production traffic or analyst performance.

```sh
python -m examples.measure_diagnostic_output --output outputs/diagnostic_output.json
```
