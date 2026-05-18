#!/usr/bin/env python3
"""
Unit tests for assemble_markdown.py.

Covers the canonical assembly pipeline used by both AGENT_PDF2MD Phase 4
(initial assembly of per-page Markdown into a single source) and by
AGENT_EQUATION_AUDIT Phase 3c (re-assembly after `process_flagged.py`
applies fixes via the anchored page template).

Run:
    python3 -m pytest tools/pdf2md/test_assemble_markdown.py -v
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
_SPEC = importlib.util.spec_from_file_location("assemble_markdown", _HERE / "assemble_markdown.py")
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["assemble_markdown"] = _MOD
_SPEC.loader.exec_module(_MOD)


def _make_work_dir(tmp: Path, *, pages_rendered: list[int],
                   page_contents: dict[int, str] | None = None,
                   page_template: str = "page_{page:04d}.md") -> Path:
    """Build a synthetic per-page WORK_DIR fixture."""
    pages_dir = tmp / "work"
    pages_dir.mkdir()
    manifest = {"pdf_path": "x.pdf", "pages_rendered": pages_rendered, "dpi": 300}
    (pages_dir / "manifest.json").write_text(json.dumps(manifest))
    for page_num in pages_rendered:
        if page_contents is None:
            content = f"# Page {page_num}\n\nBody text for page {page_num}.\n"
        elif page_num not in page_contents:
            continue  # leave the page file missing on disk
        else:
            content = page_contents[page_num]
        name = page_template.format(page=page_num)
        (pages_dir / name).write_text(content)
    return pages_dir


class HappyPath(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_assemble_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_three_pages_assembled_with_default_separator(self):
        pages_dir = _make_work_dir(self.tmp, pages_rendered=[1, 2, 3])
        out = self.tmp / "assembled.md"
        assembled, missing = _MOD.assemble(pages_dir, out)
        self.assertEqual(assembled, 3)
        self.assertEqual(missing, [])
        text = out.read_text()
        # Page bodies present in order
        self.assertIn("Page 1", text)
        self.assertIn("Page 2", text)
        self.assertIn("Page 3", text)
        # Default separator present between pages (2 occurrences for 3 pages)
        self.assertEqual(text.count("\n---\n"), 2)
        # Final newline guaranteed
        self.assertTrue(text.endswith("\n"))

    def test_order_follows_sorted_pages_rendered(self):
        """Pages out of order in manifest still assemble in numerical order."""
        pages_dir = _make_work_dir(self.tmp, pages_rendered=[3, 1, 2])
        out = self.tmp / "assembled.md"
        _MOD.assemble(pages_dir, out)
        text = out.read_text()
        i1 = text.index("Page 1")
        i2 = text.index("Page 2")
        i3 = text.index("Page 3")
        self.assertLess(i1, i2)
        self.assertLess(i2, i3)

    def test_returns_assembled_count_and_missing_list(self):
        pages_dir = _make_work_dir(self.tmp, pages_rendered=[1, 2, 3, 4],
                                   page_contents={1: "p1", 3: "p3"})
        out = self.tmp / "assembled.md"
        assembled, missing = _MOD.assemble(pages_dir, out)
        self.assertEqual(assembled, 2)
        self.assertEqual(sorted(missing), [2, 4])


class MissingAndEmptyPages(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_assemble_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_missing_page_file_replaced_with_placeholder(self):
        pages_dir = _make_work_dir(self.tmp, pages_rendered=[1, 2, 3],
                                   page_contents={1: "one", 3: "three"})
        out = self.tmp / "assembled.md"
        _MOD.assemble(pages_dir, out)
        text = out.read_text()
        self.assertIn("*[Page 2: conversion unavailable]*", text)
        self.assertIn("one", text)
        self.assertIn("three", text)

    def test_empty_page_file_replaced_with_empty_placeholder(self):
        pages_dir = _make_work_dir(self.tmp, pages_rendered=[1, 2],
                                   page_contents={1: "one", 2: "   \n\n  "})
        out = self.tmp / "assembled.md"
        assembled, missing = _MOD.assemble(pages_dir, out)
        text = out.read_text()
        self.assertIn("*[Page 2: empty]*", text)
        # Empty pages still count as missing for the report
        self.assertEqual(missing, [2])
        self.assertEqual(assembled, 1)


class Separators(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_assemble_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_custom_separator(self):
        pages_dir = _make_work_dir(self.tmp, pages_rendered=[1, 2])
        out = self.tmp / "assembled.md"
        _MOD.assemble(pages_dir, out, separator="===")
        text = out.read_text()
        self.assertIn("\n===\n", text)
        self.assertNotIn("\n---\n", text)

    def test_empty_separator_collapses_to_double_newline(self):
        pages_dir = _make_work_dir(self.tmp, pages_rendered=[1, 2])
        out = self.tmp / "assembled.md"
        _MOD.assemble(pages_dir, out, separator="")
        text = out.read_text()
        self.assertNotIn("\n---\n", text)
        # The two page bodies should be joined by a blank-line gap
        self.assertIn("Page 1", text)
        self.assertIn("Page 2", text)


class PageTemplates(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_assemble_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_anchored_template_consumed(self):
        """The EQUATION_AUDIT re-assembly uses the anchored template."""
        pages_dir = _make_work_dir(
            self.tmp, pages_rendered=[1, 2],
            page_template="page_{page:04d}.anchored.md",
        )
        out = self.tmp / "assembled.md"
        assembled, missing = _MOD.assemble(
            pages_dir, out, page_template="page_{page:04d}.anchored.md"
        )
        self.assertEqual(assembled, 2)
        self.assertEqual(missing, [])

    def test_resolve_page_filename_rejects_parent_dir_traversal(self):
        # ".." in resolved template must be refused
        with self.assertRaises(SystemExit):
            _MOD.resolve_page_filename("../escape_{page:04d}.md", 1)

    def test_resolve_page_filename_rejects_absolute_path(self):
        with self.assertRaises(SystemExit):
            _MOD.resolve_page_filename("/abs/page_{page:04d}.md", 1)

    def test_resolve_page_filename_rejects_invalid_format(self):
        # Template referencing a key not in the substitution dict
        with self.assertRaises(SystemExit):
            _MOD.resolve_page_filename("page_{bogus:04d}.md", 1)

    def test_resolve_page_filename_happy_path(self):
        self.assertEqual(
            _MOD.resolve_page_filename("page_{page:04d}.md", 7),
            "page_0007.md",
        )


class WhitespaceNormalization(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_assemble_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_excess_blank_lines_collapsed_to_three(self):
        pages_dir = _make_work_dir(self.tmp, pages_rendered=[1],
                                   page_contents={1: "before\n\n\n\n\n\nafter\n"})
        out = self.tmp / "assembled.md"
        _MOD.assemble(pages_dir, out)
        text = out.read_text()
        # The collapse rule rewrites runs of 4+ newlines down to exactly 3
        self.assertNotIn("\n\n\n\n", text)

    def test_final_newline_always_present(self):
        pages_dir = _make_work_dir(self.tmp, pages_rendered=[1],
                                   page_contents={1: "no trailing newline"})
        out = self.tmp / "assembled.md"
        _MOD.assemble(pages_dir, out)
        text = out.read_text()
        self.assertTrue(text.endswith("\n"))
        # And exactly one final newline, not many
        self.assertFalse(text.endswith("\n\n"))


class ManifestErrors(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_assemble_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_missing_manifest_exits_1(self):
        pages_dir = self.tmp / "work"
        pages_dir.mkdir()
        with self.assertRaises(SystemExit) as ctx:
            _MOD.assemble(pages_dir, self.tmp / "out.md")
        self.assertEqual(ctx.exception.code, 1)

    def test_empty_pages_rendered_exits_1(self):
        pages_dir = self.tmp / "work"
        pages_dir.mkdir()
        (pages_dir / "manifest.json").write_text(
            json.dumps({"pdf_path": "x.pdf", "pages_rendered": [], "dpi": 300})
        )
        with self.assertRaises(SystemExit) as ctx:
            _MOD.assemble(pages_dir, self.tmp / "out.md")
        self.assertEqual(ctx.exception.code, 1)


class OutputCreation(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_assemble_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_output_parent_dir_created_if_missing(self):
        pages_dir = _make_work_dir(self.tmp, pages_rendered=[1])
        out = self.tmp / "deep" / "nested" / "out.md"
        _MOD.assemble(pages_dir, out)
        self.assertTrue(out.is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
