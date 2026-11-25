# Discovery-role mapping sensitivity

Frozen on 25 November 2026 before computing the results below. The published unrestricted case outcomes were already known. This comparison adds one interpretation assumption to the existing graphs and keeps the original results separate.

Use both reports in the chronological DFIR holdout and the assessable CISA advisory AA25-266A. Each case uses its recorded parent-level graph. The other CISA advisory has no assessable sequence in its recorded graph. Use every three-label query from each case's known parent labels, including repetitions. Keep this vocabulary fixed across conditions. The earlier two development cases and the Microsoft and AnnoCTR readings are outside this comparison.

Apply bounds to every withheld action whose recorded identity groups explicitly described discovery behavior. The [frozen specification](discovery_design.json) lists the four occurrences and their source references. The roles come from the recorded incident wording. All other withheld mappings remain open.

For the narrower condition, allow every active parent technique tagged Discovery in the pinned Enterprise ATT&CK v12.1 release. For the broader condition, allow the union of the Discovery and Execution parents to test whether labeling the execution of discovery commands changes the result. An active parent is an attack-pattern object that is neither a sub-technique, revoked, nor deprecated and has the specified tactic in the Enterprise kill chain. Both bounds are conditional assumptions about the interpretation of grouped actions. They do not confirm a technique or split the actions into constituent commands.

Report the unrestricted, broader and narrower status counts separately for each case. Record how many unrestricted unresolved answers become unsupported under either bound. Identify which originally projected unresolved answers change status. Keep the projection's known edges fixed. As a sensitivity check, remove each narrower bound in turn and count how many unresolved answers that removal restores. Check that adding a bound never changes a known witness and that the narrower condition cannot be more permissive than the broader condition.

The comparison measures consequences of assumptions on fixed graphs. The bounded outcomes do not establish the correctness of a tactic bound or provide a population estimate. A change from unresolved to unsupported can reflect an incorrect bound as well as a more plausible reading.
