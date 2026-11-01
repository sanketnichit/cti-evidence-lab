# Contributing and Research Workflow

This repository is an individual academic research project. Contributions and experiments must preserve reproducibility and evidence provenance.

## Before adding code

1. Link the change to a research question or experiment.
2. Record relevant papers and dataset documentation in `research/EVIDENCE_LEDGER.md`.
3. Check data and model licences and document restrictions.
4. Keep test data out of development and prompt tuning.
5. Add tests for parsing, offsets, taxonomy validation, and evidence-link integrity where applicable.

## Experiment records

Every experiment should record commit, dataset/split/version, ATT&CK version, model revision, configuration, random seed, hardware, and evaluation command.

## Pull requests

Prefer small changes with one clear purpose. Include tests, expected outputs, and methodological consequences. Never include raw CTI data or secrets without an explicit licence and security review.
