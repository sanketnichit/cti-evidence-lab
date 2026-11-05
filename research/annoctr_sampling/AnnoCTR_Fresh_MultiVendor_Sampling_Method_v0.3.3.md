# AnnoCTR fresh multi-vendor feasibility sample method v0.3.2

**Prepared:** 3 November 2026  
**Status:** Corrected feasibility-sampling rule; corpus screened; five rank-1 candidates reviewed by AI; no human eligibility decision or base report selection is locked. This version clarifies that the 112 link-positive count is an inventory statistic, not the sampling frame.

## Source frame and manifest

The official `AnnoCTR/all/splits.tsv` contains 400 unique report IDs. The 120 IDs assigned to `train`, `dev`, or `test` are the manifest-defined GNE+CyNE subset. The `ext` split contains 280 additional general-layer-only reports and is excluded from this ATT&CK-mapping sample frame.

| Donor | All 400 reports | GNE+CyNE frame |
|---|---:|---:|
| Intel471 | 34 | 30 |
| Lab52 / S2 Grupo | 28 | 23 |
| Proofpoint | 101 | 28 |
| QuoIntelligence | 14 | 12 |
| ZScaler | 223 | 27 |
| **Total** | **400** | **120** |

## Corpus-screening results (3 November 2026)

The uploaded official corpus archive passed ZIP integrity validation. All 400 manifest reports have base text, full linking, MITRE-only linking, and TimeML files; zero expected paired files are missing.

- 118/120 train/dev/test reports have cybersecurity-specific rows in the full linking export.
- 112/120 have at least one valid ATT&CK technique link from a canonical ATT&CK URL.
- Eight reports have no valid ATT&CK technique link in the MITRE-only export.
- The following two reports have no cyber-specific rows in full linking, empty MITRE-only exports, and no CyNE labels in the inspected `nc_tags`/`te_tags` fields: `proofpoint_2021-05-24_compromised-cloud-accounts-cost-firms` and `quoteintelligence_2020-07-09_what-is-tiber-eu-and`. Full source-text review indicates the first is a sponsored survey-summary article about cloud compromise costs, and the second is a general TIBER-EU framework explainer. They remain in the official 120-row inventory but are out-of-scope candidates under the study's CTI-report genre rule, pending the researcher's documented scope decision. Their absence of CyNE/ATT&CK links is corroborating inventory evidence, not the exclusion rule by itself. If the scope is broadened beyond CTI reports, they must be reconsidered under a revised frame.
- Across all 400 TimeML files: 3,324 `TIMEX3` tags; zero `EVENT`, `MAKEINSTANCE`, `TLINK`, and `SIGNAL` tags. TimeML therefore does not provide event-instance or event-to-event temporal relation gold for this project.
- Automated text comparison found no exact normalized-text duplicates and no report pairs with 5-word-shingle Jaccard similarity >= 0.50 across all 400 reports. This does not rule out paraphrase or external syndication.

See `data/processed/annoctr_screening/SCREENING_REPORT_v0.1.md`, `data/processed/annoctr_screening/AnnoCTR_Corpus_Screening_v0.1.csv`, and `data/processed/annoctr_screening/screening_summary.json` for detailed methods and report-level outputs.

## Base feasibility sample

Target: **five reports**, one per donor, selected only after eligibility review.

The tracked frame CSV keeps machine triage and human decisions in separate columns. `ai_triage_status` records the inventory/AI screening state only. `source_scope_eligibility` remains `PENDING`, while `local_research_use_status` and `public_reuse_status` remain `UNRESOLVED` until the researcher records those decisions independently. `researcher_review_status=NOT_REVIEWED` means no human decision has been locked for that row. These defaults are not approvals or exclusions.

1. Verify that the exact source text and corresponding MITRE-link file exist and are readable. The full scan found all paired files. A file may be present but contain no AnnoCTR ATT&CK links; non-empty link labels are not required for manual source annotation.
2. Record exact corpus path, raw source-text SHA-256, title, and publication date.
3. Verify canonical source URL, publication date, author/vendor attribution, and report identity.
4. Check provenance and rights evidence. The repository README licenses the corpus CC BY-SA 4.0; preserve attribution and indicate modifications. Do not assume the CTI Evidence Lab MIT licence relicenses third-party source material.
5. Check exact duplicates, near-duplicates, series/part relationships, syndication, and whether a report aggregates multiple operations or campaigns.
6. Record separate human decisions for `source_scope_eligibility` (`ELIGIBLE` / `INELIGIBLE` with reason) and `local_research_use_status`. Record `public_reuse_status` separately; unresolved public redistribution does not automatically make a report unusable for local annotation if a documented local-use basis exists. Only after the first two gates pass, choose the eligible report with the lowest `random_priority_sha256` in each donor stratum.
7. For substantive eligibility, confirm the source is within the declared CTI-report scope and can be annotated faithfully while separating mentions, activity units, tool capabilities, campaign/episode containers, and distinct event occurrences. Missing AnnoCTR CyNE/ATT&CK links alone do not prove that a source is not manually annotatable.
8. Do not use event enumerability, a pair opportunity, or a positive temporal relation as a per-report eligibility or replacement rule. A report with zero resolved event leaves or zero positive temporal relations remains a valid base-sample outcome if it passes the source/scope/research-use eligibility gate.
9. Separate local research-use suitability from public redistribution permission. Keep raw source text and extended spans local until the rights/reuse gate has been resolved.

**Deterministic priority seed:** `CTI-EVIDENCE-LAB-ANNOCTR-PILOT-2026-11-03-v1`  
Priority is the SHA-256 hex digest of `seed|report_id`; rank is ascending within donor. The seed and method must remain unchanged once eligibility review starts.

The five rank-1 candidates and all 120 frame records are stored in the version-controlled `AnnoCTR_Fresh_MultiVendor_Sample_Frame_v1.0.csv`. This CSV, rather than an untracked workbook, is the canonical repository record of donor strata, deterministic priority hashes, ranks, and current review states. The rank-1 entries are candidates only, not selected reports; source triage does not replace the researcher's separate source-scope, local-use, and public-reuse decisions.

If a donor stratum has no eligible report, record that outcome; do not silently substitute another donor. If the rank-1 report is ineligible because of source identity, CTI-report scope, provenance, or local research-use constraints, advance to the next hash-ranked report and record the reason. Never advance because the report lacks resolved event pairs, shared ATT&CK mappings, or positive temporal edges. If necessary, revise the pilot design before annotating.

## Additional challenge cases

No purposive stress report is selected or frozen in this version-controlled frame. Any later stress cases must be recorded in a separate, versioned report-level register with predeclared challenge criteria, and must not overlap the five base reports. In particular, the Intel471 Groove rank-1 candidate cannot be counted a second time as a stress case if it enters the base sample. A report that fails a predeclared source/scope/local-use gate cannot be retained as a stress case merely to preserve an interesting challenge.

No candidate is selected because it has a high repeated-technique count, multiple resolvable events, a shared-technique pair, or a positive temporal edge. Such counts only locate text worth reviewing; they do not establish event multiplicity or temporal edges.

## Rights notes

- The AnnoCTR repository README states the corpus is licensed CC BY-SA 4.0.
- The included repository `LICENSE.txt` is the CC BY-SA 4.0 legal code.
- Preserve attribution and indicate modifications; adapted material shared publicly must comply with CC BY-SA 4.0 or a compatible licence.
- Keep raw reports local during the pilot. Before releasing derived annotation rows containing source spans, review whether they constitute adapted material or a substantial extraction from the database.
- The project MIT licence does not relicense third-party reports or dataset content.

## Corrected separation of gates

Record these as different fields and decisions:

- `source_scope_eligibility`: whether the document is genuinely within the declared CTI-report scope and matches its source identity;
- `local_research_use_status`: whether the documented dataset/source basis permits the planned local annotation activity;
- `public_reuse_status`: whether raw text, spans, or adapted annotations can be redistributed (a separate rights decision);
- `event_pair_opportunity`: determined after annotation from distinct resolved atomic event leaves and the pinned mapping sets;
- `temporal_edge_outcome`: determined after full-report source annotation;
- `projection_outcome`: determined only after annotations are human-locked.

The prior `AnnoCTR_Sample_Adequacy_and_Fallback_Audit_v0.1` recommended an event-enumerability gate before replacing a rank-1 report. That gate is superseded as a base-sample selection rule because it conditions selection on a property the study intends to measure. Preserve the old audit for history; use its event-enumerability observations only as descriptive diagnostics.

## Limits

This is a **protocol-feasibility sample**, not a representative/probability sample for estimating population prevalence. Results from five base reports plus purposive stress cases must not be presented as vendor or corpus prevalence. A later prevalence study needs a separate, pre-specified probability-sampling design and sample-size justification.

Repeated technique mentions are not events. A capability description is not an execution. Source order or numbering is not chronology. Causality/dependency and shared campaign context are not automatically temporal BEFORE/AFTER. All event and temporal labels require report-local evidence.

## Version 0.3.1 correction note

- The base inventory remains all 120 manifest-defined GNE+CyNE reports, not only the 112 reports with existing valid ATT&CK links. The eight no-link reports remain eligible for source-first manual annotation if they pass the declared source/scope and local-use gates.
- The two no-CyNE reports remain in the official inventory but are source-genre exclusion candidates because full-text review identifies them as a sponsored survey-summary article and a general framework explainer. The researcher must record the scope decision; missing annotation links are not themselves grounds for exclusion.
- No rank-2 candidate may replace a rank-1 report because of event yield, same-technique pair opportunity, or positive temporal edges.

## Sources

- Official manifest: https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/main/AnnoCTR/all/splits.tsv
- AnnoCTR repository and corpus licence: https://github.com/boschresearch/anno-ctr-lrec-coling-2024
- AnnoCTR paper: https://aclanthology.org/2024.lrec-main.103/
- CC BY-SA 4.0 legal code: https://creativecommons.org/licenses/by-sa/4.0/
- CTI Evidence Lab screening implementation: https://github.com/sanketnichit/cti-evidence-lab/blob/main/scripts/screen_annoctr.py
- CTI Evidence Lab draft sample plan: https://github.com/sanketnichit/cti-evidence-lab/blob/main/research/PILOT_SAMPLING_PLAN_v0.1.md
- CTI Evidence Lab candidate content review: https://github.com/sanketnichit/cti-evidence-lab/blob/main/research/ANNOCTR_CANDIDATE_CONTENT_REVIEW_v0.2.md

## Provenance of this screening snapshot

Input archive SHA-256: `118549e9ce885559cd0c07a8de42b321892754cc2e4f07fea0230eaefe4cea35`. The raw corpus archive is intentionally not included in the CTI Evidence Lab working bundle. Only aggregate/report-level counts, text hashes, and source metadata fields are exported.


## Version 0.3.2 correction note

- The version-controlled CSV is the canonical 120-row frame artifact; no workbook is required to reproduce the donor counts or hash-priority ordering.
- The priority seed, SHA-256 hash formula, within-vendor ranks, five rank-1 candidate IDs, and 120-report frame are unchanged.
- The Intel471 Groove rank-1 record remains a base candidate only. No sample selection, human eligibility decision, local-use permission, or public-reuse decision is implied by this correction.