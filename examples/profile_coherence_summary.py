"""Check the manuscript's results table against the reproduced artifacts."""
import json

from examples.profile_coherence import ROOT

MANUSCRIPT = ROOT / "research/PROFILE_COHERENCE_REPORT_v0.2.md"
ARTIFACTS = ROOT / "research/experiments/profile_coherence_v0.2"
START = "<!-- profile-results:start -->"
END = "<!-- profile-results:end -->"


def results_table(uncertainty, identity, shared_source):
    recorded = uncertainty["recorded_profiles"]
    cases = (
        ("domain-controller", "Domain controller", recorded["domain-controller/parent"]),
        ("rdp", "RDP", recorded["rdp/parent"]),
        ("netsupport-identity", "NetSupport", identity["pooling_comparison"]),
    )
    lines = [
        "| Profile group | Queries | Supported | Unresolved | Pooled-only known witnesses | Pooled-only possible witnesses | Supported in every profile |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for group, label, row in cases:
        cells = [
            label, f"{row['query_count']:,}", row["coherent"]["SUPPORTED"],
            f"{row['coherent']['UNRESOLVED_MAPPING']:,}", row["witness_counts"]["known"]["pooled_only"],
            row["witness_counts"]["possible"]["pooled_only"], len(shared_source[group]["stable_queries"]),
        ]
        lines.append("| " + " | ".join(map(str, cells)) + " |")
    return "\n".join(lines)


def verify_table(uncertainty, identity, shared_source):
    text = MANUSCRIPT.read_text(encoding="utf-8")
    _, start, rest = text.partition(START)
    table, end, trailing = rest.partition(END)
    if not start or not end or START in trailing or table.strip() != results_table(uncertainty, identity, shared_source):
        raise ValueError("The manuscript's recorded-profile table differs from reproduced results")


if __name__ == "__main__":
    inputs = ("uncertainty_results.json", "netsupport_identity_results.json", "shared_source_results.json")
    verify_table(*(json.loads((ARTIFACTS / name).read_bytes()) for name in inputs))
    print("Verified the manuscript results table.")
