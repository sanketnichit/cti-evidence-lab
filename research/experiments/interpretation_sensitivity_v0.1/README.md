# Sensitivity to source interpretation

This experiment asks which answers depend on individual assertions in the two recorded incident cases. It starts from the parent-level interpretation with proposed cleanup mappings and all supplied RDP relations, and the extended script interpretation for the domain-controller case. Both are conditional baseline graphs. Each case keeps its baseline query vocabulary fixed so an intervention cannot remove a question from the denominator.

Generate every single intervention and every unordered pair of compatible interventions from three rules:

- Omit one supplied ordering relation.
- Withhold one occurrence's known mapping while retaining the action and its ordering. Any query label may fill the unknown under the open completion rule.
- Exclude one occurrence and its incident relations to model a stricter reading of action eligibility.

Excluding an occurrence makes withholding its mapping or independently omitting an incident relation redundant, so those pairs are skipped. Counts are by intervention, even when different interventions yield the same remaining graph. The design measures loss of recorded evidence. The next experiment measures addition, substitution and identity merge separately.

## Results

| Conditional baseline | Queries per scenario | Single interventions | Paired interventions | Supported baseline queries | Unsupported baseline loop-projection answers |
|---|---:|---:|---:|---:|---:|
| RDP with proposed cleanup mappings | 8 | 12 | 54 | 3 | 2 |
| Extended domain-controller script sequence | 125 | 17 | 120 | 4 | 1 |

Each of the 203 scenarios removed support for at least one baseline query. In the 10 single mapping withdrawals, all 21 affected supported query instances became unresolved. In the nine single relation omissions and ten single occurrence exclusions, all 35 affected supported query instances became unsupported in the retained graph. These counts concern repeated alternatives over two interpretations. They describe neither independent reports nor observed error frequencies.

The ordinary loop-preserving projection still returns the archive → script → archive query after omitting any one of B1, B2 or B3. Those relations belong to the earlier part of the graph. Omitting B4 or B5 removes the projected answer, and both omissions also remove support for the real script → archive → script query. The same accepted pair edges can therefore be necessary for a supported query and sufficient for a misleading projected query.

Withholding the mapping of the earlier execution occurrence (`execute_beacon`) leaves B4 and B5 intact, so archive → script → archive is still returned by the projection. It becomes unresolved under the open rule because a different connected path can match if that earlier occurrence receives the archive label. The original projected join is still incompatible. The status change reflects a possibility introduced by a permissive completion assumption. It does not establish that the alternative label is plausible or that the original join is warranted.

## Reproduction

```sh
python -m examples.interpretation_sensitivity --output outputs/interpretation_sensitivity.json
python -m examples.interpretation_sensitivity --summary --output outputs/interpretation_sensitivity_summary.json
```

[Committed results](results.json) group scenarios by intervention family. The detailed output identifies the relation or occurrence changed and includes all three-way status transitions, support losses and outcomes for the original unsupported projected queries. Full study reproduction checks the committed counts and packages the detailed output. Each run checks that removing evidence creates neither a new confirmed witness nor a new ordinary projected answer.

## Sensitivity to incorrect or extra assertions

Use the same two complete baseline profiles and change one assertion at a time. Enumerate every missing directed ordering edge, every substitution of a known label with a different label from the baseline vocabulary, and every merge of two actions with the same label. A merge redirects all incident relations to the retained identity. Keep self-loops during validation so that collapsing ordered actions cannot silently erase their contradiction. Reject cyclic graphs before query scoring.

Use two references. The baseline graph determines which queries gain or lose support under the edit. The edited graph determines which answers each representation preserves on the supplied input. A newly supported answer here is new relative to the recorded baseline. For example, an added edge may follow by transitivity but still falls outside the baseline's supplied-edge query. These interventions model possible input faults and do not assume that the baseline is independent ground truth.

| Edit | Candidates | Acyclic and scored | Scenarios gaining support | New / lost supported instances |
|---|---:|---:|---:|---:|
| Add one ordering link | 33 | 12 | 9 | 12 / 0 |
| Substitute one mapping | 28 | 28 | 28 | 54 / 57 |
| Merge same-label actions | 3 | 0 | Unassessed | Unassessed |

The loop-preserving endpoint join agrees with the edited occurrence oracle in every scored scenario. It therefore keeps all 66 newly supported instances relative to the baseline. Four of these instances were previously returned only by ordinary loop traversal. For example, assigning the archive label to the earlier execution action in the domain-controller graph makes the previously unsupported archive-script-archive query gain a connected witness. The edit changes the reference evidence and therefore changes how the same technique sequence is judged.

All three same-label merges in the incident profiles collapse ordered actions and create cycles. The synthetic counterexample from the manuscript provides an acyclic merge control. Merge the two unrelated middle actions with label B in A → B and B → C. The resulting graph passes validation and now supports A → B → C even with endpoint joins. The control shows why structural validation cannot replace source review of action identity. The two incident graphs supply no evidence about the frequency of acyclic merges.

```sh
python -m examples.interpretation_error_study --summary --output outputs/input_error_summary.json
python -m examples.interpretation_error_study --output outputs/interpretation_input_errors.json
```

Full reproduction compares the [committed summary](input_error_results.json) and packages all scenario details. The result describes two conditional baseline profiles and one synthetic control.
