# AGENT HARNESS SDK Cutover Checklist

Baseline reference:
- Branch: `main`
- Commit: `9ae2447`
- Tag target: `baseline-sdk-cutover-2026-02-07`

## Pre-Cutover
- [x] `git tag -a baseline-sdk-cutover-2026-02-07 9ae2447 -m "Pre-SDK wholesale migration baseline"`
- [x] `git push origin baseline-sdk-cutover-2026-02-07`
- [x] `git switch -c migration/agent-sdk-wholesale && git push -u origin migration/agent-sdk-wholesale`

## Runtime Files
- [x] `frontend/package.json` — remove `@anthropic-ai/sdk`, add `@anthropic-ai/claude-agent-sdk`.
- [x] `frontend/package-lock.json` — regenerate lockfile after dependency swap.
- [x] `frontend/lib/harness/agent-sdk-manager.ts` (new) — implement `startTurn/isRunning/interrupt/kill` using `query()`.
- [x] `frontend/lib/harness/agent-sdk-manager.ts` — pass SDK options: `cwd`, `resume`, `model`, `maxTurns`, `includePartialMessages`, `allowedTools`, `disallowedTools`, `systemPrompt` preset `claude_code` with `append`, `tools` preset `claude_code`, `settingSources`.
- [x] `frontend/lib/harness/agent-sdk-manager.ts` — map `permissionMode: "dontAsk"` to SDK `permissionMode: "bypassPermissions"` and set `allowDangerouslySkipPermissions: true`.
- [x] `frontend/lib/harness/agent-sdk-manager.ts` — keep logging parity (`turn:start`, `turn:model`, `session:init`, `tool:start`, `tool:result`, `turn:complete`, `process:exit`).
- [x] `frontend/lib/harness/agent-sdk-event-mapper.ts` (new) — map `SDKMessage` to existing `UIEvent` contract.
- [x] `frontend/lib/harness/index.ts` — replace `claudeCodeManager` wiring with `agentSdkManager`.
- [x] `frontend/lib/harness/types.ts` — remove CLI-only fields (`claudeExecutable`), add any SDK option types needed.
- [x] `frontend/lib/harness/defaults.ts` — add explicit SDK defaults for `settingSources` and Claude Code preset usage.
- [x] `frontend/lib/harness/persona-manager.ts` — keep `CLAUDE.md` model read; ensure value is passed into SDK options path.
- [x] `frontend/lib/harness/logger.ts` — keep as-is unless event payload schema needs minor adjustments.
- [x] `frontend/lib/harness/env-filter.ts` — remove child-process env filtering if unused; keep redaction utilities if still referenced.

## API Routes
- [x] `frontend/app/api/harness/turn/route.ts` — keep SSE contract unchanged; point execution to SDK manager.
- [x] `frontend/app/api/harness/interrupt/route.ts` — interrupt via SDK manager session abort (not process signal).
- [ ] `frontend/app/api/harness/session/create/route.ts` — no behavior change expected; verify compatibility.
- [ ] `frontend/app/api/harness/session/[id]/route.ts` — no behavior change expected; verify compatibility.
- [ ] `frontend/app/api/harness/session/list/route.ts` — no behavior change expected; verify compatibility.
- [x] `frontend/app/api/chat/route.ts` — delete (legacy path removal in wholesale migration).

## Frontend/UI
- [ ] `frontend/components/ChatPanel.tsx` — verify no contract changes required; only adjust if event shape differs.
- [ ] `frontend/components/SettingsModal.tsx` — keep model config flow; verify it still drives SDK model selection.
- [ ] `frontend/components/ResizableLayout.tsx` — update wording if it references old runtime behavior.

## Validation Scripts
- [x] `frontend/scripts/validate-harness-section8.mjs` — remove mock `claudeExecutable` flow; add SDK-native parse/interruption checks.
- [x] `frontend/scripts/validate-harness-premerge.mjs` — update to run SDK-based validation assertions.

## Docs
- [x] `frontend/README.md` — replace “spawns `claude -p`” with SDK runtime description and required settings.
- [x] `frontend/docs/harness/chirality_harness_graphs_and_sequence.md` — replace child-process/NDJSON graph with SDK `query()` flow.
- [x] `frontend/docs/harness/harness_manual_validation.md` — update test matrix for SDK path.
- [x] `frontend/docs/harness/harness_ci_integration.md` — update CI expectations and failure signatures.
- [x] `frontend/AGENT_HARNESS_DECISIONS.md` — record hard cutover decision and no-dual-path rule.
- [x] `frontend/AGENT_HARNESS_IMPLEMENTATION_CHECKLIST.md` — replace CLI tasks with SDK tasks.
- [x] `frontend/AGENT_HARNESS_SESSION_LOG.md` — append migration run log and parity results.

## Removals
- [x] `frontend/lib/harness/claude-code-manager.ts` — delete after SDK manager parity is passing.
- [x] `frontend/lib/harness/stream-parser.ts` — delete after SDK message mapper fully replaces NDJSON parsing.

## Merge Gate (must all pass)
- [x] `npm run lint`
- [x] `npx tsc --noEmit`
- [x] `npm run harness:validate:section8`
- [x] Manual parity: model from `CLAUDE.md`, tool policy behavior, interrupt reliability, SSE event order, latency/cost not worse than baseline threshold.

## Conventions
- https://platform.claude.com/docs/en/agent-sdk/typescript
- https://platform.claude.com/docs/en/agent-sdk/migration-guide
- https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts

## Task ID Index
| Task ID | Checklist Item | Primary Files |
|---|---|---|
| `PRE-001` | Create baseline tag locally | Git ref only |
| `PRE-002` | Push baseline tag to origin | Git ref only |
| `PRE-003` | Create and push migration branch | Git ref only |
| `RT-001` | Swap dependencies to Agent SDK | `frontend/package.json` |
| `RT-002` | Refresh lockfile after dependency swap | `frontend/package-lock.json` |
| `RT-003` | Implement SDK runtime manager | `frontend/lib/harness/agent-sdk-manager.ts` |
| `RT-004` | Configure `query()` parity options | `frontend/lib/harness/agent-sdk-manager.ts` |
| `RT-005` | Map permission mode parity (`dontAsk` -> `bypassPermissions`) | `frontend/lib/harness/agent-sdk-manager.ts` |
| `RT-006` | Preserve harness logging parity for SDK runtime | `frontend/lib/harness/agent-sdk-manager.ts` |
| `RT-007` | Implement SDK message to `UIEvent` mapper | `frontend/lib/harness/agent-sdk-event-mapper.ts` |
| `RT-008` | Replace runtime wiring to SDK manager | `frontend/lib/harness/index.ts` |
| `RT-009` | Update shared harness types for SDK | `frontend/lib/harness/types.ts` |
| `RT-010` | Add SDK defaults (`settingSources`, Claude Code presets) | `frontend/lib/harness/defaults.ts` |
| `RT-011` | Ensure `CLAUDE.md` model propagates into SDK turn options | `frontend/lib/harness/persona-manager.ts` |
| `RT-012` | Adjust logger payloads only if required by SDK event shape | `frontend/lib/harness/logger.ts` |
| `RT-013` | Remove/refactor child process env filtering if no longer needed | `frontend/lib/harness/env-filter.ts` |
| `API-001` | Route turn SSE through SDK manager | `frontend/app/api/harness/turn/route.ts` |
| `API-002` | Route interrupt via SDK abort | `frontend/app/api/harness/interrupt/route.ts` |
| `API-003` | Verify session create route compatibility | `frontend/app/api/harness/session/create/route.ts` |
| `API-004` | Verify session get/delete route compatibility | `frontend/app/api/harness/session/[id]/route.ts` |
| `API-005` | Verify session list route compatibility | `frontend/app/api/harness/session/list/route.ts` |
| `API-006` | Remove deprecated legacy chat route | `frontend/app/api/chat/route.ts` |
| `UI-001` | Verify chat event contract unchanged | `frontend/components/ChatPanel.tsx` |
| `UI-002` | Verify model settings flow still drives runtime model | `frontend/components/SettingsModal.tsx` |
| `UI-003` | Update runtime wording if needed | `frontend/components/ResizableLayout.tsx` |
| `VAL-001` | Update section-8 validation script for SDK runtime | `frontend/scripts/validate-harness-section8.mjs` |
| `VAL-002` | Update premerge validation script for SDK runtime | `frontend/scripts/validate-harness-premerge.mjs` |
| `DOC-001` | Update frontend README runtime description | `frontend/README.md` |
| `DOC-002` | Update architecture/sequence diagrams | `frontend/docs/harness/chirality_harness_graphs_and_sequence.md` |
| `DOC-003` | Update manual validation runbook | `frontend/docs/harness/harness_manual_validation.md` |
| `DOC-004` | Update CI integration runbook | `frontend/docs/harness/harness_ci_integration.md` |
| `DOC-005` | Record cutover decision | `frontend/AGENT_HARNESS_DECISIONS.md` |
| `DOC-006` | Replace implementation checklist entries | `frontend/AGENT_HARNESS_IMPLEMENTATION_CHECKLIST.md` |
| `DOC-007` | Append migration execution log | `frontend/AGENT_HARNESS_SESSION_LOG.md` |
| `RM-001` | Delete old CLI runtime manager | `frontend/lib/harness/claude-code-manager.ts` |
| `RM-002` | Delete NDJSON parser runtime dependency | `frontend/lib/harness/stream-parser.ts` |
| `GATE-001` | Lint passes | `npm run lint` |
| `GATE-002` | Typecheck passes | `npx tsc --noEmit` |
| `GATE-003` | Harness validation passes | `npm run harness:validate:section8` |
| `GATE-004` | Manual parity checks pass | Manual run |

## Phase-Based Commit Batches
| Phase | Commit Batch | Task IDs | Notes |
|---|---|---|---|
| `P0` | `P0-C1` Baseline safety refs | `PRE-001`, `PRE-002`, `PRE-003` | No file edits; creates rollback anchors before migration work starts. |
| `P1` | `P1-C1` SDK dependency and contracts | `RT-001`, `RT-002`, `RT-009`, `RT-010` | Establishes compile-time contract and defaults first. |
| `P1` | `P1-C2` SDK engine scaffolding | `RT-003`, `RT-007` | Adds new runtime manager and event mapper without cutting over yet. |
| `P2` | `P2-C1` Runtime cutover | `RT-004`, `RT-005`, `RT-008`, `RT-011`, `API-001`, `API-002` | Switches turn/interrupt execution to SDK with parity options. |
| `P2` | `P2-C2` Observability and env cleanup | `RT-006`, `RT-012`, `RT-013` | Finalizes logging parity and removes process-specific leftovers. |
| `P3` | `P3-C1` Legacy path removal | `API-006`, `RM-001`, `RM-002` | Deletes old CLI/NDJSON runtime after SDK path is proven green. |
| `P4` | `P4-C1` Validation scripts update | `VAL-001`, `VAL-002` | Aligns automation with SDK runtime behavior. |
| `P4` | `P4-C2` Documentation update | `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-005`, `DOC-006`, `DOC-007` | Brings runbooks/spec logs in sync with cutover implementation. |
| `P5` | `P5-C1` Merge gate run | `GATE-001`, `GATE-002`, `GATE-003`, `GATE-004` | Final acceptance checkpoint before PR merge. |
