# CTI Evidence Lab

Research-first study of evidence-constrained temporal attack-graph reconstruction from cyber threat intelligence (CTI) reports.

**Status:** literature, dataset, and annotation-protocol audit. No model or novel contribution is claimed as completed.

## Working question

For temporal relations between ATT&CK-grounded event mentions in CTI reports, does relation-specific evidence supervision and explicit abstention improve temporal-edge reliability at useful coverage compared with an appropriate baseline?

This is a hypothesis, not an established research gap. Event-mention graphs and temporal relation extraction already exist in general NLP; ChronoCTI already addresses temporal CTI graphs; recent CTI work addresses evidence mining and graph relationships. The project must establish a defensible contribution through a systematic literature and data audit before implementation.

## Research integrity

- Separate report-local event instances from ATT&CK taxonomy concepts.
- Never infer chronology from narrative order alone in the primary evidence-supported setting.
- Keep `NO_TEMPORAL_CLAIM` distinct from model `ABSTAIN`.
- Every positive edge must link to report evidence that supports the relation, not merely mention each endpoint.
- Preserve source offsets, dataset versions, ATT&CK release, model revisions, splits, and experiment configs.
- No raw reports, annotations, or model weights are redistributed until their licences and underlying content rights are confirmed.
- Keep report families and duplicates grouped across train/test splits.
- Report coverage and error together; abstention must not hide poor recall.

## Repository layout

```text
docs/       research charter, audit, architecture, methodology, decisions, roadmap
research/   related-work matrix, evidence ledger, annotation protocol
src/        implementation (not started)
tests/      tests (not started)
data/       local data only; raw and processed files are git-ignored
notebooks/  exploratory analysis only
```

## Current phase

Validate the research question, legal data access, annotation feasibility, and fair baseline comparison before coding. See `docs/PROJECT_STATUS.md` and `docs/ROADMAP.md`.

## License

The repository's original software and documentation are under the MIT License. This does not grant rights to third-party CTI reports, datasets, papers, trademarks, or model weights referenced by the project.
