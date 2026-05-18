"""Tests for tools.source_audit.normalize_prose."""
from __future__ import annotations

import unittest

from tools.source_audit.normalize_prose import normalize_for_diff, normalize_prose


class NormalizeProse(unittest.TestCase):
    def test_smart_quotes_to_ascii(self):
        self.assertEqual(normalize_prose("“hello”"), '"hello"')
        self.assertEqual(normalize_prose("don’t"), "don't")

    def test_dashes_unified(self):
        self.assertEqual(normalize_prose("a—b"), "a-b")
        self.assertEqual(normalize_prose("a–b"), "a-b")

    def test_nbsp_to_space(self):
        self.assertEqual(normalize_prose("a b"), "a b")

    def test_ligature_fi(self):
        self.assertEqual(normalize_prose("ﬁnal"), "final")

    def test_ligature_ffl(self):
        self.assertEqual(normalize_prose("aﬄuence"), "affluence")

    def test_soft_hyphen_stripped(self):
        self.assertEqual(normalize_prose("re­cent"), "recent")

    def test_linebreak_hyphen_dehyphenated(self):
        self.assertEqual(normalize_prose("prog-\nress"), "progress")

    def test_multispace_collapsed(self):
        self.assertEqual(normalize_prose("a    b"), "a b")

    def test_case_preserved(self):
        # case-only differences are real, not cosmetic
        self.assertNotEqual(normalize_prose("Hello"), normalize_prose("hello"))


class NormalizeForDiff(unittest.TestCase):
    def test_collapses_newlines(self):
        self.assertEqual(normalize_for_diff("a\nb\nc"), "a b c")

    def test_trailing_punctuation_stripped(self):
        self.assertEqual(normalize_for_diff("hello."), normalize_for_diff("hello"))
        self.assertEqual(normalize_for_diff("hello,"), normalize_for_diff("hello"))
        self.assertEqual(normalize_for_diff("hello;"), normalize_for_diff("hello"))

    def test_typography_normalized_into_diff_form(self):
        self.assertEqual(
            normalize_for_diff("don’t “stop”"),
            normalize_for_diff("don't \"stop\""),
        )


if __name__ == "__main__":
    unittest.main()
