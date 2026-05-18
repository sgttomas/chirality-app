#!/usr/bin/env python3
"""
aggregate_asset_manifest.py
Merge per-page PDF2MD asset materialization manifests into one document manifest.

Usage:
    python3 aggregate_asset_manifest.py WORK_DIR OUTPUT_JSON [--doc-stem MWK_1956]

Inputs:
    WORK_DIR      PDF2MD work directory containing page_NNNN_assets_materialized.json files
    OUTPUT_JSON   document-level asset manifest path
    --doc-stem    optional expected document stem

Outputs:
    OUTPUT_JSON containing all page asset records in page/order sequence.

Example:
    python3 tools/pdf2md/aggregate_asset_manifest.py \
      ./MWK_1956_pdf2md_work ./_Sources/MWK_1956_assets_manifest.json --doc-stem MWK_1956
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PAGE_MANIFEST_RE = re.compile(r"^page_(\d{4})_assets_materialized\.json$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate PDF2MD per-page asset manifests.")
    parser.add_argument("work_dir")
    parser.add_argument("output_json")
    parser.add_argument("--doc-stem")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    work_dir = Path(args.work_dir).resolve()
    output_json = Path(args.output_json).resolve()
    if not work_dir.is_dir():
        raise SystemExit(f"ERROR: work_dir is not a directory: {work_dir}")

    manifests: list[tuple[int, Path]] = []
    for path in work_dir.glob("page_*_assets_materialized.json"):
        match = PAGE_MANIFEST_RE.match(path.name)
        if match:
            manifests.append((int(match.group(1)), path))
    manifests.sort()

    # Read optional page_folios.json (produced by the pdf2md-folio-extract
    # fan-out). Keys are physical page numbers as strings; values are the
    # skill's per-page JSON envelope (`run_status`, `page_label`,
    # `page_label_source`, etc.). Missing file is fine — every page record
    # falls back to `page_label_source: "unreviewed"`.
    page_folios: dict[str, dict] = {}
    page_folios_path = work_dir / "page_folios.json"
    if page_folios_path.is_file():
        try:
            raw_folios = json.loads(page_folios_path.read_text(encoding="utf-8"))
            if isinstance(raw_folios, dict):
                page_folios = {str(k): v for k, v in raw_folios.items() if isinstance(v, dict)}
        except (OSError, json.JSONDecodeError) as exc:
            issues_preload = [f"page_folios.json: failed to read ({exc})"]
        else:
            issues_preload = []
    else:
        issues_preload = []

    pages = []
    assets = []
    issues = list(issues_preload)
    doc_stems = set()
    for page_num, path in manifests:
        data = json.loads(path.read_text(encoding="utf-8"))
        doc_stem = data.get("doc_stem")
        if doc_stem:
            doc_stems.add(str(doc_stem))
        if args.doc_stem and doc_stem and doc_stem != args.doc_stem:
            issues.append(f"{path.name}: doc_stem {doc_stem!r} != expected {args.doc_stem!r}")
        page_assets = data.get("assets", [])
        if not isinstance(page_assets, list):
            issues.append(f"{path.name}: assets is not a list")
            page_assets = []
        # v3 additive fields: page_label / page_label_source.
        # Sourcing precedence:
        #   - page_folios.json present + page keyed with SUCCESS/NO_FOLIO →
        #     take the skill's `page_label` and `page_label_source` ("vlm")
        #   - page_folios.json present + page keyed with FAILED/FAILED_INPUTS →
        #     page_label=null, page_label_source="vlm_failed"
        #   - file absent OR page not keyed → page_label=null,
        #     page_label_source="unreviewed"
        page_label: str | None = None
        page_label_source = "unreviewed"
        folio_record = page_folios.get(str(page_num))
        if folio_record is not None:
            run_status = folio_record.get("run_status")
            if run_status in {"SUCCESS", "NO_FOLIO"}:
                raw_label = folio_record.get("page_label")
                page_label = raw_label if isinstance(raw_label, str) or raw_label is None else None
                raw_source = folio_record.get("page_label_source")
                page_label_source = raw_source if isinstance(raw_source, str) and raw_source else "vlm"
            else:
                # FAILED, FAILED_INPUTS, or anything unexpected → mark failed
                page_label = None
                page_label_source = "vlm_failed"

        pages.append(
            {
                "page": page_num,
                "manifest_path": str(path),
                "asset_count": len(page_assets),
                "anchored_markdown": data.get("anchored_markdown", ""),
                "page_label": page_label,
                "page_label_source": page_label_source,
            }
        )
        for asset in page_assets:
            if isinstance(asset, dict):
                record = dict(asset)
                record["page"] = page_num
                assets.append(record)

    output = {
        "schema_version": "pdf2md-assets-document/v3",
        "doc_stem": args.doc_stem or (sorted(doc_stems)[0] if len(doc_stems) == 1 else ""),
        "work_dir": str(work_dir),
        "page_manifest_count": len(manifests),
        "asset_count": len(assets),
        "pages": pages,
        "assets": assets,
        "issues": issues,
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"page_manifests={len(manifests)} assets={len(assets)} output={output_json}")
    if issues:
        print(f"issues={len(issues)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
