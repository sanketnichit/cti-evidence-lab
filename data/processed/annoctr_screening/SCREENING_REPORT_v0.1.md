# AnnoCTR corpus screening report v0.1

**Screened:** 3 November 2026  
**Input archive SHA-256:** `118549e9ce885559cd0c07a8de42b321892754cc2e4f07fea0230eaefe4cea35`  
**ZIP integrity:** passed  
**Output:** 400 report-level inventory rows; no raw source text copied.

## Manifest-defined frame

The official `splits.tsv` has 400 unique report IDs: 70 train, 16 dev, 34 test and 280 ext. The 120 train/dev/test IDs form the GNE+CyNE sampling frame.

| Donor | GNE+CyNE reports |
|---|---:|
| Intel471 | 30 |
| Lab52 / S2 Grupo | 23 |
| Proofpoint | 28 |
| QuoIntelligence | 12 |
| ZScaler | 27 |
| **Total** | **120** |

## Screening results

- All 400 reports have the expected text, full linking, MITRE-only linking and TimeML files.
- 118/120 GNE+CyNE reports have at least one cybersecurity-specific record in the full `linking/` export.
- 112/120 have at least one valid canonical ATT&CK technique URL in `linking_mitre_only/`.
- Eight GNE+CyNE reports have no valid canonical ATT&CK technique link in that export.
- The two reports with no observed cybersecurity-specific rows in the full linking export are:
  - `proofpoint_2021-05-24_compromised-cloud-accounts-cost-firms`
  - `quoteintelligence_2020-07-09_what-is-tiber-eu-and`
- Across all 400 TimeML files: 3,324 TIMEX3; zero EVENT, MAKEINSTANCE, TLINK or SIGNAL tags.
- No expected paired files were missing.

## Interpretation constraints

The 120-row frame is defined by the official manifest, not by pre-existing ATT&CK-link availability. The 112 figure is descriptive inventory only. Missing AnnoCTR mappings are not automatically negative or UNMAPPED human annotations.

The two no-CyNE-row reports remain in the 120-row inventory while the researcher decides whether their content falls outside the declared CTI-report scope. Their link absence is not itself the exclusion criterion.

TimeML provides time-expression markup here, not event-instance identities or event-to-event temporal gold. Repeated technique mentions are not event counts.

## Files

- `AnnoCTR_Corpus_Screening_v0.1.csv` — full report-level metadata inventory only.
- `screening_summary.json` — archive hash, manifest counts, key aggregates and limitations.

Raw report text is not included in this output.