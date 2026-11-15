#!/usr/bin/env python3
"""Checks that the committed 0.160.0 to 0.167.0 comparison is consistent with itself.

The result and its dispositions are evidence, made once by a tool that is not maintained (see
the note beside them). Nothing is regenerated and nothing is executed here: these checks read the
two files and say only what the files say. Run from `app/`:
python3 supplier_checks/test_version_advance_evidence.py
"""
import json
import unittest
from pathlib import Path

FOLDER = Path(__file__).resolve().parent / "version_advance"
RESULT = FOLDER / "0.160.0-to-0.167.0.json"
DISPOSITIONS = FOLDER / "0.160.0-to-0.167.0.dispositions.json"


def strict(path):
    def pairs(items):
        keys = [key for key, _ in items]
        if len(keys) != len(set(keys)):
            raise ValueError("a key is repeated in " + path.name)
        return dict(items)
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)


class CommittedComparison(unittest.TestCase):
    def test_the_file_says_passed_for_these_two_pins_with_no_reason_against(self):
        result = strict(RESULT)
        self.assertEqual((result["from"], result["to"]), ("0.160.0", "0.167.0"))
        self.assertEqual((result["verdict"]["verdict"], result["verdict"]["reasons"],
                          result["verdict"]["undisposed_findings"],
                          result["verdict"]["dispositions_naming_no_finding"]), ("passed", [], [], []))
        self.assertEqual(result["scenarios"], ["nv04", "st5"])

    def test_each_of_its_51_findings_is_disposed_exactly_once_by_the_authored_file(self):
        result, authored = strict(RESULT), strict(DISPOSITIONS)
        findings = [finding["id"] for finding in result["findings"]]
        self.assertEqual((len(findings), len(set(findings))), (51, 51))
        self.assertEqual(sorted(entry["finding"] for entry in authored), sorted(findings))
        for entry in authored:
            self.assertEqual(set(entry) - {"group"}, {"finding", "decided_by", "decision", "where_recorded"})
            self.assertTrue(all(isinstance(value, str) and value.strip() for value in entry.values()))

    def test_the_result_carries_the_dispositions_as_the_authored_file_has_them(self):
        key = lambda entry: entry["finding"]
        self.assertEqual(sorted(strict(RESULT)["verdict"]["dispositions"], key=key),
                         sorted(strict(DISPOSITIONS), key=key))

    def test_the_result_names_its_limits_and_every_binding_it_did_not_check(self):
        result = strict(RESULT)
        self.assertTrue(result["limits"][0].startswith("the recorded evidence at each pin is established up to"))
        unchecked = [row for row in result["identity"]["bindings"] if row["state"] != "bound"]
        self.assertEqual(len(unchecked), 7)
        self.assertTrue(all(row["state"].startswith("not checked: ") for row in unchecked))


if __name__ == "__main__":
    unittest.main()
