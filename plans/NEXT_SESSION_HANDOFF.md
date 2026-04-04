# Next Session Handoff

## Quick Orientation

1. Read `INIT.md`, then `AGENTS.md`.
2. Read `agents/AGENT_HELPS_HUMANS.md` (Type 0) — adopt this design posture first.
3. Read this handoff prompt through to the end.
4. Then adopt `agents/AGENT_WORKING_ITEMS.md` as your working persona.

You are collaborating with the human on architecture work in `plans/`.

## What Just Happened

The full phased stabilization and executable skills plan is complete (Phases 0–6):

| Commit | Phase | Summary |
|---|---|---|
| `fe989d4` | 0 | Stabilization: `.gitignore`, registered tools, fixed counts |
| `f19050a` | — | EQUIPMENT_EXTRACT agent → repo-native skill |
| `417559d` | 1 | Resolved-skill model: frontmatter parsing, tool allowlist intersection |
| `ce1929f` | 2–5 | Run records, structural validation, tool-use auditing, profile/skill separation |
| `ca2c759` | 6 | Plan/handoff updates, commit discipline applied |

Key architectural additions to `agents/AGENT_TASK.md`:
- **Run record persistence** — `{ScopePath}/_run_records/TASK_RUN_*.md`, Markdown with YAML frontmatter, two-phase lifecycle
- **Structural validation** — named checklist of pre-execution and post-execution checks
- **Tool policy compliance** — `ToolsUsed` entries in `allowed-tools` format, `ToolPolicyCompliance` field
- **Profile/skill separation** — documented principle: profiles own structure, skills own method

## Where You Are On The Roadmap

The governing roadmap `plans/PHASED_STABILIZATION_AND_EXECUTABLE_SKILLS_PLAN.md` is **complete**.

| Phase | Status |
|---|---|
| 0 — Stabilize | **Done** |
| 1 — Executable skill resolution | **Done** |
| 2 — Standard run records | **Done** |
| 3 — Light validation around resolved state | **Done** |
| 4 — Tool-use auditing | **Done** |
| 5 — Profile/skill separation | **Done** |
| 6 — Commit discipline | **Done** |

## What's Next

With the executable-skill substrate complete, the following work is eligible:

### Source-grounding updates (ready)

Plan: `plans/AGENT_SOURCE_GROUNDING_INSTRUCTION_UPDATE_PLAN.md`
Targets: `agents/AGENT_DOMAIN_DOCUMENTS.md`, `agents/AGENT_4_DOCUMENTS.md`

**Important caveat for DOMAIN_DOCUMENTS:** The current `AGENT_DOMAIN_DOCUMENTS.md` Pass 3 has a strict failure mode for unreadable sources (see lines ~150 and ~319). The "continue with TBD" ruling may conflict with that existing contract. Resolve this design tension before implementing.

### Other potential next steps

- Promote any remaining plan-level policies into canonical docs
- Build additional skills using the now-stable skill substrate
- Validate the run-record mechanism with a real Type 2 run

## Carried-Forward Human Rulings

| Decision | Ruling |
|---|---|
| Missing local sources during drafting | Continue with `TBD`; do not fail the run |
| Pass 3 source re-read evidence | Require explicit evidence in the run report |
| `_REFERENCES.md` source type distinction | Mention the distinction exists but don't enforce yet |
| Named standards as governing authority | Governing only when their actual text is locally accessible |

## Current Repo State

- 44 indexed agents (`AGENTS.md`)
- 3 repo-native skills (`skills/`: pdf2md, deliverable-consistency, equipment-extract)
- 55 registered tools (`tools/REGISTRY.md`)
- Working tree clean; branch is `main`, 8 commits ahead of origin

## Key Files To Read

| File | Why |
|---|---|
| `agents/AGENT_TASK.md` | The execution shell — now includes run records, structural validation, tool compliance, profile/skill separation |
| `agents/AGENT_DELIVERABLE_TASK.md` | Profile with structural/method classification in RATIONALE |
| `skills/SKILL_TEMPLATE.md` | Canonical skill format |
| `plans/AGENT_SOURCE_GROUNDING_INSTRUCTION_UPDATE_PLAN.md` | Source-grounding work package — now eligible |
