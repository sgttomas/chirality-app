# Chirality Harness Validation (Automated)

Date: 2026-02-08

Project root: `/Users/ryan/ai-env/projects/chirality-app`

Validation script: `frontend/scripts/validate-harness-section8.mjs`
Pre-merge wrapper: `frontend/scripts/validate-harness-premerge.mjs`
CI workflow: `.github/workflows/harness-premerge.yml`

## Prerequisites

- Harness server reachable at `HARNESS_BASE_URL` (default `http://127.0.0.1:3000`)
- Claude CLI installed and available on `PATH`
- `ANTHROPIC_API_KEY` available in the process environment (or injected as CI secret)

Quick checks:

```bash
which claude
claude --version
echo "${ANTHROPIC_API_KEY:+set}"
```

## Usage

Canonical local pre-merge sequence:

1. Start frontend server:

```bash
cd frontend
npm run dev -- --hostname 127.0.0.1 --port 3000
```

2. Run pre-merge wrapper in a separate shell:

```bash
cd frontend
npm run harness:validate:premerge
```

3. Collect stable summary artifact:

`frontend/artifacts/harness/section8/latest/summary.json`

Direct Section 8 run (without stable artifact copy):

```bash
cd frontend
./scripts/validate-harness-section8.mjs
```

CI/pre-merge command:

```bash
cd frontend
npm run harness:validate:premerge
```

Optional environment overrides:

- `HARNESS_BASE_URL` (default: `http://127.0.0.1:3000`)
- `HARNESS_VALIDATION_ARTIFACT_ROOT` (default: `${TMPDIR:-/tmp}/chirality-harness-validation`)
- `HARNESS_REQUEST_TIMEOUT_MS` (default: `180000`)
- `HARNESS_PREMERGE_ARTIFACT_DIR` (default: `frontend/artifacts/harness/section8/latest`)

## Machine-Readable Outputs

- Script stdout includes:
  - `HARNESS_VALIDATION_SUMMARY_PATH=<path>`
  - `HARNESS_VALIDATION_STATUS=pass|fail`
- `HARNESS_PREMERGE_ARTIFACT_PATH=<stable-path>` (wrapper command)
- JSON summary is written to:
  - `${TMPDIR:-/tmp}/chirality-harness-validation/latest/summary.json`
  - `frontend/artifacts/harness/section8/latest/summary.json` (stable CI artifact path via wrapper)

CI upload target path:

- `frontend/artifacts/harness/section8/latest/summary.json`

Run captured in this session:

- `HARNESS_VALIDATION_STATUS=pass`
- `HARNESS_VALIDATION_SUMMARY_PATH=/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-harness-validation/latest/summary.json`
- `HARNESS_PREMERGE_STATUS=pass`
- `HARNESS_PREMERGE_ARTIFACT_PATH=/Users/ryan/ai-env/projects/chirality-app/frontend/artifacts/harness/section8/latest/summary.json`

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

Guidance on when to mirror full artifacts to stable CI paths:

- `frontend/docs/harness/harness_artifact_mirroring_guidance.md`
- `frontend/docs/harness/harness_ci_integration.md`

## Common Failures and Fixes

- `fetch failed`
  - Cause: server not running or not reachable at `HARNESS_BASE_URL`.
  - Fix: start server on `http://127.0.0.1:3000` or set `HARNESS_BASE_URL` to a reachable URL.
- Missing auth/key errors
  - Cause: `ANTHROPIC_API_KEY` not present in runtime/CI environment.
  - Fix: export key in shell running server/validator, or configure CI secret `ANTHROPIC_API_KEY`.
- Missing summary artifact after run
  - Cause: wrapper failed before publish, or summary generation failed.
  - Fix: check wrapper output for `HARNESS_VALIDATION_STATUS` and verify both:
    - `${TMPDIR:-/tmp}/chirality-harness-validation/latest/summary.json`
    - `frontend/artifacts/harness/section8/latest/summary.json`

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
