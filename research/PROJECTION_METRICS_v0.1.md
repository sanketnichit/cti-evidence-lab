# Projection Metrics v0.1 — Event Instances to ATT&CK Techniques

**Date:** 1 November 2026  
**Status:** Candidate definitions for toy-graph testing and pilot review; not finalized or implemented.

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

### 4.2 Same-technique endpoint overlap

For each mapped explicit temporal event edge (e=(u,v)), define:

[
S(e) = A(u) \cap A(v)
]

Report:
- **same-technique-overlap edge rate:** fraction of mapped event edges for which (S(e)\ne\varnothing);
- **self-only edge rate:** fraction for which every pair in (Q(e)) is a self-pair ((t,t));
- **diagonal projection share:** fraction of all event-edge-to-technique-pair mappings ((e,(a,b))) for which (a=b).

These are distinct. With multi-label mappings, two instances may share one technique and also project to cross-technique pairs. Do not call the entire event edge “lost” when only one of several projected pairs is a self-pair.

If the target graph discards self-loops (as many technique-pair candidate generators do), the diagonal part is unrepresentable in that graph. State the graph convention explicitly.

### 4.3 Technique-pair collision / occurrence conflation

For a projected pair (p=(a,b)\in P_r), let:

[
E_p = \{e\in E_{\text{temp}}:p\in Q(e)\}
]

Report:
- number and proportion of projected technique pairs with (|E_p|\ge2);
- excess event-edge multiplicity (C_r=\sum_{p\in P_r}\max(0,|E_p|-1));
- distribution of (|E_p|), not just the average.

This measures how many different event-instance relations share the same technique pair after projection. Report separately whether their temporal labels agree or conflict. If one event edge maps to multiple technique pairs because it is multi-label, the provenance map must retain that fan-out.

### 4.4 Relation-label conflation (optional extension)

If (E_{\text{temp}}) contains multiple temporal labels, retain the label on every source edge. For each projected pair (p), count the distinct normalized temporal labels among (E_p).

A projected pair with multiple labels is label-ambiguous under a single-label pair model. Do not merge BEFORE, AFTER, OVERLAP, SIMULTANEOUS or CONCURRENT_UNSPECIFIED into one class. Any normalization (e.g. AFTER(A,B) to BEFORE(B,A)) must preserve the original direction and evidence in the source annotation.

### 4.5 Projection-induced strict-order cycles

Use only explicitly supported strict BEFORE edges. First check that the adjudicated event-instance graph is acyclic. Exclude or separately adjudicate source-level contradictory cycles.

Project these edges to a unique-technique graph and check whether contraction creates a directed cycle that was absent from the event-instance graph. A canonical example is:

[
a_1 \rightarrow b_1 \rightarrow a_2,\quad A(a_1)=A(a_2)=\{T_A\},\quad A(b_1)=\{T_B\}
]

The instance graph is acyclic, but its technique projection contains (T_A\rightarrow T_B\rightarrow T_A).

Report report-level cycle incidence and the number of projected cycles, not just whether an arbitrary graph traversal found one. Do not mix overlap, simultaneity, concurrency, causal/dependency or narrative-order edges into this test.

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

## 8. Current implementation gate

Do not implement a model yet. First:
1. finish source/provenance checks;
2. select 5–8 reports with transparent criteria and more than one vendor if feasible;
3. run human annotation under protocol v0.2;
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
