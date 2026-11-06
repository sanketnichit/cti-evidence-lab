# Event-universe and ChronoCTI comparison boundary — research decision note v0.1

**Prepared:** 6 November 2026  
**Status:** Methodological proposal; researcher approval required.

## 1. The protocol does not currently define an intrusion-only event universe

Protocol v0.5 defines an event instance as a distinguishable report-local occurrence and defines a primary event leaf as a resolved atomic occurrence. It does not expressly restrict event leaves to victim-side intrusion actions. The earlier source-review language that claimed no relation existed between two resolved intrusion event leaves was therefore too narrow to settle whether the report contained any event relation at all.

## 2. Recommended stratification

Keep source-derived units visible, but report them in separate strata:

- **Operational attack-action occurrences:** adversary actions described as part of an attack incident; this is the proposed ChronoCTI-comparable stratum.
- **Threat-actor communications/disclosures:** posts, forum messages, public claims and response blogs. These may be resolved report-local communication occurrences; they are not automatically ATT&CK attack actions.
- **Analyst/sample observations:** detection of a sample, submission to a scanner, reverse-engineering findings. These are analyst-side observations, not adversary actions.
- **Generic capabilities:** malware functions, command handlers and generalized TTPs without a resolved report-local execution. Retain as GENERIC_BEHAVIOUR/unresolved rather than atomic event leaves.

The primary ChronoCTI comparison should use the operational attack-action stratum unless the researcher approves a broader estimand. Communication events may be retained in a parallel report-event layer and their temporal relations described separately. Do not count them as attack-action/ATT&CK projection edges by default.

## 3. Intel471 candidate pair

The pinned source dates a dyadka0220 Babuk source-code post to 3 September 2021 and a Groove response blog to 7 September 2021. This is a source-supported candidate BEFORE relation between two communication occurrences. It should be retained as a candidate relation with direct timestamp evidence and a proposed shared "Babuk fallout public communications" scope.

It is not accepted as a primary attack-action relation and must not be converted into an intrusion chronology. The scope and event-stratum policy remains a researcher decision.

## 4. ChronoCTI label boundary

The ChronoCTI paper defines three positive categories: BEFORE, SIMULTANEOUS-OVERLAP (SIM-OV), and CONCURRENT; NULL denotes no relation. It focuses on attack-action temporal relations and excludes social-media posts, malware features/capabilities and other non-attack content from its CTI report sample.

The draft crosswalk is a proposal only:
- ChronoCTI BEFORE groups BEFORE/AFTER and immediate-before/after relations into a direction-normalized precedence class.
- SIM-OV is close to project OVERLAP and may include SIMULTANEOUS; the exact project SIMULTANEOUS definition needs semantic reconciliation.
- CONCURRENT may correspond to CONCURRENT_UNSPECIFIED only when the source supports independent concurrent actions.
- NULL is not equivalent to a missing pair. Only an actually assessed candidate pair may receive NO_TEMPORAL_CLAIM under a frozen candidate-pair rule.

## 5. Confirmatory versus feasibility design

The fixed five rank-one reports remain a feasibility set. They do not constitute a confirmatory design or support population prevalence. A confirmatory study requires a separately defined sampling frame, inclusion rules aligned with the comparison target, a sample-size rationale and a predeclared analysis plan. Do not convert five-report feasibility results into inferential claims.
