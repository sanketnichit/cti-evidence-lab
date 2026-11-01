# Projection Metrics v0.1 — Event Instances to ATT&CK Techniques

**Date:** 1 November 2026  
**Status:** Candidate definitions with a synthetic Python prototype; not validated on human-annotated CTI data.

## 1. Scope

The proposed primary experiment is descriptive: compare a human-annotated event-instance temporal graph with a report-level ATT&CK technique projection. It does not begin with a learned model.

The goal is to measure whether event-instance identity and explicitly supported temporal relations are lost, conflated or made ambiguous when multiple occurrences are normalized to ATT&CK concepts.

## 2. Objects and notation

For one report:

- (V): set of human-resolved event instances (`instance_status = RESOLVED`).
- (M): set of text mentions, each linked to an event instance where identity is resolved.
- (A(v) \subseteq T): set of zero or more evidence-backed ATT&CK technique/sub-technique IDs assigned to event instance (v), with one pinned ATT&CK version.
- (E_{\text{before}} \subseteq V \times V): explicitly supported, adjudicated strict BEFORE relations between event instances.
- (E_{\text{temp}}): all explicitly supported, adjudicated temporal relations if the experiment later includes overlap/simultaneity as separate edge labels.

Only resolved event instances enter (V). Keep unresolved mentions, generic behaviour statements and non-events in separate counts. Never turn a generic technique statement into an event instance solely because it has an ATT&CK mapping.

A single event instance may have multiple ATT&CK mappings. A multi-mapped event remains one event node. Multiple mentions or technique mappings do not imply multiple executions.

## 3. Projection

Let the report's unique technique node set be:

[
T_r = \bigcup_{v \in V} A(v)
]

For an event-to-event temporal relation (e=(u,v)), its possible ordered technique-pair image is:

[
Q(e) = A(u) \times A(v)
]

If either endpoint has no supported technique mapping, (Q(e)=\varnothing); that temporal relation is not representable in the ATT&CK-only projection. Track it as unmapped rather than dropping it silently.

The projected technique-pair set is:

[
P_r = \bigcup_{e \in E_{\text{temp}},\; Q(e)\ne\varnothing} Q(e)
]

This set projection deduplicates repeated technique pairs. Keep a provenance map from each projected pair back to all source event-pair relations; never overwrite the original event graph. Only explicit positive temporal labels may enter this projection: BEFORE, AFTER, OVERLAP, SIMULTANEOUS and CONCURRENT_UNSPECIFIED. NO_TEMPORAL_CLAIM, VAGUE_OR_AMBIGUOUS, NOT_ASSESSABLE, and causal/dependency/narrative-order labels must never be supplied as positive temporal edges.

**Versioning rule:** compare exact ATT&CK IDs under a single pinned release. Parent/sub-technique collapsing is a separate sensitivity analysis, not something to do implicitly.

## 4. Candidate measurements

### 4.1 Repeated-instance prevalence

For technique (t) in report (r), let (V_{r,t}=\{v\in V_r:t\in A(v)\}).

[
R_r = \mathbb{1}[\exists t: |V_{r,t}|\ge 2]
]

Across a defined sample, report the fraction of eligible reports with (R_r=1), alongside numerator/denominator and confidence interval. A 5–8 report pilot must **not** be presented as an estimate for all CTI reports.

This metric counts distinct human-resolved event instances, not mentions.

### 4.2 Shared technique mappings across temporal-edge endpoints

For each mapped explicit temporal event edge (e=(u,v)), define:

[
S(e) = A(u) \cap A(v)
]

Report:
- **same-technique-overlap edge rate:** fraction of mapped event edges for which (S(e)\ne\varnothing);
- **self-only edge rate:** fraction for which every pair in (Q(e)) is a self-pair ((t,t));
- **diagonal projection share:** fraction of all event-edge-to-technique-pair mappings ((e,(a,b))) for which (a=b).

These are distinct. With multi-label mappings, two instances may share one technique and also project to cross-technique pairs. Do not call the entire event edge “lost” when only one of several projected pairs is a self-pair.

**Unit distinction:** the edge rate counts each source event relation once, even if either endpoint has multiple technique mappings. The pair-mapping share counts each distinct mapping combination in \\(Q(e)\\). Always report both units; do not describe mapping-combination counts as event-edge counts.

If the target graph discards self-loops (as many technique-pair candidate generators do), the diagonal part is unrepresentable in that graph. State the graph convention explicitly.


### 4.3 Omission under a distinct-technique-pair restriction

ChronoCTI's paper defines its candidate pair universe over 120 techniques using \((120^2-120)/2\), which excludes same-technique diagonal pairs. Its public graph code also constructs candidate pairs only for distinct technique indices. This is a documented design choice in that approach, not a claim that all CTI graph systems must do the same.

For each event relation (e=(u,v)), split its technique-pair image into:

[
Q_{diag}(e)={(t,t):t\in A(u)\cap A(v)}
]

[
Q_{distinct}(e)=Q(e)\setminus Q_{diag}(e)
]

Record three separate outcomes:

1. **Fully omitted event relation:** (Q_{distinct}(e)=\varnothing). The event pair has no non-diagonal technique pair and is therefore unavailable under a distinct-technique-pair candidate rule.
2. **Partially represented event relation:** both (Q_{diag}(e)\ne\varnothing) and (Q_{distinct}(e)\ne\varnothing). Some technique mapping combinations are excluded, but at least one distinct pair remains.
3. **No diagonal mapping:** (Q_{diag}(e)=\varnothing). All of the event edge's mapping combinations are non-diagonal.

The implementation reports:
- count of unique distinct-technique pairs;
- count of event edges with at least one distinct pair;
- count of event edges without a distinct pair;
- pair-mapping share that is non-diagonal;
- edge-level coverage over mapped edges and over all positive temporal edges;
- a provenance map from each distinct pair to its source event edges.

Unmapped event edges are reported separately, even though they also have no distinct technique pair. This prevents an unmapped edge from being misreported as a same-technique omission.

**Interpretation rule:** for multi-mapped event instances, do not label an entire temporal relation as lost just because one shared technique ID creates a diagonal pair. It is fully omitted only when no non-diagonal pair remains. The current metrics are descriptive and do not reproduce every stage or label convention of ChronoCTI.

**Primary paper source:** Rahman et al. (2025), Section 4.5.1–4.5.2: https://doi.org/10.1007/s10115-025-02491-6
### 4.4 Technique-pair collision / occurrence conflation

For a projected pair (p=(a,b)\in P_r), let:

[
E_p = \{e\in E_{\text{temp}}:p\in Q(e)\}
]

Report:
- number and proportion of projected technique pairs with (|E_p|\ge2);
- excess event-edge multiplicity (C_r=\sum_{p\in P_r}\max(0,|E_p|-1));
- distribution of (|E_p|), not just the average.

This measures how many different event-instance relations share the same technique pair after projection. Report separately whether their temporal labels agree or conflict. If one event edge maps to multiple technique pairs because it is multi-label, the provenance map must retain that fan-out.

### 4.5 Relation-label conflation (optional extension)

If (E_{\text{temp}}) contains multiple temporal labels, retain the label on every source edge. For each projected pair (p), count the distinct normalized temporal labels among (E_p).

A projected pair with multiple labels is label-ambiguous under a single-label pair model. Do not merge BEFORE, AFTER, OVERLAP, SIMULTANEOUS or CONCURRENT_UNSPECIFIED into one class. Any normalization (e.g. AFTER(A,B) to BEFORE(B,A)) must preserve the original direction and evidence in the source annotation.

### 4.6 Projection-induced strict-order cycles

Use only explicitly supported strict BEFORE and AFTER edges. Normalize AFTER(A,B) as BEFORE(B,A) in the cycle-analysis view; retain the original label and endpoints in the source annotation. First check that the adjudicated event-instance graph is acyclic. Exclude or separately adjudicate source-level contradictory cycles. Then attribute every projected cycle to the source event edges that generated it; multi-mapped endpoints can create cycles through a single-edge Cartesian-product fan-out.

Project these edges to a unique-technique graph and check whether contraction creates a directed cycle that was absent from the event-instance graph. However, the implementation forms the Cartesian product of endpoint mapping sets. A single event relation whose source and target both have multiple technique mappings can therefore generate both directions of a technique pair (for example, A→B and B→A) by mapping fan-out alone. This is a projection artifact, not evidence of multiple event occurrences.

For every projected strongly connected component, retain the source event-edge IDs that generated its internal technique edges. Separate:
- **single-edge mapping-fanout cycles:** all internal technique edges in the component are generated by one source event relation;
- **multi-edge projection cycles:** the component requires at least two distinct source event relations.

Only the second category is a candidate for an occurrence-conflation explanation, and it still requires source-text inspection. Report both categories and do not interpret all projected cycles as repeated occurrences.

A canonical example of a multi-edge projection cycle is:

[
a_1 \rightarrow b_1 \rightarrow a_2,\quad A(a_1)=A(a_2)=\{T_A\},\quad A(b_1)=\{T_B\}
]

The instance graph is acyclic, but its technique projection contains (T_A\rightarrow T_B\rightarrow T_A).

Report report-level cycle incidence, the number of projected SCCs, the number attributable to one source-edge mapping fan-out, and the number requiring multiple source event edges. Do not mix overlap, simultaneity, concurrency, causal/dependency or narrative-order edges into this test.

## 5. Coverage and missingness

Report projection coverage separately:
- fraction of resolved event instances with at least one supported ATT&CK mapping;
- fraction of explicit temporal event edges for which both endpoints have at least one mapping;
- fraction of relation-evidence spans that are present and offset-valid;
- number of unresolved event mentions and generic-behaviour statements.

Do not remove unmapped endpoints from the denominator without showing the coverage loss. An ATT&CK projection cannot preserve identity for unmapped event instances.

## 6. Toy tests required before implementation

Manually construct and hand-check at least these cases:

1. **One execution, several mentions:** all mentions corefer to one event instance; no repeated-instance count.
2. **Two distinct executions, same technique:** two resolved event nodes map to one ATT&CK node.
3. **Two same-technique events with BEFORE:** projection creates a self-relation; verify whether the chosen technique graph keeps or discards self-loops.
4. **Many event pairs, one technique pair:** verify collision count and retained provenance.
5. **Multi-label endpoint:** one event maps to more than one technique; verify fan-out without duplicate event nodes.
6. **Unmapped endpoint:** relation remains in event graph but cannot enter ATT&CK pair graph.
7. **Projection-induced cycle:** verify only strict BEFORE edges can create the reported cycle metric.
8. **Conflicting/ambiguous text:** unresolved relations stay out of positive-edge metrics.

For each toy case, manually compute the event graph, mapping sets, projected pairs and metric values. A second person should independently check the worked examples if possible.

## 7. Interpretation constraints

- A graph projection can create representational collisions; it does not prove the source report's underlying behaviour was misinterpreted.
- An ATT&CK concept is a taxonomy category, not an occurrence identifier.
- A temporal expression alone does not establish a relation between two events.
- Sentence/narrative order alone does not establish physical chronology.
- Attack Flow dependency edges and STIX semantic relationships are not temporal BEFORE relations.
- Report positive and negative/ambiguous evidence together. Do not select only reports that show the effect.
- The pilot is a feasibility study. Only a larger, transparently sampled corpus can estimate prevalence or support statistical claims.

## 8. Implementation gate and status

A pure-Python toy implementation is in `src/projection_metrics.py`; tests are in `tests/test_projection_metrics.py`. It rejects non-positive/ambiguous labels, retains relation provenance, canonicalizes symmetric relations and normalizes AFTER to strict-before orientation for cycle checks. It has not been executed in this session and has not been used on human-annotated CTI data.

Do not implement a learned model yet. First:
1. finish source/provenance checks;
2. select 5–8 reports with transparent criteria and more than one vendor if feasible;
3. run human annotation under protocol v0.3;
4. have a second human annotate an overlapping subset if possible;
5. test toy cases and finalize definitions;
6. then choose statistical summaries and whether a predictive task is justified.


## 9. Toy implementation added

A pure-Python prototype is in `src/projection_metrics.py`; toy unit tests are in `tests/test_projection_metrics.py`; a synthetic example is in `examples/toy_projection_demo.py`.

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python examples/toy_projection_demo.py
```

The prototype:
- accepts only explicit positive temporal relation labels;
- supports zero, one or multiple ATT&CK mappings per event instance;
- canonicalizes symmetric technique pairs and preserves direction for BEFORE/AFTER;
- retains the many-to-many provenance from technique pairs back to source event edges;
- reports unmapped edge coverage rather than silently dropping those edges;
- keeps same-technique diagonal projections separate from strict cycle analysis;
- only treats projection-induced cycles as interpretable if the source BEFORE graph is acyclic.

A GitHub Actions workflow is configured to run the standard-library unit tests on relevant pushes and pull requests. Its execution status has not yet been confirmed from this audit session. These tests validate synthetic cases only; they do not validate the annotation definitions or establish any empirical finding.

## 9. Reproduction commands

From the repository root:

```bash
python -m unittest discover -s tests -v
python examples/toy_projection_demo.py
```

These commands have been added to the project README and GitHub Actions workflow. The GitHub connector did not return any commit status entries during this audit, so test execution has **not** been independently verified. Do not claim a passing test suite until a run is observed.


## 10. Mapping fan-out and cycle provenance clarification — 1 November 2026

The implementation uses \\(A(u)\\times A(v)\\) for a temporal edge \\(e=(u,v)\\). This is a set-valued projection of every source/target mapping combination, not a claim that every combination is independently asserted in the report. For a multi-mapped event endpoint, it may create multiple directed technique pairs from one source event relation.

Accordingly:
- distinguish source **event-edge counts** from **event-edge-to-technique-pair mapping counts**;
- preserve the provenance map from each projected pair to the original event-edge IDs;
- report whether a projected SCC is generated by one source event edge or requires multiple source event edges;
- do not treat a single-edge mapping-fanout cycle as evidence of repeated event instances;
- retain multi-mapping support, but report the cycle analysis as a sensitivity diagnostic until the mapping-to-graph semantics are justified.

The code field `shared_technique_endpoint_edges` means that source and target event instances share at least one ATT&CK technique ID. It does **not** mean the temporal relation label is OVERLAP. The older `same_technique_overlap_edges` label was ambiguous and has been renamed.
