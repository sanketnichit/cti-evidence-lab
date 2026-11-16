# RECON v0.4 manifest

- Package: CTI Annotation Schema RECON v0.4 activity-stratum extension
- Status: draft; not approved or frozen
- Parent: RECON v0.1 + RECON v0.2 + RECON v0.3
- Primary stratum: ATTACK_ACTION
- Primary comparison-scope rule: SHARED_RESOLVED_INCIDENT_SCOPE_v0.1 (nearest shared RESOLVED INCIDENT; relation must cite same scope)
- Sensitivity rules: NEAREST_COMMON_RESOLVED_NON_REPORT_SCOPE_v0.1; EXPLICIT_SHARED_EVENT_COMPARISON_SCOPE_ASSIGNMENT_v0.3
- Auxiliary strata: THREAT_ACTOR_COMMUNICATION, ANALYST_OBSERVATION, GENERIC_CAPABILITY, OTHER_NON_PRIMARY, UNRESOLVED_CLASSIFICATION
- Canonical representation: one-to-one activity_unit_strata.csv extension keyed by report_id, annotator_id, annotation_pass_id, activity_unit_id
- Lock: activity_stratum_locks.csv binds the complete stratum rows to the v0.2 selected-analysis lock reference
- Structural validator: validator/validate_activity_strata.py
- Primary projection filter: analysis/primary_attack_action_projection.py
- Synthetic tests: tests/test_activity_strata.py (25 tests; passed in GitHub Actions run #272 on 16 November 2026, as part of 266 total synthetic test executions)
- Real annotations: 0
- Selected final partitions with stratum locks: 0
- Real projections: 0
- IAA: not measured
- Empirical findings: none

The v0.1 activity_units register and its checksum-controlled package remain unchanged. The logical `activity_unit.activity_stratum` field is stored in a versioned companion register to preserve the reconstructed ancestor schema. The v0.4 full-package validator additionally enforces required v0.1 confidence, adjudication-status and evidence-span-kind values, plus the remaining clearly required non-empty cells and report-registry conditional reason pairings described in `docs/DATA_MODEL_AND_VALIDATION_RULES.md`.

- Lock preconditions: lock creation and verification revalidate the v0.2 selected-final decision against the v0.1 report registry and require valid complete v0.4 stratum coverage. Verify the v0.2 selected-analysis digest separately through the v0.2 selected-partition adapter using the exact frozen source text before projection.
- Adjudication boundary: v0.4 stratum rows support `UNREVIEWED` only; lock creation/verification support `SINGLE_ANNOTATOR_FINAL` only. Multi-annotator CONSENSUS or ADJUDICATED_FINAL use requires a dedicated stratum adjudication register and procedure.


- Time-evidence target identity: mention-only time rows resolve through `event_mentions.activity_unit_id`; when both `activity_unit_id` and `mention_id` are populated, they must resolve to the same unit. Conflicting dual targets fail full-package validation.
- Required-cell gates: provenance/version/extraction metadata, scope labels/descriptions, activity-unit summaries, mention kind, evidence text, mapping ATT&CK version, comparison-scope IDs on relation/assessment rows, and adjudication reviewer/field/rationale/date are non-empty; retrieval date must be ISO YYYY-MM-DD; OUT_OF_VOCAB mappings retain baseline vocabulary ID and SHA-256.
