# Evidence-backed sequence investigation

**Updated 20 November 2026. Working prototype and evaluation contract.**

## Decision supported

Given a three-technique query, does the retained interpretation contain three distinct occurrences connected by two supplied BEFORE edges? If a technique graph answers yes, which source occurrences actually connect? If the answer depends on unresolved mappings, which mappings matter?

The investigator returns an inspectable answer record containing occurrence and relation identities, source locators, mapping caveats, profile choices and input hashes. It also shows the specific incompatible edge joins behind projected paths. The record can be exported and recomputed against the repository. This is reproducible evidence accounting, not a digital signature or proof that an interpretation is semantically correct.

## Relationship to the closest work

| Work | Established capability | What this prototype tests |
|---|---|---|
| [Attack Flow language, checked 19 November 2026](https://center-for-threat-informed-defense.github.io/attack-flow/language/) | Discrete action identities, optional technique IDs, action-level source references, confidence and effects | A query-specific diagnostic over explicit BEFORE relations, with occurrence witnesses and incompatible joins. Attack Flow effects are not imported as temporal evidence. |
| [ChronoCTI, sections 4.5–4.6](https://link.springer.com/article/10.1007/s10115-025-02491-6) | Temporal relation extraction over technique pairs and aggregated temporal features | Representational fidelity on supplied occurrence graphs. The technique-pair control is an abstraction baseline, not a run of ChronoCTI or a claim about its extraction scores. |
| [AttackSeqBench v3](https://arxiv.org/abs/2503.03170v3) | Benchmarking reasoning about attack sequences across tactical, technical and procedural dimensions | Recomputable witnesses and abstention for one tightly specified graph query. This is not a replacement for its broader question-answering evaluation. |

Action graphs, provenance and reasoning under incomplete information are established ideas. This prototype does not claim to invent them. Its candidate contribution is the combination of a precise CTI query contract, failure localization, source-bound interpretations and query-specific uncertainty checks. Novelty and practical benefit beyond this combination remain to be demonstrated.

## Answer semantics

- **Supported:** at least one retained path has all three queried labels in its known mapping sets. The answer remains conditional on those sets, identities and relations.
- **Unresolved mapping:** no fully mapped witness exists, but a retained path could match if the listed unknown mappings received the required labels.
- **Not supported:** neither kind of witness exists in the retained graph. This does not establish absence in the incident or report.

Unknown mapping sets may take any queried label. Known sets and supplied edges remain fixed. This is deliberately an open mapping-completion rule, not a closed list of the previously proposed candidate labels. It does not model missing actions, missing temporal edges, mistaken mappings, uncertain coreference or every alternative interpretation.

Query-specific status differs from an aggregate error score. In the archive-withheld profile, only two of four source paths are fully mapped, so the case-level error score remains unassessed. The RDP → transfer → execution query nevertheless has a complete witness and can be supported. No earlier aggregate results are changed.

## Optional mapping bounds

The CLI now accepts explicit allowed-label bounds for unknown occurrences. A bounded export retains both the unrestricted answer and the answer under the assumptions, plus paths excluded by those bounds. A singleton candidate remains unresolved. These constraints cannot modify known mappings, and source-reference checks do not establish that a candidate list is exhaustive. The [mapping-bound contract and example](experiments/bounded_mapping_v0.1/README.md) describe the format and 21,952 finite checks. Existing case results and the five-publisher comparison retain their unrestricted semantics; the browser explorer also remains unrestricted.

## Implemented investigation tasks

| Task | Record | Inspectable outcome |
|---|---|---|
| Verify an ordinary sequence | Domain-controller core query | One connected occurrence witness and its source bindings |
| Diagnose a misleading path | Extended archive → script → archive query | The two middle script IDs differ; ordinary traversal joins incompatible edge images |
| Explain a missed answer | RDP full-edge repeated-technique query | A real witness exists, but excluding diagonals removes a required edge image |
| Identify a resolvable uncertainty | Withheld archive mapping on a compatible source path | The unknown occurrence and required technique are named explicitly |
| Check stability | Same query across same-taxonomy profiles | Inclusion, edge and mapping changes remain visible; no probabilities inferred |
| Reproduce an answer | Downloaded JSON record | Exact recomputation against current case records detects changed answers or evidence metadata |

## Evaluation completed

The finite completion oracle checks **1,728** graph-query inputs: three ordered vertices, two labels, singleton-or-unknown mappings and all forward-edge subsets. It independently enumerates assignments to unknown labels and agrees with the three-way query classification. This is a bounded implementation check, not a universal theorem or field evaluation.

All **532** case/profile/query combinations in the two cases and eight profiles are generated from their candidate-label vocabularies. Tests check witness references and source-locator completeness. A DOM harness exercises all query states and both case snapshots. A separate Chromium test opens the offline file at 320, 390 and 1280 px, checks the three answer states for viewport overflow, verifies keyboard navigation and accessible selector names, and downloads an answer for CLI verification. A local Chromium run also checked publisher snapshot matching and verified that a rejected snapshot with an external image reference generates no web request. Desktop and narrow screenshots were inspected. This covers one browser engine and selected accessibility checks.

The case queries produce 16 supported, 15 mapping-unresolved and 501 not-supported answers. These totals are constructed coverage counts over overlapping profiles, not 532 independent observations, accuracy scores or prevalence estimates. [Machine-readable results](experiments/investigation_v0.1/results.json) retain the denominators and per-profile breakdown.

## Fixed external comparison

A [five-publisher extension](experiments/external_sequence_evaluation_v0.1/README.md), selected before content review, retains all five reports and separates incident evidence from conditional procedures. Four procedure graphs yield 70 constructed queries: two supported, four unresolved and 64 not supported in the retained graphs. All four representations agree on the decidable queries. No qualifying incident sequence is established in this group. The password fallback exposes an overbroad possibility under open mapping completion; it is not scored as a proven false positive. These results constrain the prototype claim and do not measure analyst efficacy.

## Remaining efficacy test

The [analyst pilot protocol](ANALYST_PILOT_v0.1.md) fixes eight tasks and crosses the two reports, views and presentation orders. It includes packet generation and scoring for statuses, abstentions and relation witnesses. Participant data collection has yet to begin.

The consequential claim is that witnesses and targeted abstention help resolve an investigation question more accurately or with less effort than a technique-only view. That claim requires a fixed task set and separate scoring for answer correctness, source support, warranted abstention and interpretation errors. Analyst time savings and independent reliability have not been measured. No performance superiority is claimed from a functional interface or passing software checks.

## Reproduction

```sh
python scripts/build_investigation.py
python scripts/investigate_sequence.py --case domain-controller --profile extended_script_sequence --query T1560 T1059 T1560 --output outputs/investigation/answer.json
python scripts/investigate_sequence.py --verify outputs/investigation/answer.json
python -m examples.investigation_benchmark
```

Open `outputs/investigation/index.html` directly in a browser; it needs no service or network connection. The bundled query pickers cover the recorded candidate labels. The CLI accepts other identifiers under the same graph semantics. Raw reports are excluded. Optional local HTML loading displays passages only after the paragraph snapshot hash matches; it transmits no source text.

For DOM integration checks, install `jsdom@26.1.0` into a separate test directory and run `node scripts/test_investigation_ui.cjs /path/to/jsdom`. Two optional source-HTML arguments enable the matching-snapshot and rejection checks. The main Python analysis remains standard-library only.

For the browser check, install `playwright@1.58.2` into that test directory and run its CLI with `install --only-shell chromium`. Build the investigator and run `node scripts/test_investigation_browser.cjs /path/to/playwright`. An optional domain-controller HTML argument enables the matching snapshot check. The browser run writes screenshots and `browser-export.json` in `outputs/investigation/`. GitHub Actions runs the browser check and uploads the screenshots alongside the offline file.
