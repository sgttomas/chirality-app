# Chirality Frontend + Harness Runtime

This frontend uses the Chirality Harness (`/api/harness/*`) to run Claude Code turns and stream events to the UI.

## Runtime Requirements

- Node.js + npm (project uses Next.js 16)
- Claude Code CLI available on `PATH` (the server spawns `claude -p ...`)
- `ANTHROPIC_API_KEY` set in the server environment

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

- Run Section 8 pre-merge validation with:

```bash
./scripts/validate-harness-section8.mjs
```

- The script writes deterministic artifacts to `${TMPDIR:-/tmp}/chirality-harness-validation/latest`.
- Machine-readable status is emitted in stdout and persisted at `${TMPDIR:-/tmp}/chirality-harness-validation/latest/summary.json`.
- Full usage/details: `docs/harness/harness_manual_validation.md`.

## Legacy Route

- `POST /api/chat` remains available for compatibility but is deprecated.
- New work should use harness routes only.

## Troubleshooting

- `session:error` with missing key/auth issues:
  - Confirm `ANTHROPIC_API_KEY` is set in the same shell/process running `npm run dev`.
- `spawn ENOENT` / no Claude execution:
  - Ensure Claude CLI is installed and on `PATH` (`which claude`).
- Turn appears blocked or tool calls fail in headless runs:
  - Check `opts.permissionMode` and tool policy (`tools`, `disallowedTools`, `autoApproveTools`).
  - In `dontAsk`, unapproved tools are denied by design.
- No stream output in client:
  - Verify `/api/harness/turn` response header is `text/event-stream` and no proxy is buffering.
- Need low-level diagnostics:
  - Inspect `.chirality/logs/harness.log` for `process:spawn`, `parse:error`, `session:error`, and `process:exit` entries.
  - Inspect `.chirality/prompts/{sessionId}-system.txt` to replay a turn directly in Claude CLI.
