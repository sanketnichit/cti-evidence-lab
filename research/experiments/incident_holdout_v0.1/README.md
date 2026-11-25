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

The first and third errors depend on potentially contestable readings. In a post-review sensitivity check, omit B21 because the reference to prior activity could denote the preceding episode as a whole. This leaves six supported and two unsupported projected answers. In a separate check, omit B12 because the broad remote execution description may group events that the next sentences describe in more detail. This leaves seven supported and two unsupported projected answers. The T1105 → T1059 → T1560 mismatch survives either omission because its middle actions belong to explicitly separate episodes. These checks address edge eligibility. Identity adjudication remains a separate source-review task.

The query counts enumerate label triples for each retained graph. Their size depends on the vocabulary, and the open mapping rule admits some implausible completions. They should not serve as independent sample sizes or performance rates. The report-level finding is one agreement case and one case with conditional join errors. Independent reviewers and a different publisher frame are needed for broader conclusions.

## Reproduction

```sh
python scripts/evaluate_incident_holdout.py
python scripts/evaluate_incident_holdout.py --source-directory outputs/incident_holdout
```

The first command recomputes [results.json](results.json) from the two case records. The second also checks the canonical text and 28 paragraph bindings against the locally saved publisher HTML files named `21520.html` and `22587.html`. Compare the source hash first if retrieving the pages again. CI reproduces the result from the recorded case evidence. The taxonomy definitions were checked against the pinned Enterprise ATT&CK v12.1 release, whose hash is recorded with each case. No publisher HTML is included in the repository.
