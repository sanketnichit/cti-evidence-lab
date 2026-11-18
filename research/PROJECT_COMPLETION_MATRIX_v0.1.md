# CTI Evidence Lab — research completion matrix

## Current quality checkpoint — 18 November 2026

Submission packaging does not close the research project. The [connected-sequence query study](QUERY_FIDELITY_STUDY_v0.1.md) adds a practical evaluation: identical acyclic technique graphs can have different supported occurrence-sequence answers. A four-way comparison separates diagonal retention from endpoint-compatible joins, with finite singleton and set-valued mapping experiments, full confusion matrices, explicit query denominators, a proof and inspectable counterexamples. It does not establish extraction quality, corpus prevalence or novelty of occurrence graphs. The next substantive gap is source-backed evaluation of these queries and review of interpretation errors; adding more schema gates or packaging alone does not address it.


## Completed exploratory submission — 18 November 2026

The [report](FEASIBILITY_REPORT_v0.1.md) and [submission guide](../docs/SUBMISSION_GUIDE.md) are the current entry points. The delivered scope includes the fixed five-report source review, 120 source identities, 33 pilot pointers, 22 critical-review passages, seven representation controls and 4,096 exhaustive finite graph cases. Local verification passes all 306 tests and 31 base-package checksums. A single reproduction command creates a source-text-free submission ZIP with commit and file hashes; optional PDF rendering is included. The useful standalone v0.4 independent-reviewer check from an old branch is preserved on main.

This completes the exploratory feasibility deliverable. The original formal empirical-study requirements below remain future work, not completed gold annotation or independent review. Historical dated entries are retained for traceability.


**Updated: 17 November 2026.**

## Purpose

The objective is a defensible, reproducible academic investigation of information retained or lost when distinct, evidence-supported attack-action occurrences and their temporal relations are projected to ATT&CK **distinct-technique-pair** graphs.

A functioning validator is not itself a finding. The study needs evidence that the report supports the event identities, temporal claims and mappings, as well as an explicit comparison target. Claims about novelty and population rates are conditional on real results.

## Coverage checklist

| Workstream | Current evidence | What remains before the project is finished |
|---|---|---|
| Motivation and question | `docs/RESEARCH_CHARTER.md`; narrow descriptive question defined | Ensure final title and abstract match actual measured outcomes |
| Literature and novelty | Related-work matrix, ChronoCTI baseline audit, research gap notes | Complete primary-source publication/schema comparison; distinguish existing event-level methods and competing projection definitions; no unsupported novelty claim |
| Data inventory and provenance | 400-report AnnoCTR inventory; archive hash; 120-row analysis frame | Preserve exact corpus revision; document local revalidation of source bytes for every annotated report |
| Rights and attribution | Dataset licence and maintainer clarification tracked; publisher-side qualifications recorded | Keep attribution/ShareAlike on adapted source material; exclude raw text and extended excerpts unless authorised; preserve report-specific exceptions |
| Sampling and leakage | Five donor strata, fixed SHA-256 prioritisation, genre decisions for two historical rows | Complete rank-one eligibility/source review independently of event yield; check family/syndication leakage before any expanded sample |
| Event identity and scope | RECON registers distinguish mentions, events, series, episodes and scopes | Human source-first decisions, including generic/capability cases, incident-boundary checks and unresolved states |
| Temporal evidence | Direct source/timestamp semantics, evidence support roles, tests | Human confirmation of actual claim entailment, event endpoints, timestamps and relation evidence for each accepted edge |
| ATT&CK mappings | Pinned Enterprise v12.1 crosswalk and A_120 parent-level rules | Accept/reject mappings for real source events; report exact-level sensitivity separately |
| Annotation and review | Protocol v0.5 draft; locks and validation; adjudicated-final currently fail-closed | Approve a concise pilot rule set; perform actual human source review; track time, disagreements and reviewer identity; use single-annotator pilot without implying IAA |
| Projection mathematics | Deterministic four-way edge classification; collision/cycle provenance; synthetic tests | Validate against fully reviewed source-backed rows; document self-loop and multimap representation alternatives |
| Baselines and controls | Reproduced ChronoCTI workbook analysis described in audit records; toy comparisons | Recheck primary baseline references; avoid comparing incomparable labels/corpora; run only fair baseline experiments |
| Statistical claims | Report-level denominators and conditional rates defined, gates implemented | No prevalence claim from five pilot reports; use new justified sampling if estimation is needed; report uncertainty clustered by report |
| Code and integration | GitHub Actions, test suites, schema checksums, adapters and lock validation | Run full CI on each final commit and tagged version; regression-test actual reviewed inputs; report known limitations |
| Reproducibility | Source/version hashes, deterministic seed, schema manifests and CI packaging | Freeze final protocol/code and data-access procedure, document exact commands and outputs, keep datasets/licence terms clear |
| Results and interpretation | No human-locked AnnoCTR results or real-report projections | Collect genuine results, sensitivity/error analysis and negative outcomes; decide whether research question remains feasible |
| Paper, report and presentation | Research charter and draft methodology exist | Write only after evidence; include methods, results with uncertainty, limitations, ethics/provenance, citations and artifact instructions |

## Focus for the next phase

An [exploratory feasibility report](FEASIBILITY_REPORT_v0.1.md), source-integrity audit, curated five-report dispositions, [critical second pass](feasibility/exploratory_review_v0.1/CRITICAL_REVIEW.md) and seven reproducible representation controls are now delivered. External review is unavailable, so the exploratory deliverable proceeds with explicit limits rather than waiting for reviewers. [Two separate review packets](reviewer_kit/COORDINATOR.md) remain optional future resources. The original completion conditions below still apply to the formal empirical study, which is a separate, unfinished milestone.

The next deliverable should be **a completed evidence-first pilot**, not another collection of schema extensions. The smallest adequate pilot uses the existing fixed five, a single approved event/scope/mapping/temporal protocol and one real recorded reviewer per report. The researcher can choose a single-annotator feasibility pass first; independent agreement then requires a second genuinely independent human reader.

An initial pilot need not use the `ADJUDICATED_FINAL` role. That role is still blocked because the record/field review-coverage policy is incomplete, and the v0.4 attack-action stratum also has no multi-annotator adjudication extension. These limitations do not justify inventing consensus or bypassing locks.

## Completion conditions

A completed research study must be able to reproduce all reported counts from verified source-backed annotations, define the technique representation precisely, separate the fixed feasibility sample from subsequent cohorts, report negative and unresolved outcomes, and clearly explain limitations. Good engineering test coverage is necessary but not sufficient. Until these conditions hold, the project remains a strong implementation and research-design prototype—not a finished empirical study.
