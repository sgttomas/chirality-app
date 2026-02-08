# Harness CI Integration (SDK Runtime)

Scope: pre-merge harness validation in CI.

## Canonical Workflow

- Workflow file: `.github/workflows/harness-premerge.yml`
- CI command: `cd frontend && npm run harness:validate:premerge`
- Uploaded artifact:
  - `frontend/artifacts/harness/section8/latest/summary.json`

## CI Prerequisites

- `HARNESS_BASE_URL` reachable by the job (default `http://127.0.0.1:3000`)
- Anthropic auth injected in runtime env (for example `ANTHROPIC_API_KEY`)

## Job Flow

1. Checkout repository
2. Setup Node.js
3. `cd frontend && npm ci`
4. Start frontend server
5. Poll readiness at `/api/harness/session/list?projectRoot=...`
6. Run `npm run harness:validate:premerge`
7. Wrapper validates Section8 summary schema:
   - required SDK test IDs are present
   - legacy `regression.api_chat_reachability` is absent
8. Verify summary exists at `frontend/artifacts/harness/section8/latest/summary.json`
9. Upload summary artifact

## Failure Expectations

- Wrapper exits non-zero: job fails.
- Missing stable summary artifact: job fails.
- Invalid summary shape or missing required SDK test IDs: job fails.
