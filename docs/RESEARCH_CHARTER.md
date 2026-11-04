# Research Charter

## Working title

**Event-Instance-Level Temporal Relation Extraction for Evidence-Grounded Cyber Threat Intelligence**

The title is provisional and may change after the literature and dataset audit.

## Problem context

CTI reports describe attack behavior in natural language. Existing systems commonly normalize reported behavior to MITRE ATT&CK techniques, which is useful for sharing and comparison. However, a technique is a taxonomy concept, not a unique occurrence of an action in one incident.

A report can describe several distinct occurrences of the same technique. It can also mention the same occurrence more than once. These are different problems:
- **Repeated event occurrences:** two or more distinct actions map to the same ATT&CK technique.
- **Event coreference:** two or more text mentions refer to the same underlying action occurrence.

ChronoCTI defines its temporal-relation task over pairs of ATT&CK techniques within a report and builds graphs with techniques as nodes. This makes it a valuable direct baseline, but also creates a concrete representation question: what incident-level temporal detail is lost when repeated event occurrences are collapsed into a single technique node?

Existing work already covers CTI event extraction, temporal attack graphs, ATT&CK-linked behaviour and technique-pair temporal prediction. General NLP also studies event coreference and temporal relations. This project does not claim novelty for generic CTI event extraction, ATT&CK mapping, attack sequencing or event-level graph construction. Its remaining candidate contribution is narrower: a human source-grounded measurement of which distinct occurrence-level relations are explicitly supported in a transparently sampled CTI report set, and what information is retained, conflated or omitted by a named distinct-technique-pair projection.

## Primary research question

 > Across a transparently sampled set of CTI reports, how often does a report explicitly support a temporal relation between two distinct, resolved activity occurrences that share one or more ATT&CK technique mappings, and what occurrence identity or temporal information is retained, partially represented or lost when those occurrences are projected to a representation that permits only distinct technique pairs?

## Secondary research question

 > Conditional on the source-grounded event-instance annotations, which parts of the observed occurrence identity and temporal structure remain represented, become partially represented, are conflated, or are omitted under the named distinct-technique-pair projection?

This is a descriptive representation comparison, not an evaluation of ChronoCTI model outputs on AnnoCTR. ChronoCTI's learned model has not been run on the AnnoCTR reports.

## Candidate hypotheses

- **H1 — Aggregation consequence:** When two distinct event instances share a technique, a representation that excludes diagonal technique pairs cannot preserve that same-technique event-pair edge as a distinct technique pair. This is a consequence of the projection definition; the empirical question is how often the source reports actually support such relations.
- A model-based comparison of event-instance extraction or evidence-grounded relation prediction is a possible later extension, conditional on the annotation pilot, a fair baseline and sufficient data.

The initial study is descriptive and tests annotation feasibility and representation-level measurement. It does not claim model superiority or generic hallucination reduction.

## Units and definitions

- **Report:** one source CTI document or report version.
- **Event mention:** a text span that describes an action.
- **Event instance:** one actual action occurrence described in the report. Multiple event mentions may refer to the same instance.
- **ATT&CK concept:** a taxonomy-level technique or sub-technique ID. Many event instances may link to one concept.
- **Temporal relation:** a relation between two event instances, not simply between two technique IDs.
- **Relation evidence:** text span(s) that support the relationship between the two event instances.

## Scope

In scope:
- event-mention identification and source offsets;
- distinguishing separate occurrences from coreferential mentions;
- ATT&CK concept grounding as metadata;
- temporal relation annotation and evidence localization;
- comparison of event-instance and technique-level representations;
- reproducible baselines, error analysis, and annotation agreement.

Out of scope until separately justified:
- general-purpose CTI chatbot;
- autonomous incident response or live SOC integration;
- threat prediction or attribution claims;
- training a large language model from scratch;
- complex dashboards before the data model is validated;
- adding causal, conditional, or multi-document relations to the first experiment.

## Research integrity requirements

1. No novelty claim until the primary literature and actual annotation schemas have been compared.
2. Treat an event mention and an event instance as distinct annotation objects.
3. Do not infer distinct occurrences merely because the same technique is mentioned twice.
4. Do not merge distinct occurrences merely because they share an ATT&CK ID.
5. Every positive relation must be supported by relation-specific report evidence.
6. Distinguish `NO_RELATION` from `UNRESOLVED` and from model `ABSTAIN`.
7. Preserve original offsets, report versions, source provenance, ATT&CK version, and dataset licence.
8. Split by report and group duplicate/syndicated reports to prevent leakage.
9. Report annotation agreement and unresolved rates before presenting model scores.
10. Negative or inconclusive results are valid outcomes.

## Decision rule

Proceed beyond the pilot only if the data support reliable source-grounded annotation, occurrence boundaries are defensible, source rights are clear, and a fair named-projection comparison can be reproduced. A zero-positive pilot is not failure if it reveals a genuine limitation of the sampling frame or annotation protocol. Otherwise narrow or replace the project.
