#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "aggregate_campaign_asset_manifest", _HERE / "aggregate_campaign_asset_manifest.py"
)
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["aggregate_campaign_asset_manifest"] = _MOD
_SPEC.loader.exec_module(_MOD)


class AggregateCampaignAssetManifest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_campaign_manifest_"))
        self.root = self.tmp / "industry-practices"
        self.root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _pdf(self, chapter: str, stem: str) -> Path:
        chapter_dir = self.root / chapter
        chapter_dir.mkdir(parents=True, exist_ok=True)
        pdf = chapter_dir / f"{stem}.pdf"
        pdf.write_bytes(b"%PDF")
        return pdf

    def _manifest(self, path: Path, stem: str, asset_path: str = "tables/a.xlsx"):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "schema_version": "pdf2md-assets-document/v3",
                    "doc_stem": stem,
                    "page_manifest_count": 1,
                    "asset_count": 1,
                    "pages": [{"page": 1, "asset_count": 1}],
                    "assets": [{"asset_id": f"{stem}_p0001_tbl01", "kind": "tbl", "page": 1, "xlsx_path": asset_path}],
                    "issues": [],
                }
            ),
            encoding="utf-8",
        )

    def test_prefers_new_manifest_location(self):
        pdf = self._pdf("01-alpha", "01-alpha-01")
        new_manifest = pdf.parent / "_assets" / pdf.stem / f"{pdf.stem}_assets_manifest.json"
        legacy_manifest = pdf.parent / f"{pdf.stem}_pdf2md_work" / "asset_manifest.json"
        self._manifest(new_manifest, pdf.stem, "tables/new.xlsx")
        self._manifest(legacy_manifest, pdf.stem, "tables/old.xlsx")

        out = self.root / "industry-practices_assets_manifest.json"
        data, regenerated, _ = _MOD.build_campaign_manifest(self.root, out, "industry-practices")

        self.assertEqual(regenerated, 0)
        self.assertEqual(data["asset_count"], 1)
        self.assertEqual(data["assets"][0]["xlsx_path"], "01-alpha/_assets/01-alpha-01/tables/new.xlsx")

    def test_uses_legacy_manifest_when_new_missing(self):
        pdf = self._pdf("02-beta", "02-beta-01")
        legacy_manifest = pdf.parent / f"{pdf.stem}_pdf2md_work" / "asset_manifest.json"
        self._manifest(legacy_manifest, pdf.stem, "figures/old.png")
        legacy_asset_dir = pdf.parent / f"{pdf.stem}_assets"
        legacy_asset_dir.mkdir()

        out = self.root / "industry-practices_assets_manifest.json"
        data, regenerated, _ = _MOD.build_campaign_manifest(self.root, out, "industry-practices")

        self.assertEqual(regenerated, 0)
        self.assertEqual(data["assets"][0]["xlsx_path"], "02-beta/02-beta-01_assets/figures/old.png")

    def test_regenerates_missing_manifest_from_page_materialized(self):
        pdf = self._pdf("03-gamma", "03-gamma-01")
        work = pdf.parent / f"{pdf.stem}_pdf2md_work"
        work.mkdir()
        asset_root = pdf.parent / f"{pdf.stem}_assets"
        page_manifest = work / "page_0001_assets_materialized.json"
        page_manifest.write_text(
            json.dumps(
                {
                    "doc_stem": pdf.stem,
                    "page": 1,
                    "anchored_markdown": str(work / "page_0001.anchored.md"),
                    "assets_root": str(asset_root),
                    "assets": [{"asset_id": "a1", "kind": "tbl", "xlsx_path": "tables/a.xlsx"}],
                }
            ),
            encoding="utf-8",
        )

        out = self.root / "industry-practices_assets_manifest.json"
        data, regenerated, _ = _MOD.build_campaign_manifest(self.root, out, "industry-practices")

        self.assertEqual(regenerated, 1)
        self.assertTrue((work / "asset_manifest.json").is_file())
        self.assertEqual(data["assets"][0]["xlsx_path"], "03-gamma/03-gamma-01_assets/tables/a.xlsx")
        self.assertEqual(data["assets"][0]["source_doc_stem"], pdf.stem)


if __name__ == "__main__":
    unittest.main()
