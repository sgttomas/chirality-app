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
