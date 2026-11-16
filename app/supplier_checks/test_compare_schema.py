"""Comparison completeness at failure-prone JSON boundaries; no supplier execution."""
import unittest

import compare_schema as comparison


class ComparisonTests(unittest.TestCase):
    def test_missing_null_false_and_integers_are_distinct(self):
        for before, after in [({}, {"x": None}), ({"x": None}, {}), (False, 0), (1, 1.0),
                              ([1, 2], [2, 1]), ({"a/b": True}, {"a/b": False})]:
            self.assertTrue(comparison.differences(before, after))
        self.assertEqual(comparison.differences({"a/b": True}, {"a/b": False})[0]["path"], "/a~1b")
        self.assertEqual(comparison.differences({"x": None}, {"x": None}), [])

    def test_references_under_all_combinators_and_cycles_are_read(self):
        doc = {"definitions": {"a": {"allOf": [{"$ref": "#/definitions/b"}]},
                               "b": {"anyOf": [{"$ref": "#/definitions/a"}]},
                               "c/d": False}, "oneOf": [{"$ref": "#/definitions/c~1d"}]}
        rows = comparison.references(doc)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[-1]["target_sha256"], comparison.digest(False))
        for ref in ["#/definitions/missing", "elsewhere.json#/a", "#/oneOf/01", "#/definitions/c~2d"]:
            with self.assertRaises(comparison.admission.Refused):
                comparison.references({**doc, "$ref": ref})
        with self.assertRaises(comparison.admission.Refused):
            comparison.references({"$dynamicRef": "#/definitions/a", **doc})

    def test_a_null_definition_is_refused_not_taken_as_missing(self):
        with self.assertRaises(comparison.admission.Refused):
            comparison.definitions({"definitions": {"a": None}}, False)
        self.assertEqual(comparison.definitions({"definitions": {"a": False}}, False), {"/definitions/a": False})

    def test_an_unread_or_repeated_method_is_not_silently_omitted(self):
        row = {"properties": {"method": {"enum": ["thread/read"]}}}
        for variants in [[row, row], [{"allOf": [row]}]]:
            with self.assertRaises(comparison.admission.Refused):
                comparison.methods({"definitions": {"ClientRequest": {"oneOf": variants}}})


if __name__ == "__main__":
    unittest.main()
