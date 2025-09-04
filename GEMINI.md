
# Gemini Context: Chirality AI App

This document provides a comprehensive overview of the Chirality AI App project to guide future AI-driven development and analysis.

## Project Overview

Chirality AI is a Next.js application designed to transform complex problems into structured, actionable solutions. It implements a unique **three-pass semantic document generation** process (V1→V2→V3), which iteratively refines a set of documents for maximum coherence and utility.

The generation process is initiated by **matrix-driven orchestration**, where semantic matrices from an external `chirality-framework` act as "seeds of thought." This produces four core document types:
- **DS (Data Sheet):** Technical specifications and data models.
- **SP (Standard Procedure):** Step-by-step implementation workflows.
- **X (Solution Template):** Integrated solution frameworks.
- **M (Guidance):** Strategic recommendations and risk analysis.

The generated documents then serve as "seeds of evidence" for a **Retrieval-Augmented Generation (RAG)** chat interface, enabling intelligent, context-aware conversations grounded in the project's specific solutions.

**Key Technologies:**
- **Frontend:** Next.js 15, React 18, TypeScript, Tailwind CSS
- **Backend:** Next.js API Routes (Node.js)
- **AI:** OpenAI API
- **State Management:** File-based JSON persistence and Zustand for UI
- **Python Integration:** The app interfaces with the Python-based `chirality-framework` for matrix processing.

The project's core philosophy is to be a "systematic thinking" partner that augments human intellect by providing structure and reducing cognitive load, rather than simply being a one-shot answer generator.

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
- **Run in development mode:**
  ```bash
  npm run dev
  ```
  The application will be available at `http://localhost:3001`.

- **Build for production:**
  ```bash
  npm run build
  ```

- **Run unit tests:**
  ```bash
  npm test
  ```

- **Run linter:**
  ```bash
  npm run lint
  ```

- **Check TypeScript types:**
  ```bash
  npm run type-check
  ```

## Development Conventions

Development practices are strict to ensure high-quality, maintainable code.

### Coding Style
- **TypeScript Strict Mode:** The entire codebase must be compliant with TypeScript's `strict` mode.
- **Explicit Typing:** Avoid `any`. Use explicit `interface` or `type` definitions for all data structures.
- **Error Handling:** All asynchronous operations and API routes must include comprehensive `try...catch` blocks and return appropriate error responses.

### Testing
- **Automated Tests:** All contributions should be covered by unit tests where applicable. Run `npm test` before submitting changes.
- **Manual Testing:** A comprehensive manual testing checklist is required for all contributions, covering critical workflows like document generation (single-pass and three-pass), chat integration, and state persistence.

### Commits and Pull Requests
- **Branching Strategy:**
  - Features: `feature/add-new-feature`
  - Bug Fixes: `fix/resolve-bug`
  - Documentation: `docs/update-documentation`
- **Commit Message Format:** Commits must follow a specific format, including a scope and a `Documentation Assessment` block.
  ```
  type(scope): brief description

  Documentation Assessment: [NONE|STANDARD_UPDATE|SIGNIFICANT_REVISION]
  Scope: [TECHNICAL_ACCURACY|USER_EXPERIENCE|...]
  Methodology: [FEATURE_DOCUMENTATION|EXAMPLE_FIX|...]

  Detailed description of changes.
  ```
- **Pull Requests:** PRs must include a clear description of the problem and solution, evidence of testing (screenshots or logs), and confirmation that relevant documentation has been updated.

### Core Philosophy
- **Systematic Thinking:** Development should align with the core philosophy of providing structured, iterative tools.
- **Human-in-the-Loop:** Features should augment the user's ability to think and solve problems, not replace them.
- **Auditable & Deterministic:** Processes should be traceable. The V1→V2→V3 hashing and matrix-seeding are key to this.
