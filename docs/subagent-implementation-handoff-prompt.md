# Handoff Prompt For Next Codex Instance

Use this prompt verbatim in a new Codex session:

---

Continue implementation in:
`/Users/ryan/ai-env/projects/chirality-app`

Source of truth plan:
`/Users/ryan/ai-env/projects/chirality-app/docs/subagent-implementation-plan.md`

Read the plan file first and execute the remaining steps in order, updating step statuses in that file as you go.

Constraints:
1. Preserve existing SSE/UI contract for phase-1 behavior.
2. Keep subagent feature behind `CHIRALITY_ENABLE_SUBAGENTS`.
3. Keep initial Type 1 subagent allowlist limited to ORCHESTRATOR and RECONCILIATION.
4. Enforce governance alignment: delegation must honor gate/seal requirements from `docs/CONTRACT.md`.
5. Do not revert unrelated user changes.
6. After each major step, update the plan's Decision Log with date + concise summary.

Immediate execution order:
1. Step 0 - Governance Conformance (seal/gate enforcement + metadata contract alignment).
2. Step 1 - Registry Safety Hardening (`AGENT_TYPE: 2` enforcement in subagent registry).
3. Step 2 - Durable subagent lifecycle logging in harness logs.
4. Step 3 - Add validator assertion for "subagents off => unchanged behavior".
5. Step 4 - Update frontend README operator guidance.
6. Step 5 - Run verification gates and report outcomes.

Before final response:
1. Provide a concise status report by step (DONE/IN_PROGRESS/PENDING).
2. Include file-level change summary.
3. Call out any blockers (missing dependencies, failing tests, unclear semantics).

---

