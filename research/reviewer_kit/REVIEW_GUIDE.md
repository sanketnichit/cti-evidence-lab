# Independent source review guide

Version 0.1 — 17 November 2026. **Protocol calibration, not formal gold annotation.**

## Purpose

We are studying what information is lost when individual attack occurrences are represented only by ATT&CK technique names. First we need to find out what the reports actually support. A report with no suitable event pair is as useful to this exercise as a report with one. Do not search for a preferred answer.

The same five fixed reports go to both reviewers. Work separately, without consulting project drafts or each other's answers. The sample was chosen earlier; it is not a new random population sample. This guide simplifies the draft protocol for calibration. It does not approve or freeze the formal schema.

## 1. Read each source

Read the complete supplied text, including captions and tables. Embedded image links are not image evidence: if an interpretation needs an unavailable image or another article, record that limitation. Do not open indicators of compromise or execute anything described in the reports. This is a text-reading task.

Fill one row in `report_reviews.csv` for each report. Use:

- `prior_exposure`: NONE, SOURCE_SEEN, or PROJECT_DRAFT_SEEN.
- `source_read_completely`: YES or NO.
- `text_sufficient`: YES, NO, or UNCERTAIN, with a reason. A readable report with no suitable events can still be sufficient.
- `report_genre`: a short description in your own words.
- `source_scope_eligible`: YES, NO, or UNCERTAIN. The target is a report describing malicious cyber activity or its technical investigation. Do not exclude a report merely because it lacks an event pair.
- `resolved_attack_occurrences`: your count, or blank if you cannot determine it. Blank is not zero.
- `qualifying_temporal_pair`: YES, NO, or UNCERTAIN. YES means two distinct attack occurrences in a supported shared incident, with an explicitly supported temporal relation. A shared ATT&CK mapping is assessed separately, not required for this field.
- Record minutes actually spent, review date, missing information and reasons.

## 2. Separate activities from occurrences

Use `activity_units.csv`. Give each candidate a stable local ID such as A01. Include borderline candidates so we can understand disagreements.

An occurrence is one distinguishable action that happened, or one distinguishable attempted action. Repeated mentions can refer to the same occurrence. A tool name, malware hash, capability, command option, or technique name is not itself an occurrence. A named victim or exact timestamp is helpful but is **not required** if other evidence distinguishes the action.

`activity_class`: ATTACK_ACTION, COMMUNICATION, ANALYST_OBSERVATION, CAPABILITY, or OTHER. `occurrence_status`: RESOLVED, SERIES_OR_EPISODE, GENERIC, or UNRESOLVED. `confidence`: HIGH, MEDIUM, or LOW, with a reason rather than confidence alone.

Use `incident_id` only when the text supports that incident context, and explain the evidence in `rationale`. Sharing an actor, campaign, victim organization or report is not sufficient by itself. Leave it blank when uncertain. Do not merge separate incidents to create a pair.

## 3. Record actual temporal evidence

Use `temporal_relations.csv` only for proposed positive relations between activity IDs you recorded. Labels are BEFORE, AFTER, OVERLAP, SIMULTANEOUS or CONCURRENT_UNSPECIFIED. Use `direct_source` for an explicit source assertion and `direct_timestamp` only for strict order supported by occurrence-time bounds with timezone evidence. Publication, compilation, sample-submission and discovery dates are not automatically attack times.

Relation evidence must support the relation, not merely mention both endpoints. The order of paragraphs, diagrams, command lists or ATT&CK tactics does not establish chronology. A dependency does not automatically mean BEFORE. If uncertain, put the question in `questions.csv`; do not force a positive relation.

For `shared_incident_supported`, use YES, NO or UNCERTAIN with a reason. Multiple source spans may be recorded in additional rows with the same relation ID only if clearly marked as additional evidence in the rationale; these are not extra relations.

## 4. Map techniques cautiously

Use `technique_mappings.csv` if you have the relevant ATT&CK knowledge. Otherwise leave it empty and explain the limitation in `questions.csv`; source review is still useful.

Record one candidate technique per row. `mapping_status`: SOURCE_EXPLICIT, ANALYST_PROPOSED, or UNRESOLVED. If a source lists techniques for the whole report, do not assign them to every activity. Do not infer a sub-technique or parent solely from a familiar malware name. Exact mappings will be reconciled later against the project's pinned Enterprise ATT&CK v12.1 crosswalk; this packet does not ask you to certify taxonomy compatibility.

## 5. Evidence locations

Offsets are zero-based, end-exclusive Unicode code-point positions into the exact `.txt` file. Do not change line endings or source wording. If you cannot calculate offsets reliably, leave those cells blank and put the section, paragraph/line and a short unique phrase in `rationale`. We can resolve that locator later and return it for confirmation. Do not guess offsets.

For an example unrelated to the sources, in `Alpha ran. Beta stopped.` the span `[0, 9)` selects `Alpha ran`. This explains positions only; it is not an answer to any report.

## 6. Return the first pass

Return all five CSVs and `manifest.json`, zipped together, before comparing answers. Keep your original copy. A partially completed return is fine if you identify which reports were read completely. Do not fill missing decisions with zeros. Use only the pseudonymous R1/R2 identifier; no private contact details are needed.

The coordinator will check source locations, align candidate IDs by source evidence, and list disagreements about occurrence identity, scope, temporal relations and mappings separately. Corrections will preserve both original submissions. Discussion after the first pass is reconciliation, not an additional independent review.

Two returns do not automatically establish an agreement score. Unit alignment, overlap coverage and the scoring rule must be specified before calculating it. No reliability statistic will be reported from one reviewer, partial forms, or differently defined event universes.
