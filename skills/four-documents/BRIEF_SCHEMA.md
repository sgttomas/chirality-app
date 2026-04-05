# BRIEF_SCHEMA — four-documents

This skill runs up to three passes within one invocation, selected by the `RUN_PASSES` brief parameter. The ORCHESTRATOR setup pipeline dispatches this skill twice: once before semantic lensing exists (`RUN_PASSES=P1_P2`) and once after (`RUN_PASSES=P3_ONLY`).

## RUN_PASSES parameter (optional, default `FULL`)

| Value | Meaning | Pipeline phase |
|---|---|---|
| `FULL` | Run Pass 1 + Pass 2 + Pass 3 | Ad-hoc re-runs when `_SEMANTIC_LENSING.md` already exists |
| `P1_P2` | Run Pass 1 + Pass 2 only (skip Step 6) | ORCHESTRATOR Phase 2.2 (before CHIRALITY_LENS) |
| `P3_ONLY` | Run Pass 3 only (requires existing drafts + `_SEMANTIC_LENSING.md`) | ORCHESTRATOR Phase 2.5 (after CHIRALITY_LENS) |

Any other value produces `RUN_STATUS=FAILED_INPUTS`.

**Preconditions for `P3_ONLY`:**
- The four docs (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`) must already exist in `DELIVERABLE_PATH`.
- `{DELIVERABLE_PATH}/_SEMANTIC_LENSING.md` must exist.
- If either is missing: `RUN_STATUS=FAILED_INPUTS` (no file modifications).

## Required fields

| Field | Type / values | Notes |
|---|---|---|
| `TaskSkill` | `four-documents` | Must match skill folder name |
| `DELIVERABLE_PATH` | Absolute path | One production unit folder (alias: `deliverable_folder`) |
| `DECOMPOSITION_REF` | Absolute path | Path to decomposition doc(s) or folder |

## Optional fields

| Field | Default | Allowed values |
|---|---|---|
| `RUN_PASSES` | `FULL` | `FULL`, `P1_P2`, `P3_ONLY` |
| `ALLOW_OVERWRITE_STATES` | `OPEN, INITIALIZED, SEMANTIC_READY` | Comma-separated list of `_STATUS.md` states that permit overwrite |
| `OBJECTIVE_ASSOCIATION_MODE` | `PACKAGE_HEURISTIC` | `PACKAGE_HEURISTIC` or explicit mode |
| `DECOMP_VARIANT` | `PROJECT` | `PROJECT`, `SOFTWARE` (see DOMAIN note below) |

### `DECOMP_VARIANT` — DOMAIN rejection

| Value | Behavior |
|---|---|
| `PROJECT` (default) | Process as PROJECT_DECOMP deliverable |
| `SOFTWARE` | Process as SOFTWARE_DECOMP deliverable |
| `DOMAIN` | **Unsupported** — returns `RUN_STATUS=UNSUPPORTED_VARIANT` without modifying files |

DOMAIN Knowledge Types use variable document schemas and are handled by the separate `domain-documents` skill. If a brief passes `DECOMP_VARIANT=DOMAIN` to this skill, it returns `UNSUPPORTED_VARIANT` so the invoker can route to the correct skill.

## Safe-overwrite behavior

If `{DELIVERABLE_PATH}/_STATUS.md` `Current State` is NOT in `ALLOW_OVERWRITE_STATES`:
- The skill does NOT overwrite the four documents.
- Returns `RUN_STATUS=SKIPPED_PROTECT_HUMAN_WORK` + the observed state.

This honors prior human work without requiring the invoker to probe state.

## Write boundary

- Write target: `{DELIVERABLE_PATH}/` only.
- Writable files:
  - `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` (overwrite allowed when state permits)
  - `_STATUS.md` (safe update only: `OPEN → INITIALIZED` when Pass 1/2 ran)
- Never modified: `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_MEMORY.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`.

The brief SHOULD declare:

```yaml
AllowedWriteTargets:
  - "{DELIVERABLE_PATH}/"
```

## Example brief — RUN_PASSES=P1_P2 (ORCHESTRATOR Phase 2.2)

```markdown
PURPOSE: Draft four documents for production unit (Pass 1 + Pass 2, pre-lensing)
RequestedBy: 4_DOCUMENTS
ScopePath: {DELIVERABLE_PATH}
TaskSkill: four-documents

AllowedWriteTargets:
  - "{DELIVERABLE_PATH}/"

RuntimeOverrides:
  DELIVERABLE_PATH: /abs/path/to/Project/_Deliverables/DEL-014-3/
  DECOMPOSITION_REF: /abs/path/to/Project/_Decomposition/PROJECT_DECOMP_LATEST.md
  RUN_PASSES: P1_P2
  DECOMP_VARIANT: PROJECT
```

## Example brief — RUN_PASSES=P3_ONLY (ORCHESTRATOR Phase 2.5)

```markdown
PURPOSE: Apply semantic lensing enrichment (Pass 3, post-lensing)
RequestedBy: 4_DOCUMENTS
ScopePath: {DELIVERABLE_PATH}
TaskSkill: four-documents

AllowedWriteTargets:
  - "{DELIVERABLE_PATH}/"

RuntimeOverrides:
  DELIVERABLE_PATH: /abs/path/to/Project/_Deliverables/DEL-014-3/
  DECOMPOSITION_REF: /abs/path/to/Project/_Decomposition/PROJECT_DECOMP_LATEST.md
  RUN_PASSES: P3_ONLY
  DECOMP_VARIANT: PROJECT
```

## Example brief — RUN_PASSES=FULL (ad-hoc re-run)

```markdown
PURPOSE: Full redraft with existing semantic lensing register
RequestedBy: ORCHESTRATOR
ScopePath: {DELIVERABLE_PATH}
TaskSkill: four-documents

AllowedWriteTargets:
  - "{DELIVERABLE_PATH}/"

RuntimeOverrides:
  DELIVERABLE_PATH: /abs/path/to/Project/_Deliverables/DEL-014-3/
  DECOMPOSITION_REF: /abs/path/to/Project/_Decomposition/PROJECT_DECOMP_LATEST.md
  RUN_PASSES: FULL
  ALLOW_OVERWRITE_STATES: "OPEN, INITIALIZED, SEMANTIC_READY"
  OBJECTIVE_ASSOCIATION_MODE: PACKAGE_HEURISTIC
  DECOMP_VARIANT: SOFTWARE
```

## Notes

- `DELIVERABLE_PATH` is the canonical brief field name; `deliverable_folder` is accepted as an alias.
- The 4_DOCUMENTS wrapper agent passes `RUN_PASSES` through from ORCHESTRATOR; invokers that call the skill directly must provide `RUN_PASSES` explicitly or accept the `FULL` default.
- `ALLOW_OVERWRITE_STATES` default reflects the standard PREPARATION → 4_DOCUMENTS Phase 2.2 → CHIRALITY_LENS → 4_DOCUMENTS Phase 2.5 lifecycle (`OPEN` after PREPARATION, `INITIALIZED` after Pass 1/2, `SEMANTIC_READY` after lensing).
- A single invocation operates on ONE deliverable; the wrapper is responsible for per-deliverable dispatch across a decomposition set.
