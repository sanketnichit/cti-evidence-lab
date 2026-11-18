# CTI Evidence Lab: submission and demonstration

This submission completes the exploratory feasibility study of occurrence identity in technique-level CTI graphs. Start with the [report](../research/FEASIBILITY_REPORT_v0.1.md). It contains the question, related work, source procedure, findings, projection argument, experiments and limitations. The original gold-annotation/prevalence study remains future work; this submission does not claim that result.

## Reproduce the submission

Requirements: Git and Python 3.11 or later. Run from a clean repository checkout:

```sh
python scripts/reproduce_study.py
```

The command runs all five test suites (306 tests at this checkpoint), checks 31 base-package hashes, regenerates seven controls and 4,096 finite graph cases, and builds `outputs/submission/CTI_Evidence_Lab_Submission.zip`. It records the exact Git commit, Python version, test output, source-audit mode and file hashes. Outputs do not change tracked study records. A dirty checkout is rejected by default; `--allow-dirty` is only for development and marks the package accordingly.

The basic run uses the committed source audit. For a fresh source check, use the official AnnoCTR checkout's `AnnoCTR/all` directory:

```sh
python scripts/reproduce_study.py --corpus-root /path/to/AnnoCTR/all --recover-crlf
```

`--recover-crlf` permits line-ending recovery only when it exactly reproduces the pre-recorded source hash. It does not rewrite source files. This run verifies 120 report identities, 33 pilot evidence pointers and 22 critical-review passages. A hash check establishes text identity, not the correctness of a judgment.

For the PDF report, install the optional rendering dependency and add `--pdf` to either reproduction command:

```sh
python -m pip install reportlab
python scripts/reproduce_study.py --pdf
```

The report can also be rendered separately with `python scripts/build_report_pdf.py`. The underlying analysis has no third-party Python dependencies. Raw corpus text stays local and is not part of the submission ZIP.

## What to open

| Artifact | Purpose |
|---|---|
| `CTI_Evidence_Lab_Report.pdf` (with `--pdf`) | Readable report with clickable references |
| `representation_controls.md` and `.json` | Seven worked graph comparisons and their provenance |
| `finite_checks.json` | Exhaustive finite check: 4,096 graphs, 6,144 edges, zero oracle disagreements |
| `exploratory_review.json` | Five-report dispositions; unresolved evidence stays unresolved |
| `source_integrity.json` | Source identities and evidence-pointer checks without report text |
| `validation.json` | Test results, commit, runtime and source-verification mode |
| `manifest.json` | SHA-256 for every packaged file except the manifest itself |
| `CTI_Evidence_Lab_Submission.zip` | Repository under `cti-evidence-lab/`, outputs under `generated/`, and manifest |

After extracting the ZIP, use `generated/` to inspect this run. To rerun, clone the repository and check out the commit recorded in the manifest; the ZIP does not embed Git history. GitHub Actions also verifies code and blank schema bundles on main.

## Five-minute demonstration

1. State the question: a technique is a behavior category; two occurrences of the same behavior are still distinct events.
2. Open the report's projection argument. When two endpoints have the same single mapping, excluding diagonal technique pairs removes their relation.
3. Open the seven-control table. Show that allowing a self-loop still merges occurrence endpoints, and that mapping fan-out can create a projected cycle from one source edge.
4. Open `finite_checks.json`. Explain the exhaustive construction before discussing its counts; these are controlled inputs, not incident frequencies.
5. Open the five-report source findings. Explain the unresolved mappings and incident linkage. The retained occurrence candidate is not a census, and no qualifying within-technique pair is established.
6. Open `validation.json` and the manifest. Show that the implementation and reported artifacts can be reproduced from the identified commit.

## Boundaries of the conclusion

The project demonstrates specific representational losses and cycle ambiguities, plus the difficulty of obtaining suitable occurrence-pair evidence from the fixed source set. It does not measure corpus prevalence, extraction accuracy, independent agreement or a new system's superiority. Optional future reviewer packets are documented separately; their existence is not completed review.
