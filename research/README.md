# Research materials

## Studies and results

| Study | Design | Artifacts |
|---|---|---|
| Occurrence identity in technique-level CTI graphs | Exploratory feasibility and controlled representation study | [Report](FEASIBILITY_REPORT_v0.1.md) |
| Connected-sequence query fidelity | Two exhaustive finite constructions; four representations | [Methods](QUERY_FIDELITY_STUDY_v0.1.md), [results](experiments/query_fidelity_v0.1/README.md) |
| Evidence-backed investigation | Query witnesses, incompatible joins, mapping-specific uncertainty and export verification | [Workflow and evaluation](INVESTIGATION_WORKFLOW_v0.1.md) |
| Representation controls | Seven specified graph comparisons and a 4,096-case oracle check | [Controls](experiments/representation_controls_v0.1/README.md), [finite check](experiments/representation_controls_v0.1/finite_checks.json) |
| AnnoCTR feasibility | Five fixed donor-stratified candidates; exposed exploratory review | [Review](feasibility/exploratory_review_v0.1/README.md), [critical assessment](feasibility/exploratory_review_v0.1/CRITICAL_REVIEW.md) |
| Fixed source extension | All five rank-two donor reports; selection committed before this text review | [Review and coverage](feasibility/rank_two_extension_v0.1/README.md), [protocol](feasibility/rank_two_extension_v0.1/PROTOCOL.md) |
| Repeated RDP attempts | Purposive source-bound case with outcome and mapping sensitivities | [Case study](case_studies/dfir_rdp_v0.1/README.md) |
| RDP and account lifecycle | Same-case extension with four actions and explicit unresolved cleanup mapping | [Sequence sensitivity](case_studies/dfir_rdp_sequence_v0.2/README.md) |
| Domain-controller sequence | Second intrusion chosen by chronological metadata before content review | [Core and extended queries](case_studies/dfir_html_smuggling_v0.1/README.md) |

The finite constructions are synthetic. The source studies are exploratory and have no independent agreement estimate. The two external intrusion cases are not part of the AnnoCTR sampling frame or a held-out evaluation set; the second uses the publisher's chronological metadata after the first.

## Data and source access

AnnoCTR is available from [Bosch Research](https://github.com/boschresearch/anno-ctr-lrec-coling-2024). The corpus inventory, pinned revision and archive identity are documented in the [screening report](../data/processed/annoctr_screening/SCREENING_REPORT_v0.1.md) and [source audit](feasibility/exploratory_review_v0.1/source_integrity.json). Adapted AnnoCTR annotation material retains CC BY-SA 4.0 attribution and terms. Raw report texts are not redistributed here.

The RDP case uses a separately retrieved publisher page. Its [case record](case_studies/dfir_rdp_v0.1/case.json) identifies the source, retrieval time, snapshot hashes and evidence offsets. The source article remains subject to its publisher's rights.

## Methods and provenance

- [Related-work matrix](RELATED_WORK_MATRIX.md) and [query-study comparison](QUERY_FIDELITY_STUDY_v0.1.md#relationship-to-established-work).
- [Protocol v0.5 draft](protocol/CTI_Event_Instance_Annotation_Protocol_v0.5-draft.md) and [schema reconciliation](protocol/PROTOCOL_SCHEMA_RECONCILIATION_v0.1.md).
- [Metric and decision records](metric_contract/), [sampling records](annoctr_sampling/) and [annotation drafts](annotation_drafts/AnnoCTR_Pilot_v0.1/).
- [Schema reconstruction](schema_reconstruction/): versioned validation and projection implementations; the original missing package is not represented as recovered.
- [Calibration protocol](reviewer_kit/COORDINATOR.md) and [review instrument](reviewer_kit/REVIEW_GUIDE.md). These are research materials, not completed review results.

Earlier versioned documents and audits record methodological history. Current results and limitations are summarized in [study status](../docs/PROJECT_STATE.md). Execution commands and artifact formats are documented in [reproducibility](../docs/REPRODUCIBILITY.md).

The [fixed five-publisher evaluation](experiments/external_sequence_evaluation_v0.1/README.md) adds a separate rank-three cohort. Its four conditional procedure graphs show no accuracy advantage on decidable queries; primary incident-sequence errors remain unassessed.
