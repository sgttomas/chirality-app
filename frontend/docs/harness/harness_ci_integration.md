# Harness CI Integration

Scope: pre-merge harness validation in CI.

## Canonical Workflow

- Workflow file: `.github/workflows/harness-premerge.yml`
- Wrapper command executed in CI: `cd frontend && npm run harness:validate:premerge`
- Stable artifact uploaded by CI:
  - `frontend/artifacts/harness/section8/latest/summary.json`

## CI Prerequisites

- `HARNESS_BASE_URL` reachable by the job (default `http://127.0.0.1:3000`)
- Claude CLI installed and on `PATH`
- `ANTHROPIC_API_KEY` injected as CI secret (`secrets.ANTHROPIC_API_KEY`)

## Job Flow

1. Checkout repository
2. Setup Node.js
3. `cd frontend && npm ci`
4. Start frontend server
5. Poll readiness at `/api/harness/session/list?projectRoot=...`
6. Run `npm run harness:validate:premerge`
7. Verify summary exists at `frontend/artifacts/harness/section8/latest/summary.json`
8. Upload summary artifact

## Failure Expectations

- Wrapper exit non-zero: job fails.
- Missing stable summary artifact: job fails.
