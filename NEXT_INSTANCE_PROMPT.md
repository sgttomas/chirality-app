# Next Instance Prompt — Subagent Visibility & Tool Activity Enhancements

## Context

You are working on the chirality-app, an Electron + Next.js desktop application that wraps the Anthropic Claude Agent SDK (`@anthropic-ai/claude-agent-sdk@^0.2.37`). The app provides a harness layer for running AI agents against local project folders. A "Toolkit" panel was recently added (Phase 1 complete) to expose more SDK capabilities in the UI.

This prompt covers the **next area of work**: improving visual indicators for subagent activity, task assignments, and progress in the frontend.

---

## What Exists Today

### Architecture Summary

- **SDK wrapper:** `frontend/lib/harness/agent-sdk-manager.ts` calls `query()` from the SDK, iterates `SDKMessage` objects, and maps them to `UIEvent` objects via `agent-sdk-event-mapper.ts`
- **Event stream:** SSE from `POST /api/harness/turn` delivers `UIEvent` objects to the frontend
- **Frontend consumer:** `frontend/components/ChatPanel.tsx` handles events in `handleHarnessEvent()` and renders tool chips

### UIEvent Types (from `frontend/lib/harness/types.ts`)

```typescript
type UIEvent =
  | { type: "chat:delta"; sessionId: string; text: string }
  | { type: "chat:complete"; sessionId: string; text: string }
  | { type: "tool:start"; sessionId: string; toolUseId: string; name: string; input: Record<string, unknown> }
  | { type: "tool:result"; sessionId: string; toolUseId: string; content: string; isError: boolean }
  | { type: "session:init"; sessionId: string; claudeSessionId: string | null; model: string; tools: string[] }
  | { type: "session:complete"; sessionId: string; costUsd: number; usage: UsageInfo }
  | { type: "session:error"; sessionId: string; error: string }
  | { type: "process:exit"; sessionId: string; code: number | null; signal: string | null };
```

### Current Tool Chip System (ChatPanel.tsx)

All tool executions are rendered as ephemeral "tool chips" in the chat status area:

```typescript
type ToolChipStatus = "running" | "done" | "error";
type ToolChip = { toolUseId: string; name: string; status: ToolChipStatus };
```

- `tool:start` → `upsertToolChip(toolUseId, toolName, "running")` — orange chip with braille spinner
- `tool:result` → `markToolResult(toolUseId, isError)` — green ✓ or red ✕, auto-removed after 2.2s
- Max 4 chips visible at once (`TOOL_CHIP_LIMIT = 4`)
- Status text set via `toolStatusLabel(name)` which checks `TOOL_STATUS_LABELS` map then falls through to `humanizeToolName()`

**`TOOL_STATUS_LABELS` map (line 141-148):**
```typescript
const TOOL_STATUS_LABELS: Record<string, string> = {
  read_file: "Reading file",
  write_file: "Writing file",
  execute_command: "Running command",
  list_directory: "Scanning directory",
  search_file_content: "Searching files",
  glob: "Finding files",
};
```

Note: "Task" is NOT in this map. It falls through to `humanizeToolName("Task")` → `"Task"`.

**Event handler (line 843-880):**
```typescript
case "tool:start": {
  toolNameByUseIdRef.current[event.toolUseId] = event.name;
  clearToolTimer(event.toolUseId);
  upsertToolChip(event.toolUseId, event.name, "running");
  setStatusText(toolStatusLabel(event.name));
  return false;
}
case "tool:result": {
  markToolResult(event.toolUseId, event.isError);
  setStatusText(event.isError ? "Tool returned an error" : "Analyzing tool result");
  return false;
}
```

### How Subagents Look Today

When the SDK's Task tool fires, it appears as a **generic "Task" chip with a spinner**. There is:

- No indication of which subagent (PREPARATION, 4_DOCUMENTS, DEPENDENCIES, etc.)
- No description shown
- No distinct visual treatment
- No elapsed time
- No progress tracking
- No nested tool activity from inside the subagent
- No per-subagent cost attribution

### What Data IS Available in the Event Stream

The `tool:start` event for a Task invocation carries `input: Record<string, unknown>` with these fields:

| Field | Example Value | Currently Used? |
|-------|--------------|-----------------|
| `input.subagent_type` | `"PREPARATION"`, `"4_DOCUMENTS"`, `"DEPENDENCIES"` | ❌ Logged to console only (event-mapper.ts line 224) |
| `input.description` | `"Create folder structure and metadata"` | ❌ Logged to console only (event-mapper.ts line 225) |
| `input.prompt` | Full prompt text sent to subagent | ❌ Not surfaced anywhere |

The `tool:result` event for a Task carries `content` (subagent output text) and `isError`.

### What the Backend Tracks (but doesn't surface to UI)

In `agent-sdk-manager.ts` (line 454-504), the harness maintains an `activeSubagentRuns` map:

```typescript
type ActiveSubagentRun = {
  toolUseId: string;
  subagentType: string;
  description: string | null;
  startedAt: string;
};
```

Lifecycle logged to `.chirality/logs/harness.log`:
- `subagent:start` — toolUseId, subagentType, description, startedAt
- `subagent:complete` — adds finishedAt
- `subagent:interrupted` — adds finishedAt + reason

### What the TodoWrite Tool Provides

When the agent uses the `TodoWrite` tool, it fires as a `tool:start` event with `input.todos` containing a structured array:

```typescript
input.todos = [
  { content: "Fix authentication bug", status: "in_progress", activeForm: "Fixing authentication bug" },
  { content: "Run tests", status: "pending", activeForm: "Running tests" },
  { content: "Deploy to staging", status: "completed", activeForm: "Deploying to staging" },
]
```

This is currently shown as a generic "Todowrite" tool chip. The structured task data is not parsed or rendered.

---

## Enhancement Opportunities (No Backend Changes Needed)

### Tier 1 — Quick Wins (~10-30 lines each)

**1. Subagent identity on chip**
When `event.name === "Task"`, extract `event.input.subagent_type` and use it as the chip label:
- Instead of: `⠋ Task`
- Show: `⠋ PREPARATION`
- Or: `⠋ Task: PREPARATION`

**2. Subagent description tooltip**
Add `event.input.description` to the chip's `title` attribute so hovering shows what the subagent is doing.

**3. Add "Task" to TOOL_STATUS_LABELS**
Map `Task` to a more descriptive label: `"Delegating to subagent"`.

**4. Distinct chip styling for subagents**
When `event.name === "Task"`, apply a different color class (e.g., purple/guiding palette) to visually distinguish delegation from direct tool use.

### Tier 2 — Medium Effort (new state/components)

**5. Subagent elapsed time**
Add `startedAt: number` to the `ToolChip` type. For running chips, compute and display elapsed time (e.g., `⠋ PREPARATION — 12s`). Update via interval while chip is in "running" status.

**6. Persistent subagent tracker**
Instead of ephemeral chips (auto-removed after 2.2s), accumulate Task tool events into a dedicated **subagent activity list** that persists for the duration of the turn. Shows all subagents with their status (pending/running/complete/error), type, description, and elapsed time.

**7. Tool input/output detail drawer**
Make tool chips clickable/expandable. On click, show:
- For `tool:start`: the tool's `input` (JSON, collapsed)
- For `tool:result`: the tool's `content` (text, collapsed)
- For Task tools: the subagent prompt and result

**8. TodoWrite visualization**
When `event.name === "TodoWrite"` on `tool:start`, parse `event.input.todos` and render a structured task list with status indicators (pending/in_progress/completed). Update on subsequent TodoWrite events. This gives real-time visibility into agent task planning.

### Tier 3 — Requires Backend/SDK Changes

**9. Nested tool activity from subagents**
Currently, tool calls made *inside* a subagent do not bubble to the parent's event stream. The parent only sees `tool:start` (Task) and `tool:result` (Task). Individual Bash/Read/Write calls within the subagent are invisible.

Would require: SDK support for forwarding child process events to parent, or a custom event channel.

**10. Per-subagent cost attribution**
Cost is only reported on `session:complete` for the entire turn. No breakdown per subagent.

Would require: SDK support for per-tool-use cost tracking or usage reporting.

---

## Key Files

| File | Role | Lines |
|------|------|-------|
| `frontend/components/ChatPanel.tsx` | Event handler, tool chip rendering, status text | ~1460 |
| `frontend/lib/harness/types.ts` | UIEvent type definitions, ToolChip types | 166 |
| `frontend/lib/harness/agent-sdk-event-mapper.ts` | SDKMessage → UIEvent mapping, subagent correlation logging | ~260 |
| `frontend/lib/harness/agent-sdk-manager.ts` | ActiveSubagentRun tracking, lifecycle logging | ~570 |
| `frontend/app/globals.css` | Tool chip animations, toolkit styling | ~450 |

### ChatPanel.tsx Key Line References

| Concept | Lines |
|---------|-------|
| `TOOL_STATUS_LABELS` map | 141-148 |
| `humanizeToolName()` | 154-159 |
| `toolStatusLabel()` | 161-163 |
| `TOOL_CHIP_LIMIT`, `TOOL_CHIP_SETTLE_MS` | 151-152 |
| `ToolChip` type, `ToolChipStatus` type | ~100-110 (search for `type ToolChip`) |
| `upsertToolChip()` | 482-488 |
| `markToolResult()` | 490-494 |
| `handleHarnessEvent()` — tool:start case | 855-861 |
| `handleHarnessEvent()` — tool:result case | 862-866 |
| Tool chip JSX rendering | 1383-1417 |
| Status text area | 1370-1382 |

### agent-sdk-event-mapper.ts Key Line References

| Concept | Lines |
|---------|-------|
| Task tool detection + subagent_type extraction | 221-229 |
| parent_tool_use_id logging | 232-239 |

### agent-sdk-manager.ts Key Line References

| Concept | Lines |
|---------|-------|
| `ActiveSubagentRun` type | 30-35 |
| `activeSubagentRuns` map creation | within `startTurn()` |
| Task tool:start detection → map insert | 454-475 |
| Task tool:result detection → map delete + lifecycle log | 488-505 |
| Turn exit → log stranded subagents | 559-569 |

---

## Existing Design Patterns to Follow

### Visual Language
- **Primary accent:** Orange (`#f97316`, `var(--color-accent-orange)`)
- **Cognitive palette:** Purple/guiding (`#8b5cf6`, `var(--color-guiding)`) — suitable for subagent distinction
- **Text:** Main (`#f8fafc`), Dim (`#94a3b8`)
- **Monospace:** JetBrains Mono (`.mono` class)
- **Font sizes:** 8-11px for metadata, 9px for labels

### Component Patterns
- Tool chips: `mono inline-flex items-center gap-1.5 rounded border px-2 py-1 text-[9px] uppercase tracking-[0.1em]`
- Status badges: `mono rounded border px-2 py-0.5 text-[9px] uppercase tracking-[0.1em]`
- Collapsible sections: `useState` toggle with SVG chevron rotation
- Animations: `@keyframes` in globals.css, respect `prefers-reduced-motion`

### State Management
- Local React state with `useState` / `useRef`
- `sessionsRef.current` for accessing latest sessions in closures
- `updateSession()` pattern for immutable session updates
- localStorage persistence via existing `useEffect` at line 1040-1044

---

## Recently Completed Work (Toolkit Panel — Phase 1)

### New Files Added
- `frontend/lib/toolkit-config.ts` — Core types, validation, `buildTurnOptsFromToolkit`, preset storage
- `frontend/components/Toolkit.tsx` — Collapsible panel with Tier A fields + governance form
- `frontend/components/ToolkitPresets.tsx` — Preset save/load/apply/delete
- `frontend/scripts/validate-toolkit.mjs` — 35-check validation suite

### ChatPanel.tsx Changes
- `LocalChatSession` now has `toolkitOverrides: ToolkitOverrides`
- `streamTurn()` uses `buildTurnOptsFromToolkit()` instead of hardcoded `{ apiKey }`
- `sendPrompt()` has validation gate via `validateToolkitOverrides()`
- `ensureBootedHarnessSession()` sends only `apiKey` + optional `model` (narrowly scoped)
- `<Toolkit>` panel rendered right of messages column
- Override count badge in header metadata area
- Auto-collapse toolkit at width < 900px

### Invariants Maintained
1. SSE contract unchanged (no backend modifications)
2. Default path unchanged when toolkit overrides are empty
3. Governance visible in UI but runtime delegation remains fail-closed in harness gates

---

## Suggested Implementation Order

If asked to implement subagent visibility enhancements:

1. **Start with Tier 1 quick wins** — subagent identity on chips, description tooltip, distinct styling. These are ~10-30 lines of change in `ChatPanel.tsx` and `globals.css`, zero risk, high visibility improvement.

2. **Then TodoWrite visualization** — parse `input.todos` and render a task list. Medium effort but provides real-time insight into agent planning.

3. **Then subagent tracker** — persistent activity list for the turn duration. Replaces ephemeral chips for Task tools with a dedicated section.

4. **Then tool detail drawer** — expandable tool executions with input/output. Highest effort but most comprehensive.

All of the above require **zero backend changes**. The data is already in the event stream.
