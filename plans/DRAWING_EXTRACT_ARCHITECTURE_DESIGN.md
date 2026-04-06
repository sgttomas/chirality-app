# DRAWING_EXTRACT Architectural Design — Phase 2 Deliverables

**Status:** Design artifacts only. No file edits. Locked contracts for Phase 3+ implementation.
**Date:** 2026-04-05
**Source plan:** `/Users/ryan/.claude/plans/giggly-munching-pascal.md`
**Input:** `plans/DRAWING_EXTRACT_TOOL_AUDIT.md` + Phase 1 crop-adequacy spike findings

---

## Deliverable 1 — Drawing-type + extraction-target registry

Implemented in this slice: `PFD` only. Other types stubbed with fail-fast at orchestrator entry.

| drawing_type | status | extraction_target | status | Notes |
|--------------|--------|-------------------|--------|-------|
| `PFD` | IMPLEMENTED | `top_equipment_header_basic` | IMPLEMENTED | Subsumes legacy `top_equipment_header_with_dwg`; 4 base columns |
| `PFD` | IMPLEMENTED | `top_equipment_header_detailed` | IMPLEMENTED | Adds catalog + extra descriptor fields |
| `PFD` | — | `title_block_metadata` | STUBBED (future) | Extract drawing number, revision, date, scale |
| `PFD` | — | `body_process_lines` | STUBBED (future) | Extract process stream IDs + endpoints |
| `PFD` | — | `vessel_internals` | STUBBED (future) | Extract internal callouts |
| `P_AND_ID` | STUBBED | — | — | Fail fast at orchestrator pre-flight |
| `ISOMETRIC` | STUBBED | — | — | Fail fast at orchestrator pre-flight |
| `GA` | STUBBED | — | — | Fail fast at orchestrator pre-flight |

**Valid combinations this slice:** `(PFD, top_equipment_header_basic)`, `(PFD, top_equipment_header_detailed)`. Any other combination rejects at orchestrator Phase 0 pre-flight.

---

## Deliverable 2 — Core-vs-repertoire protocol split + PFD hook mapping

### Core phases (type-agnostic, implemented once in orchestrator)

| Phase | Purpose |
|-------|---------|
| Phase 0 | Pre-flight validation: DRAWING_TYPE supported; EXTRACTION_TARGET valid for drawing_type; stubbed-type fail-fast; compatibility shim remap |
| Phase 1 | Rasterize pages |
| Phase 1.5 | Crop preparation (dispatches type/target crop hook) |
| Phase 2 | Page-worker dispatch with target-aware per-page artifact paths + resume-validation against stub frontmatter |
| Phase 2.5 | Title-block verification (type/target hook, optional) |
| Phase 2.6 | Stub-count / QA reporting (type/target hook) |
| Phase 2.7 | Sanitization (type/target hook) |
| Phase 2.7b | Schema-consistency validation (core) |
| Phase 2.8 | Recovery fallback (type/target hook, invoked only on operator opt-in) |
| Phase 2.9 | Final QA reporting (type/target hook) |
| Phase 3 | Assembly (core; calls type/target assembly hook) |
| Phase 3.5 | Optional merge (core; gated on `MERGE_EXISTING_DATA=true`) |
| Phase 4 | Final report (core) |

### PFD repertoire hook registry

| Hook point | PFD `top_equipment_header_basic` | PFD `top_equipment_header_detailed` |
|------------|------------------------------------|-------------------------------------|
| Crop prep | `prepare_header_crops.py` (default geometry 0.18) | `prepare_header_crops.py` (default 0.18 + per-page overrides on failure) |
| Page-worker logic | drawing-extract-page skill, basic target | drawing-extract-page skill, detailed target |
| Title-block verify | `extract_pdf_titleblock_text.py` (optional) | `extract_pdf_titleblock_text.py` (optional) |
| Stub-count QA | `report_stub_counts.py` (basic metrics) | `report_stub_counts.py` (detailed metrics: capture rate, required-field warnings, identical-value heuristic) |
| Sanitization | `sanitize_equipment_stubs.py` (tag/name filtering) | `sanitize_equipment_stubs.py` (tag/name filtering, preserves descriptor columns) |
| Recovery fallback | `recover_deepcut_multiblock_headers.py` (opt-in, Deepcut only) | `recover_deepcut_multiblock_headers.py` (opt-in, Deepcut only) |
| Schema-consistency validation | (not applicable; fixed schema) | `validate_detailed_schema.py` |
| Assembly (CSV) | `assemble_equipment_csv.py` (4 base columns) | `assemble_equipment_csv.py` (base + catalog + extra) |
| Assembly (MD) | `assemble_equipment_markdown.py` (4 base columns) | `assemble_equipment_markdown.py` (base + catalog + extra) |
| Metadata backfill | `backfill_stub_system_names.py` (system_name only) | `backfill_stub_system_names.py` (system_name + optionally other fields) |
| Duplicate flagging | `flag_duplicate_equipment_csv.py` (key=equipment_number) | `flag_duplicate_equipment_csv.py` (key=equipment_number) |
| Dedupe (optional, downstream) | `dedupe_equipment_csv.py` (key=equipment_number) | `dedupe_equipment_csv.py` (key=equipment_number) |
| Merge (repertoire-scoped) | `merge_equipment_detailed.py` + `flag_merge_conflicts.py` | `merge_equipment_detailed.py` + `flag_merge_conflicts.py` |

---

## Deliverable 3 — Canonical stub metadata frontmatter schema (v1)

YAML frontmatter at top of every detailed-mode markdown_stub:

```yaml
---
drawing_type: PFD
extraction_target: top_equipment_header_detailed
source_pdf: PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined.pdf
source_page: 7
requested_known_fields:
  - equipment_type
  - duty_text
  - capacity_text
requested_extra_fields:
  - name: material_text
    description: "stainless steel grade or material designation printed beneath equipment item"
required_fields: []
drawing: PFD-235633-1000-001
system_name: INLET PIG RECEIVER
status: SUCCESS
---
```

For `top_equipment_header_basic` (simpler):

```yaml
---
drawing_type: PFD
extraction_target: top_equipment_header_basic
source_pdf: PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined.pdf
source_page: 7
drawing: PFD-235633-1000-001
system_name: INLET PIG RECEIVER
status: SUCCESS
---
```

**Required keys (both targets):** `drawing_type`, `extraction_target`, `source_pdf`, `source_page`, `drawing`, `system_name`, `status`.

**Required keys (detailed only):** `requested_known_fields`, `requested_extra_fields`, `required_fields` (may be empty lists).

**Status values:** `SUCCESS`, `NO_FINDINGS`, `FAILED_INPUTS`, `FAILED` (unchanged from current skill contract).

**Body structure (unchanged pattern):**
- H1 page title
- Markdown findings table (columns = base + requested_known_fields + requested_extra_fields.name for detailed; 4 base columns for basic)
- NO_FINDINGS narrative (when applicable)
- Extraction status line

---

## Deliverable 4 — Per-page artifact path contract

```
{SOURCE_DIR}/
  {DRAWING_TYPE}/
    {EXTRACTION_TARGET}/
      {PDF_STEM}_page_{NNNN}_stub.md                                          # per-page stub
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}.md                      # combined MD
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}.csv                     # combined CSV
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_duplicate_flags.csv     # dup flags
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_schema_validation.csv   # validator report (detailed only)
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_merge_result.csv        # merge output (opt)
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_merge_conflicts.csv     # merge conflicts (opt)
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_merge_unmatched_extracted.csv  # unmatched extracted (opt)
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_merge_unmatched_existing.csv   # unmatched existing (opt)
```

Example (West Doe Deepcut, detailed target, pages 7-16):
```
domain-test/domains/West_Doe_Deepcut_DBM/_Sources/
  PFD/
    top_equipment_header_detailed/
      PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined_page_0007_stub.md
      ...
      PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined_combined_pages_0007_0016.md
      PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined_combined_pages_0007_0016.csv
      ...
```

**Rationale:** per-target subdirectory prevents cross-target artifact collisions (basic and detailed do not share stub namespace). `PDF_STEM` is the PDF filename without extension.

**Backward-compatibility:** legacy artifacts at `{SOURCE_DIR}/{PDF_STEM}_page_{NNNN}_equipment_stub.md` are left in place; the new path is distinct, not a rename.

---

## Deliverable 5 — Resume-safety contract

When an orchestrator run resumes (finds existing per-page stub files), it validates each stub's YAML frontmatter against the current run's parameters:

| Frontmatter field | Must match current run |
|-------------------|-------------------------|
| `drawing_type` | MUST equal current `DRAWING_TYPE` |
| `extraction_target` | MUST equal current `EXTRACTION_TARGET` |
| `source_pdf` | MUST match current PDF filename |
| `source_page` | MUST equal the page number in the filename |
| `requested_known_fields` | MUST equal current run's list (detailed only) |
| `requested_extra_fields` | MUST equal current run's list by name + description (detailed only) |
| `required_fields` | MUST equal current run's list (detailed only) |

**On mismatch:** orchestrator rejects the run with error `existing stub at {path} has schema mismatch; options: (1) clear stubs in target subdirectory, (2) dispatch to a new SOURCE_DIR, or (3) rerun with matching parameters`.

**On match:** stub is reused (existing behavior). Only missing pages are dispatched to page workers.

**On missing stub:** page is queued for extraction (existing behavior).

---

## Deliverable 6 — Target-driven column order

### `top_equipment_header_basic` (4 columns, fixed)

| Position | Column |
|---------:|--------|
| 1 | `equipment_number` |
| 2 | `equipment_name` |
| 3 | `system_name` |
| 4 | `drawing` |

Combined CSV also includes `source_page` (5 columns total); stub table has 4 (`source_page` is in frontmatter).

### `top_equipment_header_detailed` (variable columns)

| Section | Columns | Order |
|---------|---------|-------|
| Base (always present) | `equipment_number`, `equipment_name`, `system_name`, `drawing` | Fixed order as listed |
| Catalog (per run) | subset of `requested_known_fields` | Canonical catalog order (see below) |
| Extra (per run) | `requested_extra_fields[*].name` values | Request order (as provided in brief) |

**Canonical catalog order (v1):**
1. `equipment_type`
2. `duty_text`
3. `capacity_text`
4. `power_text`
5. `size_text`
6. `material_text`

Combined CSV also includes `source_page` at the end.

**Note — catalog expansion based on spike:** `material_text` promoted from EXTRA_FIELD example to v1 known-field catalog. Spike evidence: present in 10+/19 Deepcut pages and 7+/9 descriptor-rich Comp & Liquids pages. Includes "CARBON STEEL", "316SS", "SUREFLOW 0300BF30OSS", etc.

---

## Deliverable 7 — Name-collision rules for EXTRA_FIELDS

Every element of `requested_extra_fields` has shape `{name, description}`.

**`name` normalization:** lowercase ASCII letters + digits + underscores only. Regex: `^[a-z][a-z0-9_]*$`. Max length: 40 characters.

**Collision rules (fail-fast at orchestrator Phase 0 pre-flight):**

| Collision type | Behavior |
|----------------|----------|
| `name` matches base column (`equipment_number`, `equipment_name`, `system_name`, `drawing`, `source_page`) | REJECT with error: `extra field name '{name}' collides with base column` |
| `name` matches any catalog field (whether requested or not) | REJECT with error: `extra field name '{name}' collides with known-field catalog entry '{field}'` |
| Two extra fields share the same `name` in one run | REJECT with error: `duplicate extra field name '{name}'` |
| `name` does not match regex | REJECT with error: `invalid extra field name '{name}'; must match /^[a-z][a-z0-9_]*$/` |

**`description` constraints:** non-empty; max 200 chars; single line (no newlines).

---

## Deliverable 8 — Compatibility shim semantics

### Orchestrator level

When a brief provides `EXTRACTION_MODE=top_equipment_header_with_dwg`:
1. Log deprecation warning: `EXTRACTION_MODE is deprecated; use DRAWING_TYPE=PFD + EXTRACTION_TARGET=top_equipment_header_basic. Remapping for this run.`
2. Set `DRAWING_TYPE=PFD`, `EXTRACTION_TARGET=top_equipment_header_basic`.
3. Proceed with normal Phase 0 validation.

### Skill (page worker) level

Same remap applied when `drawing-extract-page` receives a brief with `EXTRACTION_MODE=top_equipment_header_with_dwg` (direct dispatch not via orchestrator).

### Scope of shim

- **Only** `EXTRACTION_MODE=top_equipment_header_with_dwg` is remapped.
- Any other legacy `EXTRACTION_MODE` value rejects with: `unknown EXTRACTION_MODE '{value}'; use DRAWING_TYPE + EXTRACTION_TARGET`.
- Shim is advertised in runbook as a one-slice transitional capability. Hard cutover planned for a follow-on slice.

### Interaction with other parameters

If a brief provides BOTH `EXTRACTION_MODE=top_equipment_header_with_dwg` AND `DRAWING_TYPE`/`EXTRACTION_TARGET`, orchestrator prefers the new parameters and warns: `both legacy and new parameters provided; using new parameters`.

---

## Deliverable 9 — Stubbed-type fail-fast semantics

Orchestrator Phase 0 pre-flight validation sequence:

1. Resolve effective `DRAWING_TYPE` (applying compatibility shim if needed).
2. If `DRAWING_TYPE` not in `{PFD, P_AND_ID, ISOMETRIC, GA}`: REJECT with `unknown drawing_type '{value}'; valid: PFD (implemented), P_AND_ID/ISOMETRIC/GA (stubbed)`.
3. If `DRAWING_TYPE ∈ {P_AND_ID, ISOMETRIC, GA}`: REJECT with `drawing_type '{type}' is registered but not implemented; see 'How to add a new drawing type' in AGENT_DRAWING_EXTRACT.md`.
4. Resolve effective `EXTRACTION_TARGET`.
5. If `EXTRACTION_TARGET` not valid for `DRAWING_TYPE`: REJECT with `extraction_target '{target}' not valid for drawing_type '{type}'; valid targets: {list}`.
6. Only if (2), (3), (4), (5) all pass does orchestrator proceed to rasterization.

**No rasterization work is performed before pre-flight completes.** No work-dir side effects. No crop generation. Fail-fast path costs ~100ms.

---

## Deliverable 10 — Combined-CSV schema contract

### `top_equipment_header_basic` combined CSV

```
equipment_number,equipment_name,system_name,drawing,source_page
PR-1010-2,PIG RECEIVER,INLET PIG RECEIVER,PFD-242510-1000-001,7
...
```

Header line: `equipment_number,equipment_name,system_name,drawing,source_page`

Row shape: one row per extracted equipment finding. NO_FINDINGS pages produce zero rows (reported separately in run log).

### `top_equipment_header_detailed` combined CSV

Header line is **run-dependent**. Fixed ordering:
```
equipment_number,equipment_name,system_name,drawing,<requested_known_fields in canonical order>,<requested_extra_fields in request order>,source_page
```

Example with `REQUESTED_KNOWN_FIELDS=[equipment_type, duty_text]` + `EXTRA_FIELDS=[{name: material_text,...}]`:
```
equipment_number,equipment_name,system_name,drawing,equipment_type,duty_text,material_text,source_page
V-1600-2,INLET SEPARATOR,INLET SEPARATION,PFD-242510-1100-001,VESSEL,3-PHASE SEPARATION,316SS,22
...
```

Blank cells for requested-but-not-visible values (not null, not "NO_VALUE" — empty string).

### Downstream tool contract

W3 (merge) and other CSV-consuming tools read the combined CSV using `csv.DictReader`. The required key columns for merge are:
- `equipment_number` (merge key, always present)
- Optional provenance for conflict-reporting: `equipment_name`, `drawing`, `source_page`

Merge does not depend on detailed-mode catalog/extra columns; merges passthrough any columns present in both inputs.

---

## Deliverable 11 — Equivalence gate spec (4-part, post-4b)

Run at Gate 4c — **after** W2 assembly + W4 QA outputs exist.

### Input
- Reference: `domain-test/domains/West_Doe_Deepcut_DBM/_Sources/PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined_equipment_combined_pages_0007_0106.csv` (legacy combined CSV)
- Reference dup-flags: `domain-test/domains/West_Doe_Deepcut_DBM/_Sources/PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined_equipment_combined_pages_0007_0106_duplicate_flags.csv`
- Legacy NO_FINDINGS page set: derived by grepping existing per-page equipment_stub.md files for `Extraction status: NO_FINDINGS`
- Candidate: new-framework output at `domain-test/domains/West_Doe_Deepcut_DBM/_Sources/PFD/top_equipment_header_basic/...combined_pages_0007_0106.*`

### Gate 1 — Row set equivalence
Compare 4-tuple `(equipment_number, equipment_name, drawing, source_page)` sets:
```sh
diff <(cut -d, -f1,2,4,5 legacy.csv | sort -u) <(cut -d, -f1,2,4,5 new.csv | sort -u)
```
**Pass criterion:** zero diff. Any added or missing tuples = fail.

### Gate 2 — NO_FINDINGS page set equivalence
Compare the set of pages reported as NO_FINDINGS:
```sh
python3 tools/drawing_extract/report_stub_counts.py <new_source_dir> /tmp/new_counts.csv --start-page 7 --end-page 106
diff <(awk -F, '$2=="NO_FINDINGS"{print $1}' legacy_counts.csv | sort) \
     <(awk -F, '$2=="NO_FINDINGS"{print $1}' /tmp/new_counts.csv | sort)
```
**Pass criterion:** zero diff.

### Gate 3 — Provenance field equivalence
Per-row match on (`drawing`, `system_name`) — by (`equipment_number`, `source_page`) key:
```sh
python3 <(cat <<'EOF'
import csv
legacy = {(r['equipment_number'], r['source_page']): (r['drawing'], r['system_name']) for r in csv.DictReader(open('legacy.csv'))}
new = {(r['equipment_number'], r['source_page']): (r['drawing'], r['system_name']) for r in csv.DictReader(open('new.csv'))}
mismatches = [k for k in legacy if k in new and legacy[k] != new[k]]
missing = [k for k in legacy if k not in new]
added = [k for k in new if k not in legacy]
print(f"mismatches={len(mismatches)} missing={len(missing)} added={len(added)}")
if mismatches: [print(f"  MISMATCH {k}: legacy={legacy[k]} new={new[k]}") for k in mismatches[:10]]
EOF
)
```
**Pass criterion:** zero mismatches, missing, added.

### Gate 4 — Duplicate-flag CSV equivalence
```sh
diff <(sort legacy_duplicate_flags.csv) <(sort new_duplicate_flags.csv)
```
**Pass criterion:** zero diff (modulo ordering). Flagged equipment_numbers and duplicate_type classifications must match.

### Gate outcome
All 4 gates must pass. Any failure blocks progress to Phase 5 until root-caused and either (a) fixed in W1/W2/W4, or (b) explicitly documented as an intentional divergence with rationale.

---

## Additional architectural notes (beyond the 11 deliverables)

### Per-page crop override workflow (from Phase 1 gate)

When extraction fails or under-captures on specific pages:

1. **Detection**: `report_stub_counts.py` QA output flags suspicious pages (low row count, NO_FINDINGS where findings expected, blank primary keys). Human inspects flagged page's rendered image vs. existing crops.

2. **Diagnosis**: if descriptor text extends beyond current crop bounds → geometry override needed for this page.

3. **Override invocation**:
   ```sh
   python3 tools/drawing_extract/prepare_header_crops.py <work_dir> --pages <N> --header-height-ratio 0.22
   ```
   This overwrites the crops for just page N with the new ratio. Other pages are untouched.

4. **Re-extraction**: delete the stub for page N from the target subdirectory, re-dispatch DRAWING_EXTRACT with the same parameters. Only page N re-extracts (other stubs are reused via resume).

5. **Reproducibility**: log per-page override decisions in a `page_crop_overrides.md` note alongside the work-dir, so reruns can reproduce the overrides.

This is **documentation-only** (no new code in v1) — the existing CLI already supports page-specific crop overrides via `--pages` + `--header-*-ratio` flags.

### Catalog expansion rationale

V1 catalog = `[equipment_type, duty_text, capacity_text, power_text, size_text, material_text]` (6 fields).

`material_text` added based on spike evidence:
- Deepcut: observed in 10+/19 sampled descriptor-rich pages
- Comp & Liquids: observed in 7+/9 sampled descriptor-rich pages
- Values like "CARBON STEEL", "316SS", "CS", specific material callouts

Promoted from EXTRA_FIELD example to known-field catalog with semantic definition:
> `material_text`: material of construction, specification, or grade callout (e.g., "CARBON STEEL", "316SS", "DUPLEX", "SUREFLOW 0300BF30OSS")

### Future catalog expansion policy

When a new catalog field is added:
- Skill version bumps (`chirality-skill-version: "2"` → `"3"`)
- Historical stubs produced under prior versions remain readable (the `extraction_target` + frontmatter schema still parse)
- Legacy catalog fields remain in the catalog forever (no removals)
- Addition requires SKILL.md edit + validator regression

### Duplicate handling policy (clarification)

`flag_duplicate_equipment_csv.py` flags duplicates; `dedupe_equipment_csv.py` removes them. Default workflow:
- Always run dup-flag (post-assembly)
- Only run dedupe when operator explicitly requests it (default: preserve duplicates + flag them)

This preserves the existing convention from `AGENT_DRAWING_EXTRACT.md`.

---

## Phase 2 completion

All 11 deliverables locked + additional architectural notes captured. Phase 3 (skill contract implementation) proceeds with this design as blueprint.

**Gate for Phase 2:** Human review of this document. Approval required before Phase 3 file edits begin.

EOF
