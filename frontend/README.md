# Chirality Frontend + Harness Runtime

This frontend uses the Chirality Harness (`/api/harness/*`) backed by the Anthropic Agent SDK (`query()`) to run turns and stream events to the UI.

## Runtime Requirements

- Node.js + npm (project uses Next.js 16)
- Anthropic authentication available to the server process (for example `ANTHROPIC_API_KEY`)
- For pre-merge harness validation, frontend server reachable at `HARNESS_BASE_URL` (default `http://127.0.0.1:3000`)
- App instruction bundle root resolvable (default autodetect; override with `CHIRALITY_INSTRUCTION_ROOT`)

Example:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
npm run dev
```

## Start the App

```bash
npm run dev
```

Open `http://localhost:3000`.

## Runtime Root Model

- `projectRoot`: user-selected working root (`cwd`) where agents execute and where `.chirality/*` runtime state is written.
- `instructionRoot`: fixed release-managed instruction bundle (`AGENTS.md`, `README.md`, `agents/*`, `CLAUDE.md`).
- Harness persona loading, boot fingerprinting, and global model lookup read from `instructionRoot`.

## Subagent Delegation (Phase 1)

- Feature flag: `CHIRALITY_ENABLE_SUBAGENTS`
  - Delegation is disabled unless this is exactly `"true"` in the server environment.
- Initial Type 1 allowlist:
  - `ORCHESTRATOR`
  - `RECONCILIATION`
- Required turn-level governance token when delegation is enabled:
  - `opts.subagentGovernance.contextSealed === true`
  - `opts.subagentGovernance.pipelineRunApproved === true`
  - `opts.subagentGovernance.approvalRef` is a non-empty string
  - `opts.subagentGovernance.approvedBy` is optional
- Fail-closed behavior:
  - Missing/invalid governance token does not fail the turn.
  - The turn continues without subagent injection.

## Toolkit Panel (Operator)

Current behavior:

- A collapsible Toolkit panel in chat exposes per-turn controls (for example model, max turns, tool policy, include-partials, and governance token fields).
- Zero-impact default is preserved: when no Toolkit overrides are active, effective runtime behavior matches the default path.
- Delegation governance inputs are visible for operator workflows, but runtime gate enforcement remains authoritative.
  - Invalid/missing governance metadata continues to block delegation while allowing the parent turn.

Operator preference storage:

- Toolkit UI state/presets may be stored in browser localStorage for convenience.
- localStorage preferences are non-authoritative and MUST NOT be treated as project execution truth.

## Desktop Packaging (Installers)

Build outputs:
- macOS: `.dmg`
- Windows: `.exe` (NSIS)

Commands:

```bash
cd frontend
npm install
npm run desktop:dist
```

Packaging notes:
- `desktop:dist` runs `next build` before `electron-builder`.
- `instructionRoot` files are bundled into `resources/instruction-root`.
- End-user runtime remains filesystem-native (no database setup).

### Signing and Notarization Placeholders (Release Readiness)

The repo now includes placeholder config for release signing:
- macOS hardened runtime + entitlements: `electron/entitlements.mac.plist`
- macOS notarization hook: `electron/notarize.cjs` (runs after signing when env vars are present)
- Windows signing metadata placeholder: `build.win.publisherName` in `package.json` (replace before signed release)

Recommended release command:

```bash
cd frontend
npm run desktop:dist:release
```

Environment variables for signed/notarized releases:
- macOS code-signing: `CSC_LINK`, `CSC_KEY_PASSWORD`
- macOS notarization: `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID`
- Windows code-signing: `WIN_CSC_LINK`, `WIN_CSC_KEY_PASSWORD` (or `CSC_LINK`, `CSC_KEY_PASSWORD`)

Unsigned dev builds continue to work when these variables are not set.

GitHub Actions release template:
- Workflow file: `.github/workflows/desktop-release-template.yml`
- Trigger:
  - `push` tags matching `v*` (auto build + draft release publish)
  - `workflow_dispatch` (optional publish when `publish_release=true`)
- Secrets consumed by the workflow:
  - `CSC_LINK`, `CSC_KEY_PASSWORD`
  - `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID`
  - `WIN_CSC_LINK`, `WIN_CSC_KEY_PASSWORD`

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

2. In a separate shell, run toolkit validation and then the wrapper command:

```bash
cd frontend
npm run harness:validate:toolkit
npm run harness:validate:premerge
```

3. Collect the stable summary artifact:

`frontend/artifacts/harness/section8/latest/summary.json`

- The wrapper runs toolkit validation (`./scripts/validate-toolkit.mjs`) and then the canonical Section 8 validator (`./scripts/validate-harness-section8.mjs`) non-interactively.
- Canonical artifacts remain at `${TMPDIR:-/tmp}/chirality-harness-validation/latest`.
- Stable CI artifact is published at `frontend/artifacts/harness/section8/latest/summary.json`.
- Wrapper stdout prints `HARNESS_PREMERGE_ARTIFACT_PATH=<absolute-path>` for collection/upload steps.
- Full usage/details: `docs/harness/harness_manual_validation.md`.
- CI wiring details: `docs/harness/harness_ci_integration.md`.
- Mirroring strategy guidance: `docs/harness/harness_artifact_mirroring_guidance.md`.
- CI wiring: `.github/workflows/harness-premerge.yml` runs the same wrapper command and uploads `frontend/artifacts/harness/section8/latest/summary.json`.

## Troubleshooting

- `fetch failed` during `npm run harness:validate:premerge`:
  - The validator could not reach `HARNESS_BASE_URL`.
  - Confirm frontend server is running and reachable at `http://127.0.0.1:3000` (or set `HARNESS_BASE_URL` to the correct URL).
- `session:error` with missing key/auth issues:
  - Confirm `ANTHROPIC_API_KEY` is set in the same shell/process running `npm run dev` (or injected as a CI secret).
- Wrapper completed but artifact missing:
  - Validate `frontend/artifacts/harness/section8/latest/summary.json` exists.
  - If missing, the pre-merge wrapper should fail; inspect wrapper stdout/stderr for `Missing Section 8 summary artifact`.
- Turn appears blocked or tool calls fail in headless runs:
  - Check `opts.permissionMode` and tool policy (`tools`, `disallowedTools`, `autoApproveTools`).
  - In `dontAsk`, unapproved tools are denied by design.
- No stream output in client:
  - Verify `/api/harness/turn` response header is `text/event-stream` and no proxy is buffering.
- Need low-level diagnostics:
  - Inspect `.chirality/logs/harness.log` for `turn:start`, `turn:model`, `session:init`, `tool:start`, `tool:result`, `turn:complete`, `session:error`, and `process:exit` entries.
  - Subagent lifecycle telemetry is logged as:
    - `subagent:registry_applied`
    - `subagent:start`
    - `subagent:complete`
    - `subagent:interrupted`
    - `subagent:governance_blocked` (delegation attempt blocked by missing/invalid governance token)
