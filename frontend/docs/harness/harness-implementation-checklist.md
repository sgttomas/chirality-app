# Chirality Harness Implementation Checklist (SDK Runtime)

Source of truth for migration execution: `frontend/AGENT_HARNESS_SDK_CUTOVER_CHECKLIST.md`

This file captures the post-cutover implementation baseline and intentionally reflects SDK-only runtime behavior.

## 0) Non-negotiable constraints

- [x] Runtime uses Anthropic Agent SDK `query()` (no CLI subprocess manager path).
- [x] SSE `UIEvent` contract remains stable for `ChatPanel`.
- [x] Persona + system append prompting remains in runtime flow.
- [x] `dontAsk` permission mode maps to SDK `bypassPermissions` with explicit danger flag.
- [x] No legacy `/api/chat` route.

## 1) Harness runtime modules

- [x] `frontend/lib/harness/types.ts` updated for SDK turn options.
- [x] `frontend/lib/harness/defaults.ts` defines explicit SDK defaults (`settingSources`, `claude_code` presets).
- [x] `frontend/lib/harness/agent-sdk-event-mapper.ts` maps `SDKMessage -> UIEvent`.
- [x] `frontend/lib/harness/agent-sdk-manager.ts` implements `startTurn/isRunning/interrupt/kill` over `query()`.
- [x] `frontend/lib/harness/index.ts` wires `agentSdkManager` as the runtime singleton.
- [x] `frontend/lib/harness/session-manager.ts` persists sessions and `claudeSessionId`.
- [x] `frontend/lib/harness/persona-manager.ts` continues `CLAUDE.md` model propagation into runtime opts.
- [x] `frontend/lib/harness/logger.ts` emits parity operational events for SDK runs.
- [x] `frontend/lib/harness/env-filter.ts` retains redaction helpers; child-process env filtering removed from active runtime path.

## 2) API routes

- [x] `POST /api/harness/turn` streams SDK-backed SSE events.
- [x] `POST /api/harness/interrupt` interrupts SDK query sessions.
- [x] `POST /api/harness/session/create` compatible.
- [x] `GET /api/harness/session/list` compatible.
- [x] `GET /api/harness/session/:id` compatible.
- [x] `DELETE /api/harness/session/:id` compatible with in-flight protection.

## 3) Legacy removals

- [x] `frontend/app/api/chat/route.ts` removed.
- [x] `frontend/lib/harness/claude-code-manager.ts` removed.
- [x] `frontend/lib/harness/stream-parser.ts` removed.

## 4) Validation + premerge

- [x] `frontend/scripts/validate-harness-section8.mjs` is SDK-native (no mocked `claudeExecutable` path, no `/api/chat` regression test).
- [x] `frontend/scripts/validate-harness-premerge.mjs` validates SDK summary schema/test IDs and publishes stable artifact.
- [x] Stable artifact path remains `frontend/artifacts/harness/section8/latest/summary.json`.

## 5) Documentation alignment

- [x] `frontend/README.md` updated for SDK runtime guidance.
- [x] `frontend/docs/harness/chirality_harness_graphs_and_sequence.md` updated to SDK architecture.
- [x] `frontend/docs/harness/harness_manual_validation.md` updated to SDK validation matrix.
- [x] `frontend/docs/harness/harness_ci_integration.md` updated to SDK CI assertions.
- [x] `frontend/AGENT_HARNESS_DECISIONS.md` includes hard-cutover/no-dual-path decision.
