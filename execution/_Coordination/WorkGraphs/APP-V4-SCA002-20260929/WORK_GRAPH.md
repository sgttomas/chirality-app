# Work graph — App v4: SCA-V4-001 closure audit and SCA-V4-002

Method: `construct-local-work-graph`.

- **Selected workflows:** `audit-scope-closure`, `scope-change`,
  `scope-of-work` (REVISE), `dependency-extract`, `project-dag`.
- **Maintainer:** HELP_HUMAN, this session, under the recorded
  WORKING_ITEMS consultation (as in APP-V4-BASIS-ALIGN-20260928).
- **Predecessor:** APP-V4-BASIS-ALIGN-20260928, merged in
  [#1055](https://github.com/sgttomas/chirality/pull/1055) at `8cca9170`.
- **Owner direction:** [OWNER_DECISIONS.md](../../AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md).

| ID / outcome | Write scope | Needs | Completion check | State |
|---|---|---|---|---|
| S0 Graph, direction | Run folder, graph | Owner | Committed | ACTIVE |
| CA1 SCA-V4-001 closure audit | `_Evaluation/` per audit-scope-closure (read-only on project state) | Accepted SCA-V4-001 | One closure verdict; rerun requirements | ACTIVE |
| P1 SCA-V4-002 packet (groups 1–2 prep) | Run folder `AMENDMENT_PACKET/` | Scope list; CA1 findings | Exact wording; owner items | ACTIVE |
| K1 Owner checkpoint A | — | P1 | Accept or adjust | PLANNED |
| AK Apply, group 3, REVISE, re-extract | Per the accepted route | K1 | Validations | PLANNED |
| D DAG-003 (if the arcs are confirmed) | `_DAG/_Candidates/DAG-003/` | AK | Strict audit; review; owner accepts | PLANNED |
| CA2 SCA-V4-002 closure audit | `_Evaluation/` | D | Verdict | PLANNED |
