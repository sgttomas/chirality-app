# Chirality Harness v0.5 — Frontend Implementation Checklist

Source of truth: `AGENT_HARNESS_SPEC-v2-3.md`  
Supporting runtime/sequence maps: `frontend/docs/harness/chirality_harness_graphs_and_sequence.md`

## 0) Non-negotiable constraints

- [x] Use Claude Code CLI subprocess (`claude -p`) as execution engine.
- [x] Use NDJSON only: `--output-format stream-json --include-partial-messages --verbose`.
- [x] Use `--append-system-prompt-file` (not `--system-prompt`).
- [x] Treat `system/init.session_id` as authoritative `claudeSessionId`.
- [x] Enforce one in-flight turn per session (409 on conflict).
- [x] Apply env filtering (denylist first, then explicit whitelist).
- [x] Never log secrets; redact sensitive values in logs.

## 1) Harness core module scaffolding

### New files

- [x] `frontend/lib/harness/types.ts`
  - [x] Define `Session`, `SessionSummary`, `TurnOpts`, `UsageInfo`, `UIEvent`, `PersonaConfig`, `LogEntry`.
- [x] `frontend/lib/harness/defaults.ts`
  - [x] Add constants: `DEFAULT_MAX_TURNS`, `DEFAULT_PERMISSION_MODE`, `PROMPT_TOKEN_BUDGET`, log limits.
- [x] `frontend/lib/harness/env-filter.ts`
  - [x] Implement `filterChildEnv(env: NodeJS.ProcessEnv): NodeJS.ProcessEnv`.
  - [x] Implement `redactForLogs(value: string): string`.
- [x] `frontend/lib/harness/logger.ts`
  - [x] Implement `appendLog(projectRoot: string, entry: LogEntry): Promise<void>`.
  - [x] Implement log rotation `rotateIfNeeded(projectRoot: string): Promise<void>` (10MB -> `.1`).
- [x] `frontend/lib/harness/stream-parser.ts`
  - [x] Implement `parseNdjsonLine(line: string): unknown | null` (skip blank, warn on parse error, no throw).
  - [x] Implement `mapClaudeEventToUiEvents(...)` for all mapped events.
  - [x] Implement `extractToolUseFromAssistantMessage(...)`.
  - [x] Implement `extractToolResultFromUserMessage(...)`.
- [x] `frontend/lib/harness/claude-code-manager.ts`
  - [x] Implement class `ClaudeCodeManager` with `startTurn`, `interrupt`, `kill`, `isRunning`.
  - [x] Keep `activeRuns: Map<string, ChildProcess>`.
  - [x] Spawn `claude` with spec flags and optional `--resume`.
  - [x] Emit final `process:exit`; emit `session:error` before exit if no `result` was seen.
  - [x] Capture stderr lines into logger at warn level.

## 2) Persona/context module

### New file

- [x] `frontend/lib/harness/persona-manager.ts`
  - [x] `load(projectRoot, personaId): Promise<PersonaConfig | null>`.
  - [x] `list(projectRoot): Promise<PersonaConfig[]>`.
  - [x] `buildSystemPrompt(projectRoot, persona, mode): Promise<string>`.
  - [x] `writeSystemPromptFile(projectRoot, sessionId, prompt): Promise<string>` (atomic write).
  - [x] Parse YAML frontmatter fields:
    - [x] `tools` -> `--tools`
    - [x] `disallowed_tools` -> `--disallowedTools`
    - [x] `auto_approve_tools` -> `--allowedTools`
    - [x] `max_turns` override
  - [x] mtime cache for `README.md`, `AGENTS.md`, persona file.
  - [x] 16k token budget enforcement (~4 chars/token): truncate persona first, then project context.

## 3) Session persistence module

### New file

- [x] `frontend/lib/harness/session-manager.ts`
  - [x] `create(projectRoot, persona, mode): Promise<Session>`.
  - [x] `resume(sessionId): Promise<Session>`.
  - [x] `save(session): Promise<void>` (atomic write temp + rename).
  - [x] `list(projectRoot?): Promise<SessionSummary[]>` (sort by `updatedAt` desc).
  - [x] `get(sessionId): Promise<Session>`.
  - [x] `delete(sessionId): Promise<void>`.
  - [x] Persist under `{projectRoot}/.chirality/sessions/{id}.json`.
  - [x] Store/update `claudeSessionId` from `session:init`.

## 4) Server orchestrator wiring

### New file

- [x] `frontend/lib/harness/index.ts`
  - [x] Export singleton instances: `sessionManager`, `personaManager`, `claudeCodeManager`.
  - [x] Implement `startHarnessTurn({ sessionId, message, opts })` as async generator yielding `UIEvent`.
  - [x] Add resume fallback behavior:
    - [x] If resume fails, emit `session:error`, retry once without `--resume`, capture new `session:init`.
  - [x] Persist session updates on `session:init`, `session:complete`, and terminal exit.

## 5) API routes (`/api/harness/*`)

### New files

- [x] `frontend/app/api/harness/turn/route.ts`
  - [x] `POST` request body: `{ sessionId, message, opts? }`.
  - [x] Return `text/event-stream` and stream `UIEvent`s as SSE.
  - [x] Enforce 409 if `claudeCodeManager.isRunning(sessionId)`.
- [x] `frontend/app/api/harness/interrupt/route.ts`
  - [x] `POST` request body: `{ sessionId }`.
  - [x] Call `claudeCodeManager.interrupt(sessionId)`.
- [x] `frontend/app/api/harness/session/create/route.ts`
  - [x] `POST` body: `{ projectRoot, persona, mode }`.
  - [x] Return `201 { session }`.
- [x] `frontend/app/api/harness/session/list/route.ts`
  - [x] `GET` query: `projectRoot?`.
- [x] `frontend/app/api/harness/session/[id]/route.ts`
  - [x] `GET` -> `{ session }`.
  - [x] `DELETE` -> `204`.

## 6) Frontend chat integration

### Existing file updates

- [x] `frontend/components/ChatPanel.tsx`
  - [x] Replace `/api/chat` request path with harness flow:
    - [x] On init: create/load harness session via `/api/harness/session/*`.
    - [x] On send: open SSE `POST /api/harness/turn`.
  - [x] Add SSE event handlers for all `UIEvent` types:
    - [x] `chat:delta` append assistant text incrementally.
    - [x] `chat:complete` finalize assistant message.
    - [x] `tool:start`, `tool:result` add terminal-style entries.
    - [x] `session:init` store model + `claudeSessionId` in local UI state.
    - [x] `session:complete` update metadata.
    - [x] `session:error` display error message/toast entry.
    - [x] `process:exit` clear loading state and re-enable input.
  - [x] Add `interrupt` button/state -> call `POST /api/harness/interrupt`.
  - [x] Keep per-view local chat history UX, but server is source of session metadata.
  - [x] Remove direct dependency on user-provided Anthropic key in UI for harness turns.
- [x] `frontend/components/ResizableLayout.tsx`
  - [x] Pass mode/persona metadata needed for harness session creation.
- [x] `frontend/components/WorkbenchView.tsx`
  - [x] Map `agentName` to harness persona id.
  - [x] Keep autoPrompt behavior as user message (first turn).
- [x] `frontend/components/PipelineView.tsx`
  - [x] Map `selectedVariant` to persona id for session create.
- [x] `frontend/components/DirectLinkView.tsx`
  - [x] Ensure mode is sent as `"direct"` for session create.

## 7) Transition strategy from current `/api/chat`

### Existing file updates

- [x] `frontend/app/api/chat/route.ts`
  - [x] Mark deprecated in header comment.
  - [x] Do not remove until harness flow is stable and UI switched.
- [x] `frontend/README.md`
  - [x] Document harness env requirements (`ANTHROPIC_API_KEY`, Claude CLI installed).
  - [x] Document new API routes and troubleshooting steps.

## 8) Validation checklist (must pass)

- [x] Smoke: send prompt, receive streaming `chat:delta`, then `chat:complete`, then `process:exit`.
- [x] Session init: verify `session:init` captures emitted `session_id` and persists `claudeSessionId`.
- [x] Resume: turn 2 uses `--resume {claudeSessionId}` and maintains continuity.
- [x] Permissions: default `dontAsk` denies unapproved tools without hang; approved tools proceed.
- [x] Persona injection: prompt file exists at `.chirality/prompts/{sessionId}-system.txt`.
- [x] Interrupt/kill: long turn interrupted and exits cleanly with `process:exit`.
- [x] Parse robustness: malformed NDJSON lines are logged + skipped (no crash).
- [x] Secret safety: logs show redaction and filtered env behavior.
- [x] Repeatable pre-merge automation exists under `frontend/scripts/validate-harness-section8.mjs` with machine-readable summary + deterministic artifacts.
- [x] CI/pre-merge wrapper target publishes `summary.json` to stable `frontend/artifacts/harness/section8/latest/summary.json` and prints artifact path in stdout.
- [x] Root `.gitignore` ignores runtime churn in `.chirality/logs/`, `.chirality/prompts/`, and `.chirality/sessions/` without ignoring the full `.chirality/` tree.
- [x] CI wiring runs `cd frontend && npm run harness:validate:premerge`, verifies `frontend/artifacts/harness/section8/latest/summary.json`, and uploads that summary as build artifact.
- [x] Runbook docs explicitly cover `HARNESS_BASE_URL` reachability, Claude CLI + `ANTHROPIC_API_KEY` prerequisites, canonical local run sequence, and common failure remediation.

## 9) Assignment slices (parallelizable)

- [x] **Assignment A — Harness Core**
  - [x] `frontend/lib/harness/{types,defaults,env-filter,logger,stream-parser,claude-code-manager}.ts`
- [x] **Assignment B — Persona + Session + Orchestrator**
  - [x] `frontend/lib/harness/{persona-manager,session-manager,index}.ts`
- [x] **Assignment C — API + UI Integration**
  - [x] `frontend/app/api/harness/**`
  - [x] `frontend/components/{ChatPanel,ResizableLayout,WorkbenchView,PipelineView,DirectLinkView}.tsx`
- [x] **Assignment D — Verification + Docs**
  - [x] `frontend/README.md`
  - [x] Manual verification log covering section 8.
  - [x] Automated Section 8 validation script + usage docs.
  - [x] Pre-merge wrapper target + stable artifact publishing docs.
