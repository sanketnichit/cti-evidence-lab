import copy
import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from scripts.evaluate_external_sequences import DIRECTORY, load_records, run_evaluation, score_graph, validate, validate_recorded_source_audit


class ExternalSequenceEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.selection, self.review = load_records()

    def test_frozen_results_reproduce_and_no_primary_absence_claim(self):
        result = run_evaluation(self.selection, self.review)
        self.assertEqual(result, json.loads((DIRECTORY / 'results.json').read_text(encoding='utf-8')))
        primary = result['strata']['INCIDENT_OBSERVED']
        self.assertEqual(primary['selected_reports'], 5)
        self.assertEqual(primary['usable_reports'], 0)
        self.assertIsNone(primary['query_error_counts'])
        for report in result['reports']:
            if not report['graphs']:
                self.assertIsNone(report['query_error_counts'])

    def test_cannot_drop_unproductive_report_or_change_source(self):
        self.review['reports'].pop(0)
        with self.assertRaises(ValueError):
            validate(self.selection, self.review)
        self.selection, self.review = load_records()
        self.review['reports'][0]['source_text_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            validate(self.selection, self.review)

    def test_unknown_labels_do_not_become_negative_examples(self):
        graph = self.review['reports'][4]['graphs'][0]
        result = score_graph(graph)
        self.assertEqual(result['status_counts']['UNRESOLVED_MAPPING'], 2)
        self.assertEqual(result['status_counts']['SUPPORTED'], 0)
        self.assertEqual(result['models']['loop_pairs']['unresolved_returns'], 1)
        self.assertEqual(result['models']['loop_pairs']['unsupported_positives'], 0)
        query = next(q for q in result['queries'] if q['query'] == ['T1555'] * 3)
        self.assertEqual(query['status'], 'UNRESOLVED_MAPPING')
        self.assertTrue(query['returned']['loop_pairs'])
        self.assertFalse(query['returned']['loop_pairs_with_endpoint_join'])

    def test_no_advantage_case_is_retained(self):
        graph = self.review['reports'][2]['graphs'][0]
        result = score_graph(graph)
        self.assertEqual(result['status_counts']['SUPPORTED'], 1)
        for model in result['models'].values():
            self.assertEqual(model['returned_answers'], 1)
            self.assertEqual(model['missed_supported'], 0)
            self.assertEqual(model['unsupported_positives'], 0)

    def test_rejects_dangling_evidence_cycles_and_promoted_primary(self):
        for mutation in ('evidence', 'cycle', 'primary'):
            review = copy.deepcopy(self.review)
            graph = review['reports'][2]['graphs'][0]
            if mutation == 'evidence':
                graph['relations'][0]['evidence_ids'] = ['missing']
            elif mutation == 'cycle':
                graph['relations'][1]['target_event'] = 'enable'
            else:
                review['reports'][2]['primary_sequence_status'] = 'ESTABLISHED'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate(self.selection, review)

    def test_empty_graph_has_unassessed_errors(self):
        graph = copy.deepcopy(self.review['reports'][2]['graphs'][0])
        graph['relations'] = []
        result = score_graph(graph)
        self.assertEqual(result['assessment_status'], 'UNASSESSED_NO_PATHS')
        self.assertTrue(all(m['unsupported_positives'] is None for m in result['models'].values()))

    def test_recorded_source_audit_cannot_silently_lose_binding(self):
        audit = json.loads((DIRECTORY / 'source_integrity.json').read_text(encoding='utf-8'))
        validate_recorded_source_audit(self.selection, self.review, audit)
        audit['sources'][0]['verified_evidence_ids'].pop()
        with self.assertRaises(ValueError):
            validate_recorded_source_audit(self.selection, self.review, audit)

    def test_protocol_hash_survives_git_checkout_newlines(self):
        text = (DIRECTORY / 'PROTOCOL.md').read_text(encoding='utf-8')
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            for newline in ('\n', '\r\n'):
                (folder / 'PROTOCOL.md').write_bytes(text.replace('\n', newline).encode())
                with patch('scripts.evaluate_external_sequences.DIRECTORY', folder):
                    validate(self.selection, self.review)


if __name__ == '__main__':
    unittest.main()
