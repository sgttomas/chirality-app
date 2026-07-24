# lens-register — Brief Schema

## Dispatch role

`lens-register` is the normal PROJECT_SETUP Phase 2.4 setup-pipeline skill for PROJECT / SOFTWARE semantic lensing. It is dispatched through TASK as a bounded method pack. It reads one deliverable folder, parses `_SEMANTIC.md`, scans production documents, and writes `_SEMANTIC_LENSING.md`.

Use TASK generic shell for normal PROJECT_SETUP dispatch. This skill supplies its own method contract and write-boundary requirements, and the brief must authorize `_SEMANTIC_LENSING.md` writes.

## Required

- `ScopePath` — absolute path to one production unit folder; this is the TASK-normalized scope root.
- `TaskSkill` — `lens-register`.
- `RuntimeOverrides.deliverable_folder` — same absolute path as `ScopePath`; this is the skill's explicit scope anchor.
- `_SEMANTIC.md` must exist in the deliverable folder. If absent, the skill writes a blocking `_SEMANTIC_LENSING.md` header and stops.

## Recommended

- `RuntimeOverrides.DECOMP_VARIANT` — `PROJECT` | `SOFTWARE` (default `PROJECT`).
- `RuntimeOverrides.STATUS_POLICY` — `NO_STATUS_TOUCH` for normal Phase 2.4.
- `RuntimeOverrides.PRODUCTION_FORMAT` — resolver-selected
  `LEGACY_FOUR_DOC`, `SOW_V1`, or authorized `MIGRATION_DUAL`; dual mode
  requires `FORMAT_AUTHORITY_REF`.
- `AllowedWriteTargets` — include only:
  - `{deliverable_folder}/_SEMANTIC_LENSING.md`
  - `{deliverable_folder}/_run_records/` (TASK shell output)

## Optional / compatibility aliases

- `deliverable_folder` may be provided as a top-level legacy field, but `RuntimeOverrides.deliverable_folder` is preferred.
- `DeliverablePath` is accepted only as a compatibility alias when an existing caller provides it. It does not affect TASK write authorization.
- `DECOMP_VARIANT` may be provided top-level or in `RuntimeOverrides`; runtime override wins.

## Unsupported

- `DECOMP_VARIANT=DOMAIN` is not supported. DOMAIN pipelines skip semantic lensing. The skill refuses gracefully and does not write `_SEMANTIC_LENSING.md`.
- Multi-deliverable scope is not accepted.
- Cross-deliverable scanning is not accepted.
- Following external references from `_REFERENCES.md` is not accepted unless a separate explicitly authorized task provides those sources as in-scope inputs.

## Canonical PROJECT_SETUP Phase 2.4 brief

```markdown
PURPOSE: Generate the deliverable-local semantic lensing register for one production unit.
RequestedBy: PROJECT_SETUP

ScopePath: {DELIVERABLE_PATH}
TaskSkill: lens-register

Tasks:
  - Load `skills/lens-register/SKILL.md` and companion files.
  - Read `_SEMANTIC.md` and the production documents for this deliverable.
  - Parse only primary Result tables for matrices A, B, C, F, D, X, E.
  - Generate or overwrite `{DELIVERABLE_PATH}/_SEMANTIC_LENSING.md`.
  - Run lens-register QA and validator when available.

ApplyEdits: true
AllowedWriteTargets:
  - {DELIVERABLE_PATH}/_SEMANTIC_LENSING.md
  - {DELIVERABLE_PATH}/_run_records/

RuntimeOverrides:
  DECOMP_VARIANT: {PROJECT|SOFTWARE}
  deliverable_folder: {DELIVERABLE_PATH}
  STATUS_POLICY: NO_STATUS_TOUCH

CustomInstructions:
  - Treat `_SEMANTIC.md` as a lens source, not an authority.
  - Ignore Matrix Summary, Matrix Z, derivation tables, and structural matrices K, G, T.
  - Keep production documents, `_SEMANTIC.md`, and `_STATUS.md` read-only.
  - Record only warranted items with SourcePath and SectionRef.
  - Use lens-specific `NO_ITEMS` notes; do not repeat boilerplate.
  - Do not follow external references outside the deliverable folder.
  - Do not claim `validate_lens_register.py` PASS unless the validator actually ran.

ExpectedOutputs:
  - `{DELIVERABLE_PATH}/_SEMANTIC_LENSING.md`
  - `{DELIVERABLE_PATH}/_run_records/TASK_RUN_*.md`
```

## Files the skill expects to find in scope

Required:
- `_SEMANTIC.md` — source of lens matrices A, B, C, F, D, X, E.

Recommended / contextual:
- `_CONTEXT.md` — deliverable identity.
- `_STATUS.md` — read-only lifecycle state.
- `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` — standard production document set. Missing docs produce `[WARNING] MISSING_DOC`, not failure.
- `ScopeOfWork.md` — selected production contract for `SOW_V1`; candidate
  replacement only in authorized `MIGRATION_DUAL`.
- `_REFERENCES.md` — deliverable-local metadata only; list pointers but do not expand them.

## Output location

- `{deliverable_folder}/_SEMANTIC_LENSING.md` — overwritten each run.
- `{deliverable_folder}/_run_records/TASK_RUN_*.md` — TASK shell run record, not a skill-authored output.
