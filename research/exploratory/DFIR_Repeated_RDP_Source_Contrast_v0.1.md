# Repeated RDP attempts: exploratory source contrast

**17 November 2026 — method-development example, not accepted annotation.**

**18 November follow-up:** A [source-bound exploratory case](../case_studies/dfir_rdp_v0.1/README.md) now records the occurrence interpretation, three exact passage bindings and outcome/mapping sensitivities. This earlier conditional example is retained as history. Neither record is a formal selected-final annotation or part of the AnnoCTR sample.

**Source:** The DFIR Report, [A Truly Graceful Wipe Out](https://thedfirreport.com/2023/06/12/a-truly-graceful-wipe-out/), 12 June 2023. Refer to the **Case Summary**, paragraphs describing the temporary Remote Desktop Users account, the attempted tunneled RDP connection, its removal after approximately 15 minutes, and a second unsuccessful attempt. The Command and Control section contains a separate network-signature observation: that is not automatically a third attempt.

## Reason for using this case

The central project question concerns distinct attack occurrences that map to the same ATT&CK technique. Unlike the five fixed AnnoCTR feasibility reports, this previously discussed source explicitly describes two attempts separated by account removal and recreation. It therefore offers a useful challenge for event identity and ordered-relation definitions. It is **not** an independently selected or blinded test case.

| Candidate | Description based on the Case Summary | Remaining checks |
|---|---|---|
| RDP-1 | First unsuccessful attempted tunneled RDP connection | Evidence offsets, incident scope and relation to later mentions |
| RDP-2 | Second unsuccessful attempted tunneled RDP connection | Confirm distinct identity and do not count a restatement as another attempt |
| RDP-1 BEFORE RDP-2 | Source explicitly gives an intervening removal and repetition | Preserve exact source evidence and confirm comparison scope |
| ATT&CK mapping | Candidate T1021.001 (RDP) maps to parent T1021 in pinned v12.1 crosswalk | Assess each source-backed mapping independently before acceptance |

The source does not say either RDP attempt succeeded, nor does a 15-minute account lifetime establish a precise event timestamp. T1021 is a technique concept and cannot identify either individual attempt. The pinned crosswalk establishes taxonomy compatibility, not the correctness of an annotation.

## Conditional projection

From the repository root run:

```bash
python -m examples.exploratory_rdp_projection
python -m unittest tests.test_exploratory_rdp_projection -v
```

If the report supports two accepted distinct RDP event leaves, a shared resolved incident scope, the direct BEFORE relation and accepted A_120 T1021 mappings for both, the pure projection module returns:

- 2 distinct event occurrences and 1 positive temporal event relation;
- 1 diagonal T1021→T1021 mapping combination;
- 0 edges in a graph restricted to **distinct technique pairs**.

This is a mathematical consequence of the stated projection rules, **not** a measured finding on the project data. A graph model allowing technique self-loops or retaining event provenance is a different comparison target. No claim is made about the published ChronoCTI model's prediction for this report.

## Safeguards

Do not add this case to AnnoCTR's five-report sample, report-level denominators, IAA calculations or prevalence claims. The example has been discussed previously and cannot count as blind independent annotation. The original report must be frozen, source offsets checked, rights considered, and all event, mapping and temporal decisions independently completed before anyone could treat a record as a real study annotation.

**Status:** exploratory only; no new human labels or real-report projection results.
