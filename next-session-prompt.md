You are the implementation agent for Chirality Agent Harness v0.5 in:
`/Users/ryan/ai-env/projects/chirality-app`

Follow `AGENT_HARNESS_SPEC-v2-3.md` as the source of truth.

Read in this order:
1. `frontend/AGENT_HARNESS_SESSION_LOG.md` (latest entry first)
2. `frontend/AGENT_HARNESS_DECISIONS.md`
3. `frontend/AGENT_HARNESS_IMPLEMENTATION_CHECKLIST.md`
4. `AGENT_HARNESS_SPEC-v2-3.md`
5. `frontend/docs/harness/harness_manual_validation.md`
6. `frontend/docs/harness/harness_artifact_mirroring_guidance.md`
7. `frontend/README.md`
8. `frontend/package.json`
9. `.gitignore` (repo root)
10. `frontend/.gitignore`
11. `frontend/scripts/validate-harness-section8.mjs`
12. `frontend/scripts/validate-harness-premerge.mjs`
13. `frontend/app/api/chat/route.ts`
14. `frontend/app/api/harness/turn/route.ts`
15. `frontend/lib/harness/claude-code-manager.ts`
16. `frontend/lib/harness/logger.ts`

Then start coding immediately unless blocked.

Scope for this run:
Primary goal: complete operational hardening updates for pre-merge harness validation across three areas:
1) runtime artifact ignore hygiene,
2) CI/pre-merge pipeline wiring,
3) prerequisite/runbook documentation clarity.

Keep using `frontend/scripts/validate-harness-section8.mjs` as canonical Section 8 logic and `frontend/scripts/validate-harness-premerge.mjs` as wrapper entrypoint.

## Detailed implementation instructions

### A) Root ignore hygiene (`.gitignore`) for runtime harness churn

Problem:
- Runtime harness files under `.chirality/` are currently polluting `git status` during validation runs.

Required updates:
- Update repo-root `.gitignore` (not only `frontend/.gitignore`) to ignore runtime-generated harness artifacts:
  - `.chirality/logs/`
  - `.chirality/prompts/`
  - `.chirality/sessions/`

Rules:
- Do not ignore the entire `.chirality/` directory; keep scope precise to runtime outputs.
- Do not delete local runtime files.
- If any of those files are currently tracked, untrack safely (`git rm --cached ...`) without deleting working copies.

Acceptance criteria:
- After running validation, `git status --short` no longer includes `.chirality/logs/*`, `.chirality/prompts/*`, or `.chirality/sessions/*` changes/new files.

### B) CI/pre-merge pipeline wiring for wrapper command + artifact upload

Goal:
- Ensure pre-merge automation is actually runnable in CI, not only manually.

Required updates:
- Add CI wiring that runs:
  - `npm run harness:validate:premerge` from `frontend/`
- Ensure CI archives/uploads:
  - `frontend/artifacts/harness/section8/latest/summary.json`

Implementation guidance:
- First detect existing CI provider/config in repo.
- If none exists, add a minimal CI config with explicit pre-merge job (prefer `.github/workflows/harness-premerge.yml` unless repo clearly uses another provider).
- Job should include, at minimum:
  1. checkout
  2. Node setup (project-compatible version)
  3. install deps (`cd frontend && npm ci`)
  4. start frontend server reachable at `HARNESS_BASE_URL` (default `http://127.0.0.1:3000`)
  5. wait/poll for readiness (`/api/harness/session/list?...`)
  6. run wrapper target (`npm run harness:validate:premerge`)
  7. upload `frontend/artifacts/harness/section8/latest/summary.json` as job artifact
- Fail the job if:
  - wrapper exits non-zero,
  - or summary artifact is missing.

Security and runtime constraints:
- Do not commit secrets.
- Use CI secret injection for `ANTHROPIC_API_KEY` if required by environment.
- Do not weaken permission/tool safety.

Acceptance criteria:
- CI config clearly invokes the wrapper and uploads the stable summary artifact.
- Paths in pipeline match actual repo layout exactly.

### C) Prerequisite/runbook documentation clarity

Goal:
- Prevent operator confusion about why validation fails (`fetch failed`, missing server, missing auth/env).

Required docs updates:
- `frontend/README.md`
- `frontend/docs/harness/harness_manual_validation.md`
- Add or update any CI-specific harness doc file if needed (for example `frontend/docs/harness/harness_ci_integration.md`).

Must document explicitly:
- Pre-merge validation requires harness server reachable at `HARNESS_BASE_URL` (default `http://127.0.0.1:3000`).
- Required runtime prerequisites:
  - Claude CLI installed and on `PATH`
  - `ANTHROPIC_API_KEY` available in process/CI environment
- Canonical local run sequence:
  1. start server
  2. run `npm run harness:validate:premerge`
  3. collect `frontend/artifacts/harness/section8/latest/summary.json`
- Common failure modes and fixes:
  - `fetch failed` (server not running/reachable)
  - auth/key missing
  - missing artifact path after run

Acceptance criteria:
- Docs contain exact command examples and exact artifact path.
- Docs align with actual wrapper behavior and env names.

Target files (minimum expected):
- `.gitignore`
- `frontend/README.md`
- `frontend/docs/harness/harness_manual_validation.md`
- CI config file(s) for repo provider (`.github/workflows/*` or equivalent)
- Optional CI-specific harness doc (only if useful and concise)
- Any minimal support files required by CI wiring

Hard constraints:
- Keep Assignment A + B + C behavior intact.
- Keep `/api/chat` route available (already deprecated; no removal).
- Preserve session CRUD behavior and filesystem persistence under `.chirality/sessions/{id}.json`.
- `system/init.session_id` remains authoritative for `claudeSessionId`.
- Never leak secrets in logs, docs examples, or API responses.
- One in-flight turn per session remains enforced (409 conflict).
- Do not weaken tool-permission safety to make tests pass.

Validation before finishing:
1. Lint/typecheck touched code/docs-supporting scripts.
2. Run `npm run harness:validate:premerge` end-to-end and capture stdout status lines.
3. Confirm stable artifact exists at:
   - `frontend/artifacts/harness/section8/latest/summary.json`
4. Confirm docs reflect:
   - server reachability prerequisite,
   - required env/auth,
   - exact wrapper command,
   - exact artifact upload/archive path.
5. Confirm root ignore hygiene:
   - `.chirality/logs/*`, `.chirality/prompts/*`, `.chirality/sessions/*` no longer clutter `git status`.
6. Regression checks:
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
