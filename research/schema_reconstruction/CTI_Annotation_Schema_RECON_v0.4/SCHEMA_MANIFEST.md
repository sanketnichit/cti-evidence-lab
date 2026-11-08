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
- Synthetic tests: tests/test_activity_strata.py (13 tests; passed in GitHub Actions run #226 on 8 November 2026)
- Real annotations: 0
- Selected final partitions with stratum locks: 0
- Real projections: 0
- IAA: not measured
- Empirical findings: none

The v0.1 activity_units register and its checksum-controlled package remain unchanged. The logical activity_unit.activity_stratum field is stored in a versioned companion register to preserve the reconstructed ancestor schema.
