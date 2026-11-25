# Chronological incident holdout results

The [protocol](PROTOCOL.md) was published in [8a89f97](https://github.com/sanketnichit/cti-evidence-lab/commit/8a89f977a937bb278984a5363f01149be09345c1) before reviewing both selected reports for this comparison. Both reports supplied usable Case Summary graphs. This holds publisher and genre roughly constant while testing new incidents. The frame is the saved metadata response from one publisher.

| Report | Actions / ordering links | Withheld mappings | Supported / unresolved / unsupported queries | Ordinary projected returns | Endpoint-compatible returns |
|---|---:|---:|---:|---:|---:|
| [ScreenConnect to Hive](https://thedfirreport.com/2023/09/25/from-screenconnect-to-hive-ransomware-in-61-hours/) | 17 / 16 | 6 | 1 / 526 / 804 | 1 supported | 1 supported |
| [NetSupport intrusion](https://thedfirreport.com/2023/10/30/netsupport-intrusion-results-in-domain-compromise/) | 27 / 22 | 5 | 7 / 907 / 2,461 | 7 supported, 2 unresolved, 3 unsupported | 7 supported |

The four representations give the same answer in the Hive case for every decidable query. Its fully mapped witness connects the start of exfiltration, an account change and manual encryption. The recorded graph distinguishes the successful manual encryption from the failed wider deployment. It leaves several grouped or underspecified actions unmapped. In the NetSupport case, we exclude reported inferences of exfiltration and keep failed or uncertain attempts visible where they take part in a candidate chain.

The ordinary distinct-pair and loop-preserving views agree on the NetSupport errors. The three unsupported returns each join two edges at a shared label even though the edges name different middle actions:

| Projected query | Ambiguous join |
|---|---|
| T1003 → T1059 → T1219 | A later event collection action is joined to an earlier script execution because both map to T1059. |
| T1105 → T1059 → T1560 | The same two script occurrences are joined in the opposite direction. |
| T1562 → T1047 → T1053 | A transition to remote execution is joined to a separately described payload execution through the shared WMI technique label. |

The first and third errors depend on potentially contestable readings. The reference in B21 could denote the preceding episode as a whole. Omitting it leaves six supported and two unsupported projected answers. The broad remote execution description in B12 may group events that the next sentences describe in more detail. Omitting it leaves seven supported and two unsupported projected answers. Omitting both leaves six supported returns, one unresolved return and one unsupported return in each ordinary view. The surviving T1105 → T1059 → T1560 mismatch joins the early script execution (P2) to later event-log collection (P10). The source describes these as separate actions. This is a post-review check of the existing interpretation. Independent identity adjudication remains pending.

The query counts enumerate label triples for each retained graph. Their size depends on the vocabulary, and the open mapping rule admits some implausible completions. They should not serve as independent sample sizes or performance rates. The report-level finding is one agreement case and one case with conditional join errors. Independent reviewers and a different publisher frame are needed for broader conclusions.

## Reproduction

```sh
python scripts/evaluate_incident_holdout.py
python scripts/evaluate_incident_holdout.py --source-directory outputs/incident_holdout
```

The first command recomputes [results.json](results.json) from the two case records. The second also checks the canonical text and 28 paragraph bindings against the locally saved publisher HTML files named `21520.html` and `22587.html`. Compare the source hash first if retrieving the pages again. CI reproduces the result from the recorded case evidence. The taxonomy definitions were checked against the pinned Enterprise ATT&CK v12.1 release, whose hash is recorded with each case. No publisher HTML is included in the repository.

## Independent source review

The [review guide](REVIEW_GUIDE.md) and packet generator provide source links and blank forms for an independent reading. They contain no proposed actions, labels or answers. Generate one packet per reviewer and provide only the ZIP.

```sh
python scripts/incident_source_review.py --build outputs/holdout-review --reviewer R01
python scripts/incident_source_review.py --build outputs/holdout-review --reviewer R02
python scripts/incident_source_review.py --validate /path/to/extracted-return
```

Keep the first submissions and a record of which source version each reviewer used. Paragraph locations refer to the opening prose under Case Summary. Resolve version differences against the recorded source hashes before comparing judgments. Structural validation checks form completeness, references and cycles in retained ordering. Semantic decisions require checking the source.

### Comparing two returns

Generate a blank alignment from two validated return directories. Keep those directories, the alignment and the output private.

```sh
python scripts/compare_incident_reviews.py outputs/returned/R01 outputs/returned/R02 --output outputs/review-comparison/alignment.json
```

For each report, set `source_basis` to `MATCHING`, `DIFFERENT` or `UNVERIFIED` and document the basis in `source_note`. Use `MATCHING` when the same saved snapshot was supplied or the Case Summary versions were confirmed to match. The tool records the coordinator's judgment. It compares decisions when both reviews are complete and the basis is matching. Leave `groups` empty for other reports.

Align actions using source evidence, incident scope and granularity before consulting the technique IDs or relation decisions. In `groups`, account for each submitted action once. Each group specifies `left` and `right` arrays of action IDs and a short `reason`. One ID on each side is a one-to-one match. Multiple IDs record a split, merge or many-to-many alignment. For an unmatched action, use one ID and an empty array on the other side. Preserve the completed alignment before scoring.

```sh
python scripts/compare_incident_reviews.py outputs/returned/R01 outputs/returned/R02 --alignment outputs/review-comparison/alignment.json --output outputs/review-comparison/descriptive-results.json
```

The result binds the exact returns and alignment by SHA-256 and preserves completion and prior exposure. Eligibility uses one-to-one matches. Outcomes and mappings use the one-to-one actions retained by both reviewers. Split, merged and unmatched actions contribute to alignment coverage. The candidate relation set is the union of directed pairs that either reviewer recorded between mutually retained one-to-one actions. Opposite directions stay separate. Each missing decision is `UNRECORDED`. Only pairs with a decision on both sides enter the exact-match numerator and denominator. The result preserves the candidate rows and the counts left outside the comparable set. Keep raw disagreements and subsequent adjudication in separate records.

The selected pair set is shaped by both reviewers' submissions. For two reports, report descriptive counts and worked disagreements with their denominators. Prior exposure should accompany any interpretation. No independent source-review results have been collected.
