# RECON v0.4 primary attack-action projection rules

1. Select only activity units with activity_stratum=ATTACK_ACTION, unit_role=event_leaf, granularity=atomic_event, and instance_status=RESOLVED.
2. Retain all activity units and all stratum decisions in the annotation source bundle. Filtering happens only in the primary analytical view; no auxiliary row is deleted.
3. Retain a temporal relation in the primary edge set only when both endpoint IDs belong to the selected attack-action event-leaf set, the label is a positive temporal label, the relation basis is direct_source or direct_timestamp, and scope_compatibility is COMPATIBLE.
4. Exclude same-stratum auxiliary and mixed-stratum relations from the primary graph. Report their counts/IDs in separate diagnostics.
5. Pass only accepted, source-supported A_120 mappings for selected attack-action units to the projection metric. An unmapped attack-action event stays in the event universe; it is not dropped from event counts.
6. Compute pair opportunity only over the same selected attack-action event-leaf set, under one explicitly named scope-pair rule. If that rule is not approved, show candidate counts only and withhold inferential/report-level rates.
7. A caller must validate the base bundle, full stratum coverage and stratum lock, and selected-analysis lock before projecting reviewed data. The projection helper itself is a deterministic filter/metric adapter, not a replacement for these validation gates.

The synthetic tests verify that a communication-only edge, a mixed attack/communication edge, and mappings attached to communication units do not contribute to primary attack-action projection or pair-opportunity metrics.
