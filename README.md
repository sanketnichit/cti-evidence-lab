# CTI Evidence Lab

A student-led empirical study of event-instance identity and temporal information loss in ATT&CK-normalized cyber threat intelligence (CTI) representations.

**Status (8 November 2026):** AnnoCTR screening and the 120-report historical frame are prepared. The dataset maintainer has clarified that source-material use and publication of derivatives are permitted under the corpus CC BY-SA licence, subject to attribution and ShareAlike. Two non-CTI source documents are excluded from the declared study scope but retained in the inventory. The five-report pre-annotation draft contains 18 proposed activity units, nine scope candidates, 26 pinned-source anchors, and separate mapping/temporal triage; these remain unreviewed proposals, not human annotations or empirical results. The adopted primary analytical stratum is incident-linked attack-action occurrences, with communications, analyst observations and generic capabilities retained separately. RECON v0.4 now supplies the logical activity_stratum field through a one-to-one companion register, with a validator, selected-analysis-bound stratum lock and attack-action-only projection/pair-opportunity filter; 12 synthetic tests pass. The extension remains a draft and formal annotation is still blocked pending review and the remaining protocol decisions. No novel contribution is claimed as established.

## Provisional primary research question

> Across a transparently sampled set of CTI reports, how often does a report explicitly support a temporal relation between two distinct, resolved activity occurrences that share one or more ATT&CK technique mappings, and what occurrence identity or temporal information is retained, partially represented, or lost when those occurrences are projected to a representation that permits only distinct technique pairs?

This is a candidate report-level estimand, not a validated research gap. ChronoCTI uses a 120-technique pair universe that excludes same-technique diagonal pairs, and its paper identifies Enterprise ATT&CK v12.1. Existing work already covers CTI event extraction, temporal attack graphs, ATT&CK mapping and technique-pair temporal prediction. The possible contribution is narrower: human source-evidenced measurement of what occurrence-level relations are supported in a named CTI sample and what a specified distinct-technique-pair projection retains, conflates or omits. We have not run ChronoCTI's learned model on AnnoCTR and must not describe our projection as its measured error rate.

## Research integrity

- Distinguish event mentions, event instances, event coreference, and ATT&CK taxonomy concepts.
- Do not infer physical chronology from narrative order alone.
- Do not treat an Attack Flow dependency edge as a temporal BEFORE relation.
- Keep `NO_TEMPORAL_CLAIM`, `UNRESOLVED`, and model `ABSTAIN` distinct.
- Every positive temporal edge must link to source evidence that supports the relation, not merely mention both endpoints.
- Preserve source offsets, report versions, dataset versions, ATT&CK release, model revisions, splits, and experiment configs.
- Keep raw AnnoCTR reports and extended verbatim excerpts out of Git. Adapted annotation material derived from AnnoCTR must retain source attribution and be published under the same CC BY-SA licence; the repository MIT licence applies to project software, not source reports or adapted annotation data.
- Group report families, syndicated copies, and near-duplicates across train/test splits.
- Report coverage and errors together; abstention must not hide poor recall.
- Gold evaluation labels must be created and adjudicated by human annotators against the original source evidence; automated suggestions are not ground truth.
- The researcher is responsible for methodological decisions, annotations, experiments, interpretation, and conclusions.

## Repository layout

```text
docs/       research charter, audits, architecture, methodology, decisions, roadmap, project state
research/   related work, evidence ledger, protocols, sampling, schema reconstruction, metric contracts and annotation drafts
src/        legacy v0.3 projection and annotation-validation utilities (synthetic checks only)
tests/      synthetic unit tests
examples/   synthetic examples only
scripts/    local data-screening utilities
data/raw/   local source corpus only; never commit raw reports or full source text
data/processed/annoctr_screening/  three allow-listed, text-free screening metadata files only
```

## Current phase

With the dataset-maintainer permission clarification recorded, a source-first pre-annotation pass has been prepared for the five fixed rank-one candidates. The adopted primary universe is incident-linked attack-action occurrences; auxiliary communications, analyst observations and generic capabilities remain separately visible. Individual report eligibility, event boundaries, scope and mapping decisions remain unapproved. RECON v0.4 now enforces the boundary through a required one-to-one activity_unit_strata.csv companion register, complete-evidence validator, lock, and primary projection/pair-opportunity filter. The extension leaves v0.1 unchanged and remains a draft. Formal annotation remains blocked pending review of v0.4 and resolution of the remaining scope/semantic decisions before a complete protocol/schema freeze. The current source of truth is `docs/PROJECT_STATE.md`; RECON v0.3 compares the legacy, incident-bounded and explicit-assignment scope-pair rules, but none is researcher-approved. See the latest consistency review in `docs/audits/CTI_Evidence_Lab_Project_Wide_Consistency_Audit_v1.4.md` and the researcher decision register in `research/metric_contract/CTI_Evidence_Lab_Researcher_Decision_Register_v0.2.md`. Earlier gap, roadmap, and pilot documents remain part of the project history.

## Citation and author name

The machine-readable author fields in `CITATION.cff` intentionally store the given name and family name separately: given name **Sanket**, family name **Nichit**. GitHub's generated citation may render a conventional abbreviated form such as **Nichit, S.**; that is a citation-style choice, not a different author name.

For a human-readable reference with the full name, use:

> **Sanket Nichit** (2026). *CTI Evidence Lab* (Version 0.1.0) [Computer software]. https://github.com/sanketnichit/cti-evidence-lab

For BibTeX, use the full-name-preserving entry in `CITATION.bib`.

## License

The repository's original software and documentation are under the MIT License. This does not grant rights to third-party CTI reports, datasets, papers, trademarks, or model weights referenced by the project.


## Small prototype

The current code is deliberately limited to synthetic and annotation-quality checks:
- `src/projection_metrics.py`: project event-instance relation edges to ATT&CK technique pairs and calculate coverage, mapping collisions, diagonal omissions and cycle diagnostics.
- `src/annotation_validation.py`: validate CSV annotation offsets, event references and relation evidence.
- `tests/`: synthetic tests only; do not interpret them as results on CTI reports.

The projection uses a Cartesian product when an event endpoint has multiple ATT&CK mappings. This preserves all mapped pair combinations, but it can also create a technique-level cycle from a **single** source event relation. Cycle diagnostics therefore retain source-edge provenance and distinguish single-edge mapping fan-out from cycles requiring multiple source event relations.

Latest executable-code CI verification on 8 November 2026: GitHub Actions run [#183](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/42430969469) passed on documentation head `31793084ae028594035376dcb01adf0f1c695ad9`, with executable sources unchanged from code commit `fcf0bb11009e45cc861eafb457373ee8f00c47c6`. It executed **60 root tests**, **73 RECON v0.1 tests**, **78 RECON v0.2 tests**, and **15 RECON v0.3 tests** — **226 successful synthetic test executions**. The run includes source-text integrity, fail-closed relation/mapping validation, distinct-pair projection diagnostics, all five Mobile ATT&CK non-primary retention cases, complete event-to-scope review, v0.3 assignment locks and role guards, blank-register validation, v0.1 package checksums, blank-bundle validators, scope-numerator/denominator parity regressions and the projection demo. These checks are synthetic/code-integrity checks only, not real-report findings.

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python -m examples.toy_projection_demo
```

The structured five-report pre-annotation draft is in `research/annotation_drafts/AnnoCTR_Pilot_v0.1/`; the earlier first-report dry-run starter remains in `research/PILOT_REPORT_01_STARTER.md`. This repository contains no completed report-level human annotations or gold partitions.

## AnnoCTR screening utility

After downloading the official AnnoCTR repository, inventory the full corpus locally:

```bash
python scripts/screen_annoctr.py \
  --root /path/to/anno-ctr-lrec-coling-2024/AnnoCTR/all \
  --output data/annoctr_screening.csv \
  --top-per-vendor 5
```

The scanner reads the official `splits.tsv` document-level manifest (120 GNE+CyNE reports in `train`/`dev`/`test`; 280 GNE-only reports in `ext`). It detects cybersecurity-specific annotation types in the full `linking/` export, while counting canonical ATT&CK technique links from `linking_mitre_only/`. It recognizes the QuoIntelligence filename alias and ignores context/negative-linking variants. It also reports the presence of both linking exports separately. Repeated mentions remain candidate locators, not event-instance labels. Synthetic tests are in `tests/test_annoctr_screening.py`.


## Dataset, sampling and schema checkpoint — 4 November 2026

The official AnnoCTR archive has been screened locally. Its SHA-256 is recorded in
`data/processed/annoctr_screening/screening_summary.json`. The inventory covers all
400 manifest reports; the official train/dev/test GNE+CyNE frame contains 120 reports
(30 Intel471, 23 Lab52/S2 Grupo, 28 Proofpoint, 12 QuoIntelligence and 27 ZScaler).
All expected text/linking/TimeML paired files are present. 118/120 GNE+CyNE reports
have cyber-specific rows in the full linking export; 112/120 have a valid canonical
ATT&CK technique link. These link counts are descriptive inventory only and do not
filter the 120-report frame. The two no-CyNE-row documents remain in the inventory
pending a researcher content-scope decision.

The tracked screening CSV contains report-level metadata only (IDs, split/vendor,
counts, flags and hashes); it contains no report text or long source excerpts. The
`.gitignore` allow-list names only this CSV, `SCREENING_REPORT_v0.1.md`, and
`screening_summary.json`; other files under `data/processed/` remain ignored.
The raw AnnoCTR corpus is not included in this repository. The source-hash convention is strict UTF-8, optional leading BOM removal, preserved CRLF/LF, no Unicode normalization, and zero-based end-exclusive Python code-point offsets. On 4 November 2026, all 120 frame `source_text_sha256` values were independently recomputed from the official AnnoCTR repository text files at pinned commit `d510b6949e1938d47c93a43eedd562dc538439dc`; all 120 matched. This verifies the hashes against that source revision, not the separate downloaded-archive SHA-256. To reproduce from a local corpus, use `python scripts/hash_annoctr_sources.py --corpus-root /path/to/AnnoCTR/all` (add `--write` only after reviewing any mismatches). Raw report text remains excluded from Git.

### Annotation schema reconstruction

`research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/` is a new
reconstruction based on the recovered Protocol v0.4 draft, its migration note, the
v0.4.2 conformance audit and the public v0.3 templates. It is **not** the missing
original `CTI_Annotation_Schema_v0.4.2-draft.zip`, and it is not approved or frozen
for formal annotation. The exact v0.4.1 protocol and original v0.4.2 ZIP were not
recovered. The package contains 12 blank registers, a field dictionary, controlled
vocabularies, a structural validator, a projection module, an annotation-to-projection
adapter, and 69 synthetic tests (41 validator, 16 projection, 12 adapter). None of these tests are results on real CTI reports.

### Current evidence boundary

- Five rank-1 reports remain candidates; researcher eligibility decisions are 0/5.
- Human-locked AnnoCTR annotations: 0.
- Real-report event projections: 0.
- Independent human agreement: not measured.
- Novelty: not established.
- The five-report design is a feasibility/protocol-debugging pilot, not a prevalence sample.

The 120-row sampling frame is versioned at `research/annoctr_sampling/AnnoCTR_Fresh_MultiVendor_Sample_Frame_v1.0.csv`. Automated triage and prior exposure are recorded separately from human source-scope, local research-use and public-reuse decisions. The five candidates have not received human eligibility approval. See `docs/PROJECT_STATE.md`, the project-wide audit v1.4 and the researcher decision register for current status. The RECON package remains a reconstruction, not the missing original v0.4.2 schema, and has not been approved for formal annotation.


## AnnoCTR source use and derivative data

The AnnoCTR dataset maintainer replied on 5 November 2026 that source-material licences had been checked and permit redistribution under the dataset licence, and that researchers may add annotations/change reports and publish derivative works under the same CC BY-SA licence. This is a qualified maintainer clarification, not legal advice; it did not enumerate report-level exceptions. Any adapted annotation material must retain attribution and ShareAlike. The MIT licence in this repository applies to the project's original software/documentation only; it does not relicense source reports or derivative annotation datasets. Raw AnnoCTR reports and extended verbatim excerpts are not committed. See `research/rights/AnnoCTR_Research_Use_Permission_Clarification_v0.1.md`.


## Sampling and annotation protocol update — 5 November 2026

Two no-CyNE reports—a sponsored Ponemon survey summary and a TIBER-EU framework explainer—have been dispositioned INELIGIBLE for the declared CTI-report scope based on their source content. Both remain in the historical 120-report inventory; their absence of CyNE/ATT&CK annotations was not the exclusion basis. The current text-free frame is `research/annoctr_sampling/AnnoCTR_Fresh_MultiVendor_Sample_Frame_v1.0.csv`, with the updated method in `research/annoctr_sampling/AnnoCTR_Fresh_MultiVendor_Sampling_Method_v0.3.3.md`.

The annotation working rules are consolidated in `research/protocol/CTI_Event_Instance_Annotation_Protocol_v0.5-draft.md` and `research/metric_contract/CTI_Evidence_Lab_Researcher_Decision_Register_v0.2.md`. These remain drafts pending reconciliation with the reconstructed register schema. The five rank-one reports remain candidates, not selected reports; human-locked annotations remain at zero.
