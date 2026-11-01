# Candidate System Architecture

This is a research hypothesis, not an implementation specification. Validate every layer with a small annotation pilot before implementing a full pipeline.

```text
Authorized CTI report + immutable source metadata
                      |
       text normalization + offset preservation
                      |
              event mention detection
                      |
          event-mention coreference / clustering
                      |
            report-local event instances
                      |
       ATT&CK concept grounding (optional metadata)
                      |
          candidate event-instance pairs
                      |
             temporal relation prediction
                      |
        relation-specific evidence attribution
                      |
       accept / unresolved / abstain decision
                      |
       traceable event-instance temporal graph
```

## Core representation

### Event mention

A span in the report that describes an action. It has:
- report ID and document version;
- source character offsets (zero-based, end-exclusive);
- exact source text;
- sentence/paragraph location;
- optional normalised description.

### Event instance

One underlying action occurrence in the incident narrative. An event instance can have multiple text mentions. It has:
- stable report-local instance ID;
- one or more linked event mentions;
- optional actor, object, target, time, and context arguments;
- one or more ATT&CK concept links where supported.

### ATT&CK concept

A reusable taxonomy item. It is linked to an event instance but is not the event instance itself. Several distinct occurrences may share one technique ID.

### Temporal edge

A directed or symmetric temporal relation between event instances. Its record must include:
- source and target instance IDs;
- relation label;
- supporting evidence span(s);
- annotation/model provenance;
- confidence and adjudication status.

A sentence that merely mentions both endpoints is not necessarily evidence for the relation between them.

## Provisional relation labels

The vocabulary must be reconciled with ChronoCTI's exact schema and tested in the pilot:
- `BEFORE`: source event occurs before target event.
- `OVERLAP`: time intervals overlap; define exact scope from annotation examples.
- `CONCURRENT`: events occur during the same period but are independent, if annotators can reliably distinguish it from overlap.
- `NO_RELATION`: the report does not establish a positive temporal relation for this candidate pair.
- `UNRESOLVED`: source wording does not support a reliable human decision.

Keep model `ABSTAIN` outside the gold-label vocabulary.

## Evidence categories to test

- explicit temporal cue;
- cross-sentence contextual evidence;
- report chronology / narrative order only;
- domain prior only;
- ambiguous or conflicting evidence.

Do not accept narrative order or domain prior alone as direct evidence in the primary evidence-supported evaluation.

## Representation comparison

The key comparison is between:
1. **Technique-level graph:** aggregate event descriptions by ATT&CK concept within a report, following the broad representation used by ChronoCTI.
2. **Event-instance graph:** preserve separate event occurrences and their relations; repeated text mentions can be coreferentially linked to one instance.

The project should measure information loss under aggregation, not merely claim that an event-instance graph is more detailed.
