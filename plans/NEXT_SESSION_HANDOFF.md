# Next Session Handoff

## Quick Orientation

1. Read `INIT.md`, then `AGENTS.md`.
2. Read `agents/AGENT_HELPS_HUMANS.md` (Type 0) — adopt this design posture first.
3. Read this handoff prompt through to the end.
4. Then adopt `agents/AGENT_WORKING_ITEMS.md` as your working persona for the implementation session — evidence-first, bounded increments, conflict surfacing, human authority.

You are collaborating with the human on architecture work in `plans/`.

## What Just Happened

Phase 2 (standard run records) was designed and implemented in this session:

1. `417559d` — Phase 1 resolved-skill model (prior session)
2. *(uncommitted)* — Phase 2 run-record persistence: TASK now produces a durable Markdown run record (`_run_records/TASK_RUN_*.md`) with YAML frontmatter for every Type 2 run. Two-phase lifecycle: written at normalization with `PENDING`, updated at completion with final status. All changes in `agents/AGENT_TASK.md`.

Design decisions resolved:
- **Format:** Markdown with YAML frontmatter (13 machine-consumed fields + 9 body headings)
- **Location:** `{ScopePath}/_run_records/` — stays within deliverable-local write scope
- **Lifecycle:** Two-phase (PENDING at normalization, final status at completion, immutable after)
- **Interaction:** Independent from MEMORY.md and NEXT_INSTANCE_STATE.md

## Where You Are On The Roadmap

The governing roadmap is `plans/PHASED_STABILIZATION_AND_EXECUTABLE_SKILLS_PLAN.md`.

| Phase | Status |
|---|---|
| 0 — Stabilize | **Done** |
| 1 — Executable skill resolution | **Done** |
| 2 — Standard run records | **Done** |
| 3 — Light validation around resolved state | **Next** |
| 4 — Tool-use auditing | Queued |
| 5 — Profile/skill separation | Queued |
| 6 — Commit discipline | Queued |

The source-grounding supporting work package is now eligible (see rulings below).

## Phase 3 — What To Do Next

Read `plans/PHASED_STABILIZATION_AND_EXECUTABLE_SKILLS_PLAN.md` §Phase 3.

**Goal:** Validate the new execution substrate without overreaching into heavy auditing too early.

**Validate now:**
- resolved skill folder exists
- referenced companion files are either present or explicitly absent
- allowed tools resolve to real paths
- write targets stay within normalized scope
- required run-record fields are present

**Defer until later:**
- strict proof that the first-declared tool was used first
- deep semantic validation of skill content
- cross-run analytics
- strict tool-policy auditing across all task types

## Carried-Forward Human Rulings (for source-grounding work, now eligible)

| Decision | Ruling |
|---|---|
| Missing local sources during drafting | Continue with `TBD`; do not fail the run |
| Pass 3 source re-read evidence | Require explicit evidence in the run report |
| `_REFERENCES.md` source type distinction | Mention the distinction exists but don't enforce yet |
| Named standards as governing authority | Governing only when their actual text is locally accessible |

These apply to `plans/AGENT_SOURCE_GROUNDING_INSTRUCTION_UPDATE_PLAN.md` which targets `agents/AGENT_DOMAIN_DOCUMENTS.md` and `agents/AGENT_4_DOCUMENTS.md`.

**Important caveat for DOMAIN_DOCUMENTS:** The current `AGENT_DOMAIN_DOCUMENTS.md` Pass 3 already has a strict failure mode for unreadable sources (see lines ~150 and ~319). The "continue with TBD" ruling may conflict with that existing contract. Resolve this design tension before implementing the source-grounding updates.

## Current Repo State

- 44 indexed agents (`AGENTS.md`)
- 3 repo-native skills (`skills/`: pdf2md, deliverable-consistency, equipment-extract)
- 55 registered tools (`tools/REGISTRY.md`)
- `agents/AGENT_EQUIPMENT_EXTRACT.md` exists on disk but is NOT indexed — kept as reference
- Working tree has uncommitted Phase 2 changes; branch is `main`

## Key Files To Read

| File | Why |
|---|---|
| `plans/PHASED_STABILIZATION_AND_EXECUTABLE_SKILLS_PLAN.md` | Master roadmap — read Phase 3 |
| `agents/AGENT_TASK.md` | The execution shell — now includes run-record persistence (§Run record persistence, §Run-record file format, PROTOCOL steps 1/5/6) |
| `skills/SKILL_TEMPLATE.md` | Canonical `allowed-tools` format locked in Phase 1 |
| `plans/AGENT_SOURCE_GROUNDING_INSTRUCTION_UPDATE_PLAN.md` | Source-grounding work package — now eligible |
