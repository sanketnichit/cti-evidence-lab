"""Build a portable offline sequence investigator from verified case records."""
import argparse
import json
import subprocess
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.investigate_sequence import AVAILABLE_CASES, certificate, load_case, profile_graph, record_context
from scripts.compare_sequence_profiles import GROUPS, compare_query, comparison_context


def browser_comparison(group, case, vocabulary):
    """Share blank answers and invariant fields across the offline query index."""
    context, profiles = comparison_context(group, case)
    context["detail"] = "summary"
    blank = compare_query(profiles, ("__absent__",) * 3, summary_only=True)
    del blank["query"]
    for row in blank["profile_answers"].values():
        del row["query"]
    answers = {}
    for query in product(vocabulary, repeat=3):
        answer = compare_query(profiles, query, summary_only=True)
        changes = {field: answer[field] for field in ("best_profile_status", "pooled_status", "pooled_witnesses")
                   if answer[field] != blank[field]}
        profile_changes = {}
        for name, row in answer["profile_answers"].items():
            changed = {field: value for field, value in row.items()
                       if field != "query" and value != blank["profile_answers"][name][field]}
            if changed:
                profile_changes[name] = changed
        if profile_changes:
            changes["profile_answers"] = profile_changes
        if changes:
            answers["|".join(query)] = changes
    return {"context": context, "blank": blank, "answers": answers}


def pooling_control():
    labels = {"u": {"A"}, "v": {"B"}, "w": {"C"}}
    left = {"relation_id": "L", "relation": "BEFORE", "source_event": "u", "target_event": "v"}
    right = {"relation_id": "R", "relation": "BEFORE", "source_event": "v", "target_event": "w"}
    return compare_query({"left_only": (labels, [left]), "right_only": (labels, [right])},
                         ("A", "B", "C"), summary_only=True)


def build(destination):
    cases = []
    for key in AVAILABLE_CASES:
        case = load_case(key)
        profiles = []
        for p in case["profiles"]:
            level = p.get("taxonomy_level", "parent")
            vocabulary = sorted({label for n in case["occurrences"]
                                 if (label := n["candidate_" + level + "_mapping"])})
            answers = {}
            if case.get("query_assessment") == "UNASSESSED":
                vocabulary = []
                common = record_context(key, case, *profile_graph(case, p["name"]))
            else:
                common = None
                for query in product(vocabulary, repeat=3):
                    value = certificate(key, case, p["name"], query)
                    answers["|".join(query)] = {"answer": value.pop("answer"), "certificate_sha256": value.pop("certificate_sha256")}
                    common = value
            profiles.append({"name": p["name"], "level": level, "vocabulary": vocabulary,
                             "common": common, "answers": answers,
                             "exclusions": case.get("exclusions", [])})
        entry = {"key": key, "title": case["source"]["title"], "profiles": profiles}
        group = "netsupport-identity" if key == "dfir-netsupport" else key
        if group in GROUPS:
            vocabulary = next(p["vocabulary"] for p in profiles if p["level"] == "parent")
            entry["comparison"] = browser_comparison(group, case, vocabulary)
        cases.append(entry)
    payload = {"cases": cases, "pooling_control": pooling_control(),
               "repository_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "working_tree_dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).strip())}
    # JSON remains inert even if a future source title contains an HTML closing tag.
    serialized = json.dumps(payload, separators=(",", ":"), ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    template = (ROOT / "web/investigation.html").read_text(encoding="utf-8")
    if template.count("__INVESTIGATION_DATA__") != 1:
        raise ValueError("Expected one data placeholder")
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(template.replace("__INVESTIGATION_DATA__", serialized), encoding="utf-8", newline="")
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/investigation/index.html")
    print("Investigator written:", build(parser.parse_args().output).name)
