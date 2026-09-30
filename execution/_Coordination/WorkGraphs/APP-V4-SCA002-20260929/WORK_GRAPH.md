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
| S0 Graph, direction | Run folder, graph | Owner | Committed | COMPLETE |
| CA1 SCA-V4-001 closure audit | `_Evaluation/` per audit-scope-closure (read-only on project state) | Accepted SCA-V4-001 | One closure verdict; rerun requirements | COMPLETE — OPEN, then superseded: CLOSED_WITH_OBSERVATIONS |
| P1 SCA-V4-002 packet (groups 1–2 prep) | Run folder `AMENDMENT_PACKET/` | Scope list; CA1 findings | Exact wording; owner items | COMPLETE |
| K1 Owner checkpoint A | — | P1 | Accept or adjust | COMPLETE — DECISION-2 |
| AK Apply, group 3, REVISE, re-extract | Per the accepted route | K1 | Validations | COMPLETE — DECISION-3; 9 REVISEs; 11 UPDATEs |
| D DAG-003 (if the arcs are confirmed) | `_DAG/_Candidates/DAG-003/` | AK | Strict audit; review; owner accepts | COMPLETE — DECISION-4; published; CURRENT |
| CA2 SCA-V4-002 closure audit | `_Evaluation/` | D | Verdict | COMPLETE — CLOSED_WITH_OBSERVATIONS |
