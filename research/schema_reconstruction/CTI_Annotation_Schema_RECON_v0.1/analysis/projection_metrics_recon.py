"""Projection metrics for CTI Schema RECON v0.1 (synthetic/provisional).

This module works only on already validated, human-locked primary annotation
rows. It is not wired to AnnoCTR reports and does not perform semantic
annotation. Input mapping sets must be derived from accepted, source-supported
A_120 mappings via ``build_a120_mapping_sets``.

The module intentionally separates:
- source event-edge counts;
- event-edge -> technique-pair combinations;
- unique target distinct-technique pairs;
- edge projection outcomes; and
- strict-order cycle diagnostics.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Iterable, Mapping, Sequence

POSITIVE_RELATIONS = {
    "BEFORE", "AFTER", "OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"
}
STRICT_ORDER_RELATIONS = {"BEFORE", "AFTER"}
SYMMETRIC_RELATIONS = {"OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"}
SOURCE_SUPPORTED_MAPPING_BASES = {
    "report_explicit_subtechnique", "report_explicit_parent", "source_supported_analyst_candidate"
}


@dataclass(frozen=True)
class TechniqueMapping:
    mapping_id: str
    activity_unit_id: str
    baseline_parent_technique_id: str
    mapping_decision_status: str
    mapping_basis: str
    baseline_mapping_status: str


@dataclass(frozen=True)
class TemporalEdge:
    edge_id: str
    source_event: str
    target_event: str
    relation: str
    relation_basis: str = "direct_source"
    scope_compatibility: str = "COMPATIBLE"


def build_a120_mapping_sets(
    mapping_rows: Iterable[TechniqueMapping],
    a120_ids: Iterable[str],
    eligible_event_ids: Iterable[str],
) -> tuple[dict[str, set[str]], dict[str, int]]:
    """Build primary mapping sets from accepted, source-supported A_120 rows.

    Alternative/rejected/unresolved/workbook-only/out-of-vocabulary rows are
    excluded and counted. This function does not validate source semantics;
    callers must supply rows already checked by the schema validator.
    """
    vocabulary = set(a120_ids)
    eligible_events = set(eligible_event_ids)
    result: dict[str, set[str]] = {event_id: set() for event_id in eligible_events}
    stats = {
        "input_mapping_rows": 0,
        "accepted_a120_mapping_rows": 0,
        "excluded_nonaccepted": 0,
        "excluded_unsupported_basis": 0,
        "excluded_out_of_vocab_or_unresolved": 0,
        "excluded_non_event_unit": 0,
    }
    seen_ids: set[str] = set()
    for row in mapping_rows:
        stats["input_mapping_rows"] += 1
        if not row.mapping_id:
            raise ValueError("Mapping IDs must be non-empty.")
        if row.mapping_id in seen_ids:
            raise ValueError(f"Duplicate mapping_id: {row.mapping_id}")
        seen_ids.add(row.mapping_id)
        if row.activity_unit_id not in eligible_events:
            stats["excluded_non_event_unit"] += 1
            continue
        if row.mapping_decision_status != "ACCEPTED":
            stats["excluded_nonaccepted"] += 1
            continue
        if row.mapping_basis not in SOURCE_SUPPORTED_MAPPING_BASES:
            stats["excluded_unsupported_basis"] += 1
            continue
        if row.baseline_mapping_status != "IN_VOCAB" or row.baseline_parent_technique_id not in vocabulary:
            stats["excluded_out_of_vocab_or_unresolved"] += 1
            continue
        result[row.activity_unit_id].add(row.baseline_parent_technique_id)
        stats["accepted_a120_mapping_rows"] += 1
    return result, stats


def _strongly_connected_components(
    nodes: Iterable[str], edges: Iterable[tuple[str, str]]
) -> list[tuple[str, ...]]:
    adjacency: dict[str, list[str]] = {node: [] for node in nodes}
    for source, target in edges:
        adjacency.setdefault(source, []).append(target)
        adjacency.setdefault(target, [])
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    components: list[tuple[str, ...]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for neighbour in adjacency[node]:
            if neighbour not in indices:
                visit(neighbour)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbour])
            elif neighbour in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[neighbour])
        if lowlinks[node] == indices[node]:
            members: list[str] = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                members.append(member)
                if member == node:
                    break
            components.append(tuple(sorted(members)))

    for node in sorted(adjacency):
        if node not in indices:
            visit(node)
    return components


def _cyclic_components(
    nodes: Iterable[str], edges: Iterable[tuple[str, str]]
) -> list[tuple[str, ...]]:
    edge_list = list(edges)
    self_loops = {(source, target) for source, target in edge_list if source == target}
    return [
        component for component in _strongly_connected_components(nodes, edge_list)
        if len(component) > 1 or any((node, node) in self_loops for node in component)
    ]


def _relation_class(edge: TemporalEdge) -> str:
    # BEFORE and AFTER are one normalized strict-order representation class.
    return "STRICT_ORDER" if edge.relation in STRICT_ORDER_RELATIONS else edge.relation


def _normalized_strict_pair(edge: TemporalEdge, pair: tuple[str, str]) -> tuple[str, str]:
    return (pair[1], pair[0]) if edge.relation == "AFTER" else pair


def project_report_recon(
    techniques_by_event: Mapping[str, Iterable[str]],
    temporal_edges: Sequence[TemporalEdge],
) -> dict:
    """Project validated primary event edges using the RECON v0.1 metric contract.

    Expected input:
      * one report + one annotator + one annotation pass;
      * techniques_by_event contains only accepted A_120 parent IDs;
      * temporal_edges contains only positive, directly supported relations
        with eligible distinct event-leaf endpoints and compatible scope.

    The function enforces input shape and relation eligibility but cannot
    independently establish event-leaf status, source evidence, or scope
    ancestry; those are enforced by the schema validator before this step.
    """
    normalized: dict[str, tuple[str, ...]] = {}
    for event_id, values in techniques_by_event.items():
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError("Event IDs must be non-empty strings.")
        if isinstance(values, (str, bytes)):
            raise TypeError("Technique mappings must be an iterable of IDs, not a string.")
        techniques = {value for value in values if value}
        if any(not isinstance(value, str) for value in techniques):
            raise TypeError(f"Technique IDs for {event_id!r} must be strings.")
        normalized[event_id] = tuple(sorted(techniques))

    edge_ids: set[str] = set()
    for edge in temporal_edges:
        if not edge.edge_id or not edge.source_event or not edge.target_event:
            raise ValueError("Edge IDs and endpoint IDs must be non-empty.")
        if edge.edge_id in edge_ids:
            raise ValueError(f"Duplicate edge ID: {edge.edge_id}")
        edge_ids.add(edge.edge_id)
        if edge.source_event == edge.target_event:
            raise ValueError(f"Self-event edge is invalid: {edge.edge_id}")
        if edge.relation not in POSITIVE_RELATIONS:
            raise ValueError(f"Non-positive/unsupported temporal relation: {edge.relation!r}")
        if edge.relation_basis not in {"direct_source", "direct_timestamp"}:
            raise ValueError(f"Non-primary relation basis is not projectable: {edge.relation_basis!r}")
        if edge.scope_compatibility != "COMPATIBLE":
            raise ValueError("Only scope-compatible primary relations are projectable.")
        missing = [event_id for event_id in (edge.source_event, edge.target_event) if event_id not in normalized]
        if missing:
            raise ValueError(f"Edge {edge.edge_id!r} references unknown event(s): {missing}")

    all_techniques = sorted({technique for ids in normalized.values() for technique in ids})
    edge_status: dict[str, str] = {}
    edge_to_pairs: dict[str, list[tuple[str, str]]] = {}
    edge_to_diagonal_pairs: dict[str, list[tuple[str, str]]] = {}
    edge_to_distinct_pairs: dict[str, list[tuple[str, str]]] = {}
    relation_class_pairs: dict[tuple[str, tuple[str, str]], set[str]] = defaultdict(set)
    global_pair_edges: dict[tuple[str, str], set[str]] = defaultdict(set)
    global_pair_labels: dict[tuple[str, str], set[str]] = defaultdict(set)
    diagonal_mapping_count = 0
    all_mapping_combinations = 0
    mapped_edge_ids: list[str] = []
    unmapped_edge_ids: list[str] = []
    shared_edge_ids: list[str] = []

    normalized_before_event_edges: list[tuple[str, str]] = []
    for edge in temporal_edges:
        source_ids = normalized[edge.source_event]
        target_ids = normalized[edge.target_event]
        if edge.relation == "BEFORE":
            normalized_before_event_edges.append((edge.source_event, edge.target_event))
        elif edge.relation == "AFTER":
            normalized_before_event_edges.append((edge.target_event, edge.source_event))

        if not source_ids or not target_ids:
            edge_status[edge.edge_id] = "unmapped_endpoint"
            edge_to_pairs[edge.edge_id] = []
            edge_to_diagonal_pairs[edge.edge_id] = []
            edge_to_distinct_pairs[edge.edge_id] = []
            unmapped_edge_ids.append(edge.edge_id)
            continue

        mapped_edge_ids.append(edge.edge_id)
        raw_pairs = set(product(source_ids, target_ids))
        if edge.relation in SYMMETRIC_RELATIONS:
            pairs = sorted({tuple(sorted(pair)) for pair in raw_pairs})
            normalized_pairs = pairs
        else:
            pairs = sorted(raw_pairs)
            normalized_pairs = sorted({_normalized_strict_pair(edge, pair) for pair in pairs})

        diagonal = [pair for pair in pairs if pair[0] == pair[1]]
        distinct = [pair for pair in pairs if pair[0] != pair[1]]
        edge_to_pairs[edge.edge_id] = pairs
        edge_to_diagonal_pairs[edge.edge_id] = diagonal
        edge_to_distinct_pairs[edge.edge_id] = distinct
        all_mapping_combinations += len(pairs)
        diagonal_mapping_count += len(diagonal)

        shared = bool(set(source_ids).intersection(target_ids))
        if shared:
            shared_edge_ids.append(edge.edge_id)
        if shared and not distinct:
            edge_status[edge.edge_id] = "fully_omitted"
        elif shared and distinct:
            edge_status[edge.edge_id] = "partially_represented"
        else:
            edge_status[edge.edge_id] = "no_diagonal_mapping"

        rclass = _relation_class(edge)
        for pair in normalized_pairs:
            if pair[0] == pair[1]:
                continue
            relation_class_pairs[(rclass, pair)].add(edge.edge_id)
            global_pair_edges[pair].add(edge.edge_id)
            global_pair_labels[pair].add(_relation_class(edge))

    mapped_count = len(mapped_edge_ids)
    total_edges = len(temporal_edges)
    status_counts = {
        status: sum(1 for value in edge_status.values() if value == status)
        for status in ("unmapped_endpoint", "fully_omitted", "partially_represented", "no_diagonal_mapping")
    }
    assert sum(status_counts.values()) == total_edges

    # Collisions are calculated only in the target distinct-technique-pair
    # graph and separately by relation class/orientation.
    distinct_pair_provenance_by_relation_class = {
        f"{relation_class}|{pair[0]}->{pair[1]}": sorted(edge_ids_for_pair)
        for (relation_class, pair), edge_ids_for_pair in sorted(relation_class_pairs.items())
    }
    collisions_by_relation_class = {
        key: edge_ids_for_pair
        for key, edge_ids_for_pair in distinct_pair_provenance_by_relation_class.items()
        if len(edge_ids_for_pair) > 1
    }
    all_distinct_pair_collisions = {
        f"{pair[0]}->{pair[1]}": sorted(edge_ids_for_pair)
        for pair, edge_ids_for_pair in sorted(global_pair_edges.items())
        if len(edge_ids_for_pair) > 1
    }
    label_conflicts = {
        f"{pair[0]}->{pair[1]}": sorted(labels)
        for pair, labels in sorted(global_pair_labels.items())
        if len(labels) > 1
    }

    source_cycles = _cyclic_components(set(normalized), normalized_before_event_edges)
    technique_strict_pairs = {
        pair for (relation_class, pair), ids in relation_class_pairs.items()
        if relation_class == "STRICT_ORDER" and ids
    }
    technique_cycles = _cyclic_components(all_techniques, technique_strict_pairs)
    cycle_provenance = []
    for component in technique_cycles:
        component_set = set(component)
        internal_pairs = sorted(pair for pair in technique_strict_pairs if pair[0] in component_set and pair[1] in component_set)
        source_ids = sorted({
            edge_id for pair in internal_pairs
            for edge_id in relation_class_pairs[("STRICT_ORDER", pair)]
        })
        single_source_edges_inducing_cycle = []
        for source_edge_id in source_ids:
            pairs_from_one_source_edge = [
                pair for pair in internal_pairs
                if source_edge_id in relation_class_pairs[("STRICT_ORDER", pair)]
            ]
            if _cyclic_components(component_set, pairs_from_one_source_edge):
                single_source_edges_inducing_cycle.append(source_edge_id)
        cycle_provenance.append({
            "technique_nodes": list(component),
            "internal_pairs": [list(pair) for pair in internal_pairs],
            "source_event_edge_ids": source_ids,
            "source_event_edge_count": len(source_ids),
            "single_source_edges_inducing_cycle": single_source_edges_inducing_cycle,
            "single_event_edge_mapping_fanout": bool(single_source_edges_inducing_cycle),
        })

    return {
        "counts": {
            "resolved_event_instances": len(normalized),
            "mapped_event_instances": sum(1 for ids in normalized.values() if ids),
            "unique_techniques": len(all_techniques),
            "positive_temporal_edges": total_edges,
            "mapped_positive_temporal_edges": mapped_count,
            "unmapped_endpoint_edges": status_counts["unmapped_endpoint"],
            "fully_omitted_edges": status_counts["fully_omitted"],
            "partially_represented_edges": status_counts["partially_represented"],
            "no_diagonal_mapping_edges": status_counts["no_diagonal_mapping"],
            "same_technique_endpoint_edges": len(shared_edge_ids),
            "event_edge_to_pair_combinations": all_mapping_combinations,
            "diagonal_mapping_combinations": diagonal_mapping_count,
            "distinct_pair_combinations": all_mapping_combinations - diagonal_mapping_count,
            "unique_distinct_technique_pairs": len(global_pair_edges),
            "distinct_pair_collision_keys_by_relation_class": len(collisions_by_relation_class),
            "distinct_pair_collision_keys_global": len(all_distinct_pair_collisions),
            "distinct_pair_label_conflicts": len(label_conflicts),
            "source_strict_order_cycle_components": len(source_cycles),
            "projected_strict_order_cycle_components": len(technique_cycles),
            "projected_cycle_components_with_multiple_source_edges": sum(1 for row in cycle_provenance if row["source_event_edge_count"] > 1),
            "projected_cycle_components_requiring_multiple_source_edges": sum(1 for row in cycle_provenance if not row["single_event_edge_mapping_fanout"]),
            "projected_cycle_components_from_single_edge_fanout": sum(1 for row in cycle_provenance if row["single_event_edge_mapping_fanout"]),
        },
        "rates": {
            "full_omission_rate_mapped_edges": status_counts["fully_omitted"] / mapped_count if mapped_count else None,
            "partial_representation_rate_mapped_edges": status_counts["partially_represented"] / mapped_count if mapped_count else None,
            "no_diagonal_mapping_rate_mapped_edges": status_counts["no_diagonal_mapping"] / mapped_count if mapped_count else None,
            "same_technique_endpoint_rate_mapped_edges": len(shared_edge_ids) / mapped_count if mapped_count else None,
            "diagonal_mapping_share": diagonal_mapping_count / all_mapping_combinations if all_mapping_combinations else None,
        },
        "edge_projection_status": dict(sorted(edge_status.items())),
        "projection": {
            "edge_to_pairs": {edge_id: [list(pair) for pair in pairs] for edge_id, pairs in sorted(edge_to_pairs.items())},
            "edge_to_diagonal_pairs": {edge_id: [list(pair) for pair in pairs] for edge_id, pairs in sorted(edge_to_diagonal_pairs.items())},
            "edge_to_distinct_pairs": {edge_id: [list(pair) for pair in pairs] for edge_id, pairs in sorted(edge_to_distinct_pairs.items())},
            "distinct_pair_provenance_by_relation_class": distinct_pair_provenance_by_relation_class,
            "distinct_pair_collisions_by_relation_class": collisions_by_relation_class,
            "distinct_pair_collisions_global": all_distinct_pair_collisions,
            "distinct_pair_label_conflicts": label_conflicts,
        },
        "strict_order_cycle_analysis": {
            "source_event_graph_is_acyclic": not bool(source_cycles),
            "projection_cycle_analysis_valid": not bool(source_cycles),
            "source_cycle_components": [list(component) for component in source_cycles],
            "projected_cycle_components": [list(component) for component in technique_cycles],
            "projected_cycle_provenance": cycle_provenance,
        },
    }
