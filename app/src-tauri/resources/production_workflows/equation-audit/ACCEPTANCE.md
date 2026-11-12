# equation-audit acceptance

An equation-audit closure is valid when:

### S1 — All flagged entries have been resolved
At Phase 6 close, `flagged.json` contains zero entries (the file may exist as `{}` or be absent). Any entry that could not be auto-interpreted has been handled by the human through additional review iterations.

### S2 — All backcheck entries have been re-reviewed
At Phase 6 close, `backcheck.json` contains zero entries that match currently-extracted equations. Stale entries whose equations no longer exist (because their hash changed via further fixes) are non-blocking.

### S3 — Unreviewed coverage meets the allowance
At Phase 6 close, the count of unreviewed equations does not exceed `ALLOW_UNREVIEWED` (default 0, i.e., full coverage required).

### S4 — Tools are invoked correctly
Equation extraction, schema validation, state scanning, fix application, migration, and cropping are performed by deterministic Python tools, not by LLM reasoning embedded inside a tool.

### S5 — Prose-note interpretation is delegated via compliant TASK dispatch
Each prose-shaped flagged-entry description is converted to LaTeX by a `TASK+equation-flag-interpret` dispatch using the INIT-TASK brief shape, NOT by WORKING_ITEMS itself and NOT by a subprocess fork inside `process_flagged.py`.

### S6 — Bbox detection (when enabled) is delegated via compliant TASK dispatch
When `ENABLE_CROPS=true`, per-page display-equation bounding boxes are computed by `TASK+equation-bbox-detect` dispatches that read one page raster and produce one `page_NNNN_eq_bboxes.json` per dispatch.

### S7 — Schema gate is enforced before fix-apply
`process_flagged.py` runs `validate_flagged_schema.py` as a fail-fast gate at the start of Phase 3c, refusing to apply fixes if any entry has a prose-shaped description. The gate is unconditional: there is no bypass flag. R12 enforcement (LLM reasoning belongs in the `equation-flag-interpret` workflow, not in this tool) depends on this gate being load-bearing.

### S8 — Snapshot is immutable
Once closed, files under `{SOURCE_AUDIT_ROOT}/snapshots/EQ_{book}_{TS}/` are not modified. WORKING_ITEMS’ writes after closure go to `working/` (the next iteration's surface), not into closed snapshots.

### S9 — _LATEST pointer matches the most recent closure
After Phase 6, `{SOURCE_AUDIT_ROOT}/_LATEST.md` references the snapshot directory created in this run, with the closure timestamp and headline metrics.

### S10 — Provenance is preserved
Every entry in `verified.json`, `flagged.json`, and `backcheck.json` carries `page` + `hash` keying back to a specific equation in `equations.jsonl`. The fix-apply step records `prev_hash` and `prev_latex` in `backcheck.json` so the audit trail is reconstructable.

### S11 — Review states are disjoint
The closure scan reports `overlaps == 0`. The permitted-unreviewed allowance never waives flags, current backcheck entries, or overlapping states.
