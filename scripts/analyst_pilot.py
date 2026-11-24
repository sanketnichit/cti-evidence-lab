"""Generate counterbalanced analyst packets and score protocol responses."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from itertools import product
from collections import Counter
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
    for block_order, (case_key, view) in enumerate(GROUPS[group], 1):
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
            key[task_id] = {"view": view, "case": case_key, "block_order": block_order,
                            "status": answer["status"],
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
                lines.append(
                    "UNKNOWN means the technique mapping is unconfirmed, not an accepted ATT&CK ID. "
                    "Rows containing UNKNOWN show relation evidence only, not confirmed technique pairs. "
                    "Occurrence endpoints are deliberately hidden in this view."
                )
                lines.append("")
                projected = defaultdict(list)
                for row in relations:
                    source = mappings[row["source_event"]] or {"UNKNOWN"}
                    target = mappings[row["target_event"]] or {"UNKNOWN"}
                    for pair in product(source, target):
                        projected[pair].append(aliases[row["relation_id"]])
                lines.extend(f"- {left} → {right} · {', '.join(sorted(ids))}"
                             for (left, right), ids in sorted(projected.items()))
                if not projected:
                    lines.append("No retained relation rows.")
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
            "task": row["task"], "view": target["view"], "case": target["case"],
            "block_order": target["block_order"], "expected": target["status"],
            "status_correct": correct, "cannot_tell": status == "CANNOT_TELL",
            "unsupported_positive": status == "SUPPORTED" and target["status"] == "NOT_SUPPORTED",
            "unresolved_called_supported": status == "SUPPORTED" and target["status"] == "UNRESOLVED_MAPPING",
            "status_and_witness_correct": correct and sorted(ids) in target["witnesses"] if target["witnesses"] else None,
        })
    return {"packet": response["packet"], "items": results}



def _metrics(items):
    """Descriptive counts only. Rates belong to the stated assigned denominators."""
    return {
        "assigned": len(items),
        "status_correct": sum(bool(item["status_correct"]) for item in items),
        "cannot_tell": sum(bool(item["cannot_tell"]) for item in items),
        "unsupported_positive": sum(bool(item["unsupported_positive"]) for item in items),
        "unresolved_called_supported": sum(bool(item["unresolved_called_supported"]) for item in items),
        "witness_assigned": sum(item["status_and_witness_correct"] is not None for item in items),
        "status_and_witness_correct": sum(item["status_and_witness_correct"] is True for item in items),
    }


def summarize(responses):
    """Score complete response packets; retain participants as independent units.

    Deliberately requires actual completed files with anonymous IDs. Blank
    generated response templates are not data and cannot produce a summary.
    """
    if not responses:
        raise ValueError("At least one completed participant response is required")
    participants = []
    participant_ids = set()
    all_items = []
    by_packet = Counter()
    for response in responses:
        if not isinstance(response, dict):
            raise ValueError("Each response must be a JSON object")
        identifier = response.get("participant_id")
        if (not isinstance(identifier, str) or not identifier
                or len(identifier) > 64
                or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in identifier)):
            raise ValueError("Each completed response needs an anonymous participant_id (letters, digits, _ or -)")
        if identifier in participant_ids:
            raise ValueError(f"Duplicate participant_id: {identifier}")
        participant_ids.add(identifier)
        scored = score(response)
        group = scored["packet"]
        by_packet[group] += 1
        items = scored["items"]
        views = {view: _metrics([row for row in items if row["view"] == view])
                 for view in ("technique", "occurrence")}
        if any(view["assigned"] != 4 or view["witness_assigned"] != 2 for view in views.values()):
            raise ValueError("Packet design no longer matches the fixed 4+4 tasks and two witness items per view")
        participants.append({
            "participant_id": identifier,
            "packet": group,
            "per_view": views,
            "per_case": {
                case: _metrics([row for row in items if row["case"] == case])
                for case in TASKS
            },
            "per_block_order": {
                str(block): _metrics([row for row in items if row["block_order"] == block])
                for block in (1, 2)
            },
            "occurrence_minus_technique_status_accuracy":
                (views["occurrence"]["status_correct"] - views["technique"]["status_correct"]) / 4,
            "occurrence_minus_technique_witness_accuracy":
                (views["occurrence"]["status_and_witness_correct"] -
                 views["technique"]["status_and_witness_correct"]) / 2,
        })
        all_items.extend(items)

    def aggregate(key, values):
        return {value: _metrics([row for row in all_items if str(row[key]) == str(value)])
                for value in values}

    rotations = min(by_packet.get(group, 0) for group in GROUPS)
    return {
        "analysis_type": "DESCRIPTIVE_ANALYST_PILOT",
        "status": "OBSERVED_RESPONSES_NOT_SOURCE_GOLD",
        "participants": len(participants),
        "packet_balance": {group: by_packet[group] for group in GROUPS},
        "complete_four_packet_rotations": rotations,
        "participants_in_incomplete_rotation": len(participants) - 4 * rotations,
        "overall": _metrics(all_items),
        "by_view": aggregate("view", ("technique", "occurrence")),
        "by_case": aggregate("case", TASKS),
        "by_block_order": aggregate("block_order", (1, 2)),
        "per_participant": participants,
        "limitations": [
            "Convenience sample: no population or analyst-performance superiority inference.",
            "Reference answers are conditional on two previously recorded source interpretations.",
            "Task items are repeated within two reports and are not independent observations.",
            "No timing, source annotation agreement or interactive-browser efficacy is measured.",
            "Only complete eight-task submissions are scored; incomplete cases require separate disclosure.",
        ],
    }


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build", type=Path, metavar="DIRECTORY")
    mode.add_argument("--score", type=Path, metavar="RESPONSE")
    mode.add_argument("--summarize", type=Path, nargs="+", metavar="COMPLETED_RESPONSE")
    args = parser.parse_args()
    if args.summarize:
        print(json.dumps(summarize([json.loads(path.read_text(encoding="utf-8"))
                                    for path in args.summarize]), indent=2))
        return
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
