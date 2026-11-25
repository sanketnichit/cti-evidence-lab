# Explicit bounds on unknown mappings

**20 November 2026. Optional sensitivity analysis, implemented in the query engine and CLI.**

The unrestricted investigator allows an unknown occurrence to take any queried label. The fixed five-publisher evaluation exposed a limitation: an unknown SMTP-transmission mapping could make a repeated credential-recovery query unresolved, even though that label is implausible for transmission. A candidate list helps only if its completeness is an explicit assumption. Merely proposing a label does not establish that all other labels are impossible.

## Contract

An allowed-label bound limits the possible labels of one retained occurrence whose mapping is currently unknown. Each CLI constraint requires an occurrence ID, a nonempty allowed-label list, a rationale and source-evidence references. The record declares `ALLOWED_LABEL_UPPER_BOUND` semantics.

- The bounds are assumptions, not accepted mappings. Even a singleton allowed set remains unresolved when it is needed by a query.
- Unlisted unknown occurrences remain unrestricted. Known mapping sets and temporal edges cannot be changed by a constraint.
- Empty lists, duplicate constraints or labels, absent occurrences and missing evidence references are rejected. An empty domain is not used to assert that an action has no applicable technique.
- Parent profiles require parent-format identifiers. Exact profiles permit parent or sub-technique identifiers. Syntax checks do not validate membership in the pinned taxonomy or prove a semantic mapping.
- A constrained negative means no compatible path under the declared bounds. It does not establish absence in the incident or validate the bounds.

The engine lists each previously possible path excluded by a bound, including the occurrence, required label and allowed labels. Known witnesses remain unchanged. The only possible classification change caused by narrowing domains is from unresolved to not supported; a bound cannot manufacture positive evidence.

## Inspectable example

[archive_bound_assumption.json](archive_bound_assumption.json) is an explicitly hypothetical upper bound on the archive occurrence in the existing withheld-mapping profile. It is not an exhaustive candidate annotation established by the source.

```sh
python scripts/investigate_sequence.py --case domain-controller --profile archive_mapping_withheld --query T1059 T1059 T1059 --mapping-constraints research/experiments/bounded_mapping_v0.1/archive_bound_assumption.json --output outputs/investigation/bounded-answer.json
python scripts/investigate_sequence.py --verify outputs/investigation/bounded-answer.json
```

| Question | Unrestricted | With the illustrative archive bound |
|---|---|---|
| T1059 → T1059 → T1059 | Unresolved: archive occurrence could take T1059 | Not supported under the bound; the required archive label is excluded |
| T1059 → T1560 → T1059 | Unresolved archive mapping | Still unresolved; a candidate is not confirmed |
| T1021 → T1570 → T1218 | Supported core chain | Same supported core chain |

Version 2 answer records embed the full constraint record, the unrestricted answer and the constrained answer. Verification recomputes both against current case records and detects changes to recorded fields. It does not authenticate the author or independently validate a newly constructed record. Unconstrained version 1 records retain their existing structure and behavior. The browser's bundled case explorer continues to show unrestricted answers; custom bounds are a CLI feature.

## Verification and research boundary

An independent completion enumerator checks **21,952** graph-query inputs: three ordered vertices, every forward-edge subset, two query labels and seven per-vertex states (three known sets and four unknown/domain states). The implementation agrees with the enumerator and preserves known witnesses. In 1,456 constructed inputs, a declared bound changes unresolved to not supported. These are assumption-dependent changes, not corrected field errors or an accuracy improvement. [Results](results.json) retain the counts and scope.

The original unrestricted benchmark, two source cases and frozen five-publisher comparison are unchanged. No candidate sets have been retroactively imposed on those evaluations. Practical validation needs separately justified candidate bounds and an evaluation design fixed before inspecting resulting scores. Incorrect bounds can suppress a real possibility; provenance references alone do not prevent that error.

```sh
python -m examples.bounded_mapping_checks
python scripts/reproduce_study.py
```

The complete reproduction includes `bounded_mapping_checks.json` and `bounded_mapping_assumption_example.json`. Regression checks cover CLI export and verification, missing references, invalid domains, multiple paths, singleton uncertainty, unchanged unrestricted results and the finite completion enumeration.

## Discovery-role sensitivity across three cases

The [design](DISCOVERY_PROTOCOL.md) was [published before scoring](https://github.com/sanketnichit/cti-evidence-lab/commit/225ad1312218b146c4a7bcccdd9dd62b098918e8). It bounds four explicitly grouped discovery occurrences and leaves eleven other unknown mappings open. The conditions use 30 active Discovery parents or 43 active Discovery and Execution parents from the pinned release. Every condition uses the same query vocabulary for a given case.

| Case | Queries | Known support in every condition | Unresolved, open | Unresolved, Discovery or Execution | Unresolved, Discovery only |
|---|---:|---:|---:|---:|---:|
| Hive | 1,331 | 1 | 526 | 497 | 490 |
| NetSupport | 3,375 | 7 | 907 | 455 | 268 |
| CISA AA25-266A | 216 | 3 | 46 | 43 | 43 |

All other queries are unsupported in the corresponding retained graph. In NetSupport, removing only the narrower bound on domain-controller discovery restores 419 unresolved answers. Removing only the bound on the earlier discovery group restores 250. These are separate counterfactuals with overlapping query sets. Both bounds leave known support unchanged.

Both candidate sets change one of the two originally unresolved projected NetSupport answers to unsupported under the assumptions. Neither changes the three originally unresolved projected answers in the CISA graph. In the affected NetSupport query, the possible occurrence path depended on assigning credential dumping, T1003, to a reported discovery group. The known projected pairs remain in place.

NetSupport's fixed query vocabulary contains no Discovery labels. The narrower condition therefore excludes every witness through either bounded occurrence for that matrix. The choice of query vocabulary partly explains the large decrease. As an illustration outside the frozen matrix, T1219 → T1082 → T1098 remains unresolved under the narrower bound because T1082 is allowed for the earlier discovery group. This exercise measures sensitivity to the candidate sets and query scope. It supplies no independently validated correction rate. [Recorded results](discovery_results.json)

```sh
python -m examples.discovery_bound_sensitivity
python -m examples.discovery_bound_sensitivity --taxonomy /path/to/enterprise-attack-12.1.json
```

The optional taxonomy argument checks the release hash and regenerates both tactic lists. The recorded design and case hashes use sorted, compact JSON so checkout line endings do not affect them. The complete reproduction recomputes the comparison and includes `discovery_mapping_sensitivity.json`.
