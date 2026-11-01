# CTI Evidence Lab

A student-led, research-first study of event-instance granularity and temporal information in cyber threat intelligence (CTI) representations.

**Status:** Research feasibility and annotation pilot setup. Toy projection/validation prototypes exist; no human annotations or empirical results yet. No novel contribution is claimed as established.

## Provisional primary research question

> In CTI reports containing multiple distinct occurrences of the same MITRE ATT&CK technique, what event-instance identity and explicitly supported temporal distinctions are lost, conflated, or made ambiguous when the report is reduced to a report-level technique-node or technique-pair representation?

This is a candidate to test, not a validated research gap. ChronoCTI already predicts temporal relations between ATT&CK technique pairs. General NLP already studies event mentions, event coreference, and temporal relation extraction. Our potential contribution is a CTI-specific empirical analysis of representation granularity, supported by human annotations and a reproducible projection/evaluation protocol.

## Conditional secondary question

If the annotation pilot is feasible:

> Can evidence-linked event-instance relation extraction improve temporal-edge reliability at a useful level of coverage compared with appropriate technique-pair and text-based baselines?

This secondary model question is not part of the primary experiment until data availability, annotation reliability, and sample size are established.

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
- Never use AI-generated annotations as gold ground truth. Human annotations and adjudication establish the evaluation labels.
- Maintain a lightweight AI assistance log; the student researcher owns methodological decisions, annotations, experiments, interpretation, and conclusions.

## Repository layout

```text
docs/       research charter, audit, architecture, methodology, decisions, roadmap
research/   related-work matrix, evidence ledger, annotation protocol
src/        pure-Python toy projection and annotation-validation utilities
tests/      synthetic unit tests (execution status pending verification)
data/       local data only; raw and processed files are git-ignored
notebooks/  exploratory analysis only
```

## Current phase

Validate the research question, legal data access, annotation feasibility, and fair baseline comparison before building a full pipeline or model. The current audit is in `docs/RESEARCH_GAP_AUDIT_2026-11-01.md`; see also `docs/PROJECT_STATUS.md`, `docs/ROADMAP.md`, `research/PILOT_REPORT_01_STARTER.md`, and `research/templates/README.md`.

## Citation and author name

The machine-readable author fields in `CITATION.cff` intentionally store the given name and family name separately: given name **Sanket**, family name **Nichit**. GitHub's generated citation may render a conventional abbreviated form such as **Nichit, S.**; that is a citation-style choice, not a different author name.

For a human-readable reference with the full name, use:

> **Sanket Nichit** (2026). *CTI Evidence Lab* (Version 0.1.0) [Computer software]. https://github.com/sanketnichit/cti-evidence-lab

For BibTeX, use the full-name-preserving entry in `CITATION.bib`.

## License

The repository's original software and documentation are under the MIT License. This does not grant rights to third-party CTI reports, datasets, papers, trademarks, or model weights referenced by the project.


## Small prototype

The current code is deliberately limited to synthetic and annotation-quality checks:
- `src/projection_metrics.py`: project event-instance relation edges to ATT&CK technique pairs and calculate candidate collision/coverage/cycle summaries.
- `src/annotation_validation.py`: validate CSV annotation offsets, event references and relation evidence.
- `tests/`: synthetic tests; do not interpret them as results on CTI reports.

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python examples/toy_projection_demo.py
```

The first human dry-run candidate and instructions are in `research/PILOT_REPORT_01_STARTER.md`. No AI-generated labels are committed as gold annotations.
