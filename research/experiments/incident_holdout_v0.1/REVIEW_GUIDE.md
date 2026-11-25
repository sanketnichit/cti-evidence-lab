# Independent review of two incident summaries

Review the two reports in `sources.csv` in the listed order. Read each Case Summary in full. Use the rest of the report to check ambiguity or contradictions. Work independently and use only the source pages, the pinned technique definitions, and this packet until you submit. Record prior exposure to proposed answers or another review in `reviews.csv`.

## What to record

1. Complete one row in `reviews.csv` per report. Mark a report `COMPLETE`, `PARTIAL` or `INACCESSIBLE`. A complete review can retain zero actions or zero relations. In the notes, record the source access date and any snapshot identifier you received. Explain exclusions, uncertainty and any scope limitations.
2. In `actions.csv`, assign a local ID to each candidate action that can participate in an explicitly ordered chain of three actions. Give a short paraphrase, the evidence location and the reason for your choice of action boundary. Use `RETAINED`, `UNCERTAIN` or `EXCLUDED` for eligibility. For outcome, use `REPORTED`, `SUCCEEDED`, `ATTEMPTED` or `UNCERTAIN`. A failed attempt can be a distinct action.
3. Use the [Enterprise ATT&CK v12.1 release](https://github.com/mitre-attack/attack-stix-data/blob/master/enterprise-attack/enterprise-attack-12.1.json). Record a parent technique ID only when the action evidence justifies it. Leave the mapping empty if it remains unresolved, and explain why.
4. In `relations.csv`, refer to the IDs in your own action table. Use `BEFORE` for an ordering supported by the words of the Case Summary or by a stated time reference. Use `UNCERTAIN` for an ordering that depends on ambiguous identity, timing or scope. Use `EXCLUDE` for a tempting pair you judged out of scope. Include your rationale. Narrative position and tactic order alone are insufficient. Record both edge directions only when you are documenting competing uncertain readings.
5. For each action or relation, name the paragraph within Case Summary, counting the first prose paragraph as 1. Add a short paraphrase of the specific clause that identifies the evidence. If you relied on a detail elsewhere to qualify an interpretation, include its section name and location in the rationale. Use your own words throughout.

Save the original CSV filenames, headers and UTF-8 encoding. Return `reviews.csv`, `actions.csv`, `relations.csv` and `packet.json`. Use the assigned reviewer ID and omit names, email addresses and other personal details.
