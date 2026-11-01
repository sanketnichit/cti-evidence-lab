# Project Status — 2026-11-01

**Current phase:** Research question refinement and dataset feasibility.  
**Implementation status:** Not started.  
**Novelty status:** Not established.

## Completed discovery work

- Audited the seven initial project blueprints.
- Verified ChronoCTI as a direct temporal CTI baseline.
- Read ChronoCTI's task definition: it predicts temporal relations between ATT&CK technique pairs within a report and builds technique-node graphs.
- Verified ChronoCTI's paper links a public Figshare data record (version 3); the earlier project note saying the data was private is superseded.
- Identified the report-level event-relation benchmark gap described in a 2026 cybersecurity event-extraction survey, while distinguishing it from ChronoCTI's technique-pair task.
- Inspected the SMAH-CTI public schema and licence: action spans and ATT&CK labels are available at sentence level, but no event-to-event temporal labels.
- Identified AnnoCTR as a possible full-document English CTI corpus and APTIE as a related Chinese multi-task event/relation dataset.
- Added a dataset feasibility plan and explicit stop/pivot gates.

## Current candidate

Measure how much temporal structure is lost when a CTI report is represented as ATT&CK technique nodes rather than report-local event instances. A secondary experiment may test evidence-linked event-instance relation extraction if annotation is feasible.

This is a hypothesis to test—not a validated gap, novel method, implemented system, or publication claim.

## Blocking gates

1. Inspect ChronoCTI Figshare version 3 files, exact schema, metadata, and licences.
2. Inspect candidate AnnoCTR/SMAH-CTI formats and source-report rights.
3. Run a 5–8 report annotation pilot focused on repeated technique occurrences and event coreference.
4. Assess positive relation counts, unresolved rate, annotation time, and independent agreement.
5. Only then select corpus, baselines, split, metrics, and implementation scope.

## Decision rule

If repeated occurrences are rare or not reliably distinguishable in the available reports, do not force the event-instance hypothesis. Pivot to a benchmark audit or a different, data-supported CTI research question.
