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

- [ ] `frontend/lib/harness/persona-manager.ts`
  - [ ] `load(projectRoot, personaId): Promise<PersonaConfig | null>`.
  - [ ] `list(projectRoot): Promise<PersonaConfig[]>`.
  - [ ] `buildSystemPrompt(projectRoot, persona, mode): Promise<string>`.
  - [ ] `writeSystemPromptFile(projectRoot, sessionId, prompt): Promise<string>` (atomic write).
  - [ ] Parse YAML frontmatter fields:
    - [ ] `tools` -> `--tools`
    - [ ] `disallowed_tools` -> `--disallowedTools`
    - [ ] `auto_approve_tools` -> `--allowedTools`
    - [ ] `max_turns` override
  - [ ] mtime cache for `README.md`, `AGENTS.md`, persona file.
  - [ ] 16k token budget enforcement (~4 chars/token): truncate persona first, then project context.

## 3) Session persistence module

### New file

- [ ] `frontend/lib/harness/session-manager.ts`
  - [ ] `create(projectRoot, persona, mode): Promise<Session>`.
  - [ ] `resume(sessionId): Promise<Session>`.
  - [ ] `save(session): Promise<void>` (atomic write temp + rename).
  - [ ] `list(projectRoot?): Promise<SessionSummary[]>` (sort by `updatedAt` desc).
  - [ ] `get(sessionId): Promise<Session>`.
  - [ ] `delete(sessionId): Promise<void>`.
  - [ ] Persist under `{projectRoot}/.chirality/sessions/{id}.json`.
  - [ ] Store/update `claudeSessionId` from `session:init`.

## 4) Server orchestrator wiring

### New file

- [ ] `frontend/lib/harness/index.ts`
  - [ ] Export singleton instances: `sessionManager`, `personaManager`, `claudeCodeManager`.
  - [ ] Implement `startHarnessTurn({ sessionId, message, opts })` as async generator yielding `UIEvent`.
  - [ ] Add resume fallback behavior:
    - [ ] If resume fails, emit `session:error`, retry once without `--resume`, capture new `session:init`.
  - [ ] Persist session updates on `session:init`, `session:complete`, and terminal exit.

## 5) API routes (`/api/harness/*`)

### New files

- [x] `frontend/app/api/harness/turn/route.ts`
  - [x] `POST` request body: `{ sessionId, message, opts? }`.
  - [x] Return `text/event-stream` and stream `UIEvent`s as SSE.
  - [x] Enforce 409 if `claudeCodeManager.isRunning(sessionId)`.
- [x] `frontend/app/api/harness/interrupt/route.ts`
  - [x] `POST` request body: `{ sessionId }`.
  - [x] Call `claudeCodeManager.interrupt(sessionId)`.
- [ ] `frontend/app/api/harness/session/create/route.ts`
  - [ ] `POST` body: `{ projectRoot, persona, mode }`.
  - [ ] Return `201 { session }`.
- [ ] `frontend/app/api/harness/session/list/route.ts`
  - [ ] `GET` query: `projectRoot?`.
- [ ] `frontend/app/api/harness/session/[id]/route.ts`
  - [ ] `GET` -> `{ session }`.
  - [ ] `DELETE` -> `204`.

## 6) Frontend chat integration

### Existing file updates

- [ ] `frontend/components/ChatPanel.tsx`
  - [ ] Replace `/api/chat` request path with harness flow:
    - [ ] On init: create/load harness session via `/api/harness/session/*`.
    - [ ] On send: open SSE `POST /api/harness/turn`.
  - [ ] Add SSE event handlers for all `UIEvent` types:
    - [ ] `chat:delta` append assistant text incrementally.
    - [ ] `chat:complete` finalize assistant message.
    - [ ] `tool:start`, `tool:result` add terminal-style entries.
    - [ ] `session:init` store model + `claudeSessionId` in local UI state.
    - [ ] `session:complete` update metadata.
    - [ ] `session:error` display error message/toast entry.
    - [ ] `process:exit` clear loading state and re-enable input.
  - [ ] Add `interrupt` button/state -> call `POST /api/harness/interrupt`.
  - [ ] Keep per-view local chat history UX, but server is source of session metadata.
  - [ ] Remove direct dependency on user-provided Anthropic key in UI for harness turns.
- [ ] `frontend/components/ResizableLayout.tsx`
  - [ ] Pass mode/persona metadata needed for harness session creation.
- [ ] `frontend/components/WorkbenchView.tsx`
  - [ ] Map `agentName` to harness persona id.
  - [ ] Keep autoPrompt behavior as user message (first turn).
- [ ] `frontend/components/PipelineView.tsx`
  - [ ] Map `selectedVariant` to persona id for session create.
- [ ] `frontend/components/DirectLinkView.tsx`
  - [ ] Ensure mode is sent as `"direct"` for session create.

## 7) Transition strategy from current `/api/chat`

### Existing file updates

- [ ] `frontend/app/api/chat/route.ts`
  - [ ] Mark deprecated in header comment.
  - [ ] Do not remove until harness flow is stable and UI switched.
- [ ] `frontend/README.md`
  - [ ] Document harness env requirements (`ANTHROPIC_API_KEY`, Claude CLI installed).
  - [ ] Document new API routes and troubleshooting steps.

## 8) Validation checklist (must pass)

- [x] Smoke: send prompt, receive streaming `chat:delta`, then `chat:complete`, then `process:exit`.
- [x] Session init: verify `session:init` captures emitted `session_id` and persists `claudeSessionId`.
- [x] Resume: turn 2 uses `--resume {claudeSessionId}` and maintains continuity.
- [ ] Permissions: default `dontAsk` denies unapproved tools without hang; approved tools proceed.
- [x] Persona injection: prompt file exists at `.chirality/prompts/{sessionId}-system.txt`.
- [x] Interrupt/kill: long turn interrupted and exits cleanly with `process:exit`.
- [ ] Parse robustness: malformed NDJSON lines are logged + skipped (no crash).
- [x] Secret safety: logs show redaction and filtered env behavior.

## 9) Assignment slices (parallelizable)

- [x] **Assignment A — Harness Core**
  - [x] `frontend/lib/harness/{types,defaults,env-filter,logger,stream-parser,claude-code-manager}.ts`
- [ ] **Assignment B — Persona + Session + Orchestrator**
  - [ ] `frontend/lib/harness/{persona-manager,session-manager,index}.ts`
- [ ] **Assignment C — API + UI Integration**
  - [ ] `frontend/app/api/harness/**`
  - [ ] `frontend/components/{ChatPanel,ResizableLayout,WorkbenchView,PipelineView,DirectLinkView}.tsx`
- [ ] **Assignment D — Verification + Docs**
  - [ ] `frontend/README.md`
  - [ ] Manual verification log covering section 8.
