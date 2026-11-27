"""Explain why a pooled witness belongs to no recorded interpretation."""
import argparse
import json
from collections import Counter
from itertools import combinations, combinations_with_replacement
from pathlib import Path

from examples.profile_coherence import ROOT, finite_profiles, witness_masks

RESULTS = ROOT / "research/experiments/profile_coherence_v0.2/conflict_results.json"


def witness_facts(path, query):
    return (("before", *path[:2]), ("before", *path[1:]),
            *(("label", node, label) for node, label in zip(path, query)))


def contains(profile, fact):
    mappings, edges = profile
    kind, first, second = fact
    return (first, second) in edges if kind == "before" else second in mappings.get(first, ())


def explain(profiles, path, query):
    facts = witness_facts(path, query)
    coverage = [set(i for i, profile in enumerate(profiles) if contains(profile, fact)) for fact in facts]
    if any(not members for members in coverage) or set.intersection(*coverage):
        raise ValueError("Expected a pooled witness with no supporting profile")
    for size in range(2, len(facts) + 1):
        cores = [indexes for indexes in combinations(range(len(facts)), size)
                 if not set.intersection(*(coverage[i] for i in indexes))]
        if cores:
            return {
                "facts": [{"kind": kind, "arguments": [first, second],
                           "profiles": [i + 1 for i in sorted(members)]}
                          for (kind, first, second), members in zip(facts, coverage)],
                "minimum_size": size,
                "minimum_conflicts": [[i + 1 for i in core] for core in cores],
            }
    raise AssertionError("An incompatible full witness must contain a conflict")


def finite_check():
    counts = Counter()
    for profiles in combinations_with_replacement(finite_profiles(), 2):
        for (path, query), mask in witness_masks(profiles).items():
            if mask:
                continue
            result = explain(profiles, path, query)
            facts = witness_facts(path, query)
            # With two profiles, a pooled false witness must have a fact
            # exclusive to each profile. Compare against all such fact pairs.
            expected = [[a + 1, b + 1] for a, b in combinations(range(5), 2)
                        if all(not (contains(profile, facts[a]) and contains(profile, facts[b]))
                               for profile in profiles)]
            if result["minimum_conflicts"] != expected or result["minimum_size"] != 2:
                raise AssertionError("Conflict explanation differs from direct pair enumeration")
            counts[str(result["minimum_size"])] += 1
    return dict(counts)


def omit_one_controls():
    path, query = ("u", "v", "w"), ("A", "B", "C")
    facts = witness_facts(path, query)
    controls = {}
    for size in (3, 4, 5):
        profiles = []
        for omitted in range(size):
            labels = {node: set() for node in path}
            edges = set()
            for i, (kind, first, second) in enumerate(facts):
                if i == omitted:
                    continue
                if kind == "before":
                    edges.add((first, second))
                else:
                    labels[first].add(second)
            profiles.append((labels, edges))
        if witness_masks(profiles).get((path, query)) != 0:
            raise AssertionError("The designed witness should exist only in the pool")
        result = explain(profiles, path, query)
        if result["minimum_conflicts"] != [list(range(1, size + 1))]:
            raise AssertionError("Expected exactly the first facts to conflict")
        controls[str(size)] = result
    return controls


def run():
    return {"finite_minimum_size_counts": finite_check(), "omit_one_controls": omit_one_controls()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    elif result != json.loads(RESULTS.read_bytes()):
        raise SystemExit("Profile conflict explanations differ from the recorded results")
    else:
        print("Reproduced minimum conflicts for pooled witnesses.")


if __name__ == "__main__":
    main()
