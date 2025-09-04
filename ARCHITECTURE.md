# Architecture Overview (v2.0.0)

This document describes the canonical 11‑station semantic valley pipeline, the “foundation” traversal mode, and the main components of the chirality‑app v2.0.0 implementation.

## Design Principles
- Canonical pipeline: S1→S11, preserving ontological modalities.
- Foundation‑first: Default to S1–S5 + S11 for fast, practical results.
- Clarity over abstraction: Separate domain, core, API, and UI.
- Deterministic exports: Packets validated by JSON Schema; artifacts written to disk.

## Pipeline Model (11 Stations)
Stations and modalities:
- S1 Problem (problem) → J
- S2 Requirements/Data Sheet (systematic) → DS (from C)
- S3 Objectives/Standard Procedure (process) → SP (from D)
- S4 Guidance (epistemic) → GD (from X)
- S5 Evaluation Checklist (process) → EC (from E)
- S6 Evaluation (process) → reserved
- S7 Assessment (epistemic) → reserved
- S8 Implementation (alethic) → reserved
- S9 Integration (epistemic) → reserved
- S10 Reflection (alethic) → reserved
- S11 Resolution (resolution) → Final

Execution modes:
- Foundation (default): S1, S2, S3, S4, S5, S11
- Full: S1..S11 (S6–S10 to be implemented)

Internal execution groups (scheduler detail):
- G1:S1, G2:S2, G3:S3, G4:S4+S5, G5:S6, G6:S7, G7:S8, G8:S9+S10, G9:S11

## Documents and Matrix Alignment
- DS (Data Sheet) ← Matrix C (S2)
- SP (Standard Procedure) ← Matrix D (S3)
- GD (Guidance Document) ← Matrix X (S4)
- EC (Evaluation Checklist) ← Matrix E (S5)
- Final Resolution ← synthesis at S11

## Packets and Schema
- Packet shape: `{ id, createdAt, station, modality, payload, meta? }`
- One packet per station; lines written to `runs/<runId>/packets.jsonl`
- Canonical schema: `schemas/packet.json` (validated in CI)
- Export summary: `runs/<runId>/run.json` with durations, counts, resolution

## Core Modules
- `src/domain/`: Station types, metadata, validators
- `src/core/state.ts`: Run state, selectors, document updates
- `src/core/stations/`: S1..S11 processors (S6–S10 placeholders)
- `src/core/orchestrator.ts`: Mode‑aware traversal; progress; dependency checks
- `src/core/exporter.ts`: Writes run artifacts; list/read helpers
- `src/core/llm/service.ts`: LLM integration; reads `OPENAI_MODEL`

## Validators
- Transition validator: sequential order within the selected execution list
- Dependency validator (foundation): J@S1 → DS@S2 → SP@S3 → GD@S4 → EC@S5 → Final@S11
- Currently warn‑only in orchestrator; tighten once S6–S10 are implemented

## API Surface
- `POST /api/pipeline/traverse` → runs traversal; supports `options.mode: 'foundation'|'full'`
- `GET /api/export/run?runId=...` → returns file paths and sizes if exported
- Errors follow `{ code: 'ERR_*', message, details? }`

## UI
- Minimal page with problem input, mode selector, station list with modality chips, and resolution output

## CI/CD
- Typecheck, lint, tests, build
- Foundation traversal sample + AJV validation against `schemas/packet.json`
- Build artifacts + sample run ZIP upload
- Legacy sweep blocks deprecated patterns

## Testing
- Unit tests for validators and schema
- API smoke tests for both endpoints
- Orchestrator traversal test (skipped without API key)

## Notes on Legacy Materials
- Older nine‑station and RAG/chat docs are archived and out of scope for v2.0.0. See `archive/legacy/`.
