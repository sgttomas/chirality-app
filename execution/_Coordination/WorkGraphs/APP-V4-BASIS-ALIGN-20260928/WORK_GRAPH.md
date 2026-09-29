# Work graph — App v4: align the accepted basis (SoW, registers, DAG-002, wording)

Method: `chirality-root:bundled:workflow:construct-local-work-graph`.

- **Selected workflows:**
  - `chirality-root:bundled:workflow:scope-change` (basis and SoW);
  - `…:scope-of-work` (REVISE);
  - `…:dependency-extract` (registers);
  - `…:project-dag` (currency and successor).
- **Maintainer:** HELP_HUMAN, this Claude Code session. It acts as the
  undertaking's integrator under a **recorded consultation of
  `agents/AGENT_WORKING_ITEMS.md`** (sha256 prefix `9ae4bea25bd9`). No separate
  WORKING_ITEMS session is running; the workflows name WORKING_ITEMS as
  coordinator. It dispatches bounded Type 2 TASK executors directly.
- **Owner direction:** see [OWNER_DECISIONS.md](../../AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md).

## Intent

Bring the accepted basis in line with the owner's decisions (DECISION-1…5),
and with the first increment's closeout proposals, before more design builds
on it.

**Completion conditions:**

1. The scope-change amendment is prepared, accepted by the owner at the
   grouped checkpoints, and applied:
   - the PRD, ARCHITECTURE, HOST_INTEGRATION and EXAMINATION wording;
   - the per-deliverable ScopeOfWork revisions by `scope-of-work` REVISE.
2. The register rows are applied per deliverable, and a currency audit
   records the departure.
3. DAG-002 is assembled, audited (`audit_dag.py --canonical --strict`),
   independently reviewed and accepted by the owner, and `_DAG/_LATEST.md`
   moves.
4. The owner confirms lifecycle recording, or leaves it for later.
5. There is an independent review, PRs merged under standing authority, a
   receipt and MEMORY rows.

**Excluded:**

- SWBPIPE, PEC and Domains work;
- host joins;
- new design content;
- any SoW change not traced to an owner decision or an accepted C1 proposal.

## Work

States: PLANNED, READY, ACTIVE, BLOCKED, UNCERTAIN, COMPLETE.

| ID / outcome | Write scope | Needs | Completion check | State |
|---|---|---|---|---|
| B0 Graph, decisions, briefs | Run folder, graph | Owner direction | Committed | COMPLETE |
| P1 Amendment packet (scope-change groups 1–2 preparation) | Run folder `AMENDMENT_PACKET/` only | C1-A/B/C, CLOSEOUT_ACCOUNT, DECISION-3/4/5, intake findings | Atomic actions validated; exact wording for the basis docs and each SoW; the C1 proposals refreshed against the current Design; impact on the DAG listed | COMPLETE |
| P2 DAG successor preparation | Run folder `DAG_PREP/` only | C1 register/arc proposals, DAG-001 | Mirror rows per deliverable; the 40 arcs re-checked against current evidence; the disputed arc analysed; SCC recomputation; a successor plan | COMPLETE |
| K1 Owner checkpoint A (scope-change groups 1+2) | — | P1, P2 | The owner accepts or adjusts the amendment, the lifecycle and the disputed arc | ACTIVE — presented |
| A* Apply | Basis docs; ScopeOfWork (REVISE); registers | K1 | Per-deliverable briefs; validation | PLANNED |
| D1 Currency audit → DAG-002 candidate, audit, review | `_Evaluation/DAGCurrency/`, `_DAG/_Candidates/DAG-002/` | A* | audit_dag strict passes; independent review | PLANNED |
| K2 Owner checkpoint B (DAG-002 acceptance; scope-change group 3) | — | D1, review | Accept / reject / repair | PLANNED |
| F Publish, receipt, PRs | `_DAG/DAG-002`, `_LATEST`, receipt, MEMORY | K2 | Merged | PLANNED |
