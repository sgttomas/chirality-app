#!/usr/bin/env python3
"""
titleblock_stub_layout.py
Parser/renderer for DRAWING_SET/titleblock_index stubs.

This module is deterministic and LLM-independent. It intentionally does not
import the PFD equipment stub layout module.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


BODY_COLUMNS: tuple[str, ...] = (
    "dwg_no",
    "sheet_no",
    "sheet_title",
    "revision",
    "area_or_module",
    "drawing_family_proposal",
    "titleblock_corner",
    "confidence",
)

VALID_STATUSES: frozenset[str] = frozenset({"SUCCESS", "NO_TITLEBLOCK", "FAILED", "FAILED_INPUTS"})
VALID_FAMILIES: frozenset[str] = frozenset({"PFD", "P_AND_ID", "ISOMETRIC", "GA", "OTHER", "REFERENCE_OR_LEGEND", "TBD"})
VALID_CONFIDENCE: frozenset[str] = frozenset({"high", "medium", "low", "TBD", ""})
VALID_CORNERS: frozenset[str] = frozenset({"tl", "tr", "bl", "br", "TBD", ""})


@dataclass
class TitleblockStub:
    source_pdf: str
    source_page: int
    corner_crop_geometry: dict[str, float]
    status: str
    finding_count: int
    row: dict[str, str]
    note: str = ""


def _yaml_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def render(model: TitleblockStub) -> str:
    row = {col: str(model.row.get(col, "")) for col in BODY_COLUMNS}
    lines = [
        "---",
        "drawing_type: DRAWING_SET",
        "extraction_target: titleblock_index",
        f"source_pdf: {model.source_pdf}",
        f"source_page: {model.source_page}",
        "corner_crop_geometry:",
        f"  width_ratio: {_yaml_scalar(model.corner_crop_geometry.get('width_ratio', ''))}",
        f"  height_ratio: {_yaml_scalar(model.corner_crop_geometry.get('height_ratio', ''))}",
        f"status: {model.status}",
        f"finding_count: {model.finding_count}",
        "---",
        "",
        f"# Page {model.source_page} - DRAWING_SET titleblock_index",
        "",
        "| " + " | ".join(BODY_COLUMNS) + " |",
        "| " + " | ".join(["---"] * len(BODY_COLUMNS)) + " |",
        "| " + " | ".join(row[col] for col in BODY_COLUMNS) + " |",
        "",
    ]
    if model.status == "NO_TITLEBLOCK":
        lines.append("- No titleblock was identified.")
    if model.note:
        lines.append(f"- Note: {model.note}")
    lines.append(f"- Extraction status: `{model.status}`")
    return "\n".join(lines) + "\n"


def render_template_for_brief(source_pdf: str, page_num: int, width_ratio: float, height_ratio: float) -> str:
    return render(
        TitleblockStub(
            source_pdf=source_pdf,
            source_page=page_num,
            corner_crop_geometry={"width_ratio": width_ratio, "height_ratio": height_ratio},
            status="SUCCESS",
            finding_count=1,
            row={
                "dwg_no": "<DWG_NO or TBD>",
                "sheet_no": "<SHEET_NO or TBD>",
                "sheet_title": "<SHEET_TITLE or TBD>",
                "revision": "<REV or TBD>",
                "area_or_module": "<AREA_OR_MODULE or TBD>",
                "drawing_family_proposal": "<PFD|P_AND_ID|ISOMETRIC|GA|OTHER|REFERENCE_OR_LEGEND|TBD>",
                "titleblock_corner": "<tl|tr|bl|br|TBD>",
                "confidence": "<high|medium|low>",
            },
        )
    )


def _parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    fm_text = text[4:end].strip("\n")
    body = text[end + 4 :].lstrip("\n")
    data: dict[str, object] = {}
    current_map: dict[str, object] | None = None
    for line in fm_text.splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and current_map is not None:
            key, _, value = line.strip().partition(":")
            current_map[key] = _parse_scalar(value.strip())
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not value:
            current_map = {}
            data[key] = current_map
        else:
            current_map = None
            data[key] = _parse_scalar(value)
    return data, body


def _parse_scalar(value: str) -> object:
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


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
        rows.append(dict(zip(header, values)))
    return header, rows


def parse(path: Path) -> TitleblockStub:
    text = Path(path).read_text(encoding="utf-8")
    data, body = _parse_frontmatter(text)
    _header, rows = _parse_table(body)
    row = rows[0] if rows else {col: "" for col in BODY_COLUMNS}
    return TitleblockStub(
        source_pdf=str(data.get("source_pdf", "")),
        source_page=int(data.get("source_page", 0) or 0),
        corner_crop_geometry=dict(data.get("corner_crop_geometry", {}) or {}),
        status=str(data.get("status", "")),
        finding_count=int(data.get("finding_count", 0) or 0),
        row=row,
    )


def validate(model: TitleblockStub) -> list[str]:
    errors: list[str] = []
    if model.status not in VALID_STATUSES:
        errors.append(f"invalid status: {model.status}")
    if model.finding_count not in {0, 1}:
        errors.append("finding_count must be 0 or 1")
    if model.status == "SUCCESS" and model.finding_count != 1:
        errors.append("SUCCESS requires finding_count=1")
    if model.status == "NO_TITLEBLOCK" and model.finding_count != 0:
        errors.append("NO_TITLEBLOCK requires finding_count=0")
    family = model.row.get("drawing_family_proposal", "")
    if family and family not in VALID_FAMILIES:
        errors.append(f"invalid drawing_family_proposal: {family}")
    confidence = model.row.get("confidence", "")
    if confidence not in VALID_CONFIDENCE:
        errors.append(f"invalid confidence: {confidence}")
    corner = model.row.get("titleblock_corner", "")
    if corner not in VALID_CORNERS:
        errors.append(f"invalid titleblock_corner: {corner}")
    return errors


def resolve_stub_path(source_dir: Path, pdf_stem: str, page_num: int, run_folder: str | None = None) -> Path:
    base = Path(source_dir) / "DRAWING_SET" / "titleblock_index"
    if run_folder:
        base = base / run_folder
    return base / f"{pdf_stem}_page_{page_num:04d}_titleblock_stub.md"
