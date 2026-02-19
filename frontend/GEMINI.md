# Chirality Command Center // Project Memory

## Current Snapshot (2026-02-19)

**Operational model:** Filesystem-as-state with a Next.js GUI over the Chirality Harness (`/api/harness/*`), backed by the Anthropic Agent SDK (`query()`). Electron infrastructure has been removed in favor of a pure Next.js web/local-server model.

This document replaces older assumptions and tracks the transition to a hardened engineering standard.

## 1) Technical Stack

- Frontend: Next.js 16 (App Router), React 19, Tailwind CSS v4.
- Runtime orchestration: `frontend/lib/harness/*` (`agent-sdk-manager`, `session-manager`, `persona-manager`).
- Core APIs:
  - `POST /api/harness/session/create`
  - `GET /api/harness/session/list`
  - `GET|DELETE /api/harness/session/:id`
  - `POST /api/harness/turn` (SSE)
  - `POST /api/harness/interrupt`
  - File/project utilities: `/api/fs`, `/api/fs/read`, `/api/system/list`, `/api/project/config`, `/api/project/deliverables`
- Design language: Neural/Glass UI, light/dark mode support, EB Garamond + JetBrains Mono.
- **Removed:** Electron desktop infrastructure (main, preload, icons) removed for architectural simplicity.

## 2) Persistence Model

- Harness session records: `<projectRoot>/.chirality/sessions/<sessionId>.json`.
- Harness logs: `<projectRoot>/.chirality/logs/harness.log` (rotated).
- Browser storage:
  - `sessionStorage["chirality_project_root"]` for shared project root.
  - `localStorage["anthropic_api_key"]` for API key.
  - `localStorage["sessions_<viewId>"]` for local chat transcript/session UI state.

## 3) UX Modes

- **Portal (home):** Hex-grid navigation + deliverables dashboard.
- **Workbench:** Persona-driven interactive mode.
- **Pipeline:** Task-family/variant-driven mode.
- **Direct Link:** Raw direct mode (`mode="direct"`).
- Shared shell: `ResizableLayout` centralizes global footer actions, including root-directory selection.

## 4) Harness Contract Notes

- UI turn streaming depends on stable SSE `UIEvent` types:
  - `session:init`, `chat:delta`, `chat:complete`, `tool:start`, `tool:result`, `session:complete`, `session:error`, `process:exit`.
- **Subagent Injection:** Harness now supports subagent definitions injected into the SDK `query()` options.
- **Task Tool Enforcement:** When subagents are present, the `Task` tool is automatically enabled and auto-approved to allow the model to delegate work.
- `POST /api/harness/interrupt` interrupts active SDK turns and is reflected through terminal events.
- Chat UX direction is status-text-first (compact tool/in-flight feedback).

## 5) UI Polish Status

Source of truth: `frontend/docs/ui/UI_POLISH_EXECUTION_PLAN.md` (cosmetic pass notes dated 2026-02-08).

Completed slices:

1. Slice #1 (`globals.css` foundation + reusable classes) - `878872d`
2. Slice #2 (`page.tsx` shell + shared root-selector polish in `ResizableLayout.tsx`) - `ddfc3ab`, `474a023`
3. Slice #3 (`DashboardList.tsx` hierarchy/loading-empty/root-context polish) - `db3cb4f`
4. Slice #4 (`ChatPanel.tsx` status language/readability/in-flight polish) - `dd26440`
5. Slice #5 (file/system/utility component polish) - `e451e43`
6. Slice #6 (accessibility + responsive + hydration sanity pass) - `9093679`

## 6) Engineering Standards & Governance

A new `docs/` directory defines professional engineering standards for the project:

- `CONTRACT.md`: Authoritative catalog of project invariants.
- `SPEC.md`: Physical filesystem structures, schemas, and lifecycle states.
- `DIRECTIVE.md`: Workflow and behavioral mandates.
- `PLAN.md` & `TYPES.md`: Strategic and classification frameworks.

## 7) Agent Instruction Standard

All `AGENT_*.md` files have been updated to a standardized metadata format:

- **Metadata Headers:** YAML-like block with `description`.
- **Classification:** Explicit `AGENT_TYPE` (0, 1, 2) and `AGENT_CLASS` (Persona/Task).
- **Hardened Schemas:** New agents like `AGENT_ESTIMATE_PREP` (Type 2) follow strict CSV schema families (1-9) as defined in `docs/SPEC.md`.

## 8) Validation Baseline

Current baseline checks:

- `npm run lint` (frontend) - pass
- `npx tsc --noEmit` (frontend) - pass
- `npm run harness:validate:premerge` (frontend) - pass (9/9)

Notes:

- In network-restricted environments, `npm run build` may fail fetching Google Fonts (`EB Garamond`, `JetBrains Mono`).
- `frontend/app/api/fs/read/route.ts` can emit Turbopack broad-pattern warnings due to unrestricted path resolution design.
