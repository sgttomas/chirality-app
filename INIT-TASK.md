# INIT-TASK — Session Initialization (Task Agent)

## Layered agent model (0/1/2)

This repository uses a layered agent architecture:

- **Agent 0 / Type 0 (Architect):** defines and maintains canonical standards, contracts, and role boundaries.
- **Agent 1 / Type 1 (Manager):** interprets intent, decomposes work, writes briefs, routes to Specialists, and merges results.
- **Agent 2 / Type 2 (Specialist):** executes a narrow brief straight-through and returns outputs + evidence.

**Rule of thumb:**
- Use **INIT-PERSONA** for sessions that involve interpretation, orchestration, or multi-step planning (Type 0/1 behavior).
- Use **INIT-TASK** for direct execution by a Type 2 task agent.
- Use **INIT-CUSTOM** when you need a bespoke INIT but still want to remain framework-consistent.

Use this INIT file when you want to run a **Type 2 task agent directly**. Task agents should execute a bounded assignment straight-through, producing durable, auditable outputs (typically into a tool root) without requiring mid-run human decisions. Use **INIT-PERSONA** for **Type 0 / Type 1** agents.

> **Task Agents:** `4_DOCUMENTS`, `AGGREGATION`, `CHIRALITY_FRAMEWORK`, `CHIRALITY_LENS`, `DEPENDENCIES`, `ESTIMATING`, `PREPARATION`, `RECONCILIATION`, `TASK_SETUP`.

---

## Project Context

**Project Name:** 
**Project Workspace (absolute):** `/Users/ryan/ai-env/projects/chirality-app-test/test/`  
**Execution Root (absolute):** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-7/`  
**Decomposition File (absolute):** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-7/_Decomposition/`
**Key Reference Documents (paths):** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-7/_Sources/`

Only read Decomposition File and References Documents if prompted by the user, or when required to later by your persona agent instructions.

---

EOF
