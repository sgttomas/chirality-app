# Chirality Agent Harness — Contract, Specification & Implementation Plan

**Version:** 2.3  
**Status:** Ready for Implementation  
**Date:** 2026-02-07  
**Context:** This document supersedes v1.1. The core architectural decision has changed: instead of building a custom agentic harness (PTY management, Anthropic streaming driver, tool dispatch, sentinel envelope), Chirality wraps **Claude Code as a child process**. Claude Code provides the stateful shell, tool execution, permission system, and agentic loop. Chirality provides the GUI, persona management, session lifecycle, and event routing.

---

## Part 1: Contract

---

### 1.1 Architectural Decision Record

**Decision:** Use Claude Code CLI as the agent execution engine, spawned as a child process per turn.

**Rationale:**
- Claude Code already provides stateful shell integration (persistent CWD, env across turns), tool execution (`Bash`, `Read`, `Write`, `Edit`, `Grep`, `Glob`, `TodoWrite`, and others), built-in permission management (`--permission-mode`, tool availability via `--tools`, explicit deny via `--disallowedTools`, and auto-approval via `--allowedTools`), the Anthropic streaming protocol, tool-call JSON assembly, retry logic, and loop guards (`--max-turns`).
- The developer already uses Claude Code daily via the terminal and the OAuth subscription platform. This is the same runtime, accessed via subprocess.
- Building a custom PTY manager, sentinel envelope, stream scanner, Anthropic driver, and tool dispatcher would replicate ~10+ days of engineering that Claude Code already ships.
- Claude Code exposes `--output-format stream-json` which emits NDJSON events suitable for real-time GUI consumption, and `--resume SESSION_ID` for multi-turn session continuations.

**What Chirality owns:** GUI, persona system, session lifecycle, event routing, context injection, observability.  
**What Claude Code owns:** Shell execution, tool dispatch, LLM communication, permission enforcement, agentic loop.

**Future provision:** A Claude Agent SDK exists for both Python (`claude-agent-sdk`) and TypeScript (`@anthropic-ai/claude-agent-sdk`) that provides programmatic access with callbacks, hooks, and native message objects. If the child process approach hits limitations (e.g., permission prompt interception, fine-grained hook control), migrating to the SDK is a natural next step that preserves the same architecture. Adding a non-Anthropic model driver is a separate future milestone, not a current requirement.

---

### 1.2 Module Boundaries

The harness consists of four modules. Each module owns one concern.

```
┌─────────────────────────────────────────────────────┐
│                   Chirality GUI                      │
│          (Next.js — already built)                   │
└──────────────┬──────────────────────────┬────────────┘
               │ UIEvents (SSE)           │ REST API
               ▼                          ▼
┌──────────────────────┐   ┌──────────────────────────┐
│   ClaudeCodeManager  │   │     SessionManager       │
│  (process lifecycle  │   │  (persist/resume/list)   │
│   + stream parsing)  │   │                          │
└──────────┬───────────┘   └──────────────────────────┘
           │
           ▼
┌──────────────────────┐
│   PersonaManager     │
│  (context injection  │
│   + tool scoping)    │
└──────────────────────┘
```

**Dependency rule:** The GUI depends on ClaudeCodeManager and SessionManager. ClaudeCodeManager depends on PersonaManager (to build context before spawning). No module depends on the GUI.

---

### 1.3 Type Definitions

All types are in TypeScript. The implementation language is TypeScript/Node.js to match the existing Chirality frontend stack.

```typescript
// ── Session ──────────────────────────────────────────

interface Session {
  id: string;                          // UUIDv4 (Chirality's session ID)
  createdAt: string;                   // ISO 8601
  updatedAt: string;                   // ISO 8601
  projectRoot: string;                 // absolute path to project
  persona: string | null;              // e.g. "DECOMP", "ORCHESTRATOR", null for Direct
  mode: "workbench" | "pipeline" | "direct";
    claudeSessionId: string | null;        // Claude Code session_id from system/init (source of truth for --resume)
}

// ── Claude Code Stream Events ────────────────────────
//
// When spawned with --output-format stream-json --verbose --include-partial-messages,
// Claude Code emits NDJSON (one JSON object per line) to stdout.
//
// With --verbose and --include-partial-messages, events include raw Anthropic
// API stream events wrapped in { type: "stream_event", event: {...} }.
// Without those flags, events are higher-level message objects.
//
// The types below represent the high-level events (without --include-partial-messages).
// For text streaming, use --include-partial-messages and filter for
// stream_event where event.delta.type === "text_delta".

// High-level events (--output-format stream-json, no --include-partial-messages):
type ClaudeCodeEvent =
  | { type: "system"; subtype: "init"; session_id: string; tools: string[]; model: string }
  | { type: "assistant"; message: { id: string; content: ContentBlock[] }; session_id: string }
  | { type: "user"; message: { id: string; content: ContentBlock[] }; session_id: string }
  | { type: "result"; subtype: "success"; result: string; session_id: string;
      total_cost_usd: number; usage: UsageInfo }
  | { type: "result"; subtype: "error"; error: string; session_id: string }
  | { type: "result"; subtype: "max_turns"; session_id: string };

// With --include-partial-messages, you additionally receive:
type StreamDeltaEvent =
  | { type: "stream_event"; event: {
      type: "content_block_delta";
      delta: { type: "text_delta"; text: string } | { type: "input_json_delta"; partial_json: string };
    }; session_id: string }
  | { type: "stream_event"; event: {
      type: "content_block_start";
      content_block: { type: "tool_use"; id: string; name: string } | { type: "text"; text: string };
    }; session_id: string }
  | { type: "stream_event"; event: {
      type: "content_block_stop";
    }; session_id: string };

type ContentBlock =
  | { type: "text"; text: string }
  | { type: "tool_use"; id: string; name: string; input: Record<string, unknown> }
  | { type: "tool_result"; tool_use_id: string; content: string | Array<Record<string, unknown>>;
      is_error?: boolean };

interface UsageInfo {
  input_tokens: number;
  output_tokens: number;
  cache_read_input_tokens?: number;
  cache_creation_input_tokens?: number;
}

// ── UI Events (Chirality GUI ← Harness) ─────────────

type UIEvent =
  | { type: "chat:delta"; sessionId: string; text: string }
  | { type: "chat:complete"; sessionId: string; text: string }
  | { type: "tool:start"; sessionId: string; toolUseId: string; name: string; input: Record<string, unknown> }
  | { type: "tool:result"; sessionId: string; toolUseId: string; content: string; isError: boolean }
  | { type: "session:init"; sessionId: string; claudeSessionId: string | null; model: string; tools: string[] }
  | { type: "session:complete"; sessionId: string; costUsd: number; usage: UsageInfo }
  | { type: "session:error"; sessionId: string; error: string }
  | { type: "process:exit"; sessionId: string; code: number | null; signal: string | null };

 // ── Persona ──────────────────────────────────────────

interface PersonaConfig {
  id: string;                          // e.g. "DECOMP", "ORCHESTRATOR"
  sourceFile: string;                  // e.g. "agents/AGENT_PROJECT_DECOMP.md"
  allowedTools?: string[];             // Claude Code tool names (e.g. "Read", "Bash(git *)")
  disallowedTools?: string[];          // Claude Code tool names to deny
  maxTurns?: number;                   // override default max turns for this persona
}

// ── Logging ──────────────────────────────────────────

interface LogEntry {
  timestamp: string;                   // ISO 8601 with milliseconds
  sessionId: string;
  level: "debug" | "info" | "warn" | "error";
  event: string;                       // e.g. "turn:start", "process:spawn", "parse:error"
  data?: Record<string, unknown>;
}
```

---

### 1.4 Module Contracts

#### ClaudeCodeManager

```typescript
interface ClaudeCodeManager {
  /**
   * Spawn a Claude Code process for a turn.
   * Sends the user message via -p flag and streams results.
   * Claude Code handles the entire agentic loop internally.
   * Yields UIEvent objects parsed from Claude Code's NDJSON output.
   */
  startTurn(
    session: Session,
    userMessage: string,
    opts?: TurnOpts
  ): AsyncIterable<UIEvent>;

  /**
   * Send SIGINT to the running Claude Code process.
   * Equivalent to Ctrl-C — lets Claude Code clean up gracefully.
   */
  interrupt(sessionId: string): void;

  /**
   * Hard kill: SIGTERM, wait 5s, then SIGKILL if still alive.
   */
  kill(sessionId: string): void;

  /** Whether a Claude Code process is currently running for this session. */
  isRunning(sessionId: string): boolean;
}

interface TurnOpts {
  permissionMode?: "default" | "acceptEdits" | "dontAsk" | "plan"; // maps to --permission-mode

  // Tool availability and policy (turn-level overrides)
  tools?: string;                      // maps to --tools (availability). default: "default"
  disallowedTools?: string[];           // maps to --disallowedTools (hard deny). repeatable flags
  autoApproveTools?: string[];          // maps to --allowedTools (auto-approve/no prompt). repeatable flags

  // Optional overrides that take precedence over persona defaults if provided
  toolsOverride?: string;
  disallowedToolsOverride?: string[];
  autoApproveToolsOverride?: string[];

  maxTurns?: number;                   // maps to --max-turns (default: 25)
  systemPromptAppend?: string;          // additional context for this turn only (appended after persona)
  verbose?: boolean;                    // maps to --verbose (default: true)
  includePartialMessages?: boolean;     // maps to --include-partial-messages (default: true)
}
```

**Guarantees:**
- Only one Claude Code process runs per session at a time. `startTurn()` rejects with an error if called while a process is already running for that session.
- The async iterable yields `UIEvent` objects parsed from Claude Code's `--output-format stream-json` NDJSON stdout.
- On process exit (normal or crash), a `process:exit` event is the final event yielded.
- If the process exits without emitting a `result` event, the harness yields `session:error` before `process:exit`.
- `stderr` lines are captured and logged at `warn` level, not yielded as UIEvents.
- The spawned process inherits a filtered environment (§2.2).

#### PersonaManager

```typescript
interface PersonaManager {
  /**
   * Load persona configuration from the project's agents/ directory.
   * Parses frontmatter for tool restrictions and settings.
   * Returns null if persona not found.
   */
  load(projectRoot: string, personaId: string): Promise<PersonaConfig | null>;

  /** List available personas by scanning agents/AGENT_*.md files. */
  list(projectRoot: string): Promise<PersonaConfig[]>;

  /**
   * Build the system prompt for a turn. Assembles base identity,
   * project context, persona instructions, and mode instructions.
   * Passed to Claude Code via --append-system-prompt.
   */
  buildSystemPrompt(
    projectRoot: string,
    persona: PersonaConfig | null,
    mode: Session["mode"]
  ): Promise<string>;
}
```

**Guarantees:**
- `buildSystemPrompt()` reads `README.md`, `AGENTS.md`, and the persona's `AGENT_*.md` file from `projectRoot`.
- Files are cached with `mtime` invalidation (re-read only when modified on disk).
- The total appended prompt is capped at 16,000 tokens. Truncation priority: persona instructions first, then project context. The base identity and mode instructions are never truncated.
- If no persona is set (Direct mode), only the base prompt and project context are included.

#### SessionManager

```typescript
interface SessionManager {
  create(projectRoot: string, persona: string | null, mode: Session["mode"]): Promise<Session>;
  resume(sessionId: string): Promise<Session>;
  save(session: Session): Promise<void>;
  list(projectRoot?: string): Promise<SessionSummary[]>;
  delete(sessionId: string): Promise<void>;
}

interface SessionSummary {
  id: string;
  createdAt: string;
  updatedAt: string;
  persona: string | null;
  mode: Session["mode"];
  projectRoot: string;
}
```

**Guarantees:**
- Sessions are persisted to `{projectRoot}/.chirality/sessions/{id}.json`.
- `save()` uses atomic write (write to `.tmp`, rename).
- `save()` is called after every completed turn.
- `resume()` reads the session and uses the stored `claudeSessionId` to pass `--resume` on the next turn.
- If Claude Code's `--resume` fails (e.g., Claude Code session data was cleared), the harness starts a fresh Claude Code session, logs a warning, and updates `claudeSessionId`.

---

### 1.5 Event Flow

```
User types message in GUI
        │
        ▼
GUI calls: POST /api/harness/turn { sessionId, message }
        │
        ▼
API route:
  1. SessionManager.resume(sessionId)
  2. PersonaManager.buildSystemPrompt(projectRoot, persona, mode)
  3. ClaudeCodeManager.startTurn(session, message, opts)
        │
        ▼
ClaudeCodeManager spawns:
  claude -p "${message}" \
    --output-format stream-json \
    --include-partial-messages \
    --verbose \
    --max-turns ${maxTurns} \
    --session-id ${sessionId}             # stable UUIDv4 chosen by Chirality
    --resume ${sessionId}                 # omit on first turn; include thereafter
    --append-system-prompt-file "${systemPromptFile}" \
    --permission-mode ${permissionMode}   # default per Chirality mode (see TurnOpts)
    --tools "${tools}"                    # tool availability allowlist (or "default")
    --disallowedTools "${disallowedTools}"# hard deny (repeatable)
    --allowedTools "${autoApproveTools}"  # auto-approval only (repeatable)
        │
        ▼
stdout: NDJSON lines → parse → map to UIEvent → yield
stderr: lines → LogEntry at warn level
        │
        ▼
API route streams UIEvents to GUI via SSE
        │
        ▼
GUI routes:
  chat:delta       → Chat pane (append text token-by-token)
  chat:complete    → Chat pane (finalize, show cost)
  tool:start       → Terminal pane / activity indicator
  tool:result      → Terminal pane / file tree refresh
  session:init     → Store claudeSessionId
  session:complete → Save session, update history sidebar
  session:error    → Error toast
  process:exit     → Re-enable input, handle crashes
```

---

## Part 2: Specification

---

### 2.1 Claude Code Process Lifecycle

Each call to `startTurn()` spawns a new Claude Code process. Claude Code manages its own agentic loop internally — it calls the LLM, decides on tools, executes them, reads results, and loops until it produces a final text response or hits its turn limit.

**Spawn command:**

```bash
claude -p "${USER_MESSAGE}" \
  --output-format stream-json \
  --include-partial-messages \
  --verbose \
  --max-turns ${MAX_TURNS} \
  --append-system-prompt-file "${SYSTEM_PROMPT_FILE}" \
  ${RESUME_FLAG} \
  ${TOOL_FLAGS}
```

**Flag mapping:**

| Chirality Concept | Claude Code Flag | Notes |
|-------------------|-----------------|-------|
| User message | `-p "message"` | Non-interactive / print mode |
| Streaming output | `--output-format stream-json` | NDJSON to stdout |
| Text deltas | `--include-partial-messages` | Enables `stream_event` with `text_delta` |
| Debug info | `--verbose` | Richer event detail in stream |
| Turn limit | `--max-turns N` | Default: 25 |
| Persona prompt | `--append-system-prompt-file ./prompt.txt` | Appends to Claude Code’s built-in prompt (preferred) |
| Session resume | `--resume SESSION_ID` | Continues prior conversation |
| Tool availability | `--tools "Read,Grep,Glob,Bash"` | Per-persona tool allowlist |
| Tool deny | `--disallowedTools "Write" "Edit"` | Per-persona hard deny |
| Auto-approve tools | `--allowedTools "Bash(git *)" "Read"` | Tools that run without prompting |
| Permission mode | `--permission-mode dontAsk` | Headless-safe default: auto-deny tools unless explicitly auto-approved/allowed (see policy) |


**Headless permission strategy (v0.5):**
- Default `--permission-mode dontAsk` for `pipeline` and `workbench` turns running in `-p` mode.
  - In this mode Claude Code **does not prompt**; tool actions are **denied unless allowed**.
  - Allow specific safe actions by supplying `--allowedTools` patterns (auto-approve) and by constraining availability with `--tools`.
- `direct` mode may also use `dontAsk` by default; users who want interactive approvals should run Claude Code interactively outside the harness.
- Do **not** use permissive bypass modes (e.g., skip/bypass permissions) in v0.5; treat them as explicit, opt-in “YOLO” only.

**Why `--append-system-prompt` / `--append-system-prompt-file` instead of `--system-prompt`:** The `--system-prompt` flag fully replaces Claude Code's built-in system prompt, which includes its tool definitions, safety instructions, and behavioral calibration. Using `--append-system-prompt` (or the preferred `--append-system-prompt-file`) preserves all of that and adds the persona/project context on top.

**Process management:**
- Spawned via Node.js `child_process.spawn()` with `{ stdio: ['pipe', 'pipe', 'pipe'] }`.
- The user message is passed as the print-mode query argument (after `-p`). For very large messages, the implementation MAY switch to stdin to avoid shell/argv escaping limits.
- The system prompt is passed via `--append-system-prompt-file` (preferred) to avoid argv length limits and escaping issues.
- `stdout` is read as a UTF-8 line stream. Each line is parsed as JSON.
- `stderr` is read line-by-line for debug logging.
- The process is tracked in an in-memory `Map<sessionId, ChildProcess>`.
- `interrupt()` sends `SIGINT`. `kill()` sends `SIGTERM`, waits 5 seconds, then `SIGKILL`.

**One process per session at a time:** If a turn is in progress and the user sends another message, the API route rejects with 409 Conflict. Claude Code does not support concurrent operations on the same session.

---

### 2.2 Environment Safety

The spawned Claude Code process inherits the server's environment, filtered for safety.

**Hard denylist (stripped from child process env):** Any env var matching these patterns is removed before spawning:
- `*_SECRET`, `*_PASSWORD`, `*_CREDENTIAL`
- `*_KEY`, `*_TOKEN`, `*_API_KEY`
- `DATABASE_URL`, `REDIS_URL` (may contain credentials)

**Precedence:** Apply the hard denylist first, then re-add any explicitly whitelisted variables (for example `ANTHROPIC_API_KEY`).

**Explicitly passed through:**
- `ANTHROPIC_API_KEY` — Claude Code requires this. Never logged, never emitted in any UIEvent or LogEntry.
- `PATH`, `HOME`, `USER`, `SHELL`, `TERM` — standard shell operation.
- `NODE_ENV`, `NODE_OPTIONS` — needed if Claude Code runs Node-based tools.

**API key handling:** The `ANTHROPIC_API_KEY` must be available to the Claude Code process. Recommended: set it in the server's environment. The harness never logs it, never includes it in stream output, and redacts it from any spawn command logged for diagnostics.

---

### 2.3 Stream Parsing

Claude Code's `--output-format stream-json` with `--include-partial-messages` and `--verbose` emits NDJSON to stdout. The `ClaudeCodeManager` reads stdout line-by-line, parses each line as JSON, and maps it to a `UIEvent`.

**Mapping logic:**

| Claude Code Event | UIEvent | Notes |
|-------------------|---------|-------|
| `{ type: "system", subtype: "init" }` | `session:init` | Captures `session_id`, `model`, `tools` |
| `{ type: "stream_event", event: { delta: { type: "text_delta" } } }` | `chat:delta` | Token-by-token text streaming |
| `{ type: "stream_event", event: { type: "content_block_start", content_block: { type: "tool_use" } } }` | `tool:start` | Tool invocation beginning |
| `{ type: "assistant", message: { content: [...] } }` | (extract tool_use blocks) | Complete assistant turn — use for tool:start if stream_events were missed |
| `{ type: "user", message: { content: [{ type: "tool_result" }] } }` | `tool:result` | Tool execution result |
| `{ type: "result", subtype: "success" }` | `chat:complete` + `session:complete` | Final response text + cost/usage |
| `{ type: "result", subtype: "error" }` | `session:error` | Claude Code error |
| `{ type: "result", subtype: "max_turns" }` | `session:error` | Turn limit reached |

**Robustness rules:**
- Malformed JSON lines (parse failure) are logged at `warn` level and skipped.
- Unknown event types or subtypes are ignored. Claude Code may add new event types in future versions.
- If the process exits without emitting a `result` event, the harness emits `session:error` with the exit code as context, followed by `process:exit`.
- Empty lines and whitespace-only lines are silently skipped.

---

### 2.4 Persona-to-Context Mapping

When a session has an active persona, the `PersonaManager` builds a system prompt appended to Claude Code's built-in prompt via `--append-system-prompt-file` (preferred) or `--append-system-prompt`.

**System prompt assembly order:**

```
[1. Base identity — static]
  You are operating within the Chirality Command Center.
  Project root: {projectRoot}
  Mode: {workbench|pipeline|direct}

[2. Project context — dynamic, from projectRoot]
  Contents of README.md (if exists, max 4KB)
  Contents of AGENTS.md (if exists, max 4KB)

[3. Persona instructions — conditional]
  Full contents of agents/AGENT_{persona}.md (if persona is set)

[4. Mode-specific instructions — conditional]
  Workbench: "Interactive workbench mode. Engage conversationally.
              Explain your reasoning. Ask for clarification when needed."
  Pipeline:  "Pipeline execution mode. Execute the task efficiently
              with minimal interaction. Report results concisely."
  Direct:    "Direct terminal mode. Execute commands as requested.
              Minimal commentary."
```

**Per-persona tool scoping:** Persona files may declare tool restrictions and auto-approval policies via a YAML frontmatter block:

```markdown
---
tools: "Read,Grep,Glob,Bash"           # maps to --tools (availability allowlist)
disallowed_tools: ["Write","Edit"]        # maps to --disallowedTools (hard deny)
auto_approve_tools: ["Bash(git *)","Read"]# maps to --allowedTools (no prompt)
max_turns: 10
---
# AGENT_DECOMP

You are the decomposition agent...
```

The `PersonaManager` parses this frontmatter and passes restrictions to `ClaudeCodeManager` as:
- `--tools` for *tool availability* (allowlist),
- `--disallowedTools` for *hard denies* (removed from context), and
- `--allowedTools` only for *auto-approval* (tools that can run without prompting).
If no frontmatter is present, `--tools "default"` is used and auto-approval is determined by the session’s permission policy.

**Caching:** Each file is read once per session and cached with its `mtime`. On each turn, `stat()` checks for changes. If `mtime` differs, the file is re-read.

**Token budget:** The total appended system prompt must not exceed 16,000 tokens (estimated at ~4 chars/token). If exceeded, truncation priority: persona instructions are cut first, then project context. The base identity and mode instructions are never truncated.

---

### 2.5 Session Resume

Claude Code supports session continuations via `--resume SESSION_ID`. Chirality leverages this for multi-turn conversations.

**Flow:**

1. **First turn** of a new session: Chirality starts Claude Code **without** `--resume`.
   - (Optional) Chirality MAY pass `--session-id {session.id}` to request a deterministic ID.
   - Chirality MUST still treat the `system/init.session_id` emitted by Claude Code as authoritative.
2. **Capture session_id:** The stream parser listens for `{ type: "system", subtype: "init" }` and stores `session_id` into `session.claudeSessionId`.
   - If `--session-id` was supplied and does **not** match `session_id`, log a warning and prefer the emitted `session_id`.
3. **Subsequent turns:** Chirality passes `--resume {session.claudeSessionId}`.
4. **Resume failure:** If `--resume` fails (e.g., Claude Code storage cleared), Claude Code will error.
   - The harness starts a fresh session (no `--resume`), captures the new `session_id` from init, updates `claudeSessionId`, and emits `session:error` + `session:init`.


**What Chirality persists vs. what Claude Code persists:**
- **Claude Code** persists the full conversation transcript, tool results, and internal state in its own session storage (`~/.claude/projects/`).
- **Chirality** persists session metadata only: IDs, persona, mode, timestamps. It does not duplicate the conversation transcript.
- If Chirality needs to display prior turns on session resume (e.g., populating the chat pane), it re-reads from Claude Code's session data or replays from its own event log (see §2.7).

---

### 2.6 Streaming Protocol (GUI ↔ Harness)

**API routes:**

```
POST   /api/harness/turn              { sessionId, message }
  → Response: text/event-stream (SSE of UIEvents)

POST   /api/harness/interrupt          { sessionId }
  → Response: 200 OK | 404 Not Found

POST   /api/harness/session/create     { projectRoot, persona, mode }
  → Response: 201 { session }

GET    /api/harness/session/list       ?projectRoot=...
  → Response: 200 [SessionSummary, ...]

GET    /api/harness/session/:id
  → Response: 200 { session }

DELETE /api/harness/session/:id
  → Response: 204 No Content
```

**GUI event routing:**

| UIEvent | GUI Target |
|---------|-----------|
| `chat:delta` | Chat pane — append text token by token |
| `chat:complete` | Chat pane — finalize message, show cost badge |
| `tool:start` | Terminal pane — show tool name + input summary |
| `tool:result` | Terminal pane — show result, trigger file tree refresh |
| `session:init` | Status bar — show model name, store claudeSessionId |
| `session:complete` | History sidebar — update, save session |
| `session:error` | Error toast / warning banner |
| `process:exit` | Re-enable message input, handle crashes |

---

### 2.7 Observability

**Log location:** `{projectRoot}/.chirality/logs/harness.log`  
**Format:** JSONL (one JSON object per line).

**What is logged:**

| Event | Level | Data |
|-------|-------|------|
| Turn started | info | `{ userMessage (first 200 chars), persona, mode }` |
| Process spawned | info | `{ command (API key redacted), pid }` |
| session:init received | info | `{ claudeSessionId, model, tools }` |
| Tool invoked | info | `{ toolName, inputSummary (first 200 chars) }` |
| Tool result | info | `{ toolName, isError, contentLength }` |
| Turn completed | info | `{ costUsd, inputTokens, outputTokens, durationMs }` |
| Resume attempted | info | `{ claudeSessionId }` |
| Resume failed | warn | `{ claudeSessionId, error }` |
| Process exited | info | `{ exitCode, signal, durationMs }` |
| Parse error | warn | `{ line (first 500 chars) }` |
| stderr output | warn | `{ line (first 500 chars) }` |
| Unhandled error | error | `{ message, stack }` |

**Sensitive data:** The spawn command is logged with `ANTHROPIC_API_KEY` redacted. User messages are truncated to 200 characters. Tool inputs containing file contents are truncated to 200 characters.

**Rotation:** When `harness.log` exceeds 10MB, it is renamed to `harness.log.1` (overwriting any existing `.1` file) and a new `harness.log` is started. One rotated file kept.

**Diagnostic prompt replay:** The harness saves the system prompt used for each turn to `.chirality/prompts/{sessionId}-system.txt` (overwritten each turn). This enables running the same prompt directly through Claude Code CLI to isolate whether a bug is in the wrapper or the model:

```bash
claude -p "the exact user message" \
  --output-format stream-json \
  --append-system-prompt-file ".chirality/prompts/SESSION_ID-system.txt" \
  --resume CLAUDE_SESSION_ID
```

---

## Part 3: Implementation Plan

Four phases. Each produces a working, testable artifact.

---

### Phase 1: ClaudeCodeManager + Stream Parser
**Estimated effort:** 2–3 days  
**Dependencies:** Claude Code CLI installed (e.g., via npm package `@anthropic-ai/claude-code` or Anthropic’s recommended installer).  
**Deliverable:** `src/harness/claude-code-manager.ts`, `src/harness/stream-parser.ts`

Tasks:
1. Implement `startTurn()`: build the `claude` command from session + persona + opts, spawn via `child_process.spawn()`.
2. Implement stdout line-by-line reading (split on `\n`, handle partial lines with a buffer).
3. Implement the `ClaudeCodeEvent → UIEvent` mapping (§2.3).
4. Implement `stream_event` handling for `text_delta` → `chat:delta` (token-by-token streaming).
5. Implement `tool_use` content block detection → `tool:start`, and `tool_result` user messages → `tool:result`.
6. Implement `result` event handling → `chat:complete` / `session:complete` / `session:error`.
7. Implement stderr capture → log entries.
8. Implement process tracking (`Map<sessionId, ChildProcess>`), `interrupt()`, `kill()`, `isRunning()`.
9. Implement env filtering (§2.2) — strip sensitive vars, preserve required ones.
10. Handle process exit: detect missing `result` event → emit `session:error` before `process:exit`.

**Tests:**
- Spawn Claude Code with `-p "What is 2+2?" --output-format stream-json --max-turns 1`. Assert `session:init` is emitted first. Assert `chat:delta` events arrive. Assert `chat:complete` or `session:complete` is emitted. Assert `process:exit` follows.
- Interrupt test: spawn a multi-turn task, call `interrupt()`, assert process terminates and `process:exit` is emitted.
- Env filtering test: set `TEST_SECRET_PASSWORD=foo` in env, assert it is absent from child process env. Assert `ANTHROPIC_API_KEY` is present.
- Malformed line test: feed a non-JSON line to the parser, assert it is logged and skipped without crashing.

**Risk:** Claude Code's `stream-json` event format is not versioned. A Claude Code update could change event shapes. Mitigation: defensive parsing (unknown fields/types are ignored, not thrown), and the diagnostic replay mechanism (§2.7) to quickly identify format changes.

---

### Phase 2: PersonaManager + Context Injection
**Estimated effort:** 1–2 days  
**Dependencies:** Phase 1  
**Deliverable:** `src/harness/persona-manager.ts`

Tasks:
1. Implement `load()`: read `agents/AGENT_{id}.md`, parse YAML frontmatter for `tools`, `disallowed_tools`, `max_turns`.
2. Implement `list()`: scan `agents/AGENT_*.md` files, return `PersonaConfig[]`.
3. Implement `buildSystemPrompt()` per §2.4: assemble base identity + project context + persona instructions + mode instructions.
4. Implement file cache with `mtime` invalidation.
5. Implement token budget enforcement (16K cap, ~4 chars/token, truncation priority).
6. Save assembled system prompt to `.chirality/prompts/{sessionId}-system.txt` for diagnostic use (§2.7).

**Tests:**
- Create a mock project with `README.md`, `AGENTS.md`, and `agents/AGENT_DECOMP.md` with frontmatter `tools: [Read, Grep]`. Load persona. Assert `allowedTools` is `["Read", "Grep"]`. Build system prompt. Assert all three files appear. Assert token budget is respected.
- Modify `README.md` on disk. Rebuild prompt. Assert cache invalidation works (new content appears).
- Set persona to null. Assert no persona instructions in prompt.

---

### Phase 3: SessionManager + Persistence
**Estimated effort:** 1–2 days  
**Dependencies:** Phase 1 (needs `claudeSessionId` from stream)  
**Deliverable:** `src/harness/session-manager.ts`

Tasks:
1. Implement `create()`: generate UUID, initialize session object, create `.chirality/sessions/` directory.
2. Implement `save()`: atomic write (`write .tmp` → `rename`) to `{projectRoot}/.chirality/sessions/{id}.json`.
3. Implement `resume()`: read session JSON. If `claudeSessionId` is set, it will be used by `ClaudeCodeManager` for `--resume`.
4. Implement `list()`: scan `.chirality/sessions/`, return summaries sorted by `updatedAt` descending.
5. Implement `delete()`: remove session file, kill associated process if running.
6. Hook `save()` into the turn lifecycle: on `session:complete` or `process:exit`, update session with latest `claudeSessionId` and persist.

**Tests:**
- Create a session. Start a turn. Assert `claudeSessionId` is captured from `session:init` and saved. Resume. Assert `claudeSessionId` is available for `--resume`. Delete. Assert file is removed.

---

### Phase 4: API Routes + GUI Wiring
**Estimated effort:** 2–3 days  
**Dependencies:** All prior phases  
**Deliverable:** Next.js API routes + frontend event handling

Tasks:
1. Implement `POST /api/harness/turn`: validate session exists, reject 409 if turn in progress, call `ClaudeCodeManager.startTurn()`, pipe `UIEvent` stream as SSE.
2. Implement `POST /api/harness/interrupt`: call `ClaudeCodeManager.interrupt()`, return 200.
3. Implement session CRUD routes (create, list, get, delete).
4. Wire `chat:delta` → chat pane (token-by-token append).
5. Wire `chat:complete` → chat pane (finalize message, show cost badge).
6. Wire `tool:start` / `tool:result` → terminal pane activity.
7. Wire `session:init` → status bar (model name), store `claudeSessionId`.
8. Wire `session:error` → error toast.
9. Wire `process:exit` → re-enable message input.
10. Wire session create/resume/list → History sidebar.
11. Wire persona selection + mode selection → session creation.

**End-to-end test:** Select DECOMP persona → create Workbench session → send message → chat text streams token-by-token → agent uses a tool → `tool:start` appears → `tool:result` triggers file tree refresh → send follow-up message → session resumes via `--resume` → interrupt mid-turn → process stops → re-enable input.

---

### Phase Summary

| Phase | Deliverable | Effort | Depends On | Core Risk |
|-------|------------|--------|-----------|-----------|
| 1 | ClaudeCodeManager + StreamParser | 2–3d | — | stream-json format stability |
| 2 | PersonaManager | 1–2d | Phase 1 | Frontmatter parsing edge cases |
| 3 | SessionManager | 1–2d | Phase 1 | --resume reliability |
| 4 | GUI Wiring | 2–3d | All | SSE event routing correctness |
| **Total** | | **6–10 days** | | |

---

### File Structure

```
src/harness/
├── claude-code-manager.ts   # Phase 1: process lifecycle + event emission
├── stream-parser.ts         # Phase 1: NDJSON parsing + event mapping
├── persona-manager.ts       # Phase 2: persona loading + system prompt assembly
├── session-manager.ts       # Phase 3: session CRUD + persistence
├── logger.ts                # Structured JSONL logger (§2.7)
├── types.ts                 # All shared types from §1.3
├── defaults.ts              # Default config constants (max turns, token budget, etc.)
└── index.ts                 # Public API: startTurn, interrupt, createSession, etc.
```

---

### What Was Removed (and Why)

| v1.1 Module | Why Removed | Claude Code Equivalent |
|-------------|-------------|----------------------|
| `TerminalManager` | Claude Code owns the shell | Stateful bash with persistent CWD/env |
| `sentinel-scanner.ts` | No sentinel envelope needed | Claude Code tracks state internally |
| `AnthropicDriver` | Claude Code owns LLM communication | Built-in SDK with streaming, retry, caching |
| `ToolDispatcher` | Claude Code owns tool routing + permissions | `--tools`, `--disallowedTools`, `--allowedTools`, permission prompts |
| `harness-loop.ts` | Claude Code owns the agentic loop | Internal loop with `--max-turns` guard |
| `events.ts` | Simplified to inline types | — |

**Estimated savings:** 6–10 days of implementation removed. The sentinel scanner (partial-read safety across chunk boundaries) and Anthropic streaming driver (input_json_delta accumulation) were the two highest-risk components.

---

### Open Decisions

1. **Claude Code version pinning:** The `stream-json` output format is not versioned. Decide whether to pin a specific Claude Code version or track latest. Consider a version check on startup that logs a warning if the installed version differs from the tested version.

2. **Conversation history display on resume:** Claude Code owns the conversation transcript. If the GUI needs to show prior turns when resuming a session, options are: (a) re-read from Claude Code's session storage at `~/.claude/projects/`, (b) maintain a Chirality-side event log that replays into the chat pane, or (c) show a "session resumed" marker and only display new turns. Option (c) is simplest for v0.5.

3. **Permission prompt interception:** In `-p` mode, Claude Code may auto-approve tool use or may error if a tool isn't in `--allowedTools`. Verify how Claude Code behaves in non-interactive mode under `--permission-mode dontAsk` when a tool is requested but not covered by `--allowedTools` / allow rules (deny vs error), and confirm that your chosen allow patterns prevent hangs. If not, the Claude Agent SDK provides a `permission_callback` mechanism.

4. **Agent SDK migration:** Anthropic provides a Claude Agent SDK for programmatic embedding (TypeScript package is commonly referred to as `@anthropic-ai/claude-agent-sdk`, and Python as `claude-agent-sdk` — verify current package names before implementation). The SDK provides a structured API with streaming callbacks, hooks, and native message objects. If the child process approach hits limitations (e.g., needing fine-grained hook control, permission callbacks, or structured outputs), migrating to the SDK preserves the same architectural shape with better integration.

5. **Subagent orchestration:** Out of scope for v0.5. Claude Code supports `--agents` for defining custom subagents. Revisit when the ORCHESTRATOR persona needs child agents.

---

### Definition of Done (v0.5 Harness)

The harness is shippable when:
1. A user can select a persona, create a session, and send a message.
2. Claude Code's response streams token-by-token into the chat pane.
3. Tool invocations appear in the terminal pane with start/result feedback.
4. Follow-up messages resume the same Claude Code session via `--resume`.
5. Session history persists across app restarts.
6. The user can interrupt a running turn.
7. Persona tool restrictions are enforced via Claude Code's `--tools` (availability allowlist) and `--disallowedTools` (hard deny). Auto-approval is configured via `--allowedTools`.
