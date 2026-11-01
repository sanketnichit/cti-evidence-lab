# Human Pilot Starter — Report 01

**Purpose:** test whether the event-instance annotation protocol is understandable and usable on one real report before committing to the 5–8 report feasibility pilot.

**Do not treat this as a result.** No event identities or temporal relations have been annotated yet.

## Source report

Candidate: `intel471_2020-03-26_analysis-of-an-attempted-attack`

- [Open the full report text](https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/main/AnnoCTR/all/text/intel471_2020-03-26_analysis-of-an-attempted-attack.txt)
- [Open its MITRE-only technique-link records](https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/main/AnnoCTR/all/linking_mitre_only/intel471_2020-03-26_analysis-of-an-attempted-attack.json)
- [Open its TimeML file](https://github.com/boschresearch/anno-ctr-lrec-coling-2024/blob/main/AnnoCTR/all/time/intel471_2020-03-26_analysis-of-an-attempted-attack.tml)
- [Open the AnnoCTR corpus README and licensing statement](https://github.com/boschresearch/anno-ctr-lrec-coling-2024)

The repository describes the corpus as CC BY-SA 4.0 and says that it includes 400 reports from commercial CTI providers. Per-report provenance and original source terms still need checking before using report text in a publication or redistributing excerpts. Do not add raw report text to this project's repository.

## Why this report was shortlisted

A mechanical source-file screen found:
- 15,211 characters in the source text;
- 64 MITRE-link records in total;
- 32 technique-link records across five unique technique IDs;
- 24 technique-link mention records mapped to T1059;
- 31 TIMEX3 tags in its TimeML file;
- zero TimeML EVENT, MAKEINSTANCE or TLINK tags.

The 24 T1059 records are **not 24 events**. They may include repeated references to one action, separate actions, generic descriptions, artefacts, or context. The human reader has to determine which, if any, are specific event instances. Similarly, TIMEX3 tags are temporal expressions, not event-to-event relations.

## Your first task: read, do not label by guess

1. Read the complete report from beginning to end.
2. Identify every passage that appears to describe a specific action performed in the reported operation. Do not annotate generic capability descriptions as specific events.
3. For each candidate action mention, record its exact character offsets in the original text. Offsets are zero-based and end-exclusive.
4. Decide whether it describes a specific report-local occurrence, a generic behaviour statement, a non-event, or an unresolved instance.
5. Where two mentions appear to describe the same occurrence, propose a shared event-instance ID and explain the textual evidence. Where separate occurrences are proposed, explain the distinction.
6. Assign one or more ATT&CK mappings only where the report itself supports them. The pre-existing mapping file is a candidate locator, not an instruction to accept every label.
7. Only after event identity is decided, look for explicit temporal relations between distinct event instances. Record the exact evidence that connects both arguments and supports the relation. Do not infer order from sentence position.

## Files to use

Fill the blank templates:
- `research/templates/report_registry.csv`
- `research/templates/event_mentions.csv`
- `research/templates/event_mappings.csv`
- `research/templates/temporal_relations.csv`

Use `research/ANNOTATION_PROTOCOL_v0.3.md` and follow `research/PILOT_SAMPLING_PLAN_v0.1.md` before freezing the pilot sample. Keep one report ID consistent across all files. It is fine for a report to produce zero positive temporal relations; do not invent them to make the experiment look successful.

## Stop point

After Report 01, review the annotation guide before doing the other four reports. Record:
- time taken;
- number of candidate event mentions;
- resolved / unresolved / generic behaviour / not-an-event counts;
- event instances with multiple technique mappings;
- explicit temporal relation count by label;
- difficult decisions and why;
- whether the current categories were understandable.

A second human should independently annotate this report or an overlapping subset if possible. If no second human is available, we will not report inter-annotator agreement.

**Pilot inclusion status:** shortlisted only. Confirm report provenance and source-text rights in the AnnoCTR provenance file before freezing it into a formal pilot sample.


## Preliminary source-file screening note — review only after your first pass

To reduce anchoring, read the source report and make your own first-pass event-mention notes before relying on this locator. This is **not an annotation** and must not be copied into the gold CSVs without independent human verification.

A direct inspection of the linked technique file found 64 newline-delimited JSON records: 32 technique, 28 malware and 4 tactic records. Of the technique rows, 24 are linked to T1059. Their mention spans mix macro-related wording with references to an Excel document builder, documents, sample files and repeated descriptions. They are not 24 event mentions, 24 executions, or automatically valid event-to-technique mappings.

The report prose also contains an explicit local ordering cue describing a file as retrieved/saved **before being executed** (around character offset 4,009 in the current source text). Treat this only as a candidate relation cue. A human must identify the two action arguments, decide whether they are separate resolved event instances, verify any ATT&CK mappings independently, and record the exact evidence offsets. No relation has been pre-annotated.

**Interpretation:** this candidate is promising for testing the protocol because it contains both repeated technique-link annotations and at least one explicit temporal cue. It is not yet confirmed as suitable for the formal pilot, and it says nothing about prevalence across AnnoCTR.
