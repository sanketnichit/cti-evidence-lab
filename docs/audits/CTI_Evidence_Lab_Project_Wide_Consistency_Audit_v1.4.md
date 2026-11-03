# CTI Evidence Lab — Project-wide consistency audit v1.4

**Audit date:** 3 November 2026  
**Scope:** Research question and novelty positioning; GitHub state; AnnoCTR corpus/screening/sampling; five rank-1 source reviews and the ZScaler AI worked draft; protocol v0.4.1; schema v0.4.2 crosswalk; templates/validator; projection metrics/code; earlier DFIR cases; ChronoCTI baseline; related work; rights/provenance; frame/workbook integrity; current action order.  
**Status:** AI-assisted audit and recommendations. This is not a human annotation lock, a frozen protocol, legal advice, a novelty determination, or an empirical result.

---

**v1.4 update:** audited the new v0.4.2 schema package against protocol v0.4.1; identified remaining field/validator gaps; independently rechecked all 120 priority hashes, within-vendor ranks and source-text hashes; corrected stale dashboard and batch-review references in the sample-frame workbook; and flagged an Intel471 overlap between the base candidate list and stress queue.

## 1. Executive verdict

The project is **methodologically developed but not empirically demonstrated**. The local work includes a reproducible 400-report inventory, a deterministic all-120 candidate frame, five AI-assisted source reviews, a corrected selection rule, a v0.4.1 protocol draft, a v0.4.2 blank schema proposal with a conformance audit, a ChronoCTI workbook/code audit, and synthetic projection/validation prototypes. However, no human annotation has been locked, no real-report projection result exists, and novelty remains unproven.

The most consequential new finding is a close prior-work neighbour: Wu’s February 2026 NTU master’s thesis already performs incident-scoped malicious-activity extraction, assigns event IDs, maps events to zero or multiple ATT&CK techniques with evidence-grounded validation, infers temporal ordering and causal dependencies, and merges redundant/coarse events into an attack life cycle. Broad claims that CTI event-level temporal reconstruction is novel are therefore untenable. Our possible niche must be narrower and demonstrated through a systematic comparison: human source-evidenced temporal relations between resolved report-local occurrences, explicit occurrence/scope/granularity decisions, and quantitative analysis of what is omitted, partially retained, or conflated by a ChronoCTI-style distinct-technique-pair projection. Even that remains a candidate contribution.

The highest-priority open issues are:

1. **Literature positioning:** compare explicitly against Wu (2026), SMAH-CTI, APTIE, CASIE, ChronoCTI, and attack-sequence/dependency work. Do not claim that an event-extraction/ATT&CK/life-cycle pipeline is novel.
2. **Protocol/schema implementation:** v0.4.1 is a detailed but unapproved draft; v0.4.2 supplies the missing blank registers but still lacks a matching validator, explicit temporal `evidence_scope`, annotation/version/pass fields, defined evidence-link keys and enforced cross-register invariants.
3. **Projection implementation:** the prototype does not emit a named `partially_represented` edge count/list, and `project_report()` does not itself reject a same-event endpoint edge. Add explicit safeguards and tests before empirical use.
4. **Human decisions and rights:** five rank-1 candidates remain pending human source-scope/local-use decisions. An AI ZScaler worked draft exists, but is not gold and contains a temporal-link row that violates the v0.4.1 endpoint rules.

The sampling-frame question is substantially resolved by Sampling Method v0.3.2 and frame v0.9: keep the full 120-report manifest-defined GNE+CyNE inventory, do not condition on the 112 reports with existing ATT&CK links, and treat the two no-CyNE documents as source-genre exclusion candidates based on content, pending the researcher’s declared scope decision. The frame v0.9 also fixes stale internal handoff references and flags one candidate duplicated between the base review and stress queue.

## 2. Current source-of-truth hierarchy

Different artifacts are at different maturity levels. They must not be treated as if they were all final or synchronized.

| Area | Current strongest artifact | Status / caveat |
|---|---|---|
| Public repository | `main` at `b0024866bdfbe680b296861d81ac50d0e53b9806` (1 Nov 2026) | Public repo snapshot. No changes were pushed during this audit. |
| Research question / annotation protocol | `CTI_Event_Instance_Annotation_Protocol_v0.4.1-draft.md` | Best current local consolidation draft; not approved, frozen, or validated. It does not replace v0.2/v0.3 until researcher approval. |
| Annotation schema proposal | `CTI_Annotation_Schema_v0.4.2-draft/` + `CTI_Annotation_Schema_v0.4.2_Conformance_Audit_v0.1.md` | All eight minimum registers are present, but explicit evidence scope, version/pass identity, evidence-link keying and validator enforcement remain open. Not approved or ready for data entry. |
| Public annotation templates | `research/templates/*` on GitHub | Still aligned to v0.3, not v0.4.1. They are not adequate for a v0.4.1 annotation pass yet. |
| Public validator / projection code | `src/annotation_validation.py`, `src/projection_metrics.py` at current `main` | Useful structural and synthetic prototypes. They do not validate v0.4.1 semantic decisions or real annotations. |
| AnnoCTR screening | `AnnoCTR_Corpus_Screening_v0.1.csv` plus screening report | Screening rerun reproduced. The local v0.2 CSV is byte-identical to v0.1, not a revised screen. |
| Sampling | `AnnoCTR_Fresh_MultiVendor_Sampling_Method_v0.3.2.md` and frame workbook v0.9 | Corrected operational draft: all 120 manifest-defined GNE+CyNE reports remain in inventory; the 112 link-positive count is descriptive, not an eligibility filter. Two no-CyNE reports are genre-exclusion candidates pending human scope decision. Hash order is unchanged; one stress-queue duplicate is now flagged. |
| Five-report method correction | `AnnoCTR_Five_Report_Reaudit_and_Sampling_Correction_v0.1.md` | Correctly supersedes the event-enumerability exclusion gate. Sampling Method v0.3.2 resolves the 120-versus-112 issue and the base/stress overlap; schema migration is still incomplete. |
| Five-report source review | `AnnoCTR_Five_Report_Batch_Review_v0.2.xlsx`, triage workbook v0.1, plus individual source notes | AI-assisted triage only. Researcher decisions remain pending. |
| Prior DFIR cases | Three-case workbook/synthesis family | AI-exposed protocol-development material; none is fresh blind gold. |
| ChronoCTI baseline | `CTI_ChronoCTI_Baseline_Reproduction_Audit_v0.1.zip` | Workbook/code-control-flow audit; not full model reproduction. |

**Version housekeeping correction:** v1.3 overstated the completeness of the v0.7/v0.8 workbook cleanup. Direct inspection of v0.8 still found a dashboard title reading v0.7, four candidate notes pointing to the v0.1 batch-review workbook, a handoff cell pointing to v0.1, and an Intel471 stress row duplicating the current rank-1 base candidate. These residual issues are corrected/flagged in v0.9; v0.8 is retained as a historical snapshot.

## 3. Research question and the exact object of study

The current candidate question is:

> Across a transparently sampled set of CTI reports, how often does a report explicitly support a temporal relation between two distinct, resolved activity occurrences that share one or more ATT&CK technique mappings, and what occurrence identity or temporal information is retained, partially represented, or lost when those occurrences are projected to a representation that permits only distinct technique pairs?

This is a **candidate empirical question**, not a novelty claim or a result.

The two parts must be measured separately:

- **Report-level phenomenon:** does a report support a positive, source-evidenced temporal relation between two distinct resolved atomic activity occurrences, within a comparable scope, whose accepted ATT&CK mapping sets intersect?
- **Projection consequence:** after projecting the supported relation's accepted mapping sets to technique pairs, is it fully omitted, partially represented, or represented without a diagonal mapping? Do different event relations collide onto the same technique pair?

The project must keep these objects distinct:

| Object | Operational meaning | Not equivalent to |
|---|---|---|
| Mention | Exact text span referring to activity | Execution or event identity |
| Event instance | One distinguishable report-local occurrence | Tool, technique, malware family, host, sentence, or mention |
| Repeated series | Repetition asserted, but individual executions are not separable | A count inferred from repeated wording |
| Episode | A bounded phase/period that may contain multiple executions | One atomic execution per day or per phase |
| Scope | Context within which event identities and relations can be compared | “Everything in one report” |
| ATT&CK mapping | Evidence-backed taxonomy label attached to an event leaf | Event identity or execution count |
| Temporal relation | Source-supported relative time between two event instances | Narrative order, causality, dependency, or an Attack Flow edge by default |

The v0.4.1 rule that only `RESOLVED` `event_leaf` units with `atomic_event` granularity enter the primary event graph is sound. Keep series, episodes, report-level aggregates, generic behaviour, and unresolved activity visible in separate records and denominators. Do not inflate atomic counts with containers.

## 4. Repository and implementation status

### 4.1 GitHub state

The latest `main` commit independently checked during this audit is:

`b0024866bdfbe680b296861d81ac50d0e53b9806` — “Qualify unreproduced ChronoCTI cycle counts” (1 November 2026).

The recent AnnoCTR source reviews, v0.4.1 protocol draft, v0.4.2 schema proposal, sampling frame v0.9, and rights/triage work are local working artifacts, not synchronized into the public repo. The public repository still presents the v0.3 annotation protocol/templates and v0.1 projection-metric documentation.

CI run #26 succeeded for the synthetic projection tests and toy example on commit `e65704c7c339f73fa3a75587e3effb7acf209f9f`. The compare from that commit to current `main` showed 11 documentation/research-only commits and no changed source/test/workflow files. It is fair to say the current code is the same code that passed those tests; it is **not** fair to say the CI job ran on the current HEAD. In either case, synthetic tests do not validate human annotations or real-report findings.

No GitHub files were changed or pushed in this audit.

### 4.2 Annotation template and v0.4.1 protocol mismatch — P0

The v0.4.1 protocol requires more structure than the public templates currently allow:

- `event_mentions.csv` has mention offsets/status and an `event_instance_id`, but no formal `scope_id`, `unit_id`, `granularity`, `unit_role`, `count_status`, parent-container ID, or separate activity-unit record.
- `event_mappings.csv` has technique ID/version/evidence but no `mapping_basis` field and no machine-readable distinction between an accepted mapping and an alternative candidate.
- `temporal_relations.csv` has endpoint IDs, relation label and evidence, but no `relation_basis` (`direct_source`, `direct_timestamp`, `derived_transitive`, etc.) or explicit endpoint-scope compatibility record.
- There is no dedicated scope register or activity-unit/container register in the published template set.
- The template README still points to protocol v0.3.

This is not just cosmetic. v0.4.1 says to create activity-unit records before resolving event IDs, retain container-parent relationships, and separate direct from derived/inferred relations. The current templates cannot encode all of that without stuffing important decisions into free-text notes. That would make later validation and analysis fragile.

**Required migration before annotation:** define and version a v0.4.1 schema with, at minimum:

1. a `scopes` table: report, annotator, scope ID/type, parent scope if applicable, description, evidence/locator, confidence and status;
2. an `activity_units` table: unit ID, scope ID, granularity, unit role, instance status, count status/count fields, parent unit, source description/evidence and status;
3. an `event_mentions` table linking each exact mention to an activity-unit/event ID, with offsets and mention-specific metadata;
4. a `event_mappings` table with mapping basis, pinned ATT&CK release, exact technique ID, baseline parent ID, evidence, and an explicit accepted-vs-alternative decision;
5. a `temporal_relations` table with event-leaf endpoints, relation label, relation basis, scope compatibility, evidence span(s), and adjudication state;
6. a `report_registry` that freezes source URL/path, source hash, dataset version, attribution, rights status and text-transformation details.

The final header definitions and identifiers should be frozen before data entry. Do not begin by populating the v0.3 CSVs and trying to retrofit the missing information later.

### 4.3 Validator limitations and multi-annotator handling — P0/P1

`src/annotation_validation.py` correctly describes itself as a structural/offset validator, not a semantic judge. It checks source spans, ID references, status consistency, mapping/relation evidence and some endpoint rules. It cannot determine whether the event identity, mapping, scope or temporal interpretation is actually correct.

Specific items to fix or explicitly constrain:

- The validator filters rows by `report_id` but does not partition by `annotator_id`. If two annotators' rows are placed together in the same CSV, they can be combined or rejected as duplicate IDs. For IAA, use separate per-annotator files or update the validator to filter by both report and annotator and make IDs annotator-scoped.
- The validator does not check the v0.4.1 fields listed above: granularity, unit role, count status, mapping basis, relation basis, scope compatibility, accepted/alternative mapping status, or container hierarchy.
- Its return count named `mapped_relation_rows` is currently the number of all temporal relation rows, including assessment/non-positive labels. Rename it to `temporal_relation_rows`, and separately count positive graph edges and pair assessments.
- The validator should verify that every positive event edge connects distinct resolved atomic event leaves in a comparable scope; current v0.3 checks some of the endpoint identity requirements, but not the v0.4.1 granularity/scope rules.
- Offset checking is only valid for the exact frozen text and transformation recorded in the registry. Preserve the original and the exact normalized annotation text; never silently normalize whitespace after offsets are created.

A second annotator is a human. An LLM or prior automated reconstruction is not a second rater. If no independent human is available, report that agreement was not measured; a later blind re-annotation by the same researcher is intra-annotator consistency, not IAA.

### 4.4 Projection prototype: strengths and corrections — P1

The prototype already has useful design features:

- one event remains one event even with multiple mapping IDs;
- relation-aware Cartesian-product projection `A(u) × A(v)`;
- edge-to-pair provenance;
- separate diagonal, shared-technique, unmapped and self-only counts;
- symmetric relation canonicalization;
- strict BEFORE/AFTER cycle analysis separated from overlap/concurrency;
- source-edge provenance for single-edge mapping-fanout cycles versus multi-edge projection cycles.

Before using it on human annotations, fix or document these points:

1. **Fully omitted vs unmapped:** `event_edges_without_distinct_technique_pair` currently includes unmapped edges as well as mapped self-only edges. The actual fully omitted *mapped* edge IDs are the self-only edges. Add explicitly named counts for mapped-full-omission and unmapped-endpoint edges, and do not describe the combined set as diagonal loss.
2. **Partial representation:** the number of partially represented mapped edges is derivable from shared-technique-endpoint edges minus self-only edges, but should be output directly with a clearly named numerator and denominator.
3. **Collision scope:** current collision counts use the complete projection, including diagonal pairs. Also report collision/conflation in the target distinct-technique-pair graph separately so diagonal-only collisions are not described as retained pair-graph collisions.
4. **Accepted mappings vs alternatives:** the Cartesian product is appropriate only over mappings accepted for the primary analysis. If two mappings are competing interpretations rather than simultaneous valid labels, do not treat both as members of `A(v)` in the primary result. Keep alternatives as candidates/sensitivity records.
5. **Distinct event endpoints:** the annotation validator checks that temporal-relation endpoints differ, but `project_report()` itself should also reject `source_event == target_event`. A self-loop is not a relation between two distinct occurrences and must not enter the metric function.
6. Add tests for the preceding cases and for scope/granularity filtering at the data-preparation boundary. Keep the pure projection function small; semantic scope checks can be done by a validated adapter before calling it.

Do not combine edge counts, event-edge-to-pair mapping combinations, and unique technique-pair counts into one “information-loss percentage”. They are different units.

## 5. AnnoCTR corpus and sampling audit

### 5.1 Reproduced corpus inventory

The official AnnoCTR manifest has 400 report IDs:

| Split | Reports |
|---|---:|
| train | 70 |
| dev | 16 |
| test | 34 |
| ext | 280 |
| **Total** | **400** |

The current candidate frame is the 120 train/dev/test reports with the cyber-specific annotation layer (GNE+CyNE), not all 400 reports. Donor counts are:

| Donor | Reports in 120-report frame |
|---|---:|
| Intel471 | 30 |
| Lab52 / S2 Grupo | 23 |
| Proofpoint | 28 |
| QuoIntelligence | 12 |
| ZScaler | 27 |
| **Total** | **120** |

Screening results:

- all 400 manifest reports have the expected text, full-linking, MITRE-only-linking and TimeML files;
- 118/120 have cyber-specific rows in the full linking exports;
- 112/120 have at least one valid canonical ATT&CK technique link in the MITRE-only export;
- 8/120 have no valid ATT&CK technique link in that export;
- 2 manifest reports have no observed cyber-specific linking records in the inspected linking exports: `proofpoint_2021-05-24_compromised-cloud-accounts-cost-firms` and `quoteintelligence_2020-07-09_what-is-tiber-eu-and`;
- 3,324 TIMEX3 tags were found across the corpus, with zero EVENT, MAKEINSTANCE, TLINK, or SIGNAL tags;
- 0 exact normalized-text duplicate groups and 0 high-overlap pairs at the checked five-word-shingle Jaccard threshold. This does not rule out paraphrase, syndicated copies with edits, or shared source material.

The corpus TimeML files therefore provide time-expression annotations, not event-instance or event-to-event temporal relation gold. A TIMEX3 tag does not tell us which event happened when or how two events relate.

The official corpus ZIP SHA-256 recorded in the local screen is `118549e9ce885559cd0c07a8de42b321892754cc2e4f07fea0230eaefe4cea35`.

The v0.1 and v0.2 screening CSVs have identical SHA-256 values (`fc6552832fbb48f6d21d49012943e37b00dab783d1556a1a09f1128fbb7dde8f`) and identical file sizes. **v0.2 is not a new or corrected screening snapshot.** Treat v0.1 as the screening result and note the duplicate export; do not imply the v0.2 file changed the counts.

### 5.2 Sampling frame decision — resolved in local method v0.3.2

The correct starting inventory is the **120 manifest-defined GNE+CyNE reports** in train/dev/test. The 112 reports with at least one valid existing ATT&CK link are an inventory statistic, not the base sampling frame. Source-level ATT&CK mappings for this study must be independently supported from the frozen source text; they must not inherit AnnoCTR link presence as an eligibility condition.

The screen found 8/120 reports with no valid canonical ATT&CK technique link in the MITRE-only export. Six of these still have cyber-specific annotation records and remain eligible for source-first manual annotation if they pass source-scope, provenance and local-use gates. A missing AnnoCTR technique link is not equivalent to a human `UNMAPPED` decision.

Two manifest entries have no observed CyNE records and no valid ATT&CK links: `proofpoint_2021-05-24_compromised-cloud-accounts-cost-firms` and `quoteintelligence_2020-07-09_what-is-tiber-eu-and`. Full-text review identifies them as a sponsored survey-summary article about cloud account compromise costs and a general TIBER-EU framework explainer. They remain in the official 120-row inventory, but are source-genre exclusion candidates under the declared CTI-report scope. The researcher must record any content-based exclusion explicitly. The absence of linking records is corroborating inventory evidence, not the exclusion rationale.

**Resolved method:** use all 120 manifest records as the documented frame; record the two genre candidates separately; do not prefilter to 112; and record the six other no-link reports as existing-annotation missingness. The five base reports remain one per donor and are selected by fixed hash priority only after each report passes source-scope and local research-use gates. This resolves the old 120-versus-112 uncertainty without claiming that all 120 are eligible CTI reports.

### 5.3 Sampling procedure and limits

The fixed seed is `CTI-EVIDENCE-LAB-ANNOCTR-PILOT-2026-11-03-v1`. Frame v0.9 contains the same 120 report IDs, donor counts, priority hashes, within-donor ranks, and source-text hashes. An independent recheck found 0 priority-hash mismatches, 0 rank mismatches, and 0 source-text-hash mismatches. v0.9 corrects residual stale title/handoff references found in v0.8 and flags the Intel471 Groove row that appeared in both the base rank-1 review and the stress queue. Candidate ordering and report rows are unchanged. The first hash-ranked candidates are:

1. Intel471 — `intel471_2021-09-09_groove-gang-ransomware-babuk-revil`
2. Lab52 — `lab52_2022-01-12_tokyox-dll-side-loading-an`
3. Proofpoint — `proofpoint_2021-07-01_malware-masquerades-privacy-tool`
4. QuoIntelligence — `quoteintelligence_2020-04-20_winnti-group-insights-from-the`
5. ZScaler — `zscaler_2021-07-14_targeted-attack-government-organizations-delivers`

The deterministic hash priority is a reproducible, random-like selection order within each vendor stratum. The proposed five-report, one-per-donor pilot is a **feasibility/protocol-debugging sample**, not a representative sample for prevalence. Equal allocation across donors is not proportional to their sizes. It must not be used to claim overall or vendor-level population prevalence.

The correct rule is the one in the sampling method and five-report re-audit: **a report does not need two event leaves, a repeated technique, or a positive temporal relation to remain in the base feasibility sample.** The adequacy audit's event-enumerability gate is superseded. Event-pair opportunity and temporal relations are outcomes recorded after sample selection, not pre-selection requirements.

Advance to the next hash-ranked report only if a pre-specified identity, source-completeness, provenance/rights or practical annotation eligibility criterion fails—not because the report lacks the result being investigated. If a donor has no eligible candidate, document that and revise the design transparently.

The five reports have not been formally selected or frozen: v0.9 still shows zero human eligibility decisions and zero selected reports. The AI triage workbook shows 5 likely annotatable recommendations, but the researcher gate remains pending for all five.

## 6. Five candidate source reviews — reconciled status

These reviews are **AI-assisted source triage**, not annotations or final eligibility decisions. All five remain in the base candidate queue pending the researcher's eligibility decisions, with text-reuse status AMBER.

| Candidate | What the report can test | Main safeguard | Current position |
|---|---|---|---|
| Intel471 — Groove/Babuk/RaaS ecosystem | Mixed actor/forum/victim/historical contexts and report-level TTP aggregation | Do not merge unrelated victims, forums, historical Babuk cases and Groove/BlackMatter contexts into one incident timeline. 63 linking rows and repeated T1486 mentions are not execution counts. | Likely annotatable; high scope/provenance risk; human decision pending. |
| Lab52 — TokyoX Part 2 | Capability-vs-execution, sample-vs-event, unknown C2 evidence | The six command handlers are capabilities, not six victim-side executions. Five-minute sleep is code logic, not observed recurring beacons. Part 1 is a related but distinct article. | Likely annotatable for protocol testing; may produce few/no primary event leaves; human decision pending. |
| Proofpoint — Privacy Tools / Smoke Loader | Strongest candidate for explicit stage order | The article describes Smoke Loader downloaded first and its infection subsequently downloading follow-on malware. RedLine and Raccoon are alternative payload families; do not order them or assume both occur in one host infection. The two stages are not yet human-locked event leaves. | Highest priority for careful human event/mapping adjudication; do not pre-label positive. |
| QuoIntelligence — Winnti historical analysis | Multiple target/sample scopes and date-type uncertainty | Keep German chemical-company and South Korean gaming-company contexts separate. Distinguish sample detection, victim awareness, compilation metadata and attack time. Preserve the year ambiguity in “Friday, 13 January” and “21 February”; do not repair it. | Likely annotatable; high scope/date ambiguity; human decision pending. |
| ZScaler — Netwire RAT | One identified email-send candidate and a broader repeated-delivery series | One email is dated 30 June 2021, 10:44 AM PKT. Three document hashes are artifacts, not three emails or executions. The “campaign began July” statement is a separate source claim, not a chronology to repair. | Likely annotatable; one AI-proposed atomic event candidate, series/aggregate units; human decision pending. |

Additional cautions:

- The local `AnnoCTR_ZScaler_Worked_Annotation_Draft_v0.1.xlsx` is an AI-assisted, unreviewed worked source pass, not a human annotation, selected report, gold record, or agreement result. It contains a `Temporal Links` row from `AU-ZS-SERIES` (a repeated-series container) to `AU-ZS-EMAIL-01` (an atomic email event), labelled `UNRESOLVED_SCOPE_TIME_CONFLICT`. A container cannot be a primary event-edge endpoint under v0.4.1. Move the campaign-start/email-date discrepancy to typed `time_evidence` and a decision/scope note; do not count it as a temporal edge.
- Intel471's 63, Lab52's 15, Proofpoint's 8, QuoIntelligence's 41 and ZScaler's 69 AnnoCTR technique-link records are mention/linking-layer statistics, not event-level mappings.
- QuoIntelligence's publisher-explicit technique table and ZScaler's publisher-explicit TTP table must stay separate from AnnoCTR links and any new analyst mapping.
- Proofpoint's AnnoCTR T1105 mention applies to the follow-on download context; it does not automatically assign T1105 to both the initial Smoke Loader delivery and the follow-on download. If both event leaves are given the same technique in the primary analysis, each mapping needs its own source-based evidence and human decision.
- The earlier assistant replies that called Lab52, QuoIntelligence or ZScaler ineligible for the primary sample solely because no event pair had been found were too strong. That confused annotation outcome with sample eligibility. Those exclusion conclusions are superseded; their event-level limitations remain valid observations.

## 7. Rights and provenance

The official AnnoCTR repository states that the `AnnoCTR` corpus folder is CC BY-SA 4.0. The dataset-level licence is the documented basis for local analysis, attribution and any licensed adaptation, but the legal code only grants rights the licensor controls. The CTI Evidence Lab MIT code licence does not relicense report text.

The current publisher-specific rights scan remains **AMBER** for all five reports:

- **Lab52/S2 Grupo:** highest-priority clarification. Its legal notice says reproduction of site content requires prior written authorisation; this appears in tension with the corpus-level CC BY-SA statement.
- **Intel471:** clarify donor/publisher scope, particularly the article's McAfee Enterprise ATR cross-publication and site terms.
- **Proofpoint:** the terms page located was for Proof-of-Concept/Desktop material, not clearly the public threat-intelligence blog; do not misapply it.
- **QuoIntelligence:** no separate article-specific open licence was verified in the scan.
- **ZScaler:** the legal page located concerns product/subscription terms, not necessarily the public security blog article.

Local annotation and public redistribution are different gates. Keep raw reports and long verbatim spans local. Public outputs should prefer report ID, title, publisher, canonical URL, date, source hash, concise paraphrase and line/paragraph locators until permissions and applicable licence scope are clearer. This is workflow guidance, not a legal determination.

## 8. Earlier DFIR development cases

The three cases `r-dfir-1`, `r-dfir-2`, and `r-dfir-8` remain useful for protocol/code debugging, but they are AI-exposed and purposive. **Human-locked cases: 0/3.** Do not call them a fresh blind set, gold standard, independent annotation, or prevalence sample.

- **r-dfir-1:** two RDP attempts and an intermediate account-removal event. A direct source-based first-attempt-before-second-attempt relation may coexist with an intermediate relation. Current AI recommendation is `direct_source`; researcher decision is still pending. Earlier direct-vs-derived wording differed across artifacts; preserve this as unresolved until the researcher accepts a decision.
- **r-dfir-2:** four LSASS-related periods are best treated as activity episodes in the current analysis, not four confirmed atomic executions. T1003/T1003.001 remains an analyst mapping candidate, not a publisher-explicit label for every period.
- **r-dfir-8:** ChronoCTI's raw `NEXT` technique graph has an SCC involving T1059 and T1105. Current strict source reconstruction does not explain the cycle. An SMB movement mapping candidate such as T1570 (with alternatives still requiring review) must not be automatically replaced by T1105. The cause of the benchmark cycle is unresolved.

The prior three-case synthesis's 14 strict `BEFORE` links / 4 same-technique omissions / 3 unmapped / 7 retained counts are focal, purposive and mixed-granularity bookkeeping. They are not a pooled rate. Recompute only after activity units have been reclassified and event leaves separated from episode/series/aggregate containers. They also represent strict `BEFORE` bookkeeping, not all positive temporal labels.

The six-case blind kit is not blind for the researcher if cases were previously exposed. It could only support an independent human annotation pass for an annotator who has not seen prior keys or analyses and is given the same source and frozen protocol without revealing the former annotations.

## 9. ChronoCTI baseline — exact level of reproduction

The supplied ChronoCTI archive was inspected at workbook and source-code level. The following points were reproduced:

- 120 selected technique IDs;
- paper formula `(120² - 120) / 2 = 7,140` unordered dyads of distinct techniques;
- released graph-generation loop uses `idx1 != idx2` and both ordered orientations, giving 14,280 directional candidates;
- both conventions exclude diagonal `(T,T)` pairs;
- workbook has 2,104 relation rows across 94 reports (73 train / 21 eval): `NEXT` 1,338, `OVERLAP` 564, `CONCURRENT` 92, blank 110;
- 11 raw report-specific ordered pair keys have multiple distinct nonblank labels; reverse expansion for symmetric `OVERLAP`/`CONCURRENT` produces 22 orientation-specific conflict keys;
- with the original workbook rows preserved first and reverse symmetric rows appended afterward, the loader's last-row-wins loop yields 14 final `OVERLAP` and 8 final `NEXT` outcomes among those 22 conflict keys;
- 110 blank rows include 108 with at least one missing endpoint and two with both selected endpoints populated (`r-1040: T1204→T1218`, eval; `r-dfir-25: T1047→T1570`, train).

The public code loops through matching workbook rows and overwrites the class flags, so multiple distinct nonblank labels for the same key are not preserved as a multi-label target. The loader sets `NULL=1` only when no workbook row matches; a complete-endpoint blank row that does match could leave all class flags zero. The exact number of resulting model rows affected is unknown because the intermediate feature JSON `temporal_features_v2/all_reports_threshold_95_v3.json` is missing from the supplied/public release. The feature JSON join cannot be reproduced, so no exact impact on the final training matrix or model metrics can be claimed.

**Do not call this a full ChronoCTI reproduction.** It is a workbook inventory and source-code control-flow audit, not end-to-end feature reconstruction, model re-training, or evaluation re-run.

Semantic rules:

- Preserve raw workbook `NEXT` as `NEXT`.
- Any `NEXT`→`BEFORE-like` normalization is a separate baseline hypothesis with rationale/status.
- Refer to benchmark cycles as **ChronoCTI NEXT-graph cycles**.
- Use **strict source-evidenced BEFORE/AFTER cycle** only for a human-annotated event graph with relation-specific evidence.
- Do not map a ChronoCTI technique edge one-to-one to a source event pair: the released benchmark lacks event IDs and relation-specific source spans.
- The 7,140 vs 14,280 distinction is a paper-count/code-orientation discrepancy, not a proven model bug.

## 10. Related work and defensible positioning

The project must not claim that cybersecurity event extraction, CTI/ATT&CK mapping, event graphs, evidence-grounded extraction, or attack-sequence reasoning is novel by itself.

Important comparisons that need to be in the next related-work matrix revision:

| Work | What it establishes | Difference relevant to this project |
|---|---|---|
| **AnnoCTR (LREC-COLING 2024)** | 400 English CTI reports; document-level entity, time-expression and cyber-concept/ATT&CK annotations. | The inspected files provide TIMEX3, but not event-instance coreference or event-to-event temporal relation gold. |
| **SMAH-CTI (Findings EMNLP 2026)** | 100 public CTI reports and sentence-level relevance, CTI NER, ATT&CK mapping and grounded procedure-description tasks. Dataset is CC BY-NC 4.0; software/code is MIT. | Important modern CTI benchmark; its stated tasks and schema are not a document-level event-coreference / event-to-event temporal graph annotation resource. Do not assume the dataset licence is MIT. |
| **Wu (2026), NTU master’s thesis, *LLM-Based Construction of Attack Life Cycles from CTI Reports*** | Incident-scoped malicious-activity identification; unique sentence IDs inherited as event IDs; zero/one/multiple ATT&CK mappings with evidence-grounded validation; inferred event ordering and causal dependencies; event merging for duplicates and granularity differences; multi-report life-cycle synthesis. | Closest process-level neighbour found. Its ordering is inferred from attacker intent, functional prerequisites and causal/ATT&CK semantics rather than requiring direct source-evidenced temporal links as primary gold; its 11-report evaluation is structural because correctness ground truth is unavailable. It must be compared directly.
| **83-report ATT&CK classification study (arXiv:2606.18166, 2026 preprint)** | 2,076 human-annotated sentences from 83 DFIR reports, 114 ATT&CK techniques and reported κ=0.68. | Sentence-level multi-label technique classification, not event identity or event-to-event temporal relation annotation. It weakens generic claims about lack of human-labelled ATT&CK classification on complex reports. |
| **APTIE (Scientific Data 2026)** | 116 Chinese APT reports, 139 event instances, entity and relation annotations. | Each sentence is an independent unit; entities, relations and events are identified within sentence boundaries; cross-sentence aggregation and document-level reasoning are explicitly out of scope. Its relation labels are semantic entity relations, not event-to-event temporal edges. |
| **EventRelBench (Findings EMNLP 2025)** | General-domain event-relation QA over coreference, temporal, causal and supersub relations at sentence and document level. | Event-relation extraction is established general NLP prior art. It is not CTI/ATT&CK-specific. |
| **AttackSeqBench (2025 preprint / 2026 version)** | Uses CTI reports to construct tactic/technique/procedure sequences and evaluates LLM sequence reasoning; reports 408 filtered CTI reports in its sequence construction. | Very close adjacent CTI sequence-reasoning work. It is not the same as a human gold annotation of report-local occurrence identity and relation-specific event-pair evidence; compare its sequence construction and evidence provenance carefully. |
| **Hou et al. (arXiv:2607.19742, 2026)** | 20 CTI reports and 334 human-validated attack steps; models each step with preconditions, behavior and postconditions for dependency/reachability reasoning. | Close attack-chain work. Its main semantics are state/dependency/reachability, not a benchmark of pairwise source-evidenced temporal relations between resolved occurrences. |
| **CSEM-CTI (iScience 2026)** | Evidence mining for sentence-level ATT&CK/tactic/technique classification and faithfulness analysis. | Evidence-grounded CTI classification is already prior art. Our evidence must support the relation between two occurrence IDs, not only an ATT&CK label. |
| **CASIE (AAAI 2020), CySecED, MAVEN-ERE, TIMELINE, MATRES** | CTI event extraction and general-domain event/coreference/temporal relation annotation are established. | Include as annotation and evaluation precedents; do not position event graphs or temporal relation extraction generically as new. |

The 2026 cybersecurity event-extraction survey reports no public dataset for event-relation extraction under the task definition used in its review. Do not generalize this to mean CTI has no event, entity-relation or life-cycle resources. APTIE includes 139 event instances and 1,506 semantic entity relations but defines tasks at sentence level and excludes cross-sentence aggregation/document-level reasoning. SMAH-CTI includes sentence-level relevance, NER, multi-label ATT&CK mapping and grounded procedure descriptions, but its public schema has no occurrence/coreference IDs or event-to-event temporal relation layer. CASIE supports event detection and argument extraction (including time arguments and realis), but is not a document-level temporal event-pair gold corpus. Wu (2026) is a close system-level neighbour that constructs incident-scoped event life cycles. The survey motivates a precise missing annotation/evaluation design; it does not establish novelty by itself. This supports a carefully qualified motivation, not proof that no relevant dataset or adjacent work exists. APTIE, SMAH-CTI, AttackSeqBench, the 83-report ATT&CK benchmark, and the reachable-attack-chain work must be compared by exact annotation unit, relation semantics, cross-sentence scope, identity model, and evidence requirements.

**Narrowed candidate niche (not a novelty claim):** a human-annotated report-local representation with explicit activity-unit granularity and scope; mention-to-occurrence identity and mapping provenance; direct source/timestamp-supported relations between distinct resolved atomic occurrences as primary temporal gold; and a measured analysis of edge-level full omission, partial retention, non-diagonal retention and pair conflation under the **specific distinct-technique-pair constraint** used by the ChronoCTI-style baseline. The distinction from Wu (2026) is not “we build event graphs” or “we map CTI actions to ATT&CK”; it is the evidence standard and explicit projection-loss analysis. This is plausible but unproven.

## 11. Metrics: correct the research question before computing anything

Protocol v0.4.1 currently defines a “Repeated-occurrence report rate” as reports with at least two resolved atomic event leaves sharing a technique divided by eligible sampled reports. That is a **pair-opportunity rate**, not the primary RQ outcome, because it does not require a temporal relation.

Retain it under a corrected name:

**Same-technique pair-opportunity report rate**

`reports with at least one pair of distinct, scope-compatible resolved atomic event leaves whose accepted baseline mapping sets intersect / eligible sampled reports`

Add the actual primary report-level measure:

**Within-technique temporal-relation report rate**

`reports with at least one directly source/timestamp-supported positive temporal relation between distinct, scope-compatible resolved atomic event leaves whose accepted baseline mapping sets intersect / eligible sampled reports`

For each report, separately record:

1. eligible report included in the denominator;
2. at least one resolved atomic event leaf;
3. at least one pair of distinct, scope-compatible event leaves;
4. at least one same-technique mapping pair opportunity;
5. at least one directly supported positive temporal relation;
6. at least one positive temporal relation whose endpoint mapping sets intersect;
7. number of positive temporal event edges fully omitted, partially represented, or with no diagonal mapping;
8. unmapped endpoint edges, `VAGUE_OR_AMBIGUOUS`, and `NOT_ASSESSABLE` separately.

The primary temporal relation incidence can include all positive temporal labels only if the protocol explicitly defines that estimand. Report strict `BEFORE`/`AFTER` separately from `OVERLAP`, `SIMULTANEOUS` and `CONCURRENT_UNSPECIFIED`; do not blend them into the strict-order cycle metric. If the actual scientific intent is only precedence, narrow the RQ and label set rather than using a broader phrase.

No unannotated event pair is a negative example by default. `NO_TEMPORAL_CLAIM` is allowed only for pairs in a declared, pre-specified candidate-pair assessment frame. `NOT_ASSESSABLE` is not equivalent to no relation, and a missing AnnoCTR link is not automatically an unmapped human result.

## 12. Stop/go list and next execution order

### P0 — resolve before any formal annotation

1. **Confirm the report-scope rule and the two genre candidates.** Preserve the 120-row official GNE+CyNE inventory. Record the two no-CyNE documents as content-based out-of-scope candidates only if the researcher accepts the declared CTI-report scope; do not exclude them merely because they lack CyNE/ATT&CK links. Keep the six other no-link reports available for source-first annotation.
2. **Approve the exact baseline mapping level in the research question.** The v0.4.1 draft defines `A_120(v)` as the evidence-supported parent technique IDs in ChronoCTI's pinned selected-120 vocabulary, with exact/sub-technique mapping retained separately. Make the RQ and primary results explicitly use `A_120`; keep exact-ID/sub-technique overlap as a separate sensitivity analysis. Pin the exact vocabulary file, ATT&CK release basis, and SHA-256 in the annotation registry.
3. **Approve the primary temporal-label scope already specified in v0.4.1.** As drafted, the primary within-technique report outcome includes direct-source/direct-timestamp `BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` relations between distinct resolved atomic event leaves in comparable scopes. Strict cycle analysis uses only normalized `BEFORE`/`AFTER`. Approve this distinction or revise the RQ and protocol before annotation; do not mix the broad relation-incidence numerator with the strict-order cycle subset.
4. **Approve the report-level denominator and missingness policy.** The v0.4.1 draft separates same-technique pair opportunity from the primary within-technique temporal-relation outcome, and separates `NOT_ASSESSABLE` report status from a zero-edge but assessable report. Confirm the assessable-report denominator, eligibility denominator for assessability coverage, and treatment of reports with zero event leaves. Do not call a five-report feasibility result prevalence.
5. **Migrate the annotation data model before data entry.** Implement the v0.4.1 registers and required fields: report registry, scopes, activity units, exact mentions, typed time evidence, exact and baseline-parent mappings with accepted/alternative status and mapping basis, positive temporal relations with relation basis and scope compatibility, plus optional candidate-pair assessments. Freeze headers, controlled vocabularies, source normalization, offsets, IDs, and report/annotator partitioning before annotating.
6. **Make the five researcher decisions explicitly and separately.** For each rank-1 report, record `source_scope_eligibility`, `local_research_use_status`, and `public_reuse_status`. The first two govern entry to local annotation; public reuse is separate. The event yield, same-technique opportunity, and positive relation count must not influence selection or replacement.
7. **Approve the narrow contribution claim only after the structured prior-work comparison.** Wu (2026), AttackSeqBench, the reachable-attack-chain framework, APTIE, the 150-report STIX dataset, SMAH-CTI, EventRelBench, ChronoCTI and adjacent systems already cover substantial parts of CTI event extraction, ATT&CK mapping, attack sequencing, event relationships, or evidence-supported structured CTI. Do not claim novelty for those broad capabilities. The candidate niche is the human evidence standard plus report-level measurement of occurrence-level information under a named distinct-technique-pair projection; this remains unproven.

### P1 — resolve before real-data metric runs

8. Add projection safeguards/tests: reject same-event endpoints in `project_report()`; explicitly emit fully-omitted-mapped, partially-represented, no-diagonal and unmapped-endpoint counts/IDs; make the mapped-edge denominator explicit; retain distinct-pair provenance and accepted mappings only.
9. Extend the validator for v0.4.1 semantics: event leaf/container role, granularity, count status, parent hierarchy, scope compatibility, mapping basis/acceptance, time-evidence types, relation directness, report assessability, and annotator isolation. Rename `mapped_relation_rows` to a non-misleading temporal-row count and separately report positive edges and pair assessments.
10. Decide and document a human double-annotation/adjudication path. If no second human is available, state that IAA was not measured; AI review is not a second annotator.
11. Complete a row-by-row prior-work comparison using annotation unit, event identity/coreference, activity granularity, scope, temporal semantics, evidence basis, mapping multiplicity, relation endpoints, human gold/IAA, and projection analysis. Prior-work overlap is substantial enough that title/abstract-only comparison is inadequate.
12. Confirm rights for intended public outputs, beginning with Lab52/S2 Grupo and Intel471/McAfee; local-use status and public redistribution status remain separate.
13. Keep ChronoCTI raw labels and normalized hypotheses separate; seek the missing intermediate feature JSON only if full model reproduction remains necessary and access/licence can be established.

### P2 — housekeeping after the substantive decisions

14. Earlier frame cleanup attempted to correct dashboard/handoff metadata in v0.7 and clarify researcher gates in v0.8, but residual stale references remained in v0.8. Frame v0.9 is the first version in this audit that corrects the remaining title/handoff references and flags the base/stress overlap. Preserve v0.7/v0.8 as historical snapshots.
15. Mark the sample-adequacy document's event-enumerability gate as superseded in the audit trail; do not delete it.
16. The v0.1, v0.2 and 3-November recheck screening CSVs are byte-identical (400 rows; SHA-256 `fc6552832fbb48f6d21d49012943e37b00dab783d1556a1a09f1128fbb7dde8f`). Keep one canonical copy in future handoffs; retain the others only as duplicate audit snapshots.
17. Synchronize the approved protocol, schema, validator, docs and README to GitHub in one reviewed commit when ready. Do not push a draft as if approved.

### After the gates

- Freeze source text copies and hashes.
- Complete the source read and scopes before event IDs.
- Annotate mentions and units, then mappings, then positive relations.
- Validate offsets and structure; have a second human independently annotate an overlapping subset if available.
- Lock the annotation and hash the files before revealing any baseline labels or cycle status.
- Only then build event graphs and technique projections.
- Treat the five-report pilot as feasibility evidence only. A larger prevalence study needs a separately justified probability-sampling design, adequate sample size and any required stratification weights.

## 13. What is complete and what is not

### Completed / verified groundwork

- Official AnnoCTR archive downloaded, integrity-checked and extracted locally.
- 400-report manifest and 120-report cyber-specific frame screened.
- ATT&CK link availability and TimeML limitations inventoried.
- Deterministic hash-priority ordering produced for all 120 reports and independently reproduced.
- Five rank-1 candidates source-reviewed at AI-triage level.
- Publisher/source provenance and rights cautions inventoried.
- ChronoCTI workbook and selected source-code control flow audited.
- Projection and evidence-offset validation prototypes have synthetic tests.

### Not completed

- No researcher source-scope/local-use eligibility decision locked for the five candidates (0/5).
- No final five-report base sample selected/frozen (0/5).
- No v0.4.1-compatible final annotation schema/validator release.
- No human-locked event mentions, event units, mappings or temporal relations for the AnnoCTR batch.
- No independent human agreement result.
- No human source-evidenced event graph or real-report projection metric.
- No prevalence estimate or generalizable rate.
- No full ChronoCTI feature-table/model reproduction.
- No validated novelty claim or publication-ready result.

**Bottom line:** the project is not broken, but its novelty must be narrowed after Wu (2026), its annotation schema must be made executable, and sampling must stay independent of pre-existing AnnoCTR technique labels and event yield. The five rank-1 candidates remain pending human source-scope/local-use decisions; no report should be replaced because it yields no events or temporal edges. Annotate from frozen source text, preserve unknowns, then calculate projection metrics only after human lock.

---

## 14. v1.2 and v1.3 audit findings added on 3 November 2026

### 14.1 Close prior work: Wu (2026)

The thesis *LLM-Based Construction of Attack Life Cycles from CTI Reports* (He-Chien Wu, National Taiwan University, February 2026; DOI 10.6342/NTU202600249) is the closest work found in this audit. Its pipeline segments CTI report narrative into sentences, gives each sentence a unique identifier, filters for concrete malicious activities attributable to a focal incident, emits event records with IDs/summaries/justifications, maps each event to zero/one/multiple ATT&CK techniques with evidence-grounded validation, and constructs a life cycle by inferring ordering and prerequisite/enablement causal dependencies. It also merges semantically duplicate or overly coarse events with justifications. These overlap directly with parts of our proposed data and workflow.

The methodological contrast is that Wu’s event ordering explicitly does **not** rely solely on source temporal markers: it uses attacker intent, functional prerequisites, and causal/ATT&CK semantics to infer order. The thesis’s evaluation across 11 reports is structural and explicitly says correctness ground truth is unavailable. Its life-cycle output is therefore not equivalent to a human gold set of direct report-evidenced event-to-event temporal relations. We cannot claim novelty for incident-scoped CTI activity extraction, event IDs, multi-mapping, or inferred attack-life-cycle construction. Our remaining candidate distinction is an explicit human evidence standard plus a measured projection analysis against a defined technique-pair representation.

### 14.2 Other annotation datasets: exact distinctions

- **SMAH-CTI (Findings EMNLP 2026):** 100 CTI reports and 12,304 sentence-level instances; relevance, CTI NER, multi-label ATT&CK tactic/technique/sub-technique mapping, and grounded procedure descriptions. The public schema has sentence/document identifiers, context-before, techniques, procedure and entity spans, but no occurrence/coreference IDs or event-to-event temporal relation records. Dataset licence is CC BY-NC 4.0; code is MIT.
- **APTIE (Scientific Data 2026):** 116 Chinese APT reports, 2,574 entities, 1,506 relations, and 139 event instances across 808 sentences. Tasks are sentence-bounded; cross-sentence aggregation/document-level reasoning is outside scope. Do not call its entity-relation layer temporal event-pair gold.
- **CASIE (AAAI 2020):** cybersecurity event detection and argument extraction over 1,000 news articles, including time arguments and event realis; it does not supply the event-instance temporal-relation graph required here.
- **Han et al. (Scientific Reports 2025):** event extraction includes Actual/Other/Generic status and time arguments; its event-relation task links event types to arguments, not two event instances in temporal order.

### 14.2A Additional close prior work checked during this audit

- **AttackSeqBench (Ma et al., 2025 arXiv version; related 2026 ICLR-under-review manuscript):** defines an attack sequence as ordered ATT&CK tactics with associated techniques/sub-techniques, procedures and a CTI outline. It constructs sequences from extracted TTPs across 408 reports and builds tactic, technique and procedure QA tasks; some negative procedure questions are made by negating temporal prepositions. This is strong prior work on CTI attack-sequence understanding and sequence QA, so do not claim generic CTI attack-sequence reasoning as novel. It is not the same as a human-annotated report-local event-instance graph with every temporal edge linked to relation-specific source evidence and a measured `A_120` projection-loss analysis. A related 2026 manuscript with the same benchmark name was marked under review in the retrieved OpenReview PDF. Its relationship to the arXiv version should be verified rather than counted as a separate independent study; do not cite it as an accepted ICLR paper unless publication status is later verified.
- **Reachable attack-chain framework (Hou et al., arXiv July 2026):** extracts ordered attack-behavior skeletons, constrains step granularity with a 16-class behavior vocabulary, adds preconditions/postconditions, normalizes predicates, repairs dependencies, and runs Datalog reachability. The reported evaluation uses 20 CTI reports and 334 human-validated attack steps. This is a very close system-level neighbour for report-level attack-step identity, granularity and sequence/dependency representation. It does not, on the evidence reviewed here, establish the same target as a human gold set of direct source/timestamp-supported event-to-event temporal relations followed by a controlled distinct-technique-pair projection-loss measurement. Do not frame the present project as the first to construct event/activity sequences from CTI.
- **APTIE (Sun et al., Scientific Data, 25 May 2026):** 116 Chinese CTI reports, 808 unique sentences, 2,574 entities, 1,506 semantic entity relations, and 139 event-triggering instances. Its units are sentence-level; the authors explicitly state that cross-sentence aggregation and document-level reasoning are outside the dataset scope. Its relation task is semantic relations among STIX objects (e.g., uses/targets/originates-from), not a report-local event-to-event temporal-relation graph. It still precludes a generic claim that CTI event extraction or CTI entity-relation annotation is absent.
- **150-report STIX 2.1 CTI graph dataset (Das et al., arXiv July 2026 preprint):** reports 4,777 entities, 5,817 STIX semantic relationships and 1,273 attack-pattern objects mapped to 269 ATT&CK IDs; 25 reports were independently assessed and adjudicated. The manuscript explicitly says the dataset does not model temporal attack sequences and lists temporal relations as future work. It is an important adjacent source-grounded ATT&CK/structured-graph dataset, not direct temporal-event gold. It should be cited as a preprint, not represented as a peer-reviewed released benchmark.
- **SMAH-CTI (Jaffal et al., Findings EMNLP 2026):** sentence-level relevance, CTI NER, multi-label ATT&CK tactic/technique/sub-technique mapping and grounded procedures over 100 reports. Its schema contains sentence IDs, context-before, techniques, procedures and entity spans, but no event-instance/coreference ID or event-pair temporal relation records.
- **EventRelBench (Gong et al., Findings EMNLP 2025):** 35K sentence- and document-level event-relation questions covering coreference, temporal, causal and supersub relations. It is general-domain ERE, not an ATT&CK-grounded CTI occurrence-projection study. It means we cannot claim broad document-level event-relation reasoning or temporal relation extraction as novel.
- **83-report ATT&CK classification dataset (Ryan et al., arXiv June 2026):** human-annotated 2,076 sentences from 83 reports, 114 ATT&CK techniques, reported κ=0.68. It strengthens the prior art on human-annotated ATT&CK mapping in complex report text, but the unit/task is sentence-level technique classification, not event identity or event-pair temporal relations.

**Resulting novelty boundary:** the broad building blocks—event/activity extraction, assigning event identifiers, multi-mapping to ATT&CK, ordering activities, attack sequence QA, causal/dependency modeling, and source-grounded CTI graph creation—are already represented in recent work. The proposed contribution must be an empirical measurement/annotation design centered on (i) separate report-local occurrence identity and granularity, (ii) directly supported temporal relations between resolved occurrence leaves, and (iii) information retained/partially represented/omitted/conflated by a specifically defined `A_120` distinct-technique-pair projection. The literature reviewed so far does not prove that this combined question is novel; a systematic search and full-text comparison are still required.

### 14.3 Research-question wording should expose the baseline mapping level

The v0.4.1 protocol defines primary same-technique overlap using baseline-compatible parent mapping sets `A_120(v)`, mapped to ChronoCTI’s pinned selected-120 technique vocabulary. The natural-language RQ still says “share one or more ATT&CK technique mappings” without naming that level. Before approval, clarify that the primary result uses `A_120` and exact sub-technique overlap is a separate sensitivity analysis. Suggested operational wording:

> Within a transparently sampled feasibility set of CTI reports, what proportion of assessable reports contain a directly source- or timestamp-supported temporal relation between two distinct resolved atomic activity occurrences, in a compatible scope, whose accepted parent mappings overlap in ChronoCTI’s selected-120 ATT&CK vocabulary; and what mapping-level relation information is fully omitted, partially retained, or conflated by a distinct-technique-pair projection?

This is draft wording, not an approved RQ or population-prevalence estimand. For the five-report feasibility sample, report counts and per-report outcomes only.

### 14.4 ZScaler AI draft: concrete protocol conformance failure

The AI worked draft contains a `Temporal Links` row from a repeated-series container to an atomic email event, labelled `UNRESOLVED_SCOPE_TIME_CONFLICT`. A container cannot be a primary event-edge endpoint. The campaign-start/email-date discrepancy belongs in typed `time_evidence` and a decision/scope note, not in the temporal-relation graph. The v0.4.1 schema must encode endpoint `unit_role`, `granularity`, `instance_status` and `scope_id`, and the validator must enforce them. This draft is not human annotation.

### 14.5 Remaining implementation gaps

1. `src/projection_metrics.py` does not itself reject a temporal edge where `source_event == target_event`; the annotation validator does, but the pure projection API should enforce the same invariant.
2. `project_report()` can derive partial representation from diagonal and non-diagonal pair mappings, but it does not return a named `partially_represented` count/list. Add it and test full omission, partial representation and no diagonal mapping separately.
3. Public annotation templates/validator remain v0.3; v0.4.1 needs report scopes, activity units, typed time evidence, mapping basis/accepted status, baseline-parent mapping, relation basis, compatible scope and report-level assessability.
4. Clarify `A_120` parent-level mappings versus exact technique/sub-technique mappings in the RQ and result tables. Do not mix them.

### 14.6 Sampling file/workbook corrections

At the time of v1.3, Sampling Method v0.3.1 and frame v0.8 superseded the earlier method and frame. They are now superseded by Method v0.3.2 and frame v0.9. The 120 GNE+CyNE inventory and 112 link-positive descriptive count are unchanged. The two no-CyNE records remain genre-exclusion candidates pending researcher confirmation; six other reports without valid ATT&CK links remain eligible for source-first annotation if other gates pass. The v0.9 frame retains the fixed hash ranks and candidate ordering while correcting stale internal references and flagging the base/stress overlap.

The v0.1, v0.2 and 3-November recheck screening CSVs are byte-identical (400 records; SHA-256 `fc6552832fbb48f6d21d49012943e37b00dab783d1556a1a09f1128fbb7dde8f`). Keep one canonical screening CSV in future handoffs.

## Source links checked during this audit

- CTI Evidence Lab repository: https://github.com/sanketnichit/cti-evidence-lab
- AnnoCTR repository and corpus licence: https://github.com/boschresearch/anno-ctr-lrec-coling-2024
- AnnoCTR paper: https://aclanthology.org/2024.lrec-main.103/
- ChronoCTI paper: https://doi.org/10.1007/s10115-025-02491-6
- ChronoCTI code: https://github.com/rayhanur-rahman/ChronoCTI
- SMAH-CTI page: https://seal.cs.ucf.edu/projects/smah-cti.html
- SMAH-CTI paper: https://aclanthology.org/2026.findings-emnlp.1180/
- 83-report ATT&CK classification preprint: https://arxiv.org/abs/2606.18166
- APTIE paper: https://doi.org/10.1038/s41597-026-07487-7
- EventRelBench paper: https://aclanthology.org/2025.findings-emnlp.482/
- AttackSeqBench preprint: https://arxiv.org/abs/2503.03170
- Reachable attack chains preprint: https://arxiv.org/abs/2607.19742
- CSEM-CTI paper: https://doi.org/10.1016/j.isci.2026.116466
- Cybersecurity event-extraction survey: https://doi.org/10.1049/cmu2.70187
- TIMELINE: https://aclanthology.org/2023.emnlp-main.1016/
- MAVEN-ERE: https://aclanthology.org/2022.emnlp-main.60/
- CASIE: https://doi.org/10.1609/aaai.v34i05.6401
- MITRE Attack Flow: https://center-for-threat-informed-defense.github.io/attack-flow/introduction/


## Additional sources reviewed for v1.2

- Wu, H.-C. (2026). *LLM-Based Construction of Attack Life Cycles from CTI Reports*. Master’s thesis, National Taiwan University. DOI: https://doi.org/10.6342/NTU202600249. Full text: https://tdr.lib.ntu.edu.tw/jspui/retrieve/5301efd0-5f40-4dfe-8cf4-6623bfb48110/ntu-114-1.pdf
- Ma et al. (2025). *AttackSeqBench: Benchmarking Large Language Models in Analyzing Attack Sequences within Cyber Threat Intelligence*. arXiv:2503.03170. https://arxiv.org/abs/2503.03170
- AttackSeqBench related manuscript marked under review at ICLR 2026 in the retrieved OpenReview PDF: https://openreview.net/pdf?id=e3Z60Ri5JP
- Hou et al. (2026). *An Automated Framework for Extracting Reachable Attack Chains from Cyber Threat Intelligence Reports*. arXiv:2607.19742. https://arxiv.org/abs/2607.19742
- Sun et al. (2026). *A multi-task information extraction Chinese dataset for APT cyber threat intelligence*. Scientific Data. https://doi.org/10.1038/s41597-026-07487-7
- Das et al. (2026 preprint). *A Structured Cyber Threat Intelligence Dataset Using STIX 2.1 Entities and MITRE ATT&CK Mappings*. arXiv:2607.23312. https://arxiv.org/abs/2607.23312
- Ryan et al. (2026). *Evaluating Open-Source LLMs for Multi-Label ATT&CK Technique Classification on CTI Reports*. arXiv:2606.18166. https://arxiv.org/abs/2606.18166
- Gong et al. (2025). *EventRelBench: A Comprehensive Benchmark for Evaluating Event Relation Understanding in Large Language Models*. Findings EMNLP 2025. https://aclanthology.org/2025.findings-emnlp.482/
- SMAH-CTI paper: https://aclanthology.org/2026.findings-emnlp.1180/
- SMAH-CTI schema: https://github.com/davidmohaisen/SMAH-CTI/blob/main/schema/schema.json
- APTIE paper: https://doi.org/10.1038/s41597-026-07487-7
- CASIE paper: https://doi.org/10.1609/aaai.v34i05.6401
- Cybersecurity event-extraction survey: https://doi.org/10.1049/cmu2.70187

## v1.3 local artifact hashes

- `AnnoCTR_Fresh_MultiVendor_Sampling_Method_v0.3.1.md`: `7e63d30143abf9f8b9d229fe8f0ce63a93de22a8d98248efe85c56ff778ce916`
- `AnnoCTR_Fresh_MultiVendor_Sample_Frame_v0.8.xlsx`: `fceed15abc0f379e069fb21262fe9de9b9c0f3b0bf2b564081c7b28b1bcfe8e1`
- `CTI_Event_Instance_Annotation_Protocol_v0.4.1-draft.md`: `b77eebe701a51b3cef3d2091e95efcbb50b2288fe5604ea4f9fcd08b8da40b83`


---

## 15. v1.4 schema and workbook cross-checks (3 November 2026)

### 15.1 Schema v0.4.2 — meaningful but incomplete migration

The blank schema package `CTI_Annotation_Schema_v0.4.2-draft` contains all eight minimum registers named in protocol v0.4.1 (`report_registry`, `report_scopes`, `activity_units`, `event_mentions`, `event_mappings`, `time_evidence`, `temporal_relations`, and optional `candidate_pair_assessments`). It adds `evidence_spans`, `record_evidence_links`, `non_temporal_relations`, and `adjudication_log`. All 15 entries in its SHA256 manifest match and the ZIP passes integrity testing.

It is still not a frozen data-entry schema. The separate conformance audit identifies P0/P1 items: explicit temporal evidence scope, annotation/schema/pass identity, evidence-link row keying, unit/granularity/status invariants, mention-to-unit status consistency, relation endpoint/scope/basis validation, selected-120 vocabulary availability, direct-versus-linked evidence rules, candidate-pair scope rules, non-temporal endpoint granularity, mapping status/basis combinations, and timestamp normalization rules.

Most importantly, there is no v0.4.2 validator or synthetic validator test suite yet. The public GitHub v0.3 validator cannot be described as validating v0.4.2. Do not start the five-report annotation until protocol/schema decisions are approved and the new validator passes synthetic tests.

### 15.2 Corrected frame v0.9 and residual v0.8 issues

Direct inspection found that frame workbook v0.8 retained stale internal metadata despite the prior audit's statement that these items had been corrected:

- Dashboard cell A1 still labelled the workbook v0.7.
- Four rank-1 candidate notes still referenced `AnnoCTR_Five_Report_Batch_Review_v0.1.xlsx` rather than the current structured workbook v0.2.
- The Batch Review Handoff sheet still pointed to the v0.1 workbook.
- The Intel471 Groove report was simultaneously in the rank-1 base candidate list and marked `PURPOSIVE_STRESS` in the stress queue.

Frame v0.9 now changes the dashboard label, updates the batch-review workbook handoff references to v0.2, and flags the duplicated Intel471 row as `BASE_CANDIDATE_OVERLAP` / `DO_NOT_SELECT_AS_STRESS`. It does not select or freeze any report.

The sampling method is now v0.3.2. It states explicitly that only *additional, non-overlapping* reports may be used as purposive stress cases. If the Intel471 candidate enters the base sample it cannot also be counted as stress; if it fails a predeclared source/scope/local-use gate, it cannot re-enter as stress.

### 15.3 Independent integrity checks on frame v0.9

Rechecked all 120 frame rows against the documented seed and the frozen AnnoCTR source text:

| Check | Result |
|---|---:|
| Report rows | 120 |
| Donor strata | 5 |
| Vendor counts | 30 / 23 / 28 / 12 / 27 |
| Priority SHA256 mismatches | 0 |
| Within-vendor rank mismatches | 0 |
| Frozen source-text SHA256 mismatches | 0 |

The five rank-1 candidate IDs are unchanged. This confirms priority order and source provenance hashes, not report eligibility or event content.

### 15.4 Screening export duplication

The three local screening CSVs (`v0.1`, `v0.2`, and the 3-November recheck) are byte-identical: SHA256 `fc6552832fbb48f6d21d49012943e37b00dab783d1556a1a09f1128fbb7dde8f`. Keep one canonical screening export in future bundles; do not describe these as three independent screening runs.

### 15.5 Local artifact status

The frame v0.9 and method v0.3.2 corrections are local artifacts only. The public GitHub repository remains at the previously verified `b002486...` main head and has not been changed. The v0.4.2 schema and conformance audit are also local drafts, not a public implementation.