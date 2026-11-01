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

General NLP already studies event mentions, event coreference, and temporal relations. The project is not claiming those representations are novel. The potential contribution is an empirical, CTI-specific investigation of this granularity problem, supported by a clearly documented annotation protocol and reproducible evaluation.

## Primary research question

> How much temporal structure is lost when CTI reports are represented as ATT&CK technique nodes rather than distinct report-local event instances?

## Secondary research question

> Can an evidence-linked event-instance representation recover temporal relations with better event-level fidelity than a technique-pair representation, at a useful level of coverage?

The secondary question is conditional on the annotation pilot and a reproducible baseline being feasible.

## Candidate hypotheses

- **H1 — Aggregation loss:** In reports containing multiple distinct occurrences of the same ATT&CK technique, collapsing occurrences into one technique node loses or conflates at least some event-level temporal distinctions.
- **H2 — Relation fidelity:** An event-instance graph evaluated against event-instance annotations provides more faithful temporal structure than a graph that aggregates by technique ID.
- **H3 — Evidence support:** Requiring relation-specific source spans reduces unsupported temporal edges compared with a model that predicts relations without producing relation evidence.

These hypotheses are unverified. We will measure how often their preconditions occur before deciding whether to test them at scale.

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

Proceed beyond the pilot only if the data contain enough repeated event occurrences and temporal relations, annotation boundaries are sufficiently reliable, source rights are clear, and a fair baseline comparison can be reproduced. Otherwise narrow or replace the project.
