# Extend drawing extraction

Load for an authorized workflow/tool design assignment with HELPS_HUMANS.

## Extension point: Adding a new drawing type

The core-vs-repertoire split is designed so a new drawing type (e.g., `ISOMETRIC`, `GA`) can be added without modifying the core protocol. To scaffold a new drawing type:

1. **Registry entry** — add the drawing type + its extraction targets to:
   - The target-dispatch registry in CONTRACT.md (move from `stubbed (fail-fast)` to `implemented`).
   - The workflow contract: `workflows/drawing-extract-page/WORKFLOW.md` § Drawing-type + extraction-target registry and `CONTRACT.md#brief` § Supported combinations.
2. **Crop-prep tool** — register the new drawing type's crop geometry in `tools/drawing_extract/prepare_header_crops.py` (`DRAWING_TYPE_CROP_SPECS` registry). For a type whose header geometry differs substantially from PFD, this may require adding new crop kinds beyond `top_header`, `top_header_slice_*`, `titleblock`.
3. **Page-worker target spec** — extend `workflows/drawing-extract-page/WORKFLOW.md` § Step 3 (Extract according to target) with the new target's extraction semantics (what regions, what fields, what rules).
4. **Assembly hook** — either refactor `assemble_equipment_csv.py` / `assemble_equipment_markdown.py` to accept the new target (if columns map similarly), or add dedicated assembly tools scoped to the new repertoire (e.g., `assemble_valve_list_csv.py`).
5. **QA hook** — extend or wrap `report_stub_counts.py` with target-appropriate metrics, or add a new tool (e.g., `report_loop_counts.py` for P&ID instrument loops).
6. **Sanitization hook** — either refactor `sanitize_equipment_stubs.py` filters per target, or add a new sanitizer tool scoped to the new repertoire.
7. **Duplicate-flag key / merge key** — decide the repertoire's natural identity key (e.g., instrument `tag` for P&ID, `valve_number` for valve lists). Add a dedicated merge tool if the new repertoire supports cross-dataset merging.
8. **Spike** — run a crop-adequacy spike on representative drawings of the new type to validate crop geometry defaults, parallel to Phase 1 of the original slice.
9. **Tests** — extend W1 schema core tests for the new `(drawing_type, extraction_target)` combinations; add tool-specific regression fixtures where warranted.
10. **Orchestrator protocol** — add the new drawing type's mapping to the target-dispatch registry in CONTRACT.md. Register any new core vs. hook phases the new repertoire needs.

The core protocol itself (Phase 0 pre-flight, Phase 1 rasterize, Phase 2 dispatch, Phase 3 assembly, Phase 3.5 optional merge, Phase 4 final report) does NOT need to change when adding a drawing type — only the hook dispatches within the Phase 1.5 / 2.5 / 2.6 / 2.7 / 2.8 / 2.9 / 3 / 3.5 phases gain new (drawing_type × extraction_target) branches.
