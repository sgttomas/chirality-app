# Chirality Harness Validation (Automated, SDK Runtime)

Date: 2026-02-08

Project root: `/Users/ryan/ai-env/projects/chirality-app`

Validation script: `frontend/scripts/validate-harness-section8.mjs`
Pre-merge wrapper: `frontend/scripts/validate-harness-premerge.mjs`
CI workflow: `.github/workflows/harness-premerge.yml`

## Prerequisites

- Harness server reachable at `HARNESS_BASE_URL` (default `http://127.0.0.1:3000`)
- Anthropic authentication available to the server runtime (for example `ANTHROPIC_API_KEY`)

Quick checks:

```bash
echo "${ANTHROPIC_API_KEY:+set}"
curl -s "http://127.0.0.1:3000/api/harness/session/list?projectRoot=/tmp" >/dev/null
```

## Usage

Canonical local pre-merge sequence:

1. Start frontend server:

```bash
cd frontend
npm run dev -- --hostname 127.0.0.1 --port 3000
```

2. Run wrapper in a second shell:

```bash
cd frontend
npm run harness:validate:premerge
```

3. Read stable summary artifact:

`frontend/artifacts/harness/section8/latest/summary.json`

Direct canonical run (without stable artifact copy):

```bash
cd frontend
./scripts/validate-harness-section8.mjs
```

## Machine-Readable Outputs

- Section8 script stdout:
  - `HARNESS_VALIDATION_SUMMARY_PATH=<path>`
  - `HARNESS_VALIDATION_STATUS=pass|fail`
- Premerge wrapper stdout:
  - `HARNESS_PREMERGE_ARTIFACT_PATH=<stable-path>`
  - `HARNESS_PREMERGE_SOURCE_SUMMARY_PATH=<tmp-path>`
  - `HARNESS_PREMERGE_STATUS=pass|fail`
  - `HARNESS_PREMERGE_TEST_COUNT=<n>`

Summary locations:

- `${TMPDIR:-/tmp}/chirality-harness-validation/latest/summary.json`
- `frontend/artifacts/harness/section8/latest/summary.json`

## Artifact Layout

Deterministic artifact folder:

- `${TMPDIR:-/tmp}/chirality-harness-validation/latest/`

Key outputs:

- `summary.json`
- `sse/*.sse`
- `api/*.json`
- `logs/*.json`
- `cleanup/sessions.json`

## Section 8 Matrix (SDK-native)

| Check | Command path | Observed output | Result |
| --- | --- | --- | --- |
| Smoke stream ordering | `./scripts/validate-harness-section8.mjs` | `session:init`, `chat:delta`, `chat:complete`, `session:complete`, `process:exit` | PASS |
| Session persistence + resume continuity | same | session file/API persist `claudeSessionId`; resumed turn emits `session:init`; persisted value matches latest init | PASS |
| Permissions under `dontAsk` (deny + allow) | same | deny case does not execute unapproved Bash; allow case emits `tool:result` containing `UNAPPROVED_ALLOW_TEST` | PASS |
| Interrupt behavior | same | `/api/harness/interrupt` returns `200 {"ok":true}`; stream emits terminal `process:exit` with interruption marker | PASS |
| SDK-native stream handling (no NDJSON parser layer) | same | successful turn emits `chat:complete` + `process:exit`; no `parse:error` logs for the session | PASS |

## Additional Regression Checks in Script

- `setup.server_reachable`
- `regression.session_crud`
- `section8.smoke_stream`
- `section8.session_persistence_resume`
- `section8.permissions_dontask`
- `section8.interrupt_sigint`
- `section8.sdk_native_stream`
