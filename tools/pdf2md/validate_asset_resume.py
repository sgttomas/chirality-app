#!/usr/bin/env python3
"""
validate_asset_resume.py
Validate reusable PDF2MD asset materialization manifests against current page rasters.

Usage:
    python3 validate_asset_resume.py WORK_DIR [--pages 1-10,12]

Inputs:
    WORK_DIR   PDF2MD work directory containing manifest.json, page_NNNN.png,
               and optional page_NNNN_assets_materialized.json files
    --pages    optional page selection. Defaults to pages_rendered from manifest.json.

Outputs:
    resume_safety=OK when all existing materialization manifests match current
    page rasters and referenced anchored Markdown / asset files exist.
    Exit 0 = reusable manifests are safe; missing manifests are skipped.
    Exit 1 = one or more existing manifests are stale or incomplete.
    Exit 2 = setup/input error.

Example:
    python3 tools/pdf2md/validate_asset_resume.py ./MWK_1956_pdf2md_work --pages 1-10
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate PDF2MD asset materialization resume safety.")
    parser.add_argument("work_dir")
    parser.add_argument("--pages", help="Page selection like 1,3,5-10. Default: manifest pages_rendered.")
    return parser.parse_args()


def parse_pages(value: str) -> list[int]:
    pages: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start > end:
                raise ValueError(f"invalid page range: {part}")
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    if any(page < 1 for page in pages):
        raise ValueError("pages must be positive integers")
    return sorted(pages)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest_pages(work_dir: Path) -> list[int]:
    manifest_path = work_dir / "manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"ERROR: manifest.json not found in {work_dir}")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    pages = data.get("pages_rendered", [])
    if not isinstance(pages, list) or not pages:
        raise SystemExit("ERROR: manifest.json has no pages_rendered list")
    try:
        return sorted(int(page) for page in pages)
    except (TypeError, ValueError) as exc:
        raise SystemExit("ERROR: manifest pages_rendered contains non-integer values") from exc


def relative_asset_exists(assets_root: Path, value: str) -> bool:
    if not value:
        return True
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return False
    return (assets_root / path).is_file()


def main() -> int:
    args = parse_args()
    work_dir = Path(args.work_dir).resolve()
    if not work_dir.is_dir():
        print(f"ERROR: work_dir is not a directory: {work_dir}", file=sys.stderr)
        return 2

    try:
        pages = parse_pages(args.pages) if args.pages else load_manifest_pages(work_dir)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    checked = 0
    skipped_missing = 0
    issues: list[str] = []

    for page in pages:
        page_image = work_dir / f"page_{page:04d}.png"
        materialized = work_dir / f"page_{page:04d}_assets_materialized.json"
        if not materialized.exists():
            skipped_missing += 1
            continue
        checked += 1
        if not page_image.is_file():
            issues.append(f"page {page}: page image missing: {page_image}")
            continue
        try:
            data = json.loads(materialized.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(f"page {page}: materialization manifest is invalid JSON: {exc}")
            continue

        if int(data.get("page", -1)) != page:
            issues.append(f"page {page}: manifest page field is {data.get('page')!r}")
        expected_hash = str(data.get("page_image_sha256", ""))
        actual_hash = sha256(page_image)
        if expected_hash != actual_hash:
            issues.append(f"page {page}: page_image_sha256 mismatch")

        anchored = Path(str(data.get("anchored_markdown", "")))
        if not anchored.is_absolute():
            anchored = (work_dir / anchored).resolve()
        if not anchored.is_file():
            issues.append(f"page {page}: anchored Markdown missing: {anchored}")

        assets_root_raw = str(data.get("assets_root", ""))
        assets_root = Path(assets_root_raw).resolve() if assets_root_raw else None
        if assets_root is None or not assets_root.is_dir():
            issues.append(f"page {page}: assets_root missing or not a directory: {assets_root_raw}")
            continue
        for asset in data.get("assets", []):
            if not isinstance(asset, dict):
                issues.append(f"page {page}: asset entry is not an object")
                continue
            for key in ("png_path", "xlsx_path"):
                value = str(asset.get(key) or "").strip()
                if value and not relative_asset_exists(assets_root, value):
                    issues.append(f"page {page}: {key} does not resolve under assets_root: {value}")

    print(f"checked={checked}")
    print(f"skipped_missing={skipped_missing}")
    if issues:
        print("resume_safety=FAIL")
        for issue in issues[:100]:
            print(f"  - {issue}")
        if len(issues) > 100:
            print(f"  ... {len(issues) - 100} more")
        return 1
    print("resume_safety=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
