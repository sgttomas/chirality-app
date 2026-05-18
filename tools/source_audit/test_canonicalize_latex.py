"""Tests for tools.source_audit.canonicalize_latex (v1 textual)."""
from __future__ import annotations

import unittest

from tools.source_audit.canonicalize_latex import (
    canonicalize_latex_v1,
    equation_content_equal,
)


class CanonicalizeLatexV1(unittest.TestCase):
    def test_dfrac_equiv_frac(self):
        self.assertEqual(
            canonicalize_latex_v1(r"\dfrac{a}{b}"),
            canonicalize_latex_v1(r"\frac{a}{b}"),
        )

    def test_tfrac_equiv_frac(self):
        self.assertEqual(
            canonicalize_latex_v1(r"\tfrac{a}{b}"),
            canonicalize_latex_v1(r"\frac{a}{b}"),
        )

    def test_mathrm_and_rm_brace_equivalent(self):
        self.assertEqual(
            canonicalize_latex_v1(r"\mathrm{d}x"),
            canonicalize_latex_v1(r"{\rm d}x"),
        )

    def test_operatorname_to_mathrm(self):
        self.assertEqual(
            canonicalize_latex_v1(r"\operatorname{sin} x"),
            canonicalize_latex_v1(r"\mathrm{sin} x"),
        )

    def test_tag_numeric_stripped(self):
        self.assertEqual(
            canonicalize_latex_v1(r"x=y \tag{2.4}"),
            canonicalize_latex_v1("x=y"),
        )

    def test_tag_alphanumeric_stripped(self):
        self.assertEqual(
            canonicalize_latex_v1(r"S_{EB} = 1.6(S_c+S_h) \tag{3.13a}"),
            canonicalize_latex_v1(r"S_{EB} = 1.6(S_c+S_h)"),
        )

    def test_tag_empty_stripped(self):
        self.assertEqual(
            canonicalize_latex_v1(r"a+b \tag{}"),
            canonicalize_latex_v1("a+b"),
        )

    def test_bare_tag_without_braces_preserved(self):
        # Defensive: `\tag` not followed by `{...}` is not the canonical
        # form. Leave it so a genuinely malformed proposal still surfaces.
        self.assertNotEqual(
            canonicalize_latex_v1(r"a+b \tag"),
            canonicalize_latex_v1(r"a+b"),
        )

    def test_tag_strip_does_not_mask_math_difference(self):
        # `a+b \tag{1}` vs `a-b \tag{1}` — the tag is stripped from both,
        # but the +/- difference must remain visible.
        self.assertNotEqual(
            canonicalize_latex_v1(r"a+b \tag{1}"),
            canonicalize_latex_v1(r"a-b \tag{1}"),
        )
        # `a+b \tag{1}` vs `a+b \tag{2}` — both strip to `a+b`; equal.
        self.assertEqual(
            canonicalize_latex_v1(r"a+b \tag{1}"),
            canonicalize_latex_v1(r"a+b \tag{2}"),
        )

    def test_thin_spaces_removed(self):
        self.assertEqual(
            canonicalize_latex_v1(r"a\,b"),
            canonicalize_latex_v1(r"ab"),
        )
        self.assertEqual(
            canonicalize_latex_v1(r"a\;b\!c\:d"),
            canonicalize_latex_v1(r"abcd"),
        )

    def test_left_right_dropped(self):
        self.assertEqual(
            canonicalize_latex_v1(r"\left( a + b \right)"),
            canonicalize_latex_v1(r"(a + b)"),
        )

    def test_brace_around_single_token_stripped(self):
        self.assertEqual(
            canonicalize_latex_v1(r"{a} + {b}"),
            canonicalize_latex_v1(r"a + b"),
        )

    def test_brace_in_superscript_preserved(self):
        # x^{2} should NOT collapse to x^2 textually here, because
        # {2} after ^ is semantically equivalent only structurally;
        # the regex specifically preserves these to avoid false-merging.
        self.assertEqual(
            canonicalize_latex_v1(r"x^{2}"),
            canonicalize_latex_v1(r"x^{2}"),
        )
        # but x^{2} and x^2 should *not* be falsely declared equal by
        # the textual canonicalizer (different surface forms; v2 AST
        # would unify, v1 leaves as a real-looking proposal).
        self.assertNotEqual(
            canonicalize_latex_v1(r"x^{2}"),
            canonicalize_latex_v1(r"x^2"),
        )

    def test_whitespace_collapsed(self):
        self.assertEqual(
            canonicalize_latex_v1("a   +   b"),
            canonicalize_latex_v1("a+b"),
        )

    def test_genuine_difference_preserved(self):
        # a+b vs a-b must remain unequal
        self.assertNotEqual(
            canonicalize_latex_v1("a + b"),
            canonicalize_latex_v1("a - b"),
        )

    def test_equation_content_equal_helper(self):
        self.assertTrue(equation_content_equal(r"\dfrac{a}{b}", r"\frac{a}{b}"))
        self.assertFalse(equation_content_equal(r"\frac{a}{b}", r"\frac{a}{c}"))


if __name__ == "__main__":
    unittest.main()
