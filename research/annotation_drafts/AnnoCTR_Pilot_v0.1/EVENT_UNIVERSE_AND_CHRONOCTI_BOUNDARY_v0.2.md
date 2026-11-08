# Event-universe and ChronoCTI comparison boundary — decision note v0.2

**Prepared:** 8 November 2026  
**Status:** Working research-design decision adopted under delegated project direction. Protocol/schema freeze remains pending. This decision does not approve any individual pre-annotation unit or create human annotations.

## 1. Decision

Use **incident-linked attack-action occurrences** as the primary analytical stratum for the ChronoCTI-comparable study. Retain other report-local event-like material in separately identified descriptive strata. Do not mix those strata in the primary event-pair universe, positive-edge counts, pair-opportunity denominators, or ATT&CK projection metrics.

This refines the earlier v0.1 proposal. The unit is not restricted to actions physically performed by an attacker, nor to victim-side intrusion actions only. It is defined by the action's function in a specific attack incident.

## 2. Operational definition

An **attack-action occurrence** is a concrete, report-local action that the source describes as part of conducting, enabling, or completing a specific cyberattack or attack incident. It may be performed by an adversary, malware, or a user/system whose action is induced or manipulated as part of the attack chain.

Examples can include:
- delivery of a targeted phishing email or malicious attachment;
- a targeted user's opening or execution of a malicious attachment when the report supports that occurrence;
- exploitation, execution, persistence, command and control, collection, exfiltration, impact, or an operational extortion step;
- a preparatory or infrastructure action only when the source ties that specific action to the conduct of the particular attack.

An event does **not** qualify merely because it appears in a CTI report, is performed by a threat actor, has a date, or can be assigned an ATT&CK technique. It must be a concrete action in a report-supported attack chain, not simply commentary about that chain, an analyst observation, a general capability, or an infrastructure state observed after the fact.

Classification is independent of ATT&CK mapping. A qualifying attack-action occurrence remains in the primary event universe even when no defensible ATT&CK mapping is available; that outcome must remain visible as unmapped. Conversely, a report-level ATT&CK list or a plausible technique label does not make a communication, observation, capability, or generic description a primary attack-action occurrence.

## 3. Medium-neutral boundary for communications

Communication is not automatically excluded. Classify by operational function, not by medium.

- Include a targeted phishing message, malicious delivery message, or a victim-directed extortion/ransom communication when the source ties it to a specific attack as an operational step.
- A leak-site publication may qualify when the source establishes it as an incident-linked extortion/impact step, rather than merely an observation that data was publicly hosted.
- Keep forum creation, public source-code posts, public claims, response blogs, and commentary in a **threat-actor communication/platform stratum** unless the source establishes that the communication itself performed an operational step in a specific attack.
- Do not convert publication dates into attack-occurrence times without source evidence that the publication is the attack action being studied.

The Intel471 dates for the dyadka0220 source-code post (3 September 2021) and Groove response blog (7 September 2021) support a candidate temporal relation between two communication occurrences. On the current source review, they are not demonstrated as two steps in one operational cyberattack. Retain the candidate in the communication stratum; do not use it as a primary ChronoCTI-comparable attack-action edge.

## 4. Parallel descriptive strata

Retain relevant source-derived units, including resolved atomic communication events, without pooling them into the primary attack-action analysis:

1. **Threat-actor communications/platform events:** forum launches, public posts, claims, response blogs, and disclosures that are not established as operational steps in a specific attack.
2. **Analyst/sample observations:** sample detection, scanner submission, discovery, reverse engineering, or lab analysis. These describe an observation or analysis process, not automatically an attack action.
3. **Generic capabilities/behaviour:** malware functions, command handlers, generalized TTPs, or recurring patterns without a resolved report-local execution. Retain as generic/unresolved behaviour; do not fabricate atomic events.
4. **Other non-primary activity:** report-local events that do not meet the primary definition and do not fit the above strata; retain with rationale.

Only occurrences classified as ATTACK_ACTION may enter the primary ChronoCTI-comparable event-pair universe, and only after they independently pass the existing resolved/atomic/event-leaf, evidence, relation, and scope gates. Relations between two communication events may be described in a parallel view. Mixed-stratum relations do not enter the primary graph.

## 5. ChronoCTI alignment and rationale

The version-of-record ChronoCTI paper describes its target as temporal relations among attack actions in cyberattack incidents. Its report-selection criteria require step-by-step incident narratives and exclude social-media posts, malware features/capabilities, and other non-attack material. Its own example treats phishing followed by a user executing a malicious macro as an attack-action sequence, which is why an attacker-only or victim-side-only restriction would be too narrow.

Reference: Rahman et al., *Mining temporal attack patterns from cyberthreat intelligence reports*, Knowledge and Information Systems (published 22 July 2025), https://doi.org/10.1007/s10115-025-02491-6, especially Sections 1, 2.3 and 4.4.2.

This aligns the comparison population without claiming that the project reproduces ChronoCTI's model, labels, or performance evaluation. Preserve the raw ChronoCTI labels and the separate proposed crosswalk; this event-universe decision does not settle label semantics or the comparison-scope rule.

## 6. Consequences for the five-report feasibility draft

The current pre-annotation proposals remain unaccepted and are not empirical findings:

- **Intel471:** the forum launch and two public communication events remain outside the primary attack-action stratum on current evidence. The 3 September / 7 September communication pair remains a secondary candidate relation.
- **Lab52:** sample analysis is an analyst observation; reverse-engineered command handlers and malware functions are generic capabilities unless the report establishes specific executions.
- **Proofpoint:** the campaign and delivery chain remain at episode/series or generic-behaviour level in the current draft; do not invent atomic executions.
- **QuoIntelligence:** sample detections are analyst observations; the compromise remains an unresolved episode in the current draft.
- **Zscaler:** the specifically dated spear-phishing email is a candidate primary attack-action occurrence. It still requires human source review; no second resolved primary event endpoint or primary positive temporal relation is currently proposed.

The fixed five-report set remains a feasibility set. Do not replace reports or broaden the event universe because the current drafts yield few or no primary temporal edges. If the primary event/edge yield is inadequate, report that limitation and design a separately justified confirmatory sample; do not change the estimand after seeing the yield.

## 7. Schema and freeze implications

RECON v0.4 now implements the logical activity_unit.activity_stratum field as a required one-to-one companion register, activity_unit_strata.csv. This preserves the checksum-controlled v0.1 base package rather than editing its frozen activity_units header in place. The controlled vocabulary is ATTACK_ACTION, THREAT_ACTOR_COMMUNICATION, ANALYST_OBSERVATION, GENERIC_CAPABILITY, OTHER_NON_PRIMARY, and UNRESOLVED_CLASSIFICATION. The v0.4 validator enforces complete, evidence-backed coverage; the projection helper sends only ATTACK_ACTION event leaves, mappings, direct positive relations and pair opportunities into primary metrics. Same-stratum auxiliary and mixed-stratum relations remain visible in separate diagnostics. The stratum lock binds those decisions to the v0.2 selected-analysis lock. Synthetic tests cover the routing and post-lock mutation gate. The extension is structurally implemented but remains a draft pending protocol/schema review and freeze. The pre-annotation CSV's analysis_stratum_candidate remains triage metadata, not a canonical decision.

The existing analysis_stratum_candidate column in the pre-annotation CSV is a proposal aid, not a canonical annotation field. Do not begin formal annotation or call the schema frozen until this requirement is implemented and reconciled. No human annotations, selected final partitions, real-report projections, IAA results, or empirical findings are created by this decision.