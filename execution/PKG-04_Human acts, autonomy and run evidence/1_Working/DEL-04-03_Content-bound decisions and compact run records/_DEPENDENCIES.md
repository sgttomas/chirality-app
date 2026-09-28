# Dependencies: DEL-04-03 Content-bound decisions and compact run records

## Dependency Tracking Mode
- **Mode:** FULL_GRAPH
- **Register:** the declared sections of this file together with Dependencies.csv (schema v3.1) when present (docs/SPEC.md §5.3)
- **Notes:** `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`; no individual human-declared edge yet. Accepted interface descriptions are sources for later extraction, not declarations inferred by scaffolding.

---

## Declared Upstream (I need these before I can proceed)
- None declared at initial setup.

## Declared Downstream (These need me)
- None declared at initial setup.

---

## Extracted Dependency Register

- 20 ACTIVE EXTRACTED rows: 10 ANCHOR (1 parent + 7 scope + 2 objective traces), 10 EXECUTION. No DECLARED or RETIRED rows.
- Execution targets: 2 DELIVERABLE, 3 PACKAGE, 5 EXTERNAL, 0 UNKNOWN; 4 UPSTREAM and 6 DOWNSTREAM.

| Dependency ID | Class | Direction / type | Target |
|---|---|---|---|
| DEP-04-03-001 | ANCHOR | UPSTREAM / IMPLEMENTS_NODE | PKG-04 |
| DEP-04-03-002 | ANCHOR | UPSTREAM / TRACES_TO_REQUIREMENT | SOW-092 |
| DEP-04-03-003 | ANCHOR | UPSTREAM / TRACES_TO_REQUIREMENT | SOW-093 |
| DEP-04-03-004 | ANCHOR | UPSTREAM / TRACES_TO_REQUIREMENT | SOW-094 |
| DEP-04-03-005 | ANCHOR | UPSTREAM / TRACES_TO_REQUIREMENT | SOW-095 |
| DEP-04-03-006 | ANCHOR | UPSTREAM / TRACES_TO_REQUIREMENT | SOW-096 |
| DEP-04-03-007 | ANCHOR | UPSTREAM / TRACES_TO_REQUIREMENT | SOW-143 |
| DEP-04-03-008 | ANCHOR | UPSTREAM / TRACES_TO_REQUIREMENT | SOW-186 |
| DEP-04-03-009 | ANCHOR | UPSTREAM / TRACES_TO_REQUIREMENT | OBJ-004 |
| DEP-04-03-010 | ANCHOR | UPSTREAM / TRACES_TO_REQUIREMENT | OBJ-005 |
| DEP-04-03-011 | EXECUTION | DOWNSTREAM / INTERFACE | PKG-02 |
| DEP-04-03-012 | EXECUTION | DOWNSTREAM / INTERFACE | PKG-03 |
| DEP-04-03-013 | EXECUTION | DOWNSTREAM / INTERFACE | PKG-06 |
| DEP-04-03-014 | EXECUTION | DOWNSTREAM / HANDOVER | DEL-04-02 |
| DEP-04-03-015 | EXECUTION | DOWNSTREAM / HANDOVER | DEL-09-11 |
| DEP-04-03-016 | EXECUTION | DOWNSTREAM / INTERFACE | Responsible host implementation owner — host-agent run recording |
| DEP-04-03-017 | EXECUTION | UPSTREAM / INTERFACE | DEP-001 |
| DEP-04-03-018 | EXECUTION | UPSTREAM / INTERFACE | Supplied evidence of an actually performed human act |
| DEP-04-03-019 | EXECUTION | UPSTREAM / CONSTRAINT | Owner with affected App/SWB contract owners — operation classes and classifier-permission choices |
| DEP-04-03-020 | EXECUTION | UPSTREAM / CONSTRAINT | Shared contract, SWB implementation and App/shared contract owners — affected implementation allocation |

## Lifecycle Summary

- ACTIVE: 20; RETIRED: 0. Closure: NOT_APPLICABLE 10 (anchors); PENDING 10 (execution); SATISFIED 0.
- INITIALIZED remains the checked local-contract threshold recorded by the manager. For the two local Deliverable targets, RequiredMaturity=INITIALIZED does not establish actual run-record handoff, receipt, implementation, witness, adoption or qualification. Package/external maturity remains TBD.
- Actual host evidence, faithful-recording case evidence and affected owner choices remain distinct inputs/conditions. No execution availability or global closure is claimed.

## Run Notes

- Method: `chirality-root:bundled:workflow:dependency-extract`; MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE.
- SCOPE=DEL-04-03; RUN_ROOT=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`. DECOMPOSITION_PATH=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`.
- SOURCE_DOCS=ScopeOfWork.md; ANCHOR_DOC=ScopeOfWork.md; EXECUTION_DOC_ORDER=[ScopeOfWork.md]; DOC_ROLE_MAP=DEFAULT. Pass 1 completed with ten anchors before Pass 2 added ten execution rows.
- Canonical companion registers resolved identity/labels only. Frozen historical candidate labels do not reverse the accepted Group3 basis. Every extracted edge is supported by this Deliverable's ScopeOfWork.md; sibling contracts supply no edges.
- Five consumer handoffs are explicit: PKG-02/03/06 consume record meaning; App DEL-04-02 receives run evidence; App DEL-09-11 receives records for its separate later witness. The host-agent shared-format interface is an additional external output. Package consumers are not guessed down to individual Deliverables.
- External host evidence is required only for host-dependent use. DEP-001 is the accepted external-contribution identifier, not a local DependencyID or App Deliverable; its namespace is the accepted snapshot's External_Dependencies.csv as cited in ScopeOfWork.md B2/TBD-002. The exact external implementation/evidence location is not supplied. No common service, deployment, wire format, persistence or reuse allocation is prescribed.
- Positive faithful-recording cases use evidence of an actual performed act. This input does not require a fresh act, another prior act, universal acceptance, professional judgment, or global reserved-class ruling. Recording remains distinct from the actor's decision. Missing or unsupported acts/outcomes remain unknown.
- OI-001/OI-002 operation/classifier choices and OI-013/OI-014 implementation-allocation choices apply only at their affected points of need. Ordinary-file authority, faithful attribution and content-bound lapse may proceed independently. No blanket hold is created.
- No edge was inferred from DEL-04-01 policy ownership, the excluded acts list, source citations, runtime behavior alone, or later witness ownership. REQ-005's actual record transfer supports the later-witness handoff without making witness participation a prerequisite here.
- Declared mirroring: added 0, refreshed 0, retired 0; skipped 2 initial-setup placeholders. Human-owned sections are byte-identical; prior run history is preserved.
- Checks passed: canonical 29-column schema; 22 distinct enum-value validations; 37 stable-ID validations; one parent; no duplicated edge/ID; evidence present and verbatim (maximum 30 words); applicable field completeness and target placement; source SHA before/after; counts and declared-section preservation. External DEP-001 is not subjected to the local DEP-{PKG}-{DEL}-{SEQ} format. Optional whole-execution EVQ/DRB report not run; direct local evidence/prefix checks passed.
- Remaining limits: actual technical evidence and decisions are not supplied by extraction; their fulfilment remains PENDING. External evidence/case identities and exact owner-choice dispositions remain unresolved at the stated points of need. Local extraction makes no project DAG, scheduling, acceptance, adoption or lifecycle decision.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:26:48+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted Group3 decomposition resolved at `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. ACTIVE 20 (ANCHOR 10, EXECUTION 10); no integrity warnings; conditional/external input limitations retained.
