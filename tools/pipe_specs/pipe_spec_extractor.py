#!/usr/bin/env python3
"""
pipe_spec_extractor.py
Shared extraction module for Millenia Engineering Piping Class PDFs.

Public API:
    extract_pipe_spec(pdf_path: Path) -> ExtractionResult

ExtractionResult fields:
    spec_id, revision, source_pdf, source_sha256,
    page_count, blank_pages,
    header_rows: list[dict]        (field, value)
    table_rows:  list[dict]        (normalized tables.csv schema)
    raw_rows:    list[dict]        (audit-format _raw_rows.csv schema)
    diagnostics: list[dict]        (metric, value, note)
    status:      "ok" | "parse_fail"
    failure_reason: str

Determinism:
    - No LLM calls, no network, no API keys.
    - Pure spatial parsing via PyMuPDF (`fitz`).
    - Output ordering is deterministic: rows ordered by (section, section_row_id).

Inputs:
    pdf_path -- absolute Path to a Pipe Spec PDF file. Must exist.

Outputs:
    Pure data; this module does not write to disk. CLIs and the batch
    driver write CSVs derived from this result.

Write scope:
    None. Read-only with respect to the filesystem.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import fitz  # PyMuPDF
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit(
        "ERROR: PyMuPDF (fitz) is not installed. Run: pip install pymupdf"
    ) from exc


# ---------------------------------------------------------------------------
# Constants and schema
# ---------------------------------------------------------------------------

SECTION_ORDER = ["PIPE", "FLANGES_FITTINGS", "BOLTING_GASKETS", "TUBING", "VALVES"]

SECTION_SLUGS = {
    "PIPE": "pipe",
    "FLANGES_FITTINGS": "flanges_fittings",
    "BOLTING_GASKETS": "bolting_gaskets",
    "TUBING": "tubing",
    "VALVES": "valves",
}

# Inner-header column tokens we expect for each section. Variants are tolerated.
# The first column is treated as the "ITEM-like" anchor and is accepted as
# either ITEM or TYPE (some specs use TYPE for the PIPE/FLANGES section).
SECTION_INNER_HEADER_TOKENS = {
    "PIPE": ["ITEM", "NPS", "MIN SCH", "ENDS", "DESCRIPTION", "NOTE / CODE"],
    "FLANGES_FITTINGS": [
        "ITEM",
        "NPS",
        "MIN SCH/RTG",
        "CONN.",
        "DESCRIPTION",
        "NOTE / CODE",
    ],
    "BOLTING_GASKETS": ["ITEM", "NPS", "RTG", "DESCRIPTION", "NOTE / CODE"],
    "TUBING": ["TYPE", "OD", "MIN WT", "DESCRIPTION", "NOTE / CODE"],
    "VALVES": [
        "ITEM",
        "NPS",
        "TAG",
        "CLASS/RTG",
        "ENDS",
        "TRIM",
        "DESCRIPTION",
        "NOTE / CODE",
    ],
}

# Synonyms for the first ("ITEM-like") column header. When a section's
# header row is missing the canonical first token, accept any of these.
ITEM_COLUMN_SYNONYMS = {"ITEM", "TYPE"}

# Mandatory header labels (must all be present for `ok`).
MANDATORY_HEADER_LABELS = [
    "PIPING CLASS",
    "Rev",
    "SERVICE / COMMMODITY",  # spec misspelling preserved
    "ANSI RATING/MATERIAL",
    "MAWP",
    "TEMPERATURE LIMITS",
    "DESIGN CODE",
]

OPTIONAL_HEADER_LABELS = [
    "P.W.H.T.",
    "N.D.E.",
    "C.A",
    "HYDROTEST",
    "revision_date",
    "service_description",
]

# tables.csv schema (column order is contractual)
TABLES_COLUMNS = [
    "piping_class",
    "source_pdf",
    "source_revision",
    "source_sha256",
    "source_page",
    "section",
    "section_row_id",
    "source_header_signature",
    "item_or_type",
    "item_filled",
    "nps_or_size",
    "schedule_or_rating",
    "tag",
    "conn_or_ends",
    "trim",
    "description",
    "note_code",
    "note_code_filled",
]

# _raw_rows.csv schema (long format)
RAW_ROWS_COLUMNS = [
    "piping_class",
    "source_pdf",
    "source_revision",
    "source_sha256",
    "source_page",
    "section",
    "section_row_id",
    "raw_column",
    "raw_value",
]

# _header.csv schema
HEADER_COLUMNS = [
    "field",
    "value",
    "source_pdf",
    "source_revision",
    "source_sha256",
]

# _diagnostics.csv schema
DIAGNOSTICS_COLUMNS = ["metric", "value", "note"]


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass
class ExtractionResult:
    spec_id: str
    revision: str
    source_pdf: str
    source_sha256: str
    page_count: int
    blank_pages: int
    header_rows: list[dict[str, str]] = field(default_factory=list)
    table_rows: list[dict[str, str]] = field(default_factory=list)
    raw_rows: list[dict[str, str]] = field(default_factory=list)
    diagnostics: list[dict[str, str]] = field(default_factory=list)
    status: str = "ok"
    failure_reason: str = ""

    def section_counts(self) -> dict[str, int]:
        counts = {sec: 0 for sec in SECTION_ORDER}
        for r in self.table_rows:
            sec = r.get("section", "")
            if sec in counts:
                counts[sec] += 1
        return counts


# ---------------------------------------------------------------------------
# Filename parsing
# ---------------------------------------------------------------------------

FILENAME_RE = re.compile(r"^(?P<spec_id>.+?)_R(?P<rev>\d+)$")


def parse_filename(stem: str) -> tuple[str, str] | None:
    """Return (spec_id, revision) or None if non-conforming."""
    m = FILENAME_RE.match(stem)
    if not m:
        return None
    return m.group("spec_id"), f"R{m.group('rev')}"


# ---------------------------------------------------------------------------
# Word helpers
# ---------------------------------------------------------------------------


def _sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _cluster_rows(words: list[tuple], y_tol: float = 3.0) -> list[list[tuple]]:
    """Group words into rows by y-midpoint clustering.

    Words are assigned greedily into rows whose representative y is within
    `y_tol`. Words within a row are sorted by x. Rows are returned sorted
    by representative y.
    """
    if not words:
        return []
    # Sort by y first (then x) for stable grouping
    sw = sorted(words, key=lambda w: (round((w[1] + w[3]) / 2, 2), w[0]))
    rows: list[list[tuple]] = []
    row_y: list[float] = []
    for w in sw:
        my = (w[1] + w[3]) / 2
        placed = False
        for i, ry in enumerate(row_y):
            if abs(my - ry) <= y_tol:
                rows[i].append(w)
                # update running mean
                row_y[i] = (ry * len(rows[i]) + my) / (len(rows[i]) + 1)
                placed = True
                break
        if not placed:
            rows.append([w])
            row_y.append(my)
    # Sort each row by x and the rows by y
    indexed = sorted(zip(row_y, rows), key=lambda p: p[0])
    return [sorted(r, key=lambda w: w[0]) for _, r in indexed]


def _join_words(ws: list[tuple]) -> str:
    return " ".join(w[4] for w in ws).strip()


def _cluster_numeric(values: list[float], tol: float = 3.0) -> list[float]:
    """Cluster near-equal coordinates and return their means."""
    if not values:
        return []
    groups: list[list[float]] = []
    for value in sorted(values):
        if not groups or abs(value - groups[-1][-1]) > tol:
            groups.append([value])
        else:
            groups[-1].append(value)
    return [sum(group) / len(group) for group in groups]


def _cell_text_lines_first(ws: list[tuple], y_tol: float = 3.0) -> str:
    """Join words in reading order, preserving visual line order first.

    This is required for merged cells: sorting all words by x alone interleaves
    two wrapped lines into a corrupted sentence.
    """
    rows = _cluster_rows(ws, y_tol=y_tol)
    return " ".join(_join_words(row) for row in rows if row).strip()


def _overlap(a0: float, a1: float, b0: float, b1: float) -> float:
    return max(0.0, min(a1, b1) - max(a0, b0))


def extract_vertical_rules(page: Any, y_top: float, y_bot: float) -> list[float]:
    """Extract vertical table rules from PyMuPDF drawing geometry.

    These PDFs encode table strokes primarily as thin filled rectangles rather
    than line items. Both representations are accepted. Candidate x positions
    are clustered, and tiny-overlap artifacts are discarded.
    """
    candidates: list[tuple[float, float, float]] = []
    for drawing in page.get_drawings():
        for item in drawing.get("items", []):
            if not item:
                continue
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                if abs(p1.x - p2.x) < 0.5 and abs(p1.y - p2.y) > 5.0:
                    y0, y1 = sorted((p1.y, p2.y))
                    if _overlap(y0, y1, y_top, y_bot) > 0:
                        candidates.append((p1.x, max(y0, y_top), min(y1, y_bot)))
            elif item[0] == "re":
                rect = item[1]
                if rect.width <= 2.0 and rect.height > 5.0:
                    y0, y1 = rect.y0, rect.y1
                    if _overlap(y0, y1, y_top, y_bot) > 0:
                        candidates.append(
                            (
                                (rect.x0 + rect.x1) / 2.0,
                                max(y0, y_top),
                                min(y1, y_bot),
                            )
                        )

    if not candidates:
        return []

    groups: list[list[tuple[float, float, float]]] = []
    for candidate in sorted(candidates, key=lambda c: c[0]):
        if not groups or abs(candidate[0] - groups[-1][-1][0]) > 3.0:
            groups.append([candidate])
        else:
            groups[-1].append(candidate)

    span = max(1.0, y_bot - y_top)
    min_coverage = max(8.0, span * 0.08)
    xs: list[float] = []
    for group in groups:
        coverage = sum(max(0.0, y1 - y0) for _x, y0, y1 in group)
        if coverage < min_coverage:
            continue
        xs.append(sum(x for x, _y0, _y1 in group) / len(group))
    return xs


def extract_horizontal_rules(
    page: Any, x_left: float, x_right: float, y_top: float, y_bot: float
) -> list[float]:
    """Extract horizontal rules crossing a given x interval."""
    candidates: list[float] = []
    for drawing in page.get_drawings():
        for item in drawing.get("items", []):
            if not item:
                continue
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                if abs(p1.y - p2.y) < 0.5 and abs(p1.x - p2.x) > 5.0:
                    x0, x1 = sorted((p1.x, p2.x))
                    y = p1.y
                    if y_top <= y <= y_bot and _overlap(x0, x1, x_left, x_right) > 0:
                        candidates.append(y)
            elif item[0] == "re":
                rect = item[1]
                if rect.height <= 2.0 and rect.width > 5.0:
                    y = (rect.y0 + rect.y1) / 2.0
                    if y_top <= y <= y_bot and _overlap(rect.x0, rect.x1, x_left, x_right) > 0:
                        candidates.append(y)
    return _cluster_numeric(candidates, tol=2.0)


# ---------------------------------------------------------------------------
# Header parsing
# ---------------------------------------------------------------------------

# Approximate y-bound of header block: top of page down to first banner (PIPE).
# We use label anchoring rather than fixed coordinates.

HEADER_FIELD_MAP = {
    # Internal field name -> list of label-token sequences (lowercased, joined by space)
    "piping_class": [["piping", "class"]],
    "service_commodity": [["service", "/", "commmodity"], ["service", "commmodity"]],
    "ansi_rating_material": [["ansi", "rating/material"]],
    "mawp": [["mawp"]],
    "pwht": [["p.w.h.t."]],
    "temperature_limits": [["temperature", "limits"]],
    "nde": [["n.d.e."]],
    "corrosion_allowance": [["c.a"]],
    "hydrotest": [["hydrotest"]],
    "design_code": [["design", "code"]],
    "revision": [["rev"]],
}


def _find_label_bbox(
    rows: list[list[tuple]], tokens: list[str]
) -> tuple[int, tuple[float, float, float, float]] | None:
    """Find a contiguous run of words in any row matching the given lowercased
    token sequence (case-insensitive). Returns (row_index, (x0,y0,x1,y1)) or None.
    """
    n = len(tokens)
    for ri, row in enumerate(rows):
        for i in range(0, len(row) - n + 1):
            window = row[i : i + n]
            if all(window[j][4].lower() == tokens[j] for j in range(n)):
                x0 = min(w[0] for w in window)
                y0 = min(w[1] for w in window)
                x1 = max(w[2] for w in window)
                y1 = max(w[3] for w in window)
                return ri, (x0, y0, x1, y1)
    return None


def _value_to_right(
    rows: list[list[tuple]],
    row_index: int,
    label_bbox: tuple[float, float, float, float],
    next_label_x: float | None = None,
    y_tol: float = 5.0,
) -> str:
    """Return the concatenated text of words to the right of a label bbox on
    the same row (within y_tol of the label center), up to next_label_x or EOL.
    """
    lx0, ly0, lx1, ly1 = label_bbox
    label_cy = (ly0 + ly1) / 2
    target_words: list[tuple] = []
    for row in rows:
        for w in row:
            cy = (w[1] + w[3]) / 2
            if abs(cy - label_cy) > y_tol:
                continue
            if w[0] < lx1 - 0.5:
                continue
            if next_label_x is not None and w[0] >= next_label_x - 0.5:
                continue
            target_words.append(w)
    target_words.sort(key=lambda w: w[0])
    return _join_words(target_words)


def parse_header_block(
    words: list[tuple],
    banner_top_y: float,
    diagnostics: dict[str, int] | None = None,
) -> dict[str, str]:
    """Extract header fields from the document header block.

    Parameters:
        words: list of (x0, y0, x1, y1, text, block, line, word) tuples
        banner_top_y: y of first banner (PIPE) — header is everything above it

    Returns dict mapping internal field names to extracted values
    (empty string when not found).
    """
    header_words = [w for w in words if w[3] <= banner_top_y]
    rows = _cluster_rows(header_words, y_tol=3.0)

    # Locate every label and its bbox
    label_bboxes: dict[str, tuple[int, tuple[float, float, float, float]]] = {}
    for field_name, alt_tokens in HEADER_FIELD_MAP.items():
        for tokens in alt_tokens:
            res = _find_label_bbox(rows, tokens)
            if res is not None:
                label_bboxes[field_name] = res
                break

    # Build per-row sorted list of label x-edges so we can stop scanning
    # at the next label on the same row.
    row_labels: dict[int, list[tuple[float, str]]] = {}
    for fname, (ri, bb) in label_bboxes.items():
        row_labels.setdefault(ri, []).append((bb[0], fname))
    for ri in row_labels:
        row_labels[ri].sort()

    out: dict[str, str] = {f: "" for f in HEADER_FIELD_MAP}

    for fname, (ri, bb) in label_bboxes.items():
        # Find the next label on the same row (by x) to bound the value scan
        same_row_sorted = row_labels.get(ri, [])
        next_x = None
        for x0, name in same_row_sorted:
            if x0 > bb[2] + 0.5:
                next_x = x0
                break
        out[fname] = _value_to_right(rows, ri, bb, next_label_x=next_x)

    # Special handling: PIPING CLASS value is the class id printed near top
    # right of the form (e.g., "AA1"). Capture all words to the right of the
    # PIPING CLASS label on the same row.
    # Already handled by _value_to_right.

    # Service description (secondary line): scan below the SERVICE /
    # COMMMODITY label inside the service-value x-band. The revision date sits
    # in a right-hand header column on many sheets, so the x-band must be
    # bounded on both sides and date-like tokens are rejected.
    sc = label_bboxes.get("service_commodity")
    if sc is not None:
        ri, bb = sc
        col_left = bb[2] + 5.0
        service_y0 = bb[1] - 5.0
        service_y1 = bb[3] + 5.0
        right_candidates = []
        for fname, (_lri, lbb) in label_bboxes.items():
            if fname == "service_commodity":
                continue
            lcy = (lbb[1] + lbb[3]) / 2.0
            if service_y0 <= lcy <= service_y1 and lbb[0] > bb[2]:
                right_candidates.append(lbb[0] - 2.0)
        if right_candidates:
            col_right = min(right_candidates)
        else:
            col_right = bb[2] + 360.0
            if diagnostics is not None:
                diagnostics["service_description_wide_bound_used"] = (
                    diagnostics.get("service_description_wide_bound_used", 0) + 1
                )

        date_re = re.compile(r"^\d{1,2}[./-]\d{1,2}[./-]\d{2,4}$")

        def row_service_words(row: list[tuple]) -> list[tuple]:
            return [
                w
                for w in row
                if w[0] >= col_left
                and w[2] <= col_right
                and not date_re.match(w[4])
                and not re.match(r"^Rev\\.?$", w[4], flags=re.IGNORECASE)
            ]

        service_value = ""
        for candidate_row in rows[ri + 1 : ri + 4]:
            ws = sorted(row_service_words(candidate_row), key=lambda w: w[0])
            text = _join_words(ws)
            if text:
                service_value = text
                break
        out["service_description"] = service_value
    else:
        out["service_description"] = ""

    # Revision date: typically appears below the "Rev N" label in the same column.
    rev = label_bboxes.get("revision")
    if rev is not None:
        ri, bb = rev
        col_left = bb[0] - 10.0
        col_right = bb[2] + 60.0
        # Search for a date-like token within col bounds, below label row
        date_re = re.compile(r"^\d{1,2}[./-]\d{1,2}[./-]\d{2,4}$")
        candidates: list[tuple[float, str]] = []
        for row in rows:
            for w in row:
                if w[1] <= bb[3]:
                    continue
                if w[0] < col_left or w[2] > col_right:
                    continue
                if date_re.match(w[4]):
                    candidates.append((w[1], w[4]))
        if candidates:
            candidates.sort()
            out["revision_date"] = candidates[0][1]
        else:
            out["revision_date"] = ""
    else:
        out["revision_date"] = ""

    return out


# ---------------------------------------------------------------------------
# Banner detection
# ---------------------------------------------------------------------------

# Banner words appear at the left rail. PyMuPDF reports rotated text with
# vertical bbox extents (y1 - y0 large compared to x1 - x0). We accept any
# word whose left edge is within ~30 points of the page left edge AND whose
# text matches a banner token.

BANNER_TOKENS = {
    "PIPE": "PIPE",
    "FLANGES": "FLANGES_FITTINGS",
    "FITTINGS": "FLANGES_FITTINGS",
    "BOLTING": "BOLTING_GASKETS",
    "GASKETS": "BOLTING_GASKETS",
    "TUBING": "TUBING",
    "VALVES": "VALVES",
}


def detect_banners(words: list[tuple]) -> dict[str, tuple[float, float]]:
    """Return mapping of canonical section name -> (y_top, y_bottom) of banner.

    For BOLTING_GASKETS, multiple banner words may exist; we merge them.
    Punctuation (trailing comma, slash, etc.) on banner words is tolerated.
    Banner words must (a) start near the left rail and (b) be vertically
    elongated (rotated text glyph: height >> width).
    """
    banners: dict[str, list[tuple[float, float]]] = {}
    for w in words:
        if w[0] >= 30:
            continue
        # Normalize: strip non-alphabetic edge chars
        text = re.sub(r"[^A-Za-z]+$", "", w[4]).upper()
        text = re.sub(r"^[^A-Za-z]+", "", text)
        if text not in BANNER_TOKENS:
            continue
        # Rotated banner glyph height should be >= width (allow some slack)
        height = w[3] - w[1]
        width = w[2] - w[0]
        if height < width:
            continue
        sec = BANNER_TOKENS[text]
        banners.setdefault(sec, []).append((w[1], w[3]))

    out: dict[str, tuple[float, float]] = {}
    for sec, bands in banners.items():
        y_top = min(b[0] for b in bands)
        y_bot = max(b[1] for b in bands)
        out[sec] = (y_top, y_bot)
    return out


# ---------------------------------------------------------------------------
# Inner header detection and column-band creation
# ---------------------------------------------------------------------------


def _find_inner_header_row(
    rows: list[list[tuple]], section: str
) -> tuple[int, list[tuple]] | None:
    """Find the inner header row for a given section by matching expected tokens.

    Looks for a row containing at least 3 of the expected primary tokens
    (ITEM/TYPE/NPS/OD/etc.) — sufficient to disambiguate from data rows.
    Accepts ITEM/TYPE as synonyms for the leftmost ("item-like") column.
    """
    expected = SECTION_INNER_HEADER_TOKENS[section]
    primary = []
    for tok in expected:
        primary.extend(tok.split())
    primary_set = {t.upper() for t in primary}
    primary_set.discard("/")  # noise
    # Accept TYPE/ITEM synonyms
    primary_set |= ITEM_COLUMN_SYNONYMS

    best_idx = None
    best_hits = 0
    for i, row in enumerate(rows):
        toks = {w[4].upper() for w in row}
        hits = len(toks & primary_set)
        # Require at least one of the section's *non-item* primary tokens
        # to be present, so we don't match arbitrary rows that just happen
        # to contain an ITEM/TYPE token.
        non_item = primary_set - ITEM_COLUMN_SYNONYMS
        non_item_hits = len(toks & non_item)
        if hits > best_hits and non_item_hits >= 2:
            best_hits = hits
            best_idx = i

    if best_idx is None or best_hits < 3:
        return None
    return best_idx, rows[best_idx]


def _match_header_columns(
    header_row: list[tuple], section: str
) -> list[tuple[str, list[tuple]]]:
    """Return matched header word groups in expected-column order."""
    expected = SECTION_INNER_HEADER_TOKENS[section]
    sorted_row = sorted(header_row, key=lambda w: w[0])
    matches: list[tuple[str, list[tuple]]] = []

    cursor = 0
    for col_idx_outer, col in enumerate(expected):
        col_tokens = col.split()
        accept_synonyms = col_idx_outer == 0 and col_tokens[0].upper() in ITEM_COLUMN_SYNONYMS
        found_start = None
        for start in range(cursor, len(sorted_row) - len(col_tokens) + 1):
            ok = True
            for k, ct in enumerate(col_tokens):
                w_text = sorted_row[start + k][4].upper()
                if k == 0 and accept_synonyms:
                    if w_text not in ITEM_COLUMN_SYNONYMS:
                        ok = False
                        break
                elif w_text != ct.upper():
                    ok = False
                    break
            if ok:
                found_start = start
                break
        if found_start is None:
            # Try fuzzy: just match the first token of the column name
            for start in range(cursor, len(sorted_row)):
                first_tok_text = sorted_row[start][4].upper()
                if first_tok_text == col_tokens[0].upper() or (
                    accept_synonyms and first_tok_text in ITEM_COLUMN_SYNONYMS
                ):
                    found_start = start
                    break
            if found_start is None:
                continue
            end = found_start + 1
            for k in range(1, len(col_tokens)):
                if (
                    end < len(sorted_row)
                    and sorted_row[end][4].upper() == col_tokens[k].upper()
                ):
                    end += 1
                else:
                    break
            # Use actual matched first-column word as canonical name when
            # synonym substitution occurred, so raw_rows reflects what the
            # PDF actually printed.
            if accept_synonyms:
                actual_first = sorted_row[found_start][4].upper()
                canonical = actual_first if len(col_tokens) == 1 else (
                    actual_first + " " + " ".join(col_tokens[1:])
                )
            else:
                canonical = col
            matches.append((canonical, sorted_row[found_start:end]))
            cursor = end
        else:
            end = found_start + len(col_tokens)
            if accept_synonyms:
                actual_first = sorted_row[found_start][4].upper()
                canonical = actual_first if len(col_tokens) == 1 else (
                    actual_first + " " + " ".join(col_tokens[1:])
                )
            else:
                canonical = col
            matches.append((canonical, sorted_row[found_start:end]))
            cursor = end

    return matches


def _header_midpoint_bands(
    header_row: list[tuple], matches: list[tuple[str, list[tuple]]], page_width: float
) -> list[tuple[float, float, str]]:
    """Fallback column bands derived from header label left edges."""
    label_lefts = [(col, min(w[0] for w in ws)) for col, ws in matches if ws]
    bands: list[tuple[float, float, str]] = []
    for idx, (col, x_lo) in enumerate(label_lefts):
        if idx == 0:
            band_lo = 0.0
        else:
            band_lo = (label_lefts[idx - 1][1] + x_lo) / 2.0
        if idx + 1 < len(label_lefts):
            band_hi = (x_lo + label_lefts[idx + 1][1]) / 2.0
        else:
            band_hi = page_width
        bands.append((band_lo, band_hi, col))
    return bands


def _interval_for_x(x: float, rule_xs: list[float]) -> int | None:
    for idx in range(len(rule_xs) - 1):
        if rule_xs[idx] <= x < rule_xs[idx + 1]:
            return idx
    if len(rule_xs) >= 2 and abs(x - rule_xs[-1]) < 0.01:
        return len(rule_xs) - 2
    return None


def _build_column_bands(
    header_row: list[tuple],
    section: str,
    page_width: float,
    *,
    page: Any | None = None,
    y_top: float | None = None,
    y_bottom: float | None = None,
    diagnostics: dict[str, int] | None = None,
) -> tuple[list[tuple[float, float, str]], str]:
    """Build (x_lo, x_hi, canonical_column_name) bands plus header signature."""
    expected = SECTION_INNER_HEADER_TOKENS[section]
    matches = _match_header_columns(header_row, section)
    signature = ",".join(canonical for canonical, _ws in matches)

    def inc(name: str, amount: int = 1) -> None:
        if diagnostics is not None:
            diagnostics[name] = diagnostics.get(name, 0) + amount

    if page is None or y_top is None or y_bottom is None:
        inc("rule_line_fallbacks")
        return _header_midpoint_bands(header_row, matches, page_width), signature

    rule_xs = extract_vertical_rules(page, y_top, y_bottom)
    if len(rule_xs) < 2:
        inc("rule_line_fallbacks")
        return _header_midpoint_bands(header_row, matches, page_width), signature

    matched_intervals: dict[str, int] = {}
    interval_to_cols: dict[int, list[str]] = {}
    for canonical, ws in matches:
        if not ws:
            continue
        x0 = min(w[0] for w in ws)
        x1 = max(w[2] for w in ws)
        interval = _interval_for_x((x0 + x1) / 2.0, rule_xs)
        if interval is None:
            continue
        matched_intervals[canonical] = interval
        interval_to_cols.setdefault(interval, []).append(canonical)

    # Fill expected columns that did not have literal header text. FA1 PIPE,
    # for example, prints DESCRIPTION vertically inside the data body instead
    # of on the header row.
    expected_to_interval: dict[str, int] = dict(matched_intervals)
    # If a missing column is squeezed out because the next header label is
    # visually centered over the preceding wide column, shift that next header
    # one interval to the right when an unused rule interval exists. This
    # handles FA1 PIPE: DESCRIPTION is not printed in the header row, while
    # NOTE / CODE is centered left of its data column.
    for idx, col in enumerate(expected):
        if col in expected_to_interval:
            continue
        prev_candidates = [
            (j, expected_to_interval[expected[j]])
            for j in range(0, idx)
            if expected[j] in expected_to_interval
        ]
        next_candidates = [
            (j, expected_to_interval[expected[j]])
            for j in range(idx + 1, len(expected))
            if expected[j] in expected_to_interval
        ]
        if not prev_candidates or not next_candidates:
            continue
        _prev_j, prev_i = prev_candidates[-1]
        next_j, next_i = next_candidates[0]
        if next_i == prev_i + 1 and next_i + 1 < len(rule_xs) - 1:
            occupied = set(expected_to_interval.values())
            if next_i + 1 not in occupied:
                for shift_idx in range(next_j, len(expected)):
                    shift_col = expected[shift_idx]
                    if shift_col in expected_to_interval:
                        expected_to_interval[shift_col] += 1

    for idx, col in enumerate(expected):
        if col in expected_to_interval:
            continue
        prev_candidates = [
            (j, expected_to_interval[expected[j]])
            for j in range(0, idx)
            if expected[j] in expected_to_interval
        ]
        next_candidates = [
            (j, expected_to_interval[expected[j]])
            for j in range(idx + 1, len(expected))
            if expected[j] in expected_to_interval
        ]
        assigned = None
        if prev_candidates and next_candidates:
            prev_j, prev_i = prev_candidates[-1]
            next_j, next_i = next_candidates[0]
            expected_gap = next_j - prev_j
            interval_gap = next_i - prev_i
            if expected_gap == interval_gap:
                assigned = prev_i + (idx - prev_j)
        elif prev_candidates:
            prev_j, prev_i = prev_candidates[-1]
            assigned = prev_i + (idx - prev_j)
        elif next_candidates:
            next_j, next_i = next_candidates[0]
            assigned = next_i - (next_j - idx)
        if assigned is not None and 0 <= assigned < len(rule_xs) - 1:
            expected_to_interval[col] = assigned

    duplicate_mapping = any(len(cols) > 1 for cols in interval_to_cols.values())
    missing_columns = [col for col in expected if col not in expected_to_interval]
    header_word_intervals = {
        _interval_for_x((w[0] + w[2]) / 2.0, rule_xs)
        for w in header_row
    }
    mapped_intervals = set(expected_to_interval.values())
    unmapped_header_intervals = {
        i for i in header_word_intervals if i is not None and i not in mapped_intervals
    }
    if duplicate_mapping or missing_columns or unmapped_header_intervals:
        inc(f"column_mapping_warning_{SECTION_SLUGS[section]}")
        inc("column_mapping_warnings")

    bands: list[tuple[float, float, str]] = []
    used_intervals: set[int] = set()
    for col in expected:
        interval = expected_to_interval.get(col)
        if interval is None or interval in used_intervals:
            continue
        bands.append((rule_xs[interval], rule_xs[interval + 1], col))
        used_intervals.add(interval)
    if len(bands) < 2:
        inc("rule_line_fallbacks")
        return _header_midpoint_bands(header_row, matches, page_width), signature

    inc("rule_line_columns_used")
    return bands, signature


# ---------------------------------------------------------------------------
# Row extraction within a section
# ---------------------------------------------------------------------------


def _section_words(
    words: list[tuple],
    band_y_lo: float,
    band_y_hi: float,
    page_width: float,
    exclude_left_rail: float = 35.0,
) -> list[tuple]:
    """Words in [band_y_lo, band_y_hi], excluding the left rail (banner)."""
    out = []
    for w in words:
        cy = (w[1] + w[3]) / 2
        if cy <= band_y_lo or cy >= band_y_hi:
            continue
        if w[2] <= exclude_left_rail:
            continue
        out.append(w)
    return out


def _assign_word_to_band(
    w: tuple, bands: list[tuple[float, float, str]]
) -> str | None:
    cx = (w[0] + w[2]) / 2
    for x_lo, x_hi, col in bands:
        if x_lo <= cx < x_hi:
            return col
    # Fallback: nearest band
    return None


def _row_bbox_overlaps(prev_row_y: tuple[float, float], y_lo: float, y_hi: float) -> bool:
    return not (y_hi <= prev_row_y[0] or y_lo >= prev_row_y[1])


def extract_section_rows(
    words: list[tuple],
    section: str,
    band_y_lo: float,
    band_y_hi: float,
    page_width: float,
    page: Any,
    page_num: int,
    diagnostics: dict[str, int],
) -> tuple[
    list[dict[str, str]],  # raw_rows: each = {raw_column: raw_value} per row
    str,  # header signature
]:
    """Extract rows within one section. Returns (list of {col: value} dicts, signature).

    Each returned row dict carries the per-section raw column names as keys.
    Continuation visual rows (wrapped descriptions) are merged into the
    logical row anchored above them.
    """
    sec_words = _section_words(words, band_y_lo, band_y_hi, page_width)
    if not sec_words:
        return [], ""

    rows = _cluster_rows(sec_words, y_tol=3.0)

    inner = _find_inner_header_row(rows, section)
    if inner is None:
        return [], ""
    header_idx, header_row = inner
    bands, signature = _build_column_bands(
        header_row,
        section,
        page_width,
        page=page,
        y_top=band_y_lo,
        y_bottom=band_y_hi,
        diagnostics=diagnostics,
    )
    if not bands:
        return [], signature

    data_rows = rows[header_idx + 1 :]

    # Cluster data rows further: a row whose primary anchor cells (ITEM/NPS or
    # TYPE/OD) are blank but which has DESCRIPTION text is a continuation.
    primary_anchor_cols = {
        "PIPE": ["NPS"],
        "FLANGES_FITTINGS": ["NPS"],
        "BOLTING_GASKETS": ["NPS"],
        "TUBING": ["OD"],
        "VALVES": ["NPS", "TAG"],
    }[section]
    item_like_col = "TYPE" if section == "TUBING" else "ITEM"

    def _row_to_cells(row: list[tuple]) -> dict[str, list[tuple]]:
        cells: dict[str, list[tuple]] = {b[2]: [] for b in bands}
        for w in row:
            col = _assign_word_to_band(w, bands)
            if col is None:
                diagnostics["unmapped_words"] = diagnostics.get("unmapped_words", 0) + 1
                continue
            cells[col].append(w)
        return cells

    def _cell_text(cell: list[tuple]) -> str:
        cell_sorted = sorted(cell, key=lambda w: w[0])
        return _join_words(cell_sorted)

    logical_rows: list[dict[str, Any]] = []

    def _cells_anchor_blank(cells: dict[str, list[tuple]]) -> bool:
        return all(_cell_text(cells.get(c, [])) == "" for c in primary_anchor_cols)

    def _cells_item_present(cells: dict[str, list[tuple]]) -> bool:
        return _cell_text(cells.get(item_like_col, [])) != ""

    def _extend_logical_row(target: dict[str, Any], cells: dict[str, list[tuple]], row_words: list[tuple]) -> None:
        for col, ws in cells.items():
            target["cells"].setdefault(col, []).extend(ws)
        if row_words:
            target["y_top"] = min(target["y_top"], min(w[1] for w in row_words))
            target["y_bottom"] = max(target["y_bottom"], max(w[3] for w in row_words))

    for raw in data_rows:
        cells = _row_to_cells(raw)
        row_words = [w for ws in cells.values() for w in ws]
        anchor_blank = _cells_anchor_blank(cells)
        item_present = _cells_item_present(cells)

        merge_with_previous = False
        if logical_rows:
            prev_cells = logical_rows[-1]["cells"]
            prev_anchor_blank = _cells_anchor_blank(prev_cells)
            prev_item_present = _cells_item_present(prev_cells)
            if anchor_blank and not item_present:
                merge_with_previous = True
            elif anchor_blank and item_present and prev_anchor_blank and prev_item_present:
                merge_with_previous = True
            elif (not anchor_blank) and prev_anchor_blank and prev_item_present:
                merge_with_previous = True

        if merge_with_previous:
            _extend_logical_row(logical_rows[-1], cells, row_words)
            diagnostics["row_continuations_merged"] = (
                diagnostics.get("row_continuations_merged", 0) + 1
            )
        else:
            if row_words:
                y_top = min(w[1] for w in row_words)
                y_bottom = max(w[3] for w in row_words)
            else:
                y_top = 0.0
                y_bottom = 0.0
            logical_rows.append({"cells": cells, "y_top": y_top, "y_bottom": y_bottom})

    item_col = "TYPE" if section == "TUBING" else "ITEM"
    item_band = next((b for b in bands if b[2] in ITEM_COLUMN_SYNONYMS), None)
    if item_band is not None:
        h_rules = extract_horizontal_rules(page, item_band[0], item_band[1], band_y_lo, band_y_hi)
        for idx, logical in enumerate(logical_rows):
            item_words = logical["cells"].get(item_col, [])
            if not item_words:
                continue
            item_text = _cell_text_lines_first(item_words)
            if not item_text:
                continue
            item_y = (
                min(w[1] for w in item_words) + max(w[3] for w in item_words)
            ) / 2.0
            above = [y for y in h_rules if y < item_y]
            below = [y for y in h_rules if y > item_y]
            if not above or not below:
                continue
            span_top = max(above)
            span_bottom = min(below)
            covered = [
                row_idx
                for row_idx, row in enumerate(logical_rows)
                if span_top - 0.75
                <= (row["y_top"] + row["y_bottom"]) / 2.0
                <= span_bottom + 0.75
            ]
            if not covered:
                continue
            first_idx = min(covered)
            if first_idx != idx:
                logical_rows[first_idx]["cells"][item_col] = item_words
                logical["cells"][item_col] = []
                diagnostics["item_first_row_anchored"] = (
                    diagnostics.get("item_first_row_anchored", 0) + 1
                )

    # Convert to text dicts
    out_rows: list[dict[str, str]] = []
    for logical in logical_rows:
        cells = logical["cells"]
        row_dict: dict[str, str] = {}
        for col, ws in cells.items():
            row_dict[col] = _cell_text_lines_first(ws)
        row_dict["__y_top"] = f"{logical['y_top']:.3f}"
        row_dict["__y_bottom"] = f"{logical['y_bottom']:.3f}"
        out_rows.append(row_dict)

    # Drop trailing all-blank rows
    while out_rows and all(
        v == "" for k, v in out_rows[-1].items() if not k.startswith("__")
    ):
        out_rows.pop()

    return out_rows, signature


# ---------------------------------------------------------------------------
# Long-form normalization
# ---------------------------------------------------------------------------


def _item_value(raw_row: dict[str, str]) -> str:
    """Pick the section's item-or-type value from either ITEM or TYPE keys."""
    return raw_row.get("ITEM") or raw_row.get("TYPE") or ""


def _normalize_to_tables_row(
    section: str, raw_row: dict[str, str], item_filled: bool
) -> dict[str, str]:
    if section == "PIPE":
        return {
            "item_or_type": _item_value(raw_row),
            "item_filled": "true" if item_filled else "false",
            "nps_or_size": raw_row.get("NPS", ""),
            "schedule_or_rating": raw_row.get("MIN SCH", ""),
            "tag": "",
            "conn_or_ends": raw_row.get("ENDS", ""),
            "trim": "",
            "description": raw_row.get("DESCRIPTION", ""),
            "note_code": raw_row.get("NOTE / CODE", ""),
            "note_code_filled": "false",
        }
    if section == "FLANGES_FITTINGS":
        return {
            "item_or_type": _item_value(raw_row),
            "item_filled": "true" if item_filled else "false",
            "nps_or_size": raw_row.get("NPS", ""),
            "schedule_or_rating": raw_row.get("MIN SCH/RTG", ""),
            "tag": "",
            "conn_or_ends": raw_row.get("CONN.", ""),
            "trim": "",
            "description": raw_row.get("DESCRIPTION", ""),
            "note_code": raw_row.get("NOTE / CODE", ""),
            "note_code_filled": "false",
        }
    if section == "BOLTING_GASKETS":
        return {
            "item_or_type": _item_value(raw_row),
            "item_filled": "true" if item_filled else "false",
            "nps_or_size": raw_row.get("NPS", ""),
            "schedule_or_rating": raw_row.get("RTG", ""),
            "tag": "",
            "conn_or_ends": "",
            "trim": "",
            "description": raw_row.get("DESCRIPTION", ""),
            "note_code": raw_row.get("NOTE / CODE", ""),
            "note_code_filled": "false",
        }
    if section == "TUBING":
        return {
            "item_or_type": _item_value(raw_row),
            "item_filled": "true" if item_filled else "false",
            "nps_or_size": raw_row.get("OD", ""),
            "schedule_or_rating": raw_row.get("MIN WT", ""),
            "tag": "",
            "conn_or_ends": "",
            "trim": "",
            "description": raw_row.get("DESCRIPTION", ""),
            "note_code": raw_row.get("NOTE / CODE", ""),
            "note_code_filled": "false",
        }
    if section == "VALVES":
        return {
            "item_or_type": _item_value(raw_row),
            "item_filled": "true" if item_filled else "false",
            "nps_or_size": raw_row.get("NPS", ""),
            "schedule_or_rating": raw_row.get("CLASS/RTG", ""),
            "tag": raw_row.get("TAG", ""),
            "conn_or_ends": raw_row.get("ENDS", ""),
            "trim": raw_row.get("TRIM", ""),
            "description": raw_row.get("DESCRIPTION", ""),
            "note_code": raw_row.get("NOTE / CODE", ""),
            "note_code_filled": "false",
        }
    return {}


# ---------------------------------------------------------------------------
# Top-level extraction
# ---------------------------------------------------------------------------


def extract_pipe_spec(pdf_path: Path) -> ExtractionResult:
    """Extract a Pipe Spec PDF into ExtractionResult.

    Idempotent and deterministic.
    """
    pdf_path = Path(pdf_path)
    source_pdf = pdf_path.name
    sha = _sha256_of_file(pdf_path)

    parsed_name = parse_filename(pdf_path.stem)
    if parsed_name is None:
        # Fail-fast: non-conforming filename
        result = ExtractionResult(
            spec_id=pdf_path.stem,
            revision="",
            source_pdf=source_pdf,
            source_sha256=sha,
            page_count=0,
            blank_pages=0,
            status="parse_fail",
            failure_reason=(
                f"Filename does not match required pattern '<spec_id>_R<digits>': "
                f"{pdf_path.stem!r}"
            ),
        )
        result.diagnostics = _diagnostics_from(result, header_label_coverage=0,
                                               section_count=0,
                                               template_checks={"filename_pattern": False})
        return result

    spec_id, revision = parsed_name

    diagnostics_counters: dict[str, int] = {
        "unmapped_words": 0,
        "row_continuations_merged": 0,
        "item_forward_fills_applied": 0,
        "item_first_row_anchored": 0,
        "rule_line_columns_used": 0,
        "rule_line_fallbacks": 0,
        "column_mapping_warnings": 0,
        "service_description_wide_bound_used": 0,
    }

    try:
        doc = fitz.open(pdf_path)
    except Exception as exc:
        result = ExtractionResult(
            spec_id=spec_id,
            revision=revision,
            source_pdf=source_pdf,
            source_sha256=sha,
            page_count=0,
            blank_pages=0,
            status="parse_fail",
            failure_reason=f"PyMuPDF failed to open file: {exc!r}",
        )
        result.diagnostics = _diagnostics_from(
            result, header_label_coverage=0, section_count=0,
            template_checks={"pdf_open": False}
        )
        return result

    page_count = doc.page_count
    blank_pages = 0

    # Find the first non-blank page (the form page). Pipe specs are
    # single-page; only blank trailing pages are tolerated.
    form_page_num: int | None = None
    form_page_words: list[tuple] = []
    for i in range(page_count):
        page = doc[i]
        words = page.get_text("words")
        if not words:
            blank_pages += 1
            continue
        if form_page_num is None:
            form_page_num = i + 1  # 1-indexed
            form_page_words = words

    if form_page_num is None:
        doc.close()
        result = ExtractionResult(
            spec_id=spec_id,
            revision=revision,
            source_pdf=source_pdf,
            source_sha256=sha,
            page_count=page_count,
            blank_pages=blank_pages,
            status="parse_fail",
            failure_reason="PDF has no pages with extractable words.",
        )
        result.diagnostics = _diagnostics_from(
            result, header_label_coverage=0, section_count=0,
            template_checks={"any_words": False}, extra=diagnostics_counters
        )
        return result

    # Cache form page geometry for column-band right edge and section bounds.
    form_page = doc[form_page_num - 1]
    page_width = form_page.rect.width
    page_height = form_page.rect.height

    # --- Banner detection ---
    banners = detect_banners(form_page_words)
    section_count = len(banners)

    template_checks: dict[str, bool] = {}
    template_checks["all_5_banners_present"] = section_count == 5

    # --- Header parsing (above first banner) ---
    if banners:
        banner_top_y = min(b[0] for b in banners.values())
    else:
        banner_top_y = 0.0
    header_fields = (
        parse_header_block(form_page_words, banner_top_y, diagnostics_counters)
        if banners
        else {}
    )

    header_label_coverage = sum(1 for v in header_fields.values() if v)
    # Mandatory header label coverage (count how many of the 7 mandatory are populated)
    mandatory_field_keys = [
        "piping_class",
        "revision",
        "service_commodity",
        "ansi_rating_material",
        "mawp",
        "temperature_limits",
        "design_code",
    ]
    mandatory_missing = [k for k in mandatory_field_keys if not header_fields.get(k)]
    template_checks["mandatory_header_labels_present"] = len(mandatory_missing) == 0

    # --- Per-section row extraction ---
    # The rotated banner glyphs are positioned VERTICALLY within their section
    # (not at the top), so we cannot use banner y_top -> next banner y_top as
    # section bounds. Instead, locate each section's inner header row directly
    # by scanning all rows of the page for the expected primary tokens, then
    # use inner-header y positions to delimit sections in printed order.
    page_rows = _cluster_rows(
        [w for w in form_page_words if w[2] > 35.0],  # exclude rotated banners
        y_tol=3.0,
    )
    # Score every page row for each section's expected token set, then assign
    # each section to a distinct row in printed order. Sections appear in a
    # known print order (PIPE, FLANGES_FITTINGS, BOLTING_GASKETS, TUBING,
    # VALVES) — so we scan page_rows top-down and pick rows that best match
    # the next expected section's distinguishing tokens.

    # Distinguishing tokens (helps disambiguate similar inner headers).
    distinguishing = {
        "PIPE": {"ENDS"},
        "FLANGES_FITTINGS": {"CONN."},
        "BOLTING_GASKETS": {"RTG"},
        "TUBING": {"OD", "MIN", "WT"},
        "VALVES": {"TAG", "TRIM"},
    }

    def _row_match_score(row: list[tuple], section: str) -> int:
        expected = SECTION_INNER_HEADER_TOKENS[section]
        primary = []
        for tok in expected:
            primary.extend(tok.split())
        primary_set = {t.upper() for t in primary} - {"/"}
        primary_set |= ITEM_COLUMN_SYNONYMS
        toks = {w[4].upper() for w in row}
        non_item = primary_set - ITEM_COLUMN_SYNONYMS
        non_item_hits = len(toks & non_item)
        if non_item_hits < 2:
            return 0
        # Bonus for distinguishing tokens
        dist_hits = len(toks & distinguishing.get(section, set()))
        return len(toks & primary_set) + 5 * dist_hits

    # Pre-compute (y, row_index, row) sorted by y (already true from
    # _cluster_rows).
    page_rows_with_y: list[tuple[float, int, list[tuple]]] = []
    for ri, row in enumerate(page_rows):
        if not row:
            continue
        y_mid = sum((w[1] + w[3]) / 2 for w in row) / len(row)
        page_rows_with_y.append((y_mid, ri, row))

    # Find inner headers using y-domain bracketing by banner positions.
    # Banners are rotated and sit vertically centered within their sections.
    # Each section's y-domain is bounded by adjacent banners' y_top values:
    #   domain(section_i) = (prev_banner_y_top, next_banner_y_top)
    # within which we pick the highest-scoring inner-header-like row.
    # When token sets across two adjacent sections are identical (e.g., a
    # spec where both PIPE and FLANGES_FITTINGS rows print "TYPE NPS MIN
    # SCH CONN. DESCRIPTION NOTE / CODE"), the row with the smallest y in
    # the domain is taken — this matches the printed top-to-bottom order.
    inner_header_locations: list[tuple[float, str, int]] = []
    used_indices: set[int] = set()
    banner_order = sorted(banners.items(), key=lambda kv: kv[1][0])

    for i, (sec, (banner_y_top, banner_y_bot)) in enumerate(banner_order):
        # Lower bound: previous banner's y_top, or 0 for first section.
        if i == 0:
            y_lo = 0.0
        else:
            y_lo = banner_order[i - 1][1][0]
        # Upper bound: next banner's y_top, or page height for last section.
        if i + 1 < len(banner_order):
            y_hi = banner_order[i + 1][1][0]
        else:
            y_hi = page_height

        cands: list[tuple[int, float, int]] = []  # (score, y, ri)
        for y_mid, ri, row in page_rows_with_y:
            if ri in used_indices:
                continue
            if y_mid <= y_lo or y_mid >= y_hi:
                continue
            score = _row_match_score(row, sec)
            if score >= 3:
                cands.append((score, y_mid, ri))
        if not cands:
            continue
        # Highest score wins; tie-break by smallest y (earliest in print
        # order) so adjacent sections with identical inner-header token
        # sets are distinguished by position.
        cands.sort(key=lambda c: (-c[0], c[1]))
        score, y_mid, ri = cands[0]
        inner_header_locations.append((y_mid, sec, ri))
        used_indices.add(ri)

    inner_header_locations.sort(key=lambda t: t[0])

    # Build section bounds: start = inner header y; end = next inner header y
    # (or page bottom). Each section's data words live below its own inner
    # header and above the next section's inner header.
    section_y_bounds: dict[str, tuple[float, float]] = {}
    for i, (y_mid, sec, _ridx) in enumerate(inner_header_locations):
        if i + 1 < len(inner_header_locations):
            y_end = inner_header_locations[i + 1][0] - 0.5
        else:
            y_end = page_height
        # Start a hair above the inner header so the header row clusters into
        # the section's row set and is detectable.
        section_y_bounds[sec] = (y_mid - 5.0, y_end)

    table_rows: list[dict[str, str]] = []
    raw_rows: list[dict[str, str]] = []
    inner_header_present: dict[str, bool] = {sec: False for sec in SECTION_ORDER}

    piping_class_value = header_fields.get("piping_class", "")

    # Stable provenance fields shared across all rows
    base_provenance = {
        "piping_class": piping_class_value,
        "source_pdf": source_pdf,
        "source_revision": revision,
        "source_sha256": sha,
        "source_page": str(form_page_num),
    }

    for section in SECTION_ORDER:
        if section not in section_y_bounds:
            continue
        y_lo, y_hi = section_y_bounds[section]
        sec_rows, signature = extract_section_rows(
            form_page_words,
            section,
            y_lo,
            y_hi,
            page_width,
            form_page,
            form_page_num,
            diagnostics_counters,
        )
        if signature:
            inner_header_present[section] = True

        # Forward-fill ITEM / TYPE within section. The actual column name
        # depends on what the PDF printed; pick whichever ITEM-like key
        # appears in the raw rows (ITEM or TYPE).
        item_col_name: str | None = None
        for r in sec_rows:
            for k in ("ITEM", "TYPE"):
                if k in r:
                    item_col_name = k
                    break
            if item_col_name:
                break
        if item_col_name is None:
            item_col_name = "TYPE" if section == "TUBING" else "ITEM"
        last_item = ""
        slug = SECTION_SLUGS[section]
        for ridx, raw in enumerate(sec_rows, start=1):
            current_item = raw.get(item_col_name, "")
            item_filled = False
            if current_item == "" and last_item != "":
                raw[item_col_name] = last_item
                item_filled = True
                diagnostics_counters["item_forward_fills_applied"] = (
                    diagnostics_counters.get("item_forward_fills_applied", 0) + 1
                )
            elif current_item != "":
                last_item = current_item
            section_row_id = f"{slug}:{ridx:03d}"

            normalized = _normalize_to_tables_row(section, raw, item_filled)
            row_out = {
                **base_provenance,
                "section": section,
                "section_row_id": section_row_id,
                "source_header_signature": signature,
                **normalized,
            }
            table_rows.append(row_out)

            # Build raw rows (long format) for audit
            for col, val in raw.items():
                if col.startswith("__"):
                    continue
                raw_rows.append(
                    {
                        **base_provenance,
                        "section": section,
                        "section_row_id": section_row_id,
                        "raw_column": col,
                        "raw_value": val,
                    }
                )

    template_checks["all_sections_have_inner_header"] = all(
        inner_header_present.get(sec, False) for sec in SECTION_ORDER if sec in section_y_bounds
    ) and section_count == 5

    # --- Determine status ---
    failure_reason = ""
    status = "ok"
    if not template_checks.get("all_5_banners_present", False):
        status = "parse_fail"
        failure_reason = (
            f"Expected all 5 section banners; found {section_count}: "
            f"{sorted(banners.keys())}"
        )
    elif not template_checks.get("mandatory_header_labels_present", False):
        status = "parse_fail"
        failure_reason = (
            "Mandatory header labels missing values: "
            + ",".join(mandatory_missing)
        )
    elif not template_checks.get("all_sections_have_inner_header", False):
        missing_inner = [s for s in SECTION_ORDER if not inner_header_present.get(s)]
        status = "parse_fail"
        failure_reason = "Sections missing recognizable inner header: " + ",".join(missing_inner)

    # --- Build header rows (always — but only emitted on ok) ---
    header_field_order = [
        "piping_class",
        "service_commodity",
        "service_description",
        "ansi_rating_material",
        "mawp",
        "pwht",
        "temperature_limits",
        "nde",
        "corrosion_allowance",
        "hydrotest",
        "design_code",
        "revision",
        "revision_date",
    ]
    header_csv_rows = []
    for fname in header_field_order:
        header_csv_rows.append(
            {
                "field": fname,
                "value": header_fields.get(fname, ""),
                "source_pdf": source_pdf,
                "source_revision": revision,
                "source_sha256": sha,
            }
        )

    # --- Stable order: rows are already produced in (section, section_row_id) order ---
    # Re-sort to be defensive.
    table_rows.sort(key=lambda r: (SECTION_ORDER.index(r["section"]), r["section_row_id"]))
    raw_rows.sort(
        key=lambda r: (
            SECTION_ORDER.index(r["section"]),
            r["section_row_id"],
            r["raw_column"],
        )
    )

    result = ExtractionResult(
        spec_id=spec_id,
        revision=revision,
        source_pdf=source_pdf,
        source_sha256=sha,
        page_count=page_count,
        blank_pages=blank_pages,
        header_rows=header_csv_rows if status == "ok" else [],
        table_rows=table_rows if status == "ok" else [],
        raw_rows=raw_rows if status == "ok" else [],
        status=status,
        failure_reason=failure_reason,
    )

    # Per-section row counts
    counts = {sec: 0 for sec in SECTION_ORDER}
    for r in table_rows:
        counts[r["section"]] = counts.get(r["section"], 0) + 1

    result.diagnostics = _diagnostics_from(
        result,
        header_label_coverage=header_label_coverage,
        section_count=section_count,
        template_checks=template_checks,
        extra={
            **diagnostics_counters,
            "rows_pipe": counts.get("PIPE", 0),
            "rows_flanges_fittings": counts.get("FLANGES_FITTINGS", 0),
            "rows_bolting_gaskets": counts.get("BOLTING_GASKETS", 0),
            "rows_tubing": counts.get("TUBING", 0),
            "rows_valves": counts.get("VALVES", 0),
        },
    )

    doc.close()
    return result


def _diagnostics_from(
    result: ExtractionResult,
    *,
    header_label_coverage: int,
    section_count: int,
    template_checks: dict[str, bool],
    extra: dict[str, int] | None = None,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    extra = extra or {}

    def add(metric: str, value: Any, note: str = "") -> None:
        rows.append({"metric": metric, "value": str(value), "note": note})

    add("source_pdf", result.source_pdf)
    add("spec_id", result.spec_id)
    add("source_revision", result.revision)
    add("source_sha256", result.source_sha256)
    add("page_count", result.page_count)
    add("blank_pages_skipped", result.blank_pages)
    add("header_label_coverage", header_label_coverage)
    add("section_count", section_count)
    add("rows_pipe", extra.get("rows_pipe", 0))
    add("rows_flanges_fittings", extra.get("rows_flanges_fittings", 0))
    add("rows_bolting_gaskets", extra.get("rows_bolting_gaskets", 0))
    add("rows_tubing", extra.get("rows_tubing", 0))
    add("rows_valves", extra.get("rows_valves", 0))
    add("unmapped_words", extra.get("unmapped_words", 0))
    add("row_continuations_merged", extra.get("row_continuations_merged", 0))
    add("item_forward_fills_applied", extra.get("item_forward_fills_applied", 0))
    add("item_first_row_anchored", extra.get("item_first_row_anchored", 0))
    add("rule_line_columns_used", extra.get("rule_line_columns_used", 0))
    add("rule_line_fallbacks", extra.get("rule_line_fallbacks", 0))
    add("column_mapping_warnings", extra.get("column_mapping_warnings", 0))
    add(
        "service_description_wide_bound_used",
        extra.get("service_description_wide_bound_used", 0),
    )
    add("parse_status", result.status)
    if result.failure_reason:
        add("failure_reason", result.failure_reason)
    for check, passed in sorted(template_checks.items()):
        add(f"template_check.{check}", "pass" if passed else "fail")
    return rows
