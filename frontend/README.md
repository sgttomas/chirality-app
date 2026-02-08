# Chirality Frontend + Harness Runtime

This frontend uses the Chirality Harness (`/api/harness/*`) to run Claude Code turns and stream events to the UI.

## Runtime Requirements

- Node.js + npm (project uses Next.js 16)
- Claude Code CLI available on `PATH` (the server spawns `claude -p ...`)
- `ANTHROPIC_API_KEY` set in the server environment
- For pre-merge harness validation, frontend server reachable at `HARNESS_BASE_URL` (default `http://127.0.0.1:3000`)

Example:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
which claude
claude --version
npm run dev
```

## Start the App

```bash
npm run dev
```

Open `http://localhost:3000`.

## Harness API Routes

- `POST /api/harness/session/create`
  - Body: `{ "projectRoot": "/abs/path", "persona": "ORCHESTRATOR" | null, "mode": "workbench" | "pipeline" | "direct" }`
  - Returns: `201 { session }`
- `GET /api/harness/session/list?projectRoot=/abs/path`
  - Returns: `200 [SessionSummary]`
- `GET /api/harness/session/:id`
  - Returns: `200 { session }`
- `DELETE /api/harness/session/:id`
  - Returns: `204` (or `409` if a turn is currently in-flight)
- `POST /api/harness/turn`
  - Body: `{ "sessionId": "...", "message": "...", "opts": { ... } }`
  - Returns: `text/event-stream` with UI events (`session:init`, `chat:delta`, `chat:complete`, `tool:start`, `tool:result`, `session:complete`, `session:error`, `process:exit`)
- `POST /api/harness/interrupt`
  - Body: `{ "sessionId": "..." }`
  - Returns: `{ "ok": true }` when a run is active

## Validation Automation

Canonical local pre-merge run sequence:

1. Start the server (default binds to `http://127.0.0.1:3000`):

```bash
cd frontend
npm run dev -- --hostname 127.0.0.1 --port 3000
```

2. In a separate shell, run the wrapper command:

```bash
cd frontend
npm run harness:validate:premerge
```

3. Collect the stable summary artifact:

`frontend/artifacts/harness/section8/latest/summary.json`

- The wrapper runs the canonical Section 8 validator (`./scripts/validate-harness-section8.mjs`) non-interactively.
- Canonical artifacts remain at `${TMPDIR:-/tmp}/chirality-harness-validation/latest`.
- Stable CI artifact is published at `frontend/artifacts/harness/section8/latest/summary.json`.
- Wrapper stdout prints `HARNESS_PREMERGE_ARTIFACT_PATH=<absolute-path>` for collection/upload steps.
- Full usage/details: `docs/harness/harness_manual_validation.md`.
- CI wiring details: `docs/harness/harness_ci_integration.md`.
- Mirroring strategy guidance: `docs/harness/harness_artifact_mirroring_guidance.md`.
- CI wiring: `.github/workflows/harness-premerge.yml` runs the same wrapper command and uploads `frontend/artifacts/harness/section8/latest/summary.json`.

## Legacy Route

- `POST /api/chat` remains available for compatibility but is deprecated.
- New work should use harness routes only.

## Troubleshooting

- `fetch failed` during `npm run harness:validate:premerge`:
  - The validator could not reach `HARNESS_BASE_URL`.
  - Confirm frontend server is running and reachable at `http://127.0.0.1:3000` (or set `HARNESS_BASE_URL` to the correct URL).
- `session:error` with missing key/auth issues:
  - Confirm `ANTHROPIC_API_KEY` is set in the same shell/process running `npm run dev` (or injected as a CI secret).
- `spawn ENOENT` / no Claude execution:
  - Ensure Claude CLI is installed and on `PATH` (`which claude`).
- Wrapper completed but artifact missing:
  - Validate `frontend/artifacts/harness/section8/latest/summary.json` exists.
  - If missing, the pre-merge wrapper should fail; inspect wrapper stdout/stderr for `Missing Section 8 summary artifact`.
- Turn appears blocked or tool calls fail in headless runs:
  - Check `opts.permissionMode` and tool policy (`tools`, `disallowedTools`, `autoApproveTools`).
  - In `dontAsk`, unapproved tools are denied by design.
- No stream output in client:
  - Verify `/api/harness/turn` response header is `text/event-stream` and no proxy is buffering.
- Need low-level diagnostics:
  - Inspect `.chirality/logs/harness.log` for `process:spawn`, `parse:error`, `session:error`, and `process:exit` entries.
  - Inspect `.chirality/prompts/{sessionId}-system.txt` to replay a turn directly in Claude CLI.
