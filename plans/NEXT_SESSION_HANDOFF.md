# Next Session Handoff

## Quick Orientation

1. Read `INIT.md`, then `AGENTS.md`.
2. Read `agents/AGENT_HELPS_HUMANS.md` (Type 0) — adopt this design posture first.
3. Read this handoff prompt through to the end.
4. Then adopt `agents/AGENT_WORKING_ITEMS.md` as your working persona.

You are collaborating with the human on architecture work.

## What Just Happened

The phased stabilization plan, source-grounding work, and initial skill extraction are all complete. Two runtime validation runs confirmed the substrate works end-to-end.

| Commit | Summary |
|---|---|
| `fe989d4` | Phase 0 stabilization |
| `f19050a` | EQUIPMENT_EXTRACT → repo-native skill |
| `417559d` | Phase 1 resolved-skill model |
| `ce1929f` | Phases 2–5: run records, structural validation, tool auditing, profile/skill separation |
| `ca2c759`–`816523c` | Phase 6 commit discipline, plan/handoff finalization |
| `1df5787` | Source-access ruling: hard fail for all passes |
| `39205ab` | Source-grounding redlines for `4_DOCUMENTS` and `DOMAIN_DOCUMENTS` |
| `7be6ada` | Source-grounding plan marked done |
| `eaa3f44` | Extracted semantic-lensing skill from DELIVERABLE_TASK |

**Runtime validation (two runs exercised, not committed):**
1. `deliverable-consistency` against `DEL-02.01_Pipeline-Design-Basis` — tool-backed, profile-coupled, tool policy PASS
2. `semantic-lensing` against `DEL-08.01_Steam-line-design-supply-install-tie-in` — reasoning-only, profile-coupled, lens tags produced

Both runs produced valid `_run_records/TASK_RUN_*.md` artifacts with correct two-phase lifecycle.

**Policy sweep (user-completed, included in this changeset):**
- Source-grounding policy notes marked as reflected in implementation
- Document-discovery policy partially adopted into `skills/README.md` and `docs/REPO_INVENTORY.md`
- Validator enhanced

## Where You Are

The master plan is **complete**. No queued work packages remain.

Current focus: **skill extraction from DELIVERABLE_TASK** (Phase 5 continuation).

### Skill extraction status

From `agents/AGENT_DELIVERABLE_TASK.md` RATIONALE §Profile / skill classification:

| Method-like behavior | Status |
|---|---|
| Semantic lensing mode | **Extracted** → `skills/semantic-lensing/` |
| Proposal output format (PROPOSAL: blocks) | **Next** |
| Baseline scan defaults (top 5 / top 5 / deps) | Reassess after proposal-format lands |

### Recommended sequence

1. Build `proposal-format` skill — the PROPOSAL: block output pattern
2. Validate with one real TASK run
3. Reassess baseline-scan defaults — may be better as generic fallback than a named skill

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
- 4 repo-native skills (`skills/`: pdf2md, deliverable-consistency, equipment-extract, semantic-lensing)
- 55 registered tools (`tools/REGISTRY.md`)
- Branch is `main`

## Key Files To Read

| File | Why |
|---|---|
| `agents/AGENT_TASK.md` | Execution shell with run records, validation, tool compliance, profile/skill separation |
| `agents/AGENT_DELIVERABLE_TASK.md` | Profile with structural/method classification — proposal format is the next extraction target |
| `skills/SKILL_TEMPLATE.md` | Canonical skill format |
| `skills/README.md` | Skill discovery guidance (newly promoted from policy) |
