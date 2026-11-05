# Schema manifest — RECON v0.2 temporal evidence extension

- Version: 0.2
- Prepared: 5 November 2026
- Status: draft; researcher review required; not approved or frozen
- Type: additive extension
- Parent: `../CTI_Annotation_Schema_RECON_v0.1`
- Real report rows: 0
- Synthetic tests only: yes
- Semantic evidence review: not performed
- Strict timestamp uncertainty ordering: not implemented

## Evidence roles

- `RELATION_CUE`: required; stored in `temporal_relations.primary_evidence_span_id`.
- `EVENT_A_SUPPORT`: required; stored in `temporal_relation_evidence.csv`.
- `EVENT_B_SUPPORT`: required; stored in `temporal_relation_evidence.csv`.
- `RELATION_CONTEXT`: optional; stored in `temporal_relation_evidence.csv`.

This extension does not replace or alter RECON v0.1 and does not claim equivalence to the missing original v0.4.2 schema.