# Chirality Harness Validation (Automated)

Date: 2026-02-07

Project root: `/Users/ryan/ai-env/projects/chirality-app`

Validation script: `frontend/scripts/validate-harness-section8.mjs`

## Usage

```bash
cd frontend
./scripts/validate-harness-section8.mjs
```

Optional environment overrides:

- `HARNESS_BASE_URL` (default: `http://127.0.0.1:3000`)
- `HARNESS_VALIDATION_ARTIFACT_ROOT` (default: `${TMPDIR:-/tmp}/chirality-harness-validation`)
- `HARNESS_REQUEST_TIMEOUT_MS` (default: `180000`)

## Machine-Readable Outputs

- Script stdout includes:
  - `HARNESS_VALIDATION_SUMMARY_PATH=<path>`
  - `HARNESS_VALIDATION_STATUS=pass|fail`
- JSON summary is written to:
  - `${TMPDIR:-/tmp}/chirality-harness-validation/latest/summary.json`

Run captured in this session:

- `HARNESS_VALIDATION_STATUS=pass`
- `HARNESS_VALIDATION_SUMMARY_PATH=/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-harness-validation/latest/summary.json`

## Artifact Layout

Deterministic artifact folder:

- `${TMPDIR:-/tmp}/chirality-harness-validation/latest/`

Key files produced:

- `summary.json` (full machine-readable result)
- `sse/*.sse` (raw SSE for each turn)
- `api/*.json` (route response captures)
- `logs/*.json` (log snippets used for assertions)
- `mock/bin/claude` (mocked binary used for malformed NDJSON test)
- `cleanup/sessions.json` (best-effort session cleanup report)

## Section 8 Matrix (Automated Evidence)

| Check | Command path | Observed output | Result |
| --- | --- | --- | --- |
| Smoke stream (`chat:delta -> chat:complete -> process:exit`) | `./scripts/validate-harness-section8.mjs` | `turn-smoke.sse` events: `session:init`, `chat:delta`, `chat:delta`, `chat:complete`, `session:complete`, `process:exit` | PASS |
| Session init persistence + resume (`--resume`) | same | Session API + file persisted `claudeSessionId=bc3dbc58-f6ee-4237-877b-8d2943c6da13`; `logs/resume-spawn-snippets.json` contains spawn command with `--resume`; second turn completed with `chat:complete` + `process:exit` | PASS |
| Permissions under `dontAsk` (deny + allow) | same | Deny case (`tools=Read`) emitted unavailable `Bash` tool error and exited; allow case (`tools=Bash`, `autoApproveTools=["Bash(echo *)"]`) emitted tool result containing `UNAPPROVED_ALLOW_TEST` | PASS |
| Interrupt behavior (`SIGINT` path handling) | same | `POST /api/harness/interrupt` returned `200 {"ok":true}`; turn emitted `session:error` and terminal `process:exit` (interruption without result) | PASS |
| Parse robustness (malformed NDJSON via mocked `claude`) | same | Turn run with `opts.claudeExecutable` pointing to `mock/bin/claude`; `logs/mock-parse-errors.json` recorded one `parse:error` for `MALFORMED_LINE_FOR_PARSE_TEST`; stream still reached `chat:complete` + `process:exit` | PASS |
| `/api/chat` reachability regression | same | `POST /api/chat` returned `401` with `{"error":"API Key required"}` (route still reachable) | PASS |

## Additional Regression Checks Included by Script

- Session CRUD (`create/list/get/delete`) under `/api/harness/session/*`
- Turn path end-to-end under `/api/harness/turn`
- Interrupt endpoint behavior under `/api/harness/interrupt`

All checks above were `PASS` in the captured run (`summary.status = "pass"`).
