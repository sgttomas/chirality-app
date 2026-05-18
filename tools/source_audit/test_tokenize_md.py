"""Tests for tools.source_audit.tokenize_md."""
from __future__ import annotations

import unittest

from tools.source_audit.tokenize_md import (
    AssetRef,
    Blank,
    EquationBlock,
    Placeholder,
    ProseLine,
    tokenize,
)


class Tokenize(unittest.TestCase):
    def test_pure_prose(self):
        toks = tokenize("Hello world\nSecond line")
        self.assertEqual(toks, [ProseLine("Hello world"), ProseLine("Second line")])

    def test_blank_line_emits_blank_token(self):
        toks = tokenize("A\n\nB")
        self.assertEqual(toks, [ProseLine("A"), Blank(), ProseLine("B")])

    def test_consecutive_blank_lines_collapse(self):
        toks = tokenize("A\n\n\n\nB")
        self.assertEqual(toks, [ProseLine("A"), Blank(), ProseLine("B")])

    def test_display_equation_extracted(self):
        toks = tokenize("Before\n$$E = mc^2$$\nAfter")
        self.assertEqual(
            toks,
            [ProseLine("Before"), EquationBlock("E = mc^2"), Blank(), ProseLine("After")],
        )

    def test_multiple_display_equations(self):
        toks = tokenize("$$a$$ middle $$b$$")
        kinds = [type(t).__name__ for t in toks]
        self.assertIn("EquationBlock", kinds)
        self.assertEqual(kinds.count("EquationBlock"), 2)

    def test_placeholder_figure(self):
        toks = tokenize("[FIGURE: caption text]")
        self.assertEqual(toks, [Placeholder("fig", "caption text")])

    def test_placeholder_table(self):
        toks = tokenize("[TABLE: pump dims]")
        self.assertEqual(toks, [Placeholder("tbl", "pump dims")])

    def test_placeholder_image(self):
        toks = tokenize("[IMAGE: masthead]")
        self.assertEqual(toks, [Placeholder("img", "masthead")])

    def test_placeholder_case_insensitive(self):
        toks = tokenize("[figure: c]")
        self.assertEqual(toks, [Placeholder("fig", "c")])

    def test_md_image_classified_by_path(self):
        toks = tokenize("![alt](figures/x.png)")
        self.assertEqual(toks, [AssetRef("fig", "figures/x.png")])

    def test_md_link_to_xlsx_classified_as_table(self):
        toks = tokenize("[XLSX](tables/data.xlsx)")
        self.assertEqual(toks, [AssetRef("tbl", "tables/data.xlsx")])

    def test_md_image_to_images_dir(self):
        toks = tokenize("![](images/logo.png)")
        self.assertEqual(toks, [AssetRef("img", "images/logo.png")])

    def test_inline_text_with_brackets_is_prose(self):
        toks = tokenize("This is normal prose with [bracketed] phrases.")
        self.assertEqual(toks, [ProseLine("This is normal prose with [bracketed] phrases.")])

    def test_display_equation_multiline_latex(self):
        toks = tokenize("$$\\frac{a}{b} = c$$")
        self.assertEqual(toks, [EquationBlock("\\frac{a}{b} = c")])

    def test_mixed_content(self):
        md = (
            "Intro paragraph.\n"
            "\n"
            "$$x = 1$$\n"
            "\n"
            "[FIGURE: A diagram]\n"
            "\n"
            "Final words."
        )
        toks = tokenize(md)
        # filter out blanks for type-only comparison
        types = [type(t).__name__ for t in toks if not isinstance(t, Blank)]
        self.assertEqual(types, ["ProseLine", "EquationBlock", "Placeholder", "ProseLine"])


if __name__ == "__main__":
    unittest.main()
