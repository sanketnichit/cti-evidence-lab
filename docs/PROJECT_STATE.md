# Study status

**Updated: 25 November 2026. Research in progress.**

CTI Evidence Lab evaluates temporal-edge retention and connected-sequence query fidelity under technique-level projection. The evidence comprises controlled experiments, three separate five-report AnnoCTR reviews, four DFIR incident cases, two CISA advisories and a two-entry Microsoft series sample. The [research manuscript](../research/FEASIBILITY_REPORT_v0.1.md) presents results and limits together.

## Available evidence

| Component | Current result | Boundary |
|---|---|---|
| Representation controls | Seven deterministic comparisons and a 4,096-graph edge-state/cycle check | Synthetic inputs |
| Connected-sequence queries | Four representations; 5,184 singleton and 4,096 set-valued mapping graphs | Fidelity to supplied graphs, not extraction accuracy |
| AnnoCTR source inventory | 400-report inventory; fixed 120-report cybersecurity frame | Annotation counts are not occurrence counts |
| Fixed feasibility cohort | Five rank-one donor candidates with recorded interpretations and counterarguments | No independently validated occurrence-pair dataset |
| Fixed source extension | Five rank-two reports; all texts read and 22 additional passage bindings verified | No qualifying primary three-occurrence sequence established; query errors unassessed |
| Fixed five-publisher evaluation | Rank-three selection frozen before review; 17 verified bindings; four conditional procedure graphs, 70 queries | No qualifying primary incident sequence; no accuracy advantage on decidable queries |
| Source audit | 120 identities, 33 pilot pointers and 22 critical-review passages checked | Hash identity does not establish semantic correctness |
| RDP case | Two provisional attempt-level occurrences, one BEFORE edge, three verified passages | Purposive selection; outside AnnoCTR; only one edge |
| RDP sequence extension | Same intrusion; four actions, four ordering links and seven verified passage bindings | Cleanup mapping unresolved; query comparison conditional on that mapping |
| Second intrusion | Three-action core query; six-action extension, exact-technique comparison and 13 verified bindings | Ordinary success in the core; extended join error conditional on the archive mapping |
| Chronological incident holdout | Two DFIR reports; one agreement case, one with three unsupported ordinary returns | Same-publisher conditional interpretations |
| Independent source review | Answer-free packets and alignment-based descriptive comparison for two returns | Participant returns pending |
| CISA extension | Two advisories; one unassessed, one with three unresolved loop returns | Purposive search frame |
| Microsoft series prefix | One report unassessed from the prose and one publisher link pointing to a different installment | One accessible selected report |
| Runtime and output cost | 16 scaling workloads and 16 repeated-label workloads with exact witness and join counts | Synthetic graphs and single-machine timing |
| Answer-index storage | Exact known-label encodings compared on 19 synthetic workloads and 12 recorded profiles | Compact JSON sizes for a fixed query |
| Interpretation sensitivity | 203 evidence-removal scenarios and 40 acyclic input-error edits | Constructed changes to two incident graphs |
| Investigation prototype | Six offline case records, 5,454 query combinations across five assessable cases, and Chromium, Firefox and WebKit checks at three viewport widths | Safari devices, assistive technology and practical analyst benefit remain untested |
| Mapping-bound sensitivity | Paired open and constrained CLI answers, 21,952 finite query checks, and a frozen discovery-role comparison across three incident graphs | Depends on declared bounds and case query vocabulary |
| Software verification | Five test suites, full reproduction in CI and 31 immutable base-package checksums | Code and artifact integrity |

## Interpretation and sampling

The five AnnoCTR candidates are retained regardless of apparent event yield. Their source review does not establish a qualifying same-technique temporal pair under the current primary rules. Unresolved evidence is not a negative occurrence label or a zero-prevalence estimate.

The separate rank-two extension retains all five additional reports selected by the existing donor order. Selection was committed before this review. Explicit reconnaissance-before-phishing evidence and live sample-analysis execution are retained, but neither resolves a primary three-occurrence intrusion sequence. The original cohort, this extension and the external case are not pooled into a prevalence denominator.

The RDP case uses a separate publisher snapshot and exposed, purposive selection. Its analysis distinguishes attempt-inclusive eligibility, confirmed-success eligibility and withheld mappings. The sequence extension adds two account-removal occurrences from the same intrusion. Its conservative profile has no fully mapped paths and does not assess query errors. Assuming the proposed cleanup mapping permits a conditional comparison of three two-edge paths; the local-edge sensitivity retains two paths that all four representations answer correctly. Neither version contributes a corpus denominator or independent agreement statistic.

## Method and implementation

The working event universe is incident-linked attack-action occurrences. Temporal edges require relation-specific support and compatible incident scope. Primary taxonomy comparisons use the pinned Enterprise ATT&CK v12.1 A_120 parent vocabulary. Narrative order, malware capability lists and dependency edges alone do not establish observed BEFORE relations.

Protocol v0.5 and RECON extensions remain drafts. RECON v0.1 is a reconstructed replacement, not the unrecovered original schema package. Its immutable package files and checksums remain unchanged. The source-bound case records are separate from selected-final annotation partitions and do not bypass annotation locks.

## Open research questions

- How often suitable source narratives support stable occurrence identity, mappings and connected sequence queries remains unmeasured.
- Source comparisons cover DFIR, CISA and Microsoft. Broader sampling and independent interpretation review remain open.
- Independent annotation reliability, population prevalence, learned extraction performance and superiority over published systems are not established.
- The contribution requires continued comparison with existing action-based and temporal graph methods; occurrence graphs themselves are established prior art.

The [methods preprint](https://github.com/sanketnichit/cti-evidence-lab/releases/tag/preprint-v0.1) presents representation fidelity on supplied graphs. Independent agreement and analyst efficacy remain open empirical questions.

[Research artifacts](../research/README.md), [reproduction](REPRODUCIBILITY.md), [research directions](ROADMAP.md), and the versioned method/audit records provide the supporting detail. Earlier status snapshots are historical records; this document summarizes the current study.
