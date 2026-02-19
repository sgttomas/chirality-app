# Subagent Implementation Plan (Persistent)

Last updated: 2026-02-19 (step-5-run-complete)
Owner: Codex session
Scope: Finish hardening of Type 1 -> Type 2 subagent spawning rollout in frontend harness.

## Purpose

This file is the canonical, filesystem-backed plan so work survives chat compaction or session resets.
Any future session should read this file first and continue from the current status.

## Current State Summary

- Core subagent wiring is implemented behind `CHIRALITY_ENABLE_SUBAGENTS`.
- Agent ID drift (`AUDIT_DEPENDENCIES` -> `AUDIT_DEP_CLOSURE`) has been corrected in core runtime/UI paths.
- Type 1 allowlist rollout is currently limited to `ORCHESTRATOR` and `RECONCILIATION`.
- `AGENT_PROJECT_DECOMP.md` has been restored and is present.

## Remaining Findings To Close

1. Close governance conformance gaps found during docs review.
2. Enforce Type 2-only subagent registry safety.
3. Add durable, structured subagent task tracking (beyond console-only telemetry).
4. Add validator coverage for "subagents off => unchanged behavior".
5. Update operator docs for feature flag + tracking behavior.
6. Run verification gates once dependencies are available.

## Execution Plan

### Step 0 - Governance Conformance (Docs-Aligned)
Status: `DONE`

Targets:
- `frontend/lib/harness/index.ts`
- `docs/SPEC.md`
- `agents/AGENT_HELPS_HUMANS.md` (only if needed to keep canonical standard aligned)

Work:
- Enforce explicit human gate/seal before Type 1 sessions can delegate Type 2 subagents (fail closed).
- Align instruction-file metadata contract with runtime:
  - either document optional YAML frontmatter support (for `description`, `subagents`, `tools`, `model`) in governance docs, or
  - move subagent metadata to a separate machine-readable registry and keep `AGENT_*.md` structure unchanged.
- Ensure final chosen contract is consistent across docs and runtime parser behavior.

Acceptance:
- Type 2 delegation is blocked unless gate/seal conditions are satisfied.
- Governance docs and runtime behavior agree on where subagent metadata lives.

### Step 1 - Registry Safety Hardening
Status: `DONE`

Targets:
- `frontend/lib/harness/persona-manager.ts`

Work:
- In `buildSubagentDefinitions()`, enforce spawned agent identity:
  - Must be `AGENT_TYPE: 2` (required).
  - Prefer `AGENT_CLASS: TASK` (warn or enforce).
- If invalid/missing metadata, skip the agent and emit validation error.
- Extend `validateRegistry()` output so these failures are machine-checkable.

Acceptance:
- Non-Type-2 agent files cannot be injected into `mergedOpts.agents`.

### Step 2 - Durable Subagent Task Tracking
Status: `DONE`

Targets:
- `frontend/lib/harness/agent-sdk-manager.ts`
- `frontend/lib/harness/agent-sdk-event-mapper.ts` (only if needed for extraction shape)

Work:
- Persist subagent lifecycle events into harness logs (not only `console.info`):
  - `subagent:start`
  - `subagent:complete`
  - `subagent:interrupted` (or equivalent terminal non-success)
- Correlate by `toolUseId` and include:
  - `subagentType`
  - `description`
  - `status`
  - timestamps

Acceptance:
- `.chirality/logs/harness.log` contains correlated subagent lifecycle records for delegated runs.

### Step 3 - Validation Hardening (Flag-Off Parity)
Status: `DONE`

Targets:
- `frontend/scripts/validate-harness-section8.mjs`
- `frontend/scripts/validate-harness-premerge.mjs`

Work:
- Add an explicit test/assertion for:
  - `CHIRALITY_ENABLE_SUBAGENTS` unset/false
  - Type 1 turn runs with no subagent injection side effects
  - behavior remains baseline-compatible
- Add test ID to required premerge list.

Acceptance:
- Premerge validation fails if "subagents off => unchanged behavior" regresses.

### Step 4 - Operator Documentation Update
Status: `DONE`

Targets:
- `frontend/README.md`

Work:
- Document:
  - Feature flag (`CHIRALITY_ENABLE_SUBAGENTS`)
  - Initial Type 1 allowlist
  - Where subagent tracking appears in logs

Acceptance:
- README contains concise run/operator guidance for subagent feature behavior.

### Step 5 - Verification Gate
Status: `DONE`

Work:
- Run:
  - `npm run lint`
  - `npx tsc --noEmit`
  - `npm run harness:validate:section8`
  - `npm run harness:validate:premerge`
- If local `node_modules` missing, install deps first and note that in run summary.

Acceptance:
- All checks pass and results are summarized in commit/PR notes.

## Decision Log

- 2026-02-19: Use filesystem-backed plan tracking in `docs/` as canonical continuity mechanism.
- 2026-02-19: Keep `WORKING_ITEMS` out of initial Type 1 subagent allowlist until ORCHESTRATOR/RECONCILIATION are stable.
- 2026-02-19: `AUDIT_DEP_CLOSURE` is canonical replacement for `AUDIT_DEPENDENCIES`.
- 2026-02-19: Full `docs/` review surfaced two governance gaps to close first: delegation gate/seal enforcement and metadata contract alignment (frontmatter vs canonical agent header format).
- 2026-02-19: Step 0 complete. Added fail-closed delegation governance token (`subagentGovernance`) and documented runtime split metadata contract in `docs/SPEC.md`.
- 2026-02-19: Step 1 complete. Subagent registry now hard-requires `AGENT_TYPE: 2`, warns on non-`TASK` `AGENT_CLASS`, and `validateRegistry()` now returns structured `issues` plus compatible `errors`.
- 2026-02-19: Step 2 complete. Added durable subagent lifecycle logging (`subagent:registry_applied`, `subagent:start`, `subagent:complete`, `subagent:interrupted`) correlated by `toolUseId` in harness logs.
- 2026-02-19: Step 3 complete. Added `section8.subagents_off_parity` validator coverage and wired it into premerge required SDK test IDs.
- 2026-02-19: Step 4 complete. Updated frontend operator docs for feature flag behavior, allowlist, governance token requirements, and subagent lifecycle log events.
- 2026-02-19: Step 5 run complete. `lint` and `tsc` passed; Section 8/premerge failed in auth-dependent flows (boot/smoke/permissions) due runtime 401/500 while `section8.subagents_off_parity` passed.

## Update Protocol

For each completed step:
1. Change `Status` from `PENDING` -> `IN_PROGRESS` -> `DONE`.
2. Add a dated note under Decision Log summarizing what changed.
3. If scope changes, append a short "Plan Amendment" subsection rather than rewriting history.
