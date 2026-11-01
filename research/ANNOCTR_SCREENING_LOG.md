# AnnoCTR Screening Log — Preliminary Candidate Reports

**Date:** 1 November 2026  
**Corpus:** AnnoCTR (CC BY-SA 4.0 according to its official corpus README)  
**Purpose:** Technical/source screening before a human annotation feasibility pilot.  
**Status:** Preliminary convenience screen; no pilot labels have been created.

## Why these reports were inspected

The official AnnoCTR repository contains per-report source text, BIO/JSON annotations, MITRE linking output and TimeML files. The initial screen searched for documents with multiple link records to the same ATT&CK technique so we could test whether the source text gives enough context to distinguish repeated mentions from distinct report-local occurrences.

This screen is **not random, not representative and not a prevalence estimate**. All five documents below are from Intel471. Selection was intentionally based on files that were straightforward to locate and on repeat mentions in technique-link output. This introduces source and selection bias.

## Files and observed counts

Each inspected document has a paired raw text file, MITRE-only link JSON and TimeML file in the official repository's `AnnoCTR/all/` tree.

| Report identifier | Source-text characters | All MITRE link records | Technique link records | Unique technique IDs | Repeated technique link counts (top) | TIMEX3 tags | EVENT / MAKEINSTANCE / TLINK tags |
|---|---:|---:|---:|---:|---|---:|---|
| `intel471_2020-03-26_analysis-of-an-attempted-attack` | 15,211 | 64 | 32 | 5 | T1059: 24 | 31 | 0 / 0 / 0 |
| `intel471_2020-05-04_changes-in-revil-ransomware-version` | 3,624 | 29 | 17 | 3 | T1486: 8; T1543: 7; T1547: 2 | 3 | 0 / 0 / 0 |
| `intel471_2020-10-13_travelex-ddos-attack-lazarus-group` | 3,618 | 18 | 13 | 2 | T1499: 11; T1486: 2 | 9 | 0 / 0 / 0 |
| `intel471_2020-10-15_trickbot-online-emotet-microsoft-cyber` | 4,169 | 23 | 7 | 4 | T1566: 3; T1105: 2 | 9 | 0 / 0 / 0 |
| `intel471_2021-05-10_darkside-ransomware-colonial-pipeline-attack` | 5,620 | 54 | 26 | 9 | T1486: 17; T1499: 2 | 9 | 0 / 0 / 0 |

**How to read these counts:** a “technique link record” is a linked text mention mapped to an ATT&CK concept in the AnnoCTR output. It is not an event instance. The repeated counts only indicate multiple concept-linked mentions, not multiple executions.

## What this screen establishes

1. The repository contains full report text and associated annotation/linking files for these documents, so a human source-text annotation workflow is technically feasible.
2. The TimeML files for all five inspected reports contain temporal-expression elements (TIMEX3) but no TimeML EVENT, MAKEINSTANCE or TLINK elements. These specific files therefore do not provide event-event temporal gold links.
3. Several documents contain repeated ATT&CK technique-linked mentions. Whether those mentions refer to one occurrence, multiple occurrences, general capabilities, artefacts, or explanatory references must be decided by human reading.
4. A high mention count does not guarantee useful repeated-instance cases or clear temporal relationships.

## Provisional candidates for human review

The following order is only a screening priority, not a final pilot selection:
- `intel471_2020-03-26_analysis-of-an-attempted-attack`: longest screened report and many T1059-linked mentions; needs close reading to separate concrete actions from repeated references and generic explanations.
- `intel471_2020-05-04_changes-in-revil-ransomware-version`: compact report with multiple repeated technique links; useful to test whether short reports yield resolvable event instances.
- `intel471_2021-05-10_darkside-ransomware-colonial-pipeline-attack`: more technique-linked context and repeated T1486 mentions; inspect carefully for repeated behaviour versus descriptive repetition.
- The two October 2020 reports can be considered additional short-document contrasts.

Do not lock the pilot to five Intel471 reports. Before finalizing the 5–8 report pilot, screen reports from at least two other AnnoCTR donor sources where files are accessible, record the same counts, and use transparent inclusion criteria. If the report-level licence/provenance check identifies any restriction, exclude the affected report or obtain permission.

## Human screen and annotation sheet

For every candidate report, the human reviewer must record:
- report ID, title, donor/source, publication date, source URL, repository path, file SHA/hash and licence/provenance status;
- whether text is complete and matches offsets in BIO/JSON annotation files;
- candidate action mentions with exact offsets;
- for each mention, RESOLVED / UNRESOLVED / GENERIC_BEHAVIOUR / NOT_AN_EVENT;
- event-instance IDs only where a specific occurrence is supported;
- zero or more ATT&CK mappings per event instance, each with evidence;
- explicit temporal relation candidates and exact relation-specific evidence spans;
- whether the report actually contains enough positive and ambiguous/no-relation cases for the pilot;
- annotation time, decisions requiring adjudication and reasons for exclusion.

A second human annotator should independently review a subset if possible. AI can help locate candidate passages, but human annotators must assign the gold event identities and temporal relations.

## Source

Official repository and corpus licence: https://github.com/boschresearch/anno-ctr-lrec-coling-2024  
Paper: https://aclanthology.org/2024.lrec-main.103/

**Decision:** AnnoCTR remains the leading pilot candidate, not a final corpus selection. The initial screen establishes file availability and repeated linked-mention candidates, not repeated distinct event instances or temporal-link density.


## Full-corpus donor distribution and automated inventory plan

The original paper's Table 2 reports the 120 reports with both annotation layers as follows:

| Donor collection | Reports |
|---|---:|
| Intel471 | 30 |
| Lab52 | 23 |
| Proofpoint | 28 |
| QuoIntelligence | 12 |
| ZScaler | 27 |
| **Total** | **120** |

The five-report screen above was only from Intel471, so it is not the intended sampling frame. A local inventory utility has now been added at `scripts/screen_annoctr.py`. It scans the actual `AnnoCTR/all/` report text, MITRE-only link JSON and TimeML files, writes aggregate counts to CSV, and prints candidate locators separately by vendor. It does not infer event instances or temporal relations and does not copy report text into its output.

After downloading/cloning the official AnnoCTR repository locally, run:

```bash
python scripts/screen_annoctr.py \
  --root /path/to/anno-ctr-lrec-coling-2024/AnnoCTR/all \
  --output data/annoctr_screening.csv \
  --top-per-vendor 5
```

The scanner's synthetic unit tests are in `tests/test_annoctr_screening.py`. Execution of the full test suite and the scanner on the actual full corpus has not yet been confirmed in this session.

For final pilot selection:
1. inspect the inventory CSV;
2. shortlist from at least three vendors if available (not only the largest donor);
3. read every shortlisted report manually;
4. check donor/source URL, report date and provenance before selecting;
5. choose a mix of repeated-technique mention counts, report lengths and temporal-expression densities; and
6. human-decide whether there are distinct report-local event instances and explicit relation evidence.

Do not choose the highest mention-count reports alone: this would bias the pilot toward dense reports and vendor-specific writing styles.
