# CTI Evidence Lab

[![DOI: 10.5281/zenodo.24533052](https://zenodo.org/badge/DOI/10.5281/zenodo.24533052.svg)](https://doi.org/10.5281/zenodo.24533052)

**Occurrence identity and temporal information loss in cyber threat intelligence graphs.**

CTI Evidence Lab studies how replacing individual attack occurrences with ATT&CK technique nodes changes temporal relations and sequence-query answers. It combines controlled graph experiments, source-bound exploratory cases, and evidence-validation software.

[Methods preprint v0.1](https://doi.org/10.5281/zenodo.24533052) · [GitHub release](https://github.com/sanketnichit/cti-evidence-lab/releases/tag/preprint-v0.1) · [Reproduction and data access](docs/REPRODUCIBILITY.md#methods-preprint-v01)

## Sequence investigator

Ask whether three techniques form one connected occurrence sequence. Inspect the supporting actions, locate incompatible joins in a technique graph, compare interpretation profiles and export a recomputable answer record.

```sh
python scripts/build_investigation.py
```

Open `outputs/investigation/index.html` in a browser. The artifact covers four DFIR reports and two CISA advisories. Five cases offer three-technique queries and verifiable JSON exports. The unassessed advisory shows the retained evidence and exclusions. Matching publisher HTML can be opened locally for DFIR passages. CISA evidence uses PDF page locators. [Workflow and evaluation](research/INVESTIGATION_WORKFLOW_v0.1.md)

For unresolved mappings, the CLI can also [compare explicit candidate bounds](research/experiments/bounded_mapping_v0.1/README.md). Exports preserve the unrestricted answer and show which assumptions exclude a possible path.

## Research question

Can a technique-level path establish a connected sequence of source-supported attack occurrences?

Two occurrence graphs can have identical technique projections while supporting different sequence answers. The example below has no projected cycle: the ambiguity comes from merging distinct occurrences with the same technique label.

![Identical technique projections with different occurrence-sequence answers](research/experiments/query_fidelity_v0.1/sequence_counterexample.svg)

## Findings and evidence

- **Edge loss:** a relation between two occurrences mapped exclusively to the same technique disappears when diagonal technique pairs are excluded.
- **Sequence ambiguity:** retaining self-loops does not recover occurrence identity. Endpoint-compatible joins and diagonal retention address different query failures.
- **Source sensitivity:** the exploratory RDP case separates attempted actions, confirmed successes and withheld mappings, producing different eligible graphs.

The controlled experiments enumerate 5,184 singleton-mapping graphs and 4,096 set-valued-mapping graphs. Four DFIR cases and two CISA advisories show agreement, unsupported joins and unresolved projected answers under the recorded interpretations. The fifteen AnnoCTR readings assess source suitability in three separate groups. The [manuscript](research/FEASIBILITY_REPORT_v0.1.md) distinguishes these results from independent annotation and prevalence claims.

## Research artifacts

The [analyst pilot](research/ANALYST_PILOT_v0.1.md) provides four ready-to-run packets for comparing what reviewers can verify from technique pairs and individual occurrences.

| Artifact | Contents |
|---|---|
| [Five-publisher evaluation](research/experiments/external_sequence_evaluation_v0.1/README.md) | Frozen selection, conditional procedures and no-advantage results |
| [Research manuscript](research/FEASIBILITY_REPORT_v0.1.md) | Formal result, experiments, source interpretations, runtime and limitations |
| [DFIR holdout](research/experiments/incident_holdout_v0.1/README.md) and [CISA extension](research/experiments/cisa_incident_extension_v0.1/README.md) | Selected incident narratives, source bindings, and query comparisons |
| [Microsoft series prefix](research/experiments/microsoft_incident_series_v0.1/README.md) | Fixed two-report sample, limits of narrative prose and one publisher link mismatch |
| [Query-fidelity study](research/QUERY_FIDELITY_STUDY_v0.1.md) | Counterexample, proof, four-way comparison and full confusion matrices |
| [RDP case study](research/case_studies/dfir_rdp_v0.1/README.md) | Source-bound occurrence interpretation and outcome/mapping sensitivities |
| [RDP sequence extension](research/case_studies/dfir_rdp_sequence_v0.2/README.md) | Four actions from the same intrusion; conditional sequence results and unresolved mapping coverage |
| [Domain-controller sequence](research/case_studies/dfir_html_smuggling_v0.1/README.md) | Second intrusion; successful core query, join error and exact-technique sensitivity |
| [AnnoCTR feasibility review](research/feasibility/exploratory_review_v0.1/README.md) | Five fixed reports, source bindings and unresolved judgments |
| [Fixed source extension](research/feasibility/rank_two_extension_v0.1/README.md) | Five additional reports selected before review; ordering, execution context and coverage |
| [Research index](research/README.md) | Data access, protocols, sampling and provenance records |
| [Study status](docs/PROJECT_STATE.md) | Current evidence and remaining research limitations |

## Reproduction

Python 3.11+ and Git are required. From a clean checkout:

```sh
python scripts/reproduce_study.py
```

This runs the test suites, regenerates experiments and case sensitivities, and produces a versioned artifact archive with file hashes. Source rechecks require local source copies; PDF rendering optionally requires ReportLab. Commands, data-access details and artifact formats are documented in [Reproducibility](docs/REPRODUCIBILITY.md).

[Continuous integration](https://github.com/sanketnichit/cti-evidence-lab/actions/workflows/projection-tests.yml) verifies the software, schema checksums and blank annotation bundles. These checks do not validate the meaning of source interpretations.

## Repository structure

```text
research/   studies, results, source records, protocols and schema reconstruction
src/        occurrence queries and projection/validation utilities
examples/   controlled experiments and historical illustrations
scripts/    source audits, case analysis and reproduction
tests/     regression and finite-oracle checks
docs/       methodology, architecture, status and reproducibility
```

## Citation and license

Nichit, S. (2026). *When technique graphs lose incident sequence evidence* (v0.1). Zenodo. [Version DOI 10.5281/zenodo.24533052](https://doi.org/10.5281/zenodo.24533052)

Use the version DOI when citing v0.1. The concept DOI identifies the preprint across versions. Citation files cover both the paper and the software. [All versions](https://doi.org/10.5281/zenodo.24533051) · [CITATION.cff](CITATION.cff) · [CITATION.bib](CITATION.bib)

Original project software and documentation are [MIT licensed](LICENSE). Source reports retain their own rights. Adapted AnnoCTR material retains CC BY-SA 4.0 attribution and terms; raw reports are not distributed in this repository.
