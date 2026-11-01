# Pilot Sampling Plan v0.1

**Status:** Draft selection protocol for a feasibility pilot. It is not a population-sampling plan and cannot support prevalence estimates.

## 1. Why this plan exists

The pilot should test whether the protocol can be applied consistently across different CTI report styles. It must not select reports simply because they appear to contain the desired same-technique temporal relations. Repeated technique-link mentions are screening locators, not event-instance labels.

AnnoCTR reports five donor sources in its cybersecurity-specific layer: Intel471, Lab52, Proofpoint, QuoIntelligence and ZScaler. The corpus paper reports 120 cybersecurity-specific reports across those sources. See the [AnnoCTR LREC-COLING paper](https://aclanthology.org/2024.lrec-main.103/) for the corpus description and donor distribution.

## 2. Eligibility checks before selection

A report is eligible only when:

1. The source text and report-level MITRE-link file are both present and readable.
2. A stable report identifier and a hash of the exact source text can be recorded.
3. Its provenance and the applicable rights/terms are sufficiently clear for the intended research use. A corpus-level licence statement alone does not replace per-report source/provenance review.
4. It is not a duplicate, syndicated copy or near-duplicate of another selected report. Check titles, dates, vendor/source URLs and text similarity before freezing the sample.
5. The report is in the language and scope declared by the study.

TimeML availability and TIMEX3 counts are useful inventory fields, but **they are not eligibility requirements** and do not establish event-to-event temporal relations. The five TimeML files already inspected contained no EVENT, MAKEINSTANCE or TLINK tags.

## 3. Feasibility pilot: 5–8 reports

Use a deliberately mixed pilot:

- **Base coverage:** aim for one eligible report from each of the five donor sources. If a source has no report passing the eligibility checks, record the reason rather than silently replacing it with an unverified report.
- **Additional reports:** if using 6–8 reports, add up to three reports from different donors where possible, chosen to exercise different annotation challenges (for example, repeated technique-link mentions, longer cross-sentence narratives, or sparse/ambiguous temporal information).
- **Do not impose a positive-edge quota.** A report with no explicit positive temporal relations is a valid pilot outcome.
- **Do not select on the outcome.** Do not choose a report because a reviewer already believes it contains same-technique temporal edges.
- **Record selection type:** mark each report as BASE_STRATIFIED, PURPOSIVE_STRESS, or INITIAL_DRY_RUN. Do not combine these types silently in later analysis.

For reports within a stratum, use a recorded random seed or a documented deterministic rule to select from the eligible pool. Do not simply take the report with the largest repeated-technique count. Keep the candidate inventory and selection decisions locally.

## 4. Treatment of Report 01

intel471_2020-03-26_analysis-of-an-attempted-attack is an **initial dry-run candidate**, not a confirmed member of the formal pilot. It was shortlisted because the first convenience screen showed repeated technique-link mentions and the source text contains a candidate explicit temporal cue. Since it was chosen after inspecting those signals, it must not be presented as randomly selected or used alone to estimate relation prevalence.

Before freezing it into the sample:
- review the provenance workbook and source rights;
- check for duplicates/near-duplicates;
- independently read the full report and complete the annotation pass;
- record annotation time and all unresolved decisions.

## 5. What the pilot can and cannot answer

The pilot can assess:
- whether event mentions can be resolved into report-local event instances;
- whether ATT&CK mappings can be independently supported by source evidence;
- whether explicit temporal relations can be annotated with evidence spans;
- which label definitions are ambiguous or costly;
- whether the workflow and CSV validator are usable.

The pilot **cannot** establish:
- how common same-technique temporal relations are across CTI reports;
- that the research gap is novel or important in the wider CTI literature;
- model performance or generalization;
- representative vendor-level prevalence.

## 6. Gate after the pilot

Proceed to a larger descriptive study only after reviewing annotation consistency, evidence quality, report rights, duplicate handling, and annotation cost. The larger study needs its own report-level sampling frame, stratification/weights where appropriate, and pre-specified analysis. Do not reuse this small purposive feasibility sample as if it were representative.

If repeated event instances or explicit temporal relations are rare, ambiguous, or too costly to annotate reliably, narrow or abandon the question rather than relaxing the definitions after seeing the results.
