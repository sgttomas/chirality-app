---
name: equation-audit
description: "Review extracted display equations with the human, interpret correction notes, apply validated fixes, backcheck changes, and close an immutable audit snapshot."
---

# Review and correct display equations

WORKING_ITEMS coordinates the review loop. The human supplies observations and verification; TASK interprets individual prose notes and detects page-bounded equation geometry. Tools extract, validate, apply, rescan, and preserve the evidence.

## Paths and review basis

`SOURCE_AUDIT_ROOT` is the complete equation-audit root, normally `{source}/audit/equations/`. Its children are `working/`, `snapshots/`, and `_LATEST.md`; append no second `equations/` component. The brief also declares writable page Markdown under `WORK_DIR` and the assembled `SOURCE_MD`, because fix application updates those surfaces.

Review identity is the physical page and equation content hash. Changed content requires fresh verification. Closed snapshots remain immutable; subsequent work occurs in `working/` and produces a new snapshot.

## Review loop

1. **Confirm the run.** Resolve the source and paths, inspect current review state, and agree the crop option and permitted unreviewed count (`ALLOW_UNREVIEWED`, default 0).
2. **Extract.** Generate the equation index and browser review surface. When crops are enabled, dispatch TASK with `Workflow: equation-bbox-detect` for each relevant page, crop with tools, then regenerate the surface.
3. **Review with the human.** The human verifies equations or exports correction flags. Keep page/hash identity and export provenance when incorporating browser state.
4. **Interpret and validate flags.** Dispatch TASK with `Workflow: equation-flag-interpret` for each prose-shaped correction. Ambiguous notes return for human clarification. Run `validate_flagged_schema.py` before applying any fix; raw prose cannot become replacement LaTeX.
5. **Apply and backcheck.** Run `process_flagged.py`, preserve prior hash/LaTeX in backcheck records, re-extract, and refresh affected crops. The human rechecks changed equations. Iterate until flags and current backcheck entries are resolved.
6. **Close with actual coverage.** Scan the current state and compare unreviewed coverage with the accepted allowance. The human accepts the closure. Copy the working evidence and run records into a new snapshot, then update `_LATEST.md`. State the verified and permitted-unreviewed counts explicitly.

## Selected resources

[CONTRACT.md](CONTRACT.md) defines parameters, artifact layout, tool interfaces, and closure evidence. [PROCEDURE.md](PROCEDURE.md) supplies current-stage commands, browser export handling, legacy layout migration, and detailed gate conditions. [ACCEPTANCE.md](ACCEPTANCE.md) defines closure checks.

Resolve tools against the declared tool root. Return unresolved ambiguity, stale or orphan sidecar keys, failures, and remaining review coverage as explicit handoff state.
