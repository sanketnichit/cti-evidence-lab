# Sequence witnesses across alternative interpretations

The [v0.1 preprint](https://doi.org/10.5281/zenodo.24533052) studies whether technique-pair projection loses sequence witnesses within a supplied graph. This experiment studies a different failure. An apparent witness can retain all three occurrence identities while combining edges or labels that are never present together in one recorded interpretation.

## Ordering-evidence sensitivity design

Use all six cases already included in the offline investigator and every recorded parent-level profile. Keep unassessed cases visible. This is a fixed artifact cohort of four DFIR reports and two CISA advisories. The case records and their prior review status determine the cohort.

Compare deletion of one ordering row with withdrawal of one source unit at a time. For HTML, a unit is a cited paragraph. For PDFs, it is a cited page. Withdrawing a unit removes every ordering row that cites it, including rows with citations to other units. This conservative rule models loss of jointly cited evidence. It does not decide whether another citation suffices. Occurrences and mappings stay fixed. The vocabulary is the active profile's known parent labels before deletion. The possible-witness calculation admits each of those labels at withheld mappings.

For each intervention report the number of rows removed, witness counts lost and query status changes. A query can retain its status after losing a witness. Report how many distinct supported queries lose support somewhere in each intervention family. Retain evidence IDs and affected row IDs to allow inspection. Compare deletions within each profile. These interventions measure sensitivity to the recorded evidence bindings, with different unit granularity for DFIR and CISA.

The six cases yielded 11 parent profiles, one of which remained unassessed. All 23 supported profile/query instances lost support under at least one single-row deletion. The grouped interventions therefore identified no additional fragile fully supported queries in this cohort. In the constructed control, two alternative witnesses survive every single-row deletion but both disappear when their shared citation page is withdrawn.

| Case and recorded profile | Initially unresolved | Most lost after one row deletion | Most lost after one unit, first citation rule | Most lost after one unit, last citation rule |
|---|---:|---:|---:|---:|
| ScreenConnect to Hive | 526 | 203 | 223 | 223 |
| NetSupport | 907 | 387 | 611 | 596 |
| CISA AA25-266A | 46 | 28 | 34 | 28 |

The first citation rule drops a row when any cited unit is withdrawn. The last citation rule retains it while at least one cited unit remains. Multiple spans on one page still count as one unit. These rules bound witness losses and the number of unresolved queries that become unsupported for policies that retain every intact row and remove every row that loses all its citations. They do not determine whether the surviving passages support a particular edge. In NetSupport, paragraph 5 yields the largest loss under both rules. One of its three ordering rows also cites paragraph 6 and survives under the last citation rule. Across the CISA profile, the largest grouped loss exceeds the individual-row loss only under the first citation rule. The unresolved counts depend on the open mapping assumptions and count conditional queries within a profile. [Detailed results and citations](ordering_evidence_results.json)

For each fully supported query, the analysis searches unit subsets in increasing size and records one smallest set that removes every known witness. The first citation rule gives a one-unit cut for all 23 supported instances. Under the last citation rule, 17 still have a one-unit cut and six domain-controller instances require two units. These six come from three profiles of one incident. The JSON stores the first rule's interventions under `source_unit`. The `last_citation_overrides` entries replace only the units whose affected rows differ. The `minimum_source_unit_cuts` rows list one exact minimum under each rule.

```sh
python -m examples.ordering_evidence_sensitivity
```

Full reproduction checks and includes `ordering_evidence_sensitivity.json`.

### Reading the citations behind the six rule-sensitive instances

All six instances came from the domain-controller report. We examined every ordering row in that report, conditional on the supplied occurrence identities. A passage counts as sufficient when it gives the relative order of those actions. A temporal reference to the preceding paragraph also needs the paragraph identifying its antecedent. The original HTML and all 13 recorded span hashes matched the saved snapshot. This follow-up was selected after observing the difference between the two rules. [Case record and passage locators](../../case_studies/dfir_html_smuggling_v0.1/case.json)

| Row | Sufficient paragraphs under this reading | Basis |
|---|---|---|
| B1 | 9 or 54 | Paragraph 9 describes transfer through the established session. Paragraph 54 places the transfer during that session, assuming the recorded session identity. |
| B2 | 9, 25 or 66 individually | Each places execution of the transferred file after the transfer to the domain controller. |
| B3 | 9 and 10 together | Paragraph 10 orders discovery after a preceding action. Paragraph 9 identifies that antecedent as execution on the domain controller. |
| B4 | 10 or 63 | Both place archiving after discovery completed, given the recorded identity of the discovery run. |
| B5 | 10 | This paragraph explicitly orders the second batch run after archiving. |

Re-executing the queries over paragraph withdrawals gives two distinct outcomes among the six. The session–transfer–execution sequence occurs in three profiles. In each, its only smallest withdrawal set is paragraphs 9 and 54 together. The other three instances depend on B3. Removing either paragraph 9 or paragraph 10 alone breaks their known witness. These counts describe repeated queries in one incident. Independent assessment of the antecedent and occurrence identities remains open. Run `python -m examples.domain_controller_citation_roles` for every minimum set, including the seventh supported instance where the original bounds already agreed.

### Independent review of the citation reading

The review packet gives the publisher link, five proposed action orderings and their candidate passage locators. Provide the ZIP alone to each reviewer. The form asks which passage sets establish the ordering and records uncertainty about the action identities. Generate one packet per reviewer.

```sh
python scripts/review_domain_controller_citations.py --reviewer R01 --output outputs/citation-review-R01.zip
python scripts/review_domain_controller_citations.py --return-form outputs/returned/R01/review.json --output outputs/returned/R01/analysis.json
```

Use `--source-html` when the reviewer supplies their snapshot. The result records the snapshot check, declared exposure, input hash and rows whose sets match the project reading. A complete return recomputes the seven original supported profile/query instances. An empty withdrawal set means the returned judgments already leave the query without a known witness. A partial return records the undecided rows and leaves the cut analysis pending. Report the judgments descriptively for this incident, conditional on the given action pairs and candidate passages. Keep individual returns and analyses private.

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

## Sensitivity to omitting interpretations

For each of the three recorded groups, keep the full group's parent-technique vocabulary and evaluate every nonempty subset of profiles. Each query keeps the best status reached in one retained profile. The analysis holds the open mapping rule fixed and checks each retained subset against direct queries on its constituent profiles. It counts how many omissions are needed for the first status drop and records the affected supported queries.

| Group | Initially supported | Lose support after one omission | Need two omissions to lose support | Supported in every nonempty subset |
|---|---:|---:|---:|---:|
| Domain controller | 4 | 2 | 1 | 1 |
| RDP | 3 | 1 | 2 | 0 |
| NetSupport | 8 | 1 | 0 | 7 |

Omitting the co-referent NetSupport interpretation makes the WMI sequence unsupported within the remaining readings. The other three single-omission losses shift from supported to unresolved. For queries initially classified as unresolved, eight domain-controller queries and two RDP queries become unsupported under a single omission. In NetSupport, 14 require two omissions and 893 remain unresolved in every nonempty subset. These counts describe sensitivity to the supplied readings. Several profiles reuse the same evidence, so categorical stability does not establish independent corroboration. [Recorded results](profile_omission_results.json)

```sh
python -m examples.profile_omission
```

Full reproduction checks and includes `profile_omission.json`.

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

Query status can agree even when a pooled explanation includes an unsupported sequence. In the matched control `same_status_different_witnesses`, two profile pairs have identical fact counts and each contains a shared valid path. Only the pair that splits the other path's edges across profiles has a pooled-only witness. Witness-level enumeration found none in the recorded RDP, domain-controller, or NetSupport groups. The `possible` count includes known witnesses. [Control and original group counts](uncertainty_results.json) · [NetSupport counts](netsupport_identity_results.json)

The comparison export includes the per-profile answers, mappings, relation evidence, and all pooled candidates. Each candidate names its supporting profiles or records a minimum conflict. The possible-witness list includes fully known witnesses. Conflict fact indices are one-based within the fact list, and profile numbers refer to `answer.profile_order`.

```sh
python scripts/compare_sequence_profiles.py --group netsupport-identity --query T1562 T1047 T1053 --output outputs/profile-comparison.json
python scripts/compare_sequence_profiles.py --verify outputs/profile-comparison.json
```

The other groups are `rdp` and `domain-controller`, both at the parent level. The NetSupport export exposes the identity assumption behind the WMI witness. Full reproduction includes the verified example. [v0.2 manuscript draft](../../PROFILE_COHERENCE_REPORT_v0.2.md)

Add `--summary-only` for a compact export. Per-profile witnesses and incompatible joins are counted. The pooled witnesses, minimum conflicts and source records are still included. Verify either export with the same `--verify` command.

The offline investigator displays the same parent-level comparisons. Build it with `python scripts/build_investigation.py` and open `outputs/investigation/index.html`. Choose NetSupport and **Show the WMI identity example** to see which reading connects the firewall change and task creation through the same execution. Expand **Actions and source evidence** for the two ordering relations and their passage locators. The constructed pooling example identifies the split edges and the profiles that provide them. **Download comparison record** saves the compact format used by the verifier above.

## Runtime and storage design

Each synthetic profile contains disjoint three-action paths. One path in four splits its edges between alternating profiles, and the middle mapping is withheld in one path in eight. The query fixes one label at each position. The design varies actions per profile (24, 96, 192 at two profiles), profile count (2, 8, 16 at 96 actions), and label density (one or four known labels at 96 actions and two profiles). Query paths, ordering facts and action IDs are fixed when varying label density. Each workload checks the focused result against filtering the exhaustive masks and checks the exported support against those masks.

The benchmark times exhaustive masks, focused masks, and the full and compact comparisons separately. It warms each operation once, rotates their order over seven timed calls, and reports median wall-clock time. Input construction, serialization and file I/O are outside those timings. One separate `tracemalloc` call measures peak Python allocations for each operation, excluding the prebuilt inputs. Bytes are measured for pretty-printed UTF-8 JSON and gzip for the synthetic inputs alone and with either answer. Verified NetSupport exports supply sizes for a real artifact with evidence and spans included.

```sh
python -m examples.profile_scaling --output outputs/profile-scaling.json
```
