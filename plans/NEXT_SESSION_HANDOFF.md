# Next Session Handoff

## Quick Orientation

1. Read `INIT.md`, then `AGENTS.md`.
2. Read `agents/AGENT_HELPS_HUMANS.md` (Type 0) — adopt this design posture first.
3. Read this handoff prompt through to the end.
4. Then adopt `agents/AGENT_WORKING_ITEMS.md` as your working persona.

You are collaborating with the human on architecture work.

## What Just Happened

The phased stabilization plan, source-grounding work, and DELIVERABLE_TASK skill extraction are all complete. Three runtime validation runs confirmed the substrate works end-to-end.

| Commit | Summary |
|---|---|
| `fe989d4` | Phase 0 stabilization |
| `f19050a` | EQUIPMENT_EXTRACT → repo-native skill |
| `417559d` | Phase 1 resolved-skill model |
| `ce1929f` | Phases 2–5: run records, structural validation, tool auditing, profile/skill separation |
| `ca2c759`–`816523c` | Phase 6 commit discipline |
| `1df5787` | Source-access ruling: hard fail for all passes |
| `39205ab` | Source-grounding redlines for `4_DOCUMENTS` and `DOMAIN_DOCUMENTS` |
| `7be6ada` | Source-grounding plan marked done |
| `eaa3f44` | Extracted semantic-lensing skill |
| `f4916e0` | Extracted proposal-format skill |
| `e3b455a` | Policy sweep, validator enhancement |

**Runtime validation (3 runs exercised, not committed):**
1. `deliverable-consistency` against DEL-02.01 — tool-backed, profile-coupled, tool policy PASS
2. `semantic-lensing` against DEL-08.01 — reasoning-only, profile-coupled, lens tags produced
3. `proposal-format` against DEL-06.01 — reasoning-only, baseline scan mode, structured PROPOSAL: blocks

All produced valid `_run_records/TASK_RUN_*.md` with correct two-phase lifecycle.

**DELIVERABLE_TASK extraction is complete:**

| Behavior | Status |
|---|---|
| Semantic lensing | Extracted → `skills/semantic-lensing/` |
| Proposal output format | Extracted → `skills/proposal-format/` |
| Baseline scan defaults | Absorbed into `proposal-format` default mode |

Method prose remains inline in DELIVERABLE_TASK for backward compatibility. The profile/skill classification note is updated to reflect extraction status.

## Where You Are

The master plan is **complete**. The DELIVERABLE_TASK extraction seam is **exhausted**. No queued work packages remain.

The project is in a good place to wait for the next genuine recurring method before expanding the skill layer further.

## Carried-Forward Human Rulings

| Decision | Ruling |
|---|---|
| Missing local source *files* | Hard fail (`FAILED_INPUTS`) for all passes |
| Missing information *within* accessible sources | Continue with `TBD`; do not fail the run |
| Pass 3 source re-read evidence | Require explicit evidence in the run report |
| `_REFERENCES.md` source type distinction | Mention the distinction exists but don't enforce yet |
| Named standards as governing authority | Governing only when their actual text is locally accessible |

## Current Repo State

- 44 indexed agents (`AGENTS.md`)
- 5 repo-native skills (`skills/`: pdf2md, deliverable-consistency, equipment-extract, semantic-lensing, proposal-format)
- 55 registered tools (`tools/REGISTRY.md`)
- Branch is `main`

## Key Files To Read

| File | Why |
|---|---|
| `agents/AGENT_TASK.md` | Execution shell with run records, validation, tool compliance, profile/skill separation |
| `agents/AGENT_DELIVERABLE_TASK.md` | Profile with extraction-complete classification in RATIONALE |
| `skills/SKILL_TEMPLATE.md` | Canonical skill format |
| `skills/README.md` | Skill discovery guidance |
