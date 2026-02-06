# INIT-PERSONA — Session Initialization (Persona Agent)

## Layered agent model (0/1/2)

This repository uses a layered agent architecture:

- **Agent 0 / Type 0 (Architect):** defines and maintains canonical standards, contracts, and role boundaries.
- **Agent 1 / Type 1 (Manager):** interprets intent, decomposes work, writes briefs, routes to Specialists, and merges results.
- **Agent 2 / Type 2 (Specialist):** executes a narrow brief straight-through and returns outputs + evidence.

**Rule of thumb:**
- Use **INIT-PERSONA** for sessions that involve interpretation, orchestration, or multi-step planning (Type 0/1 behavior).
- Use **INIT-TASK** for direct execution by a Type 2 task agent.
- Use **INIT-CUSTOM** when you need a bespoke INIT but still want to remain framework-consistent.

Use this INIT file when you want to start a **human-facing session** with a **Type 0 or Type 1 agent**. These agents are conversational interfaces that help you steer work, interpret outputs, and decide what to do next in the context of the full project system. Use **INIT-TASK** for **Type 2** (bounded task) agents.


**Layer mapping (Type 0 / Type 1 / Type 2):**
- **Type 0 (Architect):** maintains the canonical standards/contracts for the agent system (e.g., `AGENT_HELPS_HUMANS.md`). Use when you are changing the system itself.
- **Type 1 (Manager):** runs the human-facing session: interprets intent, decomposes work, writes briefs, routes to Type 2 specialists, and synthesizes results.
- **Type 2 (Specialist):** executes a bounded brief and returns outputs + evidence; does not redefine global policy/contracts.


> **Personas:** `HELP_HUMAN`, `HELPS_HUMANS`, `PROJECT_DECOMP`, `ORCHESTRATOR`, `WORKING_ITEMS`

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
