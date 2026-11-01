# Candidate System Architecture

This is a research hypothesis, not an implementation specification. Event schema and edge semantics must be validated during the annotation pilot.

```text
Authorized CTI report + immutable source metadata
                      |
             normalization / segmentation
                      |
           event-instance mention extraction
                      |
       source spans + ATT&CK concept grounding
                      |
          candidate event-pair generation
                      |
            temporal relation prediction
                      |
        relation-specific evidence attribution
                      |
        evidence / contradiction / ambiguity checks
                      |
                 accept / abstain
                      |
       traceable event graph + audit record
```

## Core distinctions

- **Event instance:** a specific occurrence or report mention of an adversarial action, with report-local identity and offsets.
- **ATT&CK concept:** a taxonomy-level technique/sub-technique ID. Multiple event instances may link to the same concept.
- **Temporal edge:** a relation between two event instances, not merely between two technique IDs.
- **Relation evidence:** one or more text spans that justify the relation. A span that only mentions one event does not by itself justify the edge.

Event-mention graphs are established prior work. A potential diagnostic is whether collapsing repeated report-local event mentions into ATT&CK technique nodes loses measurable temporal information in CTI reports.

## Candidate relation vocabulary

Begin by matching ChronoCTI semantics where possible. The following labels are provisional and must be reconciled with its paper and actual workbook:

- `BEFORE`: one event occurs before another.
- `SIMULTANEOUS_OVERLAP`: events overlap in the specific sense defined by the source annotation manual.
- `CONCURRENT`: independent events occur during the same phase, if reliably distinguishable.
- `NO_TEMPORAL_CLAIM`: source does not establish a positive relation for the pair.
- `UNRESOLVED`: annotators cannot confidently determine a relation.

Keep model `ABSTAIN` separate from the ground-truth label set.

## Candidate evidence categories

- `EXPLICIT_CUE`: text has a temporal marker or construction.
- `CROSS_SENTENCE_CONTEXT`: relation requires resolving a reference across sentences with identifiable textual support.
- `NARRATIVE_ORDER_ONLY`: inferred only from report ordering; not accepted as direct evidence in the primary condition.
- `DOMAIN_PRIOR_ONLY`: plausible from generic attack knowledge but unsupported by the report.
- `AMBIGUOUS_OR_CONFLICTING`: source evidence is insufficient or contradictory.

These categories need pilot examples, adjudication, and agreement analysis before becoming gold labels.

## Design constraints

- Preserve raw source offsets through normalization and segmentation.
- Do not silently convert report order into event order.
- Store confidence, evidence type, schema validity, and review status as separate fields.
- Pin ATT&CK release identifiers.
- Store dataset IDs and source URLs rather than re-hosting copyrighted reports.
- Preserve the distinction between source-reported fact and model inference.
