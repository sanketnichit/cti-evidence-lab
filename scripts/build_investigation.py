"""Build a portable offline sequence investigator from verified case records."""
import argparse
import json
import subprocess
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.investigate_sequence import CASES, certificate, load_case


def build(destination):
    cases = []
    for key in CASES:
        case = load_case(key)
        profiles = []
        for p in case["profiles"]:
            level = p.get("taxonomy_level", "parent")
            vocabulary = sorted({n["candidate_" + level + "_mapping"] for n in case["occurrences"]})
            answers = {}
            common = None
            for query in product(vocabulary, repeat=3):
                value = certificate(key, case, p["name"], query)
                answers["|".join(query)] = {"answer": value.pop("answer"), "certificate_sha256": value.pop("certificate_sha256")}
                common = value
            profiles.append({"name": p["name"], "level": level, "vocabulary": vocabulary, "common": common, "answers": answers})
        cases.append({"key": key, "title": case["source"]["title"], "profiles": profiles})
    payload = {"cases": cases, "repository_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
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
