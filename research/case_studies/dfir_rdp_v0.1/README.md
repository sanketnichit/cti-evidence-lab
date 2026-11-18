# Repeated RDP attempts: source-bound exploratory case

**18 November 2026. Separately selected case; outside the AnnoCTR cohort.**

This advances the earlier conditional illustration into an explicit, source-bound interpretation. It remains unvalidated and cannot contribute to corpus prevalence or agreement statistics. Prior exposure and purposive selection are recorded in `case.json`.

## Source and interpretation

The DFIR Report's [A Truly Graceful Wipe Out](https://thedfirreport.com/2023/06/12/a-truly-graceful-wipe-out/), published 12 June 2023, narrates two attempted tunneled RDP connections around a temporary-account procedure. The first outcome is qualified; the second is reported as failed. The account's lifetime does not establish an exact inter-attempt duration. Account lifecycle statements and a network alert do not establish additional connection attempts.

The case retains two attempt-level occurrences and one direct BEFORE relation. This uses explicit repetition and ordering, not paragraph position. A group-level description can coexist with those leaves; replacing them by one group would answer a different granularity question. The mapping is an interpretation of attempted T1021.001 behavior, normalized to T1021 through the pinned Enterprise ATT&CK v12.1 crosswalk. It does not imply a successful authenticated session.

## Evidence and uncertainty

`case.json` records three evidence passages: the Case Summary, account-lifecycle context in Persistence, and the network observation in Command and Control. Each has canonical paragraph offsets, paragraph number and a substring hash. The record also includes retrieval time, raw HTML hash, canonical text hash, event and edge evidence references, decision rationales and the taxonomy file hash.

The publisher HTML was saved locally on 18 November 2026. It is not redistributed. Canonicalization extracts nonempty HTML paragraph text, decodes entities, collapses within-paragraph whitespace, and joins paragraphs with LF. This is a new snapshot convention for this case; it does not alter AnnoCTR's source convention. A changed source fails verification rather than silently moving the evidence. Raw HTML differences with identical canonical paragraphs are reported separately.

No images or underlying telemetry were independently validated. Hashes establish source identity, not correctness of event or mapping judgments. The retained count concerns the narrated attempts, not a complete inventory of packets, sessions or intrusion activity.

## Sensitivity analysis

| Analysis choice | Included occurrences | BEFORE edges | Fully omitted edges | Unmapped edges | Loop-inclusive pair images |
|---|---:|---:|---:|---:|---:|
| Include narrated attempts and proposed mappings | 2 | 1 | 1 | 0 | 1 |
| Require confirmed successful actions | 0 | 0 | 0 | 0 | 0 |
| Include attempts but withhold technique mappings | 2 | 1 | 0 | 1 | 0 |

The second row is a change of target population, not evidence that the attempts did not occur. The third row isolates mapping uncertainty: an unrepresented edge without mappings is not counted as diagonal omission. A loop preserves a technique-pair image but does not identify its occurrence endpoints. No corpus percentage is calculated.

This case has only one retained edge. It therefore **does not evaluate the connected two-step query** introduced in the query-fidelity study, which requires three occurrences and two source-supported edges. Finding and auditing suitable chains remains work to do. This case addresses the simpler same-technique edge question and exposes the effect of outcome and mapping choices.

## Reproduce

```sh
python scripts/analyze_rdp_case.py --output outputs/rdp_case_results.json
python scripts/audit_rdp_case.py --source-html /path/to/saved/source.html
```

The first command regenerates graph sensitivities from the recorded interpretation. The second rechecks a local publisher snapshot against the exact evidence bindings. The audit exports hashes and offsets, not source paragraphs. `source_integrity.json` records the completed local audit, while `results.json` records the deterministic analysis. Their roles are separate.

The record does not modify formal annotation locks, the fixed five-report sample, or earlier protocol-development records. Original publisher content retains its own rights; the repository software licence does not grant rights to the article.
