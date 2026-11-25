# Sensitivity to source interpretation

This experiment asks which answers depend on individual assertions in the two recorded incident cases. It starts from the parent-level interpretation with proposed cleanup mappings and all supplied RDP relations, and the extended script interpretation for the domain-controller case. Both are conditional baseline graphs. Each case keeps its baseline query vocabulary fixed so an intervention cannot remove a question from the denominator.

Generate every single intervention and every unordered pair of compatible interventions from three rules:

- Omit one supplied ordering relation.
- Withhold one occurrence's known mapping while retaining the action and its ordering. Any query label may fill the unknown under the open completion rule.
- Exclude one occurrence and its incident relations to model a stricter reading of action eligibility.

Excluding an occurrence makes withholding its mapping or independently omitting an incident relation redundant, so those pairs are skipped. Counts are by intervention, even when different interventions yield the same remaining graph. The design measures loss of recorded evidence. Incorrect added edges, inappropriate occurrence merges, mapping substitutions and source annotation disagreement need separate analyses.

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
