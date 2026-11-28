"""Recompute supported-query cuts under a passage-level reading of ordering evidence."""
import json
from itertools import combinations

from examples.ordering_evidence_sensitivity import RESULTS
from scripts.investigate_sequence import load_case, profile_graph
from src.sequence_investigation import investigate


# Each tuple is one sufficient set of spans, conditional on the recorded action IDs.
SUPPORT = {
    "B1": [("E2",), ("E7",)],
    "B2": [("E2",), ("E4",), ("E9",)],
    "B3": [("E2", "E3")],
    "B4": [("E3",), ("E8",)],
    "B5": [("E3",)],
}


def run():
    case = load_case("domain-controller")
    paragraphs = {row["evidence_id"]: row["paragraph_number"] for row in case["evidence"]}
    for edge in case["relations"]:
        assert set(edge["evidence_ids"]) == set().union(*SUPPORT[edge["relation_id"]])
    results = json.loads(RESULTS.read_bytes())["domain-controller"]
    rows = []
    for profile, result in results.items():
        _, _, mappings, relations = profile_graph(case, profile)
        units = sorted({paragraphs[e] for row in relations for e in row["evidence_ids"]})
        for cut in result["minimum_source_unit_cuts"]:
            query = cut["query"]
            for size in range(len(units) + 1):
                cuts = []
                for withdrawn in combinations(units, size):
                    retained = [row for row in relations if any(
                        all(paragraphs[e] not in withdrawn for e in group) for group in SUPPORT[row["relation_id"]]
                    )]
                    if investigate(mappings, retained, query, summary_only=True)["status"] != "SUPPORTED":
                        cuts.append(withdrawn)
                if cuts:
                    assert len(cut["first_citation"]) <= size <= len(cut["last_citation"])
                    rows.append({"profile": profile, "query": query, "minimum_withdrawals": cuts})
                    break
    return rows


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
