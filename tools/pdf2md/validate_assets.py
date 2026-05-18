#!/usr/bin/env python3
"""
validate_assets.py
Validate PDF2MD asset references against the document asset manifest and disk.

Usage:
    python3 validate_assets.py --markdown MWK_1956.md --manifest MWK_1956_assets_manifest.json --assets-root _Sources

Inputs:
    --markdown     assembled Markdown file
    --manifest     document-level asset manifest from aggregate_asset_manifest.py
    --assets-root  folder containing figures/, tables/, and images/

Outputs:
    PASS/FAIL summary on stdout. Exit 0 when all referenced and manifest-declared
    assets resolve; exit 1 for orphan/widow/missing asset findings; exit 2 for
    input/setup errors.
    Recognizes inline Markdown links/images, reference-style link definitions,
    and HTML <img src="..."> references.

Example:
    python3 tools/pdf2md/validate_assets.py \
      --markdown domain/_Sources/MWK_1956.md \
      --manifest domain/_Sources/MWK_1956_assets_manifest.json \
      --assets-root domain/_Sources
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


INLINE_DEST_RE = re.compile(r"(?<!\\)\]\(([^)]+)\)")
REFERENCE_DEF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
HTML_IMG_SRC_RE = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
ASSET_PREFIXES = ("figures/", "tables/", "images/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate PDF2MD asset references.")
    parser.add_argument("--markdown", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--assets-root", required=True)
    return parser.parse_args()


def extract_asset_links(markdown: str) -> set[str]:
    links = set()
    for pattern in (INLINE_DEST_RE, REFERENCE_DEF_RE, HTML_IMG_SRC_RE):
        for match in pattern.finditer(markdown):
            target = match.group(1).strip()
            target = target.strip("<>")
            target = target.split("#", 1)[0].split("?", 1)[0]
            if target.startswith("./"):
                target = target[2:]
            if target.startswith(ASSET_PREFIXES):
                links.add(target)
    return links


def manifest_paths(manifest: dict) -> tuple[set[str], set[str]]:
    """Collect asset paths declared by the materialized manifest.

    Returns (linked_paths, supporting_paths):
      - linked_paths     — must be referenced from the assembled Markdown
      - supporting_paths — must be on disk but are not Markdown-linked
                           (e.g. the canonical `table_data` JSON sidecar)

    For `tbl` entries flagged `needs_extraction: true`, the manifest does
    NOT promise a rendered XLSX — those entries declare only their PNG crop
    (when present). Validators must respect this gap so the corpus can
    legitimately carry "table visible but not yet structurally extracted"
    records without failing the asset-resolution check.
    """
    linked: set[str] = set()
    supporting: set[str] = set()
    for asset in manifest.get("assets", []):
        if not isinstance(asset, dict):
            continue
        png = str(asset.get("png_path") or "").strip()
        if png:
            linked.add(png)
        if asset.get("kind") == "tbl" and asset.get("needs_extraction"):
            continue
        xlsx = str(asset.get("xlsx_path") or "").strip()
        if xlsx:
            linked.add(xlsx)
        td_json = str(asset.get("table_data_json_path") or "").strip()
        if td_json:
            supporting.add(td_json)
    return linked, supporting


def collect_folio_warnings(manifest: dict, manifest_path: Path) -> list[str]:
    """Surface page-label warnings without failing validation.

    Two classes of warning:
      1. Schema-version drift: if the manifest is v2 (pre-folio) but a
         `page_folios.json` exists alongside the per-page materialized
         manifests in the same work_dir, the aggregator likely wasn't
         re-run after folio extraction.
      2. Low-confidence VLM folios: when a page record advertises
         `page_label_source == "vlm"`, look up the page in the work_dir's
         `page_folios.json` and warn if the skill reported
         `confidence == "low"`.
    The manifest itself doesn't carry confidence — the validator opens
    `page_folios.json` from the recorded `work_dir` (if reachable) to get it.
    Both warning classes are advisory; the validator never fails on them.
    """
    warnings: list[str] = []

    work_dir_str = str(manifest.get("work_dir") or "").strip()
    page_folios_path: Path | None = None
    if work_dir_str:
        candidate = Path(work_dir_str) / "page_folios.json"
        if candidate.is_file():
            page_folios_path = candidate

    schema_version = str(manifest.get("schema_version") or "")
    if schema_version == "pdf2md-assets-document/v2" and page_folios_path is not None:
        warnings.append(
            f"manifest schema_version is v2 but {page_folios_path} exists — "
            f"re-run aggregate_asset_manifest.py to produce v3 with page_label fields"
        )

    page_folios: dict[str, dict] = {}
    if page_folios_path is not None:
        try:
            raw = json.loads(page_folios_path.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                page_folios = {str(k): v for k, v in raw.items() if isinstance(v, dict)}
        except (OSError, json.JSONDecodeError):
            page_folios = {}

    for page in manifest.get("pages", []) or []:
        if not isinstance(page, dict):
            continue
        if page.get("page_label_source") != "vlm":
            continue
        page_num = page.get("page")
        if page_num is None:
            continue
        folio = page_folios.get(str(page_num))
        if not isinstance(folio, dict):
            continue
        if folio.get("confidence") == "low":
            label = page.get("page_label")
            warnings.append(
                f"page {page_num}: low-confidence VLM folio page_label={label!r}"
            )
    return warnings


def disk_asset_paths(root: Path) -> set[str]:
    paths = set()
    for dirname in ASSET_PREFIXES:
        directory = root / dirname.rstrip("/")
        if not directory.is_dir():
            continue
        for path in directory.iterdir():
            if path.is_file():
                paths.add(f"{dirname}{path.name}")
    return paths


def main() -> int:
    args = parse_args()
    markdown_path = Path(args.markdown).resolve()
    manifest_path = Path(args.manifest).resolve()
    assets_root = Path(args.assets_root).resolve()

    for path in (markdown_path, manifest_path):
        if not path.is_file():
            print(f"ERROR: missing input file: {path}", file=sys.stderr)
            return 2
    if not assets_root.is_dir():
        print(f"ERROR: assets root is not a directory: {assets_root}", file=sys.stderr)
        return 2

    markdown_links = extract_asset_links(markdown_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    warnings = collect_folio_warnings(manifest, manifest_path)
    for warning in warnings:
        print(f"WARNING: {warning}")
    linked_paths, supporting_paths = manifest_paths(manifest)
    declared_paths = linked_paths | supporting_paths
    disk_paths = disk_asset_paths(assets_root)

    missing_on_disk = sorted(path for path in markdown_links | declared_paths if path not in disk_paths)
    orphan_links = sorted(path for path in markdown_links if path not in declared_paths)
    widow_manifest_paths = sorted(path for path in linked_paths if path not in markdown_links)
    unmanifested_disk_paths = sorted(path for path in disk_paths if path not in declared_paths)

    print(f"markdown_links={len(markdown_links)}")
    print(f"manifest_paths={len(declared_paths)}")
    print(f"disk_paths={len(disk_paths)}")

    findings = {
        "missing_on_disk": missing_on_disk,
        "orphan_links": orphan_links,
        "widow_manifest_paths": widow_manifest_paths,
        "unmanifested_disk_paths": unmanifested_disk_paths,
    }
    for name, values in findings.items():
        if values:
            print(f"{name}={len(values)}")
            for value in values[:50]:
                print(f"  - {value}")
            if len(values) > 50:
                print(f"  ... {len(values) - 50} more")

    if any(findings.values()):
        print("asset_validation=FAIL")
        return 1
    print("asset_validation=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
