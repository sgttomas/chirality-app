# Cycle-Driven Resolution — Dependency Graph Doctrine

Chirality AI Ltd.
Date: 2026-06-15, Revision 0, Issued for Use

**How dependency graphs are built, audited, and kept acyclic across the agent operating system.**

---

## 1. Purpose

This document defines the operating system's doctrine for building and
maintaining dependency graphs — the directed graphs (e.g., a project's approved
`DAG`) that record what depends on what. It is **project-neutral framework
governance**: it states the reusable principle and the method, while each project
records its own *adoption*, *rollout*, and *re-derivation triggers* in its own
coordination, plan, and decision surfaces.

It is referenced by the shared agent instructions
(`agents/AGENT_WORKING_ITEMS.md`, `agents/AGENT_TASK.md`) and by the `AGENTS.md`
Governance Integration Rules, where it is a peer of the snapshot, handoff-state,
closure, and sequencing rules.

**Provenance.** Distilled from a 2026-06-13 design discussion on dependency
modeling. The core insight: a DAG is objective-relative and its edges are often
subjective, but the strongly-connected-component (SCC) condensation is unique and
always a DAG. The doctrine makes *cycle-driven resolution* an explicit, reusable
competence rather than an ad-hoc audit footnote.

## 2. The doctrine

1. **No canonical DAG a priori.** A dependency graph is relative to a stated
   *objective* and *edge semantics* (build-order ≠ runtime ≠ knowledge ≠
   data-flow ≠ deployment). Fix both before drawing edges; never conflate graphs
   drawn for different objectives.

2. **SCCs are the objective skeleton.** Under fixed semantics the SCC
   condensation is unique and always a DAG. Treat the SCC set — not the
   hand-drawn edges — as the authoritative signal of *where ordering is genuinely
   undecided*. An edge in no cycle needs no adjudication; its direction is
   consistent with some valid global order regardless of interpretation.

3. **Localize and record the subjective calls.** Interpretive decisions are
   required only on cycle-closing edges. Resolve each non-trivial SCC by one of
   four named moves, with a recorded rationale — never reconcile a cycle
   silently:
   - **Decompose** a too-coarse node (the usual root cause — split interface from
     implementation, concern from concern).
   - **Invert** a dependency behind a contract/interface so the edge reverses.
   - **Merge** the cluster and accept it as one indivisible unit.
   - **Cut** an edge by reclassifying it as out-of-objective (e.g.,
     runtime/test/optional, not sequencing).

   *Decompose* and *invert* are design refinements an agent may propose; *cut*
   and *merge* encode a subjective interpretation into authority and are
   therefore **human-gated**.

4. **Cycle-participating edges stay non-gating until resolved.** An edge inside an
   unresolved SCC must not drive blocker queues, wave placement, schedule,
   priority, dispatch readiness, or implementation-readiness claims until the SCC
   is resolved.

5. **Proportionality.** Obvious resolutions get a one-line note; contested ones
   (cut/merge, or objective-dependent) get a decision packet. Apply the lens when
   work is tangled or an audit flags an SCC — do not ritualize it everywhere.

## 3. Guardrails

- **Objective-scoping.** The doctrine is applied *per objective + edge
  semantics*. It does not unify graphs across objectives, and it catches
  *circular* subjectivity, not *ordering/priority* subjectivity — an
  acyclic-but-"wrong" graph is not flagged by SCC analysis.
- **Proportionality is load-bearing.** The failure mode is ossifying into "every
  cycle needs a packet." Trivial decompose/invert → a one-line note; only
  cut/merge or objective-dependent calls → a packet.
- **Hairball caution.** A single giant SCC reduces "resolve into a DAG" to a
  feedback-arc-set problem (NP-hard); tooling should report SCC sizes so large
  components get human attention rather than a naive auto-cut.

## 4. Graph lifecycle and re-derivation trigger

The active edge set of an approved graph is kept **acyclic by construction**;
cycles live only in a non-gating candidate layer pending resolution.

A new approved graph version is **event-driven by a decomposition revision /
scope change (SCA), not periodic.** That event is the occasion to re-run the
dependency extraction and closure audit and to resolve any new SCC by a recorded
move. Absent such an event, an approved graph that still matches its decomposition
basis is current; re-deriving it produces no new information and is not warranted.

When the trigger fires, the method is applied at the **closure audit**: compute
SCCs, and for each non-trivial SCC choose decompose / invert / merge / cut with a
recorded rationale, iterating until the strict graph is acyclic.

## 5. Tooling

The method is supported by shared tooling under `tools/`:

- `tools/coordination/audit_dag.py` — computes SCCs (Tarjan) and emits the DAG
  audit.
- `tools/coordination/analyze_dep_closure.py` — closure-level analysis (SCCs,
  orphans, hubs, bidirectional pairs).
- the `dependency-extract` skill and the `AGGREGATION` agent — produce and roll
  up the deliverable-local dependency registers the graph is built from.

Tooling reports SCC membership and sizes; it does not make cut/merge decisions,
which are human-gated.

## 6. How agents and projects apply it

- **Agents.** The shared agent instructions carry the habit: a structural cycle
  is surfaced like any other conflict and resolved by a named move, never
  silently linearized (`AGENT_WORKING_ITEMS.md` Conflict-transparency invariant +
  the Phase 3 Conflict-Table companion; `AGENT_TASK.md` epistemic controls — a
  bounded worker surfaces an in-slice SCC with the four options rather than
  choosing an order).
- **Projects.** Each project records its own adoption, rollout, and DAG
  re-derivation triggers in its own coordination record, plan, and decision
  register. This doctrine is the shared principle they reference; it is not a
  substitute for those project-local records.
- **Instances.**
  - *chirality-piping* adopted the doctrine on 2026-06-15 (`DEC-040`); its
    adoption record, surface-by-surface rollout, and DAG-007 re-derivation
    trigger live in
    `projects/chirality-piping/plans/PLAN_2026-06-13_cycle_driven_resolution_doctrine.md`.
    Its active graph has 0 active SCCs (dormant during application integration).
  - *chirality-app-dev* is the live operational exemplar: its
    `PKG-00_DAG_Closure_and_Project_Control` runs SCC closure against an active
    cyclic graph, recording retire/preserve (cut/keep) rulings with immutable
    closure snapshots.

## Document History

| Date | Revision | Description |
|------|----------|-------------|
| 2026-06-15 | 0 | Initial issue. Lifted from the chirality-piping cycle-driven resolution doctrine (`PLAN_2026-06-13`, adopted `DEC-040`) into a project-neutral shared doctrine. |
