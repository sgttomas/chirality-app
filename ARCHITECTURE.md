# Architecture Overview

This document defines a lean, explicit architecture for Chirality AI App that mirrors the canonical semantic valley traversal and removes unnecessary generalization. It aligns PHILOSOPHY (semantic handedness) with INTERFACE (CLI/manifest/JSONL) and focuses the codebase on a scripted pipeline rather than an agentic framework.

## Design Principles
- Canonical pipeline: {Problem} → Systematic → Process → Epistemic → Process → Epistemic → Alethic → Epistemic → Alethic → {Resolution}
- Minimal generalization: Abstract only when the code has multiple concrete call-sites that truly share behavior.
- Separation of concerns: Framework ingestion, orchestration pipeline, generation prompts, and API surfaces stay modular.
- Compatibility first: Introduce new contracts behind adapters; deprecate gradually.

## Pipeline Model (Nine Stations)
Each station is explicit, named, and side‑effect free. Orchestration composes stations in order and persists outputs deterministically.

- S0 Problem: Problem statement normalization and validation
- S1 Systematic: Structure the problem (constraints, givens, invariants)
- S2 Process: Operational pathfinding (procedures, actors, inputs/outputs)
- S3 Epistemic: Knowledge claims and evidence requirements
- S4 Process: Refine procedures informed by S3
- S5 Epistemic: Update knowledge assertions from S4
- S6 Alethic: Necessity/possibility analysis (must/should/can’t)
- S7 Epistemic: Reconcile claims with alethic modalities
- S8 Alethic: Final modal synthesis → Resolution statements

Implementation: `lib/orchestrator/pipeline/` exposes `runStation(name, input)` and `runTraversal(problem)`. Each station owns its prompt template and post‑processing.

## Documents and Mappings
- DS (data‑handed), SP (process‑handed), X (solution‑handed), M (strategic‑handed)
- Matrices → documents (INTERFACE): C→DS, D→SP, X+E→X, E→M
- Stable ordering: sort by `meta.order` then `id`; preserve `citations`/`refs`

## Core Data Structure (Triple → Packet)
Keep runtime compatibility but tighten semantics:
- Current: `Triple<T> = { text: T; terms_used: string[]; warnings: string[] }`
- Target: `Packet<T> = { text: T; context?: { terms?: string[]; notes?: string[] }; flags?: { risk?: boolean } }`
Migration path:
- Introduce `type Triple<T> = Packet<T>` compatibility typedef
- Map `terms_used`→`context.terms`, `warnings`→`context.notes` (only where useful)
- Limit warnings to stations that assess risk (M, alethic/epistemic), not every call

## Module Layout (Target)
- `lib/framework/` ingestion + manifest/jsonl validation (INTERFACE compliant)
- `lib/orchestrator/pipeline/` nine stations with pure transforms
- `lib/orchestrator/prompts/` one template per station (no generic prompt factory unless duplicated)
- `src/chirality-core/` state/persistence and RAG compaction only
- `src/app/api/` routes: `/core/*` (state/orchestrate), `/agent/*` (framework), `/chat/*` (RAG)
- Optional graph kept behind `FEATURE_GRAPH_ENABLED`; no hard runtime dependency

## API Alignment
- Preserve existing endpoints and response shapes; add `finals.packet` alongside `finals.triple` for transition
- Enforce INTERFACE.md rules: run_id pattern, manifest version checks, JSONL schemas, checksums

## Deprecation & Debt Removal
- Remove unused helpers and generic “agent” abstractions not used by pipeline
- Isolate feature‑flagged code (Neo4j/GraphQL) to optional modules
- Collapse one‑off utilities into station‑local helpers

## Testing
- Station tests: prompt IO post‑processing and invariants
- Pipeline tests: deterministic ordering, matrix→document mapping, traversal integrity
- Ingestion tests: manifest/schema/version compatibility, checksum verification

---

# Refactor Strategy (Compatibility First)

1) Types: Introduce `Packet<T>`; create `Triple<T>` alias and adapters. Update only call‑sites that do risk/terms reporting.
2) Orchestration: Implement `pipeline/` with nine stations and a thin `runTraversal()` that composes them. Keep V1/V2/V3 as a compatibility mode that maps to station groups.
3) Prompts: Move templates into `prompts/` by station, dropping generic factories unless duplicated.
4) Framework ingestion: Strict INTERFACE.md validation and stable ordering utilities.
5) API: Add `packet` fields in responses; mark legacy `triple` as deprecated in docs.
6) Cleanup: Remove dead code and unused abstractions; gate optional graph under feature flag.
7) Tests: Add station and mapping tests; keep existing suites green; migrate gradually.
8) Docs: Ensure PHILOSOPHY ↔ INTERFACE alignment reflected here; update README and API_REFERENCE once `packet` is surfaced.

