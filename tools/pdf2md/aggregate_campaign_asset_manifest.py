#!/usr/bin/env python3
"""
Aggregate industry-practices per-PDF asset manifests into one campaign manifest.

Supports both manifest locations used during the campaign:
  1. <chapter>/_assets/<stem>/<stem>_assets_manifest.json
  2. <chapter>/<stem>_pdf2md_work/asset_manifest.json

When neither exists, the per-PDF manifest is regenerated from
page_NNNN_assets_materialized.json files in the work directory.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


PAGE_MANIFEST_RE = re.compile(r"^page_(\d{4})_assets_materialized\.json$")
ASSET_PATH_FIELDS = ("png_path", "xlsx_path", "table_data_json_path")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate industry-practices campaign asset manifests.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--doc-stem", default="industry-practices")
    return parser.parse_args()


def page_manifest_paths(work_dir: Path) -> list[tuple[int, Path]]:
    paths: list[tuple[int, Path]] = []
    for path in work_dir.glob("page_*_assets_materialized.json"):
        match = PAGE_MANIFEST_RE.match(path.name)
        if match:
            paths.append((int(match.group(1)), path))
    paths.sort()
    return paths


def regenerate_document_manifest(work_dir: Path, output_json: Path, doc_stem: str) -> dict:
    pages = []
    assets = []
    issues = []
    for page_num, path in page_manifest_paths(work_dir):
        data = json.loads(path.read_text(encoding="utf-8"))
        page_assets = data.get("assets", [])
        if not isinstance(page_assets, list):
            issues.append(f"{path.name}: assets is not a list")
            page_assets = []
        pages.append(
            {
                "page": page_num,
                "manifest_path": str(path),
                "asset_count": len(page_assets),
                "anchored_markdown": data.get("anchored_markdown", ""),
                "page_label": None,
                "page_label_source": "unreviewed",
            }
        )
        for asset in page_assets:
            if isinstance(asset, dict):
                record = dict(asset)
                record["page"] = page_num
                assets.append(record)

    output = {
        "schema_version": "pdf2md-assets-document/v3",
        "doc_stem": doc_stem,
        "work_dir": str(work_dir),
        "page_manifest_count": len(pages),
        "asset_count": len(assets),
        "pages": pages,
        "assets": assets,
        "issues": issues,
    }
    output_json.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def resolve_manifest(root: Path, pdf_path: Path) -> tuple[Path, dict, bool]:
    stem = pdf_path.stem
    chapter = pdf_path.parent
    new_manifest = chapter / "_assets" / stem / f"{stem}_assets_manifest.json"
    if new_manifest.is_file():
        return new_manifest, json.loads(new_manifest.read_text(encoding="utf-8")), False

    work_dir = chapter / f"{stem}_pdf2md_work"
    legacy_manifest = work_dir / "asset_manifest.json"
    if legacy_manifest.is_file():
        return legacy_manifest, json.loads(legacy_manifest.read_text(encoding="utf-8")), False

    page_manifests = page_manifest_paths(work_dir)
    if not page_manifests:
        raise SystemExit(f"ERROR: no per-page materialized manifests for {pdf_path.relative_to(root)}")
    data = regenerate_document_manifest(work_dir, legacy_manifest, stem)
    return legacy_manifest, data, True


def infer_asset_root(root: Path, pdf_path: Path, manifest_path: Path, manifest: dict) -> Path:
    stem = pdf_path.stem
    chapter = pdf_path.parent
    if manifest_path.parent.name == stem and manifest_path.parent.parent.name == "_assets":
        return manifest_path.parent

    for page in manifest.get("pages", []):
        if not isinstance(page, dict):
            continue
        page_manifest = Path(str(page.get("manifest_path") or ""))
        if page_manifest.is_file():
            data = json.loads(page_manifest.read_text(encoding="utf-8"))
            assets_root = data.get("assets_root")
            if assets_root:
                return Path(str(assets_root)).resolve()

    new_root = chapter / "_assets" / stem
    if new_root.exists():
        return new_root
    legacy_root = chapter / f"{stem}_assets"
    if legacy_root.exists():
        return legacy_root
    return new_root


def rewrite_path(root: Path, asset_root: Path, value: str) -> str:
    if not value:
        return ""
    path = Path(value)
    if path.is_absolute():
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            return value
    return (asset_root / value).resolve().relative_to(root).as_posix()


def build_campaign_manifest(root: Path, output: Path, doc_stem: str) -> tuple[dict, int, Counter]:
    root = root.resolve()
    pages = []
    assets = []
    issues = []
    regenerated_count = 0
    chapter_counts: Counter[str] = Counter()
    source_doc_count = 0

    for pdf_path in sorted(root.glob("[0-9][0-9]-*/*.pdf")):
        source_doc_count += 1
        chapter_rel = pdf_path.parent.relative_to(root).as_posix()
        stem = pdf_path.stem
        manifest_path, manifest, regenerated = resolve_manifest(root, pdf_path)
        regenerated_count += int(regenerated)
        asset_root = infer_asset_root(root, pdf_path, manifest_path, manifest)

        for issue in manifest.get("issues", []) or []:
            issues.append(f"{chapter_rel}/{stem}: {issue}")

        for page in manifest.get("pages", []) or []:
            if not isinstance(page, dict):
                continue
            record = dict(page)
            record["chapter"] = chapter_rel
            record["source_doc_stem"] = stem
            record["source_manifest_path"] = str(manifest_path.relative_to(root))
            pages.append(record)

        for asset in manifest.get("assets", []) or []:
            if not isinstance(asset, dict):
                continue
            record = dict(asset)
            for field in ASSET_PATH_FIELDS:
                record[field] = rewrite_path(root, asset_root, str(record.get(field) or ""))
            record["chapter"] = chapter_rel
            record["source_doc_stem"] = stem
            record["source_manifest_path"] = str(manifest_path.relative_to(root))
            assets.append(record)
            chapter_counts[chapter_rel] += 1

    assets.sort(key=lambda a: (a.get("chapter", ""), a.get("source_doc_stem", ""), int(a.get("page") or 0), a.get("asset_id", "")))
    pages.sort(key=lambda p: (p.get("chapter", ""), p.get("source_doc_stem", ""), int(p.get("page") or 0)))

    output_data = {
        "schema_version": "pdf2md-assets-campaign/v1",
        "doc_stem": doc_stem,
        "root": str(root),
        "source_doc_count": source_doc_count,
        "page_count": len(pages),
        "asset_count": len(assets),
        "regenerated_manifest_count": regenerated_count,
        "chapter_asset_counts": dict(sorted(chapter_counts.items())),
        "pages": pages,
        "assets": assets,
        "issues": issues,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(output_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_data, regenerated_count, chapter_counts


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    if not root.is_dir():
        raise SystemExit(f"ERROR: root is not a directory: {root}")
    data, regenerated_count, chapter_counts = build_campaign_manifest(root, output, args.doc_stem)
    print(f"source_docs={data['source_doc_count']}")
    print(f"pages={data['page_count']}")
    print(f"assets={data['asset_count']}")
    print(f"regenerated_manifests={regenerated_count}")
    for chapter, count in sorted(chapter_counts.items()):
        print(f"chapter_assets {chapter}={count}")
    print(f"output={output}")
    if data["issues"]:
        print(f"issues={len(data['issues'])}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
