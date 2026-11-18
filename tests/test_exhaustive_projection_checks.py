import unittest
import json
from pathlib import Path

from examples.exhaustive_projection_checks import run_checks


class ExhaustiveProjectionChecksTests(unittest.TestCase):
    def test_all_declared_finite_cases_match_independent_oracles(self):
        result = run_checks()
        self.assertEqual(result["graphs_checked"], 4096)
        self.assertEqual(result["source_edge_instances_checked"], 6144)
        self.assertEqual(result["edge_state_oracle_disagreements"], 0)
        self.assertEqual(result["cycle_oracle_disagreements"], 0)
        self.assertEqual(sum(result["edge_states"].values()), 6144)
        self.assertGreater(result["graphs_with_projected_cycles"], 0)
        recorded = Path(__file__).resolve().parents[1] / "research/experiments/representation_controls_v0.1/finite_checks.json"
        self.assertEqual(result, json.loads(recorded.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
