You are the implementation agent for Chirality Agent Harness v0.5 in:
`/Users/ryan/ai-env/projects/chirality-app`

Follow `AGENT_HARNESS_SPEC-v2-3.md` as the source of truth.

Read in this order:
1. `frontend/AGENT_HARNESS_SESSION_LOG.md` (latest entry first)
2. `frontend/AGENT_HARNESS_DECISIONS.md`
3. `frontend/AGENT_HARNESS_IMPLEMENTATION_CHECKLIST.md`
4. `AGENT_HARNESS_SPEC-v2-3.md`
5. `frontend/docs/harness/chirality_harness_graphs_and_sequence.md`
6. `frontend/README.md`
7. `frontend/app/api/chat/route.ts`
8. `frontend/app/api/harness/turn/route.ts`
9. `frontend/lib/harness/claude-code-manager.ts`
10. `frontend/lib/harness/stream-parser.ts`
11. `frontend/lib/harness/logger.ts`
12. `frontend/lib/harness/env-filter.ts`
13. `frontend/lib/harness/index.ts`

Then start coding immediately unless blocked.

Scope for this run:
Primary goal: implement automated validation for Section 8 and make it repeatable for pre-merge use.
- Add an executable validation script under `frontend/scripts/` that runs the Section 8 matrix end-to-end:
  - smoke stream (`chat:delta` -> `chat:complete` -> `process:exit`),
  - session init persistence and resume (`--resume`) behavior,
  - permission behavior under `dontAsk` (unapproved denied; explicitly approved proceeds),
  - interrupt behavior (`SIGINT` path),
  - parse robustness via malformed NDJSON injection (mocked `claude` binary),
  - `/api/chat` reachability regression check.
- Script should produce machine-readable pass/fail output and preserve raw artifacts (SSE/log snippets) in a deterministic temp folder.
- Document script usage and expected outputs in `frontend/docs/harness/harness_manual_validation.md`.
- If needed, add a short “Validation automation” section in `frontend/README.md` linking to the script.

Target files:
- `frontend/scripts/` (new validation script)
- `frontend/docs/harness/harness_manual_validation.md`
- `frontend/README.md` (only if script usage guidance is added)
- Any minimal harness files needed to support deterministic validation (only if required)

Hard constraints:
- Keep Assignment A + B + C behavior intact.
- Keep `/api/chat` route available (already deprecated; no removal).
- Preserve session CRUD behavior and filesystem persistence under `.chirality/sessions/{id}.json`.
- `system/init.session_id` remains authoritative for `claudeSessionId`.
- Never leak secrets in logs or API responses.
- One in-flight turn per session remains enforced (409 conflict).
- Do not weaken tool-permission safety to make tests pass.

Validation before finishing:
1. Lint/typecheck on touched files.
2. Run the new automated validation script and capture its summary output.
3. Confirm Section 8 evidence is updated in docs (commands + observed output + pass/fail).
4. Regression checks:
   - Harness session CRUD + turn + interrupt paths still working.
   - `/api/chat` still reachable.

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
