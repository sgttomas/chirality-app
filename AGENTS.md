# Repository Guidelines (v2.0.0)

Concise guide for contributors and AI coding agents working on chirality‑app. The app implements an 11‑station semantic valley pipeline with a default “foundation” traversal (S1–S5 + S11), canonical packet schema/exports, a minimal API/UI, and CI schema validation.

## Project Structure
- `src/app/`
  - `api/pipeline/traverse/route.ts` — POST traversal
  - `api/export/run/route.ts` — GET export metadata
  - `api/export/file/route.ts` — GET export file download (run.json, packets.jsonl)
  - `page.tsx` — UI entry
- `src/components/` — `TraversalInterface`, `ProblemForm`, `StationDisplay`, `ModalityChip`, `ResultsDisplay`
- `src/core/` — `orchestrator.ts`, `state.ts`, `exporter.ts`, `llm/service.ts`, `stations/`
- `src/domain/` — station metadata/types, validators
- `schemas/packet.json` — canonical Packet schema (validated in CI)
- `docs/` — see `docs/INDEX.md` for the v2 table of contents

Legacy/optional:
- `lib/framework/*` matrix utilities (optional); graph/Neo4j docs are archived

## Build, Test, Dev
- `npm run dev` — dev server (Turbopack)
- `npm run build` — production build; `npm start` — serve
- `npm run lint` — ESLint; `npm run type-check` — TypeScript
- `npm test` — Jest unit tests (schema/validators/API)

Tip: legacy scripts in `package.json` that reference chat/graph are not used in v2.

## Environment
- `OPENAI_MODEL` — single source of truth for model selection (recommended: `gpt-4.1-nano`)
- `OPENAI_API_KEY` — optional for foundation mode (fallbacks); required for full mode

## API Contracts (canonical)
- POST `/api/pipeline/traverse` — body `{ problem: { title, statement }, options?: { mode: 'foundation'|'full' } }`
- GET `/api/export/run?runId=...` — export metadata
- GET `/api/export/file?runId=...&name=run.json|packets.jsonl` — file download
- Errors: `{ code: 'ERR_*', message, details? }`

## Packets & Exports
- Exports written to `runs/<runId>/run.json` and `runs/<runId>/packets.jsonl`
- Validate with AJV locally (see README/TROUBLESHOOTING) and in CI

## Coding Style
- TypeScript strict; ESLint enforced
- Components: `PascalCase`; hooks `useX`
- Names: variables/functions `camelCase`; types/interfaces `PascalCase`; constants `SCREAMING_SNAKE_CASE`
- Use path aliases where defined

## Testing Guidelines
- Prioritize tests for: validators (transition/deps), schema compliance (AJV), API endpoints
- When adding station logic: keep stations pure/idempotent; expand schema tests if payloads change

## Commit & PR Guidelines
- Commits: Conventional Commits format `type(scope): short summary`
- PRs: clear problem/solution, testing evidence (logs/screens), updated docs for user-visible changes

## Do / Don’t (important)
- Do:
  - Use foundation mode defaults unless full mode is required
  - Keep `OPENAI_MODEL` env the only source of model selection
  - Validate exports against `schemas/packet.json`
  - Keep dependency validation aligned with implemented stations
- Don’t:
  - Reintroduce legacy endpoints (`/api/chat/*`, `/api/agent/*`) or S0–S8 model
  - Hardcode model names in code; use env vars
  - Add graph/Neo4j as a runtime dependency

## Roadmap Pointers
- Near‑term: S6–S10 logic, stricter schema station→operation mapping, dependency validator hard‑fail, UI export viewer
- Medium‑term: convergence criteria for full mode, optional matrix ingestion seeds, multi‑run management

Refer to `docs/INDEX.md`, `README.md`, and `ARCHITECTURE.md` for current behavior and design decisions. Avoid touching archived or legacy materials unless explicitly asked.
