# Work graph — SCA-V4-003 (contract proposals of App v4 design passes 2 and 3)

Method: `chirality-root:bundled:workflow:construct-local-work-graph`, for an
undertaking run through `workflows/scope-change`.

- **Run:** `APP-V4-SCA003-20261002`. Records:
  [`AgentRuns/APP-V4-SCA003-20261002/`](../../AgentRuns/APP-V4-SCA003-20261002/).
- **Maintainer:** HELP_HUMAN under the recorded WORKING_ITEMS consultation.
- **Owner direction:** see the run's OWNER_DECISIONS.md.
- **Predecessor amendment:** SCA-V4-002 (CLOSED_WITH_OBSERVATIONS). Graph:
  DAG-003.

| ID / outcome | Write scope | Needs | Check | State |
|---|---|---|---|---|
| S0 Open run | Run folder; this graph | Owner direction | Committed | COMPLETE |
| P1 Ledger, impact, arcs, owner items | `AMENDMENT_PACKET/` | S0 | Every proposal once, with source and disposition | COMPLETE — 209 rows, 16 owner items |
| P3 Pre-change baseline | `BASELINE/` | S0 | Audit run, manifest | COMPLETE — 0/35/93 |
| P2 Exact ScopeOfWork blocks | `AMENDMENT_PACKET/SOW_REVISIONS_*.md` | P1 | Dry-run clean | COMPLETE — 147 blocks, 19/19 validate; RP1 repairs |
| V Independent review of the packet | `reviews/` | P1, P2, P3 | No blocking finding | COMPLETE — V23 HOLD, RP1, V23b READY FOR CHECKPOINT |
| K1 Owner checkpoint: groups 1–2 | OWNER_DECISIONS.md | V | Owner answer recorded | ACTIVE — package presented |
| AK… Apply, audit, group 3, dependency-extract, DAG currency/DAG-004 | per method | K1 | per method | PLANNED |
