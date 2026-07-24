#!/usr/bin/env python3
"""Build a per-source TOC skeleton + dispatch plan for DOMAIN_DECOMP Phase 1.

Reads a single source's <book>.md and <book>_assets_manifest.json. Emits two
JSON artifacts:

  - <book>_skeleton.json
      Ordered list of every Markdown heading found in <book>.md, with depth,
      parent SectionID, line range, inferred page range, inline figure / table /
      equation reference labels, asset IDs materialized inside the section's
      line range, an estimated MD-token cost, and a heuristic front/back-matter
      flag intended as a starting point for the Gate 1.5 reviewer.

  - <book>_dispatch_plan.json
      Ordered list of dispatch units (one per slice of the reviewable skeleton)
      that the orchestrator iterates in Phase 2 to fan out the
      `domain-source-atomize` skill. Each unit has a stable unit_id, a line
      range that is a contiguous slice of <book>.md, the list of target
      SectionIDs covered by the slice, an estimated token cost, and a flag for
      oversized-section dispatch units. Clustering rules:

      (a) never split mid-section while the section is below the split
          threshold;
      (b) cluster adjacent in-scope sections up to --budget-tokens;
      (c) when a single section exceeds --section-split-threshold, emit each
          of its ### sub-section descendants as its own unit, then fall back
          to a single oversized unit for any leaf section that still exceeds
          the threshold without further sub-divisions.

Front-matter and back-matter sections (heuristic flag or override) are
excluded from the dispatch plan.

This is a deterministic tool. No LLM dependency.

Usage:
  python3 tools/decomp/build_source_skeleton.py \\
      --md <book>.md \\
      --asset-manifest <book>_assets_manifest.json \\
      --output-skeleton <book>_skeleton.json \\
      --output-dispatch-plan <book>_dispatch_plan.json \\
      [--source-prefix PSE] \\
      [--budget-tokens 15000] \\
      [--section-split-threshold 25000] \\
      [--front-matter-overrides JSON] \\
      [--back-matter-overrides JSON] \\
      [--in-scope-overrides JSON]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUMBERED_TITLE_RE = re.compile(r"^(\d+(?:\.\d+)*)\s+(.+)$")
CHAPTER_TITLE_RE = re.compile(r"^Chapter\s+(\d+)", re.IGNORECASE)
INLINE_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
INLINE_LINK_PNG_RE = re.compile(r"\[(?:[^\]]*)\]\(([^)\s]+\.png)\)")
INLINE_LINK_CSV_RE = re.compile(r"\[(?:[^\]]*)\]\(([^)\s]+\.csv)\)")
PAGE_MARKER_RE = re.compile(r"<!--\s*PDF2MD-ASSETS:(?:START|END)\s+page=(\d+)\s*-->")
FIG_REF_RE = re.compile(r"\b(?:Fig|Figure|FIG)\.?\s*(\d+(?:[.\-]\d+)+[A-Za-z]?)")
TABLE_REF_RE = re.compile(r"\bTable\s*(\d+(?:[.\-]\d+)+[A-Za-z]?)")
EQ_REF_RE = re.compile(r"\b(?:Eq|Equation|EQ)\.?\s*\(?(\d+(?:[.\-]\d+)+[a-z]?)\)?")
WORD_RE = re.compile(r"\S+")

FRONT_MATTER_PATTERNS = [
    r"^(?:cover|title\s*page|frontispiece)\b",
    r"^(?:dedication|epigraph)\b",
    r"^(?:contents|table\s+of\s+contents|toc)\b",
    r"^(?:preface|foreword)\b",
    r"^acknowledg",
    r"^(?:nomenclature|notation|symbols|abbreviations)\b",
    r"^(?:copyright|colophon|disclaimer|legal\s+notice)\b",
    r"^about\s+the\s+author",
    r"^(?:isbn|library\s+of\s+congress)",
]
BACK_MATTER_PATTERNS = [
    r"^(?:references|bibliography|works\s+cited)\b",
    r"^(?:index)\b",
    r"^(?:glossary)\b",
    r"^author\s+index",
    r"^subject\s+index",
]
FRONT_MATTER_RE = [re.compile(p, re.IGNORECASE) for p in FRONT_MATTER_PATTERNS]
BACK_MATTER_RE = [re.compile(p, re.IGNORECASE) for p in BACK_MATTER_PATTERNS]
NOISE_TITLE_RE = re.compile(r"^Unmatched\s+Page\s+Assets$", re.IGNORECASE)

WORD_TO_TOKEN_RATIO = 1.35


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build skeleton JSON + dispatch plan JSON for one source book.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--md", required=True, type=Path,
                   help="Path to the source's <book>.md")
    p.add_argument("--asset-manifest", required=True, type=Path,
                   help="Path to the source's <book>_assets_manifest.json")
    p.add_argument("--output-skeleton", required=True, type=Path,
                   help="Where to write <book>_skeleton.json")
    p.add_argument("--output-dispatch-plan", required=True, type=Path,
                   help="Where to write <book>_dispatch_plan.json")
    p.add_argument("--source-prefix", default=None,
                   help="Short prefix to use for IDs in this skeleton "
                        "(default: derive from manifest doc_stem)")
    p.add_argument("--budget-tokens", type=int, default=15000,
                   help="Soft per-unit token budget (default 15000)")
    p.add_argument("--section-split-threshold", type=int, default=25000,
                   help="Section size at/above which we attempt sub-section "
                        "split (default 25000)")
    p.add_argument("--front-matter-overrides", default=None,
                   help="JSON array of SectionIDs to force-flag as front matter")
    p.add_argument("--back-matter-overrides", default=None,
                   help="JSON array of SectionIDs to force-flag as back matter")
    p.add_argument("--in-scope-overrides", default=None,
                   help="JSON array of SectionIDs to force in scope by clearing "
                        "front/back-matter flags")
    return p.parse_args()


def derive_prefix(doc_stem: str) -> str:
    """Make a short identifier prefix from a doc_stem.

    Strategy: take initials from words separated by '-' or '_'. If the final
    word is purely numeric (e.g., a volume number), append the full numeric
    token to keep volumes distinguishable. Truncate to 8 chars max. Fall back
    to a 4-char alphanumeric truncation if initials don't yield ≥2 chars.
    """
    parts = [p for p in re.split(r"[-_\s]+", doc_stem) if p]
    if not parts:
        return "SRC"
    initials_letters = "".join(p[0] for p in parts if not p.isdigit())
    trailing_digits = parts[-1] if parts[-1].isdigit() else ""
    combined = (initials_letters + trailing_digits).upper()
    if len(combined) >= 2:
        return combined[:8]
    alnum = re.sub(r"[^A-Za-z0-9]", "", doc_stem)
    return alnum[:4].upper() or "SRC"


def load_md(md_path: Path) -> list[str]:
    return md_path.read_text(encoding="utf-8").splitlines()


def load_manifest(manifest_path: Path) -> dict:
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def build_png_to_asset(manifest: dict) -> dict[str, dict]:
    """Index manifest assets by png_path basename for inline-link lookup."""
    out: dict[str, dict] = {}
    for a in manifest.get("assets", []):
        png = a.get("png_path") or ""
        if png:
            out[Path(png).name] = a
            out[png] = a
    return out


def extract_section_number(title: str) -> str | None:
    m = NUMBERED_TITLE_RE.match(title)
    return m.group(1) if m else None


def is_front_matter_heuristic(title: str, line_start: int, total_lines: int) -> bool:
    stripped = title.strip()
    if NUMBERED_TITLE_RE.match(stripped):
        return False
    if not any(rx.search(stripped) for rx in FRONT_MATTER_RE):
        return False
    # Only flag when the section sits in the first 10% of the document.
    return line_start <= max(1, total_lines // 10)


def is_back_matter_heuristic(title: str, line_end: int, total_lines: int) -> bool:
    stripped = title.strip()
    if NUMBERED_TITLE_RE.match(stripped):
        return False
    if not any(rx.search(stripped) for rx in BACK_MATTER_RE):
        return False
    # Only flag when the section sits in the last 10% of the document.
    return line_end >= max(1, total_lines - total_lines // 10)


def estimate_tokens(lines: list[str], line_start: int, line_end: int) -> int:
    word_count = 0
    for ln in lines[line_start - 1:line_end]:
        word_count += len(WORD_RE.findall(ln))
    return int(round(word_count * WORD_TO_TOKEN_RATIO))


def parse_headings(lines: list[str]) -> list[dict]:
    """Return one entry per heading line: depth, title, line_no, noise flag."""
    out: list[dict] = []
    for i, raw in enumerate(lines, start=1):
        m = HEADING_RE.match(raw)
        if not m:
            continue
        hashes, title = m.group(1), m.group(2).strip()
        if NOISE_TITLE_RE.match(title):
            continue
        out.append({
            "depth": len(hashes),
            "title": title,
            "line_no": i,
        })
    return out


def assign_parents(headings: list[dict]) -> list[dict]:
    """Walk headings in document order and set parent_index using depth."""
    stack: list[tuple[int, int]] = []  # (depth, index_into_headings)
    for idx, h in enumerate(headings):
        while stack and stack[-1][0] >= h["depth"]:
            stack.pop()
        h["parent_index"] = stack[-1][1] if stack else None
        stack.append((h["depth"], idx))
    return headings


def section_id(prefix: str, ordinal: int) -> str:
    return f"SEC-{prefix}-{ordinal:04d}"


def collect_page_line_index(lines: list[str]) -> list[tuple[int, int]]:
    """Return [(line_no, page_no), ...] for every PDF2MD-ASSETS page marker."""
    out: list[tuple[int, int]] = []
    for i, raw in enumerate(lines, start=1):
        m = PAGE_MARKER_RE.search(raw)
        if m:
            out.append((i, int(m.group(1))))
    return out


def page_for_line(line_no: int, page_anchors: list[tuple[int, int]]) -> int | None:
    """Find the page-marker page for the given line, by nearest-preceding match."""
    page = None
    for lno, pg in page_anchors:
        if lno <= line_no:
            page = pg
        else:
            break
    return page


def scan_section_content(
    lines: list[str],
    line_start: int,
    line_end: int,
    png_index: dict[str, dict],
    page_anchors: list[tuple[int, int]],
) -> dict:
    """Walk the section's lines once and collect refs, assets, and page range."""
    figure_refs: set[str] = set()
    table_refs: set[str] = set()
    equation_refs: set[str] = set()
    asset_ids: list[str] = []
    pages: set[int] = set()

    page_hint = page_for_line(line_start, page_anchors)
    if page_hint is not None:
        pages.add(page_hint)

    body_lines = lines[line_start - 1:line_end]
    for raw in body_lines:
        for ref in FIG_REF_RE.findall(raw):
            figure_refs.add(ref)
        for ref in TABLE_REF_RE.findall(raw):
            table_refs.add(ref)
        for ref in EQ_REF_RE.findall(raw):
            equation_refs.add(ref)

        for path in INLINE_IMAGE_RE.findall(raw):
            name = Path(path).name
            asset = png_index.get(name) or png_index.get(path)
            if asset and asset.get("asset_id") not in asset_ids:
                asset_ids.append(asset["asset_id"])
                pg = asset.get("page")
                if isinstance(pg, int):
                    pages.add(pg)
        for path in INLINE_LINK_PNG_RE.findall(raw):
            name = Path(path).name
            asset = png_index.get(name) or png_index.get(path)
            if asset and asset.get("asset_id") not in asset_ids:
                asset_ids.append(asset["asset_id"])
                pg = asset.get("page")
                if isinstance(pg, int):
                    pages.add(pg)
        for path in INLINE_LINK_CSV_RE.findall(raw):
            # Table assets are linked via CSV path; map back to the manifest
            # by replacing .csv → look up sibling .png if present.
            stem = Path(path).stem
            png_name = stem + ".png"
            asset = png_index.get(png_name)
            if asset and asset.get("asset_id") not in asset_ids:
                asset_ids.append(asset["asset_id"])
                pg = asset.get("page")
                if isinstance(pg, int):
                    pages.add(pg)
        for m in PAGE_MARKER_RE.finditer(raw):
            pages.add(int(m.group(1)))

    page_first = min(pages) if pages else None
    page_last = max(pages) if pages else None

    return {
        "figure_refs": sorted(figure_refs),
        "table_refs": sorted(table_refs),
        "equation_refs": sorted(equation_refs),
        "asset_ids": asset_ids,
        "page_first": page_first,
        "page_last": page_last,
    }


def build_sections(
    lines: list[str],
    headings: list[dict],
    prefix: str,
    png_index: dict[str, dict],
    page_anchors: list[tuple[int, int]],
) -> list[dict]:
    assign_parents(headings)
    total_lines = len(lines)
    sections: list[dict] = []
    parent_chapter_seen: list[bool] = []

    chapter_ancestry = [False] * len(headings)
    for idx, h in enumerate(headings):
        title = h["title"]
        is_chapter_marker = bool(CHAPTER_TITLE_RE.search(title))
        parent_idx = h["parent_index"]
        inherits_chapter = (
            chapter_ancestry[parent_idx]
            if parent_idx is not None
            else False
        )
        chapter_ancestry[idx] = bool(is_chapter_marker or inherits_chapter)

    for idx, h in enumerate(headings):
        line_start = h["line_no"]
        if idx + 1 < len(headings):
            line_end = headings[idx + 1]["line_no"] - 1
        else:
            line_end = total_lines

        sid = section_id(prefix, idx + 1)
        parent_idx = h["parent_index"]
        parent_id = section_id(prefix, parent_idx + 1) if parent_idx is not None else None

        body = scan_section_content(lines, line_start, line_end, png_index, page_anchors)
        tokens = estimate_tokens(lines, line_start, line_end)
        section_number = extract_section_number(h["title"])

        is_front = is_front_matter_heuristic(h["title"], line_start, total_lines) and not chapter_ancestry[idx]
        is_back = is_back_matter_heuristic(h["title"], line_end, total_lines) and not chapter_ancestry[idx]

        sections.append({
            "section_id": sid,
            "depth": h["depth"],
            "title": h["title"],
            "section_number": section_number,
            "parent_section_id": parent_id,
            "parent_chapter_idx": parent_idx,  # internal hint; pruned at write time
            "line_start": line_start,
            "line_end": line_end,
            "page_first": body["page_first"],
            "page_last": body["page_last"],
            "estimated_md_tokens": tokens,
            "is_front_matter": is_front,
            "is_back_matter": is_back,
            "in_scope_default": not (is_front or is_back),
            "figure_refs": body["figure_refs"],
            "table_refs": body["table_refs"],
            "equation_refs": body["equation_refs"],
            "asset_ids": body["asset_ids"],
        })
    return sections


def apply_overrides(
    sections: list[dict],
    front_overrides: list[str],
    back_overrides: list[str],
    in_scope_overrides: list[str],
) -> list[dict]:
    front_set = set(front_overrides)
    back_set = set(back_overrides)
    in_scope_set = set(in_scope_overrides)
    for s in sections:
        if s["section_id"] in front_set:
            s["is_front_matter"] = True
        if s["section_id"] in back_set:
            s["is_back_matter"] = True
        if s["section_id"] in in_scope_set:
            s["is_front_matter"] = False
            s["is_back_matter"] = False
        s["in_scope_default"] = not (s["is_front_matter"] or s["is_back_matter"])
    return sections


def direct_descendants(parent_idx: int, sections: list[dict]) -> list[int]:
    """Return indices of every section in the subtree rooted at parent_idx."""
    parent_depth = sections[parent_idx]["depth"]
    out: list[int] = []
    for j in range(parent_idx + 1, len(sections)):
        if sections[j]["depth"] <= parent_depth:
            break
        out.append(j)
    return out


def direct_children(parent_idx: int, sections: list[dict]) -> list[int]:
    """Return indices of direct (parent_index == parent_idx) children."""
    parent_id = sections[parent_idx]["section_id"]
    return [
        j for j in range(parent_idx + 1, len(sections))
        if sections[j]["parent_section_id"] == parent_id
    ]


def compute_preamble_tokens(
    section_idx: int,
    sections: list[dict],
    lines: list[str],
) -> tuple[int, int]:
    """Return (preamble_line_end, preamble_md_tokens) for a section that has
    in-scope children — the line range from the section heading to the line
    immediately before its first in-scope child's heading."""
    s = sections[section_idx]
    in_scope_kids = [
        j for j in direct_children(section_idx, sections)
        if sections[j]["in_scope_default"]
    ]
    if not in_scope_kids:
        return s["line_end"], s["estimated_md_tokens"]
    first_child = sections[in_scope_kids[0]]
    preamble_end = first_child["line_start"] - 1
    if preamble_end < s["line_start"]:
        return s["line_start"] - 1, 0
    tokens = estimate_tokens(lines, s["line_start"], preamble_end)
    return preamble_end, tokens


def build_atomic_candidates(
    sections: list[dict],
    lines: list[str],
) -> list[dict]:
    """Produce a non-overlapping ordered list of atomic dispatch candidates.

    A section with no in-scope children contributes one candidate covering its
    full line range. A section with in-scope children contributes a preamble
    candidate (covering the parent's own text before the first in-scope child)
    followed recursively by each in-scope child's atomic candidates.

    Out-of-scope sections (front/back matter) are skipped entirely.
    """
    candidates: list[dict] = []

    def walk(idx: int) -> None:
        s = sections[idx]
        if not s["in_scope_default"]:
            return
        in_scope_kids = [
            j for j in direct_children(idx, sections)
            if sections[j]["in_scope_default"]
        ]
        if not in_scope_kids:
            candidates.append({
                "primary_section_idx": idx,
                "target_section_ids": [s["section_id"]],
                "line_start": s["line_start"],
                "line_end": s["line_end"],
                "estimated_md_tokens": s["estimated_md_tokens"],
                "is_preamble": False,
            })
            return
        preamble_end, preamble_tokens = compute_preamble_tokens(idx, sections, lines)
        if preamble_end >= s["line_start"] and preamble_tokens > 0:
            candidates.append({
                "primary_section_idx": idx,
                "target_section_ids": [s["section_id"]],
                "line_start": s["line_start"],
                "line_end": preamble_end,
                "estimated_md_tokens": preamble_tokens,
                "is_preamble": True,
            })
        for j in in_scope_kids:
            walk(j)

    # Identify roots — sections whose parent is None or whose parent is out of
    # scope (children of skipped front/back matter still need to be walked).
    in_scope = {s["section_id"] for s in sections if s["in_scope_default"]}
    for i, s in enumerate(sections):
        if not s["in_scope_default"]:
            continue
        parent_id = s["parent_section_id"]
        if parent_id is None or parent_id not in in_scope:
            walk(i)
    return candidates


def build_dispatch_plan(
    sections: list[dict],
    lines: list[str],
    budget_tokens: int,
    split_threshold: int,
    prefix: str,
) -> list[dict]:
    """Cluster atomic candidates into dispatch units honoring the budget and
    split rules. Oversized candidates (>= split_threshold) become their own
    unit and are flagged contains_oversized_section=True; the section-split
    behavior happens implicitly via build_atomic_candidates, which decomposes
    parents with in-scope children into preamble + per-child candidates."""

    candidates = build_atomic_candidates(sections, lines)

    units: list[dict] = []
    unit_counter = 0
    pending: list[dict] = []
    pending_tokens = 0

    def emit(items: list[dict], oversized: bool) -> None:
        nonlocal unit_counter
        if not items:
            return
        unit_counter += 1
        uid = f"UNIT-{prefix}-{unit_counter:04d}"
        line_start = min(c["line_start"] for c in items)
        line_end = max(c["line_end"] for c in items)
        target_ids: list[str] = []
        for c in items:
            for sid in c["target_section_ids"]:
                if sid not in target_ids:
                    target_ids.append(sid)
        est = sum(c["estimated_md_tokens"] for c in items)
        units.append({
            "unit_id": uid,
            "line_start": line_start,
            "line_end": line_end,
            "target_section_ids": target_ids,
            "estimated_md_tokens": est,
            "contains_oversized_section": oversized,
        })

    def flush() -> None:
        nonlocal pending, pending_tokens
        emit(pending, oversized=False)
        pending = []
        pending_tokens = 0

    for c in candidates:
        if c["estimated_md_tokens"] >= split_threshold:
            flush()
            emit([c], oversized=True)
            continue
        if pending and pending_tokens + c["estimated_md_tokens"] > budget_tokens:
            flush()
        pending.append(c)
        pending_tokens += c["estimated_md_tokens"]

    flush()
    return units


def fail(msg: str, code: int = 2) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return code


def main() -> int:
    args = parse_args()

    if not args.md.exists():
        return fail(f"--md not found: {args.md}")
    if not args.asset_manifest.exists():
        return fail(f"--asset-manifest not found: {args.asset_manifest}")
    if args.budget_tokens <= 0:
        return fail("--budget-tokens must be positive")
    if args.section_split_threshold <= args.budget_tokens:
        return fail("--section-split-threshold must exceed --budget-tokens")

    front_overrides = json.loads(args.front_matter_overrides) if args.front_matter_overrides else []
    back_overrides = json.loads(args.back_matter_overrides) if args.back_matter_overrides else []
    in_scope_overrides = json.loads(args.in_scope_overrides) if args.in_scope_overrides else []
    if (
        not isinstance(front_overrides, list)
        or not isinstance(back_overrides, list)
        or not isinstance(in_scope_overrides, list)
    ):
        return fail(
            "--front-matter-overrides, --back-matter-overrides, "
            "and --in-scope-overrides must be JSON arrays"
        )

    manifest = load_manifest(args.asset_manifest)
    doc_stem = manifest.get("doc_stem") or args.md.stem
    prefix = args.source_prefix or derive_prefix(doc_stem)

    lines = load_md(args.md)
    headings = parse_headings(lines)
    if not headings:
        return fail("no Markdown headings found")

    png_index = build_png_to_asset(manifest)
    page_anchors = collect_page_line_index(lines)
    sections = build_sections(lines, headings, prefix, png_index, page_anchors)
    sections = apply_overrides(sections, front_overrides, back_overrides, in_scope_overrides)

    # Strip internal-only fields before writing
    for s in sections:
        s.pop("parent_chapter_idx", None)

    dispatch_units = build_dispatch_plan(
        sections,
        lines,
        budget_tokens=args.budget_tokens,
        split_threshold=args.section_split_threshold,
        prefix=prefix,
    )

    skeleton = {
        "schema_version": 1,
        "source": doc_stem,
        "source_prefix": prefix,
        "md_path": str(args.md),
        "asset_manifest_path": str(args.asset_manifest),
        "total_md_lines": len(lines),
        "section_count": len(sections),
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sections": sections,
    }

    dispatch_plan = {
        "schema_version": 1,
        "source": doc_stem,
        "source_prefix": prefix,
        "skeleton_path": str(args.output_skeleton),
        "md_path": str(args.md),
        "budget_tokens": args.budget_tokens,
        "section_split_threshold": args.section_split_threshold,
        "unit_count": len(dispatch_units),
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "units": dispatch_units,
    }

    args.output_skeleton.parent.mkdir(parents=True, exist_ok=True)
    args.output_dispatch_plan.parent.mkdir(parents=True, exist_ok=True)
    args.output_skeleton.write_text(json.dumps(skeleton, indent=2) + "\n", encoding="utf-8")
    args.output_dispatch_plan.write_text(json.dumps(dispatch_plan, indent=2) + "\n", encoding="utf-8")

    in_scope = sum(1 for s in sections if s["in_scope_default"])
    print(
        f"source={doc_stem} prefix={prefix} sections={len(sections)} "
        f"in_scope={in_scope} units={len(dispatch_units)} "
        f"skeleton={args.output_skeleton.name} dispatch={args.output_dispatch_plan.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
