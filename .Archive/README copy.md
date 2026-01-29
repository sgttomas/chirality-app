# Canola Oil Transload Facility — Phase 1 (Design & Build)

This repository is a **deliverable-centric workspace** for producing the engineering and project documentation required for the **Canola Oil Transload Facility — Phase 1** Design & Build contract.

The workflow uses a multi-agent documentation framework designed for **EPC / design-build, multi-discipline** projects:

- Work is performed **inside a deliverable folder** (“working-item”).
- Deliverables progress through a **local lifecycle**: `OPEN → INITIALIZED → IN_PROGRESS → CHECKING → ISSUED`.
- **Stage gates** (30/60/90/IFC, etc.) and cross-deliverable coordination are **human-managed** and may live in a Gantt/table/etc.
- Cross-deliverable coherence checks happen only when humans choose to run the **RECONCILIATION** agent.

## Filesystem paths

| Item | Absolute Path |
|---|---|
| Project workspace | `/Users/ryan/ai-env/projects/chirality-app/test/` |
| Execution workspace | `/Users/ryan/ai-env/projects/chirality-app/test/execution/` |
| Decomposition file | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` |
| Agent instructions | `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_INSTRUCTIONS_BUNDLE_2026-01-28_v3/` |
| CHIRALITY-APP agent | `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_CHIRALITY-APP.md` |
| Employer's Req Vol 2 Pt 1 | `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_1_Employers_Requirements.pdf` |
| Employer's Req Vol 2 Pt 2 | `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_2_Employers_Requirements.pdf` |
| Employer's Req Vol 2 Pt 3 | `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_3_Employers_Requirements.pdf` |

## Project snapshot

Source of truth: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`.

- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Employer:** DP World Fraser Surrey Inc.
- **Contract type:** Design & Build
- **Decomposition size:** 36 packages / 210 deliverables
- **Key parameters (high-level):** 1,000,000 MT/a permitted throughput; 45,000 MT storage (3 × 15,000 MT tanks); 32 railcar unloading stations

## What lives where

### Repository inputs

- `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — the project scope decomposition (packages, deliverables, objectives, reference-doc list, decisions captured).
- `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_INSTRUCTIONS_BUNDLE_2026-01-28_v3/` — agent instruction documents (the "system specification" for how the agents operate).
- `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_CHIRALITY-APP.md` — the human guidance / navigator agent.

### Runtime workspace (created by ORCHESTRATOR)

When you run the ORCHESTRATOR, it creates the execution workspace at `/Users/ryan/ai-env/projects/chirality-app/test/execution/` with:

- `test/execution/_Coordination/_COORDINATION.md` — a **human-owned** record of how coordination is being represented (schedule-first / declared deps / full graph) and whether dependencies are tracked in-file.
- `test/execution/{PKG-ID}_{PkgLabel}/` — one folder per package.
- `test/execution/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/` — one folder per deliverable.

Each deliverable folder contains:

- `_CONTEXT.md` — canonical identity + decomposition pointer
- `_DEPENDENCIES.md` — dependency mode + declared edges (or a NOT_TRACKED stub)
- `_STATUS.md` — lifecycle state + history
- `_REFERENCES.md` — pointers to the sources you want to work from
- `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` — the four scaffolding documents

### Filesystem-safe folder names (important)

Some deliverable names in the decomposition contain characters that cannot appear in folder names (example: `/`).

- Folder names use **sanitized labels**: `{PkgLabel}` and `{DelLabel}`.
- The canonical (unsanitized) names still appear exactly in `_CONTEXT.md` for traceability.

## How to use the framework (typical EPC path)

### 1) Choose your coordination representation (human decision)

Most EPC / multi-discipline projects work best with:

- **Representation:** Schedule-first (Gantt / stage gates)
- **Dependency tracking mode:** `NOT_TRACKED` (or `DECLARED` if you want to capture a small set of interface-critical edges)

Why: maintaining a full dependency DAG across 200+ deliverables is usually high effort and easy to make wrong.

### 2) Run ORCHESTRATOR → Initialize

Provide the decomposition file path and confirm:

- representation (Schedule-first | Declared deps | Full graph)
- dependency tracking mode (`NOT_TRACKED` | `DECLARED` | `FULL_GRAPH`)

ORCHESTRATOR will also surface the decomposition’s **Reference Documents** list and **Decisions Captured** so you can supply baseline inputs early.

### 3) Run ORCHESTRATOR → Scaffold

ORCHESTRATOR spawns PREPARATION to create:

- package folders + lifecycle subfolders
- one deliverable folder per DEL-ID
- minimum viable fileset in each deliverable folder

### 4) Run ORCHESTRATOR → Initialize drafts

ORCHESTRATOR spawns 4_DOCUMENTS for each deliverable to generate initial drafts of:

- `Datasheet.md`
- `Specification.md`
- `Guidance.md`
- `Procedure.md`

4_DOCUMENTS only sets `_STATUS.md` from `OPEN → INITIALIZED` **if the deliverable is currently `OPEN`** (no state regression).

### 5) Do real work via WORKING_ITEMS (human + agent)

WORKING_ITEMS sessions are how you iterate deliverables with engineering judgment.

Inside a WORKING_ITEMS session:

- You work **inside one deliverable folder**.
- The agent produces/updates **all four documents together**.
- Every non-trivial claim is sourced, or labeled **ASSUMPTION** / **TBD**.
- If there’s a contradiction, the agent must present a **Conflict Table** and request a human ruling.

### 6) Review and issue (CHECKING / ISSUED)

Recommended convention:

- When submitting for review (`CHECKING`): copy a review package into `2_Checking/To/` (include DEL-ID + date/rev in filenames).
- When issuing (`ISSUED`): place issued copies in `3_Issued/` (archive older issues as needed).

The deliverable folder stays under `1_Working/`; `_STATUS.md` is the authoritative lifecycle indicator.

### 7) Cross-deliverable checks (optional) via RECONCILIATION

Run RECONCILIATION only when humans choose (often at freeze points):

- Provide explicit scope (packages or deliverables)
- Provide a gate label (e.g., “30% Freeze”)
- Provide focus areas (interfaces, parameters, terminology, assumptions)

RECONCILIATION is **read-only** and outputs a reconciliation report + conflict table for human rulings.

## Project-specific notes

- The decomposition’s **objective mapping is best-effort** and may be expressed as **deliverable ranges by package**.
  - When objectives are not listed per deliverable, use **package-based association** and confirm priority with the human.
- Review **Scope Focus / exclusions** and **Decisions Captured** before committing requirements; these sections often contain critical interface boundaries and responsibility splits.
- Baseline inputs referenced by the decomposition include Employer's Requirements volumes (Vol 2 Part 1–3), located at `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf`. If you don't have them yet, index them in `_REFERENCE_INDEX.md` and treat related requirements as **TBD** until provided.

## Getting help

- Use **CHIRALITY-APP** as your “how do I use these agents?” navigator.
- Use **ORCHESTRATOR** when you need filesystem-grounded reporting of where the project stands.
- Use **WORKING_ITEMS** when you want to actually produce or refine a deliverable.

For an operator-facing summary of the agents and how to invoke them, see `/Users/ryan/ai-env/projects/chirality-app/AGENTS.md`.
