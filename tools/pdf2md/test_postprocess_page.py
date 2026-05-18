#!/usr/bin/env python3
"""
Unit tests for postprocess_page.py — the 10-rule deterministic cleanup.

Each rule has at least one focused test. The pipeline as a whole is
exercised by integration tests in test_postprocess_pipeline.

Run:
    python3 -m pytest tools/pdf2md/test_postprocess_page.py -v
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location("postprocess_page", _HERE / "postprocess_page.py")
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["postprocess_page"] = _MOD
_SPEC.loader.exec_module(_MOD)


class Rule1NormaliseLineEndings(unittest.TestCase):
    def test_crlf_to_lf(self):
        self.assertEqual(_MOD.normalise_line_endings("a\r\nb\r\nc"), "a\nb\nc")

    def test_lone_cr_to_lf(self):
        self.assertEqual(_MOD.normalise_line_endings("a\rb\rc"), "a\nb\nc")

    def test_mixed_crlf_and_cr(self):
        self.assertEqual(_MOD.normalise_line_endings("a\r\nb\rc\n"), "a\nb\nc\n")


class Rule2StripMarkdownFences(unittest.TestCase):
    def test_strip_outer_fence_no_lang(self):
        self.assertEqual(_MOD.strip_markdown_fences("```\nhello\n```"), "hello")

    def test_strip_outer_fence_with_lang(self):
        self.assertEqual(_MOD.strip_markdown_fences("```markdown\nhello\n```"), "hello")

    def test_inner_fences_preserved(self):
        text = "intro\n\n```python\nprint('x')\n```\n\noutro"
        # No outer fences -> unchanged (modulo leading/trailing trim)
        self.assertIn("```python", _MOD.strip_markdown_fences(text))
        self.assertIn("print('x')", _MOD.strip_markdown_fences(text))

    def test_fence_with_backticks_in_lang_not_stripped(self):
        # Lang token with embedded backticks is treated as content, not fence
        text = "```py`ext\nx\n```"
        self.assertIn("```py`ext", _MOD.strip_markdown_fences(text))


class Rule3TrimTrailingWhitespace(unittest.TestCase):
    def test_strips_trailing_spaces(self):
        self.assertEqual(_MOD.trim_trailing_whitespace("a   \nb \nc"), "a\nb\nc")

    def test_strips_trailing_tabs(self):
        self.assertEqual(_MOD.trim_trailing_whitespace("a\t\t\nb"), "a\nb")

    def test_preserves_leading_whitespace(self):
        self.assertEqual(_MOD.trim_trailing_whitespace("  a   \n    b"), "  a\n    b")


class Rule4CollapseBlankLines(unittest.TestCase):
    def test_4_newlines_collapse_to_3(self):
        self.assertEqual(_MOD.collapse_blank_lines("a\n\n\n\nb"), "a\n\n\nb")

    def test_5_newlines_collapse_to_3(self):
        self.assertEqual(_MOD.collapse_blank_lines("a\n\n\n\n\nb"), "a\n\n\nb")

    def test_3_or_fewer_preserved(self):
        self.assertEqual(_MOD.collapse_blank_lines("a\n\n\nb"), "a\n\n\nb")
        self.assertEqual(_MOD.collapse_blank_lines("a\n\nb"), "a\n\nb")


class Rule5NormaliseHeadingSpacing(unittest.TestCase):
    def test_blank_line_inserted_before_heading(self):
        self.assertEqual(_MOD.normalise_heading_spacing("para\n# Heading"), "para\n\n# Heading")

    def test_heading_at_start_no_leading_blank(self):
        self.assertEqual(_MOD.normalise_heading_spacing("# Heading\npara"), "# Heading\npara")

    def test_collapses_excess_blanks_before_heading(self):
        self.assertEqual(
            _MOD.normalise_heading_spacing("para\n\n\n\n# Heading"),
            "para\n\n# Heading",
        )

    def test_all_heading_levels(self):
        for prefix in ("#", "##", "###", "####"):
            text = f"para\n{prefix} Heading"
            self.assertIn(f"\n\n{prefix} Heading", _MOD.normalise_heading_spacing(text))


class Rule6FixBrokenTables(unittest.TestCase):
    def test_inserts_separator_when_missing(self):
        text = "| A | B |\n| 1 | 2 |\n"
        result = _MOD.fix_broken_tables(text)
        self.assertIn("| --- | --- |", result)

    def test_does_not_double_separator(self):
        text = "| A | B |\n| --- | --- |\n| 1 | 2 |\n"
        result = _MOD.fix_broken_tables(text)
        # Only one separator should appear
        self.assertEqual(result.count("| --- | --- |"), 1)

    def test_non_table_unchanged(self):
        text = "Just prose.\nAnother line."
        self.assertEqual(_MOD.fix_broken_tables(text), text)


class Rule7RemoveMidTableSeparators(unittest.TestCase):
    def test_separator_at_position_2_kept(self):
        text = "| A | B |\n| --- | --- |\n| 1 | 2 |\n| 3 | 4 |\n"
        result = _MOD.remove_mid_table_separators(text)
        self.assertEqual(result.count("| --- | --- |"), 1)

    def test_extra_separator_in_middle_removed(self):
        text = "| A | B |\n| --- | --- |\n| 1 | 2 |\n| --- | --- |\n| 3 | 4 |\n"
        result = _MOD.remove_mid_table_separators(text)
        self.assertEqual(result.count("| --- | --- |"), 1)


class Rule8RemoveHallucinatedImages(unittest.TestCase):
    def test_example_com_placeholder_replaced_with_italic_alt(self):
        text = "before ![Yield curve](https://example.com/plot.png) after"
        self.assertEqual(_MOD.remove_hallucinated_images(text), "before *Yield curve* after")

    def test_placeholder_com_replaced(self):
        text = "![alt](https://placeholder.com/x.png)"
        self.assertEqual(_MOD.remove_hallucinated_images(text), "*alt*")

    def test_local_figures_path_preserved(self):
        text = "![caption](figures/x.png)"
        self.assertEqual(_MOD.remove_hallucinated_images(text), text)

    def test_local_tables_path_preserved(self):
        text = "![caption](tables/y.csv)"
        self.assertEqual(_MOD.remove_hallucinated_images(text), text)

    def test_real_https_link_preserved(self):
        text = "![alt](https://example-real.org/x.png)"
        # Not in fake-domains list, so preserved
        self.assertEqual(_MOD.remove_hallucinated_images(text), text)

    def test_empty_url_replaced(self):
        text = "![alt]()"
        self.assertEqual(_MOD.remove_hallucinated_images(text), "*alt*")

    def test_empty_url_empty_alt_removed_entirely(self):
        text = "x![]()y"
        self.assertEqual(_MOD.remove_hallucinated_images(text), "xy")


class Rule9RemoveInvisibleChars(unittest.TestCase):
    def test_zero_width_space_removed(self):
        self.assertEqual(_MOD.remove_invisible_chars("a​b"), "ab")

    def test_bom_removed(self):
        self.assertEqual(_MOD.remove_invisible_chars("﻿hello"), "hello")

    def test_soft_hyphen_removed(self):
        self.assertEqual(_MOD.remove_invisible_chars("co­operate"), "cooperate")

    def test_zwj_zwnj_word_joiner_removed(self):
        self.assertEqual(_MOD.remove_invisible_chars("a‌b‍c⁠d"), "abcd")

    def test_normal_unicode_preserved(self):
        self.assertEqual(_MOD.remove_invisible_chars("σε λεμ"), "σε λεμ")


class Rule10EnsureFinalNewline(unittest.TestCase):
    def test_adds_newline_when_missing(self):
        self.assertEqual(_MOD.ensure_final_newline("hello"), "hello\n")

    def test_no_double_newline(self):
        self.assertEqual(_MOD.ensure_final_newline("hello\n"), "hello\n")

    def test_strips_excess_trailing_whitespace(self):
        self.assertEqual(_MOD.ensure_final_newline("hello\n\n\n"), "hello\n")

    def test_empty_input_returns_single_newline(self):
        self.assertEqual(_MOD.ensure_final_newline(""), "\n")
        self.assertEqual(_MOD.ensure_final_newline("   "), "\n")


class FullPipeline(unittest.TestCase):
    def test_postprocess_idempotent_on_clean_input(self):
        text = "# Heading\n\nPara.\n"
        self.assertEqual(_MOD.postprocess(text), text)

    def test_postprocess_handles_messy_vlm_output(self):
        vlm_output = (
            "```markdown\r\n"
            "# Heading   \r\n"
            "\r\n\r\n\r\n\r\n"
            "Para with ​zero-width space.   \r\n"
            "\r\n"
            "| A | B |\r\n"
            "| 1 | 2 |\r\n"
            "\r\n"
            "![bad](https://example.com/x.png)\r\n"
            "```\r\n"
        )
        result = _MOD.postprocess(vlm_output)
        # Fence stripped
        self.assertNotIn("```markdown", result)
        self.assertFalse(result.startswith("```"))
        # CRLF normalized
        self.assertNotIn("\r", result)
        # Invisible chars removed
        self.assertNotIn("​", result)
        # Table separator inserted
        self.assertIn("| --- | --- |", result)
        # Hallucinated image stripped
        self.assertNotIn("example.com", result)
        self.assertIn("*bad*", result)
        # Excessive blank lines collapsed
        self.assertNotIn("\n\n\n\n", result)
        # Ends with single trailing newline
        self.assertTrue(result.endswith("\n"))
        self.assertFalse(result.endswith("\n\n"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
