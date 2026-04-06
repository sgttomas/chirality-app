#!/usr/bin/env python3
"""
normalize_equipment_stub_layout.py
Canonical parser/renderer for per-page drawing-extract equipment stubs.

Supports two stub formats:
- v2 (drawing-type-aware): YAML frontmatter + variable-column findings table
- legacy (pre-v2): bullet-list header + fixed 4-column findings table

Auto-detects input format. Renders in v2 format when data dict carries
`format_version="v2"` (or at minimum `drawing_type` + `extraction_target`).
Otherwise renders in legacy format so pre-v2 callers continue to round-trip.

This module is the frozen contract for W2/W3/W4 tooling per DRAWING_EXTRACT
Phase 4a. The canonical dict schema, column derivation, and path resolvers
defined here are the interface consumed by assembly, QA, sanitation, and
merge tools.

CLI modes:
- In-place legacy normalization (default, back-compat): reads legacy stubs
  from `{source_dir}/{pdf_stem}_page_{NNNN}_equipment_stub.md`, rewrites
  canonical legacy layout in place.
- Legacy->v2 migration: reads legacy stubs and writes v2 stubs to
  `{source_dir}/{drawing_type}/{extraction_target}/{pdf_stem}_page_{NNNN}_stub.md`.
  Activated by supplying `--drawing-type` + `--extraction-target`.

Exit codes: 0 success, 2 setup error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Contract constants (frozen at Phase 4a for W2/W3/W4 consumption)
# ---------------------------------------------------------------------------

BASE_COLUMNS: tuple[str, ...] = (
    "equipment_number",
    "equipment_name",
    "system_name",
    "drawing",
)

KNOWN_FIELD_CATALOG: tuple[str, ...] = (
    "equipment_type",
    "equipment_description",
    "capacity_text",
    "power_text",
)

DRAWING_TYPES: frozenset[str] = frozenset({"PFD", "P_AND_ID", "ISOMETRIC", "GA"})
DRAWING_TYPES_IMPLEMENTED: frozenset[str] = frozenset({"PFD"})

EXTRACTION_TARGETS_BY_TYPE: dict[str, frozenset[str]] = {
    "PFD": frozenset({"top_equipment_header_basic", "top_equipment_header_detailed"}),
}

VALID_STATUSES: frozenset[str] = frozenset({"SUCCESS", "NO_FINDINGS", "FAILED_INPUTS", "FAILED"})

LEGACY_EXTRACTION_MODE: str = "top_equipment_header_with_dwg"

EXTRA_FIELD_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
EXTRA_FIELD_NAME_MAX = 40
EXTRA_FIELD_DESCRIPTION_MAX = 200


# ---------------------------------------------------------------------------
# Path resolvers
# ---------------------------------------------------------------------------


def resolve_stub_path(
    source_dir: Path,
    drawing_type: str,
    extraction_target: str,
    pdf_stem: str,
    page_num: int,
) -> Path:
    """Return the v2 target-aware stub path under ``source_dir``.

    Contract: {source_dir}/{drawing_type}/{extraction_target}/{pdf_stem}_page_{NNNN}_stub.md
    """
    return (
        Path(source_dir)
        / drawing_type
        / extraction_target
        / f"{pdf_stem}_page_{page_num:04d}_stub.md"
    )


def resolve_legacy_stub_path(source_dir: Path, pdf_stem: str, page_num: int) -> Path:
    """Return the legacy (pre-v2) stub path under ``source_dir``."""
    return Path(source_dir) / f"{pdf_stem}_page_{page_num:04d}_equipment_stub.md"


# ---------------------------------------------------------------------------
# Column derivation + extra-field validation
# ---------------------------------------------------------------------------


def build_column_order(
    extraction_target: str,
    requested_known_fields: list[str] | None = None,
    requested_extra_fields: list[dict[str, str]] | None = None,
) -> list[str]:
    """Derive canonical column order for a stub's findings table.

    Basic target: 4 base columns (equipment_number, equipment_name,
    system_name, drawing).

    Detailed target: 4 base + requested_known_fields (filtered to the
    canonical catalog order) + requested_extra_fields.name (request order).
    """
    columns: list[str] = list(BASE_COLUMNS)
    if extraction_target == "top_equipment_header_detailed":
        requested_known_fields = list(requested_known_fields or [])
        requested_extra_fields = list(requested_extra_fields or [])
        for catalog_field in KNOWN_FIELD_CATALOG:
            if catalog_field in requested_known_fields:
                columns.append(catalog_field)
        for extra in requested_extra_fields:
            name = str(extra.get("name", ""))
            if name:
                columns.append(name)
    return columns


def validate_extra_fields_collisions(
    requested_known_fields: list[str],
    requested_extra_fields: list[dict[str, str]],
    required_fields: list[str],
) -> list[str]:
    """Return a list of collision/validation errors. Empty list means valid.

    Enforces the naming rules from SKILL.md for detailed-target runs:
    - extra field name matches regex, length bound
    - description non-empty, length bound, single-line
    - no collision with base columns (incl. source_page) or any catalog field
    - no duplicates in extra fields
    - required_fields subset of requested_known_fields union extra.name
    """
    errors: list[str] = []
    base = set(BASE_COLUMNS) | {"source_page"}
    catalog = set(KNOWN_FIELD_CATALOG)
    seen: set[str] = set()
    for extra in requested_extra_fields:
        name = str(extra.get("name", "") or "")
        description = str(extra.get("description", "") or "")
        if not EXTRA_FIELD_NAME_RE.match(name) or len(name) > EXTRA_FIELD_NAME_MAX:
            errors.append(
                "invalid extra field name "
                f"'{name}'; must match /^[a-z][a-z0-9_]*$/ and <= "
                f"{EXTRA_FIELD_NAME_MAX} chars"
            )
            continue
        if not description or len(description) > EXTRA_FIELD_DESCRIPTION_MAX or "\n" in description:
            errors.append(
                f"invalid extra field description for '{name}'; must be "
                f"non-empty, <= {EXTRA_FIELD_DESCRIPTION_MAX} chars, single line"
            )
        if name in base:
            errors.append(f"extra field name '{name}' collides with base column")
        if name in catalog:
            errors.append(
                f"extra field name '{name}' collides with known-field catalog entry '{name}'"
            )
        if name in seen:
            errors.append(f"duplicate extra field name '{name}'")
        seen.add(name)
    requestable = set(requested_known_fields) | seen
    for required in required_fields:
        if required not in requestable:
            errors.append(
                f"required field '{required}' not in requested known fields union extra fields"
            )
    return errors


# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------


def parse_stub(path: Path, page_num: int) -> dict:
    """Parse either a v2 or legacy stub and return a canonical dict.

    The returned dict has this shape (both formats):
        format_version: "v2" | "legacy"
        drawing_type: str (defaults "PFD" for legacy)
        extraction_target: str (defaults "top_equipment_header_basic" for legacy)
        source_pdf: str
        source_page: str (preserves legacy "7 / 106" form when present)
        drawing: str
        system_name: str
        status: str  -- one of VALID_STATUSES
        note: str
        columns: list[str]
        rows: list[list[str]]  -- values in column order
        requested_known_fields: list[str]  (empty for basic)
        requested_extra_fields: list[{"name": str, "description": str}]  (empty for basic)
        required_fields: list[str]  (empty for basic)
        extraction_mode: str  (legacy alias for back-compat; empty for native v2)
    """
    text = Path(path).read_text(encoding="utf-8")
    if _is_v2_stub(text):
        return _parse_stub_v2(text, page_num)
    return _parse_stub_legacy(text, page_num)


def _is_v2_stub(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        return stripped == "---"
    return False


def _extract_backticked(line: str) -> str:
    parts = line.split("`")
    if len(parts) >= 2:
        return parts[1].strip()
    return ""


def _parse_stub_legacy(text: str, page_num: int) -> dict:
    """Parse the legacy (pre-v2) bullet-list stub format.

    This preserves the prior parse_stub behavior exactly so that back-compat
    callers (sanitize_equipment_stubs.py, report_stub_counts.py,
    recover_deepcut_multiblock_headers.py) continue to round-trip without
    modification: status/note are derived from row content, not from the
    Extraction-status bullet line.
    """
    lines = text.splitlines()

    source_pdf = ""
    source_page = f"{page_num}"
    extraction_mode = LEGACY_EXTRACTION_MODE
    drawing = ""
    system_name = ""
    rows: list[list[str]] = []

    for line in lines:
        if "Source PDF:" in line:
            source_pdf = _extract_backticked(line)
        elif "Source page:" in line:
            source_page = _extract_backticked(line) or f"{page_num}"
        elif "Extraction mode:" in line:
            extraction_mode = _extract_backticked(line) or extraction_mode
        elif "DWG NO.:" in line:
            drawing = _extract_backticked(line)
        elif "System name:" in line:
            system_name = _extract_backticked(line)

    in_table = False
    for line in lines:
        if line.startswith("| equipment_number | equipment_name | system_name | drawing |"):
            in_table = True
            continue
        if line.startswith("| equipment_number | equipment_name | drawing |"):
            in_table = True
            continue
        if in_table and line.startswith("| ---"):
            continue
        if in_table and line.startswith("| "):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) == 4:
                if not parts[2]:
                    parts[2] = system_name
                rows.append(parts)
            elif len(parts) == 3:
                rows.append([parts[0], parts[1], system_name, parts[2]])
            continue
        if in_table and not line.startswith("| "):
            break

    status = "SUCCESS"
    note = "Top-of-sheet equipment header present."
    meaningful_rows = [row for row in rows if row[0] or row[1] or row[3]]
    if not meaningful_rows:
        status = "NO_FINDINGS"
        note = "No separated top-of-sheet equipment header was identified."
        rows = [["", "", system_name, ""]]

    drawing_type = "PFD"
    extraction_target = "top_equipment_header_basic"

    return {
        "format_version": "legacy",
        "drawing_type": drawing_type,
        "extraction_target": extraction_target,
        "source_pdf": source_pdf,
        "source_page": source_page,
        "drawing": drawing,
        "system_name": system_name,
        "status": status,
        "note": note,
        "columns": list(BASE_COLUMNS),
        "rows": rows,
        "requested_known_fields": [],
        "requested_extra_fields": [],
        "required_fields": [],
        "extraction_mode": extraction_mode,
    }


def _parse_stub_v2(text: str, page_num: int) -> dict:
    """Parse v2 (YAML frontmatter + markdown body) stub format."""
    lines = text.splitlines()
    start_idx: int | None = None
    end_idx: int | None = None
    for idx, line in enumerate(lines):
        if line.strip() == "---":
            if start_idx is None:
                start_idx = idx
            else:
                end_idx = idx
                break
    if start_idx is None or end_idx is None:
        raise ValueError("malformed v2 stub: could not locate YAML frontmatter delimiters")

    frontmatter = _parse_simple_yaml(lines[start_idx + 1 : end_idx])
    body_lines = lines[end_idx + 1 :]

    drawing_type = str(frontmatter.get("drawing_type", "") or "")
    extraction_target = str(frontmatter.get("extraction_target", "") or "")
    source_pdf = str(frontmatter.get("source_pdf", "") or "")
    source_page_raw = frontmatter.get("source_page", page_num)
    source_page = str(source_page_raw if source_page_raw != "" else page_num)
    drawing = str(frontmatter.get("drawing", "") or "")
    system_name = str(frontmatter.get("system_name", "") or "")
    status = str(frontmatter.get("status", "SUCCESS") or "SUCCESS")

    requested_known_fields = [str(x) for x in (frontmatter.get("requested_known_fields") or [])]
    requested_extra_fields_raw = frontmatter.get("requested_extra_fields") or []
    requested_extra_fields: list[dict[str, str]] = []
    for entry in requested_extra_fields_raw:
        if isinstance(entry, dict):
            requested_extra_fields.append(
                {
                    "name": str(entry.get("name", "")),
                    "description": str(entry.get("description", "")),
                }
            )
    required_fields = [str(x) for x in (frontmatter.get("required_fields") or [])]

    columns = build_column_order(
        extraction_target, requested_known_fields, requested_extra_fields
    )

    rows: list[list[str]] = []
    note = ""
    expected_header = "| " + " | ".join(columns) + " |"
    in_table = False
    last_bullet: str | None = None
    for line in body_lines:
        if line.strip() == expected_header.strip():
            in_table = True
            continue
        if in_table and line.startswith("| ---"):
            continue
        if in_table and line.startswith("| "):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) == len(columns):
                rows.append(parts)
            continue
        if in_table and not line.startswith("| "):
            in_table = False
        if line.startswith("- Extraction status:"):
            if last_bullet is not None:
                note = last_bullet
            continue
        if line.startswith("- "):
            last_bullet = line[2:].strip()

    return {
        "format_version": "v2",
        "drawing_type": drawing_type,
        "extraction_target": extraction_target,
        "source_pdf": source_pdf,
        "source_page": source_page,
        "drawing": drawing,
        "system_name": system_name,
        "status": status,
        "note": note,
        "columns": columns,
        "rows": rows,
        "requested_known_fields": requested_known_fields,
        "requested_extra_fields": requested_extra_fields,
        "required_fields": required_fields,
        "extraction_mode": "",
    }


# ---------------------------------------------------------------------------
# Minimal YAML parser for the v2 frontmatter schema
# ---------------------------------------------------------------------------


def _parse_simple_yaml(lines: list[str]) -> dict:
    """Parse the constrained YAML subset used by v2 stub frontmatter.

    Supported forms:
      key: scalar
      key: []
      key:
        - item
        - item
      key:
        - name: x
          description: y
    """
    result: dict = {}
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        if line.startswith(" "):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            items: list = []
            i += 1
            while i < n and lines[i].startswith("  "):
                item_line = lines[i][2:]
                if item_line.startswith("- "):
                    item_body = item_line[2:].strip()
                    if ":" in item_body:
                        ikey, _, ival = item_body.partition(":")
                        entry = {ikey.strip(): _unquote_yaml(ival.strip())}
                        i += 1
                        while i < n and lines[i].startswith("    "):
                            cont = lines[i][4:]
                            if ":" in cont:
                                ckey, _, cval = cont.partition(":")
                                entry[ckey.strip()] = _unquote_yaml(cval.strip())
                            i += 1
                        items.append(entry)
                        continue
                    items.append(_unquote_yaml(item_body))
                i += 1
            result[key] = items
            continue
        if value == "[]":
            result[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if inner:
                result[key] = [_coerce_yaml_scalar(_unquote_yaml(v.strip())) for v in inner.split(",")]
            else:
                result[key] = []
        else:
            result[key] = _coerce_yaml_scalar(_unquote_yaml(value))
        i += 1
    return result


def _unquote_yaml(value: str) -> str:
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if len(value) >= 2 and value[0] == "'" and value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def _coerce_yaml_scalar(value: str):
    stripped = value.strip()
    if stripped.lstrip("-").isdigit():
        try:
            return int(stripped)
        except ValueError:
            return value
    return value


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------


def render_stub(page_num: int, data: dict) -> str:
    """Render a stub in v2 or legacy format.

    Format selection:
      - data['format_version'] == 'v2' -> v2 YAML-frontmatter render.
      - Missing format_version BUT drawing_type and extraction_target set
        -> v2 render (explicit v2 caller that did not set format_version).
      - Otherwise -> legacy render (back-compat for pre-v2 dict shapes).
    """
    fv = str(data.get("format_version", "") or "")
    if fv == "legacy":
        return _render_stub_legacy(page_num, data)
    if fv == "v2":
        return _render_stub_v2(page_num, data)
    if data.get("drawing_type") and data.get("extraction_target"):
        return _render_stub_v2(page_num, data)
    return _render_stub_legacy(page_num, data)


def _render_stub_legacy(page_num: int, data: dict) -> str:
    """Render the legacy bullet-list stub format (byte-identical to pre-v2)."""
    extraction_mode = data.get("extraction_mode") or LEGACY_EXTRACTION_MODE
    status = data.get("status") or "SUCCESS"
    note = data.get("note") or "Top-of-sheet equipment header present."
    lines = [
        f"# Page {page_num} Equipment Extraction",
        "",
        f"- Source PDF: `{data.get('source_pdf', '')}`",
        f"- Source page: `{data.get('source_page', page_num)}`",
        f"- Extraction mode: `{extraction_mode}`",
        f"- DWG NO.: `{data.get('drawing', '')}`",
        f"- System name: `{data.get('system_name', '')}`",
        "",
        "| equipment_number | equipment_name | system_name | drawing |",
        "| --- | --- | --- | --- |",
    ]
    for row in data.get("rows", []):
        cells = list(row) + ["", "", "", ""]
        lines.append(f"| {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} |")
    lines.extend(
        [
            "",
            f"- {note}",
            f"- Extraction status: `{status}`",
            "",
        ]
    )
    return "\n".join(lines)


def _render_stub_v2(page_num: int, data: dict) -> str:
    """Render the v2 stub: YAML frontmatter + markdown body."""
    drawing_type = str(data.get("drawing_type", "") or "")
    extraction_target = str(data.get("extraction_target", "") or "")
    if not drawing_type or not extraction_target:
        raise ValueError(
            "v2 render requires drawing_type and extraction_target; "
            f"got drawing_type={drawing_type!r}, extraction_target={extraction_target!r}"
        )

    source_pdf = str(data.get("source_pdf", "") or "")
    source_page_int = _coerce_source_page_int(data.get("source_page", page_num))
    drawing = str(data.get("drawing", "") or "")
    system_name = str(data.get("system_name", "") or "")
    status = str(data.get("status") or "SUCCESS")
    note = str(data.get("note", "") or "")

    is_detailed = extraction_target == "top_equipment_header_detailed"
    requested_known_fields = [str(x) for x in (data.get("requested_known_fields") or [])]
    requested_extra_fields_raw = list(data.get("requested_extra_fields") or [])
    requested_extra_fields: list[dict[str, str]] = []
    for entry in requested_extra_fields_raw:
        if isinstance(entry, dict):
            requested_extra_fields.append(
                {
                    "name": str(entry.get("name", "")),
                    "description": str(entry.get("description", "")),
                }
            )
    required_fields = [str(x) for x in (data.get("required_fields") or [])]

    columns = list(data.get("columns") or build_column_order(
        extraction_target, requested_known_fields, requested_extra_fields
    ))

    frontmatter: list[str] = ["---"]
    frontmatter.append(f"drawing_type: {drawing_type}")
    frontmatter.append(f"extraction_target: {extraction_target}")
    frontmatter.append(f"source_pdf: {_emit_yaml_scalar(source_pdf)}")
    frontmatter.append(f"source_page: {source_page_int}")
    if is_detailed:
        frontmatter.extend(_emit_yaml_list_scalars("requested_known_fields", requested_known_fields))
        frontmatter.extend(
            _emit_yaml_list_dicts(
                "requested_extra_fields",
                requested_extra_fields,
                ("name", "description"),
            )
        )
        frontmatter.extend(_emit_yaml_list_scalars("required_fields", required_fields))
    frontmatter.append(f"drawing: {_emit_yaml_scalar(drawing)}")
    frontmatter.append(f"system_name: {_emit_yaml_scalar(system_name)}")
    frontmatter.append(f"status: {status}")
    frontmatter.append("---")

    title = f"# Page {page_num} \u2014 {drawing_type} {extraction_target}"
    table_header = "| " + " | ".join(columns) + " |"
    table_sep = "| " + " | ".join("---" for _ in columns) + " |"

    rows_source = list(data.get("rows") or [])
    if not rows_source:
        rows_source = [[""] * len(columns)]

    rendered_rows: list[str] = []
    for row in rows_source:
        padded = list(row) + [""] * max(0, len(columns) - len(row))
        padded = padded[: len(columns)]
        rendered_rows.append("| " + " | ".join(padded) + " |")

    body = [title, "", table_header, table_sep] + rendered_rows + [
        "",
        f"- {note}" if note else "- ",
        f"- Extraction status: `{status}`",
        "",
    ]

    return "\n".join(frontmatter) + "\n\n" + "\n".join(body)


def _coerce_source_page_int(value) -> int:
    if isinstance(value, int):
        return value
    text = str(value).strip()
    if "/" in text:
        text = text.split("/")[0].strip()
    try:
        return int(text)
    except ValueError:
        return 0


_YAML_RESERVED_SCALARS = frozenset(
    {"null", "~", "true", "false", "yes", "no", "on", "off"}
)


def _emit_yaml_scalar(value) -> str:
    text = "" if value is None else str(value)
    if text == "":
        return '""'
    needs_quote = False
    if text.strip() != text:
        needs_quote = True
    elif text[0] in "-?*&!|>'\"%@`":
        needs_quote = True
    elif any(ch in text for ch in ":#[]{},\n"):
        needs_quote = True
    elif text.lower() in _YAML_RESERVED_SCALARS:
        needs_quote = True
    else:
        try:
            float(text)
            needs_quote = True
        except ValueError:
            pass
    if needs_quote:
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


def _emit_yaml_list_scalars(key: str, items: list[str]) -> list[str]:
    if not items:
        return [f"{key}: []"]
    out = [f"{key}:"]
    for item in items:
        out.append(f"  - {item}")
    return out


def _emit_yaml_list_dicts(
    key: str,
    items: list[dict[str, str]],
    field_order: tuple[str, ...],
) -> list[str]:
    if not items:
        return [f"{key}: []"]
    out = [f"{key}:"]
    for item in items:
        first = True
        for field in field_order:
            val = _emit_yaml_scalar(item.get(field, ""))
            prefix = "  - " if first else "    "
            out.append(f"{prefix}{field}: {val}")
            first = False
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize equipment stub markdown layout.")
    parser.add_argument("source_dir")
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    parser.add_argument(
        "--drawing-type",
        help="If set (with --extraction-target), migrate legacy stubs to v2 format at the target-aware path.",
    )
    parser.add_argument(
        "--extraction-target",
        help="Required when --drawing-type is supplied.",
    )
    args = parser.parse_args()

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    source_dir = Path(args.source_dir).resolve()
    if not source_dir.is_dir():
        print(f"ERROR: source directory not found: {source_dir}", file=sys.stderr)
        return 2

    if bool(args.drawing_type) != bool(args.extraction_target):
        print(
            "ERROR: --drawing-type and --extraction-target must be supplied together",
            file=sys.stderr,
        )
        return 2

    if args.drawing_type:
        return _cli_migrate_to_v2(
            source_dir,
            args.pdf_stem,
            args.start_page,
            args.end_page,
            args.drawing_type,
            args.extraction_target,
        )
    return _cli_normalize_legacy_in_place(
        source_dir, args.pdf_stem, args.start_page, args.end_page
    )


def _cli_normalize_legacy_in_place(
    source_dir: Path, pdf_stem: str, start_page: int, end_page: int
) -> int:
    updated = 0
    missing_pages: list[int] = []
    for page_num in range(start_page, end_page + 1):
        stub_path = resolve_legacy_stub_path(source_dir, pdf_stem, page_num)
        if not stub_path.is_file():
            missing_pages.append(page_num)
            continue
        original = stub_path.read_text(encoding="utf-8")
        parsed = parse_stub(stub_path, page_num)
        parsed["format_version"] = "legacy"
        normalized = render_stub(page_num, parsed)
        if normalized != original:
            stub_path.write_text(normalized, encoding="utf-8")
            updated += 1
    print(f"updated={updated}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    return 0


def _cli_migrate_to_v2(
    source_dir: Path,
    pdf_stem: str,
    start_page: int,
    end_page: int,
    drawing_type: str,
    extraction_target: str,
) -> int:
    if drawing_type not in DRAWING_TYPES:
        print(
            f"ERROR: unknown drawing_type '{drawing_type}'; valid: {sorted(DRAWING_TYPES)}",
            file=sys.stderr,
        )
        return 2
    if drawing_type not in DRAWING_TYPES_IMPLEMENTED:
        print(
            f"ERROR: drawing_type '{drawing_type}' is registered but not implemented",
            file=sys.stderr,
        )
        return 2
    valid_targets = EXTRACTION_TARGETS_BY_TYPE.get(drawing_type, frozenset())
    if extraction_target not in valid_targets:
        print(
            f"ERROR: extraction_target '{extraction_target}' not valid for drawing_type "
            f"'{drawing_type}'; valid: {sorted(valid_targets)}",
            file=sys.stderr,
        )
        return 2

    out_dir = source_dir / drawing_type / extraction_target
    out_dir.mkdir(parents=True, exist_ok=True)

    migrated = 0
    missing_pages: list[int] = []
    for page_num in range(start_page, end_page + 1):
        legacy_path = resolve_legacy_stub_path(source_dir, pdf_stem, page_num)
        if not legacy_path.is_file():
            missing_pages.append(page_num)
            continue
        parsed = parse_stub(legacy_path, page_num)
        parsed["format_version"] = "v2"
        parsed["drawing_type"] = drawing_type
        parsed["extraction_target"] = extraction_target
        parsed["columns"] = build_column_order(
            extraction_target,
            parsed.get("requested_known_fields"),
            parsed.get("requested_extra_fields"),
        )
        out_path = resolve_stub_path(
            source_dir, drawing_type, extraction_target, pdf_stem, page_num
        )
        rendered = render_stub(page_num, parsed)
        out_path.write_text(rendered, encoding="utf-8")
        migrated += 1

    print(f"migrated={migrated}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    print(f"output_dir={out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
