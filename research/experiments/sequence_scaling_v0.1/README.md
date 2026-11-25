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

The small endpoint-query times and much larger diagnostic times measure different operations. The investigator sorts all ordered occurrence triples before filtering for edges and calls the cubic source oracle through its projection comparison. It also materializes incompatible joins, whose output size can grow with the product of two matching edge sets. An adjacency-based path scan and query-specific projection comparisons are the next performance targets. A future benchmark should include larger graphs, sparse and incomplete mappings, peak memory, and multiple runs on different machines. Current timings describe these synthetic workloads and this implementation.
