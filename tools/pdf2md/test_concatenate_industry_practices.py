#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "concatenate_industry_practices", _HERE / "concatenate_industry_practices.py"
)
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["concatenate_industry_practices"] = _MOD
_SPEC.loader.exec_module(_MOD)


class ConcatenateIndustryPractices(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_concat_industry_"))
        self.root = self.tmp / "industry-practices"
        self.root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _doc(self, chapter: str, stem: str, md: str) -> Path:
        chapter_dir = self.root / chapter
        chapter_dir.mkdir(parents=True, exist_ok=True)
        (chapter_dir / f"{stem}.pdf").write_bytes(b"%PDF")
        md_path = chapter_dir / f"{stem}.md"
        md_path.write_text(md, encoding="utf-8")
        return md_path

    def test_collects_only_markdown_with_sibling_pdf_and_sorts(self):
        self._doc("02-beta", "02-beta-01", "b")
        self._doc("01-alpha", "01-alpha-01", "a")
        (self.root / "NOTE.md").write_text("skip", encoding="utf-8")
        orphan_dir = self.root / "01-alpha"
        (orphan_dir / "orphan.md").write_text("skip", encoding="utf-8")

        out = self.root / "industry-practices.md"
        source_count, chapter_count, _, empty = _MOD.concatenate(self.root, out)
        text = out.read_text(encoding="utf-8")

        self.assertEqual(source_count, 2)
        self.assertEqual(chapter_count, 2)
        self.assertEqual(empty, [])
        self.assertLess(text.index("01-alpha-01"), text.index("02-beta-01"))
        self.assertNotIn("orphan", text)
        self.assertNotIn("skip", text)

    def test_rewrites_new_and_legacy_asset_layouts(self):
        new_stem = "01-alpha-01"
        legacy_stem = "02-beta-01"
        self._doc("01-alpha", new_stem, "![x](tables/new.png)")
        self._doc("02-beta", legacy_stem, "[old](figures/old.png)")
        new_asset = self.root / "01-alpha" / "_assets" / new_stem / "tables" / "new.png"
        legacy_asset = self.root / "02-beta" / f"{legacy_stem}_assets" / "figures" / "old.png"
        new_asset.parent.mkdir(parents=True)
        legacy_asset.parent.mkdir(parents=True)
        new_asset.write_bytes(b"x")
        legacy_asset.write_bytes(b"x")

        out = self.root / "industry-practices.md"
        _, _, rewritten, _ = _MOD.concatenate(self.root, out)
        text = out.read_text(encoding="utf-8")

        self.assertEqual(rewritten, 2)
        self.assertIn("01-alpha/_assets/01-alpha-01/tables/new.png", text)
        self.assertIn("02-beta/02-beta-01_assets/figures/old.png", text)

    def test_emits_chapter_heading_once(self):
        self._doc("01-alpha", "01-alpha-01", "one")
        self._doc("01-alpha", "01-alpha-02", "two")

        out = self.root / "industry-practices.md"
        _MOD.concatenate(self.root, out)
        text = out.read_text(encoding="utf-8")

        self.assertEqual(text.count("## Alpha"), 1)
        self.assertIn("### 01-alpha-01", text)
        self.assertIn("### 01-alpha-02", text)


if __name__ == "__main__":
    unittest.main()
