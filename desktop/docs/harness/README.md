# Harness Validation Suite

> **D-GOV-43 (A2) note, 2026-09-12:** Codex is the only engine. The adapter
> boundary is the Runtime service's Unix-socket API; the App starts, owns and
> stops that service as a child process, and the service owns the stock,
> lockfile-pinned `codex app-server`. The renderer channel is loopback HTTP
> and SSE through the in-process Next server. The browser stream carries an
> extensible representation that preserves upstream method names, identifiers
> and payloads with normalized views for known items; the former eight-name
> `UIEvent` set is compatibility history. A closed stream never interrupts a
> turn; explicit Stop is the interrupt. The `agentsdk-*` scripts and the
> Anthropic network proof below are Claude-path compatibility history and are
> not MVP evidence.

This suite validates the harness runtime contract for session lifecycle, turn execution, SSE streaming, options fallback resolution, subagent governance gates, and attachment behavior.

## Scripts

- `npm run harness:validate:section8`
  - Executes `frontend/scripts/validate-harness-section8.mjs`.
  - Emits machine-readable lines:
    - `HARNESS_VALIDATION_SUMMARY_PATH=<path>`
    - `HARNESS_VALIDATION_STATUS=pass|fail`
- `npm run harness:validate:section9`
  - Executes `frontend/scripts/validate-harness-section9.mjs`.
  - Runs the current Section 9 deterministic ID groups against targeted Vitest files.
  - Emits machine-readable lines:
    - `HARNESS_SECTION9_SUMMARY_PATH=<path>`
    - `HARNESS_SECTION9_STATUS=pass|fail`
- `npm run harness:validate:premerge`
  - Executes the section8 validator and enforces required test IDs.
  - Executes the section9 validator in report-only mode for the initial integration cycle.
  - Copies the summary to `frontend/artifacts/harness/section8/latest/summary.json`.
- `npm run harness:validate:agentsdk-packaged-proof`
  - Imports the packaged SDK module from `app.asar.unpacked`.
  - Runs a scripted no-live `query()` turn to record the resolved native subprocess command.
  - Verifies controlled `CLAUDE_CONFIG_DIR` and `HOME` propagation for transcript/config posture.
  - Defaults to `frontend/dist/mac-arm64/Chirality.app/Contents/Resources`; use `--bundle-root` and
    `--output-root` for mounted-DMG package-content evidence.
- `npm run validate:release-quality`
  - Runs the runtime-premerge evidence wrapper: full Vitest, typecheck, standalone Section 9, and premerge unless premerge is explicitly skipped with reason.
  - Writes `frontend/artifacts/harness/release-quality/latest/summary.json`.
  - Records Section 9 as standalone-blocking for the wrapper while preserving premerge Section 9 as report-only.
- `npm run proof:secret-scan`
  - Scans tracked app-dev files and generated harness evidence for high-confidence secret material.
  - Writes `frontend/artifacts/harness/security/latest/secret-scan-summary.json` without raw secret values.
- `npm run proof:network-policy`
  - Runs the current network-policy proof for loopback plus Anthropic outbound posture.
  - Use `-- --provider agentSdk --scripted-agent-sdk` for the offline scripted Agent SDK proof path.

## Prerequisites

- Node.js `>=22.19.0`
- Frontend dependencies installed in `frontend/`
- Harness API reachable at `HARNESS_BASE_URL` (defaults to `http://127.0.0.1:3000`)
- Valid working root configured via `HARNESS_PROJECT_ROOT` (recommended: `examples/example-project`)
- If `HARNESS_PROJECT_ROOT` points inside instruction root (for example `examples/example-project`), the section8 validator auto-stages it to a temp external workroot to satisfy `WORKING_ROOT_CONFLICT` policy.

## Local Run

From `frontend/`:

```bash
npm run harness:validate:section8
npm run harness:validate:section9
npm run harness:validate:premerge
npm run validate:release-quality
npm run proof:secret-scan
npm run proof:network-policy
```

Optional environment overrides:

```bash
HARNESS_BASE_URL=http://127.0.0.1:3000 \
HARNESS_PROJECT_ROOT=/absolute/path/to/project-root \
npm run harness:validate:premerge
```

## CI Integration

Run in a headless step after the harness API surface is available:

```bash
cd frontend
npm ci
HARNESS_BASE_URL=http://127.0.0.1:3000 \
HARNESS_PROJECT_ROOT=$GITHUB_WORKSPACE/examples/example-project \
npm run harness:validate:premerge
```

Fail the pipeline when command exit code is non-zero.

## Artifacts

- Live run outputs: `${TMPDIR:-/tmp}/chirality-harness-validation/latest/`
- Section 9 live run outputs: `${TMPDIR:-/tmp}/chirality-harness-section9-validation/latest/`
- Stable premerge summary: `frontend/artifacts/harness/section8/latest/summary.json`
- Stable Section 9 summary: `frontend/artifacts/harness/section9/latest/summary.json`
- Release-quality wrapper summary: `frontend/artifacts/harness/release-quality/latest/summary.json`
- Integrity summary (instruction-root): `frontend/artifacts/harness/instruction-root-integrity/latest/summary.json`
- Packaged SDK proof summary: `frontend/artifacts/harness/packaged-agent-sdk/latest/summary.json`
- Secret-scan summary: `frontend/artifacts/harness/security/latest/secret-scan-summary.json`
- Network-policy proof summaries: `frontend/artifacts/harness/network-policy/`

## Repeatability Check

Run `npm run harness:validate:premerge` twice against the same harness state and confirm:

- both runs exit `0`
- both summaries report `"status": "pass"`
- required test IDs are unchanged
