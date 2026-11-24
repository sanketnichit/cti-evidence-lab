import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from examples.bounded_mapping_checks import run_checks
from scripts.investigate_sequence import certificate, load_case, verify_certificate
from src.sequence_investigation import investigate

ROOT = Path(__file__).resolve().parents[1]


def edges():
    return [dict(relation_id='uv', source_event='u', target_event='v', relation='BEFORE'),
            dict(relation_id='vw', source_event='v', target_event='w', relation='BEFORE')]


def constraints():
    return {'version': '1.0', 'semantics': 'ALLOWED_LABEL_UPPER_BOUND', 'constraints': [
        {'occurrence_id': 'archive_results', 'allowed_techniques': ['T1560'],
         'rationale': 'Test-only upper-bound assumption; no claim of independently established completeness.',
         'evidence_ids': ['E3']}]}


class MappingConstraintTests(unittest.TestCase):
    def test_bound_explains_excluded_path_and_preserves_open_answer(self):
        mappings = {'u': {'A'}, 'v': set(), 'w': {'C'}}
        self.assertEqual(investigate(mappings, edges(), ['A', 'B', 'C'])['status'], 'UNRESOLVED_MAPPING')
        result = investigate(mappings, edges(), ['A', 'B', 'C'], mapping_domains={'v': {'D'}})
        self.assertEqual(result['status'], 'NOT_SUPPORTED')
        self.assertEqual(result['domain_excluded_witnesses'][0]['excluded_requirements'],
                         [{'occurrence_id': 'v', 'required_technique': 'B', 'allowed_techniques': ['D']}])
        self.assertIn('declared allowed-label bounds', result['scope'])

    def test_singleton_candidate_does_not_become_accepted_mapping(self):
        result = investigate({'u': {'A'}, 'v': set(), 'w': {'C'}}, edges(), ['A', 'B', 'C'], mapping_domains={'v': {'B'}})
        self.assertEqual(result['status'], 'UNRESOLVED_MAPPING')
        self.assertFalse(result['known_witnesses'])
        self.assertFalse(result['projection_comparisons']['distinct_pairs']['returned'])

    def test_unlisted_unknown_stays_open(self):
        result = investigate({'u': set(), 'v': set(), 'w': {'C'}}, edges(), ['X', 'B', 'C'], mapping_domains={'v': {'B'}})
        self.assertEqual(result['status'], 'UNRESOLVED_MAPPING')
        self.assertEqual(len(result['unresolved_witnesses'][0]['required_mappings']), 2)

    def test_other_path_preserves_support_or_uncertainty(self):
        relations = edges() + [dict(relation_id='ux', source_event='u', target_event='x', relation='BEFORE'),
                               dict(relation_id='xw', source_event='x', target_event='w', relation='BEFORE')]
        for labels, expected in (({'B'}, 'SUPPORTED'), (set(), 'UNRESOLVED_MAPPING')):
            result = investigate({'u': {'A'}, 'v': labels, 'w': {'C'}, 'x': set()}, relations,
                                 ['A', 'B', 'C'], mapping_domains={'x': {'D'}})
            self.assertEqual(result['status'], expected)
            self.assertEqual(len(result['domain_excluded_witnesses']), 1)

    def test_invalid_domains_are_not_silently_ignored(self):
        mappings = {'u': {'A'}, 'v': set(), 'w': {'C'}}
        for domain in ({}, [], {'v': []}, {'v': 'B'}, {'v': ['B', 'B']}, {'v': [None]}, {'x': ['B']}, {'u': ['A']}):
            with self.subTest(domain=domain), self.assertRaises(ValueError):
                investigate(mappings, edges(), ['A', 'B', 'C'], mapping_domains=domain)

    def test_certificate_retains_open_comparison_and_detects_tampering(self):
        record = certificate('domain-controller', load_case('domain-controller'), 'archive_mapping_withheld',
                             ['T1059', 'T1059', 'T1059'], mapping_constraints=constraints())
        self.assertEqual(record['certificate_version'], '2.0')
        self.assertEqual(record['unrestricted_answer']['status'], 'UNRESOLVED_MAPPING')
        self.assertEqual(record['answer']['status'], 'NOT_SUPPORTED')
        self.assertTrue(verify_certificate(record))
        for field in ('rationale', 'allowed_techniques', 'evidence_ids'):
            changed = copy.deepcopy(record)
            changed['mapping_constraints']['constraints'][0][field] = {'rationale': 'Changed', 'allowed_techniques': ['T1059'], 'evidence_ids': ['missing']}[field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_certificate(changed)

    def test_bounds_require_auditable_assumptions(self):
        case = load_case('domain-controller')
        for field, value in (('rationale', ''), ('evidence_ids', []), ('evidence_ids', ['missing']),
                             ('allowed_techniques', ['T1560.001']), ('occurrence_id', 'rdp_dc')):
            record = constraints()
            record['constraints'][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                certificate('domain-controller', case, 'archive_mapping_withheld', ['T1059'] * 3, mapping_constraints=record)

    def test_cli_roundtrip_and_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'constraints.json'
            output = Path(directory) / 'answer.json'
            source.write_text(json.dumps(constraints()), encoding='utf-8')
            command = [sys.executable, str(ROOT / 'scripts/investigate_sequence.py')]
            run = subprocess.run(command + ['--profile', 'archive_mapping_withheld', '--query', 'T1059', 'T1059', 'T1059', '--mapping-constraints', str(source), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            verified = subprocess.run(command + ['--verify', str(output)], capture_output=True, text=True)
            self.assertEqual(verified.returncode, 0, verified.stderr)
            source.write_text('{"version":"1.0","version":"2.0"}', encoding='utf-8')
            run = subprocess.run(command + ['--query', 'T1059', 'T1059', 'T1059', '--mapping-constraints', str(source)], capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('Duplicate JSON key', run.stderr)

    def test_complete_finite_oracle_and_monotonicity(self):
        result = run_checks()
        self.assertEqual(result['finite_query_checks'], 21952)
        self.assertEqual(result, json.loads((ROOT / 'research/experiments/bounded_mapping_v0.1/results.json').read_text(encoding='utf-8')))


if __name__ == '__main__':
    unittest.main()
