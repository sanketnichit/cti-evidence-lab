# Five-publisher sequence evaluation

**19 November 2026. Exploratory comparison; no independent semantic validation.**

The new source group does **not** establish a representation-accuracy advantage. This is a useful boundary on the prototype's claims, not a failed result to replace with more favorable reports.

## Fixed selection and scope

[Selection and protocol](PROTOCOL.md) were committed in [12033e2](https://github.com/sanketnichit/cti-evidence-lab/commit/12033e21e821df2cc65e077274b9e987d96c1659) before the five full corpus texts were read. The rank-three entries from the existing seeded five-donor frame were retained without replacements. All five complete texts were read; all five source identities and 17 passage bindings were rechecked. Ranks one and two and the existing DFIR cases are separate evidence groups.

| Publisher | Primary incident sequence | Secondary procedure | Consequential boundary |
|---|---|---|---|
| Intel471 | Not established | None scored | Defensive disruption is not an adversary intrusion step; ransomware discussion aggregates incidents |
| Lab52 / S2 Grupo | Not established | None scored | Explicit exploit-before-movement pair does not establish a second edge; kill-chain headings alone are insufficient |
| Proofpoint | Not established | Three conditional chains | Campaign delivery observations do not establish victim macro enablement; a local drop is not necessarily ingress |
| QuoIntelligence | Not established | None scored | Separate supply-chain examples and hypothetical access cannot be joined into one incident |
| ZScaler | Not established | Password fallback branch | Failed and fallback attempts are distinct; SMTP transmission lacks the evidence needed to accept T1048 |

The primary stratum therefore has **0 usable reports out of 5 selected**, with query errors **unassessed**, not zero. This is not evidence that the incidents lacked sequences. The bounded text interpretations omit image evidence and may be too conservative. In particular, a dependency-based interpretation of the Lab52 terminal-server account could admit an extra edge; this protocol disallows that inference.

## Conditional procedure results

Each graph is queried over its entire candidate-label triple universe. Procedures are scored separately so different campaigns cannot acquire cross-campaign edges. The two macro chains share a template and are not independent observations.

| Procedure | Queries | Supported | Mapping unresolved | Not supported in retained graph |
|---|---:|---:|---:|---:|
| Dridex macro chain | 27 | 1 | 0 | 26 |
| ZLoader macro chain | 27 | 1 | 0 | 26 |
| NetWire downloader chain | 8 | 0 | 2 | 6 |
| Password fallback | 8 | 0 | 2 | 6 |
| Constructed coverage total | 70 | 2 | 4 | 64 |

All four representations return the two supported answers and have **zero unsupported positives on decidable queries** and **zero missed supported answers**. These are conditional agreement counts, not extraction accuracy, prevalence or analyst performance. The two all-correct chains remain visible rather than being discarded.

Ordinary loop-preserving traversal also returns T1555 → T1555 → T1555 for the password fallback. Its one retained T1555 pair can be traversed twice. Endpoint joins reject that reused edge image. The investigator returns **unresolved mapping**, because the third action's mapping is unknown and the open completion rule permits T1555. It does not score the Boolean return as a proven false positive. Assigning a credential-recovery label to SMTP transmission is semantically implausible: this example exposes the looseness of unrestricted mapping completion. A future constrained-candidate model would need a declared, independently justified candidate set; it must not be introduced after seeing the answer simply to improve a score.

## Interpretation sensitivity

For the Dridex and ZLoader chains, user enablement, interpreter execution and payload transfer are three separately modeled actions. A coarser model merging enablement and execution leaves only two actions and no three-action query. That alternative is recorded, so the two supported answers cannot be presented as interpretation-independent facts.

The password branch assumes the first recovery attempt fails, the fallback succeeds and recovered credentials are transmitted. The source describes that procedure; it does not establish a victim-specific run. Webcam functionality is explicitly disabled in the analyzed configuration and separate stealing modules execute on separate threads. Neither is silently attached to this branch.

The pinned [Enterprise ATT&CK v12.1 STIX release](https://github.com/mitre-attack/attack-stix-data/blob/master/enterprise-attack/enterprise-attack-12.1.json) was downloaded and checked against the repository's existing SHA-256 before inspecting the five relevant parent definitions. T1048 requires a different protocol or alternate destination relative to the main C2 channel; SMTP alone does not establish that condition. Per-action rationales, rejected interpretations and source locators are in [review.json](review.json). Publisher text and taxonomy bytes are not bundled here.

## Reproduction

```sh
python scripts/evaluate_external_sequences.py
python scripts/evaluate_external_sequences.py --corpus-root /path/to/AnnoCTR/all --recover-crlf
python scripts/reproduce_study.py
```

The first command recomputes and compares [results.json](results.json) using public records only. The optional corpus command checks source hashes and all passage offsets. [source_integrity.json](source_integrity.json) records the local audit; hash verification does not establish semantic truth. The full reproduction package includes the generated comparison and its source audit. CI reruns the comparison and regression checks.

## Consequence for the paper

The synthetic result establishes a representational limitation and the earlier source cases illustrate it conditionally. This fixed extension provides broader publisher coverage but no new qualifying incident sequence and no new decidable accuracy advantage. A defensible paper must report that boundary. General usefulness still requires suitable incident-level evidence, an interpretation-error study and practical task evaluation. No analyst-time or independent-review claim follows from these records.
