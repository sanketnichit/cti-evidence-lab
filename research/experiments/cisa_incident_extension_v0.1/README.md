# CISA incident-response extension results

The [protocol](PROTOCOL.md) fixed two advisories in [4226161](https://github.com/sanketnichit/cti-evidence-lab/commit/4226161d99c4b6b35f91acf38818fd0c82f5cbca) before full narrative review. The source frame is a recorded purposive search with prior snippet exposure. Both advisories remain in the denominator.

| Advisory | Retained actions / links | Withheld mappings | Supported / unresolved / unsupported queries | Distinct-pair returns | Loop-preserving returns | Endpoint-join returns |
|---|---:|---:|---:|---:|---:|---:|
| [AA24-046A](https://www.cisa.gov/sites/default/files/2024-02/aa24-046a-threat-actor-leverages-compromised%20account-of%20former-employee.pdf) | 3 / 1 | 2 | Unassessed | Unassessed | Unassessed | Unassessed |
| [AA25-266A](https://www.cisa.gov/sites/default/files/2025-09/AA25-266A_advisory_cisa_shares_lessons_learned_from_ir_engagement.pdf) | 13 / 11 | 4 | 3 / 46 / 167 | 3 supported, 2 unresolved | 3 supported, 3 unresolved | 3 supported in each join variant |

AA24-046A supports a link from account access to discovery. The report does not establish a distinct, observed intermediate action or order the grouped service authentications against the directory queries. The graph therefore contains no assessable two-edge sequence. The acquisition and subsequent use of credentials are also described with different levels of certainty. See the case record for individual exclusions.

In AA25-266A, all four representations preserve the three supported queries and return zero decided unsupported positives. The three extra loop-preserving returns are unresolved under the open mapping rule. Their projected joins lack a shared middle occurrence. A separate retained path could match if the required unknown mapping or mappings were accepted.

The repeated T1190 query exposes a specific limit. The projection reuses one edge between two separate dated access events and produces two hops. The only compatible occurrence witness would instead require assigning T1190 to two lateral-movement actions. Those assignments are unsupported by the source and arise because the open rule allows any label for an unknown action. The recorded classification remains unresolved. Treating the query as a decided error would require an independently justified mapping restriction. The [results](results.json) include each unresolved return, its incompatible join and the labels a separate path would require.

The AA25-266A graph uses the incident prose. Where the overview orders movement destinations and the detailed wording leaves the route unclear, the record retains the reported order and withholds a technique. The dated proxy passage may overlap another reported activity cluster, so it contributes no additional occurrence. These choices are reviewable interpretations. The two advisories establish one unassessable case and one case of agreement on decidable queries with unresolved projected returns. Report genre, vocabulary and annotation scope differ from the DFIR holdout, so the query counts remain separate.

## Reproduction

```sh
python scripts/evaluate_cisa_extension.py
python scripts/evaluate_cisa_extension.py --pdf-directory outputs/cisa_extension
```

The first command checks recorded results using the same graph evaluator as the chronological incident holdout. The optional PDF audit expects `AA24-046A.pdf` and `AA25-266A.pdf` in the supplied directory and `pypdf==6.21.4`. It verifies each PDF hash, the canonical text of every cited page, and all 16 passage hashes. Canonical text uses the layout extractor and collapses whitespace to single spaces per page. Offsets count Unicode code points and end exclusively. The local PDF renders were inspected to distinguish narrative paragraphs from figures and tables. The repository records offsets and rationales without republishing the PDFs.
