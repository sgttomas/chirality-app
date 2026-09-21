# Agent Disposition Matrix — D-GOV-11

> **Status:** Closed migration record. Every disposition in this matrix,
> including the D-GOV-18 supersessions, was verified implemented against the
> live tree on 2026-08-02 (see Verification Record below); closure was
> accepted by the owner through the merge of the closing tranche. This
> record is historical: `AGENTS.md` is the live agent index, and the
> substance of the Removal Rule is carried forward by D-GOV-13 and the
> dedicated-specialist requirements in `AGENTS.md`. Roles created after
> this migration by their own rulings (e.g., TASK_MANAGEMENT per D-GOV-32)
> are outside this record's scope.

| Role / family | Disposition | Destination or basis | Current state |
|---|---|---|---|
| HELP_HUMAN | REWRITE | Sole Agent 0 Supervising Architect | Implemented; managed runtime required for executable child sessions |
| HELPS_HUMANS | EXPAND | Agent 1 component-design manager | Implemented |
| DECOMP_BASE | EXTRACT | `docs/DECOMPOSITION_STANDARD.md`; design assistance to HELPS_HUMANS | Implemented; persona removed |
| SKILLMAKER | MERGE | HELPS_HUMANS skill-design mode | Implemented; persona removed, skill standards retained |
| TOOLMAKER | MERGE | HELPS_HUMANS tool-design mode | Implemented; persona removed, tool registry/contracts retained |
| CONTEXT_TRANSPOSE | MERGE | HELPS_HUMANS component/migration design; bounded run work uses TASK or ephemeral generalist | Implemented; persona removed |
| SCHEDULING | MERGE | PROJECT_SETUP schedule workflow; calculation/rendering downward | Implemented at instruction layer; persona removed |
| EVALUATION | EXPAND → **superseded by D-GOV-18 (RULED 2026-07-21): SLIM-TO-SHELL** | Generic audit orchestration plus old RECONCILIATION audit/coherence semantics | Implemented. D-GOV-18 Item 2 (RULED) re-disposes EVALUATION as a thin Agent 1 shell + new `evaluation-protocol` skill (full demotion structurally infeasible); shell retains name, subagents allowlist, `_Evaluation/` quarantine, fan-in validation. Effective per D-GOV-18 ruling 2026-07-21; Item 8 PR sequence landed (verified 2026-08-02) |
| RECONCILIATION | RECREATED | Deliverable-corpus concordance from the ratified method plus app-dev and piping proto-run evidence | Activated from the integrated calibration/pause evidence; resumed proto-runs retain their pinned methods and report terminal lessons before PR #188 integration |
| PDF2MD | RETAIN / SLIM | Agent 1 source-contract manager; page work to TASK/generalist, deterministic work to tools | Manager boundary implemented; further slimming incremental |
| DRAWING_EXTRACT | RETAIN / SLIM | Agent 1 target/schema manager; sheet work to TASK/generalist, deterministic work to tools | Manager boundary implemented; further slimming incremental |
| PROJECT_SETUP (formerly ORCHESTRATOR) | RETAIN / EXPAND → **superseded by D-GOV-18 (RULED 2026-07-21): RENAME / NARROW** | Setup, coordination, control loops, scheduling gates | Implemented at instruction layer. D-GOV-18 Item 1 (RULED) renames ORCHESTRATOR → PROJECT_SETUP (`agents/AGENT_PROJECT_SETUP.md`) and narrows the charter to one-time workspace initialization + setup pipelines + estimation (Function 4 stays); control-loop Function 5 moves to HELPS_HUMANS (Item 3), Function 3 stays. Effective per D-GOV-18 ruling 2026-07-21; Item 8 PR sequence landed (verified 2026-08-02) |
| WORKING_ITEMS | EXPAND | Package-level Agent 1; manages one activated package, its deliverable work graph, Agent 2 delegation, notices, and package fan-in | Implemented and validated under D-GOV-12 |
| SOFTWARE_DEV | DEFER | First use WORKING_ITEMS plus software activation profiles, TASK skills, tools, and ephemeral generalists | Reconsider only after app-dev and piping trials demonstrate persistent manager semantics |
| REVIEW, CHANGE, RESEARCH | RETAIN / SLIM | Human decisions and formal handoffs remain manager semantics | Current contracts rebound; further slimming is evidence-driven. CHANGE: D-GOV-18 Item 4 (RULED) records the concrete first slim tranche — slim `agents/AGENT_CHANGE.md` to authority semantics (routine-closeout conditions, `APPROVE:`/`APPROVE_DESTRUCTIVE:` gates, no-silent-integration, branches-are-candidate-work, coordination handoffs), leaving method mechanics to agent judgment; `change-method` recorded as a future Reuse Candidate. REVIEW ruled SAFE, future-slim only (D-GOV-18 Item 5). Effective per D-GOV-18 ruling 2026-07-21; Item 8 PR sequence landed (verified 2026-08-02) |
| PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP | RETAIN / REBIND | Consume external decomposition standard | Implemented |
| SCOPE_CHANGE, DOMAIN_ENGINE, DBM_PUBLISHER, EQUATION_AUDIT | RETAIN / SLIM | Preserve human/domain gates; move repetition downward | Current contracts rebound; further slimming is evidence-driven |
| PREPARATION, RESEARCHER, AGGREGATION, DOMAIN_HYPERGRAPH, AUDIT_*, EVALUATION_* | RETAIN / REQUALIFIED | Approved dedicated Agent 2 roles under D-GOV-13; future TASK-skill/tool migration remains replacement-first | Persistent output/recovery schemas and live compatibility references recorded; named execution remains subject to all runtime gates |
| TASK | RETAIN | Default recurring-method Agent 2 shell | Live |

## Removal Rule

No remaining dedicated Agent 2 file is removed until its replacement, callers, compatibility behavior, validation, and tests land together. A retained dedicated package still requires an explicit D-GOV-11 qualification record and human approval.

## External Dependencies (historical)

The earlier app-dev and piping calibration/pause evidence grounds the current
RECONCILIATION contract. Their resumed proto-runs remained isolated under
pinned methods until the PR #188 integration completed; the redesign branch
was subsequently revalidated and merged. This section is retained as the
record of that ordering constraint.

## Verification Record (2026-08-02)

Owner-directed verification of every row against the live tree:

- **Removed personas absent:** no `AGENT_DECOMP_BASE.md`, `AGENT_SKILLMAKER.md`,
  `AGENT_TOOLMAKER.md`, `AGENT_CONTEXT_TRANSPOSE.md`, `AGENT_SCHEDULING.md`,
  `AGENT_ORCHESTRATOR.md`, or `AGENT_SOFTWARE_DEV.md` in `agents/`.
- **Retained roles present:** all roles in the matrix resolve to live
  `agents/AGENT_*.md` files matching the `AGENTS.md` index.
- **D-GOV-18 Item 1:** `agents/AGENT_PROJECT_SETUP.md` exists (rename
  landed); its charter delegates control-loop artifact authoring to
  HELPS_HUMANS per Item 3.
- **D-GOV-18 Item 2:** `agents/AGENT_EVALUATION.md` is a thin shell that
  loads the live `skills/evaluation-protocol` skill and retains the
  subagents allowlist, `_Evaluation/` quarantine, and fan-in validation.
- **D-GOV-18 Item 4:** `agents/AGENT_CHANGE.md` is slimmed to authority
  semantics with `APPROVE:` / `APPROVE_DESTRUCTIVE:` gates; the
  `change-method` skill correctly does not exist (future Reuse Candidate).
- **SOFTWARE_DEV deferral holds:** no persona file; `AGENTS.md` records
  software activations through WORKING_ITEMS profiles.
