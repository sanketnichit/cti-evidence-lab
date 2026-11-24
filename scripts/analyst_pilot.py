"""Generate counterbalanced analyst packets and score protocol responses."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.investigate_sequence import load_case, profile_graph
from src.sequence_investigation import investigate

# Each report contributes support, mapping uncertainty, and two negative items.
TASKS = {
    "rdp": (
        ("R1", "proposed_cleanup_full_edges", ("T1021", "T1021", "T1070")),
        ("R2", "unresolved_cleanup", ("T1021", "T1021", "T1070")),
        ("R3", "proposed_cleanup_full_edges", ("T1021", "T1021", "T1021")),
        ("R4", "proposed_cleanup_local_edges", ("T1021", "T1070", "T1070")),
    ),
    "domain-controller": (
        ("D1", "core_transfer_execution", ("T1021", "T1570", "T1218")),
        ("D2", "archive_mapping_withheld", ("T1059", "T1560", "T1059")),
        ("D3", "extended_script_sequence", ("T1560", "T1059", "T1560")),
        ("D4", "core_transfer_execution", ("T1218", "T1570", "T1021")),
    ),
}
GROUPS = {
    "A": (("rdp", "technique"), ("domain-controller", "occurrence")),
    "B": (("rdp", "occurrence"), ("domain-controller", "technique")),
    "C": (("domain-controller", "occurrence"), ("rdp", "technique")),
    "D": (("domain-controller", "technique"), ("rdp", "occurrence")),
}


def packet(group):
    lines = [
        f"# Sequence review · packet {group}", "",
        "For each question, look for three distinct actions connected by two supplied BEFORE relations. "
        "Use only the retained interpretation for that question. An unknown label can take any queried technique. "
        "A technique pair can occur more than once, and two pairs with a shared label may come from different actions.", "",
        "Choose **SUPPORTED** if the supplied interpretation establishes the chain, **UNRESOLVED_MAPPING** if "
        "a connected chain could match through unknown mappings, or **NOT_SUPPORTED** if neither applies. "
        "Choose **CANNOT_TELL** if the view gives you insufficient information or you cannot decide. "
        "When you choose SUPPORTED or UNRESOLVED_MAPPING, give the two relation IDs for one witness. "
        "Leave relation IDs empty for the other responses.", "",
        "Work in packet order. Complete each question before proceeding. Use the supplied views and notes only.", "",
    ]
    key = {}
    for case_key, view in GROUPS[group]:
        case = load_case(case_key)
        evidence = {row["evidence_id"]: row for row in case["evidence"]}
        lines.extend([f"## {case['source']['title']}", "", f"View: **{view}**", ""])
        for task_id, profile_name, query in TASKS[case_key]:
            _, nodes, mappings, relations = profile_graph(case, profile_name)
            answer = investigate(mappings, relations, query)
            relations = sorted(relations, key=lambda row: row["relation_id"])
            aliases = {row["relation_id"]: f"L{i}" for i, row in enumerate(relations, 1)}
            action_ids = {event_id: f"A{i}" for i, event_id in enumerate(sorted(nodes), 1)}
            witnesses = answer["known_witnesses"] if answer["status"] == "SUPPORTED" else answer["unresolved_witnesses"]
            key[task_id] = {"view": view, "status": answer["status"],
                            "witnesses": [sorted(aliases[r] for r in w["relation_ids"]) for w in witnesses]}
            lines.extend([f"### {task_id} · {' → '.join(query)}", "",
                          f"Retained actions: {len(nodes)}. Unknown mappings: {sum(not labels for labels in mappings.values())}.", ""])
            if view == "occurrence":
                lines.extend(f"- `{alias}` · {', '.join(sorted(mappings[event_id])) or 'unknown'}"
                             for event_id, alias in action_ids.items())
                lines.append("")
                for row in relations:
                    lines.append(f"- `{action_ids[row['source_event']]}` → `{action_ids[row['target_event']]}` · `{aliases[row['relation_id']]}`")
            else:
                projected = defaultdict(list)
                for row in relations:
                    for pair in product(mappings[row["source_event"]], mappings[row["target_event"]]):
                        projected[pair].append(aliases[row["relation_id"]])
                lines.extend(f"- {left} → {right} · {', '.join(sorted(ids))}"
                             for (left, right), ids in sorted(projected.items()))
                if not projected:
                    lines.append("No technique pairs with two known labels.")
            lines.extend(["", "Relation locators (publisher narrative paragraph numbers)", ""])
            for row in relations:
                paragraphs = sorted({evidence[e]["paragraph_number"] for e in row["evidence_ids"]})
                lines.append(f"- `{aliases[row['relation_id']]}` · {', '.join(map(str, paragraphs))}")
            lines.append("")
    return "\n".join(lines), key


def response_template(group, key):
    return {"packet": group, "responses": [
        {"task": task, "status": "", "relation_ids": []} for task in key
    ]}


def score(response):
    _, key = packet(response["packet"])
    rows = response["responses"]
    if [row["task"] for row in rows] != list(key):
        raise ValueError("Response tasks must appear exactly once in assigned packet order")
    results = []
    for row in rows:
        target = key[row["task"]]
        status = row["status"]
        ids = row["relation_ids"]
        if status not in {"SUPPORTED", "UNRESOLVED_MAPPING", "NOT_SUPPORTED", "CANNOT_TELL"}:
            raise ValueError(f"Invalid status for {row['task']}")
        if (not isinstance(ids, list) or any(not isinstance(i, str) or not i.strip() for i in ids)
                or len(ids) != len(set(ids)) or len(ids) > 2):
            raise ValueError(f"Expected zero to two unique relation IDs for {row['task']}")
        if status in {"NOT_SUPPORTED", "CANNOT_TELL"} and ids:
            raise ValueError(f"Relation IDs must be empty for {status}")
        correct = status == target["status"]
        results.append({
            "task": row["task"], "view": target["view"], "expected": target["status"],
            "status_correct": correct, "cannot_tell": status == "CANNOT_TELL",
            "unsupported_positive": status == "SUPPORTED" and target["status"] == "NOT_SUPPORTED",
            "unresolved_called_supported": status == "SUPPORTED" and target["status"] == "UNRESOLVED_MAPPING",
            "status_and_witness_correct": correct and sorted(ids) in target["witnesses"] if target["witnesses"] else None,
        })
    return {"packet": response["packet"], "items": results}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build", type=Path, metavar="DIRECTORY")
    mode.add_argument("--score", type=Path, metavar="RESPONSE")
    args = parser.parse_args()
    if args.score:
        print(json.dumps(score(json.loads(args.score.read_text(encoding="utf-8"))), indent=2))
        return
    args.build.mkdir(parents=True, exist_ok=True)
    for group in GROUPS:
        body, key = packet(group)
        (args.build / f"packet-{group}.md").write_text(body, encoding="utf-8")
        write_json(args.build / f"response-{group}.json", response_template(group, key))
    print("Generated four packets and response templates.")


if __name__ == "__main__":
    main()
