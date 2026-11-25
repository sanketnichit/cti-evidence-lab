"""Reproduce the paired investigator timing and record-equivalence check."""
import argparse
import json
import platform
import random
import subprocess
from itertools import combinations, product
from pathlib import Path
from types import ModuleType

from examples.sequence_scaling import samples_ms, workload
from scripts.investigate_sequence import CASES, load_case, profile_graph
from src.occurrence_queries import source_answers
from src.sequence_investigation import investigate

BASELINE = "95ad3a8f24657ce6971f4c7098ac429c772068a5"


def relation(identifier, source, target):
    return dict(relation_id=identifier, source_event=source, target_event=target, relation="BEFORE")


def require_match(before, mappings, relations, query, domains=None):
    arguments = (mappings, relations, query)
    if before(*arguments, mapping_domains=domains) != investigate(*arguments, mapping_domains=domains):
        raise AssertionError(f"Answer record mismatch for {query!r}")


def check_records(before):
    count = 0
    for name in CASES:
        case = load_case(name)
        for profile in case["profiles"]:
            _, _, mappings, relations = profile_graph(case, profile["name"])
            level = profile.get("taxonomy_level", "parent")
            vocabulary = sorted({n[f"candidate_{level}_mapping"] for n in case["occurrences"]})
            for query in product(vocabulary, repeat=3):
                require_match(before, mappings, relations, query)
                count += 1
    rng = random.Random(835)
    for _ in range(300):
        nodes = [str(i) for i in range(rng.randint(3, 10))]
        mappings = {node: {label for label in "ABC" if rng.random() < 0.4} for node in nodes}
        relations = []
        for source, target in combinations(nodes, 2):
            if rng.random() < 0.4:
                for _ in range(rng.randint(1, 2)):
                    relations.append(relation(f"R{len(relations)}", source, target))
        rng.shuffle(relations)
        query = [rng.choice("ABC") for _ in range(3)]
        domains = {node: {rng.choice("ABC")} for node in nodes if not mappings[node]} or None
        for bounds in (None, domains):
            require_match(before, mappings, relations, query, bounds)
            count += 1
    return count


def measure(before):
    results = []
    for size, shape, width in product((16, 32, 64, 128), ("chain", "hub"), (1, 2)):
        mappings, edges = workload(size, shape, width)
        relations = [relation(f"L{i}", u, v) for i, (u, v) in enumerate(sorted(edges))]
        query = min(source_answers(mappings, edges))
        require_match(before, mappings, relations, query)
        result = dict(occurrences=size, shape=shape, labels_per_node=width, query=query)
        methods = [("before", before), ("after", investigate)]
        if len(results) % 2:
            methods.reverse()
        for label, operation in methods:
            result[label] = samples_ms(lambda: operation(mappings, relations, query), 7)
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    # Load the fixed, previously published implementation for an in-process
    # comparison. The blob is selected by commit ID, independent of user input.
    old = ModuleType("previous")
    source = subprocess.check_output(
        ["git", "show", f"{BASELINE}:src/sequence_investigation.py"], text=True, encoding="utf-8")
    exec(source, old.__dict__)
    result = dict(
        baseline_commit=BASELINE, python=platform.python_version(),
        system=platform.system(), machine=platform.machine(),
        checked_records=check_records(old.investigate), workloads=measure(old.investigate),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="")
    print(f"Matched {result['checked_records']} query records and measured {len(result['workloads'])} workloads.")


if __name__ == "__main__":
    main()
