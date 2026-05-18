# lens-register — Brief Schema

## Required

- `DeliverablePath` (or `deliverable_folder`) — absolute path to one production unit folder. Must contain `_SEMANTIC.md`.

## Optional

- `DECOMP_VARIANT` — `PROJECT | SOFTWARE` (default `PROJECT`)

> **Note:** DOMAIN variant is not supported (DOMAIN pipelines skip the semantic lensing step). If `DECOMP_VARIANT=DOMAIN` is passed in a brief, the skill refuses gracefully per `QA_CHECKS.md`.

## Example brief

```yaml
TaskProfile: (none)
TaskSkill: lens-register
ScopePath: /abs/path/to/deliverable-folder
RuntimeOverrides:
  DECOMP_VARIANT: PROJECT
```

## Fields by semantic role

| Field | Role | Source |
|---|---|---|
| `DeliverablePath` / `deliverable_folder` / `ScopePath` | Scope anchor | ORCHESTRATOR Phase 2.4, per variant folder patterns |
| `DECOMP_VARIANT` | Variant of decomposition pipeline | ORCHESTRATOR frontmatter or explicit override |

## Files the skill expects to find in scope

- `_SEMANTIC.md` — **required** (source of lens matrices A, B, C, F, D, X, E)
- `_CONTEXT.md` — recommended (deliverable identity)
- `_STATUS.md` — recommended (read-only)
- `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` — the standard four-document set (each optional; missing docs produce `[WARNING] MISSING_DOC` header entries, not failures)
- `_REFERENCES.md` — optional (listed but not expanded unless instructed)

## Output location

- `{DeliverablePath}/_SEMANTIC_LENSING.md` — overwritten each run
