# Project Status — 2026-11-01

**Current phase:** Research validation and data-access audit.  
**Implementation status:** Not started.  
**Novelty status:** Not established.

## Completed discovery work

- Audited the seven initial project blueprints from the source report.
- Identified TRAM as established ATT&CK mapping work and ChronoCTI as a direct CTI temporal-graph precedent.
- Identified general NLP event-graph and long-distance temporal-relation precedents.
- Identified recent CTI evidence-mining and structured-graph research that narrows the possible contribution.
- Recorded dataset and third-party report licensing/access concerns.

## Current candidate

A CTI-specific empirical study of temporal relations between report-local event instances, relation-specific evidence attribution, and selective prediction/abstention.

This is a hypothesis to test—not a validated gap, novel method, implemented system, or publication claim.

## Blocking gates

1. Verify the primary literature and exact task overlap, including work published in 2026.
2. Resolve lawful access to a suitable CTI temporal-relation corpus or design a small rights-cleared annotation pilot.
3. Inspect the ChronoCTI workbook schema and determine whether event identity or evidence spans are already present.
4. Finalize a reproducible event-pair annotation protocol and assess annotator agreement.
5. Define baselines, leakage-resistant splits, metrics, and acceptance/abstention rules.
6. Only then approve implementation scope.

## Next review

Update this file after each gate with evidence, decisions, and links to the relevant commit. Do not mark a gate complete without a source or artifact supporting it.
