"""Measure query sensitivity to omitting specified interpretation profiles."""
import argparse
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

from examples.profile_coherence import ROOT, witness_masks
from examples.profile_uncertainty import STATUSES, reference_ranks
from scripts.compare_sequence_profiles import GROUPS, comparison_context

RESULTS = ROOT / "research/experiments/profile_coherence_v0.2/profile_omission_results.json"


def evaluate(profiles):
    names = list(profiles)
    graphs = [
        (mappings, {(row["source_event"], row["target_event"]) for row in relations})
        for mappings, relations in profiles.values()
    ]
    vocabulary = sorted({label for mappings, _ in graphs for labels in mappings.values() for label in labels})
    queries = list(product(vocabulary, repeat=3))
    known, possible = defaultdict(int), defaultdict(int)
    for index, completion in ((known, ()), (possible, vocabulary)):
        for (_, query), mask in witness_masks(graphs, completion_vocabulary=completion).items():
            index[query] |= mask
    reference = [reference_ranks(graph, queries) for graph in graphs]

    def ranks(retained):
        mask = sum(1 << i for i in retained)
        result = {
            query: 2 if known[query] & mask else 1 if possible[query] & mask else 0
            for query in queries
        }
        if result != {query: max(reference[i][query] for i in retained) for query in queries}:
            raise AssertionError("Retained-profile masks disagree with direct per-profile queries")
        return result

    indices = range(len(names))
    baseline = ranks(indices)
    scenarios = []
    first_loss = {}
    for count in range(1, len(names)):
        for omitted in combinations(indices, count):
            retained = [i for i in indices if i not in omitted]
            after = ranks(retained)
            losses = Counter()
            supported_losses = []
            for query, before in baseline.items():
                if after[query] < before:
                    losses[f"{STATUSES[before]} -> {STATUSES[after[query]]}"] += 1
                    first_loss.setdefault(query, count)
                    if before == 2:
                        supported_losses.append({"query": list(query), "remaining_status": STATUSES[after[query]]})
            scenarios.append({"omitted": [names[i] for i in omitted], "status_losses": dict(losses),
                              "supported_losses": supported_losses})
    summary = Counter((STATUSES[before], str(first_loss.get(query, "never"))) for query, before in baseline.items())
    return {
        "query_count": len(queries),
        "profiles": names,
        "minimum_omissions_for_status_loss": {
            status: {count: total for (state, count), total in sorted(summary.items()) if state == status}
            for status in STATUSES[1:]
        },
        "scenarios": scenarios,
    }


def run():
    return {group: evaluate(comparison_context(group)[1]) for group in GROUPS}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    elif result != json.loads(RESULTS.read_bytes()):
        raise SystemExit("Profile omission differs from recorded results")
    else:
        print("Reproduced all nonempty subsets of the three recorded profile groups.")
