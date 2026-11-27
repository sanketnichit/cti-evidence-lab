"""Compare three source-based readings of the NetSupport WMI passage."""
import argparse
import json
from pathlib import Path

from examples.profile_uncertainty import compare
from scripts.audit_rdp_case import verify
from scripts.investigate_sequence import AVAILABLE_CASES, ROOT, load_case, profile_graph
from src.sequence_investigation import investigate

RESULTS = ROOT / "research/experiments/profile_coherence_v0.2/netsupport_identity_results.json"
QUERIES = {
    "wmi_identity": ("T1562", "T1047", "T1053"),
    "separate_script_actions": ("T1105", "T1059", "T1560"),
}


def identity_profiles(source_html=None):
    key = "dfir-netsupport"
    if source_html is not None:
        record = json.loads(AVAILABLE_CASES[key].read_bytes())
        verify(source_html.read_bytes(), record)
    _, _, mappings, relations = profile_graph(load_case(key), "recorded_parent_profile")
    # The conditional reading treats the summary and detailed execution as the
    # same occurrence. Redirect only the cited edge and verify that no other
    # relation depends on the removed occurrence.
    summary_edge, = [row for row in relations if row["relation_id"] == "B12"]
    assert (summary_edge["source_event"], summary_edge["target_event"]) == ("firewall_change", "remote_execution")
    assert mappings["remote_execution"] == mappings["payload_run"] == {"T1047"}
    conservative = [row for row in relations if row["relation_id"] != "B12"]
    assert all("remote_execution" not in (r["source_event"], r["target_event"]) for r in conservative)
    co_referent = {node: labels for node, labels in mappings.items() if node != "remote_execution"}
    return {
        "recorded": (mappings, relations),
        "omit_summary_edge": (mappings, conservative),
        "co_referent_execution": (
            co_referent,
            [*conservative, {**summary_edge, "relation_id": "B12-aligned", "target_event": "payload_run"}],
        ),
    }


def run(source_html=None):
    alternatives = identity_profiles(source_html)
    profiles = {}
    for name, (labels, edges) in alternatives.items():
        profiles[name] = {}
        for question, query in QUERIES.items():
            answer = investigate(labels, edges, query)
            row = answer["projection_comparisons"]["loop_pairs"]
            profiles[name][question] = {
                "query": list(query), "status": answer["status"], "ordinary_returned": row["returned"],
                "endpoint_join_returned": row["endpoint_join_returned"],
                "known_witnesses": answer["known_witnesses"],
            }
    vocabulary = sorted(set().union(*alternatives["recorded"][0].values()))
    graphs = [(labels, {(r["source_event"], r["target_event"]) for r in edges})
              for labels, edges in alternatives.values()]
    return {"profiles": profiles, "pooling_comparison": compare(graphs, vocabulary)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-html", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.source_html)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    elif result != json.loads(RESULTS.read_bytes()):
        raise SystemExit("Identity sensitivity differs from the recorded result")
    else:
        print("Reproduced NetSupport identity sensitivity.")


if __name__ == "__main__":
    main()
