# Chirality Harness Decisions Register

Purpose: record implementation decisions that should persist across sessions to avoid rework and drift.

## Usage

- Add a new decision when behavior/design is non-obvious or when alternatives were considered.
- Do not rewrite history; supersede by adding a new decision that references the old ID.
- Keep each decision testable and tied to files or interfaces.

## Decision Template

```md
## D-XXX: <Short title>
- Date:
- Status: proposed | accepted | superseded
- Context:
- Decision:
- Consequences:
- References:
```

## D-000: v2.3 spec is authoritative
- Date: 2026-02-07
- Status: accepted
- Context: multiple historical approaches exist (custom Anthropic loop vs Claude Code subprocess harness).
- Decision: implementation follows `AGENT_HARNESS_SPEC-v2-3.md` as source of truth for architecture and behavior.
- Consequences: new work must align to subprocess + NDJSON + SSE design; conflicting legacy patterns are deprecated.
- References:
  - `AGENT_HARNESS_SPEC-v2-3.md`
  - `frontend/docs/harness/chirality_harness_graphs_and_sequence.md`

## D-001: Keep legacy `/api/chat` during migration
- Date: 2026-02-07
- Status: accepted
- Context: existing UI currently depends on `/api/chat` and direct Anthropic SDK flow.
- Decision: do not remove `/api/chat` until `/api/harness/*` is stable and UI switch is complete.
- Consequences: temporary dual-path backend is expected; avoid breaking existing chat until cutover.
- References:
  - `frontend/app/api/chat/route.ts`
  - `frontend/AGENT_HARNESS_IMPLEMENTATION_CHECKLIST.md`

## D-002: Checklist is completion gate
- Date: 2026-02-07
- Status: accepted
- Context: multi-session work needs a consistent done definition.
- Decision: checklist items are only checked when validated, not when code is merely written.
- Consequences: improves handoff reliability and keeps progress measurable.
- References:
  - `frontend/AGENT_HARNESS_IMPLEMENTATION_CHECKLIST.md`
  - `frontend/AGENT_HARNESS_SESSION_LOG.md`

## D-003: Phase 1 uses in-memory session store until SessionManager lands
- Date: 2026-02-07
- Status: accepted
- Context: `/api/harness/turn` and `/api/harness/interrupt` are required now, while full session persistence is Assignment B.
- Decision: maintain a temporary process-wide `Map<string, Session>` keyed by `sessionId`, updating `claudeSessionId` only from `session:init`.
- Consequences: enables end-to-end streaming, resume, and conflict control immediately; state will reset on server restart and must be replaced by `session-manager.ts` next.
- References:
  - `frontend/lib/harness/claude-code-manager.ts`
  - `frontend/app/api/harness/turn/route.ts`

## D-004: Redact print-mode message in process spawn logs
- Date: 2026-02-07
- Status: accepted
- Context: logging the raw `claude -p "<message>"` command risks leaking sensitive user content.
- Decision: replace the `-p` argument in `process:spawn` log output with `[USER_MESSAGE_REDACTED]`; keep detailed text only in truncated `turn:start` logs.
- Consequences: preserves observability while meeting secret-safety constraints.
- References:
  - `frontend/lib/harness/claude-code-manager.ts`
  - `frontend/lib/harness/logger.ts`

## D-005: Session lookup uses path cache with project-root fallback probing
- Date: 2026-02-07
- Status: accepted
- Context: `SessionManager.get/resume/delete` receives only `sessionId`, while persisted files live under `{projectRoot}/.chirality/sessions/{id}.json`.
- Decision: cache `sessionId -> filePath` on create/save/load and probe candidate roots (`known roots`, `process.cwd()`, and parent) when cache misses.
- Consequences: supports persistent session lookup for the current workspace without adding a separate global index file.
- References:
  - `frontend/lib/harness/session-manager.ts`
  - `frontend/app/api/harness/turn/route.ts`

## D-006: Reject session delete while a turn is in-flight
- Date: 2026-02-07
- Status: accepted
- Context: deleting a session file during an active run can race with terminal save hooks and recreate metadata unexpectedly on `process:exit`.
- Decision: `DELETE /api/harness/session/:id` returns `409` if `claudeCodeManager.isRunning(sessionId)` is true.
- Consequences: keeps delete semantics deterministic and prevents accidental session resurrection during active execution.
- References:
  - `frontend/app/api/harness/session/[id]/route.ts`
  - `frontend/lib/harness/index.ts`

## D-007: Resume fallback retries exactly once and suppresses intermediate `process:exit`
- Date: 2026-02-07
- Status: accepted
- Context: Assignment B requires one-time fallback when `--resume` fails, but emitting the failed-attempt terminal exit before retry would prematurely signal turn completion to SSE consumers.
- Decision: `startHarnessTurn(...)` marks retry eligibility from a resume-failure `session:error`, retries exactly once with `claudeSessionId: null`, and suppresses the first attempt's `process:exit` event while still persisting session state.
- Consequences: UI receives a single terminal `process:exit` for the logical turn while still observing the required resume-failure `session:error`.
- References:
  - `frontend/lib/harness/index.ts`

## D-008: Persona frontmatter parser is implemented in-repo (no external YAML dependency)
- Date: 2026-02-07
- Status: accepted
- Context: frontend package does not include a YAML/frontmatter dependency and Assignment B requires frontmatter extraction for tool policy fields.
- Decision: implement a bounded frontmatter parser in `persona-manager.ts` supporting scalar values, inline lists, and block lists for `tools`, `disallowed_tools`, `auto_approve_tools`, and `max_turns`.
- Consequences: no dependency churn, predictable parsing behavior for harness persona files, and easy mtime-cached persona reloads.
- References:
  - `frontend/lib/harness/persona-manager.ts`

## D-009: UI local sessions keep harness metadata and re-bootstrap on contract drift
- Date: 2026-02-07
- Status: accepted
- Context: Assignment C preserves local chat-history UX while switching transport to persisted harness sessions that are scoped by `{projectRoot, mode, persona}`.
- Decision: each local chat session stores harness metadata (`sessionId`, `claudeSessionId`, `mode`, `persona`, `projectRoot`); before each turn the UI loads the stored harness session and, if missing/mismatched, creates a new one via `/api/harness/session/create`.
- Consequences: local history remains stable per view while backend session metadata remains authoritative and resumable; changing mode/persona/root safely rolls to a new harness session instead of mutating server state in place.
- References:
  - `frontend/components/ChatPanel.tsx`
  - `frontend/components/ResizableLayout.tsx`
  - `frontend/components/WorkbenchView.tsx`
  - `frontend/components/PipelineView.tsx`
  - `frontend/components/DirectLinkView.tsx`
