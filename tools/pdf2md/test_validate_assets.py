#!/usr/bin/env python3
"""
Unit tests for validate_assets.py.

Covers the four failure-mode categories the validator reports:
  - missing_on_disk:    referenced or manifest-declared paths not present
  - orphan_links:       Markdown links pointing at undeclared assets
  - widow_manifest_paths: manifest entries never referenced from Markdown
  - unmanifested_disk_paths: disk files not in the manifest

Also exercises the three link-extraction patterns (inline `![]()`,
reference-style `[ref]: path`, HTML `<img src="...">`) and the path-
normalisation rules (`./` prefix, `#anchor` / `?query` suffixes).

Run:
    python3 -m pytest tools/pdf2md/test_validate_assets.py -v
"""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location("validate_assets", _HERE / "validate_assets.py")
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["validate_assets"] = _MOD
_SPEC.loader.exec_module(_MOD)


def _make_fixture(tmp: Path, *, markdown: str, manifest_assets: list[dict],
                  disk_files: list[str]) -> tuple[Path, Path, Path]:
    """Build a synthetic <markdown.md, manifest.json, assets-root/> fixture."""
    md_path = tmp / "doc.md"
    md_path.write_text(markdown, encoding="utf-8")
    manifest_path = tmp / "manifest.json"
    manifest_path.write_text(json.dumps({"assets": manifest_assets}), encoding="utf-8")
    assets_root = tmp / "_root"
    assets_root.mkdir()
    for rel in disk_files:
        target = assets_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"x")
    return md_path, manifest_path, assets_root


def _run_main(md: Path, manifest: Path, root: Path) -> tuple[int, str]:
    sys.argv = [
        "validate_assets.py",
        "--markdown", str(md),
        "--manifest", str(manifest),
        "--assets-root", str(root),
    ]
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = _MOD.main()
    return rc, buf.getvalue()


class LinkExtraction(unittest.TestCase):
    def test_inline_image_link_extracted(self):
        links = _MOD.extract_asset_links("Body ![alt](figures/x.png) more")
        self.assertEqual(links, {"figures/x.png"})

    def test_inline_link_to_table_xlsx_extracted(self):
        links = _MOD.extract_asset_links("see [Table 1](tables/t1.xlsx)")
        self.assertEqual(links, {"tables/t1.xlsx"})

    def test_reference_style_link_definition_extracted(self):
        md = "Refer to ![Figure 1][fig1].\n\n[fig1]: figures/x.png\n"
        links = _MOD.extract_asset_links(md)
        self.assertIn("figures/x.png", links)

    def test_html_img_src_extracted(self):
        md = '<img src="images/z.png" alt="z" />'
        links = _MOD.extract_asset_links(md)
        self.assertEqual(links, {"images/z.png"})

    def test_html_img_src_single_quoted(self):
        md = "<img src='figures/y.png'>"
        links = _MOD.extract_asset_links(md)
        self.assertEqual(links, {"figures/y.png"})

    def test_non_asset_link_ignored(self):
        md = "[Anthropic](https://anthropic.com/) and ![x](http://example.com/x.png)"
        self.assertEqual(_MOD.extract_asset_links(md), set())

    def test_dot_slash_prefix_stripped(self):
        links = _MOD.extract_asset_links("![](./figures/x.png)")
        self.assertEqual(links, {"figures/x.png"})

    def test_anchor_suffix_stripped(self):
        links = _MOD.extract_asset_links("![](figures/x.png#caption)")
        self.assertEqual(links, {"figures/x.png"})

    def test_query_suffix_stripped(self):
        links = _MOD.extract_asset_links("![](figures/x.png?v=2)")
        self.assertEqual(links, {"figures/x.png"})

    def test_angle_brackets_stripped(self):
        # CommonMark permits <path> destinations
        links = _MOD.extract_asset_links("![](<figures/x.png>)")
        self.assertEqual(links, {"figures/x.png"})

    def test_escaped_bracket_not_extracted(self):
        # A backslash-escaped `]` should not start a link target
        md = "literal \\]( not a link )"
        self.assertEqual(_MOD.extract_asset_links(md), set())

    def test_multiple_links_dedup(self):
        md = "![](figures/x.png) and ![](figures/x.png) again"
        self.assertEqual(_MOD.extract_asset_links(md), {"figures/x.png"})

    def test_unrecognised_prefix_ignored(self):
        # /absolute/figures/x.png is not under one of the three asset roots
        md = "![](unrelated/x.png)"
        self.assertEqual(_MOD.extract_asset_links(md), set())


class ManifestPathExtraction(unittest.TestCase):
    def test_collects_png_and_xlsx_paths(self):
        manifest = {"assets": [
            {"png_path": "figures/x.png"},
            {"kind": "tbl", "xlsx_path": "tables/t1.xlsx",
             "table_data_json_path": "tables/t1.json"},
            {"png_path": "images/z.png", "xlsx_path": ""},
        ]}
        linked, supporting = _MOD.manifest_paths(manifest)
        self.assertEqual(linked, {"figures/x.png", "tables/t1.xlsx", "images/z.png"})
        self.assertEqual(supporting, {"tables/t1.json"})

    def test_needs_extraction_tbl_does_not_require_xlsx(self):
        """A tbl entry flagged `needs_extraction: true` must NOT contribute its
        xlsx_path (even if present) to the declared-paths set. The manifest
        is honest about the gap; validators must not promise an artifact."""
        manifest = {"assets": [
            {
                "kind": "tbl",
                "png_path": "tables/t2.png",
                "xlsx_path": "tables/t2.xlsx",  # would normally be required
                "needs_extraction": True,
            },
        ]}
        # Only the PNG crop is declared; the XLSX is not promised.
        linked, supporting = _MOD.manifest_paths(manifest)
        self.assertEqual(linked, {"tables/t2.png"})
        self.assertEqual(supporting, set())

    def test_handles_non_dict_entries(self):
        manifest = {"assets": ["string-entry", None, {"png_path": "figures/x.png"}]}
        linked, supporting = _MOD.manifest_paths(manifest)
        self.assertEqual(linked, {"figures/x.png"})
        self.assertEqual(supporting, set())

    def test_empty_assets_list(self):
        self.assertEqual(_MOD.manifest_paths({"assets": []}), (set(), set()))

    def test_missing_assets_key(self):
        self.assertEqual(_MOD.manifest_paths({}), (set(), set()))


class DiskWalk(unittest.TestCase):
    def test_walks_three_prefixes(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_validate_"))
        try:
            for rel in ("figures/a.png", "tables/b.xlsx", "images/c.png"):
                target = tmp / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"x")
            # A file in an unrelated dir is ignored
            (tmp / "other").mkdir()
            (tmp / "other" / "d.png").write_bytes(b"x")
            self.assertEqual(
                _MOD.disk_asset_paths(tmp),
                {"figures/a.png", "tables/b.xlsx", "images/c.png"},
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_missing_asset_subdirs_returns_empty(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_validate_"))
        try:
            self.assertEqual(_MOD.disk_asset_paths(tmp), set())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class EndToEndMain(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_validate_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_pass_when_everything_resolves(self):
        md, manifest, root = _make_fixture(
            self.tmp,
            markdown="![alt](figures/x.png)\n\n![](tables/t1.xlsx)\n",
            manifest_assets=[
                {"png_path": "figures/x.png"},
                {"kind": "tbl", "xlsx_path": "tables/t1.xlsx"},
            ],
            disk_files=["figures/x.png", "tables/t1.xlsx"],
        )
        rc, output = _run_main(md, manifest, root)
        self.assertEqual(rc, 0)
        self.assertIn("asset_validation=PASS", output)

    def test_missing_on_disk_fails(self):
        md, manifest, root = _make_fixture(
            self.tmp,
            markdown="![](figures/x.png)\n",
            manifest_assets=[{"png_path": "figures/x.png"}],
            disk_files=[],  # file referenced + declared, but missing on disk
        )
        rc, output = _run_main(md, manifest, root)
        self.assertEqual(rc, 1)
        self.assertIn("missing_on_disk=1", output)
        self.assertIn("figures/x.png", output)

    def test_orphan_link_fails(self):
        """Markdown references an asset the manifest doesn't declare."""
        md, manifest, root = _make_fixture(
            self.tmp,
            markdown="![](figures/orphan.png)\n",
            manifest_assets=[],
            disk_files=["figures/orphan.png"],
        )
        rc, output = _run_main(md, manifest, root)
        self.assertEqual(rc, 1)
        self.assertIn("orphan_links=1", output)

    def test_widow_manifest_path_fails(self):
        """Manifest declares an asset that no Markdown link points at."""
        md, manifest, root = _make_fixture(
            self.tmp,
            markdown="No image references here.\n",
            manifest_assets=[{"png_path": "figures/widow.png"}],
            disk_files=["figures/widow.png"],
        )
        rc, output = _run_main(md, manifest, root)
        self.assertEqual(rc, 1)
        self.assertIn("widow_manifest_paths=1", output)

    def test_unmanifested_disk_file_fails(self):
        """A file on disk under one of the three roots, not in the manifest."""
        md, manifest, root = _make_fixture(
            self.tmp,
            markdown="No references.\n",
            manifest_assets=[],
            disk_files=["images/surprise.png"],
        )
        rc, output = _run_main(md, manifest, root)
        self.assertEqual(rc, 1)
        self.assertIn("unmanifested_disk_paths=1", output)

    def test_multiple_categories_listed(self):
        md, manifest, root = _make_fixture(
            self.tmp,
            markdown="![](figures/orphan.png)\n",
            manifest_assets=[{"png_path": "figures/widow.png"}],
            disk_files=["images/surprise.png"],
        )
        rc, output = _run_main(md, manifest, root)
        self.assertEqual(rc, 1)
        # All four categories trigger at once
        self.assertIn("missing_on_disk=", output)
        self.assertIn("orphan_links=", output)
        self.assertIn("widow_manifest_paths=", output)
        self.assertIn("unmanifested_disk_paths=", output)

    def test_missing_markdown_exits_2(self):
        manifest = self.tmp / "manifest.json"
        manifest.write_text(json.dumps({"assets": []}))
        root = self.tmp / "_root"
        root.mkdir()
        sys.argv = [
            "validate_assets.py",
            "--markdown", str(self.tmp / "nope.md"),
            "--manifest", str(manifest),
            "--assets-root", str(root),
        ]
        self.assertEqual(_MOD.main(), 2)

    def test_missing_manifest_exits_2(self):
        md = self.tmp / "doc.md"
        md.write_text("")
        root = self.tmp / "_root"
        root.mkdir()
        sys.argv = [
            "validate_assets.py",
            "--markdown", str(md),
            "--manifest", str(self.tmp / "nope.json"),
            "--assets-root", str(root),
        ]
        self.assertEqual(_MOD.main(), 2)

    def test_assets_root_must_be_directory(self):
        md = self.tmp / "doc.md"
        md.write_text("")
        manifest = self.tmp / "manifest.json"
        manifest.write_text(json.dumps({"assets": []}))
        not_a_dir = self.tmp / "file.txt"
        not_a_dir.write_text("")
        sys.argv = [
            "validate_assets.py",
            "--markdown", str(md),
            "--manifest", str(manifest),
            "--assets-root", str(not_a_dir),
        ]
        self.assertEqual(_MOD.main(), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
