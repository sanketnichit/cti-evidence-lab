# When pooled incident interpretations create unsupported sequence witnesses

Sanket Nichit · CTI Evidence Lab · v0.2 manuscript draft

## Abstract

Cyber threat intelligence reports can support several readings of action identity, ordering and technique mappings. Pooling facts from those readings can produce a three-action sequence that no single reading supports, even when the pooled graph retains occurrence identities. We compare pooled and per-profile answers for known and unresolved mappings, and identify the smallest incompatible subset of facts for a pooled witness. Across 5,886 constructed profile pairs, pooling raises at least one query's status in 2,935 pairs. The evaluated recorded profiles show no such status change. A source-backed NetSupport sensitivity isolates a separate issue. One apparent projection error depends on how two execution descriptions are aligned, while another survives all three readings. The results characterize representation fidelity and uncertainty on supplied interpretations.

## Model

Each profile contains distinct action IDs, known ATT&CK label sets and explicit directed BEFORE edges. The input graph is acyclic within each profile. We compare profiles for one incident at the same taxonomy level and require shared IDs to denote the same action. The query asks for three distinct occurrences joined by two supplied edges with the three requested labels. In the open mapping analysis, an occurrence with a withheld mapping may take a queried label. Status is supported if a known witness occurs in some profile, unresolved if support requires completing a withheld mapping in some profile, and unsupported otherwise. This is existential support over the declared profiles.

The v0.1 study shows how technique-pair projection merges actions even in one profile. Our comparison keeps occurrence identities and varies whether the five witness facts must coexist in a profile. Reasoning over possible worlds is established in incomplete-data research. Here the alternatives are supplied incident interpretations, with explicit edge and label evidence. [v0.1 preprint](https://doi.org/10.5281/zenodo.24533052) · [Amendola and Libkin, 2018](https://ijcai.org/proceedings/2018/233)

## Witness support and explanation

For each of the two edges and three occurrence-label assignments in a candidate witness, record which profiles contain the fact. Intersect the five profile sets. A profile is in the intersection exactly when it supplies that witness. Union the witness intersections to obtain the supporting profiles for the query. A query can hold in every profile through different witnesses. One shared witness requires a single intersection covering every profile.

For an incompatible pooled witness, find the smallest subset of facts with empty intersection. It has at most five facts and at most as many facts as there are profiles. Selecting one missing fact per profile excludes all profiles. Our three-profile control shows why checking pairs alone can fail. Each pair of witness facts occurs together somewhere, while the full intersection is empty.

## Verification and results

Direct enumeration verifies support masks across 5,886 constructed profile pairs. For mapping uncertainty, direct per-profile query execution provides a separate answer reference. Across 47,088 pair/query instances, pooling promotes 9,216 unsupported answers to unresolved, 2,560 unsupported answers to supported, and 1,080 unresolved answers to supported. Independent pair enumeration verifies the minimum conflicts of all 3,640 incompatible known witnesses from the two-profile construction. These are finite design counts.

The two original recorded profile groups agree across all 133 parent-label queries. In NetSupport, the recorded, conservative and co-referent readings agree between pooled and profile-coherent evaluation across 3,375 queries. The WMI example changes within the co-referent reading, which connects a firewall change and task creation through the specific execution. The ordinary projection continues to return the separate script-action query in all three readings without a coherent witness. [Experiment records and source rationale](experiments/profile_coherence_v0.2/README.md)

## Artifact and limitations

The comparison command records individual profile answers, supporting profiles for each pooled candidate, conflicts, citations to the case evidence, and a case hash. Its verifier recomputes the export. The paper's conclusions depend on retained edges, aligned identities and stated completion assumptions. The examined source alternatives do not demonstrate a pooling failure in the wild. Independent reviewers would need to record coherent interpretations and align action identities before comparing their graphs. The study has no independent reviewer or analyst outcomes.

```sh
python scripts/reproduce_study.py
python scripts/compare_sequence_profiles.py --group netsupport-identity --query T1562 T1047 T1053 --output outputs/profile-comparison.json
python scripts/compare_sequence_profiles.py --verify outputs/profile-comparison.json
```
