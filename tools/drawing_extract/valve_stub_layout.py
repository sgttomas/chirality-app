#!/usr/bin/env python3
"""
valve_stub_layout.py
Parser/renderer/validator for P_AND_ID valve symbol-instance stubs.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path
import re


VALVE_SCHEMA_VERSION = "symbol_instance_v1"

CANDIDATE_COLUMNS: tuple[str, ...] = (
    "candidate_id",
    "source_page",
    "dwg_no",
    "system_name",
    "source_raster_path",
    "tile_id",
    "tile_image_path",
    "symbol_crop_path",
    "context_crop_path",
    "center_x_px",
    "center_y_px",
    "bbox_x0_px",
    "bbox_y0_px",
    "bbox_x1_px",
    "bbox_y1_px",
    "symbol_class",
    "symbol_confidence",
    "count_include",
    "review_status",
    "review_reason",
    "visible_tag_text",
    "tag_status",
    "tag_confidence",
    "nearby_line_text",
    "valve_size_text",
    "valve_type_code",
    "valve_type_name",
    "actuation",
    "detail_confidence",
    "issue_flags",
    "notes",
)

VALVE_CLASSES: frozenset[str] = frozenset(
    {
        "manual_block",
        "manual_throttle",
        "check",
        "control",
        "esd_block",
        "relief",
        "specialty_valve",
    }
)
NON_COUNT_CLASSES: frozenset[str] = frozenset({"instrument_only", "not_a_valve", "unknown"})
VALID_SYMBOL_CLASSES: frozenset[str] = VALVE_CLASSES | NON_COUNT_CLASSES
VALID_CONFIDENCE: frozenset[str] = frozenset({"high", "medium", "low", "TBD", ""})
VALID_COUNT_INCLUDE: frozenset[str] = frozenset({"true", "false"})
VALID_REVIEW_STATUS: frozenset[str] = frozenset(
    {"auto_accept", "manual_review", "human_accept", "human_reject", "superseded_duplicate"}
)
VALID_TAG_STATUS: frozenset[str] = frozenset(
    {"true_tag", "line_spec_only", "equipment_or_connector_text", "ambiguous", "none", "unreadable", ""}
)
VALID_STATUSES: frozenset[str] = frozenset({"SUCCESS", "NO_FINDINGS", "NO_FINDINGS_REFERENCE", "FAILED", "FAILED_INPUTS"})
VALID_ISSUE_FLAGS: frozenset[str] = frozenset(
    {
        "BOUNDARY_REVIEW",
        "LOW_LEGIBILITY",
        "AMBIGUOUS_SYMBOL",
        "TAG_UNRELIABLE",
        "TAG_PROFILE_REVIEW",
        "LINE_SPEC_TEXT_ONLY",
        "POSSIBLE_INSTRUMENT_ONLY",
        "GEOMETRY_DUPLICATE_REVIEW",
        "CLASSIFICATION_UNCERTAIN",
        "SIZE_NOT_LEGIBLE",
        "ACTUATION_NOT_LEGIBLE",
    }
)

DEFAULT_TRUE_TAG_RE = re.compile(r"^[A-Z]{1,6}-\d{2,5}(?:-\d{1,3})?$")
DEFAULT_LINE_SPEC_RES: tuple[re.Pattern[str], ...] = (
    re.compile(r"^\d+(?:x\d+)?(?:BA|GA|GL|CH|NE|ST)(?:-[A-Z])?(?:\s+\S+)?$"),
    re.compile(r"^\d+x\d+$"),
    re.compile(r"^\d+(?:BA|GA|GL|CH|NE|ST)-[A-Z]\s+\d{2}[A-Z]{1,3}(?:-[A-Z])?$"),
)


@dataclass
class ValveStub:
    source_pdf: str
    source_page: int
    extraction_target: str
    mode: str
    tile_id: str
    tile_grid: str
    body_box_px: list[int]
    body_exclusions: list[str]
    read_box_px: list[int]
    emit_box_px: list[int]
    overlap_px: int
    mini_grid: str
    status: str
    finding_count: int
    rows: list[dict[str, str]]
    valve_schema_version: str = VALVE_SCHEMA_VERSION
    source_raster_path: str = ""
    tile_image_path: str = ""
    dwg_no: str = "TBD"
    system_name: str = "TBD"
    scope_file: str = ""
    basic_reference_run: str = ""
    basic_counts_csv: str = ""
    tag_profile_version: str = "default_v1"
    candidate_id_rule: str = 'sha1("{source_page}|{center_x_px}|{center_y_px}|{symbol_class}")[:12]'
    reason: str = ""


def candidate_id(source_page: int | str, center_x_px: int | str, center_y_px: int | str, symbol_class: str) -> str:
    return sha1(f"{source_page}|{center_x_px}|{center_y_px}|{symbol_class}".encode("utf-8")).hexdigest()[:12]


def columns_for_mode(_mode: str) -> tuple[str, ...]:
    return CANDIDATE_COLUMNS


def is_valve_class(value: str) -> bool:
    return (value or "").strip() in VALVE_CLASSES


def parse_issue_flags(value: str) -> list[str]:
    value = (value or "").strip()
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip("'\"") for part in inner.split(",") if part.strip()]
    return [value] if value else []


def render_issue_flags(flags: list[str] | tuple[str, ...] | str) -> str:
    if isinstance(flags, str):
        flags = parse_issue_flags(flags)
    clean = [str(flag).strip() for flag in flags if str(flag).strip()]
    return "[" + ", ".join(clean) + "]" if clean else "[]"


def tag_profile_warnings(row: dict[str, str], row_num: int) -> list[str]:
    tag = (row.get("visible_tag_text") or "").strip()
    tag_status = (row.get("tag_status") or "").strip()
    if tag_status != "true_tag" or not tag:
        return []
    warnings: list[str] = []
    if not DEFAULT_TRUE_TAG_RE.fullmatch(tag):
        warnings.append(f"row {row_num}: TAG_PROFILE_REVIEW visible_tag_text does not match default true-tag grammar")
    if any(pattern.fullmatch(tag) for pattern in DEFAULT_LINE_SPEC_RES):
        warnings.append(f"row {row_num}: TAG_PROFILE_REVIEW visible_tag_text matches default line/spec heuristic")
    return warnings


def render(model: ValveStub) -> str:
    columns = columns_for_mode(model.mode)
    lines = [
        "---",
        "drawing_type: P_AND_ID",
        f"extraction_target: {model.extraction_target}",
        f"mode: {model.mode}",
        f"valve_schema_version: {model.valve_schema_version}",
        f"source_pdf: {model.source_pdf}",
        f"source_page: {model.source_page}",
        f"source_raster_path: {model.source_raster_path}",
        f"tile_id: {model.tile_id}",
        f"tile_image_path: {model.tile_image_path}",
        f"tile_grid: {model.tile_grid}",
        f"body_box_px: {_format_list(model.body_box_px)}",
        f"body_exclusions: {_format_list(model.body_exclusions)}",
        f"read_box_px: {_format_list(model.read_box_px)}",
        f"emit_box_px: {_format_list(model.emit_box_px)}",
        f"overlap_px: {model.overlap_px}",
        f"mini_grid: {model.mini_grid}",
        f"dwg_no: {model.dwg_no}",
        f"system_name: {model.system_name}",
        f"tag_profile_version: {model.tag_profile_version}",
        f"candidate_id_rule: {model.candidate_id_rule}",
    ]
    if model.scope_file:
        lines.append(f"scope_file: {model.scope_file}")
    if model.basic_reference_run:
        lines.append(f"basic_reference_run: {model.basic_reference_run}")
    if model.basic_counts_csv:
        lines.append(f"basic_counts_csv: {model.basic_counts_csv}")
    if model.reason:
        lines.append(f"reason: {model.reason}")
    lines += [
        f"status: {model.status}",
        f"finding_count: {model.finding_count}",
        "---",
        "",
        f"# Page {model.source_page} - P_AND_ID {model.extraction_target} {model.tile_id}",
        "",
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    rows = model.rows or []
    if not rows:
        rows = [{col: "" for col in columns}]
        rows[0]["issue_flags"] = "[]"
    for row in rows:
        rendered_row = []
        for col in columns:
            value = str(row.get(col, ""))
            if col == "issue_flags":
                value = render_issue_flags(value)
            rendered_row.append(value)
        lines.append("| " + " | ".join(rendered_row) + " |")
    lines += ["", f"- Extraction status: `{model.status}`"]
    if model.reason:
        lines.append(f"- Reason: {model.reason}")
    return "\n".join(lines) + "\n"


def render_template_for_brief(runtime_params: dict[str, object], mode: str) -> str:
    target = "valve_count_detailed" if mode == "detailed" else "valve_count_basic"
    row = {col: f"<{col}>" for col in CANDIDATE_COLUMNS}
    row.update(
        {
            "candidate_id": "<deterministic candidate_id>",
            "source_page": str(runtime_params.get("source_page", 1)),
            "dwg_no": "TBD",
            "system_name": "TBD",
            "source_raster_path": str(runtime_params.get("source_raster_path", "")),
            "tile_id": str(runtime_params.get("tile_id", "page_0001_r01_c01")),
            "tile_image_path": str(runtime_params.get("tile_image_path", "")),
            "symbol_class": "manual_block",
            "symbol_confidence": "medium",
            "count_include": "true",
            "review_status": "manual_review",
            "review_reason": "visible_valve_symbol",
            "tag_status": "none",
            "tag_confidence": "TBD",
            "detail_confidence": "TBD",
            "issue_flags": "[]",
        }
    )
    return render(
        ValveStub(
            source_pdf=str(runtime_params.get("source_pdf", "<SOURCE_PDF>")),
            source_page=int(runtime_params.get("source_page", 1)),
            source_raster_path=str(runtime_params.get("source_raster_path", "")),
            extraction_target=target,
            mode=mode,
            tile_id=str(runtime_params.get("tile_id", "page_0001_r01_c01")),
            tile_image_path=str(runtime_params.get("tile_image_path", "")),
            tile_grid=str(runtime_params.get("tile_grid", "5x4")),
            body_box_px=list(runtime_params.get("body_box_px", [0, 0, 0, 0])),
            body_exclusions=list(runtime_params.get("body_exclusions", ["border", "titleblock"])),
            read_box_px=list(runtime_params.get("read_box_px", [0, 0, 0, 0])),
            emit_box_px=list(runtime_params.get("emit_box_px", [0, 0, 0, 0])),
            overlap_px=int(runtime_params.get("overlap_px", 200)),
            mini_grid=str(runtime_params.get("mini_grid", "5x5")),
            status="SUCCESS",
            finding_count=1,
            rows=[row],
        )
    )


def _format_list(values: list[object]) -> str:
    return "[" + ", ".join(str(v) for v in values) + "]"


def _parse_scalar(value: str) -> object:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        parsed: list[object] = []
        for part in inner.split(","):
            token = part.strip()
            parsed.append(int(token) if re.fullmatch(r"-?\d+", token) else token)
        return parsed
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    data: dict[str, object] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = _parse_scalar(value.strip())
    return data, text[end + 4 :].lstrip("\n")


def _parse_table(body: str) -> tuple[list[str], list[dict[str, str]]]:
    table_lines = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return [], []
    header = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        values = [cell.strip() for cell in line.strip("|").split("|")]
        if len(values) < len(header):
            values += [""] * (len(header) - len(values))
        row = dict(zip(header, values))
        if any(row.get(col, "").strip() for col in header if col != "issue_flags"):
            rows.append(row)
    return header, rows


def parse(path: Path) -> ValveStub:
    text = Path(path).read_text(encoding="utf-8")
    data, body = _parse_frontmatter(text)
    _header, rows = _parse_table(body)
    return ValveStub(
        source_pdf=str(data.get("source_pdf", "")),
        source_page=int(data.get("source_page", 0) or 0),
        source_raster_path=str(data.get("source_raster_path", "")),
        extraction_target=str(data.get("extraction_target", "")),
        mode=str(data.get("mode", "")),
        valve_schema_version=str(data.get("valve_schema_version", "")),
        tile_id=str(data.get("tile_id", "")),
        tile_image_path=str(data.get("tile_image_path", "")),
        tile_grid=str(data.get("tile_grid", "")),
        body_box_px=list(data.get("body_box_px", []) or []),
        body_exclusions=list(data.get("body_exclusions", []) or []),
        read_box_px=list(data.get("read_box_px", []) or []),
        emit_box_px=list(data.get("emit_box_px", []) or []),
        overlap_px=int(data.get("overlap_px", 0) or 0),
        mini_grid=str(data.get("mini_grid", "")),
        dwg_no=str(data.get("dwg_no", "TBD")),
        system_name=str(data.get("system_name", "TBD")),
        scope_file=str(data.get("scope_file", "")),
        basic_reference_run=str(data.get("basic_reference_run", "")),
        basic_counts_csv=str(data.get("basic_counts_csv", "")),
        tag_profile_version=str(data.get("tag_profile_version", "default_v1")),
        candidate_id_rule=str(data.get("candidate_id_rule", "")),
        reason=str(data.get("reason", "")),
        status=str(data.get("status", "")),
        finding_count=int(data.get("finding_count", 0) or 0),
        rows=rows,
    )


def validate(model: ValveStub) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if model.valve_schema_version != VALVE_SCHEMA_VERSION:
        errors.append(f"invalid valve_schema_version: {model.valve_schema_version or '<missing>'}")
    if model.status not in VALID_STATUSES:
        errors.append(f"invalid status: {model.status}")
    if model.mode not in {"basic", "detailed"}:
        errors.append(f"invalid mode: {model.mode}")
    if model.extraction_target not in {"valve_count_basic", "valve_count_detailed"}:
        errors.append(f"invalid extraction_target: {model.extraction_target}")
    if model.status == "SUCCESS" and model.finding_count != len(model.rows):
        errors.append(f"finding_count={model.finding_count} but rows={len(model.rows)}")
    if model.status in {"NO_FINDINGS", "NO_FINDINGS_REFERENCE"} and model.finding_count != 0:
        errors.append(f"{model.status} requires finding_count=0")
    if model.status == "NO_FINDINGS_REFERENCE" and model.reason != "legend_or_reference_sheet":
        errors.append("NO_FINDINGS_REFERENCE requires reason=legend_or_reference_sheet")

    for idx, row in enumerate(model.rows, start=1):
        for col in CANDIDATE_COLUMNS:
            row.setdefault(col, "")
        if row.get("source_page") and str(row.get("source_page")) != str(model.source_page):
            errors.append(f"row {idx}: source_page does not match frontmatter")
        symbol_class = row.get("symbol_class", "")
        if symbol_class not in VALID_SYMBOL_CLASSES:
            errors.append(f"row {idx}: invalid symbol_class")
        if row.get("symbol_confidence", "") not in VALID_CONFIDENCE:
            errors.append(f"row {idx}: invalid symbol_confidence")
        if row.get("tag_confidence", "") not in VALID_CONFIDENCE:
            errors.append(f"row {idx}: invalid tag_confidence")
        if row.get("detail_confidence", "") not in VALID_CONFIDENCE:
            errors.append(f"row {idx}: invalid detail_confidence")
        if row.get("count_include", "") not in VALID_COUNT_INCLUDE:
            errors.append(f"row {idx}: invalid count_include")
        if row.get("review_status", "") not in VALID_REVIEW_STATUS:
            errors.append(f"row {idx}: invalid review_status")
        if row.get("tag_status", "") not in VALID_TAG_STATUS:
            errors.append(f"row {idx}: invalid tag_status")
        if row.get("count_include") == "true" and symbol_class in NON_COUNT_CLASSES:
            errors.append(f"row {idx}: count_include=true requires a valve symbol_class")
        if row.get("count_include") == "true" and not is_valve_class(symbol_class):
            errors.append(f"row {idx}: count_include=true requires isolated-crop valve classification")
        if row.get("count_include") == "true" and row.get("symbol_confidence") not in {"medium", "high"}:
            errors.append(f"row {idx}: count_include=true requires medium or high symbol_confidence")
        for col in ("center_x_px", "center_y_px", "bbox_x0_px", "bbox_y0_px", "bbox_x1_px", "bbox_y1_px"):
            if not re.fullmatch(r"\d+", row.get(col, "")):
                errors.append(f"row {idx}: {col} must be a non-negative integer")
        if _int(row.get("bbox_x0_px")) >= _int(row.get("bbox_x1_px")) or _int(row.get("bbox_y0_px")) >= _int(row.get("bbox_y1_px")):
            errors.append(f"row {idx}: bbox coordinates must form a positive rectangle")
        if not row.get("symbol_crop_path", "").strip():
            errors.append(f"row {idx}: symbol_crop_path is required")
        if not row.get("candidate_id", "").strip():
            errors.append(f"row {idx}: candidate_id is required")
        elif all(row.get(k, "") for k in ("center_x_px", "center_y_px", "symbol_class")):
            expected = candidate_id(model.source_page, row["center_x_px"], row["center_y_px"], row["symbol_class"])
            if row["candidate_id"] != expected:
                warnings.append(f"row {idx}: candidate_id differs from default rule")
        if row.get("tag_status") in {"line_spec_only", "ambiguous"} and row.get("nearby_line_text") and row.get("visible_tag_text"):
            warnings.append(f"row {idx}: nearby_line_text populated while visible_tag_text is also populated")
        for warning in tag_profile_warnings(row, idx):
            warnings.append(warning)
        for flag in parse_issue_flags(row.get("issue_flags", "")):
            if flag not in VALID_ISSUE_FLAGS:
                warnings.append(f"row {idx}: unknown issue flag {flag}")
    return errors, warnings


def _int(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


def resolve_stub_path(source_dir: Path, target: str, pdf_stem: str, page_num: int, tile_id: str, mode: str, run_folder: str | None = None) -> Path:
    base = Path(source_dir) / "P_AND_ID" / target
    if run_folder:
        base = base / run_folder
    page_prefix = f"page_{page_num:04d}_"
    tile_suffix = tile_id[len(page_prefix) :] if tile_id.startswith(page_prefix) else tile_id
    return base / f"{pdf_stem}_page_{page_num:04d}_tile_{tile_suffix}_{mode}_stub.md"
