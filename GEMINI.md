# Gemini Context: Chirality AI App

This document provides a comprehensive overview of the Chirality AI App project, reflecting the new post-refactor architecture. It is intended to guide future AI-driven development and analysis.

## Project Overview

Chirality AI is a Next.js application that transforms complex problems into structured solutions through a **canonical semantic valley traversal**. This architecture replaces the legacy three-pass (V1/V2/V3) system.

The core of the application is a **eleven-station pipeline (S1-S11)** that follows a specific ontological path: `{problem} → Systematic → Process → Epistemic → Process → Epistemic → Alethic → Epistemic → Alethic → {resolution}`. This ensures the codebase is a lean and explicit reflection of its philosophical purpose.

- **Data Structures:** The primary data structure for generated content is the **`Packet`**, an evolution of the legacy `Triple`. It provides a flexible container for document text, contextual metadata, and risk flags.
- **Orchestration:** All orchestration logic is now centralized in `src/core/orchestrator.ts`.
- **Data Ingestion:** A normalization layer at the ingestion boundary (`lib/framework/normalizeMatrix.ts`) handles inconsistencies from the upstream `chirality-framework`, ensuring internal data integrity.

**Key Technologies:**
- **Frontend:** Next.js 15, React 18, TypeScript, Tailwind CSS
- **Backend:** Next.js API Routes (Node.js)
- **AI:** OpenAI API
- **State Management:** File-based JSON persistence

## Building and Running

The project uses `npm` for dependency management and running scripts.

### Initial Setup
```bash
# Install dependencies
npm install

# Create a local environment file from the example
cp .env.example .env.local

# Add your OPENAI_API_KEY to the .env.local file
```

### Core Commands
- **Run in development mode:** `npm run dev`
- **Build for production:** `npm run build`
- **Run unit tests:** `npm test`
- **Run linter:** `npm run lint`
- **Check TypeScript types:** `npm run type-check`

### Feature Flag Management
The new pipeline architecture is governed by feature flags defined in `.env.local`.

- **`NEW_PIPELINE_ENABLED`**: (Default: `false`) Set to `true` to enable the eleven-station pipeline. When enabled, legacy endpoints are routed through the new system.
- **`FEATURE_GRAPH_ENABLED`**: (Default: `false`) Set to `true` to enable Neo4j graph integration features.

Convenience scripts are available:
- **Enable new pipeline:** `npm run pipeline:enable`
- **Disable new pipeline:** `npm run pipeline:disable`

## Development Conventions

Development practices are strict to ensure high-quality, maintainable code.

### Architectural Conventions
- **Pipeline-First:** All new orchestration logic must be implemented as a station within the `src/core/stations/` directory. The legacy `src/chirality-core/` directory is being deprecated for orchestration logic.
- **Boundary Normalization:** Inconsistencies from external data sources (like the `chirality-framework`) must be handled at the ingestion boundary. Do not allow "raw" or incomplete data types to leak into the core application logic.
- **Centralized Types:** Core document types (`DS`, `SP`, `X`, `M`) are maintained in `src/types/framework.ts`.

### Coding Style & Commits
- **TypeScript Strict Mode:** The entire codebase must be compliant with TypeScript's `strict` mode.
- **Commit Message Format:** Commits must follow the conventional commit format (`type(scope): message`).
- **Branching Strategy:** Use `feature/`, `fix/`, and `docs/` prefixes for branches.

### Testing
- **Test-Driven:** All new functionality (types, stations, utilities) must be accompanied by unit tests.
- **Parity & Regressions:** Use the "golden parity" test suite to ensure that changes to the pipeline do not alter the semantic output of the legacy system during the transition period.
- **Feature Flag Tests:** New features behind flags must include integration tests to verify that the code paths behave correctly when the flag is on or off.
