# Research Decision Log

## 2026-11-01 — Initial direction: CTI evidence and ATT&CK mapping

**Status:** Superseded as the main research question; retained as a potential component.

**Reasoning:** Sentence-level evidence mining and ATT&CK mapping are active research areas, including CSEM-CTI and SMAH-CTI. A generic CTI mapper is insufficiently differentiated.

## 2026-11-01 — Refined direction: temporal event graph with relation evidence

**Decision:** Make evidence-constrained temporal relation reconstruction the leading candidate. Preserve report-local event identity separately from ATT&CK taxonomy concepts. Require positive temporal edges to carry relation-specific source spans; allow abstention.

**Superseding caveat:** Event-mention graphs and temporal edges are established general NLP work, while CTI research already covers temporal attack graphs and evidence mining. The representation itself is not novel. The project is only a CTI-specific empirical study hypothesis pending a pilot and closer related-work review.

## 2026-11-01 — ChronoCTI data access is unresolved

**Decision:** Treat ChronoCTI as a published direct baseline, not yet as an accessible/licensed benchmark.

**Reasoning:** Its associated Figshare record appeared as “shared privately” during the initial audit. The public repository licence does not automatically settle individual dataset files or third-party report-text rights.

## 2026-11-01 — Data rights are a gate

**Decision:** Do not include source CTI reports or copied annotation files until rights are confirmed.

## 2026-11-01 — No implementation before research gates

**Decision:** Keep the repository documentation-first until dataset schema, annotation feasibility, baseline comparability, and metrics are verified.

## Open questions

- Is a lawful copy of ChronoCTI temporal labels obtainable, and what is its exact schema?
- Do existing labels already include event identity or relation-specific evidence spans?
- Is a small new annotation subset feasible, with at least two annotators?
- Which relation labels, baselines, splits, and metrics are defensible?
