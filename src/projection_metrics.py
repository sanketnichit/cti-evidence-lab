"""Pure-Python projection metrics for CTI event-instance graphs.

This module contains no NLP, parsing, model inference, or CTI data. It is a
small, deterministic research prototype used to test metric definitions on
human-authored toy graphs before any real report is annotated.

Input contract:
- each key in techniques_by_event is a resolved, report-local event instance;
- each value is the set/list of evidence-backed ATT&CK IDs assigned to it;
- each TemporalEdge is a positive temporal relation between those instances;
- AFTER is normalized internally by swapping endpoints for strict-order
  cycle analysis. Original labels, endpoint order and evidence remain in the
  input annotations.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class TemporalEdge:
    """A positive relation between two resolved event instances."""

    edge_id: str
    source_event: str
    target_event: str
    relation: str = "BEFORE"


def _strongly_connected_components(
    nodes: Iterable[str], edges: Iterable[tuple[str, str]]
) -> list[tuple[str, ...]]:
    """Return strongly connected components using Tarjan's algorithm."""

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
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for neighbour in adjacency.get(node, []):
            if neighbour not in indices:
                visit(neighbour)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbour])
            elif neighbour in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[neighbour])

        if lowlinks[node] == indices[node]:
            component: list[str] = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            components.append(tuple(sorted(component)))

    for node in sorted(adjacency):
        if node not in indices:
            visit(node)

    return components


def _cyclic_components(
    nodes: Iterable[str], edges: Iterable[tuple[str, str]]
) -> list[tuple[str, ...]]:
    edge_list = list(edges)
    components = _strongly_connected_components(nodes, edge_list)
    self_loops = {(a, b) for a, b in edge_list if a == b}
    return [
        component
        for component in components
        if len(component) > 1
        or any((node, node) in self_loops for node in component)
    ]


def project_report(
    techniques_by_event: Mapping[str, Iterable[str]],
    temporal_edges: Sequence[TemporalEdge],
) -> dict:
    """Project event-instance relations to ATT&CK technique pairs.

    Only explicit positive temporal relations are accepted as input. Allowed
    labels are BEFORE, AFTER, OVERLAP, SIMULTANEOUS and
    CONCURRENT_UNSPECIFIED. Symmetric labels are canonicalized to unordered
    technique pairs; BEFORE/AFTER remain directed. The strict-order cycle
    analysis normalizes AFTER(A,B) to BEFORE(B,A) and excludes diagonal
    technique self-pairs.
    A missing technique mapping on either endpoint makes that edge unmappable
    in the ATT&CK-only projection.

    Raises:
        ValueError: for missing event IDs, duplicate relation IDs, empty IDs,
            or an empty relation label.
    """

    normalized: dict[str, tuple[str, ...]] = {}
    for event_id, technique_ids in techniques_by_event.items():
        if not event_id:
            raise ValueError("Event IDs must be non-empty.")
        normalized[event_id] = tuple(sorted({x for x in technique_ids if x}))

    edge_ids: set[str] = set()
    for edge in temporal_edges:
        if not edge.edge_id or not edge.source_event or not edge.target_event:
            raise ValueError("Edge IDs and endpoint event IDs must be non-empty.")
        if edge.relation not in {
            "BEFORE", "AFTER", "OVERLAP", "SIMULTANEOUS",
            "CONCURRENT_UNSPECIFIED",
        }:
            raise ValueError(
                f"Edge {edge.edge_id!r} has non-positive/unsupported relation "
                f"{edge.relation!r}; absence, ambiguity, and dependency labels "
                "must not be supplied as temporal graph edges."
            )
        if edge.edge_id in edge_ids:
            raise ValueError(f"Duplicate edge ID: {edge.edge_id}")
        edge_ids.add(edge.edge_id)
        if edge.source_event == edge.target_event:
            raise ValueError("Temporal edge endpoints must be distinct event instances.")
        missing = [
            event_id
            for event_id in (edge.source_event, edge.target_event)
            if event_id not in normalized
        ]
        if missing:
            raise ValueError(
                f"Edge {edge.edge_id!r} references unknown event(s): {missing}"
            )

    resolved_events = set(normalized)
    mapped_events = {event for event, ids in normalized.items() if ids}
    techniques = sorted({t for ids in normalized.values() for t in ids})

    projected_provenance: dict[tuple[str, str], set[str]] = defaultdict(set)
    projected_labels: dict[tuple[str, str], set[str]] = defaultdict(set)
    edge_to_pairs: dict[str, list[tuple[str, str]]] = {}
    edge_to_normalized_pairs: dict[str, list[tuple[str, str]]] = {}
    mapped_edge_ids: list[str] = []
    unmapped_edge_ids: list[str] = []
    shared_technique_endpoint_ids: list[str] = []
    self_only_edge_ids: list[str] = []
    diagonal_mappings = 0
    total_pair_mappings = 0

    before_event_edges: list[tuple[str, str]] = []
    non_before_edge_ids: list[str] = []

    for edge in temporal_edges:
        if edge.relation == "BEFORE":
            before_event_edges.append((edge.source_event, edge.target_event))
        elif edge.relation == "AFTER":
            # AFTER(A, B) is strict BEFORE(B, A) in the normalized ordering
            # graph. Preserve the original relation in the source annotation.
            before_event_edges.append((edge.target_event, edge.source_event))
        elif edge.relation not in {"BEFORE", "AFTER"}:
            non_before_edge_ids.append(edge.edge_id)

        source_techniques = normalized[edge.source_event]
        target_techniques = normalized[edge.target_event]

        if not source_techniques or not target_techniques:
            unmapped_edge_ids.append(edge.edge_id)
            edge_to_pairs[edge.edge_id] = []
            continue

        mapped_edge_ids.append(edge.edge_id)
        raw_pairs = set(product(source_techniques, target_techniques))
        if edge.relation in {
            "OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"
        }:
            # These labels are symmetric, so canonicalize the technique pair
            # to avoid treating A--B and B--A as different projected pairs.
            pairs = sorted({tuple(sorted(pair)) for pair in raw_pairs})
        else:
            # Keep source endpoint order in edge_to_pairs. For derived strict-
            # order pair keys, inverse AFTER claims share BEFORE precedence.
            pairs = sorted(raw_pairs)
        edge_to_pairs[edge.edge_id] = pairs
        if edge.relation in {"OVERLAP", "SIMULTANEOUS", "CONCURRENT_UNSPECIFIED"}:
            normalized_pairs = pairs
        elif edge.relation == "AFTER":
            normalized_pairs = sorted((target, source) for source, target in pairs)
        else:
            normalized_pairs = pairs
        edge_to_normalized_pairs[edge.edge_id] = normalized_pairs

        if set(source_techniques).intersection(target_techniques):
            shared_technique_endpoint_ids.append(edge.edge_id)

        if pairs and all(source == target for source, target in pairs):
            self_only_edge_ids.append(edge.edge_id)

        for pair in normalized_pairs:
            projected_provenance[pair].add(edge.edge_id)
            relation_class = "STRICT_ORDER" if edge.relation in {"BEFORE", "AFTER"} else edge.relation
            projected_labels[pair].add(relation_class)
        total_pair_mappings += len(pairs)
        diagonal_mappings += sum(1 for pair in pairs if pair[0] == pair[1])

    projection_pairs = sorted(projected_provenance)
    # ChronoCTI's published technique-pair universe excludes diagonal pairs:
    # (T, T) is not a candidate pair. Keep the full projection above, then
    # report the distinct-technique-pair view separately.
    distinct_technique_pairs = [
        pair for pair in projection_pairs if pair[0] != pair[1]
    ]
    distinct_pair_provenance = {
        pair: sorted(projected_provenance[pair])
        for pair in distinct_technique_pairs
    }
    distinct_pair_edge_ids = sorted({
        edge_id
        for edge_id, pairs in edge_to_pairs.items()
        if any(source != target for source, target in pairs)
    })
    edge_ids_without_distinct_pair = sorted(
        set(edge_to_pairs) - set(distinct_pair_edge_ids)
    )
    distinct_pair_mappings = total_pair_mappings - diagonal_mappings

    collision_pairs = {
        pair: sorted(edge_ids_for_pair)
        for pair, edge_ids_for_pair in projected_provenance.items()
        if len(edge_ids_for_pair) > 1
    }
    label_conflation = {
        pair: sorted(labels)
        for pair, labels in projected_labels.items()
        if len(labels) > 1
    }

    before_event_nodes = sorted(resolved_events)
    source_cycles = _cyclic_components(before_event_nodes, before_event_edges)

    # Technique projection for strict ordering ignores diagonal/self-pairs,
    # matching a common unique-technique pair graph convention. The diagonal
    # information loss is separately reported above.
    projected_before_pair_provenance: dict[tuple[str, str], set[str]] = defaultdict(set)
    for edge in temporal_edges:
        if edge.relation == "BEFORE":
            normalized_pairs = edge_to_pairs[edge.edge_id]
        elif edge.relation == "AFTER":
            # The stored projection preserves the original AFTER endpoint
            # order; reverse each pair for normalized strict-BEFORE analysis.
            normalized_pairs = [
                (target, source)
                for source, target in edge_to_pairs[edge.edge_id]
            ]
        else:
            continue

        # Ignore diagonal pairs in the strict-order technique graph. Retain
        # provenance by source event relation so that cycles produced by the
        # Cartesian product of one multi-mapped event edge can be separated
        # from cycles that require multiple source event relations.
        for pair in normalized_pairs:
            if pair[0] != pair[1]:
                projected_before_pair_provenance[pair].add(edge.edge_id)

    projected_before_pairs = set(projected_before_pair_provenance)
    projection_cycles = _cyclic_components(
        techniques, sorted(projected_before_pairs)
    )
    projected_cycle_provenance = []
    for component in projection_cycles:
        component_nodes = set(component)
        internal_pairs = sorted(
            pair
            for pair in projected_before_pair_provenance
            if pair[0] in component_nodes and pair[1] in component_nodes
        )
        source_edge_ids = sorted({
            edge_id
            for pair in internal_pairs
            for edge_id in projected_before_pair_provenance[pair]
        })
        single_source_edges_inducing_cycle = []
        for source_edge_id in source_edge_ids:
            pairs_from_one_source_edge = [
                pair for pair in internal_pairs
                if source_edge_id in projected_before_pair_provenance[pair]
            ]
            if _cyclic_components(component_nodes, pairs_from_one_source_edge):
                single_source_edges_inducing_cycle.append(source_edge_id)
        projected_cycle_provenance.append({
            "technique_nodes": list(component),
            "internal_technique_pairs": [list(pair) for pair in internal_pairs],
            "source_event_edge_ids": source_edge_ids,
            "source_event_edge_count": len(source_edge_ids),
            "single_source_edges_inducing_cycle": single_source_edges_inducing_cycle,
            "single_event_edge_mapping_fanout": bool(single_source_edges_inducing_cycle),
        })

    mapped_edge_count = len(mapped_edge_ids)
    total_edge_count = len(temporal_edges)
    mapped_event_count = len(mapped_events)
    event_count = len(resolved_events)

    return {
        "counts": {
            "resolved_event_instances": event_count,
            "mapped_event_instances": mapped_event_count,
            "unique_techniques": len(techniques),
            "positive_temporal_edges": total_edge_count,
            "mapped_temporal_edges": mapped_edge_count,
            "unmapped_temporal_edges": len(unmapped_edge_ids),
            "non_before_temporal_edges": len(non_before_edge_ids),
            "projected_technique_pairs": len(projection_pairs),
            "distinct_technique_pairs": len(distinct_technique_pairs),
            "event_edge_to_pair_mappings": total_pair_mappings,
            "distinct_technique_pair_mappings": distinct_pair_mappings,
            "event_edges_with_distinct_technique_pair": len(distinct_pair_edge_ids),
            "event_edges_without_distinct_technique_pair": len(edge_ids_without_distinct_pair),
            "shared_technique_endpoint_edges": len(shared_technique_endpoint_ids),
            "self_only_edges": len(self_only_edge_ids),
            "diagonal_pair_mappings": diagonal_mappings,
            "collision_technique_pairs": len(collision_pairs),
            "excess_event_edge_multiplicity": sum(
                len(ids) - 1 for ids in collision_pairs.values()
            ),
            "label_conflated_technique_pairs": len(label_conflation),
            "source_before_cycle_components": len(source_cycles),
            "projected_before_cycle_components": len(projection_cycles),
            "projected_cycle_components_with_multiple_source_event_edges": sum(
                1 for item in projected_cycle_provenance
                if not item["single_event_edge_mapping_fanout"]
            ),
            "projected_cycle_components_from_single_source_event_edge": sum(
                1 for item in projected_cycle_provenance
                if item["single_event_edge_mapping_fanout"]
            ),
            "projected_cycle_components_requiring_multiple_source_event_edges": sum(
                1 for item in projected_cycle_provenance
                if not item["single_event_edge_mapping_fanout"]
            ),
        },
        "rates": {
            "event_mapping_coverage": (
                mapped_event_count / event_count if event_count else None
            ),
            "temporal_edge_mapping_coverage": (
                mapped_edge_count / total_edge_count if total_edge_count else None
            ),
            "shared_technique_endpoint_edge_rate": (
                len(shared_technique_endpoint_ids) / mapped_edge_count
                if mapped_edge_count
                else None
            ),
            "self_only_edge_rate": (
                len(self_only_edge_ids) / mapped_edge_count
                if mapped_edge_count
                else None
            ),
            "diagonal_mapping_share": (
                diagonal_mappings / total_pair_mappings
                if total_pair_mappings
                else None
            ),
            "distinct_pair_mapping_share": (
                distinct_pair_mappings / total_pair_mappings
                if total_pair_mappings
                else None
            ),
            "distinct_technique_pair_coverage_over_mapped_edges": (
                len(distinct_pair_edge_ids) / mapped_edge_count
                if mapped_edge_count
                else None
            ),
            "distinct_technique_pair_coverage_over_all_temporal_edges": (
                len(distinct_pair_edge_ids) / total_edge_count
                if total_edge_count
                else None
            ),
            "collision_pair_share": (
                len(collision_pairs) / len(projection_pairs)
                if projection_pairs
                else None
            ),
        },
        "projection": {
            "technique_nodes": techniques,
            "technique_pairs": [list(pair) for pair in projection_pairs],
            "distinct_technique_pairs": [
                list(pair) for pair in distinct_technique_pairs
            ],
            "distinct_pair_provenance": {
                f"{source} -> {target}": edge_ids
                for (source, target), edge_ids in sorted(
                    distinct_pair_provenance.items()
                )
            },
            "edge_ids_with_distinct_technique_pair": distinct_pair_edge_ids,
            "edge_ids_without_distinct_technique_pair": edge_ids_without_distinct_pair,
            "edge_to_pairs": {
                edge_id: [list(pair) for pair in pairs]
                for edge_id, pairs in sorted(edge_to_pairs.items())
            },
            "edge_to_normalized_pairs": {
                edge_id: [list(pair) for pair in pairs]
                for edge_id, pairs in sorted(edge_to_normalized_pairs.items())
            },
            "pair_provenance": {
                f"{source} -> {target}": sorted(ids)
                for (source, target), ids in sorted(projected_provenance.items())
            },
            "collision_pairs": {
                f"{source} -> {target}": ids
                for (source, target), ids in sorted(collision_pairs.items())
            },
            "label_conflation": {
                f"{source} -> {target}": labels
                for (source, target), labels in sorted(label_conflation.items())
            },
            "shared_technique_endpoint_edge_ids": sorted(
                shared_technique_endpoint_ids
            ),
            "self_only_edge_ids": sorted(self_only_edge_ids),
            "unmapped_edge_ids": sorted(unmapped_edge_ids),
        },
        "strict_before_cycle_analysis": {
            "source_event_graph_is_acyclic": not bool(source_cycles),
            "projection_cycle_analysis_valid": not bool(source_cycles),
            "source_cycle_components": [list(c) for c in source_cycles],
            "projected_cycle_components": [list(c) for c in projection_cycles],
            "projected_cycle_provenance": projected_cycle_provenance,
            "note": (
                "Projection-induced cycle incidence is interpretable only when "
                "the source event-instance strict-order graph is acyclic, "
                "after normalizing AFTER(A,B) to BEFORE(B,A). Diagonal "
                "technique self-pairs are excluded from this cycle test and "
                "reported separately. A cycle generated by multiple mapping "
                "combinations from only one source event relation is marked "
                "as single-event-edge mapping fanout, not independent evidence "
                "of repeated event instances."
            ),
        },
    }


def edge_from_dict(row: Mapping[str, str]) -> TemporalEdge:
    """Create a TemporalEdge from a CSV/dictionary row."""
    return TemporalEdge(
        edge_id=row["edge_id"],
        source_event=row["source_event"],
        target_event=row["target_event"],
        relation=row.get("relation", "BEFORE"),
    )
