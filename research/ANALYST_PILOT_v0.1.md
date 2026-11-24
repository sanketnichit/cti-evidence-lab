# Analyst pilot on occurrence identity

Can a reviewer answer a three-technique sequence question more reliably when the view retains individual actions? This pilot compares two displays of the same recorded interpretations. The technique view shows projected pairs, including self-loops and the relation IDs behind those pairs. The occurrence view shows the endpoint identities and mapping state of every retained action. Both show relation IDs and source paragraph locators. Answers are based on the supplied records.

## Task and assignment

Eight fixed questions use two existing intrusion reports. Each report contributes one supported chain, one mapping-dependent chain, one misleading projected answer and one negative control. Each participant gets four questions from each report, sees each report in only one view, and completes one packet. Assign consecutively in rotating groups A, B, C and D, with a randomly chosen starting group. Record the allocation and any deviations. Keep incomplete four-participant blocks visible in the analysis.

| Packet | First block | Second block |
|---|---|---|
| A | RDP, technique | Domain controller, occurrence |
| B | RDP, occurrence | Domain controller, technique |
| C | Domain controller, occurrence | RDP, technique |
| D | Domain controller, technique | RDP, occurrence |

Generate the packets from a clean checkout and record its commit. Give each participant only their packet and matching response template. The script and repository contain the scoring rules and case interpretations, so they should stay outside the participant materials. Record previous exposure and exclude anyone who already knows the task answers from the primary pilot summary. Preserve any such responses in a separate rehearsal log. Use anonymous participant IDs. Record withdrawals and incomplete submissions and report their counts by assignment, without filling in missing answers.

```sh
python scripts/analyst_pilot.py --build outputs/analyst_pilot
python scripts/analyst_pilot.py --score path/to/completed-response.json
```

## Scoring and reporting

Report status correctness, abstentions, unsupported positives, and unresolved answers incorrectly called supported. Score a correct witness only when the status is correct and the two relation IDs match a reference witness. The witness denominator includes all assigned supported and unresolved items in completed packets, including wrong and abstaining responses. The status denominator includes all eight items in each completed packet. Treat CANNOT_TELL as abstention and retain it in the denominator.

Tabulate counts by participant, view, report and block order. Compare the two view scores within each participant, then inspect whether the pattern holds across assignments. Report the achieved participant count and assignment balance. The eight repeated questions share two reports, so pooled item counts do not provide independent observations. A small convenience sample supports a descriptive pilot only. Do not collect timing for this protocol. A timing comparison needs fixed timing instrumentation and a separate protocol.

The answer key is conditional on the two recorded interpretations and the unrestricted mapping rule. The pilot isolates the information exposed by the two views. It does not test source extraction, semantic annotation agreement, custom mapping bounds, or the interactive browser workflow. Participants cannot be blinded to the visible representation. Fixed within-block order can produce learning effects. The chosen cases illustrate known behaviors, so any observed result would need a fresh task set before generalization.

## Current status

Packet generation and scoring have been checked with constructed responses. Participant recruitment and data collection have yet to begin.
