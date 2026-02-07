You are the implementation agent for Chirality Agent Harness v0.5 in:
`/Users/ryan/ai-env/projects/chirality-app`

Follow `AGENT_HARNESS_SPEC-v2-3.md` as the source of truth.

Read in this order:
1. `frontend/AGENT_HARNESS_SESSION_LOG.md` (latest entry first)
2. `frontend/AGENT_HARNESS_DECISIONS.md`
3. `frontend/AGENT_HARNESS_IMPLEMENTATION_CHECKLIST.md`
4. `AGENT_HARNESS_SPEC-v2-3.md`
5. `frontend/docs/harness/chirality_harness_graphs_and_sequence.md`
6. `frontend/components/ChatPanel.tsx`
7. `frontend/components/ResizableLayout.tsx`
8. `frontend/components/WorkbenchView.tsx`
9. `frontend/components/PipelineView.tsx`
10. `frontend/components/DirectLinkView.tsx`
11. `frontend/app/api/harness/turn/route.ts`
12. `frontend/app/api/harness/session/create/route.ts`
13. `frontend/app/api/harness/session/list/route.ts`
14. `frontend/app/api/harness/session/[id]/route.ts`
15. `frontend/lib/harness/index.ts`
16. `frontend/lib/harness/types.ts`

Then start coding immediately unless blocked.

Scope for this run:
Primary goal: start Assignment C by wiring frontend chat flow to Harness APIs.
- Migrate `ChatPanel` send flow from `/api/chat` to harness session + SSE turn flow.
- Ensure session bootstrap path is in place (create/load harness session with mode/persona/projectRoot).
- Handle all required harness `UIEvent` types in chat UI:
  - `chat:delta`, `chat:complete`, `tool:start`, `tool:result`,
  - `session:init`, `session:complete`, `session:error`, `process:exit`.
- Add interrupt action/state wired to `POST /api/harness/interrupt`.
- Keep existing UX behavior where possible (local chat history and loading transitions).

Target files:
- `frontend/components/ChatPanel.tsx`
- `frontend/components/ResizableLayout.tsx` (if needed for mode/persona/projectRoot wiring)
- `frontend/components/WorkbenchView.tsx` (if needed for persona mapping)
- `frontend/components/PipelineView.tsx` (if needed for persona mapping)
- `frontend/components/DirectLinkView.tsx` (if needed for direct mode wiring)

Hard constraints:
- Keep Assignment A + Assignment B behavior intact.
- Keep `/api/chat` intact during migration (do not remove route).
- Preserve session CRUD behavior and filesystem persistence under `.chirality/sessions/{id}.json`.
- `system/init.session_id` remains authoritative for `claudeSessionId`.
- Never leak secrets in logs or API responses.
- One in-flight turn per session remains enforced (409 conflict).

Implementation requirements:
- Frontend must use harness session endpoints before turn streaming:
  - create/load session (`/api/harness/session/*`)
  - turn stream (`POST /api/harness/turn`, SSE)
  - interrupt (`POST /api/harness/interrupt`)
- Session metadata tracked in UI state must include at least:
  - `sessionId`, `claudeSessionId`, `mode`, `persona`.
- `session:error` must surface in UI (message or toast-equivalent entry).
- `process:exit` must always clear in-flight/loading state.
- If needed, map existing UI mode/persona selectors to harness persona IDs without breaking current views.

Validation before finishing:
1. Lint/typecheck on touched files.
2. Frontend smoke flow:
   - Start a session from UI path (or equivalent test harness path).
   - Send a message and verify streamed `chat:delta`/`chat:complete` rendering.
   - Verify `session:init` metadata is captured in UI state.
   - Verify `process:exit` restores input availability.
3. Interrupt flow:
   - Start a long-running turn.
   - Trigger interrupt and verify stream exits cleanly and UI unblocks.
4. Regression check:
   - Existing harness session CRUD + turn route behavior remains working.
   - `/api/chat` route remains untouched and available.

Progress tracking required at end:
1. Update completed boxes in `frontend/AGENT_HARNESS_IMPLEMENTATION_CHECKLIST.md`.
2. Append new entry to `frontend/AGENT_HARNESS_SESSION_LOG.md` using template.
3. Add non-obvious decisions to `frontend/AGENT_HARNESS_DECISIONS.md`.
4. Include exactly one “Next session first task”.

Final report format:
1. Files changed
2. Completed vs partial checklist items
3. Validation results
4. Blockers/risks
5. Next exact tasks
