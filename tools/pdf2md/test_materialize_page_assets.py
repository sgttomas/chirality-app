#!/usr/bin/env python3
"""
Unit tests for materialize_page_assets.py — focused on the strict-rejection
paths added when the asset-pipeline contract was tightened. The tool is now
the gate that surfaces skill-contract drift to the orchestrator.

Run:
    python3 -m pytest tools/pdf2md/test_materialize_page_assets.py -v
"""

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
    "materialize_page_assets", _HERE / "materialize_page_assets.py"
)
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["materialize_page_assets"] = _MOD
_SPEC.loader.exec_module(_MOD)


def _write_json(payload, tmpdir: Path) -> Path:
    p = tmpdir / "page_0001_assets.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


class LoadAssetsStrict(unittest.TestCase):
    """The contracted shape per skills/pdf2md-page-assets/SKILL.md is strict."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_mat_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_canonical_shape_accepted(self):
        p = _write_json(
            {
                "schema_version": "pdf2md-page-assets/v1",
                "run_status": "SUCCESS",
                "doc_stem": "X", "page": 1, "total_pages": 1,
                "asset_policy": "prose-document-assets-v1",
                "assets": [{"kind": "fig", "ordinal": 1, "caption": "Y",
                            "bbox_norm": [0.1, 0.1, 0.9, 0.9]}],
                "issues": [],
            },
            self.tmp,
        )
        result = _MOD.load_assets(p)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["kind"], "fig")

    def test_bare_list_rejected(self):
        p = _write_json([{"kind": "fig"}], self.tmp)
        with self.assertRaises(SystemExit) as ctx:
            _MOD.load_assets(p)
        self.assertIn("JSON object", str(ctx.exception))

    def test_sibling_tables_key_rejected(self):
        p = _write_json(
            {"assets": [], "tables": [{"kind": "tbl"}]}, self.tmp
        )
        with self.assertRaises(SystemExit) as ctx:
            _MOD.load_assets(p)
        self.assertIn("forbidden sibling-keys", str(ctx.exception))
        self.assertIn("tables", str(ctx.exception))

    def test_sibling_figures_key_rejected(self):
        p = _write_json(
            {"assets": [], "figures": [{"kind": "fig"}]}, self.tmp
        )
        with self.assertRaises(SystemExit) as ctx:
            _MOD.load_assets(p)
        self.assertIn("figures", str(ctx.exception))

    def test_missing_assets_field_rejected(self):
        p = _write_json({"schema_version": "v1"}, self.tmp)
        with self.assertRaises(SystemExit) as ctx:
            _MOD.load_assets(p)
        self.assertIn("missing required `assets`", str(ctx.exception))

    def test_assets_not_list_rejected(self):
        p = _write_json({"assets": "not a list"}, self.tmp)
        with self.assertRaises(SystemExit) as ctx:
            _MOD.load_assets(p)
        self.assertIn("must be a JSON array", str(ctx.exception))


class BboxStrict(unittest.TestCase):
    def test_list_form_accepted(self):
        bbox = _MOD.bbox_from_asset({"bbox_norm": [0.1, 0.2, 0.3, 0.4]})
        self.assertEqual(bbox, [0.1, 0.2, 0.3, 0.4])

    def test_dict_form_rejected(self):
        """The dict form was a legacy fallback that masked skill drift."""
        bbox = _MOD.bbox_from_asset({"bbox_norm": {"x0": 0.1, "y0": 0.2, "x1": 0.3, "y1": 0.4}})
        self.assertIsNone(bbox)

    def test_wrong_length_rejected(self):
        self.assertIsNone(_MOD.bbox_from_asset({"bbox_norm": [0.1, 0.2, 0.3]}))
        self.assertIsNone(_MOD.bbox_from_asset({"bbox_norm": [0.1, 0.2, 0.3, 0.4, 0.5]}))

    def test_missing_rejected(self):
        self.assertIsNone(_MOD.bbox_from_asset({}))

    def test_non_numeric_rejected(self):
        self.assertIsNone(_MOD.bbox_from_asset({"bbox_norm": ["a", "b", "c", "d"]}))


class CaptionStrict(unittest.TestCase):
    def test_caption_field_only(self):
        self.assertEqual(_MOD.caption_from_asset({"caption": "Hello"}), "Hello")

    def test_title_field_no_longer_falls_back(self):
        """Previously caption_from_asset would fall back to title/label/name —
        those alternates masked drift. Strict version reads only `caption`."""
        self.assertEqual(_MOD.caption_from_asset({"title": "X"}), "")
        self.assertEqual(_MOD.caption_from_asset({"label": "X"}), "")
        self.assertEqual(_MOD.caption_from_asset({"name": "X"}), "")

    def test_empty_caption_returns_empty(self):
        self.assertEqual(_MOD.caption_from_asset({}), "")
        self.assertEqual(_MOD.caption_from_asset({"caption": ""}), "")


class KindStrict(unittest.TestCase):
    def test_canonical_literals_accepted(self):
        self.assertEqual(_MOD.normalize_kind({"kind": "fig"}), "fig")
        self.assertEqual(_MOD.normalize_kind({"kind": "tbl"}), "tbl")
        self.assertEqual(_MOD.normalize_kind({"kind": "img"}), "img")

    def test_alias_words_rejected(self):
        """Previously kind aliases like `figure`, `image`, `diagram`, `chart`,
        `logo`, `photo` were normalized. The strict version rejects them."""
        for alias in ("figure", "image", "table", "diagram", "plot", "chart",
                      "logo", "photo", "photograph"):
            self.assertEqual(_MOD.normalize_kind({"kind": alias}), "",
                             f"alias {alias!r} should be rejected")

    def test_alternate_keys_rejected(self):
        """Previously `type`/`subtype` would be consulted as fallbacks."""
        self.assertEqual(_MOD.normalize_kind({"type": "fig"}), "")
        self.assertEqual(_MOD.normalize_kind({"subtype": "fig"}), "")

    def test_missing_kind_returns_empty(self):
        self.assertEqual(_MOD.normalize_kind({}), "")

    def test_uppercase_rejected(self):
        """Canonical literals are lowercase; uppercase is drift."""
        self.assertEqual(_MOD.normalize_kind({"kind": "FIG"}), "")
        self.assertEqual(_MOD.normalize_kind({"kind": "Fig"}), "")


class TableDataValidation(unittest.TestCase):
    """The materializer wraps render_table_xlsx.validate_table_data so the
    rest of the page survives one bad table. These tests cover the wrapper +
    the canonicalization helpers."""

    def _td(self) -> dict:
        return {
            "schema_version": "pdf2md-table/v1",
            "header_rows": 1,
            "section_dividers": [],
            "continuation_of": None,
            "footnotes": [],
            "rows": [
                {"cells": [{"value": "A", "is_header": True}]},
                {"cells": [{"value": 1, "type": "number"}]},
            ],
        }

    def test_valid_table_data_returns_no_issues(self):
        self.assertEqual(_MOD.validate_table_data(self._td()), [])

    def test_invalid_schema_version_recorded_as_issue(self):
        bad = self._td()
        bad["schema_version"] = "pdf2md-table/v0"
        issues = _MOD.validate_table_data(bad)
        self.assertEqual(len(issues), 1)
        self.assertIn("invalid_table_data", issues[0])
        self.assertIn("schema_version", issues[0])

    def test_table_data_sha256_is_canonical(self):
        # Same content, different key insertion order → same hash.
        td1 = self._td()
        td2 = {
            "rows": td1["rows"],
            "schema_version": td1["schema_version"],
            "header_rows": td1["header_rows"],
            "section_dividers": td1["section_dividers"],
            "continuation_of": td1["continuation_of"],
            "footnotes": td1["footnotes"],
        }
        self.assertEqual(_MOD.table_data_sha256(td1), _MOD.table_data_sha256(td2))

    def test_canonical_json_sorted_and_lf_terminated(self):
        text = _MOD.canonical_table_data_json(self._td())
        self.assertTrue(text.endswith("\n"))
        # Sorted keys: continuation_of comes before footnotes alphabetically
        self.assertLess(text.find('"continuation_of"'), text.find('"footnotes"'))


class TableReferenceRendering(unittest.TestCase):
    """build_reference (and the inline rewriter equivalents) emit [XLSX] —
    the legacy [CSV] form is gone."""

    def test_table_reference_uses_xlsx_label(self):
        asset = {
            "asset_id": "X_p0001_tbl01",
            "kind": "tbl",
            "caption": "Demo",
            "xlsx_path": "tables/X_p0001_tbl01_demo.xlsx",
            "png_path": "tables/X_p0001_tbl01_demo.png",
            "issues": [],
        }
        ref = _MOD.build_reference(asset)
        self.assertIn("[XLSX](tables/X_p0001_tbl01_demo.xlsx)", ref)
        self.assertNotIn("[CSV]", ref)

    def test_table_reference_needs_extraction_marker(self):
        asset = {
            "asset_id": "X_p0001_tbl02",
            "kind": "tbl",
            "caption": "Bbox-only",
            "xlsx_path": "",
            "png_path": "tables/X_p0001_tbl02.png",
            "needs_extraction": True,
            "issues": [],
        }
        ref = _MOD.build_reference(asset)
        self.assertIn("needs_extraction", ref)


if __name__ == "__main__":
    unittest.main(verbosity=2)
