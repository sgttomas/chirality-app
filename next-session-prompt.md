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
Primary goal: add a CI/pre-merge wrapper target for harness validation and publish machine-readable artifacts.
- Keep using `frontend/scripts/validate-harness-section8.mjs` as the canonical Section 8 runner.
- Add a wrapper target/command that:
  - runs Section 8 automation non-interactively for pre-merge use,
  - exits non-zero on validation failure,
  - persists `summary.json` to a stable artifact path suitable for CI collection (not only temp output),
  - prints the final artifact location clearly in stdout.
- Update docs so operators can run the pre-merge command and know exactly which artifact file to upload/archive.
- Do not regress existing harness behavior while adding wrapper/packaging logic.

Target files:
- `frontend/package.json` (add pre-merge validation target if needed)
- `frontend/scripts/` (wrapper script and/or artifact publish helper)
- `frontend/docs/harness/harness_manual_validation.md`
- `frontend/README.md`
- Any minimal harness files needed to support CI-safe artifact publishing (only if required)

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
2. Run the new pre-merge wrapper target end-to-end and capture its summary/artifact output.
3. Confirm docs reflect the wrapper command and stable artifact path.
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
