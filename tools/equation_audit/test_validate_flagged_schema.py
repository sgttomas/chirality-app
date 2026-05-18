#!/usr/bin/env python3
"""
Unit tests for validate_flagged_schema.py.

Covers the prose-detection heuristic (the key reason this tool gates
process_flagged.py — preventing natural-language notes from reaching the
deterministic fix-applier without first being converted to LaTeX via the
equation-flag-interpret skill).

Run:
    python3 -m pytest tools/equation_audit/test_validate_flagged_schema.py -v
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "validate_flagged_schema", _HERE / "validate_flagged_schema.py"
)
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["validate_flagged_schema"] = _MOD
_SPEC.loader.exec_module(_MOD)


class ProseDetection(unittest.TestCase):
    """Heuristic: prose-like iff no `\\<command>` AND >=3 distinct English stop-words."""

    def test_pure_latex_not_prose(self):
        self.assertFalse(_MOD.is_prose_like(r"\frac{2}{\sqrt{3}} Y = \sigma_1 - \sigma_3"))

    def test_natural_language_correction_note_is_prose(self):
        note = "the numerical constant 1.155 should be replaced with the symbol kappa"
        self.assertTrue(_MOD.is_prose_like(note))

    def test_short_replacement_directive_is_prose(self):
        self.assertTrue(_MOD.is_prose_like("the denominator should be 2 not 3"))

    def test_pure_math_without_english_not_prose(self):
        self.assertFalse(_MOD.is_prose_like("x = 2 + 3"))
        self.assertFalse(_MOD.is_prose_like("Y / 2 = sigma_1 - sigma_3"))

    def test_single_symbol_not_prose(self):
        self.assertFalse(_MOD.is_prose_like("X"))
        self.assertFalse(_MOD.is_prose_like("0.5"))

    def test_empty_not_prose(self):
        """An empty description fails the non-empty check separately; is_prose_like
        only flags prose, not emptiness."""
        self.assertFalse(_MOD.is_prose_like(""))
        self.assertFalse(_MOD.is_prose_like("   "))

    def test_one_stop_word_not_prose(self):
        # Heuristic requires 3+ distinct stop-words
        self.assertFalse(_MOD.is_prose_like("the equation"))

    def test_two_distinct_stop_words_not_prose(self):
        self.assertFalse(_MOD.is_prose_like("the and equation"))

    def test_latex_command_overrides_stopwords(self):
        """Even if a description contains many English words, presence of a
        backslash command (e.g. \\frac) means it's LaTeX with annotations,
        not prose."""
        mixed = r"the corrected form should be \frac{x}{y}"
        # has \frac → not prose; the validator accepts it because LaTeX is present
        self.assertFalse(_MOD.is_prose_like(mixed))


class EntryValidation(unittest.TestCase):
    def test_valid_entry_no_errors(self):
        errors = _MOD.validate_entry(
            "5:b4fcc24a1569",
            {
                "page": 5,
                "hash": "b4fcc24a1569",
                "current_latex": r"\sigma = f(\epsilon)",
                "description": r"\sigma_0 = f(\epsilon)",
                "flagged_at": "2026-05-16",
            },
        )
        self.assertEqual(errors, [])

    def test_invalid_key_shape(self):
        errors = _MOD.validate_entry(
            "5:bad",
            {"page": 5, "hash": "bad", "current_latex": "x", "description": "y", "flagged_at": "t"},
        )
        self.assertTrue(any("must match" in e for e in errors))

    def test_hash_mismatches_key(self):
        errors = _MOD.validate_entry(
            "5:aaaaaaaaaaaa",
            {
                "page": 5,
                "hash": "bbbbbbbbbbbb",
                "current_latex": "x",
                "description": "y",
                "flagged_at": "t",
            },
        )
        self.assertTrue(any("hash field" in e and "!=" in e for e in errors))

    def test_missing_required_field(self):
        errors = _MOD.validate_entry(
            "5:aaaaaaaaaaaa",
            {"page": 5, "hash": "aaaaaaaaaaaa", "current_latex": "x", "description": "y"},
        )
        self.assertTrue(any("missing required field 'flagged_at'" in e for e in errors))

    def test_prose_description_rejected_with_skill_pointer(self):
        errors = _MOD.validate_entry(
            "5:aaaaaaaaaaaa",
            {
                "page": 5,
                "hash": "aaaaaaaaaaaa",
                "current_latex": "x",
                "description": "the numerator should be increased by two not three",
                "flagged_at": "t",
            },
        )
        self.assertTrue(any("equation-flag-interpret" in e for e in errors))

    def test_empty_description_rejected(self):
        errors = _MOD.validate_entry(
            "5:aaaaaaaaaaaa",
            {
                "page": 5,
                "hash": "aaaaaaaaaaaa",
                "current_latex": "x",
                "description": "",
                "flagged_at": "t",
            },
        )
        self.assertTrue(any("non-empty" in e for e in errors))

    def test_value_must_be_object(self):
        errors = _MOD.validate_entry("5:aaaaaaaaaaaa", "not a dict")
        self.assertTrue(any("must be a JSON object" in e for e in errors))

    def test_negative_page_rejected(self):
        errors = _MOD.validate_entry(
            "0:aaaaaaaaaaaa",
            {
                "page": 0,
                "hash": "aaaaaaaaaaaa",
                "current_latex": "x",
                "description": "y",
                "flagged_at": "t",
            },
        )
        self.assertTrue(any("positive int" in e for e in errors))

    def test_short_hash_rejected(self):
        errors = _MOD.validate_entry(
            "5:abcdef",
            {
                "page": 5,
                "hash": "abcdef",
                "current_latex": "x",
                "description": "y",
                "flagged_at": "t",
            },
        )
        self.assertTrue(any("12 hex chars" in e for e in errors))


class FileLevelMain(unittest.TestCase):
    """Smoke-test the CLI entry point via main() against tmpfile inputs."""

    def _write_json(self, payload):
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, dir="/tmp"
        )
        json.dump(payload, f)
        f.close()
        return Path(f.name)

    def test_main_pass_on_canonical(self):
        path = self._write_json(
            {
                "5:b4fcc24a1569": {
                    "page": 5,
                    "hash": "b4fcc24a1569",
                    "current_latex": r"\sigma",
                    "description": r"\sigma_0",
                    "flagged_at": "2026-05-16",
                }
            }
        )
        sys.argv = ["validate_flagged_schema.py", "--flagged-json", str(path)]
        rc = _MOD.main()
        self.assertEqual(rc, 0)
        path.unlink()

    def test_main_fail_on_prose(self):
        path = self._write_json(
            {
                "5:b4fcc24a1569": {
                    "page": 5,
                    "hash": "b4fcc24a1569",
                    "current_latex": "x",
                    "description": "the denominator should be 2 not 3 and that is final",
                    "flagged_at": "2026-05-16",
                }
            }
        )
        sys.argv = ["validate_flagged_schema.py", "--flagged-json", str(path)]
        rc = _MOD.main()
        self.assertEqual(rc, 1)
        path.unlink()

    def test_main_missing_file(self):
        sys.argv = [
            "validate_flagged_schema.py",
            "--flagged-json",
            "/tmp/nonexistent_xyz_12345.json",
        ]
        rc = _MOD.main()
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
