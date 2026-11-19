"""Reproduce the frozen five-publisher comparison without exporting source text."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from itertools import permutations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_pilot_sources import FRAME, read_csv, verified_text
from scripts.audit_rank_two_review import verify_spans
from src.occurrence_queries import evaluate, validate as validate_graph
from src.sequence_investigation import investigate

DIRECTORY = ROOT / 'research/experiments/external_sequence_evaluation_v0.1'
SEED = 'CTI-EVIDENCE-LAB-ANNOCTR-PILOT-2026-11-03-v1'
STRATA = ('INCIDENT_OBSERVED', 'PROCEDURE_CONDITIONAL')
MODELS = ('distinct_pairs', 'loop_pairs', 'distinct_pairs_with_endpoint_join', 'loop_pairs_with_endpoint_join')


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def record_hash(value):
    return digest(json.dumps(value, sort_keys=True, separators=(',', ':')))


def unique(items, key):
    result = {item[key]: item for item in items}
    if len(result) != len(items):
        raise ValueError('Duplicate ' + key)
    return result


def validate(selection, review):
    # Protocol text is tracked as LF by Git; universal-newline decoding makes
    # this record stable in Windows checkouts. Source-text hashes stay strict.
    if review['protocol_sha256'] != digest((DIRECTORY / 'PROTOCOL.md').read_text(encoding='utf-8')) or review['selection_commit'] != '12033e21e821df2cc65e077274b9e987d96c1659':
        raise ValueError('Protocol or pre-review commit changed')
    if review['taxonomy']['release'] != 'Enterprise ATT&CK v12.1' or review['taxonomy']['stix_sha256'] != 'e84679af4bc46bba2ba92f60182101f146d5b966898e47924de7321e6bffeaa1':
        raise ValueError('Changed taxonomy release')
    if selection['rank'] != 3 or selection['seed'] != SEED:
        raise ValueError('Changed rank or seed')
    if selection['frame_path'] != FRAME.relative_to(ROOT).as_posix() or selection['frame_sha256'] != digest(FRAME.read_bytes()):
        raise ValueError('Changed selection frame')
    frame = read_csv(FRAME)
    for donor in {row['donor'] for row in frame}:
        rows = sorted((r for r in frame if r['donor'] == donor), key=lambda r: r['random_priority_sha256'])
        for rank, row in enumerate(rows, 1):
            if row['random_priority_sha256'] != digest(SEED + '|' + row['report_id']) or int(row['random_rank_within_vendor']) != rank:
                raise ValueError('Priority ranks do not reproduce')
    expected = {r['report_id']: r for r in frame if r['random_rank_within_vendor'] == '3'}
    chosen = unique(selection['reports'], 'report_id')
    reports = unique(review['reports'], 'report_id')
    if set(chosen) != set(expected) or set(reports) != set(chosen):
        raise ValueError('All five selected reports must remain in the evaluation')
    for rid, row in chosen.items():
        if any(expected[rid].get(k) != v for k, v in row.items()):
            raise ValueError('Selection metadata changed')
    if review['status'] != 'EXPLORATORY_SOURCE_INTERPRETATIONS' or review['independently_validated'] is not False:
        raise ValueError('Independent validation is not established')
    for rid, report in reports.items():
        if report['source_text_sha256'] != chosen[rid]['source_text_sha256'] or report['full_corpus_text_read'] is not True:
            raise ValueError('Incomplete or unbound source review')
        if not report['primary_assessment'].strip() or not report['exclusions']:
            raise ValueError('Missing interpretation or counterevidence')
        evidence = unique(report['evidence'], 'evidence_id')
        for e in evidence.values():
            if any(type(e[k]) is not int for k in ('char_start', 'char_end', 'line_start', 'line_end')) or not 0 <= e['char_start'] < e['char_end'] or not 1 <= e['line_start'] <= e['line_end'] or not re.fullmatch('[0-9a-f]{64}', e['span_sha256']):
                raise ValueError('Invalid source binding')
        def references(item):
            if not item['evidence_ids'] or not set(item['evidence_ids']) <= evidence.keys():
                raise ValueError('Missing evidence reference')
        for exclusion in report['exclusions']:
            references(exclusion)
            if not exclusion['assessment'].strip():
                raise ValueError('Missing exclusion rationale')
        unique(report['graphs'], 'graph_id')
        for graph in report['graphs']:
            if graph['stratum'] not in STRATA or not graph['condition'].strip() or not graph['alternative_reading'].strip():
                raise ValueError('Missing graph scope or alternative')
            nodes = unique(graph['occurrences'], 'event_id')
            unique(graph['relations'], 'relation_id')
            for node in nodes.values():
                references(node)
                if not node['mapping_rationale'].strip() or not node['description'].strip() or not node['candidate_mappings']:
                    raise ValueError('Missing mapping rationale or vocabulary')
                for key in ('mappings', 'candidate_mappings'):
                    if not isinstance(node[key], list) or len(node[key]) != len(set(node[key])) or any(not isinstance(t, str) or not re.fullmatch(r'T\d{4}', t) for t in node[key]):
                        raise ValueError('Invalid parent mapping set')
                if not set(node['mappings']) <= set(node['candidate_mappings']):
                    raise ValueError('Known mapping absent from vocabulary')
            for edge in graph['relations']:
                references(edge)
                if edge['relation'] != 'BEFORE' or not edge['temporal_rationale'].strip():
                    raise ValueError('Only justified BEFORE edges supported')
            mappings = {n: set(row['mappings']) for n, row in nodes.items()}
            edges = {(r['source_event'], r['target_event']) for r in graph['relations']}
            validate_graph(mappings, edges)
        primary = any(g['stratum'] == 'INCIDENT_OBSERVED' and paths_for(g) for g in report['graphs'])
        if report['primary_sequence_status'] != ('ESTABLISHED' if primary else 'NOT_ESTABLISHED'):
            raise ValueError('Primary status disagrees with retained paths')
    return reports


def paths_for(graph):
    edges = {(r['source_event'], r['target_event']) for r in graph['relations']}
    return [p for p in permutations([n['event_id'] for n in graph['occurrences']], 3)
            if (p[0], p[1]) in edges and (p[1], p[2]) in edges]


def score_graph(graph):
    mappings = {n['event_id']: set(n['mappings']) for n in graph['occurrences']}
    edges = {(r['source_event'], r['target_event']) for r in graph['relations']}
    paths = paths_for(graph)
    vocab = sorted({t for n in graph['occurrences'] for t in n['candidate_mappings']})
    # Independent oracle: enumerate all assignments over the fixed query vocabulary.
    # Singleton completions suffice to establish possible membership of any one query.
    known = {q for p in paths for q in product(*(mappings[n] for n in p))}
    possible = set()
    for p in paths:
        possible.update(product(*(mappings[n] or set(vocab) for n in p)))
    results = evaluate(mappings, edges)
    questions = []
    for query in product(vocab, repeat=3):
        status = 'SUPPORTED' if query in known else 'UNRESOLVED_MAPPING' if query in possible else 'NOT_SUPPORTED'
        answer = investigate(mappings, graph['relations'], query)
        if answer['status'] != status:
            raise ValueError('Investigator disagrees with direct path oracle')
        questions.append({'query': list(query), 'status': status,
                          'returned': {m: query in results['answers'][m] for m in MODELS},
                          'known_witnesses': answer['known_witnesses'],
                          'unresolved_witnesses': answer['unresolved_witnesses']})
    assessed = bool(paths)
    comparison = {}
    for model in MODELS:
        comparison[model] = {
            'returned_answers': sum(q['returned'][model] for q in questions),
            'unsupported_positives': sum(q['returned'][model] and q['status'] == 'NOT_SUPPORTED' for q in questions) if assessed else None,
            'missed_supported': sum(not q['returned'][model] and q['status'] == 'SUPPORTED' for q in questions) if assessed else None,
            'unresolved_returns': sum(q['returned'][model] and q['status'] == 'UNRESOLVED_MAPPING' for q in questions) if assessed else None,
        }
    return {'graph_id': graph['graph_id'], 'stratum': graph['stratum'],
            'assessment_status': 'CONDITIONAL_ON_INTERPRETED_GRAPH' if assessed else 'UNASSESSED_NO_PATHS',
            'occurrences': len(mappings), 'edges': len(edges), 'source_paths': len(paths),
            'fully_mapped_paths': sum(all(mappings[n] for n in p) for p in paths),
            'query_vocabulary': vocab, 'query_universe_size': len(questions),
            'status_counts': {s: sum(q['status'] == s for q in questions) for s in ('SUPPORTED', 'UNRESOLVED_MAPPING', 'NOT_SUPPORTED')},
            'models': comparison, 'queries': questions}


def run_evaluation(selection, review):
    reports = validate(selection, review)
    details = []
    for rid, report in reports.items():
        graphs = [score_graph(g) for g in report['graphs']]
        details.append({'report_id': rid, 'primary_sequence_status': report['primary_sequence_status'],
                        'query_error_counts': None if not any(g['source_paths'] for g in graphs) else 'SEE_SCOPED_GRAPHS',
                        'graphs': graphs})
    strata = {}
    for stratum in STRATA:
        graphs = [g for r in details for g in r['graphs'] if g['stratum'] == stratum and g['source_paths']]
        strata[stratum] = {'selected_reports': len(reports),
                          'usable_reports': sum(any(g['stratum'] == stratum and g['source_paths'] for g in r['graphs']) for r in details),
                          'graphs': len(graphs),
                          'constructed_query_counts': {s: sum(g['status_counts'][s] for g in graphs) for s in ('SUPPORTED', 'UNRESOLVED_MAPPING', 'NOT_SUPPORTED')},
                          'query_error_counts': {m: {k: sum(g['models'][m][k] for g in graphs) for k in ('unsupported_positives', 'missed_supported', 'unresolved_returns')} for m in MODELS} if graphs else None}
    return {'status': 'EXPLORATORY_REPRESENTATION_COMPARISON_NOT_FIELD_EFFICACY',
            'selection_sha256': record_hash(selection), 'review_sha256': record_hash(review),
            'selected_reports': len(reports), 'fully_read_reports': len(reports),
            'source_evidence_bindings': sum(len(r['evidence']) for r in reports.values()),
            'strata': strata, 'reports': details,
            'limits': 'Conditional fidelity on recorded interpretations. Repeated labels, related procedures and queries are not independent observations. No incident prevalence, extraction accuracy, independent semantic validation or analyst benefit estimated.'}


def audit_sources(selection, review, corpus_root, recover_crlf=False):
    reports = validate(selection, review)
    rows = []
    for rid, report in reports.items():
        text, metadata = verified_text((Path(corpus_root) / 'text' / (rid + '.txt')).read_bytes(), report['source_text_sha256'], recover_crlf)
        verify_spans(text, report['evidence'])
        rows.append({'report_id': rid, **metadata, 'verified_evidence_ids': [e['evidence_id'] for e in report['evidence']]})
    return {'status': 'SOURCE_BYTES_AND_OFFSETS_VERIFIED_NOT_SEMANTIC_VALIDATION',
            'selection_sha256': record_hash(selection), 'review_sha256': record_hash(review), 'sources': rows}


def load_records():
    return tuple(json.loads((DIRECTORY / name).read_text(encoding='utf-8')) for name in ('selection.json', 'review.json'))


def validate_recorded_source_audit(selection, review, audit):
    reports = validate(selection, review)
    if audit['status'] != 'SOURCE_BYTES_AND_OFFSETS_VERIFIED_NOT_SEMANTIC_VALIDATION' or audit['selection_sha256'] != record_hash(selection) or audit['review_sha256'] != record_hash(review):
        raise ValueError('Recorded audit does not bind current records')
    sources = unique(audit['sources'], 'report_id')
    if set(sources) != set(reports):
        raise ValueError('Incomplete recorded source audit')
    for rid, row in sources.items():
        if row['source_text_sha256'] != reports[rid]['source_text_sha256'] or row['verified_evidence_ids'] != [e['evidence_id'] for e in reports[rid]['evidence']]:
            raise ValueError('Recorded evidence coverage mismatch')
        if row['source_text_char_count'] < max(e['char_end'] for e in reports[rid]['evidence']):
            raise ValueError('Evidence outside recorded source')
    return audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Regenerate committed results')
    parser.add_argument('--corpus-root', type=Path)
    parser.add_argument('--recover-crlf', action='store_true')
    args = parser.parse_args()
    selection, review = load_records()
    result = run_evaluation(selection, review)
    path = DIRECTORY / 'results.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    elif result != json.loads(path.read_text(encoding='utf-8')):
        raise SystemExit('FAIL: committed comparison differs from recomputation')
    if args.corpus_root:
        audit = audit_sources(selection, review, args.corpus_root, args.recover_crlf)
        path = DIRECTORY / 'source_integrity.json'
        if args.write:
            path.write_text(json.dumps(audit, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        print('Verified source bindings:', sum(len(r['verified_evidence_ids']) for r in audit['sources']))
    print(json.dumps({'status': result['status'], 'strata': result['strata']}, indent=2))


if __name__ == '__main__':
    main()
