# Repository Guidelines

Concise contributor guide for the Chirality AI App (Next.js + TypeScript) implementing three‑pass DS/SP/X/M generation with RAG chat and optional matrix integration.

## Project Structure & Module Organization
- `src/app/` Next.js App Router (pages, layout, API routes)
- `src/components/` UI and chat components; `src/hooks/` React hooks
- `src/chirality-core/` orchestration/state; `lib/` framework, generator, orchestrator
- `docs/` product docs; `__tests__/` Jest tests; `public/` assets; `config/`, `types/`

## Build, Test, and Development Commands
- `npm run dev` local dev (Turbopack). `npm run dev:webpack` to disable Turbopack
- `npm run build` build for production; `npm start` serve build
- `npm run lint` ESLint; `npm run type-check` TypeScript strict check
- `npm test` Jest unit tests; `npm run orchestrate:test` orchestration smoke
- `npm run env:check` validate required env; `npm run update-docs-index` refresh docs index

## Coding Style & Naming Conventions
- TypeScript strict (`tsconfig.json`); 2‑space indent; Prettier config in `.prettierrc`
- ESLint (`eslint-config-next`) enforced via `npm run lint`
- Components: `PascalCase` files (e.g., `ChatWindow.tsx`); hooks `useX`
- Variables/functions `camelCase`; types/interfaces `PascalCase`; constants `SCREAMING_SNAKE_CASE`
- Use path aliases: `@/*`, `@/lib/*`, `@/config/*`

## Testing Guidelines
- Framework: Jest + ts-jest. Tests live in `__tests__` or alongside as `*.test.ts(x)`
- Write tests for core logic, error paths, and matrix ingestion where applicable
- Run locally with `npm test`; ensure `npm run type-check` and `npm run lint` pass

## Commit & Pull Request Guidelines
- Commits: `type(scope): short summary` (Conventional Commits). Include Documentation Assessment flags when updating docs
- PRs must include: clear description, linked issues, testing evidence (logs/screens), and updated docs when user-facing behavior changes

## Security & Configuration Tips
- Configure via `.env.local` (required: `OPENAI_API_KEY`; optional: Neo4j vars, `RBAC_ENABLED=true`)
- For protected exports, pass `x-role: approver` header. Avoid committing secrets
