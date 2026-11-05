# Protocol / Schema Decision Proposal v0.1

**Date:** 5 November 2026  
**Status:** Researcher-review proposal only — not approved, frozen, or a replacement protocol  
**Basis:** Protocol v0.5-draft and RECON v0.1 reconciliation register

## Purpose

Resolve scope and data-model decisions before preparing a new schema version. RECON v0.1 remains a reconstruction, not the missing original v0.4.2 schema. This proposal authorizes no formal annotation.

## Recommended pilot scope

| Topic | Recommendation | Reason |
|---|---|---|
| Atomic event temporal relations | Keep in primary pilot | Core question: distinct resolved atomic occurrences, compatible scope, relation-specific evidence, and direct-source or qualifying timestamp basis. |
| Episode/container relations | Defer from primary pilot | No separate register; must not weaken the atomic-event gate or mix container relations into the event graph. Optionally note observed episode-level relation for later review. |
| ChronoCTI pair alignment | Defer from first annotation pass; consider as separate secondary analysis | First lock report-local event identity and temporal evidence. A technique-pair row is not automatically one source event pair. Preserve raw ChronoCTI `NEXT`; any BEFORE-like conversion remains a separately identified hypothesis. |
| Temporal evidence roles | Required schema change before freeze | Add controlled roles `RELATION_CUE`, `EVENT_A_SUPPORT`, `EVENT_B_SUPPORT`, and `RELATION_CONTEXT`. Keep exact source text in canonical evidence spans; do not duplicate cue text. |
| Evidence-scope completeness | Role-aware requirement | A sentence span may support multiple roles if it genuinely contains them. Cross-sentence claims require cue and argument support for both endpoints. Document-context claims require contextual spans and rationale. Section order alone is not temporal evidence. |
| Final analysis partition | Required before multi-pass or multi-annotator aggregation | Add partition selection record/manifest: partition role (`DEVELOPMENT`, `REPEAT`, `INDEPENDENT`, `CONSENSUS`, `ADJUDICATED_FINAL`), lock reference, selection status and rationale. At most one final analysis partition per report; never sum annotator/pass rows. |
| Timestamp normalization | Required before direct-timestamp edges enter primary graph | Preserve raw expression and evidence. Define accepted format, precision and timezone states; check interval/order consistency. If strict order is not invariant under uncertainty, do not emit strict `BEFORE`/`AFTER`. |
| Pair opportunity and report aggregation | Define in metric contract; implement after schema freeze | Pair opportunity differs from observed positive edges. Define compatible event-pair universe, mapping projection, denominator and missingness before rates. |
| Human agreement | Report as not measured unless a second human annotator is available | AI is not a second annotator. Same-person repeat can measure intra-annotator consistency only, with exposure disclosed. |

## Proposed evidence-link contract

Retain the existing architecture:

- `evidence_spans`: exact source text, frozen source hash and offsets.
- `record_evidence_links`: additional spans attached to a target record with a controlled evidence role.
- `temporal_relations.primary_evidence_span_id`: primary relation evidence; do not duplicate the same span/role in the link register.

For a positive temporal relation, the reviewer must identify the relation cue or timestamp basis, source support for Event A, source support for Event B, and any context needed to interpret the relation. A single span may serve multiple roles only if it truly supports each. Role completeness is a structural gate, not semantic proof.

## Later baseline-alignment register (only if approved)

Keep benchmark alignment separate from `event_mappings` and `candidate_pair_assessments`. At minimum record benchmark source/version and raw pair ID; raw ordered/directed labels; zero, one or multiple candidate report-local event pairs; alignment outcome (`SUPPORTED`, `MULTIPLE_CANDIDATE_PAIRS`, `AMBIGUOUS`, `UNMAPPED`, `NOT_ASSESSABLE`); evidence/rationale; and review status. Do not infer one-to-one correspondence.

## Freeze gates

- [ ] Researcher accepts/edits these scope recommendations.
- [ ] Temporal evidence roles and scope-specific completeness appear in vocabulary, field dictionary, data-model rules and validator.
- [ ] Timestamp uncertainty policy is executable or assigned to a documented manual procedure.
- [ ] Final-partition selection is defined before repeated-pass or multi-annotator aggregation.
- [ ] Episode relations and baseline alignment are explicitly deferred or isolated in dedicated tested registers.
- [ ] Metric contract defines event-pair opportunity, occurrence compression, projection outcomes and report-level denominators.
- [ ] Synthetic regression tests, manifest, QA record and checksums are regenerated; CI passes.
- [ ] Researcher explicitly approves and freezes the protocol/schema version.

## Recommendation

Adopt the minimal primary-pilot scope: atomic event relations only; defer episode relations and benchmark alignment. Implement evidence-role completeness, timestamp uncertainty rules and final-partition selection in a newly versioned schema. Do not begin formal annotation until the researcher approves the resulting protocol and schema.

## Current boundary

This proposal creates no annotation, eligibility decision, event identity, temporal edge, mapping, benchmark alignment or empirical result. The five rank-one AnnoCTR reports remain feasibility candidates; AI-exposed source reviews remain protocol-development material.
