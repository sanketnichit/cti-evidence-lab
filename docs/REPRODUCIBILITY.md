# Reproducibility

The experiments require Python 3.11 or later and Git. Analysis and validation use the Python standard library. PDF rendering optionally requires ReportLab.

## Methods preprint v0.1

The [preprint release](https://github.com/sanketnichit/cti-evidence-lab/releases/tag/preprint-v0.1) distributes the paper and artifact from the tagged source revision. From a clone with the tag available, run:

```sh
git switch --detach preprint-v0.1
python -m pip install reportlab==4.4.9
python scripts/reproduce_study.py --pdf --output-dir outputs/preprint-v0.1
```

The PDF footer identifies the source commit. Repository links inside the PDF use that commit. The output archive includes the manuscript, results, offline investigator, and a SHA-256 manifest. The release records the available source rechecks described below. The preprint addresses representation fidelity, with source interpretation and analyst efficacy left as separate empirical questions.

Use the version DOI to cite this exact paper and archive. The concept DOI points to the preprint's version series. The PDF, reproduction ZIP and checksum file on Zenodo match the corresponding files on the tagged GitHub release by SHA-256. [Zenodo record](https://zenodo.org/records/24533052) · [Version DOI](https://doi.org/10.5281/zenodo.24533052) · [Concept DOI](https://doi.org/10.5281/zenodo.24533051)

## Complete reproduction

From a clean checkout:

```sh
python scripts/reproduce_study.py
```

The command runs five test suites, verifies 31 immutable RECON v0.1 package checksums, regenerates representation controls and query-fidelity experiments, and evaluates the recorded exploratory RDP case and its sequence extension. It records the Git commit, runtime, source-verification modes and SHA-256 file manifest. A dirty tree is rejected unless `--allow-dirty` is explicitly supplied; such runs are marked as development builds.

The output archive is `outputs/submission/CTI_Evidence_Lab_Submission.zip`. The filename is retained for compatibility; this is a reproducible artifact snapshot, not a publication or peer-review status. It contains repository files under `cti-evidence-lab/`, generated results under `generated/`, and `manifest.json`. Git history, raw source reports and private review packets are excluded.

## Source verification

Without source paths, reproduction uses the recorded audits and reports `RECORDED_AUDIT_ONLY`. Fresh checks require local copies:

```sh
python scripts/reproduce_study.py --corpus-root /path/to/AnnoCTR/all --recover-crlf
python scripts/audit_rdp_case.py --source-html /path/to/saved/publisher.html
```

The AnnoCTR audit checks 120 source identities, 33 pilot pointers and 22 critical-review passages. `--recover-crlf` accepts line-ending recovery only when it exactly matches the previously recorded source hash; original files are unchanged. The separate RDP audit verifies three passages against its publisher-paragraph snapshot convention. Its sequence extension verifies seven bindings, including those original three, against the same snapshot. All checks can be included in one reproduction run by adding `--rdp-source-html /path/to/saved/publisher.html`.

Hash equality verifies source identity and evidence locations, not semantic correctness. Source acquisition and attribution are documented in the [research index](../research/README.md).

The fixed rank-two extension adds five source readings and 22 passage bindings. With `--corpus-root`, reproduction rechecks those bindings against the same corpus; without it, the recorded audit must match the exact selection and review records. `python scripts/audit_rank_two_review.py --corpus-root /path/to/AnnoCTR/all --recover-crlf` runs that audit separately.

The second external intrusion has a separate publisher snapshot and 13 passage bindings. Supply it with `--incident-source-html /path/to/saved/source.html`; this option is distinct from `--rdp-source-html`, which verifies the original intrusion and its same-case extension.

### Recheck all available inputs in one run

Use the `all/` directory from the pinned Bosch Research AnnoCTR revision. The audit checks individual report text against the frozen frame hashes. Publisher URLs and snapshot identities are documented in the case records. [Pinned AnnoCTR revision](https://github.com/boschresearch/anno-ctr-lrec-coling-2024/tree/d510b6949e1938d47c93a43eedd562dc538439dc), [DFIR holdout](../research/experiments/incident_holdout_v0.1/README.md), [CISA advisories](../research/experiments/cisa_incident_extension_v0.1/README.md), [Microsoft reports](../research/experiments/microsoft_incident_series_v0.1/README.md)

```sh
python -m pip install pypdf==6.21.4
python scripts/reproduce_study.py \
  --corpus-root /path/to/AnnoCTR/all --recover-crlf \
  --rdp-source-html /path/to/rdp.html \
  --incident-source-html /path/to/domain-controller.html \
  --holdout-source-directory /path/to/dfir-holdout \
  --cisa-pdf-directory /path/to/cisa \
  --microsoft-pdf-directory /path/to/microsoft \
  --attack-taxonomy /path/to/enterprise-attack-12.1.json
```

The DFIR holdout directory uses `21520.html` and `22587.html`. The CISA directory uses `AA24-046A.pdf` and `AA25-266A.pdf`. The Microsoft directory uses `report-1.pdf` and `excluded-report-4.pdf`, whose cover documents the link mismatch for installment 2. The taxonomy argument rechecks the discovery and execution parent lists against the pinned STIX file.

Each source argument is optional. The archive's `validation.json` records the verification mode for each input group. If a provided file fails its integrity check, the run fails. The archive records source locators and audit results without including the downloaded files.

## Individual analyses

```sh
python -m examples.representation_controls
python -m examples.exhaustive_projection_checks
python -m examples.query_fidelity_benchmark
python scripts/analyze_rdp_case.py
python scripts/analyze_sequence_case.py
python scripts/analyze_incident_sequences.py
python scripts/audit_rank_two_review.py
```

The original conditional RDP illustration remains a historical method-development example. The source-bound case is analyzed by `analyze_rdp_case.py`.

## Generated artifacts

| Artifact | Contents |
|---|---|
| `representation_controls.json` / `.md` | Seven controlled representation comparisons |
| `finite_checks.json` | Edge-state and cycle-oracle checks over 4,096 graphs |
| `query_fidelity.json` / `.md` | Four representations, full confusion matrices, query strata and counterexamples |
| `rdp_case_results.json` | Outcome and mapping sensitivities for the separate exploratory case |
| `rdp_source_integrity.json` | Publisher snapshot and passage-binding verification |
| `sequence_case_results.json` | Mapping coverage and conditional sequence comparison for the same intrusion |
| `sequence_source_integrity.json` | Seven passage bindings against the same publisher snapshot |
| `incident_sequence_results.json` | Core, extended, exact-technique and withheld-mapping profiles for the second intrusion |
| `incident_source_integrity.json` | Thirteen bindings against the second publisher snapshot |
| `investigation_checks.json` | Finite mapping-completion oracle and case-query coverage |
| `sequence_investigator.html` | Portable offline query inspector with evidence locators and answer export |
| `exploratory_review.json` | Recorded five-report feasibility judgments |
| `rank_two_review.json` | Complete five-report extension coverage and unassessed query status |
| `rank_two_source_integrity.json` | Source hashes and 22 extension passage bindings |
| `source_integrity.json` | AnnoCTR source and evidence-pointer audit |
| `validation.json` | Suite results, commit, runtime and verification modes |
| `manifest.json` | SHA-256 for every packaged file except the manifest itself |

The archive contains no `.git` directory. Reproduction from the identified revision requires cloning the repository and checking out the manifest's commit.

`python scripts/build_investigation.py` also builds a standalone inspector at `outputs/investigation/index.html`. Its embedded answers are generated by the same Python engine as the CLI, rather than a separate browser implementation. Export verification uses `python scripts/investigate_sequence.py --verify /path/to/sequence-answer.json`. This compares against current case records, not a digital signature or independent source interpretation.

## Report rendering

```sh
python -m pip install reportlab
python scripts/build_report_pdf.py
```

`--pdf` on the complete reproduction command includes the rendered manuscript in the archive. `scripts/build_query_figure.py` generates the vector counterexample figure. The archive includes recomputed `incident_holdout_results.json`, `cisa_extension_results.json` and `microsoft_series_results.json`. The main reproduction checks those results against the committed records. To verify paragraph or page hashes against saved publisher copies, use the optional source checks for [DFIR](../research/experiments/incident_holdout_v0.1/README.md), [CISA](../research/experiments/cisa_incident_extension_v0.1/README.md) and [Microsoft](../research/experiments/microsoft_incident_series_v0.1/README.md).

## Continuous integration

[GitHub Actions](https://github.com/sanketnichit/cti-evidence-lab/actions/workflows/projection-tests.yml) runs the root and RECON v0.1–v0.4 suites, verifies base-package checksums, validates blank schema bundles and packages the tested source revision. Software checks do not establish the accuracy of source interpretations or independent annotation agreement.

## Fixed five-publisher comparison

`python scripts/evaluate_external_sequences.py` recomputes the committed rank-three results without source files. Add `--corpus-root /path/to/AnnoCTR/all --recover-crlf` to verify all five texts and 17 evidence bindings. Full reproduction includes `external_sequence_results.json` and `external_sequence_source_integrity.json`; the validation record distinguishes a reused source audit from a fresh local check.

## Explicit mapping bounds

The [bounded-mapping example](../research/experiments/bounded_mapping_v0.1/README.md) demonstrates `--mapping-constraints` and version 2 answer verification. Full reproduction adds `bounded_mapping_checks.json` and `bounded_mapping_assumption_example.json`. Bounds are explicit sensitivity assumptions, not newly accepted annotations. Existing unrestricted outputs remain unchanged.
