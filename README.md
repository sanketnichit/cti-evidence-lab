# CTI Evidence Lab

A student-led empirical study of event-instance identity and temporal information loss in ATT&CK-normalized cyber threat intelligence (CTI) representations.

**Status (3 November 2026):** AnnoCTR corpus screening and multi-vendor feasibility-frame preparation are complete; a draft reconstructed annotation schema and synthetic validator/projection pipeline are versioned separately. No human annotations or real-report projection results exist. No novel contribution is claimed as established.

## Provisional primary research question

> In CTI reports, how often do two distinct event instances mapped to the same MITRE ATT&CK technique have an explicitly supported temporal relation, and what event-level temporal information becomes unrepresentable when those occurrences are projected to a distinct-technique-pair representation that excludes diagonal pairs?

This is a candidate to test, not a validated research gap. ChronoCTI explicitly defines a distinct-technique-pair universe over 120 ATT&CK techniques, excluding same-technique diagonal pairs. General NLP already studies event mentions, event coreference, and temporal relation extraction. Our potential contribution is a CTI-specific empirical measurement of how often this exclusion matters in source reports, supported by human event-instance annotations and reproducible projection metrics.

## Research integrity

- Distinguish event mentions, event instances, event coreference, and ATT&CK taxonomy concepts.
- Do not infer physical chronology from narrative order alone.
- Do not treat an Attack Flow dependency edge as a temporal BEFORE relation.
- Keep `NO_TEMPORAL_CLAIM`, `UNRESOLVED`, and model `ABSTAIN` distinct.
- Every positive temporal edge must link to source evidence that supports the relation, not merely mention both endpoints.
- Preserve source offsets, report versions, dataset versions, ATT&CK release, model revisions, splits, and experiment configs.
- Do not redistribute raw reports, annotations, or model weights until their licences and underlying content rights are confirmed.
- Group report families, syndicated copies, and near-duplicates across train/test splits.
- Report coverage and errors together; abstention must not hide poor recall.
- Gold evaluation labels must be created and adjudicated by human annotators against the original source evidence; automated suggestions are not ground truth.
- The researcher is responsible for methodological decisions, annotations, experiments, interpretation, and conclusions.

## Repository layout

```text
docs/       research charter, audits, architecture, methodology, decisions, roadmap, project state
research/   related work, evidence ledger, protocols, sampling, schema reconstruction and metric contracts
src/        public v0.3-era projection and annotation-validation utilities
tests/      synthetic unit tests
examples/   synthetic examples only
scripts/    local data-screening utilities
data/raw/   local source corpus only; never commit raw reports or full source text
data/processed/annoctr_screening/  three allow-listed, text-free screening metadata files only
```

## Current phase

Validate the research question, legal data access, annotation feasibility, and fair baseline comparison before building a full pipeline or model. The current source of truth is `docs/PROJECT_STATE.md`, with the latest consistency review in `docs/audits/CTI_Evidence_Lab_Project_Wide_Consistency_Audit_v1.4.md` and open methodological choices in `research/metric_contract/CTI_Evidence_Lab_Researcher_Decision_Register_v0.1.md`. Earlier gap, roadmap, and pilot documents remain part of the project history.

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

Latest observed verification: [GitHub Actions run #26](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/41314970298) passed **28 synthetic unit tests** and the module-based toy demo. This validates synthetic code paths only; it is not evidence from real CTI reports.

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python -m examples.toy_projection_demo
```

The first report dry-run instructions are in `research/PILOT_REPORT_01_STARTER.md`. This repository contains no completed report-level gold annotations.

## AnnoCTR screening utility

After downloading the official AnnoCTR repository, inventory the full corpus locally:

```bash
python scripts/screen_annoctr.py \
  --root /path/to/anno-ctr-lrec-coling-2024/AnnoCTR/all \
  --output data/annoctr_screening.csv \
  --top-per-vendor 5
```

The scanner reads the official `splits.tsv` document-level manifest (120 GNE+CyNE reports in `train`/`dev`/`test`; 280 GNE-only reports in `ext`). It detects cybersecurity-specific annotation types in the full `linking/` export, while counting canonical ATT&CK technique links from `linking_mitre_only/`. It recognizes the QuoIntelligence filename alias and ignores context/negative-linking variants. It also reports the presence of both linking exports separately. Repeated mentions remain candidate locators, not event-instance labels. Synthetic tests are in `tests/test_annoctr_screening.py`.


## Latest project checkpoint — 3 November 2026

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
The raw AnnoCTR corpus remains local and is not included in this repository.

### Annotation schema reconstruction

`research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/` is a new
reconstruction based on the recovered Protocol v0.4 draft, its migration note, the
v0.4.2 conformance audit and the public v0.3 templates. It is **not** the missing
original `CTI_Annotation_Schema_v0.4.2-draft.zip`, and it is not approved or frozen
for formal annotation. The exact v0.4.1 protocol and original v0.4.2 ZIP were not
recovered. The package contains 12 blank registers, a field dictionary, controlled
vocabularies, a structural validator, a projection module, an annotation-to-projection
adapter, and 39 synthetic tests. None of these tests are results on real CTI reports.

### Current evidence boundary

- Five rank-1 reports remain candidates; researcher eligibility decisions are 0/5.
- Human-locked AnnoCTR annotations: 0.
- Real-report event projections: 0.
- Independent human agreement: not measured.
- Novelty: not established.
- The five-report design is a feasibility/protocol-debugging pilot, not a prevalence sample.

The 120-row sampling frame is versioned at `research/annoctr_sampling/AnnoCTR_Fresh_MultiVendor_Sample_Frame_v0.9.csv`. Its AI triage state is separate from the still-pending human source-scope, local research-use, and public-reuse decisions. See `docs/PROJECT_STATE.md`, the project-wide audit v1.4, and the researcher decision register for current status and open decisions. The original v0.3 public implementation is
left unchanged; the RECON package is kept isolated until the researcher approves the
protocol/schema migration.
