# semantic-matrix-build — Brief Schema

## Required

- `deliverable_folder` (or `DeliverablePath`) — absolute path to one production unit folder (resolved by ORCHESTRATOR per variant folder patterns)
- `decomposition_path` — absolute path to the decomposition document (for traceability; do not re-interpret scope)

## Optional

- `DECOMP_VARIANT` — `PROJECT` | `SOFTWARE` | `DOMAIN` (default `PROJECT`)

## Runtime overrides examples

| Key | Example value | Notes |
|---|---|---|
| `DECOMP_VARIANT` | `PROJECT` | default; standard four-document set |
| `DECOMP_VARIANT` | `SOFTWARE` | software-variant folder + four-document set |
| `DECOMP_VARIANT` | `DOMAIN` | DOMAIN variant; reads `Scoping.md` + `KA-*.md` Knowledge Artifact files |

## Custom instructions examples

Typical brief invocation patterns:

- **Standard PROJECT run:** Provide `deliverable_folder` + `decomposition_path`; omit `DECOMP_VARIANT` (defaults to `PROJECT`). Skill reads `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`.
- **SOFTWARE variant:** Provide `deliverable_folder` + `decomposition_path` + `DECOMP_VARIANT=SOFTWARE`. Production document set is the same as PROJECT; terminology is unchanged.
- **DOMAIN variant:** Provide `deliverable_folder` + `decomposition_path` + `DECOMP_VARIANT=DOMAIN`. Skill discovers non-metadata `.md` files (typically `Scoping.md` + `KA-*.md` Knowledge Artifact files). Entity terminology substitutes per the Variant Awareness table in SKILL.md.

## Not accepted

- Multi-deliverable scope. Each invocation processes exactly one deliverable folder.
- Cross-deliverable scanning or comparison.
- Authority to edit production documents (read-only).
