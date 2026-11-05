# Research Decision Log

## 2026-11-01 — Initial direction: CTI evidence and ATT&CK mapping

**Status:** Superseded as the main research question; retained as a possible component.

**Reasoning:** Sentence-level evidence mining and ATT&CK mapping are active research areas, including TRAM, CSEM-CTI, and SMAH-CTI. A generic mapper is insufficiently differentiated.

## 2026-11-01 — Refined direction: temporal CTI relations

**Status:** Superseded as the full research question; retained as the domain and baseline.

**Reasoning:** ChronoCTI already predicts temporal relations between ATT&CK technique pairs and constructs technique-node graphs.

## 2026-11-01 — Current candidate: event-instance granularity

**Decision:** Investigate how much temporal structure is lost when report-local action occurrences are collapsed into ATT&CK technique nodes.

**Reasoning:** A technique is an abstract taxonomy concept, whereas an incident report can describe multiple distinct occurrences of the same technique and multiple mentions of one occurrence. ChronoCTI defines its task over technique pairs, making this a clear representation difference to test.

**Caveat:** Event mention graphs and event coreference are established general NLP topics. A CTI-specific contribution is not established until the literature, annotation pilot, and data comparison support it.

## 2026-11-01 — Corrected ChronoCTI data-availability note

**Decision:** Treat the ChronoCTI Figshare version 3 record as a public data-access route, as explicitly linked in the paper's Data Availability section.

**Correction:** An earlier internal note said the Figshare item appeared private. That note is superseded. Actual files, version metadata, and per-artifact licence must still be inspected before reuse.

## 2026-11-01 — Dataset-driven stop gate

**Decision:** Run a 5–8 report annotation pilot before model development.

**Reasoning:** The research depends on whether separate event occurrences and event coreference can be distinguished consistently, and whether there are enough repeated techniques and temporal relations to evaluate.

## Open questions

- What exactly is in ChronoCTI Figshare v3, and how are its data files licensed?
- How often do reports contain multiple distinct instances of the same technique?
- Can annotators reliably separate different event occurrences from repeated mentions of the same event?
- Does AnnoCTR contain full texts and usable span/time annotations for the candidate reports?
- Can SMAH-CTI Action spans be paired with underlying full reports under its CC BY-NC licence?
- Is a second independent annotator available for the pilot?


## 2026-11-05 — AnnoCTR source permissions and derivative material

**Decision:** Use the five fixed rank-one AnnoCTR candidates for local research annotation and derivative publication under the dataset's CC BY-SA licence, subject to attribution and ShareAlike, on the basis of the dataset maintainer's written clarification received 5 November 2026.

**Boundary:** The response was qualified by the maintainer's recollection and was not legal advice; it did not provide a report-level exception list. Keep raw reports and extended verbatim excerpts out of Git. The repository MIT licence applies to project software, not source reports or adapted annotation material. See `research/rights/AnnoCTR_Research_Use_Permission_Clarification_v0.1.md`.

## 2026-11-05 — Two no-CyNE documents outside the CTI-report scope

**Decision:** Mark `proofpoint_2021-05-24_compromised-cloud-accounts-cost-firms` and `quoteintelligence_2020-07-09_what-is-tiber-eu-and` as `INELIGIBLE` for the declared CTI-report source scope. Retain both in the historical 120-report manifest and exclude them from `N_eligible`.

**Reasoning:** The first is a sponsored survey summary; the second is a framework explainer. Neither reports a report-local observed intrusion, actor operation, campaign or activity sequence. Missing CyNE/ATT&CK rows are not the exclusion rationale. The six other no-link reports are not excluded on this basis.

## 2026-11-05 — Adopted annotation controls for the AnnoCTR feasibility draft

**Decision:** Adopt explicit evidence-scope criteria, source-evidence-based mapping acceptance and alternative handling, prior-exposure coding, and a non-exhaustive candidate-pair negative protocol. The researcher's future pass on the five previously reviewed rank-one candidates is `AI_EXPOSED`; an independent second human reviewer is the only route to an unexposed overlapping pass, provided they have not seen prior per-report interpretations.

**Boundary:** These are annotation controls, not annotations. Protocol v0.5-draft is a new draft, not recovered v0.4.1; RECON v0.1 is not the original v0.4.2 schema and remains unapproved.
