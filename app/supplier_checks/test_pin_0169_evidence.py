"""Internal completeness of the retained comparison, not a repeat qualification."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent / "version_advance"


class PinEvidence(unittest.TestCase):
    def test_every_exact_finding_has_one_authored_disposition(self):
        result = json.loads((ROOT / "0.167.0-to-0.169.0.json").read_bytes())
        decisions = json.loads((ROOT / "0.167.0-to-0.169.0.dispositions.json").read_bytes())
        findings = [row["id"] for row in result["findings"]]
        self.assertEqual(len(findings), len(set(findings)))
        self.assertEqual(sorted(findings), sorted(row["finding"] for row in decisions))
        changed = {(row["bundle"], row["pointer"]) for row in result["definitions"] if row["state"] != "unchanged"}
        found = {(row["bundle"], row["pointer"]) for row in result["findings"] if "bundle" in row}
        self.assertEqual(changed, found)
        for row in decisions:
            self.assertEqual(row["decided_by"], "App Agent 0, 2026-11-15")
            self.assertTrue(row["decision"].strip())
            self.assertTrue(all(path in result["consumer_binding"]["files"] for path in row["consumer_evidence"]))
        self.assertEqual(set(result["recorded_exchanges"]), {"st5", "nv04"})
        for case in result["recorded_exchanges"].values():
            self.assertEqual(case["0.167.0"]["methods_and_group_counts"], case["0.169.0"]["methods_and_group_counts"])


if __name__ == "__main__":
    unittest.main()
