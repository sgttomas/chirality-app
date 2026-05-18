---
name: pandid-valve-tile
description: OBSOLETE legacy per-tile P&ID valve candidate extraction retained for historical readability; new runs use pandid-valve-symbol-instance.
compatibility: Historical only; not dispatched by DRAWING_EXTRACT for new P_AND_ID valve_count_basic or valve_count_detailed runs
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL - pandid-valve-tile

OBSOLETE: This legacy skill is retained only to read historical stubs. New P&ID valve runs must dispatch `pandid-valve-symbol-instance` and must not auto-migrate legacy rows into `symbol_instance_v1`.

## Purpose

Extract valve candidate rows from one P&ID tile image. The tile contains a larger read zone and a smaller emit zone drawn by deterministic preprocessing. The skill may use the read zone for context, but it emits rows only for valve symbols whose visual center lies inside the emit zone.

This skill supports two modes:

- `basic` - count-oriented candidate rows with coarse valve category, visible tag, location bucket, and issue flags.
- `detailed` - basic columns plus valve size, valve type, and actuation where visible.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the `DRAWING_EXTRACT` orchestrator.

## Inputs

### Required

- `RuntimeOverrides.SOURCE_PDF_NAME`
- `RuntimeOverrides.PAGE_NUM`
- `RuntimeOverrides.TILE_ID`
- `RuntimeOverrides.TILE_IMAGE_PATH`
- `RuntimeOverrides.OUTPUT_PATH`
- `RuntimeOverrides.MODE` - `basic` or `detailed`
- `RuntimeOverrides.TILE_GEOMETRY` - `tile_grid`, `body_box_px`, `body_exclusions`, `read_box_px`, `emit_box_px`, `overlap_px`, `mini_grid`

### Optional

- `RuntimeOverrides.ALLOW_REFERENCE_SHEETS` - default `false`.
- `RuntimeOverrides.SCOPE_FILE` - optional operator-selected page scope provenance.
- `RuntimeOverrides.BASIC_REFERENCE_RUN` - optional detailed-pass provenance for the basic run used for reconciliation.
- `RuntimeOverrides.BASIC_COUNTS_CSV` - optional detailed-pass provenance for the basic counts CSV used for reconciliation.

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `MODE` | Extraction mode | Required | `basic`, `detailed` |
| `TILE_IMAGE_PATH` | Tile image with emit-zone overlay | Required | Existing image path |
| `TILE_ID` | Page/tile identifier | Required | `page_NNNN_rRRcCC` |
| `TILE_GEOMETRY` | Tile geometry metadata | Required | See plan schema |
| `ALLOW_REFERENCE_SHEETS` | Process legend/reference tiles | `false` | Boolean |

## Tool usage

No deterministic tools are invoked by this skill. Tile preparation, validation, assembly, aggregation, duplicate flagging, and reconciliation belong to deterministic tools invoked by the orchestrator.

## Method

1. Validate runtime inputs.
2. Read `TILE_IMAGE_PATH`.
3. If the tile clearly belongs to a legend, symbols, abbreviation, or reference sheet and `ALLOW_REFERENCE_SHEETS` is not true, emit `NO_FINDINGS_REFERENCE` with `reason=legend_or_reference_sheet`.
4. Inspect the read zone for context.
5. Emit only valve candidates whose visual center is inside the outlined emit zone.
6. Use the 5x5 overlay to set `approx_location_in_emit_box` (`A1` through `E5`).
7. In `detailed` mode, fill size/type/actuation fields only when visible. Otherwise emit `TBD`.
8. Write exactly one markdown stub at `OUTPUT_PATH`.

## Controlled values

`valve_category`:

- `manual_block`
- `manual_throttle`
- `check`
- `control`
- `esd_block`
- `relief`
- `unknown`

`tag_basis`:

- `visible_near_symbol`
- `inferred_from_designation`
- `TBD`

`issue_flags` initial vocabulary:

- `BOUNDARY_REVIEW`
- `LOW_LEGIBILITY`
- `AMBIGUOUS_SYMBOL`
- `CLASSIFICATION_UNCERTAIN`
- `SIZE_NOT_LEGIBLE`
- `LINE_NUMBER_NOT_LEGIBLE`

Unknown future flags may be emitted, but validators will record warnings.

## Output format

Every output stub begins with YAML frontmatter matching the runtime geometry. Body columns:

Basic:

```text
valve_index | valve_category | valve_tag | tag_basis | approx_location_in_emit_box | issue_flags | notes
```

Detailed adds:

```text
valve_size_text | valve_type_code | valve_type_name | actuation
```

`issue_flags` is serialized as `[FLAG_A, FLAG_B]`; empty is `[]`.

## Run statuses

- `SUCCESS` - one or more candidates emitted.
- `NO_FINDINGS` - no valve candidates in the emit zone.
- `NO_FINDINGS_REFERENCE` - reference/legend page detected and not overridden.
- `FAILED` - tile could not be interpreted.
- `FAILED_INPUTS` - missing or invalid runtime inputs.

## Non-negotiable constraints

- One invocation handles one tile.
- The emit-zone rule is mandatory.
- Visible-but-outside candidates are not emitted as rows.
- Pixel coordinates are not requested or used.
- `approx_location_in_emit_box` must be one of `A1..E5`.
- Tags are extracted when visible but are never required.
- Unknown values are `TBD`.
- The skill writes only `OUTPUT_PATH`.

## QA expectations

- Frontmatter geometry matches the run.
- `finding_count` equals the number of emitted body rows.
- `NO_FINDINGS` and `NO_FINDINGS_REFERENCE` have `finding_count: 0`.
- Basic mode does not emit detailed columns.
- Detailed mode includes detailed columns.
- Every emitted candidate has a non-empty `valve_index`, `valve_category`, `approx_location_in_emit_box`, and `issue_flags`.
