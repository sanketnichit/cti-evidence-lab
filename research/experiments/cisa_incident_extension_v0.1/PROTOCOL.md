# CISA incident-response extension

Fixed 25 November 2026 before the full narrative review. This is a purposive cross-publisher comparison using a frozen discovery frame. The CISA advisory index returned HTTP 403. Search results and excerpts were visible before selection.

The discovery query was `site:cisa.gov cybersecurity advisories 2024 threat actors exploit compromise federal agency observed incident CISA AA 2024`, batched with `site:cisa.gov cybersecurity advisories archive 2024 federal investigation observed compromise incident CISA red team title AA` and `CISA cybersecurity advisories archived list 2024 AA24 catalog github json`. From the returned primary PDF candidates, retain the two with metadata and snippets identifying an incident-response investigation. The visible campaign advisory and red-team report are outside the target genre. Follow-up metadata lookup confirmed the product IDs. Keep both selected reports regardless of content yield or access. The search index and ranking do not define a census.

| Status | Product ID | Discovery disposition |
|---|---|---|
| Selected | AA24-046A | [Former employee account incident](https://www.cisa.gov/sites/default/files/2024-02/aa24-046a-threat-actor-leverages-compromised%20account-of%20former-employee.pdf) |
| Selected | AA25-266A | [Incident response engagement](https://www.cisa.gov/sites/default/files/2025-09/AA25-266A_advisory_cisa_shares_lessons_learned_from_ir_engagement.pdf) |
| Outside genre | AA24-241A | Campaign advisory |
| Outside genre | AA24-326A | Red-team assessment |

Read the incident narrative sections of the PDFs. Keep incident-linked actions with explicit dates, elapsed time or wording that orders two concrete actions. When actions have the same stated date, use within-day textual ordering only where the wording supports it. Treat time ranges and unresolved identities conservatively. Keep different hosts and different initial access attempts distinct. Use the reports' prose to identify candidates and exclude generalized tradecraft, recommendations, response actions and table-only technique listings. A repeated label is insufficient to connect two edges.

Record PDF page numbers, canonical page-text hashes and passage offsets. Use Enterprise ATT&CK v12.1 parent labels with a concrete rationale. Withhold uncertain labels. Apply the same three-distinct-action query, two explicit BEFORE edges and four representation controls used in the chronological holdout. Use the fixed per-case candidate vocabulary and separate supported, unresolved and unsupported results. A case without an assessable chain stays in the denominator with query errors unassessed. Interpret results as transfer to a different publisher and report format on a small set of cases.
