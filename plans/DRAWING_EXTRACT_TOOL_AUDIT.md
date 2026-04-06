# DRAWING_EXTRACT Tool Audit — Phase 0 Classification

**Status:** Complete. Classification only; no retirement/archive actions taken.
**Date:** 2026-04-05
**Context:** Phase 0 of the plan at `/Users/ryan/.claude/plans/giggly-munching-pascal.md` — generalizing DRAWING_EXTRACT from PFD top-header equipment extractor into drawing-type-aware workflow.

---

## Classification classes

| Class | Meaning |
|-------|---------|
| `CORE-GENERAL` | Tool generalizes to all drawing types; lives in core pipeline layer |
| `REFACTOR-TO-GENERALIZE` | Tool has a generalizable core; refactor to drawing-type + target-awareness |
| `PFD-REPERTOIRE` | PFD-specific; belongs in PFD repertoire hooks |
| `PROJECT-FALLBACK` | West-Doe-specific; retained as project-scoped fallback |
| `RECOMMEND-RETIRE` | No value in general framework (no tools currently flagged) |

---

## Classification matrix

| # | Tool | Current scope | Classification | Rationale |
|---|------|---------------|----------------|-----------|
| 1 | `prepare_header_crops.py` | PFD-specific (top-header + bottom-right titleblock geometry) | **REFACTOR-TO-GENERALIZE** | Logic is purely geometric (ratio-driven crops); nothing equipment-specific inside. Output filenames (`top_header`, `titleblock`) and hardcoded header-at-top / titleblock-at-bottom-right geometry are PFD-top-header assumptions. P&IDs, isometrics, GA drawings crop different regions. |
| 2 | `normalize_equipment_stub_layout.py` | Equipment-specific (hardcoded fields + 4-column schema) | **REFACTOR-TO-GENERALIZE** | Stub parser/renderer and table schema are equipment-PFD targets (`equipment_number`, `equipment_name`, `system_name`, `drawing`; `DWG NO.:` label). Tool *shape* — canonicalize page-level stubs to deterministic layout — is drawing-general. |
| 3 | `sanitize_equipment_stubs.py` | PFD equipment-specific (West-Doe-flavored rule sets) | **PFD-REPERTOIRE** | Entire body is target-specific deterministic QC: `INSTRUMENT_PREFIXES`, `EQUIPMENT_PREFIX_STOP_WORDS`, `NOTE_NAME_STARTS`/`_CONTAINS` drawn from Deepcut PFD noise. Outer loop is generalizable, but rule body is irreducibly PFD-equipment knowledge. |
| 4 | `assemble_equipment_csv.py` | Equipment-specific 5-column output schema | **REFACTOR-TO-GENERALIZE** | Per-page aggregation, dual-source parsing, NO_FINDINGS handling, missing-page reporting are drawing-general. Equipment-specific: column set, stub table signatures, `_equipment_stub.md` filename conventions. |
| 5 | `assemble_equipment_markdown.py` | Equipment-specific 4-column output schema + PFD-specific narrative | **REFACTOR-TO-GENERALIZE** | Mirror of CSV assembler. Near-duplicate; merits consolidation behind one schema-driven assembler with `--format csv\|md`. |
| 6 | `report_stub_counts.py` | Equipment-specific columns (via parse_stub import) | **REFACTOR-TO-GENERALIZE** | QA-coverage concept (row count, blank-tag count, status) is drawing-general. Equipment-specificity via imported `parse_stub` + output column names. "blank_tag" becomes "blank_primary_key" per target. |
| 7 | `flag_duplicate_equipment_csv.py` | Nearly drawing-general; equipment labels in output columns only | **REFACTOR-TO-GENERALIZE** | Already accepts `--key`. Classification compares `equipment_name` + `drawing` (equipment-labeled). Cheapest generalization: add `--conflict-fields` + `--output-key-label`. |
| 8 | `dedupe_equipment_csv.py` | drawing-general (equipment-specific default key) | **REFACTOR-TO-GENERALIZE** | Logic is a generic "dedupe CSV by key, keep first occurrence". Only `--key equipment_number` default + filename encode equipment-specificity. |
| 9 | `backfill_stub_system_names.py` | equipment-specific / PFD-leaning | **REFACTOR-TO-GENERALIZE** | Stub-upsert mechanics are generic metadata-backfill operations. Hard-coded to `system_name` attribute and 3-vs-4-column equipment schema. Concept applies to any drawing_type. |
| 10 | `extract_pdf_titleblock_text.py` | PFD-specific, West-Doe-flavored | **REFACTOR-TO-GENERALIZE** | `pdftotext -layout` harness and regex harvesting are drawing-general. `PROJECT_TITLE_RE` hardcodes West Doe string, `TITLE_SUFFIX_RE` hardcodes PFD. Demotable to per-target title-block parser hook with caller-supplied anchors. |
| 11 | `recover_deepcut_multiblock_headers.py` | West-Doe-specific, PFD-specific, fixture-driven | **PROJECT-FALLBACK** | Entire `PAGE_FIXTURES` dict is hand-curated equipment rows tied to one project PDF. Cannot generalize without becoming a different tool. Filename contains `deepcut`. |
| 12 | `reconcile_west_doe_comp_and_liquids_packages.py` | West-Doe-specific (242510 project) | **PROJECT-FALLBACK** | Hard-codes 9 package-name constants + inference rules keyed to drawing-number prefix `PFD-242510-`. `MANUAL_ADDITIONS` is 16 hand-curated rows. Filename contains `west_doe`. |
| 13 | `report_west_doe_comp_and_liquids_package_matches.py` | West-Doe-specific (242510 project) | **PROJECT-FALLBACK** | Directly imports West-Doe package constants + `MANUAL_ADDITIONS`. `PACKAGE_CANDIDATE_ROWS` hardcodes master-CSV row numbers. Report shape welded to West-Doe master-CSV column schema. |

---

## Summary statistics

| Classification | Count | Tools |
|----------------|------:|-------|
| `CORE-GENERAL` | 0 | — |
| `REFACTOR-TO-GENERALIZE` | 9 | 1, 2, 4, 5, 6, 7, 8, 9, 10 |
| `PFD-REPERTOIRE` | 1 | 3 |
| `PROJECT-FALLBACK` | 3 | 11, 12, 13 |
| `RECOMMEND-RETIRE` | 0 | — |
| **Total** | **13** | |

---

## Cross-tool observations

1. **No pure core-general tools.** Every drawing-extract tool currently encodes equipment-schema, PFD-geometry, or West-Doe-project assumptions. The "core pipeline" layer will emerge from refactoring 9 tools against a shared extraction-target schema, not from tools that already live there.

2. **Shared generalization seam: extraction-target schema descriptor.** An extraction-target schema (header fields, table column list, filename suffix, primary-key field, conflict fields) flows through parse/normalize/report/assemble. Introducing this schema descriptor unblocks 5+ refactors at once.

3. **Filename conventions are a hidden coupling.** `_equipment_stub.md`, `_equipment_rows.csv`, `top_header`/`titleblock` crop names, literal markdown table-header strings (`| equipment_number | equipment_name | ...`) are repeated across five tools. Parameterizing them in one place (a target profile) removes the duplication.

4. **assemble_equipment_csv.py + assemble_equipment_markdown.py are near-duplicates** differing only in output format. Merit consolidation during refactor into one schema-driven assembler with `--format csv|md`.

5. **Geometry (crop ratios) and semantics (equipment rule sets) need different generalization strategies.** Crop geometry belongs in a drawing-type profile (PFD/P&ID/iso/GA). Semantic rule sets (instrument-prefix blocklists, note-like-name detectors) belong in per-target hook modules that live in the repertoire layer.

6. **Fixture-driven project fallbacks are not retirement candidates.** `recover_deepcut_multiblock_headers.py`, `reconcile_west_doe_comp_and_liquids_packages.py`, `report_west_doe_comp_and_liquids_package_matches.py` are irreducibly West-Doe-scoped. They belong as project-fallback hooks invoked only when operators explicitly enable them per project.

7. **Title-block verification is drawing-general but currently West-Doe-anchored.** `extract_pdf_titleblock_text.py` has a drawing-general harness (pdftotext + regex) but carries a hardcoded West Doe project-title anchor. Refactor lifts anchors into per-target title-block parser hooks.

---

## Implications for Phase 4 worker assignments

Based on this classification, the Phase 4 worker groupings remain as planned:

| Worker | Tools (classification) | Count |
|--------|------------------------|------:|
| W1 schema core | `normalize_equipment_stub_layout.py` (REFACTOR) | 1 |
| W2 assembly / validator | `assemble_equipment_csv.py` + `assemble_equipment_markdown.py` (REFACTOR) + `validate_detailed_schema.py` (NEW) | 3 |
| W3 merge suite | `merge_equipment_detailed.py` (NEW) + `flag_merge_conflicts.py` (NEW) | 2 |
| W4 QA / sanitizer | `sanitize_equipment_stubs.py` (PFD-REPERTOIRE) + `report_stub_counts.py` (REFACTOR) | 2 |

**Additional tools identified by audit** (not in original Phase 4 scope — evaluate during architectural design):
- `dedupe_equipment_csv.py` (REFACTOR) — candidate for core-pipeline dedup step
- `backfill_stub_system_names.py` (REFACTOR) — candidate for target-aware metadata backfill
- `flag_duplicate_equipment_csv.py` (REFACTOR) — already parameterized with `--key`, cheapest refactor
- `prepare_header_crops.py` (REFACTOR) — PFD crop-geometry profile; refactor to crop-spec registry

**Project-fallbacks (no refactor, keep as-is):**
- `recover_deepcut_multiblock_headers.py`
- `reconcile_west_doe_comp_and_liquids_packages.py`
- `report_west_doe_comp_and_liquids_package_matches.py`

**Recommendation for Phase 2 architectural design:** consider whether to expand Phase 4 worker scope to include the additional REFACTOR tools (items above), or defer them to a follow-on refactor slice. The nine REFACTOR-TO-GENERALIZE tools naturally cluster around a shared extraction-target schema descriptor — doing them together may be cheaper than sequencing.

---

## Out of scope (this slice)

- Retirement/archive of any tool
- Implementation of refactors (Phase 4 work)
- Drawing-type profile definitions for P&ID, isometric, GA
- Project-fallback hook registration contract

EOF
