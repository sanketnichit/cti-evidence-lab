# Event-Instance and Temporal-Evidence Annotation Protocol (Draft)

**Status:** Pilot draft only. Do not use as final gold-label guidance without reconciliation against existing datasets and an independent annotation trial.

## 1. Annotation unit

Annotate within one report. First identify event mentions and assign stable report-local IDs. Then consider candidate pairs of event instances and annotate only what the report supports.

Do not merge repeated mentions solely because they map to the same ATT&CK technique. Do not split mentions if they clearly refer to the same event occurrence.

## 2. Event mention fields

For each mention, record:
- report ID and source version;
- event ID;
- exact text span (character offsets, half-open convention);
- sentence/paragraph identifier;
- normalized event description (annotator-written, not replacing source text);
- candidate ATT&CK technique ID and taxonomy version, if determinable;
- coreference link to another mention if it clearly refers to the same occurrence;
- confidence and adjudication status.

## 3. Candidate pair fields

For each ordered pair:
- source event ID;
- target event ID;
- relation label;
- relation evidence span(s);
- evidence category;
- annotator confidence;
- unresolved/needs-adjudication flag;
- short rationale for adjudication only.

## 4. Provisional relation definitions

- `BEFORE`: evidence establishes source event occurs before target event.
- `OVERLAP`: events overlap in time; exact semantics must follow the selected corpus/manual.
- `CONCURRENT`: events occur during the same interval or phase but are not causally dependent, only if distinction is consistently annotatable.
- `NO_TEMPORAL_CLAIM`: text does not establish any positive temporal relation for this pair.
- `UNRESOLVED`: report wording or context does not support a reliable annotator decision.

The distinction between overlap and concurrent must be tested; merge categories if agreement is inadequate.

## 5. Evidence rules

Positive relation evidence must support the relation between the pair. A span that only mentions the source event or target event is not sufficient by itself.

Record separately:
- explicit temporal cue;
- cross-sentence contextual evidence;
- narrative order only;
- domain prior only;
- conflicting/ambiguous evidence.

In the primary evidence-grounded setting, narrative order or domain prior alone is not accepted as sufficient support.

## 6. Annotation workflow

1. Annotator reads the report in full.
2. Annotator marks event mentions and offsets.
3. Candidate pairs are generated using a documented procedure; do not show only model-positive pairs to annotators.
4. Annotator assigns relation, evidence span(s), and confidence.
5. A second annotator works independently on an overlapping subset.
6. Disagreements are adjudicated by a qualified reviewer.
7. Report relation agreement, evidence span agreement, unresolved rate, and time per report.

## 7. Pilot checklist

- Do annotators distinguish separate occurrences of the same technique?
- Is the relation vocabulary mutually understandable and exhaustive enough?
- Can a temporal edge be supported by a concise evidence span?
- Are implicit/cross-sentence relations reproducibly annotated?
- Is `NO_TEMPORAL_CLAIM` distinguishable from missing evidence?
- Are overlap and concurrency independently annotatable?
- Is candidate-pair generation manageable without biasing annotators?
- Is a multi-annotator design feasible?
