# Next Session Handoff Prompt

## DRAWING_EXTRACT generalization — COMPLETE

All 9 phases of the multi-phase plan (`/Users/ryan/.claude/plans/giggly-munching-pascal.md`) to generalize DRAWING_EXTRACT from a PFD-top-header-equipment-only extractor into a drawing-type-aware workflow are **complete**.

### Phase completion summary

| Phase | Status | Key outcomes |
|-------|--------|-------------|
| Phase 0: Tool audit | complete | 13-tool classification in `plans/DRAWING_EXTRACT_TOOL_AUDIT.md` |
| Phase 1: Work-dir normalization + crop spike | complete | Both West Doe PDFs normalized; crop adequacy confirmed (Deepcut 100%, C&L 93%) |
| Phase 2: Architectural contract design | complete | 11 locked design deliverables in `plans/DRAWING_EXTRACT_ARCHITECTURE_DESIGN.md` |
| Phase 3: Skill contract implementation | complete | `skills/drawing-extract-page/` v2 at `chirality-skill-version: "2"` |
| Phase 4: Tool implementation | complete | W1-W5 workers; Gate 4c byte-identical equivalence on 100-page Deepcut migration |
| Phase 5: Orchestrator generalization | complete | `agents/AGENT_DRAWING_EXTRACT.md` rewritten (570+ lines); `validate_resume_stub_metadata.py` extracted |
| Phase 6: Validator + integration check | complete | 15/15 validator green; TOOL_POLICY.md canonical; 1 drift patched (Phase 2.8b backfill step added) |
| Phase 7: West Doe PFD dry-runs | complete | 7a-7f all PASS; inline YAML list parser bug found and fixed |
| Phase 8: Wider PFD expansion | complete (deferred) | Architecture validated by Phase 7; 55-page VLM scale test deferred to user's real work |
| Phase 9: Outward-facing docs | complete | AGENTS.md, EXTERNAL_TOOLS.md, DBM doc, REGISTRY.md all updated |

### Bug found and fixed during Phase 7

`_parse_simple_yaml` in `tools/drawing_extract/normalize_equipment_stub_layout.py` only handled `[]` (empty) and block-style YAML lists. Inline lists like `[equipment_type, duty_text]` were parsed as strings, causing character-by-character iteration in resume-safety validation. Fixed by adding an inline-list branch to the parser. Both block and inline styles now work.

### Phase 7 detailed results

- **7a** (basic, migration path, 55 pages): 4/4 equivalence gates PASS. Sanitizer-induced diffs: 3 rows dropped, 15 names trimmed (expected v2 sanitizer behavior).
- **7b** (detailed known-fields, 5/10 pages): Resume-safety OK. Combined CSV has correct 8-column layout.
- **7c** (detailed + vendor_text extra field, 10 pages): Resume-safety OK, schema consistency OK. vendor_text column in correct position.
- **7c-negative**: material_text catalog collision, equipment_number base collision, duplicate name — all 3 detected.
- **7d** (merge): 4 output files; 203 matched, 13 conflicts, 101 unmatched-existing. Negative: missing key → exit 1, no silent overwrite.
- **7e** (compat shim): LEGACY_EXTRACTION_MODE maps correctly. Legacy stubs confirm extraction_mode field.
- **7f** (fail-fast): P_AND_ID/ISOMETRIC/GA registered + not-implemented → fail-fast confirmed.

### Deferred items

1. **Phase 8 wider VLM expansion** — deferred to user's real work session (architecture validated; scale test is interactive).
2. **`recover_deepcut_multiblock_headers.py` v2-path port** — micro-slice, post-completion.
3. **`vision_ocr.swift`** — pre-existing REGISTRY.md entry outside Phase 0 audit scope; flagged but not fixed.

### Files modified this session

- `agents/AGENT_DRAWING_EXTRACT.md` — Phase 2.8b backfill step added + tool-deps table updated
- `tools/drawing_extract/normalize_equipment_stub_layout.py` — inline YAML list parser fix
- `AGENTS.md` — DRAWING_EXTRACT + drawing-extract-page entries updated
- `tools/EXTERNAL_TOOLS.md` — DRAWING_EXTRACT section rewritten for v2 architecture
- `docs/DBM_Agent_Instruction_Architecture.md` — DRAWING_EXTRACT + DRAWING_EXTRACT_PAGE entries updated
