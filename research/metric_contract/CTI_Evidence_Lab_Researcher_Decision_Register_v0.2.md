# CTI Evidence Lab — Researcher Decision Register v0.2

**Prepared:** 8 November 2026  
**Status:** Updated working decision record. The AnnoCTR permission gate, two source-scope dispositions, evidence-scope rules, mapping-acceptance rules, prior-exposure handling, candidate-pair negative-label rules and primary attack-action event-universe boundary and incident-bounded primary comparison-scope rule have been adopted under delegated project direction. The protocol and reconstructed schema remain drafts and are not frozen.  
**Purpose:** Separate decisions already grounded in available documents from provisional recommendations and choices that require explicit researcher approval before formal annotation.

## 1. How to read this register

- **Source-grounded:** explicitly stated by an available project artifact.
- **Adopted working default:** selected under delegated project direction; this does not freeze the protocol or reconstructed schema.
- **Recommended:** the current best methodological recommendation, still open for revision.
- **Blocked by missing original:** the exact wording or field design in Protocol v0.4.1 / Schema v0.4.2 cannot be verified because those original files are unavailable.

The current executable package is `CTI_Annotation_Schema_RECON_v0.1`. It is a reconstruction, not the original v0.4.2 schema, and must not be used for formal annotation until the decisions below are reviewed and the schema is approved/frozen.

## 2. Decisions and current recommendations

| # | Decision | Source-grounded position | Current recommendation | Status |
|---|---|---|---|---|
| 1 | Sampling population | The official manifest has 120 GNE+CyNE reports and 112 with an existing valid ATT&CK link. The 112 count is a linking-layer statistic, not the source-annotation frame. A second-pass read found a sponsored Ponemon survey summary (Proofpoint) and a TIBER-EU framework explainer (QuoIntelligence), not report-local CTI incident reporting. | Keep all 120 records in the historical inventory. Exclude those two documents from the declared CTI-report source-scope population based on genre/content; retain the other six no-link reports for source-first review if their independent gates pass. Missing CyNE/ATT&CK links alone are not an exclusion basis. | **Two source-scope exclusions recorded 5 November 2026; 118 records remain in the candidate frame, not automatically eligible** |
| 2 | Base feasibility selection | Five rank-1 candidates were selected by deterministic within-vendor hash priority, one per donor. They are candidate reports, not selected reports. | Keep the five rank-1 candidates in order. Advance only for predeclared source identity, completeness, scope, provenance/rights or practical local-use failure—not for event yield or a missing positive edge. | **Method correction adopted; 0/5 human eligibility decisions** |
| 3 | Primary mapping vocabulary | ChronoCTI's version-of-record paper states in Section 4.1 that its study used Enterprise ATT&CK v12.1 (193 techniques). The selected `A_120` vocabulary is pinned to the exact `selected_techniquesWName.json` source commit/blob in the repo. | Use accepted, source-supported parent-level `A_120` mappings as the primary analysis vocabulary. Keep exact technique/sub-technique `A_exact` results as a separate sensitivity view. Enterprise ATT&CK v12.1 is the pinned working crosswalk release. | **Working default adopted; 737-row crosswalk generated, committed and covered by passing synthetic CI on 5 November 2026; empirical annotation still pending** |
| 4 | Positive temporal labels in primary incidence | Available Protocol v0.4-draft includes `BEFORE`, `AFTER`, `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` as positive temporal labels. Audit v1.4 describes the v0.4.1 primary within-technique outcome using these five. | Count all five labels for broad within-technique temporal-relation incidence only when relation-specific evidence, event eligibility and compatible scope are satisfied. A `direct_timestamp` basis is limited to strict `BEFORE`/`AFTER`; `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` require an explicit `direct_source` assertion. Strict cycle analysis remains a separate `BEFORE`/`AFTER`-only subset. | **Working default adopted 4 November 2026; timestamp-basis boundary specified 14 November 2026; protocol/schema freeze remains open** |
| 5 | Strict-order cycle analysis | Protocol and audits distinguish temporal relation labels from strict ordering. | Use only `BEFORE`/`AFTER` for strict-order cycles. In derived pair-key views normalize `AFTER(A,B)` to the same precedence as `BEFORE(B,A)` and treat both as `STRICT_ORDER`; retain the original source label, endpoint order and evidence in the annotation registers. | **Source-grounded rule; synthetic implementation corrected, real-data validation pending** |
| 6 | Report-level denominator | Audit v1.4 distinguishes eligible reports, zero-event outcomes and `NOT_ASSESSABLE`. The report registry separately records source/scope eligibility, local-use permission, report assessability and full-report review completion. | Count each report once. Define `N_eligible` as reports passing source/scope eligibility and local-research-use permission; public-reuse permission is separate. Define `N_assessable` as eligible reports with at least one completed human full-report review partition, a complete/readable frozen source, and `report_assessability=ASSESSABLE`, after report-level eligibility/local-use/assessability conflicts are resolved. If multiple annotators or passes exist, calculate report-level outcomes from the designated locked final annotation or agreed/adjudicated consensus partition, not by summing partitions. Report `N_assessable / N_eligible` coverage. Retain a fully reviewed report with zero resolved event leaves as an assessable zero outcome. Keep `NOT_ASSESSABLE`, `PENDING`, incomplete review and unresolved decision conflicts out of `N_assessable`; report them separately and never recode them as zero. | **Adopted as the project default on 4 November 2026 under delegated decision; protocol/schema remain provisional** |
| 7 | Pair opportunity versus positive relation | Audit v1.4 says the repeated-occurrence measure is opportunity, not the primary temporal outcome. | Report separate rates: (a) same-technique pair opportunity; (b) positive within-technique temporal relation. Never use pair opportunity as a proxy for a positive temporal result. | **Strongly supported; metric naming/formula approval pending** |
| 8 | Negative pair labels | Available protocol describes full-report positive-relation discovery separately from optional candidate-pair assessments. Missing pairs are not necessarily reviewed negatives. | Do not construct an exhaustive all-pairs negative matrix. Use `NO_TEMPORAL_CLAIM` only in a declared candidate-pair assessment frame with a frozen generation rule/version. `NOT_ASSESSABLE`, missing rows and unresolved pairs remain distinct. | **Adopted working rule 5 November 2026; included in Protocol v0.5-draft** |
| 9 | Primary event graph eligibility | Recovered Protocol v0.4-draft and audits restrict the primary graph to resolved atomic `event_leaf` activity units. | Require distinct endpoints, `event_leaf`, `atomic_event`, `RESOLVED`, compatible recorded scope, relation-specific evidence, and direct source/timestamp relation basis. Keep series, episodes, aggregates, generic behaviour and unresolved units visible outside the primary graph. | **Source-grounded; exact cross-register status rules still need approval** |
| 10 | Evidence scope | Recovered v0.4 draft contains `evidence_scope`; audit v0.4.2 says explicit values should include `SENTENCE`, `CROSS_SENTENCE`, `DOCUMENT_CONTEXT`. The v0.4.2 schema audit says the column was absent from the missing schema draft. | Retain explicit evidence scope on temporal relations. `DOCUMENT_CONTEXT` does not relax direct-source/direct-timestamp evidence requirements; record all required argument-support spans. | **Adopted working rule 5 November 2026; included in Protocol v0.5-draft** |
| 11 | Mapping acceptance | Audit v0.4.2 requires mapping basis and accepted-vs-alternative semantics; public v0.3 does not encode them. | Accept report-explicit mappings with source evidence; accept analyst candidates only after human rationale/evidence review; keep workbook-only/unresolved/rejected/alternative-only out of primary mapping sets; preserve multiple independently supported accepted mappings without multiplying event instances. | **Adopted working rule 5 November 2026; included in Protocol v0.5-draft** |
| 12 | Human agreement | No independent human second annotation has been completed. AI-assisted review is not an independent human rater. | Arrange a genuinely independent second annotator for an overlapping subset if feasible. Otherwise state that IAA was not measured; a same-researcher washout pass is intra-annotator consistency only. | **Open researcher/workflow decision** |
| 15 | Prior AI triage exposure | Five rank-one candidates were previously reviewed with automated suggestions, including proposed activity units/series. Prior report-specific machine-generated interpretations have already been reviewed. | Record the researcher's pass on the five rank-one reports as `AI_EXPOSED`; a washout/read-again pass does not erase exposure. An independent second human annotator can be `UNEXPOSED` only if they have not seen earlier report-specific interpretations. Automated suggestions are never a second rater. | **Adopted working rule 5 November 2026; apply in Protocol v0.5-draft** |
| 16 | Source text hashing and offsets | The 120-row frame contains `source_text_sha256`, while raw AnnoCTR report text remains local and excluded from the repository. | Use strict UTF-8; strip only an optional leading BOM; preserve CRLF/LF; no Unicode normalization; hash UTF-8 bytes of the exact decoded text; use zero-based, end-exclusive Python Unicode code-point offsets. | **120/120 frame hashes matched official AnnoCTR text files at pinned source commit `d510b6949e1938d47c93a43eedd562dc538439dc` on 4 November 2026; archive ZIP hash is a separate check** |
| 17 | Primary event universe | ChronoCTI's version-of-record paper targets temporal relations in step-by-step cyberattack incident narratives and excludes social-media posts, malware capabilities/features, and non-attack content. Its example includes both phishing delivery and the induced user execution of a malicious attachment. | Use incident-linked attack-action occurrences as the primary ChronoCTI-comparable stratum. Include concrete actions that conduct, enable, or complete a specific attack, including induced user/system actions; classify communications by their operational role, not their medium. Retain public commentary/platform events, analyst/sample observations, generic capabilities, and other non-primary activity in separate descriptive strata. Stratum assignment must be independent of ATT&CK mapping. Keep the five fixed rank-one reports unchanged regardless of event yield. | **Adopted as a working research-design decision on 8 November 2026. Draft enforcement implemented in RECON v0.4 with one-to-one activity_unit_strata.csv coverage, stratum locks and primary projection/pair-opportunity filtering; 13 synthetic tests passed in CI run #226. Protocol/schema freeze and individual pre-annotation decisions remain pending.** |
| 18 | Primary comparison-scope rule for event-pair opportunity | ChronoCTI describes its input as a textual description of an attack incident and filters for CTI reports that narrate cyberattack incidents step-by-step (Rahman et al., 2025, Sections 1 and 4.4.2). The legacy nearest-common-non-report ancestor rule can compare separate INCIDENT nodes merely because they share a campaign/operation/organisation ancestor. | Use the nearest shared `scope_type=INCIDENT`, `scope_status=RESOLVED` ancestor. Count each event pair once; require a primary positive temporal relation to cite that exact same nearest incident scope. Campaign/operation/organisation/host/OTHER scopes alone do not create primary pair opportunity. Preserve broader-scope relations and calculate the legacy and explicit-assignment approaches only as separate sensitivity analyses. Do not invent incident scopes to create eligible pairs. | **Adopted as the working primary rule on 8 November 2026 under delegated project direction; v0.2 aggregator and v0.4 attack-action projection default updated, numerator/denominator parity enforced in code. Protocol/schema freeze remains pending; no real-report rates exist.** |
| 19 | Timestamp-derived relation semantics and timezone normalization | RECON v0.2 already checks invariant strict `BEFORE`/`AFTER` ordering across retained endpoint intervals, but the earlier protocol did not define what bounds represented or prevent non-strict labels from using timestamp-only evidence. | Treat normalized bounds as closed ranges of possible occurrence instants, not action durations. `direct_timestamp` may support only `BEFORE`/`AFTER`, with strict separation across every retained A/B interval combination. Require explicit source assertions (`direct_source`) for `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED`; do not infer them from equal timestamps, shared dates, or overlapping uncertainty windows. Preserve the literal source zone, reject unresolved/inferred/ambiguous timezone interpretations for timestamp-derived edges, and normalize accepted bounds to UTC. | **Adopted as a working default on 14 November 2026 under delegated project direction; v0.2 validator and 86-test suite verified in CI run #236. Timezone correctness and semantic entailment remain human-reviewed; full protocol/schema freeze pending.** |
| 13 | Rights and outputs | AnnoCTR identifies the corpus as CC BY-SA 4.0. The dataset maintainer replied on 5 November 2026 that source-material licences had been checked and allow redistribution under the dataset licence, and that annotations/adaptations may be published under the same licence. His recollection was qualified and not legal advice. | Record local research use and derivative publication as PERMITTED for the five fixed rank-one candidates, subject to attribution and ShareAlike. Keep raw reports and extended excerpts out of Git; keep source-scope eligibility separate; do not apply the repository MIT licence to source-derived annotation material. Reopen only if a report-specific exception emerges. | **Maintainer clarification received 5 November 2026; working permission gate cleared, subject to stated qualification and CC BY-SA conditions** |
| 14 | Novelty claim | ChronoCTI directly predicts temporal relations over ATT&CK technique pairs; APTIE adds Chinese CTI event extraction and entity-relation labels; SMAH-CTI adds sentence-level NER, ATT&CK mapping and procedures; a July 2026 survey describes cybersecurity ERE as underdeveloped and notes no unified public benchmark. | Keep the candidate contribution limited to source-grounded identity of distinct report-local activity occurrences, explicit temporal relations between them, and the information retained/conflated/omitted under a named distinct-technique-pair projection. Do not claim event extraction, ATT&CK mapping, entity-relation extraction or temporal CTI extraction as new. | **Not approved; 5 November 2026 literature boundary refreshed; full schema-level comparison and empirical feasibility still required** |

## 2A. Operational rules adopted for the pilot draft — 5 November 2026

The following working rules are derived from the recovered Protocol v0.4-draft and the current RECON data model. They were adopted under delegated project direction on 5 November 2026 and are incorporated into Protocol v0.5-draft. They do not constitute human annotations, validate semantic labels, or freeze the reconstructed schema.

### Evidence scope on temporal relations

| Value | Proposed operational meaning | What qualifies | What does not qualify |
|---|---|---|---|
| `SENTENCE` | The relation and the endpoint references are supported within one sentence. | One sentence contains the temporal cue or timestamp relation and enough argument support to identify both event leaves. | A sentence merely naming two events without relating them. |
| `CROSS_SENTENCE` | The relation is supported across two or more linked sentences. | A temporal cue in one sentence and an explicit, unambiguous reference/coreference to one or both endpoints in another; record every necessary span. | Ordering sentences in the report and assuming that the described actions happened in that order. |
| `DOCUMENT_CONTEXT` | Relation support requires multiple passages or wider report context. | The source still contains a direct temporal assertion or explicit timestamp evidence; link the relation-specific cue and the endpoint-supporting passages, and state the argument connection in notes. | Inferring chronology from headings, section order, analyst knowledge, campaign narrative, or the fact that both events appear in the same report. |

**Adopted gate:** `DOCUMENT_CONTEXT` describes where the evidence is distributed; it does not weaken the direct-evidence requirement. A positive primary edge still requires `direct_source` or `direct_timestamp`, two distinct resolved atomic event leaves, compatible comparison scope, and relation-specific evidence. If the connection between passages requires an analyst inference rather than a source-supported reference, retain it as unresolved/inference outside the primary graph.

### Timestamp-derived temporal labels and timezone normalization

1. `normalized_start`/`normalized_end` are closed bounds on possible occurrence instants, not an estimate of action duration. Point times have equal bounds; coarse precision uses the full possible range and requires uncertainty notes.
2. Only an `ATTACK_OCCURRENCE` time record tied to the matching endpoint can support `direct_timestamp`. Detection, discovery, publication, upload, compilation, report-retrieval and attack-period times are not substitutes.
3. A timestamp-only positive may be `BEFORE` or `AFTER` only. For `BEFORE(A,B)`, every retained A interval must satisfy `A_end < B_start`; `AFTER` reverses the test. Equality, touching bounds, overlap, or any retained unresolved candidate blocks a strict timestamp edge.
4. `OVERLAP`, `SIMULTANEOUS`, and `CONCURRENT_UNSPECIFIED` require explicit source wording and `direct_source`. Matching timestamps, same-day dates, common time windows, and overlapping uncertainty intervals do not establish these labels.
5. Preserve the literal source zone/offset. Do not infer timezone from location or publisher context. Ambiguous abbreviations and unresolved DST folds/gaps cannot be normalized to a single instant. Accepted normalized bounds use UTC and `normalized_timezone=UTC`; the raw source zone remains in `timezone_text`.
6. If source wording and timestamps conflict, preserve and review the discrepancy; do not silently prefer either. Human review remains responsible for occurrence identity, correct time type, timezone interpretation and relation entailment.

### Mapping decision and acceptance

1. Preserve the exact ATT&CK technique/sub-technique ID supported by the report and validate its name and parent through the pinned Enterprise ATT&CK v12.1 crosswalk. Do not map from a malware family, tool name, threat actor label, or a workbook occurrence alone.
2. `report_explicit_subtechnique` and `report_explicit_parent` mean the report itself explicitly supplies the corresponding ATT&CK mapping. Retain a source span showing that explicit mapping.
3. `source_supported_analyst_candidate` means the report describes a specific activity and a human annotator proposes a technique based on the ATT&CK definition. It is a candidate until the annotator records a rationale and mapping-specific evidence span and a human review accepts it. The basis is permitted for an accepted mapping only after that review; the validator cannot decide semantic fit.
4. `workbook_only` and `unresolved` must never be accepted into primary `A_exact` or `A_120`.
5. `ALTERNATIVE` is for mutually exclusive competing interpretations of one mapping decision. Put them in a shared alternative group and exclude them from the accepted set until resolved. Do not mark two independently supported techniques as alternatives merely because one event has multiple mappings.
6. Multiple independently supported `ACCEPTED` mappings may coexist on one activity unit. Each requires its own evidence and confidence. Multiple mapping rows never create additional event instances.
7. A technique can enter primary `A_120` only when the mapping decision is `ACCEPTED`, the basis is source-supported, the exact ID resolves through the pinned crosswalk, the parent is in `A_120`, and the lifecycle rule is satisfied. This is a human mapping decision plus a mechanical taxonomy check—not an automatic ATT&CK suggestion.

### Prior exposure and independent review

| Value | Proposed recording rule |
|---|---|
| `UNEXPOSED` | The annotator has not seen earlier annotation decisions, candidate spans, mapping suggestions, or feasibility interpretations for that report. |
| `AI_EXPOSED` | The annotator has seen machine-generated triage, candidate event/mapping suggestions, or prior automated interpretations for that report. |
| `HUMAN_EXPOSED` | The annotator has seen another human's annotation decisions for that report before completing their own pass. |
| `MIXED` | Both machine-generated and other-human annotation material were seen before the pass. |
| `UNKNOWN` | Exposure history cannot be established with confidence. |

**Adopted exposure rule:** the researcher's eventual annotation pass on the five rank-1 reports should be recorded as `AI_EXPOSED`, because the source-first feasibility interpretations have already been reviewed. A washout interval may support a repeatability check, but it does not erase exposure or turn that pass into a blind pass. A genuinely independent second annotator may be recorded as `UNEXPOSED` only if they have not seen the earlier report-specific interpretations or labels. Keep independent passes separate until both are locked; measure intra-annotator consistency for a repeat pass and inter-annotator agreement only across independent human passes.

### Candidate-pair assessment and negative labels

- Positive temporal-relation discovery remains a full-report source-review task; it must not be restricted to pairs found by a candidate generator.
- `NO_TEMPORAL_CLAIM` may be assigned only to an actual pair that was reviewed under a frozen `candidate_rule_id` and `candidate_rule_version`.
- `VAGUE_OR_AMBIGUOUS` means the source appears to relate the pair temporally but the relation cannot be resolved.
- `NOT_ASSESSABLE` means the available evidence/context does not permit a defensible pair judgment.
- A missing row or blank cell means not assessed. It is not a negative temporal label.
- Do not generate an exhaustive all-pairs negative matrix merely to fill the register. Report the candidate-pair rule and its coverage separately from full-report positive-edge discovery.

### Researcher-owned dispositions still required

| Item | Current recommendation | Formal status |
|---|---|---|
| Proofpoint sponsored Ponemon survey summary with no CyNE rows | Exclude from the CTI threat-report source-scope eligible population; retain its historical row in the 120-report manifest. The reason is source genre/scope, not missing ATT&CK links. | **Adopted INELIGIBLE 5 November 2026** |
| QuoIntelligence TIBER-EU framework explainer with no CyNE rows | Exclude from the CTI threat-report source-scope eligible population; retain its historical row in the 120-report manifest. The reason is source genre/scope, not missing ATT&CK links. | **Adopted INELIGIBLE 5 November 2026** |
| Five rank-1 report local research use | Proceed under the AnnoCTR CC BY-SA licence on the basis of the 5 November maintainer clarification; maintain attribution and record the licence basis. | Permission gate cleared for all five; researcher/source-scope eligibility remains pending |
| Public reuse of derivatives | Publish adapted annotation material under the same CC BY-SA licence, with attribution and ShareAlike. Keep raw reports and extended excerpts out of Git; assess any later quotation/excerpt plan separately. | Derivative-publication gate cleared for all five, subject to licence conditions and the maintainer's stated qualification |

These source-scope dispositions change two eligibility fields in the successor frame v1.0 while preserving both rows in the historical 120-report inventory. The remaining protocol defaults do not create any event-level labels or human annotations. They are working project decisions, not evidence that any report contains a particular event or temporal relation.


## 2B. Additional protocol-boundary proposals — 5 November 2026

These are recommendations for the initial feasibility pilot, not adopted researcher decisions. They are recorded here because the current protocol and reconstructed registers must not imply that an unsupported relation type can be annotated in an improvised field.

| Item | Source-grounded position | Current recommendation | Formal status |
|---|---|---|---|
| Temporal evidence field representation | RECON v0.2 stores the relation cue as `temporal_relations.primary_evidence_span_id`, exact text/offsets in `evidence_spans`, and endpoint/context support in `temporal_relation_evidence.csv`. Protocol v0.5 previously listed duplicate `cue_text` and `argument_support` fields. | Use linked evidence-span IDs and role-coded support; do not duplicate verbatim source text in separate cue/argument free-text fields. Require A/B support on positive direct relations and the v0.2 scope gates. | **Implemented as a draft protocol/schema reconciliation; researcher approval still required at freeze** |
| Episode-to-episode temporal relations | Protocol v0.5 previously requested a separate exploratory register, but RECON v0.1/v0.2 has no such register. Episode containers are distinct from atomic event leaves. | Defer episode-to-episode relation records from the initial pilot. Preserve episode containers and their evidence/time information; do not use episode IDs in the primary atomic temporal register. Add a separate register only in a later approved extension. | **Proposed; researcher approval required** |
| ChronoCTI pair-to-event alignment | Benchmark technique-pair rows have no report-local event IDs or relation-specific source spans. The current RECON package has no dedicated alignment register. | Defer record-level benchmark-to-event-pair labels from the initial pilot. Preserve raw benchmark IDs/labels/provenance separately; do not overload event mappings or candidate-pair assessments. | **Proposed; researcher approval required** |
| Scope-pair opportunity denominator | The legacy v0.2 rule treats any nearest shared resolved non-report ancestor as sufficient and can include cross-incident pairs under a broad campaign/operation ancestor. ChronoCTI frames its input as a description of an attack incident and selects step-by-step incident narratives. | Use the nearest shared resolved INCIDENT ancestor for primary opportunity and require a primary positive relation to name that exact same scope. Keep the legacy nearest shared non-report ancestor and v0.3 explicit event-to-scope assignment as separate sensitivities. A report with no defensible resolved INCIDENT scope remains assessable but contributes no incident-bounded pair opportunity; do not create incident scopes to increase yield. | **Adopted working primary rule 8 November 2026; code default and relation-scope filter updated, 13 v0.4 tests and affected v0.2 scope tests passed in CI run #228 (241 synthetic test executions total); formal protocol/schema freeze and real-report rates remain pending.** |


### Primary comparison-scope decision — 8 November 2026

The primary pair universe is incident-bounded. This follows ChronoCTI's own stated task framing: a textual description of an attack incident, and report inclusion based on a step-by-step incident narrative. The broad nearest-common-ancestor rule is not a suitable primary rule because it can treat separate incidents as comparable solely through campaign, actor-operation, victim-organisation, host or OTHER ancestry.

The selected primary rule is the nearest shared resolved INCIDENT scope. If nested INCIDENT nodes are shared, use the nearest; count the event pair once. A positive relation must cite the same scope ID. A campaign-only relationship does not qualify for primary opportunity or primary positive-edge counts. The relation remains in the source annotation and may be included in a separately labelled broader-context sensitivity view.

The explicit v0.3 assignment rule remains valuable as a separate sensitivity because it requires event-by-scope decisions, evidence and rationale, and a dedicated lock. It is not primary: it can affirm broader shared non-report scopes and its current lock supports SINGLE_ANNOTATOR_FINAL only. The legacy rule is also retained as a diagnostic upper-bound/broader-context sensitivity. Each sensitivity must recompute both numerator and denominator under its own rule.

**Source:** Rahman et al., *Mining temporal attack patterns from cyberthreat intelligence reports*, Knowledge and Information Systems (2025), Sections 1 and 4.4.2, https://doi.org/10.1007/s10115-025-02491-6.

**Feasibility implication:** the current five-report scope-candidate draft contains campaign, actor-operation, victim-organisation and OTHER scopes, but no accepted INCIDENT scope. All candidate scope rows remain unaccepted. Do not relabel them as INCIDENT merely to permit pair counting. This may produce zero primary pair opportunities in the feasibility batch; report that limitation rather than broadening the primary estimand after reviewing event yield.

### Scope-comparability validator parity — technical correction, 5 November 2026

The v0.1 validator and v0.2 opportunity counter now use one shared helper for resolved comparison-scope ancestry. A primary positive temporal relation or `COMPATIBLE` candidate-pair assessment must identify a scope that is a shared `RESOLVED` ancestor of both endpoints and whose type is in the same provisional non-report comparison set used by opportunity counting. A `REPORT_AGGREGATE`, provisional, unresolved, or otherwise non-comparable scope is rejected. This guarantees that a structurally accepted primary relation cannot fall outside the pair-opportunity universe. The helper preserves the current broad scope set, including `CAMPAIGN`, `ACTOR_OPERATION`, `VICTIM_ORGANISATION`, `HOST`, and `OTHER`; whether those scopes should permit cross-incident comparability remains an open researcher decision. No rate gate is opened by this correction.

The deferrals do not prevent the study from annotating source-supported relations between distinct atomic event leaves or measuring how those event edges are transformed by the named technique-pair projection. They do prevent the initial pilot from claiming an event-level gold alignment to ChronoCTI's benchmark pair rows or reporting episode-edge metrics.

---

### Permission-chain clarification route — 5 November 2026

The official AnnoCTR README states that the corpus is licensed CC BY-SA 4.0 and identifies a dataset contact. A written response from that contact was received on 5 November 2026. He stated that, to the best of his recollection, source-material licences had been checked and permit redistribution under the dataset licence; he also said that researchers may add annotations/change reports and publish derivatives under the same CC BY-SA licence. The response was qualified and expressly not legal advice. The project records local research annotation and derivative publication as PERMITTED for the five rank-one candidates, subject to attribution and ShareAlike. No per-report exception list was provided. Keep raw corpus text and extended excerpts out of Git; the repository MIT licence applies to project software, not source-derived annotation material.

Sources:
- https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/main/README.md
- https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/main/LICENSE.txt
- https://creativecommons.org/licenses/by-sa/4.0/
### Rights review update — 5 November 2026

A focused check of primary-source terms found that the AnnoCTR repository README states CC BY-SA 4.0 for the corpus and acknowledges Intel471 and Lab52/S2 Grupo as donors. Intel471's current Terms of Service reserve copying/reproduction/download/distribution rights absent written authorization unless otherwise permitted; the Lab52 legal notice allows one offline personal/non-commercial copy but separately restricts reproduction and transformation without prior written authorization. For Proofpoint, the public blog article carries a copyright footer, while its linked terms directory covers customer/product/service terms rather than a general blog-content licence; a separate 2014 login-portal terms page was not treated as governing the public article. QuoIntelligence's linked Terms and Conditions are expressly for the Mercury client portal, and its privacy policy is not a content licence; terms for a similarly named but distinct legal entity were not applied. Zscaler's blog disclaimer provides no reuse licence, while its Legal Overview points to a customer-product subscription agreement rather than a general blog-content licence. No article-specific reuse grant was verified for these three publishers. These checks do **not** decide the validity or scope of the corpus-level licence, and absence of a located grant is not a legal conclusion that use is prohibited. The 5 November maintainer clarification now supports local research annotation and derivative publication under the AnnoCTR CC BY-SA licence for all five rank-one candidates, subject to attribution and ShareAlike. The five frame rows record PERMITTED for local research use and public reuse of derivatives; source-scope eligibility remains pending.

Sources:
- https://github.com/boschresearch/anno-ctr-lrec-coling-2024
- https://www.intel471.com/legal/terms-of-service
- https://www.lab52.io/legal_note
- https://www.proofpoint.com/us/blog/threat-insight/malware-masquerades-privacy-tool
- https://www.proofpoint.com/us/legal/license
- https://login.proofpoint.com/termsconditions/
- https://quointelligence.eu/2020/04/winnti-group-insights-from-the-past/
- https://quointelligence.eu/terms-conditions/
- https://quointelligence.eu/privacy-policy/
- https://www.zscaler.com/blogs/security-research/targeted-attack-government-organizations-delivers-netwire-rat
- https://www.zscaler.com/legal/overview

## 3. Missing-original dependencies

The exact `CTI_Event_Instance_Annotation_Protocol_v0.4.1-draft.md` and original `CTI_Annotation_Schema_v0.4.2-draft.zip` remain unrecovered. Available materials include Protocol v0.4-draft, its migration note, the v0.4.2 conformance audit, project-wide audit v1.4, five-report re-audit v0.1, sampling method v0.3.2, and the public v0.3 repository templates/validator.

Consequently, the following cannot be asserted as exact original v0.4.2 details: all 12 register headers and column order, complete original enum lists, exact required/optional markers, evidence-link key policy, complete candidate-pair labels, exact non-temporal endpoint schema, and whether the ZIP bundled the selected-120 file. RECON v0.1 supplies explicit proposed fields for a new reconstruction, not recovered original headers.

## 4. Current technical readiness versus research readiness

| Area | Status |
|---|---|
| A_120 source provenance | Pinned to ChronoCTI commit and blob; ordered ID-only extraction SHA-256 recorded |
| RECON schema package | 12 blank proposed registers; not original v0.4.2; not approved/frozen |
| RECON v0.1 structural validator | 41 synthetic tests pass |
| RECON v0.1 projection module | 16 synthetic tests pass |
| RECON v0.1 register-to-projection adapter | 11 synthetic tests pass; requires a matching computed partition/source digest |
| RECON v0.1 combined suite | 69/69 pass (41 validator, 16 projection, 12 adapter) |
| RECON v0.2 extension, selection and aggregation suite | 72/72 synthetic tests pass |
| Root repository suite | 57/57 synthetic tests pass |
| Latest combined CI verification | 198 successful test executions in GitHub Actions run #144 on 5 November 2026; all 31 RECON v0.1 checksums and both blank-bundle validators passed |
| Real AnnoCTR data through RECON | 0 rows |
| Researcher eligibility decisions | 0/5 |
| Human annotation locks | 0 |
| IAA | Not measured |
| Real-report projection results | 0 |
| Research prevalence estimate | None; five-report sample is feasibility-only |

## 5. Approval boundary and next sequence

1. **Complete — crosswalk technical gate.** The 737-row v12.1 exact-to-parent artifact is generated, independently inspected and hash-verified; the RECON validator checks accepted exact IDs, canonical names, explicit parents, vocabulary status and lifecycle flags. The current RECON v0.1/v0.2 and root synthetic suites passed in CI run #144: 198 successful test executions across the three suites. This is a working technical default, not a researcher protocol/schema freeze.
2. Resolve the two no-CyNE source-scope recommendations and the remaining evidence-scope, mapping-acceptance and prior-exposure choices. Keep researcher-owned decisions visibly pending until explicitly disposed.
3. **Complete — dataset-level permission gate.** The 5 November maintainer response supports local research annotation and derivative publication under the AnnoCTR CC BY-SA licence. Maintain attribution/ShareAlike, keep raw reports out of Git, and reopen only for a report-specific exception. Source-scope and researcher eligibility are separate.
4. Reconcile the working defaults against the exact protocol and schema originals if recovered; otherwise explicitly approve or revise RECON as a new schema version, never as v0.4.2.
5. Freeze protocol/schema/version/pass identity and hash the approved package before source-first annotation. An exposed human pass is not blind; projection requires explicit confirmation and a computed digest matching the selected human-approved source/partition registers.

**No formal annotation should begin solely because the 194 synthetic test executions pass.** These tests show that the proposed structure behaves as coded on synthetic fixtures; they do not establish semantic validity, protocol approval, source eligibility, human agreement, or research findings.


### Maintainer response disposition — 5 November 2026

The written response clears the dataset-level permission gate for the current five-report feasibility batch, but it does not answer scientific eligibility questions. The five rows have been updated to `local_research_use_status=PERMITTED` and `public_reuse_status=PERMITTED` in the sampling frame. Their `source_scope_eligibility` and `researcher_review_status` fields remain pending. This is a licence-based working disposition, not a legal opinion or a report-specific legal review. Any later evidence of an excluded contribution or rights-holder objection must be recorded and applied to the affected report only.


## 2B. Adopted source-scope decisions — 5 November 2026

The following two source-scope decisions were adopted under delegated project direction after the complete source texts were reviewed:

| Report ID | Disposition | Reason |
|---|---|---|
| `proofpoint_2021-05-24_compromised-cloud-accounts-cost-firms` | `INELIGIBLE` | Sponsored Ponemon survey-summary article; no report-local intrusion, actor operation, campaign or source-grounded cyber-activity sequence. |
| `quoteintelligence_2020-07-09_what-is-tiber-eu-and` | `INELIGIBLE` | TIBER-EU framework explainer; references to threats describe framework scenarios, not a report-local observed intrusion, operation or campaign. |

Both records remain in the 120-row historical manifest. The successor frame v1.0 records `source_scope_eligibility=INELIGIBLE`, a reason in `exclusion_reason`, and `researcher_review_status=DECISION_RECORDED`. The exclusion is based on declared source genre/scope, not absence of CyNE/ATT&CK annotations. The remaining 118 rows are not automatically eligible; independent source, completeness, local-use and review gates still apply.

## 2C. Protocol and schema version boundary

The new `CTI_Event_Instance_Annotation_Protocol_v0.5-draft.md` consolidates the adopted working rules and is a new draft built from the recovered v0.4 draft. It does not claim to recover missing Protocol v0.4.1. `CTI_Annotation_Schema_RECON_v0.1` remains a reconstruction, not the original v0.4.2 schema, and remains unapproved/unfrozen until its fields and validators are reconciled against Protocol v0.5 and approved as a new package.


## Technical remediation checkpoint — 5 November 2026

The repository remediation set:
- blocks selected-final projection when source-scope, local-use, or assessability decisions conflict across report partitions;
- requires a `CONSENSUS` row to point to at least two distinct, completed independent input partitions;
- requires an `ADJUDICATED_FINAL` row to have an `ADJUDICATED` log entry that resolves to a real record in the selected report/annotator/pass partition;
- brings the standalone RECON v0.1 adapter into line with the report-level conflict gate;
- distinguishes cycle components that merely contain multiple source edges from those that actually require multiple source edges;
- rejects self-event temporal edges in the legacy root projection function; and
- points the AnnoCTR source-hash utility and its regression test at the canonical frame v1.0.

These are structural/workflow safeguards. They do not create annotations, select reports, approve the protocol/schema, or establish empirical findings.


### RECON v0.3 explicit comparison-scope extension — 5 November 2026

The additive v0.3 draft adds an event-to-comparison-scope decision register and a separate lock tied to the v0.2 selected-analysis lock. Each ASSIGNED record is scoped to one resolved atomic event leaf and one report-local resolved non-report comparison scope in that event's resolved ancestry. It requires an evidence span and rationale. UNCERTAIN rows are retained but do not contribute to pair opportunity; a missing row is not interpreted as a negative assessment. A primary positive temporal relation or COMPATIBLE candidate-pair assessment must use a comparison scope explicitly assigned to both endpoints.

The v0.2 aggregator now supports three named rules: nearest common resolved non-report scope, shared resolved INCIDENT scope, and explicit shared event comparison-scope assignment. The v0.3 wrapper validates the assignment register and its lock before invoking the explicit-assignment rule. The explicit rule was a recommended candidate at the time the v0.3 extension was first drafted. Following the 8 November 2026 decision it is retained as a broader-context sensitivity, not the primary metric rule. All rate approval gates remain closed by default. Synthetic comparison is not evidence of semantic validity or empirical results.


### RECON v0.3 completeness and adjudication audit — 6 November 2026

The first v0.3 draft allowed a missing event-to-scope row to produce no pair opportunity even though it could mean either "not reviewed" or a negative decision. This is corrected in the draft validator: every resolved atomic event leaf must now have one explicit decision for each eligible RESOLVED non-report ancestor scope. The states are ASSIGNED, NOT_ASSIGNED and UNCERTAIN. A missing row is an incomplete review error; NOT_ASSIGNED is explicit and does not count as opportunity. The base RECON v0.1 bundle and the v0.2 selected-final register are validated before a v0.3 assignment lock is created or accepted.

A second boundary remains open: the v0.1 adjudication log cannot target the v0.3 assignment register. The v0.3 draft therefore accepts only UNREVIEWED decisions and its lock path permits SINGLE_ANNOTATOR_FINAL only. CONSENSUS and ADJUDICATED_FINAL selections are blocked until a dedicated v0.3 assignment-adjudication register, validation rules and protocol procedure are designed. This is an implementation limitation, not a researcher-approved decision to abandon independent annotation or adjudication.
