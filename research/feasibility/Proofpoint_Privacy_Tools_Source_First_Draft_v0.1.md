# Proofpoint — Privacy Tools / Smoke Loader source-first feasibility draft v0.1

**Status:** Reviewer draft only. Not a locked annotation, not included in denominators, and not an empirical result.  
**Candidate:** Rank-1 Proofpoint report in the fixed 120-report frame.  
**Source title:** *Malware Masquerades as Privacy Tool*  
**Publication date:** 1 July 2021  
**Canonical publisher page:** https://www.proofpoint.com/us/blog/threat-insight/malware-masquerades-privacy-tool

## 1. Source identity

- AnnoCTR report ID: `proofpoint_2021-07-01_malware-masquerades-privacy-tool`
- Official AnnoCTR source text: `AnnoCTR/all/text/proofpoint_2021-07-01_malware-masquerades-privacy-tool.txt`
- Official source-text Git blob: `c5bce2c745b83ab1bb650f4f22b94cf67fe41499`
- Frame `source_text_sha256`: `b3653c517baef27621db962ef305875e6d71ee44e40403d0892e22fe5e76e517`
- The canonical publisher page confirms the title and publication date. The article describes a privacy-themed malware-distribution campaign.

## 2. Proposed scope structure

**Candidate scope:** the Privacy Tools malware-distribution campaign described in this report.

**Candidate parent unit:** one report-local `activity_episode` representing the described download/infection chain.

The report describes the initial Smoke Loader download and a subsequent follow-on malware download. It does not identify a named victim host or a specific execution timestamp. The distinction between two atomic event leaves inside one campaign episode and a single broader activity episode is therefore the main reviewer decision.

## 3. Candidate activity units

| Candidate ID | Proposed description | Candidate role / granularity | Source evidence pointer | Current disposition |
|---|---|---|---|---|
| `PT-E01` | Initial delivery/download of Smoke Loader through the fake Privacy Tools site. | Candidate `event_leaf` / `atomic_event`, nested under the campaign episode. | Source-text character offsets `2518–2611`. | Candidate only; resolve whether this describes a distinct report-local occurrence rather than generic chain behaviour. |
| `PT-E02` | Subsequent download of follow-on data-stealing malware by the Smoke Loader infection. | Candidate `event_leaf` / `atomic_event`, nested under the same episode. | Source-text character offsets `2784–2933`. | Candidate only; exact payload identity/co-occurrence is not resolved. |

The sentence at offsets `2934–3011` lists RedLine and Raccoon Stealer as second-stage payloads. It does not establish that both were installed in the same host infection, or provide an order between them. Do not create separate event leaves for those two malware families from this sentence alone.

The report also mentions related samples shared by other researchers. Those samples are not additional report-local executions in this candidate chain and should not become extra event leaves without their own report-specific evidence and scope.

## 4. Candidate temporal relation

| Field | Candidate value |
|---|---|
| Endpoints | `PT-E01` → `PT-E02` |
| Relation label | `BEFORE` |
| Relation basis | `direct_source` |
| Evidence scope | `CROSS_SENTENCE` |
| Relation evidence pointer | Source-text character offsets `2784–2933`; read with the initial-payload evidence at `2518–2611` |
| Temporal certainty | Source directly describes the second download as subsequent to the initial Smoke Loader delivery. |
| Event-time timestamp | None supplied for either download. Do not convert the 1 July 2021 publication date into an attack time. |

This is a candidate source-grounded ordering claim. It enters the primary temporal graph only if the reviewer resolves both endpoints as distinct, resolved atomic event leaves in a compatible comparison scope.

## 5. Candidate mapping

The report does not explicitly state an ATT&CK technique ID for either candidate event. The following is therefore an analyst mapping candidate, not a report-explicit mapping:

| Candidate event | Exact ID candidate | v12.1 technique name | Parent / A_120 status | Mapping disposition |
|---|---|---|---|---|
| `PT-E01` | No accepted ID yet. `T1189` (Drive-by Compromise) and `T1204` (User Execution) are possible concepts to check, but the source describes a user downloading a fake privacy tool; it does not explicitly describe browser exploitation on site visit or the user opening/executing the downloaded file. | — | Both parent IDs occur in A_120, but membership does not establish that either mapping applies. | `UNRESOLVED`; do not promote either candidate without source support. |
| `PT-E02` | `T1105` | Ingress Tool Transfer | Top-level; parent `T1105`; present in pinned `A_120`. | `source_supported_analyst_candidate`; `UNRESOLVED` pending reviewer acceptance. |

The v12.1 crosswalk maps top-level `T1105`, `T1189` and `T1204` to themselves, and all three parent IDs are in `A_120`. This establishes vocabulary compatibility only. It does not establish semantic correctness of any candidate mapping. The source-grounded mapping judgment still requires review.

## 6. What this could show — and what it cannot show yet

The source provides a candidate `BEFORE` relation between the initial Smoke Loader delivery and the later follow-on malware download. It does **not** currently establish a same-technique pair: `PT-E01` has no accepted mapping, while `T1105` is only a candidate for `PT-E02`. Do not claim within-technique temporal incidence or a projection omission from this draft.

If a reviewer later accepts a source-supported parent mapping for `PT-E01`, recompute the shared-technique opportunity from the complete accepted mapping sets. Even then, do not classify the edge as fully omitted until all accepted mappings for both endpoints are known; distinct technique pairs may still be retained.

## 7. Reviewer decisions to resolve

1. Does this report support two distinct report-local atomic event occurrences, or should the two stages remain descriptions within one broader activity episode?
2. Is the campaign scope sufficiently explicit and compatible for the two candidate endpoints?
3. Is there enough source evidence to map the initial lure-site download to an ATT&CK technique at all? Does the follow-on malware transfer support `T1105` under the pinned v12.1 mapping rules?
4. Are RedLine and Raccoon alternative examples of follow-on payloads for this chain, rather than two separately evidenced event instances? The current source wording supports keeping them together as unresolved payload identities.
5. Keep attack-event timestamps unknown; publication date is not event time.

**No row from this draft has been entered into the canonical annotation registers. No numerator, denominator, prevalence rate, projection metric or research finding is derived from it.**
