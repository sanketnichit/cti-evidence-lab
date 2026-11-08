# RECON v0.4 controlled vocabulary

## activity_stratum

| Value | Operational meaning | Primary attack-action analysis |
|---|---|---|
| ATTACK_ACTION | Concrete report-local action that conducts, enables, or completes a specific cyberattack/incident. Medium-neutral; may include adversary, malware, or induced user/system actions. | Eligible after all existing event-leaf, evidence, temporal-relation and scope gates pass. |
| THREAT_ACTOR_COMMUNICATION | Forum launch, public post, claim, response blog, disclosure, or platform communication not established as an operational step in a specific attack. | Excluded; retain for separate descriptive analysis. |
| ANALYST_OBSERVATION | Sample detection/submission, discovery, reverse engineering, or lab analysis. | Excluded; retain for separate descriptive analysis. |
| GENERIC_CAPABILITY | Malware function, command handler, generalized TTP, or capability without a resolved report-local execution. | Excluded; cannot be a resolved atomic event leaf. |
| OTHER_NON_PRIMARY | Report-local activity that is relevant to the source but outside the declared primary attack-action estimand. | Excluded; retain with rationale. |
| UNRESOLVED_CLASSIFICATION | Evidence does not support a defensible choice among the defined strata. | Excluded; retain as unresolved, not as a negative event. |

## stratum_basis

- REPORT_EXPLICIT — the source itself makes the classification clear.
- SOURCE_SUPPORTED_HUMAN_JUDGMENT — a human annotator classifies the unit based on the source and records a rationale.
- UNRESOLVED — the annotator cannot resolve the stratum from the available source evidence. This basis is mandatory for UNRESOLVED_CLASSIFICATION and cannot be used for the other values.
