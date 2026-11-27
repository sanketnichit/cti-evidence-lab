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

## Open mapping uncertainty

Apply the existing open completion rule separately within each profile. An unknown occurrence can take any label in the fixed query vocabulary. Known labels and BEFORE edges stay fixed in that profile. A coherent answer is **supported** if a known witness exists in at least one profile, **unresolved** if only a witness requiring completion exists in at least one, and **unsupported** if neither exists. This is an existential answer over the recorded interpretations.

For the pooling comparison, union the known facts and union the possible facts separately. If a label is withheld in one profile and known in another, the pooled possible facts still include the open possibilities contributed by the first. Pooling edges and eligible labels can then increase the apparent support of a query. The test checks each coherent answer against direct execution of the existing query engine by profile, and checks the pooled possibilities against distinct-path enumeration.

Across the same 5,886 constructed pairs and all eight queries per pair, pooling increases an answer's status in 2,935 pairs. The 47,088 graph-pair/query instances contain these increases.

| Coherent status | Pooled status | Query instances |
|---|---|---:|
| Unsupported | Unresolved | 9,216 |
| Unsupported | Supported | 2,560 |
| Unresolved | Supported | 1,080 |

The first control splits the required edges across profiles and withholds the middle label. Pooling makes the chain appear possible even though neither profile has a complete path. The second control puts the full path in a profile with a withheld middle label, and the known label in a profile missing one edge. Pooling upgrades that query to supported. The two forms of error affect different decisions.

In the two recorded parent-level profile groups, pooling and coherent evaluation agree on all 133 queries. The RDP group has three supported and two unresolved queries. The domain-controller group has four supported and eight unresolved queries. These matrices enumerate the labels known somewhere in each group. They describe sensitivity to the supplied alternatives and vocabulary. [Detailed uncertainty results](uncertainty_results.json)

```sh
python -m examples.profile_uncertainty
```

Full reproduction includes `profile_uncertainty.json`.

## NetSupport action identity sensitivity

The recorded NetSupport graph assigns two T1047 actions to paragraph P6. One represents the broad description of further remote execution. The other represents the specific payload run. The paragraph places a change to firewall settings before the broad activity and task creation after the specific run. Whether the opening description refers to that same payload run determines whether those ordering links share a middle action. [Recorded holdout interpretation](../incident_holdout_v0.1/README.md)

The comparison keeps the recorded graph as one profile. A conservative profile omits B12, the link to the broad execution description. A third profile treats the description as a reference to the specific run, removes the duplicate action and directs the link to that run as B12-aligned. This last reading assumes that the opening time relation applies to the specific run. The paragraph also permits reading the opening as a summary of several actions, so this assumption remains open to review.

| Reading of P6 | T1562 → T1047 → T1053 in the occurrence graph | Ordinary pair traversal |
|---|---|---|
| Separate actions | Unsupported | Returns the query |
| Omit the broad ordering link | Unsupported | No return |
| Same execution | Supported by B12-aligned and B14 | Returns the query |

The separate script-action mismatch (T1105 → T1059 → T1560) remains unsupported in the occurrence graph in all three profiles. The ordinary projection returns it in each. Across the full 3,375-query parent vocabulary, pooled and profile-coherent statuses agree. The WMI change arises within one coherent interpretation. These post-review alternatives identify which finding depends on action identity. They provide no independent adjudication. [Results and witnesses](netsupport_identity_results.json)

```sh
python -m examples.netsupport_identity_sensitivity
python -m examples.netsupport_identity_sensitivity --source-html /path/to/22587.html
```

The second command also verifies the saved HTML and paragraph locators. Full reproduction checks and includes `netsupport_identity_sensitivity.json`.

## Explaining a pooled-only witness

A pooled witness has five facts, comprising two ordering links and three occurrence-label assignments. Each fact occurs in at least one profile. A **minimum conflict** is a smallest subset of those facts that occurs together in no profile. Listing the profiles for each fact makes the conflict inspectable. The explanation reports every smallest subset when several tie. It applies to a single pooled witness. A query can still have a different, coherent witness.

The search tests subsets in increasing size. A conflict needs at most five facts because the full witness is already incompatible. It also needs at most as many facts as there are profiles. Pick one missing fact per profile and take their union. Every profile then lacks at least one selected fact. With two profiles, every incompatible pooled witness therefore has a two-fact conflict.

Direct pair enumeration confirms all conflict explanations for the 3,640 incompatible witnesses in the existing finite two-profile design. New controls reach the bound with three, four and five profiles. In each control, each profile omits a different required fact. In the three-profile control, every pair of facts has a common profile, yet the full witness has none. A test that only checks pairs would miss this case. The examples use known labels and fixed edges under constructed alternatives. They establish a diagnostic and its boundary. [Conflict results](conflict_results.json)

```sh
python -m examples.profile_conflicts
```

Full reproduction checks and includes `profile_conflicts.json`.

## Compare and verify one query

The comparison export includes the per-profile answers, mappings, relation evidence, and all pooled candidates. Each candidate names its supporting profiles or records a minimum conflict. The possible-witness list includes fully known witnesses. Conflict fact indices are one-based within the fact list, and profile numbers refer to `answer.profile_order`.

```sh
python scripts/compare_sequence_profiles.py --group netsupport-identity --query T1562 T1047 T1053 --output outputs/profile-comparison.json
python scripts/compare_sequence_profiles.py --verify outputs/profile-comparison.json
```

The other groups are `rdp` and `domain-controller`, both at the parent level. The NetSupport export exposes the identity assumption behind the WMI witness. Full reproduction includes the verified example. [v0.2 manuscript draft](../../PROFILE_COHERENCE_REPORT_v0.2.md)
