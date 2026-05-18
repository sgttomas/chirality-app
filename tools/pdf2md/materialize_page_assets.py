#!/usr/bin/env python3
"""
materialize_page_assets.py
Crop page-level prose-document assets and write anchored Markdown.

Usage:
    python3 materialize_page_assets.py --page-image page_0003.png --page-md page_0003.md \
      --asset-json page_0003_assets.json --assets-root _Sources --doc-stem MWK_1956 \
      --page 3 --output-md page_0003.anchored.md --manifest-output page_0003_assets_materialized.json

Inputs:
    --page-image       Rasterized page PNG
    --page-md          Clean per-page Markdown
    --asset-json       VLM-emitted page asset JSON from pdf2md-page-assets
    --assets-root      Public folder that will contain figures/, tables/, images/
    --doc-stem         Document stem used in stable asset IDs
    --page             1-indexed page number
    --output-md        Anchored per-page Markdown output
    --manifest-output  Per-page materialization manifest JSON
    --padding-ratio    Optional crop padding around bbox_norm (default: 0.05)

Outputs:
    Asset crops in assets-root/figures, assets-root/tables, assets-root/images;
    table CSVs under assets-root/tables; anchored per-page Markdown; and a
    per-page materialization manifest.

Example:
    python3 tools/pdf2md/materialize_page_assets.py \
      --page-image work/page_0003.png --page-md work/page_0003.md \
      --asset-json work/page_0003_assets.json --assets-root domain/_Sources \
      --doc-stem MWK_1956 --page 3 --output-md work/page_0003.anchored.md \
      --manifest-output work/page_0003_assets_materialized.json
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("ERROR: Pillow is required for asset cropping") from exc


# render_table_xlsx lives alongside this tool. Load it dynamically so this
# module can be imported via importlib.util in tests without polluting
# sys.modules with a package-qualified name.
def _load_render_table_xlsx():
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location(
        "render_table_xlsx", here / "render_table_xlsx.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("render_table_xlsx", module)
    spec.loader.exec_module(module)
    return module


_RENDER_TABLE_XLSX = _load_render_table_xlsx()


KIND_DIR = {
    "fig": "figures",
    "tbl": "tables",
    "img": "images",
}

# Canonical kind literals — must match skills/pdf2md-page-assets/SKILL.md exactly.
# `fig` / `tbl` / `img` are the only accepted values; the brief-builder
# (tools/pdf2md/build_page_assets_brief.py) repeats this constraint in
# CustomInstructions so the skill knows the contract before emitting.
CANONICAL_KINDS = frozenset({"fig", "tbl", "img"})

ASSET_BLOCK_RE = re.compile(
    r"\n*<!-- PDF2MD-ASSETS:BEGIN page=\d+ -->.*?<!-- PDF2MD-ASSETS:END page=\d+ -->\n*",
    re.DOTALL,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize PDF2MD page assets and anchored Markdown.")
    parser.add_argument("--page-image", required=True)
    parser.add_argument("--page-md", required=True)
    parser.add_argument("--asset-json", required=True)
    parser.add_argument("--assets-root", required=True)
    parser.add_argument("--doc-stem", required=True)
    parser.add_argument("--page", required=True, type=int)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--manifest-output", required=True)
    parser.add_argument("--padding-ratio", type=float, default=0.05)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slugify(value: str, default: str = "untitled", max_len: int = 40) -> str:
    normalized = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        slug = default
    return slug[:max_len].strip("-") or default


def bbox_from_asset(asset: dict) -> list[float] | None:
    """Extract bbox_norm as a 4-element list of floats.

    STRICT: only accepts the contracted shape `[x0, y0, x1, y1]` (per
    skills/pdf2md-page-assets/SKILL.md). Returns None on any deviation
    (missing, wrong length, dict shape, non-numeric entries) — caller
    appends an `invalid_bbox_norm` issue to the asset record."""
    raw = asset.get("bbox_norm")
    if not isinstance(raw, list) or len(raw) != 4:
        return None
    try:
        bbox = [float(item) for item in raw]
    except (TypeError, ValueError):
        return None
    return bbox


def padded_bbox_px(bbox_norm: list[float], width: int, height: int, padding_ratio: float) -> tuple[int, int, int, int] | None:
    x0, y0, x1, y1 = bbox_norm
    pad = max(0.0, padding_ratio)
    x0 = max(0.0, min(1.0, x0 - pad))
    y0 = max(0.0, min(1.0, y0 - pad))
    x1 = max(0.0, min(1.0, x1 + pad))
    y1 = max(0.0, min(1.0, y1 + pad))
    left = round(x0 * width)
    top = round(y0 * height)
    right = round(x1 * width)
    bottom = round(y1 * height)
    if left >= right or top >= bottom:
        return None
    return (left, top, right, bottom)


def canonical_table_data_json(table_data: dict) -> str:
    """Canonical text form of a table_data block (for hashing).

    Sorted keys, no extraneous whitespace, LF-terminated — deterministic
    across runs and platforms so `table_data_sha256` is reproducible.
    """
    return json.dumps(table_data, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"


def table_data_sha256(table_data: dict) -> str:
    return hashlib.sha256(canonical_table_data_json(table_data).encode("utf-8")).hexdigest()


def validate_table_data(table_data: dict) -> list[str]:
    """Validate a table_data block per pdf2md-table/v1.

    Returns a list of issue strings (empty when valid). Wraps the renderer's
    structural validator (which raises SystemExit) so the materializer can
    record the failure on the asset record and continue with the rest of
    the page rather than aborting the whole run.
    """
    try:
        _RENDER_TABLE_XLSX.validate_table_data(table_data)
    except SystemExit as exc:
        return [f"invalid_table_data:{exc}"]
    return []


def load_assets(path: Path) -> list[dict]:
    """Load and validate page asset JSON per the strict contract.

    Required shape (per skills/pdf2md-page-assets/SKILL.md):
        {
          "schema_version": "pdf2md-page-assets/v1",
          "run_status": "SUCCESS" | "NO_ASSETS" | "FAILED" | "FAILED_INPUTS",
          "doc_stem": "...",
          "page": <int>,
          "total_pages": <int>,
          "asset_policy": "...",
          "assets": [...],
          "issues": [...]
        }

    STRICT: rejects sibling-keys legacy (`tables`/`figures`/`images`),
    bare-list legacy, and any shape other than the contracted dict-with-
    `assets` form. A failed load aborts the run rather than silently
    materializing a malformed input. To migrate older artifacts to the
    contracted shape, regenerate them via the pdf2md-page-assets skill.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(
            f"ERROR: {path} top-level must be a JSON object per "
            f"skills/pdf2md-page-assets/SKILL.md; got {type(data).__name__}"
        )
    if "assets" not in data:
        raise SystemExit(
            f"ERROR: {path} missing required `assets` field. The page-assets "
            f"contract uses a flat `assets: [...]` array — no sibling "
            f"`tables`/`figures`/`images` keys. Regenerate via the skill."
        )
    assets = data["assets"]
    if not isinstance(assets, list):
        raise SystemExit(f"ERROR: {path}: `assets` must be a JSON array, got {type(assets).__name__}")
    # Reject any sibling-keys legacy explicitly to surface drift loudly.
    forbidden_siblings = [k for k in ("tables", "figures", "images") if k in data]
    if forbidden_siblings:
        raise SystemExit(
            f"ERROR: {path}: forbidden sibling-keys {forbidden_siblings} alongside "
            f"`assets`. The contract is a flat `assets` array; tables / figures / "
            f"images are entries inside `assets` with kind 'tbl'/'fig'/'img'."
        )
    return [asset for asset in assets if isinstance(asset, dict)]


def caption_from_asset(asset: dict) -> str:
    """Extract caption per the strict contract: only the `caption` field.

    STRICT: per skills/pdf2md-page-assets/SKILL.md, captions go in the
    `caption` field. The previous fallback chain to `title`/`label`/`name`
    is removed — those alternates masked skill contract drift."""
    value = asset.get("caption")
    if value:
        return str(value).strip()
    return ""


def normalize_kind(asset: dict) -> str:
    """Return the asset's kind iff it is one of the three canonical literals.

    STRICT: only `asset["kind"]` is consulted; only `fig`/`tbl`/`img` are
    accepted. Aliases (`figure`, `image`, `table`, `diagram`, `plot`,
    `chart`, `logo`, etc.) and alternate keys (`type`, `subtype`) are
    rejected (return ""). The caller treats "" as `unknown_kind` and skips
    the asset with an explicit issue."""
    raw = asset.get("kind")
    if isinstance(raw, str) and raw in CANONICAL_KINDS:
        return raw
    return ""


def strip_existing_asset_block(text: str) -> str:
    return ASSET_BLOCK_RE.sub("\n\n", text).rstrip()


def collapse_label_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def escape_markdown_label(value: str) -> str:
    """Escape Markdown label delimiters while preserving readable caption text."""
    text = collapse_label_text(value)
    return (
        text.replace("\\", "\\\\")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


def escape_bold_text(value: str) -> str:
    """Escape caption text used inside bold spans in generated asset blocks."""
    text = escape_markdown_label(value)
    return text.replace("*", "\\*").replace("_", "\\_")


def build_reference(asset: dict) -> str:
    caption = collapse_label_text(asset.get("caption") or asset.get("title") or asset["asset_id"])
    label = escape_markdown_label(caption)
    bold_caption = escape_bold_text(caption)
    if asset["kind"] in {"fig", "img"}:
        if asset.get("png_path"):
            return f"![{label}]({asset['png_path']})"
        issues = ", ".join(asset.get("issues", [])) or "asset pending"
        return f"> **{asset['kind'].upper()} - {bold_caption}** - {issues}"

    links = []
    if asset.get("xlsx_path"):
        links.append(f"[XLSX]({asset['xlsx_path']})")
    if asset.get("png_path"):
        links.append(f"[source crop]({asset['png_path']})")
    if asset.get("needs_extraction"):
        links.append("needs_extraction")
    suffix = " and ".join(links) if links else "asset pending"
    return f"> **Table - {bold_caption}** - see {suffix}"


def main() -> int:
    args = parse_args()
    if args.page < 1:
        raise SystemExit("ERROR: --page must be >= 1")

    page_image = Path(args.page_image).resolve()
    page_md = Path(args.page_md).resolve()
    asset_json = Path(args.asset_json).resolve()
    assets_root = Path(args.assets_root).resolve()
    output_md = Path(args.output_md).resolve()
    manifest_output = Path(args.manifest_output).resolve()

    for path in (page_image, page_md, asset_json):
        if not path.is_file():
            raise SystemExit(f"ERROR: required input is missing: {path}")

    assets_root.mkdir(parents=True, exist_ok=True)
    for dirname in KIND_DIR.values():
        (assets_root / dirname).mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    manifest_output.parent.mkdir(parents=True, exist_ok=True)

    assets = load_assets(asset_json)
    counters = {kind: 0 for kind in KIND_DIR}
    materialized: list[dict] = []

    with Image.open(page_image) as image:
        width, height = image.size
        for index, asset in enumerate(assets, start=1):
            kind = normalize_kind(asset)
            if not kind:
                raw_kind = asset.get("kind")
                materialized.append({
                    "source_index": index,
                    "status": "skipped",
                    "issues": [
                        f"non_canonical_kind:{raw_kind!r}; "
                        f"expected one of fig/tbl/img per skills/pdf2md-page-assets/SKILL.md"
                    ],
                })
                continue

            counters[kind] += 1
            ordinal = asset.get("ordinal")
            try:
                ordinal_int = int(ordinal)
            except (TypeError, ValueError):
                ordinal_int = counters[kind]
            if ordinal_int < 1:
                ordinal_int = counters[kind]

            caption = caption_from_asset(asset)
            # `slug` is an advisory field per skills/pdf2md-page-assets/SKILL.md
            # (line 150: "Downstream tools normalize it and append it to a stable
            # ID"). Prefer the skill-emitted slug when present; fall back to a
            # caption-derived slug. slugify() normalizes either way.
            slug = slugify(str(asset.get("slug") or caption or "untitled"))
            asset_id = f"{args.doc_stem}_p{args.page:04d}_{kind}{ordinal_int:02d}"
            basename = f"{asset_id}_{slug}"
            target_dir = assets_root / KIND_DIR[kind]
            png_path = target_dir / f"{basename}.png"
            xlsx_path = target_dir / f"{basename}.xlsx" if kind == "tbl" else None
            json_path = target_dir / f"{basename}.json" if kind == "tbl" else None

            issues: list[str] = []
            bbox_norm = bbox_from_asset(asset)
            bbox_px = None
            if bbox_norm is None:
                issues.append("missing_or_invalid_bbox_norm")
            else:
                bbox_px = padded_bbox_px(bbox_norm, width, height, args.padding_ratio)
                if bbox_px is None:
                    issues.append("invalid_bbox_geometry")
                else:
                    image.crop(bbox_px).save(png_path)

            needs_extraction = False
            table_data_hash = ""
            if kind == "tbl":
                # STRICT: the legacy `csv_text` field is rejected. The canonical
                # table representation is the structured `table_data` block per
                # skills/pdf2md-page-assets/SKILL.md (pdf2md-table/v1).
                if "csv_text" in asset:
                    raise SystemExit(
                        f"ERROR: asset {asset_id} carries legacy `csv_text` field. "
                        f"The canonical contract is the structured `table_data` block "
                        f"(pdf2md-table/v1) per skills/pdf2md-page-assets/SKILL.md. "
                        f"Regenerate via the pdf2md-page-assets skill."
                    )

                needs_extraction = bool(asset.get("needs_extraction"))
                table_data = asset.get("table_data")
                if needs_extraction:
                    if table_data is not None:
                        issues.append("needs_extraction_with_table_data:contract_violation")
                elif table_data is None:
                    issues.append("missing_table_data")
                else:
                    td_issues = validate_table_data(table_data)
                    if td_issues:
                        issues.extend(td_issues)
                    else:
                        table_data_hash = table_data_sha256(table_data)
                        if json_path is not None:
                            json_path.write_text(
                                canonical_table_data_json(table_data),
                                encoding="utf-8",
                            )
                        if xlsx_path is not None:
                            try:
                                _RENDER_TABLE_XLSX.render(
                                    table_data,
                                    xlsx_path,
                                    caption=caption,
                                    doc_stem=args.doc_stem,
                                    page=args.page,
                                    ordinal=ordinal_int,
                                    slug=slug,
                                )
                            except SystemExit as exc:
                                issues.append(f"render_xlsx_failed:{exc}")

            record = {
                "asset_id": asset_id,
                "kind": kind,
                "ordinal": ordinal_int,
                "caption": caption,
                "slug": slug,
                "bbox_norm": bbox_norm,
                "bbox_px": list(bbox_px) if bbox_px else None,
                "png_path": f"{KIND_DIR[kind]}/{png_path.name}" if png_path.exists() else "",
                "xlsx_path": (
                    f"{KIND_DIR[kind]}/{xlsx_path.name}" if xlsx_path and xlsx_path.exists() else ""
                ),
                "table_data_json_path": (
                    f"{KIND_DIR[kind]}/{json_path.name}" if json_path and json_path.exists() else ""
                ),
                "status": "materialized" if not issues else "degraded",
                "issues": issues,
            }
            if kind == "tbl":
                record["needs_extraction"] = needs_extraction
                if table_data_hash:
                    record["table_data_sha256"] = table_data_hash
            if png_path.exists():
                record["png_sha256"] = sha256(png_path)
            if xlsx_path and xlsx_path.exists():
                record["xlsx_sha256"] = sha256(xlsx_path)
            if json_path and json_path.exists():
                record["table_data_json_sha256"] = sha256(json_path)
            materialized.append(record)

    markdown = strip_existing_asset_block(page_md.read_text(encoding="utf-8"))
    references = [build_reference(asset) for asset in materialized if asset.get("status") in {"materialized", "degraded"}]
    if references:
        block = [
            f"<!-- PDF2MD-ASSETS:BEGIN page={args.page} -->",
            "",
            "#### Extracted Page Assets",
            "",
            *references,
            "",
            f"<!-- PDF2MD-ASSETS:END page={args.page} -->",
        ]
        markdown = markdown.rstrip() + "\n\n" + "\n\n".join(block) + "\n"
    else:
        markdown = markdown.rstrip() + "\n"
    output_md.write_text(markdown, encoding="utf-8")

    manifest = {
        "schema_version": "pdf2md-assets-materialized/v2",
        "doc_stem": args.doc_stem,
        "page": args.page,
        "page_image": str(page_image),
        "page_image_sha256": sha256(page_image),
        "source_asset_json": str(asset_json),
        "assets_root": str(assets_root),
        "anchored_markdown": str(output_md),
        "assets": materialized,
    }
    manifest_output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"assets={len(materialized)} materialized_manifest={manifest_output}")
    print(f"anchored_markdown={output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
