# When pooled incident interpretations create unsupported sequence witnesses

Sanket Nichit · CTI Evidence Lab · v0.2 manuscript draft

## Abstract

Cyber threat intelligence reports can support several readings of action identity, ordering and technique mappings. Pooling facts from those readings can produce a three-action sequence that no single reading supports, even when the pooled graph retains occurrence identities. We compare pooled and per-profile answers for known and unresolved mappings, and identify the smallest incompatible subset of facts for a pooled witness. Across 5,886 constructed profile pairs, pooling raises at least one query's status in 2,935 pairs. The evaluated recorded profiles show no such status change. A source-backed NetSupport sensitivity isolates a separate issue. One apparent projection error depends on how two execution descriptions are aligned, while another survives all three readings. The results characterize representation fidelity and uncertainty on supplied interpretations.

## Model

Each profile contains distinct action IDs, known ATT&CK label sets and explicit directed BEFORE edges. The input graph is acyclic within each profile. We compare profiles for one incident at the same taxonomy level and require shared IDs to denote the same action. The query asks for three distinct occurrences joined by two supplied edges with the three requested labels. In the open mapping analysis, an occurrence with a withheld mapping may take a queried label. Status is supported if a known witness occurs in some profile, unresolved if support requires completing a withheld mapping in some profile, and unsupported otherwise. This is existential support over the declared profiles.

The v0.1 study shows how technique-pair projection merges actions even in one profile. Our comparison keeps occurrence identities and varies whether the five witness facts must coexist in a profile. [v0.1 preprint](https://doi.org/10.5281/zenodo.24533052)

## Related work and contribution

Conditional tables and event-table semirings already support query evaluation over alternatives. The profile masks here are a bit representation of sets of interpretations, with intersection for a join and union for alternative witnesses. The research contribution is applying that established semantics to an evidence-backed CTI sequence task and testing what is lost at both the answer and witness levels. [Imieliński and Lipski, 1984, §5](https://www.inf.unibz.it/~nutt/Teaching/FDBs1718/FDBsPapers/imielinskiLipski-JACM-84.pdf) · [Green, Karvounarakis and Tannen, 2007, §3](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf)

ChronoCTI predicts temporal relations between technique pairs. Attack Flow preserves action identity and supports Boolean operators on input effects. TRACE-CTI records the evidence and validation state of individual technique claims. Each addresses a different unit of analysis from the joint support of two explicitly reported ordering facts and three mappings within one reading. We compare these published contracts and evaluate the representation on identical supplied inputs. Extraction accuracy and analyst performance require separate evaluations. [Closest-system comparison](RELATED_WORK_MATRIX.md#interpretation-coherence)

## Witness support and explanation

For each of the two edges and three occurrence-label assignments in a candidate witness, record which profiles contain the fact. Intersect the five profile sets. A profile is in the intersection exactly when it supplies that witness. Union the witness intersections to obtain the supporting profiles for the query. A query can hold in every profile through different witnesses. One shared witness requires a single intersection covering every profile.

Pooling checks whether each fact has a nonempty support set before joining. Two nonempty sets can be disjoint, so checking nonemptiness before the join can introduce a witness. Even per-fact support counts cannot recover that joint information. Suppose the two required edges each occur in one of two profiles. Both edges can be in the first profile, or one edge can be in each profile. The pooled edges and counts are identical. With the three labels fixed in both profiles, the first arrangement supports the witness and the split arrangement does not. Add the same second path carrying the same three labels to both profiles in both arrangements. Both now answer the query as supported, but the split arrangement still contains an unsupported pooled witness.

For an incompatible pooled witness, find the smallest subset of facts with empty intersection. It has at most five facts and at most as many facts as there are profiles. Selecting one missing fact per profile excludes all profiles. Our three-profile control shows why checking pairs alone can fail. Each pair of witness facts occurs together somewhere, while the full intersection is empty.

## Verification and results

Direct enumeration verifies support masks across 5,886 constructed profile pairs. For mapping uncertainty, direct per-profile query execution provides a separate answer reference. Across 47,088 pair/query instances, pooling promotes 9,216 unsupported answers to unresolved, 2,560 unsupported answers to supported, and 1,080 unresolved answers to supported. Independent pair enumeration verifies the minimum conflicts of all 3,640 incompatible known witnesses from the two-profile construction. These are finite design counts.

The control with a second path preserves the supported answer and adds exactly one unsupported pooled witness in the split arrangement. Direct per-profile enumeration also checks witness fidelity on the recorded groups. Pooling adds no unsupported witnesses across 3,508 group/query instances. The possible-witness counts include known witnesses.

| Profile group | Parent-label queries | Pooled known witnesses | Pooled possible witnesses | Pooled-only witnesses |
|---|---:|---:|---:|---:|
| RDP | 8 | 3 | 8 | 0 |
| Domain controller | 125 | 4 | 12 | 0 |
| NetSupport | 3,375 | 8 | 1,013 | 0 |

In NetSupport, the co-referent reading connects a firewall change and task creation through the same reported WMI execution. The conventional technique-pair projection continues to return the separate script-action query in all three readings without a coherent witness. This latter finding concerns pooling across occurrences within a reading, while the table concerns pooling across readings. [Experiment records and source rationale](experiments/profile_coherence_v0.2/README.md)

An ordering-evidence sensitivity sweep covers all six investigator cases and all 11 recorded parent profiles. One profile remained unassessed. Every one of the 23 supported profile/query instances depended on at least one individual ordering row. Grouping withdrawals by citation unit changed the results for unresolved queries. In NetSupport, removing the most consequential single row eliminated 387 of 907 unresolved answers. Withdrawing the most consequential paragraph eliminated 611 under a conservative rule that drops every row citing that paragraph. The result measures dependence on recorded evidential bindings while holding the actions and mappings fixed. [Design, scope and results](experiments/profile_coherence_v0.2/README.md#ordering-evidence-sensitivity-design)

Allowing a row to survive while any cited unit remains reduces the maximum NetSupport loss to 596. In CISA AA25-266A this alternative reduces the maximum from 34 to 28, equal to the largest single-row loss. Exhaustive search finds that six domain-controller profile/query instances require at least two citation units to be withdrawn under the last citation rule. Each loses all known witnesses after one unit under the first citation rule. These are bounds under stated citation-retention assumptions. They do not adjudicate the individual citations. [Exact cuts and intervention results](experiments/profile_coherence_v0.2/ordering_evidence_results.json)

## Computational cost and storage

For a single query, the focused evaluator tests the three requested labels on each candidate path and avoids enumerating every label combination. Across five workloads with four labels per mapped action, it matched the exhaustive mask results and was 1.5–3.3 times as fast, with 17–18% of the peak Python allocations. At one label per mapped action, the speed difference was small. These figures are from one Windows machine with CPython 3.12.14 and exclude input construction, file I/O and serialization.

The full comparison lists incompatible joins between left and right projected edges. Their count can grow with the product of the two edge counts, even in sparse graphs. On the 16-profile workload with 96 actions per profile, listing 8,640 incompatible joins across profiles took 32.9 ms for the full comparison. Counting the same joins and retaining pooled explanations took 13.6 ms. Peak Python allocations were 4.95 MiB and 0.31 MiB, respectively. The synthetic inputs and answer occupied 9.51 MB in full and 0.37 MB in compact JSON, or 108 kB and 7.3 kB after gzip compression. The source-backed NetSupport export was 44.4 kB in full and 43.1 kB in compact JSON because most of that record is evidence and case data. Sparse synthetic paths and one selected query bound the scope of these measurements. [Design and rerun command](experiments/profile_coherence_v0.2/README.md#runtime-and-storage-design) · [Raw measurements](experiments/profile_coherence_v0.2/scaling_results.json)

## Artifact and limitations

The comparison command records individual profile answers, supporting profiles for each pooled candidate, conflicts, citations to the case evidence, and a case hash. Its verifier recomputes the export. The paper's conclusions depend on retained edges, aligned identities and stated completion assumptions. The examined source alternatives do not demonstrate a pooling failure in the wild. Independent reviewers would need to record coherent interpretations and align action identities before comparing their graphs. The study has no independent reviewer or analyst outcomes.

The chronological holdout has an answer-free review instrument and a predefined analysis for two matching, completed returns. The witness audit restricts the comparison to actions both reviewers retained and aligned one to one, with each reviewer's edges and mappings kept separate. It reports how much of the submitted evidence falls outside that shared universe. This design measures witness agreement conditional on alignment. Reviewer choices about action boundaries remain visible through the split, merge and unmatched counts. [Independent review and analysis](experiments/incident_holdout_v0.1/README.md#independent-source-review)

```sh
python scripts/reproduce_study.py
python scripts/compare_sequence_profiles.py --group netsupport-identity --query T1562 T1047 T1053 --output outputs/profile-comparison.json
python scripts/compare_sequence_profiles.py --verify outputs/profile-comparison.json
```
