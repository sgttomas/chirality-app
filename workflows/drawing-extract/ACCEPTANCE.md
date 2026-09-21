# drawing-extract acceptance

A drawing-extract run is valid when:

### S1 — Drawing-type + extraction-target validated at Phase 0
Stubbed drawing types reject at pre-flight with no rasterization, no crops, no work-dir side effects. Valid combinations proceed; invalid ones reject.

### S2 — Requested page range processed
Every page or tile in scope is classified as `SUCCESS`, `NO_FINDINGS`, `NO_FINDINGS_REFERENCE`, `FAILED`, or `FAILED_INPUTS`.

### S3 — Page extraction delegated
Page/tile image interpretation is performed by target-specific TASK workflow dispatches with drawing-type-aware runtime overrides.

### S4 — Target-aware per-page artifact paths
Stubs are written at target-aware paths under `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/`; P&ID and drawing-set runs use run folders frozen at closure. No stubs are written at legacy top-level paths.

### S5 — Resume-safety contract enforced
Existing per-page stubs are reused only when their YAML frontmatter matches the current run's full parameter tuple. File existence alone does NOT satisfy resume.

### S6 — Combined outputs written
The target's required combined outputs exist at target-aware paths unless every page/tile failed.

### S7 — No-findings pages preserved
Pages with no matching extraction targets are recorded explicitly and reported to the human.

### S8 — Provenance preserved
Combined outputs preserve `drawing`, `system_name`, and `source_page` fields derived from page outputs.

### S9 — Schema-consistency validated (detailed target)
For `top_equipment_header_detailed`, `validate_detailed_schema.py` exits 0 before assembly runs. Divergent stubs block the run.

### S10 — Crop-first path applied (PFD targets)
Helper crops, slice generation, stub-count reporting, and deterministic sanitization all ran unless the run failed before extraction.

### S11 — Compatibility shim warning emitted
If `EXTRACTION_MODE=top_equipment_header_with_dwg` was provided, the deprecation warning was emitted at Phase 0 and reiterated in the final report.

### S12 — Merge outputs match EXISTING_DATA_PATH schema (when merged)
When `MERGE_EXISTING_DATA=true`, merge outputs include all 4 files (result, conflicts, unmatched-extracted, unmatched-existing) at target-aware paths.
