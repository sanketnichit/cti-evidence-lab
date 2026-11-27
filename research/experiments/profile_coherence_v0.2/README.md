# Sequence witnesses across alternative interpretations

The [v0.1 preprint](https://doi.org/10.5281/zenodo.24533052) studies whether technique-pair projection loses sequence witnesses within a supplied graph. This experiment studies a different failure. An apparent witness can retain all three occurrence identities while combining edges or labels that are never present together in one recorded interpretation.

## Query and reference

An interpretation profile supplies an acyclic BEFORE graph and sets of known labels. Within an incident and taxonomy level, occurrence IDs must denote the same actions across profiles. Evaluate the same three-label query under four conditions.

| Condition | What suffices |
|---|---|
| Pooled | The two edges and three known labels occur somewhere in the profile union |
| Some profile | One profile supplies all facts for at least one witness |
| Every profile | Each profile supplies a witness, which can differ across profiles |
| Shared witness | The same three occurrences with the queried labels and edges form a witness in every profile |

For a candidate witness, intersect the sets of profiles containing each of its two edges and each of its three occurrence-label facts. With an empty intersection, no profile supports that witness. With a nonempty intersection, each member profile contains all five facts and hence the witness. The union of those intersections across an individual query's witnesses identifies exactly the profiles supporting the query. An intersection over profiles for one witness is stronger than coverage from several different witnesses. The implementation discards repeated endpoints even when pooling creates a cycle. Empty mapping sets supply no known labels.

## Verification and results

An independent enumeration lists distinct occurrence triples in each profile and in the pooled graph. It checks exact support for every candidate witness on 5,886 unordered pairs with replacement. The profiles use three ordered vertices, every subset of the two forward chain edges, and selectors for label A, label B, or no known label at each vertex. Pooling yields at least one query supported by neither profile in 2,040 pairs, with 3,640 such query instances. These counts describe a constructed test space.

Two controls isolate unsupported combinations. One splits the two edges across profiles. Another gives one profile both edges with the middle mapping withheld, and the other the missing label with only one edge. A third control supports the query in every profile through different middle occurrences. A pooled two-edge cycle supplies no distinct-action witness.

| Recorded profile group | Pooled | Some profile | Every profile | Shared witness |
|---|---:|---:|---:|---:|
| RDP, parent labels, 4 profiles | 3 | 3 | 0 | 0 |
| Domain controller, parent labels, 3 profiles | 4 | 4 | 1 | 1 |

These are all groups in the offline artifact with multiple profiles for the same case and taxonomy level. Neither group yields a union-only query or a pooled witness absent from every profile. Each has an extended profile that already contains its pooled known facts. The example with different witnesses proves the distinction under a designed control. The source comparison establishes coverage only for the supplied alternatives. [Machine-readable results](results.json)

An independent extension would need coherent source interpretations recorded before comparison. Use only one-to-one action alignments where identity and scope agree, and retain unresolved alignments separately. The existing [independent review protocol](../incident_holdout_v0.1/README.md#independent-source-review) provides the source-review intake procedure. There are no participant results in this analysis.

```sh
python -m examples.profile_coherence
```

The complete study command verifies and includes `profile_coherence.json`.
