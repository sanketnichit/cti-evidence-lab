# CTI Annotation Schema RECON v0.4 — activity-stratum extension

**Status:** Draft extension; researcher review and protocol freeze remain required.  
**Parent layers:** RECON v0.1 base registers, v0.2 temporal evidence/selected-final partitions, and v0.3 comparison-scope assignments.  
**Real activity-stratum decisions:** 0.  
**Purpose:** distinguish incident-linked attack-action occurrences from auxiliary report-local event strata and ensure only attack-action endpoints enter primary ChronoCTI-comparable metrics.

## Why v0.4 is additive

RECON v0.1 is a reconstruction with a fixed, checksum-controlled activity_units header. It is not edited in place. This extension stores the logical activity_unit.activity_stratum field in a one-to-one companion register, activity_unit_strata.csv, keyed by report/annotator/pass/activity_unit_id. Every activity unit must have exactly one stratum row. Treat this field as part of the v0.4 annotation schema; do not omit it because a source unit is inconvenient to classify.

This normalized extension preserves the v0.1 base package and its existing validators. A future full schema package may inline the field in activity_units.csv, but must preserve the same controlled values, one-to-one invariant, lock semantics and projection gates.

## Controlled activity_stratum values

- ATTACK_ACTION — a concrete report-local action that conducts, enables, or completes a specific cyberattack/incident. This is medium-neutral and may include adversary, malware, or induced user/system actions.
- THREAT_ACTOR_COMMUNICATION — a forum launch, public post, claim, response blog, or disclosure not established as an operational step in a specific attack.
- ANALYST_OBSERVATION — sample detection/submission, discovery, reverse engineering, or lab analysis.
- GENERIC_CAPABILITY — generalized malware function, command handler, or TTP without a resolved report-local execution.
- OTHER_NON_PRIMARY — report-local activity retained for description but outside the primary attack-action estimand.
- UNRESOLVED_CLASSIFICATION — the evidence does not support a defensible stratum assignment.

Classification is independent of ATT&CK mapping. An attack action remains in the primary event universe when no defensible technique mapping exists; the unmapped outcome remains visible. A technique label does not promote a communication, observation, or generic capability into ATTACK_ACTION.

## Registers

- registers/activity_unit_strata.csv — one evidence-backed stratum decision per activity unit and annotation partition.
- registers/activity_stratum_locks.csv — lock of all stratum decisions in each selected-final partition, bound to the RECON v0.2 selected-analysis lock reference.
- docs/FIELD_DICTIONARY.md, docs/CONTROLLED_VOCABULARIES.md, docs/DATA_MODEL_AND_VALIDATION_RULES.md, docs/PRIMARY_PROJECTION_RULES.md — field, vocabulary, invariant, routing and analysis contracts.

## Validation and analysis

Run the structural extension validator:

    python research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/validator/validate_activity_strata.py --base-bundle research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1 --strata-file research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/registers/activity_unit_strata.csv

Create stratum locks only after a selected-final analysis partition and all its activity-unit stratum decisions are complete:

    python research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/analysis/create_activity_stratum_locks.py --base-bundle research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1 --selection-file research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.2/registers/analysis_partition_selection.csv --strata-file research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/registers/activity_unit_strata.csv --output research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.4/registers/activity_stratum_locks.csv --locked-by YOUR_RESEARCHER_ID --lock-date YYYY-MM-DD

The primary projection helper filters the event universe, mapping rows, relation edges and pair-opportunity universe before projection. It defaults to the nearest shared RESOLVED INCIDENT ancestor; a primary relation must cite that exact same nearest incident scope. Cross-incident pairs sharing only a campaign/operation ancestor are excluded from primary metrics. The legacy broad-ancestor and explicit-assignment rules remain separate sensitivities. Auxiliary same-stratum relations and mixed-stratum relations remain countable in separate diagnostics but cannot enter primary attack-action projections or denominators.

## Safety gates

- Every base activity unit must have one and only one stratum decision; missing, duplicate, and orphan rows fail.
- Every decision requires a source evidence span and rationale; unresolved classification uses basis UNRESOLVED.
- This draft records `adjudication_status=UNREVIEWED` only. It has no activity-stratum adjudication log, so AGREED/ADJUDICATED rows are rejected and the v0.4 lock workflow supports only `SINGLE_ANNOTATOR_FINAL`. CONSENSUS and ADJUDICATED_FINAL partitions require a separately versioned adjudication extension before use.
- GENERIC_CAPABILITY cannot be represented as a resolved atomic event leaf.
- Both endpoints of a primary positive temporal edge must be ATTACK_ACTION. Same-stratum auxiliary edges and mixed-stratum edges are retained but routed outside primary analysis.
- Mapping rows for auxiliary events never contribute to the primary A_120 mapping sets.
- Stratum decisions are bound to the selected-analysis lock; post-lock edits invalidate the lock.

The lock-creation command and lock validator both revalidate the v0.2 selected-final decision against the base report registry and revalidate the complete v0.4 stratum register before accepting a lock. This prevents an ineligible or no-longer-assessable partition from being locked using only a hash-shaped selection reference. The v0.2 selected-analysis digest is a separate upstream gate: verify it with the v0.2 selected-partition adapter against the exact frozen source text before running the primary projection helper.

The v0.4 full-package validator also fails closed on required v0.1 `annotator_confidence`, `adjudication_status`, and `evidence_spans.span_kind` values. These fields were already documented as controlled in the v0.1 field dictionary, but the original v0.1 validator did not check every applicable register. The additional checks preserve the checksum-controlled v0.1 package unchanged and are covered by v0.4 regression tests.

The v0.4 full-package validator also enforces required non-empty base cells that the v0.1 loader did not check generically: report provenance/version/extraction fields, scope labels/descriptions, activity-unit summaries, descriptive `mention_kind`, evidence text, mapping ATT&CK version, comparison-scope IDs on relation/assessment rows, and adjudication reviewer/field/rationale/date. It validates `retrieval_date` as ISO `YYYY-MM-DD` and requires baseline vocabulary provenance for `OUT_OF_VOCAB` mappings. Conditional and optional fields remain governed by their existing field-specific rules. The checksum-controlled v0.1 package remains unchanged.

The report-registry conditional reason gates are also enforced: `source_scope_reason` is required for `INELIGIBLE`/`PENDING` source-scope decisions, `local_research_use_basis` is required for every recorded local-use status, and `assessability_reason` is required for `NOT_ASSESSABLE`/`PENDING` reports. These prevent a status enum from standing in for its required rationale.

The full-package validation also checks time-evidence target identity. The field dictionary permits an activity-unit target, a mention target, or both; a mention resolves to its activity unit through `event_mentions`. When both targets are present they must resolve to the same activity unit. The v0.2 direct-timestamp validator accepts mention-only time evidence by resolving the mention before endpoint-support matching.

## Research-readiness boundary

The package contains blank registers and synthetic tests only. It creates no human annotations, selected-final partitions, real-report projections, IAA measurements, or empirical findings. The working comparison-scope rule, timestamp semantics and alternative-mapping lifecycle are now recorded in Protocol v0.5-draft and the decision register; v0.3 explicit-scope assignment remains a single-annotator sensitivity because multi-annotator adjudication is not implemented. These decisions are not formal protocol/schema freeze approval. Do not begin annotation until the whole reconstructed package is reviewed, versioned, approved and frozen.
