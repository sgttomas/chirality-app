# Repository Guidelines (v2.1.0)

Concise guide for contributors and AI coding agents working on chirality‑app. The app implements an 11‑station semantic valley pipeline with a default “foundation” traversal (S1–S5 + S11), canonical packet schema/exports, a minimal API/UI, and CI schema validation.

## Project Structure
- `src/app/`
  - `api/pipeline/traverse/route.ts` — POST traversal
  - `api/export/run/route.ts` — GET export metadata
  - `api/export/file/route.ts` — GET export file download (run.json, packets.jsonl)
  - `api/import/seeds/route.ts` — POST seed extraction (framework → app)
  - `page.tsx` — UI entry
- `src/components/` — `TraversalInterface`, `ProblemForm`, `StationDisplay`, `ModalityChip`, `ResultsDisplay`
- `src/core/` — `orchestrator.ts`, `state.ts`, `exporter.ts`, `llm/service.ts`, `stations/`
- `src/domain/` — station metadata/types, validators
- `schemas/packet.json` — canonical Packet schema (validated in CI)
- `docs/` — see `docs/INDEX.md` for the v2 table of contents

Legacy/optional:
- `lib/framework/*` matrix utilities (optional); `lib/seeds/*` (seed extractor/cache helpers);
  graph/Neo4j docs are archived

## Build, Test, Dev
- `npm run dev` — dev server (Turbopack)
- `npm run build` — production build; `npm start` — serve
- `npm run lint` — ESLint; `npm run type-check` — TypeScript
- `npm test` — Jest unit tests (schema/validators/API)

Tip: legacy scripts in `package.json` that reference chat/graph are not used in v2.

## Environment
- `OPENAI_MODEL` — single source of truth for model selection (recommended: `gpt-4.1-nano`)
- `OPENAI_API_KEY` — optional for foundation mode (fallbacks); required for full mode
- Seed extraction & UI:
  - `CHIRALITY_RUNS_DIR` — base directory for framework runs (default: `runs`)
  - `SEEDS_ENABLE_HEURISTICS` — enable text heuristics (default: false)
  - `SEEDS_VERIFY_CHECKSUMS` — verify checksums during ingestion (default: true)
  - `SEEDS_PERSIST` — persist cache to `runs/<runId>/seeds.json` (default: true)
  - `NEXT_PUBLIC_SEEDS_ENABLE` — show “Load Seeds” UI (default: false)

## API Contracts (canonical)
- POST `/api/pipeline/traverse` — body `{ problem: { title, statement }, options?: { mode: 'foundation'|'full' } }`
- GET `/api/export/run?runId=...` — export metadata
- GET `/api/export/file?runId=...&name=run.json|packets.jsonl` — file download
- POST `/api/import/seeds` — body `{ runId, options? }` → framework seeds (independent of exports)
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
- Include seeds importer tests: unsupported format, record-count mismatch (safe), checksum modes (warn/skip/fail), heuristics behavior, streaming performance; integration for `/api/import/seeds` (dev‑only fixtures)

## Commit & PR Guidelines
- Commits: Conventional Commits format `type(scope): short summary`
- PRs: clear problem/solution, testing evidence (logs/screens), updated docs for user-visible changes

## Do / Don’t (important)
- Do:
  - Use foundation mode defaults unless full mode is required
  - Keep `OPENAI_MODEL` env the only source of model selection
  - Validate exports against `schemas/packet.json`
  - Keep dependency validation aligned with implemented stations
  - Use `/api/import/seeds` for framework → app seeds; keep `/api/export/run` strict
- Don’t:
  - Reintroduce legacy endpoints (`/api/chat/*`, `/api/agent/*`) or S0–S8 model
  - Hardcode model names in code; use env vars
  - Add graph/Neo4j as a runtime dependency

## Roadmap Pointers
- Near‑term: S6–S10 logic, stricter schema station→operation mapping, dependency validator hard‑fail, UI export viewer
- Medium‑term: convergence criteria for full mode, optional matrix ingestion seeds, multi‑run management

Refer to `docs/INDEX.md`, `README.md`, and `ARCHITECTURE.md` for current behavior and design decisions. Avoid touching archived or legacy materials unless explicitly asked.
